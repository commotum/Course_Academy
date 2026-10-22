import sys
sys.dont_write_bytecode=True
import pathlib,json,re,random,subprocess,hashlib,shutil,platform
from fractions import Fraction
from math import isqrt
from collections import Counter,defaultdict
E=pathlib.Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy');PY=str(REPO/'.venv/bin/python')
sys.path.insert(0,str(W));import generator as g

def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(n):return json.load(open(E/n))
def enum(x):return x.get(':db/ident') if isinstance(x,dict) else x
# Exact public-notation parser, independent of generator's classification fields.
def signature(t):
 t=re.sub(r'\s+','',t).replace('\\dfrac','\\frac');sg=-1 if t.startswith('-') else 1;t=t.lstrip('-')
 if '\\pi' in t:
  m=re.fullmatch(r'\\frac\{\\pi\}\{(\d+)\}',t);assert m or t=='\\pi',t
  return ('pi',Fraction(sg,int(m[1]) if m else 1))
 m=re.fullmatch(r'(\d*)\\sqrt\{?(\d+)\}?',t)
 if m:
  a=sg*int(m[1] or 1);b=int(m[2]);factor=1
  for n in range(2,isqrt(b)+1):
   while b%(n*n)==0:factor*=n;b//=n*n
  return ('rat',Fraction(a*factor)) if b==1 else ('root',a*factor,b)
 m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',t)
 return ('rat',Fraction(sg*int(m[1]),int(m[2]))) if m else ('rat',sg*Fraction(t))
def tex(text):return re.search(r'\$([^$]+)\$',text)[1].split('=',1)[0]
def target(q):
 p=q[':question/problem'].split('?',1)[0];return re.search(r'(?:\\mathbb\{)?([ZQR])',p)[1],bool(re.search(r'_\{?0',p)),1 if '+' in p else -1

def member(text,t):
 v=signature(tex(text));rat=v[0]=='rat';s=(v[1]>0)-(v[1]<0);integer=rat and v[1].denominator==1
 return t[1] if s==0 else s==t[2] and (t[0]=='R' or rat) and (t[0]!='Z' or integer)
def entries(q):
 if enum(q[':question/answer-fields'][0][':answer-field/type']).endswith('/radio'):
  return re.findall(r'(?m)^(?:IV|III|II|I|[1-4])\.\s*(\$[^$]+\$)',q[':question/problem'])
 return [f[':answer-field/key'] for f in q[':question/answer-fields'] if f[':answer-field/key'] not in ('None','None of the above')]
def subset(label):
 return sum(1<<('I','II','III','IV').index(x) for x in re.findall(r'\b(?:IV|III|II|I)\b',label))
def mask(r):
 q=r['question'];es=entries(q);assert len(es)==4;return sum(1<<i for i,k in enumerate(es) if member(k,target(q)))
def cv(f):
 ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def expected(r):
 q=r['question'];m=mask(r)
 if enum(q[':question/answer-fields'][0][':answer-field/type']).endswith('/radio'):
  bank=q[':question/answer-fields'][0][':answer-field/choices'];assert len({subset(a[':answer/value']) for a in bank})==len(bank)
  matches=[a[':answer/value'] for a in bank if subset(a[':answer/value'])==m];assert len(matches)==1;return matches
 return [str(not m).lower() if f[':answer-field/key'] in ('None','None of the above') else str(member(f[':answer-field/key'],target(q))).lower() for f in q[':question/answer-fields']]
def verify(r):
 q=r['question'];assert [cv(f) for f in q[':question/answer-fields']]==expected(r),q[':question/id']
 lines=[l for l in q[':question/worked-solution'].splitlines() if l.startswith('- ')];assert len(lines)==4
 identities=0
 for i,line in enumerate(lines):
  assert signature(tex(line)) in [signature(tex(e)) for e in entries(q)],line
  assert member(line,target(q))==('does *not* belong' not in line),line
  mathparts=re.findall(r'\$([^$]+)\$',line)
  # Check displayed simplifications and fraction conversions independently.
  for p in mathparts:
   if '=' in p:
    vals=p.split('=');assert all(signature(v)==signature(vals[0]) for v in vals);identities+=len(vals)-1
  if 'since it can be written as $' in line:
   rhs=re.search(r'since it can be written as \$([^$]+)\$',line)[1];assert signature(rhs)==signature(tex(line));identities+=1
 return identities

def main():
 source=json.load(open(J/'source/source.json'))['material']['kp'];orig=source[':knowledge-point/questions']
 # Verify bundled captured snapshot against original, not the author's oracle.
 assert json.load(open(W/'source_cases.json'))[':knowledge-point/questions']==orig
 replays=g.replay_sources();save('replay-records.json',replays);byid={r['generation']['source_question_ids'][0]:r for r in replays}
 replaychecks=[]
 for q in orig:
  r=byid[q[':question/id']];nq=r['question'];verify(r)
  assert len(q[':question/answer-fields'])==len(nq[':question/answer-fields'])
  for old,new in zip(q[':question/answer-fields'],nq[':question/answer-fields']):
   assert enum(old[':answer-field/type'])==enum(new[':answer-field/type'])
   assert re.sub(r'\s','',old[':answer-field/key'])==re.sub(r'\s','',new[':answer-field/key'])
   assert [a[':answer/value'] for a in old[':answer-field/choices']]==[a[':answer/value'] for a in new[':answer-field/choices']]
   if old.get(':answer-field/correct'):assert cv(old)==cv(new)
  replaychecks.append({'source_id':q[':question/id'],'passed':True,'fields':len(nq[':question/answer-fields']),'mask':mask(r),'original_key_and_solution_available':bool(q.get(':question/worked-solution'))})
 save('source-replay-checks.json',replaychecks)
 batch=json.load(open(J/'samples.json'));save('batch-records.json',batch)
 fresh=g.batch('easy',32,92169723);save('fresh-records.json',fresh)
 controlled=[]
 for t in g.TARGETS:
  for mode in ('radio','checkbox'):
   masks=range(16) if mode=='radio' or t in ('Q0-','Z0+') else (0,15)
   for m in masks:
    _,ns,_=g.sample(random.Random(5512026+m),t,m)
    r=g.generate(t,ns,seed=5512026,index=m,response=mode);assert mask(r)==m;controlled.append(r)
 save('controlled-records.json',controlled)
 ns=[g.number('integer',0),g.number('sqrt',1,2),g.number('fraction',1,2),g.number('integer',-3)]
 pairs=[];pairchecks=[]
 for mode in ('radio','checkbox'):
  rs=[g.generate(t,ns,response=mode,seed=19031) for t in ('Q0+','R0+','Q0-','Q-','Z0+')]
  ns2=list(ns);ns2[2]=g.number('fraction',3,4);rs.append(g.generate('Q0+',ns2,response=mode,seed=19031))
  assert [mask(r) for r in rs]==[5,7,9,8,1,5]
  pairs+=rs;pairchecks.append({'response':mode,'expected_masks':[5,7,9,8,1,5],'actual_masks':[mask(r) for r in rs],'changes':['base Q to R','sign + to -','exclude zero','base Q to Z','irrelevant 1/2 to 3/4'],'record_indices':list(range(len(pairs)-6,len(pairs)))})
 save('counterfactual-records.json',pairs);save('counterfactual-checks.json',pairchecks)
 ns=[g.number('sqrt',-1,3),g.number('decimal',-2),g.number('integer',0),g.number('sqrt',-1,4)]
 canonical=[g.generate('Q-',ns,response=mode,seed=4109) for mode in ('radio','checkbox')];assert all(mask(r)==10 for r in canonical);save('canonical-records.json',canonical)
 records=replays+batch+fresh+controlled+pairs+canonical;identities=sum(verify(r) for r in records)
 checks=[]
 for i,r in enumerate(records):
  cs=[]
  for j,(f,v) in enumerate(zip(r['question'][':question/answer-fields'],expected(r))):
   for a in f[':answer-field/choices']:
    cs.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==v else 'rejected','purpose':'independent visible membership; complete offered response bank'})
  checks.append({'label':f'independent-{i}','record':r,'checks':cs})
 save('grader-input.json',checks)
 save('math-checks.json',{'records':len(records),'solution_bullets':len(records)*4,'exact_equalities':identities,'failures':[],'method':'Exact Fraction arithmetic and extraction of square factors from visible notation; independent class/sign/zero membership; radio subset labels parsed independently; every offered distractor checked. Canonical mask 10 in both modes.','commands':[PY+' -B review.py']})
 save('delivery-input.json',fresh+controlled+pairs+canonical)
 # UI includes restored source banks, target-changing pairs and exact batch question.
 render=[byid[s] for s in ('59f3318f-8861-5823-9f55-694de5f640be','891fa895-d529-5c21-9765-4d2a287c7001','c620ed83-c013-5ff0-8983-14697bd50f1b','c2a941ac-46f5-56a9-b5ba-03889446453a')]+pairs[:2]+[pairs[5]]+pairs[6:8]+[pairs[11]]+[batch[0],batch[2]]
 save('render-records.json',render)
 def run(args,root=W):return subprocess.run([PY,'-B',str(root/'generator.py')]+args,capture_output=True,text=True,cwd=E)
 rel=E/'relocated';rel.mkdir(exist_ok=True)
 manifest=json.load(open(W/'package.json'))
 for name in ['package.json']+manifest['files']:shutil.copy2(W/name,rel/name)
 a=run(['--seed','4120901','--count','5']);b=run(['--seed','4120901','--count','5']);c=run(['--seed','4120901','--count','5'],rel)
 assert a.returncode==b.returncode==c.returncode==0 and a.stdout==b.stdout==c.stdout
 tests=[]
 for args,code in [(['--difficulty','hard'],2),(['--count','-1'],2),(['--count','0'],0)]:
  r=run(args);assert r.returncode==code;tests.append({'args':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 assert platform.python_version()==manifest['dependencies']['python'];assert manifest['dependencies']['packages']=={}
 save('packaging-checks.json',{'python_actual':platform.python_version(),'manifest':manifest,'determinism':True,'relocation':True,'boundaries':tests,'runtime':'stdlib only; JSON stdout; no assets or external outputs; only declared files copied for relocation'})
 save('scope-checks.json',{'source_refs':['05d0929b-b494-531b-9eea-35af04606555','ce8a56c1-709e-50e8-ac10-d3f92bf15db0'],'passed':True,'rationale':'Both source response contracts; four real candidates; elementary fractions, roots, pi, one-place decimals and integers; same class/sign/zero intersection, no extra prerequisite. Added targets Q0-/Z0+ are observed source targets; unrestricted masks alter assignments without adding reasoning stages. Generated radio bank remains five complete subset choices.','unsupported':'Moderate/hard and complex candidates are outside declared domain, not omitted supported source families.'})
 (E/'session-state.md').write_text('Independent source replay, restored-family controlled construction, exact visible mathematics, canonical example, counterfactual relationships and packaging completed. Retained regression fails original and passes revision. Native grader and renderer inputs saved; next run shared tools, inspect screenshots, finish decision/delivery report. Package untouched.\n')
 print(json.dumps({'source':len(replays),'batch':len(batch),'fresh':len(fresh),'controlled':len(controlled),'records':len(records),'equalities':identities,'grader_checks':sum(len(c['checks']) for c in checks),'render_records':len(render)}))
if __name__=='__main__':main()
