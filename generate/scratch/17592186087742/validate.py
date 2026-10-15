"""Independent displayed bank algebra, source replay and actual learner grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('circle_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
LEVELS=g.LEVELS;GENERATOR_UUID=g.GENERATOR_UUID

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def fingerprint(q):
 r=g.radius_from_prompt(q[':question/problem']);oriented='counterclockwise' in q[':question/problem']
 return g.digest({'radius':str(r),'task':'oriented'if oriented else'recognition'})
def as_record(q):
 q=copy.deepcopy(q);q[':question/id']=str(q[':question/id']);q[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);fs=[]
 for f in q[':question/answer-fields']:
  fs.append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']}for a in f[':answer-field/choices']]})
 q[':question/answer-fields']=fs
 q={k:q[k]for k in (':question/id',':question/difficulty',':question/problem',':question/worked-solution',':question/answer-fields')}
 return {'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':q,'generation':{'template':'existing'}}
def math_value(s):
 s=s.replace('⁡','').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin')
 fn='cos'if r'\cos'in s else'sin';co=s.split('\\'+fn)[0].strip();co=g.parse_value('x='+s+',y='+s)[0][0]
 return co,fn

def check_math(rec):
 q=rec['question'];r=g.radius_from_prompt(q[':question/problem']);theta=sp.Symbol('t',real=True)
 assert r>0 and ':question/worked-solution'in q and '{{'not in q[':question/worked-solution']
 # Read the final displayed solution equation independently from the answer key.
 equations=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);last=equations[-1]
 match=re.search(r'x=(.*?),\\,y=(.*?),\\,',last);assert match,last
 solution=g.parse_value('x='+match[1]+',y='+match[2]);assert solution==[(r,'cos',0),(r,'sin',0)],solution
 keys=[f[':answer-field/key']for f in q[':question/answer-fields']]
 if keys!=['selection']:
  assert set(keys)=={'field-1','field-2'}
  assert all('{{'+key+'}}'in q[':question/problem']for key in keys)
 for f in q[':question/answer-fields']:
  correct=f[':answer-field/correct'][1];answers=f[':answer-field/choices'];assert len({a[':answer/id']for a in answers})==len(answers)
  assert sum(a[':answer/id']==correct for a in answers)==1
  if f[':answer-field/type'].endswith('/radio'):
   assert len(answers)==5;objects=[];truth=[]
   for a in answers:
    xy=g.parse_value(a[':answer/value']);es=[amp*(sp.cos(theta)if fn=='cos'else sp.sin(theta))+h for amp,fn,h in xy]
    objects.append(tuple(es));on=sp.trigsimp(es[0]**2+es[1]**2-r*r)==0
    oriented='counterclockwise'in q[':question/problem'];good=bool(on)
    if oriented:
     cross=sp.trigsimp(es[0]*sp.diff(es[1],theta)-es[1]*sp.diff(es[0],theta));good=good and sp.simplify(es[0].subs(theta,0)-r)==0 and es[1].subs(theta,0)==0 and cross>0
    truth.append(bool(good));assert bool(good)==(a[':answer/id']==correct),(a[':answer/value'],r)
   assert len(set(objects))==5 and sum(truth)==1
  else:
   fn='cos'if f[':answer-field/key']=='field-1'else'sin'
   assert all(math_value(a[':answer/value'])==(r,fn)for a in answers)
 return fingerprint(q)
def check(rec):
 assert rec['knowledge_point']['db_id']==g.KP_ID
 assert check_math(rec)==rec['generation']['task_fingerprint']
 gen=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1]
 replay=g.generate(level,gen['seed'],template=gen['template'],parameters=gen['parameters'])
 # Output assets may have been published; the underlying PNG bytes and math stay identical.
 def normalized(r):
  r=copy.deepcopy(r);r['question'][':question/problem']=re.sub(r'!\[\]\(.*?\)','{{circle}}',r['question'][':question/problem']);r['generation']['assets']=[];return r
 assert normalized(rec)==normalized(replay),'Instance replay mismatch'
 return fingerprint(q)
def native(rec,label=None):
 checks=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  ci=f[':answer-field/correct'][1];c=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==ci)
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==ci else'rejected','purpose':'mathematically verified source bank'}for a in f[':answer-field/choices'])
  else:
   checks.extend([{'field_index':i,'submitted':c,'expected':'accepted','purpose':'canonical RHS fragment'},{'field_index':i,'submitted':'('+c+')','expected':'accepted','purpose':'equivalent grouped expression'},{'field_index':i,'submitted':'('+c+')+1','expected':'rejected','purpose':'incorrect translated fragment'}])
 return {'label':label or rec['question'][':question/id'],'record':rec,'checks':checks}
def main():
 replays=[];components=[];fixtures=[];reviews=[];coverage={};errors=[];total=matched=0;complete=0
 for sid,q in g.ORIGINALS.items():
  r=sp.Rational(g.RADII[sid]);assert g.radius_from_prompt(q[':question/problem'])==r
  info={'source':sid,'radius':str(r),'level':g.level_of(sid),'profile':'bank-'+sid if sid in g.PROFILES else None,'source_fields':q[':question/answer-fields'],'source_prompt':q[':question/problem'],'source_solution':q.get(':question/worked-solution'),'components':[]}
  if sid in g.PROFILES:
   expected=g.bank(sid,r);actual=[]
   for f in q[':question/answer-fields']:
    for a in f[':answer-field/choices']:
     value=a[':answer/value'];corrected=value
     if sid=='q-6896'and '3,5'in value:
      corrected=value.replace('3,5','3.5');errors.append({'source':sid,'answer':a[':answer/id'],'original':value,'supported_correction':corrected,'evidence':'Other component is 3.5, r=7, complete shared profile is r/2 in both coordinates; original malformed component is excluded from counts.'})
     xy=g.parse_value(corrected);actual.append(xy);total+=1
     matches=[]
     for index,(a1,b1,swap,h,k)in enumerate(expected):
      if xy==[(a1,'sin'if swap else'cos',h),(b1,'cos'if swap else'sin',k)]:matches.append(index)
     assert len(matches)==1,(sid,corrected,matches);matched+=1
     info['components'].append({'source_answer':a[':answer/id'],'original':value,'complete_recipe':[str(z)for z in g.PROFILES[sid][matches[0]]],'reproduced_at_source':True,'correction':corrected if corrected!=value else None})
   assert len(actual)==len(expected)==5;complete+=1
  if sid not in g.INCOMPLETE:
   rec=g.generate(g.level_of(sid),template=sid,parameters={'radius':str(r)});check(rec)
   strip=lambda s:re.sub(r'!\[\]\(.*?\)','{{circle}}',s)
   assert strip(rec['question'][':question/problem'])==strip(q[':question/problem'])
   assert rec['question'][':question/worked-solution']==q[':question/worked-solution']
   if sid in g.PROFILES:
    generated=[g.parse_value(a[':answer/value'])for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]
    assert sorted(map(str,generated))==sorted(map(str,actual))
    original_correct=g.parse_value(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']);assert original_correct==[(r,'cos',0),(r,'sin',0)]
   else:assert check_math(as_record(q))
   fixtures.append(native(rec,'source-'+sid));replays.append(rec)
   seen=set()
   for n in range(16):
    variant=g.generate(g.level_of(sid),n,template=sid);check(variant);fixtures.append(native(variant,sid+'-'+str(n)));seen.add(variant['generation']['parameters']['radius'])
    if n<2:reviews.append({'original':q,'variant':variant})
   coverage[sid]={'sampled_radii':sorted(seen),'cases':16,'fixed_slots':['center=(0,0)','theta in [0,2pi)','one traversal','start=(r,0) and CCW for moderate'],'variable_slots':['positive radius'],'unseen_eligible_positions':[]}
  else:info['status']='Evidence-only missing difficulty, solution, correct designation; all five bank values replayed, excluded from inventory'
  components.append(info)
 # Explicit lower/upper radius and rational workloads; reject every unsupported band.
 for level,sid,rs in [('easy','q-105915',['1/5','30']),('easy','q-6877',['2']),('moderate','q-321890',['2','30'])]:
  for r in rs:
   rec=g.generate(level,template=sid,parameters={'radius':r});check(rec);fixtures.append(native(rec,'boundary-'+level+r))
 for level,p in [('hard',{'radius':'7'}),('moderate',{'radius':'1/2'}),('easy',{'radius':'0'}),('easy',{'radius':'31'})]:
  try:g.generate(level,parameters=p);raise AssertionError('Invalid level/domain admitted')
  except ValueError:pass
 # Radius change, with the exact same template; inspect prompt, final solution, keys and plot.
 controlled=[g.generate('moderate',template='q-321890',parameters={'radius':r})for r in ('11','13')]
 for rec in controlled:check(rec)
 assert controlled[0]['generation']['task_fingerprint']!=controlled[1]['generation']['task_fingerprint']
 a=g.generate('easy',seed=1,template='q-105915',parameters={'radius':'11'});b=g.generate('easy',seed=99,template='q-105915',parameters={'radius':'11'});assert a['question'][':question/id']==b['question'][':question/id']
 # Exercise the exact scheduler CLI contract and distinct batch semantics.
 for level in LEVELS:
  out=subprocess.run([sys.executable,str(HERE.with_suffix('.py')),'--difficulty',level,'--count','5','--seed','88','--format','json'],capture_output=True,text=True,check=True)
  batch=json.loads(out.stdout);assert isinstance(batch,list)and len(batch)==5
  assert len({fingerprint(r['question'])for r in batch})==5
  for rec in batch:check(rec);fixtures.append(native(rec,'scheduler-cli-'+level+rec['question'][':question/id']))
 save(HERE/'engine-input.json',fixtures);subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 save(HERE/'source-replay.json',replays);save(HERE/'components.json',components);save(HERE/'source-errors.json',errors);save(HERE/'review.json',reviews);save(HERE/'controlled-radius-review.json',controlled)
 (HERE/'review.md').write_text('\n\n---\n\n'.join('Original '+x['original'][':question/math-academy-id']+'\n\n'+x['original'][':question/problem']+'\n\n'+x['original'][':question/worked-solution']+'\n\nVariant\n\n'+g.markdown(x['variant'])for x in reviews))
 result={'status':'passed','generator_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(Path(__file__)),'source_basis':g.SNAP['basis'],'source_count':len(g.ORIGINALS),'supported_levels':list(LEVELS),'unsupported_levels':['hard'],'complete_source_banks_matched':complete,'complete_source_banks_total':len(g.PROFILES),'source_choice_values_matched':matched,'source_choice_values_total':total,'source_errors':errors,'missing_fields_preserved':sorted(g.INCOMPLETE),'source_solutions_replayed':len(replays),'slot_coverage':coverage,'native_records':len(fixtures),'native_report':'engine-report.json','native_binary_sha256':sha(HERE/'check-engine'),'engine_library_sha256':sha(HERE.parents[2]/'target/release/deps/libcourse_academy_engine-db2f80585ab00950.rlib'),'unresolved_comparisons':[]}
 save(HERE/'validation.json',result);print(json.dumps({k:result[k]for k in ('status','complete_source_banks_matched','source_choice_values_matched','native_records')}))
if __name__=='__main__':main()
