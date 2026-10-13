"""Independent actual-printed readback, source fidelity, and native grading."""
import importlib.util,json,re,subprocess,hashlib
from pathlib import Path
import sympy as S
D=Path(__file__).parent;REPO=D.parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
G=module('cross_generator',D.with_suffix('.py'))
# Independent recursive-descent parser, not generator sympify/string converter.
P=module('independent_printed_parser',REPO/'generate/runs/current/vector-math-parser.py')
raw=json.loads((D/'source.json').read_text())['record'];sources={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']};cases=json.loads((D/'source-cases.json').read_text())
def eq(a,b):return all(S.simplify(x-y)==0 for x,y in zip(a,b))
def printed_inputs(prompt):
 pairs=list(re.finditer(r'\$([aubv])\s*=\s*([^$]+)\$',prompt))[:2];assert len(pairs)==2
 return tuple(P.vector(m.group(2).strip().rstrip('.')) for m in pairs)
def matrix_value(body):
 lines=body.split(r'\\');assert len(lines) in (2,3)
 if len(lines)==3:
  assert lines[0].strip()=='i & j & k'
  a,b=[S.Matrix([P.scalar(z) for z in row.split('&')]) for row in lines[1:]]
  return a.cross(b),a,b
 a,b=[[P.scalar(z) for z in row.split('&')] for row in lines]
 return a[0]*b[1]-a[1]*b[0]
def readback(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];a,b=printed_inputs(q[':question/problem']);c=a.cross(b)
 assert r['knowledge_point']['db_id']==G.KP_ID
 assert r'\times' in q[':question/problem']
 for text in (q[':question/problem'],q[':question/worked-solution']):
  assert text.count('$')%2==0
  depth=0
  for ch in text:
   if ch=='{':depth+=1
   if ch=='}':depth-=1
   assert depth>=0
  assert depth==0
 sol=q[':question/worked-solution'];body=sol.split(r'\begin{aligned}',1)[1].rsplit(r'\end{aligned}',1)[0];rows=body.split(r' \\  & =')
 assert len(rows)>=4
 for n,row in enumerate(rows):
  if r'\begin{aligned}' in row:
   spans=list(re.finditer(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',row));assert spans
   if n==0:
    assert len(spans)==1;val,pa,pb=matrix_value(spans[0].group(1));assert eq(pa,a) and eq(pb,b) and eq(val,c)
   else:
    assert len(spans)==3;v=S.Matrix([matrix_value(m.group(1)) for m in spans]);v[1]*=-1;assert eq(v,c)
  else:
   assert eq(P.vector(row.strip().rstrip('.')),c),(r['generation'],n,row,c)
 for f in q[':question/answer-fields']:
  assert f[':answer-field/id'];correct=f[':answer-field/correct'][1];answers=f[':answer-field/choices'];match=[z for z in answers if z[':answer/id']==correct];assert len(match)==1
  assert len({z[':answer/id'] for z in answers})==len(answers)
  if f[':answer-field/type'].endswith('radio'):
   values=[P.vector(z[':answer/value']) for z in answers]
   assert eq(P.vector(match[0][':answer/value']),c)
   for i,v in enumerate(values):assert all(not eq(v,w) for w in values[:i])
  else:
   key=f[':answer-field/key'];assert '{{'+key+'}}' in q[':question/problem']
   idx=int(key.split('-')[1])-1;sign=-1 if re.search(r'\{\{field-'+str(idx)+r'\}\}\$\\,i\\,-',q[':question/problem']) and idx==1 else 1
   # Read the actual supplied operator immediately before each component blank.
   prior=q[':question/problem'].split('{{'+key+'}}')[0]
   if idx>0 and re.search(r'\\,-\\,\$\s*$',prior):sign=-1
   assert S.simplify(P.scalar(match[0][':answer/value'])*sign-c[idx])==0,(key,prior,match,c)
 return a,b,c,len(rows)
def engine_checks(r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  ref=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('radio'):
   checks +=[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ref else 'rejected','purpose':'all owned choices'} for a in f[':answer-field/choices']]
  else:
   val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ref)
   # Keep distinct unreduced equivalent entries, not CAS-collapsed tautologies.
   equiv='('+val+')+1-1';wrong='('+val+')+1'
   checks +=[{'field_index':i,'submitted':z,'expected':expected,'purpose':why} for z,expected,why in ((val,'accepted','canonical component'),(equiv,'accepted','native unreduced equivalent fragment'),(wrong,'rejected','wrong component'))]
 return checks
records=[];review=[];fidelity=[];engine=[]
for case in cases:
 t=case['template'];q=sources[case['source_math_academy_id']]
 r=G.generate('easy',template=t,parameters=case['parameters'],profile=case['bank_profile']);readback(r)
 rr=G.generate('easy',template=t,parameters=case['parameters'],profile=case['bank_profile']+':raw')
 original=q[':question/answer-fields'];original=[original[0]] if case.get('legacy_evidence_only') else [f for f in original if f.get(':answer-field/correct') or t=='q-1408']
 matched=total=keys=keytotal=0
 for of,gf in zip(original,r['question'][':question/answer-fields']):
  assert of[':answer-field/key']==gf[':answer-field/key'];assert of[':answer-field/type'][':db/ident']==gf[':answer-field/type']
  ov=[a[':answer/value'] for a in of[':answer-field/choices']];gv=[a[':answer/value'] for a in gf[':answer-field/choices']];assert len(ov)==len(gv)
  parse=P.vector if gf[':answer-field/type'].endswith('radio') else lambda z:S.Matrix([P.scalar(z)])
  for z in ov:
   hits=[w for w in gv if eq(parse(z),parse(w))];assert len(hits)==1;(matched:=matched+1)
  total+=len(ov)
  if of.get(':answer-field/correct'):
   keytotal+=1;cv=next(z[':answer/value'] for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1]);assert eq(parse(cv),parse(of[':answer-field/correct'][':answer/value']));keys+=1
 prompt_exact=rr['question'][':question/problem']==q[':question/problem'];solution_exact=bool(q.get(':question/worked-solution')) and rr['question'][':question/worked-solution']==q[':question/worked-solution']
 assert prompt_exact,(t,rr['question'][':question/problem'],q[':question/problem'])
 if q.get(':question/worked-solution'):assert solution_exact,t
 fidelity.append({'template':t,'complete_bank_match':True,'matched_values':matched,'total_values':total,'matched_original_correct_designations':keys,'original_correct_designations':keytotal,'missing_original_correct_designations':len(original)-keytotal,'raw_prompt_exact':prompt_exact,'raw_solution_exact':solution_exact,'original_solution_present':bool(q.get(':question/worked-solution'))})
 records.append(r);review.append({'label':'Original replay '+t,'record':r,'raw_original':q,'raw_profile':rr})
 changed=G.generate('easy',template=t,parameters={'a_scale':2,'b_scale':1},profile=case['bank_profile']);readback(changed)
 assert G.generate('easy',seed=55,template=t,parameters={'a_scale':2,'b_scale':1},profile=case['bank_profile'])['question'][':question/id']==changed['question'][':question/id']
 records.append(changed);review.append({'label':'Generated changed-parameter opaque bank '+t,'record':changed})
for level in ('easy','moderate','hard'):
 for t in ('tuple_radio','basis_radio','tuple_blank','basis_blank'):
  for seed in (31,41):
   r=G.generate(level,seed,template=t);a,b,_,_=readback(r);records.append(r);review.append({'label':f'Authored {level} {t} seed {seed}','record':r})
   p=r['generation']['parameters'];assert G.generate(level,73,template=t,parameters=p)['question'][':question/id']==r['question'][':question/id']
# Broad signed/zero/fraction workload and readback across every normal template.
for level in ('easy','moderate','hard'):
 for seed in range(80):
  for t in ('tuple_radio','basis_radio','tuple_blank','basis_blank'):readback(G.generate(level,seed,template=t))
for level,p in [('moderate',{'a':[1,0,3],'b':[2,3,4]}),('hard',{'a':['2/4',1,2],'b':[2,3,4]}),('hard',{'a':['20/2','2/3',1],'b':['3/4',2,3]})]:
 try:G.generate(level,parameters=p)
 except ValueError:pass
 else:raise AssertionError('Explicit workload guard bypassed')
# Fail closed on explicit complete-bank collisions and incompatible profiles.
for kwargs in ({'parameters':{'a':[1,0,0],'b':[0,1,0]}},{'template':'q-1405','profile':'authored:five_operations'}):
 try:G.generate('easy',**kwargs)
 except ValueError:pass
 else:raise AssertionError('Invalid complete profile accepted')
original=G.generate('hard',31)
p=original['generation']['parameters'];alias={key:[str(S.sympify(z)*2)+'/2' for z in values] for key,values in p.items()}
assert G.generate('hard',93,parameters=alias)['generation']['mathematical_fingerprint']==original['generation']['mathematical_fingerprint']
# Every source-bank covariance combination is checked, including same-output inputs.
for t in G.RECIPES:
 for sa in ('1/2',1,2):
  for sb in ('1/2',1,2):readback(G.generate('easy',template=t,parameters={'a_scale':sa,'b_scale':sb}))
for n,r in enumerate(records):engine.append({'label':str(n)+':'+r['generation']['template'],'record':r,'checks':engine_checks(r)})
(D/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
(D/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
md=[]
for entry in review:
 md.append('## '+entry['label']+'\n\n'+G.markdown(entry['record']))
 if 'raw_original' in entry:md.append('\nCaptured source prompt:\n\n'+entry['raw_original'][':question/problem']+'\n\nCaptured solution:\n\n'+entry['raw_original'].get(':question/worked-solution','[Missing original solution; generated solution is authored.]'))
(D/'review.md').write_text('\n\n'.join(md)+'\n')
report={'status':'passed','database_writes':0,'basis':1356,'sources':27,'source_replay_profiles_including_legacy':28,'easy_observed_sources':26,'unrated_sources':1,'observed_moderate':0,'observed_hard':0,'fidelity':fidelity,'matched_source_values':sum(z['matched_values'] for z in fidelity),'total_source_values':sum(z['total_values'] for z in fidelity),'matched_original_correct_designations':sum(z['matched_original_correct_designations'] for z in fidelity),'original_correct_designations':sum(z['original_correct_designations'] for z in fidelity),'missing_original_correct_designations':sum(z['missing_original_correct_designations'] for z in fidelity),'raw_exact_prompts':sum(z['raw_prompt_exact'] for z in fidelity),'raw_exact_solutions':sum(z['raw_solution_exact'] for z in fidelity),'original_solution_denominator':sum(z['original_solution_present'] for z in fidelity),'independent_printed_readback_records':len(records)+960+252,'review_records':len(records),'engine':json.loads((D/'engine-report.json').read_text()),'source_repairs':['q-1408 authoritative screenshot confirms cross operator; missing key independently inferred; missing solution authored','q-1405 duplicated legacy field retained as explicit replay profile, normal question uses authoritative keyed field','q-282147 distributed product row missing parentheses corrected in normal replay, raw evidence preserves anomaly','q-281976/977 exact single-slash scalar source values verified; JSON escaping is not a repair'],'unresolved_findings':[],'bank_intent_limit':'All observed wrong bank intent remains unresolved; covariance profiles are explicit replay evidence, not default error recipes.'}
(D/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('PASS:',len(records),'review records;',report['matched_source_values'],'source values;',report['original_correct_designations'],'original keys;',report['missing_original_correct_designations'],'missing original keys honestly excluded.')

if (D/'freeze.json').exists():
 frozen=json.loads((D/'freeze.json').read_text())
 for name,expected in frozen['artifacts'].items():
  assert hashlib.sha256((REPO/name).read_bytes()).hexdigest()==expected,('Frozen artifact changed',name)
 print('Frozen final artifact hashes verified.')
