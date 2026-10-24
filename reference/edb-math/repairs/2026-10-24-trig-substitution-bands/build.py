"""Build self-contained reviewed packages and matching repository entrypoints."""
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import argparse

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT/'generate/scratch/17592186068915'))
sys.path.insert(0, str(ROOT/'generate/scratch'))
import trig_substitution as engine

KPS = (17592186068916, 17592186068917, 17592186068918)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true')
    install=parser.parse_args().install
    spec = importlib.util.spec_from_file_location('old_printed', ROOT/'generate/scratch/17592186068918/printed.py')
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    for kp in KPS:
        directory = H/str(kp)
        source = json.loads((directory/'source/source.json').read_text())
        inv = json.loads((directory/'inventory/inventory.json').read_text())
        record = source['material']['kp']
        blocked, failed = [], []
        for question in inv['questions']+[inv['canonical_example']]:
            try:
                body, lo, hi = reader.integral(question[':question/problem'])
                blocked.append(engine.task_key(body, lo, hi))
            except Exception as exc:
                failed.append({'question': question.get(':db/id'), 'error': str(exc)})
        # All old generated tasks must be excluded mathematically, not just by UUID.
        assert not any(q[':db/id'] in {row['question'] for row in failed}
                       for q in inv['questions'] if not q.get(':question/math-academy-id'))
        origin = {
            17592186068916: {'easy': 'Source-anchored linear indefinite derivative families, extended to all four familiar primitives',
                'moderate': 'Source-anchored definite linear arguments; integer slopes, both endpoint contributions',
                'hard': 'Source-anchored shifted/fractional slopes; authored combination with two nonzero endpoint values'},
            17592186068917: {'easy': 'Authored introductory band: integer multiples of an exact power-inner derivative; no imported easy anchor',
                'moderate': 'Source-anchored nonunit reciprocal coefficient, shifted power arguments, and square-root substitution',
                'hard': 'Source-anchored definite nonlinear substitution or reciprocal inner function; excludes zero-result repetition'},
            17592186068918: {'easy': 'Authored introductory f-prime/f recognition; sources have no easy labels',
                'moderate': 'Authored intermediate band: affine trig/power denominator plus coefficient adjustment; sources have no moderate labels',
                'hard': 'Source-anchored definite log evaluation, nested substitution, or supported rational rearrangement'},
        }[kp]
        evidence = {'kp': {'db_id': kp, 'id': str(record[':knowledge-point/id']), 'title': record[':knowledge-point/title']},
            'basis': source['basis'], 'band_origin': origin,
            'excluded_tasks': sorted(set(blocked)), 'exclusion_parse_limitations': failed,
            'source_counts': {band: sum(q.get(':question/difficulty', {}).get(':db/ident') == ':question.difficulty/'+band
                                      for q in inv['questions'] if q.get(':question/math-academy-id')) for band in origin},
            'placement_exclusions': ['q-113983', 'q-113979'] if kp == 17592186068916 else [],
            'authored_response_extension': 'All new records use exact-entry blanks to assess the substitution directly. No source-bank fidelity claimed; original code and complete banks archived.',
            'families': {band: list(cases) for band, cases in engine.CASE[kp].items()}}
        contract = {'version': engine.VERSION, 'band_origin': origin,
                    'families': evidence['families'], 'pool_policy': 'Structural family first, then valid parameters. No zero definite answers or old task reuse. Both coefficient signs within each family.',
                    'answer_form': 'Render the canonical answer once, use it verbatim as the worked solution final result; preserve trig arguments and show log quotient conversion.',
                    'calibration_limit': 'Source labels are evidence, not an external psychometric validation of authored bands.'}
        wrapper = f'''#!/usr/bin/env python3
"""Repaired KP {kp}: controlled substitution practice."""
import json
from pathlib import Path
import sys
LOCAL=Path(__file__).with_suffix('')
if not (LOCAL/'trig_substitution.py').is_file(): LOCAL=Path(__file__).resolve().parent
sys.path.insert(0,str(LOCAL))
import trig_substitution as model
KP={kp}
EVIDENCE=json.loads((LOCAL/'source-evidence.json').read_text())
def generate(level,seed=0,template=None,**kwargs):
    return model.generate(KP,level,seed,template,evidence=EVIDENCE,**kwargs)
def batch(level,count=8,seed=0,template=None):
    return model.batch(KP,level,count,seed,evidence=EVIDENCE,template=template)
if __name__=='__main__': model.cli(KP,LOCAL)
'''
        destinations=[directory/'package']
        if install:destinations.append(ROOT/f'generate/scratch/{kp}')
        for dest in destinations:
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT/'generate/scratch/trig_substitution.py', dest/'trig_substitution.py')
            shutil.copy2(ROOT/'generate/scratch/17592186068915/trig_format.py', dest/'trig_format.py')
            (dest/'source-evidence.json').write_text(json.dumps(evidence, indent=2)+'\n')
            (dest/'band-contract.json').write_text(json.dumps(contract, indent=2)+'\n')
            (dest/'generator.py' if dest.name == 'package' else ROOT/f'generate/scratch/{kp}.py').write_text(wrapper)
        capabilities = {'supported_levels': list(origin), 'imported_source_counts': evidence['source_counts'],
            'band_origin': origin, 'band_contract': 'band-contract.json', 'implementation_version': engine.VERSION,
            'maximum_records_per_call': 200, 'unsupported_levels_filled': False,
            'sampling': contract['pool_policy'], 'response_policy': evidence['authored_response_extension']}
        if install:(ROOT/f'generate/scratch/{kp}/capabilities.json').write_text(json.dumps(capabilities, indent=2)+'\n')
        print(kp, 'packaged; exclusions', len(blocked), 'parse limitations', len(failed))


if __name__ == '__main__':
    main()
