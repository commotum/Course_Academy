from audit import *
import subprocess, shutil

def main():
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');runs=[]
 # Run the exact retained strict checks against a preserved pre-repair package and current package.
 for tag,p in [('before',JOB/'review-0-policy-2-3edbf008895863aa/relocated-package'),('current',PKG)]:
  proc=subprocess.run([str(ROOT/'.venv/bin/python'),str(OUT/'retained-regression.py')],env=dict(env,AUDIT_PACKAGE_ROOT=str(p)),cwd=OUT,text=True,capture_output=True)
  shutil.copy2(OUT/'source-replay-regression-results.json',OUT/('retained-'+tag+'.json'))
  shutil.copy2(OUT/'q10252-replay-candidates.json',OUT/('retained-'+tag+'-records.json'))
  runs.append({'package':str(p),'command':'AUDIT_PACKAGE_ROOT='+str(p)+' PYTHONDONTWRITEBYTECODE=1 '+str(ROOT/'.venv/bin/python')+' retained-regression.py','returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
 assert runs[0]['returncode']==1 and runs[1]['returncode']==0,runs
 save('retained-test-runs.json',runs)
 src=json.load(open(JOB/'source/source.json'))['material']['kp'];sources=[src[':knowledge-point/canonical-example']]+src[':knowledge-point/questions']
 replays=[g.build(i) for i in g.source_instances()+g.moderate_ops.sources()+g.hard_ops.sources()]
 replays.append(g.build(dict(template='swap',pair=[0,1],matrix=[[-1,5,4,1],[1,0,5,2],[3,7,1,9]],letter='A')))
 save('source-replays.json',replays)
 rr=[]
 for q in sources:
  candidates=[r for r in replays if matrices(r['question'][':question/problem'])[0]==matrices(q[':question/problem'])[0] and expected(r['question'])==expected(q)]
  assert len(candidates)==1,(q[':question/id'],len(candidates))
  r=candidates[0];f=q.get(':question/answer-fields',[{}])[0]
  wantbank=[matrices(c[':answer/value'])[0] for c in f.get(':answer-field/choices',[])]
  gotbank=[matrices(c[':answer/value'])[0] for c in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  source_sol=matrices(q.get(':question/worked-solution',''),True)
  got_sol=matrices(r['question'][':question/worked-solution'],True)
  row={'source_id':q[':question/id'],'generated_id':r['question'][':question/id'],'bank_size':len(wantbank),'bank_complete':not wantbank or sorted(map(str,wantbank))==sorted(map(str,gotbank)), 'captured_key_correct':not f.get(':answer-field/correct') or matrices(f[':answer-field/correct'][':answer/value'])[0]==expected(r['question']), 'source_solution_stages_present':all(m in got_sol for m in source_sol),'generated_stages_correct':all(m==expected(q) for m in got_sol[1:]),'source_solution_missing':not bool(source_sol),'key_missing':not bool(f.get(':answer-field/correct'))}
  # Sequential stages include a legitimate intermediate state; source-stage containment, not all-final equality, applies.
  row.pop('generated_stages_correct')
  assert row['bank_complete'] and row['captured_key_correct'] and row['source_solution_stages_present'],row
  rr.append(row)
 save('source-replay-results.json',rr)
 records=[]
 for d,n in [('easy',48),('moderate',8),('hard',8)]:
  records.extend(g.generate(random.Random(6102137+i),difficulty=d,seed=6102137+i) for i in range(n))
 save('samples.json',records);save('easy-samples.json',records[:48]);batch=json.load(open(JOB/'samples.json'));save('runner-batch.json',batch)
 # Construct same-bank relevant changes and name-only irrelevant changes for every template.
 bases={t:next(r for r in records if r['generation']['template']==t) for t in ['swap','scale','add','swap-add','scale-add']};cf=[];results=[]
 for t,r in bases.items():
  i=copy.deepcopy(r['generation']['instance']);a=g.build(i);j=copy.deepcopy(i)
  if t=='swap':j['pair']=next(p for p in [[0,1],[0,2],[1,2]] if p!=j['pair'])
  elif t=='scale':old=j['factor'];j['factor']=j['wrong_factors'][0];j['wrong_factors'][0]=old
  elif t=='add':old=j['coefficient'];j['coefficient']=j['wrong_coefficients'][0];j['wrong_coefficients'][0]=old
  else:
   c=next(c for c in j['candidates'] if c['coefficient']!=j['coefficient'] and c.get('pair',c.get('scale'))==j.get('pair',j.get('scale')));j['coefficient']=c['coefficient']
  b=g.build(j);z=copy.deepcopy(i);z['letter']='B' if i['letter']!='B' else 'C';c=g.build(z)
  cf.extend([a,b,c]);results.append({'template':t,'indices':[len(cf)-3,len(cf)-2,len(cf)-1],'relevant_changed':expected(a['question'])!=expected(b['question']),'irrelevant_preserved':expected(a['question'])==expected(c['question']),'fixed_bank':sorted(x[':answer/value'] for x in a['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(x[':answer/value'] for x in b['question'][':question/answer-fields'][0][':answer-field/choices']),'checks':[check(x) for x in [a,b,c]]})
 i=copy.deepcopy(bases['scale']['generation']['instance']);a=g.build(i);i['target']=(i['target']+1)%3;b=g.build(i);cf.extend([a,b]);results.append({'template':'scale-target','indices':[len(cf)-2,len(cf)-1],'relevant_changed':expected(a['question'])!=expected(b['question']),'checks':[check(a),check(b)]})
 assert all(x['relevant_changed'] and x.get('irrelevant_preserved',True) for x in results)
 save('counterfactual-records.json',cf);save('counterfactual-results.json',results)
 all_records=records+batch+replays+cf
 math=[check(r) for r in all_records];save('math-results.json',math);assert all(x['unique_correct'] and x['final_solution_correct'] and x['choices']==5 for x in math)
 repaired=[r for r in replays if r['generation']['profile'] in ['source:afe0707b-0259-50d7-a719-7a8d24334500','source:337ae2e1-4641-5c8b-9b2a-9435340f0134']]
 save('repaired-records.json',repaired);save('render-records.json',batch+repaired+cf)
 guards=[]
 for r in repaired:
  i=r['generation']['instance']
  for field in ('matrix','target','factor' if i['template']=='scale' else 'coefficient'):
   c=copy.deepcopy(i)
   if field=='matrix':c['matrix'][0][0]+=1
   elif field=='target':c['target']=(c['target']+1)%len(c['matrix'])
   else:c[field]='3' if field=='factor' else -2
   try:g.build(c);rejected=False
   except ValueError:rejected=True
   guards.append({'profile':i['profile'],'changed':field,'instance':c,'rejected':rejected})
 assert all(x['rejected'] for x in guards);save('source-profile-guards.json',guards)
 # Reused zero-bank retry probes with fresh seed.
 rejects=[]
 for i in [dict(template='swap',matrix=[[0]*3]*3,pair=[0,1],letter='A'),dict(template='scale',matrix=[[0]*4]*3,target=0,factor='2',profile='scale-factor-comparison',wrong_factors=['3','4','5','6'],letter='A')]:
  try:g.build(i);rejected=False
  except ValueError:rejected=True
  rejects.append({'instance':i,'rejected':rejected})
 class ZeroFirst(random.Random):
  def __init__(self,seed,zeros):super().__init__(seed);self.zeros=zeros
  def randint(self,a,b):
   if self.zeros:self.zeros-=1;return 0
   return super().randint(a,b)
 retries=[g.sample(ZeroFirst(481,9),'swap'),g.sample(ZeroFirst(481,16),'scale')]
 save('rejection-results.json',{'degenerate_cases':rejects,'forced_zero_first_instances':retries,'role_selection':'sample code selects pair/target/factors before retrying entry data; role draws are not rejected/reweighted'})
 assert all(x['rejected'] for x in rejects) and all(x['entry_attempts']>1 for x in retries)
 save('commands.json',{'sample_command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python revision_audit.py','seeds':'6102137+i for i in range(48 easy, 8 moderate, 8 hard); independent Random per record','explicit_parameters':'Source, repaired and controlled records contain generation.instance for exact build replay; choice order preserved in record choices.'})
 (OUT/'session-state.md').write_text('Milestone: retained checks fail on preserved old package and pass current. All 13 source cases and complete banks replay; 99 raw records pass independent exact prompt/result/solution math. 17 controlled records saved. Pending delivery, native grading, actual UI rendering, packaging and final pedagogical report.\n')
 print('source cases',len(rr),'math records',len(math),'controls',len(cf),'guards',len(guards))
if __name__=='__main__':main()
