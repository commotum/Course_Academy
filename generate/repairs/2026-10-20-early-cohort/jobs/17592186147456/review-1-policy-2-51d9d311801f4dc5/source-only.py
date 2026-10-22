import os,sys,json,pathlib,importlib.util,hashlib,shutil,subprocess,re,itertools,collections,copy
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
R=pathlib.Path('/home/jake/Developer/Course_Academy');J=R/'generate/repairs/2026-10-20-early-cohort/jobs/17592186147456'; W=J/'workspace'; PY=R/'.venv/bin/python'
def save(n,d): (E/n).write_text(json.dumps(d,indent=2,default=str)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
if not (E/'package-before.json').exists():save('package-before.json',hashes())
sys.path.insert(0,str(W));sys.path.insert(0,str(W/'checks/vendor'))
spec=importlib.util.spec_from_file_location('review_generator',W/'17592186147456.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import sympy as s
from sympy.parsing.latex import parse_latex
x,y,z=s.symbols('x y z',positive=True)
def parse(t):
 t=t.replace('⁡','').replace('{e}','e'); t=re.sub(r'\\operatorname\{(tan|sin|cos|sec|ln)\}', lambda m:'\\'+m.group(1)+' ',t); t=t.replace('{cos}',r'\cos '); return parse_latex(t).subs({s.Symbol('x'):x,s.Symbol('y'):y,s.Symbol('z'):z})
def eq(t):
 t=t.strip('$').replace('{y}^{′}','z').replace('y^{′}','z').replace("y'",'z')
 lhs,rhs=t.split('='); l=parse(lhs);b=parse(rhs);m=s.diff(l,z);a=s.simplify(l-m*z);assert not a.has(z) and not m.has(z)
 return tuple(map(s.simplify,(m,a,b)))
def independent(e):
 m,a,b=e; A=s.simplify(a/m);B=s.simplify(b/m)
 def power(v):
  n=s.simplify(y*s.diff(v,y)/v);return n if not n.has(y) else None
 pa,pb=power(A),power(B)
 good=pa is not None and pb is not None and pa!=pb and (pa==1 or pb==1)
 return bool(good),A,B,pa,pb

def fieldvalue(f):
 ref=f[':answer-field/correct']; aid=ref[1] if isinstance(ref,list) else ref[':answer/id']
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def flags_record(r):
 fs=r['question'][':question/answer-fields']
 if fs[0][':answer-field/type']==':answer-field.type/checkbox':return tuple(fieldvalue(f)=='true' for f in fs[:3])
 v=fieldvalue(fs[0]);return tuple(bool(re.search(r'\b'+label+r'\b',v)) for label in ['I','II','III'])
def prompted_eqs(r):return [eq(t) for t in re.findall(r'- \*\*[IV]+\.\*\* \$(.*?)\$',r['question'][':question/problem'])]


# Replay every rated source profile, compare all equations as symbolic triples and complete banks.
source=load(J/'source/source.json')['material']; sqs=source['kp'][':knowledge-point/questions'];replays=[];replayresults=[]
for t,(level,_) in g.CASES.items():
 q=next(q for q in sqs if q[':question/math-academy-id']==t)
 rr=g.generate(level,template=t,parameters={'left_scales':[1]*3,'right_scales':[1]*3},replay=True);replays.append(rr)
 if q[':question/answer-fields'][0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
  src_eqs=[eq(f[':answer-field/key']) for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above'];
  flags={s.srepr(e):f[':answer-field/correct'][':answer/value'] for f,e in zip([f for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above'],src_eqs)}
  generated=prompted_eqs(rr); matches=all(any(all(s.simplify(u-v)==0 for u,v in zip(a,b)) for b in generated) for a in src_eqs)
  bank_ok=len(rr['question'][':question/answer-fields'])==len(q[':question/answer-fields'])
 else:
  src_eqs=[eq(t) for t in re.findall(r'\$(.*?)\$',q[':question/problem'])];generated=prompted_eqs(rr)
  matches=all(all(s.simplify(u-v)==0 for u,v in zip(a,b)) for a,b in zip(src_eqs,generated))
  bank_ok=sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in rr['question'][':question/answer-fields'][0][':answer-field/choices'])
 replayresults.append({'source_id':q[':question/id'],'template':t,'all_equations_replayed':matches,'complete_bank':bank_ok,'key':flags_record(rr),'source_solution_available':True})
save('source-replay-records.json',replays)
missing=[]
for q in [source['kp'][':knowledge-point/canonical-example']]+sqs:
 if q[':question/math-academy-id'] not in g.CASES:
  try:g.generate('easy',template=q[':question/math-academy-id']);outcome='unexpectedly accepted'
  except Exception as e:outcome=type(e).__name__+': '+str(e)
  missing.append({'source_id':q[':question/id'],'source_template':q[':question/math-academy-id'],'solution_available':':question/worked-solution' in q,'answer_fields_available':':question/answer-fields' in q,'outcome':outcome})
save('source-replay.json',{'rated_results':replayresults,'unrepresented_source':missing,'source_corrections':['q-108916 duplicated equation name corrected','q-108911 malformed final quote corrected'],'limits':'Two unrated drafts lack authoritative key/solution, canonical lacks answer fields. Inferred draft keys are I and III; II only.'})
# Reject malformed/out-of-domain inputs without silently changing them.
reject=[]
for name,args in [('hard',{'level':'hard'}),('wrong rating',{'level':'easy','template':'q-108920'}),('zero scalar',{'level':'easy','template':'q-108911','parameters':{'left_scales':[0,1,1],'right_scales':[1,1,1]}}),('six scalar',{'level':'easy','template':'q-108911','parameters':{'left_scales':[6,1,1],'right_scales':[1,1,1]}}),('bool scalar',{'level':'easy','template':'q-108911','parameters':{'left_scales':[True,1,1],'right_scales':[1,1,1]}}),('unrepresentable radio subset',{'level':'easy','template':'q-108915','parameters':{'decisions':[False,False,False],'left_scales':[1]*3,'right_scales':[1]*3}})]:
 try:g.generate(**args);result='accepted'
 except Exception as e:result=type(e).__name__
 reject.append({'case':name,'arguments':args,'result':result})
save('rejections.json',reject)

print(json.dumps(load(E/'source-replay.json')))
