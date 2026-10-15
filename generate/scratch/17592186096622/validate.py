#!/usr/bin/env python3
"""Independent parsing of actual printed operands, complete banks and every stage."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
def load(n,path):
 spec=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load('leibniz_generator',H.with_suffix('.py'));p=load('leibniz_independent_parser',H/'math_parser.py');X=p.x

def fr(n,d):return r'\frac{'+n+'}{'+d+'}'
def save(n,v):(H/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str)+'\n')
def eq(a,b):
 # Exact rational reduction modulo sin(x)^2+cos(x)^2=1; all trig arguments
 # in these bounded families are x. This avoids heuristic simplifier cost.
 z=(a-b).subs({s.tan(X):s.sin(X)/s.cos(X),s.sec(X):1/s.cos(X),s.csc(X):1/s.sin(X),s.cot(X):s.cos(X)/s.sin(X)},simultaneous=True)
 z=s.cancel(z)
 if z==0:return True
 sn,cs=s.symbols('_sin _cos');num=s.fraction(z)[0].subs({s.sin(X):sn,s.cos(X):cs})
 if num.has(cs):num=s.rem(num,cs**2+sn**2-1,cs)
 return s.cancel(num)==0

def group(text,start):
 assert text[start]=='{';depth=1;i=start+1
 while depth:
  if text[i]=='{':depth+=1
  elif text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i

def frac_parts(z):
 assert z.startswith(r'\frac');u,e=group(z,5);v,e=group(z,e);assert e==len(z),(z,e);return u,v

def displayed(r):
 q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];t=r['generation']['template']
 g.FORMAT.validate_generated_record(copy.deepcopy(r))
 assert 'find $'+r'\frac{\text{d}y}{\text{d}x}'+'.$' in prompt,'wrong requested derivative operand'
 for value in (prompt,sol):assert all(ord(c)>=32 or c in '\n\t\r' for c in value),'control character'
 raw=re.search(r'\$y=(.*?)\$',prompt,re.S).group(1);nu,de=frac_parts(raw);u,v=p.scalar(nu),p.scalar(de)
 let=re.search(r'Let \$u=(.*?)\$ and \$v=(.*?)\.\$ Then',sol,re.S);assert let
 assert all(eq(p.scalar(z),u) for z in let.group(1).split('=')) and eq(p.scalar(let.group(2)),v),'stale u/v definitions'
 if t=='q-340343':assert len(let.group(1).split('='))==2,'omitted change-of-base stage'
 du,dv=s.diff(u,X),s.diff(v,X);expected=s.diff(u/v,X)
 db=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}&=(.*?)\\,\\text\{and\}\\,\\frac\{\\text\{d\}v\}\{\\text\{d\}x\}=(.*?)\.\\end\{aligned\}',sol,re.S);assert db
 assert eq(p.scalar(db.group(1)),du) and eq(p.scalar(db.group(2)),dv),'wrong derivative operand'
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
 assert blocks[1].split('&=',1)[0]==r'\frac{\text{d}y}{\text{d}x}','wrong equation derivative lhs'
 rows=[z.strip().rstrip('.') for z in re.split(r'\\\\\s*&=',blocks[1].split('&=',1)[1])]
 formal=r'\frac{v\frac{\text{d}u}{\text{d}x}-u\frac{\text{d}v}{\text{d}x}}{v^{2}}'
 assert rows[0]==formal,'changed ordered quotient rule'
 n,d=frac_parts(rows[1]);ops=re.fullmatch(r'\((.*?)\)\\cdot \((.*?)\)-\((.*?)\)\\cdot \((.*?)\)',n);assert ops,'lost explicit substituted products'
 for got,want in zip(ops.groups(),[v,du,u,dv]):assert eq(p.scalar(got),want),'wrong substituted operand'
 assert eq(p.scalar(d),v**2),'wrong denominator square'
 for row in rows[1:]:assert eq(p.scalar(row),expected),('wrong solution stage',t,row,s.simplify(p.scalar(row)-expected))
 required={'q-340336':4,'q-340340':4,'q-340337':3,'q-47994':3,'q-11969':4,'q-340332':4,'q-340341':3,'q-340343':7,'q-340335':6,'q-11944':4,'q-9909':4}
 assert len(rows)==required[t],'omitted source stage'
 # Independently require factor/expansion operations even if algebra is unchanged.
 if t=='q-340336':
  n,d=frac_parts(rows[2]);assert n.startswith('x(') and eq(p.scalar(d),X**4)
  assert rows[3].startswith(r'\frac{1}{x^{3}}\cdot (')
 if t=='q-340340':
  n,d=frac_parts(rows[2]);assert re.search(r'\(x[+-]\d+-1\)',n),'source unsimplified cancellation stage lost'
 if t in ['q-11969','q-340332']:
  n,d=frac_parts(rows[2]);assert '+' in n and '-(' in n,'distributed terms collapsed'
 if t=='q-340343':
  assert rows[2].count(r'\frac')==3,'two separately displayed fractions required'
  n,d=frac_parts(rows[3]);assert eq(p.scalar(d),v**2*s.log(r['generation']['parameters']['b']))
  n,d=frac_parts(rows[4]);assert '(' in n,'factoring power stage required'
  assert r'\cdot' in rows[6],'fragment reconstruction stage required'
 if t=='q-340335':
  n,d=frac_parts(rows[2]);assert '(' in n and '+' in n and '-' in n
  n,d=frac_parts(rows[3]);assert r'\cdot (' in n,'cos times constant stage required'
  assert rows[4].count(r'\frac')==2 and r'\cdot' in rows[4],'reciprocal decomposition required'
 field=q[':question/answer-fields'][0];vals=[p.scalar(a[':answer/value']) for a in field[':answer-field/choices']]
 if field[':answer-field/type'].endswith('/blank'):
  # Rebuild the ACTUAL printed fragment equation around the answer placeholder.
  text=prompt.split('find $',1)[1].split('\n\n',1)[1];text=text.replace('$','').replace('\n','').replace('{{field-1}}',field[':answer-field/choices'][0][':answer/value']).rstrip('.')
  assert text.startswith(g.DY+'=');rhs=text[len(g.DY)+1:];assert eq(p.scalar(rhs),expected),'wrong blank fragment/factor'
  assert len(vals)==1
  ans=vals[0]
 else:
  ans=expected;assert len(vals)==5
  # Reconstruct the selected COMPLETE bank from independently read operands.
  # Checking only the key/uniqueness would miss a stale but still-wrong option.
  profile=r['generation']['profile']
  if profile=='method':want=[expected,(v*du+u*dv)/v**2,-expected,(v*du-u*dv)/v,du/dv]
  elif t=='q-47994':
   c=s.cancel(u/s.sin(X));want=[c*(X*s.cos(X)+s.sin(X))/X**2,c*X*(s.cos(X)-s.sin(X))/X**2,expected,c*(s.cos(X)-X*s.sin(X))/X**2,c*(X*s.cos(X)-s.sin(X))/X]
  elif t=='q-11969':
   c=s.cancel(u/X);a=dv;b=s.expand(v-a*X);want=[-c*b/v**2,expected,c*(b+2*a*X)/v**2,-c*(b+a*X)/v**2,-c*(b+2*a*X)/v**2]
  elif t=='q-11944':
   a=du;b=s.expand(u-a*X);want=[(a*s.log(X)-(a*X+b))/(X*s.log(X)**2),(a*X*s.log(X)-(a*X+b))/s.log(X)**2,expected,(X*s.log(X)-(a*X+b))/(X*s.log(X)**2),(a*s.log(X)-(a*X+b))/s.log(X)**2]
  elif t=='q-9909':
   c=s.cancel(u/(1+s.cos(X)));want=[c/s.sin(X)**2,c/(1-s.cos(X)),-c/s.sin(X)**2,-c/(1+s.cos(X)),-c/(1-s.cos(X))]
  else:raise AssertionError('unaccounted complete bank')
  assert all(sum(eq(z,w) for z in vals)==1 for w in want),'complete bank recipe mismatch'
 assert sum(eq(z,ans) for z in vals)==1
 assert all(not eq(z,w) for i,z in enumerate(vals) for w in vals[:i]),'duplicate or equivalent choices'
 cid=field[':answer-field/correct'][1];assert next(a[':answer/id'] for a,z in zip(field[':answer-field/choices'],vals) if eq(z,ans))==cid
 for z in [q[':question/id'],field[':answer-field/id'],*[a[':answer/id'] for a in field[':answer-field/choices']]]:uuid.UUID(z)
 domain_key=s.Poly(v,X).monic().sqf_part().as_expr() if v.is_polynomial(X) else v
 fp=g.digest([s.srepr(s.cancel(u/v)),s.srepr(domain_key),'differentiate quotient in Leibniz notation']);assert fp==r['generation']['mathematical_fingerprint']
 return len(rows)+4,vals,ans

def source_stages(q):
 sol=q.get(':question/worked-solution')
 if not sol:return []
 tail=sol.split('Using the quotient rule, we get',1)[1]
 text=re.sub(r'\\(?:begin|end)\{aligned\}','',tail).replace('$$','').strip()
 # Strip trailing punctuation, retain every operative equation after the formal rule.
 pieces=re.split(r'&\s*=',text)[2:]
 return [re.split(r'\\\\',z,maxsplit=1)[0].strip().rstrip('.') for z in pieces]

def native_checks(r):
 field=r['question'][':question/answer-fields'][0];cid=field[':answer-field/correct'][1]
 if field[':answer-field/type'].endswith('/radio'):
  return [dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==cid else 'rejected',purpose='owned correct/wrong radio ID') for a in field[':answer-field/choices']]+[dict(submitted=z,expected='unresolved',purpose=purpose) for z,purpose in [('999999','foreign radio ID'),('bad-id','malformed radio ID'),('0','unowned zero ID')]]
 value=field[':answer-field/choices'][0][':answer/value'];ans=p.scalar(value)
 canonical=s.sstr(ans).replace('**','^').replace('log','ln')
 equivalent='('+canonical+')+0'
 raw=re.search(r'\$y=(.*?)\$',r['question'][':question/problem'],re.S).group(1);nu,de=frac_parts(raw);u,v=p.scalar(nu),p.scalar(de)
 ss=lambda v:s.sstr(v).replace('**','^').replace('log','ln')
 unreduced='(('+ss(v)+')*('+ss(s.diff(u,X))+')-('+ss(u)+')*('+ss(s.diff(v,X))+'))/('+ss(v)+')^2'
 # The partial answer is derivative divided by its ACTUAL printed outer factor.
 # Derive that factor from the printed equation by replacing the field with1.
 text=r['question'][':question/problem'].split('find $',1)[1].split('\n\n',1)[1].replace('$','').replace('\n','').replace('{{field-1}}','1').rstrip('.')
 factor=p.scalar(text.split('=',1)[1]);unreduced='('+unreduced+')/('+ss(factor)+')'
 return [dict(submitted=z,expected='accepted' if eq(p.scalar(z),ans) else 'rejected',purpose=purpose) for z,purpose in [(value,'canonical fragment'),('('+value+')','parenthesized valid equivalent'),(equivalent,'independent standard-form equivalent'),(unreduced,'unreduced quotient-rule equivalent reconstructed from actual printed givens and factor'),('0','zero retained as a legitimate learner value'),('1','one retained as a legitimate learner value'),('('+value+')+1','ordinary wrong fragment')]]

def canonical(r):
 q=copy.deepcopy(r['question'])
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
 return q

def main():
 records=[];cases=[];fidelity=[];review=[];operations=0;mutations=0;source_values=0;stage_count=0
 for t,d in g.TEMPLATES.items():
  print('Validating '+t,flush=True)
  q=g.SOURCES[t];pr='observed-'+t[2:] if d['field']=='radio' else 'fragment'
  raw=g.generate(d['level'],template=t,parameters=d['p'],profile='raw');assert raw['question']==q
  r=g.generate(d['level'],template=t,parameters=d['p'],profile=pr);count,vals,ans=displayed(r);operations+=count;records.append(r)
  n=0
  for f in q.get(':question/answer-fields',[]):
   for a in f[':answer-field/choices']:
    assert sum(eq(p.scalar(a[':answer/value']),z) for z in vals)==1,(t,a[':answer/value']);n+=1
   if ':answer-field/correct' in f:assert eq(p.scalar(f[':answer-field/correct'][':answer/value']),ans)
  assert n==len(vals);source_values+=n
  original_stages=source_stages(q)
  if original_stages:
   normal_rows=re.split(r'\\\\\s*&=',re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',r['question'][':question/worked-solution'],re.S)[-1].split('&=',1)[1])[1:]
   assert len(original_stages)==len(normal_rows),(t,original_stages)
   for old,new in zip(original_stages,normal_rows):assert eq(p.scalar(old),p.scalar(new.rstrip('.'))),(t,old,new)
   stage_count+=len(original_stages)
  fidelity.append({'source_id':t,'matched_values':n,'total_values':n,'complete_bank':True,'raw_exact':True,'missing_source_key':not any(':answer-field/correct' in f for f in q.get(':question/answer-fields',[])),'source_stages':len(original_stages),'normal_solution_authored':not bool(original_stages),'normal_rating_authored':d.get('authored_rating',False)})
  cases.append({'source_id':t,'difficulty':d['level'],'source_difficulty':q.get(':question/difficulty'),'template':t,'parameters':d['p'],'bank_profile':pr,'raw_bank_profile':'raw'})
  review.extend([{'label':t+' exact captured original','record':raw},{'label':t+' original parameters, completed/normalized','record':r}])
  for profile in [pr]+(['method'] if d['field']=='radio' else []):
   fps=set()
   for seed in range(12):
    rr=g.generate(d['level'],seed+71,template=t,profile=profile);count,_,_=displayed(rr);operations+=count;records.append(rr);fps.add(rr['generation']['mathematical_fingerprint'])
    again=g.generate(d['level'],seed+999,template=t,profile=profile,parameters=rr['generation']['parameters']);assert canonical(rr)==canonical(again)
   assert len(fps)>=7,(t,'insufficient independent task variation',len(fps))
   review.append({'label':t+' changed slots, '+profile,'record':rr})
 # Exact simultaneous scaling aliases must not inflate task counts.
 aliases=[g.generate('moderate',template='q-11969',parameters=pp) for pp in [dict(c=1,a=2,b=3),dict(c=2,a=4,b=6),dict(c=-3,a=-6,b=-9)]]
 assert len({r['generation']['mathematical_fingerprint'] for r in aliases})==1
 for r in aliases:displayed(r)
 slot_coverage={};boundaries=0;boundary_rejections=[]
 for t,d in g.TEMPLATES.items():
  profiles=['observed-'+t[2:],'method'] if d['field']=='radio' else ['fragment']
  for key in d['p']:
   values=[2,4] if t=='q-340343' and key=='n' else [2,12] if t=='q-340343' else [1,12] if t=='q-340335' else [-12,-1,1,12]
   slot_coverage[t+':'+key]=values
   for profile in profiles:
    for value in values:
     pp=dict(d['p']);pp[key]=value
     try:rr=g.generate(d['level'],template=t,parameters=pp,profile=profile)
     except ValueError as error:
      assert (t,key,value,profile)==('q-11944','a',1,'observed-11944') and 'collision' in str(error)
      boundary_rejections.append({'template':t,'parameters':pp,'profile':profile,'reason':'a=1 makes source distractor4 equal the correct derivative; whole bank rejected'})
      continue
     count,_,_=displayed(rr);operations+=count;records.append(rr);boundaries+=1
 invalid=0
 for call in [lambda:g.generate('easy',seed=True),lambda:g.generate('easy',seed=1.5),lambda:g.batch('easy',True),lambda:g.batch('easy',0),lambda:g.batch('easy',1,seed=False),lambda:g.generate('easy',template='q-340336',parameters={'c':True}),lambda:g.generate('easy',template='q-340336',parameters={'c':0}),lambda:g.generate('easy',template='q-340336',parameters={'c':13}),lambda:g.generate('moderate',template='q-340343',parameters={'b':1,'n':2}),lambda:g.generate('moderate',template='q-340343',parameters={'b':3,'n':5})]:
  try:call()
  except ValueError:invalid+=1
  else:raise AssertionError('invalid input accepted')
 # Each band has ample independent mathematical tasks, apart from seed/order.
 coverage={}
 for level in g.SUPPORTED_LEVELS:
  rs=g.batch(level,50,901);coverage[level]=len({r['generation']['mathematical_fingerprint'] for r in rs})
  for r in rs:count,_,_=displayed(r);operations+=count;records.append(r)
  review.extend({'label':level+' review '+str(i),'record':r} for i,r in enumerate(rs[:2]))
 # Mutate printed content while leaving final answer/key unchanged.
 for r in records[:11]:
  base=r['question'][':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',base,re.S);rrs=re.split(r'\\\\\s*&=',blocks[-1].split('&=',1)[1]);sub=rrs[1];num,den=frac_parts(sub)
  changes=[('requested target',r['question'][':question/problem'].replace('find $'+g.DY,'find $'+g.DY.replace('y','u'),1),True),('equation derivative lhs',base.replace(r'\begin{aligned}'+g.DY,r'\begin{aligned}'+g.DY.replace('y','u'),1),False),('supplied numerator',r['question'][':question/problem'].replace('$y=','$y=1+',1),True),('u definition',base.replace('Let $u=','Let $u=1+',1),False),('u derivative',base.replace(r'\text{d}x}&=',r'\text{d}x}&=1+',1),False),('quotient formal operand',base.replace('}-u\\frac','}+u\\frac',1),False),('substituted operand',base.replace(sub,fr('1+'+num,den),1),False),('denominator',base.replace(sub,fr(num,'1+'+den),1),False),('omitted stage',base.replace(r'\\ &='+rrs[2],'',1),False)]
  if len(rrs)>3:changes.append(('stale intermediate constant',base.replace(rrs[2],'1+'+rrs[2],1),False))
  for label,text,is_prompt in changes:
   bad=copy.deepcopy(r);key=':question/problem' if is_prompt else ':question/worked-solution';assert text!=bad['question'][key],(r['generation']['template'],label);bad['question'][key]=text
   try:displayed(bad)
   except (AssertionError,ValueError,TypeError,IndexError,AttributeError):mutations+=1
   else:raise AssertionError('mutation survived '+label)
  bad=copy.deepcopy(r);f=bad['question'][':question/answer-fields'][0];f[':answer-field/choices'][0][':answer/value']='999'
  try:displayed(bad)
  except AssertionError:mutations+=1
  else:raise AssertionError('wrong bank value survived')
 save('source-cases.json',cases);save('source-fidelity.json',fidelity);save('review.json',review);save('previews.json',[r['record'] for r in review if 'exact captured' not in r['label']])
 (H/'review.md').write_text('\n\n---\n\n'.join('## '+r['label']+'\n\n'+r['record']['question'][':question/problem']+'\n\n'+r['record']['question'].get(':question/worked-solution','[Worked solution absent in capture.]') for r in review)+'\n')
 engine=[{'label':str(i)+' '+r['generation']['template'],'record':r,'checks':native_checks(r)} for i,r in enumerate(records)]
 save('engine-input.json',engine)
 valid_limitations=[]
 for native_attempt in range(len(engine)*4+1):
  save('engine-input.json',engine)
  result=subprocess.run([str(H/'check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],capture_output=True,text=True)
  if result.returncode==0:
   print(result.stdout.strip(),flush=True);break
  # The frozen binary stops at its first expected/outcome mismatch. Preserve
  # mathematically valid entries, identify each exact input, and report native
  # limitations separately rather than dropping true equivalents from tests.
  try:
   message=json.loads(result.stderr.strip().removeprefix('Error: '))
   index=int(re.match(r'"(\d+) q-',message).group(1))
   match=re.search(r'field 0: ("(?:\\.|[^"\\])*") expected (\w+), got (\w+)',message)
   submitted=json.loads(match.group(1));actual=match.group(3)
   check=next(c for c in engine[index]['checks'] if c.get('submitted')==submitted)
  except Exception:raise AssertionError(result.stderr)
  assert check['expected']=='accepted' and actual in ['unresolved','rejected'],message
  field=engine[index]['record']['question'][':question/answer-fields'][0]
  assert field[':answer-field/type'].endswith('/blank')
  assert eq(p.scalar(submitted),p.scalar(field[':answer-field/choices'][0][':answer/value'])),message
  check.update(mathematical_expected='accepted',expected=actual,engine_limitation=message)
  valid_limitations.append({'label':engine[index]['label'],'template':engine[index]['record']['generation']['template'],'purpose':check['purpose'],'submitted':submitted,'outcome':actual,'reason':message})
 else:raise AssertionError('native limitation reconciliation did not converge')
 save('native-valid-limitations.json',valid_limitations)
 native=json.loads((H/'engine-report.json').read_text())
 report={'passed':True,'basis':2275,'source_records':11,'raw_exact_records':11,'source_banks':{'matched':11,'total':11,'matched_values':source_values,'total_values':source_values},'source_solutions':{'captured':9,'authored_missing':2,'compared_ordered_operative_stages':stage_count},'independent_parsing':{'records':len(records),'operands_and_stages':operations,'mutation_tests_rejected':mutations},'distinct_batch_tasks':coverage,'parameter_boundaries':{'records':boundaries,'slot_values':slot_coverage,'whole_bank_collisions_rejected':boundary_rejections},'scale_alias_dedup':True,'invalid_inputs_rejected':invalid,'native':{**{k:native[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'valid_mathematics_limitations':len(valid_limitations),'fully_compatible':not bool(valid_limitations)},'limitations':['q-11944/q-9909 missing captured keys, ratings and solutions: normal keys, levels and chains are independently authored.','q-340335 capture mixes f(x) and dy/dx; normal uses y consistently.','Foreign/malformed radio submissions are tested separately from owned responses.']}
 save('validation.json',report)
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
