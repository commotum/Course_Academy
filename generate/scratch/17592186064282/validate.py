"""Independent printed-function/operator/chain/evaluation/tangent readback."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent;R=D.parents[2]
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('independent_reader',D/'tex-parser.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x,u,y=p.x,p.u,p.y
for fn in ('sec','csc','cot','tan'):p.functions[fn]=lambda arg,fn=fn:getattr(s,fn)(arg,evaluate=False)

def read(t):return p.scalar(t.replace(r'\dfrac',r'\frac').replace('[','(').replace(']',')').strip('$'))
def derive(F,v=x):
 if not F.has(s.sec,s.csc,s.cot):return s.diff(F,v)
 terms=s.Add.make_args(F);term=next(z for z in terms if z.has(s.sec,s.csc,s.cot));trig=next(iter(term.atoms(s.sec,s.csc,s.cot)));arg=trig.args[0];coef=term/trig
 fn=lambda name:getattr(s,name)(arg,evaluate=False)
 outer={s.sec:fn('sec')*fn('tan'),s.csc:-fn('csc')*fn('cot'),s.cot:-fn('csc')**2}[trig.func]
 return coef*outer*s.diff(arg,v)+s.diff(F-term,v)

def equivalent(a,b):
 if a==b:return True
 delta=a-b
 parity={}
 for f in delta.atoms(s.sin,s.cos,s.sec,s.csc,s.tan,s.cot):
  arg=s.expand(f.args[0]);turn=arg.coeff(s.pi);shift_sign=1
  if turn.is_Integer:
   arg=arg-turn*s.pi;shift_sign=(-1)**int(turn) if f.func in (s.sin,s.cos,s.sec,s.csc) else 1
  negative=arg.could_extract_minus_sign();arg=-arg if negative else arg;parity[f]=shift_sign*(-1 if negative and f.func in (s.sin,s.csc,s.tan,s.cot) else 1)*(f.func(arg,evaluate=False) if arg.free_symbols else f.func(arg))
 delta=delta.xreplace(parity);sub={};circles=[]
 for i,arg in enumerate(sorted({f.args[0] for f in delta.atoms(s.sin,s.cos,s.sec,s.csc,s.tan,s.cot)},key=str)):
  si,co=s.symbols('Q'+str(i)+' P'+str(i));circles.append((si,co));sub.update({s.sin(arg):si,s.cos(arg):co,s.sec(arg):1/co,s.csc(arg):1/si,s.tan(arg):si/co,s.cot(arg):co/si})
 num=s.cancel(delta.xreplace(sub)).as_numer_denom()[0]
 for si,co in circles:num=s.rem(num,si*si+co*co-1,si)
 return s.expand(num)==0

def blocks(text):return [z.strip().rstrip('.,') for z in re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)]
def prompt(q):
 bs=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',q[':question/problem'],re.S)
 F=None
 for b in bs:
  m=re.search(r'(?:f\(x\)|y)\s*=\s*(.+)',b)
  if m and re.search(r'\\(?:operatorname\{)?(?:sec|csc|cot)',m[1]):F=read(m[1]);break
 assert F is not None,'printed function absent'
 assert F.free_symbols<={x}
 trig=list(F.atoms(s.sec,s.csc,s.cot));assert len(trig)==1
 term=next(t for t in s.Add.make_args(F) if t.has(trig[0]));tail=F-term;inner=trig[0].args[0];outer=term.subs(trig[0],trig[0].func(u))
 # Read x0 from the printed point or evaluation instruction, independently.
 x0=None
 if 'equation of the tangent' in q[':question/problem']:
  b=next(b for b in bs if ',' in b and re.search(r'\(|\\left\(',b));point=b.replace(r'\left','').replace(r'\right','').strip().rstrip('.')
  if point.startswith('(') and point.endswith(')'):x0,y0=[read(t) for t in point[1:-1].split(',')]
  else:raise AssertionError('printed tangent point shape')
  assert equivalent(F.subs(x,x0),y0),'point is off printed curve'
 elif 'slope' in q[':question/problem']:
  candidates=[b for b in bs if re.match(r'x\s*=',b)]
  assert len(candidates)==1;c=candidates[0];x0=read(c.split('=',1)[1])
 if x0 is not None:
  arg=s.simplify(inner.subs(x,x0));den=s.cos(arg) if trig[0].func==s.sec else s.sin(arg);assert den!=0,'evaluation pole'
 return F,x0,inner,outer,tail

def verify(r,source_fidelity=True):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];g.validate_generated_record(r);F,x0,inner,outer,tail=prompt(q);level=q[':question/difficulty'].split('/')[-1]
 assert level in g.SUPPORTED_LEVELS
 assert s.degree(inner,x) in (1,2,3)
 if level=='easy':assert x0 is None and tail==0
 if level=='moderate':assert x0 is not None or tail!=0
 if level=='hard':assert x0 is not None and 'equation of the tangent' in q[':question/problem']
 derivative=derive(F);ans=derivative if x0 is None else s.simplify(derivative.subs(x,x0));y0=None if x0 is None else s.simplify(F.subs(x,x0))
 expected=[ans]
 if level=='hard':expected=[ans,y0-ans*x0] if len(q[':question/answer-fields'])==2 else [ans*x+y0-ans*x0]
 for f,val in zip(q[':question/answer-fields'],expected):
  assert f[':answer-field/type'] in (':answer-field.type/blank',':answer-field.type/radio')
  pairs=[]
  for a in f[':answer-field/choices']:
   raw=a[':answer/value'];assert '$' not in raw and a[':answer/type']==':answer.type/math'
   if '=' in raw:lhs,rhs=raw.split('=');assert lhs.strip()=='y';v=read(rhs)
   else:v=read(raw)
   assert v.free_symbols<={x};pairs.append((a[':answer/id'],v))
  correct=[aid for aid,v in pairs if equivalent(v,val)];assert correct==[f[':answer-field/correct'][1]],'printed bank/key error'
  assert all(not equivalent(v,w) for i,(_,v) in enumerate(pairs) for _,w in pairs[:i]),'printed bank collision'
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  else:assert len(pairs)==5
 sol=q[':question/worked-solution'];bs=blocks(sol)
 if source_fidelity:assert sol==g.normal_solution(r['generation']['template'],r['generation']['parameters']['a']),'source prose/stage drift'
 # Independent shape readback uses source profile stage counts, never generic rows.
 observed=g.QUESTIONS[r['generation']['template']][':question/worked-solution']
 assert [len(z.split(r'\\')) for z in bs]==[len(z.split(r'\\')) for z in blocks(g.normal_solution(r['generation']['template'],1))],'ordered stage counts drift'
 assert sol.count('First,')==observed.count('First,')
 assert sol.count('Differentiating gives')==observed.count('Differentiating gives')
 assert 'We now apply the chain rule' in sol
 if x0 is not None:assert sol.count('Evaluating at')==observed.count('Evaluating at')
 if level=='hard':assert 'Finally, we find the equation of the tangent' in sol
 functions={'f':F,'y':F,'g':F-tail,'h':tail}
 formal_count=0
 def expression(t):
  nonlocal formal_count
  t=t.strip().rstrip('.,').replace(r'\left','').replace(r'\right','')
  t=re.sub(r'\\(?:d?frac)\{\\(?:textrm|text)(?:\{d\}|\s+d)\s*([yfghu])\}\{\\(?:textrm|text)(?:\{d\}|\s+d)\s*([xu])\}',lambda m:r'\frac{\mathrm{d}'+m[1]+'}{'+r'\mathrm{d}'+m[2]+'}',t)
  t=re.sub(r'\{([fygh])\}\^\{′\}',lambda m:m[1]+r'\prime',t)
  t=re.sub(r'([fygh])\'\s*',lambda m:m[1]+r'\prime',t)
  # Source boxed scalar wrappers retain their complete nested mathematical value.
  t=re.sub(r'\\bbox\[[^]]*\]', '',t)
  t=t.replace(r'\require{cancel}','')
  t=re.sub(r'\\prime(?!\()',lambda _:r'\prime(x)',t)
  evaluated='{|}_{x=' in t or r'\atX0' in t
  t=t.replace(r'\atX0','')
  t=re.sub(r'\{\|\}_\{x=[^}]*\}', '',t)

  # Actual formal operators, with dependent function and independent variable.
  def op(m):
   nonlocal formal_count
   fn,v=m[1],m[2];formal_count+=1
   if fn=='u':assert v=='x';value=s.diff(inner,x)
   elif v=='u':assert fn in (('g',) if tail else ('f','y'));value=derive(outer,u).subs(u,inner)
   else:assert v=='x' and fn in functions;value=derive(functions[fn])
   return '('+s.latex(value)+')'
  t=re.sub(r'\\frac\{\\mathrm\{d\}([yfghu])\}\{\\mathrm\{d\}([xu])\}',op,t)
  def prime(m):
   nonlocal formal_count
   fn,arg=m[1],read(m[2]);formal_count+=1;assert fn in functions
   assert arg==x or x0 is not None and equivalent(arg,x0),'formal prime evaluated at wrong input'
   return '('+s.latex(derive(functions[fn]).subs(x,arg))+')'
  t=re.sub(r'([yfgh])\\prime\((.*?)\)',prime,t)
  t=re.sub(r'([fgh])\(x\)',lambda m:'('+s.latex(functions[m[1]])+')',t)
  t=t.replace('{y}_{1}','y_1').replace('{x}_{1}','x_1')
  t=t.replace('y_1','('+s.latex(y0)+')') if y0 is not None else t
  t=t.replace('x_1','('+s.latex(x0)+')') if x0 is not None else t
  if x0 is not None:t=re.sub(r'(?<![A-Za-z])m(?![A-Za-z])',lambda _: '('+s.latex(ans)+')',t)
  if t=='u':return inner
  if t in ('f','g') or t=='y' and level!='hard':return outer.subs(u,inner)
  value=read(t).subs(u,inner)
  return value.subs(x,x0) if evaluated else value
 nrows=0
 for b in bs:
  b=re.sub(r'\{\|\}_\{x=[^}]*\}',lambda _:r'\atX0',b)
  b=b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace(r'\require{cancel}','');b=re.sub(r'\\\\\[[^]]*\]',lambda _:r'\\',b);b=b.replace(r'\text{and}',r'\qquad').replace(r'\,',r'\qquad');prev=None
  for row in b.split(r'\\'):
   for seg in row.split(r'\qquad'):
    seg=seg.strip().lstrip(',').strip().rstrip('.,');seg=seg.replace('&','')
    if not seg:continue
    parts=seg.split('=');assert len(parts)>=2,(seg,'expected equality')
    # Chained source equalities are checked successively as complete objects.
    lhs=parts[0].strip() or prev;assert lhs is not None;prev=lhs
    parsed=[expression(lhs)]+[expression(rhs) for rhs in parts[1:]]
    if level=='hard':parsed=[z.subs(y,ans*x+y0-ans*x0) if z.has(y) else z for z in parsed]
    for A,B in zip(parsed,parsed[1:]):assert equivalent(A,B),(seg,A,B);nrows+=1
 assert formal_count>=5
 return {'rows':nrows,'formal_operators':formal_count,'task':g.digest([s.srepr(F),s.srepr(x0) if x0 is not None else None,level])}

def save(name,v):(D/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def scrub(q):
 q=copy.deepcopy(q);q.pop(':question/id',None)
 for f in q.get(':question/answer-fields',[]):
  f.pop(':answer-field/id',None)
  if ':answer-field/correct' in f:
   key=f[':answer-field/correct'][1];f[':answer-field/correct']=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key)
  for a in f[':answer-field/choices']:a.pop(':answer/id',None)
 return q

def checks(r):
 out=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  val=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/radio'):
   out+=[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'field-owned answer ID'} for a in f[':answer-field/choices']]
   out += [{'field_index':i,'submitted':'999999','expected':'unresolved','purpose':'expected native foreign answer ID gate'}]
  else:
   parsed=read(val);trigs=parsed.atoms(s.sec,s.csc,s.cot,s.tan)
   if trigs:
    sub={f:({s.sec:1/s.cos(f.args[0]),s.csc:1/s.sin(f.args[0]),s.cot:s.cos(f.args[0])/s.sin(f.args[0]),s.tan:s.sin(f.args[0])/s.cos(f.args[0])}[f.func]) for f in trigs};alt=s.latex(parsed.xreplace(sub))
   elif r'\sqrt' in val:alt=re.sub(r'\\sqrt\{(\d+)\}',lambda m:r'\frac{'+m[1]+r'}{\sqrt{'+m[1]+'}}',val)
   else:
    F,x0,*_=prompt(r['question']);m=s.simplify(derive(F).subs(x,x0));y0=s.simplify(F.subs(x,x0));alt=s.latex(y0)+'+('+s.latex(m)+')(x-('+s.latex(x0)+'))'
   assert alt!=val
   out += [{'field_index':i,'submitted':val,'expected':'accepted','purpose':'canonical blank'}, {'field_index':i,'submitted':alt,'expected':'accepted','purpose':'independent reciprocal identity / rationalized radical / point-slope blank'}, {'field_index':i,'submitted':'0','expected':'rejected','purpose':'wrong zero blank'}, {'field_index':i,'submitted':r'('+val+r')+1','expected':'rejected','purpose':'wrong offset blank'}, {'field_index':i,'submitted':'','expected':'unresolved','purpose':'expected native incomplete-submission gate'}]
 return out

def main():
 records=[];reviews=[];raw=[];counts={'prompts':0,'full_records_with_omissions':0,'full_banks':0,'values':0,'correct_designations':0,'solutions':0,'feedback_attributes':0};tasks={l:set() for l in g.SUPPORTED_LEVELS};coverage={};rows=0
 for k,l in g.LEVELS.items():
  rr=g.generate(l,template=k,parameters={'a':1},profile='raw:'+k);original=g.clean(g.QUESTIONS[k]);assert scrub(rr['question'])==original,(k,'raw mismatch');raw.append(rr)
  counts['full_records_with_omissions']+=1;counts['prompts']+=1;counts['solutions']+=int(':question/worked-solution' in original);counts['feedback_attributes']+=sum('feedback' in key for f in original.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[]) for key in a)
  counts['full_banks']+=len(original.get(':question/answer-fields',[]));counts['values']+=sum(len(f[':answer-field/choices']) for f in original.get(':question/answer-fields',[]));counts['correct_designations']+=sum(':answer-field/correct' in f for f in original.get(':question/answer-fields',[]))
  changed=g.generate(l,template=k,parameters={'a':2},profile='raw:'+k);assert scrub(changed['question'])!=original;reviews.append({'role':'Math Academy captured source and raw replay','source_id':k,'original':g.QUESTIONS[k],'replay':rr,'changed_raw':changed})
  if l=='unrated':continue
  coverage[k]=[]
  for a in range(1,9 if k=='q-310222' else 10):
   r=g.generate(l,template=k,parameters={'a':a});v=verify(r);rows+=v['rows'];records.append(r);tasks[l].add(v['task']);coverage[k].append(a)
  reviews.append({'role':'normal source-family completion or repaired presentation','source_id':k,'records':[g.generate(l,template=k,parameters={'a':a}) for a in (1,2)]})
 # Replay all raw banks at originals independently as whole values; mathematical
 # error412 remains preserved raw and excluded from normal. Missing keys stay absent.
 source_values=[];raw_changed_values=0
 for k,l in g.LEVELS.items():
  for a in range(1,10):
   rr=g.generate(l,template=k,profile='observed_raw',parameters={'a':a});q=rr['question'];F,x0,inner,outer,tail=prompt(q);correct=derive(F) if x0 is None else s.simplify(derive(F).subs(x,x0))
   if l=='hard':expected=[correct,F.subs(x,x0)-correct*x0] if len(q.get(':question/answer-fields',[]))==2 else [correct*x+F.subs(x,x0)-correct*x0]
   else:expected=[correct]
   for f,val in zip(q.get(':question/answer-fields',[]),expected):
    vs=[read(z[':answer/value'].split('=')[-1]) for z in f[':answer-field/choices']];match=[z[':answer/id'] for z,v in zip(f[':answer-field/choices'],vs) if equivalent(v,val)];assert len(match)==1,(k,a,'changed raw bank')
    if ':answer-field/correct' in f:assert match==[f[':answer-field/correct'][1]]
    assert all(not equivalent(v,w) for i,v in enumerate(vs) for w in vs[:i]);raw_changed_values+=len(vs)
    if a==1:source_values.extend(vs)
 # Negative controls target rendered math, structural stages, input and domain.
 negative=[];specimen=g.generate('hard',template='q-342412',parameters={'a':2})
 for kind in ('outer-sign','inner-factor','formal-input','chain-component','substitution','point','key','structure'):
  r=copy.deepcopy(specimen);q=r['question'];t=q[':question/worked-solution']
  if kind=='outer-sign':q[':question/worked-solution']=t.replace(r'-2\csc',r'2\csc',1)
  elif kind=='inner-factor':q[':question/worked-solution']=t.replace(r'\dfrac{\pi}{2} x^{2}',r'\dfrac{\pi}{3} x^{2}',1)
  elif kind=='formal-input':q[':question/worked-solution']=t.replace("m=f'(1)","m=f'(2)",1)
  elif kind=='chain-component':q[':question/worked-solution']=t.replace(r'\cdot',r'+',1)
  elif kind=='substitution':q[':question/problem']=q[':question/problem'].replace('x^{3}','x^{2}',1)
  elif kind=='point':q[':question/problem']=q[':question/problem'].replace('(1,4)','(1,5)')
  elif kind=='key':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='0'
  else:q[':question/worked-solution']=t.replace('Differentiating gives','',1)
  assert r!=specimen,kind
  try:verify(r,source_fidelity=False)
  except (AssertionError,ValueError,TypeError):negative.append(kind)
  else:raise AssertionError('mutation survived '+kind)
 pole=g.generate('moderate',template='q-342405',parameters={'a':2});pole['question'][':question/problem']=pole['question'][':question/problem'].replace(r'\dfrac{1}{2}',r'\frac{1}{\sqrt{2}}')
 try:verify(pole,source_fidelity=False)
 except AssertionError as e:assert 'pole' in str(e);negative.append('evaluation-pole')
 else:raise AssertionError('evaluation pole accepted')
 for bad in (r'\dfrac x 13',r'\dfrac 1 13',r'\dfrac 12 13',r'\frac{12}13',r'\frac12{13}'):
  try:read(bad)
  except ValueError:negative.append('unbraced-multi-digit:'+bad)
  else:raise AssertionError('multi-digit TeX fraction shorthand accepted')
 shorthand=g.generate('moderate',template='q-31341',parameters={'a':9})
 shorthand['question'][':question/problem']=shorthand['question'][':question/problem'].replace(r'\dfrac{x}{13}',r'\dfrac x 13')
 try:verify(shorthand,source_fidelity=False)
 except ValueError:negative.append('rendered-fraction-argument-mutation')
 else:raise AssertionError('rendered multi-digit fraction mutation survived')
 assert read(r'\frac{12}{13}')==s.Rational(12,13)
 assert read(r'\dfrac 4 5')==s.Rational(4,5)
 fraction_cases=[]
 for a in range(1,10):
  for profile in (None,'observed_raw'):
   r=g.generate('moderate',template='q-31341',parameters={'a':a},profile=profile);q=r['question']
   for key in (':question/problem',':question/worked-solution'):p.validate_fraction_shorthand(q[key])
   F,x0,inner,outer,tail=prompt(q);assert equivalent(inner,1-x/(a+4));assert x0==1
   if a>=6:
    assert r'\dfrac{x}{'+str(a+4)+'}' in q[':question/problem']
    assert r'\dfrac{1}{'+str(a+4)+'}' in q[':question/worked-solution']
    assert r'\dfrac{'+str(a+3)+'}{'+str(a+4)+'}' in q[':question/worked-solution']
   fraction_cases.append({'a':a,'profile':profile or 'normal','denominator':a+4,'fraction_argument_guard':'pass'})
 save('fraction-render-validation.json',fraction_cases)
 for a in (0,10,-1,1.5):
  try:g.generate('easy',template='q-31333',parameters={'a':a})
  except ValueError:negative.append('bound:'+str(a))
  else:raise AssertionError('invalid bound accepted')
 try:g.generate('easy',template='q-310222',parameters={'a':9})
 except ValueError:negative.append('serving-bound:q-310222/a9')
 else:raise AssertionError('unsupported learner bound accepted')
 for bad in ({},{'a':True},{'a':2,'extra':3}):
  try:g.generate('easy',template='q-31333',parameters=bad)
  except ValueError:negative.append('explicit-parameters:'+str(bad))
  else:raise AssertionError('explicit parameter fallback accepted')
 for level in g.SUPPORTED_LEVELS:
  batch=g.batch(level,count=5,seed=3);assert len({r['generation']['parameter_fingerprint'] for r in batch})==5
 assert len({r['question'][':question/id'] for r in records})==len(records)
 for r in records:assert r==g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed'],template=r['generation']['template'],parameters=r['generation']['parameters']),(r['generation']['template'],'determinism')
 diagnostic=g.generate('easy',template='q-310222',parameters={'a':9},profile='observed_raw');df=diagnostic['question'][':question/answer-fields'][0];dv=df[':answer-field/choices'][0][':answer/value']
 inputs=[{'label':str(i)+'/'+r['generation']['template'],'record':r,'checks':checks(r)} for i,r in enumerate(records)];inputs.append({'label':'raw-only-unsupported-upper-bound','record':diagnostic,'checks':[{'field_index':0,'submitted':'0','expected':'unresolved','purpose':'raw-only unsupported domain witness at a9'},{'field_index':0,'submitted':'('+dv+')+1','expected':'unresolved','purpose':'raw-only unsupported wrong offset at a9'}]});save('grader-input.json',inputs)
 subprocess.run([str(R/'generate/runs/current/check-engine'),str(D/'grader-input.json'),str(D/'grader-report.json')],check=True,timeout=60);native=json.loads((D/'grader-report.json').read_text());assert native['documented_unresolved_checks']==2+sum(len(r['question'][':question/answer-fields']) for r in records)
 for row in native['records']:
  for check in row['checks']:
   if check['outcome']=='unresolved':assert (check['reason']=='answer every field before submitting' and check['submitted']=='') or (check['reason']=='selected answer does not belong to this field' and check['submitted']=='999999') or (check['purpose'].startswith('raw-only unsupported') and check['reason'] in ('symbolic equivalence is not established by the supported rules','answer comparison has unresolved domain differences'))
 save('source-cases.json',[{'source_id':k,'template':k,'difficulty':l,'parameters':{'a':1},'bank_profile':'raw:'+k} for k,l in g.LEVELS.items()]);save('review.json',reviews)
 out=[]
 for row in reviews:
  out.append('## '+row['source_id']+' — '+row['role'])
  if 'original' in row:out.extend(['Original:\n'+row['original'][':question/problem']+'\n\n'+row['original'].get(':question/worked-solution','[Absent]'),'Exact raw replay:\n'+g.markdown(row['replay']),'Changed raw (evidence only):\n'+g.markdown(row['changed_raw'])])
  else:out.extend('Normal generated:\n'+g.markdown(r) for r in row['records'])
 (D/'review.md').write_text('\n\n'.join(out)+'\n')
 inv=[{'role':'authored field-completion review variant','relationship_to_source_templates':{'source_id':k,'kind':'source-family normal field completion; no independent MA evidence'},'record':g.generate(l,template=k,parameters={'a':a})} for l,k in [('easy','q-31333'),('moderate','q-31341'),('hard','q-48510')] for a in (2,3)]
 save('authored-field-completions.json',inv)
 save('independent-inventory.json',{'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'questions':[]})
 save('validation.json',{'status':'pass','source_basis':2275,'source_fidelity':counts,'original_values_independently_parsed':len(source_values),'all_parameterized_raw_bank_values_checked':raw_changed_values,'all_parameterized_raw_records_checked':117,'math':{'normal_instances':len(records),'printed_equality_rows':rows,'negative_controls':negative,'fraction_argument_cases':len(fraction_cases),'slot_coverage':coverage,'native_bound_repair':'q-310222 learner eligible a1..8; original evidence/domain diagnostics retain a9; served wrong0/+1 and reciprocal equivalents tested at upper bound8','meaningful_task_counts':{l:len(v) for l,v in tasks.items()},'fingerprint_exclusions':['raw/default aliases','seed','option order','profile banks'],'fingerprint_inclusions':['printed function','actual requested point','derivative/slope/tangent task']},'native_serving_unresolved':0,'native_contract_gates':sum(len(r['question'][':question/answer-fields']) for r in records),'raw_only_unsupported_diagnostics':2,'native_grading':{k:native[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'raw_ineligible':['all raw profiles evidence-only; unrated missing key/solution preserved','missing answer fields preserved','q-31341 f prime x evaluation label preserved','q-342412 nested csc bracket error preserved'],'database_writes':0,'registration_writes':0,'baseline':'No registered generator entity at current frozen candidate snapshot; no existing numeric script found.'})
 print(json.dumps({'pass':True,'source':counts,'math_instances':len(records),'rows':rows,'task_counts':{l:len(v) for l,v in tasks.items()},'native':{k:native[k] for k in ['accepted_checks','rejected_checks']}}))
if __name__=='__main__':main()
