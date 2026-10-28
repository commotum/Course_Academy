"""Consolidated report from actual committed receipts and final verification."""
import collections,json
from pathlib import Path
H=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
f=read(H/'final-verification.json');assert f['passed']and not f['remaining_unkeyed_fields']
g=read(H/'final-check/grading.json');r=read(H/'final-check/rendering.json');assert not g['documented_unresolved_checks'] and r['passed']
probes=read(H/'published-probe/verification.json');assert probes['passed']
commits=read(H/'commits.json');pubs=[p for batch in read(H/'publication-batches.json')for p in read(H/batch/'generator-publications.json')]
attrs=collections.Counter(p['attribute']for c in commits for p in read(H/c/'plan.json').get('cas',[]));unique={(p['entity'],p['attribute'])for c in commits for p in read(H/c/'plan.json').get('cas',[])}
assert all(read(H/n)['passed']for n in ['engine-regressions.json','importer-regressions.json','grader-api-verification.json','live-http-grader-verification.json','assets/render-validation.json'])
lines=[
'# Quality audit: 99 topics, 2026-10-28',
'',
f"Completed using three disjoint subagents and EDB. The scope contains **{f['topics']} topics, {f['questions_examples']:,} questions/examples, {f['tutorials']} tutorials, 311 knowledge points, and 265 initially registered generators**. All 41 scoped multistep parent statements were also checked. The baseline was T9837; consolidated readback is T{f['basis_t']}.",
'',
'## Repairs applied',
'',
f"The committed batches made {f['scalar_changes']:,} guarded scalar assertions ({len(unique):,} distinct entity/attribute pairs), created {f['created_owned_answers']} independently derived owned canonical answers for empty blank banks, and removed {f['membership_retractions']} obsolete duplicate field memberships. Their entities and histories remain present. The resulting {f['active_fields']:,} active fields have unique keys and owned canonical answers, with no unkeyed fields remaining. These counts include source notation and formatting restorations; they are not a count of distinct mathematical errors.",
'',
'| Committed batch | Transaction basis | Scalar changes | Detached memberships | New answers |',
'| --- | ---: | ---: | ---: | ---: |']
for c in commits:
 v=read(H/c/'verification.json');lines.append(f"| [{c}]({c}/verification.json) | {v['basis_t']} | {v['scalar_changes']} | {v['membership_retractions']} | {v['created_owned_answers']} |")
lines += ['',
'The substantive defects included lost cross-product/curl operators, a hidden alignment minus imported as a coefficient, a visible boxed placeholder discarded as spacing, matrix response frames flattened from source HTML tables, an answered historical capture leaking into the problem, missing canonical links/solutions, and stale generated notation. Source font roles, set braces, highlighting, and formula fences were restored where the original capture established them. Intentional source illustrations and valid authored notation variants were retained.',
'',
'Independent mathematical corrections were kept separate from source restorations. Examples include a contradictory parameter bound, an arccos domain intermediate that incorrectly excluded endpoints, a function label missing its third argument, and an ambiguous free-coordinate question clarified without changing its bank or answer key. Full start-point, interval, orientation, and component constraints were checked before judging alternative parameterizations valid; no radio-to-checkbox migration was warranted.',
'',
'## Preventing recurrence',
'',
f"**{len({p['kp']for p in pubs})} corrected generator packages were published and registered**, with immutable digest verification and probes of the actual installed entrypoints. Affected successors were checked outside the repository from two package locations and different output directories, including owned UUID and served asset-byte stability. Frozen per-group manifests document supported difficulty/template coverage and independent mathematical checks. Unaffected packages were sampled through their supported APIs; this is not a proof of every possible random draw.",
'',
'The question capture and historical importer now distinguish bare hidden MathML spacing from a decorated visible box. Authentic regression fixtures protect the phantom-minus and boxed-placeholder cases; a separate ordered-operator regression protects curl and scalar triple products. The generator and capture documentation now requires full task constraints, operator-role preservation, source identity verification, and archive discovery that includes hashed history captures and valid previous copies.',
'',
'The shared grader now admits and compares supported whole polynomial circle equations after rearrangement or nonzero rational scaling, and recognizes the imported Unicode multiplication glyphs. Wrong centers/radii remain rejected. These engine changes passed the full unit suite and read-only answer-preview API checks. The application was restarted with the repaired learning binary; no QA attempts, XP, exposure, or timing records were created.',
'',
'## Verification and limits',
'',
f"- Consolidated native grading: **{g['accepted_checks']:,} accepted canonical checks, {g['rejected_checks']:,} rejected incorrect checks, zero unresolved**. Selection checks verify the actual owned answer identity dispatch; independently derived mathematics is recorded separately in the group proofs.",
f"- Strict actual-player rendering: **{r['fields']:,} fields, zero unresolved TeX commands or leaked display fences**. Stored learner keystrokes are not treated as authored math.",
'- Source assets: 4,091 unique served files, 8,182 desktop/mobile decode and overflow checks, zero missing assets. Actual question controls, including every scoped checkbox label and matrix/rich blank layout, received separate viewport checks in the group reports.',
'- Regression suites: 247 engine unit tests and 46 focused importer tests passed; read-only native/API circle and multiplication checks passed.',
'- Every original question, field, and answer UUID was retained; the original topic/KP pool links remain. Each write used compare-and-set or full-membership guards, native speculative preview, an explicit agent source, stable request identity, exact receipt-datom comparison, and readback. Detached banks were checked for current and retained learner-response history at the guarded write basis.',
'- Original problem captures were available for **4,112 of 4,221 source-ID records**. The remaining **109 lack a retained original prompt**; solution-only or bank-only evidence was not counted as an original prompt. Their current structure, rendering, and grading contracts were checked, but source fidelity cannot be certified without the missing material. The other 3,623 records are generated and have no original MA question ID.',
'- All visible strings and response contracts were audited. Mathematical proof is family-specific and strongest for changed content and affected generator families; this report does not claim an independent symbolic re-solution of every unchanged question or every tutorial intermediate.',
'',
'## Evidence',
'',
'- [Exact final readback](final-verification.json), [native grading](final-check/grading.json), [strict rendering](final-check/rendering.json), [installed generator probes](published-probe/verification.json).',
'- [Group 1 content handoff](group-1/content-handoff.json), [group 2 content handoff](group-2/content-freeze-1/handoff.json), [group 3 content handoff](group-3/content-handoff.json). Later group 2 source supplements and clarification are included in the transaction table.',
'- [Per-topic inventory](inventory.json), [complete KP topology](complete-kp-topology.json), [source eligibility](source-eligibility.json), [mathematical correction reconciliation](authored-reconciliation-verification.json).',
'- [Engine regressions](engine-regressions.json), [importer regressions](importer-regressions.json), [live HTTP grader verification](live-http-grader-verification.json), [application activation](app-activation.json).',
'']
if f.get('additional_pool_links_since_snapshot'):lines += [f"Additional pool links observed after the baseline: {f['additional_pool_links_since_snapshot']}. See the supplemental audit before treating these newer records as covered.",'']
(H/'REPORT.md').write_text('\n'.join(lines));print('Consolidated report written:',H/'REPORT.md')
