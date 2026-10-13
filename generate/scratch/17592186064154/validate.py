#!/usr/bin/env python3
"""Independent displayed-math, source, identity, formatting and native grading QA."""
import importlib.util,json,re,pathlib,subprocess,hashlib
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor,rationalize
R=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('rate_generator',R.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
source=json.loads((R/'source.json').read_text())['record'];sources={q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']}
cases=json.loads((R/'source-cases.json').read_text())
T=S.Symbol('t',real=True);X=S.Symbol('x',positive=True)

def group(s,pos):
 assert s[pos]=='{',s[pos:]
 depth=1;j=pos+1
 while depth:
  if s[j]=='{':depth+=1
  if s[j]=='}':depth-=1
  j+=1
 return s[pos+1:j-1],j

def parse(s):
 s=s.strip().rstrip('.').replace(r'\dfrac',r'\frac')
 while r'\frac' in s or r'\sqrt' in s:
  m=re.search(r'\\(frac|sqrt)',s);pos=m.end();a,end=group(s,pos)
  if m[1]=='frac':b,end=group(s,end);rep='(('+str(parse(a))+')/('+str(parse(b))+'))'
  else:rep='sqrt('+str(parse(a))+')'
  s=s[:m.start()]+rep+s[end:]
 s=s.replace(r'\cdot','*').replace(r'\sin','sin').replace('sin⁡','sin').replace(r'\pi','pi').replace('{','(').replace('}',')').replace('^','**')
 # e is Euler's constant, never an independent variable.
 return parse_expr(s,local_dict={'e':S.E,'pi':S.pi,'t':T,'x':X,'sin':S.sin,'sqrt':S.sqrt},transformations=standard_transformations+(convert_xor,implicit_multiplication_application,rationalize),evaluate=True)

def norm(s):return re.sub(r'\s+','',s).replace('≈',r'\approx')

def balanced(s):
 assert s.count('$')%2==0
 depth=0
 for c in s:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert '@@' not in s and '--' not in s and '+-' not in s

def prompt_rates(record):
 q=record['question'];g=record['generation'];name=g['template'];problem=q[':question/problem']
 # Read supplied expressions from the displayed prompt, independently of generation values.
 math=re.findall(r'\$([^$]+)\$',problem)
 functions={}
 for s in math:
  m=re.match(r"(?:\{)?([A-Za-z])(?:\})?(?:'|\^\{'\})?\((t|x)\)\s*=\s*(.*)",s)
  if m:functions[m[1]]=parse(m[3].rstrip(',.'))
 if name.startswith('stock'):return functions['h' if name=='stock_h' else 'g'],S.Integer(0),X
 if name in ['drug','battery']:return functions['c'],S.Integer(0),T
 if name=='bacteria':return functions['G'],S.Integer(0),T
 if name=='krill':return functions['B'],S.Integer(0),T
 if name=='muons':return functions['M'],S.Integer(0),T
 if name in ['crocodiles','elephants']:return functions['B'],functions['D'],T
 if name=='pool':return functions['F'],functions['L'],T
 return functions['O'],functions['C'],T

def independent(record):
 q=record['question'];g=record['generation'];p=g['parameters'];name=g['template'];sol=q[':question/worked-solution']
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==G.KP_ID
 for text in [q[':question/problem'],sol]:balanced(text)
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];correct=field[':answer-field/correct'][1]
 assert len({a[':answer/id'] for a in choices})==len(choices)
 assert correct in [a[':answer/id'] for a in choices]
 if field[':answer-field/type'].endswith('/blank'):assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
 inflow,outflow,var=prompt_rates(record)
 # Independently recover the requested time from displayed prose, including calendar/clock context.
 problem=q[':question/problem']
 if name=='clock_factory':
  clock=re.search(r'24-hour time \$(\d+)\\text\{:\}(\d+)\$',problem);time=S.Rational(int(clock[1])*60+int(clock[2])-480,60)
 elif name in ['krill','elephants','crocodiles']:
  dates=re.findall(r'\$(\d{4})[.?]?\$',problem);time=S.Integer(dates[-1])-S.Integer(dates[0])
 elif name.startswith('stock'):time=S.Integer(re.search(r'week \$(\d+)\?',problem)[1])
 elif name=='pool':time=parse(re.search(r'pool \$([^$]+)\$ minutes after',problem)[1])
 elif name=='factory':time=parse(re.search(r'construction \$([^$]+)\$ days after',problem)[1])
 else:time=parse(re.search(r'after \$([^$]+)\$ (?:hours|microseconds)',problem)[1])
 assert time==G.exact(p['t'])
 for body in re.findall(r'\$([^$]+)\$',sol):
  for stated in re.findall(r'(?:t|x)\s*=\s*([0-9]+(?:\.[0-9]+)?)',body):assert parse(stated)==time,('stale prose substitution',name,body,time)
 r=S.simplify(inflow.subs(var,time));ex=S.simplify(outflow.subs(var,time));result=S.simplify(r-ex)
 assert r>0 and ex>=0
 d=g['round_digits'];expected=G.rnd(result,d) if d is not None else result
 assert S.simplify(expected-G.exact(g['answer']))==0
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1]
 rows=re.split(r'\\\\\s*&\s*',block)
 rhs=[]
 for row in rows:
  row=row.split('&',1)[-1].strip();approx=row.startswith('≈') or row.startswith(r'\approx');row=re.sub(r'^(?:=|≈|\\approx)\s*','',row)
  v=parse(row);rhs.append(v)
  if approx:assert abs(S.N(v-result,30))<=S.Rational(1,2)*10**(-d)
  else:assert S.simplify(v-result)==0,(name,row,v,result)
 # Stage count/shape distinguishes power reduction and individual arithmetic evaluation.
 count={'drug':3,'battery':4,'bacteria':4,'krill':3,'muons':3,'stock_h':3,'stock_g':2,'elephants':3,'crocodiles':3,'pool':3,'factory':4,'clock_factory':4}[name]
 assert len(rows)==count,(name,len(rows))
 assert '('+G.num(time)+')' in rows[0] or name.startswith('stock')
 if name in ['battery','bacteria']:assert r'\frac' in rows[2] if name=='battery' else r'\cdot' in rows[2]
 if name in ['factory','clock_factory']:assert ('sin⁡' if name=='factory' else r'\sin') in rows[1] and 'sin' not in rows[2]
 actual_values=[parse(a[':answer/value'].split('$')[1]) if '$' in a[':answer/value'] else parse(a[':answer/value']) for a in choices]
 assert len(set(str(S.simplify(v)) for v in actual_values))==len(actual_values)
 for a,v in zip(choices,actual_values):assert bool(S.simplify(v-expected)==0)==(a[':answer/id']==correct),(name,a,v,expected,correct)
 if name in ['drug','battery','bacteria','krill','muons','stock_g','stock_h'] and g['profile']=='authored_operations':assert all(v>=0 for v in actual_values)
 if g['profile']=='authored_operations':
  raw=[result,r+ex,ex-r,r,-ex] if ex else [result,2*result,result/2,G.exact(p['a']),G.exact(p['a'])*time]
  derived=[G.rnd(v,d) if d is not None else S.simplify(v) for v in raw]
 elif g['profile'].startswith('observed_'):
  derived=[]
  for item in G.DATA[name]['bank']:
   if item['recipe']=='correct':derived.append(expected)
   elif item['recipe']=='coefficient-scale':derived.append(G.rnd(G.exact(p['a'])*S.Rational(item['ratio']),item.get('decimals',0)))
   else:derived.append(G.exact(p['a'])*S.Integer(p['base'])**time)
 else:derived=[expected]
 assert sorted(str(S.simplify(v)) for v in actual_values)==sorted(str(S.simplify(v)) for v in derived),(name,'displayed recipes mismatch')
 return expected

engine=[];review=[];report={'source_total':len(cases),'banks':0,'radio_banks':0,'blank_fields':0,'options':0,'original_correct_designations':0,'repaired_correct_designations':0,'raw_prompt_exact':0,'supported_prompt_repairs':0,'raw_solution_exact':0,'notation_normalized_solutions':0,'authored_missing_solutions':0,'source_field_repairs':0}

def native(r,label):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];answers=f[':answer-field/choices'];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'every owned option'} for a in answers]
 else:
  value=next(a[':answer/value'] for a in answers if a[':answer/id']==correct)
  checks=[{'submitted':value,'expected':'accepted','purpose':'canonical fragment'},{'submitted':str(G.exact(value)+1),'expected':'rejected','purpose':'wrong fragment'}]
  eq=str(G.exact(value).p*2)+'/'+str(G.exact(value).q*2)
  rounded='round' in r['question'][':question/problem'].lower()
  checks.append({'submitted':eq,'expected':'rejected' if rounded else 'accepted','purpose':'unreduced equivalent; genuine rounded numeric instruction retains form sensitivity' if rounded else 'unreduced exact equivalent'})
 engine.append({'label':label,'record':r,'checks':checks})

for c in cases:
 r=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);independent(r);native(r,c['source_id']);review.append({'label':'Original parameter replay '+c['source_id'],'record':r})
 src=sources[c['source_id']];q=r['question'];f=q[':question/answer-fields'][0];old=src.get(':question/answer-fields',[])
 if old:
  originals=sorted(a[':answer/value'] for a in old[0][':answer-field/choices']);generated=sorted(a[':answer/value'] for a in f[':answer-field/choices']);assert originals==generated,(c['source_id'],originals,generated)
  report['options']+=len(originals);report['banks']+=1
  report['radio_banks' if f[':answer-field/type'].endswith('/radio') else 'blank_fields']+=1
  if old[0].get(':answer-field/correct'):
   ov=old[0][':answer-field/correct'][':answer/value'];nv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ov==nv;report['original_correct_designations']+=1
  else:report['repaired_correct_designations']+=1
 else:report['source_field_repairs']+=1
 if q[':question/problem']==src[':question/problem']:report['raw_prompt_exact']+=1
 else:
  assert c['template'].startswith('stock') or not old
  report['supported_prompt_repairs']+=1
 if ':question/worked-solution' not in src:report['authored_missing_solutions']+=1
 elif q[':question/worked-solution']==src[':question/worked-solution']:report['raw_solution_exact']+=1
 else:
  assert norm(q[':question/worked-solution'])==norm(src[':question/worked-solution']),(c['source_id'],'full prose/stage fidelity mismatch')
  report['notation_normalized_solutions']+=1
 # Explicit changed-parameter replay of each observed bank through public API.
 if c['bank_profile'].startswith('observed_'):
  changed=dict(c['parameters']);changed['a']=G.num(G.exact(changed['a'])*S.Rational(3,2))
  if 'b' in changed:changed['b']=G.num(G.exact(changed['b'])*S.Rational(3,2))
  if c['template']=='pool':changed['k']=str(G.exact(changed['k'])*S.Rational(3,2))
  if 'amp' in changed:changed['amp']=int(changed['amp']*S.Rational(3,2))
  if c['template']=='battery':changed['a']=100;changed['base']=4
  rr=G.generate(c['level'],template=c['template'],parameters=changed,profile=c['bank_profile']);independent(rr);native(rr,c['template']+' observed profile variant');review.append({'label':'Generated observed-profile variant '+c['template'],'record':rr})

fingerprints={};random_count=0
for template,level in G.TEMPLATES.items():
 ids=set();tasks=set()
 for seed in range(80):
  r=G.generate(level,seed,template);independent(r);random_count+=1;ids.add(r['question'][':question/id']);tasks.add(r['generation']['mathematical_fingerprint'])
  rr=G.generate(level,seed+999,template,parameters=r['generation']['parameters'],profile=r['generation']['profile']);assert rr['question'][':question/id']==r['question'][':question/id'];assert sorted(a[':answer/id'] for a in rr['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
  if seed<2:native(r,template+' generated '+str(seed));review.append({'label':'Generated default variant '+template+' '+str(seed),'record':r})
 assert len(tasks)>=(15 if template=='stock_g' else 25),(template,'too little substantive variation',len(tasks))
 fingerprints[template]={'unique_content':len(ids),'unique_math_tasks':len(tasks),'samples':80}
# Invalid hard/easy collapse and sign/time domains must reject explicit calls.
for name,changes in [('clock_factory',{'t':'7','period':14}),('clock_factory',{'amp':0}),('stock_h',{'t':0}),('battery',{'a':200}),('factory',{'t':'1/2'}),('elephants',{'k':0})]:
 p=G.sample(name,__import__('random').Random(1));p.update(changes)
 try:G.generate(G.TEMPLATES[name],template=name,parameters=p)
 except ValueError:pass
 else:raise AssertionError('invalid workload accepted '+name)
(R/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n');subprocess.run(['generate/runs/current/check-engine',str(R/'engine-input.json'),str(R/'engine-report.json')],check=True)
(R/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
text=['# Review — Determining a Rate of Change','Immutable source math basis 1356. Originals retain raw evidence below; generated replay includes explicitly supported repairs.']
for c in cases:
 src=sources[c['source_id']];text+=['## Raw source '+c['source_id'],src[':question/problem'],'Source worked solution: '+src.get(':question/worked-solution','(absent)'), 'Source values: '+json.dumps([[a[':answer/value'] for a in f.get(':answer-field/choices',[])] for f in src.get(':question/answer-fields',[])],ensure_ascii=False),'Documented repairs: '+str(c['repairs'])]
for r in review:text+=['## '+r['label'],G.markdown(r['record'])]
(R/'review.md').write_text('\n\n'.join(text)+'\n')
report.update(status='pass',random_instances=random_count,variation=fingerprints,native_grading=json.loads((R/'engine-report.json').read_text()),displayed_math='Every supplied prompt function, independently recovered time, every displayed stage and choice parsed and checked.',plots='none',unresolved_findings=['Original intent behind coefficient-scale replay distractors cannot be inferred; those profiles are opt-in and are never default.','No exact-ID newer original MA stock widget available locally. Only one derivative endpoint expression each is captured; global reciprocal-root supplied families are authored generalizations, and original h/g definitions are unavailable.','Native rounded numeric entries reject equivalent unreduced fractions, as genuine rounding is form-sensitive.'],engine_sha256=hashlib.sha256(pathlib.Path('generate/runs/current/check-engine').read_bytes()).hexdigest())
(R/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['native_grading','variation']},indent=2))
