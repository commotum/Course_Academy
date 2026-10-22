"""Reproduce stored generated records using the retained original implementation."""
import importlib.util,json
from pathlib import Path
from check_repair import E,HERE,inspect,save

def main():
    spec=importlib.util.spec_from_file_location('legacy',E/'legacy-generator.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    inventory=json.loads((HERE.parent/'source/inventory.json').read_text())['questions']
    historical=json.loads((HERE/'17592186119847/reference/replenishment/basis-2639/generated.json').read_text())
    source=json.loads((HERE.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];source_ids={q[':question/id'] for q in source}
    historical_ids={r['question'][':question/id']:r for r in historical}
    affected=[];reproduced=[];checks=[]
    for q in inventory:
        qid=q[':question/id']
        if qid in source_ids:
            checks.append({'question_id':qid,'classification':'original source; not marked generated'});continue
        assert qid in historical_ids,'Untested generated inventory record'
        record=historical_ids[qid];meta=record['generation']
        again=old.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],meta['seed'])
        assert again==record,'Legacy seed replay mismatch'
        assert again['question'][':question/id']==qid
        assert again['question'][':question/problem']==q[':question/problem']
        assert again['question'][':question/worked-solution']==q[':question/worked-solution']
        sf=q[':question/answer-fields'][0];gf=again['question'][':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
        assert next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
        reproduced.append(again);fact=inspect(again)
        finding=None
        if meta['bank_profile']=='q-79405':
            # Legacy bank [r-1,n,r,r+1,m]; feasibility and distinctness force
            # n and m above r+1. Thus rank is always second smallest.
            assert fact['numerical_order']==1
            finding='Legacy q-79405 generated bank always makes rank the second-smallest option, independently of the supplied pivot count.'
            affected.append({'question_id':qid,'entity_id':q[':db/id'],'finding':finding,'reproduction':'python check_inventory.py (legacy.generate easy seed=2068592730; profile=q-79405; name=A rows=12 columns=7 count=1 kind=pivot)','evidence_path':'../workspace/evidence/generated-records.json'})
        checks.append({'question_id':qid,'classification':'historical generated record reproduced exactly','profile':meta['bank_profile'],'finding':finding})
    save('generated-records.json',reproduced)
    (HERE/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
    save('inventory-audit.json',{'inventory_records':len(inventory),'source_records':len(source_ids),'historical_generated_reproduced':len(reproduced),'affected_records':len(affected),'checks':checks,'limits':['Silent batch truncation cannot itself affect a stored individual record.','No key/math defect was demonstrated in the two stored generated records.','Fixed numerical-order weakness demonstrated for the stored q-79405 profile; other probabilistic learner shortcuts are not exhaustively excluded.','Original source records are excluded from affected generated-instance claims.']})
    print(json.dumps({'inventory':len(inventory),'generated_reproduced':len(reproduced),'affected':len(affected)}))
if __name__=='__main__':main()
