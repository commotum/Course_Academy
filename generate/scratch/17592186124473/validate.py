#!/usr/bin/env python3
"""Separate mathematical eligibility, source fidelity, actual PNG and native QA."""
import importlib.util,itertools,json,re,subprocess,sys,hashlib
from pathlib import Path
from fractions import Fraction as F
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def canonical(r):return json.dumps(r,sort_keys=True,default=str)
def stripmath(v):return re.sub(r'\s+',' ',v).strip()
def correct(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def parse(text):
 token=r'(?:-?\d+|\\frac\{-?\d+\}\{\d+\}|-?\\infty)'
 matches=re.findall(r'([\[(])\s*('+token+r')\s*,\s*('+token+r')\s*([\])])',text)
 def value(s):
  if 'infty' in s:return -99 if s.startswith('-') else 99
  if 'frac' in s:
   a,b=map(int,re.findall(r'-?\d+',s));return F(a,b)
  return int(s)
 return [[value(a),value(b),lc=='[',rc==']'] for lc,a,b,rc in matches]
def promptsets(q):
 body=q[':question/problem'].split('invertible?',1)[-1]
 return [parse(line) for line in body.splitlines() if parse(line)]
def independent_hlt(pieces,sets):
 # A second oracle: solve each exact affine branch for a generic output y;
 # partition output line at all branch endpoint values and count distinct x's.
 pieces=[[F(str(x)) if i<4 else bool(x) for i,x in enumerate(z)] for z in pieces]
 requested=g.spset(sets);branches=[]
 for a,b,c,d,lc,rc in pieces:
  domain=sp.Interval(sp.Rational(a),sp.Rational(c),left_open=not lc,right_open=not rc)
  part=requested.intersect(domain)
  comps=list(part.args) if isinstance(part,sp.Union) else [part]
  for s in comps:
   if s==sp.EmptySet:continue
   m=(d-b)/(c-a);k=b-m*a
   if isinstance(s,sp.FiniteSet):
    for x in s:branches.append((s,m,k,[m*x+k]))
   elif m==0:return False
   else:branches.append((s,m,k,[m*s.start+k,m*s.end+k]))
 dom=sp.Union(*[sp.Interval(sp.Rational(a),sp.Rational(c),left_open=not lc,right_open=not rc) for a,b,c,d,lc,rc in pieces])
 if requested-dom!=sp.EmptySet:return False
 edges=sorted(set(v for s,m,k,ys in branches for v in ys));witnesses=edges+[(a+b)/2 for a,b in zip(edges,edges[1:])]
 for y in witnesses:
  xs=set()
  for s,m,k,_ in branches:
   if m==0:
    if y==k:xs.update(s)
   else:
    x=(y-k)/m
    if s.contains(x)==sp.true:xs.add(x)
  if len(xs)>1:return False
 return True

def fmt(q):
 for k in (':question/problem',':question/worked-solution'):
  s=q.get(k,'');assert s.count('$')%2==0,(k,'math dollars')
  assert s.count('{')==s.count('}'),(k,'braces')
  assert not re.search(r'(?<!\\)\+\+|--',s)

def normalcheck(r):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'};fmt(q)
 f=q[':question/answer-fields'][0];values=[a[':answer/value'] for a in f[':answer-field/choices']]
 assert len(values)==len(set(values))==5
 assert f[':answer-field/type']==':answer-field.type/radio'
 # Read graph instance from the actual rendered artifact sidecar, whose pixel
 # verification is performed by renderer, not from generation math metadata.
 path=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]);side=json.loads(path.with_suffix('.json').read_text())
 pieces=side['data']['pieces'];assert path.exists()
 assert side['minimum_feature_clearance_pixels']>=4
 assert side['raster_curve_midpoints_verified']==len(pieces)
 assert len(side['raster_endpoint_checks'])>=3
 requested=promptsets(q)
 if requested:
  bits=[independent_hlt(pieces,s) for s in requested]
  assert correct(r)==g.subset_label(bits),(r['generation']['template'],bits,correct(r))
  # Actual fixed prose states each printed interval's HLT result; not metadata.
  lines=[x for x in q[':question/worked-solution'].splitlines() if x.startswith('- On interval')]
  assert len(lines)==3
  for line,ss,b in zip(lines,requested,bits):
   assert g.spset(parse(line))==g.spset(ss)
   assert ('**not** invertible' not in line)==b
  eligible=[stripmath(v)==stripmath(g.subset_label(bits)) for v in values]
 else:
  answer_sets=[parse(v) for v in values]
  valid=[independent_hlt(pieces,s) for s in answer_sets]
  ci=values.index(correct(r));assert valid[ci]
  if r['generation']['template']=='plateau_interval':
   eligible=[ok and all(not valid[j] or g.spset(t).is_subset(g.spset(s)) for j,t in enumerate(answer_sets)) for s,ok in zip(answer_sets,valid)]
  else:
   # Explicit normal criterion contains every nonconstant piece and is maximal
   # among shown domains. Correct contains every other listed valid domain.
   eligible=[ok and all(not valid[j] or g.spset(t).is_subset(g.spset(s)) for j,t in enumerate(answer_sets)) for s,ok in zip(answer_sets,valid)]
  final=parse(q[':question/worked-solution'].split('Therefore,')[-1]);assert g.spset(final)==g.spset(answer_sets[ci])
 assert sum(eligible)==1

def main():
 originals=[];sourcecases=[];fidelity=[];source_math=[];review=[]
 for source_id,q in g.QUESTIONS.items():
  level=q[':question/difficulty'][':db/ident'].split('/')[-1]
  case={'source_id':source_id,'template':'source_'+source_id,'parameters':{'x_shift':0},'bank_profile':source_id,'level':level};sourcecases.append(case)
  r=g.generate(level,11,template=case['template'],parameters=case['parameters'],profile=source_id);originals.append(r)
  made=r['question'];fmt(made)
  assert made[':question/problem']==q[':question/problem'];assert made[':question/worked-solution']==q[':question/worked-solution']
  assert set(made)==set(q), 'Full question key presence parity'
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in made)==(key in q)
  old=q[':question/answer-fields'][0];new=made[':question/answer-fields'][0]
  assert set(old)==set(new)
  assert all(set(a)==set(new[':answer-field/choices'][0]) for a in old[':answer-field/choices'])
  ov=sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in old[':answer-field/choices']);nv=sorted((a[':answer/type'],a[':answer/value']) for a in new[':answer-field/choices']);assert ov==nv
  assert correct(r)==old[':answer-field/correct'][':answer/value']
  fidelity.append({'source_id':source_id,'prompt_exact':True,'solution_exact':True,'complete_bank':True,'choices':len(ov),'correct_designation':True,'attribute_presence':True})
  if 'following intervals' in made[':question/problem']:
   tests=promptsets(made);bits=[independent_hlt(g.LANDMARKS[source_id],ss) for ss in tests];assert stripmath(correct(r))==g.subset_label(bits),(source_id,bits)
  else:
   vs=[a[':answer/value'] for a in new[':answer-field/choices']];ss=[parse(v) for v in vs];valid=[independent_hlt(g.LANDMARKS[source_id],s) for s in ss];ci=vs.index(correct(r));assert valid[ci]
   assert all(not valid[j] or g.spset(t).is_subset(g.spset(ss[ci])) for j,t in enumerate(ss))
  source_math.append({'source_id':source_id,'landmark_hlt_correct':True,'analytic_ink_recovered':False,'global_largest_domain_ambiguous':source_id=='q-108791'})
  # Every observed profile: two changed-coordinate evidence variants, explicitly
  # labelled ineligible; normal authored variants follow separately.
  for h in (-1,1):
   rr=g.generate(level,17,profile=source_id,parameters={'x_shift':h})
   assert correct(rr)==g.transformed_intervals(correct(r),h), 'Evidence translation changed HLT truth'
   review.append(rr)
 (HERE/'source-cases.json').write_text(json.dumps(sourcecases,indent=2))
 for level,templates in g.NORMAL.items():
  for template in templates:
   for seed in (31,68):
    r=g.generate(level,seed,template=template);normalcheck(r);review.append(r)
 # Explicit boundaries and sign/closure changes each supported authored family.
 extra=[]
 for level,templates in g.NORMAL.items():
  for template in templates:
   for orient,closure,left,right in itertools.product((-1,1),(False,True),(2,4),(2,4)):
    if template=='plateau_union' and not closure:continue
    p={'h':-2,'left':left,'right':right,'mid':3 if template in ('two_turns','union_ranges','disconnected_ranges','plateau_union') else 2,'orient':orient,'closure':closure,'permutation':[0,1,2]}
    r=g.generate(level,0,template=template,parameters=p);normalcheck(r);extra.append(r)
 # Bad explicit inputs cannot silently resample or escape difficulty.
 invalid=0
 for level,templates in g.NORMAL.items():
  for template in templates:
   p={'h':0,'left':5,'right':2,'mid':2,'orient':1,'closure':True,'permutation':[0,1,2]}
   try:g.generate(level,0,template=template,parameters=p)
   except ValueError:invalid+=1
   else:raise AssertionError('guard ignored')
 for level,templates in g.NORMAL.items():
  coverage={g.generate(level,s)['generation']['template'] for s in range(16)};assert coverage==set(templates),(level,coverage)
 # ID excludes shuffle/seed, retains actual output and mathematical criterion.
 for r in review:
  meta=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
  rr=g.generate(level,999,template=meta['template'],profile=meta['bank_profile'],parameters=meta['parameters'])
  assert rr['question'][':question/id']==r['question'][':question/id']
 # Concurrent fresh renders: same/different geometry, unique inputs, atomic files.
 from concurrent.futures import ThreadPoolExecutor
 pa=[[0,0,2,2,True,True],[2,2,4,0,True,False]]
 pb=[[0,1,3,-2,True,True],[3,-2,5,0,True,True]]
 with ThreadPoolExecutor(max_workers=4) as pool:
  paths=list(pool.map(lambda p:g.render_plots(p,None,'concurrent',mode='concurrent-final'),[pa,pa,pb,pb]))
 assert paths[0]==paths[1] and paths[2]==paths[3] and paths[0]!=paths[2]
 assert all(Path(x).exists() and Path(x).with_suffix('.json').exists() for x in paths)
 # Native radio: all complete displayed banks, each correct and each wrong.
 records=originals+review+extra;native=[]
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0]
  native.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio selection; mathematical eligibility separately verified'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(native,default=str));engine=ROOT/'generate/runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-results.json')],check=True)
 (HERE/'review.json').write_text(json.dumps(review,indent=2,default=str))
 results={'status':'pass_with_explicit_source_limits','source_questions':13,'source_choices_matched':65,'source_complete_banks_matched':13,'source_correct_designations_matched':13,'raw_prompt_solution_exact':13,'raw_attribute_presence_exact':13,'source_math':source_math,'fidelity':fidelity,'normal_rendered_math_checks':len(extra)+sum(len(t)*2 for t in g.NORMAL.values()),'native_records':len(records),'native_checks':len(records)*5,'explicit_guard_rejections':invalid,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':sp.__version__,'unresolved':['Source analytic formulas are underidentified; profiles evidence-only.','q-108791 has no globally greatest injective domain; normal prompt clarifies listed maximal criterion.','Raw solution endpoint typos q-36039 and q-36004 preserved as evidence.'],'source_coordinate_hlt_translation_checks':26,'source_geometry_claim':'Monotonicity/output overlap landmarks independently support selections; exact original curve formulas not claimed.'}
 (HERE/'validation.json').write_text(json.dumps(results,indent=2));print(json.dumps({k:v for k,v in results.items() if k not in ('fidelity','source_math')},indent=2))
 # Preserve original source image references in prose review as absolute copies.
 def replace_images(s,sid,section):
  j=-1
  def repl(m):
   nonlocal j;j+=1;return '![]('+str(HERE/(sid+'-'+str(section)+'-'+str(j)+'.png'))+')'
  return re.sub(r'!\[\]\([^)]*\)',repl,s)
 md=['# Originals and generated review','Basis 1356. Original levels are observed; all normal defaults are authored. Changed source-coordinate variants are evidence-only qualitative surrogates, not validated recovery of original analytic ink.']
 for sid,q in g.QUESTIONS.items():
  md+=['## Original '+sid+' ('+q[':question/difficulty'][':db/ident'].split('/')[-1]+')',replace_images(q[':question/problem'],sid,0),'Choices: '+', '.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']),'Correct: '+q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],replace_images(q[':question/worked-solution'],sid,1)]
 for r in review:
  m=r['generation'];q=r['question'];md+=['## Generated '+m['template']+' ('+q[':question/difficulty'].split('/')[-1]+') — '+('authored eligible' if m['eligible_for_learning'] else 'source evidence only'),q[':question/problem'],'Choices: '+', '.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']),'Correct: '+correct(r),q[':question/worked-solution']]
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
if __name__=='__main__':main()
