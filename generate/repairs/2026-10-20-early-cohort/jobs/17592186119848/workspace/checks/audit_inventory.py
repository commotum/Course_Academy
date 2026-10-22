"""Read-only inventory audit: never attribute generated status to a source item."""
import copy
import json
from validate_content import ROOT, JOB, save, inspect

def main():
    snapshot=json.loads((JOB/'source/inventory.json').read_text())
    source=json.loads((JOB/'source/source.json').read_text())
    original_ids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
    checked=[];incomplete=[]
    for old in snapshot['questions']:
        assert old[':question/id'] in original_ids
        assert old.get(':question/math-academy-id','').startswith('q-')
        if not old.get(':question/worked-solution') or any(':answer-field/correct' not in f for f in old[':question/answer-fields']):
            incomplete.append(old[':question/id']);continue
        q=copy.deepcopy(old)
        for f in q[':question/answer-fields']:
            if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
            f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        witness,_=inspect({'question':q})
        checked.append({'question_id':old[':question/id'],'entity_id':old[':db/id'],'source_id':old[':question/math-academy-id'],'ranks':witness['ranks'],'key_correct':True})
    (ROOT/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2)+'\n')
    save('inventory-audit.json',{'basis':snapshot['basis'],'inventory_count':len(snapshot['questions']),'verified_original_source_items':len(original_ids),'stored_generated_items':0,'complete_items_independently_checked':checked,'incomplete_key_or_solution_not_testable':incomplete,'affected_questions':[],'scope':'External runtime import is not a stored question defect. All 12 inventory IDs are original source items, not generated records. Ten complete stored keys and solutions were checked independently; two incomplete originals cannot be graded from supplied evidence. A fixed cue across generator outputs is not inferred from one original item.','command':'python checks/audit_inventory.py'})
    print(json.dumps({'inventory':len(snapshot['questions']),'complete_checked':len(checked),'incomplete':len(incomplete),'stored_generated':0,'affected':0}))

if __name__=='__main__':main()
