import hashlib
import json
from pathlib import Path

SOURCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy')
OUT = Path('/tmp/newer-captures-prepared')
archive = SOURCE/'mathematical-corrections'
events = {}
for path in sorted(archive.rglob('review.json')):
    directory = path.parent
    verification = directory/'verification.json'
    transaction = directory/'transaction.edn'
    if not verification.exists() or not transaction.exists():
        continue
    review = json.loads(path.read_text())
    proof = json.loads(verification.read_text())
    assert proof.get('committed') and proof.get('mathematical_check_passed'), str(path)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == proof['review_sha256'], str(path)
    assert hashlib.sha256(transaction.read_bytes()).hexdigest() == proof['transaction_sha256'], str(path)
    mid = review.get('question') or review['question_id']
    key = mid, proof['basis_after']
    event = {'question':mid, 'old_basis':proof['basis_after'], 'review_path':str(path),
             'verification_path':str(verification), 'old_transaction_path':str(transaction),
             'original_content':review['original_content'], 'corrected_content':review['corrected_content'],
             'rationale':review.get('rationale'), 'review_sha256':proof['review_sha256'],
             'transaction_sha256':proof['transaction_sha256']}
    if key not in events or len(path.parts) < len(Path(events[key]['review_path']).parts):
        events[key] = event
events = sorted(events.values(),key=lambda x:(x['old_basis'], x['question']))
def keys(q):
    return {f['key']: f.get('correct_value') for f in q.get('answer_fields',[])}
for event in events:
    original, corrected = event['original_content'], event['corrected_content']
    event['answer_key_changed'] = keys(original) != keys(corrected)
    event['changed_attributes'] = [k for k in ['problem','worked_solution','answer_fields'] if original.get(k) != corrected.get(k)]
current = {e['question']:e for e in events}
reconciliations = []
inventory = json.loads(Path('/tmp/newer-captures-inventory.json').read_text())
for activity in inventory['activities']:
    file = Path(activity['path'])/'edb-import/replacement-report.json'
    if not file.exists():continue
    report = json.loads(file.read_text())
    def walk(value):
        if isinstance(value,dict):
            if (value.get('attribute') in ['answer-field/correct', ':answer-field/correct']
                    and value.get('action')=='replace'):
                reconciliations.append({'task':activity['task'],'stream':activity['stream'],'old_basis':activity['basis'],'report_path':str(file),'decision':value})
            for v in value.values():walk(v)
        elif isinstance(value,list):
            for v in value:walk(v)
    walk(report)
(OUT/'correction-events.json').write_text(json.dumps({'events':events},ensure_ascii=False,indent=2)+'\n')
(OUT/'answer-reconciliations.json').write_text(json.dumps({'decisions':reconciliations},ensure_ascii=False,indent=2)+'\n')
lines = ['# Newer capture correction review','',
         'Preparation only. Nothing in this migration has been transacted. All original Math Academy content must be committed first with `:org/Math-Academy` as source. Corrections follow on the same question entities, with the assistant source entity that will be created later. Jake is not the correction source.','',
         f'The saved mathematical-correction archive contains {len(current)} affected entities and {len(events)} distinct verified correction events, including earlier versions. Each event is bound to its reviewed content and old transaction by the saved verification hashes. Old transactions contain old entity IDs and are evidence, not files to replay.','',
         '## Changes to canonical answer values','',
         'These are exact string comparisons. Unit and notation changes are included; this count is not a count of mathematical errors.','']
changes=[e for e in current.values() if e['answer_key_changed']]
for e in sorted(changes,key=lambda x:x['question']):
    lines += [f"### {e['question']} — old basis {e['old_basis']}",'',f"Original MA: `{json.dumps(keys(e['original_content']),ensure_ascii=False)}`",'',f"Reviewed correction: `{json.dumps(keys(e['corrected_content']),ensure_ascii=False)}`",'',e['rationale'] or '', '',f"[Review]({e['review_path']}) · [Old transaction]({e['old_transaction_path']}) · [Verification]({e['verification_path']})",'']
lines += ['## All reviewed correction events','', '| Entity | Old basis | Changed content | Evidence |','|---|---:|---|---|']
for e in events:
    lines.append(f"| {e['question']} | {e['old_basis']} | {', '.join(e['changed_attributes'])} | [review]({e['review_path']}) |")
lines += ['', '## Answer-source reconciliations','',
          f'{len(reconciliations)} saved replacement decisions for `answer-field/correct` are recorded separately in `answer-reconciliations.json`. These include replacement of locally interpreted or differently formatted answers with MA evidence. They must not all be treated as our mathematical corrections.','',
          'The full original and corrected content, rationales, old transaction paths and verification paths are in `correction-events.json`. The mathematical-corrections directory will be preserved alongside this review.','']
(OUT/'correction-review.md').write_text('\n'.join(lines))
print(json.dumps({'entities':len(current),'events':len(events),'current_answer_value_changes':len(changes),'answer_reconciliations':len(reconciliations)},indent=2))
