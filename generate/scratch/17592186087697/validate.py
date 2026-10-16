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
  elif 'do not lie on the main diagonal are not zeros' in bullet or 'off the main diagonal is nonzero' in bullet:
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
 evidence=HERE/'structural-fix';evidence.mkdir(exist_ok=True)
 records=[];coverage={}
 for mid,t in g.TEMPLATES.items():
  replay=g.generate(template=mid,parameters=t['parameters']);independent(replay);records.append(replay)
  assert replay['question'][':question/problem']==t['problem'] and replay['question'][':question/worked-solution']==t['worked_solution']
  for mask in range(8):
   r=g.generate(seed=720+mask,template=mid,selection=mask);independent(r);assert r['generation']['selection']==mask;records.append(r)
  sampled=[g.generate(seed=i,template=mid) for i in range(200)]
  for r in sampled:independent(r)
  masks={r['generation']['selection'] for r in sampled};assert masks==set(range(8))
  roles=[sorted({r['generation']['roles'][i] for r in sampled}) for i in range(3)]
  assert all(set(slot)=={'identity','diagonal','rectangular','offdiagonal'} for slot in roles)
  coverage[mid]={'samples':len(sampled),'selections':sorted(masks),'roles_per_label':dict(zip(t['labels'],roles))}
  records.extend(sampled)
 # Hold dimensions, labels and other matrices constant; change only F's
 # off-diagonal entry. The answer must change from H,M to F,H,M.
 p={'matrices':[[['2','1'],['0','3']],[['0','0'],['0','1']],[['2','0'],['0','3']]],'witnesses':[[1,2],None,None]}
 before=g.generate(template='q-68744',parameters=p);independent(before)
 changed=copy.deepcopy(p);changed['matrices'][0][0][1]='0';changed['witnesses'][0]=None
 after=g.generate(template='q-68744',parameters=changed);independent(after)
 assert before['generation']['selection']==6 and after['generation']['selection']==7
 for mutation in ('solution','key','prompt'):
  bad=copy.deepcopy(after['question'])
  if mutation=='solution':bad[':question/worked-solution']=before['question'][':question/worked-solution']
  elif mutation=='prompt':bad[':question/problem']=before['question'][':question/problem']
  else:
   f=bad[':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']=='false')
  try:solution_check(bad)
  except AssertionError:pass
  else:raise AssertionError('Stale '+mutation+' escaped')
 records.extend([before,after])
 # Identity is a subset of diagonal; the all-zero matrix is diagonal but not identity.
 boundary={'matrices':[[['0','0'],['0','0']],[['1','0'],['0','1']],[['1','0'],['0','0']]],'witnesses':[None,None,None]}
 for template,expected in [('q-68744',7),('q-68741',2)]:
  r=g.generate(template=template,parameters=boundary);independent(r);assert r['generation']['selection']==expected;records.append(r)
 for key in ('negative','oversized','bad_witness','selection'):
  bad=copy.deepcopy(p);kw={}
  if key=='negative':bad['matrices'][0][0][0]='-4'
  elif key=='oversized':bad['matrices'][0]=[['1']*5 for _ in range(2)]
  elif key=='bad_witness':bad['witnesses'][0]=[2,1]
  else:kw['selection']=7
  try:g.generate(template='q-68744',parameters=bad,**kw)
  except ValueError:pass
  else:raise AssertionError('Invalid parameters accepted: '+key)
 batch=[g.generate(seed=20261016+mask,template=mid,selection=mask) for mid in ('q-68744','q-68741') for mask in range(8)]
 for r in batch:independent(r)
 assert len({r['generation']['parameter_fingerprint'] for r in batch})==16
 records.extend(batch)
 # Replay all original boolean banks and correct designations from saved source.
 source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for mid,t in g.TEMPLATES.items():
  q=qs[mid];fresh=g.generate(template=mid,parameters=t['parameters'])['question'];solution_check(q)
  for f in fresh[':question/answer-fields']:
   old=next(x for x in q[':question/answer-fields'] if x[':answer-field/key']==f[':answer-field/key'])
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices'])
   assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==old[':answer-field/correct'][':answer/value']
 build_engine()
 (evidence/'native-input.json').write_text(json.dumps([{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)]))
 subprocess.run([str(HERE/'check-engine'),str(evidence/'native-input.json'),str(evidence/'native-report.json')],check=True)
 native=json.loads((evidence/'native-report.json').read_text());assert native['documented_unresolved_checks']==0
 (evidence/'batch.json').write_text(json.dumps(batch,indent=2))
 (evidence/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in batch))
 result={'passed':True,'version':g.VERSION,'records_checked':len(records),'coverage':coverage,'source_banks_replayed':5,'source_boolean_choices_replayed':30,'controlled_single_entry_classification_change':True,'native_grading':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),Path(__file__),HERE/'templates.json',HERE/'check-engine']}}
 (evidence/'validation.json').write_text(json.dumps(result,indent=2))
 print(json.dumps({'passed':True,'records':len(records),'source_replays':5,'selection_masks_per_template':8,'native_grading':result['native_grading']}))

if __name__=='__main__':main()
