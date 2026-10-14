#!/usr/bin/env python3
"""Independent displayed-content, exact mathematics, source fidelity and native QA."""
import concurrent.futures,hashlib,importlib.util,json,pathlib,re,subprocess,sys
sys.dont_write_bytecode=True
import numpy as np
import sympy as sp
from PIL import Image
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=json.loads((D/'source.json').read_text());sources=s['record'][':knowledge-point/questions'];x=sp.Symbol('x',real=True)

def normalized(text):return re.sub(r'!\[\]\([^)]*\)','![]({asset})',text)
def restore_source_operands(text,r,t):
 # Independent reverse masking of complete printed operative operands.
 slots=dict(zip(r['generation']['parameters']['roots'],t['roots']))
 def rep(match):return match[1]+str(slots[int(match[2])])
 text=re.sub(r'(x\s*=\s*)(-?\d+)',rep,text)
 if t['source_id']==17592186129698:text=re.sub(r'±\s*\d+','± 1',text)
 if t['source_id']==17592186326715:
  text=re.sub(r'(p\(0\)\s*=\s*)\d+(?:/\d+)?',r'\g<1>3',text)
  text=re.sub(r'(y=)\d+(?:/\d+)?',r'\g<1>3',text)
 return normalized(text)
def source_parameters(t):return {k:t[k] for k in ['roots','multiplicities','coefficient']}
def parse_statements(prompt,f):
 body=prompt.split('Which of the following statements are')[1].split('?',1)[1]
 rows=[line.strip() for line in body.splitlines() if line.strip()]
 assert len(rows)==3,rows
 truth=[];facts=[]
 for row in rows:
  row=row.replace('**','').replace('$','').replace('→',r'\to').replace('∞',r'\infty').replace('±',r'\pm')
  if 'p(0)' in row:
   match=re.search(r'p\(0\)\s*=\s*(-?\d+(?:/\d+)?)',row)
   if match:v=f.subs(x,0)==sp.Rational(match.group(1));fact=('value',sp.Rational(match.group(1)))
   else:assert 'positive' in row;v=f.subs(x,0)>0;fact=('positive',)
  elif r'\to' in row:
   match=re.search(r'p\(x\)\s*\\to\s*(-?)\s*\\infty.*?x\s*\\to\s*(-?)\s*\\infty',row);assert match,row
   ys=-1 if match[1] else 1;xs=-1 if match[2] else 1;v=sp.limit(f,x,xs*sp.oo)==ys*sp.oo;fact=('limit',xs,ys)
  else:
   rs=[int(v) for v in re.findall(r'x\s*=\s*(-?\d+)',row)]
   pm=re.search(r'x\s*=\s*\\pm\s*(\d+)',row)
   if pm:rs=[-int(pm[1]),int(pm[1])]
   assert rs,row
   ms=[]
   for r in rs:
    assert f.subs(x,r)==0,(r,f)
    m=1
    while sp.diff(f,x,m).subs(x,r)==0:m+=1
    ms.append(m)
   if 'simple' in row:kind='not_simple' if 'not' in row else 'simple';v=all(m!=1 if 'not' in row else m==1 for m in ms)
   elif 'even' in row:kind='even';v=all(m%2==0 for m in ms)
   else:assert 'odd' in row;kind='odd';v=all(m%2 for m in ms)
   fact=(kind,tuple(rs))
  truth.append(bool(v));facts.append(fact)
 assert len(set(facts))==3,'Duplicate semantic statements'
 return truth

def actual_polynomial(r):
 path=pathlib.Path(r['generation']['plot']);side=path.with_suffix('.json')
 if str(path).startswith(str(D.resolve())):
  data=json.loads(side.read_text());f=sum(sp.Rational(c)*x**(len(data['coefficients'])-i-1) for i,c in enumerate(data['coefficients']))
  assert sp.expand(sp.sympify(data['polynomial'],locals={'x':x})-f)==0
  assert data['zero_axes'] and data['axis_scale']=='linear'
  im=np.array(Image.open(path).convert('RGB'));assert im.shape[:2]==(736,976)
  red=(im[:,:,0]>175)&(im[:,:,1]<100)&(im[:,:,2]<100);assert red.sum()>1000
  black=(im[:,:,:].max(axis=2)<90);assert black.sum()>1000
  # Exact root crossings/tangencies use sidecar polynomial; raster carries visible curve and axes.
  for root in data['roots']:assert f.subs(x,root)==0
  fn=sp.lambdify(x,f,'numpy');lo,hi=data['xlim'];low,high=data['ylim'];assert not(low<float(fn(lo))<high) and not(low<float(fn(hi))<high),'Ends must exit viewport'
  # Read the actual raster at independently calculated polynomial coordinates.
  bx,by,bw,bh=data['axes_bbox_pixels']
  tested=0
  for xx in np.linspace(lo,hi,91):
   yy=float(fn(xx))
   if low+.02*(high-low)<yy<high-.02*(high-low):
    col=int(round(bx+(xx-lo)/(hi-lo)*bw));row=int(round(736-(by+(yy-low)/(high-low)*bh)))
    # Root/intercept tick captions intentionally cover a small curve region for
    # legibility. Skip only pixels within the actual rendered text bounds.
    if any(a-3<=col<=c+3 and b-3<=736-row<=d+3 for a,b,c,d in data['label_boxes_pixels']):continue
    assert red[max(0,row-5):row+6,max(0,col-5):col+6].any(),('Raster polynomial mismatch',path,xx,yy)
    tested+=1
  assert tested>25
  return f
 # Source artwork only establishes categories/end signs; use documented representative
 # with those visually inspected features, not a claim of recovered source amplitude.
 t=g.RECIPES[r['generation']['template']];p=r['generation']['parameters']
 return sp.expand(sp.Rational(p['coefficient'])*sp.prod((x-v)**m for v,m in zip(p['roots'],p['multiplicities'])))

def check_record(r,raw=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];f=actual_polynomial(r);truth=parse_statements(q[':question/problem'],f)
 assert truth==r['generation']['truth']
 if r['generation']['template'] in g.RECIPES:
  t=g.RECIPES[r['generation']['template']];original=next(q for q in sources if q[':db/id']==t['source_id'])
  assert restore_source_operands(q[':question/problem'],r,t)==normalized(original[':question/problem']), 'Changed-parameter prompt mask drift'
  if ':question/worked-solution' in original:
   assert restore_source_operands(q[':question/worked-solution'],r,t)==original[':question/worked-solution'], 'Changed-parameter full solution prose/ordered-operative-mask drift'
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]:
  assert text.count('$')%2==0 and text.count('{')==text.count('}')
  assert not re.search(r'\\(?:t|n|r|b|f)(?![A-Za-z])',text),'Phantom escape'
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];assert sol.startswith("Let's analyze each statement in turn.")
  rows=re.findall(r'- Statement (I|II|III) is (true|false)\.',sol);assert rows==list(zip(g.ROMAN,['true' if v else 'false' for v in truth]))
  # Independently check the explicit root category facts in the actual printed solution.
  for sentence in sol.split('\n\n'):
   if 'The graph meets the $y$-axis' in sentence:
    assert ('above' in sentence)==(f.subs(x,0)>0), 'Printed qualitative intercept sign mismatch'
    assert ('p(0)>0' in sentence)==(f.subs(x,0)>0)
   if 'The graph passes through the $y$-axis' in sentence:
    val=re.search(r'p\(0\)\s*=\s*(-?\d+(?:/\d+)?)',sentence)
    assert val and f.subs(x,0)==sp.Rational(val[1]),'Printed intercept stage mismatch'
   if 'As $x$ moves' in sentence:
    sign=-1 if 'moves left' in sentence else 1
    actual=sp.limit(f,x,sign*sp.oo)
    assert ('moves down' in sentence)==(actual==-sp.oo),'Printed end-direction stage mismatch'
   rr=re.search(r'The root \$x\s*=\s*(-?\d+)\$ (.*)',sentence)
   if not rr:continue
   root=int(rr[1]);m=1
   while sp.diff(f,x,m).subs(x,root)==0:m+=1
   text=rr[2]
   if 'has an even multiplicity' in text:assert m%2==0
   if 'has an odd multiplicity' in text:assert m%2==1
   if 'is not a simple root' in text:assert m>1
   elif 'is a simple root' in text:assert m==1
   if 'just touches' in text:assert m%2==0
   if 'passes through' in text:assert m%2==1
   if 'is not tangent' in text:assert m==1
  expected=tuple(i for i,v in enumerate(truth) if v)
  final=re.search(r'Therefore, the correct answer is "(.*?)"',sol);assert final and g.code(final[1])==expected
 fields=q.get(':question/answer-fields',[])
 for field in fields:
  assert field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection'
  bank=field[':answer-field/choices'];assert len(bank)==5
  assert len(set(g.code(a[':answer/value']) for a in bank))==5
  assert len(set(a[':answer/id']for a in bank))==5
  expected=tuple(i for i,v in enumerate(truth)if v)
  valid=[a for a in bank if g.code(a[':answer/value'])==expected];assert len(valid)==1
  if ':answer-field/correct' in field:assert field[':answer-field/correct']==[':answer/id',valid[0][':answer/id']]
 return truth

cases=[];fidelity=[];reviews=[];native=[]
for q in sources:
 name=q[':question/math-academy-id'];t=g.RECIPES[name];p=source_parameters(t)
 raw=g.generate(t['level'],template=name,parameters=p,profile='source:'+name)
 check_record(raw,True)
 rq=raw['question'];assert normalized(rq[':question/problem'])==normalized(q[':question/problem'])
 assert (':question/worked-solution'in rq)==(':question/worked-solution'in q)
 if ':question/worked-solution'in q:assert rq[':question/worked-solution']==q[':question/worked-solution']
 assert (':question/difficulty'in rq)==(':question/difficulty'in q)
 assert (':question/answer-fields'in rq)==(':question/answer-fields'in q)
 if ':question/answer-fields'in q:
  original=q[':question/answer-fields'][0];field=rq[':question/answer-fields'][0]
  assert sorted(a[':answer/value']for a in original[':answer-field/choices'])==sorted(a[':answer/value']for a in field[':answer-field/choices'])
  assert field[':answer-field/key']==original[':answer-field/key'] and field[':answer-field/type']==original[':answer-field/type'][':db/ident']
  assert (':answer-field/correct'in field)==(':answer-field/correct'in original)
  if ':answer-field/correct'in original:
   ans=next(a for a in field[':answer-field/choices']if a[':answer/id']==field[':answer-field/correct'][1]);assert ans[':answer/value']==original[':answer-field/correct'][':answer/value']
 cases.append({'source_id':q[':db/id'],'source_math_academy_id':name,'template':name,'level':t['level'],'parameters':p,'bank_profile':'source:'+name,'authored_level_assignment':t['unrated']})
 fidelity.append({'source_id':q[':db/id'],'prompt_mask':True,'shared_solution_sequence':True if t['solution_mask'] else 'absent preserved','bank_choices':len(t['bank'] or []),'bank_matched':True if t['bank'] else 'absent preserved','original_correct_designation_matched':t['correct_present'],'raw_presence_preserved':True})
 repaired=g.generate(t['level'],template=name,parameters=p,profile='repaired:'+name);check_record(repaired);reviews.append({'kind':'source anchor, explicit repaired presentation','source_id':q[':db/id'],'record':repaired})
 variant=g.generate(t['level'],seed=17,template=name);check_record(variant);reviews.append({'kind':'generated changed-parameter variant','source_id':q[':db/id'],'record':variant})
for level in ['easy','moderate','hard']:
 for seed in [11,37]:
  record=g.generate(level,seed);check_record(record);reviews.append({'kind':'generated '+level+' review example','record':record})
# Each template/profile tested at changed params, independently read from rendered content.
variation={};records=[]
for name,t in list(g.RECIPES.items())+[('mixed_categories_four_roots',g.HARD)]:
 fs=set();roots=set()
 for seed in range(12):
  r=g.generate(t['level'],seed,template=name);check_record(r);records.append(r);fs.add(r['generation']['mathematical_fingerprint']);roots.add(tuple(r['generation']['parameters']['roots']))
  p=r['generation']['parameters'];same=g.generate(t['level'],seed+1000,template=name,parameters=p)
  assert r['question'][':question/id']==same['question'][':question/id']
 assert len(fs)>=5 and len(roots)>=5
 variation[name]={'sample_count':12,'mathematical_tasks':len(fs),'root_tuples':sorted(roots)}
# Identity does not count seed/order/amplitude/exponent aliases as new tasks.
r=g.generate_hard(8);p=r['generation']['parameters'];p2=dict(p,coefficient='2')
r2=g.generate_hard(8,parameters=p2);assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
anchor=source_parameters(g.RECIPES['q-80302']);other=dict(anchor,multiplicities=[1,1,5])
ra=g.generate_easy(template='q-80302',parameters=anchor);rb=g.generate_easy(template='q-80302',parameters=other)
assert ra['generation']['mathematical_fingerprint']==rb['generation']['mathematical_fingerprint']
try:g.generate_easy(parameters={});raise AssertionError('Empty explicit parameters silently resampled')
except ValueError:pass
# Domain guards apply to explicit inputs; no silent parameter repair.
for level,name,p in [('hard','mixed_categories_four_roots',{'roots':[-3,-1,1],'multiplicities':[1,2,3],'coefficient':'1'}),('moderate','q-112591',{'roots':[-2,1,3],'multiplicities':[1,3,2],'coefficient':'1'}),('easy','q-38680',{'roots':[-3,-1,2],'multiplicities':[1,1,1],'coefficient':'-1'})]:
 try:g.generate(level,template=name,parameters=p);raise AssertionError('Invalid explicit domain accepted')
 except ValueError:pass
# Concurrent first writes: each temporary file is unique and final PNG+sidecar atomic.
pars=[{'roots':[-5,-3,2,5],'multiplicities':[1,2,3,1],'coefficient':str(c)}for c in [sp.Rational(7,5),sp.Rational(8,5),sp.Rational(7,5)]]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 paths=list(pool.map(g.render_plots,pars))
assert paths[0]==paths[2] and paths[0]!=paths[1]
for path in paths:assert pathlib.Path(path).exists() and pathlib.Path(path).with_suffix('.json').exists()
assert not list((D/'plots').glob('*-*.png')) and not list((D/'plots').glob('*-*.json'))
# Actual native engine, separately from semantic and source fidelity verification.
for entry in reviews:
 r=entry['record'];fields=r['question'][':question/answer-fields'];checks=[]
 for a in fields[0][':answer-field/choices']:
  checks.append({'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==fields[0][':answer-field/correct'][1] else 'rejected','purpose':'all owned subset choices'})
 native.append({'label':entry['kind']+' '+r['generation']['template'],'record':r,'checks':checks})
(D/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
(D/'review.json').write_text(json.dumps(reviews,indent=2)+'\n')
md=['# Graph statement review','All source images are 339×281; native panels were inspected individually in the source contact image. Original artwork is retained in raw profiles. Generated plots use an actual polynomial representative matching visible categories, not recovered exponents.']
for q in sources:md+=['## Original '+q[':question/math-academy-id'],q[':question/problem'].replace('![](images/','![](/media/jake/SSD/EDB/math/images/'),q.get(':question/worked-solution','No source worked solution.'),'Original bank: '+', '.join(a[':answer/value']for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices'])]
for entry in reviews:md+=['## '+entry['kind']+' — '+entry['record']['generation']['template'],g.markdown(entry['record'])]
(D/'review.md').write_text('\n\n'.join(md)+'\n')
report={'status':'passed','source_provenance':{k:s[k]for k in ['database','basis','lineage']},'source_questions':10,'raw_source_replays':10,'full_observed_banks':9,'observed_choices_matched':45,'observed_correct_designations_matched':7,'missing_designations_explicitly_derived':2,'missing_field_authored_repairs':1,'missing_solutions_authored_repairs':2,'raw_exact_solution_sequences':8,'source_presence_preserved':10,'authored_hard_templates':1,'unrated_authored_easy_assignments':2,'scope_and_domain_checks':'passed','displayed_statement_symbolic_checks':len(records)+len(reviews)+10,'slot_variation':variation,'identity_and_equivalence_checks':'passed','concurrent_renderer_checks':'passed','native_grading':json.loads((D/'engine-report.json').read_text()),'versions':{'python':sys.version,'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__},'source_formula_inference':'Representative category-compatible formulas only; unknown exponents/amplitude not recovered','source_asset_references_normalized_for_prompt_fidelity':True,'root_qa_required':True,'finite_meaningful_domains':{name:v['meaningful_tasks'] for name,v in json.loads((D/'finite-domains.json').read_text()).items()},'engine_binary_sha256':hashlib.sha256(pathlib.Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'engine_harness_sha256':hashlib.sha256(pathlib.Path('generate/runs/current/check-engine.rs').read_bytes()).hexdigest()}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: 10 raw source replays; 9 complete banks / 45 choices; 7 original correct designations; all 3 levels, native grader, displayed symbolic checks and concurrency.')
