import json,sys,importlib.util,subprocess,hashlib,collections,re,shutil
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy'); E=R/'reference/edb-math/repairs/2026-10-28-implicit-intercept-scaffolding'; P=E/'package';sys.path[:0]=[str(E),str(P),str(R/'scripts')]
import math_audit as a
from generator_publish import normalized_question,jsonable
from generator_packages import build_manifest,manifest_digest
from generator_pipeline import digest

def save(n,x): (E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def load_module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=load_module('old_generator',Path('/media/jake/SSD/EDB/math/generators/04/04d24c7ca12e603e1125a2bf8982efca603e11cefe57f689c75a5af7c3aa8cde/generator.py'))
g=a.g; seed=20261028;allrows=[];observations=[];band_batches={};cases=[];paths=[]
for band in ['easy','moderate','hard']:
 rows=g.generate(band,5,seed);save('final-'+band+'.json',rows);band_batches[band]={'batch_hash':digest(rows),'count':len(rows),'seed':seed,'assets':{}}
 more=g.generate(band,12,2936070573);save('sample-'+band+'.json',more)
 before=old.generate(band,5,seed)
 if band!='easy': assert rows==before,'Untouched bands must remain byte-for-byte equivalent'
 else:
  for b,n in zip(before,rows):
   bq=normalized_question(b['question'],identity=False);nq=normalized_question(n['question'],identity=False)
   bq[':question/problem']=bq[':question/problem'].split('\n\nUse ')[0]
   assert bq==nq,'Only prompt hints may change'
 for r in rows+more:
  assert not any(token in r['question'][':question/problem'] for token in ['Use $','On the $','differentiation has been started','y-y_0','dy}{dx}'])
  observed=a.inspect(r);observations.append({'band':band,'question_id':r['question'][':question/id'],**observed})
  assert 'Differentiate implicitly' in r['question'][':question/worked-solution']
  assert 'Use the given point and this slope' in r['question'][':question/worked-solution']
  assert 'Substitute and simplify' in r['question'][':question/worked-solution']
  checks=[]
  for i,f in enumerate(r['question'][':question/answer-fields']):
   if f[':answer-field/type'].endswith('/radio'):
    for choice in f[':answer-field/choices']:
     checks.append({'field_index':i,'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if choice[':answer/id']==f[':answer-field/correct'][1] else 'rejected'})
   else:
    val=a.algebra(a.correct(f)[':answer/value']);checks += [{'field_index':i,'submitted':str(val),'expected':'accepted'},{'field_index':i,'submitted':str(val+1),'expected':'rejected'}]
  cases.append({'label':band+' '+r['question'][':question/id'],'record':r,'checks':checks})
  paths.append({'template':r['generation']['family']+' '+r['generation']['line']+' '+r['generation']['axis'],'field_key':','.join(f[':answer-field/key'] for f in r['question'][':question/answer-fields']),'final_expression':observed['final_expression'],'keyed_answer':str(observed['answer']),'domain':'Regular real quadratic; finite nonzero slope; contact point off requested axis.','conclusion':'Independent differentiation and line intersection match both keyed and displayed solution answers.','status':'passed','conversions':[],'sample_refs':['final-'+band+'.json','sample-'+band+'.json']})
 allrows+=rows+more
save('math.json',{'passed':True,'records':observations,'unchanged_moderate_hard':True,'easy_change':'Only hints removed; answers, choices, solutions, selection unchanged.'});save('grader-cases.json',cases);save('solution-paths.json',{'cases':paths})
assert g.replay()==old.replay();save('source-replay.json',g.replay());save('source-replay-check.json',{'passed':True,'complete_imported_replays':len(g.replay()),'comparison':'Exact equality to prior reviewed replay; runtime patch changes no replay logic.'})
# A controlled same-curve axis change must change the requested point; scalar equation rescaling must not.
controls=[]
for coeff,axis in [([1,0,2,0,0],'x'),([1,0,2,0,0],'y'),([2,0,4,0,0],'x')]:
 r=g.build('moderate',coeff,[3,2],axis,'diagonal');controls.append(r);a.inspect(r)
assert a.key(controls[0])!=a.key(controls[1]);assert a.key(controls[0])==a.key(controls[2]);save('counterfactuals.json',controls)
# Actual printed question 17592186711810 keeps the same answer without the hints.
for profile in g.PROFILES:
 try: r=g.build('easy',[1,0,4,0,0],[2,-4],'y','diagonal',profile=profile);break
 except ValueError:pass
assert a.key(r)==(a.s.Integer(0),-a.s.Rational(17,4));a.inspect(r);save('reported-case-clean.json',[r])
for name in ['final-easy','sample-easy']:
 result=subprocess.run([str(R/'.venv/bin/python'),str(P/'batch_regression.py'),'--input',str(E/(name+'.json'))],capture_output=True,text=True,check=True);save(name+'-bank-check.json',json.loads(result.stdout))
probes=a.probes(g.generate('easy',24,seed),'clean fresh easy');save('shortcut-probes.json',probes)
manifest=json.loads((P/'generator-package.json').read_text());manifest=build_manifest(P,'generator.py',list(manifest['files']),dependencies=manifest['dependencies']);save('package-manifest.json',manifest);save('verification-batches.json',band_batches);save('render-samples.json',[g.generate(band,1,seed)[0] for band in ['easy','moderate','hard']])
print(json.dumps({'independent_math_records':len(allrows),'native_grader_cases':len(cases),'source_replays':len(g.replay()),'package_hash':manifest_digest(manifest),'passed':True}))
