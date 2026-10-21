"""Summarize confirmed receipts and keep a resumable per-question ledger."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def save(path,value):
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');tmp.replace(path)
def main():
 questions=json.loads((HERE/'questions.json').read_text());ledger={q[':db/id']:{'question':q[':db/id'],'fields':len(q[':question/answer-fields']),'status':'pending','evidence':[]}for q in questions}
 for r in json.loads((HERE/'other-ledger.json').read_text()):
  if r['status']=='already-complete':ledger[r['question']].update({'status':'already-complete','reason':r['evidence']})
 batches=[];pending_verification=[]
 for receipt in sorted((HERE/'batches').glob('*/attempt-*/receipt.edn')):
  if not(receipt.parent/'commit-verification.json').exists():pending_verification.append(str(receipt.parent.relative_to(HERE)))
 for file in sorted((HERE/'batches').glob('*/attempt-*/commit-verification.json')):
  receipt=json.loads(file.read_text());assert receipt['passed']and receipt['committed']
  directory=file.parent;cases=json.loads((directory/'cases.json').read_text())['cases']
  batches.append({'directory':str(directory.relative_to(HERE)),**receipt})
  for case in cases:
   row=ledger.setdefault(case['question'],{'question':case['question'],'fields':len(case['objects']),'status':'pending','evidence':[]})
   row['status']='committed';row['evidence'].append(str(directory.relative_to(HERE)));row['confirmed_basis']=receipt['basis_after']
 batches.sort(key=lambda r:r['basis_after'])
 complete=[q for q in ledger.values()if q['status']=='committed'];pending=[q['question']for q in ledger.values()if q['status']=='pending']
 summary={'initial_basis':3704,'audited_questions':len(questions),'question_checkbox_fields':sum(q['fields']for q in ledger.values()),'confirmed_repaired_questions':len(complete),'confirmed_repaired_fields':sum(q['fields']for q in complete),'already_complete_questions':sum(q['status']=='already-complete'for q in ledger.values()),'pending_questions':len(pending),'confirmed_batches':len(batches),'latest_confirmed_basis':batches[-1]['basis_after']if batches else None,'all_existing_question_repairs_confirmed':not pending,'generator_scope':'Inventoried separately; no generator source/package publication in these transactions.'}
 summary['confirmed_receipts_awaiting_verification']=pending_verification
 save(HERE/'case-ledger.json',sorted(ledger.values(),key=lambda q:q['question']));save(HERE/'remaining-question-ids.json',sorted(pending));save(HERE/'confirmed-batches.json',batches);save(HERE/'status.json',summary)
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
