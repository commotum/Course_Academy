"""Reproduce historical records with the retained old runtime; read-only inventory."""
import importlib.util,json,pathlib,re,sys
sys.dont_write_bytecode=True
P=pathlib.Path(__file__).resolve().parents[1];E=P/'evidence'
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
s=importlib.util.spec_from_file_location('old',E/'old/17592186078584.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
inv=load(P.parent/'source/inventory.json');stored={q[':question/id']:q for q in inv['questions']}
originals=load(P.parent/'source/source.json')['material']['kp'][':knowledge-point/questions'];source_ids={q[':question/id'] for q in originals}
history=load(P/'17592186078584/reference/replenishment/basis-2501/generated.json')
def norm(s):return re.sub(r'\s+','',s.replace(r'\left','').replace(r'\right','').replace(r'\,',''))
def num(a):return int(re.search(r'\d+',a[':answer/value'])[0])
records=[];tested=[];affected=[]
for record in history:
 meta=record['generation'];level=record['question'][':question/difficulty'].split('/')[-1]
 candidates=[old.generate(level,meta['seed']),old.generate(level,meta['seed'],meta['template'])]
 assert record in candidates,'Historical metadata no longer reproduced'
 r=next(r for r in candidates if r==record);q=r['question'];qid=q[':question/id'];stored_q=stored[qid];assert qid not in source_ids
 f=q[':question/answer-fields'][0];sf=stored_q[':question/answer-fields'][0]
 actual=next(num(a) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 rank=sorted(num(a) for a in f[':answer-field/choices']).index(actual)+1
 assert norm(q[':question/problem'])==norm(stored_q[':question/problem'])
 assert norm(q[':question/worked-solution'])==norm(stored_q[':question/worked-solution'])
 assert sorted(num(a) for a in f[':answer-field/choices'])==sorted(num(a) for a in sf[':answer-field/choices'])
 assert actual==num(sf[':answer-field/correct'])
 records.append(r);tested.append(dict(question_id=qid,entity_id=stored_q[':db/id'],rank=rank,complete_record_reproduced=True))
 if rank==4 and level in ['moderate','hard']:
  affected.append(dict(question_id=qid,entity_id=stored_q[':db/id'],finding='Historical target-time bank fixes the correct time at numeric rank four (second largest), bypassing calibration and logarithmic inversion.',reproduction=f'/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/inventory.py; frozen generate({level!r}, seed={meta["seed"]}, template={meta["template"]!r}); see generation metadata in generated-records.json',evidence_path='../workspace/evidence/generated-records.json'))
assert len(affected)==7
save('generated-records.json',records);save('affected-inventory.json',dict(affected_questions=affected));save('inventory-results.json',dict(basis=inv['basis'],inventory_count=len(stored),source_count=len(source_ids),tested_generated=len(tested),tested=tested,untested_generated_ids=sorted(set(stored)-source_ids-{r['question'][':question/id'] for r in records}),source_questions_excluded=True,note='Paths in affected-inventory.json are relative to the supplied author-1 evidence_root and resolve into the writable workspace. Original source questions are not marked generated.'))
print(json.dumps(dict(affected=len(affected),tested=len(tested),untested_generated=len(set(stored)-source_ids-{r['question'][':question/id'] for r in records}))))
