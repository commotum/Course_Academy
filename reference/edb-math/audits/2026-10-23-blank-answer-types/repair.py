"""Preview, commit and read back the exact five user-authorized type-only CASes."""
import collections,copy,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection,kw,loads
QP='[:find (pull ?q [* {:question/difficulty [:db/ident]} {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/correct [* {:answer/type [:db/ident]}]} {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]) :in $ [?q ...] :where [?q :question/id _]]'
AP='[:find (pull ?a [* {:answer/type [:db/ident]}]) :in $ [?a ...] :where [?a :answer/id _]]'
def save(name,v):(H/name).write_text(json.dumps(v,default=str,indent=2)+'\n')
def check_report(r,changes,committed):
 assert r[':edb/committed'] is committed;ds=r[':edb/tx-data'];expected=collections.Counter([(c['answer'],17592186045499,False) for c in changes]+[(c['answer'],17592186045498,True) for c in changes]);ids={c['answer'] for c in changes};assert collections.Counter((d[0],d[2],d[-1]) for d in ds if d[0] in ids)==expected;assert len(ds)==2*len(changes)+1;assert all(d[-2]==17592186576411 for d in ds)

def expected_answers(rows,ids):
 result=copy.deepcopy(rows)
 for row in result:
  if row[0][':db/id'] in ids:row[0][':answer/type'][':db/ident']=kw('answer.type/math')
 return result

def expected_trees(rows,ids):
 result=copy.deepcopy(rows)
 for row in result:
  for f in row[0][':question/answer-fields']:
   for a in f[':answer-field/choices']+[f[':answer-field/correct']]:
    if a[':db/id'] in ids:a[':answer/type'][':db/ident']=kw('answer.type/math')
 return result

def main():
 assert sys.argv[1:] in (['--preview'],['--apply-user-authorized']);changes=json.load(open(H/'changes.json'));reviews=json.load(open(H/'individual-review.json'));assert len(changes)==5 and len(reviews)==48;ids={c['answer'] for c in changes};all_ids=sorted({c['answer'] for c in reviews}|{17592186232881});qids=sorted({q for c in changes for q in c['questions']}|{17592186233932});db=connection();sha=hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest();forms=loads((H/'transaction.edn').read_text());assert forms==[[kw('db/cas'),c['answer'],kw('answer/type'),kw('answer.type/text'),kw('answer.type/math')] for c in changes]
 if sys.argv[1]=='--preview':
  basis=db.basis();trees=db.query(QP,[qids],H,'preflight-trees',basis);answers=db.query(AP,[all_ids],H,'preflight-answers',basis);lookup={r[0][':db/id']:r[0] for r in answers};assert len(lookup)==49
  for c in changes:assert lookup[c['answer']][':answer/type'][':db/ident']==':answer.type/text' and lookup[c['answer']][':answer/value']==c['value']
  assert lookup[17592186232881][':answer/type'][':db/ident']==':answer.type/math'
  text=db.command('with','--source',':agent/codex','--file',H/'transaction.edn');(H/'preview.edn').write_text(text);p=loads(text);check_report(p,changes,False);save('preview-verification.json',{'sha256':sha,'basis_t':basis,'exact_type_only_diff_verified':True,'types_to_change':5,'text_types_to_preserve':43,'known_fixed_example_preserved':True,'committed':False});print('Preview verified: exactly five answer/type changes; original example stays math.');return
 proof=json.load(open(H/'preview-verification.json'));assert proof['sha256']==sha and proof['exact_type_only_diff_verified'];assert json.load(open(H/'ui-verification.json'))['passed'];grade=json.load(open(H/'grading-report.json'));assert grade['accepted_checks']==5 and grade['rejected_checks']==5 and grade['documented_unresolved_checks']==0
 intent={'database':'math','source':':agent/codex','endpoint':'/tmp/edb-math/writer.sock','file':str(H/'transaction.edn'),'sha256':sha,'request_key':'repair-blank-answer-types-2026-10-23-'+sha[:24]}
 if (H/'commit-intent.json').exists():assert json.load(open(H/'commit-intent.json'))==intent
 else:save('commit-intent.json',intent)
 receipt=None
 if (H/'receipt.edn').exists():
  try:receipt=loads((H/'receipt.edn').read_text())
  except ValueError:pass
 if not isinstance(receipt,dict) or receipt.get(':edb/committed') is not True:
  save('submission-started.json',{'at':datetime.now(timezone.utc).isoformat(),'intent':intent,'authorization':'User requested audit and correction of mathematical blank answers typed as text, preserving values, identities, field links and history; continuing authorized database repair work.'})
  command=[db.args.edb_bin,'transact','--database','math','--source',intent['source'],'--file',intent['file'],'--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000']
  with (H/'receipt.edn').open('w') as out,(H/'submit.stderr').open('w') as err:subprocess.run(command,env=db.env,stdout=out,stderr=err,timeout=160,check=True)
  receipt=loads((H/'receipt.edn').read_text())
 check_report(receipt,changes,True);basis=receipt[':edb/db-after-t'];before_basis=receipt[':edb/db-before-t'];before=db.query(QP,[qids],H,'at-commit-trees-before',before_basis);after=db.query(QP,[qids],H,'trees-after',basis);assert after==expected_trees(before,ids)
 previous=db.query(AP,[all_ids],H,'at-commit-answers-before',before_basis);current=db.query(AP,[all_ids],H,'answers-after',basis);assert current==expected_answers(previous,ids);assert len(current)==49
 report={'committed':True,'database':'math','basis_t':basis,'blank_fields_audited':18849,'text_correct_answers_reviewed':48,'answer_types_corrected':5,'affected_questions':4,'text_answers_retained':43,'existing_example_unchanged':True,'complete_question_field_answer_trees_verified':True,'values_ids_links_and_learner_state_preserved':True,'only_answer_type_and_transaction_metadata_changed':True,'request_key':intent['request_key'],'sha256':sha};save('verification.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
