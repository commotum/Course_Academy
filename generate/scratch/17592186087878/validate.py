#!/usr/bin/env python3
"""Independent displayed-math, source fidelity, identity and native grader audit."""
from pathlib import Path
import importlib.util,json,re,hashlib,subprocess,difflib,sys
import sympy as sp
ROOT=Path(__file__).resolve().parent
SCRIPT=ROOT.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,C=g.x,g.C;y=sp.Symbol('y');Z=sp.Symbol('Z')

def parse(text):
 # Independent recursive TeX reader with substitution symbols. The generator's
 # collision helper is not used for source/value correctness verification.
 text=text.replace('\\\\','\\').replace('⁡','').replace('−','-')
 text=re.sub(r'\\operatorname\{(sin|cos|ln)\}',r'\\\1 ',text)
 text=text.replace(r'\log',r'\ln').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\,','').replace(' ','').strip('.')
 ts=re.findall(r'\\(?:frac|sin|cos|ln)|\d+|[A-Za-z]|[^\s]',text);i=0
 def group():
  nonlocal i
  if ts[i] in ('{','('):
   closing='}' if ts[i]=='{' else ')';i+=1;v=expr();assert ts[i]==closing,(text,ts[i]);i+=1;return v
  return atom()
 def atom():
  nonlocal i
  t=ts[i];i+=1
  if t==r'\frac':return group()/group()
  if t in (r'\sin',r'\cos',r'\ln'):
   v=group()
   if v.is_number and i<len(ts) and ts[i]=='x':i+=1;v*=x
   return {r'\sin':sp.sin,r'\cos':sp.cos,r'\ln':sp.log}[t](v)
  if t in ('{','('):i-=1;return group()
  if t in ('-','+'):return (-1 if t=='-' else 1)*atom()
  if t.isdigit():return sp.Integer(t)
  return {'x':x,'y':y,'Z':Z,'C':C,'e':sp.E}[t]
 def factor():
  nonlocal i
  v=atom()
  if i<len(ts) and ts[i]=='^':i+=1;v=v**group()
  return v
 def prod():
  nonlocal i
  v=factor()
  while i<len(ts) and ts[i] not in ('+','-','}',')'):
   t=ts[i]
   if t in ('*','/'):i+=1;w=factor();v=v*w if t=='*' else v/w
   else:v*=factor()
  return v
 def expr():
  nonlocal i
  v=prod()
  while i<len(ts) and ts[i] in ('+','-'):
   t=ts[i];i+=1;w=prod();v=v+w if t=='+' else v-w
  return v
 result=expr();assert i==len(ts),(text,i);return result

def eqfamily(a,b):
 A,B=sp.diff(a,C),sp.diff(b,C)
 if A==0 or B==0:return False
 return sp.simplify(sp.diff(A/B,x))==0 and sp.simplify(sp.diff((a.subs(C,0)-b.subs(C,0))/B,x))==0

def sameIF(a,b):return a!=0 and b!=0 and sp.simplify(sp.diff(a/b,x))==0

def printed_ode(record):
 prompt=record['question'][':question/problem'];components=re.findall(r'\$\$.*?\$\$|\$[^$]*\$',prompt,re.S)
 equation=components[0].strip('$\n').split(',')[0].strip('.')
 equation=equation.replace(g.D,'Z').replace(r'\frac{dy}{dx}','Z')
 left,right=equation.split('=');L,R=parse(left),parse(right)
 a=sp.expand(L).coeff(Z);P=sp.expand(L).coeff(y)/a;Q=R/a
 assert a!=0 and sp.expand(L-a*Z-a*P*y)==0
 return P,Q

def check_format(text):
 assert text.count('$')%2==0
 depth=0
 for char in text:
  if char=='{':depth+=1
  elif char=='}':depth-=1
  assert depth>=0,text
 assert depth==0,text
 assert not re.search(r'\+\-|\-\-',text)


def eval_stage(text,P,Q,I,Y,preserve_constant=False):
 text=text.strip().rstrip('.')
 for old,val in [('P(x)',P),('Q(x)',Q),('I(x)',I)]:text=text.replace(old,'('+sp.latex(val)+')')
 text=text.replace(g.D,'('+sp.latex(sp.diff(Y,x))+')')
 prefixes=[g.DP,r'\frac{d}{dx}']
 for prefix in prefixes:
  while prefix in text:
   start=text.index(prefix);openpos=start+len(prefix);assert text[openpos]=='('
   depth=0
   for end in range(openpos,len(text)):
    if text[end]=='(':depth+=1
    elif text[end]==')':depth-=1
    if depth==0:break
   inside=text[openpos+1:end]
   value=sp.simplify(sp.diff(parse(inside).subs(y,Y).subs(C,0),x))
   text=text[:start]+'('+sp.latex(value)+')'+text[end+1:]
 # Replace indefinite integrals with a C=0 representative. Intermediate source
 # rows omit the arbitrary constant before their explicit antiderivative row.
 while r'\int ' in text:
  match=re.search(r'\\int (.*?)(?:\\,)?(?:\\text\{d\}x|dx)',text)
  assert match,text
  val=sp.integrate(sp.simplify(parse(match[1]).subs(y,Y).subs(C,0)),x)
  text=text[:match.start()]+'('+sp.latex(val)+')'+text[match.end():]
 value=parse(text).subs(y,Y)
 return value if preserve_constant else value.subs(C,0)


def validate_record(record):
 assert set(record)=={'knowledge_point','question','generation'}
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 q=record['question'];P,Q=printed_ode(record);fields=q[':question/answer-fields'];correct={};stagecount=0
 assert len(fields)==2 and {f[':answer-field/key'] for f in fields}=={'field-1','field-2'}
 for f in fields:
  key=f[':answer-field/key'];assert f[':answer-field/type']==':answer-field.type/select'
  assert '{{'+key+'}}' in q[':question/problem']
  values=[];hits=[]
  for a in f[':answer-field/choices']:
   check_format(a[':answer/value']);assert '$' not in a[':answer/value'];v=parse(a[':answer/value']);values.append(v)
   if key=='field-1':valid=v!=0 and sp.simplify(sp.diff(v,x)-P*v)==0
   else:valid=sp.simplify(sp.diff(v,x)+P*v-Q)==0 and sp.diff(v,C)!=0
   if valid:hits.append(a[':answer/id']);correct[key]=v
  assert hits==[f[':answer-field/correct'][1]],(record['generation'],key,hits)
  for i,a in enumerate(values):
   for b in values[i+1:]:assert not (sameIF(a,b) if key=='field-1' else eqfamily(a,b)),('equivalent bank',key)
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(values)
 Y=correct['field-2'].subs(C,0);I=correct['field-1']
 for text in [q[':question/problem'],q[':question/worked-solution']]:check_format(text)
 # Verify actual printed ordered rows, including the first distributed sum.
 for body in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S):
  prev=None
  for row in body.split('\\\\'):
   left,right=row.split('& =');left=left.strip();right=right.strip()
   if not left:left=prev
   prev=left
   preserve_constant='C' in right
   stageY=correct['field-2'] if preserve_constant else Y
   a=eval_stage(left,P,Q,I,stageY,preserve_constant);b=eval_stage(right,P,Q,I,stageY,preserve_constant)
   assert sp.simplify(a-b)==0,(record['generation'],left,right,sp.simplify(a-b))
   stagecount+=1
 # Full C-dependent final row must agree with the correct solution family.
 finals=re.findall(r'\by & =(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
 assert len(finals)>=1
 assert eqfamily(parse(finals[-1].rstrip('.')),correct['field-2'])
 return stagecount


def native_item(label,record):
 checks=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Entire owned select bank'})
 return {'label':label,'record':record,'checks':checks}


def main():
 cases=json.loads((ROOT/'source-cases.json').read_text());records=[];rawbanks=0;rawchoices=0;normalchoices=0;designations=0;solution_exact=0;prompt_exact=0;stages=0;math_wrong_total=0;math_wrong_normal=0;coverage=[]
 for case in cases:
  print('Source replay:',case['source_id'],flush=True)
  t=case['template'];s=g.TEMPLATES[t];source=g.QUESTIONS[case['source_id']]
  rawrecord=g.generate(s['level'],template=t,parameters=case['parameters'],profile=case['original_bank_profile'])
  raw={'banks':{f[':answer-field/key']:[a[':answer/value'] for a in f[':answer-field/choices']] for f in rawrecord['question'][':question/answer-fields']}}
  rec=g.generate(s['level'],template=t,parameters=case['parameters'],profile=case['bank_profile'])
  stages+=validate_record(rec);records.append(native_item(case['source_id'],rec));entry={'source_id':case['source_id'],'fields':[]}
  sourceP,sourceQ=printed_ode(rec)
  if rec['question'][':question/problem']==source[':question/problem']:prompt_exact+=1
  else:raise AssertionError('Prompt fidelity')
  if ':question/worked-solution'in source:
   assert rec['question'][':question/worked-solution']==source[':question/worked-solution'];solution_exact+=1
  for sf in source[':question/answer-fields']:
   key=sf[':answer-field/key'];original=[parse(a[':answer/value']) for a in sf[':answer-field/choices']];rendered=[parse(v) for v in raw['banks'][key]]
   unmatched=list(rendered)
   for value in original:
    hit=next((i for i,v in enumerate(unmatched) if sp.simplify(value-v)==0),None);assert hit is not None,(case,key,value);unmatched.pop(hit);rawchoices+=1
   assert not unmatched;rawbanks+=1
   nf=next(f for f in rec['question'][':question/answer-fields'] if f[':answer-field/key']==key)
   normal=[parse(a[':answer/value']) for a in nf[':answer-field/choices']];nmatch=sum(any(sp.simplify(v-w)==0 for w in normal) for v in original)
   # One-to-one matches, so a duplicated source correct answer counts only once.
   unmatched=list(normal);nmatch=0
   for value in original:
    hit=next((i for i,v in enumerate(unmatched) if sp.simplify(value-v)==0),None)
    valid=(value!=0 and sp.simplify(sp.diff(value,x)-sourceP*value)==0) if key=='field-1' else (sp.simplify(sp.diff(value,x)+sourceP*value-sourceQ)==0 and sp.diff(value,C)!=0)
    if not valid:math_wrong_total+=1;math_wrong_normal+=hit is not None
    if hit is not None:nmatch+=1;unmatched.pop(hit)
   normalchoices+=nmatch
   if ':answer-field/correct'in sf:
    expected=parse(sf[':answer-field/correct'][':answer/value']);actual=parse(next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]));assert sp.simplify(expected-actual)==0;designations+=1
   entry['fields'].append({'key':key,'raw_matched':len(original),'normal_matched':nmatch,'total':len(original),'stored_designation':':answer-field/correct'in sf})
  coverage.append(entry)
 review=[];tasks={level:set() for level in ['easy','moderate','hard']}
 for t,s in g.TEMPLATES.items():
  print('Printed mathematics:',t,flush=True)
  for seed in range(12):
   rec=g.generate(s['level'],seed,template=t);stages+=validate_record(rec);records.append(native_item(t+':'+str(seed),rec));tasks[s['level']].add(rec['generation']['parameter_fingerprint'])
   if seed<2:review.append(rec)
  # Fixed explicit parameters preserve identity across seed/order changes.
  r1=g.generate(s['level'],11,template=t,parameters=s['base']);r2=g.generate(s['level'],90,template=t,parameters=s['base']);assert r1['question'][':question/id']==r2['question'][':question/id']
  bad=dict(s['base']);key=next(iter(bad));bad[key]=99
  try:g.generate(s['level'],template=t,parameters=bad)
  except ValueError:pass
  else:raise AssertionError('Explicit bounds bypass')
 # Every valid source profile gets changed-parameter exercise as well.
 for name,p in g.PROFILES.items():
  if name=='q-335409':continue # Raw equivalent duplicate is explicitly rejected.
  s=g.TEMPLATES[p['template']]
  rec=g.generate(s['level'],22,profile=name);stages+=validate_record(rec);records.append(native_item('profile:'+name,rec))
 try:g.generate('hard',template='power_sin',profile='q-335409')
 except g.SampleRejected:pass
 else:raise AssertionError('Raw ambiguous source bank needs explicit parameters')
 # Family semantics explicitly exercise C scaling and shifting, and IF scaling.
 assert eqfamily(C*sp.exp(3*x), (2*C+7)*sp.exp(3*x))
 assert not eqfamily(C*sp.exp(3*x),C*sp.exp(-3*x))
 assert sameIF(2*x**3,x**3)
 for level,bank in tasks.items():assert len(bank)>=15,(level,len(bank))
 (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 sections=['# Source originals and generated variants','\nRaw originals below are evidence, including their recorded anomalies.']
 for case in cases:
  q=g.QUESTIONS[case['source_id']];sections+=['\n## Original '+case['source_id'],q[':question/problem']]
  for f in q[':question/answer-fields']:
   sections+=['\n**'+f[':answer-field/key']+' raw bank**']+['- `'+a[':answer/value']+'`' for a in f[':answer-field/choices']]
  sections+=['\n**Raw worked solution**',q.get(':question/worked-solution','Not captured; generated solution is authored.')]
  for r in review:
   if r['generation']['template']==case['template']:sections+=['\n### Generated variant (authored bank)',g.markdown(r)]
 for r in review:
  if r['generation']['template']=='power_cos':sections+=['\n### Authored cosine peer (canonical example e-21742)',g.markdown(r)]
 (ROOT/'review.md').write_text('\n\n'.join(sections)+'\n')
 (ROOT/'engine-input.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
 engine=Path('generate/runs/current/check-engine')
 subprocess.run([str(engine),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 engine_report=json.loads((ROOT/'engine-report.json').read_text())
 report={'status':'pass-with-documented-source-anomalies','database':g.SOURCE['database'],'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'source_questions':len(cases),'source_prompt_exact':{'matched':prompt_exact,'total':8},'captured_worked_solution_exact':{'matched':solution_exact,'total':5},'missing_worked_solutions':3,'raw_extraction_bank_fidelity':{'matched':rawbanks,'total':16,'choice_values_matched':rawchoices,'choice_values_total':65},'normal_replay_choice_fidelity':{'matched':normalchoices,'total':65,'complete_banks':15,'total_banks':16,'repair':'One duplicated correct option in q-335409 replaced; all five original source stages retained.'},'mathematically_wrong_source_options':{'normal_matched':math_wrong_normal,'total':math_wrong_total,'qualification':'Determined independently from displayed ODE; missing source designations are not inferred matches.'},'stored_correct_designations':{'matched':designations,'total_present':10,'missing':6,'missing_not_counted_as_matched':True},'independently_derived_designations':6,'validated_printed_math_stages':stages,'sampled_task_counts':{k:len(v) for k,v in tasks.items()},'native_grading':{k:engine_report[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks','database_writes']},'native_binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'source_coverage':coverage,'scope':'General solutions only; two select fields; no initial value conditions or substitutions; no plots.','unresolved_findings':['Original hard bank is ambiguous; explicit fixed-parameter evidence-only replay is available; normal authored/repaired records remain unique. Six stored correct refs and three worked solutions absent; generated repairs are independently derived, not source matches.']}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='source_coverage'},indent=2))
if __name__=='__main__':main()
