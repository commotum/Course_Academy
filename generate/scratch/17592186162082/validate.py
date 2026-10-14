#!/usr/bin/env python3
"""Independent printed-expression/geometry, source-bank/prose and native grading QA."""
import concurrent.futures,hashlib,importlib.util,json,math,re,subprocess,sys,tempfile
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('piecewise',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def group(text,i):
 assert text[i]=='{';depth=1;j=i+1
 while depth:
  if text[j]=='{':depth+=1
  if text[j]=='}':depth-=1
  j+=1
 return text[i+1:j-1],j

def parse(text):
 text=text.replace('π',r'\pi').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').strip().rstrip('.')
 def convert(text):
  out='';i=0
  while i<len(text):
   if text.startswith(r'\frac',i):
    a,k=group(text,i+5);b,j=group(text,k);out+='(('+convert(a)+')/('+convert(b)+'))';i=j
   elif text.startswith(r'\sqrt',i):
    a,j=group(text,i+5);out+='sqrt('+convert(a)+')';i=j
   elif text.startswith(r'\pi',i):out+='pi';i+=3
   elif text[i]=='{':
    a,j=group(text,i);out+='('+convert(a)+')';i=j
   else:out+=text[i];i+=1
  return out
 return parse_expr(convert(text).replace('^','**'),local_dict={'pi':s.pi,'sqrt':s.sqrt,'r':s.Symbol('r')},transformations=standard_transformations+(implicit_multiplication_application,))
def normtext(text):
 text=re.sub(r'!\[\]\([^)]*\)','![](PLOT)',text)
 # Ignore presentation-only TeX spelling and whitespace; preserve prose and ordered rows.
 text=text.replace(r'\text{d}s',r'\textrm ds').replace('π',r'\pi')
 return re.sub(r'\s+','',text)
def rows(text):return re.findall(r'\$\$\s*(.*?)\s*\$\$',text,re.S)
def numeric_rows(text):
 result=[]
 for row in rows(text)[2:]:
  vals=[]
  for x in row.split('=')[1:]:
   if r'\int' not in x:vals.append(parse(x))
  result.append(vals)
 return result

def check(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 q=rec['question'];m=rec['generation'];f=q[':question/answer-fields'][0];opts=f[':answer-field/choices'];assert len(opts)==5 and f[':answer-field/type']==':answer-field.type/radio'
 for entity,key in [(q,':question/id'),(f,':answer-field/id')]+[(a,':answer/id') for a in opts]:__import__('uuid').UUID(entity[key])
 assert f[':answer-field/correct'][0]==':answer/id' and f[':answer-field/correct'][1] in [a[':answer/id'] for a in opts]
 assert all('$' not in a[':answer/value'] for a in opts)
 values=[s.simplify(parse(a[':answer/value'])) for a in opts];assert all(s.simplify(a-b)!=0 for i,a in enumerate(values) for b in values[i+1:])
 # Read actual plot sidecars, independently derive exact endpoint distances/radius.
 side=json.loads(Path(m['assets']['solution']).with_suffix('.json').read_text());curves=side['curves'];t=m['template'];p={k:s.Rational(v) for k,v in m['parameters'].items()}
 # Numeric curve coordinates independently compared to exact plotted ticks and source-family relations.
 def point(x):return [s.Rational(str(round(v,10))) for v in x]
 L=[]
 for i,c in enumerate(curves):
  if len(c)>2:
   center=side['geometry']['center'];radius=s.Rational(side['geometry']['arc'][0]);cx,cy=map(float,center)
   assert all(abs(math.hypot(x-cx,y-cy)-float(radius))<1e-7 for x,y in c)
   angles=[math.atan2(y-cy,x-cx) for x,y in c];angle=sum((b-a+math.pi)%(2*math.pi)-math.pi for a,b in zip(angles,angles[1:]));fraction={'semi':1,'three_quarter':s.Rational(3,2),'quarter_closed':s.Rational(1,2),'quarter_open':s.Rational(1,2)}[t];assert abs(angle-float(fraction*s.pi))<1e-7;L.append(radius*fraction*s.pi)
  else:
   a,b=point(c[0]),point(c[-1]); # recover rationals with denominator <=3 from plotted coordinates
   a=[s.Rational(float(x)).limit_denominator(3) for x in a];b=[s.Rational(float(x)).limit_denominator(3) for x in b];L.append(s.sqrt(sum((u-v)**2 for u,v in zip(a,b))))
 for role,path in m['assets'].items():
  from PIL import Image
  im=Image.open(path);assert im.format=='PNG' and im.size==(432,364)
  assert Path(path).with_suffix('.json').exists()
 if 'r' in p:
  printed=re.search(r'of radius \$r=([^$]+)\.\$',q[':question/worked-solution']);assert printed
  assert parse(printed.group(1))==s.Rational(side['geometry']['arc'][0])
  prompt_radius=re.search(r'of radius \$([^$]+)\$',q[':question/problem'])
  if prompt_radius:assert parse(prompt_radius.group(1))==s.Rational(side['geometry']['arc'][0])
 assert len(curves)==(3 if t=='three_segments' else 2);assert side['labels']==['C_'+str(i+1) for i in range(len(curves))]
 A=s.simplify(sum(L));assert sum(s.simplify(v-A)==0 for v in values)==1;assert parse(next(a[':answer/value'] for a in opts if a[':answer/id']==f[':answer-field/correct'][1]))==A
 numeric=numeric_rows(q[':question/worked-solution']);assert len(numeric)==3
 targets=[L[0],L[1],A] if t!='three_segments' else [L[0],L[1],A]
 for rr,target in zip(numeric,targets):
  assert rr
  for value in rr:assert s.simplify(value.subs(s.Symbol('r'),p.get('r',1))-target)==0,(rr,target)
 # Structural source-shape rows: first facts, then primitive lengths, then sum; repeated sentence preserved for quarter_open.
 assert len(rows(q[':question/worked-solution']))==5
 assert ('Calculate ${\\int }_{C}' in q[':question/worked-solution']) == (t=='quarter_open')
 assert r'f(x,y)' not in q[':question/problem']
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in opts]:
  assert text.count('$')%2==0;depth=0
  for ch in text:
   if ch=='{':depth+=1
   if ch=='}':depth-=1
   assert depth>=0
  assert depth==0
 assert 'calculator-required' not in str(q)
 return A

def main():
 normalized_cases=[{'source_id':qid,'template':t,'level':lv,'profile':qid,'parameters':p} for qid,t,lv,p in [('q-122481','semi','easy',{'r':2}),('q-122843','three_quarter','easy',{'r':2}),('q-122484','quarter_closed','moderate',{'r':2}),('q-122828','three_segments','moderate',{'a':3,'b':4}),('q-122845','two_segments','moderate',{'a':3,'b':2,'h':4}),('q-122850','quarter_open','moderate',{'r':4})]]
 raw_cases=[];raw_records=[];raw_fidelity=[]
 for case in normalized_cases:
  source=g.SOURCE_Q[case['source_id']];observed=source.get(':question/difficulty',{}).get(':db/ident');level=observed.rsplit('/',1)[-1] if observed else case['level']
  raw_case=case|{'level':level,'profile':'raw-'+case['source_id'],'observed_attribute_presence':{'difficulty':observed is not None,'correct_ref':':answer-field/correct' in source[':question/answer-fields'][0],'worked_solution':':question/worked-solution' in source}}
  raw_cases.append(raw_case);rec=g.generate(level,template=case['template'],profile=raw_case['profile'],parameters=case['parameters']);question=rec['question'];field=question[':question/answer-fields'][0];original_field=source[':question/answer-fields'][0]
  assert rec['generation']['evidence_only'] and not rec['generation']['eligible_for_normal_generation']
  assert question[':question/problem']==source[':question/problem']
  assert question.get(':question/worked-solution')==source.get(':question/worked-solution')
  assert (':question/difficulty' in question)==(':question/difficulty' in source)
  assert question.get(':question/difficulty')==observed
  assert (':question/worked-solution' in question)==(':question/worked-solution' in source)
  assert (':answer-field/correct' in field)==(':answer-field/correct' in original_field)
  assert field[':answer-field/type']==original_field[':answer-field/type'][':db/ident']
  assert field[':answer-field/key']==original_field[':answer-field/key']
  assert [a[':answer/value'] for a in field[':answer-field/choices']]==[a[':answer/value'] for a in original_field[':answer-field/choices']]
  assert [a[':answer/id'] for a in field[':answer-field/choices']]==[a[':answer/id'] for a in original_field[':answer-field/choices']]
  if ':answer-field/correct' in original_field:assert field[':answer-field/correct']==[':answer/id',original_field[':answer-field/correct'][':answer/id']]
  raw_records.append({'label':'raw-source/'+case['source_id'],'record':rec})
  changed={k:str(s.Rational(v)*2) for k,v in case['parameters'].items()};variant=g.generate(level,template=case['template'],profile=raw_case['profile'],parameters=changed)
  assert variant['generation']['preserved_attribute_presence']==rec['generation']['preserved_attribute_presence']
  if ':question/worked-solution' in question:check(variant)
  else:
   # Independent geometry/stage validation uses an explicitly authored completion;
   # raw evidence remains untouched with no key/rating/solution inserted.
   completed=g.generate('moderate',template=case['template'],parameters=changed);A=check(completed)
   assert variant['generation']['assets']['prompt']==completed['generation']['assets']['prompt']
   vv=[parse(a[':answer/value']) for a in variant['question'][':question/answer-fields'][0][':answer-field/choices']]
   assert sum(s.simplify(z-A)==0 for z in vv)==1 and all(s.simplify(a-b)!=0 for i,a in enumerate(vv) for b in vv[i+1:])
  raw_records.append({'label':'raw-variant/'+case['source_id'],'record':variant})
  raw_fidelity.append({'source_id':case['source_id'],'exact_prompt':True,'exact_solution_if_present':':question/worked-solution' in source,'exact_choice_strings':5,'attribute_presence_preserved':True,'original_asset_references_preserved':True,'correct_ref_present':':answer-field/correct' in original_field,'difficulty_present':observed is not None})
 (ROOT/'source-cases.json').write_text(json.dumps(raw_cases,indent=2)+'\n');(ROOT/'normalized-source-cases.json').write_text(json.dumps(normalized_cases,indent=2)+'\n');(ROOT/'raw-source-records.json').write_text(json.dumps(raw_records,indent=2)+'\n')
 records=[];fidelity=[]
 for case in normalized_cases:
  rec=g.generate(case['level'],parameters=case['parameters'],template=case['template'],profile=case['profile']);check(rec);source=g.SOURCE_Q[case['source_id']];opts=source[':question/answer-fields'][0][':answer-field/choices'];actual=rec['question'][':question/answer-fields'][0][':answer-field/choices']
  for a in opts:assert sum(s.simplify(parse(a[':answer/value'])-parse(b[':answer/value']))==0 for b in actual)==1
  assert normtext(source[':question/problem'])==normtext(rec['question'][':question/problem'])
  sourcekey=source[':question/answer-fields'][0].get(':answer-field/correct');keymatched=False
  if sourcekey:
   keymatched=s.simplify(parse(sourcekey[':answer/value'])-check(rec))==0;assert keymatched
  solution=source.get(':question/worked-solution');solmatch=None;prosematch=None
  if solution:
   # Entire nonmath prose, not a few fixed phrases, plus every math row and sequence.
   def proseonly(x):return re.sub(r'\$.*?\$','MATH',re.sub(r'\$\$.*?\$\$','MATH',re.sub(r'!\[\]\([^)]*\)','PLOT',x),flags=re.S),flags=re.S)
   prosematch=normtext(solution)==normtext(rec['question'][':question/worked-solution']);assert prosematch,(case['source_id'],proseonly(solution),proseonly(rec['question'][':question/worked-solution']))
   before=numeric_rows(solution);after=numeric_rows(rec['question'][':question/worked-solution']);assert len(before)==len(after)
   solmatch=all(len(a)==len(b) and all(s.simplify(x-y)==0 for x,y in zip(a,b)) for a,b in zip(before,after));assert solmatch,(before,after)
  fidelity.append({'source_id':case['source_id'],'options_matched':5,'total':5,'correct_designation_matched':keymatched,'missing_key':sourcekey is None,'full_solution_prose_matched':prosematch,'ordered_numeric_stages_matched':solmatch,'raw_exact_solution':solution==rec['question'][':question/worked-solution'] if solution else None});records.append(('source/'+case['source_id'],rec))
  # All empirical banks exercised at changed dimensions, preserving profile formulas.
  changed={k:s.Rational(v)*2 for k,v in case['parameters'].items()};changed={k:str(v) for k,v in changed.items()}
  variant=g.generate(case['level'],seed=44,template=case['template'],profile=case['profile'],parameters=changed);check(variant);records.append(('empirical-variant/'+case['source_id'],variant))
 generated=[]
 for level in ('easy','moderate','hard'):
  for t in (['quarter_open','three_segments'] if level=='hard' else [k for k,v in g.TEMPLATES.items() if v[0]==level]):
   for seed in range(8):
    r=g.generate(level,seed=seed,template=t);check(r);assert r==g.generate(level,seed=seed,template=t);generated.append((level+'/'+t+'/'+str(seed),r))
   same=g.generate(level,99,template=t,parameters=r['generation']['parameters']);assert same['question'][':question/id']==r['question'][':question/id']
 records+=generated
 # Deliberate printed-stage corruption must fail even with untouched metadata/key.
 import copy
 corrupted=copy.deepcopy(records[0][1]);corrupted['question'][':question/worked-solution']=corrupted['question'][':question/worked-solution'].replace('=2\\pi+4','=2\\pi+5')
 # Whitespace in SymPy TeX is presentation-specific, so alter the exact printed segment row.
 corrupted=copy.deepcopy(records[0][1]);corrupted['question'][':question/worked-solution']=corrupted['question'][':question/worked-solution'].replace(g.I(2)+'=4.',g.I(2)+'=5.')
 try:check(corrupted)
 except AssertionError:pass
 else:raise AssertionError('Printed stage corruption escaped independent check')
 # Exhaust every finite authored hard radius through the public generator.
 hard_radii=sorted({s.Rational(k,d) for d in (2,3) for k in range(1,12*d+1) if k%d})
 assert len(hard_radii)==36 and all(0<r<=12 for r in hard_radii)
 for radius in hard_radii:check(g.generate('hard',template='quarter_open',parameters={'r':str(radius)}))
 for seed in range(18):
  for level in ('easy','moderate','hard'):check(g.generate(level,seed=seed))
 try:g.generate('easy',profile='raw-q-122481',parameters={})
 except ValueError:pass
 else:raise AssertionError('Empty explicit raw parameters silently replaced by anchors')
 # Explicit guard checks rather than letting shared broad bounds bypass workload policies.
 for level,t,p in [('easy','semi',{'r':'1/2'}),('hard','quarter_open',{'r':2}),('moderate','three_segments',{'a':3,'b':5}),('hard','semi',{'r':'3/2'}),('moderate','two_segments',{'a':2,'b':3,'h':4})]:
  try:g.generate(level,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit parameters accepted')
 # Fresh concurrent renders, identical and different parameters; private temporary roots.
 with tempfile.TemporaryDirectory(prefix='concurrent-',dir=ROOT) as temp:
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
   results=list(pool.map(lambda r:g.render_plots('quarter_open',{'r':s.Rational(r)},temp),['5/2','7/3','5/2','11/3']))
  assert results[0]==results[2]
  for val,assets in zip(['5/2','7/3','5/2','11/3'],results):
   for name in assets.values():assert json.loads(Path(name).with_suffix('.json').read_text())['parameters']['r']==val
  assert not list(Path(temp).glob('render-*'))
 engine=[]
 gradeable_raw=[(x['label'],x['record']) for x in raw_records if ':answer-field/correct' in x['record']['question'][':question/answer-fields'][0]]
 for label,r in records+gradeable_raw:
  f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
  checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Every owned radio option'} for a in f[':answer-field/choices']];engine.append({'label':label,'record':r,'checks':checks})
 (ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2));subprocess.run([str(g.SOURCE.parents[2]/'check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 review=[{'label':label,'record':rec} for label,rec in records[:12]]
 for level in ('easy','moderate','hard'):review += [{'label':label,'record':r} for label,r in generated if label.startswith(level+'/')][:2]
 # Include every authored family as well as two per level.
 for t in g.TEMPLATES:review += [{'label':label,'record':r} for label,r in generated if '/'+t+'/' in label][:1]
 (ROOT/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 report={'status':'worker-validated; parent independent QA pending','basis':2275,'source_banks':6,'source_choices_matched':30,'source_choices_total':30,'source_wrong_options_matched':24,'source_wrong_options_total':24,'observed_wrong_designations_matched':20,'inferred_missing_key_wrong_choices':4,'observed_correct_designations_matched':5,'observed_correct_designations_total':5,'inferred_missing_designations':1,'full_available_solutions_prose_and_numeric_sequence_matched':5,'available_solutions_total':5,'raw_exact_solution_strings':5,'raw_source_contract':{'exact_prompts':6,'exact_banks':6,'exact_choice_strings':30,'exact_available_solutions':5,'preserved_attribute_presence_cases':6,'missing_key_solution_rating_cases':1,'records':raw_fidelity},'normalized_reconstruction_exact_solution_strings':sum(x['raw_exact_solution'] is True for x in fidelity),'presentation_normalized_solutions':5,'record_checks':len(records),'raw_gradeable_record_checks':len(gradeable_raw),'raw_ungradeable_source_contracts':1,'source_fidelity':fidelity,'native_engine':json.loads((ROOT/'engine-report.json').read_text()),'fresh_concurrency_calls':4,'all_allowed_hard_radii_tested':36,'normal_seed_sweep_each_level':18,'database_writes':0,'calculator_requirements':'unknown: absent in all six sources','unresolved':['q122484 difficulty, correct designation and solution absent: authored moderate, derived key and source-shaped solution','No observed hard questions; bounded rational hard policy is authored','Several empirical distractor intentions underidentified; never normal defaults','Matplotlib style differs from source asset, geometry and instructional cues preserved'],'versions':{'python':sys.version,'sympy':s.__version__,'matplotlib':__import__('matplotlib').__version__}}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');subprocess.run([sys.executable,str(ROOT/'finalize-evidence.py')],check=True);print(json.dumps({k:v for k,v in report.items() if k not in ('native_engine','source_fidelity')},indent=2))
if __name__=='__main__':main()
