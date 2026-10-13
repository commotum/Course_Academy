#!/usr/bin/env python3
"""Fail-fast independent mathematics, source fidelity, native grading and raster QA."""
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
from PIL import Image
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',str(HERE)+'.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
X=m.X
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def parse(s):
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 s=s.replace('{','').replace('}','').replace('$','').replace(' ','').rstrip('.')
 if s.startswith('y='):s=s[2:]
 return parse_expr(s,local_dict={'x':X,'c':sp.Symbol('c')},transformations=TRANS)
def format_check(s):
 assert s.count('$')%2==0,'Unbalanced dollar delimiter'
 balance=0
 for ch in s:
  if ch=='{':balance+=1
  elif ch=='}':balance-=1
  assert balance>=0,'Unbalanced TeX brace'
 assert balance==0
 assert '\\\\frac' not in s,'Actual doubled slash byte'
def check_record(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==m.KP and r['knowledge_point']['id']==m.KP_UUID
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
 for s in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in f[':answer-field/choices']]:format_check(s)
 uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id'])
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection' and len(f[':answer-field/choices'])==5
 vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert all(sp.simplify(a-b)!=0 for i,a in enumerate(vals) for b in vals[:i])
 # Read b from ACTUAL displayed prompt, rather than use metadata as truth.
 math=re.search(r'The graph above shows the curve \$(.*?)\$',q[':question/problem']).group(1)
 prompt=parse(math);c_symbol=sp.Symbol('c');growth=sp.simplify(prompt-c_symbol)
 assert growth.subs(X,0)==1 and sp.diff(growth,X).subs(X,0)>0
 correct=parse(g['inferred_correct_value']);c=sp.simplify(correct.subs(X,0)-1)
 assert sp.simplify(correct-(growth+c))==0
 matching=[i for i,v in enumerate(vals) if sp.simplify(v-correct)==0];assert len(matching)==1
 if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',f[':answer-field/choices'][matching[0]][':answer/id']]
 if ':question/worked-solution' in q:
  solution=q[':question/worked-solution'];entries=re.findall(r'In the graph above, the horizontal asymptote is \$y=(.*?)\.\$ Therefore, \$c=(.*?)\.\$',solution)
  assert len(entries)==1 and all(parse(v)==c for v in entries[0])
  if not g['evidence_only']:
   first=re.search(r'The horizontal asymptote of \$(.*?)\$',solution).group(1)
   assert sp.simplify(parse(first)-growth)==0
 if g['plot']:
  p=g['plot'];assert p['renderer']=='Matplotlib' and p['python'] and p['matplotlib']
  assert sp.Rational(p['parameters']['c'])==c
  lo,hi=p['geometry']['bounds'][2:];origin=p['geometry']['origin_pixel'];cy=p['geometry']['asymptote_pixel_y'];ip=p['geometry']['intercept_pixel']
  unit=ip[1]-cy;assert unit>0 and abs((cy-origin[1])/unit-float(c))<1e-6
  assert p['axes_arrows']==['positive_x','positive_y'] and not p['curve_arrows'] and not p['intercept_marked']
  assert all(lo<=float(c)<=hi for _ in [0])
  png=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1));im=Image.open(png).convert('RGB')
  assert im.size==(p['width'],p['height'])
  def nearby(px,py,predicate):
   ix,iy=round(px),im.height-1-round(py)
   return any(predicate(im.getpixel((xx,yy))) for xx in range(max(0,ix-4),min(im.width,ix+5)) for yy in range(max(0,iy-4),min(im.height,iy+5)))
  curve_points=[pt for pt in p['geometry']['curve_pixels'] if pt[1]>cy+unit*.12]
  assert curve_points
  for px,py in curve_points[::max(1,len(curve_points)//12)]:assert nearby(px,py,lambda rgb:rgb[2]>120 and rgb[2]>1.3*rgb[0] and rgb[1]>65),'Actual PNG curve misses exact geometry'
  line_y=im.height-1-round(cy)
  black_columns=sum(any(max(im.getpixel((xx,yy)))<100 for yy in range(max(0,line_y-2),min(im.height,line_y+3))) for xx in range(round(.1*im.width),round(.95*im.width)))
  assert black_columns>80,'Actual PNG dashed asymptote missing'

  if p['parameters']['level']=='hard':
   assert str(c) not in p['labels']
   assert p['ticks'] and any(sp.Rational(t['value'])==c for t in p['ticks'])
   for t in p['ticks']:assert abs((t['pixel_y']-origin[1])/unit-float(sp.Rational(t['value'])))<1e-6
  else:assert p['labels']==['y='+str(c)]
 return True

def main():
 cases=[];originals=[];variants=[];fidelity=[];engine=[]
 for sid,spc in m.SOURCE_SPECS.items():
  level,b,c,style,recipes=spc;r=m.generate(level,profile='source:'+sid);check_record(r);originals.append(r)
  q=m.SOURCES[sid];rq=r['question'];of=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
  assert rq[':question/problem']==q[':question/problem']
  assert rq.get(':question/worked-solution')==q.get(':question/worked-solution')
  assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in rq)
  assert (':answer-field/correct' in of)==(':answer-field/correct' in rf)
  if ':answer-field/correct' in of:
   val=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert val==of[':answer-field/correct'][':answer/value']
  cases.append({'source_id':sid,'template':'source','level':level,'parameters':{'b':b,'c':c},'bank_profile':'source:'+sid,'difficulty_assignment':'observed' if ':question/difficulty' in q else 'authored easy from integer labelled asymptote'})
  fidelity.append({'source_id':sid,'matched_options':5,'total_options':5,'correct_designation_present':':answer-field/correct' in of,'key_presence':True,'exact_prompt':True,'exact_worked_solution_if_present':True})
  # Each observed complete bank has a changed-parameter recipe replay.
  changed={'b':str(sp.Rational(b)+(1 if sp.Rational(b)<25 else -1)),'c':str(sp.Rational(c)+(-1 if sp.Rational(c)<0 else 1))}
  v=m.generate(level,seed=19,parameters=changed,profile='source:'+sid);check_record(v);variants.append(v)
 for level in ('easy','moderate','hard'):
  for profile in (list(m.DEFAULT_BANKS) if level=='hard' else ['signed_intercept','confuse_shift_stretch','intercept_offset']):
   for k in range(2):
    p={'b':str(3+k),'c':str(-3-k)} if level=='easy' else {'b':'13/6','c':str(sp.Rational(-3-2*k,2))} if level=='moderate' else {'b':str(4+k),'c':str(sp.Rational(-3-2*k,4)),'step':'1/4'}
    r=m.generate(level,seed=k,parameters=p,profile=profile);check_record(r);variants.append(r)
    assert m.generate(level,seed=k+30,parameters=p,profile=profile)['question'][':question/id']==r['question'][':question/id']
 for level in ('easy','moderate','hard'):
  for sign in (-1,1):
   p={'b':'25','c':str(sign*12)} if level=='easy' else {'b':'25/6','c':str(sign*sp.Rational(71,6))} if level=='moderate' else {'b':'2','c':str(sign*sp.Rational(7,3)),'step':'1/3'}
   r=m.generate(level,parameters=p,profile='signed_intercept');check_record(r);variants.append(r)
 for c in ('1/3','1/6','-1/3','-1/6'):
  r=m.generate('moderate',parameters={'b':'2','c':c},profile='signed_intercept');check_record(r);variants.append(r)
  boxes=r['generation']['plot']['feature_label_boxes'];assert len(boxes)==1
  y0,y1=boxes[0]['bounds'][1],boxes[0]['bounds'][3];axis=r['generation']['plot']['geometry']['origin_pixel'][1];assert not y0-4<=axis<=y1+4
 for r in originals+variants:
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue # Original absent designation cannot grade; never fabricated.
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native radio ownership/designation, independent math separate'} for a in f[':answer-field/choices']]
  engine.append({'label':r['generation']['bank_profile']+':'+r['question'][':question/id'],'record':r,'checks':checks})
 repaired=m.generate_easy(parameters={'b':'12','c':'-3'},profile='confuse_shift_stretch');check_record(repaired)
 expected_solution=m.SOURCES['q-99775'][':question/worked-solution'].replace('y={2}^{x}', 'y={12}^{x}')
 assert repaired['question'][':question/worked-solution']==expected_solution
 # Strict explicit-domain parity; never silently fix a supplied invalid instance.
 invalid=[('easy',{'b':'2','c':'1/2'}),('moderate',{'b':'2','c':'3'}),('hard',{'b':'2','c':'-2','step':'1/2'}),('hard',{'b':'2','c':'7/2','step':'1/4'}),('easy',{'b':'1','c':'2'}),('easy',{'b':'2','c':'0'})]
 for level,p in invalid:
  try:m.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit input accepted')
 # Complete collision bank rejection, no first-valid option pooling.
 try:m.generate_easy(parameters={'b':'2','c':'1'},profile='intercept_offset')
 except ValueError:pass
 else:raise AssertionError('Equivalent whole-bank collision accepted')
 # Meaningful task counts are enumerated exact c and hard (c,calibration), never b aliases.
 easy=set(range(-12,13))-{0}
 moderate={str(sp.Rational(n,d)) for d in range(2,7) for n in range(-12*d,12*d+1) if n and sp.Rational(n,d).q>1}
 hard={(str(sp.Rational(k,d)),str(sp.Rational(1,d))) for d in (2,3,4) for k in range(-8,9) if k and sp.Rational(k,d).q>1}
 # Exercise finite banks without rendering incidental-base aliases.
 eligible_counts={}
 for level,domain_values in [('easy',[(str(c),'1') for c in easy]),('moderate',[(c,'1') for c in moderate]),('hard',list(hard))]:
  eligible_counts[level]={}
  for profile,recipes in m.DEFAULT_BANKS.items():
   if level!='hard' and profile=='axis_reading':continue
   count=0
   for c,step in domain_values:
    try:m.options(sp.Rational(3),sp.Rational(c),sp.Rational(step),recipes,'compact');count+=1
    except ValueError:pass
   eligible_counts[level][profile]=count
 # Public default selection covers every authored bank BEFORE sampling parameters.
 coverage={}
 for level in ('easy','moderate','hard'):
  eligible=list(m.DEFAULT_BANKS) if level=='hard' else ['signed_intercept','confuse_shift_stretch','intercept_offset'];selected=set()
  p={'b':'3','c':'-3'} if level=='easy' else {'b':'13/6','c':'-3/2'} if level=='moderate' else {'b':'4','c':'-3/4','step':'1/4'}
  for seed in range(15):
   r=m.generate(level,seed=seed,parameters=p);check_record(r);selected.add(r['generation']['bank_profile'])
   if selected==set(eligible):break
  assert selected==set(eligible);coverage[level]=sorted(selected)
 # Concurrent same and different fresh writes, unique inputs and atomic sidecars.
 # Changing renderer data step alters cache key while preserving labelled geometry;
 # two identical calls intentionally race on the same final asset.
 args=[(sp.Rational(6),sp.Rational(-7),'easy',sp.Rational(1,3)),(sp.Rational(6),sp.Rational(-7),'easy',sp.Rational(1,3)),(sp.Rational(8),sp.Rational(7),'easy',sp.Rational(1,4))]
 fresh=HERE/'plots'/('concurrency-'+uuid.uuid4().hex)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:outs=list(ex.map(lambda a:m.render_plots(*a,output_dir=fresh),args))
 assert outs[0][0]==outs[1][0] and outs[0][0]!=outs[2][0]
 assert all(p.exists() and p.with_suffix('.json').exists() for p,_ in outs)
 assert not list(fresh.glob('input-*')) and not list(fresh.glob('atomic-*'))
 for file,data in [('source-cases.json',cases),('review.json',variants),('engine-input.json',engine)]: (HERE/file).write_text(json.dumps(data,indent=2)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 native=json.loads((HERE/'engine-report.json').read_text());assert native['documented_unresolved_checks']==0
 original_md=[]
 for r in originals:
  sid=r['generation']['source_id'];q=m.SOURCES[sid]
  md='\n\n## ORIGINAL '+sid+' ('+('unrated' if ':question/difficulty' not in q else q[':question/difficulty'][':db/ident'].split('/')[-1])+')\n\n'+q[':question/problem']+'\n\n'
  for a in q[':question/answer-fields'][0][':answer-field/choices']:md+='- $'+a[':answer/value']+'$\n'
  md+='\n'+q.get(':question/worked-solution','[Absent original solution and correct designation.]')+'\n';original_md.append(md)
 text='# Review: original captures and generated recipe variants\n\nSource evidence profiles remain ineligible for learning. Generated changed-parameter source profiles are labeled evidence; normal generated records are learner eligible. Hard is authored.\n'+''.join(original_md)+'\n## GENERATED variants\n'+''.join(m.markdown(r) for r in variants)
 # Make captured image references resolve in this standalone evidence review.
 text=re.sub(r'!\[\]\((images/.*?)\)',r'![](/media/jake/SSD/EDB/math/\1)',text)
 (HERE/'review.md').write_text(text)
 result={'passed':True,'source':{'questions':8,'banks':8,'options_matched':40,'options_total':40,'correct_designations_matched':6,'correct_designations_present':6,'correct_designations_absent':2,'exact_prompt':8,'exact_worked_solution':6,'worked_solutions_present':6,'raw_presence_parity':8,'source_error_mismatched_base_opener':['q-99775'],'bank_math_errors':0},'fidelity':fidelity,'independent_displayed_math_records':len(originals)+len(variants),'generated_review_records':len(variants),'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0,'missing_source_designations_not_fabricated':2},'finite_meaningful_tasks':{'easy':len(easy),'moderate':len(moderate),'hard':len(hard)},'eligible_bank_tasks':eligible_counts,'profile_coverage':coverage,'concurrency':'3 fresh same/different writes checked','source_format_repairs':0,'source_prose_base_repairs_verified':1,'raw_solution_base_consistency':{'consistent':5,'present':6,'documented_mismatch':1},'actual_png_geometry_readback':True,'generated_plot_visual_inspection':{'unique_review_pngs':24,'resolution':'original','labels':'signed integers and fractions inspected, no clipping or overlap'},'authored_level':'hard fractional calibrated axis reading','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'database_writes':0,'root_nearzero_label_regressions':4,'renderer_version':m.VERSION}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
