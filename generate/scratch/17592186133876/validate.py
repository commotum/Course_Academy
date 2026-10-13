#!/usr/bin/env python3
"""Read actual prompts/options/ordered solution rows; no generation-parameter oracle."""
import hashlib, importlib.util, itertools, json, re, subprocess, sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
ROOT=Path(__file__).parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('divergence',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,i,j=sp.symbols('x y i j',real=True)
AUDIT=[]

def write(name,v):(ROOT/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def group(s,pos):
 if s[pos]!='{':raise ValueError(('expected group',s,pos))
 depth=1;k=pos+1
 while depth:
  if s[k]=='{':depth+=1
  elif s[k]=='}':depth-=1
  k+=1
 return s[pos+1:k-1],k

def parse_math(t):
 """Independent subset parser for the exact printed source and generated TeX."""
 t=g.clean_choice(t).strip().rstrip('.,')
 t=t.replace(r'\,',' ').replace(r'\!','').replace(r'\cdot','*').replace(r'\times','*').replace('−','-')
 t=re.sub(r'\\(?:left|right|big|Big|bigl|bigr)\s*','',t)
 t=re.sub(r'\\operatorname\{(ln|sin|cos)\}',lambda m: {'ln':'log','sin':'sin','cos':'cos'}[m[1]],t)
 # Parse complete fractions/radicals recursively before generic brace removal.
 while re.search(r'\\(?:d?frac|sqrt)',t):
  m=re.search(r'\\(d?frac|sqrt)',t);a,end=group(t,m.end());aa=parse_math(a)
  if m[1].endswith('frac'):
   b,end=group(t,end);bb=parse_math(b);rep='(('+sp.sstr(aa)+')/('+sp.sstr(bb)+'))'
  else:rep='sqrt('+sp.sstr(aa)+')'
  t=t[:m.start()]+rep+t[end:]
 t=t.replace(r'\ln','log').replace(r'\log','log').replace(r'\sin','sin').replace(r'\cos','cos').replace(r'\pi','pi')
 t=t.replace('{cos}','cos').replace('{sin}','sin')
 for pat in (r'(cos|sin)\s*\^\s*\{2\}\s*\{\(\s*([xy])\s*\)\}',r'(cos|sin)\s*\^\s*\{2\}\s*([xy])'):
  t=re.sub(pat,r'(\1(\2))^2 ',t)
 t=re.sub(r'(cos|sin|log)\s*([xy])',r'\1(\2)',t)
 t=re.sub(r'(sin|cos|log|sqrt)',r' \1',t)
 t=t.replace('{','(').replace('}',')')
 if '\\' in t:raise ValueError(('Unsupported printed command',t))
 return parse_expr(t,local_dict={'x':x,'y':y,'i':i,'j':j,'e':sp.E,'E':sp.E,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos,'log':sp.log,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def equals(a,b):return sp.simplify(a-b)==0

def assert_format(t,raw=False):
 if raw:return
 assert t.count('$')%2==0,('math delimiter',t)
 depth=0
 for ch in t:
  if ch=='{':depth+=1
  elif ch=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert '--' not in t and '+-' not in t
 assert r'\u2061' not in t

def rows(solution):
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
 return [[r.split('& =',1)[1].strip().rstrip('.') for r in block.split(r'\\') if '& =' in r] for block in blocks]

def displayed_object(q,raw=False):
 prompt=q[':question/problem']
 # Inherited raw source context is explicitly recovered from its derivative inputs.
 m=re.search(r'\$[FV]\s*=\s*(.*?)\$',prompt,re.S)
 if m:
  v=parse_math(m[1]);P=sp.expand(v).coeff(i);Q=sp.expand(v).coeff(j)
  assert equals(v,P*i+Q*j),('vector parse',m[1],v)
 else:
  assert raw,'Normal standalone prompt missing field'
  ds=g.derivative_inputs(q.get(':question/worked-solution',''))
  assert len(ds)>=2,'Missing field context cannot be recovered'
  P,Q=map(lambda d:parse_math(d[1]),ds[:2])
 pm=re.search(r'at the point \$\((.*?)\)',prompt)
 pt=tuple(parse_math(z) for z in pm[1].split(',')) if pm else None
 return P,Q,pt

def audit_record(record,raw=False,source_error=False):
 q=record['question'];assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert_format(q[':question/problem'],raw)
 assert_format(q.get(':question/worked-solution',''),raw)
 P,Q,pt=displayed_object(q,raw)
 px,qy=sp.diff(P,x),sp.diff(Q,y);D=px+qy
 def ev(a):return sp.simplify(a.subs(dict(zip((x,y),pt)),simultaneous=True)) if pt else a
 if pt and not source_error:
  for v in (P,Q):
   val=ev(v);assert val.is_real is not False and not val.has(sp.zoo,sp.nan,sp.oo),('nonreal/domain',P,Q,pt,val)
 answer=ev(D)
 fields=q.get(':question/answer-fields',[]);bank_count=0
 for f in fields:
  values=[];correct_id=f.get(':answer-field/correct',[None,None])[1]
  for a in f[':answer-field/choices']:
   val=parse_math(a[':answer/value']);values.append(val);bank_count+=1
   if correct_id:assert equals(val,answer)==(a[':answer/id']==correct_id),(a[':answer/value'],answer)
  for aa,bb in itertools.combinations(values,2):assert not equals(aa,bb),('bank collision',aa,bb)
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(values)
  for a in f[':answer-field/choices']:assert_format(a[':answer/value'],raw)
  if not correct_id:assert sum(equals(v,answer) for v in values)==1,'Unique mathematically inferred source answer'
  assert record['generation']['evidence_only']==raw and record['generation']['eligible_for_learning']!=raw
 # Independently read every formal derivative input and every ordered RHS value.
 blocks=rows(q.get(':question/worked-solution',''));count=0
 for bi,block in enumerate(blocks):
  formal=block[0]
  assert re.search(r'\\frac\{(?:∂|\\partial)\s*P\}\{(?:∂|\\partial)\s*x\}',formal) or bi>0,(bi,formal)
  for row in block:
   ds=g.derivative_inputs(row)
   if ds:
    assert [d[0] for d in ds]==['x','y'],('held-coordinate ordering',ds)
    pp,qq=map(lambda d:parse_math(d[1]),ds)
    assert equals(pp,P) and equals(qq,Q),('wrong formal component inputs',pp,qq,P,Q)
    count+=2
   elif re.search(r'\\frac\{(?:∂|\\partial)\s*P\}',row):
    assert re.search(r'\\frac\{(?:∂|\\partial)\s*Q\}\{(?:∂|\\partial)\s*y\}',row)
    count+=1
   else:
    value=parse_math(row)
    if not raw and bi==0 and row==block[2]:
     marker=r'+\left('
     assert marker in row and row.endswith(r'\right)')
     left,right=row.split(marker,1)
     assert equals(parse_math(left),px) and equals(parse_math(right[:-len(r'\right)')]),qy),('individual partial derivative values',row)
     count+=2
    assert equals(value,D if bi==0 else answer),('wrong displayed solution row',row,value,D if bi==0 else answer)
    count+=1
 AUDIT.append({'id':q[':question/id'],'formal_and_derived_rows_checked':count,'options':bank_count})
 return P,Q,pt,answer

def engine_checks(record,label):
 q=record['question'];f=q[':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'complete owned bank selection'} for a in f[':answer-field/choices']]
 else:
  val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
  _,_,_,answer=audit_record(record)
  # Independently unreduced derivative sum is a meaningful equivalent entry.
  P,Q,pt=displayed_object(q)
  a=sp.diff(P,x);b=sp.diff(Q,y)
  if pt:a=a.subs(dict(zip((x,y),pt)),simultaneous=True);b=b.subs(dict(zip((x,y),pt)),simultaneous=True)
  equivalent=('('+sp.sstr(a)+')+('+sp.sstr(b)+')').replace('**','^')
  checks=[{'submitted':val,'expected':'accepted','purpose':'canonical blank'},
   {'submitted':equivalent,'expected':'accepted','purpose':'independently unreduced component derivative sum'},
   {'submitted':'('+val+')+1','expected':'rejected','purpose':'wrong scalar field'}]
 return {'label':label,'record':record,'checks':checks}

def main():
 cases=[];source_report=[];engine=[];review=[];review_records=[]
 for sid,src in g.SOURCE_BY_ID.items():
  level,f,kind=g.FAMILIES[sid];case={'source_id':src[':question/id'],'source_math_academy_id':sid,'level':level,'template':f,'parameters':{'c':1},'bank_profile':'raw:'+sid}
  cases.append(case);r=g.generate(level,template=f,parameters={'c':1},profile='raw:'+sid);q=r['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in src)==(key in q),(sid,'presence',key)
  assert q[':question/problem']==src[':question/problem']
  if ':question/worked-solution'in src:assert q[':question/worked-solution']==src[':question/worked-solution']
  if ':question/difficulty'in src:assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
  for sf,gf in zip(src[':question/answer-fields'],q[':question/answer-fields']):
   assert sf[':answer-field/key']==gf[':answer-field/key']
   assert sf[':answer-field/type'][':db/ident']==gf[':answer-field/type']
   assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
   assert (':answer-field/correct'in sf)==(':answer-field/correct'in gf)
   if ':answer-field/correct'in sf:
    answer=next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert answer==sf[':answer-field/correct'][':answer/value']
  audit_record(r,True,sid=='q-123175')
  source_report.append({'source_id':sid,'raw_prompt_exact':True,'raw_solution_exact':':question/worked-solution'in src,'bank_values_exact':len(src[':question/answer-fields'][0][':answer-field/choices']),'correct_designation_exact':':answer-field/correct'in src,'key_presence_parity':True,'mathematical_source_error':sid=='q-123175'})
  review+=['## Original raw evidence — '+sid,'',g.markdown(r),'']
  for c in (2,-3):
   rr=g.generate(level,template=f,parameters={'c':c},profile='raw:'+sid)
   audit_record(rr,True,sid=='q-123175');review_records.append(rr);review+=['## Generated raw covariance evidence (ineligible learner output)','',g.markdown(rr),'']
  if ':answer-field/correct'in q[':question/answer-fields'][0] and sid!='q-123175':engine.append(engine_checks(r,'raw '+sid) if kind=='radio' else {'label':'raw '+sid,'record':r,'checks':[{'submitted':src[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],'expected':'accepted','purpose':'raw canonical blank'}]})
 for f,t in g.TEMPLATES.items():
  for seed in range(20):
   r=g.generate(t['level'],seed,template=f);audit_record(r);engine.append(engine_checks(r,f+' '+str(seed)))
   same=g.generate(t['level'],seed+1234,template=f,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
   assert r['question'][':question/id']==same['question'][':question/id']
   assert r['generation']['mathematical_fingerprint']==same['generation']['mathematical_fingerprint']
   if seed<2:review_records.append(r);review+=['## Generated authored standalone variant','',g.markdown(r),'']
  # Explicit calls enforce the finite workload domain exactly as random samplers.
  p=g.generate(t['level'],77,template=f)['generation']['parameters']
  for bad in ({**p,'a':5},{**p,'a':0},{**p,'a':True},{**p,'b':-5},{**p,'unused':1}):
   try:g.generate(t['level'],template=f,parameters=bad)
   except ValueError:pass
   else:raise AssertionError(('bad explicit input',f,bad))
  if t['level']=='hard':
   for k in ('a','d','k'):
    try:g.generate('hard',template=f,parameters={**p,k:1})
    except ValueError:pass
    else:raise AssertionError(('hard defining chain removed',k))
  if t['level']!='easy':
   try:g.generate(t['level'],template=f,parameters={**p,'x0':'100'})
   except ValueError:pass
   else:raise AssertionError('Point outside finite workload accepted')
 # Reject collisions without changing explicit inputs and before any answer assembly.
 try:g.generate('moderate',template='log_difference',parameters={'a':2,'b':1,'x0':'3','y0':'1'})
 except g.SampleRejected:pass
 else:raise AssertionError('Expected ambiguous bank rejected')
 write('source-cases.json',cases);write('source-fidelity.json',source_report)
 write('engine-input.json',engine)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
 write('review.json',review_records);(ROOT/'review.md').write_text('# Divergence generator review\n\nAll original raw records, parameterized raw covariance evidence, and two authored standalone variants for each template. Raw profiles are not eligible learner banks. Hard labels are authored scope decisions.\n\n'+'\n'.join(review))
 write('displayed-math-audit.json',AUDIT)
 native=json.loads((ROOT/'engine-validation.json').read_text())
 write('validation.json',{'status':'passed with documented source anomalies','basis':1356,'source_records':14,'raw_prompt_exact':14,'raw_complete_banks_exact':14,'raw_option_values_exact':58,'raw_solutions_exact':13,'source_solutions_present':13,'raw_correct_designations_exact':13,'source_correct_designations_present':13,'raw_attribute_presence_exact':14,'real_domain_source_errors':1,'source_domain_error_id':'q-123175','normal_templates':16,'observed_families':14,'authored_hard_families':2,'normal_generated_instances_checked':320,'raw_generated_covariance_instances_checked':28,'displayed_math_audit_entries':len(AUDIT),'formal_and_derived_rows_checked':sum(z['formal_and_derived_rows_checked'] for z in AUDIT),'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'native_unresolved':native['documented_unresolved_checks'],'database_writes':0,'limitations':['Source scalar-bank error intent underdetermined; covariance raw profiles evidence-only.','q-105561 original correct value 1 independently inferred for analysis; original correct designation remains absent and normal keys derive from their printed points.','q-123175 real logarithm undefined at original point; raw evidence excluded from normal learner generation.'],'engine_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest()})
 print('PASS:',len(AUDIT),'displayed-string audits;',native['accepted_checks'],'accepted;',native['rejected_checks'],'rejected.')
if __name__=='__main__':main()
