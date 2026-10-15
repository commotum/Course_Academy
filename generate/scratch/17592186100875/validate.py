"""Source-bank fidelity, independent matrix arithmetic and actual learner grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('identity_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def check_record(r):
 q=r['question'];m=g.matrix(q[':question/problem']);n=m.rows
 assert m.cols==n and n in (2,3)
 assert s.eye(n)*m==m and m*s.eye(n)==m
 assert q[':question/difficulty']==':question.difficulty/easy'
 assert g.matrix(q[':question/worked-solution'])==m
 # Dimension, order, names and field locations are retained from the template.
 original=g.QS[r['generation']['template']]
 assert re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}','MATRIX',q[':question/problem'],flags=re.S)==re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}','MATRIX',g.normalize_prose(original[':question/problem']),flags=re.S)
 assert r['generation']['task_fingerprint']==g.task(q)
 assert re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}','MATRIX',q[':question/worked-solution'],flags=re.S)==re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}','MATRIX',g.normalize_prose(original[':question/worked-solution']),flags=re.S)
 fields=q[':question/answer-fields'];keys=[f[':answer-field/key'] for f in fields];assert len(set(keys))==len(keys)
 placeholders=set(re.findall(r'\{\{([^}]+)\}\}',q[':question/problem']))
 if fields[0][':answer-field/type'].endswith('/blank'):
  assert placeholders==set(keys) and len(fields)==n*n
  for f in fields:
   i=int(f[':answer-field/key'].split('-')[1])-1;expected=str(m[i]);assert len(f[':answer-field/choices'])==1
   assert f[':answer-field/choices'][0][':answer/value']==expected
 else:
  assert len(fields)==1 and not placeholders
  f=fields[0];answers=f[':answer-field/choices'];assert len(answers)==5
  values=[g.matrix(a[':answer/value']) if a[':answer/type']==':answer.type/math' else a[':answer/value'] for a in answers]
  assert len(set(map(str,values)))==5
  correct=[a for a,v in zip(answers,values) if isinstance(v,s.MatrixBase) and v==m];assert len(correct)==1
  assert correct[0][':answer/id']==f[':answer-field/correct'][1]
 for f in fields:
  answers=f[':answer-field/choices'];assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in answers]
  assert len(set(a[':answer/id'] for a in answers))==len(answers)
 assert len({a[':answer/id'] for f in fields for a in f[':answer-field/choices']})==sum(len(f[':answer-field/choices']) for f in fields)
 return True

def native_checks(r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'entire owned radio bank'} for a in f[':answer-field/choices']]
  else:
   value=f[':answer-field/choices'][0][':answer/value'];v=int(value)
   checks += [{'field_index':i,'submitted':val,'expected':expected,'purpose':purpose} for val,expected,purpose in [(value,'accepted','canonical'),(f'{v}+0','accepted','equivalent expression'),(f'{2*v}/2','accepted','equivalent fraction'),(str(v+1),'rejected','wrong adjacent integer')]]
 return checks

def main():
 fidelity=[];samples=[];preview=[];native=[];coverage={}
 for k,old in g.QS.items():
  r=g.generate(template=k,replay=True)
  bank=r['question'][':question/answer-fields'];matched=total=0
  if g.profile(k,g.original(k)) is not None:
   generated=bank[0][':answer-field/choices']
   for f in old[':question/answer-fields']:
    assert len(generated)==len(f[':answer-field/choices'])==5
    for a in f[':answer-field/choices']:
     val=g.matrix(a[':answer/value']) if ':answer.type/math'==a[':answer/type'][':db/ident'] else a[':answer/value']
     matches=[b for b in generated if (g.matrix(b[':answer/value']) if b[':answer/type']==':answer.type/math' else b[':answer/value'])==val]
     assert len(matches)==1;matched+=1;total+=1
    if ':answer-field/correct' in f:assert f[':answer-field/correct'][':answer/value']==g.tex(g.original(k))
  else:
   bykey={f[':answer-field/key']:f for f in bank}
   for f in old[':question/answer-fields']:
    assert bykey[f[':answer-field/key']][':answer-field/choices'][0][':answer/value']==f[':answer-field/correct'][':answer/value'];matched+=1;total+=1
  fidelity.append({'source':k,'source_fields':len(old[':question/answer-fields']),'matched_values':matched,'total_values':total,'complete_bank_match':True,'normal_sampling':k not in g.EXCLUDED,'missing_source_solution':':question/worked-solution' not in old,'missing_source_correct_fields':sum(':answer-field/correct' not in f for f in old[':question/answer-fields'])})
  if k in g.EXCLUDED:continue
  check_record(r);native.append({'label':k+'-replay','record':r,'checks':native_checks(r)})
  varied=[]
  for seed in range(40):
   a=g.generate(seed=seed,template=k);assert a==g.generate(seed=seed,template=k);check_record(a);samples.append(a);varied.append(a['generation']['parameters'])
  coverage[k]={'samples':40,'distinct_matrices':len(set(map(str,varied))),'entry_values':sorted({v for m in varied for row in m for v in row}),'dimensions':list(g.original(k).shape),'target_slots':'none: complete identity product'}
  assert coverage[k]['distinct_matrices']>=20
  for a in samples[-40:-37]:native.append({'label':k+'-'+str(a['generation']['seed']),'record':a,'checks':native_checks(a)})
  preview.append({'source':old,'replay':r,'variants':samples[-40:-38]})
 # Hold all entries but one fixed and verify the changed output cell and solution.
 k='q-275522';p=[[-9,0],[2,9]];a=g.generate(template=k,parameters=p);p[0][1]=-4;b=g.generate(template=k,parameters=p)
 check_record(a);check_record(b);assert a['question'][':question/answer-fields'][1][':answer-field/choices'][0][':answer/value']=='0';assert b['question'][':question/answer-fields'][1][':answer-field/choices'][0][':answer/value']=='-4'
 for level in ('moderate','hard'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('unsupported band generated')
 (HERE/'source-bank-map.json').write_text(json.dumps(fidelity,indent=2)+'\n');(HERE/'side-by-side.json').write_text(json.dumps(preview,indent=2)+'\n');(HERE/'samples.json').write_text(json.dumps(samples,indent=2)+'\n');(HERE/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'engine-validation.json')],check=True)
 report={'passed':True,'source_basis':g.SOURCE['basis'],'source_fidelity':fidelity,'matched_values':sum(x['matched_values'] for x in fidelity),'total_values':sum(x['total_values'] for x in fidelity),'normal_records_mathematically_checked':len(samples),'coverage':coverage,'changed_entry_with_other_data_fixed':True,'supported_levels':['easy'],'unsupported_levels':{'moderate':'No source evidence for greater difficulty within the identity-product backbone; no added operations or dimension incompatibility authored.','hard':'No source evidence; increasing matrix size or relabeling does not establish hard difficulty.'},'source_anomalies':['q-13762 has two fields with identical selection key; one lacks correct. Both complete banks replay, but generated variants use one valid field. Source remains unchanged.','q-13763 is unrated and lacks solution/correct designation. Full bank replays but is excluded from normal sampling. Its unique mathematical answer is M.'],'actual_grader_binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'math_correctness':'Independent SymPy identity multiplication and prompt/solution/field parsing; complete radio bank uniqueness.'}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'replayed_source_values':report['matched_values'],'validated_variants':len(samples)}))
if __name__=='__main__':main()
