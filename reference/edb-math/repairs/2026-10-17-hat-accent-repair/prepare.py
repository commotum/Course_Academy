"""Compose all audited hat repairs into a guarded transaction; never submits."""
import collections, difflib, hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture.scripts.database.edn import loads,dumps,kw
from scripts.question_capture.math_format import validate_prose
from repair import structured_occurrences,FLATTENED
HERE=Path(__file__).resolve().parent
E=HERE/'evidence'
def save(name,value): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str)+'\n')
def many(value): return [value] if isinstance(value,dict) else value
def prepare():
    status=json.loads((E/'status.json').read_text())
    groups={name:loads((E/(name+'.edn')).read_text()) for name in ['questions','tutorials','answers']}
    entities={v[':db/id']:v for rows in groups.values() for v in rows}
    candidates=json.loads((HERE/'candidates.json').read_text())
    expected={(c['entity'],c['attribute']):c['value'] for c in candidates}
    changes=[]
    for kind in ['structured','flattened']:
        for c in json.loads((HERE/kind/'changes.json').read_text()):
            changes.append({**c,'repair_kind':kind})
    changes.sort(key=lambda c:(c['entity'],c['attribute']))
    assert len(changes)==len(expected)
    assert {(c['entity'],c['attribute']) for c in changes}==set(expected)
    companions=json.loads((HERE/'companion/changes.json').read_text()) if (HERE/'companion/changes.json').exists() else []
    indexed={(c['entity'],c['attribute']):c for c in changes}
    for correction in companions:
        c=indexed[correction['entity'],correction['attribute']]
        assert c['after']==correction['before']
        assert correction['after'].replace('\\%', '%')==correction['before'].replace('\\%', '%')
        c['hat_only_after']=c['after']
        c['after']=correction['after']
        c['companion_proof_file']='companion/changes.json'
    findings=[]
    for c in changes:
        e,a,b,n=c['entity'],c['attribute'],c['before'],c['after']
        assert b==expected[e,a]==entities[e][a] and b!=n
        assert not structured_occurrences(n) and not FLATTENED.search(n)
        c['repaired_hat_occurrences']=len(structured_occurrences(b))+len(FLATTENED.findall(b))
        for f in entities[e].get(':question/answer-fields',[]):
            token='{{'+f[':answer-field/key']+'}}'
            assert b.count(token)==n.count(token)
        assert re.findall(r'!\[[^\]]*\]\([^)]+\)',b)==re.findall(r'!\[[^\]]*\]\([^)]+\)',n)
        # Authored math answers intentionally omit Markdown math delimiters.
        errors={}
        for stage,value in [('before',b),('after',n)]:
            try: validate_prose('$$\n'+value+'\n$$' if a==':answer/value' else value)
            except ValueError as error: errors[stage]=str(error)
        assert not errors.get('after') or errors.get('before')==errors['after'],(e,a,errors)
        if errors: findings.append({'entity':e,'attribute':a,**errors})
    answer_ids={c['entity'] for c in changes if c['attribute']==':answer/value'}
    fields={}
    for answer in groups['answers']:
        assert answer[':db/id'] in answer_ids
        assert answer[':answer/type'][':db/ident']==':answer.type/math'
        assert not answer.get(':task-item/_responses'), 'Never rewrite historical learner response values'
        for field in many(answer.get(':answer-field/_choices',[])):
            assert field[':answer-field/type'][':db/ident']==':answer-field.type/radio'
            fields[field[':db/id']]=field
    missing_keys=sorted(e for e,f in fields.items() if ':answer-field/correct' not in f)
    edits={(c['entity'],c['attribute']):c['after'] for c in changes}
    for field in fields.values():
        # Preserve incomplete imported banks; syntax repair does not invent a key.
        choices=field[':answer-field/choices']
        resulting=[(a[':answer/type'][':db/id'],edits.get((a[':db/id'],':answer/value'),a[':answer/value'])) for a in choices]
        assert len(resulting)==len(set(resulting)), 'Repair must not merge distinct answer choices'
    forms=[[kw('db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in changes]
    ensures={}
    for name,rows in groups.items():
        spec={'questions':'question/validate','tutorials':'tutorial/validate','answers':'answer/validate'}[name]
        for v in rows: ensures[v[':db/id']]=spec
    for e in fields:
        if e not in missing_keys: ensures[e]='answer-field/validate'
    forms += [[kw('db/ensure'),e,kw(spec)] for e,spec in sorted(ensures.items())]
    transaction='[\n'+'\n'.join(' '+dumps(f) for f in forms)+'\n]\n'
    assert loads(transaction)==forms
    (HERE/'transaction.edn').write_text(transaction)
    save('changes.json',changes)
    (HERE/'changes.diff').write_text(''.join(''.join(difflib.unified_diff(c['before'].splitlines(True),c['after'].splitlines(True),fromfile=str(c['entity'])+' '+c['attribute']+' before',tofile=str(c['entity'])+' '+c['attribute']+' after'))+'\n' for c in changes))
    source=loads((E/'source.edn').read_text())
    assert source[0][':db/ident']==':agent/codex'
    plan={'database':status['database'],'lineage':status['lineage'],'snapshot_basis':status['basis'],'source':':agent/codex','source_eid':source[0][':db/id'],
          'changed_attributes':len(changes),'changed_entities':len({c['entity'] for c in changes}),
          'attributes':dict(collections.Counter(c['attribute'] for c in changes)),
          'repaired_hat_occurrences':sum(c['repaired_hat_occurrences'] for c in changes),
          'repair_kinds':dict(collections.Counter(c['repair_kind'] for c in changes)),
          'transaction_sha256':hashlib.sha256(transaction.encode()).hexdigest(),'transaction_bytes':len(transaction.encode()),
          'cas_forms':len(changes),'ensure_forms':len(ensures),'answer_field_ensures':len(fields)-len(missing_keys),
          'preexisting_keyless_fields_preserved':missing_keys,'all_answer_choice_banks_distinct_after':True,
          'answer_values':len(answer_ids),'answer_values_referenced_by_historical_responses':0,
          'preexisting_structural_findings':len(findings),'database_writes':0}
    plan['companion_percent_escape_fields']=len(companions)
    plan['companion_percent_escapes']=sum(len(c['after'])-len(c['before']) for c in companions)
    save('plan.json',plan)
    save('structural-validation.json',{'passed':True,'preexisting_findings':findings,'no_new_structural_errors':True,'all_audited_defects_covered':True,'answer_placeholders_and_images_preserved':True})
    print(json.dumps(plan,indent=2))
if __name__=='__main__': prepare()
