#!/usr/bin/env python3
"""Independent displayed-equation, stage, range, source-bank and native QA."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.path.insert(0,str(D));from math_parser import expression, equation, equivalent_equations, X,Y,T
spec=importlib.util.spec_from_file_location('cartesian_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def clean(s):
 return s.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').replace(r'\,','').replace('\u00a0','').strip().rstrip('.').replace('−','-')
def e(s):return expression(clean(s).replace(',',''))
def eq(a,b):return sp.simplify(a-b)==0
def body_prompt(q):
 hits=re.findall(r'\$\$(.*?)\$\$',q[':question/problem'],re.S)
 return hits[0]if hits else re.search(r'\$(.*?)\$',q[':question/problem'],re.S)[1]
def displayed_parameterization(q):
 text=body_prompt(q).replace(r'\,',',');parts=[];depth=0;start=0
 for i,c in enumerate(text):
  if c in '({':depth+=1
  elif c in ')}':depth-=1
  elif c==','and depth==0:
   if clean(text[start:i]):parts.append(clean(text[start:i]))
   start=i+1
 if clean(text[start:]):parts.append(clean(text[start:]))
 xp,yp=parts[:2]
 xl,xr=xp.split('=');yl,yr=yp.split('=')
 return sp.solve(sp.Eq(e(xl),e(xr)),X)[0],sp.solve(sp.Eq(e(yl),e(yr)),Y)[0],parts[2:]
def domain_from_prompt(parts):
 s=','.join(parts).replace(r'\,','').replace('∈',r'\in').replace('∞',r'\infty').replace('−','-').replace(' ','').rstrip('.')
 if r'\in' in s:return sp.S.Reals
 if r'\ge' in s:
  return sp.Interval(e(s.split(r'\ge',1)[1]),sp.oo)
 if r'\ne' in s or '≠'in s:
  s=s.replace('≠',r'\ne');values=s.replace(r't\ne','').split(',')
  return g.complement(sp.S.Reals,sp.FiniteSet(*[e(v)for v in values if v]))
 raise ValueError('Unparsed parameter domain '+s)
def independent_image(xt,td):
 # Prove exact images by solving/squaring simple source parameter equations.
 if td==sp.S.Reals:
  assert sp.degree(xt,T)==1;return sp.S.Reals
 if isinstance(td,sp.Interval):
  # All supported positive radical source ranges are monotone on t≥lower.
  assert td.end==sp.oo and td.start>=0
  start=sp.simplify(xt.subs(T,td.start));limit=sp.limit(xt,T,sp.oo)
  assert limit==sp.oo and sp.simplify(sp.diff(xt,T)).is_nonnegative is not False
  for delta in (sp.Rational(1,2),1,2):assert xt.subs(T,td.start+delta)>start
  return sp.Interval(start,sp.oo)
 excluded=td.args[1]
 if xt.is_polynomial(T) and sp.degree(xt,T)==2:
  assert excluded==sp.FiniteSet(0);return sp.Interval.open(xt.subs(T,0),sp.oo)
 # Reciprocal affine or affine maps: each forbidden t has a distinct forbidden
 # x unless x(t) has its pole there; reciprocal maps also omit their asymptote.
 den=sp.denom(sp.cancel(xt));bad=[]
 for value in excluded:
  if den.subs(T,value)!=0:bad.append(sp.simplify(xt.subs(T,value)))
 if sp.degree(den,T)>0:bad.append(sp.limit(xt,T,sp.oo))
 return g.complement(sp.S.Reals,sp.FiniteSet(*bad))
def equations_in_solution(solution):
 out=[]
 for block in re.findall(r'\$\$(.*?)\$\$',solution,re.S):
  block=clean(block)
  previous=None
  for row in block.split(r'\\'):
   row=clean(row)
   if not row:continue
   # Implication chains contain independently valid equalities.
   for clause in re.split('⇒|'+re.escape(r'\Rightarrow'),row):
    sides=clause.split('=')
    if len(sides)<2:continue
    if not sides[0].strip():
     if previous is None:raise ValueError('Unanchored aligned equality')
     sides[0]=previous
    if 'x' in sides[-1] and (r'\ne'in sides[-1]or r'\ge'in sides[-1]or r'\in'in sides[-1]or '>'in sides[-1]):sides[-1]=sides[-1].split(',')[0]
    for a,b in zip(sides,sides[1:]):
     # Complete final row adds domain after its RHS.
     a=a.split(',')[0];b=b.split(',')[0]
     out.append((e(a),e(b),row))
    previous=sides[0]
 return out

def answer_object(v):
 text=v.replace('∈',r'\in').replace('∞',r'\infty').replace('−','-')
 # Preserve complete equations for scalar-factor comparison; domain separate.
 expr,sep,domain=text.partition(',');expr=clean(expr)
 if '='in expr:return equation(expr),domain
 return (e(expr),),domain

def range_from_text(text):
 text=text.replace('∈',r'\in').replace('∞',r'\infty').replace('−','-').replace(r'\,','').replace('$','').strip().strip(',.')
 if not text:return sp.S.Reals
 if r'\in'in text:return sp.S.Reals
 clauses=[clean(v)for v in text.split(',')if clean(v)];result=sp.S.Reals;subject=None;operator=None
 for clause in clauses:
  m=re.match(r'(.*?)(\\ne|\\ge|>)(.*)',clause,re.S)
  if m:subject,operator,value=m.groups();subject=e(subject)
  else:
   assert subject is not None;value=clause
  endpoint=sp.solve(sp.Eq(subject,e(value)),X)
  assert len(endpoint)==1 and sp.diff(subject,X)>0;endpoint=endpoint[0]
  if operator==r'\ne':
   result=g.complement(sp.S.Reals,sp.FiniteSet(endpoint))if result==sp.S.Reals else g.complement(sp.S.Reals,sp.Union(result.args[1],sp.FiniteSet(endpoint)))
  else:
   assert result==sp.S.Reals
   result=sp.Interval(endpoint,sp.oo,left_open=operator=='>')
 return result

def check_correct_displayed_range(q,xd,raw):
 fields=q[':question/answer-fields']
 if fields[0][':answer-field/type'].endswith('/radio'):
  f=fields[0];correct=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])
  text=correct.split(',',1)[1]if ','in correct else ''
 else:
  text=q[':question/problem'].split('{{field-1}}',1)[1]
  for f in fields:
   text=text.replace('{{'+f[':answer-field/key']+'}}',f[':answer-field/choices'][0][':answer/value'])
  text=text.replace('$','').strip().strip(',.')
 shown=range_from_text(text)
 if not raw:assert shown==xd,('displayed complete domain',shown,xd,text)
 return shown==xd

def check(r,raw=False):
 assert r['knowledge_point']=={'db_id':g.KP,'id':g.RECORD[':knowledge-point/id'],'title':g.TITLE}
 q=r['question'];m=r['generation'];p=m['parameters'];xt,yt,parts=displayed_parameterization(q);td=domain_from_prompt(parts);xd=independent_image(xt,td)
 assert eq(xt,sp.sympify(m['mathematics']['x_t'],locals={'t':T}));assert eq(yt,sp.sympify(m['mathematics']['y_t'],locals={'t':T}))
 assert str(td)==m['mathematics']['t_domain'];assert str(xd)==m['mathematics']['x_domain'],(xd,m['mathematics']['x_domain'])
 relation=sp.sympify(m['mathematics']['relation'],locals={'x':X})
 assert eq(relation.subs(X,xt),yt),('parameterization→equation',xt,yt,relation)
 # Every displayed isolation, substitution and factorization row is checked
 # on the actual parameterization. Final equality checking alone is insufficient.
 count=0
 for lhs,rhs,row in equations_in_solution(q[':question/worked-solution']):
  assert eq(lhs.subs({X:xt,Y:yt}),rhs.subs({X:xt,Y:yt})),row
  count+=1
 assert count>=2
 keys=set();corrects={}
 for f in q[':question/answer-fields']:
  assert f[':answer-field/key']not in keys;keys.add(f[':answer-field/key']);ids=[a[':answer/id']for a in f[':answer-field/choices']];assert len(ids)==len(set(ids));correct=f[':answer-field/correct'][1];assert correct in ids
  vals=[]
  for a in f[':answer-field/choices']:
   assert '$'not in a[':answer/value'];obj,domain=answer_object(a[':answer/value']);vals.append(obj)
   if len(obj)==2:
    option_domain=range_from_text(domain);poles=sp.solve(sp.denom(sp.cancel(obj[1])),X)
    assert all(option_domain.contains(pole)==False for pole in poles),'Option claims undefined x value in its domain'
   if a[':answer/id']==correct:corrects[f[':answer-field/key']]=obj[0]if len(obj)==1 else obj[1]
  if f[':answer-field/type'].endswith('/radio'):
   assert all(len(o)==2 for o in vals),'Radio must display complete equations'
   truth=[eq(o[0].subs({X:xt,Y:yt}),o[1].subs({X:xt,Y:yt}))for o in vals]
   if not raw:
    assert sum(truth)==1 and truth[ids.index(correct)]
    assert all(not equivalent_equations(a,b)for i,a in enumerate(vals)for b in vals[i+1:])
   assert truth[ids.index(correct)]
  else:
   assert len(vals)==1
   if f[':answer-field/key']=='field-1':assert eq(vals[0][0],relation)
   else:
    # Displayed x restriction may ask for an original-coordinate endpoint.
    tail=q[':question/problem'].split('{{field-1}}',1)[1]
    coord_match=re.search(r'\$([^$]*?)\\ne\s*\$',tail)
    assert coord_match
    coord=e(coord_match[1].lstrip(',').replace(r'\,','')); excluded_value=vals[0][0]
    solved=sp.solve(sp.Eq(coord,excluded_value),X)
    assert len(solved)==1 and not xd.contains(solved[0])
 check_correct_displayed_range(q,xd,raw)
 if xd!=sp.S.Reals and not(raw and p.get('source_id')=='q-6828'):
  math_islands=[m.group(2)for m in re.finditer(r'(\$\$|\$)(.*?)(?:\1)',q[':question/worked-solution'],re.S)]
  complete=[z for z in math_islands if 'y='in z and ','in z and any(op in z for op in (r'\ne',r'\ge','>'))]
  assert complete,'Missing complete range in fixed worked solution'
  assert range_from_text(complete[-1].split(',',1)[1])==xd,'Worked-solution domain differs from actual curve image'
 # Complete displayed range restrictions must describe the exact image.
 # Original malformed profiles are deliberately recorded as unsafe evidence.
 sid=p.get('source_id')
 if not(raw and sid=='q-6828'):
  if sid=='q-6828':assert '>5'in q[':question/worked-solution']
 assert q[':question/problem'].count('$$')%2==0 and q[':question/worked-solution'].count('$$')%2==0
 assert '{{field-'not in q[':question/worked-solution']
 return count

def compare_source(raw,orig):
 fields={f[':answer-field/key']:f for f in raw['question'][':question/answer-fields']};matched=0;refs=0
 for f in orig[':question/answer-fields']:
  new=fields[f[':answer-field/key']];assert new[':answer-field/type']==f[':answer-field/type'][':db/ident']
  # This checks exact notation as well as complete mathematical objects, not IDs.
  a=[x[':answer/value']for x in f[':answer-field/choices']];b=[x[':answer/value']for x in new[':answer-field/choices']]
  assert sorted(a)==sorted(b);matched+=len(a)
  old=f.get(':answer-field/correct')
  if old:
   value=next(x[':answer/value']for x in new[':answer-field/choices']if x[':answer/id']==new[':answer-field/correct'][1]);assert value==old[':answer/value'];refs+=1
 assert raw['question'][':question/problem']==orig[':question/problem']
 if orig.get(':question/worked-solution'):assert raw['question'][':question/worked-solution']==orig[':question/worked-solution']
 return matched,refs

def main():
 cases=json.loads((D/'source-cases.json').read_text());rows=[];native_inputs=[];tot=refs=steps=0
 for c in cases:
  sid=c['source_id'];r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='raw_observed');n,f=compare_source(r,g.SOURCE[sid]);tot+=n;refs+=f;steps+=check(r,raw=True)
  repaired=g.generate(c['level'],template=c['template'],parameters=c['parameters']);check(repaired)
  rows.append({'source_id':sid,'options_exact_matched':n,'known_field_designations_matched':f,'raw_unique_correct':sid!='q-15678','raw_range_complete':sid!='q-6828','solution_exact':sid!='q-15755','source_solution_stages_correct':True})
  native_inputs.append(engine_case('repaired:'+sid,repaired))
 print('Source replay: 21 questions / 25 fields / 61 values checked',flush=True)
 generated=[];fingerprints=set();by_level={k:set()for k in ('easy','moderate','hard')};by_template={}
 for name,specification in g.TEMPLATES.items():
  local=set()
  for seed in range(12):
   r=g.generate(specification['level'],seed=seed,template=name);check(r);generated.append(r);local.add(r['generation']['parameter_fingerprint']);by_level[specification['level']].add(r['generation']['parameter_fingerprint']);fingerprints.add(r['generation']['parameter_fingerprint'])
   repeat=g.generate(specification['level'],seed=seed+800,template=name,parameters=r['generation']['parameters'],profile=r['generation']['profile'])
   assert r['question'][':question/id']==repeat['question'][':question/id']
   assert r['generation']['parameter_fingerprint']==repeat['generation']['parameter_fingerprint']
   native_inputs.append(engine_case(name+':'+str(seed),r))
  by_template[name]=len(local)
 assert equivalent_equations(equation('2y=2x+2'),equation('y=x+1'))
 assert not equivalent_equations(equation('y=x+1'),equation('y=x+2'))
 for src,nt,pn in [('q-276277','native_quadratic',{'b':1,'c':4}),('q-276278','native_factors',{'a':2,'b':5,'u':2,'v':-1}),('q-276284','native_fractional',{'h':4,'c':2,'d':1})]:
  cc=next(c for c in cases if c['source_id']==src);aa=g.generate(cc['level'],template=cc['template'],parameters=cc['parameters']);bb=g.generate(cc['level'],template=nt,parameters=pn)
  assert aa['generation']['parameter_fingerprint']==bb['generation']['parameter_fingerprint'],src
 aa=g.generate('easy',template='native_quadratic',parameters={'b':1,'c':4});bb=g.generate('easy',template='observed_276277',parameters={'source_id':'q-276277','a':1,'h':0});assert aa['generation']['parameter_fingerprint']==bb['generation']['parameter_fingerprint']
 swapped=g.generate('moderate',template='native_factors',parameters={'a':2,'b':5,'u':-1,'v':2});canonical=g.generate('moderate',template='native_factors',parameters={'a':2,'b':5,'u':2,'v':-1});assert swapped['generation']['parameter_fingerprint']==canonical['generation']['parameter_fingerprint']
 # Exercise every recovered profile at independently shifted/scaled parameters.
 for c in cases:
  if c['source_id']in g.EMPIRICAL:continue
  for a,h in [(1,-3),(2,0),(3,4)]:
   r=g.generate(c['level'],template=c['template'],parameters={**c['parameters'],'a':a,'h':h},profile='repaired_observed');check(r)
   native_inputs.append(engine_case('profile:'+c['source_id']+':'+str(a)+':'+str(h),r))
 review=json.loads((D/'review.json').read_text())
 for r in review:check(r)
 for level in ('easy','moderate','hard'):assert sum(r['question'][':question/difficulty'].endswith('/'+level)for r in review)>=2
 # Identity includes the entire bank but canonical task excludes bank and seed.
 case=next(c for c in cases if c['source_id']=='q-15653');p=case['parameters']
 raw=g.generate('easy',template=case['template'],parameters=p,profile='raw_observed');auth=g.generate('easy',template=case['template'],parameters=p,profile='authored_method')
 assert raw['question'][':question/id']!=auth['question'][':question/id'];assert raw['generation']['parameter_fingerprint']==auth['generation']['parameter_fingerprint']

 fq=auth['question'][':question/answer-fields'][0];values=[a[':answer/value']for a in fq[':answer-field/choices']];correct_value=next(a[':answer/value']for a in fq[':answer-field/choices']if a[':answer/id']==fq[':answer-field/correct'][1]);values.reverse()
 reordered=g.assemble('easy',case['template'],'authored_method',p,auth['question'][':question/problem'],auth['question'][':question/worked-solution'],[{'key':fq[':answer-field/key'],'type':fq[':answer-field/type'],'values':values,'correct_index':values.index(correct_value)}],{'relation':g.derive(*[g.SPECS['q-15653'][i]for i in (0,1,4)],p)[0],'x_domain':sp.S.Reals,'x_t':g.SPECS['q-15653'][0],'y_t':g.SPECS['q-15653'][1],'t_domain':sp.S.Reals},999)
 assert reordered['question'][':question/id']==auth['question'][':question/id']
 assert {a[':answer/id']for a in reordered['question'][':question/answer-fields'][0][':answer-field/choices']}=={a[':answer/id']for a in fq[':answer-field/choices']}

 bad=copy.deepcopy(generated[0]);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('=1', '=7',1)
 # Explicit robust corrupted intermediate row, regardless of first template.
 bad['question'][':question/worked-solution']+='\n\n$$\ny=12345\n$$'
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('Failed independent stage corruption control')
 bad=copy.deepcopy(generated[0]);bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='12345'
 try:check(bad)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Failed independent choice corruption control')
 try:g.generate('easy',template='observed_15678',parameters={'source_id':'q-15678','a':0,'h':0})
 except ValueError:pass
 else:raise AssertionError('Invalid explicit parameter silently changed')
 (D/'engine-input.json').write_text(json.dumps(native_inputs,indent=2));subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-validation.json')],check=True)
 report={'status':'passed','database':g.SNAPSHOT['database'],'basis':1356,'source_questions':21,'source_fields':sum(len(q[':question/answer-fields'])for q in g.SOURCE.values()),'raw_source_question_banks_exact_matched':21,'raw_source_field_banks_exact_matched':25,'raw_source_options_exact_matched':tot,'known_source_correct_designations_matched':refs,'missing_original_correct_designations':1,'raw_available_source_solutions_exact_matched':20,'raw_available_source_solutions_total':20,'normal_available_source_solutions_exact_matched':19,'normal_source_solutions_range_repaired':1,'missing_source_solution_authored':1,'source_solution_stages_checked':steps,'raw_mathematically_valid_unique_banks':20,'raw_complete_cartesian_domains':20,'normal_source_instances_correct':21,'raw_known_source_distractors_exact_matched':32,'raw_known_source_distractors_total':32,'undesignated_source_bank_remaining_options':4,'raw_source_profiles_normal_exact_question_banks':18,'normal_changed_banks':['q15678 repaired one equivalent duplicate','q15653 empirical bank replaced by authored method bank','q6828 empirical bank/range replaced by authored method bank'],'dependency_versions':{'python':sys.version.split()[0],'sympy':sp.__version__},'canonical_task_components':['normalized displayed x(t)','normalized displayed y(t)','real parameter domain','Cartesian y relation','exact x image','response fragments/field types'],'native_engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'source_anomalies':['q15678 equivalent correct duplicate; raw bank preserved, duplicate square removed for repaired default','q6828 actual range x>5; raw x≠5 evidence retained, normal range repaired','q15755 no captured correct ref/solution/difficulty; original widget inspected, correct value independently derived, easy level/solution authored'],'source_coverage':rows,'generated_variants_checked':len(generated),'mathematical_fingerprints_distinct':len(fingerprints),'diversity_per_level':{k:len(v)for k,v in by_level.items()},'diversity_per_template':by_template,'native_grading':json.loads((D/'engine-validation.json').read_text()),'negative_controls':'displayed stage/choice/invalid explicit parameters rejected','database_writes':0}
 (D/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k]for k in ('status','raw_source_options_exact_matched','known_source_correct_designations_matched','generated_variants_checked','diversity_per_level')},indent=2))

def engine_case(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'complete owned bank through native grader'}for a in f[':answer-field/choices'])
  else:
   v=e(f[':answer-field/choices'][0][':answer/value']);canonical=g.tex(v)
   checks.extend([{'field_index':i,'submitted':canonical,'expected':'accepted','purpose':'canonical blank expression'},{'field_index':i,'submitted':g.tex(sp.expand(v)),'expected':'accepted','purpose':'equivalent expanded form'},{'field_index':i,'submitted':g.tex(v+1),'expected':'rejected','purpose':'incorrect expression'}])
 return {'label':label,'record':r,'checks':checks}
if __name__=='__main__':main()
