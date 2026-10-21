import json,pathlib,re,copy,hashlib,collections
import sympy as S
R=pathlib.Path(__file__).resolve().parent
read=lambda n:json.load(open(R/n))
def save(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False))
x,y,v=S.symbols('x y v',real=True)
# A review-owned recursive TeX reader. Author parser/validator is never called here.
def group(t,pos):
 assert t[pos]=='{';depth=1;end=pos+1
 while depth:
  depth+=(t[end]=='{')-(t[end]=='}');end+=1
 return t[pos+1:end-1],end

def compile_tex(t):
 t=t.replace(r'\frac{\text{d}y}{\text{d}x}','v').replace(r'\cdot','*').replace(r'\,','').replace(r'\text{ }','').replace(r'\left','').replace(r'\right','').replace('⁡','')
 t=re.sub(r'\\operatorname\{(sin|csc)\}([0-9]*x)',lambda m:' '+m[1]+'('+m[2]+')',t).strip().rstrip('.,')
 out='';i=0
 while i<len(t):
  if t.startswith('\\frac',i):
   top,j=group(t,i+5);bot,i=group(t,j);out+='(('+compile_tex(top)+')/('+compile_tex(bot)+'))'
  elif t.startswith('\\sqrt',i):
   a,i=group(t,i+5);out+='sqrt('+compile_tex(a)+')'
  elif t[i]=='{':
   a,i=group(t,i);out+='('+compile_tex(a)+')'
  elif t[i]=='^':out+='**';i+=1
  else:out+=t[i];i+=1
 return out
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application

def expr(t):return parse_expr(compile_tex(t),local_dict={'x':x,'y':y,'v':v,'e':S.E,'sin':S.sin,'csc':S.csc,'sqrt':S.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def equation(t):
 l,r=t.split('=');return expr(l),expr(r)
def resolved(t):
 l,r=equation(t);return S.cancel((r-l.subs(v,0))/S.diff(l,v))
def same(a,b):return S.simplify(S.expand_power_exp(a-b))==0
def sep(t):
 l,r=equation(t);return S.simplify(S.diff(S.diff(l,v),x))==0 and not r.has(y,v) and l.subs(v,0)==0

def check_record(r):
 q=r['question'];prompt=re.findall(r'\$\$(.*?)\$\$',q[':question/problem'],re.S)[0];ode=resolved(prompt)
 f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];valid=[c[':answer/id'] for c in cs if sep(c[':answer/value']) and same(resolved(c[':answer/value']),ode)]
 stages=[]
 for b in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)[2:]:
  if '\\begin{aligned}' in b:
   rows=b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');lhs=None
   for row in rows:
    row=row.replace('&','').strip()
    if row.startswith('='):row=lhs+row
    else:lhs=row.split('=')[0]
    stages.append({'expression':row,'equivalent':same(resolved(row),ode)})
  else:stages.append({'expression':b.strip(),'equivalent':same(resolved(b),ode)})
 return {'id':q[':question/id'],'template':r['generation']['template'],'valid_choices':valid,'stored_key':f[':answer-field/correct'][1],'passed':valid==[f[':answer-field/correct'][1]] and all(z['equivalent'] for z in stages),'stages':stages}

records=read('independent-records.json');batch=read('batch.json');pairs=read('counterfactual-records.json');sources=read('source-replay-records.json')
results=[check_record(r) for r in records+batch+pairs+sources];save('math-results.json',{'method':'Independent recursive parsing of rendered equation strings, exact symbolic equation equivalence and separation, every solution stage. No author validation result used.','cases':results,'passed':all(c['passed'] for c in results)})
# Check every choice, including equivalent but unseparated distractors, via the native learner grader.
cases=[]
for i,r in enumerate(records+batch+pairs+sources):
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 cases.append({'label':str(i)+'/'+r['generation']['template'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key else 'rejected','purpose':'Independently established separated equivalent' if c[':answer/id']==key else 'Plausible incorrect or equivalent-but-unseparated equation'} for c in f[':answer-field/choices']]})
# Actual grading is ID-based for these radio fields; arbitrary free-entry equivalence is inapplicable.
save('grader-input.json',cases)
# Individual/conditional shortcut probes, retaining every selected option and outcome.
def probes(rs,label):
 allrows=[]
 for name,choose in [('first',lambda cs:0),('last',lambda cs:4),('shortest',lambda cs:min(range(5),key=lambda i:len(cs[i][':answer/value']))),('longest',lambda cs:max(range(5),key=lambda i:len(cs[i][':answer/value'])))]:
  for r in rs:
   f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];idx=choose(cs)
   allrows.append({'pool':label,'strategy':name,'template':r['generation']['template'],'id':r['question'][':question/id'],'chosen_index':idx,'chosen':cs[idx][':answer/value'],'success':cs[idx][':answer/id']==f[':answer-field/correct'][1]})
 return allrows
save('shortcut-results.json',probes(records,'control')+probes(batch,'batch'))
# Derivative-side y-only and x-only right-side is the taught skill, not an incidental shortcut.
roles=[]
for r in records+batch:
 f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];roles.append({'pool':'batch' if r in batch else 'control','id':r['question'][':question/id'],'template':r['generation']['template'],'eligible_by_separation_alone':sum(sep(c[':answer/value']) for c in cs),'position':next(i for i,c in enumerate(cs) if c[':answer/id']==f[':answer-field/correct'][1])})
save('decision-cases.json',roles)
# Renderer covers exact batch, all relevant/irrelevant pairs, and each other template once.
render=batch+pairs
for t in sorted(set(r['generation']['template'] for r in records)):
 render.append(next(r for r in records if r['generation']['template']==t))
save('render-records.json',render)
save('counterfactual-results.json',{'relevant':{'before_parameters':pairs[0]['generation']['parameters'],'after_parameters':pairs[1]['generation']['parameters'],'prompt_changed':pairs[0]['question'][':question/problem']!=pairs[1]['question'][':question/problem'],'solution_changed':pairs[0]['question'][':question/worked-solution']!=pairs[1]['question'][':question/worked-solution'],'key_expression_before':next(c[':answer/value'] for c in pairs[0]['question'][':question/answer-fields'][0][':answer-field/choices'] if c[':answer/id']==pairs[0]['question'][':question/answer-fields'][0][':answer-field/correct'][1]),'key_expression_after':next(c[':answer/value'] for c in pairs[1]['question'][':question/answer-fields'][0][':answer-field/choices'] if c[':answer/id']==pairs[1]['question'][':question/answer-fields'][0][':answer-field/correct'][1])},'irrelevant':{'seed_before':8102,'seed_after':8103,'prompt_preserved':pairs[0]['question'][':question/problem']==pairs[2]['question'][':question/problem'],'solution_preserved':pairs[0]['question'][':question/worked-solution']==pairs[2]['question'][':question/worked-solution'],'key_preserved':pairs[0]['question'][':question/answer-fields'][0][':answer-field/correct']==pairs[2]['question'][':question/answer-fields'][0][':answer-field/correct'],'choice_order_changed':pairs[0]['question'][':question/answer-fields'][0][':answer-field/choices']!=pairs[2]['question'][':question/answer-fields'][0][':answer-field/choices']}})
print('independent math',len(results),'passed',all(c['passed'] for c in results),'grader cases',len(cases),'render cases',len(render))
