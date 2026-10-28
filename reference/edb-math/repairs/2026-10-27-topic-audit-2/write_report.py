import json
from pathlib import Path
H=Path(__file__).resolve().parent
read=lambda n:json.loads((H/n).read_text())
v=read('final-verification.json');grade=read('final-check/grading.json');render=read('final-check/rendering.json');assets=read('assets/render-validation.json')
assert read('published-probe/verification.json')['actual_published_entrypoints']==22
assert v['passed']and render['passed']and assets['passed']and not grade['documented_unresolved_checks']
assert not v['remaining_unkeyed_fields']
commits=[(n,read(n+'/verification.json'))for n in ['q334121','commit-group-1','commit-group-2','commit-group-3','supplemental-memberships','supplemental-banks']]
topics=read('inventory.json')['topics'];publications=[p for g in range(1,4)for p in read(f'commit-group-{g}/generator-publications.json')]
report=f'''# Topic formatting, import and question audit — second batch

Completed the requested three-agent pass over all **44 topics**, **3,012 unique questions/examples**, **98 tutorials**, and their scoped activity steps and multistep contexts. The original snapshot is basis **9122**; final live verification is basis **{v['basis_t']}**. This batch is separate from the earlier 38-topic linear-algebra audit.

## Repairs committed

- **{v['scalar_changes']} scalar changes**, including source formatting, reconstructed cloze formulas, worked solutions, canonical links and answer-type corrections.
- **{v['created_owned_answers']} new field-owned canonical answers**. Thirteen complete previously empty blank banks; two deliberately authored alternatives correct invalid original-source banks. Existing values, entity IDs, UUIDs and learner responses are retained except for the individually reviewed scalar content changes.
- **{v['membership_retractions']} membership retractions**: 20 obsolete duplicate fields and 10 obsolete/contaminating/duplicate choices. Every detached entity remains in the database; reviewed detached answers have no retained learner response references.
- **22 generator registrations updated**, with exact package digests and live registration readbacks verified. There were 23 immutable package publications: the installed-entrypoint smoke test exposed one repository-ancestor helper lookup, which received a self-contained corrective successor. The final installed entrypoints all pass. No learner activity, XP, responses or timing was fabricated for testing.

| Batch | Committed basis | Scalar changes | Membership retractions | New answers |
| --- | ---: | ---: | ---: | ---: |
'''
for n,r in commits:report+=f"| {n} | {r['basis_t']} | {r['scalar_changes']} | {r['membership_retractions']} | {r['created_owned_answers']} |\n"
report+='''
Each batch saves its exact EDN transaction, guarded before-values, stable request identity, speculative native preview, durable receipt, exact expected datom comparison and readback. Final verification also checks every original question/field/answer UUID, expected memberships, canonical ownership, reviewed scalar value and registered package digest at one fresh basis. Original pool links remain present; unrelated background additions are allowed.

Three real learner blank responses arrived during the audit. Their task response references and sole field ownership were verified and their entities retained in the final model. They are separate from the 15 authored answer additions; no learner response was removed or normalized.

## Root causes and prevention

1. **Nested cloze capture lost the enclosing formula.** Historical extraction sometimes used the first MathML found inside a selected/default option. Controls are now indexed before the enclosing MathML walk and matched by their actual owning DOM control. Unsolved default states are layout evidence only; verified solved state supplies correct-answer evidence. Real solved and unsolved capture fixtures cover the repair.
2. **Historical upserts contaminated banks and duplicated fields.** Some complete keys pointed at another slot's prose conclusion; old same-key fields survived beside complete replacements. Source control indices plus independent mathematical checks establish the repaired field roles. Unused contaminating memberships were detached without deleting entities or rewriting responses.
3. **MathML semantics were dropped.** Source function-application markers under powered trig expressions, visible set braces, fonts, and teaching colors were lost. Repairs use retained source semantics, including powered operators; they do not guess functions from arbitrary unmarked words.
4. **Rendering configuration and table borders lost valid source presentation.** The local MathJax 3.2.2 renderer now loads its matching [boldsymbol extension](https://docs.mathjax.org/en/v3.2/input/tex/extensions/boldsymbol.html). Source fraction tables preserve numerator/denominator control placement and `hidden` border precedence, following the [CSS collapsed-border rules](https://www.w3.org/TR/CSS22/tables.html#border-conflict-resolution). Intentional diagrams and other source images remain images.
5. **Undefined commands and integral layout escaped ordinary rendering checks.** Glued commands such as `\\intx` were exposed by disabling MathJax's undefined-command fallback during QA. Source-proved command boundaries and standalone display integrals are repaired. Generated-record validation also rejects duplicate present field keys and validates checkbox display labels. Shared importer/generator documentation records these checks.
6. **Some generators repeated formatting defects or had operational defects.** The 22 successors include formatter prevention, supported-batch deterministic retry fixes, a slope-bank separation repair and generated-asset identity fixes. Fresh content identities are computed independently of temporary execution/output paths. Relocation tests verify IDs and image bytes. Retired/structurally-contained questions stay excluded from fresh standalone source use.
7. **A few defects originated in the source mathematics.** These are explicitly authored corrections rather than claimed source recoveries: branch/equilibrium qualifications, a system-frequency typo, an equivalent duplicate correct option, and the invalid banks in q106074/q337099. The latter two received new correct alternatives and independently checked solutions; all original alternatives remain retained. Separate supplemental evidence gives the exact derivations and domains.

## Validation and limits

'''
report+=f"- Final native release grader: **{grade['accepted_checks']} accepted + {grade['rejected_checks']} rejected** checks; **{grade['documented_unresolved_checks']} unresolved grading checks**. Every active required field has an owned canonical answer; no active duplicate field keys remain. Native dispatch compatibility is distinct from independent mathematical proof.\n"
report+=f"- Strict actual player rendering: **{render['fields']} fields**, **{len(render['failures'])} failures**. All **694 unique retained image files** decode on desktop and mobile, **1,388 checks**, no missing images or image overflow. Actual interactive select, checkbox, blank, fraction-table and graph controls also have group-specific desktop/mobile evidence.\n"
report+='''- **87 focused importer/formatter/browser regression tests pass.** The current native grader was rebuilt before testing; an older fixture incorrectly lacked existing plus/minus support and was not used to justify content changes.
- All 90 active generator registrations were reviewed through their packages and sampled outputs; 22 required successors. A further smoke test executes all 22 actual published entrypoints, with no excluded-source hits or database writes. All authored completions and changed mathematical statements have individual derivations. Group reports separately record residual, branch, model, checkbox and source-provenance checks for current and fresh samples.
- Retained original prompt evidence exists for **1,341** records. **401** source-identified records lack retained original prompt evidence; **1,270** generated/authored records have no Math Academy source identity. Source gaps are named in the group ledgers, not represented as verified source matches.
- This is exhaustive scope/inventory and defect-candidate review, not a proof of every unchanged intermediate calculation or all possible generator parameters. Parser and qualitative-graph limits remain explicit in each group report. q64220 retains a valid positive-branch `ln x` form; full real-domain `ln|x|` coverage remains a separate mathematical-content consideration.
- Noncanonical historical learner inputs containing `\\placeholder{}` are preserved. They are not authored learner-facing choice banks and are excluded from authored-content rendering claims. Genuine parent-contained steps retain their parent givens instead of being rewritten as standalone questions. Raw replay evidence can retain historical source defects; fresh serving output is tested separately.

## Evidence

The group reports are frozen pre-integration handoffs. This report and the final database verification supersede their pending repair/allocation lists, including the two subsequently completed source-bank corrections.

- [Group 1](group-1/README.md), [Group 2](group-2/REPORT.md), [Group 3](group-3/HANDOFF.md).
- [Final database verification](final-verification.json), [native grading](final-check/grading.json), [strict rendering](final-check/rendering.json), [asset checks](assets/render-validation.json), [focused regressions](focused-regressions.json).
- [Installed generator entrypoints](published-probe/verification.json), [outside-repository supported-band tests](group-1/outside-repository-validation.json), [corrective package registration](corrective-generators/generator-publications.json).
- [Supplemental source-bank corrections](group-2/supplemental-bank-plan.json), [source eligibility](source-eligibility.json), [scoped parent contexts](scoped-contexts.json).

## Requested topic coverage

| Topic entity | Title | Questions/examples |
| --- | --- | ---: |
'''
for x in topics:report+=f"| {x['entity']} | {x['title']} | {x['questions']} |\n"
(H/'REPORT.md').write_text(report)
print('Wrote',H/'REPORT.md')
