# Invertibility of intervals from descriptions

Local generator at math basis 1356. Only this KP's private script/evidence are changed; there are no DB writes, engine edits, registration or preparation for step 8.

```sh
.venv/bin/python generate/scratch/17592186124474.py --difficulty all --seed 8 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186124474.py --difficulty moderate --template q-66785 --profile raw --format json
.venv/bin/python generate/scratch/17592186124474/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and separate `generate_easy`, `generate_moderate`, `generate_hard`. Only observed radio/text selection shape is supported. Source parameters are `a,h,k,offset`; authored constant parameters are `k,offset`; authored integer/rational folded parameters are `h,k,types`.

Profiles: each source template uses its own complete `observed` bank. q-66785 instead exposes ineligible `raw` and authored `repaired`. Authored templates use `authored`. Default sampling serves every observed family and the supported repair, plus two integer folded catalogs, two rational folded catalogs, and the constant-line contrast. CLI JSON remains review data.

See classification.md and template-extraction.md for observed/authored distinctions and exact level bounds. Every source can replay through source-cases.json. Review.md contains all originals and two generated examples for every source family and every authored family; review.json contains generated records. Plot geometry/hashes are in plot-extraction.json, renderer requirements in plot-spec.md, and measured generated geometry in plots/*.json. Validation.json includes frozen input/script/native hashes and actual runtime versions.

Source fidelity is 12/12 prompts and complete solutions, 11/11 complete five-choice banks, 55/55 displayed choices, and 11/11 supplied correct designations. q-66785's absent field/designation is preserved raw and repaired separately. Exact mathematical validity, original fidelity, and real native radio grading are separate checks. The radio grader tests every owned choice; it has no free-entry equivalent-text interface. Equivalent Roman subsets are rejected as duplicate options regardless of punctuation.

The semantic catalogs are finite: easy has two tasks, authored moderate has 72 ordered interval structures, and hard has 90. Numerical translation/scaling, parameter spelling, option order and functional realizations of the same folded-domain decision do not inflate those counts. Source masks/banks are preserved independently for fidelity. Hard difficulty is an authored rational-bound comparison design claim; no hard practice example was captured.
