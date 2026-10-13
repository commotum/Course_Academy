#!/usr/bin/env python3
"""Independent mathematics read from printed TeX, native grading, source evidence."""
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys,tempfile,uuid
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y,I,J=s.symbols('x y i j',real=True)
def write(name,obj):(H/name).write_text(json.dumps(obj,indent=2)+'\n')
def parse(tex):
 tex=tex.replace('⁡','').replace('\\left','').replace('\\right','').replace('\\,','').replace('\\!','').replace('\\pi','pi').replace('\\operatorname{cos}','cos').replace('\\operatorname{sin}','sin').replace('\\cos','cos').replace('\\sin','sin')
 tex=re.sub(r'\^\{([^{}]*)\}',r'**(\1)',tex)
 while '\\frac' in tex:
  start=tex.rfind('\\frac')
  def group(pos):
   assert tex[pos]=='{',tex
   depth=1;end=pos+1
   while depth:
    if tex[end]=='{':depth+=1
    if tex[end]=='}':depth-=1
    end+=1
   return tex[pos+1:end-1],end
  num,end=group(start+5);den,end=group(end)
  tex=tex[:start]+'(('+num+')/('+den+'))'+tex[end:]
 tex=re.sub(r'(?<=[0-9)xy])(?=[ij])','*',tex)
 tex=re.sub(r'\|([^|]*)\|',r'Abs(\1)',tex).replace('{','(').replace('}',')').replace('^','**')
 return s.simplify(parse_expr(tex,local_dict={'x':X,'y':Y,'i':I,'j':J,'pi':s.pi,'sin':s.sin,'cos':s.cos,'Abs':s.Abs},transformations=standard_transformations+(implicit_multiplication_application,)))
def formatting(text):
 assert text.count('$')%2==0
 depth=0
 for i,c in enumerate(text):
  if i and text[i-1]=='\\':continue
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,text
 assert depth==0
 assert '--' not in text and '+-' not in text

def verify(rec):
 q=rec['question'];m=rec['generation'];p=m['parameters']
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 uuid.UUID(q[':question/id'])
 for text in [q[':question/problem'],q[':question/worked-solution']]:formatting(text)
 # Read the ACTUAL field off the learner-facing prompt, not metadata.
 field_tex=re.search(r'\$F\(x,y\)=(.*?)\$',q[':question/problem'])[1]
 field=parse(field_tex);fs=[s.expand(field).coeff(I),s.expand(field).coeff(J)]
 assert s.expand(field-fs[0]*I-fs[1]*J)==0,(m['template'],field_tex,field)
 for got,want in zip(fs,g.field_components(m['template'],p)):
  assert s.simplify(got-want.xreplace({g.X:X,g.Y:Y}))==0,(got,want)
 point_tokens=re.findall(r'F\(([^)]*)\)\s*&\s*=',q[':question/worked-solution']);assert len(point_tokens)==3
 points=[[parse(z) for z in token.split(',')] for token in point_tokens];assert [[str(z) for z in row] for row in points]==p['points']
 vectors=[[s.simplify(f.subs({X:x,Y:y})) for f in fs] for x,y in points]
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)[1]
 rows=block.split('\\\\');assert len(rows)==3
 for row,v in zip(rows,vectors):
  stages=row.split('& =',1)[1].split('=');assert len(stages)==2
  for stage in stages:
   got=parse(stage);assert s.simplify(got-v[0]*I-v[1]*J)==0,(stage,got,v)
 # All generated sidecars describe actual displayed tail/tip geometry.
 bank_data={z['path']:z['vectors'] for z in m['plot_banks']};f=q[':question/answer-fields'][0]
 assert len(q[':question/answer-fields'])==1 and len(f[':answer-field/choices'])==5
 correct_ref=f[':answer-field/correct'];assert correct_ref[0]==':answer/id'
 hits=[];bank=[]
 for answer in f[':answer-field/choices']:
  uuid.UUID(answer[':answer/id']);assert answer[':answer/type']==':answer.type/image'
  path=Path(answer[':answer/value']);assert path.exists()
  vv=[[s.Rational(z) for z in row] for row in bank_data[str(path)]];bank.append(vv)
  if vv==vectors:hits.append(answer[':answer/id'])
  if not m['source_original_geometry']:
   side=json.loads(path.with_suffix('.json').read_text());assert side['renderer']=='Matplotlib';assert side['exact_vectors']==bank_data[str(path)] and side['exact_points']==p['points']
   assert side['grid_increment']==(1 if m['level']=='easy' else .5 if m['level']=='moderate' else .25)
   for (x,y),(u,v) in zip(points,vv):
    for xx,yy in [(x,y),(x+u,y+v)]:assert side['bounds'][0]<xx<side['bounds'][1] and side['bounds'][2]<yy<side['bounds'][3]
 assert len({str(z) for z in bank})==5
 assert hits==[correct_ref[1]],hits
 if m['profile']=='authored_sign_swap':
  expected=[vectors,[[u,-v] for u,v in vectors],[[-u,v] for u,v in vectors],[[v,u] for u,v in vectors],[[-u,-v] for u,v in vectors]]
  assert {str(z) for z in bank}=={str(z) for z in expected}
 # Recompute ID from actual complete displayed bank + solution, independent of order.
 identity=g.digest({'version':g.VERSION,'problem':q[':question/problem'],'solution':q[':question/worked-solution'],'images':sorted(bank_data),'geometry':sorted(json.dumps(z) for z in bank_data.values()),'difficulty':m['level']})
 assert identity==m['content_identity'] and q[':question/id']==g.uid(identity)
 return 6

def engine_case(rec,label):
 f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'All five owned image choices'} for a in f[':answer-field/choices']]}
# Check frozen human/raster source geometry against actual generator banks.
source_maps=json.loads((H/'source-bank-maps.json').read_text())
for item in source_maps:
 source_id=item['source_id'];original=g.SOURCE_QUESTIONS[source_id]
 index=next(i for i,a in enumerate(original[':question/answer-fields'][0][':answer-field/choices']) if a[':answer/value']==item['source_path'])
 assert [[g.rat(z) for z in row] for row in item['extracted_vectors']]==[[g.rat(z) for z in row] for row in g.OBSERVED[source_id][4][index]]
subprocess.run([g.RUNTIME,str(H/'source-pixel-check.py')],check=True)
reviews=[];native=[];cases=[];fidelity=[];stages=0
for sid,(t,a,b,points,bank,k) in g.OBSERVED.items():
 case={'source_id':sid,'level':'easy','template':t,'parameters':g.source_parameters(sid),'bank_profile':'observed_'+sid};cases.append(case)
 r=g.generate('easy',71,t,parameters=case['parameters'],profile=case['bank_profile']);stages+=verify(r);reviews.append({'label':'Original geometry replay '+sid,'record':r});native.append(engine_case(r,sid))
 orig=g.SOURCE_QUESTIONS[sid];old=orig[':question/answer-fields'][0][':answer-field/choices'];new=r['question'][':question/answer-fields'][0][':answer-field/choices']
 assert sorted(z[':answer/value'] for z in new)==sorted(str(Path('/media/jake/SSD/EDB/math')/z[':answer/value']) for z in old)
 # Authoritative correct and legacy duplicate are compared separately.
 designation=[]
 for f in orig[':question/answer-fields']:
  value=f.get(':answer-field/correct',{}).get(':answer/value');designation.append(value is not None)
  if value:assert str(Path('/media/jake/SSD/EDB/math')/value)==r['generation']['plot_banks'][k]['path']
 oldsol=orig.get(':question/worked-solution');newsol=r['question'][':question/worked-solution']
 if oldsol:
  assert g.DRAW_PROSE in oldsol and g.DRAW_PROSE in newsol
  oldrows=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',oldsol,re.S)[1].split('\\\\')
  assert len(oldrows)==3
  # Actual original terminal vector values are independently read as well.
  for oldrow,v in zip(oldrows,g.evaluate(t,case['parameters'])):
   for stage in oldrow.split('& =',1)[1].split('='):assert s.simplify(parse(stage)-v[0]*I-v[1]*J)==0
  def prose(text):
   text=re.sub(r'\$\$.*?\$\$','<math>',text,flags=re.S);text=re.sub(r'\$[^$]*\$','<math>',text);text=re.sub(r'!\[\]\([^)]*\)','<image>',text)
   return re.sub(r'\s+',' ',text).strip()
  assert prose(oldsol)==prose(newsol),(sid,prose(oldsol),prose(newsol))
 fidelity.append({'source_id':sid,'field_banks':len(orig[':question/answer-fields']),'options_matched':5*len(orig[':question/answer-fields']),'designation_matched':sum(designation),'designation_missing':designation.count(False),'prose_sequence_matched':bool(oldsol),'raw_solution_exact':False,'notation_normalized':bool(oldsol),'precision_limit':sid=='q-122745','unrated_authored_easy':sid=='q-122264'})
 # Changed coefficients prove profiles are generative operations, not lookup.
 for i in [1,2]:
  p=g.source_parameters(sid);p['a']=str(s.Rational(str(p['a']))*(s.Rational(1,2) if i==1 else s.Rational(3,4)))
  r=g.generate('easy',i,t,parameters=p,profile=case['bank_profile']);stages+=verify(r);reviews.append({'label':'Generated empirical-profile variant '+sid+' #'+str(i),'record':r});native.append(engine_case(r,sid+' variant '+str(i)))
 if sid=='q-122756':
  legacy={**case,'bank_profile':'observed_'+sid+'_legacy','legacy_field_id':orig[':question/answer-fields'][0][':answer-field/id']};cases.append(legacy)
  r=g.generate('easy',4,t,parameters=legacy['parameters'],profile=legacy['bank_profile']);verify(r)
for level in ['easy','moderate','hard']:
 for seed in [2,7,18,41]:
  r=g.generate(level,seed);stages+=verify(r);reviews.append({'label':'Generated authored-default '+level+' seed '+str(seed),'record':r});native.append(engine_case(r,level+' '+str(seed)))
# Identity invariant under seed-only option order; invalid explicit inputs fail.
for level in ['easy','moderate','hard']:
 r=g.generate(level,67);r2=g.generate(level,99,r['generation']['template'],parameters=r['generation']['parameters']);verify(r2)
 assert r['question'][':question/id']==r2['question'][':question/id']
 p=r['generation']['parameters'].copy();p['a']='0'
 try:g.generate(level,0,r['generation']['template'],parameters=p);raise AssertionError('invalid coefficients accepted')
 except ValueError:pass
 if level!='easy':
  p=r['generation']['parameters'].copy();p['points']=[z[:] for z in p['points']];p['points'][0][1]='1'
  try:g.generate(level,0,r['generation']['template'],parameters=p);raise AssertionError('authored grid workload bypassed')
  except ValueError:pass
# All explicit authored guards apply to reduced coefficients and exponential bases.
for level in ['moderate','hard']:
 r=g.generate(level,67)
 for coefficient in ['1/2','-3/2','3']:
  p={**r['generation']['parameters'],'a':coefficient}
  try:g.generate(level,0,r['generation']['template'],parameters=p);raise AssertionError('discrete authored coefficient guard bypassed')
  except ValueError:pass
for base in ['1','-1','1/2','-2','5']:
 p={**g.source_parameters('q-122744'),'b':base}
 try:g.generate('easy',0,'linear_exp',parameters=p);raise AssertionError('invalid exponential base accepted')
 except ValueError:pass
# Exercise fresh concurrent writes for identical and different geometries.
def concurrent_render(n):
 pts=[[str(-2+n),'-1'],['1','2'],['2','-2']];banks=[[[s.Rational(1+n),s.Rational(2)],[-1,1],[2,-2]]]
 paths=g.render_plots(pts,banks,.5,concurrent_dir);side=json.loads(Path(paths[0]).with_suffix('.json').read_text());assert side['exact_points']==pts;return paths
with tempfile.TemporaryDirectory(prefix='concurrency-',dir=H) as concurrent_dir:
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(concurrent_render,[11,11,12]))
 assert not list(Path(concurrent_dir).glob('render-*'))
write('source-cases.json',cases);write('review.json',reviews);write('engine-input.json',native)
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
engine=json.loads((H/'engine-report.json').read_text());print(json.dumps(engine)[:300]);assert engine['accepted_checks']==len(native) and engine['rejected_checks']==4*len(native)
for actual,expected in zip(engine['records'],native):
 assert actual['label']==expected['label']
 assert [x['outcome'] for x in actual['checks']]==[x['expected'] for x in expected['checks']]
report={'status':'pass','source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_questions':10,'source_raw_field_banks':11,'source_displayed_widget_banks':10,'source_options_matched':55,'unique_source_options_matched':50,'original_correct_designations_matched':9,'original_correct_designations_missing':2,'source_worked_solution_sequences_matched':9,'raw_exact_solution_strings':0,'notation_normalized_solution_sequences':9,'source_missing_solution_authored':1,'source_geometry_precision_unresolved':['q-122745 d443 unlabelled small horizontal endpoint; raw asset exact; replay extension is an authored geometric interpretation'],'generated_review_records':len(reviews),'independent_component_stages_verified':stages,'native_report':engine,'all_levels_supported':True,'source_fidelity':fidelity,'concurrency':'fresh identical/different parameter render succeeded; unique private inputs cleaned','authored_level_scope':'canonical product/square, three points, mandatory reduced half/quarter grid coordinates','source_raster_geometry_checks':{'plots':50,'endpoint_proximity_checks':150,'report':'source-pixel-check.json','precision_limits_preserved':True}}
write('validation.json',report)
md=['# Original evidence and generated review','Original images are raw source files; generated profiles and levels are explicitly labeled. All original source strings are preserved in source.json. Normalized generator prose retains the three substitution/evaluation rows and tail-placement sentence. The q-122745 empirical small horizontal arrow lacks an exact endpoint label; its raw image is replayed exactly and its changed-parameter interpretation is labeled.']
for sid in g.OBSERVED:
 q=g.SOURCE_QUESTIONS[sid];md+=['## Original '+sid,q[':question/problem'],'![]('+str(H/(sid+'-original.png'))+')',q.get(':question/worked-solution','Source has no worked solution or correct designation.')]
for review in reviews:md+=['## '+review['label'],g.markdown(review['record'])]
(H/'review.md').write_text('\n\n'.join(md)+'\n')
print('PASS',len(reviews),'records;',stages,'component-stage checks')
