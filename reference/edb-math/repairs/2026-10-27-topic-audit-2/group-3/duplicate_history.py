import json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;db=connection();targets=[17592186308563,17592186307984,17592186308009,17592186306650,17592186307410,17592186305867,17592186306796]
refs=db.query('[:find ?v ?e ?a :in $ [?v ...] :where [?e ?a ?v]]',[targets],H,'q334121-incoming-refs',9122);items=db.query('[:find (pull ?item [*]) :in $ ?q :where [?item :task-item/content ?q]]',[17592186308563],H,'q334121-task-items',9122);resp=db.query('[:find ?answer (pull ?item [*]) :in $ [?answer ...] :where [?item :task-item/responses ?answer]]',[targets[3:]],H,'q334121-responses',9122);(H/'q334121-reference-evidence.json').write_text(json.dumps({'basis_t':9122,'incoming_refs':refs,'current_task_items':items,'current_answer_response_refs':resp},indent=2,default=str));print('incoming',len(refs),'items',len(items),'responses',len(resp))
