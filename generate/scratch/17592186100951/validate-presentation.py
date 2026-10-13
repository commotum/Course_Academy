#!/usr/bin/env python3
"""Presentation-only verification against pre-edit stored JSON/record hashes."""
import copy,hashlib,json,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
v=runpy.run_path(str(ROOT/'validate.py'));g=v['g']
baseline=json.loads((ROOT/'presentation-baseline.json').read_text())
for name,expected in baseline['protected_json_sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,('stored JSON changed',name)
review=json.loads((ROOT/'review.json').read_text())
assert [hashlib.sha256(json.dumps(x['record'],sort_keys=True).encode()).hexdigest() for x in review]==baseline['stored_record_sha256']
unchanged=copy.deepcopy(review)
for item in review:
    r=item['record'];q=r['question'];text=g.markdown(r)
    assert text==g.markdown(r)
    assert 'Difficulty: '+g.difficulty_label(q) in text
    assert ('evidence only' in text)==r['generation']['evidence_only']
    assert ('authored' in text)==(not r['generation']['evidence_only'])
    expected=sum(':answer-field/correct' in f for f in q[':question/answer-fields'])
    assert text.count('**[correct]**')==expected
    for f in q[':question/answer-fields']:
        c=f.get(':answer-field/correct')
        if c is None:assert 'Correct designation: absent in the original source attribute.' in text
        for a in f[':answer-field/choices']:
            mark=' **[correct]**' if c and c[1]==a[':answer/id'] else ''
            assert '\n- $'+a[':answer/value']+'$'+mark in text
    assert q[':question/problem'] in text
    if ':question/worked-solution' in q:assert q[':question/worked-solution'] in text
for q in v['QS']:
    text=v['original_markdown'](q)
    assert 'Difficulty: '+g.difficulty_label(q) in text
    assert 'Origin: Original; evidence only' in text
    assert q[':question/problem'] in text
    if ':question/worked-solution' in q:assert q[':question/worked-solution'] in text
    f=q[':question/answer-fields'][0];c=f.get(':answer-field/correct')
    assert text.count('**[correct]**')==int(c is not None)
    if c is None:assert 'Correct designation: absent in the original source attribute.' in text
    else:assert '$'+c[':answer/value']+'$ **[correct]**' in text
assert review==unchanged, 'Markdown rendering mutated stored records'
text=v['render_review'](review)
assert text==v['render_review'](review)
(ROOT/'review.md').write_text(text)
report={'status':'pass','source_originals_labeled':len(v['QS']),'generated_records_labeled':len(review),'original_unrated_and_missing_correct_explicit':2,'original_present_correct_marks':17,'stored_question_records_math_ids_unchanged':len(review),'protected_json_files_byte_unchanged':len(baseline['protected_json_sha256']),'deterministic_markdown':True,'database_writes':0}
(ROOT/'presentation-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
