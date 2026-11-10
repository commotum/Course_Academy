"""Move the imported proof dropdowns into authored equation rows; preserve banks."""
import copy
import json
from pathlib import Path
import re
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from question_capture.edn import dumps, kw

before = json.loads((H / 'questions-before.json').read_text())
after = copy.deepcopy(before)
changes = []
targets = []
for q in after:
    fields = q.get(':question/answer-fields', [])
    if not any(f[':answer-field/type'][':db/ident'] == ':answer-field.type/select' for f in fields):
        continue
    targets.append(q[':db/id'])
    if len(fields) == 1:
        # This captured one-stage question already places its dropdown inline.
        continue
    assert len(fields) == 6
    old = q[':question/problem']
    blocks = [m for m in re.finditer(r'\$\$[\s\S]*?\$\$', old)
              if all('{{field-' + str(i) + '}}' in m[0] for i in [2, 3, 4])]
    assert len(blocks) == 1
    lhs = r'D(a{y}_{1}+b{y}_{2})'
    if q[':question/math-academy-id'] == 'q-338094':
        first = (lhs + r'=(a{y}_{1}+b{y}_{2})\frac{\text{d}}{\text{d}x}'
                 r'(a{y}_{1}+b{y}_{2})-2(a{y}_{1}+b{y}_{2})')
        replacement = '$$\n' + first + '\n$$\n\n'
        sign = r'-2\cdot'
        factor = 'ab'
    else:
        replacement = ''
        sign = '+'
        factor = '2ab' if q[':question/math-academy-id'] == 'q-337728' else 'ab'
        assert '+' + factor + r'\cdot {{field-4}}' in blocks[0][0]
    replacement += ('<div class="question-equation">\n'
                    '<div>$' + lhs + '=$ {{field-2}} $' + sign + '$ {{field-3}}</div>\n'
                    '<div>$ {}+' + factor + r'\cdot$ {{field-4}}.' + '</div>\n</div>')
    new = old[:blocks[0].start()] + replacement + old[blocks[0].end():]
    assert sorted(re.findall(r'\{\{([^{}]+)\}\}', old)) == sorted(re.findall(r'\{\{([^{}]+)\}\}', new))
    q[':question/problem'] = new
    changes.append(dict(entity=q[':db/id'], attribute='question/problem', old=old, new=new,
                        reason='Keep each dropdown outside TeX and at the missing term rather than after an aligned SVG.'))

forms = [[kw('db/cas'), c['entity'], kw(c['attribute']), c['old'], c['new']] for c in changes]
forms += [[kw('db/ensure'), c['entity'], kw('question/validate')] for c in changes]
(H / 'questions-after.json').write_text(json.dumps(after, indent=2) + '\n')
(H / 'changes.json').write_text(json.dumps(changes, indent=2) + '\n')
(H / 'transaction.edn').write_text(dumps(forms) + '\n')
(H / 'plan.json').write_text(json.dumps(dict(topic=17592186050537, questions_checked=len(before),
    dropdown_questions_checked=targets, changed_questions=[c['entity'] for c in changes],
    field_types='All original selects retained', field_and_answer_ids_preserved=True,
    choice_banks_keys_solutions_and_history_preserved=True), indent=2) + '\n')
print(json.dumps(dict(changed_questions=len(changes), dropdown_questions_checked=len(targets))))
