"""Read-only independent review. Run with context Python, PYTHONDONTWRITEBYTECODE=1."""
import os,sys,json,re,importlib.util,hashlib,subprocess,shutil,platform
from pathlib import Path
from collections import Counter,defaultdict
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
E=Path(__file__).resolve().parent; J=E.parent; P=J/'workspace'; REPO=Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(P))
spec=importlib.util.spec_from_file_location('reviewed_generator',P/'17592186087886.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,v,z=S.symbols('x y v z')
DV=r'\frac{\text{d}v}{\text{d}x}'; DY=r'\frac{\text{d}y}{\text{d}x}'
def save(name,obj): (E/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str)+'\n')
def readmath(s):
 s=s.replace(DV,'z').replace(DY,'(x*z+v)').replace(r'\frac{\text{d}}{\text{d}x}(x)','1')
 s=s.replace('\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','')
 s=re.sub(r'\\operatorname\{(\w+)\}',r'\1 ',s)
 s=re.sub(r'\\(sin|cos|tan|sec)\b',r'\1 ',s)
 s=s.replace(r'\cdot','*')
 def group(i,close=None):
  out=''
  while i<len(s):
   if close and s[i]==close:return out,i+1
   if s.startswith('\\frac',i):
    i+=5;assert s[i]=='{';a,i=group(i+1,'}');assert s[i]=='{';b,i=group(i+1,'}');out+='(('+a+')/('+b+'))'
   elif s.startswith('\\cancel',i):
    i+=7;assert s[i]=='{';a,i=group(i+1,'}');out+='('+a+')'
   elif s[i] in '{(':
    a,i=group(i+1,'}' if s[i]=='{' else ')');out+='('+a+')'
   elif s[i]=='^':out+='**';i+=1
   else:out+=s[i];i+=1
  assert close is None
  return out,i
 raw,_=group(0)
 assert re.fullmatch(r'[A-Za-z0-9+*/().\s-]+',raw),raw
 return parse_expr(raw,local_dict={'x':x,'y':y,'v':v,'z':z,'e':S.E,'sin':S.sin,'cos':S.cos,'tan':S.tan,'sec':S.sec},transformations=standard_transformations+(implicit_multiplication_application,))
def rhs(q):return readmath(q[':question/problem'].split('$$')[1].strip().rstrip('.').split('=')[1])
def rate(eq):
 a,b=eq.strip().rstrip('.').split('=');d=readmath(a)-readmath(b)
 return S.cancel(-d.subs(z,0)/S.diff(d,z))
def equal(a,b):
 d=S.cancel(a-b)
 if d==0:return True
 for t in (S.Rational(7,9),S.Rational(11,7)):
  n=d.subs({v:t,x:S.Rational(5,3),y:t*S.Rational(5,3)}).evalf(40)
  if n.is_real and n.is_finite and abs(n)>S.Float('1e-25'):return False
 return S.trigsimp(d)==0

def field(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=field(r);c=f[':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def values(r):return sorted(a[':answer/value'] for a in field(r)[':answer-field/choices'])
def validate(r):
 q=r['question']; F=S.cancel(rhs(q).subs(y,v*x)); expected=(F-v)/x
 f=field(r);aa=f[':answer-field/choices'];actual=[rate(a[':answer/value']) for a in aa]
 matches=[i for i,t in enumerate(actual) if equal(t,expected)]
 assert len(matches)==1,(q[':question/id'],'key multiplicity',matches)
 assert aa[matches[0]][':answer/id']==correct(r)[':answer/id']
 assert not any(equal(a,b) for i,a in enumerate(actual) for b in actual[:i])
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S);assert len(blocks)==2
 n=0
 for block in blocks:
  lhs=None
  for row in block.split(r'\\'):
   row=row.replace('&','').strip().rstrip('.')
   left,right=row.split('=')
   if left.strip():lhs=left
   residual=(readmath(lhs)-readmath(right)).subs(y,v*x).subs(z,expected)
   assert equal(residual,0),(q[':question/id'],'bad solution row',row,str(residual))
   n+=1
 return {'id':q[':question/id'],'template':r.get('generation',{}).get('template'),'parameters':r.get('generation',{}).get('parameters'),'correct_position':matches[0]+1,'derived_rate':str(expected),'solution_rows':n}

def main():
 source=json.load(open(J/'source/source.json'));srcs=source['material']['kp'][':knowledge-point/questions']
 rows=[];replay=[];pairs=[];boundary=[]
 for src in srcs:
  t=src[':question/math-academy-id'];k0=g.ORIGINAL[t]
  r=g.generate('easy',92831,t,{'k':k0,'shift':0});rows.append(r)
  q=r['question'];old=src[':question/answer-fields'][0]
  assert q[':question/problem']==src[':question/problem'] and q[':question/worked-solution']==src[':question/worked-solution']
  assert values(r)==sorted(a[':answer/value'] for a in old[':answer-field/choices'])
  assert correct(r)[':answer/value']==old[':answer-field/correct'][':answer/value']
  replay.append({'source_id':src[':question/id'],'template':t,'exact_prompt':True,'exact_solution':True,'all_five_choices':True,'correct_equation':True})
  # Fixed family and k; all relevant residual assignments. Avoid replay boundaries.
  k=5 if k0!=5 else 4
  family=[g.generate('easy',92831,t,{'k':k,'shift':s}) for s in [-2,-1,0,1,2]]
  rows+=family
  before=family[1];after=family[3]
  assert equal(rhs(after['question'])-rhs(before['question']),2*y/x)
  assert equal(rate(correct(after)[':answer/value'])-rate(correct(before)[':answer/value']),2*v/x)
  assert values(before)==values(after)
  irrelevant=g.generate('easy',184723,t,{'k':k,'shift':1});rows.append(irrelevant)
  assert irrelevant['question'][':question/problem']==after['question'][':question/problem']
  assert irrelevant['question'][':question/worked-solution']==after['question'][':question/worked-solution']
  assert values(irrelevant)==values(after) and correct(irrelevant)[':answer/value']==correct(after)[':answer/value']
  pairs.append({'template':t,'before':before['question'][':question/id'],'after':after['question'][':question/id'],'irrelevant':irrelevant['question'][':question/id'],'relevant_change':'shift -1 to +1; only +2y/x evidence changes','expected_rate_delta':str(2*v/x),'irrelevant_change':'seed 92831 to 184723; option order may change','response_preserved':True})
  for k in [min(g.DOMAINS[t]),max(g.DOMAINS[t])]:
   r=g.generate('easy',92831,t,{'k':k,'shift':2});rows.append(r);boundary.append(r['generation'])
 save('source-replay.json',replay);save('independent-records.json',rows);save('counterfactuals.json',pairs)
 batch=json.load(open(E/'batch-records.json')); math=[]
 for r in rows+batch:
  math.append(validate(r))
 save('math-results.json',{'status':'passed','records':len(math),'solution_rows':sum(r['solution_rows'] for r in math),'results':math,'method':'Parse displayed RHS, substitute y=vx, compute (F(v)-v)/x independently of generation metadata. Exact symbolic equality for correct equations; rational-point witnesses or symbolic reduction for incorrect options. Check every displayed worked equation.'})
 # Demonstrate that our check catches the historical grouping and stale-solution defects.
 import copy
 broken=copy.deepcopy(rows[1]);broken['question'][':question/worked-solution']=rows[0]['question'][':question/worked-solution']
 try:validate(broken)
 except AssertionError as e:stale=str(e)
 else:raise AssertionError('Stale negative control accepted')
 assert not equal(rate('v+1'+DV+'=1/x'),1/(x*(v+1)))
 save('negative-controls.json',{'stale_solution_rejected':stale,'ungrouped_additive_coefficient':'v+1'+DV+'=1/x','grouped_intended_rate':'1/(x*(v+1))','ungrouped_actual_rate':str(rate('v+1'+DV+'=1/x'))})
 errors=[]
 for kw in [{'difficulty':'hard'},{'parameters':{'k':0}},{'parameters':{'k':8}},{'parameters':{'k':1.5}},{'parameters':{'k':2,'shift':3}},{'parameters':{'k':2,'shift':-3}},{'parameters':{'k':2,'shift':.5}},{'template':'q-90600','parameters':{'k':6,'shift':0,'bank_start':1}}]:
  try:g.generate(**kw)
  except ValueError as e:errors.append({'input':kw,'rejected':str(e)})
  else:raise AssertionError(('invalid input accepted',kw))
 fresh=g.batch('easy',17,721097)
 assert fresh==g.batch('easy',17,721097)
 assert len({r['generation']['parameter_fingerprint'] for r in fresh})==17
 save('fresh-batch.json',fresh)
 save('sampling.json',{'fresh_seed':721097,'fresh_batch_size':17,'deterministic':True,'distinct_prompt_mathematics':17,'boundary_records':boundary,'rejections':errors,'construction':'No rejection loop. batch() enumerates 240 family/k/shift tasks, prioritizes source decompositions, collapses equal F(v), then shuffles and samples without replacement. generate() uses cancellation windows only at shift=0 in three families; other authored banks use all five linear assignments.','scope':'Same homogeneous operators, product rule and separation. Added linear terms preserve rational degree and familiar subtraction workload. Finite positive coefficient ranges are conservative arithmetic choices, not fixed key roles.'})
 # Actual radio grading of all options; no free-entry equivalence capability is needed.
 cases=[]
 for i,r in enumerate(rows+batch+fresh):
  cid=correct(r)[':answer/id'];checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'Displayed equation independently derived from actual prompt'} for a in field(r)[':answer-field/choices']]
  cases.append({'label':str(i)+':'+r['question'][':question/id'],'record':r,'checks':checks})
 save('grader-input.json',cases)
 p=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-report.json')],capture_output=True,text=True)
 save('grader-command.json',{'command':p.args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0
 # Captured originals are NOT generated records. Audit without relabelling.
 inv=json.load(open(J/'source/inventory.json'));audit=[]
 for q in inv['questions']:
  audit.append(validate({'question':q}))
 save('inventory-audit.json',{'basis':inv['basis'],'tested_records':audit,'status':'all eight stored original records checked for displayed mathematics and historical grouping defect; no generated records in captured inventory','original_status_preserved':True})
 save('affected-inventory.json',{'affected_questions':[]})
 save('review-milestone.json',{'status':'independent checks completed','source_replays':len(replay),'math_records':len(math),'native_grader_records':len(cases)})
 (E/'session-state.md').write_text('Source-first analysis saved. Retained checks copied and run only inside evidence. Independent source replay, displayed math, counterfactual pairs, boundary/rejection and native radio grading completed. Delivery, selection, rendering and final shortcut assessment remain.\n')
 print(json.dumps({'source_replays':len(replay),'math_records':len(math),'native_cases':len(cases)}),flush=True)
if __name__=='__main__':main()
