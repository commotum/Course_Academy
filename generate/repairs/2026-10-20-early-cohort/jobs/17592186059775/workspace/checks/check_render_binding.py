"""Bind retained, visually inspected UI endpoints to fresh delivered records."""
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(W/'checks'))
from check_repair import g, key, v


def main():
    source = json.loads((W.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
    replayed = []
    for original in source:
        sid = original[':question/math-academy-id']
        if sid not in g.CASES:
            continue
        record = g.source_replay(sid)
        q = record['question']
        for name in (':question/problem', ':question/worked-solution'):
            assert q[name] == original[name], (sid, name)
        f = q[':question/answer-fields'][0]
        original_field = original[':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices']) == sorted(
            a[':answer/value'] for a in original_field[':answer-field/choices'])
        assert key(record)[':answer/value'] == original_field[':answer-field/correct'][':answer/value']
        replayed.append({'source_id': sid, 'question_id': original[':question/id'],
                         'choices': len(f[':answer-field/choices'])})
    delivered = json.loads((W/'evidence/delivery-batch-repair/accepted.json').read_text())
    rendered = json.loads((W/'evidence/author8-render-records.json').read_text())
    assert rendered == [delivered[0], delivered[-1]]
    assert rendered == json.loads((W/'evidence/author8-render/input.json').read_text())
    assert json.loads((W/'evidence/author8-render/rendering.json').read_text())['passed']
    for r in rendered:
        v.independent(r, replay=False)
    runtime = json.loads((W/'evidence/author31-boundary.log').read_text())['runtime_hashes']
    assert all(hashlib.sha256((W/name).read_bytes()).hexdigest() == value for name,value in runtime.items())
    report = {'passed': True, 'complete_source_banks': len(replayed),
              'source_choices': sum(r['choices'] for r in replayed), 'source_cases': replayed,
              'ui_records_equal_current_delivered_endpoints': True,
              'render_input': 'evidence/author8-render-records.json',
              'render_report': 'evidence/author8-render/rendering.json',
              'screenshots': ['evidence/author8-render/question-001.png', 'evidence/author8-render/question-002.png'],
              'runtime_hashes_unchanged': runtime}
    (W/'evidence/current-render-binding.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'passed': True, 'complete_source_banks': len(replayed), 'bound_ui_records': len(rendered)}))


if __name__ == '__main__':
    main()
