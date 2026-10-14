#!/usr/bin/env python3
"""Independent actual-display predicates, whole banks/stages, native memory grading."""
import collections,copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def require(ok,why):
 if not ok:raise AssertionError(why)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def displayed(prompt):
 matrices=[]
 for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S):
  rows=[[x.strip() for x in row.split('&')] for row in body.split(r'\\')]
  require(rows and rows[0] and len({len(row) for row in rows})==1,'Actual rectangular display')
  values=[]
  for row in rows:
   output=[]
   for s in row:
    expr=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',s)
    expr=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1)/(\2)',expr)
    output.append(sp.sympify(expr))
   values.append(output)
  matrices.append(values)
 return matrices
LABEL={'A row vector':'row','A column vector':'column','A column matrix':'column','A zero matrix':'zero','An identity matrix':'identity','A diagonal matrix':'diagonal','A square matrix':'square','Other':'other'}
def props(m):
 a=sp.Matrix(m);r,c=a.shape
 return {'row':r==1,'column':c==1,'zero':bool(a.is_zero_matrix),'square':r==c,'diagonal':r==c and bool(a.is_diagonal()),'identity':r==c and a==sp.eye(r),'other':r>1 and c>1 and r!=c and not a.is_zero_matrix}
def category_truth(value,m,vals):
 p=props(m);cat=LABEL[value]
 if not p[cat]:return False
 if cat=='square' and any(p[LABEL[v]] for v in vals if LABEL[v] in ('diagonal','identity')):return False
 if cat=='diagonal' and any(p[LABEL[v]] for v in vals if LABEL[v]=='identity'):return False
 return True

def vector_stage_solution(names,ms,kind):
 bullets=[];good=[]
 for n,m in zip(names,ms):
  r,c=sp.Matrix(m).shape;yes=(r==1 if kind=='row' else c==1)
  if yes:bullet=f'- ${n}$ is a {kind} vector since it has only one '+('row.' if kind=='row' else 'column.');good.append(n)
  elif kind=='row' and c==1:bullet=f"- ${n}$ is *not* a row vector. It has only one column (and ${r}$ rows), so it's a column vector."
  elif kind=='column' and r==1:bullet=f"- ${n}$ is *not* a column vector. It has only one row (and ${c}$ columns), so it's a row vector."
  else:bullet=f'- ${n}$ is *not* a {kind} vector, since it has more than $1$ '+('row' if kind=='row' else 'column')+f' (it has ${r if kind=="row" else c}$ '+('rows' if kind=='row' else 'columns')+').'
  bullets.append(bullet)
 if len(good)==1:finish=f'Therefore, only ${good[0]}$ is a {kind} vector.'
 elif not good:finish=f'Therefore, none of the matrices are {kind} vectors.'
 else:finish='Therefore, '+('only ' if len(good)<3 else '')+' and '.join('$'+x+'$' for x in good)+f' are {kind} vectors.'
 return '\n\n'.join(bullets)+'\n\n'+finish

def inspect(rec):
 kp,q,meta=rec['knowledge_point'],rec['question'],rec['generation'];t=meta['template'];level=meta['level'];raw=meta['evidence_only']
 require(kp=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'Plain outer KP keys')
 uuid.UUID(q[':question/id']);ms=displayed(q[':question/problem']);names=re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}',q[':question/problem'])
 require(names==meta['parameters']['names'],'All actual name slots')
 require(len(ms)==(1 if t=='classification' else 3),'Full assessed object count')
 require(ms==[[[g.scalar(x) for x in row] for row in m] for m in meta['parameters']['matrices']],'Actual displayed parameters')
 lo,hi=g.BOUNDS[level]
 require(all(lo<=max(sp.Matrix(m).shape)<=hi for m in ms),'Rendered level bound')
 if level!='easy' and t!='classification':
  counts=[sp.Matrix(m).cols if t=='columns' else sp.Matrix(m).rows for m in ms]
  require(any(n>1 for n in counts) and all(n==1 or lo<=n<=hi for n in counts),'Rendered extended negative-axis inspection workload')
 require(meta['eligible_for_learning']==(not raw),'Raw missing-key eligibility')
 g.validate_generated_record({**copy.deepcopy(rec),'question':{**copy.deepcopy(q),':question/worked-solution':q.get(':question/worked-solution','')}})
 fields=q[':question/answer-fields'];require(len(fields)==(3 if t in ('rows','columns') else 1),'Full field layout')
 for i,f in enumerate(fields):
  uuid.UUID(f[':answer-field/id']);vals=[a[':answer/value'] for a in f[':answer-field/choices']]
  require(len(vals)==len(set(vals))== (2 if t in ('rows','columns') else 5),'Complete distinct source bank')
  for a in f[':answer-field/choices']:uuid.UUID(a[':answer/id']);require(a[':answer/type']==':answer.type/text','Actual text answer')
  if t in ('rows','columns'):
   require(f[':answer-field/key']==names[i] and f[':answer-field/type']==':answer-field.type/checkbox','All checkbox key positions')
   truth=[v==str(props(ms[i])['row' if t=='rows' else 'column']).lower() for v in vals]
  elif t=='row_sets':
   require(f[':answer-field/type']==':answer-field.type/radio','Original subset radio contract')
   wanted={n for n,m in zip(names,ms) if props(m)['row']}
   truth=[set(re.findall(r'\$([A-Z])\$',v))==wanted for v in vals]
  else:
   require(f[':answer-field/type']==':answer-field.type/radio','Classification radio contract')
   truth=[category_truth(v,ms[0],vals) for v in vals]
  require(sum(truth)==1,'Actual criterion has exactly one designated field answer')
  # All wrong pairs are unequal in response semantics, not merely UUID strings.
  meanings=[tuple(re.findall(r'\$([A-Z])\$',v)) for v in vals] if t=='row_sets' else [LABEL[v] for v in vals] if t=='classification' else vals
  require(len(set(meanings))==len(vals),'Every complete option response has a unique meaning')
  if raw:require(':answer-field/correct' not in f,'Raw key absence retained')
  else:
   ref=f[':answer-field/correct'];require(ref[0]==':answer/id','Lookup reference type')
   index=[a[':answer/id'] for a in f[':answer-field/choices']].index(ref[1]);require(truth[index],'Independent displayed key')
 if raw:require(':question/worked-solution' not in q and ':question/difficulty' not in q,'Raw missing solution/rating preserved')
 else:
  sol=q[':question/worked-solution'];require(q[':question/difficulty']==':question.difficulty/'+level,'Difficulty enum')
  if t!='classification':require(sol==vector_stage_solution(names,ms,'column' if t=='columns' else 'row'),'Every rendered predicate/alternate-role/count stage and conclusion')
  else:
   vals=[a[':answer/value'] for a in fields[0][':answer-field/choices']];good=next(v for v in vals if category_truth(v,ms[0],vals));cat=LABEL[good]
   expected={'row':'The matrix has only one row. Hence, it is a row vector.','column':f'Notice that ${names[0]}$ is a matrix that has a single column. Therefore, it is a column vector.','diagonal':"The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. \n\nHence it's a diagonal matrix.",'identity':'The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are all ones. \n\nHence it is an identity matrix.','zero':'All the entries of the matrix are zeros. Hence, it is a zero matrix.','square':'The matrix has the same number of rows and columns. Hence, it is a square matrix.','other':'The matrix has no special name.'}[cat]
   require(sol==g.normalize_prose(expected),'Whole classification solution sentences/stages')
 content={'version':g.VERSION,'level':None if raw else level,'prompt':q[':question/problem'],'solution':None if raw else q[':question/worked-solution'],'fields':[(f[':answer-field/key'],f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),None if raw else next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])) for f in fields]}
 require(meta['content_fingerprint']==g.digest(content) and q[':question/id']==g.uid(g.digest(content)),'Actual prompt/stages/full-bank content ID')
 if t in ('rows','row_sets'):assessed={'task':'row_membership','objects':sorted([{'rows':sp.Matrix(m).rows,'one_column':sp.Matrix(m).cols==1} for m in ms],key=g.stable)}
 elif t=='columns':assessed={'task':'column_membership','objects':sorted([{'columns':sp.Matrix(m).cols,'one_row':sp.Matrix(m).rows==1} for m in ms],key=g.stable)}
 else:assessed={'task':'best_category','shape':list(sp.Matrix(ms[0]).shape),'predicates':props(ms[0])}
 require(meta['mathematical_fingerprint']==g.digest(assessed),'Actual predicate/object mathematical fingerprint')
 return ms

def fidelity(src,rec):
 q=rec['question'];require(q[':question/problem']==g.normalize_prose(src[':question/problem']),'Full normalized source prompt/layout')
 for k in (':question/difficulty',':question/worked-solution'):require((k in q)==(k in src),'Source optional attribute presence')
 if ':question/worked-solution' in src:require(q[':question/worked-solution']==g.normalize_prose(src[':question/worked-solution']),'Full source stages/prose')
 for a,b in zip(src[':question/answer-fields'],q[':question/answer-fields']):
  require(a[':answer-field/key']==b[':answer-field/key'] and a[':answer-field/type'][':db/ident']==b[':answer-field/type'],'Original field contract')
  require(collections.Counter(x[':answer/value'] for x in a[':answer-field/choices'])==collections.Counter(x[':answer/value'] for x in b[':answer-field/choices']),'Every original option')
  require((':answer-field/correct' in a)==(':answer-field/correct' in b),'Original designation absence/presence')
  if ':answer-field/correct' in a:require(a[':answer-field/correct'][':answer/value']==next(x[':answer/value'] for x in b[':answer-field/choices'] if x[':answer/id']==b[':answer-field/correct'][1]),'Original designated value')
def native_checks(rec):
 return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Complete categorical ID submissions; mathematics independently read from actual prompt'} for i,f in enumerate(rec['question'][':question/answer-fields']) if ':answer-field/correct' in f for a in f[':answer-field/choices']]
def rejects(fn):
 try:fn()
 except (ValueError,AssertionError):return
 raise AssertionError('Expected entire invalid instance to reject')

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());source_rows=[];native=[];review=[]
 for case in cases:
  rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['profile']);inspect(rec);src=g.ORIGINALS[case['source_id']];fidelity(src,rec)
  fields=src[':question/answer-fields'];source_rows.append({'source_id':case['source_id'],'prompt_normalized_match':True,'raw_prompt_match':rec['question'][':question/problem']==src[':question/problem'],'full_solution_match':True if ':question/worked-solution' in src else None,'matched_options':sum(len(f[':answer-field/choices']) for f in fields),'matched_designations':sum(':answer-field/correct' in f for f in fields),'missing_designations':sum(':answer-field/correct' not in f for f in fields),'raw_evidence_only':case['raw_missing_key']})
  if native_checks(rec):native.append({'label':'source-'+case['source_id'],'record':rec,'checks':native_checks(rec)})
  review.append({'label':'Original replay '+case['source_id'],'source':src,'record':rec})
  if case['raw_missing_key']:
   repaired=g.generate('easy',parameters=case['parameters'],profile=case['profile'].replace('_raw','_repaired'));inspect(repaired);native.append({'label':'derived-repair-'+case['source_id'],'record':repaired,'checks':native_checks(repaired)});review.append({'label':'Authored key and solution '+case['source_id'],'record':repaired})
 slot_coverage={};identities={};all_samples=[]
 for level in g.LEVELS:
  slot_coverage[level]={}
  for pf in g.DEFAULT_PROFILES:
   fps=set();shapes=set();outcomes=set();entry_patterns=set();positions=set()
   for seed in range(150):
    rec=g.generate(level,seed,profile=pf);ms=inspect(rec);all_samples.append(rec);fps.add(rec['generation']['mathematical_fingerprint']);shapes.add(tuple(sp.Matrix(m).shape for m in ms));outcomes.add(tuple(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) for f in rec['question'][':question/answer-fields']));entry_patterns.add(tuple(tuple(props(m).values()) for m in ms));positions.add(tuple('row' if props(m)['row'] else 'column' if props(m)['column'] else 'general' for m in ms))
    # Identical mathematical presentation keeps UUIDs under changed seed/order.
    replay=g.generate(level,seed+987,parameters=rec['generation']['parameters'],profile=pf)
    require(rec['question'][':question/id']==replay['question'][':question/id'],'Seed/order cannot create content identity')
   slot_coverage[level][pf]={'sampled':150,'semantic_tasks':len(fps),'shape_tuples':len(shapes),'outcomes':sorted(outcomes),'predicate_patterns':len(entry_patterns),'role_positions':sorted(positions)}
   for seed in (2,57):
    rec=g.generate(level,seed,profile=pf);review.append({'label':f'Generated {level} {pf} seed {seed}'+(' (authored level)' if level!='easy' else ''),'record':rec});native.append({'label':f'generated-{level}-{pf}-{seed}','record':rec,'checks':native_checks(rec)})
  identities[level]={r['generation']['mathematical_fingerprint'] for r in all_samples if r['generation']['level']==level}
 # Level bands truly change the inspected object's relevant count; report overlap.
 overlap={a+'-'+b:len(identities[a]&identities[b]) for a,b in itertools.combinations(g.LEVELS,2)}
 require(not any(overlap.values()),'Authored levels cannot simply relabel identical semantic tasks')
 # A role permutation changes presentation but cannot inflate mathematical capacity.
 p={'names':list('ABC'),'matrices':[[['1','0']],[['1'],['0']],[['0','1'],['1','0']]]}
 a=g.generate('easy',profile='rows',parameters=p);p['matrices'][0],p['matrices'][1]=p['matrices'][1],p['matrices'][0];b=g.generate('easy',profile='rows',parameters=p)
 require(a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id'],'Matrix permutation is presentation only')
 # API aliases and raw profiles use the same normal renderer and field-owned IDs.
 for case in cases:
  r1=g.generate('easy',parameters=case['parameters'],profile=case['profile']);r2=g.generate('easy',parameters=case['parameters'],profile=case['source_id']);require(r1['question']==r2['question'],'Profile alias content identity')
 # Exhaustive singleton and 2x2 binary overlaps; false claims cannot be hidden by UUID grading.
 overlap_probes=0
 for size in (1,2):
  for bits in itertools.product(('0','1'),repeat=size*size):
   matrix=[list(bits[i*size:(i+1)*size]) for i in range(size)]
   for pf in ('row','diagonal','other','legacy_other_repaired'):
    p={'names':['M'],'matrices':[matrix]};vals=[a[':answer/value'] for a in g.ORIGINALS[g.PROFILE_SOURCE[pf]][':question/answer-fields'][0][':answer-field/choices']]
    good=[v for v in vals if category_truth(v,[[sp.Integer(x) for x in row] for row in matrix],vals)]
    if len(good)==1:inspect(g.generate('easy',parameters=p,profile=pf))
    else:rejects(lambda:g.generate('easy',parameters=p,profile=pf))
    overlap_probes+=1
 # All eight checkbox truth masks incl. none/all and singleton both-vector membership.
 membership_probes=0
 for t in ('rows','columns'):
  for mask in itertools.product((False,True),repeat=3):
   ms=[([['0']] if yes else [['0','1'],['1','0']]) for yes in mask]
   rec=g.generate('easy',profile=t,parameters={'names':list('ABC'),'matrices':ms});inspect(rec);native.append({'label':f'checkbox-mask-{t}-{mask}','record':rec,'checks':native_checks(rec)});membership_probes+=1
 # Changed target role with entries held: transpose swaps row/column membership.
 for t in ('rows','columns'):
  p={'names':list('ABC'),'matrices':[[['1','0']],[['1'],['0']],[['0','1'],['1','0']]]};r1=g.generate('easy',profile=t,parameters=p);p['matrices']=[list(map(list,zip(*m))) for m in p['matrices']];r2=g.generate('easy',profile=t,parameters=p);inspect(r1);inspect(r2);require(next(a[':answer/value'] for a in r1['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==r1['question'][':question/answer-fields'][0][':answer-field/correct'][1])!=next(a[':answer/value'] for a in r2['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==r2['question'][':question/answer-fields'][0][':answer-field/correct'][1]),'Actual changed role changes displayed field key')
 # Finite inspected shape/property basis for all classification profiles and levels.
 finite=[];finite_union={level:set() for level in g.LEVELS}
 for level,(lo,hi) in g.BOUNDS.items():
  for pf in ('row','diagonal','other','legacy_other_repaired'):
   fps=set();valid=invalid=0
   for r in range(1,hi+1):
    for c in range(1,hi+1):
     if not lo<=max(r,c)<=hi:continue
     candidates=[[['0']*c for _ in range(r)], [['1' if i==j else '0' for j in range(c)] for i in range(r)], [['-1' if i==j else '0' for j in range(c)] for i in range(r)], [['2']*c for _ in range(r)]]
     for m in candidates:
      p={'names':['M'],'matrices':[m]};truth=[v for v in [a[':answer/value'] for a in g.ORIGINALS[g.PROFILE_SOURCE[pf]][':question/answer-fields'][0][':answer-field/choices']] if category_truth(v,[[sp.Integer(x) for x in row] for row in m],[a[':answer/value'] for a in g.ORIGINALS[g.PROFILE_SOURCE[pf]][':question/answer-fields'][0][':answer-field/choices']])]
      if len(truth)==1:
       rec=g.generate(level,parameters=p,profile=pf);inspect(rec);fps.add(rec['generation']['mathematical_fingerprint']);finite_union[level].add(rec['generation']['mathematical_fingerprint']);valid+=1
      else:rejects(lambda:g.generate(level,parameters=p,profile=pf));invalid+=1
   finite.append({'level':level,'profile':pf,'representative_instances':valid+invalid,'valid':valid,'whole_bank_rejections':invalid,'semantic_tasks_in_shape_property_basis':len(fps)})
 # Exhaust the finite three-object predicate/count domain modulo object order.
 membership_capacities=[]
 for level,(lo,hi) in g.BOUNDS.items():
  for t in ('rows','columns','row_sets'):
   representatives={}
   for r in range(1,hi+1):
    for c in range(1,hi+1):
     if not lo<=max(r,c)<=hi:continue
     n=c if t=='columns' else r
     if level!='easy' and n!=1 and not lo<=n<=hi:continue
     m=[['1']*c for _ in range(r)]
     key=(n,r==1) if t=='columns' else (n,c==1)
     representatives.setdefault(key,m)
   semantic_tasks=set();instances=0
   for triplet in itertools.combinations_with_replacement(representatives.values(),3):
    good=sum((len(m[0])==1 if t=='columns' else len(m)==1) for m in triplet)
    if level!='easy' and good==3:continue
    if t=='row_sets' and good not in (1,2):continue
    ms=list(triplet)
    if t=='row_sets':ms.sort(key=lambda m:len(m)!=1)
    rec=g.generate(level,profile='row_sets_repaired' if t=='row_sets' else t,parameters={'names':list('EFG') if t=='row_sets' else list('ABC'),'matrices':ms});inspect(rec);instances+=1;semantic_tasks.add(rec['generation']['mathematical_fingerprint']);finite_union[level].add(rec['generation']['mathematical_fingerprint'])
   require(instances==len(semantic_tasks),'No object-order capacity inflation')
   membership_capacities.append({'level':level,'template':t,'single_object_semantic_classes':len(representatives),'exhaustive_unordered_semantic_capacity':len(semantic_tasks),'tested':instances})
 # Bounds and malformed input are enforced on explicit public calls.
 for level in g.LEVELS:
  p=g.generate(level,profile='rows')['generation']['parameters'];p['matrices'][0]=[['1']*11];rejects(lambda:g.generate(level,profile='rows',parameters=p))
 rejects(lambda:g.generate('easy',profile='rows',field_type='radio'))
 rejects(lambda:g.generate('easy',profile='row',template='columns'))
 rejects(lambda:g.generate('easy',profile='row',parameters={'names':['A'],'matrices':[[['1'],['2','3']]]}))
 # Magnitudes excluded from predicate fingerprint, retained in presentation ID.
 a=g.generate('easy',profile='row',parameters={'names':['A'],'matrices':[[['2','3']]]});b=g.generate('easy',profile='row',parameters={'names':['A'],'matrices':[[['-3','2']]]});require(a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id'],'Cosmetic magnitudes are not semantic capacity')
 save('engine-input.json',native);engine=ROOT/'generate/runs/current/check-engine';completed=subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);require(completed.returncode==0,'Native engine: '+completed.stdout+completed.stderr)
 baseline=json.loads((HERE/'registered-baseline.json').read_text());require(all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha for p,sha in baseline.items()),'Entire registered generator/evidence unchanged')
 save('review.json',review);lines=['# Matrix classification draft review','', 'Source originals are retained in full in review.json. Raw missing-key records are evidence-only. Generated moderate/hard labels are authored inspection bands.']
 for item in review:
  q=item['record']['question'];lines+=['','## '+item['label'],'',q[':question/problem'],'','; '.join(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']) for f in q[':question/answer-fields']),'',q.get(':question/worked-solution','Original has no key or worked solution.')]
 (HERE/'review.md').write_text('\n'.join(lines)+'\n')
 report={'status':'passed','source_basis':g.SOURCE['basis'],'source_fidelity':source_rows,'totals':{'source_questions':7,'observed_easy':5,'unrated':2,'source_options_matched':37,'source_fields':11,'observed_designations_matched':9,'missing_designations':2,'source_solutions_matched':5,'missing_solutions':2},'samples_checked':len(all_samples),'slot_coverage':slot_coverage,'cross_level_semantic_overlap':overlap,'finite_shape_property_basis':finite,'finite_membership_capacities':membership_capacities,'finite_total_unordered_semantic_capacities':{level:len(fps) for level,fps in finite_union.items()},'binary_overlap_probes':overlap_probes,'checkbox_masks_checked':membership_probes,'native_records':len(native),'native_checks':sum(len(n['checks']) for n in native),'registered_baseline_files_unchanged':len(baseline),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'engine_source_sha256':hashlib.sha256((engine.with_suffix('.rs')).read_bytes()).hexdigest(),'runtime':{'python':sys.version,'sympy':sp.__version__},'limits':['Moderate/hard are authored dimension inspection policies, not observed ratings or new mathematical classes.','Only 7 practice source records; 2 have no observed designation/solution.','Categorical scalar magnitudes do not create semantic tasks; finite capacity remains.','Raw missing-key profiles cannot be graded and are ineligible for learning.','Radio incomparable true categories reject; 1x1 membership is independently tested without arbitrary most-specific tie breaking.']}
 save('validation.json',report);print(json.dumps({'status':'passed','samples':len(all_samples),'native_checks':report['native_checks'],'baseline_files':len(baseline),'sources':7}))
if __name__=='__main__':main()
