"""Affected-profile counterfactuals, shortcut probes, grader fixtures and small regression sample."""
import collections, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
from source_regression import ROOT, g, save, source_regression, check, system, triple

def metrics(records):
 groups=collections.defaultdict(list)
 for r in records:groups[r['generation']['source_profile']].append(r)
 result={}
 for profile,rs in groups.items():
  rows=[]
  for r in rs:
   f=r['question'][':question/answer-fields'][0];vs=[tuple(triple(c[':answer/value'])) for c in f[':answer-field/choices']];key=next(i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==f[':answer-field/correct'][1]);major=tuple(collections.Counter(v[j] for v in vs).most_common(1)[0][0] for j in range(3));pred={'lex_min':vs.index(min(vs)),'lex_max':vs.index(max(vs)),'coordinate_majority':vs.index(major) if major in vs else 0}
   pred.update({f'position_{i+1}':i for i in range(5)});rows.append((key,pred,tuple(check(r))))
  result[profile]={'count':len(rs),'distinct_solutions':len(set(x[2] for x in rows)),'correct_positions':dict(collections.Counter(str(x[0]+1) for x in rows)),'cues':{k:{'successes':sum(key==p[k] for key,p,_ in rows),'attempts':len(rows),'chance_baseline':0.2} for k in rows[0][1]},'masks':sorted({str(r['generation']['instance']['parameters'].get('mask')) for r in rs})}
 return result

def prepare():
 replays=source_regression();profiles=['q-20598','q-20589','q-20594','q-20591','q-131586'];controlled=[];pairs=[];pairreport=[]
 base={'role':0,'mask':[1,1,1],'coefficients':[2,-3,1],'translation':[0,0,0],'scale':1}
 for profile in profiles:
  for role in range(5):
   mask=g.MASKS[role%4];p=dict(base,role=role,mask=list(mask),coefficients=[(-5 if (role+j)%2 else 5) if a else 0 for j,a in enumerate(mask)],translation=[-5,0,5] if role%2 else [5,-5,0],scale=1+role%2)
   controlled.append(g.generate(seed=731,template=profile,parameters=p))
 for profile in ['q-20598','q-20589','q-20591']:
  before=g.generate(seed=731,template=profile,parameters=base);relevant=g.generate(seed=731,template=profile,parameters=dict(base,role=1));irrelevant=g.generate(seed=731,template=profile,parameters=dict(base,coefficients=[-2,3,-1]));a,b,c=map(check,[before,relevant,irrelevant]);assert a!=b and a==c
  fields=[r['question'][':question/answer-fields'][0] for r in [before,relevant,irrelevant]]
  banks=[{c[':answer/value'] for c in f[':answer-field/choices']} for f in fields];assert banks[0]==banks[1]==banks[2]
  assert len({json.dumps(system(r['question'][':question/problem'])) for r in [before,relevant,irrelevant]})==3
  pairs.extend([before,relevant,irrelevant]);pairreport.append({'profile':profile,'base':base,'relevant_change':{'role':1},'irrelevant_change':{'coefficients':[-2,3,-1]},'independent_solutions':[a,b,c],'same_bank':True,'passed':True})
 raw=g.batch('easy',5,862901)
 records=replays+[r for r in controlled]+pairs+raw
 results=[{'id':r['question'][':question/id'],'profile':r['generation']['source_profile'],'solution':check(r)} for r in records]
 save('controlled-records.json',controlled);save('counterfactual-records.json',pairs);save('counterfactual-results.json',pairreport);save('sample-records.json',raw);save('math-results.json',{'checked':len(results),'failures':[],'records':results})
 save('delivery-input.json',controlled+pairs+raw)
 cases=[]
 for i,r in enumerate(records):
  if not r['question'][':question/answer-fields']:continue
  target=check(r);f=r['question'][':question/answer-fields'][0];cases.append({'label':str(i)+' '+r['generation']['source_profile'],'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if triple(c[':answer/value'])==target else 'rejected','purpose':'Independent Fraction elimination of visible equations and substitution of complete choice'} for c in f[':answer-field/choices']]})
 save('grader-input.json',cases)
 save('render-records.json',[next(r for r in replays if r['generation']['source_profile']==p) for p in ['q-20598','q-20589','e-4709']]+[pairs[0],pairs[1],pairs[3],pairs[4],pairs[6]])
 manifest=json.loads((ROOT/'package.json').read_text());assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':g.sp.__version__}}
 for path in manifest['files']:assert (ROOT/path).is_file()
 with tempfile.TemporaryDirectory(dir=ROOT/'evidence') as tmp:
  dest=Path(tmp)
  for path in manifest['files']:shutil.copy2(ROOT/path,dest/path)
  cmd=[sys.executable,'-B','generator.py','--difficulty','easy','--count','5','--seed','862901','--format','json']
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(dest/'assets'))
  result=subprocess.run(cmd,cwd=dest,env=env,text=True,capture_output=True,check=True);assert json.loads(result.stdout)==raw
 assert g.batch('easy',5,862901)==raw
 save('packaging.json',{'determinism':True,'relocation':True,'dependencies_verified':manifest['dependencies'],'runtime_files':manifest['files']})
 save('shortcut-before.json',metrics(controlled))
 for profile,report in metrics(controlled).items():
  assert report['distinct_solutions']==5 and len(report['masks'])==4
  assert all(v['successes']<v['attempts'] for v in report['cues'].values()),profile
 print(json.dumps({'math_records':len(records),'grader_records':len(cases),'grader_responses':5*len(cases),'controlled_profiles':profiles,'render_records':8}))

def after():
 accepted=json.loads((ROOT/'evidence/delivery/accepted.json').read_text());raw=json.loads((ROOT/'evidence/delivery-input.json').read_text());controlled=json.loads((ROOT/'evidence/controlled-records.json').read_text());ids={r['generation']['semantic_hash'] for r in controlled};filtered=[r for r in accepted if r['generation']['semantic_hash'] in ids]
 for r in accepted:check(r)
 before=metrics(controlled);got=metrics(filtered);assert set(got)==set(before)
 for profile,report in got.items():
  assert report['distinct_solutions']==5 and len(report['masks'])==4
  assert all(v['successes']<v['attempts'] for v in report['cues'].values()),profile
 save('shortcut-after.json',got);save('pedagogical-variation.json',{'input_count':len(raw),'delivered_count':len(accepted),'controlled_before':before,'controlled_after':got,'counterfactual_results':'counterfactual-results.json','limits':['Tests cover restored profiles plus one existing profile per representation; prior review covered all twelve existing profiles.','No live learner history, allocation IDs or weighted selection available.','Recognizing the displayed final z is valid partial elimination; uniqueness of z is not classified as an incidental cue.','No claim that finite probes exclude every possible shortcut.']})
 print(json.dumps({'delivered':len(accepted),'controlled_survivors':len(filtered),'shortcut_failures':[]}))
if __name__=='__main__':after() if '--after' in sys.argv else prepare()
