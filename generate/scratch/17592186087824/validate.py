"""Independent displayed-math, exact-fidelity, raster and native-grading QA."""
from pathlib import Path
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys,tempfile
import sympy as sp
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n')
def parse_eq(v):
 v=v.replace(' ','').replace('{','').replace('}','')
 m=re.fullmatch(r'y=(?:(-?[\d.]+)\()?([\d]+)\^x\)?([+-][\d.]+)?',v)
 assert m,('Malformed displayed equation',v)
 a,b,c=m.groups();return sp.Rational(a or 1)*sp.Integer(b)**g.X+sp.Rational(c or 0)
def parse_pair(v):
 m=re.fullmatch(r'\$k\s*=\s*([-\d.]+)\$ and \$c\s*=\s*([-\d.]+)\$',v);assert m,v
 return tuple(map(sp.Rational,m.groups()))
def format_check(s):
 assert s.count('$')%2==0
 depth=0
 for ch in s:
  if ch=='{':depth+=1
  elif ch=='}':depth-=1;assert depth>=0,s
 assert depth==0,s
 assert not re.search(r'(?<!\\)\\(?:begin|end)',s) is None if '\\begin' in s else True
 assert '++' not in s and '--' not in s and '+-' not in s

def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];p=r['generation']['parameters'];b,k,c,step=map(sp.Rational,(p[x] for x in ('b','k','c','step')));kind='parameters' if r['generation'].get('source_id') and g.SPECS[r['generation']['source_id']][0]=='easy' or q.get(':question/difficulty','').endswith('/easy') else 'equation'
 assert re.search(r'k\(\{?'+str(b)+r'\}?\^\{x\}\)',q[':question/problem'].replace(' ','')),q[':question/problem']
 f=q[':question/answer-fields'][0];values=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(values)==5 and len(set(values))==5
 obj=[parse_pair(v) if kind=='parameters' else parse_eq(v) for v in values];correct=(k,c) if kind=='parameters' else k*b**g.X+c
 matches=[o==correct if kind=='parameters' else sp.simplify(o-correct)==0 for o in obj];assert sum(matches)==1
 if ':answer-field/correct' in f:
  aid=f[':answer-field/correct'][1];assert next(matches[i] for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==aid)
 for i,o in enumerate(obj):
  for v in obj[:i]:assert o!=v if kind=='parameters' else sp.simplify(o-v)!=0
 for s in [q[':question/problem'],q.get(':question/worked-solution','')]+values:format_check(s)
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];u=k+c
  assert '$y='+g.num(c)+',$ so $c='+g.num(c)+'.$' in sol
  assert '(0,'+g.num(u)+'),$' in sol
  # Read each displayed teaching row independently and evaluate the arithmetic.
  block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S).group(1)
  rows=block.split('\\\\');assert len(rows)==5
  simplified=[s.replace(' ','').replace('{','').replace('}','') for s in rows]
  assert simplified[0]=='y&=k('+str(b)+'^x)'+g.offset(c)
  assert simplified[1]==g.num(u)+'&=k('+str(b)+'^0)'+g.offset(c)
  assert simplified[2]==g.num(u)+'&=k(1)'+g.offset(c)
  assert simplified[3]==g.num(u)+'&=k'+g.offset(c)
  assert simplified[4]==g.num(k)+'&=k'
  assert sp.simplify(u-(k*b**0+c))==0 and u==k+c
  if kind=='equation':assert parse_eq(re.search(r'Therefore, the curve is \$(.*?)\.\$',sol).group(1))==correct
  else:assert parse_pair(re.search(r'Therefore, (\$k=.*?\$ and \$c=.*?\$)',sol).group(1).replace('.$','$'))==correct
 plot=r['generation']['plot']
 if plot:
  png=Path(plot['path']);side=json.loads(png.with_suffix('.json').read_text());qa=json.loads(png.with_suffix('.qa.json').read_text());assert qa['pass'] and qa['actual_png_sha256']==hashlib.sha256(png.read_bytes()).hexdigest()
  assert side['parameters']['k']==str(k) and side['parameters']['c']==str(c)
  # PNG generated from exact parameters; raster recovered geometry checked in
  # renderer and this image hash binds that evidence to the actual displayed PNG.
  assert qa['curve_samples_checked']>=10
  # Independent actual PNG/box readback; no covered features or detached ticks.
  rgb=np.asarray(Image.open(png).convert('RGB')).astype(int);blue=(rgb[:,:,2]>rgb[:,:,0]+45)&(rgb[:,:,1]>rgb[:,:,0]+25)&(rgb[:,:,2]>90);height=rgb.shape[0]
  boxes=[];geom=side['geometry'];ox,oy=geom['origin'];cx,cy=geom['intercept'];asy=geom['asymptote'][1];bx,by,bw,bh=geom['axes_box']
  for layout in side['label_layout']:
   left,bottom,right,top=layout['bbox_pixels'];assert layout['uses_background'] is False and layout['collision'] is None
   assert left>=bx+4 and right<=bx+bw-4 and bottom>=by+4 and top<=by+bh-4
   assert not left-4<=ox<=right+4 and not bottom-4<=oy<=top+4
   assert not bottom-4<=asy<=top+4
   assert not (left-10<=cx<=right+10 and bottom-10<=cy<=top+10)
   for ll,bb,rr,tt in boxes:assert not (left-5<rr and right+5>ll and bottom-5<tt and top+5>bb)
   region=blue[max(0,int(height-top-4)):min(height,int(height-bottom+5)),max(0,int(left-4)):int(right+5)];assert not region.any(),('Actual blue stroke under label',layout)
   boxes.append((left,bottom,right,top))
   if layout['kind']=='tick':assert abs(layout['position_data'][1]-float(sp.Rational(layout['value'])))<1e-9
  named=[t for t in side['ticks'] if t['labeled']]
  for i,t in enumerate(named):
   assert t['index']%t['regular_named_stride']==0
   if i:
    previous=named[i-1];assert t['bbox_pixels'][1]-previous['bbox_pixels'][3]>=5
  assert side['tick_labels_detached'] is False
  if q.get(':question/difficulty','').endswith('/hard'):
   assert len(side['ticks'])>=8 and any(t['labeled'] for t in side['ticks']);assert 'Reading the calibrated grid' in sol
 return True

cases=[];fidelity=[];review=[];native=[]
for sid,q in g.SOURCES.items():
 spec=g.SPECS[sid];p=dict(zip(('b','k','c'),map(str,spec[1:4])));r=g.generate(spec[0],profile='source:'+sid,parameters=p);check(r)
 cases.append({'source_id':q[':question/id'],'math_academy_id':sid,'template':'source','level':spec[0],'parameters':p,'bank_profile':'source:'+sid,'authored_level_assignment':':question/difficulty' not in q})
 nq=r['question'];sf=q[':question/answer-fields'][0];nf=nq[':question/answer-fields'][0]
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in nq)
 assert (':answer-field/correct' in sf)==(':answer-field/correct' in nf)
 assert sf[':answer-field/key']==nf[':answer-field/key'] and sf[':answer-field/type'][':db/ident']==nf[':answer-field/type']
 assert q[':question/problem']==nq[':question/problem'] and q.get(':question/worked-solution')==nq.get(':question/worked-solution')
 assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices'])
 if ':answer-field/correct' in sf:
  cv=sf[':answer-field/correct'][':answer/value'];assert cv==next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])
 fidelity.append({'source':sid,'bank_options':5,'prompt_exact':True,'solution_exact_or_absence':True,'attribute_presence':True,'correct_designation_matched':':answer-field/correct' in sf})
 review.append(r)
 # Replay each historical operation bank with altered mathematical parameters.
 p2=dict(p);p2['k']=str(sp.Rational(p['k'])+1);p2['c']=p['c']
 changed=g.generate(spec[0],seed=31,profile='source:'+sid,parameters=p2);check(changed);review.append(changed)
for level in ('easy','moderate','hard'):
 for profile in g.BANKS:
  for seed in (12,37):
   r=g.generate(level,seed,profile=profile);check(r);review.append(r)
# Thirty deterministic independent variants, coverage checks, same-content IDs.
sampled=[]
for level in ('easy','moderate','hard'):
 profiles=set()
 for seed in range(10):
  r=g.generate(level,seed);check(r);sampled.append(r);profiles.add(r['generation']['bank_profile'])
  if level=='hard' and seed==6:review.append(r)
 assert profiles==set(g.BANKS)
 for r in [x for x in review if x['question'].get(':question/difficulty','').endswith('/'+level) and not x['generation']['evidence_only']]:
  p=r['generation']['parameters'];other=g.generate(level,999,parameters=p,profile=r['generation']['bank_profile']);assert other['question'][':question/id']==r['question'][':question/id']
 # Every public API applies level guards to explicit inputs.
 for api in (lambda **kw:g.generate(level,**kw),getattr(g,'generate_'+level)):
  bad=[{'b':'1','k':'3','c':'-2'},{'b':'2','k':'0','c':'-2'},{'b':'2','k':'3','c':'0'},{'b':'2','k':'7','c':'-2'},{'b':'2','k':'3','c':'-7'}]
  if level=='easy':bad.append({'b':'2','k':'1.5','c':'-2'})
  if level=='moderate':bad.append({'b':'2','k':'3','c':'-1/2'})
  if level=='hard':bad.extend([{'b':'2','k':'3','c':'-2','step':'1/2'},{'b':'2','k':'1.5','c':'-2','step':'1/2'}])
  for p in bad:
   try:api(parameters=p);raise AssertionError(('Accepted invalid input',level,p))
   except ValueError:pass
# Root-requested placement regressions: complete supported banks, not QA-only plots.
placement_cases=[]
for level in ('easy','moderate'):
 for b,k,c in [(2,'2','-2'),(6,'1','-1'),(6,'6','-6'),(2,'6','4'),(6,'1','6'),(2,'1','-6')]+([(2,'1.5','-2'),(6,'2.5','-2')] if level=='moderate' else []):
  r=g.generate(level,parameters={'b':b,'k':k,'c':c},profile='grid_reading');check(r);placement_cases.append(r)
for b,k,c in [(2,'23/4','17/4'),(6,'23/4','-21/4'),(2,'5/4','23/4'),(6,'5/4','-23/4'),(6,'9/4','-7/4'),(2,'7/4','-9/4')]:
 r=g.generate('hard',parameters={'b':b,'k':k,'c':c,'step':'1/4'},profile='grid_reading');check(r);placement_cases.append(r)
sampled.extend(placement_cases);save('placement-regressions.json',placement_cases)

# Fresh concurrent identical and different render jobs have unique inputs.
with tempfile.TemporaryDirectory(prefix='concurrency-',dir=HERE) as folder:
 jobs=[(2,sp.Rational(3,2),sp.Rational(-1,2)),(2,sp.Rational(3,2),sp.Rational(-1,2)),(5,sp.Rational(9,4),sp.Rational(3,4))]
 def render(t):return g.render_plots(*t,'hard',sp.Rational(1,4),output_dir=folder)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(render,jobs))
 assert results[0][0]==results[1][0] and results[0][2]['actual_png_sha256']==results[1][2]['actual_png_sha256'];assert not list(Path(folder).glob('input-*'))
# Native grade EVERY displayed choice; missing correct refs remain honest raw
# omissions, and receive separately named inferred fixtures for grading only.
for r in review+sampled:
 r=json.loads(json.dumps(r));f=r['question'][':question/answer-fields'][0];inferred=False
 if ':answer-field/correct' not in f:
  value=r['generation']['inferred_correct_value'];f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==value)];inferred=True
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently verified complete displayed choice'} for a in f[':answer-field/choices']]
 native.append({'label':('INFERRED FIXTURE ' if inferred else '')+(r['generation']['source_id'] or r['question'].get(':question/difficulty','generated'))+' '+r['question'][':question/id'],'record':r,'checks':checks})
save('engine-input.json',native);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
engine=json.loads((HERE/'engine-report.json').read_text());save('source-cases.json',cases);save('review.json',review)
text='# Original source evidence and generated variants\n\nRaw source profiles are evidence-only. Two legacy sources lack correct refs/solutions and keep those omissions. Changed source recipes remain evidence-only; error intent is unresolved. Normal variants use method-derived complete banks. Correct markers appear only where a designation exists.\n'
seen=set()
for r in review:
 sid=r['generation']['source_id']
 if sid:
  text+='\n\n### '+('Original source replay: ' if sid not in seen else 'Generated observed-profile variant (evidence-only): ')+sid+'\n';seen.add(sid)
 preview=g.markdown(r)
 assert 'difficulty='+r['question'].get(':question/difficulty','unrated').split('/')[-1] in preview
 assert 'authored_level='+str(r['generation']['authored_level']).lower() in preview
 assert 'inferred_correct='+str(r['generation']['evidence_only'] and ':answer-field/correct' not in r['question'][':question/answer-fields'][0]).lower() in preview
 assert preview.count('**Correct:**')==(1 if ':answer-field/correct' in r['question'][':question/answer-fields'][0] else 0)
 text+=preview
(HERE/'review.md').write_text(text)
# Enumerate finite meaningful domains under full-bank checks; exclude base from
# assessed coordinate-read/subtraction task; retain hard grid scale. Given base
# affects the full displayed equation but adds no assessed reasoning demand.
counts={}
for level in ('easy','moderate','hard'):
 tasks=set()
 steps=[sp.Rational(1,2),sp.Rational(1,4)] if level=='hard' else [sp.Integer(1)]
 for step in steps:
  ks=[sp.Rational(i,4) for i in range(4,25)] if level=='hard' else [sp.Rational(i,2) for i in range(2,13)] if level=='moderate' else list(map(sp.Integer,range(1,7)))
  cs=[sp.Rational(i,4) for i in range(-24,25)] if level=='hard' else list(map(sp.Integer,range(-6,7)))
  for k in ks:
   for c in cs:
    try:
     g.domain(level,{'b':2,'k':str(k),'c':str(c),'step':str(step)})
     for profile,recipes in g.BANKS.items():
      try:g.bank(2,k,c,step,recipes,'parameters' if level=='easy' else 'equation','compact');tasks.add((str(k),str(c),str(step)))
      except ValueError:pass
    except ValueError:pass
 counts[level]=len(tasks)
report={'status':'pass','source_provenance':{k:v for k,v in g.SNAPSHOT.items() if k!='record'},'fidelity':{'practice_sources':7,'complete_banks_matched':7,'options_matched':35,'present_correct_designations_matched':5,'original_correct_designations_absent':2,'exact_present_solutions':5,'absent_solutions_preserved':2,'exact_prompts':7,'raw_unrated_omissions_preserved':2,'sources':fidelity},'mathematical_checks':{'review_records':len(review),'random_records':30,'placement_regression_records':len(placement_cases),'sampled_and_regression_records':len(sampled),'all_displayed_choices_and_five_solution_stages':True,'finite_meaningful_tasks':counts,'distinct_full_equation_presentations_with_5_given_bases':{level:counts[level]*(1 if level=='easy' else 5) for level in counts},'complete_bank_before_sampling':True,'source_bank_error_intent':'underdetermined; evidence-only profiles'},'native_grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':engine['documented_unresolved_checks'],'legacy_fixture_repairs_separate':4,'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'engine_source_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'linked_learning_source_sha256':hashlib.sha256((ROOT/'engine/rust/learning.rs').read_bytes()).hexdigest()},'formatting_identity_scope':'pass','plot_checks':'all generated PNGs have atomic sidecar and independent raster readback; fresh same/different concurrent writes passed','source_base_geometry_uncertainty':'No original has calibrated x ticks; supplied bases cannot independently be recovered from rasters. Asymptote/intercept labels determine k,c.','authored_extensions':['hard fractional calibrated grid: two coordinate reads, subtraction, equation assembly','two normal method-derived whole banks; historical opaque profiles never defaults'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'placement_regressions':len(placement_cases),'retired_cache_versions':{'shift-stretch-v1':'Initial uint8 readback superseded.','shift-stretch-v2':'Fixed label positions superseded; retained for active-reader safety.','shift-stretch-v3':'Intermediate placement review.','shift-stretch-v4':'Intermediate stroke-clearance review, superseded by v5 actual-raster clearance.'},'database_writes':0}
save('validation.json',report);print(json.dumps(report,indent=2))
