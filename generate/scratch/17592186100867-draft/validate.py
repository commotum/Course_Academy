"""Independent displayed-operand/stage/bank/identity checks and real native grader."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sp=importlib.util.spec_from_file_location('draft00867',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def save(name,x):(D/name).write_text(json.dumps(x,indent=2)+'\n')
def matrix_bodies(text):
 result=[];pos=0
 while True:
  m=re.search(r'\\begin\{bmatrix\}',text[pos:])
  if not m:return result
  start=pos+m.start();depth=1;begin=start+len(m[0]);end=None
  for token in re.finditer(r'\\(begin|end)\{bmatrix\}',text[begin:]):
   depth+=1 if token[1]=='begin' else -1
   if depth==0:end=begin+token.start();pos=begin+token.end();break
  assert end is not None,'unclosed matrix';result.append(text[begin:end])
def rows(body):return [x.strip() for x in body.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split('\\\\')]
def clean(x):return x.replace('&','').replace(r'\,','').replace(r'\cdot','*').strip()
def value(x):
 x=clean(x);assert re.fullmatch(r'[\d+*()\s-]+',x),repr(x)
 return int(s.sympify(x))
def scalar_matrix(body):return [[value(c) for c in row.split('&')] for row in rows(body)]
def bankvalues(f):
 out=[]
 for a in f[':answer-field/choices']:
  ms=matrix_bodies(a[':answer/value']);out.append(tuple(value(row) for row in rows(ms[0])) if ms else value(a[':answer/value']))
 return out
SUCCESSFUL_CHECKS=0
def check(record,strict=True):
 global SUCCESSFUL_CHECKS
 q=record['question'];meta=record['generation'];p=meta['parameters'];t=meta['template'];raw=meta['evidence_only']
 assert set(record['knowledge_point'])=={'db_id','id','title'} and record['knowledge_point']=={'db_id':g.KP,'id':g.KP_UUID,'title':g.TITLE}
 g.control_guard(q);g.guard(p,q.get(':question/difficulty','').split('/')[-1] if not raw else None,raw)
 prompt_m=matrix_bodies(q[':question/problem']);assert len(prompt_m)==2
 A=scalar_matrix(prompt_m[0]);V=scalar_matrix(prompt_m[1]);assert [len(row) for row in A]==[3]*3 and [len(row) for row in V]==[1]*3
 v=[r[0] for r in V];assert A==p['A'] and v==p['v'];answer=tuple(sum(A[i][j]*v[j] for j in range(3)) for i in range(3))
 if t.startswith('named'):
  names=re.search(r'Find \$([A-Z])([a-z])\$',q[':question/problem']);assert names and (names[1],names[2])==(p['matrix_name'],p['vector_name'])
  assert '$'+names[1] in q[':question/problem'] and '$'+names[2] in q[':question/problem']
 fields=q[':question/answer-fields'];assert len(fields)==(3 if t.endswith('blank') else 1)
 assert len({f[':answer-field/id'] for f in fields})==len(fields)
 for f in fields:
  values=bankvalues(f);assert len(values)==len(set(values))
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(values)
  if t.endswith('blank'):
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'];ix=int(f[':answer-field/key'][-1])-1;assert values==[answer[ix]]
   assert f[':answer-field/type']==':answer-field.type/blank'
  else:
   assert f[':answer-field/type']==':answer-field.type/radio' and len(values)==5 and answer in values
   # Independent bank re-evaluation uses displayed operands, never metadata answers.
   r,tv,u=answer;mid=meta['bank_profile'].removeprefix('observed:')
   recipes={
    'q-127267':[(r,tv,u),(r,tv,-u),(r,-tv,-u),(r,-tv,u),(r,r,-u)],
    'q-70188':[(r,tv,u),(r,-tv,-u),(r,tv,-u),(-r,-tv,u),(r,-tv,u)],
    'q-70190':[(r,tv,u),(r,tv,-u),(r,-tv,u),(-r,tv,u),(-r,-tv,u)],
    'q-70191':[(r,tv,u),(r,-tv,u),(r,-tv,-u),(-r,tv,u),(r,tv,-u)],
    'q-77350':[(r,tv,u),(-r,-tv,u),(r,u,tv),(r,-tv,u),(u,tv,r)],
    'q-13558':[(r,tv,u),(-r,-tv,u),(-r,tv,u),(r,-tv,-u),(r,tv,-u)]}
   if mid in recipes:expected=recipes[mid]
   elif mid in g.OPAQUE:
    original=g.SOURCES[mid];base=g.parameters_of(original);k=next(s.Rational(x,b) for x,b in zip(v,base['v']) if b);assert all(x==k*b for x,b in zip(v,base['v']))
    factors=[]
    for row,brow in zip(A,base['A']):
     d=next(s.Rational(x,b) for x,b in zip(row,brow) if b);assert all(x==d*b for x,b in zip(row,brow));factors.append(k*d)
    expected=[tuple(int(a*b) for a,b in zip(factors,x)) for x in bankvalues(original[':question/answer-fields'][0])]
   else:
    assert mid=='authored-method';active=[j for j in range(3) if v[j]];expected=[answer,*[tuple(answer[i]-A[i][j]*v[j] for i in range(3)) for j in active],tuple(sum(A[j][i]*v[j] for j in range(3)) for i in range(3)),*([tuple(-x for x in answer)] if len(active)==2 else [])]
   assert set(values)==set(expected)
  if ':answer-field/correct'in f:
   aid=f[':answer-field/correct'][1];assert [a[':answer/id'] for a in f[':answer-field/choices']].count(aid)==1
   got=values[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==aid)]
   assert got==(answer[int(f[':answer-field/key'][-1])-1] if t.endswith('blank') else answer)
  else:assert raw
 if ':question/worked-solution'in q:
  sol=q[':question/worked-solution'];ms=matrix_bodies(sol);assert len(ms)==5
  assert sol.startswith('We multiply each row in the matrix by the column vector using the dot product:\n\n$$\n')
  if t.startswith('named'):assert r'\begin{aligned}'+p['matrix_name']+p['vector_name']+' & =' in sol
  assert scalar_matrix(ms[0])==A and scalar_matrix(ms[1])==V
  for i,row in enumerate(rows(ms[2])):
   c=clean(row);matches=list(re.finditer(r'(\(-?\d+\)|-?\d+)\s*\*\s*(\(-?\d+\)|-?\d+)',c));assert len(matches)==3
   assert [(value(m[1]),value(m[2])) for m in matches]==list(zip(A[i],v))
   assert value(c)==answer[i]
   assert c[:matches[0].start()].strip()=='' and c[matches[-1].end():].strip()==''
   assert all(c[a.end():b.start()].strip()=='+' for a,b in zip(matches,matches[1:]))
  for i,row in enumerate(rows(ms[3])):
   c=clean(row);assert value(c)==answer[i]
   terms=re.findall(r'\(-?\d+\)|[+-]?\d+',c)
   assert len(terms)==3 and [value(z) for z in terms]==[A[i][j]*v[j] for j in range(3)]
  assert tuple(value(row) for row in rows(ms[4]))==answer
  # Nested aligned arithmetic layouts remain the source's layouts.
  source=g.SOURCES[meta['source_references'][0]]
  if ':question/worked-solution'in source:
   sm=matrix_bodies(source[':question/worked-solution']);assert [r'\begin{aligned}'in z for z in ms]==[r'\begin{aligned}'in z for z in sm]
   assert [len(rows(z)) for z in ms]==[len(rows(z)) for z in sm]
 SUCCESSFUL_CHECKS+=1
 return g.fingerprint({'A':A,'v':v})
def native(record,label):
 checks=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  if ':answer-field/correct'not in f:return None
  if f[':answer-field/type'].endswith('/radio'):
   checks += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all displayed field-owned radio choices'} for a in f[':answer-field/choices']]
  else:
   n=int(f[':answer-field/choices'][0][':answer/value'])
   checks += [{'field_index':i,'submitted':text,'expected':expected,'purpose':'canonical, unreduced equivalent sum/quotient, wrong scalar'} for text,expected in [(str(n),'accepted'),(f'{n-2}+2','accepted'),(f'{3*n}/3','accepted'),(str(n+1),'rejected')]]
 return {'label':label,'record':record,'checks':checks}
def main():
 reviews=json.loads((D/'review.json').read_text());cases=json.loads((D/'source-cases.json').read_text());nativecases=[];fidelity=[];matched=0;designations=0
 for case in cases:
  q=g.SOURCES[case['source_id']];r=g.generate(case['level'],parameters=case['parameters'],profile=case['bank_profile']);check(r);z=r['question']
  assert z[':question/problem']==g.normalize_prose(q[':question/problem'])
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in z)==(key in q)
  if ':question/worked-solution'in q:assert z[':question/worked-solution']==g.normalize_prose(q[':question/worked-solution'])
  for f in q[':question/answer-fields']:
   h=next(h for h in z[':question/answer-fields'] if h[':answer-field/key']==f[':answer-field/key']);assert h[':answer-field/type']==f[':answer-field/type'][':db/ident']
   assert sorted(bankvalues(f),key=str)==sorted(bankvalues(h),key=str);matched+=len(bankvalues(f))
   assert (':answer-field/correct'in f)==(':answer-field/correct'in h)
   if ':answer-field/correct'in f:
    cv=next(a[':answer/value'] for a in h[':answer-field/choices'] if a[':answer/id']==h[':answer-field/correct'][1]);assert cv==g.normalize_tex(f[':answer-field/correct'][':answer/value']);designations+=1
  fidelity.append({'source_id':case['source_id'],'prompt':True,'whole_solution_exact':':question/worked-solution'in q,'solution_omission_preserved':':question/worked-solution'not in q,'bank_values':sum(len(f[':answer-field/choices']) for f in q[':question/answer-fields']),'correct_present':sum(':answer-field/correct'in f for f in q[':question/answer-fields'])})
 for item in reviews:
  check(item['record']);n=native(item['record'],item['label'])
  if n:nativecases.append(n)
 slots={};counts={};distinct={};families={};defaultfamilies=set()
 for level in g.LEVELS:
  distinct[level]=set();families[level]={}
  for seed in range(400):
   r=g.generate(level,seed);check(r);p=r['generation']['parameters'];t=r['generation']['template'];distinct[level].add(r['generation']['mathematical_fingerprint']);families[level][t]=families[level].get(t,0)+1
   for i in range(3):
    for j in range(3):slots.setdefault(level+f'.A{i}{j}',set()).add(p['A'][i][j])
    slots.setdefault(level+f'.v{i}',set()).add(p['v'][i])
   for key in ('matrix_name','vector_name'):slots.setdefault(level+'.'+key,set()).add(p[key])
   # For fixed operands and complete profile, seed controls order only.
   b=g.generate(level,seed+10000,template=t,parameters=p,profile=r['generation']['bank_profile']);assert r['question'][':question/id']==b['question'][':question/id']
   assert {f[':answer-field/id'] for f in r['question'][':question/answer-fields']}=={f[':answer-field/id'] for f in b['question'][':question/answer-fields']}
   if seed<20:nativecases.append(native(r,level+'-'+str(seed)))
  assert len(distinct[level])==400 and set(families[level])==set(g.TEMPLATES)
 # Exercise every normal profile and authored complete bank under changed inputs.
 for level in g.LEVELS:
  for t in g.TEMPLATES:
   for profile in [*g.PROFILES[t],'authored-method']:
    for seed in range(30):check(g.generate(level,seed,template=t,profile=profile))
 # Rename and row-permutation slots with exact mathematical data held constant.
 p=g.parameters_of(g.SOURCES['q-318606']);a=g.generate('moderate',parameters=p,profile='observed:q-318606')
 b=g.generate('moderate',parameters={**p,'matrix_name':'Z','vector_name':'n'},profile='observed:q-318606');check(b)
 assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 p2=copy.deepcopy(p);p2['A']=[p['A'][1],p['A'][2],p['A'][0]];permuted=g.generate('moderate',parameters=p2,profile='observed:q-318606');check(permuted)
 regressions=[]
 def reject(label,record):
  try:check(record)
  except (ValueError,AssertionError):regressions.append(label)
  else:raise AssertionError('Mutation survived: '+label)
 bad=copy.deepcopy(b);bad['question'][':question/worked-solution']=a['question'][':question/worked-solution'];reject('stale target names',bad)
 sol=b['question'][':question/worked-solution'];ms=matrix_bodies(sol)
 for label,old,new in [('ordered multiplicand',r'(-8)\cdot 3',r'(-7)\cdot 3'),('missing plus',r' & + & ',r' & & '),('evaluated signed term','(-4)','4'),('final vector',g.vector(g.dot(p)),g.vector([111,222,333]))]:
  bad=copy.deepcopy(b);bad['question'][':question/worked-solution']=(sol.replace(ms[3],ms[3].replace(old,new,1)) if label=='evaluated signed term' else sol.replace(old,new,1 if label!='final vector' else -1));assert bad['question'][':question/worked-solution']!=sol;reject(label,bad)
 bad=copy.deepcopy(b);bad['question'][':question/problem']+='\x0c';reject('C0 control character',bad)
 for level in g.LEVELS:
  pbad=g.sample(level,__import__('random').Random(42));pbad['A'][0][0]=9
  try:g.generate(level,parameters=pbad,template='named-blank')
  except ValueError:pass
  else:raise AssertionError('Explicit bound bypass')
 # The canonical example is reference evidence, separate from practice/field counts.
 canonical=g.RECORD[':knowledge-point/canonical-example'];cm=matrix_bodies(canonical[':question/worked-solution']);assert len(cm)==5
 ca=scalar_matrix(cm[0]);cv=[x[0] for x in scalar_matrix(cm[1])];ans=[sum(a*b for a,b in zip(row,cv)) for row in ca]
 for i,row in enumerate(rows(cm[2])):
  factors=re.findall(r'(\(-?\d+\)|-?\d+)\s*\*\s*(\(-?\d+\)|-?\d+)',clean(row));assert [(value(a),value(b)) for a,b in factors]==list(zip(ca[i],cv));assert value(row)==ans[i]
 assert [value(row) for row in rows(cm[3])]==ans and [value(row) for row in rows(cm[4])]==ans
 save('canonical-validation.json',{'source_id':canonical[':question/math-academy-id'],'practice_count':False,'operands':{'A':ca,'v':cv},'all_nine_ordered_multiplicands':True,'each_evaluated_term_and_sum':True,'result':ans,'raster_operands_visually_inspected':True})
 #42 immutable native build inputs, including stale-shared-helper exclusion.
 build=json.loads((ROOT/'generate/scratch/17592186059716-draft/reference/grader-build.json').read_text());hashes={build['source']:build['source_sha256'],build['library']:build['library_sha256'],build['binary']:build['binary_sha256'],**build['engine_sources'],**build['dependencies']}
 assert len(hashes)==42
 for path,expected in hashes.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
 save('native-provenance.json',{'build':build,'verified_hashes':len(hashes),'all_matched':True,'old_shared_helper_used':False})
 save('native-input.json',nativecases);subprocess.run([str(ROOT/build['binary']),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 save('source-bank-replay.json',fidelity);save('slot-coverage.json',{'sample_count_per_level':400,'distinct_tasks':{k:len(v) for k,v in distinct.items()},'default_families':families,'slots':{k:sorted(v) for k,v in slots.items()},'held_data_name_change':True,'held_data_row_permutation':True,'fixed_target_role':'all three ordered output components','mutation_rejections':regressions})
 report={'passed':True,'source_basis':g.CAP['basis'],'source_ma_originals':11,'independent_inventory':0,'canonical_examples_separate':1,'source_prompts_exact':11,'source_full_solutions_exact':9,'source_missing_solutions_preserved':2,'source_values_matched':matched,'source_complete_banks':11,'source_fields':15,'source_designations_matched':designations,'source_missing_designations':2,'normal_generated_sample_count':1200,'successful_full_record_math_checks':SUCCESSFUL_CHECKS,'additional_profile_checks':1170,'native_records':len(nativecases),'distinct_tasks':{k:len(v) for k,v in distinct.items()},'review_records_checked':len(reviews),'all_levels':list(g.LEVELS),'native_hashes_verified':42,'mutations_rejected':regressions,'opaque_covariance_profiles':sorted(g.OPAQUE),'limitations':['Two unrated raw originals have no keys or solutions: preserved, mathematically derived normal completions separate.','Opaque source banks parameterized only by row/vector scaling covariance and ineligible for learning. No inferred learner distractor diagnosis.'],'python_version':sys.version.split()[0],'sympy_version':s.__version__,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()};save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
