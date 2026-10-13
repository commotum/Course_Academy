#!/usr/bin/env python3
"""Independent displayed mathematics, complete fidelity, raster and native QA."""
import math, concurrent.futures, hashlib, importlib.util, json, re, subprocess, sys, shutil, tempfile
from pathlib import Path
from PIL import Image
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x',real=True)
checks=[]
def ck(condition,message):
 if not condition: raise AssertionError(message)
 checks.append(message)
def write(name,data): (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
def parse_prompt(prompt):
 # Read the actual displayed equation, independently of generation parameters.
 text=prompt.split('$')[1].replace(' ','').replace('{','').replace('}','')
 match=re.fullmatch(r'y=([\d.]+)\(([\d.]+)\^x\)([+-][\d.]+)[,?]?',text)
 ck(match is not None,'displayed prompt equation parses')
 k,b,c=map(sp.Rational,match.groups());return k,b,c

def formatting(text):
 ck(text.count('$')%2==0,'balanced math delimiters')
 balance=0
 for c in text:
  if c=='{': balance+=1
  if c=='}': balance-=1
  ck(balance>=0,'TeX group balance nonnegative')
 ck(balance==0,'balanced TeX groups')
 ck('--' not in text and '+-' not in text,'no bare double signs')

def raster(path):
 meta=json.loads(path.with_suffix('.json').read_text());im=Image.open(path).convert('RGB');w,h=im.size
 ck(hashlib.sha256(path.read_bytes()).hexdigest()==meta['png_sha256'],'PNG sidecar hash')
 ck(re.fullmatch(r'\d+\.\d+\.\d+',meta['python_version']) and re.fullmatch(r'\d+\.\d+\.\d+',meta['matplotlib_version']),'actual renderer runtime versions recorded')
 ck(im.size==tuple(meta['size']),'plot pixel dimensions')
 o=meta['spec']['curve'];a,b,c,shift=map(sp.Rational,[o[n] for n in ('a','b','c','h')]);s=o['s'];mx,my=map(sp.Rational,o['mark'])
 ck(sp.simplify(a*b**(s*(mx-shift))+c-my)==0,'marked coordinate lies on actual curve')
 xlo,xhi,ylo,yhi=meta['bounds'];left,bottom=meta['pixel_transform'][0];right,top=meta['pixel_transform'][1]
 def pixel(x,y): return round(left+(right-left)*(x-xlo)/(xhi-xlo)),round(h-(bottom+(top-bottom)*(y-ylo)/(yhi-ylo)))
 def blue_near(xp,yp):
  return any((lambda col: col[2]>100 and col[0]<95 and col[1]>65)(im.getpixel((xx,yy))) for xx in range(max(0,xp-4),min(w,xp+5)) for yy in range(max(0,yp-4),min(h,yp+5)))
 tested=0
 for j in range(1,31):
  x=xlo+(xhi-xlo)*j/32;y=float(a)*float(b)**(s*(x-float(shift)))+float(c)
  if ylo+.08*(yhi-ylo)<y<yhi-.08*(yhi-ylo):
   xp,yp=pixel(x,y)
   # Only black stroke occlusion has a bounded allowance; labels never
   # mask features and receive independent measured clearance checks below.
   blocked= abs(yp-pixel(x,0)[1])<5 or abs(yp-pixel(x,float(c))[1])<5
   if not blocked: ck(blue_near(xp,yp),'raster blue curve at independently calculated point '+str(path)+' '+str((x,y,xp,yp)));tested+=1
 ck(tested>=3,'sufficient visible curve samples')
 for xx,yy,ww,hh in meta.get('label_boxes',[]): ck(0<=xx and xx+ww<=w and 0<=yy and yy+hh<=h,'actual labels inside PNG')
 # Independently recompute geometry beneath every measured feature text box.
 # No white backgrounds or skipped curve samples are permitted.
 zero=meta['axis_origin_pixels'];marker=meta['marker_pixels'];occupied=[]
 for layout in meta['label_layout']:
  ck(layout['uses_background'] is False and layout['collision'] is None,'feature labels have no masking background')
  ll,bb,rr,tt=layout['bbox_pixels'];pad=4
  al,ab,ar,at=meta['axes_bbox']
  ck(ll>=al+pad and rr<=ar-pad and bb>=ab+pad and tt<=at-pad,'measured feature label bounds')
  ck(not (ll-pad<=zero[0]<=rr+pad or bb-pad<=zero[1]<=tt+pad),'measured text clear of both axes')
  asy_y=bottom+(top-bottom)*(float(c)-ylo)/(yhi-ylo)
  ck(c==0 or not bb-pad<=asy_y<=tt+pad,'measured text clear of asymptote')
  ck(not (ll-7<=marker[0]<=rr+7 and bb-7<=marker[1]<=tt+7),'measured text clear of marked point')
  ck(all(not (ll-5<r and rr+5>l and bb-5<t and tt+5>b0) for l,b0,r,t in occupied),'measured feature labels clear of other feature labels')
  for j in range(4000):
   xx=xlo+(xhi-xlo)*j/3999;yy=float(a)*float(b)**(s*(xx-float(shift)))+float(c)
   if not ylo-1<yy<yhi+1:continue
   px=left+(right-left)*(xx-xlo)/(xhi-xlo);py=bottom+(top-bottom)*(yy-ylo)/(yhi-ylo)
   if ll-pad<=px<=rr+pad and bb-pad<=py<=tt+pad:raise AssertionError('Measured label intersects independently derived curve '+str(path))
  checks.append('measured label clear of complete curve')
  occupied.append((ll,bb,rr,tt))
 return meta

def record(r):
 ck(set(r['knowledge_point'])=={'db_id','id','title'},'outer knowledge_point shape')
 q=r['question'];f=q[':question/answer-fields'][0];k,b,c=parse_prompt(q[':question/problem']);v=k+c
 ck(f[':answer-field/type']==':answer-field.type/radio','source radio type')
 ck(len(f[':answer-field/choices'])==5,'complete five-choice bank')
 formatting(q[':question/problem']);solution=q.get(':question/worked-solution');kind='intercept' if r['generation']['template'].startswith('intercept') else 'graph'
 if solution:
  formatting(solution)
  if kind=='intercept':
   # Independently verify every actual numeric math stage and conclusion.
   formula=re.search(r'Therefore, \$y=(.*?)\$',solution).group(1).rstrip(',')
   kk,bb,cc=parse_prompt('$y='+formula+'$');ck((kk,bb,cc)==(k,b,c),'conclusion equation matches displayed prompt')
   coords=re.findall(r'\(0,([+-]?[\d.]+)\)',solution);ck([sp.Rational(t) for t in coords]==[1,v],'complete prose coordinate sequence')
   block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S).group(1)
   rows=block.split('\\\\');ck(len(rows)==4,'formal intercept four ordered rows')
   ck(re.sub(r'\s','',rows[0])=='y&='+g.formula(k,b,c,'0'),'printed substitution row')
   ck(re.sub(r'\s','',rows[1])=='&='+g.number(k)+r'\cdot1'+g.sign(c),'printed exponential evaluation row')
   ck(re.sub(r'\s','',rows[2])=='&='+g.number(k)+g.sign(c),'printed product evaluation row')
   ck(sp.Rational(rows[3].replace('&','').replace('=','').strip())==v,'printed collected row')
   nums=re.findall(r'\$\$\ny=(.*?)\.\n\$\$',solution)
   ck(len(nums)==2,'two method-one evaluated blocks')
   ck(nums[0]==g.number(k)+r'\cdot 1='+g.number(k),'scaled intercept block')
   ck(nums[1]==g.number(k)+g.sign(c)+'='+g.number(v),'shifted intercept block')
   ck(f'${g.number(abs(c))}$ '+('unit' if abs(c)==1 else 'units')+' '+('up' if c>0 else 'down') in solution,'prose shift direction and magnitude')
  else:
   coords=[tuple(map(sp.Rational,m)) for m in re.findall(r'\(([+-]?[\d.]+),([+-]?[\d.]+)\)',solution)]
   ck(coords==[(0,1),(0,k),(0,k),(0,v)],'complete graph prose coordinate sequence')
   ck(solution.startswith('First, we plot') and solution.index('Next,')<solution.index('Finally,'),'three ordered transformation paragraphs')
   paths=re.findall(r'!\[\]\((.*?)\)',solution);ck(len(paths)==3,'three ordered worked plots')
   for path,(aa,dd) in zip(paths,((1,0),(k,0),(k,c))):
    if path.startswith('/'): 
     o=json.loads(Path(path).with_suffix('.json').read_text())['spec']['curve'];ck(sp.Rational(o['a'])==aa and sp.Rational(o['c'])==dd and sp.Rational(o['b'])==b,'worked plot matches printed stage')
   ck('to $y='+g.number(c)+'.$' in solution,'final prose asymptote matches prompt')
 answers=f[':answer-field/choices'];correct_ref=f.get(':answer-field/correct',[None,None])[1]
 if correct_ref:
  correct=next(a for a in answers if a[':answer/id']==correct_ref)
  if kind=='intercept':
   vals=[tuple(map(sp.Rational,re.fullmatch(r'\((.*?),(.*?)\)',a[':answer/value']).groups())) for a in answers]
   ck(len(set(vals))==5,'displayed point values distinct')
   if r['generation']['bank_profile'].startswith('intercept_authored'): ck(set(vals)=={(0,v),(v,0),(0,k),(0,c),(0,k-c)},'complete authored point operation bank read from displayed values')
   cv=tuple(map(sp.Rational,re.fullmatch(r'\((.*?),(.*?)\)',correct[':answer/value']).groups()));ck(cv==(0,v),'correct displayed point independently derived')
  elif correct[':answer/value'].startswith('/'):
   all_expr=[]
   for answer in answers:
    oo=json.loads(Path(answer[':answer/value']).with_suffix('.json').read_text())['spec']['curve']
    all_expr.append(sp.Rational(oo['a'])*sp.Rational(oo['b'])**(oo['s']*(X-sp.Rational(oo['h'])))+sp.Rational(oo['c']))
   ck(all(sp.simplify(all_expr[i]-all_expr[j])!=0 for i in range(5) for j in range(i)),'complete actual plotted bank inequivalent')
   if r['generation']['bank_profile']=='graph_authored':
    expected=[k*b**X+c,k*b**(-X)+c,b**X+c,(k+2*c)*b**X-c,k*b**(X-k)+c]
    ck(all(sum(sp.simplify(e-w)==0 for w in all_expr)==1 for e in expected),'complete authored plotted operation bank independently matches displayed equation')
   o=json.loads(Path(correct[':answer/value']).with_suffix('.json').read_text())['spec']['curve']
   e=sp.Rational(o['a'])*sp.Rational(o['b'])**(o['s']*(X-sp.Rational(o['h'])))+sp.Rational(o['c'])
   ck(sp.simplify(e-(k*b**X+c))==0,'correct actual plotted curve matches printed equation')
 ck(r['generation']['python_version']==sys.version.split()[0],'actual generator Python version')
 return r

# Independently verify extracted source raster locations, each own axes origin,
# transparencies and filled point. No uncalibrated numeric base fitting is claimed.
for evidence in json.loads((HERE/'source-geometry.json').read_text())['plots']:
 path=Path('/media/jake/SSD/EDB/math')/evidence['path'];im=Image.open(path).convert('RGBA')
 ck(list(im.size)==evidence['size'],'native source image dimensions')
 ck(hashlib.sha256(path.read_bytes()).hexdigest()==evidence['sha256'],'native source asset hash')
 ox,oy=evidence['axis_origin_pixels_native']
 def is_black(col):return max(col[:3])<30 and col[3]>100
 ck(sum(is_black(im.getpixel((ox,yy))) for yy in range(im.height))>150,'own source vertical-axis origin verified')
 ck(sum(is_black(im.getpixel((xx,oy))) for xx in range(im.width))>250,'own source horizontal-axis origin verified')
 mx,my=evidence['marked_point_pixels_native']
 ck(sum((lambda col:col[2]>100 and col[0]<95 and col[1]>65 and col[3]>100)(im.getpixel((xx,yy))) for xx in range(mx-2,mx+3) for yy in range(my-2,my+3))>=10,'actual original filled blue marker verified')
 if 'profile' in evidence:
  p=g.PARAMETERS[evidence['source_id']];k,b,c=map(sp.Rational,[p[n] for n in ('k','b','c')]);member=next(o for o in g.curve_bank(k,b,c,g.PROFILES[evidence['profile']][2]) if o['recipe']==evidence['recipe'])
  direction='increasing' if sp.Rational(member['a'])*member['s']>0 else 'decreasing'
  ck(direction==evidence['direction'] and ('left' if member['s']==1 else 'right')==evidence['approach_side'],'source member direction and limiting-side recipe fidelity')

source_cases=[];originals=[];variants=[];matched_values=matched_correct=solutions=0
for profile,(kind,sid,recipes) in g.PROFILES.items():
 if not sid: continue
 source=g.source_question(profile);level=source.get(':question/difficulty',{}).get(':db/ident','easy').split('/')[-1]
 case={'source_id':sid,'template':kind,'parameters':g.PARAMETERS[sid],'bank_profile':profile,'level':level,'raw_difficulty_present':':question/difficulty' in source}
 source_cases.append(case);r=record(g.generate(level,seed=91,profile=profile,parameters=case['parameters']));originals.append(r);q=r['question'];f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
 for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'): ck((key in q)==(key in source),'raw source question key presence '+sid+' '+key)
 ck((':answer-field/correct' in f)==(':answer-field/correct' in sf),'raw correct-ref presence '+sid)
 ck(q[':question/problem']==source[':question/problem'],'exact complete source prompt '+sid)
 ck(q.get(':question/worked-solution')==source.get(':question/worked-solution'),'exact complete source solution '+sid)
 ck(sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']),'one-to-one complete source bank '+sid);matched_values+=5
 if ':question/worked-solution' in source: solutions+=1
 if ':answer-field/correct' in sf:
  ca=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);ck(ca[':answer/value']==sf[':answer-field/correct'][':answer/value'],'source correct designation '+sid);matched_correct+=1
 variant_params={'graph_unrated':{'k':'5','b':'4','c':'-3'},'intercept_base':{'k':'4','b':'6','c':'3'},'intercept_components':{'k':'2.5','b':'4','c':'2'},'intercept_swap':{'k':'3.5','b':'2','c':'6'},'intercept_signed':{'k':'2.5','b':'10','c':'-6.5'},'graph_observed':{'k':'3','b':'4','c':'-2'}}[profile]
 variants.append(record(g.generate(level,seed=11,profile=profile,parameters=variant_params)))
write('source-cases.json',source_cases)
normal=[record(g.generate(level,seed=13+i)) for level in ('easy','hard') for i in range(2)]
normal += [record(g.generate_moderate(seed=13+i,template=mask)) for mask in g.PRESENTATIONS for i in range(2)]
coverage={g.generate_moderate(seed=i)['generation']['template'] for i in range(36)}
ck(coverage==set(g.PRESENTATIONS),'actual normal default moderate presentation coverage')
for mask in g.PRESENTATIONS:
 p={'k':'2.5','b':'4','c':'3'}
 r1=g.generate_moderate(seed=1,template=mask,parameters=p);r2=g.generate_moderate(seed=98,template=mask,parameters=p)
 ck(r1['question'][':question/id']==r2['question'][':question/id'],'fixed explicit mask content identity independent of seed')
 ck(r1['generation']['parameter_fingerprint']==g.generate_moderate(template='intercept',parameters=p)['generation']['parameter_fingerprint'],'mathematical task fingerprint excludes presentation aliases')
# Regression/extremes: all feature signs, zero/near-zero intercept and shifted
# marker; explicit mask/parameters remain fixed, no cosmetic base counts.
regression_parameters=[('easy',{'k':'8','b':'10','c':'-8'}),('easy',{'k':'8','b':'1.5','c':'8'}),('easy',{'k':'3','b':'10','c':'-1'}),('hard',{'k':'1.5','b':'10','c':'-1.5'}),('hard',{'k':'1.5','b':'1.5','c':'-0.5'}),('hard',{'k':'6.5','b':'10','c':'-8.5'}),('hard',{'k':'6.5','b':'1.5','c':'8.5'}),('hard',{'k':'6.5','b':'10','c':'0.5'}),('hard',{'k':'1.5','b':'10','c':'-2.5'}),('moderate',{'k':'1.5','b':'4','c':'-2'})]
regressions=[record(g.generate(level,seed=22,parameters=p)) for level,p in regression_parameters]
write('regressions.json',regressions)

# Boundary/identity scope checks: explicit and sampled use the same guards.
for level,p in [('easy',{'k':'1.5','b':'3','c':'2'}),('moderate',{'k':'9','b':'3','c':'2'}),('hard',{'k':'2','b':'3','c':'0.5'}),('hard',{'k':'3.5','b':'3','c':'2'}),('hard',{'k':'7.5','b':'3','c':'0.5'})]:
 try: g.generate(level,parameters=p)
 except ValueError: checks.append('explicit '+level+' guard rejects invalid bounds')
 else: raise AssertionError('Scope guard accepted invalid parameters')
for r in normal:
 g1=r['generation'];r2=g.generate(g1['difficulty_design'],seed=999,parameters=g1['parameters'],profile=g1['bank_profile']);ck(r['question'][':question/id']==r2['question'][':question/id'],'seed-independent content identity')
# Enumerate actual mathematical tasks, excluding base and all bank/notation aliases.
counts={}
for level in ('easy','moderate','hard'):
 tasks=set()
 ks=range(2,9) if level=='easy' else [sp.Rational(i,2) for i in (range(3,17) if level=='moderate' else range(3,14,2))]
 cs=[i for i in range(-8,9) if i] if level=='easy' else [sp.Rational(i,2) for i in (range(-17,18) if level=='moderate' else range(-17,18,2)) if i]
 for k in ks:
  for c in cs:
   try:
    p={'k':str(k),'b':'3','c':str(c)};kk,bb,cc=g.parameters_ok(level,p);(g.intercept_bank if level=='moderate' else g.curve_bank)(kk,bb,cc,g.PROFILES['intercept_authored' if level=='moderate' else 'graph_authored'][2]);tasks.add((str(kk),str(cc)))
   except g.Rejected: pass
 counts[level]=len(tasks)
 ck(counts[level]>=50,'meaningful finite task bank '+level)
# Concurrent public generators: duplicate and distinct parameter sets, fresh
# private cache. This exercises unique input creation and atomic sidecars through
# the actual API, rather than merely invoking a renderer twice.
with tempfile.TemporaryDirectory(dir=HERE,prefix='concurrency-') as tmp:
 root=Path(tmp);shutil.copyfile(HERE/'render.py',root/'render.py');original_here=g.HERE;g.HERE=root
 try:
  def generation_job(index):
   return g.generate_easy(seed=index,parameters={'k':'3' if index<2 else '5','b':'4','c':'-2' if index<2 else '-3'})
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: concurrent=list(pool.map(generation_job,range(3)))
  ck(concurrent[0]['question'][':question/id']==concurrent[1]['question'][':question/id'],'concurrent identical parameters preserve content identity')
  ck(concurrent[0]['question'][':question/id']!=concurrent[2]['question'][':question/id'],'concurrent distinct parameters preserve distinct content identity')
  for path in (root/'plots').glob('*.png'): raster(path)
  ck(not list((root/'plots').glob('atomic-*')) and not list((root/'plots').glob('render-*')),'public concurrent unique inputs cleaned, no atomic remnants')
  # A missing sidecar must force a fresh render even when PNG exists.
  first=next((root/'plots').glob('*.json'));png=first.with_suffix('.png');old_hash=hashlib.sha256(png.read_bytes()).hexdigest();first.unlink()
  g.generate_easy(parameters={'k':'3','b':'4','c':'-2'});g.generate_easy(parameters={'k':'5','b':'4','c':'-3'})
  ck(first.exists() and hashlib.sha256(png.read_bytes()).hexdigest()==old_hash,'cache requires both PNG and sidecar; deterministic fresh rerender')
 finally: g.HERE=original_here
# Cache needs both sidecars; scoped fresh directory checks above exercise real writes.
plot_paths={Path(a[':answer/value']) for r in originals+variants+normal+regressions for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/value'].startswith('/')}
plot_paths|={Path(p) for r in originals+variants+normal+regressions for p in re.findall(r'!\[\]\((.*?)\)',r['question'].get(':question/worked-solution','')) if p.startswith('/')}
for path in sorted(plot_paths): raster(path)
# Real native grading; every bank member submitted independently. Fieldless correct
# designation cannot be graded as observed; preserve raw evidence, report separately.
engine_input=[]
for i,r in enumerate(originals+variants+normal+regressions):
 f=r['question'][':question/answer-fields'][0]
 if ':answer-field/correct' not in f: continue
 engine_input.append({'label':str(i)+':'+r['generation']['bank_profile'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'full owned radio bank member'} for a in f[':answer-field/choices']]})
write('engine-input.json',engine_input);subprocess.run([str(HERE.parents[1]/'runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine.json')],check=True,capture_output=True)
review=originals+variants+normal;write('review.json',review)
(HERE/'review.md').write_text('# Graph recognition generator review\n\nOriginals retain absent attributes. Changed historical profiles are evidence-only variants; default practice uses separately authored method-derived banks.\n\n'+'\n\n---\n\n'.join(g.markdown(r,'Original source replay' if i<len(originals) else 'Generated historical bank variant' if i<len(originals)+len(variants) else 'Generated normal practice') for i,r in enumerate(review))+'\n')
visual=json.loads((HERE/'visual-review.json').read_text())
ck(visual['version']==g.VERSION and visual['viewed_full_resolution'] and set(visual['png_sha256'])==set(map(str,plot_paths)),'current full-resolution visual coverage')
for p,hh in visual['png_sha256'].items(): ck(hashlib.sha256(Path(p).read_bytes()).hexdigest()==hh,'visually inspected current PNG hash')
first_side=json.loads(next(iter(plot_paths)).with_suffix('.json').read_text())
write('render-provenance.json',{'version':g.VERSION,**{key:first_side[key] for key in ('python_version','matplotlib_version','numpy_version','dependencies')},'uses_feature_backgrounds':False,'curve_points_under_text_exempted':False})
engine_hash=hashlib.sha256((HERE.parents[1]/'runs/current/check-engine').read_bytes()).hexdigest()
report={'passed':True,'source':g.SOURCE['basis'],'practice_sources':6,'complete_banks_matched':6,'displayed_values_matched':matched_values,'displayed_values_total':30,'observed_correct_designations_matched':matched_correct,'observed_correct_designations_total':5,'missing_original_correct_designations':1,'exact_solutions_matched':solutions,'exact_solutions_total':5,'unrated_sources_preserved':1,'normal_levels':['easy','moderate','hard'],'authored_hard':True,'task_counts_excluding_base_bank_layout_aliases':counts,'default_moderate_masks_covered':sorted(coverage),'current_visual_review_count':visual['plot_count'],'feature_label_backgrounds':False,'curve_points_under_text_exempted':False,'regression_records':len(regressions),'generated_review_records':len(review),'rendered_pngs_independently_checked':len(plot_paths),'native_records':len(engine_input),'native_checks':sum(len(x['checks']) for x in engine_input),'native_grader_sha256':engine_hash,'native_missing_correct_raw_records_ungraded':2,'source_numerical_base_uncertainty':'all ungridded distractor graphs; source raster equality preserved, only marked-feature geometry asserted','checks_passed':len(checks),'python_version':sys.version.split()[0],'sympy_version':sp.__version__}
write('validation.json',report)
# Private frozen source/script hashes separate from native grader and math results.
write('freeze.json',{'version':g.VERSION,'sha256':{str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'render.py',HERE/'validate.py',HERE/'source.json',HERE/'source-cases.json',HERE/'review.json',HERE/'source-geometry.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'README.md',HERE/'regressions.json',HERE/'visual-review.json',HERE/'render-provenance.json',HERE/'root-findings-resolution.json',HERE/'validation.json',HERE/'render-iterations.json')},'native_grader_sha256':engine_hash,'native_grader_source_sha256':hashlib.sha256((HERE.parents[1]/'runs/current/check-engine.rs').read_bytes()).hexdigest()})
print(json.dumps(report,indent=2))
