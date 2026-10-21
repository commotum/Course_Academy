"""Focused repair validation; run from any working directory using job Python."""
import collections,hashlib,json,pathlib,platform,re,shutil,subprocess,sys,tempfile
sys.dont_write_bytecode=True
from repair_regression import g,records,probe,ROOT
from visible_math import check_record,expr,resolved,same,sep
REPO=pathlib.Path('/home/jake/Developer/Course_Academy');E=ROOT/'evidence';JOB=ROOT.parent
load=lambda p:json.loads(p.read_text())
def save(n,v):(E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def key(r):
 f=r['question'][':question/answer-fields'][0]
 return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
def norm(s):return re.sub(r'\s','',s.replace(r'\left','').replace(r'\right',''))
def cues(rs):
 out={}
 for r in rs:
  t=r['generation']['template'];f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];ki=next(i for i,c in enumerate(cs) if c[':answer/id']==f[':answer-field/correct'][1]);v=[c[':answer/value'] for c in cs]
  row=out.setdefault(t,{'count':0,'positions':[0]*5,'first':0,'last':0,'shortest':0,'longest':0,'unique_fractionless':0,'unique_min_fractions':0,'unique_max_fractions':0,'profiles':collections.Counter(),'semantic_odes':set()})
  row['count']+=1;row['positions'][ki]+=1;row['first']+=ki==0;row['last']+=ki==4
  row['shortest']+=ki==min(range(5),key=lambda i:len(v[i]));row['longest']+=ki==max(range(5),key=lambda i:len(v[i]))
  ns=[z.replace(g.D,'D').count(r'\frac') for z in v]
  row['unique_fractionless']+=sum(n==0 for n in ns)==1 and ns[ki]==0
  row['unique_min_fractions']+=ns.count(min(ns))==1 and ns[ki]==min(ns)
  row['unique_max_fractions']+=ns.count(max(ns))==1 and ns[ki]==max(ns)
  row['profiles'][r['generation'].get('bank_profile','observed')]+=1
  # Semantic count comes from parsing the visible ODE, not seeds or IDs.
  row['semantic_odes'].add(str(resolved(re.findall(r'\$\$(.*?)\$\$',r['question'][':question/problem'],re.S)[0])))
 for v in out.values():v['semantic_odes']=len(v['semantic_odes'])
 return out

def main():
 sources=[];fidelity=[]
 for q in load(JOB/'source/source.json')['material']['kp'][':knowledge-point/questions']:
  sid=q[':question/math-academy-id'];t=next(t for t,d in g.TEMPLATES.items() if d[1]==sid);level,_,p=g.TEMPLATES[t]
  r=g.generate(level,8931,t,parameters=p,profile='observed');a=r['question'];f=a[':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
  tests={'prompt':norm(a[':question/problem'])==norm(q[':question/problem']),'solution':norm(a[':question/worked-solution'])==norm(q[':question/worked-solution']),'bank':sorted(norm(c[':answer/value']) for c in f[':answer-field/choices'])==sorted(norm(c[':answer/value']) for c in sf[':answer-field/choices']),'key':norm(key(r))==norm(sf[':answer-field/correct'][':answer/value'])}
  assert all(tests.values()),(sid,tests)
  sources.append(r);fidelity.append({'source_id':q[':question/id'],**tests})
 save('source-replay.json',{'passed':True,'complete_banks':len(sources),'choices':5*len(sources),'cases':fidelity});save('source-replay-records.json',sources)
 rs=records()
 for t,(level,s,p) in g.TEMPLATES.items():
  if t in ('simple_quotient','exp_quotient'):continue
  for seed in (31,49,73,97) if level=='easy' else (31,):rs.append(g.generate(level,seed,t))
 # Replay the entire old batch from generation metadata; changed banks receive fresh content IDs.
 old=load(JOB/'samples.json');batch=[g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile']) for r in old]
 save('replacement-batch.json',batch)
 pairs=[];counter=[]
 for t in ('simple_quotient','exp_quotient'):
  p={'n':1} if t=='simple_quotient' else {'n':1,'base':4,'a':3}
  before=g.generate_easy(17,t,parameters=p);after=g.generate_easy(17,t,parameters={**p,'n':4});irrelevant=g.generate_easy(19,t,parameters=p)
  assert key(before)!=key(after) and before['question'][':question/problem']!=after['question'][':question/problem'] and before['question'][':question/worked-solution']!=after['question'][':question/worked-solution']
  assert key(before)==key(irrelevant) and before['question'][':question/problem']==irrelevant['question'][':question/problem'] and before['question'][':question/worked-solution']==irrelevant['question'][':question/worked-solution']
  assert same(resolved(key(before)),resolved(key(irrelevant)))
  pairs += [before,after,irrelevant];counter.append({'template':t,'key_before':key(before),'key_after':key(after),'key_after_irrelevant_seed_change':key(irrelevant),'passed':True})
 save('counterfactual-records.json',pairs);save('counterfactual-results.json',counter)
 allrs=rs+sources+batch+pairs;math=[check_record(r) for r in allrs];assert all(v['passed'] for v in math)
 save('math-results.json',{'passed':True,'count':len(math),'cases':math});save('test-records.json',allrs)
 grader=[]
 for i,r in enumerate(allrs):
  f=r['question'][':question/answer-fields'][0];k=f[':answer-field/correct'][1]
  grader.append({'label':str(i)+'/'+r['generation']['template'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==k else 'rejected','purpose':'Independently parsed equivalent separated equation' if c[':answer/id']==k else 'Independently parsed wrong or unseparated equation'} for c in f[':answer-field/choices']]})
 save('grader-input.json',grader)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-report.json')],check=True,capture_output=True,text=True)
 easy=[r for r in rs if r['question'][':question/difficulty']==':question.difficulty/easy'];save('delivery-input.json',easy)
 inv=load(JOB/'source/inventory.json');rows=[];affected=[]
 for q in inv['questions']:
  f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];candidate=[c for c in choices if r'\frac' not in c[':answer/value'].replace(g.D,'D')];k=f[':answer-field/correct'][':answer/id'];hit=len(candidate)==1 and candidate[0][':answer/id']==k;source=':question/math-academy-id' in q
  rows.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'is_source':source,'shortcut_success':hit})
  assert source or not hit, 'Affected generated inventory requires full matching reproduction'
 save('inventory-probe.json',{'basis':inv['basis'],'tested':rows,'generated_tested':sum(not r['is_source'] for r in rows),'generated_affected':0,'limits':'All six captured generated records tested for this specific visible cue; not a claim about uncaptured inventory or other defects.'})
 save('affected-inventory.json',{'affected_questions':affected})
 save('shortcut-before-delivery.json',cues(easy))
 # Both revised profiles/families plus replacement batch member, not interchangeable render repetition.
 render=[]
 for t in ('simple_quotient','exp_quotient'):
  for prof in ('quotient-power-ladder-exchange','quotient-power-ladder-independent'):
   render.append(next(r for r in rs if r['generation']['template']==t and r['generation']['bank_profile']==prof))
 render.append(next(r for r in rs if r['generation']['template']=='sqrt_quotient'))
 save('render-records.json',render)
 import sympy
 manifest=load(ROOT/'package.json');missing=[n for n in manifest['files'] if not (ROOT/n).is_file()];assert not missing
 with tempfile.TemporaryDirectory(dir=E) as temp:
  td=pathlib.Path(temp)
  for n in manifest['files']:
   dest=td/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,dest)
  cmd=[sys.executable,str(td/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','17','--format','json']
  relocated=json.loads(subprocess.check_output(cmd,text=True,cwd=td))
  assert relocated==[g.generate_easy(17+i) for i in range(5)]
 save('packaging.json',{'passed':True,'python':platform.python_version(),'sympy':sympy.__version__,'relocated_count':5,'declared_runtime_files':manifest['files']})
 print(json.dumps({'source_banks':len(sources),'math_records':len(math),'native_choices':len(math)*5,'easy_delivery_input':len(easy),'replacement_batch':len(batch),'inventory_generated_tested':6}))
if __name__=='__main__':main()
