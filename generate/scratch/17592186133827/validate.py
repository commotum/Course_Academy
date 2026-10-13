#!/usr/bin/env python3
"""Independent printed-TeX audits + complete raw fidelity + real native grading."""
import importlib.util,json,sys,re,subprocess,hashlib,random
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
sys.dont_write_bytecode=True
ROOT=Path(__file__).parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t=g.t;u=g.u;x,y,z=g.x,g.y,g.z;i,j,k=S.symbols('i j k')

def write(name,val):(ROOT/name).write_text(json.dumps(val,indent=2,ensure_ascii=False)+'\n')
def group(s,pos,opening='{',closing='}'):
 assert s[pos]==opening,(s,pos)
 depth=1;end=pos+1
 while depth:
  assert end<len(s),(s,pos)
  depth += (s[end]==opening)-(s[end]==closing);end+=1
 return s[pos+1:end-1],end

def parse(value):
 s=value.strip().rstrip('.,').replace('⁡','').replace('π',r'\pi').replace('−','-')
 s=re.sub(r'\\(?:left|right|big|Big|bigl|bigr)\s*','',s)
 s=s.replace(r'\,',' ').replace(r'\!','').replace(r'\cdot','*').replace(r'\times','*')
 s=re.sub(r'\\operatorname\{(sin|cos)\}',r'\\\1',s)
 while '\\' in s:
  match=re.search(r'\\(d?frac|sqrt|sin|cos|pi)',s)
  assert match,('unsupported',s)
  command=match[1];pos=match.end()
  if command=='pi':result='pi'
  elif command in ('frac','dfrac'):
   a,pos=group(s,pos);b,pos=group(s,pos);result='(('+str(parse(a))+')/('+str(parse(b))+'))'
  elif command=='sqrt':
   n='2'
   if s[pos]=='[':n,pos=group(s,pos,'[',']')
   a,pos=group(s,pos);result='(('+str(parse(a))+')**(1/('+n+')))'
  else:
   power='1'
   if s[pos:pos+1]=='^':
    pos+=1
    if s[pos]=='{':power,pos=group(s,pos)
    else:power=s[pos];pos+=1
   while pos<len(s) and s[pos].isspace():pos+=1
   if s[pos]=='{':a,pos=group(s,pos)
   elif s[pos]=='(':a,pos=group(s,pos,'(',')')
   else:
    mm=re.match(r'[tuxyz](?:\^\{[^}]+\})?',s[pos:]);assert mm,s[pos:];a=mm[0];pos+=len(a)
   result=command+'('+str(parse(a))+')**('+str(parse(power))+')'
  s=s[:match.start()]+result+s[pos:]
 s=re.sub(r'\|([^|]+)\|',r'Abs(\1)',s)
 s=s.replace('{','(').replace('}',')').replace('[','(').replace(']',')')
 return parse_expr(s,local_dict={'x':x,'y':y,'z':z,'t':t,'u':u,'i':i,'j':j,'k':k,'pi':S.pi,'sin':S.sin,'cos':S.cos,'Abs':S.Abs},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def equal(a,b):return S.simplify(S.trigsimp(a-b))==0

def fmt(s):
 assert all(ord(c)>=32 or c in ('\n','\t','\r') for c in s), 'Unintended control character in learner display'
 assert s.count('$')%2==0
 depth=0
 for n,c in enumerate(s):
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert '--' not in s and '+-' not in s

def rows(sol):
 return [[r.split('& =',1)[1].strip() for r in b.split(r'\\') if '& =' in r] for b in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)]
def read_integral(expr):
 start=expr.index(r'{\int }_');factor=parse(expr[:start]) if start else S.Integer(1);pos=start+len(r'{\int }_');a,pos=group(expr,pos);assert expr[pos]=='^';b,pos=group(expr,pos+1)
 var='u' if expr.endswith(r'\text{d}u') else 't';body=expr[pos:expr.rindex(r'\,\text{d}')]
 return parse(a),parse(b),factor*parse(body),var

def prompt_object(q):
 prompt=q[':question/problem']; f=parse(re.search(r'\$f\([^$]*?\)=(.*?)\$',prompt)[1]);rv=re.search(r'r\(t\)=\\langle (.*?)\\rangle',prompt)[1];r=tuple(parse(c) for c in rv.split(','));ab=re.search(r't\\in \[(.*?),(.*?)\]\.\$',prompt);a,b=parse(ab[1]),parse(ab[2]);return f,r,a,b

COUNTS={'instances':0,'derived_rows':0}
def audit(rec):
 q=rec['question']; assert set(rec['knowledge_point'])=={'db_id','id','title'};fmt(q[':question/problem']);fmt(q[':question/worked-solution'])
 f,r,a,b=prompt_object(q);fr=S.simplify(f.subs(dict(zip((x,y,z),r)),simultaneous=True));dr=tuple(S.diff(c,t) for c in r);speed=S.sqrt(S.expand(sum(c*c for c in dr)))
 family=rec['generation']['template']
 if family=='sine_line':speed=S.sqrt(sum(S.simplify(c/S.cos(t))**2 for c in dr))*S.cos(t)
 integrand=S.simplify(fr*speed);sol=q[':question/worked-solution'];blocks=rows(sol);assert len(blocks)==5
 # Formal ds row references the actual named curve exactly once.
 assert sol.count(r"\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t")==1
 ops=re.findall(r'\\frac\{\\text\{d\}\}\{\\text\{d\}t\}\((.*?)\)\\,([ijk])',blocks[1][1])
 assert len(ops)==len(r)
 for (display,basis),actual in zip(ops,r):assert equal(parse(display),actual)
 assert equal(parse(blocks[1][2]),sum(v*base for v,base in zip(dr,(i,j,k))))
 assert blocks[1][3].count(r'\frac{\text{d}')==len(r)
 for row in blocks[1][4:]:
  value=parse(row)
  assert equal(value**2,speed**2),('speed stage',row,speed)
 for row in blocks[2]:assert equal(parse(row),fr),('substituted f',row,fr)
 if family=='cubic':assert len(blocks[2])==3 and blocks[2][1].count('t^3')==2 and '+' in blocks[2][1], 'lost separate cubic expansion operands'
 if family=='ratio':assert len(blocks[2])==3 and blocks[2][1].endswith('{t}'), 'lost cancelled denominator row'
 if family=='sine_line':assert blocks[2][1].count(r'\sin^2 t')==2 and '+' in blocks[2][1] and blocks[1][5].count(r'\cos^2 t')==2, 'lost separate squared components'
 if family=='cos_diagonal':assert len(blocks[2])==1, 'redundant substitution row'
 assert rec['generation']['mathematical_fingerprint']==g.digest([[str(v) for v in r],str(f),str(a),str(b)])
 assert 'f(r(t))' in blocks[3][0] and r"\|r'(t)\|" in blocks[3][0]
 for row in blocks[3][1:]:
  aa,bb,body,var=read_integral(row);assert equal(aa,a) and equal(bb,b) and equal(body,integrand) and var=='t',('setup',row,integrand)
 v=parse(re.search(r'substitution \$u=(.*?)\$',sol)[1]);dv=parse(re.search(r'\$\\text\{d\}u=\((.*?)\)\\,\\text\{d\}t\$',sol)[1]);assert equal(S.diff(v,t),dv)
 aa,bb,transformed,var=read_integral(blocks[4][0]);assert var=='u' and equal(aa,v.subs(t,a)) and equal(bb,v.subs(t,b))
 assert equal(transformed.subs(u,v)*dv,integrand),('substitution',transformed,dv,integrand)
 pi=2 if family=='space_ratio' else 1
 if pi==2:
  aa2,bb2,body2,var2=read_integral(blocks[4][1]);assert equal(aa2,aa) and equal(bb2,bb) and equal(body2,transformed) and var2=='u'
 prim=parse(blocks[4][pi].split(r'\big|')[0]);assert equal(S.diff(prim,u),transformed)
 upper=S.simplify(prim.subs(u,bb));lower=S.simplify(prim.subs(u,aa));answer=S.simplify(upper-lower)
 for row in blocks[4][pi+1:]:assert equal(parse(row),answer),('endpoint arithmetic',row,answer)
 # Individually evaluated BOTH endpoint components, not an oracle for only difference.
 rr=blocks[4][-2]; assert rr.startswith('(');up,pos=group(rr,0,'(',')');assert rr[pos:pos+2]=='-(';lo,pos=group(rr,pos+1,'(',')');assert equal(parse(up),upper) and equal(parse(lo),lower)
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];assert len(choices)==5
 values=[parse(v[':answer/value']) for v in choices]
 assert g.unique_bank(values)
 correct=field[':answer-field/correct'][1];assert equal(next(parse(c[':answer/value']) for c in choices if c[':answer/id']==correct),answer)
 assert sum(equal(value,answer) for value in values)==1
 # independently re-evaluate every method recipe from the PRINTED curve/integrand.
 p=rec['generation']['parameters']; metadata_values=list(map(S.sympify,rec['generation']['choice_values']))
 assert all(any(equal(v,w) for w in metadata_values) for v in values)
 # Every displayed wrong value is rederived from displayed method operands.
 W=S.simplify(transformed/(S.cos(u) if family=='cos_diagonal' else u**2 if family=='sine_line' else S.sqrt(u)))
 if family=='cos_diagonal':
  aa_curve=S.expand(r[0]).coeff(t,2);bb_curve=S.expand(r[1]).coeff(t,2);kk=S.simplify(fr/S.cos(r[0]))
  expected=[answer,answer*2*aa_curve,W*(S.cos(bb)-S.cos(aa)),W*(S.sin(b)-S.sin(a)),kk*(aa_curve+bb_curve)/aa_curve*(S.sin(bb)-S.sin(aa))]
 elif family=='sine_line':
  L=S.simplify(speed/S.cos(t));actualsq=S.integrate(fr*speed**2,(t,a,b))
  expected=[answer,answer/L,actualsq,W*(bb**3-aa**3),W*(bb**2-aa**2)/2]
 elif family=='sin_cos':
  ss=S.simplify(r[1]/S.sin(t));actualsq=S.integrate(S.expand_trig(fr*speed**2),(t,a,b));omitted=S.integrate(fr,(t,a,b))
  expected=[answer,omitted,actualsq,answer*(-2*ss**2),2*W*(S.sqrt(bb)-S.sqrt(aa))]
 else:
  coefficient=S.expand(dv).coeff(t,3 if family=='cubic' else 1)
  omitted=S.integrate(fr,(t,a,b))
  expected=[answer,answer*coefficient,2*W*(S.sqrt(bb)-S.sqrt(aa)),upper+lower,omitted]
 assert len(values)==len(expected) and all(any(equal(v,w) for w in expected) for v in values),('method bank',family,values,expected)
 COUNTS['instances']+=1;COUNTS['derived_rows']+=sum(len(b) for b in blocks)
 return answer

def engine(rec,label):
 field=rec['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'field-owned radio selection'} for a in field[':answer-field/choices']]}

def main():
 sources=[];cases=[];eng=[];review=[];markdown=[]
 for sid,source in g.SOURCES.items():
  family=g.SOURCE_TEMPLATE[sid];level=g.LEVELS[family];rec=g.generate(level,seed=13,template=family,profile='raw:'+sid,parameters={'scale':1});q=rec['question'];field=q[':question/answer-fields'][0];original=source[':question/answer-fields'][0]
  assert q[':question/problem']==source[':question/problem'];assert q.get(':question/worked-solution')==source.get(':question/worked-solution');fmt(q[':question/problem']);fmt(q.get(':question/worked-solution',''))
  for attribute in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (attribute in q)==(attribute in source)
  assert (':answer-field/correct' in field)==(':answer-field/correct' in original)
  assert sorted(a[':answer/value'] for a in field[':answer-field/choices'])==sorted(a[':answer/value'] for a in original[':answer-field/choices'])
  assert field[':answer-field/key']==original[':answer-field/key'] and field[':answer-field/type']==original[':answer-field/type'][':db/ident']
  if ':answer-field/correct' in original:
   correct=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert correct[':answer/value']==original[':answer-field/correct'][':answer/value'];eng.append(engine(rec,'raw '+sid))
  anchor=g.mathematics(family,g.ANCHORS[family]);assert any(equal(v,anchor['answer']) for v in g.SOURCE_VALUES[sid])
  for k0 in (2,5):
   rr=g.generate(level,profile='raw:'+sid,parameters={'scale':k0});assert sorted(a[':answer/value'] for a in rr['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(g.scaled(a[':answer/value'],k0) for a in original[':answer-field/choices'])
   assert rr['generation']['mathematical_fingerprint']!=rec['generation']['mathematical_fingerprint']
   fmt(rr['question'][':question/problem']);fmt(rr['question'].get(':question/worked-solution',''))
   scaledvalues=[parse(c[':answer/value']) for c in rr['question'][':question/answer-fields'][0][':answer-field/choices']]
   assert all(any(equal(v,k0*parse(a[':answer/value'])) for a in original[':answer-field/choices']) for v in scaledvalues)
  normal=g.generate(level,template=family,parameters=g.ANCHORS[family]);assert normal['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
  cases.append({'source_id':sid,'template':family,'level':level,'parameters':{'scale':1},'bank_profile':'raw:'+sid})
  sources.append({'id':sid,'prompt_exact':True,'full_bank_exact':True,'option_count':5,'solution_exact':':question/worked-solution' in source,'correct_designation_exact':':answer-field/correct' in original,'raw_presence_exact':True})
  review.append(rec);markdown +=['## Original evidence '+sid,q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in field[':answer-field/choices']),q.get(':question/worked-solution','No original worked solution or correct ref; inferred correct is $\\frac43(2\\sqrt2-1)$.')]
  variant=g.generate(level,profile='raw:'+sid,parameters={'scale':2});review.append(variant);markdown += ['### Generated opaque bank scale variant (evidence only)',variant['question'][':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in variant['question'][':question/answer-fields'][0][':answer-field/choices']),variant['question'].get(':question/worked-solution','Original worked solution absent.')]
 # At least two normal examples for EACH source-shaped family, including easy.
 for family,level in g.LEVELS.items():
  for seed in range(12):
   rec=g.generate(level,seed,template=family);audit(rec)
   same=g.generate(level,seed+111,template=family,parameters=rec['generation']['parameters']);assert rec['question'][':question/id']==same['question'][':question/id'] and rec['generation']['mathematical_fingerprint']==same['generation']['mathematical_fingerprint'];eng.append(engine(rec,family+' '+str(seed)))
   if seed<2:review.append(rec);markdown+=['## Generated '+level+' / '+family+' (authored bank)',rec['question'][':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']),rec['question'][':question/worked-solution']]
 # Default sampling must cover every observed eligible family.
 defaultfamilies={g.generate('moderate',n)['generation']['template'] for n in range(60)};assert defaultfamilies=={f for f,l in g.LEVELS.items() if l=='moderate'}
 # Explicit rejection cannot resample invalid inputs or collapse hard to planar.
 for family,p in [('space_ratio',dict(a=1,b=0,c=1,k=1,lo=1,hi=2)),('ratio',dict(a=1,h=1,k=13,ma=3,mb=5)),('parabola_easy',dict(k=0,m=3))]:
  try:g.generate(g.LEVELS[family],template=family,parameters=p)
  except ValueError:pass
  else:raise AssertionError('invalid explicit accepted')
 # Regression: mathematically equivalent collapsed rows must still be rejected.
 rec=g.generate('moderate',4,template='cubic');bad=json.loads(json.dumps(rec));old=rows(bad['question'][':question/worked-solution'])[2][1];bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(old,g.tex(g.mathematics('cubic',rec['generation']['parameters'])['fr']),1)
 try:audit(bad)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('collapsed expansion accepted')
 # Regression: endpoint primitive or derivative removal must fail an actual display audit.
 rec=g.generate('moderate',4,template='cubic');bad=json.loads(json.dumps(rec));bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(r'\frac{\text{d}}{\text{d}t}',r'\frac{\text{d}}{\text{d}u}',1)
 try:audit(bad)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('missing formal derivative accepted')
 bad=json.loads(json.dumps(rec));bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(g.tex(g.mathematics('cubic',rec['generation']['parameters'])['upper']), '999999',1)
 try:audit(bad)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('corrupt endpoint accepted')
 write('source-cases.json',cases);write('source-fidelity.json',sources);write('review.json',review);(ROOT/'review.md').write_text('\n\n'.join(markdown)+'\n');write('engine-input.json',eng)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
 native=json.loads((ROOT/'engine-validation.json').read_text())
 # Exact finite meaningful counts; full bank validity enumerated, no cosmetic aliases.
 counts={}
 for family in g.LEVELS:
  eligible=0;rejected=0;eligibility={}
  # Positive scalar factors k, 1/d, and common cubic f coefficients cannot
  # change a bank collision. These keys quotient ONLY bank validity, never
  # task identity. The finite parameter -> (curve,f,interval) map is injective.
  for p in g.domain(family):
   if family=='ratio':key=(p['a'],p['ma'],p['mb'])
   elif family=='parabola_easy':key=(p['m'],)
   elif family=='cubic':key=(p['s'],p['n'])
   elif family=='cos_diagonal':key=(p['a'],p['b'],p['angle'])
   elif family=='sine_line':key=(p['p']**2+p['q']**2,p['angle'])
   elif family=='sin_cos':key=(p['s'],)
   else:key=(p['a'],p['b']**2+p['c']**2,p['b']+p['c'],p['lo'],p['hi'])
   if key not in eligibility:
    m=g.mathematics(family,p);b0=g.banks(family,p,m);eligibility[key]=g.unique_bank([v for _,v in b0])
   if eligibility[key]:eligible+=1
   else:rejected+=1
  counts[family]={'candidate_parameter_sets':len(g.domain(family)),'eligible_mathematical_tasks':eligible,'whole_bank_collisions':rejected,'distinct_bank_eligibility_cases_exactly_checked':len(eligibility),'task_count_proof':'Parameter tuple injects into the exact displayed curve, scalar function and interval; scalar coefficient quotients used only for bank collision checks.'}
 write('domain-counts.json',counts)
 write('validation.json',{'status':'passed with documented raw source defects','source_basis':1356,'practice_sources':6,'raw_prompts_exact':6,'raw_complete_banks_exact':6,'raw_options_exact':30,'raw_solutions_exact':5,'source_solutions_present':5,'raw_correct_designations_exact':5,'source_correct_designations_present':5,'source_designated_distractors_exact':20,'source_designated_distractors_present':20,'source_undesignated_options_exact':5,'raw_presence_exact':6,'inferred_missing_correct_refs':1,'normal_instances':COUNTS['instances'],'displayed_derived_rows':COUNTS['derived_rows'],'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'native_unresolved':native['documented_unresolved_checks'],'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'finite_domains':counts,'database_writes':0,'limitations':['Scalar historical distractor intent is opaque; raw profiles are evidence-only homogeneous extensions.','q-76187 has no original solution, difficulty or correct ref; these omissions are retained in public raw replay.','Raw q-76479 wrong derivative basis labels and q-76484 derivative label/missing cosine argument are retained as evidence and corrected in normal solutions.','No blank fields observed or authored; native algebraic blank equivalence tests are inapplicable.']})
 print(json.dumps({'normal_checks':COUNTS,'source_banks':'6/6','source_values':'30/30','native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')}}))
if __name__=='__main__':main()
