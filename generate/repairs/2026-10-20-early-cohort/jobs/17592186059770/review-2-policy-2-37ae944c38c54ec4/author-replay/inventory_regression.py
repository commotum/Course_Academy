from pathlib import Path
#!/usr/bin/env python3
"""Retain d3a64bf2689aec595e8b without changing stored/source questions."""
import json,subprocess
import validate as v
from batch_regression import deliver,inspect

def old_select(r,template):
    f=r['question'][':question/answer-fields'][0]
    choices=[(a,v.matrix(a[':answer/value'])) for a in f[':answer-field/choices']]
    if template=='coefficient':
        picks=[a for a,m in choices if len(m[0])==3 and m[0][2]<0]
    else:
        picks=[a for a,m in choices if len(m[0])==4 and m[0][3]==0 and m[1][3]<0]
    return picks[0][':answer/id'] if len(picks)==1 else None

def main():
    run=subprocess.run([v.PY,str(Path(__file__).with_name('retrospective.py'))],capture_output=True,text=True)
    assert run.returncode==0,run.stdout+run.stderr
    originals=json.loads((v.E/'generated-records.json').read_text())
    assert len(originals)==5
    inventory=json.loads((v.W.parent/'source/inventory.json').read_text())
    source=json.loads((v.W.parent/'source/source.json').read_text())
    source_ids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
    assert all(r['question'][':question/id'] not in source_ids for r in originals)
    controls=[];replacements=[];plans=[];reports=[]
    for original in originals:
        meta=original['generation'];template=meta['template'];seed=meta['seed']
        assert old_select(original,template)==original['question'][':question/answer-fields'][0][':answer-field/correct'][1]
        roles=['correct','keep_rhs_sign','appearance_order_and_keep_rhs_sign'] if template=='coefficient' else ['correct','reverse_second_constant']
        group=[v.g.generate('moderate',seed,template,meta['parameters'],target_recipe=role) for role in roles]
        targets=set();banks=set();wins=[]
        for r in group:
            targets.add(v.witness(r));f=r['question'][':question/answer-fields'][0]
            banks.add(tuple(sorted(v.matrix(a[':answer/value']) for a in f[':answer-field/choices'])))
            wins.append(old_select(r,template)==f[':answer-field/correct'][1])
        assert len(banks)==1 and len(targets)==len(roles)
        assert sum(wins)==1,'Old sign rule must fail on contrasting targets from the identical bank'
        controls.extend(group)
        # New normally sampled signed parameters, equation/variable assignments,
        # and distinct target roles. These are candidates, with fresh owned IDs.
        candidates=v.g.generate_batch('moderate',2,seed,template)
        for r in candidates:v.witness(r)
        banks2={tuple(sorted(v.matrix(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])) for r in candidates}
        assert len(banks2)==1 and len({v.witness(r) for r in candidates})==2
        hits=sum(old_select(r,template)==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in candidates)
        assert hits<2
        replacements.extend(candidates)
        plans.append({'affected_question_id':original['question'][':question/id'],'candidate_question_ids':[r['question'][':question/id'] for r in candidates],'candidate_records':'inventory-replacement-records.json','status':'review candidates only; stored content unchanged'})
        reports.append({'affected_question_id':original['question'][':question/id'],'template':template,'historical_shortcut_reproduced':True,'same_bank_current_targets':len(targets),'old_rule_correct':sum(wins),'new_signed_candidate_targets':2,'old_rule_correct_on_new_candidates':hits})
    v.save('inventory-control-records.json',controls)
    v.save('inventory-replacement-records.json',replacements)
    accepted,cmd=deliver(v.E/'inventory-replacement-records.json',v.E/'inventory-replacement-delivery','moderate')
    assert len(accepted)==10
    for r in accepted:v.witness(r)
    # Generic fixed-bank proof, independent of source-template metadata.
    by_bank={}
    for r in accepted:
        f=r['question'][':question/answer-fields'][0]
        key=tuple(v.matrix(a[':answer/value']) for a in f[':answer-field/choices'])
        by_bank.setdefault(key,[]).append(v.witness(r))
    assert all(len(set(ts))==2 for ts in by_bank.values())
    cases=[]
    for r in controls+accepted:
        target=v.witness(r)
        cases.append({'label':'legacy-inventory-role-repair','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if v.matrix(a[':answer/value'])==target else 'rejected','purpose':'exact legacy parameter controls and signed varied-role replacement candidates'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
    v.save('inventory-native-input.json',cases)
    run=subprocess.run([str(v.REPO/'generate/runs/current/check-engine'),str(v.E/'inventory-native-input.json'),str(v.E/'inventory-native-report.json')],capture_output=True,text=True)
    assert run.returncode==0,run.stdout+run.stderr
    v.save('inventory-replacement-plan.json',{'finding_id':'d3a64bf2689aec595e8b','affected_questions':plans,'publication_performed':False})
    v.save('inventory-regression.json',{'finding_id':'d3a64bf2689aec595e8b','status':'passed','inventory_basis':inventory['basis'],'originals_reproduced':5,'original_source_ids_excluded':True,'cases':reports,'replacement_delivery_command':cmd,'replacement_records_accepted':len(accepted),'native_checks':5*len(cases),'limits':'All five captured generated instances exactly replayed. Source records excluded, not certified shortcut-free. Database remains unchanged; replacements await runner review/publication.'})
    print('d3a64bf2689aec595e8b passed: 5 exact stored replays; 13 changed-target controls; 10/10 signed replacement candidates delivered; 115 native checks')

if __name__=='__main__':main()
