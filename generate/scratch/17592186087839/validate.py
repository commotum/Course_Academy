"""Independent printed-TeX, raster, source fidelity and native engine checks."""
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
from PIL import Image
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('wide',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
X,Y,A,B=s.symbols('x y a b')
def group(text,i):
 assert text[i]=='{';depth=1;j=i+1
 while depth:
  depth+=(text[j]=='{')-(text[j]=='}');j+=1
 return text[i+1:j-1],j

def translate(text):
 out='';i=0
 while i<len(text):
  if text.startswith('\\frac',i):
   n,j=group(text,i+5);d,i=group(text,j);out+='(('+translate(n)+')/('+translate(d)+'))'
  else:out+=text[i];i+=1
 return out.replace('{','(').replace('}',')').replace('^','**')
def parse(text):
 text=text.strip().rstrip('.');assert '\\' not in translate(text),text
 return parse_expr(translate(text),local_dict={'x':X,'y':Y,'a':A,'b':B},transformations=standard_transformations+(implicit_multiplication_application,rationalize,),evaluate=True)
def lhs(text):
 parts=text.split('=');assert len(parts)<=2
 if len(parts)==2:assert parse(parts[1])==1
 return parse(parts[0])
def formatting(text):
 assert text.count('$')%2==0
 depth=0
 for c in text:
  depth+=(c=='{')-(c=='}');assert depth>=0
 assert depth==0
 assert not any(z in text for z in ('+-','--','\\\\frac'))

def blue_bounds(path):
 im=Image.open(path).convert('RGBA');white=Image.new('RGBA',im.size,'white');white.alpha_composite(im);im=white.convert('RGB');points=[(x,y) for y in range(im.height) for x in range(im.width) if (lambda c:c[2]>c[0]*1.2 and c[2]>c[1]*1.03 and c[0]<130)(im.getpixel((x,y)))]
 assert points,path
 return [min(x for x,y in points),max(x for x,y in points),min(y for x,y in points),max(y for x,y in points)]
def read_record(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];f=q[':question/answer-fields'][0]
 for text in [q[':question/problem'],q[':question/worked-solution'],*[a[':answer/value'] for a in f[':answer-field/choices']]]:formatting(text)
 if f[':answer-field/type'].endswith('blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 sol=q[':question/worked-solution'];a=parse(re.search(r'\$a=(.*?)\$',sol).group(1));b=parse(re.search(r'\$b=(.*?)\$',sol).group(1))
 assert a>b>0
 expected=X**2/a**2+Y**2/b**2
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S).group(1)
 rows=block.split(r' \\ ')
 for row in rows:assert s.simplify(lhs(row.replace('&','')).subs({A:a,B:b})-expected)==0,row
 style=g.SPECS[r['generation']['template']][2];assert len(rows)=={'integer':3,'fraction':4,'decimal_x':6,'decimal_y':6}[style]
 # Structural operation stages remain unsimplified where intended.
 assert '^{2}' in rows[1] and ('\\frac' in rows[2] if style!='integer' else True)
 values=[lhs(c[':answer/value']) for c in f[':answer-field/choices']]
 assert len(set(map(s.srepr,values)))==len(values)
 correct=[i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==f[':answer-field/correct'][1]];assert len(correct)==1
 assert s.expand(values[correct[0]]-expected)==0
 assert sum(s.expand(v-expected)==0 for v in values)==1
 for id_ in [q[':question/id'],f[':answer-field/id'],*[a[':answer/id'] for a in f[':answer-field/choices']]]:g.uuid.UUID(id_)
 ref=re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1)
 if not ref.startswith('images/'):
  path=Path(ref);side=json.loads(path.with_suffix('.json').read_text());assert side['equal_aspect']
  bounds=blue_bounds(path);size=Image.open(path).size;scale=min(.92*size[0]/(side['bounds'][1]-side['bounds'][0]),.90*size[1]/(side['bounds'][3]-side['bounds'][2]));assert abs((bounds[1]-bounds[0])-2*float(a)*scale)<4 and abs((bounds[3]-bounds[2])-2*float(b)*scale)<4,(bounds,a,b)
  assert list(map(s.Rational,(side['a'],side['b'])))==[a,b]
 return a,b

cases=[];originals=[];source_rows=[];source_plots=[];banks=distractors=answers=0
for q in g.QS:
 qid=q[':question/math-academy-id'];t,bank=g.source_spec(q);level=g.SPECS[t][0];a,b=g.PARAMS[qid]
 case={'source_id':qid,'question_id':q[':question/id'],'template':t,'parameters':{'a':a,'b':b},'bank_profile':'source:'+qid,'level':level};cases.append(case)
 r=g.generate(level,template=t,parameters=case['parameters'],profile=case['bank_profile']);originals.append(r);read_record(r)
 actual=r['question'];assert actual[':question/problem']==q[':question/problem'];assert actual[':question/worked-solution']==q[':question/worked-solution']
 for attr in (':question/difficulty',':question/answer-fields',':question/worked-solution'):assert (attr in actual)==(attr in q)
 f=q[':question/answer-fields'][0];h=actual[':question/answer-fields'][0]
 assert f[':answer-field/key']==h[':answer-field/key'];assert f[':answer-field/type'][':db/ident']==h[':answer-field/type']
 av=sorted(c[':answer/value'] for c in f[':answer-field/choices']);bv=sorted(c[':answer/value'] for c in h[':answer-field/choices']);assert av==bv,(qid,av,bv)
 designated=next(c[':answer/value'] for c in h[':answer-field/choices'] if c[':answer/id']==h[':answer-field/correct'][1]);assert designated==f[':answer-field/correct'][':answer/value']
 answers+=len(av);banks+=int(len(av)>1);distractors+=max(0,len(av)-1)
 path=Path('/media/jake/SSD/EDB/math')/r['generation']['plot_assets']['prompt'];bb=blue_bounds(path);sx=(bb[1]-bb[0])/(2*float(s.Rational(a)));sy=(bb[3]-bb[2])/(2*float(s.Rational(b)))
 source_plots.append({'source_id':qid,'asset':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'dimensions':Image.open(path).size,'blue_bounds_pixels':bb,'intercepts':[a,b],'pixels_per_x_unit':sx,'pixels_per_y_unit':sy,'note':'All four numeric ticks read visually at original resolution; source scales may differ.'})
 source_rows.append({'source_id':qid,'template':t,'bank':bank,'options':[{'value':c[':answer/value'],'coefficients':[str(lhs(c[':answer/value']).coeff(X,2)),str(lhs(c[':answer/value']).coeff(Y,2))],'correct':c[':answer/id']==f[':answer-field/correct'][':answer/id']} for c in f[':answer-field/choices']]})
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'option-map.json').write_text(json.dumps(source_rows,indent=2)+'\n');(HERE/'source-plot-audit.json').write_text(json.dumps(source_plots,indent=2)+'\n')
# Every finite meaningful radius pair, all styles and eligible banks: parse the actual printed formulas.
enumeration={};enumerated=0;level_tasks={l:set() for l in ('easy','moderate','hard')};default_tasks={l:set() for l in ('easy','moderate','hard')}
for template,(level,kind,style) in g.SPECS.items():
 profiles=([None] if kind=='blank' else {'integer_radio':['method','radii','double_radii','opaque_integer'],'decimal_x_radio':['method','opaque_decimal'],'decimal_y_radio':['method','reciprocal'],'quarter_radio':['method']}[template]);valid_pairs=set();counts={}
 for profile in profiles:
  count=0
  for a,b in g.domain(level,template):
   coefficients=g.recipes(a,b,profile) if profile else [(1/a**2,1/b**2)]
   if len(set(coefficients))!=len(coefficients) or any(x.is_finite is not True or y.is_finite is not True or x.is_real is not True or y.is_real is not True or x<=0 or y<=0 for x,y in coefficients):continue
   vals=g.bank_values(a,b,profile,kind);parsed=[lhs(v) for v in vals];assert len(set(map(s.srepr,parsed)))==len(vals)
   expected=X**2/a**2+Y**2/b**2;assert sum(s.expand(v-expected)==0 for v in parsed)==1
   sol=g.solution(a,b,style);block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S).group(1)
   for row in block.split(r' \\ '):assert s.expand(lhs(row.replace('&','')).subs({A:a,B:b})-expected)==0
   formatting(sol);valid_pairs.add((a,b));level_tasks[level].add((a,b));
   if profile in (None,'method'):default_tasks[level].add((a,b))
   count+=1;enumerated+=1
  counts[str(profile)]=count
 enumeration[template]={'meaningful_tasks_union_of_profiles':len(valid_pairs),'valid_complete_bank_instances_by_profile':counts}
# Two variants per template, and two per each observed complete bank. No literals are replayed here.
generated=[]
for template,(level,kind,style) in g.SPECS.items():
 seen=set()
 for seed in (17,29):
  while True:
   r=g.generate(level,seed,template)
   if r['generation']['parameter_fingerprint'] not in seen:break
   seed+=1
  seen.add(r['generation']['parameter_fingerprint']);generated.append(r)
for profile,template in [('radii','integer_radio'),('double_radii','integer_radio'),('opaque_integer','integer_radio'),('opaque_decimal','decimal_x_radio'),('reciprocal','decimal_y_radio')]:
 for seed in (41,43):generated.append(g.generate(g.SPECS[template][0],seed,template,profile=profile))
for r in generated:read_record(r)
# Fixed mathematical data has fixed identity across seeds; order varies.
for r in generated:
 gr=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 z=g.generate(level,817,gr['template'],parameters=gr['parameters'],profile=gr['bank_profile']);assert z['question'][':question/id']==r['question'][':question/id'];assert z['generation']['parameter_fingerprint']==gr['parameter_fingerprint']
# Invalid explicit workload and template inputs must fail, without silent resampling.
for level,template,p in [('easy','integer_radio',{'a':'3/2','b':'1'}),('moderate','fraction_blank',{'a':'4','b':'2'}),('hard','quarter_blank',{'a':'7/2','b':'3/2'}),('hard','quarter_radio',{'a':'25/4','b':'3/4'}),('easy','integer_radio',{'a':'2','b':'3'})]:
 try:g.generate(level,template=template,parameters=p)
 except ValueError:pass
 else:raise AssertionError('Workload guard did not reject')
# Fresh private concurrent renders use unique inputs; test same and different tasks.
nonce='concurrency-test-v1';paths=[]
for i,(a,b) in enumerate([('19/4','11/4'),('19/4','11/4'),('21/4','13/4')]):
 out=HERE/'plots'/f'{nonce}-{i}.png';paths.append(out)
 payload={'data':{'a':a,'b':b,'version':nonce},'output':str(out)};inp=HERE/'plots'/f'{nonce}-input-{i}.json';inp.write_text(json.dumps(payload));paths[-1]=(out,inp)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 fs=[pool.submit(subprocess.run,[sys.executable,str(HERE/'render.py'),str(inp)],check=True,capture_output=True) for out,inp in paths]
 for f in fs:f.result()
for out,inp in paths:
 bb=blue_bounds(out);side=json.loads(out.with_suffix('.json').read_text());a,b=map(s.Rational,(side['a'],side['b']));assert abs((bb[1]-bb[0])/(bb[3]-bb[2])-float(a/b))<.08;inp.unlink()
assert paths[0][0].read_bytes()==paths[1][0].read_bytes()
# Actual native grading, every observed/generated radio option and equivalent/incorrect blanks.
engine=[]
for i,r in enumerate(originals+generated):
 f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('radio'):
  checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every displayed selection'} for c in f[':answer-field/choices']]
 else:
  a,b=read_record(r);n=s.ilcm((1/a**2).q,(1/b**2).q);cx=n/a**2;cy=n/b**2
  equiv='('+str(cx)+'*x^2+'+str(cy)+'*y^2)/'+str(n)
  checks=[{'submitted':f[':answer-field/choices'][0][':answer/value'],'expected':'accepted','purpose':'canonical fragment'},{'submitted':equiv,'expected':'accepted','purpose':'independently combined common-denominator fragment'},{'submitted':'x^2+y^2','expected':'rejected','purpose':'incorrect unit circle'}]
 engine.append({'label':str(i),'record':r,'checks':checks})
(HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n');subprocess.run([str(Path('generate/runs/current/check-engine').resolve()),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
(HERE/'review.json').write_text(json.dumps(generated,indent=2)+'\n')
review=['# Wide ellipse review','Original captures retain basis 1356 provenance. Generated records are labeled below.']
for q,r in zip(g.QS,originals):review += ['## Original '+q[':question/math-academy-id']+' — '+q[':question/difficulty'][':db/ident'].split('/')[-1],g.markdown(r)]
for r in generated:review += ['## Generated '+r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['template']+' / '+str(r['generation']['bank_profile']),g.markdown(r)]
(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
report={'status':'pass','source_questions':len(cases),'exact_source_prompts':len(cases),'exact_source_solutions':len(cases),'matched_source_options':answers,'total_source_options':answers,'matched_distractors':distractors,'total_source_distractors':distractors,'complete_radio_banks':banks,'blank_fragments':len(cases)-banks,'correct_designations':len(cases),'source_repairs':0,'observed_bank_profiles':5,'observed_templates':5,'generated_review_records':len(generated),'finite_domain_bank_instances_checked':enumerated,'domain_counts':enumeration,'meaningful_tasks_by_level_excluding_layouts_profiles':{l:len(v) for l,v in level_tasks.items()},'normal_default_tasks_by_level_excluding_layouts':{l:len(v) for l,v in default_tasks.items()},'native_engine_provenance':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ('generate/runs/current/check-engine','generate/runs/current/check-engine.rs','generate/runs/current/engine-build.log')},'native':json.loads((HERE/'engine-report.json').read_text()),'remaining_findings':['Opaque source distractor intent in q-7603 and q-69890, and denominator-4 alternatives in q-73619, is underdetermined; replay profiles preserve parameterized evidence patterns and are excluded from defaults.','Source plots use varying pixels per axis unit; labels determine radii. Generated plots use equal aspect.','Authored hard quarter-radius difficulty is a design claim, not an observed label.']}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('native','domain_counts')},indent=2))
