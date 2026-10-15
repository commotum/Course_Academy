# Leibniz quotient generator

New numeric pair for KP17592186096622, basis2275. At assignment start the numeric script/tree did not exist and the manifest had no registered baseline. No existing registered files, shared manifests, queues, database or grader code are edited.

```sh
.venv/bin/python generate/scratch/17592186096622.py --difficulty all --count 2 --seed 110 --format markdown
.venv/bin/python generate/scratch/17592186096622/validate.py
```

The public API is generate(level, seed=0, template=None, parameters=None, profile=None, bank_profile=None), with generate_easy/moderate/hard helpers. Normal output is checked against the frozen canonical formatter at return. profile="raw" is deliberately exact evidence-only output, including absent attributes and historical malformed TeX, and bypasses normal presentation validation. It is restricted to original source parameters and is ineligible for learning. Normal solutions and native learner checks are separate from evidence output.

All eleven source families replay complete banks and ordered mathematical solution stages at their original anchors. All three difficulty levels have independently distinct parameterized tasks. The raw-keyless q-11944/q-9909 have explicitly authored normal keys, solutions and difficulty assignments. q-340335’s f/y inconsistency is corrected in normal content. review.json/review.md put every raw original beside its completed anchor and changed parameters/profile. validate.py independently reads printed givens, definitions, derivative operands, substituted factors, all stages and complete banks; it includes destructive mutation controls that leave the final key unchanged.

The frozen grader SHA256 is 71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea. engine-input.json contains owned native correct/wrong IDs, separate foreign/malformed submissions, canonical and equivalent blank fragments, and wrong 0/1 values. Any unresolved valid mathematics is reported as an engine limitation rather than silently removed. No database operation or registration is performed.

Final validation checked 432 records, 3535 independently read operands/stages, 121 rejected mathematical/structural mutations, 91 boundary records and ten invalid API inputs. All eleven source banks (27 values) and nine captured solution chains (29 operative stages) replayed. Fifty independent task identities per band were demonstrated. Seven shared math-format unit tests also passed.

The frozen grader recorded 1000 accepted, 1510 rejected and 728 unresolved checks. Of the unresolved checks, 642 are deliberately foreign/malformed radio submissions and 86 are mathematically valid unreduced blank equivalents whose extra apparent denominator holes trigger domain-comparison limits. These valid equivalents remain in engine-input.json with mathematical_expected=accepted and the exact observed native result. native-valid-limitations.json lists every case; native-batch-reports.json preserves all 432 unchanged checker reports. Native compatibility is explicitly incomplete; this is not a claim that all true equivalents grade correctly.
