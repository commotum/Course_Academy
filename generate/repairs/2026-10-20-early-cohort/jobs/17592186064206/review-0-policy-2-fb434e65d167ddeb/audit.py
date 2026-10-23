import argparse,collections,hashlib,importlib.util,json,os,pathlib,re,shutil,subprocess,sys
sys.dont_write_bytecode=True
import sympy as S
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PYTHON=REPO/'.venv/bin/python'
def save(n,v): (ROOT/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
def module(p):
 spec=importlib.util.spec_from_file_location('review_generator',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
x=S.Symbol('x')
def expr(t):
 t=t.replace(' ','').replace('⁡','')
 t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t)
 t=re.sub(r'(\d)([xu])',r'\1*\2',t)
 return S.sympify(t,locals={'x':x,'u':S.Symbol('u')})
def parse_answer(t):
 t=t.replace('⁡','').replace(' ','').replace('\\ln','\\operatorname{ln}')
 pre,arg=re.fullmatch(r'(.*?)\\operatorname\{ln\}\|([^|]+)\|\+C',t).groups()
 return expr(pre if pre not in ('','-') else pre+'1'),expr(arg)
def field(r):return r['question'][':question/answer-fields'][0]
def key(f):
 k=f[':answer-field/correct'];return k[1] if isinstance(k,list) else k[':answer/id']
def check_math(r):
 q=r['question'];f=field(r);n,d=re.search(r'\\frac\{(-?\d+)\}\{([^}]+)\}',q[':question/problem']).groups();integrand=expr(n)/expr(d)
 tests=[]
 for a in f[':answer-field/choices']:
  c,arg=parse_answer(a[':answer/value']);delta=S.cancel(c*S.diff(arg,x)/arg-integrand);tests.append({'id':a[':answer/id'],'value':a[':answer/value'],'derivative_matches':delta==0})
 last=re.findall(r'&\s*=([^&]+?)\\end\{aligned\}',q[':question/worked-solution'])[-1].strip()
 c,arg=parse_answer(last);solution_ok=S.cancel(c*S.diff(arg,x)/arg-integrand)==0
 return {'id':q[':question/id'],'choices':tests,'solution_final_derivative_matches':solution_ok,'passed':solution_ok and sum(t['derivative_matches'] for t in tests)==1 and next(t for t in tests if t['id']==key(f))['derivative_matches']}
def probes(rs):
 groups=collections.defaultdict(list)
 for r in rs:
  f=field(r);aa=[(a,*parse_answer(a[':answer/value'])) for a in f[':answer-field/choices']]
  # Recognize bank only: identical arguments, two positive coefficients >0 and one unit positive.
  if len(set(str(a[2]) for a in aa))==1 and len([a for a in aa if a[1]>0])==3:
   picked=max(aa,key=lambda a:a[1])[0];cue='same argument, three positive coefficients: choose largest positive coefficient'
  elif len(set(str(a[2]) for a in aa))==1 and len([a for a in aa if -1<a[1]<0])==1:
   picked=next(a[0] for a in aa if -1<a[1]<0);cue='same argument, unique negative proper fraction: choose it'
  else:continue
  groups[cue].append({'id':r['question'][':question/id'],'template':r.get('generation',{}).get('template'),'picked':picked[':answer/id'],'correct':picked[':answer/id']==key(f)})
 return [{'cue':c,'correct':sum(x['correct'] for x in rows),'total':len(rows),'baseline':.2,'cases':rows} for c,rows in groups.items()]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--package',type=pathlib.Path,default=JOB/'workspace');ap.add_argument('--candidate-records',type=pathlib.Path);args=ap.parse_args()
 if args.candidate_records:
  rs=load(args.candidate_records);result={'input':str(args.candidate_records),'math':[check_math(r) for r in rs],'probes':probes(rs)};save('candidate-audit.json',result);print(json.dumps({'records':len(rs),'probes':[{k:v for k,v in p.items() if k!='cases'} for p in result['probes']]}));return
 m=module(args.package/'17592186064206.py');manifest=load(args.package/'package.json')
 save('package-hashes-before.json',{p:hashlib.sha256((args.package/p).read_bytes()).hexdigest() for p in manifest['files']})
 src=load(JOB/'source/source.json');sources=src['material']['kp'][':knowledge-point/questions']
 params={'q-15707':[2,1,1],'q-49453':[3,1,4],'q-49450':[1,1,-1],'q-49454':[1,1,3],'q-49452':[1,-3,2]}
 replays=[];replay_tests=[]
 for q in sources:
  sid=q[':question/math-academy-id']
  if sid not in params:continue
  r=m.generate(template=sid,parameters=params[sid]);replays.append(r);g=r['question'];sf=q[':question/answer-fields'][0];gf=field(r)
  replay_tests.append({'source_id':q[':question/id'],'template':sid,'prompt_exact':q[':question/problem']==g[':question/problem'],'solution_exact':q[':question/worked-solution']==g[':question/worked-solution'],'bank_exact_unordered':sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices']),'correct_exact':sf[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==key(gf))})
 save('source-replays.json',replays);save('source-replay-tests.json',replay_tests)
 rs=[m.generate(seed=i) for i in range(77201,77261)]
 bounds={'q-15707':[[2,1,1],[9,1,12]],'q-49453':[[2,1,1],[9,1,12]],'q-49450':[[1,1,-1],[1,1,-12]],'q-49454':[[1,1,2],[1,1,12]],'q-49452':[[1,-2,1],[1,-9,12]]}
 for sid,ps in bounds.items():
  rs.extend(m.generate(seed=809,template=sid,parameters=p) for p in ps)
 cf=[m.generate(seed=912,template='q-15707',parameters=p) for p in [[2,1,7],[3,1,7]]]+[m.generate(seed=912,template='q-49453',parameters=[2,1,7])]
 save('counterfactual-records.json',cf);save('independent-samples.json',rs);batch=load(JOB/'samples.json');save('runner-batch.json',batch)
 save('math-results.json',[check_math(r) for r in replays+rs+batch+cf])
 save('raw-probes.json',{'independent':probes(rs),'batch':probes(batch)})
 cases=[]
 for label,records in [('replay',replays),('boundary',rs[-10:]),('batch',batch),('counterfactual',cf)]:
  for r in records:
   f=field(r);truth=check_math(r);truth={a['id']:a['derivative_matches'] for a in truth['choices']}
   cases.append({'label':label+' '+r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if truth[a[':answer/id']] else 'rejected','purpose':'independent derivative calculation'} for a in f[':answer-field/choices']]})
 save('grader-input.json',cases)
 rejects=[]
 for sid,p in [('q-49511',[2,3,5]),('q-15707',[3,5,2]),('q-15707',[1,1,7]),('q-15707',[-2,1,7]),('q-49452',[1,0,2]),('q-49454',[1,1,1]),('q-15707',[2.0,1,7])]:
  try:m.generate(template=sid,parameters=p);outcome='accepted'
  except Exception as e:outcome=f'{type(e).__name__}: {e}'
  rejects.append({'template':sid,'parameters':p,'outcome':outcome})
 save('rejections.json',rejects)
 dest=ROOT/'relocated';dest.mkdir(exist_ok=True);shutil.copy2(args.package/'17592186064206.py',dest/'17592186064206.py');(dest/'17592186064206').mkdir(exist_ok=True);shutil.copy2(args.package/'17592186064206/contract.json',dest/'17592186064206/contract.json')
 cmd=[str(PYTHON),str(dest/'17592186064206.py'),'--seed','994860459','--count','5','--difficulty','easy'];run=subprocess.run(cmd,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},cwd=ROOT)
 relocated=json.loads(run.stdout);save('relocated-batch.json',relocated)
 save('packaging.json',{'command':cmd,'python':sys.version.split()[0],'sympy':S.__version__,'manifest_dependencies':manifest['dependencies'],'relocation_matches_batch':relocated==batch,'deterministic_replay':m.batch('easy',5,994860459)==batch,'declared_runtime_imports':['stdlib','sympy'],'external_output':'stdout JSON only; no assets','history_exists':(JOB/'repair-history.json').exists(),'preflight_exists':(JOB/'repair-preflight.json').exists()})
 inv=load(JOB/'source/inventory.json');save('inventory-analysis.json',{'basis':inv['basis'],'questions':[{'id':q[':question/id'],'entity_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'generated':any('generation' in k or 'generated' in k for k in q),'retired':q.get(':question/retired',False),'has_key':all(':answer-field/correct' in f for f in q[':question/answer-fields'])} for q in inv['questions']],'conclusion':'All six captured questions are original source records, none are generated records. q-49511 has no key and fails fresh practice validation. No eligible generated historical record exists in captured inventory; original sources must not be relabeled.'});save('affected-inventory.json',{'affected_questions':[]})
 save('render-records.json',batch+cf+[rs[-1]])
 print(json.dumps({'replays':len(replays),'samples':len(rs),'math_failures':sum(not t['passed'] for t in load(ROOT/'math-results.json')),'batch_profiles':dict(collections.Counter(r['generation']['profile'] for r in batch)),'probes':[{k:v for k,v in p.items() if k!='cases'} for p in probes(rs)]}))
if __name__=='__main__':main()
