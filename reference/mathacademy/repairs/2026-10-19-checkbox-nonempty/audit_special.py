"""Cover nonstandard CLIs, finite catalogs and explicit ODE decision cases."""
import importlib.util
import json
import sys
from pathlib import Path
from scripts.generator_policy import EmptyCheckboxSelection, checkbox_selection

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def load(path, name):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

reports, records = [], []
for kp in (17592186147456, 17592186179742, 17592186119848, 17592186105908):
    g = load(ROOT / 'generate/scratch' / (str(kp) + '.py'), 'special_' + str(kp))
    current = []
    if kp == 17592186147456:
        for template, (level, _) in g.CASES.items():
            if template == 'q-108916':
                try: g.generate(level, template=template)
                except ValueError: continue
                raise AssertionError('Invariant empty family was accepted')
            for seed in range(3): current.append(g.generate(level, seed, template=template))
    elif kp == 17592186179742:
        for level in g.LEVELS:
            for seed in range(2): current.append(g.generate(level, seed))
    elif kp == 17592186119848:
        current = g.catalog()
        assert current
        assert g.batch('easy', len(current), 17)
    else:
        for source_id, q in g.ORIGINALS.items():
            fields = q.get(':question/answer-fields', [])
            if any(f.get(':answer-field/type', {}).get(':db/ident') == ':answer-field.type/checkbox' for f in fields):
                # The source-based coordinate transform is explicitly evidence-only.
                level = q.get(':question/difficulty', {}).get(':db/ident', ':question.difficulty/moderate').split('/')[-1]
                record = g.generate(level, template=source_id)
                assert record['generation'].get('evidence_only') or record['generation'].get('eligible_for_learning') is False
    for record in current:
        selected = checkbox_selection(record)
        assert not selected or any(selected), kp
    reports.append({'kp': kp, 'records': len(current), 'checkbox_records': sum(bool(checkbox_selection(r)) for r in current), 'passed': True})
    records.extend(current)
    print(json.dumps(reports[-1]), flush=True)

candidate = next(r for r in json.loads((HERE / 'patched-generators.json').read_text()) if r['kp'] == 17592186100888)
g = load(Path(candidate['updated_script']), 'ode_explicit')
try:
    g.generate('easy', decision_case=(False, False))
except ValueError as error:
    assert 'no correct selectable option' in str(error)
else:
    raise AssertionError('Explicit all-false ODE case was accepted')
ode_count = 0
for template, level in g.LEVELS.items():
    for case in ((False, True), (True, False), (True, True)):
        record = g.generate(level, template=template, decision_case=case)
        assert any(checkbox_selection(record))
        records.append(record)
        ode_count += 1
reports.append({'kp': 17592186100888, 'explicit_empty_rejected': True, 'explicit_nonempty_cases': ode_count, 'passed': True})
(HERE / 'special-audit.json').write_text(json.dumps(reports, indent=2) + '\n')
(HERE / 'special-samples.json').write_text(json.dumps(records, indent=2) + '\n')
