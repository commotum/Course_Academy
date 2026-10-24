"""Compare old/new deterministic outputs; allow only the presentation repair."""
import collections,concurrent.futures,copy,inspect,json,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from question_markers import repair_problem,validate_prompt_markers
HERE=Path(__file__).resolve().parent

def load(text,path,name):
 m=types.ModuleType(name);m.__file__=str(path.resolve());sys.modules[name]=m;exec(compile(text,str(path),'exec'),m.__dict__);return m

def semantic(q):
 q=copy.deepcopy(q);q.pop(':question/id',None)
 for f in q[':question/answer-fields']:
  f.pop(':answer-field/id',None);correct=f[':answer-field/correct'][1]
  f[':answer-field/correct']=next({k:v for k,v in a.items() if k!=':answer/id'} for a in f[':answer-field/choices'] if a[':answer/id']==correct)
  for a in f[':answer-field/choices']:a.pop(':answer/id',None)
  f[':answer-field/choices'].sort(key=lambda a:json.dumps(a,sort_keys=True))
 return q

def check(item):
 ref=item['path'];path=ROOT/ref
 if item['kind']=='fixture':return None
 if item['kind']=='package-successor':
  old=Path('/media/jake/SSD/EDB/math')/ref;path=ROOT/item['source']/old.name;before=old.read_text()
 else:before=(ROOT/item['before_file']).read_text()
 old=load(before,path,'old_'+path.stem);new=load(path.read_text(),path,'new_'+path.stem)
 levels=getattr(new,'SUPPORTED_LEVELS',None)
 if levels is None:
  levels=('easy',) if '179672' in ref else ('moderate','hard') if '147454' in ref else ('easy','moderate','hard')
 results=[]
 for level in levels:
  for seed in range(8):
   try:a=old.generate(level,seed);b=new.generate(level,seed)
   except ValueError as e:
    if 'Unsupported' in str(e) or 'unsupported' in str(e) or 'Only observed' in str(e):continue
    raise
   qa,qb=a['question'],b['question'];expected=copy.deepcopy(qa);expected[':question/problem']=repair_problem(qa[':question/problem'],qa[':question/answer-fields'])
   assert semantic(expected)==semantic(qb),(ref,level,seed,'unexpected mathematical change')
   validate_prompt_markers(qb)
   results.append({'level':level,'seed':seed,'changed':qa[':question/problem']!=qb[':question/problem'],'ids_preserved':qa[':question/id']==qb[':question/id']})
 # Cover all 38 eligible radio chain-rule parameter cases, including reported UUID.
 if '064281' in ref:
  for profile,(level,_,_,parameters) in old.PROFILES.items():
   for t in parameters:
    if not old.eligible(profile,t):continue
    a=old.generate(level,0,profile=profile,t=t);b=new.generate(level,0,profile=profile,t=t)
    expected=copy.deepcopy(a['question']);expected[':question/problem']=repair_problem(expected[':question/problem'],expected[':question/answer-fields'])
    assert expected==b['question'];validate_prompt_markers(b['question'])
    results.append({'profile':profile,'parameter':t,'changed':a['question'][':question/problem']!=b['question'][':question/problem'],'ids_preserved':True})
 assert results,ref
 return {'reference':ref,'samples':len(results),'changed':sum(r['changed'] for r in results),'identities_preserved':sum(r['ids_preserved'] for r in results),'results':results}

def main():
 changes=json.loads((HERE/'source-changes.json').read_text());results=[]
 for item in changes:
  r=check(item)
  if r:results.append(r);print(r['reference'],r['samples'],r['changed'],flush=True)
 (HERE/'generator-verification.json').write_text(json.dumps({'generators':len(results),'samples':sum(r['samples'] for r in results),'only_expected_presentation_changes':True,'results':results},indent=2)+'\n')
if __name__=='__main__':main()
