"""Reproduce captured generated inventory with the exact archived runtime, read-only."""
import sys,json,pathlib,importlib.util,re,hashlib
sys.dont_write_bytecode=True
P=pathlib.Path(__file__).resolve().parents[1];E=P/'evidence'
spec=importlib.util.spec_from_file_location('legacy',P/'checks/legacy/17592186229182.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
inv=json.loads((P.parent/'source/inventory.json').read_text());stored={q[':question/id']:q for q in inv['questions']}
arch=json.loads((P/'17592186229182/reference/replenishment/basis-2598/generated.json').read_text())
source_ids={q[':question/id'] for q in json.loads((P.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']}
rows=[];records=[];affected=[]
for r in arch:
 gen=r['generation'];rr=g.generate(r['question'][':question/difficulty'].split('/')[-1],gen['seed']);assert rr==r
 q=rr['question'];st=stored[q[':question/id']]
 assert q[':question/id'] not in source_ids
 for k in [':question/problem',':question/worked-solution']:assert q[k]==st[k]
 f=q[':question/answer-fields'][0];sf=st[':question/answer-fields'][0]
 assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
 is_single=all(re.fullmatch('[1-9]',a[':answer/value']) for a in f[':answer-field/choices'])
 if is_single and q[':question/difficulty'].endswith('/easy'):
  affected.append(dict(question_id=q[':question/id'],entity_id=st[':db/id'],finding='Single-digit easy bank has the demonstrated second-smallest shortcut',reproduction='job Python checks/check_inventory.py; archived seed '+str(gen['seed']),evidence_path='generated-records.json'))
 rows.append(dict(question_id=q[':question/id'],entity_id=st[':db/id'],complete_record_and_generation_match_archive=True,prompt_solution_bank_match_inventory=True,single_digit=is_single));records.append(rr)
assert set(stored)-source_ids=={r['question'][':question/id'] for r in records}
(E/'generated-records.json').write_text(json.dumps(records,indent=2))
(E/'inventory-reproduction.json').write_text(json.dumps({'basis':inv['basis'],'generated_questions_tested':len(records),'source_questions_excluded':len(source_ids),'untested_generated_questions':0,'matches':rows,'limits':'Verified absence of the demonstrated single-digit shortcut in this captured generated inventory only. Input-rejection and missing-replay defects do not invalidate a stored question. Original source records are not generated inventory.'},indent=2))
for path in [P/'affected-inventory.json',E/'affected-inventory.json']:path.write_text(json.dumps({'affected_questions':affected},indent=2))
old=g.generate('easy',8114);f=old['question'][':question/answer-fields'][0];vals=sorted(int(a[':answer/value']) for a in f[':answer-field/choices']);key=next(int(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert vals==[1,3,4,5,7] and vals[1]==key
(E/'original-seed-8114.json').write_text(json.dumps([old],indent=2))
print(json.dumps({'reproduced':len(records),'affected':len(affected),'original_seed_8114':{'bank':vals,'key':key}}))
