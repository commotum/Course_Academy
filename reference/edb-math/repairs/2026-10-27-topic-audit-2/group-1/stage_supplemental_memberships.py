import hashlib,json,re
from pathlib import Path
from bs4 import BeautifulSoup

H=Path(__file__).resolve().parent
evidence=json.loads((H/'supplemental-membership-evidence.json').read_text())
sources=json.loads((H/'source-control-reconstructions.json').read_text())
fields={f[':db/id']:f for f in evidence['current_fields']}
attributes={a[':db/id']:a[':db/ident']for a in evidence['attributes']}
incoming={(r['answer'],r['history']):r['rows']for r in evidence['incoming']}
proposals=[];checks=[]

for question,field,answer in [(17592186299693,17592186299291,17592186298622),(17592186299852,17592186299462,17592186297713)]:
    source=next(q for q in sources if q['entity']==question)
    current_field=fields[field];bank=current_field[':answer-field/choices']
    before=sorted(a[':db/id']for a in bank);after=[a for a in before if a!=answer]
    leak=next(a for a in bank if a[':db/id']==answer)
    current=incoming[answer,False];history=incoming[answer,True]
    assert current==[[field,1075]]
    assert all(row[0]==field and row[1]in[1075,1078]for row in history)
    assert current_field[':answer-field/correct'][':db/id']in after
    assert len(before)==5 and len(after)==4
    original=[];canonical=lambda value:re.sub(r'\s+','',value)
    for option in source['options']:
        criterion=next(c for c in option['controls']if c['key']=='field-1')
        path=Path(option['path']);capture=json.loads(path.read_text())
        html=capture.get('html')or capture.get('raw_html');assert html
        control=BeautifulSoup(html,'html.parser').find(id=criterion['dom_id']);assert control is not None
        nodes=control.find_all(class_='selectListOption')
        assert len(nodes)==len(criterion['values'])==4
        assert all('is exact'not in n.get_text(' ',strip=True)and'is not'not in n.get_text(' ',strip=True)for n in nodes)
        retained={canonical(a[':answer/value'])for a in bank if a[':db/id']!=answer}
        assert retained=={canonical(v)for v in criterion['values']}
        verdict=option['controls'][-1]
        assert verdict['key']=='field-7'and leak[':answer/value']in verdict['values']
        original.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'criterion_dom_id':criterion['dom_id'],'raw_selectListOption_count':len(nodes),
            'criterion_values':criterion['values'],'criterion_values_match_retained_current_four':True,
            'separate_verdict_control':{'key':verdict['key'],'dom_id':verdict['dom_id'],'values':verdict['values']},
            'spurious_value_absent_from_criterion_options':True})
    assert len(original)==2
    proof={'basis_t':evidence['basis_t'],'question':question,'identity':source['identity'],
        'original_banks':original,
        'current_bank':[{'entity':a[':db/id'],'identity':a[':answer/id'],'type':a[':answer/type'][':db/ident'],'value':a[':answer/value']}for a in bank],
        'current_correct_answer':current_field[':answer-field/correct'][':db/id'],
        'current_incoming_refs':[{'entity':r[0],'attribute':attributes[r[1]]}for r in current],
        'retained_history_incoming_refs':[{'entity':r[0],'attribute':attributes[r[1]],'transaction':r[2],'source':r[3],'added':r[4]}for r in history],
        'current_response_reference_count':0,'retained_historical_response_reference_count':0,
        'other_current_or_historical_owners':[],'response_attribute_schema':evidence['response_schema'],
        'retention_limit':evidence['limits'],'complete_readback':'supplemental-membership-evidence.json'}
    transaction=[':db/retract',field,':answer-field/choices',answer]
    proposals.append({'entity':field,'attribute':':answer-field/choices','before':before,'after':after,
        'operation':'retract-member','retract_value':answer,'transaction_form':transaction,'basis_guard':evidence['basis_t'],
        'reason':'Remove one unused capture/default-leak choice membership. Both original captures contain exactly four mathematical criterion options; this prose verdict belongs to the separate final control. Preserve the answer entity, identity, type, value, corrected key and every retained history event.',
        'evidence':proof,'confidence':'high'})
    checks.append({'field':field,'answer':answer,'source_capture_count':len(original),'retained_option_count':4,
        'current_or_historical_response_refs':0,'other_owners':0,'correct_key_retained':True,'only_mutation':transaction})

(H/'supplemental-membership-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n')
(H/'supplemental-membership-validation.json').write_text(json.dumps({'passed':True,'basis_t':evidence['basis_t'],
    'operations':checks,'database_writes':0,'scope':'Two memberships only; all entities, values, types and retained histories preserved.'},indent=2)+'\n')
print('Staged',len(proposals),'membership-only retractions at T'+str(evidence['basis_t']))
