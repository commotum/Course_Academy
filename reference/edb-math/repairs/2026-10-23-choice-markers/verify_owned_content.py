"""Compare complete repaired question trees immediately before/after this commit."""
import copy,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'));from migrate_learner_history import connection,loads

def main():
 db=connection();receipt=loads((HERE/'receipt.edn').read_text());fields=json.loads((HERE/'fields.json').read_text());ids=[f['entity'] for f in fields]
 query='[:find (pull ?q [* {:question/answer-fields [* {:answer-field/choices [*]} {:answer-field/correct [*]}]}]) :in $ [?q ...] :where [?q :question/id _]]'
 before=db.query(query,[ids],HERE,'owned-before',receipt[':edb/db-before-t']);after=db.query(query,[ids],HERE,'owned-after',receipt[':edb/db-after-t']);old={r[0][':db/id']:r[0] for r in before};new={r[0][':db/id']:r[0] for r in after};assert len(old)==len(new)==len(fields)
 for f in fields:
  assert old[f['entity']][':question/problem']==f['before'];expected=copy.deepcopy(old[f['entity']]);expected[':question/problem']=f['after'];assert expected==new[f['entity']],f['entity']
 report={'db_before_t':receipt[':edb/db-before-t'],'db_after_t':receipt[':edb/db-after-t'],'question_trees':len(fields),'only_problem_strings_changed':True,'all_question_ids_answer_field_ids_answer_ids_correct_links_choices_solutions_and_other_attributes_unchanged':True};(HERE/'owned-content-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
