"""Prepare affected delivery, counterfactual, renderer, and batched native cases."""
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('repairs', ROOT / 'checks/check_repairs.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
g, v, out = c.g, c.v, c.OUT

p = g.original('q-142367')
p['claims'] = [r'\text{dim(Null}(A))\ne 0', r'A\text{ is invertible}', r'\text{Col}(A)={R}^{4}']
a = g.generate(template='q-142367', parameters=p)
p['claims'][1] = r'A\text{ is not invertible}'
b = g.generate(template='q-142367', parameters=p)
assert v.inspect(a)[0] == (True, False, False)
assert v.inspect(b)[0] == (True, True, False)
assert a['question'][':question/problem'].split('\n\nI.')[0] == b['question'][':question/problem'].split('\n\nI.')[0]
replay = next(r for r in json.loads((out / 'source-replays.json').read_text()) if r['generation']['template'] == 'q-142367')
raw = json.loads((out / 'restored-profile.json').read_text()) + [replay, a, b]
accepted, cmd = c.delivery('restored', raw)
assert len(accepted) == len(raw)
for r in accepted:
    v.inspect(r)
c.save('restored-delivery-coverage.json', {'passed': True, 'command': cmd, 'raw': v.summarize(raw, True), 'delivered': v.summarize(accepted, True), 'all_survived': True, 'counterfactual': 'identical nonzero witness; invertibility claim polarity changes I-only to I-and-II'})
native = json.loads((out / 'source-native-input.json').read_text()) + json.loads((out / 'batch-native-input.json').read_text()) + [v.native(r, 'restored-delivered-' + str(i)) for i, r in enumerate(accepted)]
c.save('native-input.json', native)
forced = json.loads((out / 'original-order-delivery/accepted.json').read_text())
c.save('render-records.json', [replay, a, b, forced[0], forced[1]])
# Observe radio label/position cues separately from checkbox count coverage.
reports = {}
for name in ('original-order', 'cli-4126872122', 'cli-0', 'cli-1', 'cli-99', 'cli-2026'):
    rows = json.loads((out / (name + '-delivery/accepted.json')).read_text())
    positions = []
    subsets = []
    for r in rows:
        fs = r['question'][':question/answer-fields']
        if fs[0][':answer-field/type'].endswith('/radio'):
            positions.append(v.inspect(r)[1])
            subsets.append(v.correct(fs[0]))
    if len(positions) > 1:
        assert len(set(positions)) > 1, ('fixed radio position', name)
        assert len(set(subsets)) > 1, ('fixed radio subset', name)
    reports[name] = {'radio_positions': positions, 'radio_subsets': subsets}
c.save('radio-shortcuts.json', {'passed': True, 'delivered_batches': reports})
print('Prepared', len(native), 'native records;', sum(len(r['checks']) for r in native), 'checks; five affected UI previews. Restored variants and controlled pair all survive delivery.')
