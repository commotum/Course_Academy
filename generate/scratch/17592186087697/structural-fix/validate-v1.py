"""Independently read displayed matrices, source banks, solutions and real grading."""
import copy, hashlib, importlib.util, json, re, subprocess, uuid
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def displayed(text):
 out={}
 for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}',text):
  raw=re.sub(r'\\text\{[^}]*\}','',m[2]);rows=[[Fraction(v.strip()) for v in row.split('&')] for row in raw.split('\\\\')]
  assert rows and len({len(row) for row in rows})==1
  out[m[1]]=rows
 assert len(out)==3
 return out

def parse(text):
 kind='identity' if 'identity matrices?' in text else 'diagonal'
 items=[]
 for rows in displayed(text).values():
  items.append((len(rows),len(rows[0]),tuple(tuple(0 if v==0 else 1 if v==1 else 2 for v in row) for row in rows)))
 return json.dumps([kind,sorted(items)],separators=(',',':'))

def solution_check(q):
 matrices=displayed(q[':question/problem']);kind='identity' if 'identity matrices?' in q[':question/problem'] else 'diagonal';truth={};diagonals={};identities={}
 for name,M in matrices.items():
  square=len(M)==len(M[0]);diagonal=square and all(v==0 for i,row in enumerate(M) for j,v in enumerate(row) if i!=j);identity=square and all(v==int(i==j) for i,row in enumerate(M) for j,v in enumerate(row))
  diagonals[name]=diagonal;identities[name]=identity;truth[name]=identity if kind=='identity' else diagonal
 fields=q[':question/answer-fields'];assert len(fields)==3 and {f[':answer-field/key'] for f in fields}==matrices.keys()
 for f in fields:
  typ=f[':answer-field/type'];assert (typ.get(':db/ident') if isinstance(typ,dict) else typ)==':answer-field.type/checkbox'
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
  cr=f[':answer-field/correct'];cid=str(cr[':answer/id']) if isinstance(cr,dict) else cr[1]
  choices=[a for a in f[':answer-field/choices'] if str(a[':answer/id'])==cid];assert len(choices)==1 and choices[0][':answer/value']==str(truth[f[':answer-field/key']]).lower()
 text=q[':question/worked-solution'];bullets=re.findall(r'^- \$([A-Z])\$ is ([\s\S]*?)(?=\n\n- |\n\nTherefore,)',text,re.M);assert len(bullets)==3
 assert [n for n,b in bullets]==list(matrices)
 for name,bullet in bullets:
  M=matrices[name];assert ('*not*' not in bullet)==truth[name]
  if 'not a square matrix' in bullet:assert len(M)!=len(M[0])
  elif 'do not lie on the main diagonal are not zeros' in bullet:
   assert len(M)==len(M[0]);m=re.search(r'\$\{([a-z])\}_\{(\d)(\d)\}=(-?\d+)\\ne 0\$',bullet);assert m,bullet
   i,j=int(m[2]),int(m[3]);assert m[1]==name.lower() and i!=j and M[i-1][j-1]==Fraction(m[4])!=0
  elif kind=='identity' and '*not*' in bullet:assert diagonals[name] and not identities[name] and 'diagonal entries are not all ones' in bullet
  else:assert diagonals[name]
  if 'not an identity matrix' in bullet:assert not identities[name]
 conclusion=text.split('\n\n')[-1];assert set(re.findall(r'\$([A-Z])\$',conclusion))=={n for n,v in truth.items() if v}
 if not any(truth.values()):assert 'none' in conclusion
 return 3

def independent(r):
 q=r['question'];m=r['generation'];assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
 assert q[':question/difficulty']==':question.difficulty/easy'
 assert r==g.generate('easy',m['seed'],m['template'],m['parameters'],m['bank_profile'])
 assert parse(q[':question/problem'])==m['parameter_fingerprint'];solution_check(q)
 ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
 assert len(ids)==len(set(ids));[uuid.UUID(v) for v in ids]
 for text in (q[':question/problem'],q[':question/worked-solution']):assert text.count('$')%2==0 and text.count('{')==text.count('}')

def checks(r):return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every field-owned checkbox value through actual learner grader'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def build_engine():
 deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs';libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')};cmd=['rustc','--edition=2024','-O',str(harness)]
 for n,p in libs.items():cmd+=['--extern',n+'='+str(p)]
 cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(HERE/'check-engine')];subprocess.run(cmd,check=True)
 save('engine-build.json',{'harness_sha256':sha(harness),'libraries':{str(p):sha(p) for p in libs.values()},'binary_sha256':sha(HERE/'check-engine')})

def main():
 source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};rs=[];replays=[];coverage={};review=[]
 for mid,t in g.TEMPLATES.items():
  r=g.generate('easy',template=mid,parameters=t['parameters']);independent(r);q=qs[mid];fresh=r['question']
  assert fresh[':question/problem']==q[':question/problem'] and fresh[':question/worked-solution']==q[':question/worked-solution'];solution_check(q)
  old={f[':answer-field/key']:f for f in q[':question/answer-fields']}
  for f in fresh[':question/answer-fields']:
   original=old[f[':answer-field/key']];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in original[':answer-field/choices']);assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==original[':answer-field/correct'][':answer/value']
  replays.append({'source':mid,'matched_fields':3,'total_fields':3,'matched_values':6,'total_values':6,'matched_correct_designations':3,'missing_options':[],'extra_options':[],'exact_prompt':True,'exact_solution':True});rs.append(r)
  seen=[{'shapes':set(),'witnesses':set(),'values':set()} for _ in range(3)];valid=[]
  for seed in range(400):
   try:variant=g.generate('easy',seed,mid)
   except ValueError:continue
   independent(variant);rs.append(variant);valid.append(variant)
   for slot,(M,w) in enumerate(zip(variant['generation']['parameters']['matrices'],variant['generation']['parameters']['witnesses'])):
    seen[slot]['shapes'].add((len(M),len(M[0])));seen[slot]['witnesses'].add(tuple(w) if w else None);seen[slot]['values'].update(v for row in M for v in row)
  assert len(valid)>150
  slots=[]
  for i,(item,role) in enumerate(zip(seen,t['roles'])):
   expected={(a,b) for a in range(2,5) for b in range(2,5) if (a!=b if role=='rectangular' else a==b)};assert item['shapes']==expected
   if role=='offdiagonal':assert item['witnesses']=={(a,b) for a in range(1,5) for b in range(1,5) if a!=b}
   slots.append({'slot':i,'role':role,'shapes':sorted(item['shapes']),'witnesses':sorted(x for x in item['witnesses'] if x),'values':sorted(item['values']),'uncovered_eligible_shapes':[],'uncovered_eligible_witnesses':[]})
  coverage[mid]={'valid_seeded_samples':len(valid),'slots':slots}
  review.append('## '+mid+' original\n\n'+g.markdown(r)+'\n\nVariant\n\n'+g.markdown(valid[0]))
 # Move the mathematical witness from upper-right to lower-left while retaining size, values and other matrices.
 t=g.TEMPLATES['q-11562'];p=copy.deepcopy(t['parameters']);a=g.generate(template='q-11562',parameters=p);p['matrices'][0]=[['0','0'],['1','0']];p['witnesses'][0]=[2,1];b=g.generate(template='q-11562',parameters=p)
 independent(a);independent(b);assert '${h}_{12}=1\\ne 0$' in a['question'][':question/worked-solution'] and '${h}_{21}=1\\ne 0$' in b['question'][':question/worked-solution'];assert parse(a['question'][':question/problem'])!=parse(b['question'][':question/problem']);rs.extend([a,b])
 coverage['controlled_changed_target']={'upper_to_lower_offdiagonal':True,'same_dimensions_values_other_matrices':True,'rendered_prompt_witness_and_key_independently_checked':True}
 # Reject stale witness reference explicitly.
 stale=copy.deepcopy(b['question']);stale[':question/worked-solution']=a['question'][':question/worked-solution']
 try:solution_check(stale)
 except AssertionError:pass
 else:raise AssertionError('Stale witness escaped validation')
 save('source-bank-replay.json',replays);save('slot-coverage.json',coverage);(HERE/'review.md').write_text('\n\n'.join(review)+'\n\n## Controlled changed position\n\n'+g.markdown(b))
 build_engine();native=[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(rs)];save('engine-input.json',native);subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True);engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 caps=json.loads((HERE/'capabilities.json').read_text());caps['validated_sample_count']=len(rs);save('capabilities.json',caps)
 tracked=[HERE.with_suffix('.py'),HERE/'templates.json',HERE/'validate.py',HERE/'check-engine'];save('validation.json',{'status':'pass','basis':source['basis'],'correctness':{'independent_fraction_matrix_checks':len(rs)},'fidelity':{'complete_banks_matched':5,'complete_banks_total':5,'values_matched':30,'values_total':30,'prompt_and_solution_exact':True},'grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':0},'hashes':{str(p.relative_to(ROOT)):sha(p) for p in tracked}})
 print('Validated',len(rs),'instances, all 5 complete source banks and all eligible structural slots')
if __name__=='__main__':main()
