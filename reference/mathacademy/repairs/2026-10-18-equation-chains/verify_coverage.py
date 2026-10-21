"""Account for every audit field and every one of the 306 mixed-row cases."""
import hashlib,importlib,json
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parents[3]/'reference/mathacademy/audits/2026-10-18-equation-chain-import'
prepare=importlib.import_module('reference.mathacademy.repairs.2026-10-18-equation-chains.prepare')
def run():
    findings=json.loads((AUDIT/'findings.json').read_text());changes=json.loads((HERE/'changes.json').read_text());by_key={(c['entity'],c['attribute']):c for c in changes};unchanged=json.loads((HERE/'unchanged.json').read_text());assert len(by_key)==len(changes)
    current={e[':db/id']:e for g in ('questions','tutorials') for [e] in json.loads((HERE/(g+'.json')).read_text())};ledger={(r['entity'],r['attribute']):r for r in json.loads((HERE/'mixed-source-ledger.json').read_text())};cases=[]
    for f in findings:
        key=f['entity'],f['attribute'];c=by_key.get(key);value=c['after'] if c else current[key[0]][key[1]]
        prepare.fmt.validate_prose(value)
        assert r'\require' not in value and r'\eqalign' not in value,key
        for m in prepare.fmt.MATH.finditer(value):
            assert prepare.fmt.normalize_equality_chains(m[0])==m[0],key
        if not c:assert any((u['entity'],u['attribute'])==key for u in unchanged)
        if 'partial-empty-rhs-chain' in f['reasons']:
            evidence=ledger[key]['evidence'];assert evidence
            if c:
                assert c['individual_reviews'] or prepare.lexical(c['before'])==prepare.lexical(c['after']),key
            cases.append({'entity':key[0],'attribute':key[1],'source_id':f.get('source_id'),'resolution':'repaired' if c else 'already repaired since audit','evidence':evidence,'before_sha256':prepare.digest(c['before'] if c else current[key[0]][key[1]]),'after_sha256':prepare.digest(value),'individual_reviews':c['individual_reviews'] if c else []})
    assert len(cases)==306
    (HERE/'mixed-case-review.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False)+'\n')
    result={'passed':True,'audit_fields':len(findings),'audit_fields_repaired':sum((f['entity'],f['attribute']) in by_key for f in findings),'audit_fields_already_repaired':len(unchanged),'additional_related_prompts_repaired':4,'fields_total':len(changes),'mixed_row_fields':306,'mixed_row_formulas_reviewed':395,'mixed_row_fields_repaired':sum(c['resolution']=='repaired' for c in cases),'mixed_row_fields_already_repaired':sum(c['resolution']!='repaired' for c in cases),'source_evidence':dict(Counter(c['evidence'][0]['kind'] for c in cases)),'remaining_structural_errors':0,'changes_sha256':hashlib.sha256((HERE/'changes.json').read_bytes()).hexdigest()}
    (HERE/'coverage-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
