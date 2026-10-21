import os,sys,json,re,hashlib,shutil,subprocess,importlib.util
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1'
sys.dont_write_bytecode=True
ROOT=Path('/home/jake/Developer/Course_Academy'); PKG=Path('../workspace').resolve(); E=Path(__file__).resolve().parent
sys.path.insert(0,str(PKG));import generator as g
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
x=s.Symbol('x',real=True);u=s.Symbol('u',real=True)
def parse(t):
 t=t.replace('\\\\','\\').replace('\u2061','').replace('′',"'")
 t=re.sub(r'\\operatorname\{ln\}',r'\\ln',t)
 for z in [r'\left',r'\right',r'\,',r'\!',r'\ ']:t=t.replace(z,'')
 def group(st,i):
  while i<len(st) and st[i].isspace():i+=1
  if st[i]!='{':return st[i],i+1
  start=i+1;depth=1;i+=1
  while depth:
   if st[i]=='{':depth+=1
   if st[i]=='}':depth-=1
   i+=1
  return st[start:i-1],i
 while '\\frac' in t or '\\dfrac' in t:
  m=re.search(r'\\d?frac',t); a,i=group(t,m.end());b,j=group(t,i);t=t[:m.start()]+'(('+a+')/('+b+'))'+t[j:]
 t=t.replace(r'\cdot','*').replace(r'\times','*')
 t=re.sub(r'\\ln\s*([0-9]+)',r'log(\1)',t)
 t=re.sub(r'(?<![A-Za-z\\])ln',r'\\ln',t)
 t=re.sub(r'\\ln\s*([0-9]+)',r'log(\1)',t)
 t=t.replace(r'\sqrt','sqrt').replace(r'\ln','log').replace('{','(').replace('}',')')
 t=re.sub(r'(?<=[0-9a-z)])log', '*log',t)
 t=t.strip().removeprefix('y=')
 if '\\' in t: raise ValueError('Unknown tex '+t)
 return parse_expr(t,local_dict={'x':x,'u':u,'log':s.log,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def eq(a,b):return s.simplify(s.expand_log(a-b,force=True))==0
def expected(r):
 q=r['question'];p=q[':question/problem']
 # Actual displayed function, not metadata parameters.
 m=re.search(r'(?:f\(x\)|y)\s*=\s*(.*?)\$',p); f=parse(m[1].rstrip(' ,'));v=s.diff(f,x)
 if 'tangent' in p:
  t=parse(re.search(r'where \$x=(.*?)\$',p)[1].rstrip(' .'))
  if 'equation' in p:v=s.expand(v.subs(x,t)*(x-t)+f.subs(x,t))
  else:v=v.subs(x,t)
 elif '{{field-1}}' in p and p.count('^{')>1 and r'$\cdot' in p.split('{{field-1}}')[-1]:
  tail=p.split('{{field-1}}')[-1].strip('$');v=s.simplify(v/parse(tail.lstrip().removeprefix(r'\cdot')))
 return f,v

def save(name,z): (E/name).write_text(json.dumps(z,indent=2,ensure_ascii=False,default=str))
def key(r):
 f=r['question'][':question/answer-fields'][0];return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])

def main():
 manifest=json.load(open(PKG/'package.json'));before={f:hashlib.sha256((PKG/f).read_bytes()).hexdigest() for f in manifest['files']+['package.json']};save('package-before.json',before)
 if '--reuse' in sys.argv:
  records=json.load(open('records.json'));replays=json.load(open('source-replays.json'));pairs=json.load(open('pairs.json'))
 else:
  records=[];replays=[];pairs=[];rejections=[]
  for j,(qid,spc) in enumerate(g.SPECS.items()):
   for i in range(9):records.append(g.generate(spc['level'],seed=781301+100*j+i,template=qid))
   p=g.default_params(qid)
   replays.append(g.generate(spc['level'],seed=918781+j,template=qid,parameters=p,profile='historical:'+qid))
   # Leading sign change at original parameters: relevant, except a zero slope (none here).
   pp=dict(p);pp['a']=-pp['a']
   try:
    a=g.generate(spc['level'],seed=28491+j,template=qid,parameters=p);b=g.generate(spc['level'],seed=28491+j,template=qid,parameters=pp)
    pairs.append({'kind':'relevant','change':'flip leading exponent coefficient','template':qid,'before':a,'after':b});records.extend([a,b])
   except ValueError as ex:rejections.append({'template':qid,'params':pp,'error':str(ex)})
  # Applicable irrelevant dependency: constant shift cancels out of requested coefficient fragment.
  p=g.default_params('q-312462'); pp={**p,'d':-2}
  a=g.generate_easy(192861,'q-312462',parameters=p);b=g.generate_easy(192861,'q-312462',parameters=pp)
  pairs.append({'kind':'irrelevant','change':'change constant exponent shift in supplied-exponential fragment','template':'q-312462','before':a,'after':b});records.extend([a,b])
  # Irrelevant presentation: different shuffle/bank seed does not change derivative.
  p=g.default_params('q-107459');a=g.generate_easy(518881,'q-107459',parameters=p);b=g.generate_easy(518882,'q-107459',parameters=p)
  pairs.append({'kind':'irrelevant','change':'change bank/choice ordering seed with all function data fixed','template':'q-107459','before':a,'after':b});records.extend([a,b])
  boundaries=[]
  for qid in ['q-71881','q-107459','q-1952','q-312462']:
   p=g.default_params(qid);p.update(b=6,a=-9)
   if p['c']>1:p['c']=5
   if p['d']:p['d']=-5
   boundaries.append(g.generate_easy(631785,template=qid,parameters=p))
  records+=boundaries
  invalid=[]
  for change in [{'b':1},{'a':0},{'n':4},{'d':6},{'c':0}]:
   p={**g.default_params('q-107459'),**change}
   try:g.generate_easy(61182,template='q-107459',parameters=p);invalid.append({'params':p,'rejected':False})
   except ValueError as ex:invalid.append({'params':p,'rejected':True,'error':str(ex)})
  save('records.json',records);save('source-replays.json',replays);save('pairs.json',pairs);save('boundaries.json',{'valid':boundaries,'invalid':invalid,'pair_rejections':rejections,'sampler_rejections':g.REJECTIONS})
 batch=json.load(open('../samples.json'));save('runner-batch.json',batch)
 math=[];grade=[]
 for idx,r in enumerate(records+replays+batch):
  try:
   f,v=expected(r);fld=r['question'][':question/answer-fields'][0];answers=[(a,parse(a[':answer/value'])) for a in fld[':answer-field/choices']]
   hits=[a[':answer/id'] for a,av in answers if eq(av,v)];correct=key(r)
   good=eq(parse(correct[':answer/value']),v) and (len(hits)==1 or fld[':answer-field/type'].endswith('/blank'))
   # Verify authored worked solution final derivative line against independent derivative; source uses several layouts.
   sol=r['question'][':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
   derivblock=next(z for z in blocks if 'aligned' in z and (r'frac' in z))
   final=derivblock.split('& =')[-1].split(r'\end{aligned}')[0].strip().rstrip('.')
   derived=parse(final);derivgood=eq(derived,s.diff(f,x))
   math.append({'index':idx,'id':r['question'][':question/id'],'expected':str(v),'key':str(parse(correct[':answer/value'])),'passed':good,'solution_derivative_passed':derivgood})
   checks=[]
   if fld[':answer-field/type'].endswith('/radio'):
    checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if eq(av,v) else 'rejected','purpose':'independent displayed-expression differentiation'} for a,av in answers]
   else:
    for submitted,purpose in [(s.latex(v).replace(r'\log',r'\ln'),'independent expected'),(r'\frac{2('+s.latex(v).replace(r'\log',r'\ln')+r')}{2}','equivalent'),(s.latex(-v).replace(r'\log',r'\ln'),'wrong sign'),('0','zero wrong'),(s.latex(s.simplify(v/s.log(next(iter([r['generation']['parameters']['b']]))))),'missing log wrong')]:
     # All bases integer >1 ensure removing ln changes value.
     checks.append({'submitted':submitted,'expected':'rejected' if 'wrong' in purpose else 'accepted','purpose':purpose})
   grade.append({'label':f'record-{idx}','record':r,'checks':checks})
  except Exception as ex:math.append({'index':idx,'id':r['question'][':question/id'],'error':str(ex)})
 save('math.json',math);save('grader-input.json',grade)
 # Cross-response counterfactual checks use original response against changed instance.
 pair_results=[]
 for i,p in enumerate(pairs):
  a,b=p['before'],p['after'];fa,va=expected(a);fb,vb=expected(b)
  same=eq(va,vb);expected_same=p['kind']=='irrelevant';fld=b['question'][':question/answer-fields'][0]
  if fld[':answer-field/type'].endswith('/blank'):
   grade.append({'label':f'pair-{i}-old-response','record':b,'checks':[{'submitted':s.latex(va).replace(r'\log',r'\ln'),'expected':'accepted' if same else 'rejected','purpose':'before response submitted to after instance'}]})
  pair_results.append({'pair':i,'kind':p['kind'],'template':p['template'],'before_answer':str(va),'after_answer':str(vb),'passed':same==expected_same})
 save('pair-results.json',pair_results);save('grader-input.json',grade)
 # Source complete-bank comparison, independent TeX interpretation.
 src=json.load(open('../source/source.json'))['material']['kp'];sourcecheck=[]
 for r in replays:
  qid=r['generation']['template'];q=next(z for z in src[':knowledge-point/questions']+[src[':knowledge-point/canonical-example']] if z[':question/math-academy-id']==qid)
  out=[parse(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  for fi,fld in enumerate(q.get(':question/answer-fields',[])):
   for a in fld[':answer-field/choices']:
    v=parse(a[':answer/value']);sourcecheck.append({'source_id':q[':question/id'],'ma_id':qid,'field':fi,'source_value':a[':answer/value'],'matched':any(eq(v,z) for z in out)})
 save('source-bank-comparison.json',sourcecheck)
 # Replay and runtime relocation with only declared files, no package mutation.
 relocated=E/'relocated';relocated.mkdir(exist_ok=True)
 for fn in manifest['files']:shutil.copyfile(PKG/fn,relocated/fn)
 cmd=[sys.executable,str(relocated/'generator.py'),'--seed','781301','--count','5'];out=subprocess.check_output(cmd,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},cwd=E)
 local=subprocess.check_output([sys.executable,str(PKG/'generator.py'),'--seed','781301','--count','5'],env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},cwd=E)
 save('relocation.json',{'command':cmd,'equal':out==local,'records':json.loads(out),'versions':{'python':sys.version.split()[0],'sympy':s.__version__},'declared':manifest['dependencies']})
 save('package-after.json',{f:hashlib.sha256((PKG/f).read_bytes()).hexdigest() for f in before})
 save('sampling-summary.json',{'records':len(records),'replays':len(replays),'batch':len(batch),'pairs':len(pairs),'math_failures':[z for z in math if not z.get('passed') or not z.get('solution_derivative_passed')],'source_bank_failures':[z for z in sourcecheck if not z['matched']],'rejections':g.REJECTIONS})
 print(json.dumps(json.load(open(E/'sampling-summary.json')),indent=2))
if __name__=='__main__':main()
