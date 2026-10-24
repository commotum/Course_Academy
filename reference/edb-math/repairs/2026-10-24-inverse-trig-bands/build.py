"""Prepare four reviewable packages from the captured live instructional evidence."""
from collections import Counter
import json
from pathlib import Path
import shutil
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(H))
from read_math import source_prompt, key

KINDS = {17592186064218:'sine',17592186064219:'tangent',17592186064250:'secant',17592186064220:'definite'}
CONTRACTS = {
 'sine': {'easy':'Observed direct inverse-sine linear substitution, including integer and radical inner factors; no constant extraction.',
          'moderate':'Observed constant-radicand normalization with u=x/a; independent unit, integer, and fractional numerators.',
          'hard':'Authored composition: extract a nonunit constant and handle a non-square x coefficient; same linear substitution and arcsine primitive. No imported hard calibration.'},
 'tangent': {'easy':'Observed direct inverse-tangent substitution with integer or radical inner factor.',
             'moderate':'Observed nonunit constant normalization with u=x/a; include unit, cancelling, and independent numerators.',
             'hard':'Authored canonical e-471 composition: both quadratic coefficients nonunit; factor the constant then use an independent integer or irrational substitution factor. No imported hard calibration.'},
 'secant': {'easy':'Authored canonical e-5014 matching-differential cases: integer factor supplied in numerator, absolute value, and radical.',
            'moderate':'Observed visible |sx| and (sx)^2 with a surviving integer or fractional reciprocal factor; no normalization of |x| required.',
            'hard':'Observed |x| normalization: explicitly use |u|=s|x| with positive s; integer, radical, and denominator-prefactor cases. No new branch or integration method.'},
 'definite': {'easy':'Direct integer-factor substitution and zero lower endpoint; exact special values or retain arctan at an ordinary rational endpoint.',
              'moderate':'One denominator normalization, integer or radical scale, and a special-value or symmetric interval; show both endpoint conversions.',
              'hard':'Authored consistent workload: two nonunit coefficients, irrational substitution factor, and two unlike nonzero transformed endpoints. Both inverse values shown; every arcsine endpoint strictly internal.'},
}
ANCHORS = {
 'sine': {'easy':['q-2505','q-114024','q-114027'], 'moderate':['q-49545','q-49547','q-73712'], 'hard':['q-114024','q-114027','q-73712']},
 'tangent': {'easy':['q-49540','q-114035','q-114040'], 'moderate':['q-49548','q-114045','q-114046'], 'hard':['e-471','q-49540','q-49548']},
 'secant': {'easy':['e-5014'], 'moderate':['q-69476','q-73715','q-73716'], 'hard':['q-73717','q-114051','q-49519']},
 'definite': {'easy':['q-114074','q-49538','q-49536'], 'moderate':['q-19393','q-49546','q-351854'], 'hard':['q-19395','q-351291','q-114084']},
}
WRAPPER = '''#!/usr/bin/env python3
"""{kind} integration: repaired role-based generator; source evidence kept separately."""
from pathlib import Path
import sys
_here = Path(__file__).resolve().parent
_local = _here / 'inverse_trig.py'
sys.path.insert(0, str(_here if _local.exists() else _here.parent))
from inverse_trig import Generator
_evidence = _here / 'evidence.json'
if not _evidence.exists(): _evidence = Path(__file__).with_suffix('') / 'band-evidence.json'
_generator = Generator(_evidence)
KP_ID = _generator.kp
KP_UUID = _generator.kp_uuid
CASES = _generator.cases
SUPPORTED_LEVELS = ('easy', 'moderate', 'hard')
generate = _generator.generate
build = _generator.build
batch = _generator.batch
source_original = _generator.source_original
def generate_easy(seed=0, **kwargs): return generate('easy', seed, **kwargs)
def generate_moderate(seed=0, **kwargs): return generate('moderate', seed, **kwargs)
def generate_hard(seed=0, **kwargs): return generate('hard', seed, **kwargs)
if __name__ == '__main__': _generator.main()
'''


def main():
    coverage = []
    for kp,kind in KINDS.items():
        source = json.loads((H/'source'/f'{kp}.json').read_text())
        inventory = json.loads((H/'source'/str(kp)/'inventory.json').read_text())
        record = source['material']['kp']
        originals = record[':knowledge-point/questions'] + [record[':knowledge-point/canonical-example']]
        excluded = []
        for q in inventory['questions']+[inventory['canonical_example']]:
            body,lo,hi = source_prompt(q[':question/problem']);excluded.append(key(body,lo,hi))
        evidence = {'kp_id':kp,'kp_uuid':record[':knowledge-point/id'],'kind':kind,'title':record[':knowledge-point/title'],
                    'basis':source['basis'],'lineage':source['lineage'],'band_contract':CONTRACTS[kind], 'anchors':ANCHORS[kind],
                    'excluded_task_fingerprints':sorted(set(excluded)), 'originals':originals,
                    'source_policy':'Originals are archived evidence, not number-substitution templates. All normal banks are explicitly authored combinations of substitution error recipes; no exact source-bank generalization claim.',
                    'excluded_generation_profiles':{'q-2506':'Ambiguous arcsec-squared distractor; do not clone its bank.',
                                                    'q-351834':'Unbounded endpoints require improper-integral limits outside the present topic.'}}
        package = H/'packages'/str(kp);package.mkdir(parents=True,exist_ok=True)
        (package/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
        (package/'generator.py').write_text(WRAPPER.format(kind=kind))
        shutil.copy2(ROOT/'generate/inverse_trig.py',package/'inverse_trig.py')
        local = ROOT/'generate/scratch'/str(kp);local.mkdir(exist_ok=True)
        # Stage the legacy entrypoint until the successor package has committed.
        (H/'packages'/str(kp)/'local-entrypoint.py').write_text(WRAPPER.format(kind=kind))
        coverage.append({'kp':kp,'kind':kind,'practice_sources':dict(Counter(q[':question/difficulty'][':db/ident'] for q in record[':knowledge-point/questions'])),
                         'generated_retirement_candidates':[q[':db/id'] for q in inventory['questions'] if not q.get(':question/math-academy-id')],
                         'fingerprints_excluded':len(set(excluded)), 'originals_archived':len(originals), 'registered_generator':source['registered_generator']})
    (H/'source-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
    print(json.dumps(coverage,indent=2))


if __name__ == '__main__': main()
