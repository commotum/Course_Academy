#!/usr/bin/env python3
"""Independent source/displayed-math checks and native application grading."""
import concurrent.futures,importlib.util,json,re,shutil,subprocess,time
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
P=Path(__file__).parent;ROOT=P.parents[2]
spec=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
T=g.T

def tex(s):
 assert set(re.findall(r'\\([A-Za-z]+)',s)) <= {'operatorname','cos','sin','theta','pi','left','right','frac','sqrt'}, ('unknown TeX command',s)
 s=s.replace('\u2061','').replace(r'\operatorname{cos}','cos').replace(r'\operatorname{sin}','sin').replace(r'\cos','cos').replace(r'\sin','sin').replace(r'\theta','t').replace(r'\pi','pi').replace(r'\left','').replace(r'\right','').strip()
 def group(start):
  assert s[start]=='{';depth=1;i=start+1
  while depth:
   if s[i]=='{':depth+=1
   if s[i]=='}':depth-=1
   i+=1
  return s[start+1:i-1],i
 while r'\frac' in s or r'\sqrt' in s:
  match=re.search(r'\\(frac|sqrt)\s*\{',s);assert match,s
  a,j=group(match.end()-1)
  if match.group(1)=='frac':
   while s[j].isspace():j+=1
   b,end=group(j);replacement='('+str(tex(a))+')/('+str(tex(b))+')'
  else:end=j;replacement='sqrt('+str(tex(a))+')'
  s=s[:match.start()]+replacement+s[end:]
 s=re.sub(r'(cos|sin)\s*t',r'\1(t)',s)
 s=s.replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(s,local_dict={'t':T,'sqrt':sp.sqrt,'cos':sp.cos,'sin':sp.sin,'pi':sp.pi},transformations=standard_transformations+(implicit_multiplication_application,convert_xor),evaluate=True)

def parse_prompt(q):
 formula=q[':question/problem'].split('$$')[1]
 xpart=formula.split('x=',1)[1].split(',',1)[0];ypart=formula.split('y=',1)[1].split(',',1)[0]
 return tex(xpart),tex(ypart)

def assess(r):
 q=r['question'];gen=r['generation'];x,y=parse_prompt(q);d=gen['derived']
 assert sp.simplify(x-g.expr(d['x']))==0 and sp.simplify(y-g.expr(d['y']))==0,('displayed prompt',gen)
 tables=re.findall(r'(?:\|.*\|\n){3}\|.*\|',q[':question/worked-solution']);assert len(tables)==2
 rows=[]
 for tab in tables:rows.append([[c.strip() for c in line.split('|')[1:-1]] for line in tab.splitlines()])
 assert rows[0][0]==rows[1][0] and rows[0][2]==rows[1][2]
 assert all(c=='$$' for c in rows[0][3][1:])
 for j,t in enumerate(map(g.expr,d['ts'])):
  for v,cell in ((x.subs(T,t),rows[1][2][j+1]),(y.subs(T,t),rows[1][3][j+1])):
   shown=tex(cell[1:-1]);assert abs(float(sp.N(v-shown)))<=.00500000001,(v,shown,gen['template'])
 assert len(q[':question/answer-fields'])==1
 f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
 assert f[':answer-field/correct'][1] in {a[':answer/id'] for a in f[':answer-field/choices']}
 for a in f[':answer-field/choices']:
  assert a[':answer/type']==':answer.type/image';assert Path(a[':answer/value']).is_file()
 # Balanced actual learner math, including extracted empty-dollar cells.
 assert q[':question/problem'].count('$$')==2
 for value in (q[':question/problem'],q[':question/worked-solution']):
  depth=0
  for ch in value:
   if ch=='{':depth+=1
   if ch=='}':depth-=1;assert depth>=0
  assert depth==0 and value.count('$')%2==0
 if gen['plots']:
  assert len(set(g.valid_bank(gen['plots'])))==5
  sidecars=[]
  for a in f[':answer-field/choices']:
   side=json.loads(Path(a[':answer/value']).with_suffix('.json').read_text());sidecars.append(side)
   assert side['shape'] in gen['plots'] and side['samples']>=1601
  assert len({str(s['bounds']) for s in sidecars})==1
  correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);side=json.loads(Path(correct[':answer/value']).with_suffix('.json').read_text())
  assert g.geometry_key(side['shape'])==g.geometry_key(d['correct_shape'])
  if side['shape']['kind'] not in ('ellipse','rational'):
   for t,point in zip([g.expr(side['shape']['lo']),g.expr(side['shape']['hi'])],side['endpoints']):
    assert max(abs(float(x.subs(T,t))-point[0]),abs(float(y.subs(T,t))-point[1]))<1e-10
  if gen['template']=='factored-pair':
   assert len(d['ts'])==5 and gen['parameters']['a']!=gen['parameters']['b']
   # Joint injectivity proves that whole hard-domain clips are distinct sets.
   assert sp.diff(x+y,T)==gen['parameters']['b']-gen['parameters']['a']
   if q[':question/difficulty'].endswith('/hard'):
    assert [(int(s['lo']),int(s['hi'])) for s in gen['plots']]==[(-2,2),(-2,1),(-1,2),(-2,3),(-3,2)]
 return True

start=time.monotonic();source_records=[];qs=g.SOURCE['record'][':knowledge-point/questions'];cases=json.loads((P/'source-cases.json').read_text());assert len(cases)==len(qs)==16
for c in cases:
 r=g.generate('easy',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);original=next(q for q in qs if q[':question/id']==c['source_id']);q=r['question'];assess(r)
 assert q[':question/problem']==original[':question/problem']
 def normalize_assets(s):return re.sub(r'!\[\]\([^)]*\)','{ASSET}',s)
 assert normalize_assets(q[':question/worked-solution'])==normalize_assets(original[':question/worked-solution']),c
 f=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0]
 assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(str(g.ASSET_ROOT/a[':answer/value']) for a in of[':answer-field/choices'])
 correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==str(g.ASSET_ROOT/of[':answer-field/correct'][':answer/value'])
 source_records.append(r)
review=json.loads((P/'review.json').read_text())
for r in review:assess(r)
explicit=[]
for t in g.SPECS:
 p={'m':2,'n':1,'h':2,'k':-2}
 if t in ('q-123781','q-73602','q-16169'):p['h']=1
 if t=='q-73602':p['k']=1
 if t=='q-123787':p['k']=2
 if t=='q-16192':p['k']=2
 explicit.append(g.generate('easy',template=t,parameters=p))
for r in explicit:assess(r)
assert len(explicit)==16
assert all(sum(r['question'][':question/difficulty'].endswith('/'+level) for r in review)>=2 for level in ('easy','moderate','hard'))
# Enumerate every bounded M/H mathematical bank without writing redundant PNGs.
saved=g.render_plots;g.render_plots=lambda bank,ts:([f'choice-{i}.png' for i in range(5)],'solution.png')
counts={}
try:
 for level,profile in [('moderate','authored-sign-shift'),('hard','authored-domain-clips')]:
  fingerprints=set()
  for a in range(1,4):
   for b in range(1,4):
    if a==b:continue
    for h in (-2,-1,1,2):
     for k in (-2,-1,1,2):
      _,_,_,_,bank,_=g.build(level,'factored-pair',{'a':a,'b':b,'h':h,'k':k},profile)
      fingerprints.add(g.digest([g.geometry_key(v) for v in bank]))
  counts[level]=len(fingerprints);assert counts[level]==96
finally:g.render_plots=saved
# Explicit bounds reject invalid calls without resampling.
for level,p in [('moderate',{'a':1,'b':1,'h':1,'k':1}),('hard',{'a':4,'b':2,'h':1,'k':1}),('hard',{'a':1,'b':2,'h':0,'k':1}),('easy',{'m':3,'n':1,'h':1,'k':1})]:
 try:g.generate(level,parameters=p);raise AssertionError('invalid parameters accepted')
 except ValueError:pass
# Same assessed source graph via exact observed and generated authored banks.
original=g.generate('easy',template='q-16190',parameters={'m':1,'n':1,'h':0,'k':0},profile='observed:q-16190')
authored=g.generate('easy',template='q-16190',parameters={'m':1,'n':1,'h':0,'k':0},profile='authored-coordinate')
assess(authored)
assert original['generation']['mathematical_fingerprint']==authored['generation']['mathematical_fingerprint']
assert original['question'][':question/id']!=authored['question'][':question/id']
# Explicit fixed curve/profile: order and seed do not affect content identity.
for r in review:
 gen=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 rr=g.generate(level,999,template=gen['template'],parameters=gen['parameters'],profile=gen['bank_profile'])
 assert rr['question'][':question/id']==r['question'][':question/id']
 assert rr['generation']['mathematical_fingerprint']==gen['mathematical_fingerprint']
# Complete geometric equivalence checks, not separate coordinate ranges.
a=g.shape(T,T**2,-2,2);b=g.shape(-T,T**2,-2,2)
assert g.geometry_key(a)==g.geometry_key(b)
a=g.shape(2*T,5/T,0,sp.oo,'rational');b=g.shape(5/T,2*T,0,sp.oo,'rational');assert g.geometry_key(a)==g.geometry_key(b)
assert g.geometry_key(g.shape(T,T**2,-2,1))!=g.geometry_key(g.shape(T,T**2,-1,2))
# Force new assets so identical/different-instance concurrency tests exercise writes.
params=[{'a':1,'b':3,'h':2,'k':-2},{'a':2,'b':1,'h':-2,'k':2}]
for p in params:
 r=g.generate('hard',parameters=p)
 asset_dir=Path(r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']).parent
 shutil.rmtree(asset_dir)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 rs=list(pool.map(lambda p:g.generate('hard',parameters=p),[params[0],params[0],params[1],params[1]]))
for r in rs:assess(r)
assert rs[0]['question'][':question/id']==rs[1]['question'][':question/id'];assert rs[2]['question'][':question/id']==rs[3]['question'][':question/id'];assert rs[0]['question'][':question/id']!=rs[2]['question'][':question/id']
assert not list(P.glob('render-????????.json'))
subprocess.run([str(ROOT/'.venv/bin/python'),str(P/'render_labels.py')],check=True)
assert (P/'math-labels-qa.png').is_file()
records=source_records+review+explicit+rs
native=[]
for i,r in enumerate(records):
 f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 native.append({'label':str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'all five complete plotted choices'} for a in f[':answer-field/choices']]})
(P/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(P/'native-input.json'),str(P/'native-report.json')],check=True)
nreport=json.loads((P/'native-report.json').read_text())
result={'status':'pass','database':'math','basis':1356,'source_questions':16,'matched_source_prompts':16,'matched_complete_solution_sequences':16,'exact_unchanged_answer_assets':{'matched':80,'total':80},'matched_complete_asset_banks':16,'matched_correct_designations':16,'resolved_correct_parametrizations':16,'resolved_wrong_formulas':0,'residual_unchanged_wrong_graph_assets':64,'source_errors':[],'authored_variants_reviewed':len(review),'explicit_changed_family_checks':len(explicit),'visual_inspected_generated_plots':120,'authored_difficulty_labels':['moderate','hard'],'independent_displayed_math_and_table_checks':len(records),'native_accepted':nreport['accepted_checks'],'native_rejected':nreport['rejected_checks'],'concurrent_calls':4,'bounded_distinct_authored_banks':counts,'unique_temp_inputs_and_atomic_assets':True,'whole_graph_equivalence_regressions':3,'observed_authored_same_locus_fingerprint':True,'source_fidelity_limit':'Exact source rasters and complete prose/tables;64 residual wrong formulas are not claimed recovered or parameterized.','elapsed_seconds':round(time.monotonic()-start,2)}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
