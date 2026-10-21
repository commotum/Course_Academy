import os,sys,json,re,hashlib,importlib.util,collections,shutil,pathlib
sys.dont_write_bytecode=True
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
R=pathlib.Path(__file__).resolve().parent
B=R.parent; P=B/'workspace'; ROOT=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,d): (R/n).write_text(json.dumps(d,indent=2,ensure_ascii=False,default=str))
def hashpackage():return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
save('package-before.json',hashpackage())
spec=importlib.util.spec_from_file_location('subject',P/'17592186087879.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=s.Symbol('x',positive=True);y=s.Symbol('y');D=s.Symbol('D')
def clean(t):
 return t.replace('\\\\frac','\\frac').replace('\\\\operatorname','\\operatorname').replace('\\u2061','').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\quad','').replace(r'\!','')
def group(t,i):
 while t[i].isspace():i+=1
 assert t[i]=='{',(t,i)
 j=i+1;d=1;k=j
 while d:
  if t[k]=='{':d+=1
  if t[k]=='}':d-=1
  k+=1
 return t[j:k-1],k
def expr(t):
 t=clean(t).strip().rstrip('.').replace(r'\dfrac',r'\frac')
 t=re.sub(r'\\operatorname\{(sin|cos|ln)\}',r'\\\1',t)
 while r'\frac' in t:
  i=t.index(r'\frac');a,j=group(t,i+5);b,k=group(t,j);t=t[:i]+'(('+str(expr(a))+')/('+str(expr(b))+'))'+t[k:]
 for a,b in [(r'\cdot','*'),(r'\pi','pi'),(r'\sin',' sin '),(r'\cos',' cos '),(r'\ln',' log ')]:t=t.replace(a,b)
 t=t.replace('{','(').replace('}',')')
 return parse_expr(t,local_dict={'x':x,'y':y,'D':D,'e':s.E,'pi':s.pi,'sin':s.sin,'cos':s.cos,'log':s.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def eq(a,b):return s.simplify(a-b)==0
def promptdata(r):
 t=clean(r['question'][':question/problem']);blocks=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$',t,re.S)
 t=next(a or b for a,b in blocks if 'dy' in a+b or r'\text{d}y' in a+b)
 t=re.sub(r'\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}|\\frac\{dy\}\{dx\}','D',t)
 initial=re.search(r'y\((.*?)\)\s*=\s*(-?\d+)',t);assert initial,t
 point=expr(initial[1]);h=expr(initial[2]);ode=t[:initial.start()].replace('x>0','').rstrip(' ,');lhs,rhs=ode.split('=',1);lhs=expr(lhs);a=s.expand(lhs).coeff(D)
 return s.simplify(lhs.coeff(y)/a),s.simplify(expr(rhs)/a),point,h

def mathcheck(r):
 try:
  p,q,t,h=promptdata(r);fields=r['question'][':question/answer-fields'];checks=[]
  for fi,f in enumerate(fields):
   vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']];cid=f[':answer-field/correct'][1];correct=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==cid)
   valid=[(eq(s.diff(v,x),p*v) and v!=0) if fi==0 else (eq(s.diff(v,x)+p*v,q) and eq(v.subs(x,t),h)) for v in vals]
   checks.append({'field':fi,'valid_indices': [i for i,v in enumerate(valid) if v],'key_index':correct,'key_valid':valid[correct],'exactly_one':sum(valid)==1})
  final=re.findall(r'\$\$\s*y\s*=(.*?)\$\$',r['question'][':question/worked-solution'],re.S)
  final_ok=None
  if final:
   v=expr(final[-1]); final_ok=eq(s.diff(v,x)+p*v,q) and eq(v.subs(x,t),h)
  return {'id':r['question'][':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'displayed':{'P':str(p),'Q':str(q),'t':str(t),'h':str(h)},'fields':checks,'final_solution_valid':final_ok,'passed':all(c['key_valid'] and c['exactly_one'] for c in checks) and final_ok is not False}
 except Exception as e:return {'id':r['question'][':question/id'],'template':r['generation']['template'],'error':repr(e),'passed':False}

if __name__=='__main__':
 rows=[]
 for i in range(24):rows.append(g.generate('easy',seed=70401+i))
 for template,(level,family) in g.AUTH.items():
  if level!='easy':
   for i in range(3):rows.append(g.generate(level,seed=80211+i,template=template))
 save('independent-samples.json',rows)
 batch=json.load(open(B/'samples.json'));save('runner-batch.json',batch)
 replays=[];replay_results=[];source=json.load(open(B/'source/source.json'))['material']['kp'][':knowledge-point/questions']
 for tid,(level,fam,params,_,_) in g.OBS.items():
  rr=g.generate(level,seed=432,template=tid,parameters=params,profile='observed');replays.append(rr);src=next(q for q in source if q[':question/math-academy-id']==tid)
  banks=[]
  for f in src[':question/answer-fields']:
   rf=next(v for v in rr['question'][':question/answer-fields'] if v[':answer-field/key']==f[':answer-field/key']);a=[expr(v[':answer/value']) for v in f[':answer-field/choices']];b=[expr(v[':answer/value']) for v in rf[':answer-field/choices']];banks.append({'key':f[':answer-field/key'],'count':len(a),'complete_multiset':collections.Counter(map(s.srepr,a))==collections.Counter(map(s.srepr,b))})
  replay_results.append({'source_id':src[':question/id'],'template':tid,'prompt_exact':rr['question'][':question/problem']==src[':question/problem'],'banks':banks,'solution_available':':question/worked-solution' in src})
 save('source-replays.json',replays);save('source-replay-results.json',replay_results)
 # Explicit before/after cases; held seed controls option shuffling.
 pairs=[]
 for h in [-1,-2]:pairs.append(g.generate('easy',seed=991,parameters={'a':1,'b':2,'h':h}))
 pairs.append(g.generate('easy',seed=992,parameters={'a':1,'b':2,'h':-1}))
 # Changed observed sine initial value must update displayed condition as well as all answers.
 pairs.append(g.generate('moderate',seed=991,template='q-335812',parameters={'k':1,'h':2}))
 save('counterfactual-records.json',pairs)
 outcomes=[mathcheck(r) for r in rows+batch+pairs];save('math-results.json',outcomes)
 rejection=[]
 for label,kw in [('eligible easy coefficient a=2',dict(level='easy',parameters={'a':2,'b':2,'h':-1})),('invalid coefficient zero',dict(level='easy',parameters={'a':0,'b':2,'h':-1})),('constant equilibrium',dict(level='easy',parameters={'a':1,'b':2,'h':2})),('zero initial value',dict(level='easy',parameters={'a':1,'b':2,'h':0})),('unknown difficulty',dict(level='extreme')),('wrong field type',dict(level='easy',field_type='free'))]:
  try:g.generate(seed=991,**kw);rejection.append({'case':label,'rejected':False})
  except Exception as e:rejection.append({'case':label,'rejected':True,'exception':str(e)})
 save('rejection-results.json',rejection)
 save('runtime-results.json',{'python':sys.version.split()[0],'sympy':s.__version__,'manifest':json.load(open(P/'package.json'))['dependencies'],'deterministic_replay':rows[0]==g.generate('easy',seed=70401),'history_present':(B/'repair-history.json').exists(),'preflight_present':(B/'repair-preflight.json').exists()})
 save('render-records.json',[rows[0],pairs[0],pairs[1],pairs[2],pairs[3],*rows[24::3]])
 # Native grader tests: all choices for independent and counterfactual samples; mathematical validity determines expected status.
 cases=[]
 for r in rows+pairs:
  p,q,t,h=promptdata(r);checks=[]
  for fi,f in enumerate(r['question'][':question/answer-fields']):
   for a in f[':answer-field/choices']:
    v=expr(a[':answer/value']);valid=eq(s.diff(v,x),p*v) and v!=0 if fi==0 else eq(s.diff(v,x)+p*v,q) and eq(v.subs(x,t),h)
    checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if valid else 'rejected','purpose':'independent displayed ODE and IC verification'})
  cases.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
 save('grader-input.json',cases)
 print(json.dumps({'samples':len(rows),'replay_cases':len(replays),'replays_failed':[a for a in replay_results if not a['prompt_exact'] or not all(b['complete_multiset'] for b in a['banks'])],'math_failures':[o for o in outcomes if not o['passed']],'rejections':rejection},indent=2))
