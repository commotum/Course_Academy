# Answer representation and solution-path audit

Committed to `math` at **T6135**, source `:agent/codex`: **11 questions**, **36 content values** (34 answer values and 2 worked solutions), and one generator successor registration. Exact receipt datoms and complete affected question/field/answer trees were verified at db-after. Existing question, field and answer identities, correct-answer links, and learner facts were preserved. See [verification.json](verification.json), [changes.json](changes.json), and [receipt.edn](receipt.edn).

The root cause is a split between the mathematical expressions used to render answers and the source-shaped derivations used to render explanations. Algebraic equivalence tests can accept a representation that adds a conversion the learner was never shown. Some conversions also add a skill outside the lesson; other cases merely impose unnecessary algebra after the explanation ends. These are different from harmless TeX spellings or a conversion already demonstrated in the solution.

## Repairs

| Family | Repair |
| --- | --- |
| Product rule with exponential/logarithmic factors, KP 17592186096618 | Preserve the supplied logarithm base in coefficient banks and either blank target. Keep both source product-rule contributions visible instead of silently combining them through change of base. Publish version 3 as a new immutable package; retain the original package. |
| Vector chain rule in three variables, KP 17592186124470 | Preserve the translated inner square and exponential factors throughout the bank. Use the completed worked solution as the keyed display form, with a separate exact-value assertion. Apply the same notation policy to distractors so the correct answer does not stand out by formatting. |
| Change of variables, KP 17592186198361 | Render evaluated logarithms with the same argument as the derivation, including `ln(4)` instead of independently reducing the key to `2 ln(2)`. |
| Shifted cylindrical solid, KP 17592186129268 | End the solution in the substituted sine/cosine product used by its bank, avoiding an unnecessary final double-angle conversion. |
| Source inequality question 17592186157736 | Retain the base-8 logarithm derived in the solution instead of requiring an unshown change to natural logarithms. Both the prior natural-log entry and new canonical entry passed actual blank grading. |
| Imported assignment question 17592186405578 | Show the missing power-rule and quotient-rule steps from the difference of logarithms of positive square roots to the existing answer. Its key remains unchanged. |

The new published logarithm generator is `generators/ad/ad85641fc8ae4d1d3139254582d530b0f3b00cfecf8dc8e844284e477c8f2207/generator.py`, registered as entity **17592186676062**. Its helper and dependency files are byte-identical to the previous immutable package. The three legacy generators retain their registered repository paths. [package-publication.json](package-publication.json) retains the complete successor manifest.

## Audit coverage

The initial current-value snapshot was **T6134**. The inventory contains 650 registered knowledge points with 637 distinct registered entrypoints; all 637 files were present. Static inspection found explicit symbolic normalization calls in 241 entrypoints. Those calls are risk indicators, not defects by themselves: several topics intentionally teach those transformations, and many calls are used only for identity or validation.

The read-only function/argument scan covered **83,402 stored questions**, including 5,073 without Math Academy source IDs. It flagged 71 candidates. Contextual review confirmed nine of those as repair cases; family/endpoint review found the other two. The remaining signals were source spelling differences, already-shown conversions, field-fragment scope, plain/Unicode assignment prose, or ordinary prerequisite algebra for which no comparable generator defect was established. [candidate-dispositions.json](candidate-dispositions.json) retains every signal; [audit-summary.json](audit-summary.json) records counts and limits.

Fresh sampling checked 51 records from related generators, with no additional candidates in recognized notation. There were 17 successful CLI calls across requested moderate/hard bands; unsupported bands and one entrypoint without CLI output are recorded in [sibling-sampling.json](sibling-sampling.json). This is not an exhaustive runtime audit of all 637 entrypoints or a proof that every stored question has a complete explanation.

The scanner deliberately reports candidates instead of automatically rewriting mathematics. Reproduce the snapshot scan with:

```bash
.venv/bin/python scripts/audit_generator_representations.py \
  --snapshot .local/edb/tex-boundary-current.jsonl \
  --output /tmp/representation-candidates.json
```

The retained JSONL snapshot/index is local evidence rather than a 136 MB repository artifact. The compact candidate reports, exact affected database reads, original generator copies, and reproducible repair/check scripts are retained here.

## Prevention

The author prompt now requires deriving the answer bank from the learner's ordered solution, preserving operator inputs, domains, branches and field-fragment scope. The reviewer prompt separately requires checking both prerequisite support and the actual displayed conversion. It explicitly covers parity/double-angle identities, changed logarithm bases, expanded nested arguments, exponentials, absolute values and cancellation/branch conditions.

Review policy is now **3**. The existing `scope` check must cite a structured `solution-paths.json` with actual sample references, displayed endpoints, keys, domains and any conversions' rules, source support and shown steps. Missing evidence, failed cases, and unsupported or unshown conversions cannot pass the gate. Existing cached policy-2 approvals no longer satisfy the runner's review binding. The eight-check review result schema remains compatible; this is required evidence under `scope`, not an extra top-level check.

Template extraction and database-preparation guidance were updated as well. Authors and reviewers must exercise negative controls where algebraic equivalence passes while the instructional transition fails. The gate verifies that inspectable evidence exists; the reviewer remains responsible for mathematical and pedagogical truth. A file or a passing metadata assertion is not a universal proof of prerequisite coverage.

## Validation

- **111 unit/integration tests passed** across review evidence, pipeline, cohort, report handling, generator policy, representation regressions, and the original sine-parity regression. The latter demonstrates that the old form passes algebraic checks but fails the representation check.
- All 16 templates of the logarithm product-rule generator were exercised at three fresh seeds: **48 questions**, with **150 actual grader checks**.
- **20 fresh vector-chain-rule samples across 10 templates** were independently differentiated from their displayed prompts; additional sign/translation boundary regressions cover the repaired exponential/cosine family. Ratio-integral tests cover all three upper-bound families at both powers.
- The 11 exact proposed stored records passed **46 actual grader checks**, including acceptance of old and new blank entries and rejection of wrong entries. Radio choices were all selected by their original field-owned IDs.
- Every modified scalar value was proved equivalent. The native general equivalence helper cannot resolve some translated trig/exponential and logarithmic forms; those radio families use their strict scalar reader and exact symbolic proofs, plus actual ID grading. No unresolved comparison was treated as proof.
- All proposed questions were rendered through the unmodified learning UI. Representative screenshots were inspected. Initial rendering exposed a correct-choice formatting cue in the vector bank; the entire bank was corrected, retested and rendered again before database submission. The added assignment steps were also rendered separately. Retained rendering reports pass.
- Native database preview and committed receipt contain exactly the intended content changes, generator registration change, and transaction metadata. Complete affected question ownership trees and registration were read back at **T6135**, with no learner-state mutations.

`check_repairs.py` regenerates the exact content plan and grading inputs. `database_repair.py` publishes the new immutable package, prepares native validated CAS forms, retains the exact request key/payload, and verifies its committed result. Never create a new request key to recover an unknown outcome; reuse the retained intent.
