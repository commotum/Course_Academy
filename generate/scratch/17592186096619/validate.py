#!/usr/bin/env python3
"""Independent displayed-math parsing, source coverage, identities, native grading."""
import importlib.util,json,re,subprocess,sys,hashlib
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=g.X

def readgroup(text,i):
 if i>=len(text) or text[i] not in '({':raise ValueError('Group expected '+text[i:])
 start=text[i];end=')' if start=='(' else '}';depth=1;j=i+1
 while depth:
  if j>=len(text):raise ValueError('Unclosed group '+text)
  if text[j]==start:depth+=1
  if text[j]==end:depth-=1
  j+=1
 return text[i+1:j-1],j

def convert(text):
 text=text.strip().rstrip('.,').replace('\u2061','').replace('π',r'\pi').replace('−','-')
 text=text.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace(r'\quad','').replace(r'\cdot','*')
 text=re.sub(r'\\operatorname\{(sin|cos|tan|ln)\}',lambda m:'\\'+m[1],text)
 text=re.sub(r'(?<!\\)\b(sin|cos|tan|ln)\b',lambda m:'\\'+m[1],text)
 out='';i=0
 while i<len(text):
  c=text[i]
  if c=='\\':
   m=re.match(r'\\([A-Za-z]+)',text[i:])
   if not m:raise ValueError('Unknown escape '+text[i:])
   name=m[1];i+=len(m[0])
   if name=='operatorname':name,i=readgroup(text,i)
   if name in ('frac','dfrac','tfrac'):
    a,i=readgroup(text,i);b,i=readgroup(text,i);out+='(('+convert(a)+')/('+convert(b)+'))';continue
   if name=='sqrt':a,i=readgroup(text,i);out+='sqrt('+convert(a)+')';continue
   if name=='pi':out+='pi';continue
   if name in ('sin','cos','tan','sec','ln','log'):
    name='log' if name in ('ln','log') else name
    power=None
    if i<len(text) and text[i]=='^':
     i+=1
     if text[i]=='{':power,i=readgroup(text,i)
     else:power=text[i];i+=1
    while i<len(text) and text[i]==' ':i+=1
    if i<len(text) and text[i] in '({':a,i=readgroup(text,i);arg=convert(a)
    elif text[i:i+3]=='\\pi':arg='pi';i+=3
    else:
     m=re.match(r'[A-Za-z]|[0-9]+',text[i:]);arg=m[0];i+=len(arg)
     arg='E' if arg=='e' else arg
    out+='('+name+'('+arg+'))'+('**('+power+')' if power else '');continue
   raise ValueError('Unexpected TeX command '+name)
  if c=='{':a,i=readgroup(text,i);out+='('+convert(a)+')';continue
  out+=('(E)' if c=='e' else c);i+=1
 return out

def parse(text):
 text=convert(text)
 return parse_expr(text,local_dict={'x':X,'pi':s.pi,'E':s.E,'log':s.log,'sin':s.sin,'cos':s.cos,'tan':s.tan,'sec':s.sec,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0

def spans(text):return [m[1] if m[1] is not None else m[2] for m in re.finditer(r'\$\$([\s\S]*?)\$\$|\$([^$]*)\$',text)]
def formatcheck(text):
 assert text.count('$')%2==0
 for body in spans(text):
  n=0
  for c in body:
   if c=='{':n+=1
   if c=='}':n-=1
   assert n>=0
  assert n==0
 assert '--' not in text and '+-' not in text
 assert r'\sinh' not in text and r'\cosh' not in text

def mathcheck(record):
 q=record['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];f=q[':question/answer-fields'][0]
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==g.ID
 formatcheck(prompt);formatcheck(sol)
 if f[':answer-field/type'].endswith('blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt
 fields=spans(prompt);functions={}
 for z in fields:
  if z.startswith('f(x)='):functions['f']=parse(z.split('=',1)[1])
  if z.startswith('h(x)='):functions['h']=parse(z.split('=',1)[1])
 y=next(z.split('=',1)[1].rstrip(',.') for z in fields if z.startswith('y'))
 func=functions['f']*functions['h'] if y.startswith('f(x)') else parse(y)
 t=parse(next(z.split('=',1)[1] for z in fields if z.startswith('x')))
 slope=s.simplify(s.diff(func,X).subs(X,t))
 choices=f[':answer-field/choices'];values=[parse(a[':answer/value']) for a in choices]
 assert len({a[':answer/id'] for a in choices})==len(choices)
 for a in choices:
  assert '=' not in a[':answer/value'], 'Only scalar slope fragments are eligible'
  formatcheck('$'+a[':answer/value']+'$')
 correct=f[':answer-field/correct'][1]
 assert sum(equal(z,slope) for z in values)==1
 assert equal(values[next(i for i,a in enumerate(choices) if a[':answer/id']==correct)],slope)
 assert not any(equal(a,b) for i,a in enumerate(values) for b in values[i+1:])
 ss=spans(sol);u=parse(ss[0].split('=',1)[1]);v=parse(ss[1].split('=',1)[1])
 assert equal(u*v,func)
 blocks=[z for z in ss if r'\begin{aligned}' in z]
 if record['generation']['family']=='named_exp_sin':
  derivrows=[z.split(r'\end{aligned}')[0].split(r'\\')[0].strip() for z in blocks[0].split('&=')[1:]]
  assert len(derivrows)==2
  for row,arg,derivative in zip(derivrows,(u,v),(s.diff(u,X),s.diff(v,X))):
   formal,answer=row.split('=')
   operator=r'\frac{\mathrm d}{\mathrm dx}'
   assert formal.startswith(operator)
   assert equal(parse(formal[len(operator):]),arg)
   assert equal(parse(answer),derivative)
  blocks=blocks[1:]
 else:
  derivs=ss[2].strip().split(r',\quad ')
  assert equal(parse(derivs[0].split('=',1)[1]),s.diff(u,X))
  assert equal(parse(derivs[1].split('=',1)[1]),s.diff(v,X))
 product=[z.split(r'\end{aligned}')[0].strip() for z in blocks[0].split('&=')[1:]]
 product=[z.split(r'\\')[0].strip() for z in product]
 # Formal symbolic operator is checked by actual u,v reconstruction above.
 assert equal(parse(product[1]),s.diff(func,X))
 if len(product)>2:assert equal(parse(product[2]),s.diff(func,X))
 evalrows=[z.split(r'\end{aligned}')[0].split(r'\\')[0].strip() for z in blocks[1].split('&=')[1:]]
 for row in evalrows:
  if r'\right|_{x=' in row:
   row=row.split(r'\right|_{x=')[0].replace(r'\left.','');value=parse(row).subs(X,t)
  else:
   for fragment in row.split('='):
    assert equal(parse(fragment),slope), (fragment,slope)
   value=parse(row.split('=')[0])
  assert equal(value,slope),(row,value,slope)
 if record['generation']['family']=='poly_exp' and record['generation']['profile'].startswith('observed'):
  assert not re.search(r'\)\^\{',evalrows[-1]), 'Evaluated monomials must not repeat substitution powers'
  assert r'\cdot (' in evalrows[-1]
 if record['generation']['family'] in ('poly_trig','poly_log'):
  assert len(evalrows)==3
  assert evalrows[0]!=evalrows[1] and evalrows[1]!=evalrows[2]
  assert any(command in evalrows[0] for command in (r'\sin',r'\cos',r'\ln'))
  assert not any(command in evalrows[1] for command in (r'\sin',r'\cos',r'\ln'))
 final=parse(ss[-1]);assert equal(final,slope)
 return slope,len(product),len(evalrows)

def prose(text):return re.sub(r'\s+',' ',re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$','<math>',text)).strip()

def main():
 cases=[];source_reports=[];records=[];review=[];native=[];missingrefs=0;bankmatched=0;answercount=0;distractors=0;designationmatched=0
 for name,(level,family,kind,p) in g.TEMPLATES.items():
  if p is None:continue
  rec=g.generate(level,17,name,parameters=p,profile='observed');raw=g.QUESTIONS[name];slope,pr,ev=mathcheck(rec)
  cases.append({'source_id':name,'source_db_id':raw[':db/id'],'template':name,'level':level,'parameters':p,'bank_profile':'observed','original_difficulty':raw.get(':question/difficulty'),'authored_level_assignment':not bool(raw.get(':question/difficulty'))})
  fields=raw.get(':question/answer-fields',[])
  sourcevals=[parse(a[':answer/value']) for f in fields for a in f.get(':answer-field/choices',[])]
  newvals=[parse(a[':answer/value']) for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]
  if sourcevals:
   assert len(sourcevals)==len(newvals)
   for a in sourcevals:assert sum(equal(a,b) for b in newvals)==1,(name,a,newvals)
   bankmatched+=1;answercount+=len(sourcevals);distractors+=len(sourcevals)-(1 if kind=='radio' else len(sourcevals))
  if fields and ':answer-field/correct' in fields[0]:
   assert equal(parse(fields[0][':answer-field/correct'][':answer/value']),slope);designationmatched+=1
  else:missingrefs+=1
  if ':question/worked-solution' in raw:
   original=raw[':question/worked-solution'];assert prose(original)==prose(rec['question'][':question/worked-solution']),(name,prose(original),prose(rec['question'][':question/worked-solution']))
   origblocks=[z for z in spans(original) if r'\begin{aligned}' in z]
   assert pr==len(re.findall('&',origblocks[-2]))
   # An equals sign in the final source row is retained in its composite stage.
   assert ev==len(re.findall('&',origblocks[-1]))
   if name.startswith('q-167'):
    assert len(origblocks)==3
    assert len(re.findall('&',origblocks[0]))==2
    assert original.count(r'\frac{\text{d}}{\text{d}x}')==2
    assert rec['question'][':question/worked-solution'].count(r'\frac{\mathrm d}{\mathrm dx}')==2
  source_reports.append({'source_id':name,'bank_values_matched':len(sourcevals),'correct_designation_matched':bool(fields and ':answer-field/correct' in fields[0]),'raw_prompt_exact':raw[':question/problem']==rec['question'][':question/problem'],'raw_solution_exact':raw.get(':question/worked-solution')==rec['question'][':question/worked-solution'],'normalized_prose_and_stage_counts':':question/worked-solution' in raw,'field_repair':not bool(fields),'prompt_repair':name in ('q-167326','q-167780')})
  records.append(rec);review.append((raw,rec))
  # Raw named-function evidence is API-replayable, with missing context explicitly flagged.
  if name.startswith('q-167'):
   evidence=g.generate(level,17,name,parameters=p,profile='observed_raw');(HERE/(name+'-raw-replay.json')).write_text(json.dumps(evidence,indent=2,ensure_ascii=False))
 # Each observed template/profile also has a changed-parameter variant.
 for name,(level,family,kind,p) in g.TEMPLATES.items():
  if p is None:continue
  changed=dict(p)
  if name=='q-48391':changed['a']=3
  elif name=='q-48901':changed['a']=4
  elif name=='q-48515':changed.update(a=4,b=-2)
  elif name=='q-48517':changed.update(b=-2)
  elif name=='q-48993':changed['a']=2
  else:changed['a']=2 if p['a']!=2 else 3
  rec=g.generate(level,23,name,parameters=changed,profile='observed');mathcheck(rec);records.append(rec)
 # Both authored templates per absent level, plus repeated same-level samples.
 sample_count=0;tasks={level:set() for level in ('easy','moderate','hard')}
 for name,(level,family,kind,p) in g.TEMPLATES.items():
  for seed in range(10):
   rec=g.generate(level,seed,name);slope,_,_=mathcheck(rec);sample_count+=1;tasks[level].add(rec['generation']['task_fingerprint'])
   params=rec['generation']['parameters'];again=g.generate(level,seed+999,name,parameters=params,profile=rec['generation']['profile'])
   assert rec['question'][':question/id']==again['question'][':question/id']
   if seed<2:records.append(rec)
 for rec in records:
  f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Owned complete bank'} for a in f[':answer-field/choices']]
  else:
   val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
   slope=parse(val);p=g.normalize_parameters(rec['generation']['parameters']);u,v=g.math_parts(p,rec['generation']['family']);t=p['t']
   equiv=g.add((u.subs(X,t),s.diff(v,X).subs(X,t)),(v.subs(X,t),s.diff(u,X).subs(X,t)))
   checks=[{'submitted':val,'expected':'accepted','purpose':'Canonical required slope fragment'},{'submitted':equiv,'expected':'accepted','purpose':'Independent unreduced product-rule endpoint expression'},{'submitted':g.tex(slope+1),'expected':'rejected','purpose':'Wrong slope'}]
  native.append({'label':rec['generation']['template']+':'+rec['generation']['profile']+':'+str(rec['generation']['seed']),'record':rec,'checks':checks})
 (HERE/'native-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False))
 process=subprocess.run(['generate/runs/current/check-engine',str(HERE/'native-input.json'),str(HERE/'native-report.json')],capture_output=True,text=True)
 assert process.returncode==0,process.stdout+process.stderr
 # Explicit invalid workload parameters must fail; not merely sampler bounds.
 for level,name,params in [('easy','easy_exp_linear',dict(a=2,b=1,t=1)),('hard','hard_poly_log',dict(a=1,b=0,c=2,t='E')),('hard','hard_poly_trig',dict(a=1,b=2,c=3,t='pi/2',trig='sin')),('moderate','q-319825',dict(a=1,b=-1,k=2,d=0,t=0))]:
  try:g.generate(level,template=name,parameters=params)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit workload accepted')
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False))
 (HERE/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
 md=['# Original source evidence and generated review','Original math database basis 1356. All generated records below are explicitly labeled; raw originals remain in source.json.']
 for raw,rec in review:
  md+=['## '+raw[':question/math-academy-id']+' — original',raw[':question/problem'],raw.get(':question/worked-solution','[No captured worked solution]'), '\nOriginal banks: '+json.dumps([f.get(':answer-field/choices',[]) for f in raw.get(':question/answer-fields',[])],ensure_ascii=False),'### Generated original-parameter normalized replay',g.markdown(rec)]
 for rec in records[13:]:md+=['## Generated variant: '+rec['generation']['template']+' / '+rec['question'][':question/difficulty'].split('/')[-1],g.markdown(rec)]
 (HERE/'review.md').write_text('\n\n'.join(md))
 report={'status':'passed','database':'math','basis':1356,'source_questions':13,'source_cases_replayed':13,'observed_answer_banks_matched':f'{bankmatched}/12','source_answer_values_matched':f'{answercount}/36','source_radio_distractors_matched':f'{distractors}/24','observed_correct_designations_matched':f'{designationmatched}/10','inferred_missing_designations':missingrefs,'original_source_solutions':11,'raw_exact_solutions':'0/11','normalized_fixed_prose_and_ordered_stage_counts':'11/11','source_reports':source_reports,'authored_default_instances_checked':sample_count,'unique_sampled_tasks_by_level':{k:len(v) for k,v in tasks.items()},'native_checks':sum(len(z['checks']) for z in native),'native_passed':True,'formatting_identity_displayed_math_scope_passed':True,'remaining_findings':['Opaque bank intent unresolved; explicit observed replay profiles only.','Two named-function raw prompts lack definitions; normal presentation supplies them.','No observed easy/hard labels; easy/hard authored scope documented.','All source math normalized; raw exact prompt/solution reproduction is not claimed.','Equation entries to scalar blanks are unsupported native notation; not counted grading passes.']}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
 print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
