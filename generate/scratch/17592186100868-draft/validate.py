"""Independent validation of actual printed matrices, rows, banks and native grading.
Run from repository root with PYTHONDONTWRITEBYTECODE=1 .venv/bin/python .../validate.py.
No database access. All outputs remain in this private evidence directory.
"""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,re,subprocess,platform
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;REPO=D.parents[2]
spec=importlib.util.spec_from_file_location('kp100868_draft',D.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
def save(name,obj):(D/name).write_text(json.dumps(obj,indent=2)+'\n')
def parse(t):
 t=re.sub(r'\\[,!; ]','',t).replace(r'\cdot','*').replace('{','(').replace('}',')').replace('^','**').replace('−','-')
 t=re.sub(r'(?<=[0-9a-z])(?=[a-z])','*',t)
 return parse_expr(t,local_dict={c:S.Symbol(c) for c in 'abcdefghijklmnopqrstuvwxyz'},transformations=standard_transformations+(implicit_multiplication_application,))
def equal(a,b):return S.expand(a-b)==0

def matrices(text):
 result=[];end=0
 for m in re.finditer(r'\\begin\{bmatrix\}',text):
  if m.start()<end:continue
  a,b,end=G.mf.environment(text,m.start());body=text[a:b]
  if body.startswith(r'\begin{aligned}'):
   aa,bb,_=G.mf.environment(body,0);rows=[[''.join(row)] for row in G.mf.cells(body[aa:bb])]
  else:rows=G.mf.cells(body)
  result.append(rows)
 return result

def mask(text):
 result='';start=0
 for m in re.finditer(r'\\begin\{bmatrix\}',text):
  if m.start()<start:continue
  _,_,end=G.mf.environment(text,m.start());result+=text[start:m.start()]+'@@M@@';start=end
 return result+text[start:]

def terms(text):
 text=re.sub(r'\\[,!; ]','',text);out=[];depth=0;start=0
 for i,c in enumerate(text):
  if c in '({':depth+=1
  elif c in ')}':depth-=1
  elif c in '+-' and depth==0 and i>start:out.append(text[start:i]);start=i
 out.append(text[start:]);return out

def field_value(f):
 aid=f[':answer-field/correct'][1];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def value(v):
 m=matrices(v);return tuple(parse(c) for row in m[0] for c in row) if m else (parse(v),)
def vequal(a,b):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))

math_counts={'records':0,'ordered_product_terms':0,'ordered_evaluated_terms':0,'bank_options':0,'final_rows':0,'source_solution_stage_checks':0}
def check(r):
 G.guarded(r);G.mf.validate_generated_record(r);assert r['knowledge_point']==G.KP
 q=r['question'];p=r['generation'];t=G.TEMPLATES[p['template']]
 assert q[':question/difficulty']==':question.difficulty/'+t['level']
 mats=matrices(q[':question/problem']);assert len(mats)==2
 M=[[parse(c) for c in row] for row in mats[0]];V=[[parse(c) for c in row] for row in mats[1]]
 n=len(M);assert len(V)==len(M[0]) and all(len(row)==1 for row in V)
 def maxcoeff(es):
  vals=[]
  for e in es:
   syms=sorted(e.free_symbols,key=str);vals.extend(S.Poly(S.expand(e),*syms).coeffs() if syms else [e])
  return max([abs(x) for x in vals]+[0])
 caps=G.WORKLOAD[t['level']]
 assert maxcoeff([c for row in M for c in row]+[row[0] for row in V])<=caps['factor']
 assert maxcoeff([a*b[0] for row in M for a,b in zip(row,V)])<=caps['product']
 out=[S.expand(sum(a*b[0] for a,b in zip(row,V))) for row in M]
 assert maxcoeff(out)<=caps['collected']
 sol=matrices(q[':question/worked-solution']);assert len(sol)==(len(t['solution_matrices']) or 4)
 assert [[parse(c) for c in row] for row in sol[0]]==M and [[parse(c) for c in row] for row in sol[1]]==V
 assert len(sol[2])==n and len(sol[-1])==n
 for i,row in enumerate(sol[2]):
  assert len(row)==1;parts=terms(row[0]);assert len(parts)==len(V)
  for j,term in enumerate(parts):
   term=term.removeprefix('+');factors=term.split(r'\cdot');assert len(factors)==2
   assert equal(parse(factors[0]),M[i][j]) and equal(parse(factors[1]),V[j][0]);math_counts['ordered_product_terms']+=1
 if len(sol)==5:
  for i,row in enumerate(sol[3]):
   summands=terms(row[0]);assert len(summands)==len(V)
   for j,term in enumerate(summands):assert equal(parse(term),M[i][j]*V[j][0]);math_counts['ordered_evaluated_terms']+=1
 for i,row in enumerate(sol[-1]):assert len(row)==1 and equal(parse(row[0]),out[i]),(p['template'],p['parameters'],row,out[i]);math_counts['final_rows']+=1
 for f,tf in zip(q[':question/answer-fields'],t['fields']):
  assert f[':answer-field/key']==tf['key'] and f[':answer-field/type']==':answer-field.type/'+tf['type']
  assert len(f[':answer-field/choices'])==len(tf['choices'])
  keys=[a[':answer/id'] for a in f[':answer-field/choices']];assert len(keys)==len(set(keys))
  bank=[value(a[':answer/value']) for a in f[':answer-field/choices']]
  assert maxcoeff([x for row in bank for x in row])<=caps['collected']
  assert all(not vequal(x,y) for j,x in enumerate(bank) for y in bank[:j])
  expected=tuple(out) if tf['type']=='radio' else (out[int(tf['key'].split('-')[-1])-1],)
  assert vequal(value(field_value(f)),expected)
  if tf['type']=='blank':assert '{{'+tf['key']+'}}' in q[':question/problem']
  math_counts['bank_options']+=len(bank)
 assert len(q[':question/answer-fields'])==len(t['fields'])
 math_counts['records']+=1
 return out

source_wrapper=json.loads((D/'source.json').read_text());assert source_wrapper['database']=='math' and source_wrapper['basis']==2275 and source_wrapper['lineage']=='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';assert (D/'source.json').read_bytes()==(REPO/'generate/runs/current/refresh-2026-10-14/sources/17592186100868.json').read_bytes()
sources=source_wrapper['record'][':knowledge-point/questions'];byid={q[':question/math-academy-id']:q for q in sources};cases=json.loads((D/'source-cases.json').read_text())
replays=[];fidelity={'originals':len(sources),'complete_banks_matched':0,'choices_matched':0,'distractors_matched':0,'original_correct_designations_matched':0,'original_correct_designations_present':0,'field_shapes_matched':0,'solution_prose_sequence_matched':0,'solution_prose_sequence_present':0,'prompt_masks_matched':0,'raw_exact_solution_strings':0,'source_correct_repairs':1,'source_solution_repairs':1}
for c in cases:
 r=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']);check(r);replays.append(r);src=byid[c['source_id']]
 # Compare source structure after the authorized answer-vector display repair;
 # retained source masks remain unmodified evidence of the original capture.
 expected_prompt=src[':question/problem']
 if G.TEMPLATES[c['template']]['fields'][0]['type']=='blank':expected_prompt=G.answer_layout(expected_prompt)
 assert mask(r['question'][':question/problem'])==mask(expected_prompt);fidelity['prompt_masks_matched']+=1
 for sf,f in zip(src[':question/answer-fields'],r['question'][':question/answer-fields']):
  expected=[value(G.mf.normalize_tex(a[':answer/value'])) for a in sf[':answer-field/choices']];actual=[value(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(expected)==len(actual) and all(sum(vequal(e,a) for a in actual)==1 for e in expected), (c["source_id"],expected,actual)
  fidelity['choices_matched']+=len(expected);fidelity['distractors_matched']+=len(expected)-1 if sf[':answer-field/type'][':db/ident'].endswith('/radio') else 0;fidelity['field_shapes_matched']+=1
  if ':answer-field/correct' in sf:
   fidelity['original_correct_designations_present']+=1;assert vequal(value(field_value(f)),value(G.mf.normalize_tex(sf[':answer-field/correct'][':answer/value'])));fidelity['original_correct_designations_matched']+=1
 fidelity['complete_banks_matched']+=1
 if ':question/worked-solution' in src:
  fidelity['solution_prose_sequence_present']+=1
  assert mask(src[':question/worked-solution'])==mask(r['question'][':question/worked-solution']);fidelity['solution_prose_sequence_matched']+=1
  fidelity['raw_exact_solution_strings']+=src[':question/worked-solution']==r['question'][':question/worked-solution']
  original=matrices(src[':question/worked-solution']);generated=matrices(r['question'][':question/worked-solution']);assert len(original)==len(generated)
  for i,(a,b) in enumerate(zip(original,generated)):
   assert len(a)==len(b)
   for aa,bb in zip(a,b):
    assert len(aa)==len(bb)
    for x,y in zip(aa,bb):assert equal(parse(x),parse(y));math_counts['source_solution_stage_checks']+=1
save('source-replays.json',replays);save('source-fidelity.json',fidelity)

# Every observed family/profile at anchors and changed scales, plus every symbol
# coefficient held-data change and renaming probes. Fixed target is the entire vector.
review=[];allrecords=list(replays);slots=[];ids={};unique={l:set() for l in ['easy','moderate','hard']}
for sid,t in G.TEMPLATES.items():
 for profile in (['observed','authored-operations'] if (t['fields'][0]['type']=='radio' and sid!='q-13554') or t['level']=='hard' else ['observed']):
  for seed in range(20):
   r=G.generate(t['level'],seed+40,template=sid,profile=profile);check(r);allrecords.append(r);unique[t['level']].add(r['generation']['mathematical_fingerprint'])
   if seed<2:review.append({'label':'Generated '+sid+' '+profile+' '+str(seed),'record':r})
 c=next(c for c in cases if c['source_id']==sid);base=G.generate(t['level'],template=sid,parameters=c['parameters'],profile='observed')
 for v in t['variables']:
  seen=[]
  for scale in range(1,6):
   p=copy.deepcopy(c['parameters']);p['scales'][v]=scale
   try:r=G.generate(t['level'],template=sid,parameters=p,profile='observed')
   except ValueError as e:
    assert 'workload' in str(e);continue
   check(r);seen.append(scale)
  slots.append({'template':sid,'slot':'scale/'+v,'held_other_data':True,'values':seen})
 # Every allowed scalar name, with all other mathematical data held unchanged.
 for v in t['variables']:
  seen=[]
  for name in 'abcdefghijklmnopqrstuvwxyz':
   p=copy.deepcopy(c['parameters']);p['names'][v]=name
   if name in [p['names'][x] for x in t['variables'] if x!=v]:continue
   try:r=G.generate(t['level'],template=sid,parameters=p,profile='observed')
   except ValueError as e:
    if 'collides with column-vector' in str(e):continue
    raise
   check(r);allrecords.append(r);assert r['generation']['mathematical_fingerprint']==base['generation']['mathematical_fingerprint'];seen.append(name)
  slots.append({'template':sid,'slot':'name/'+v,'held_other_data':True,'values':seen})
 # Identity independent of option order, seed and profile aliases when display same.
 for seed in [1,2,3,99]:
  r=G.generate(t['level'],seed,template=sid,parameters=c['parameters'],profile='observed');assert r['question'][':question/id']==base['question'][':question/id']
 # Bounds must be applied to explicit parameters too.
 for bad in [0,-1,6,True]:
  p=copy.deepcopy(c['parameters']);p['scales'][t['variables'][0]]=bad
  try:G.generate(t['level'],template=sid,parameters=p);raise AssertionError('bad bound accepted')
  except ValueError:pass
# Coefficient slots for the symbolic-column moderate blank family preserve
# the source signs, unit scalar column and maximum product coefficient6.
for idx in range(4):
 for mag in range(1,7):
  p=copy.deepcopy(next(c['parameters'] for c in cases if c['source_id']=='q-318595'));p['matrix_coefficients'][idx]=mag*(1 if idx in [0,3] else -1)
  r=G.generate('moderate',template='q-318595',parameters=p);check(r);allrecords.append(r)
 slots.append({'template':'q-318595','slot':'matrix_coefficient/'+str(idx),'held_other_data':True,'values':list(range(1,7))})
for sid in ['q-275597','q-318589','q-70226']:
 for gain in [1,2]:
  p=copy.deepcopy(next(c['parameters'] for c in cases if c['source_id']==sid));p['matrix_gain']=gain;r=G.generate('hard',template=sid,parameters=p,profile='observed');check(r);allrecords.append(r)
 slots.append({'template':sid,'slot':'matrix_gain','held_other_data':True,'values':[1,2]})
# Enumerate the exact finite normal hard row-gain domains through the public
# default profile, independently validating printed factors, zero patterns and banks.
hard_domains={};hard_union=set();default_union=set();domain_records=[]
for sid,domain in G.HARD_ROW_GAINS.items():
 t=G.TEMPLATES[sid];hashes=set();gain_seen=[set(),set(),set()]
 sourcecase=next(c for c in cases if c['source_id']==sid)
 anchor=G.generate_hard(template=sid,parameters=sourcecase['parameters'],profile='observed')
 anchor_mats=matrices(anchor['question'][':question/problem']);anchor_rows=[[parse(c) for c in row] for row in anchor_mats[0]];anchor_vector=[parse(row[0]) for row in anchor_mats[1]]
 anchor_out=[S.expand(sum(a*b for a,b in zip(row,anchor_vector))) for row in anchor_rows]
 for idx,gains in enumerate(domain):
  r=G.generate_hard(idx,template=sid);assert r['generation']['profile']=='authored-operations';assert r['generation']['parameters']['row_gains']==list(gains)
  check(r);allrecords.append(r);domain_records.append(r);fp=r['generation']['mathematical_fingerprint'];hashes.add(fp);hard_union.add(fp)
  # Read actual printed objects; row gains cannot move zeros or break cancellation.
  rm=matrices(r['question'][':question/problem']);rows=[[parse(c) for c in row] for row in rm[0]];vec=[parse(row[0]) for row in rm[1]];assert vec==anchor_vector
  for i,row in enumerate(rows):
   gain_seen[i].add(gains[i]);assert all(equal(a,gains[i]*b) for a,b in zip(row,anchor_rows[i]));assert [a==0 for a in row]==[a==0 for a in anchor_rows[i]]
   out=S.expand(sum(a*b for a,b in zip(row,vec)));assert equal(out,gains[i]*anchor_out[i]);assert (out==0)==(anchor_out[i]==0)
  same=G.generate_hard(idx+len(domain),template=sid);assert same['question'][':question/id']==r['question'][':question/id']
 assert len(hashes)==len(domain)
 # Held-other-row changes test the permitted gain of each row independently.
 held=[]
 for rowidx in range(3):
  eligible=[]
  for gain in [-2,-1,1,2]:
   params=copy.deepcopy(sourcecase['parameters']);params['row_gains']=[1,1,1];params['row_gains'][rowidx]=gain
   try:r=G.generate_hard(template=sid,parameters=params,profile='authored-operations')
   except ValueError as e:assert 'workload' in str(e);continue
   check(r);eligible.append(gain);rm=matrices(r['question'][':question/problem']);rows=[[parse(c) for c in row] for row in rm[0]]
   for i,row in enumerate(rows):assert all(equal(a,(gain if i==rowidx else 1)*b) for a,b in zip(row,anchor_rows[i]))
  held.append(eligible);slots.append({'template':sid,'slot':'row_gain/'+str(rowidx+1),'held_other_rows':True,'values':eligible})
 hard_domains[sid]={'eligible_gain_tuples':len(domain),'distinct_canonical_tasks':len(hashes),'normal_default_seeds_tested':len(domain),'normal_default_coverage':len(hashes),'gain_values_by_row':[sorted(x) for x in gain_seen],'held_other_rows_values':held}
# Unqualified default selects a template as well as gains. Report the actual
# bounded seed coverage separately from complete per-family default coverage.
for seed in range(512):
 r=G.generate_hard(seed);fp=r['generation']['mathematical_fingerprint'];assert fp in hard_union;default_union.add(fp)
save('hard-domain.json',{'source_basis':2275,'normal_scope':'source scalar coefficients and column; independent eligible signed row gains; fixed source zero/cancellation patterns and stage contracts','per_family':hard_domains,'canonical_union_size':len(hard_union),'normal_per_family_default_coverage':sum(v['normal_default_coverage'] for v in hard_domains.values()),'unqualified_default_seed_count':512,'unqualified_default_distinct_tasks':len(default_union),'all_names_profiles_and_zero_multiplied_entries_excluded':True})
save('hard-domain-records.json',domain_records)
save('slot-coverage.json',slots);save('review.json',review)
# Exhaustive meaningful coefficient domains, without name/option inflation.
enumerated={}
for sid,t in G.TEMPLATES.items():
 hashes=set()
 for scalevals in [(1,)*len(t['variables']),(5,)*len(t['variables']),tuple(1 if i%2 else 5 for i in range(len(t['variables'])))]:
  # Easy numeric-vector slot is separately exercised across the complete domain.
  p={'scales':dict(zip(t['variables'],scalevals)),'names':{v:v for v in t['variables']}}
  if sid=='q-13554':p['vector']=[1,2]
  
  if sid=='q-318595':p['matrix_coefficients']=[6,-4,-5,2]
  try:r=G.generate(t['level'],template=sid,parameters=p,profile='observed')
  except ValueError as e:
   assert 'workload' in str(e);continue
  check(r);hashes.add(r['generation']['mathematical_fingerprint'])
 enumerated[sid]={'coefficient_domain_instances':len(hashes),'coefficient_combinations':5**len(t['variables']),'coverage':'representative all-low/all-high/mixed corners; every individual scale exhaustively covered with others held fixed'}
for u in range(1,5):
 for v in range(2,6):
  p=copy.deepcopy(cases[1]['parameters']);p['vector']=[u,v]
  if u==v:continue
  try:r=G.generate('easy',template='q-13554',parameters=p)
  except ValueError as e:
   assert 'workload' in str(e);continue
  check(r)
# Explicit over-cap instance from the visual review must fail unchanged.
p=copy.deepcopy(next(c['parameters'] for c in cases if c['source_id']=='q-318595'));p['scales']={'p':4,'q':5}
try:G.generate('moderate',template='q-318595',parameters=p);raise AssertionError('96-coefficient instance accepted')
except ValueError as e:assert 'workload' in str(e)
for badcoef in [[7,-4,-5,2],[6,4,-5,2]]:
 p=copy.deepcopy(next(c['parameters'] for c in cases if c['source_id']=='q-318595'));p['matrix_coefficients']=badcoef
 try:G.generate('moderate',template='q-318595',parameters=p);raise AssertionError('invalid coefficient slot accepted')
 except ValueError:pass
# C0 guard negative control.
bad=copy.deepcopy(replays[0]);bad['question'][':question/problem']+='\x01'
try:G.guarded(bad);raise AssertionError('C0 accepted')
except ValueError:pass
# Math validator negative controls: stale input-role, product sign, summand, result, key.
negative=[];valid_counts=dict(math_counts)
for label,mutate in [
 ('operand-role',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace(r'1 \\ -1 \\ -1',r'-1 \\ -1 \\ -1'))),
 ('dot-factor',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('a'+r'\cdot 1','a'+r'\cdot 2',1))),
 ('evaluated-summand',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('a+a-a','a+a+a',1))),
 ('collected-result',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'\begin{bmatrix}a \\ a+b',r'\begin{bmatrix}2a \\ a+b'))),
 ('wrong-key',lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id',next(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']!=r['question'][':question/answer-fields'][0][':answer-field/correct'][1])]))]:
 bad=copy.deepcopy(replays[0]);mutate(bad);assert bad!=replays[0],label
 try:check(bad);raise RuntimeError('validator missed '+label)
 except AssertionError:negative.append(label)

math_counts=valid_counts
# Native grader uses exact current binary+library+source/dependency hashes.
build=json.loads((REPO/'generate/scratch/17592186059716-draft/reference/grader-build.json').read_text());hashes={build['source']:build['source_sha256'],build['library']:build['library_sha256'],build['binary']:build['binary_sha256'],**build['engine_sources'],**build['dependencies']}
for path,sha in hashes.items():assert hashlib.sha256((REPO/path).read_bytes()).hexdigest()==sha,path
save('grader-provenance.json',{'verified_count':len(hashes),'verified_hashes':hashes,'binary_sha256':build['binary_sha256']})
engine=[]
for i,r in enumerate(allrecords):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete bank choice identity'})
  else:
   v=field_value(f);expr=parse(v);expanded=S.expand(expr)
   # A genuinely uncollected/expanded equivalent, not a simplified identical string.
   row=int(f[':answer-field/key'].split('-')[-1])-1;pm=matrices(r['question'][':question/problem']);M=pm[0];V=pm[1];eq='+'.join('('+M[row][j]+')('+V[j][0]+')' for j in range(len(V)))
   checks.extend([{'field_index':fi,'submitted':v,'expected':'accepted','purpose':'canonical exact scalar'}, {'field_index':fi,'submitted':eq,'expected':'accepted','purpose':'uncollected row dot-product equivalent'}, {'field_index':fi,'submitted':S.latex(expanded+1),'expected':'rejected','purpose':'incorrect scalar'}])
 engine.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':checks})
save('engine-input.json',engine)
subprocess.run([str(REPO/build['binary']),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
# Review requires all originals and at least two generated per family/profile.
reviewmd=['# Source and generated review','Originals come from frozen basis2275; source payloads and key omissions remain in source.json.']
for r in replays:
 sid=r['generation']['template'];src=byid[sid];reviewmd+=['\n## Original '+sid,src[':question/problem'],src.get(':question/worked-solution','[Original worked solution absent; repaired replay is separately labeled.]')]
 for f in src[':question/answer-fields']:reviewmd+=['\nSource '+f[':answer-field/key']+': '+'; '.join('$'+G.mf.normalize_tex(a[':answer/value'])+'$' for a in f[':answer-field/choices'])]
for item in review:
 r=item['record'];reviewmd+=['\n## '+item['label'],r['question'][':question/problem']]
 for f in r['question'][':question/answer-fields']:reviewmd+=['\n'+f[':answer-field/key']+': '+'; '.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])]
 reviewmd+=[r['question'][':question/worked-solution']]
(D/'review.md').write_text('\n\n'.join(reviewmd)+'\n')
save('render-records.json',replays+[x['record'] for x in review])
report={'status':'pass','source_fidelity':fidelity,'mathematics':math_counts,'generated_native_records':len(allrecords),'workload_caps':G.WORKLOAD,'numeric_workload_negative_controls':['q-318595 p-scale4 q-scale5 (96p²)','matrix coefficient7','matrix coefficient wrong sign'],'enumerated_domains':enumerated,'sampled_unique_math_tasks':{k:len(v) for k,v in unique.items()},'normal_hard_domain_size':len(hard_union),'normal_hard_per_family_default_coverage':sum(v['normal_default_coverage'] for v in hard_domains.values()),'unqualified_default_hard_512_seed_coverage':len(default_union),'source_provenance':{k:source_wrapper[k] for k in ['database','basis','lineage']},'negative_controls_detected':negative,'runtime':{'python':platform.python_version(),'sympy':S.__version__},'registered_numeric_work':'absent before imports; untouched; final baseline recheck required','limits':['No source difficulty/correct/solution for q-13554: easy level and mathematical repair are authored, never counted as observed designations/solution.','All source banks match as complete algebraic vectors; source distractor intent remains unverified. Observed bank profiles preserve expression patterns, normal radio defaults use a separate authored operations profile.','Raw exact worked-solution TeX differs due to structural matrix normalization; complete shared prose, stage count, ordered row products, evaluated terms and final mathematical values are checked separately.','Native scalar equivalence is tested on actual uncollected row products; native radio grading tests selected owned answer identities, with vector equivalence checked independently.','Native reserved ln token is documented by separate parser-limit-report.json: two supported disambiguated/uncollected checks accepted and one deliberately unspaced diagnostic unresolved.','Normal hard row-gain domain is exhaustively enumerated separately; broader explicit legacy scalar combinations remain bounded by the same workload caps. Names, profiles, option order and zero-multiplied matrix entries do not inflate canonical counts.']}
save('validation.json',report);print(json.dumps(report,indent=2))
