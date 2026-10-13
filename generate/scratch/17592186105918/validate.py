#!/usr/bin/env python3
"""Independent prompt/stage math, source fidelity, scope, identity, native grading."""
import importlib.util,json,hashlib,re,subprocess,sys,itertools
from fractions import Fraction
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
D=Path(__file__).parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('kp_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x');TRANS=standard_transformations+(implicit_multiplication_application,)
def math(t):
 t=t.strip().rstrip('.')
 t=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1)/(\2)',t)
 t=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',t)
 t=t.replace('\\cdot','*').replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(t,local_dict={'x':X},transformations=TRANS)
def parse_vector(t):
 if t.startswith('⟨'):return [math(e) for e in t[1:-1].split(',')]
 if t.startswith('['):return [math(e) for e in t[len('[\\begin{aligned}'):-len('\\end{aligned}]')].split(' \\\\ ')]
 out=[]
 for b in 'ijk':
  match=re.search(r'(^|[+-])([^ijk+-]*)'+b,t)
  if match:
   sign,c=match.groups();out.append(math(('-' if sign=='-' else '')+(c or '1')))
  else:out.append(sp.S(0))
 return out

def check_format(text):
 assert text.count('$')%2==0,'Unbalanced math delimiters'
 balance=0
 for i,c in enumerate(text):
  if c in '{}' and (i==0 or text[i-1]!='\\'):
   balance+=1 if c=='{' else -1
   assert balance>=0,'Unbalanced brace'
 assert balance==0,'Unbalanced braces'
 assert '+-' not in text and '--' not in text,'Ungrouped signed math'

def verify(r,allow_alias_error=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];meta=r['generation'];f=q[':question/answer-fields'][0]
 assert f[':answer-field/correct'][0]==':answer/id'
 choices=f[':answer-field/choices'];ids=[a[':answer/id'] for a in choices]
 assert len(set(ids))==len(ids) and f[':answer-field/correct'][1] in ids
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in choices]:check_format(text)
 vals=[math(a[':answer/value']) for a in choices]
 assert len(set(vals))==len(vals)
 ans=math(next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1]))
 prompt=q[':question/problem'];sol=q[':question/worked-solution'];level=q[':question/difficulty'].split('/')[-1]
 if level=='easy':
  assert 'perpendicular' in prompt or '$90^\\circ$' in prompt
  assert ans==0
  if '$90^\\circ$' in prompt:
   angle=sp.pi/2
   assert sp.cos(angle)==ans
   blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==1
   rows=blocks[0].split(' \\\\ & =');assert len(rows)==4
   rhs=[rows[0].split(' & =')[1]]+rows[1:]
   theta=sp.Symbol('theta')
   for value in rhs:
    value=value.replace('|a|','M').replace(r'\cos\theta','*cos(theta)').replace(r'\cos(90^\circ)','*cos(pi/2)')
    assert sp.simplify(math(value).subs(theta,angle))==0,'Printed right-angle scalar projection stage'
  else:
   assert 'perpendicular' in sol and '$0.$' in sol
  return
 m=re.match(r'Let \$([a-z])=(.*?)\$ and \$([a-z])=(.*?)\.\$',prompt);assert m
 n1,a,n2,b=m.groups();p,qq=parse_vector(a),parse_vector(b)
 prod=[sp.expand(a*b) for a,b in zip(p,qq)];dot=sp.expand(sum(prod))
 assert sp.degree(dot,X)==1 and dot.coeff(X)!=0
 expected=sp.solve(dot,X)[0];assert sp.simplify(ans-expected)==0
 assert all(sum(c.subs(X,expected)**2 for c in v)!=0 for v in (p,qq))
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
 rows=blocks[0].split(' \\\\  & =');assert len(rows)==3
 assert sp.expand(math(rows[1])-dot)==0,'Printed dot substitution differs from prompt'
 assert sp.expand(math(rows[2])-dot)==0,'Printed collected dot differs from prompt'
 formal=rows[0]
 if not allow_alias_error:
  assert formal.startswith(n1+r'\cdot '+n2)
  assert all('{'+n+'}_{'+c+'}' in formal for n in (n1,n2) for c in 'xyz')
  assert ('$'+n1+'$') in sol and ('$'+n2+'$') in sol
 # Validate every displayed solve equation, and exact final conclusion from prompt.
 equations=blocks[1].split(' \\\\ ')
 for row in equations:
  left,right=row.split(' & =')
  if '\\cdot' in left and not re.search(r'\d',left):continue
  lhs,rhs=math(left),math(right)
  assert sp.simplify((lhs-rhs).subs(X,expected))==0,'Displayed solving row incorrect'
 assert equations[-1].startswith('x & =') and math(equations[-1].split(' & =')[1])==expected
 A=dot.coeff(X);B=dot.subs(X,0)
 if level=='hard':
  assert sum(t.has(X) for t in prod)==2 and all(t!=0 for t in prod) and abs(A)>=2
  assert len(equations)==4
 else:assert sum(t.has(X) for t in prod)==1
 # Check method-derived bank equations independently from actual prompt.
 profile=meta['profile'];known=[a*b for a,b in zip(p,qq) if not (a*b).has(X) and a*b!=0]
 if profile=='method:two-products':want=[expected,-expected,-known[0]/A,-known[1]/A,-B]
 elif profile=='method:two-products-unit':want=[expected,-expected,-known[0]/A,-known[1]/A,(known[0]-known[1])/A]
 elif profile=='method:one-product' or profile=='method:one-product-unit':
  aa,bb=next((a,b) for a,b in zip(p,qq) if not (a*b).has(X) and a*b!=0)
  want=[expected,-expected,-B,aa,bb] if profile=='method:one-product' else [expected,-expected,aa,bb,-(aa+bb)/A]
 elif profile=='method:hard':
  cs=[t.coeff(X) for t in prod if t.has(X)];want=[expected,-expected,-B/cs[0],-B/cs[1],-B]
 else:want=vals
 assert sorted(map(str,map(sp.simplify,vals)))==sorted(map(str,map(sp.simplify,want)))

def engine_item(label,r):
 f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  for a in f[':answer-field/choices']:
   checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned choice grading'})
 else:
  a=f[':answer-field/choices'][0][':answer/value'];val=math(a)
  checks=[{'submitted':a,'expected':'accepted','purpose':'canonical exact fragment'},{'submitted':f'({sp.numer(val)*3})/({sp.denom(val)*3})','expected':'accepted','purpose':'unreduced mathematically equivalent rational fragment'},{'submitted':str(val+1),'expected':'rejected','purpose':'incorrect fragment'}]
 return {'label':label,'record':r,'checks':checks}

def run():
 sources=json.load(open(D/'source.json'))['record'][':knowledge-point/questions'];cases=json.load(open(D/'source-cases.json'))
 records=[];engine=[];review=[];fidelity=[];bank_count=0;option_count=0
 for src,c in zip(sources,cases):
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']);q=r['question']
  verify(r,allow_alias_error=c['source_id']==17592186292830)
  for k in (':question/difficulty',':question/problem',':question/worked-solution',':question/answer-fields'):assert (k in src)==(k in q)
  assert q[':question/problem']==src[':question/problem'] and q[':question/worked-solution']==src[':question/worked-solution']
  f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
  assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  rawvals=[math(a[':answer/value']) for a in sf[':answer-field/choices']];newvals=[math(a[':answer/value']) for a in f[':answer-field/choices']]
  assert sorted(map(str,rawvals))==sorted(map(str,newvals))
  correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert math(correct)==math(sf[':answer-field/correct'][':answer/value'])
  bank_count+=sf[':answer-field/type'][':db/ident'].endswith('radio');option_count+=len(rawvals)
  fidelity.append({'source_id':c['source_id'],'prompt_exact':True,'worked_solution_exact':True,'complete_bank_match':True,'correct_match':True,'presence_match':True,'documented_alias_error':c['source_id']==17592186292830})
  records.append(r);engine.append(engine_item('Observed source replay '+c['template'],r));review.append('## Captured original '+c['template']+'\n\n'+src[':question/problem']+'\n\nBank: '+', '.join(a[':answer/value'] for a in sf[':answer-field/choices'])+'\n\n'+src[':question/worked-solution']+'\n\n'+g.markdown(r))
  # Two genuinely changed parameter sets per exact source mask/profile, public API.
  orig=[[g.exact(v) for v in c['parameters'][k]] for k in ('p','q')]
  unknown=next((i,j) for i,v in enumerate(orig) for j,t in enumerate(v) if t==X)
  for factor in (-1,2):
   vectors=[list(v) for v in orig]
   for j in range(3):
    if j!=unknown[1] and vectors[0][j]!=X and vectors[0][j].is_Integer:vectors[0][j]*=factor
   # When x occurs in p, its other coordinates scaled above; when x occurs in q,
   # preserve the coefficient of x while varying all other p coordinates.
   params={k:list(map(str,v)) for k,v in zip(('p','q'),vectors)}
   v=g.generate('moderate',seed=5,template=c['template'],parameters=params,profile=c['profile']);verify(v,allow_alias_error=c['source_id']==17592186292830)
   records.append(v);engine.append(engine_item('Generated observed-profile variant '+c['template']+' factor '+str(factor),v));review.append(g.markdown(v))
  # Normal authored method bank/presentation alongside each observed bank.
  for seed in (31,71):
   v=g.generate('moderate',seed=seed,template=c['template']);verify(v);records.append(v);engine.append(engine_item('Generated normal variant '+c['template']+' seed '+str(seed),v));review.append(g.markdown(v))
 for level in ('easy','hard'):
  for template,cfg in g.TEMPLATES.items():
   if cfg['level']==level:
    for seed in (31,71):
     r=g.generate(level,seed,template);verify(r);records.append(r);engine.append(engine_item('Authored missing-level variant '+template+' seed '+str(seed),r));review.append(g.markdown(r))
 domain=json.load(open(D/'finite-domains.json'));hard_tasks=set();radio_tasks=set();hard_tuples=radio_tuples=0
 values=[n for n in range(-6,7) if n]
 for a,b,c,d in itertools.product(values,repeat=4):
  A=a+c;B=b*d
  if a==c or abs(A)<2:continue
  task=(tuple(sorted((Fraction(a,A),Fraction(c,A)))),Fraction(B,A));hard_tasks.add(task);hard_tuples+=1
  if len(set([-Fraction(B,A),Fraction(B,A),-Fraction(B,a),-Fraction(B,c),-B]))==5:radio_tasks.add(task);radio_tuples+=1
 assert (hard_tuples,len(hard_tasks),radio_tuples,len(radio_tasks))==(domain['hard_valid_blank_parameter_tuples'],domain['hard_normalized_mathematical_tasks'],domain['hard_valid_radio_parameter_tuples'],domain['hard_radio_normalized_mathematical_tasks'])
 coverage={};variety={};positions={}
 for level in ('easy','moderate','hard'):
  seen=set();fingerprints=set();correct_positions=set()
  for seed in range(200):
   r=g.generate(level,seed);verify(r)
   f=r['question'][':question/answer-fields'][0]
   if f[':answer-field/type'].endswith('/radio'):correct_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
   seen.add(r['generation']['template']);fingerprints.add(r['generation']['mathematical_fingerprint'])
   # Order changes preserve identity and mathematical fingerprint.
   again=g.generate(level,seed+999,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'])
   assert r['question'][':question/id']==again['question'][':question/id'] and r['generation']['mathematical_fingerprint']==again['generation']['mathematical_fingerprint']
  assert seen=={t for t,c in g.TEMPLATES.items() if c['level']==level},'Default family coverage'
  coverage[level]=sorted(seen);variety[level]=len(fingerprints);positions[level]=sorted(correct_positions)
  if level!='easy':assert correct_positions==set(range(5))
 assert variety['easy']==1 and variety['moderate']>100 and variety['hard']>100
 # Explicit workload guard failures must never silently resample.
 for level,template,params in [('hard','two-linear-terms',{'p':['x','sqrt(2)','2'],'q':['3','x','1']}),('hard','two-linear-terms',{'p':['x','0','2'],'q':['3','x','1']}),('hard','two-linear-terms',{'p':['x','-3','2'],'q':['3','x','1']}),('moderate','q-236734',{'p':['-1','1','2'],'q':['4','x','0']}),('moderate','q-236734',{'p':['-1','1','7'],'q':['4','x','1']})]:
  try:g.generate(level,template=template,parameters=params)
  except ValueError:pass
  else:raise AssertionError('Explicit invalid workload accepted')
 cli=subprocess.run([sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--seed','42','--count','2','--format','json'],text=True,capture_output=True)
 assert cli.returncode==0,cli.stderr
 cli_records=json.loads(cli.stdout);assert len(cli_records)==6
 for r in cli_records:verify(r)
 (D/'cli-review.json').write_text(cli.stdout)
 md=subprocess.run([sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--seed','42','--count','2','--format','markdown'],text=True,capture_output=True)
 assert md.returncode==0 and md.stdout.count('### Generated variant:')==6
 (D/'cli-review.md').write_text(md.stdout)
 (D/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n');(D/'review.md').write_text('# Review: observed originals and clearly labeled generated variants\n\nOpaque observed radio patterns are evidence only; normal method banks follow each source mask. Easy/hard are authored level designs.\n\n'+'\n\n'.join(review))
 (D/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
 native=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine.json')],text=True,capture_output=True)
 assert native.returncode==0,native.stderr
 print(native.stdout.strip());native_report=json.load(open(D/'engine.json'))
 frozen={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [D.with_suffix('.py'),D/'recipes.json',D/'source.json',D/'validate.py',D/'finite-domains.json',ROOT/'generate/runs/current/check-engine',ROOT/'generate/runs/current/check-engine.rs',ROOT/'generate/runs/current/engine-build.log']}
 result={'status':'passed','source':g.SOURCE,'source_questions':len(sources),'source_exact_prompt_matches':len(sources),'source_exact_solution_matches':len(sources),'source_raw_complete_bank_matches':len(sources),'source_radio_bank_matches':bank_count,'source_options_matched':option_count,'source_correct_designations_matched':len(sources),'source_key_presence_matches':len(sources),'raw_mathematical_answers_correct':len(sources),'documented_source_prose_alias_errors':1,'normal_source_alias_repairs':1,'cli_json_and_markdown_verified':True,'generated_review_records':len(records),'default_family_coverage':coverage,'sampled_200_meaningful_fingerprints':variety,'correct_choice_positions':positions,'finite_domains':domain,'easy_semantic_domain_size':1,'easy_supplied_information_forms':2,'native_grading':{k:native_report[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'frozen_sha256':frozen,'fidelity':fidelity,'database_writes':0,'scope':'Steps 3–7 only; easy/hard authored; opaque historical radio patterns evidence-only.'}
 (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','source_questions','source_options_matched','sampled_200_meaningful_fingerprints','native_grading']}))
if __name__=='__main__':run()
