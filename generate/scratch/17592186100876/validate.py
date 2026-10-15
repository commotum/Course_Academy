"""Independent product/key checks, complete source-bank replay, and real learner grading."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def value_matrix(t):return g.matrix(t)
def check_record(r):
 q=r['question'];ms=g.raw_matrices(q[':question/problem']);assert len(ms)==2
 a,b=[s.Matrix([[g.scalar(x) for x in row] for row in m]) for m in ms];out=a*b;column=b.cols==1
 n=a.rows if column else b.rows;basis=b if column else a
 assert n in (3,4) and list(basis).count(1)==1 and list(basis).count(0)==n-1
 j=list(basis).index(1);expected=a[:,j] if column else b[j,:];assert out==expected
 assert q[':question/difficulty']==':question.difficulty/'+('easy' if column else 'moderate')
 solution=q[':question/worked-solution'];sol=g.raw_matrices(solution)
 assert g.matrix(g.tex(sol[0]))==out and g.matrix(g.tex(sol[-1]))==out
 assert g.ordn(j) in solution and not re.search(r'\$[1-4]\$(?:st|nd|rd|th)',solution.replace(g.ordn(j),''))
 assert ('on the *left*' in solution)==(not column)
 if column:
  assert len(sol)==5
  # Independently evaluate every scalar dot product from its rendered terms.
  terms=sol[3];assert len(terms)==n and all(len(row)==1 for row in terms)
  for i,row in enumerate(terms):
   total=0
   for term in row[0].split('+'):
    lhs,rhs=term.split(r'\cdot');total+=g.scalar(lhs.strip().strip('()'))*int(rhs)
   assert s.simplify(total-out[i])==0
 fields=q[':question/answer-fields'];keys=[f[':answer-field/key'] for f in fields];assert len(set(keys))==len(keys)
 placeholders=set(re.findall(r'\{\{([^}]+)\}\}',q[':question/problem']))
 if fields[0][':answer-field/type'].endswith('/blank'):
  assert len(fields)==n and placeholders==set(keys)
  for f in fields:
   i=int(f[':answer-field/key'].split('-')[1])-1;assert len(f[':answer-field/choices'])==1
   assert s.simplify(g.scalar(f[':answer-field/choices'][0][':answer/value'])-out[i])==0
 else:
  assert len(fields)==1 and not placeholders
  f=fields[0];answers=f[':answer-field/choices'];assert len(answers)==5
  values=[g.matrix(a[':answer/value']) for a in answers];assert len(set(map(str,values)))==5
  correct=[a for a,val in zip(answers,values) if val==out];assert len(correct)==1
  assert f[':answer-field/correct'][1]==correct[0][':answer/id']
 for f in fields:assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in f[':answer-field/choices']]
 assert len({a[':answer/id'] for f in fields for a in f[':answer-field/choices']})==sum(len(f[':answer-field/choices']) for f in fields)
 assert r['generation']['task_fingerprint']==g.task(q)
 # Preserve complete prompt outside its two mathematical slots, including field layout.
 original=g.QS[r['generation']['template']]
 assert g.MATRIX.sub('MATRIX',q[':question/problem'])==g.MATRIX.sub('MATRIX',g.normalize_prose(original[':question/problem']))
 return True

def native_checks(r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete source-profile bank'} for a in f[':answer-field/choices']]
  else:
   val=f[':answer-field/choices'][0][':answer/value']
   checks += [{'field_index':i,'submitted':text,'expected':expect,'purpose':purpose} for text,expect,purpose in [(val,'accepted','canonical'),(val+'+0','accepted','equivalent expression'),(val+'+1','rejected','wrong shifted scalar')]]
 return checks

def main():
 replay=[];samples=[];native=[];side=[];coverage={}
 for k,old in g.QS.items():
  level=old.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1]
  r=g.generate(level,template=k,replay=True);bykey={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']};matched=0;total=0;distractors=0
  for f in old[':question/answer-fields']:
   new=bykey[f[':answer-field/key']];radio=f[':answer-field/type'][':db/ident'].endswith('/radio')
   old_values=[g.matrix(a[':answer/value']) if radio else g.scalar(a[':answer/value']) for a in f[':answer-field/choices']]
   new_values=[g.matrix(a[':answer/value']) if radio else g.scalar(a[':answer/value']) for a in new[':answer-field/choices']]
   assert len(old_values)==len(new_values)
   for v in old_values:assert sum(v==w for w in new_values)==1;matched+=1;total+=1
   if ':answer-field/correct' in f:
    cor=f[':answer-field/correct'][':answer/value'];generated=next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1]);assert (g.matrix(cor)==g.matrix(generated)) if radio else s.simplify(g.scalar(cor)-g.scalar(generated))==0
   if radio:distractors+=4
  replay.append({'source':k,'complete_banks':len(old[':question/answer-fields']),'matched_values':matched,'total_values':total,'matched_distractors':distractors,'total_distractors':distractors,'missing':[],'extra':[],'normal_sampling':k not in g.EXCLUDED})
  if k in g.EXCLUDED:continue
  check_record(r);native.append({'label':k+'-replay','record':r,'checks':native_checks(r)})
  variants=[]
  for seed in range(40):
   try:a=g.generate(level,seed,template=k)
   except AssertionError as e:
    if str(e)=='choice collision':continue
    raise
   assert a==g.generate(level,seed,template=k);check_record(a);variants.append(a);samples.append(a)
  targets=sorted({a['generation']['parameters']['target'] for a in variants});n=len(g.spec(k)[0]);allowed=[1] if k=='q-130247' else list(range(n));assert targets==allowed
  for target in targets:
   a=next(a for a in variants if a['generation']['parameters']['target']==target);native.append({'label':k+'-target-'+str(target),'record':a,'checks':native_checks(a)})
  coverage[k]={'samples':len(variants),'distinct_tasks':len({g.task(a['question']) for a in variants}),'target_positions':targets,'allowed_target_positions':allowed,'uncovered_positions':[],'distinct_matrices':len({str(a['generation']['parameters']['matrix']) for a in variants})}
  assert coverage[k]['distinct_tasks']>=(4 if k=='q-130247' else 20)
  side.append({'source':old,'replay':r,'variants':[next(a for a in variants if a['generation']['parameters']['target']==t) for t in targets]})
 # Changed target on identical mathematical matrix, both orientations and 4-entry row.
 changed=[]
 for k,level in [('q-275527','easy'),('q-41949','easy'),('q-337668','moderate'),('q-337673','moderate'),('q-41977','moderate')]:
  m,_,_=g.spec(k);n=len(m);pair=[]
  for j in (0,1):
   r=g.generate(level,template=k,parameters={'matrix':m,'target':j});check_record(r);pair.append(r)
  assert pair[0]['question'][':question/worked-solution']!=pair[1]['question'][':question/worked-solution'];assert pair[0]['question'][':question/answer-fields']!=pair[1]['question'][':question/answer-fields'];changed.append(pair)
 try:g.generate('hard')
 except ValueError:pass
 else:raise AssertionError('unsupported band accepted')
 for name,obj in [('source-bank-map.json',replay),('samples.json',samples),('side-by-side.json',side),('changed-target.json',changed),('native-input.json',native)]: (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'engine-validation.json')],check=True)
 report={'passed':True,'source_basis':g.SOURCE['basis'],'source_fidelity':replay,'matched_values':sum(x['matched_values'] for x in replay),'total_values':sum(x['total_values'] for x in replay),'normal_records_mathematically_checked':len(samples),'coverage':coverage,'changed_target_same_matrix':True,'supported_levels':['easy','moderate'],'unsupported_levels':{'hard':'No observed hard template. Increasing entry magnitudes or dimensions alone does not justify inventing hard difficulty within the row/column selection method.'},'source_anomalies':['q-41949 duplicated selection fields; one lacks a key. Both complete banks replay; new questions have one valid radio field.','q-41950 unrated, missing solution and key: replayed complete bank but excluded from generation and inventory.','q-130247 first displayed result has an incorrect negative second entry. Correct key and final result equal positive sqrt(2)/2. New solutions correct the typo; source unchanged.','q-41977 wrong-row distractor uses -sqrt(3) although the matrix has -sqrt(7). Preserve observed radicand-minus-four recipe; psychological interpretation unresolved.'],'actual_grader_binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'grading_entry_point':'course_academy_engine::learning::grade_field','plots':'none; all practice mathematical objects are standalone TeX matrices'}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'source_values':report['matched_values'],'validated_variants':len(samples)}))
if __name__=='__main__':main()
