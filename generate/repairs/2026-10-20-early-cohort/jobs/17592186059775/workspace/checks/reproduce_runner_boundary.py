"""Reproduce the current handoff gate without changing the runner or package.

Exit 1 means the reported unchanged-candidate failure still applies. This is a
diagnostic, not a passing repair regression or permission to change runtime data.
"""
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parents[1]
REPO = Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0, str(REPO/'scripts'))
from generator_packages import package_digest
from generator_review import validate_review


def read(path):
    return json.loads(path.read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def main():
    manifest = read(W/'package.json')
    history = read(W.parent/'repair-history.json')
    rejected = next(event for event in history['events']
                    if event['attempt'] == 3)
    review_root = Path(rejected['review_directory'])
    runner_state = read(W.parent/'job.json')
    binding = runner_state['previous_review']['binding']
    package = package_digest(W, manifest['entrypoint'], manifest['files'],
                             dependencies=manifest['dependencies'])
    source = digest(read(W.parent/'source/source.json'))
    paths = list((REPO/'engine/rust').rglob('*.rs'))
    paths.append(REPO/'generate/runs/current/check-engine')
    engine = digest({str(p.relative_to(REPO)):
                     hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    gate = (package == runner_state['last_rejected_package']
            and source == runner_state['last_rejected_source']
            and engine == runner_state['last_rejected_engine'])
    historical = read(review_root/'contract-repair/result.json')
    try:
        validate_review(historical, review_root)
    except ValueError as error:
        wrong_root_error = str(error)
        assert wrong_root_error == ('source_analysis.evidence_paths: missing, '
                                    'empty, or escaping evidence: '
                                    'correction-provenance.json')
    else:
        raise AssertionError('Historical evidence failure no longer reproduces')
    # Establish that the existing correction works at its actual evidence root.
    bundle = W/'evidence/contract-correction'
    validate_review(read(bundle/'result.json'), bundle)
    result = {
        'current_package_hash': package,
        'rejected_package_hash': rejected['package_hash'],
        'source_hash_matches_rejected_binding': source == binding['source_hash'],
        'engine_hash_matches_rejected_binding': engine == binding['engine_hash'],
        'unchanged_candidate_gate_reproduced': gate,
        'runner_stage_at_read': runner_state['stage'],
        'historical_wrong_root_error': wrong_root_error,
        'corrected_bundle_validates_at': 'evidence/contract-correction',
        'runtime_hashes': {name: hashlib.sha256((W/name).read_bytes()).hexdigest()
                           for name in ['package.json', *manifest['files']]},
        'scope': 'Read-only runner diagnosis; no installation or approval.',
    }
    (W/'evidence/author9-exact-failures.json').write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
    return 1 if gate else 0


if __name__ == '__main__':
    raise SystemExit(main())
