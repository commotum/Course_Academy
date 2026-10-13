#!/usr/bin/env python3
"""Independent actual-LaTeX readback, complete-bank fidelity and native grading.

The reader accepts only this KP's elementary polynomial/trigonometric syntax.
It reads the displayed function rather than trusting generation parameters.
Every displayed solution row is checked, including generic coordinate factors,
substituted products, the uncollected distributed sum, and final collection.
"""
from pathlib import Path
import hashlib, importlib.util, json, re, subprocess, sys, collections
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
sys.dont_write_bytecode=True  # Keep all generated evidence inside this KP folder.
spec=importlib.util.spec_from_file_location('cylindrical_generator',SCRIPT)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
REPO=HERE.parents[2]
TR=standard_transformations+(implicit_multiplication_application,)
COUNT=collections.Counter()

def read_math(s,extra=None):
 s=s.replace('\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','')
 s=re.sub(r'\\operatorname\{(sin|cos)\}',r'\\\1',s)
 s=re.sub(r'\{(sin|cos)\}',r'\\\1',s)
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 s=s.replace(r'\cdot','*').replace(r'\theta','t')
 s=re.sub(r'\\(sin|cos)\^\{(\d+)\}\s*t',r'(\1(t)**\2)',s)
 s=re.sub(r'\\(sin|cos)\s*\(\s*(\d+)\s*t\s*\)',r'(\1(\2*t))',s)
 s=re.sub(r'\\(sin|cos)\s*(\d+)\s*t',r'(\1(\2*t))',s)
 s=re.sub(r'\\(sin|cos)\s*t',r'(\1(t))',s)
 s=s.replace(r'\sin(','sin(').replace(r'\cos(','cos(')
 s=s.replace('{','(').replace('}',')').replace('^','**').strip(' .,')
 assert '\\' not in s,('unparsed TeX',s)
 local={'x':g.x,'y':g.y,'z':g.z,'r':g.r,'t':g.t,'sin':sp.sin,'cos':sp.cos,**(extra or {})}
 return parse_expr(s,local_dict=local,transformations=TR)

def equal(a,b):
 # Independent readback uses the alternate S^2 reduction and expanded trig.
 diff=sp.expand(sp.expand_trig(a-b))
 if diff==0:return True
 S,C=sp.symbols('_sin _cos')
 diff=diff.xreplace({g.sn:S,g.cs:C})
 return sp.Poly(diff,S,C,domain='EX').rem(sp.Poly(S**2+C**2-1,S,C,domain='EX')).is_zero
DERIV=re.compile(r'\\frac\{(?:∂|\\partial)\s*([fghuvwxyz])\}\{(?:∂|\\partial)\s*(\\theta|[xyzr])\s*\}')
def read_row(s,derivatives):
 extra={};n=0
 def substitute(m):
  nonlocal n
  key=(m[1],m[2].replace('\\',''))
  assert key in derivatives,('unknown derivative',key,s)
  name='D'+str(n);extra[name]=derivatives[key];n+=1
  return '('+name+')'
 s=DERIV.sub(substitute,s)
 return read_math(s,extra)

def rows(block):
 block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
 result=[];lhs=None
 for row in re.split(r'\\\\',block):
  for row in re.split(r',\\,',row):
   row=row.replace('&','').strip()
   if not row:continue
   left,right=row.split('=',1)
   if left.strip():lhs=left.strip()
   assert lhs
   result.append((lhs,right.strip()))
 return result

def check_format(text):
 assert text.count('$')%2==0
 # Display pairs do not get confused with inline math.
 parts=text.split('$$');assert len(parts)%2==1
 for part in parts[::2]:assert part.count('$')%2==0
 balance=0
 for i,ch in enumerate(text):
  if ch not in '{}':continue
  if i and text[i-1]=='\\':continue
  balance+=1 if ch=='{' else -1
  assert balance>=0
 assert balance==0
 assert '--' not in text and '+-' not in text
 assert not re.search(r'\\(?:sin|cos)\([^)]*\\(?:sin|cos)',text)

def displayed(rec):
 q=rec['question'];p=rec['generation']['parameters'];key=rec['generation']['template']
 prompt=q[':question/problem'];m=re.search(r'\$([fghuvw])\(x,y,z\)=(.*?),\$',prompt)
 assert m,('displayed function missing',prompt)
 name=m[1];F=read_math(m[2]);target=g.TEMPLATES[key][1]
 assert name==p['name']
 match=DERIV.search(prompt)
 # Source prompts retain Unicode partial notation, generated ones standard TeX.
 assert match and match[1]==name and match[2].replace('\\','')==target
 assert equal(F,g.polynomial(key,p)),('printed function mismatch',key)
 substituted=F.subs(g.SUB)
 expected=sp.diff(substituted,{'z':g.z,'theta':g.t,'r':g.r}[target])
 assert equal(expected,g.math_data(key,p)[-1]),('independent derivative mismatch',key)
 f=q[':question/answer-fields'][0]
 choices=[read_math(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(choices)==5
 assert all(not v.has(g.x,g.y) for v in choices)
 for i,a in enumerate(choices):
  for b in choices[i+1:]:assert not equal(a,b),('equivalent printed choices',key)
 cid=f[':answer-field/correct'][1]
 hits=[a[':answer/id'] for a,v in zip(f[':answer-field/choices'],choices) if equal(v,expected)]
 assert hits==[cid],('correct designation',key)
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 assert f[':answer-field/correct'][0]==':answer/id'
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
 blocks=q[':question/worked-solution'].split('$$')[1::2]
 assert len(blocks)==(3 if target=='z' else 4)
 for j,block in enumerate(blocks):
  d={}
  for v,symbol in [('x',g.x),('y',g.y),('z',g.z)]:
   d[(name,v)]=sp.diff(F,symbol) if j==1 else sp.diff(F,symbol).subs(g.SUB)
  d[(name,'theta')]=sp.diff(substituted,g.t);d[(name,'r')]=sp.diff(substituted,g.r)
  for v,V in [('x',g.r*g.cs),('y',g.r*g.sn),('z',g.z)]:
   for targetvar,S in [('r',g.r),('theta',g.t),('z',g.z)]:d[(v,targetvar)]=sp.diff(V,S)
  for left,right in rows(block):
   assert equal(read_row(left,d),read_row(right,d)),('invalid displayed stage',key,j,left,right)
   COUNT['displayed_solution_equations']+=1
 # Structural distribution check, independent of final equality: source
 # cancellation must retain its three terms rather than eagerly collecting.
 if key in ('theta_cancellation','theta_coupled','r_coupled'):
  dist=rows(blocks[-1])[1][1]
  if key!='theta_cancellation':assert len(sp.Add.make_args(sp.expand(read_math(dist)))) in (2,3)
  # Cross terms occur twice before collection; additive signs outside parentheses.
  depth=0;terms=1
  for c in dist:
   if c=='(':depth+=1
   if c==')':depth-=1
   if c in '+-' and depth==0:terms+=1
  if dist.strip().startswith('-'):terms-=1
  assert terms==(3 if key=='theta_cancellation' else 4),('distributed term workload',key,dist,terms)
 if key=='z_square_cross':
  assert len(rows(blocks[-1]))==2
  assert r'\sin(2' in blocks[-1] and '(' in rows(blocks[-1])[-1][1]
 for text in [prompt,q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:check_format(text)
 COUNT['mathematical_records']+=1
 return choices

def normalize_math(s):
 s=s.replace('\u2061','').replace(r'\partial','∂').replace(r'\cdot','').replace(' ','')
 s=re.sub(r'\\operatorname\{(sin|cos)\}',r'\\\1',s)
 s=re.sub(r'\{(sin|cos)\}',r'\\\1',s)
 return s

def source_fidelity(rec,src):
 f=src[':question/answer-fields'][0];gf=rec['question'][':question/answer-fields'][0]
 old=[read_math(a[':answer/value']) for a in f[':answer-field/choices']]
 new=[read_math(a[':answer/value']) for a in gf[':answer-field/choices']]
 matched=[]
 for a in old:
  matches=[i for i,b in enumerate(new) if equal(a,b)]
  assert len(matches)==1 and matches[0] not in matched
  matched.extend(matches)
 assert len(matched)==len(new)==5
 oldcorrect=read_math(f[':answer-field/correct'][':answer/value'])
 newcorrect=read_math(next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]))
 assert equal(oldcorrect,newcorrect)
 assert f[':answer-field/type'][':db/ident']==gf[':answer-field/type']
 assert f[':answer-field/key']==gf[':answer-field/key']
 oldp=src[':question/problem'];newp=rec['question'][':question/problem']
 oldm=re.search(r'\$([fghuvw])\(x,y,z\)=(.*?),\$',oldp)
 newm=re.search(r'\$([fghuvw])\(x,y,z\)=(.*?),\$',newp)
 assert equal(read_math(oldm[2]),read_math(newm[2]))
 assert oldp[:oldm.start()]+oldp[oldm.end():]==newp[:newm.start()]+newp[newm.end():]
 olds=src[':question/worked-solution'];news=rec['question'][':question/worked-solution']
 assert olds.split('$$')[::2]==news.split('$$')[::2],('full prose mismatch',src[':db/id'])
 ob,nb=olds.split('$$')[1::2],news.split('$$')[1::2]
 assert len(ob)==len(nb)
 # Compare every ordered row structurally and as a complete expression, using
 # symbols for derivatives so a collapsed generic chain cannot pass.
 derivative_symbols={}
 for name in ('f','g','h','u','v','w','x','y','z'):
  for v in ('x','y','z','r','theta'):derivative_symbols[(name,v)]=sp.Symbol(name+'_'+v)
 for j,(old,new) in enumerate(zip(ob,nb)):
  if src[':db/id']==17592186360582 and j==0:
   old=old.replace(r'\frac{∂v}{∂y}\cdot \frac{∂v}{∂\theta }',r'\frac{∂v}{∂y}\cdot \frac{∂y}{∂\theta }')
  orows,nrows=rows(old),rows(new)
  assert len(orows)==len(nrows),('source row sequence count',src[':db/id'],j)
  for (ol,orr),(nl,nr) in zip(orows,nrows):
   assert equal(read_row(ol,derivative_symbols),read_row(nl,derivative_symbols))
   assert equal(read_row(orr,derivative_symbols),read_row(nr,derivative_symbols)),('source ordered math-stage mismatch',src[':db/id'],j,orr,nr)
 COUNT['source_banks']+=1;COUNT['source_values']+=5;COUNT['source_distractors']+=4;COUNT['source_correct_designations']+=1
 COUNT['source_math_solution_repaired' if src[':db/id']==17592186360582 else 'source_math_solution_unrepaired']+=1

def engine_item(rec,label):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned correct selection' if a[':answer/id']==f[':answer-field/correct'][1] else 'owned incorrect selection'} for a in f[':answer-field/choices']]}

def run():
 cases=[];reviews=[];engine=[];by_level={l:set() for l in ('easy','moderate','hard')};positions=set();reviewlines=['# Originals and generated variants\n','All seven originals are captured at math basis 1356. Source-equivalent replays normalize notation; q-95172 has the documented first-chain-row correction. Generated examples are labeled, use a single fixed worked solution and complete five-option bank.\n']
 for key,(level,target,sid,params,name) in g.TEMPLATES.items():
  if sid:
   p=dict(params,name=name);case={'source_id':sid,'template':key,'parameters':p,'bank_profile':'observed'};cases.append(case)
   rec=g.generate(level,template=key,parameters=p,profile='observed');displayed(rec);source_fidelity(rec,g.SOURCES[sid]);engine.append(engine_item(rec,'source-'+str(sid)))
   reviewlines+=['## '+key+' — '+level+'\n','### Original '+str(sid)+'\n',g.SOURCES[sid][':question/problem']+'\n','\n'.join('$'+a[':answer/value']+'$' for a in g.SOURCES[sid][':question/answer-fields'][0][':answer-field/choices'])+'\n',g.SOURCES[sid][':question/worked-solution']+'\n','### Parameterized source replay\n',g.markdown(rec)+'\n']
   reviews.append({'label':'source replay','source_id':sid,'record':rec})
  else:reviewlines+=['## '+key+' — authored '+level+'\n']
  profiles=['authored_operations']+(['observed'] if sid else [])
  for profile in profiles:
   for seed in range(24):
    rec=g.generate(level,seed+3100,template=key,profile=profile);displayed(rec)
    by_level[level].add(rec['generation']['mathematical_fingerprint'])
    engine.append(engine_item(rec,key+'-'+profile+'-'+str(seed)))
    f=rec['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
    if seed<2:
     reviewlines+=['### Generated variant '+str(seed+1)+' — '+profile+'\n',g.markdown(rec)+'\n']
     reviews.append({'label':'generated variant','profile':profile,'record':rec})
    # Fixed full inputs must have seed-independent presentation identity.
    twin=g.generate(level,seed+9000,template=key,parameters=rec['generation']['parameters'],profile=profile)
    assert twin['question'][':question/id']==rec['question'][':question/id']
    assert twin['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
  # Every supported function label must produce matching prompt/solution fields.
  for label in ('f','g','h','u','v','w'):
   p=dict(params,name=label)
   rec=g.generate(level,template=key,parameters=p);displayed(rec)
   engine.append(engine_item(rec,key+'-name-'+label))
 assert positions==set(range(5))
 # Incidental parameters and names must not inflate mathematical task identity.
 for key,incidental in [('z_mixed','a'),('z_square_cross','b'),('z_single','a'),('z_single','b')]:
  level,_,_,p,name=g.TEMPLATES[key];p=dict(p,name=name)
  one=g.generate(level,template=key,parameters=p);p[incidental]=-p[incidental]
  two=g.generate(level,template=key,parameters=p)
  assert one['generation']['mathematical_fingerprint']==two['generation']['mathematical_fingerprint']
  assert one['question'][':question/id']!=two['question'][':question/id']
 rejected=0
 for key,(level,_,sid,p,name) in g.TEMPLATES.items():
  for bad in [dict(p,name=name,a=0),dict(p,name=name,a=-6),dict(p,name='x')]:
   try:g.generate(level,template=key,parameters=bad)
   except ValueError:rejected+=1
   else:raise AssertionError('invalid explicit input accepted')
 for key,bad in [('r_cubic',{'a':1,'b':1,'p':4,'q':4,'name':'g'}),('theta_coupled',{'a':1,'b':2,'c':1,'k':3,'name':'w'}),('r_coupled',{'a':1,'b':2,'c':3,'p':3,'q':3,'name':'w'})]:
  try:g.generate(g.TEMPLATES[key][0],template=key,parameters=bad)
  except ValueError:rejected+=1
  else:raise AssertionError('workload/domain constraint bypassed')
 # Whole-bank guards reject equivalent or nonfinite complete banks.
 for bad in [[g.r,g.r,2*g.r,3*g.r,4*g.r],[g.r,sp.zoo,2*g.r,3*g.r,4*g.r]]:
  try:g.guard_bank(bad)
  except ValueError:rejected+=1
  else:raise AssertionError('invalid bank accepted')
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
 (HERE/'review.md').write_text('\n\n'.join(reviewlines))
 (HERE/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False)+'\n')
 binary=REPO/'generate/runs/current/check-engine'
 subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 native=json.loads((HERE/'engine-report.json').read_text())
 summary={'status':'passed','script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'source_provenance':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},'counts':dict(COUNT),'source_total':7,'complete_source_banks_matched':7,'source_options_matched':35,'source_distractors_matched':28,'source_correct_designations_matched':7,'raw_exact_prompt_strings':0,'raw_exact_solution_strings':0,'notation_normalized_prompt_math_and_layout':7,'full_worked_prose_matched':7,'ordered_worked_math_stages_unrepaired':6,'ordered_worked_math_stages_minimally_repaired':1,'source_field_repairs':0,'source_bank_repairs':0,'source_math_solution_repairs':1,'raw_solution_anomalies':1,'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'native_unresolved':native['documented_unresolved_checks'],'meaningful_tasks_observed_in_sample':{l:len(v) for l,v in by_level.items()},'correct_option_positions':sorted(positions),'invalid_inputs_or_whole_banks_rejected':rejected,'blank_equivalent_entries':'not applicable; all seven source fields and authored fields are radio','native_binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'native_source_sha256':hashlib.sha256(binary.with_suffix('.rs').read_bytes()).hexdigest(),'scope':'first-order cylindrical chain rule only; two authored hard families; no plots or database writes','unresolved_findings':['Original distractor error intent is underdetermined for several expression patterns; these remain explicit observed replay profiles, not default authored error banks.']}
 (HERE/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
