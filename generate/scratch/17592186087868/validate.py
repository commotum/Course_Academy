"""Replay all banks; independently normalize displayed ODEs and grade every field."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('ode_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def fingerprint(q):return g.fingerprint(q)
def value(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def independent(r):
 q=r['question'];equations=g.prompt_equations(q);target='inhomogeneous' in q[':question/problem'].splitlines()[0]
 fields=q[':question/answer-fields'];assert [f[':answer-field/key'] for f in fields]==['I','II','III']
 keys=[]
 for f,(key,(p,forcing)) in zip(fields,equations):
  assert sp.Poly(p,g.X) is not None and sp.Poly(forcing,g.X) is not None
  homogeneous=sp.simplify(forcing)==0;expected=(not homogeneous) if target else homogeneous
  assert value(f)==str(expected).lower()
  assert f[':answer-field/type']==':answer-field.type/checkbox'
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
  assert all(a[':answer/type']==':answer.type/text' for a in f[':answer-field/choices'])
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==2
  keys.append((sp.srepr(p),sp.srepr(forcing)))
 # Every numeric y-prime equation in every aligned solution line must normalize
 # to one prompt equation. Each final collected equation remains equivalent.
 solution=q[':question/worked-solution'];checked=0
 for m in re.findall(r'\$\$([\s\S]*?)\$\$',solution):
  clean=m.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  for line in clean.split(r'\\'):
   if '{y}^{′}' not in line or 'P(x)' in line:continue
   p,forcing=g.equation(line.strip());assert (sp.srepr(p),sp.srepr(forcing)) in keys,line
   checked+=1
 assert checked>=3
 selected=[f[':answer-field/key'] for f in fields if value(f)=='true']
 expected={'I,II,III':'I, II and III.','I,II':'I and II only.','I,III':'I and III only.','II,III':'II and III only.','I':'I only.','II':'II only.','III':'III only.'}[','.join(selected)]
 assert solution.endswith('Therefore, the correct answer is "'+expected+'"')
 for text in [q[':question/problem'],solution]:assert text.count('$')%2==0 and text.count('{')==text.count('}')
 assert r['generation']['mathematical_key']==fingerprint(q)
 assert r==g.generate(g.level(q),r['generation']['seed'],template=r['generation']['template'],k=r['generation']['parameters']['k'])
 assert ':question/math-academy-id' not in q
 return checked
check=independent
def checks(r):
 independent(r);out=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:out.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Authored boolean checkbox choice'})
 return out
def engine_item(label,r):return {'label':label,'record':r,'checks':checks(r)}
def main():
 records=[];replays=[];complete=0;options=0;equation_checks=0
 for mid,src in g.SOURCES.items():
  level=g.level(src);r=g.generate(level,0,template=mid,k=1);q=r['question']
  assert q[':question/problem']==src[':question/problem'] and q[':question/worked-solution']==src[':question/worked-solution']
  for f,sf in zip(q[':question/answer-fields'],sorted(src[':question/answer-fields'],key=lambda f:['I','II','III'].index(f[':answer-field/key']))):
   assert f[':answer-field/key']==sf[':answer-field/key']
   assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in sf[':answer-field/choices'])
   assert value(f)==sf[':answer-field/correct'][':answer/value'];complete+=1;options+=2
  replays.append({'source':mid,'fields':3,'matched_options':6,'complete_banks':3,'missing':[],'extra':[],'markdown_exact':True})
  for k in g.DOMAIN:
   r=g.generate(level,76,template=mid,k=k);equation_checks+=independent(r);records.append(r)
 negative=0
 for difficulty in ['hard','invalid']:
  try:g.generate(difficulty)
  except ValueError:negative+=1
  else:raise AssertionError('Unsupported level accepted')
 for k in [0,7,-1,True,1.5]:
  try:g.generate('easy',k=k)
  except ValueError:negative+=1
  else:raise AssertionError('Unsupported degree multiplier')
 for difficulty in g.SUPPORTED_LEVELS:
  rows=g.candidates(difficulty,5);assert len({fingerprint(r['question']) for r in rows})==len(rows)
  for r in rows:assert r['question']==g.generate(difficulty,6,template=r['generation']['template'],k=r['generation']['parameters']['k'])['question']
  try:g.batch(difficulty,len(rows)+1,0)
  except ValueError:negative+=1
  else:raise AssertionError('Finite limit not enforced')
 corrupted=copy.deepcopy(records[0]);f=corrupted['question'][':question/answer-fields'][0];f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])]
 try:independent(corrupted)
 except AssertionError:negative+=1
 else:raise AssertionError('Wrong selection accepted')
 (H/'engine-input.json').write_text(json.dumps([engine_item(str(i),r) for i,r in enumerate(records)],indent=2))
 subprocess.run([str(H/'check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 report=json.loads((H/'engine-report.json').read_text());assert report['documented_unresolved_checks']==0
 (H/'source-bank-replay.json').write_text(json.dumps(replays,indent=2))
 (H/'review.md').write_text('\n\n---\n\n'.join('## '+mid+' original\n\n'+g.markdown(g.generate(g.level(src),0,template=mid,k=1))+'\n\n## Degree variant\n\n'+g.markdown(g.generate(g.level(src),0,template=mid,k=2)) for mid,src in g.SOURCES.items()))
 result={'status':'pass','passed':True,'source_basis':g.SOURCE['basis'],'supported_levels':list(g.SUPPORTED_LEVELS),'exhaustive_instances':len(records),'displayed_equation_checks':equation_checks,'source_complete_banks':{'matched':complete,'total':complete},'source_options':{'matched':options,'total':options},'source_markdown_exact':len(replays),'distinct_tasks':{l:len(g.candidates(l)) for l in g.SUPPORTED_LEVELS},'negative_controls':negative,'grading':{k:report[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [H.with_suffix('.py'),Path(__file__),H/'source.json',H/'source.edn',H/'check-engine',H/'capabilities.json']}}
 (H/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
