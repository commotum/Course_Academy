#!/usr/bin/env python3
"""Independent displayed-math, source, raster, scope, identity and native checks."""
import concurrent.futures, copy, hashlib, importlib.util, json, math, re, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as sp
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def assertion(v,msg):
 if not v:raise AssertionError(msg)
def angle_degrees(v):
 if '∘' in v or '^\\circ' in v:return int(re.search(r'\d+',v)[0])
 return int(sp.simplify(g.latex_expr(v)*180/sp.pi))
def read_prompt(record):
 text=record['question'][':question/problem'];ms=[m.group(2) for m in g.MATH.finditer(text) if m.group(2) is not None]
 polar=next(s for s in ms if s.startswith('(') and ',' in s and (r'pi' in s or 'π' in s or '∘' in s))
 r,a=polar.rstrip(',.').strip('()').split(',');angle=next(s for s in ms if 'AOB' in s).split('=')[1].rstrip(',.')
 return g.latex_expr(r),angle_degrees(a),angle_degrees(angle)
def numeric_math(v):
 v=v.replace(r'\cdot','*').replace(r'\,','').strip().rstrip('.')
 # Independent value parsing of actual displayed numeric product stage.
 v=re.sub(r'(?<=\))(?=\()', '*',v)
 return g.latex_expr(v)
def format_check(text):
 # Complete math spans exhaust dollar signs; nonliteral groups balance.
 assertion(text.count('$')%2==0,'dollar delimiter imbalance')
 rem=g.MATH.sub('',text);assertion('$' not in rem,'unmatched math delimiter')
 for m in g.MATH.finditer(text):
  body=m.group(1) if m.group(1) is not None else m.group(2)
  depth=0
  for i,c in enumerate(body):
   if c in '{}' and (i==0 or body[i-1]!='\\'):
    depth+=1 if c=='{' else -1;assertion(depth>=0,'unbalanced TeX group')
  assertion(depth==0,'unbalanced TeX groups')
 assertion('--' not in text and '+-' not in text,'ungrouped numeric signs')
def displayed_check(record):
 q=record['question'];r,a,d=read_prompt(record);p=record['generation']['parameters'];s=p['direction'];b=a+s*d
 expected=(sp.simplify(r*sp.cos(sp.pi*b/180)),sp.simplify(r*sp.sin(sp.pi*b/180)))
 assertion(expected==tuple(sp.sympify(x) for x in record['generation']['correct_mathematics']),'displayed prompt disagrees with metadata')
 assertion(set(record['knowledge_point'])=={'db_id','id','title'},'outer shape')
 for f in q[':question/answer-fields']:
  uuid_check(f[':answer-field/id'])
  if f[':answer-field/type'].endswith('/blank'):assertion('{{'+f[':answer-field/key']+'}}' in q[':question/problem'],'missing blank placeholder')
  vals=[g.parse_pair(z[':answer/value']) if f[':answer-field/type'].endswith('/radio') else (g.latex_expr(z[':answer/value']),) for z in f[':answer-field/choices']]
  assertion(len(set(vals))==len(vals),'equivalent option collision')
  if ':answer-field/correct' in f:
   answer=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);val=g.parse_pair(answer[':answer/value']) if len(vals)>1 else (g.latex_expr(answer[':answer/value']),)
   target=expected if len(vals)>1 else (expected[int(f[':answer-field/key'][-1])-1],)
   assertion(val==target,'actual bank designation wrong')
 for text in (q[':question/problem'],q.get(':question/worked-solution','')):format_check(text)
 if ':question/worked-solution' not in q:return
 solution=q[':question/worked-solution'];blocks=[m.group(1) for m in g.MATH.finditer(solution) if m.group(1) is not None]
 assertion(len(blocks)==4,'expected angle, conversion, x rows, y rows')
 theta=blocks[0].split('=')[1:];assertion(len(theta)==2,'angle stage count')
 lhs=re.split(r'([+-])',theta[0]);calc=angle_degrees(lhs[0])+(1 if lhs[1]=='+' else -1)*angle_degrees(lhs[2]);assertion(calc==b and angle_degrees(theta[1].strip().rstrip('.'))==b,'displayed angle sum')
 for c,value in zip(('x','y'),expected):
  block=next(t for t in blocks if r'\begin{aligned}'+c in t);rows=block.split(r'\\');assertion(len(rows)==4,'coordinate stage count')
  sub=rows[1].split('=')[1].strip();r_sub=sub[:sub.index(r'\operatorname')];trig_angle=sub[sub.index('(')+1:sub.rindex(')')]
  assertion(g.latex_expr(r_sub)==r and angle_degrees(trig_angle)==b,'actual substituted trig stage')
  val=numeric_math(rows[2].split('=')[1]);assertion(sp.simplify(val-value)==0,'actual evaluated factor product')
  final=rows[3].split('=')[1].split(r'\end')[0];assertion(sp.simplify(numeric_math(final)-value)==0,'actual final coordinate')
 final=solution.split('Therefore,')[-1];tuple_=next(m.group(2) for m in g.MATH.finditer(final) if m.group(2) and m.group(2).startswith('('));assertion(g.parse_pair(tuple_.rstrip('.'))==expected,'stale concluding coordinates')
 # Prose radius and polar coordinates independently read back.
 for s_ in [m.group(2) for m in g.MATH.finditer(solution) if m.group(2)]:
  if s_.startswith('r='):assertion(g.latex_expr(s_[2:].rstrip('.'))==r,'stale prose radius')
 for value in re.findall(r'circle of radius \$(.*?)\$',solution):
  if value.rstrip('.,')!='r':assertion(g.latex_expr(value.rstrip('.,'))==r,'stale circle-radius sentence')
 polar_tuples=[m.group(2) for m in g.MATH.finditer(solution) if m.group(2) and m.group(2).startswith('(')][:2]
 for tuple_,theta_ in zip(polar_tuples,(a,b)):
  rv,av=tuple_.rstrip(',.').strip('()').split(',');assertion(g.latex_expr(rv)==r and angle_degrees(av)==theta_,'stale prose polar tuple')

def uuid_check(v):
 import uuid
 uuid.UUID(v)
def blue(path):
 im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);rgb=np.array(bg.convert('RGB')).astype(int)
 return rgb,(rgb[:,:,2]>rgb[:,:,0]+35)&(rgb[:,:,1]>rgb[:,:,0]+20)&(rgb[:,:,0]<130)
def arc_direction(mask,origin,lo,hi,alpha,delta):
 yy,xx=np.nonzero(mask);dx=xx-origin[0];dy=origin[1]-yy;rad=np.hypot(dx,dy);ang=(np.degrees(np.arctan2(dy,dx))%360);ang=ang[(rad>=lo)&(rad<=hi)]
 scores={}
 for sign in (-1,1):
  probes=np.linspace(alpha+sign*delta*.12,alpha+sign*delta*.88,30)%360
  scores[sign]=int(sum(np.any(np.abs((ang-v+180)%360-180)<3) for v in probes))
 return max(scores,key=scores.get),scores

def raster_generated(path):
 path=Path(path);meta=json.loads(path.with_suffix('.json').read_text());rgb,mask=blue(path);assertion(hashlib.sha256(path.read_bytes()).hexdigest()==meta['sha256'],'raster/sidecar hash mismatch');assertion(list(Image.open(path).size)==meta['size_px'],'pixel size');assertion(abs(Image.open(path).info['dpi'][0]-meta['dpi'])<.1,'actual saved DPI');assertion(list(Image.open(path).info['dpi'])==meta['saved_dpi'],'saved DPI sidecar mismatch')
 matrix=np.array(meta['transform']);origin=np.array(meta['origin_px']);radius=matrix[0,0];assertion(abs(matrix[0,0]-matrix[1,1])<1e-6,'noncircular axes transformation')
 ys,xs=np.nonzero(mask);points=np.stack((xs,ys),axis=1);rel=points-origin*np.array([1,1]);rel[:,1]=-(ys-(rgb.shape[0]-origin[1]));rr=np.hypot(rel[:,0],rel[:,1]);circlepts=points[(rr>radius-4)&(rr<radius+4)]
 # Actual circle extents are bounded by saved transform plus stroke/AA allowance.
 for k in (0,1):assertion(abs(np.ptp(circlepts[:,k])-2*radius)<8,'actual circle raster geometry')
 for pt in meta['endpoints_px']:
  raster_pt=np.array([pt[0],rgb.shape[0]-pt[1]]);near=points[np.linalg.norm(points-raster_pt,axis=1)<5];assertion(len(near)>10,'missing actual filled endpoint marker')
 origin_raster=(origin[0],rgb.shape[0]-origin[1]);direction,scores=arc_direction(mask,origin_raster,.26*radius,.34*radius,meta['geometry']['alpha'],meta['geometry']['delta']);assertion(direction==meta['geometry']['direction'],'raster arc route')
 for item in meta['clearances']:
  assertion(item['curve_axis_clearance_px']>=2.0,'text overlaps unmasked curve/axis: '+str(item))
  assertion(item['marker_clearance_px']>=5,'text overlaps marker')
 for bb in meta['text_bboxes'].values():assertion(0<=bb[0]<bb[2]<=rgb.shape[1] and 0<=bb[1]<bb[3]<=rgb.shape[0],'text clipped')
 return {'path':str(path),'arc_scores':scores,'minimum_clearance_px':min(v['curve_axis_clearance_px'] for v in meta['clearances'])}

def source_geometry(qid,q):
 path=Path('/media/jake/SSD/EDB/math')/re.search(r'images/[^)]+',q[':question/problem'])[0];rgb,mask=blue(path)
 # Axes origin fitted separately for each image from long black runs.
 black=(rgb[:,:,:3].max(axis=2)<70);x=int(np.argmax(black.sum(axis=0)));y=int(np.argmax(black.sum(axis=1)));origin=(x,y)
 blue_x=np.flatnonzero(mask[y]);edges=(int(blue_x.min()),int(blue_x.max()));radius=(edges[1]-edges[0])/2
 p=g.source_params(qid);a=p['alpha'];b=a+p['direction']*p['delta'];yy,xx=np.nonzero(mask);pts=np.stack((xx,yy),axis=1);angles=[]
 for theta in (a,b):
  expected=np.array([x+radius*math.cos(math.radians(theta)),y-radius*math.sin(math.radians(theta))]);near=pts[np.linalg.norm(pts-expected,axis=1)<5];assertion(len(near)>10,'source marker not at extracted ray '+qid)
  centroid=near.mean(axis=0);measured=math.degrees(math.atan2(y-centroid[1],centroid[0]-x))%360;assertion(abs((measured-theta+180)%360-180)<3,'source endpoint angle mismatch');angles.append(measured)
 direction,scores=arc_direction(mask,origin,13,45,a,p['delta']);assertion(direction==p['direction'],'source arc direction '+qid)
 return {'source_id':qid,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'dimensions':list(Image.open(path).size),'fitted_origin_px':origin,'fitted_circle_radius_px':radius,'measured_endpoint_angles':angles,'arc_route_scores':scores,'geometry_checked':True}

def grading(records):
 inp=[]
 for i,record in enumerate(records):
  checks=[]
  for j,f in enumerate(record['question'][':question/answer-fields']):
   if ':answer-field/correct' not in f:continue
   if f[':answer-field/type'].endswith('/radio'):
    checks += [{'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete displayed radio bank'} for a in f[':answer-field/choices']]
   else:
    val=f[':answer-field/choices'][0][':answer/value'];equiv=r'\frac{'+val+r'+('+val+r')}{2}'
    checks += [{'field_index':j,'submitted':v,'expected':e,'purpose':purpose} for v,e,purpose in [(val,'accepted','canonical entry'),(equiv,'accepted','unreduced equivalent expression'),(val+'+1','rejected','wrong coordinate')]]
  if checks:inp.append({'label':str(i),'record':record,'checks':checks})
 (ROOT/'engine-input.json').write_text(json.dumps(inp,indent=2));subprocess.run(['generate/runs/current/check-engine',str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 return json.loads((ROOT/'engine-report.json').read_text())

def main():
 snapshot=Path('generate/runs/current/sources/17592186092273.json');assertion(json.loads(snapshot.read_text())==g.SOURCE,'frozen source wrapper changed')
 g.DATA['e-7116']=('3',45,90,1,'radian')
 canonical=source_geometry('e-7116',g.REC[':knowledge-point/canonical-example']);del g.DATA['e-7116']
 (ROOT/'canonical-geometry.json').write_text(json.dumps(canonical,indent=2))
 originals=[];variants=[];cases=[];geometry=[];counts={'questions':0,'banks':0,'values':0,'correct_designations':0,'exact_prompts':0,'exact_solutions':0,'solution_denominator':0}
 for qid,q in g.QUESTIONS.items():
  p=g.source_params(qid);rec=g.generate('hard',template=qid,parameters=p,profile='observed-'+qid);originals.append(rec);cases.append({'source_id':qid,'template':qid,'parameters':p,'bank_profile':'observed-'+qid,'authored_level_assignment':'hard' if ':question/difficulty' not in q else None});displayed_check(rec);geometry.append(source_geometry(qid,q))
  assertion(rec['question'][':question/problem']==q[':question/problem'],'source prompt fidelity');counts['exact_prompts']+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assertion((key in q)==(key in rec['question']),'raw key presence')
  if ':question/worked-solution' in q:assertion(q[':question/worked-solution']==rec['question'][':question/worked-solution'],'complete source prose/sequence');counts['exact_solutions']+=1;counts['solution_denominator']+=1
  counts['questions']+=1
  for old,new in zip(q[':question/answer-fields'],rec['question'][':question/answer-fields']):
   assertion(old[':answer-field/type'][':db/ident']==new[':answer-field/type'],'source layout');assertion((':answer-field/correct' in old)==(':answer-field/correct' in new),'source correct presence');assertion(sorted(a[':answer/value'] for a in old[':answer-field/choices'])==sorted(a[':answer/value'] for a in new[':answer-field/choices']),'complete source bank');counts['banks']+=1;counts['values']+=len(old[':answer-field/choices'])
   if ':answer-field/correct' in old:
    answer=next(a for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1]);assertion(answer[':answer/value']==old[':answer-field/correct'][':answer/value'],'correct designation match');counts['correct_designations']+=1
  # Genuine parameterized evidence scaling; no literal source-payload branch.
  p2=dict(p,radius=sp.sstr(g.exact(p['radius'])/2));scaled=g.generate('hard',template=qid,parameters=p2,profile='observed-'+qid);displayed_check(scaled);variants.append(scaled)
  # Every bank/template also gets a supported normal authored-bank variant.
  normal=g.generate('hard',seed=100+len(variants),template=qid);displayed_check(normal);variants.append(normal)
 for level in ('easy','moderate','hard'):
  for seed in range(6):
   r=g.generate(level,seed=seed);displayed_check(r);variants.append(r)
 default_coverage=set(r['generation']['template'] for r in variants if not r['generation']['evidence_only'] and r['generation']['template'] in g.QUESTIONS)
 # Explicit variants above cover all masks; separately demonstrate random default coverage.
 sampled=set()
 for seed in range(80):
  rec=g.generate('hard',seed=seed);sampled.add(rec['generation']['template'])
  if seed<2 or rec['generation']['template'] not in {r['generation']['template'] for r in variants[20:]}:displayed_check(rec);variants.append(rec)
  if sampled==set(g.QUESTIONS):break
 assertion(sampled==set(g.QUESTIONS),'normal default family coverage')
 variety={}
 for level in ('easy','moderate','hard'):
  dom=list(g.domain(level));task_keys={(sp.sstr(g.exact(p['radius'])),p['alpha'],p['delta'],p['direction']) for p in dom}
  valid=sum(g._valid_bank(p,'radio') for p in dom);variety[level]={'meaningful_tasks_excluding_units':len(task_keys),'blank_instances':len(dom),'radio_eligible_instances':valid}
 # Stable mathematical/content identity excludes seed/choice order.
 source=g.generate('hard',template='q-120593',profile='observed-q-120593')
 normal=g.generate('hard',template='q-120593',parameters=g.source_params('q-120593'))
 assertion(source['generation']['mathematical_fingerprint']==normal['generation']['mathematical_fingerprint'],'bank profile inflates mathematical task')
 assertion(source['question'][':question/id']!=normal['question'][':question/id'],'different displayed banks share identity')
 p=dict(radius='6',alpha=150,delta=90,direction=-1,units='degree')
 a=g.generate('hard',seed=1,template='q-120593',parameters=p);b=g.generate('hard',seed=2,template='q-120593',parameters=p);assertion(a['question'][':question/id']==b['question'][':question/id'],'seed changes content identity')
 radians=g.generate('hard',template='q-120593',parameters=dict(p,units='radian'))
 assertion(a['generation']['mathematical_fingerprint']==radians['generation']['mathematical_fingerprint'],'angle-unit alias inflates mathematical task')
 specimen=g.generate('hard',template='q-277027',parameters=dict(radius='5*sqrt(2)',alpha=135,delta=75,direction=-1,units='radian'))
 corrupted=copy.deepcopy(specimen)
 corrupted['question'][':question/worked-solution']=re.sub(r'(circle of radius \$)[^$]+(\$)',r'\g<1>10,\2',corrupted['question'][':question/worked-solution'],count=1)
 try:displayed_check(corrupted)
 except AssertionError:pass
 else:raise AssertionError('missed stale circle-radius sentence with otherwise correct arithmetic')
 for level,p in [('easy',dict(radius='12',alpha=0,delta=30,direction=1,units='degree')),('moderate',dict(radius='6',alpha=0,delta=45,direction=1,units='degree')),('hard',dict(radius='4',alpha=120,delta=30,direction=1,units='degree'))]:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('explicit workload escape')
 # Fresh independent concurrent processes: identical and different geometry,
 # unique private cache, no prior cached assets and no cache pruning.
 concurrent_dir=ROOT/'concurrent'/next(tempfile._get_candidate_names());concurrent_dir.mkdir(parents=True)
 params=[dict(radius='6',alpha=150,delta=105,direction=-1,units='degree'),dict(radius='4',alpha=60,delta=180,direction=1,units='degree')]
 render_code="import importlib.util,json,sys; s=importlib.util.spec_from_file_location('g',sys.argv[1]);g=importlib.util.module_from_spec(s);s.loader.exec_module(g);print(g.render_plots(json.loads(sys.argv[2]),sys.argv[3]))"
 def invoke(p):return subprocess.check_output([sys.executable,'-c',render_code,str(ROOT.with_suffix('.py')),json.dumps(p),str(concurrent_dir)],text=True).strip()
 with concurrent.futures.ThreadPoolExecutor(4) as pool:paths=list(pool.map(invoke,[params[0],params[0],params[1],params[1]]))
 assertion(paths[0]==paths[1] and paths[2]==paths[3] and paths[0]!=paths[2],'concurrent identity')
 assertion(len(list(concurrent_dir.glob('*')))==4,'temporary render leak')
 raster=[]
 for path in sorted(set([r['generation']['plot'] for r in variants if not r['generation']['plot'].startswith('images/')]+paths)):raster.append(raster_generated(path))
 engine=grading(originals+variants)
 (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2));(ROOT/'source-geometry.json').write_text(json.dumps(geometry,indent=2));(ROOT/'review.json').write_text(json.dumps({'originals':originals,'generated_variants':variants},indent=2,ensure_ascii=False))
 review=['# Source originals and generated variants','Raw evidence preserves omitted fields and opaque banks; normal variants are explicitly authored method-bank questions.']
 for old,var,normal in zip(originals,variants[0:20:2],variants[1:20:2]):review.extend(['\n## '+old['generation']['template']+' — original',g.markdown(old),'\n### Generated radius-scaled opaque evidence variant',g.markdown(var),'\n### Generated normal method-bank variant',g.markdown(normal)])
 for i,r in enumerate(variants[20:]):review.extend(['\n## Authored '+r['question'][':question/difficulty'].split('/')[-1]+' variant '+str(i),g.markdown(r)])
 (ROOT/'review.md').write_text('\n\n'.join(review))
 report={'passed':True,'canonical_geometry':canonical,'source_snapshot_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),'source_fidelity':counts,'raw_missing_correct_references':2,'raw_missing_solutions':2,'raw_missing_difficulty':2,'authored_missing_levels':['easy','moderate'],'raw_evidence_only_banks':8,'source_geometry':geometry,'raster_checks':raster,'variety':variety,'generated_variants_checked':len(variants),'default_family_coverage':sorted(sampled),'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_omitted_raw_records':['q-40920','q-40922'],'native_omission_reason':'Raw evidence has no source correct ref; separately authored completions are graded.','native_binary_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__},'concurrency_fresh_cache':str(concurrent_dir),'limits':['Opaque historical wrong-option intent is not recovered; complete radius-scaled evidence banks are ineligible for learning.','Two inferred answers have no captured source correct designation and do not count as designation fidelity.','Authored difficulty bounds are design claims; no easy/moderate observed practice exists.']}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ('passed','source_fidelity','variety','native')},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:
  (ROOT/'validation.json').write_text(json.dumps({'passed':False,'error':str(e)},indent=2));raise
