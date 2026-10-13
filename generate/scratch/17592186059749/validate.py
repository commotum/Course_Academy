#!/usr/bin/env python3
"""Fail-closed source fidelity, actual printed matrix/stages, native-grader QA."""
import collections,copy,hashlib,importlib.util,itertools,json,pathlib,re,subprocess,uuid
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
R=pathlib.Path(__file__).parent;ROOT=R.parents[2]
spec=importlib.util.spec_from_file_location('detgen',R.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((R/'source.json').read_text());sources={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};cases=json.loads((R/'source-cases.json').read_text())
def require(b,msg):
 if not b:raise AssertionError(msg)
def parse(text):
 # Independent conversion (not the generator's parser).
 text=text.strip().rstrip('.').replace(r'\left','').replace(r'\right','')
 def group(pos):
  require(text[pos]=='{','group opening');depth=1;i=pos+1
  while i<len(text) and depth:depth+=(text[i]=='{')-(text[i]=='}');i+=1
  require(depth==0,'group closing');return text[pos+1:i-1],i
 while '\\frac' in text or '\\sqrt' in text:
  match=re.search(r'\\(frac|sqrt)',text);a,end=group(match.end())
  if match[1]=='frac':b,end=group(end);replacement='(('+str(parse(a))+')/('+str(parse(b))+'))'
  else:replacement='sqrt('+str(parse(a))+')'
  text=text[:match.start()]+replacement+text[end:]
 text=text.replace(r'\cdot','*').replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(text,local_dict={a:S.Symbol(a,real=True) for a in 'xyzrstu'},transformations=standard_transformations+(implicit_multiplication_application,))
def equal(a,b):return S.simplify(a-b)==0
def matrix(text):
 matches=re.findall(r'\\begin\{(?:aligned|vmatrix)\}((?:(?!\\begin).)*?)\\end\{(?:aligned|vmatrix)\}',text,re.S)
 # The first prompt matrix always has exactly four scalars.
 require(matches,'matrix displayed');entries=re.split(r'&|\\\\',matches[0]);require(len(entries)==4,'four actual entries');return [parse(a.strip()) for a in entries]
def balanced(text):
 require(text.count('$')%2==0,'math delimiters');depth=0
 for c in text:
  depth+=(c=='{')-(c=='}');require(depth>=0,'brace nesting')
 require(depth==0 and '--' not in text and '+-' not in text,'formatting')
def independent(rec):
 q=rec['question'];meta=rec['generation'];name=meta['template'];p=meta['parameters'];g.guard(name,p)
 require(set(rec['knowledge_point'])=={'db_id','id','title'},'outer shape');require(rec['knowledge_point']['db_id']==g.KP_ID,'KP')
 uuid.UUID(q[':question/id']);balanced(q[':question/problem']);balanced(q[':question/worked-solution'])
 E=matrix(q[':question/problem']);a,b,c,d=E;ad=S.expand(a*d);bc=S.expand(b*c);answer=S.simplify(ad-bc)
 solution=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);require(len(blocks)==2,'two math blocks')
 require(blocks[0]==r'|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.','formal ad−bc stage')
 require(solution.startswith('For a $2\\times 2$ matrix, the determinant is given by the formula\n\n'),'whole opening prose')
 require('Using the formula, we have'+(':' if g.TEMPLATES[name][1]=='radio' else '')+'\n\n' in solution,'transition prose')
 # Remove inner matrix before splitting the outer aligned rows.
 require(all(equal(a,b) for a,b in zip(matrix(blocks[1]),E)),'solution matrix agrees with prompt')
 raw=blocks[1];inner=re.search(r'\|\\begin\{aligned\}.*?\\end\{aligned\}\|',raw)
 require(inner,'solution determinant matrix');raw=raw[:inner.start()]+'DET'+raw[inner.end():]
 raw=raw.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
 rows=re.split(r'\\\\',raw);rhs=[row.split('& =',1)[1].strip().rstrip('.') for row in rows]
 arithmetic=[a for a in rhs if a!='DET'];require(arithmetic,'arithmetic stages')
 # Check the printed multiplication inputs in their exact ad−bc order.
 first=arithmetic[0];parts=first.split(r'\cdot ');require(len(parts)==3,'two ordered products')
 # Independent expected ordered component spelling, including every sign.
 et=[g.tex(a) for a in E]
 expected=et[0]+r'\cdot '+('('+et[3]+')' if et[3].startswith('-') else et[3])+'-'+('('+et[1]+')' if et[1].startswith('-') else et[1])+r'\cdot '+('('+et[2]+')' if et[2].startswith('-') else et[2])
 require(first==expected,'ordered substituted ad−bc factors')
 require(all(equal(parse(stage),answer) for stage in arithmetic),'every actual displayed arithmetic stage')
 # Structurally validate intermediate products/subtraction/collection/factoring,
 # not merely their simplified equality. Displayed inputs determine these rows.
 expected_tail=[]
 if name in ('numeric_radical','easy_fraction','one_fraction','two_fractions','four_fractions'):expected_tail=[g.diff(g.tex(ad),g.tex(bc))]
 elif name in ('shared_monomial','factored_polynomial'):expected_tail=[g.add(g.tex(ad),g.tex(-bc))]
 elif name=='factored_bilinear':expected_tail=[g.diff(g.tex(ad),g.tex(bc)),g.add(g.tex(ad),g.tex(-bc))]
 require(arithmetic[1:1+len(expected_tail)]==expected_tail,'ordered product/subtraction stages')
 require(len(arithmetic)==(3 if name in ('easy_fraction','one_fraction','two_fractions','four_fractions','shared_monomial','factored_polynomial') else 4 if name=='factored_bilinear' else 2),'full stage count')
 f=q[':question/answer-fields'][0];require(len(q[':question/answer-fields'])==1,'one field');uuid.UUID(f[':answer-field/id'])
 kind=f[':answer-field/type'].split('/')[-1];choices=f[':answer-field/choices'];require(len(choices)==(5 if kind=='radio' else 1),'whole bank count')
 if kind=='blank':require('{{'+f[':answer-field/key']+'}}' in q[':question/problem'],'blank placeholder')
 vals=[parse(a[':answer/value']) for a in choices];require(all(not equal(a,b) for i,a in enumerate(vals) for b in vals[i+1:]),'bank collision')
 require(sum(equal(a,answer) for a in vals)==1,'exactly one correct value')
 cid=f[':answer-field/correct'];require(cid[0]==':answer/id' and any(a[':answer/id']==cid[1] and equal(parse(a[':answer/value']),answer) for a in choices),'designation')
 for a in choices:uuid.UUID(a[':answer/id']);require(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'],'answer schema')
 expected=g.digest({'version':g.VERSION,'prompt':q[':question/problem'],'solution':solution,'kind':kind,'bank':sorted(a[':answer/value'] for a in choices)})
 require(expected==meta['content_hash'] and q[':question/id']==g.ident(expected),'content identity')
 require(meta['math_fingerprint']==g.digest([S.srepr(a) for a in E]),'bank-independent canonical math fingerprint')
 return answer

def fail(fn,label):
 try:fn()
 except (ValueError,AssertionError):return
 raise AssertionError('Negative control passed: '+label)
originals=[];details=[];options=0;designations=0;solutions=0
for case in cases:
 rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);independent(rec);originals.append(rec)
 old=sources[case['source_id']];q=rec['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 require(q[':question/problem']==old[':question/problem'],'source prompt '+case['source_id'])
 ov=[parse(a[':answer/value']) for a in of[':answer-field/choices']];nv=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 require(len(ov)==len(nv) and all(sum(equal(a,b) for b in nv)==1 for a in ov),'complete original bank '+case['source_id']);options+=len(ov)
 if ':answer-field/correct' in of:
  a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);require(equal(parse(a[':answer/value']),parse(of[':answer-field/correct'][':answer/value'])),'source designation');designations+=1
 if ':question/worked-solution' in old:require(q[':question/worked-solution']==old[':question/worked-solution'],'complete source prose/math '+case['source_id']);solutions+=1
 details.append({'source_id':case['source_id'],'complete_bank_match':True,'source_designation_matched':':answer-field/correct' in of,'worked_solution_exact':':question/worked-solution' in old,'missing_designation_inferred':case['source_id']=='q-1088'})
variants=[];tests=[];counts=collections.defaultdict(set);profile_counts={}
# Every template is independently exercised, all observed complete banks included.
for name,spec in g.TEMPLATES.items():
 for i in range(30):
  rec=g.generate(spec[0],seed=1000+i,template=name);independent(rec);tests.append(rec);counts[spec[0]].add(rec['generation']['math_fingerprint'])
  if i<2:variants.append(rec)
for case in cases:
 if not case['bank_profile'].startswith('observed-'):continue
 for i in range(12):
  rec=g.generate(case['level'],seed=2000+i,template=case['template'],profile=case['bank_profile']);independent(rec)
  tests.append(rec)
  if i<2:variants.append(rec)
 profile_counts[case['bank_profile']]=12
# Exhaust every sign combination in the numerical hard workload.
for signs in itertools.product((-1,1),repeat=4):
 p=dict(g.DEFAULTS['four_fractions'])
 for key,sign in zip(('p','b','c','d'),signs):p[key]=abs(p[key])*sign
 rec=g.generate_hard(parameters=p);independent(rec);tests.append(rec);counts['hard'].add(rec['generation']['math_fingerprint'])
# Identity must ignore seed/order and profile alias, but include displayed banks.
for case,rec in zip(cases,originals):
 other=g.generate(case['level'],seed=324,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);require(rec['question'][':question/id']==other['question'][':question/id'],'seed stable identity')
 p=dict(case['parameters']);default=g.generate(case['level'],seed=44,template=case['template'],parameters=p)
 if case['bank_profile'].startswith('observed-'):require(default['question'][':question/id']!=rec['question'][':question/id'],'changed bank identity')
negative=0
for template,p in [('four_fractions',dict(g.DEFAULTS['four_fractions'],p=3)),('four_fractions',dict(g.DEFAULTS['four_fractions'],q=30)),('two_fractions',dict(g.DEFAULTS['two_fractions'],j=1)),('one_fraction',dict(g.DEFAULTS['one_fraction'],p=-2,q=4)),('easy_fraction',dict(g.DEFAULTS['easy_fraction'],d=11)),('numeric_radical',dict(g.DEFAULTS['numeric_radical'],n=4)),('linear_power',dict(g.DEFAULTS['linear_power'],a=0))]:
 fail(lambda:g.generate(g.TEMPLATES[template][0],template=template,parameters=p),template+' guard');negative+=1
fail(lambda:g.generate('moderate',template='numeric_radical'),'wrong level');negative+=1
fail(lambda:g.generate('easy',profile='observed-q-nonexistent'),'invalid profile');negative+=1
fail(lambda:g.generate('easy',template='numeric_radical',profile='blank'),'invalid radio profile');negative+=1
# Entire authored bank collision: ad==−bc produces duplicated wrong products.
fail(lambda:g.generate('easy',template='easy_fraction',parameters={'q':2,'b':5,'c':1,'d':10}),'whole bank collision');negative+=1
for which in ['prompt','formal','substitution','product','solution','answer','id']:
 bad=copy.deepcopy(originals[3]);q=bad['question']
 if which=='prompt':q[':question/problem']=q[':question/problem'].replace('17','19')
 elif which=='formal':q[':question/worked-solution']=q[':question/worked-solution'].replace('ad-bc','ab-cd')
 elif which=='substitution':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\frac{1}{2}\cdot 10-17\cdot 1',r'17\cdot 1-\frac{1}{2}\cdot 10')
 elif which=='product':q[':question/worked-solution']=q[':question/worked-solution'].replace('5-17','5-19')
 elif which=='solution':q[':question/worked-solution']=q[':question/worked-solution'].replace('Using the formula, we have:','Using a different rule:')
 elif which=='answer':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999'
 else:q[':question/answer-fields'][0][':answer-field/correct'][1]=str(uuid.uuid4())
 fail(lambda:independent(bad),which);negative+=1
# Representative native grading plus every source and observed bank variant.
engine=[]
for i,rec in enumerate(originals+variants+tests[::15]):
 f=rec['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual owned-choice grader after independent scalar validation'} for a in f[':answer-field/choices']]
 else:
  value=f[':answer-field/choices'][0][':answer/value'];E=matrix(rec['question'][':question/problem']);component=g.diff(g.mul(g.tex(E[0]),g.tex(E[3])),g.mul(g.tex(E[1]),g.tex(E[2])))
  checks=[{'submitted':v,'expected':expected,'purpose':purpose} for v,expected,purpose in [(value,'accepted','canonical'),(component,'accepted','unevaluated actual determinant product difference'),('('+value+')+1','rejected','wrong scalar')]]
 engine.append({'label':str(i),'record':rec,'checks':checks})
(R/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n');binary=ROOT/'generate/runs/current/check-engine';result=subprocess.run([str(binary),str(R/'engine-input.json'),str(R/'engine-report.json')],capture_output=True,text=True);(R/'engine.log').write_text(result.stdout+result.stderr);require(result.returncode==0,'native grader: engine.log')
(R/'review.json').write_text(json.dumps({'original_replays':originals,'generated_variants':variants},indent=2)+'\n')
parts=['# Determinant review','All raw sources are retained in source.json. q-1088 has authored easy assignment/solution and inferred correct choice; observed intent is not claimed. All hard questions are authored numerical arithmetic extensions.']
for case,rec in zip(cases,originals):
 raw=sources[case['source_id']];parts+=['## Original '+case['source_id'],raw[':question/problem'],'Raw bank: '+json.dumps([a[':answer/value'] for a in raw[':question/answer-fields'][0][':answer-field/choices']]),raw.get(':question/worked-solution','(No original worked solution)'),'### Generator replay',g.markdown(rec)]
for rec in variants:parts+=['## Generated variant / '+rec['generation']['template']+' / '+rec['generation']['bank_profile'],g.markdown(rec)]
(R/'review.md').write_text('\n\n'.join(parts)+'\n')
report={'status':'pass','source_coverage':{'sources':13,'exact_prompts':13,'complete_banks_matched':13,'displayed_values_matched':options,'original_designations_matched':designations,'missing_designations_inferred':1,'original_solutions_exact':solutions,'original_solutions_available':12,'authored_missing_solution':1},'source_details':details,'generated_instances':len(tests),'meaningful_tasks_by_level':{k:len(v) for k,v in counts.items()},'observed_profile_varied_tests':profile_counts,'negative_controls':negative,'native_grading':{'status':'pass','records':len(engine),'checks':sum(len(a['checks']) for a in engine),'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest()},'limitations':['Source scalar distractor author intent is underdetermined; explicit observed recipes are replay patterns and normal defaults are separately authored operation banks.','q-1088 lacks an original designation, difficulty and solution; inferred/authored items are counted separately.','Hard is an authored missing-level numerical fraction workload, not a recovered source label.'],'provenance':{k:source[k] for k in ('database','basis','lineage')}}
(R/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
