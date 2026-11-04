"""Build a bounded replacement pool from the reviewed portable CLIs.

Imports count toward inventory. Five is a refill floor, never a reason to
invent a new operation, rename a variable, or exceed a finite family.
"""
import collections
import concurrent.futures
import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import prepare_records, inventory_fingerprints

WORK = ROOT / 'generate/repairs/2026-11-04-four-trig-lessons'
AUDIT = ROOT / 'reference/edb-math/audits/2026-11-04-four-trig-lessons'
sys.path.insert(0, str(AUDIT))
import numeric_audit as numeric

# Load only the checker definitions, without rerunning or modifying the audit.
solution_scope = {'__file__': str(AUDIT / 'solutions_audit.py')}
exec(compile((AUDIT / 'solutions_audit.py').read_text().split('\nresults=[]')[0],
             str(AUDIT / 'solutions_audit.py'), 'exec'), solution_scope)


def gradeable(q):
    fields = q.get(':question/answer-fields', [])
    return bool(fields) and all(f.get(':answer-field/correct') for f in fields)


def enum(value):
    return value.get(':db/ident') if isinstance(value, dict) else value


def sample_parameters(kid, band):
    finite_small = (band == 'easy' and kid in {'17592186059665', '17592186059820', '17592186059662',
                   '17592186059821', '17592186059663'}) or (band == 'moderate' and kid in {'17592186059665', '17592186059820'})
    count = 5 if finite_small else 8 if kid == '17592186059672' and band == 'easy' else 10
    return count, 20261104 + ('easy', 'moderate', 'hard').index(band)


def sample(args):
    kid, folder, band = args
    count, seed = sample_parameters(kid, band)
    output = subprocess.run([sys.executable, str(folder / 'generator.py'),
                             '--difficulty', band, '--count', str(count), '--seed', str(seed), '--format', 'json'],
                            check=True, text=True, capture_output=True, timeout=180)
    return kid, band, json.loads(output.stdout)


def main():
    capture = json.loads((H / 'capture.json').read_text())
    folders = {str(p.parent.name): p.parent for p in WORK.glob('*/*/generator.py')}
    assert set(folders) == set(capture['kps'])
    def hashes(folder):
        manifest = folder / 'runtime-manifest.json'
        if not manifest.exists(): manifest = folder / 'manifest.json'
        names = json.loads(manifest.read_text())['runtime_files']
        return {name: hashlib.sha256((folder / name).read_bytes()).hexdigest() for name in names}
    runtime_before = {kid: hashes(folder) for kid, folder in folders.items()}
    tasks = [(kid, folders[kid], band) for kid in folders for band in ('easy', 'moderate', 'hard')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        samples = list(executor.map(sample, tasks))
    assert runtime_before == {kid: hashes(folder) for kid, folder in folders.items()}, 'Runtime changed during review'
    grouped = collections.defaultdict(dict)
    for kid, band, records in samples:
        grouped[kid][band] = records
    all_records, rendering, checks, ledger = [], [], [], {}
    for kid, bands in grouped.items():
        kp = capture['kps'][kid]
        originals = [q for q in kp[':knowledge-point/questions']
                     if q.get(':question/math-academy-id') and not q.get(':question/retired')]
        counts = collections.Counter(q.get(':question/difficulty', {}).get(':db/ident', '').split('/')[-1]
                                     for q in originals if gradeable(q))
        chosen = []
        seen_stems = set()
        for band, candidates in bands.items():
            # The repeated-use KP needs ordinary sampling of cancellation,
            # evaluated products and symbolic terminal products, not replay only.
            minimum = 3 if kid == '17592186059672' and band == 'moderate' else 1
            need = max(minimum, 5 - counts[band])
            seen = inventory_fingerprints(originals + ([kp[':knowledge-point/canonical-example']]
                                         if kp.get(':knowledge-point/canonical-example') else []))
            localized, duplicate_count = prepare_records(candidates, int(kid), kp[':knowledge-point/id'],
                                                         seen, Path('/tmp'), H)
            sample_folder = H / 'samples' / kid
            sample_folder.mkdir(parents=True, exist_ok=True)
            (sample_folder / f'{band}.json').write_text(json.dumps(localized, indent=2) + '\n')
            def stem(r):
                q = r['question']
                return (numeric.target(q).replace(' ', ''), tuple(enum(f[':answer-field/type']) for f in q[':question/answer-fields']))
            eligible = [r for r in localized if stem(r) not in seen_stems]
            assert len(eligible) >= need, (kid, band, need, len(eligible), duplicate_count)
            selection = eligible[:need]
            if minimum == 3:
                family = lambda r: ('symbolic' if r['generation'].get('symbolic_terminal') else r['generation']['template'])
                reps = {family(r): r for r in eligible}
                assert {'cancellation', 'product', 'symbolic'} <= set(reps), set(reps)
                selection = [reps[k] for k in ('cancellation', 'product', 'symbolic')]
                selection += [r for r in eligible if r not in selection][:need-len(selection)]
            chosen += selection
            seen_stems.update(stem(r) for r in selection)
            rendering.append(selection[0])
            for i, record in enumerate(localized):
                q = record['question']; label = f'{kid}/{band}/{i}'
                result = numeric.audit(q, label, kid)
                assert result['status'] == 'match' and not result['choice_ambiguities'], result
                solution = solution_scope['check'](q, label, kid)
                assert not solution.get('suspected_bad_equalities') and not solution.get('unparsed_equalities'), solution
                # Check all distractor pairs, including wrong-versus-wrong.
                for field in q[':question/answer-fields']:
                    if not enum(field[':answer-field/type']).endswith(('/radio', '/select')): continue
                    values = [numeric.Numeric(numeric.nodes(a[':answer/value']), {'x': .371}).evaluate()
                              for a in field[':answer-field/choices']]
                    assert all(abs(a-b) > 1e-8 for n, a in enumerate(values) for b in values[:n]), label
                checks.append({'label': label, 'math': result, 'solution': solution})
        (H / 'pools').mkdir(exist_ok=True)
        (H / 'pools' / f'{kid}.json').write_text(json.dumps(chosen, indent=2) + '\n')
        all_records += chosen
        ledger[kid] = {'imported_gradeable_by_band': dict(counts),
                       'new_by_band': dict(collections.Counter(enum(r['question'][':question/difficulty']).split('/')[-1] for r in chosen)),
                       'runtime_sha256': runtime_before[kid],
                       'sampling': {b: dict(zip(('count', 'seed'), sample_parameters(kid, b))) for b in bands},
                       'workspace': str(folders[kid].relative_to(ROOT))}
    (H / 'candidate-pool.json').write_text(json.dumps(all_records, indent=2) + '\n')
    (H / 'render-records.json').write_text(json.dumps(rendering, indent=2) + '\n')
    result = {'passed': True, 'sampled_records': len(checks), 'new_records': len(all_records),
              'solution_equality_witnesses': sum(c['solution']['checks'] for c in checks),
              'inventory': ledger, 'checks': checks}
    (H / 'pool-review.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('checks', 'inventory')}))


if __name__ == '__main__': main()
