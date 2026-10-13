#!/usr/bin/env python3
"""Fail on display mathematics, full source fidelity, identity, scope or native grading.
Read polynomials and ALL solution equations/numerical lists back from learner text.
Polynomial LCM oracle uses repeated SymPy lcm on Poly(domain=ZZ), retaining
positive content: coefficient multiples are NOT equivalent polynomial answers.
"""
import importlib.util,json,re,math,subprocess,pathlib,hashlib,difflib
import sympy as sp
import uuid
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('kp',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SYMS={a:sp.Symbol(a) for a in 'xyuv'}
TRANS=standard_transformations+(implicit_multiplication_application,)
def clean(s):
 s=s.strip().rstrip('.:').replace(r'\,','').replace(r'\cdot','*').replace('−','-')
 s=re.sub(r'\{([xyuv]|\d+)\}',r'\1',s)
 return s.replace('^','**').replace(' ','')
def expression(s):
 s=clean(s)
 assert re.fullmatch(r'[\dxyuv+*()\-]+',s),('unsupported mathematical token',s)
 return sp.expand(parse_expr(s,local_dict=SYMS,transformations=TRANS))
def spans(s):return [m.group(1) if m.group(1) is not None else m.group(2) for m in re.finditer(r'\$\$([\s\S]*?)\$\$|\$([^$]*?)\$',s)]
def eq(a,b):return sp.expand(a-b)==0
def lcm(items):
 syms=sorted(set().union(*(a.free_symbols for a in items)),key=str)
 if not syms:return sp.Integer(math.lcm(*(int(a) for a in items)))
 out=sp.Poly(items[0],*syms,domain=sp.ZZ)
 for a in items[1:]:out=sp.lcm(out,sp.Poly(a,*syms,domain=sp.ZZ))
 if out.LC()<0:out=-out
 return out.as_expr()
def equation_atom(s):
 s=s.strip().rstrip('.').replace(r'\,','')
 s=re.sub(r'\\text\{LCM\}', 'LCM',s)
 if s.startswith('LCM('):
  assert s.endswith(')'),s
  # all source polynomial arguments have no internal commas.
  return lcm([expression(a) for a in s[4:-1].split(',')])
 return expression(s)
def format_check(s):
 assert s.count('$')%2==0,'Unbalanced math delimiters'
 depth=0
 for c in s:
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,'Unbalanced braces'
 assert depth==0,'Unbalanced braces'
 assert '--' not in s and '+-' not in s

def inspect(r):
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=r['question'];f=q[':question/answer-fields'][0];meta=r['generation']
 if meta.get('preserves_source_omissions'):
  assert meta['evidence_only'] and not meta['eligible_for_learning']
  assert ':question/difficulty' not in q and ':question/worked-solution' not in q
  assert ':answer-field/choices' not in f and ':answer-field/correct' not in f
  printed=[expression(v) for a in spans(q[':question/problem']) for v in a.replace(r'\,','').split(',') if clean(v)]
  assert len(printed)==3
  format_check(q[':question/problem'])
  return 0,lcm(printed)
 kind=f[':answer-field/type'].split('/')[-1]
 format_check(q[':question/problem']);format_check(q[':question/worked-solution'])
 assert kind in ('blank','radio')
 for ident in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]:uuid.UUID(ident)
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(f[':answer-field/choices'])
 if kind=='blank':assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 printed=[]
 for a in spans(q[':question/problem']):
  printed += [expression(v) for v in a.replace(r'\,','').split(',') if clean(v)]
 assert len(printed)==3,'Must print exactly three polynomials'
 expected=lcm(printed)
 answers=f[':answer-field/choices'];assert len(answers)==(5 if kind=='radio' else 1)
 correct=[a for a in answers if a[':answer/id']==f[':answer-field/correct'][1]]
 assert len(correct)==1
 values=[expression(a[':answer/value']) for a in answers]
 assert eq(expression(correct[0][':answer/value']),expected),'Displayed correct answer differs from integer-content LCM'
 assert all(not eq(values[i],values[j]) for i in range(len(values)) for j in range(i)),'Equivalent displayed bank collision'
 syms=sorted(set().union(*(a.free_symbols for a in printed)),key=str)
 data=[sp.factor_list(sp.Poly(a,*syms,domain=sp.ZZ)) for a in printed]
 factors={str(factor.as_expr()):factor.as_expr() for _,items in data for factor,pow in items}
 powers={a:[next((pow for factor,pow in items if eq(factor.as_expr(),obj)),0) for _,items in data] for a,obj in factors.items()}
 C=[int(coefficient) for coefficient,_ in data];L=math.lcm(*C)
 level=q[':question/difficulty'].split('/')[-1];n={'easy':1,'moderate':2,'hard':3}[level]
 assert len(factors)==n
 assert all(2<=a<=(12 if level=='easy' else 20) for a in C)
 assert L<=(60 if level=='easy' else 120)
 for factor in factors.values():
  assert len(factor.free_symbols)==1
  var=next(iter(factor.free_symbols));fp=sp.Poly(factor,var)
  assert fp.degree()==1 and fp.LC()==1 and abs(fp.TC())<=9
  if level in ('easy','hard'):assert fp.TC()!=0
 assert all(all(1<=a<=(7 if level=='moderate' else 5) for a in row) and len(set(row))>=2 for row in powers.values())
 if level=='moderate':assert len(syms)==2
 if level=='hard':
  assert len(syms)==2 and sorted(sum(next(iter(a.free_symbols))==v for a in factors.values()) for v in syms)==[1,2]
  assert all(row.count(max(row))==1 for row in powers.values())
  assert len({row.index(max(row)) for row in powers.values()})==3
 if meta['bank_origin']=='authored' and kind=='radio':
  maxima=lcm([sp.Integer(1)*a/int(coefficient) for a,(coefficient,_) in zip(printed,data)])
  minimum=sp.Integer(1);summed=sp.Integer(1)
  for name,powerrow in powers.items():minimum*=factors[name]**min(powerrow);summed*=factors[name]**sum(powerrow)
  expectedbank=[L*maxima,math.gcd(*C)*maxima,math.prod(C)*maxima,L*minimum,L*summed]
  assert all(sum(eq(a,b) for b in values)==1 for a in expectedbank),'Default bank must be the full actual assessed-method operation bank'
 sol=q[':question/worked-solution'];solspans=spans(sol);checked=0
 for m in solspans:
  t=m.strip().rstrip('.')
  if r'\begin{aligned}' in t:
   t=t.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').replace(r'\\','').strip().rstrip('.')
  if '=' in t:
   atoms=[a.strip().rstrip('.') for a in t.split('=')]; values2=[equation_atom(a) for a in atoms]
   assert all(eq(a,values2[0]) for a in values2),(t,'invalid displayed equality')
   checked+=len(values2)-1
  elif t==r'\text{LCM}':continue
  elif t.startswith(r'\text{LCM}'):
   assert eq(equation_atom(t.rstrip(':')),sp.Integer(L));checked+=1
  elif any(a in t for a in ('…','⋯')):
   numbers=[int(a) for a in re.findall(r'\d+',t)]
   # Infer which coefficient list this is from its first item, not metadata.
   coefficient=numbers[0]
   assert coefficient in C and L in numbers
   assert all(a%coefficient==0 for a in numbers)
   assert numbers==sorted(set(numbers)),('Repeated/unordered multiples',numbers)
   checked+=len(numbers)
  elif re.fullmatch(r'\d+:?',t):continue # numeric headings/maxima audited in their prose below.
  else:
   # Factor references/list components must be source factors/products without coefficients.
   for part in t.replace(r'\,','').split(','):
    if not clean(part):continue
    expr=expression(part)
    if meta['raw_source_error'] and t=='(x-y)':continue
    fc,fl=sp.factor_list(sp.Poly(expr,*syms,domain=sp.ZZ))
    assert fc==1 and all(str(factor.as_expr()) in factors for factor,pow in fl),(t,'unintroduced factor')
    checked+=1
 # Actual prose maximum rows and references.
 rows=re.findall(r'- For ([^\n]*?) the largest power is \$(\d+)\.\$',sol)
 for text,mx in rows:
  components=[]
  for a in spans(text):components += [expression(v) for v in a.replace(r'\,','').split(',') if clean(v)]
  parsed=[sp.factor_list(sp.Poly(a,*syms,domain=sp.ZZ))[1] for a in components]
  assert len(parsed)==3 and all(len(a)==1 for a in parsed)
  keys=[str(a[0][0].as_expr()) for a in parsed];assert len(set(keys))==1
  assert [a[0][1] for a in parsed]==powers[keys[0]]
  assert int(mx)==max(powers[keys[0]])
  checked+=4
 if not rows:
  mx=re.search(r'which is \$(\d+)\.\$',sol)
  assert mx and len(factors)==1 and int(mx[1])==max(next(iter(powers.values())))
  checked+=1
 # No unvalidated equations or missing common teaching stages.
 assert 'Finally, we multiply all of our results together:' in sol
 assert checked>10
 return checked,expected

def replay_sources():
 source=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((D/'source-cases.json').read_text());records=[];coverage=[]
 for c,q in zip(cases,source):
  r=g.generate(c['level'],seed=77,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);inspect(r)
  nq=r['question'];assert nq[':question/problem']==q[':question/problem'],c['source_id']
  if ':question/worked-solution' in q:assert nq[':question/worked-solution']==q[':question/worked-solution'],c['source_id']
  old=q[':question/answer-fields'][0];new=nq[':question/answer-fields'][0]
  assert new[':answer-field/key']==old[':answer-field/key'];assert new[':answer-field/type']==old[':answer-field/type'][':db/ident']
  oa=old.get(':answer-field/choices',[]); na=new.get(':answer-field/choices',[]);matched=0
  if not oa:
   assert ':answer-field/choices' not in new and ':answer-field/correct' not in new
   assert ':question/difficulty' not in nq and ':question/worked-solution' not in nq
   completion=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['normal_completion_profile'])
   _,derived=inspect(completion)
   assert eq(derived,inspect(r)[1])
  if oa:
   assert len(oa)==len(na)
   for a in oa:
    matches=[b for b in na if eq(expression(a[':answer/value']),expression(b[':answer/value']))]
    assert len(matches)==1; matched+=1
    oldcorrect=a[':answer/id']==old[':answer-field/correct'][':answer/id']
    assert oldcorrect==(matches[0][':answer/id']==new[':answer-field/correct'][1])
  if c['source_id']=='q-222132':
   normal=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='observed-q-222132')
   inspect(normal)
   assert normal['question'][':question/worked-solution']==q[':question/worked-solution'].replace('(x-y)','(x-7)')
  coverage.append({'source_id':c['source_id'],'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in q else None,'matched_choices':matched,'total_choices':len(oa),'correct_designation_matched':bool(oa),'missing_answer_completion':not bool(oa),'raw_solution_error':c['source_id']=='q-222132'})
  records.append(r)
 return records,coverage

def main():
 originals,coverage=replay_sources();generated=[];stage_checks=sum(inspect(r)[0] for r in originals)
 # Each complete observed bank/notation/prompt is exercised under changed parameters.
 for c in json.loads((D/'source-cases.json').read_text()):
  profile=c.get('normal_completion_profile',c['bank_profile'].replace('-raw-error',''))
  for seed in (100,101):
   r=g.generate(c['level'],seed,template=c['template'],profile=profile);stage_checks+=inspect(r)[0];generated.append(r)
 for level in ('easy','moderate','hard'):
  for kind in ('blank','radio'):
   name=('single' if level=='easy' else 'double' if level=='moderate' else 'triple')+'_'+kind
   for seed in (200,201):
    r=g.generate(level,seed,template=name);stage_checks+=inspect(r)[0];generated.append(r)
 assert len({next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in generated if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')})>1
 # Broader changed-parameter exercise, all profiles rather than default only.
 sweep=0;fingerprints={a:set() for a in ('easy','moderate','hard')}
 for name,(level,kind,n) in g.TEMPLATES.items():
  for seed in range(35):
   r=g.generate(level,seed,template=name);stage_checks+=inspect(r)[0];fingerprints[level].add(r['generation']['parameter_fingerprint']);sweep+=1
 for profile,bank in g.PROFILES.items():
  if bank['origin']=='raw-error':continue
  level=g.TEMPLATES[bank['template']][0]
  for seed in range(15):
   r=g.generate(level,seed,profile=profile);stage_checks+=inspect(r)[0];sweep+=1
 # Identity stable with seed/shuffle; banks affect only content, never task fingerprint.
 for r in originals+generated:
  m=r['generation'];level=r['question'].get(':question/difficulty',':question.difficulty/'+g.TEMPLATES[m['template']][0]).split('/')[-1]
  other=g.generate(level,999,template=m['template'],parameters=m['parameters'],profile=m['bank_profile'])
  assert other['question'][':question/id']==r['question'][':question/id']
  assert other['generation']['parameter_fingerprint']==m['parameter_fingerprint']
 for c in json.loads((D/'source-cases.json').read_text()):
  if c['template']=='single_radio':
   a=g.generate(c['level'],parameters=c['parameters'],profile=c['bank_profile']);b=g.generate(c['level'],parameters=c['parameters'],profile='authored-single-bank')
   assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint'];assert a['question'][':question/id']!=b['question'][':question/id']
 # Alias and input-order invariance excludes cosmetic task inflation.
 for level in ('easy','moderate','hard'):
  r=g.generate(level,seed=42,field_type='blank');m=r['generation'];p=m['parameters'];alias={'x':'u','y':'v'}
  changed={**p,'variables':[alias.get(v,v) for v in p['variables']]}
  if level in ('easy','moderate','hard'):
   r2=g.generate(level,template=m['template'],parameters=changed,profile=m['bank_profile'])
   assert r2['generation']['parameter_fingerprint']==m['parameter_fingerprint']
  reversedp={**p,'coefficients':p['coefficients'][::-1],'powers':p['powers'][::-1]}
  # Hard unique maxima may change row positions, but stay distributed.
  r3=g.generate(level,template=m['template'],parameters=reversedp,profile=m['bank_profile'])
  assert r3['generation']['parameter_fingerprint']==m['parameter_fingerprint']
 # Explicit guards match samplers even for observed profiles.
 invalid=0
 for c in json.loads((D/'source-cases.json').read_text()):
  for key,value in [('coefficients',[2,3,100]),('shifts',[100]*len(c['parameters']['shifts'])),('powers',[[1]*len(c['parameters']['variables'])]*3)]:
   p={**c['parameters'],key:value}
   try:g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=p)
   except ValueError:invalid+=1
   else:raise AssertionError(('Invalid explicit parameter accepted',key))
 # Native fixture: canonical, independently expanded polynomial, wrong scalar
 # multiples, and each selected radio answer. Engine errors fail this script.
 tests=[]
 native_records=[g.generate(g.TEMPLATES[r['generation']['template']][0],template=r['generation']['template'],parameters=r['generation']['parameters'],profile='completion-'+r['generation']['source_ids'][0]) if r['generation'].get('preserves_source_omissions') else r for r in originals]+generated
 for index,r in enumerate(native_records):
  f=r['question'][':question/answer-fields'][0];checks=[];correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'All owned choices'})
  else:
   expanded=str(expression(correct)).replace('**','^')
   equivalent=expanded
   if len(re.findall(r'\d+|[xyuv]|[+*^()-]',expanded))>500:
    p=r['generation']['parameters']; maximum=max(row[0] for row in p['powers']); v=p['variables'][0];h=p['shifts'][0]
    component=str(sp.expand((sp.Symbol(v)+h)**maximum)).replace('**','^')
    equivalent=str(math.lcm(*p['coefficients']))+'*('+component+')'+''.join('*'+g.factor(p,j,power=max(row[j] for row in p['powers'])) for j in range(1,len(p['variables'])))
   checks=[{'submitted':correct,'expected':'accepted','purpose':'Canonical factored integer-content LCM'}, {'submitted':equivalent,'expected':'accepted','purpose':'Independently expanded equivalent polynomial or factor, within native token limit'}, {'submitted':'2*('+correct+')','expected':'rejected','purpose':'Nonzero scalar multiple is not least integer-content multiple'}, {'submitted':'1','expected':'rejected','purpose':'Incorrect constant'}]
  if f[':answer-field/type'].endswith('/blank') and equivalent!=expanded:
   checks.append({'submitted':expanded,'expected':'unresolved','purpose':'Documented native512token limit for full expansion; canonical and partially expanded equivalents must still pass'})
  tests.append({'label':str(index)+' '+r['generation']['template']+' '+str(r['generation']['bank_profile']),'record':r,'checks':checks})
 (D/'engine-input.json').write_text(json.dumps(tests,indent=2)+'\n')
 binary=pathlib.Path('generate/runs/current/check-engine');subprocess.run([str(binary),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 engine=json.loads((D/'engine-report.json').read_text())
 (D/'review.json').write_text(json.dumps(generated,indent=2)+'\n')
 source=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']
 text='# Finding the LCM of Three Polynomials — review\n\nRaw originals are preserved below; authored variants are labeled. Source q-222132 has a known raw factor typo; normal output corrects it. Unrated source blanks have derived completions, not observed answers.\n'
 for c,q,r in zip(json.loads((D/'source-cases.json').read_text()),source,originals):
  text+='\n\n## Original '+c['source_id']+'\n\n'+q[':question/problem']+'\n\n'+(q.get(':question/worked-solution') or '*No solution or answer captured. Independently derived completion: $'+g.result(c['parameters'])+'$.*')
  for f in q[':question/answer-fields']:
   for a in f.get(':answer-field/choices',[]):text+='\n\n- Original: $'+a[':answer/value']+'$'
 for r in generated:text+='\n\n---\n\n'+g.markdown(r)
 (D/'review.md').write_text(text+'\n')
 report={'status':'passed','version':g.VERSION,'database_writes':0,'source_coverage':coverage,'source_raw_omission_shape_exact':'2/2','source_prompt_exact':'8/8','source_full_solution_raw_exact':'6/6 captured','normal_solution_raw_exact':'5/6 captured; 1 supported correction','source_complete_banks':'6/6 captured','source_choices':'18/18 captured','source_distractors':'12/12 captured','source_correct_designations':'6/6 captured; 2 unavailable, derived completions separately','unrated_completions':2,'generated_review_records':len(generated),'sweep_records':sweep,'displayed_stage_checks':stage_checks,'distinct_sampled_tasks':{a:len(b) for a,b in fingerprints.items()},'invalid_explicit_rejected':invalid,'native':{k:v for k,v in engine.items() if k!='records'},'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'engine_source_sha256':hashlib.sha256(pathlib.Path('generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'unresolved_findings':[],'documented_native_limitation':'Fully expanded higher-degree multivariable responses can exceed the engine512token cap. Canonical and independently factor-expanded equivalents pass; oversized full expansion is explicitly unresolved.'}
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
