"""Read-only final census reconciliation and presentation audit."""
import argparse,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('lint',ROOT/'skills/radio2checkbox/scripts/lint_presentation.py');lint=importlib.util.module_from_spec(spec);spec.loader.exec_module(lint)
def read(path):return json.loads(path.read_text())
def canon(value):
 if isinstance(value,dict):return {k:canon(v)for k,v in sorted(value.items())if k!=':task-item/_responses'}
 if isinstance(value,list):return sorted((canon(v)for v in value),key=lambda x:json.dumps(x,sort_keys=True))
 return value
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--census',type=Path,default=HERE/'final-census');args=parser.parse_args()
 out=args.census;current={q[':db/id']:q for q in read(out/'questions.json')};original={q[':db/id']:q for q in read(HERE/'questions.json')}
 expected={};batches=read(HERE/'confirmed-batches.json');changed_pairs=set();datoms=0
 for b in batches:
  directory=HERE/b['directory']
  assert read(directory/'commit-verification.json')['passed']
  for c in read(directory/'cases.json')['cases']:expected[c['question']]=c
  for c in read(directory/'changes.json'):changed_pairs.add((c['entity'],c['attribute']))
  datoms+=b['exact_datoms']
 already={r['question']for r in read(HERE/'other-ledger.json')if r['status']=='already-complete'}
 new=sorted(set(current)-set(original));missing=sorted(set(original)-set(current));findings=[];mismatches=[]
 for qid,c in expected.items():
  if qid not in current:continue
  q=current[qid];a=c['after']
  for attr in [':question/problem',':question/worked-solution']:
   if q.get(attr)!=a.get(attr):mismatches.append({'question':qid,'attribute':attr})
  if canon(q[':question/answer-fields'])!=canon(a[':question/answer-fields']):mismatches.append({'question':qid,'attribute':':question/answer-fields'})
  findings+=lint.lint_question(q,c['objects'])
 for qid in already:
  q=current[qid];old=original[qid]
  assert canon(q[':question/answer-fields'])==canon(old[':question/answer-fields'])
  objects=[{'field_id':f[':db/id'],'source_label':'existing-'+str(f[':db/id']),'content':f[':answer-field/key']}for f in q[':question/answer-fields']]
  findings+=lint.lint_question(q,objects)
 unresolved=sorted(set(original)-set(expected)-already)
 result={'passed':not(new or missing or unresolved or findings or mismatches),'initial_basis':3704,'final_basis':read(out/'audit-summary.json')['basis'],'audited_questions':len(current),'repaired_questions':len(expected),'already_complete_questions':len(already),'repaired_checkbox_fields':sum(len(c['objects'])for c in expected.values()),'distinct_changed_entity_attributes':len(changed_pairs),'confirmed_transaction_datoms':datoms,'confirmed_batches':len(batches),'new_question_ids':new,'missing_question_ids':missing,'unresolved_original_ids':unresolved,'authored_value_or_bank_mismatches':mismatches,'presentation_findings':findings,'all_confirmed_receipts_verified':True,'generator_changes':False}
 (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
 (HERE/'final-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
 assert result['passed'],'Final census needs reconciliation'
if __name__=='__main__':main()
