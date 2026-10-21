import os,sys,json,pathlib,importlib.util,re,hashlib,shutil,subprocess
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
EVID=pathlib.Path(__file__).resolve().parent
JOB=EVID.parent; PKG=JOB/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,d): (EVID/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def load(n):return json.loads(pathlib.Path(n).read_text())
def snap():return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}
def module(path):
 spec=importlib.util.spec_from_file_location('review_generator',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
x,y,yp=s.symbols('x y yp',positive=True)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def parse(z):
 z=z.replace('\\\\','\\').replace('\\u2061','').replace('\u2061','')
 z=re.sub(r'\\operatorname\{(\w+)\}',r' \1 ',z)
 z=z.replace('\\left','').replace('\\right','').replace('\\cdot','*').replace('\\,','').replace('\\!','').replace('\\ln',' log ').replace('\\log',' log ').replace('\\cos',' cos ').replace('\\sin',' sin ')
 # Process nested fractions by matching their brace-balanced operands.
 def brace(t,i):
  assert t[i]=='{',(t,i)
  depth=1;j=i+1
  while depth:
   if t[j]=='{':depth+=1
   if t[j]=='}':depth-=1
   j+=1
  return t[i+1:j-1],j
 while '\\frac' in z:
  i=z.rfind('\\frac');a,j=brace(z,i+5);b,k=brace(z,j);z=z[:i]+'(('+a+')/('+b+'))'+z[k:]
 z=re.sub(r'\bln\b','log',z)
 z=re.sub(r'(cos|sin|log)\s*x\b',r' \1(x)',z)
 z=re.sub(r'(cos|sin|log)\s*\|([^|]+)\|',r' \1(\2)',z)
 z=z.replace('{','(').replace('}',')').replace('^','**').strip().rstrip('.')
 assert '\\' not in z,repr(z)
 return parse_expr(z,local_dict={'x':x,'y':y,'yp':yp,'e':s.E,'cos':s.cos,'sin':s.sin,'log':s.log},transformations=TRANS)
D=re.compile(r'\\frac\{(?:\\text\{d\}y|dy)\}\{(?:\\text\{d\}x|dx)\}')
DD=re.compile(r'\\frac\{(?:\\text\{d\}|d)\}\{(?:\\text\{d\}|d)x(?:\^\{2\})?\}')
def ode(q):
 for z in re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]+)\$',q[':question/problem']):
  z=z[0] or z[1]
  if D.search(z):
   z=D.sub(' yp ',z).split(',')[0];a,b=z.split('=');lhs=parse(a);rhs=parse(b);A=s.expand(lhs).coeff(yp);P=s.simplify(lhs.subs(yp,0)/y/A);Q=s.simplify(rhs/A);return P,Q
 raise AssertionError('no ODE')
def choice(z):
 z=z.replace('\\\\','\\').replace('\\u2061','').replace('\u2061','');mat=DD.search(z);assert mat,z
 malformed='dx^{2}' in mat.group();a,b=z[mat.end():].split('=');f=s.simplify(parse(a)/y);return f,parse(b),malformed

def field(q):return q[':question/answer-fields'][0]
def correct_id(q):
 a=field(q)[':answer-field/correct'];return a[':answer/id'] if isinstance(a,dict) else a[1]
def cue(q):
 # Answer bank only: find f whose reciprocal and square are both in the bank.
 cs=field(q)[':answer-field/choices'];fs=[choice(c[':answer/value'])[0] for c in cs];hits=[]
 for c,f in zip(cs,fs):
  if f.func==s.exp and any(s.simplify(g-1/f)==0 for g in fs) and any(s.simplify(g-f**2)==0 for g in fs):hits.append(c[':answer/id'])
 return hits

def math_check(r):
 q=r['question'];P,Q=ode(q);valid=[];fs=[]
 for a in field(q)[':answer-field/choices']:
  f,rhs,m=choice(a[':answer/value']);fs.append(f)
  if not m and s.simplify(s.diff(f,x)-P*f)==0 and s.simplify(rhs-f*Q)==0:valid.append(a[':answer/id'])
 assert valid==[correct_id(q)],(q[':question/id'],P,Q,valid)
 sol=q[':question/worked-solution'];last=re.findall(r'\$\$([\s\S]*?)\$\$',sol)[-1];last=last.replace('\\begin{aligned}','').replace('\\end{aligned}','').replace('&','').strip();f,rhs,m=choice(last)
 assert s.simplify(s.diff(f,x)-P*f)==0 and s.simplify(rhs-f*Q)==0,(q[':question/id'],'final solution')
 # Independently test displayed expanded multiplication row, not metadata.
 blocks=re.findall(r'\$\$([\s\S]*?)\$\$',sol)
 for block in blocks:
  for row in block.replace('\\begin{aligned}','').replace('\\end{aligned}','').split('\\\\'):
   if D.search(row) and 'P(x)' not in row and '=' in row:
    a,b=D.sub(' yp ',row.replace('&','')).split('=');lhs=parse(a);rhs=parse(b);A=s.expand(lhs).coeff(yp)
    assert s.simplify(lhs-A*(yp+P*y))==0 and s.simplify(rhs-A*Q)==0,(q[':question/id'],'solution row',row)
 return {'id':q[':question/id'],'P':str(P),'Q':str(Q),'valid_choices':len(valid),'bank_cue_hits':cue(q),'cue_correct':cue(q)==[correct_id(q)]}

def main():
 save('package-before.json',snap());g=module(PKG/'17592186087877.py')
 seeds=[83017,83043,83111,83203];samples=[]
 for t in ['constant_cos','scaled_constant_power','signed_constant_power']:
  for seed in seeds:samples.append(g.generate('easy',seed,template=t))
 save('samples-independent.json',samples);batch=load(JOB/'samples.json');save('runner-batch.json',batch)
 pairs=[g.generate('easy',99017,template='signed_constant_power',parameters={'a':a,'n':3}) for a in ['1','-1','2']]
 # Irrelevant display randomization: same mathematical instance, fresh shuffle seed.
 pairs.append(g.generate('easy',99018,template='signed_constant_power',parameters={'a':'1','n':3}))
 save('counterfactual-records.json',pairs)
 allrows=samples+batch+pairs
 checks=[math_check(r) for r in allrows];save('math-results.json',{'command':f'{sys.executable} {__file__}','checks':checks,'passed':True})
 cases=[]
 for r in allrows:
  q=r['question'];checks=[]
  for a in field(q)[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct_id(q) else 'rejected','purpose':'independently verified integrating factor and normalized RHS'})
  cases.append({'label':q[':question/id'],'record':r,'checks':checks})
 save('grader-input.json',cases)
 # Reproduce every supplied source with complete raw bank; compare symbols, not author claims.
 src=load(JOB/'source/source.json')['material']['kp'][':knowledge-point/questions'];replays=[];results=[]
 for sid,t,p in g.CASES:
  level=g.TEMPLATES[t][0];r=g.generate(level,401,template=t,parameters=p,profile='observed_raw');replays.append(r)
  original=next(q for q in src if q[':question/math-academy-id']==sid)
  op,oq=ode(original);rp,rq=ode(r['question']);assert s.simplify(op-rp)==0 and s.simplify(oq-rq)==0
  ob=[choice(a[':answer/value']) for a in field(original)[':answer-field/choices']];rb=[choice(a[':answer/value']) for a in field(r['question'])[':answer-field/choices']]
  assert all(any(s.simplify(f-f2)==0 and s.simplify(v-v2)==0 and m==m2 for f2,v2,m2 in rb) for f,v,m in ob),(sid,ob,rb)
  math_check(r)
  results.append({'source_id':original[':question/id'],'math_academy_id':sid,'P':str(op),'Q':str(oq),'complete_bank_match':True,'bank_size':len(ob),'missing_source_key':':answer-field/correct' not in field(original),'malformed_operator_retained_as_evidence':any(m for f,v,m in ob)})
 save('source-replay-records.json',replays);save('source-replay-results.json',{'cases':results,'canonical_example':'Independent P=2 gives I=exp(2x), consistent with canonical 1e3c0253-226d-596c-a831-7c68ec76b21c. It has no radio bank.','correction':'Source dba525fe intermediate plus sign is corrected; raw malformed differential operator is historical replay evidence only.'})
 save('render-records.json',pairs+[samples[0],samples[4],replays[3],replays[7]])
 # Runtime/package checks, explicit boundary rejection, replay, relocation.
 rejected=[]
 for kwargs in [dict(level='easy',template='signed_constant_power',parameters={'a':'0','n':3}),dict(level='easy',template='signed_constant_power',parameters={'a':'1/4','n':3}),dict(level='easy',template='signed_constant_power',parameters={'a':'1','n':0}),dict(level='easy',template='reciprocal_exp'),dict(level='easy',field_type='free')]:
  try:g.generate(seed=401,**kwargs);rejected.append({'kwargs':kwargs,'rejected':False})
  except ValueError as e:rejected.append({'kwargs':kwargs,'rejected':True,'error':str(e)})
 assert all(a['rejected'] for a in rejected)
 assert g.generate('easy',83017,template='constant_cos')==samples[0]
 relocation=EVID/'relocated-package';relocation.mkdir(exist_ok=True);shutil.copy2(PKG/'17592186087877.py',relocation/'17592186087877.py');(relocation/'17592186087877').mkdir(exist_ok=True)
 for n in ['source.json','source-current.json']:shutil.copy2(PKG/'17592186087877'/n,relocation/'17592186087877'/n)
 r=module(relocation/'17592186087877.py').generate('easy',83017,template='constant_cos');assert r==samples[0]
 save('packaging-results.json',{'python':sys.version.split()[0],'packages':{'sympy':s.__version__},'manifest_dependencies':load(PKG/'package.json')['dependencies'],'deterministic_replay':True,'relocation':True,'boundary_rejections':rejected,'source_loading':'Sibling captured JSON only; no network, output assets or DB required.','package_unchanged':snap()==load(EVID/'package-before.json')})
 (EVID/'session-state.md').write_text('Independent source account saved before package inspection. Independent samples, controlled relevant/irrelevant pairs, eight full source-bank replays, symbolic prompt/choice/solution checks and runtime/rejection checks saved. No package changes. Next: native grader, actual UI, delivery and inventory reproduction.\n')
 print('Saved',len(samples),'fresh samples,',len(batch),'batch records,',len(pairs),'counterfactuals and',len(replays),'source replays; math checks passed.')
if __name__=='__main__':main()
