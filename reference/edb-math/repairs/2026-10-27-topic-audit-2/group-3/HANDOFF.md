Group 3 handoff — EDB basis 9122

Frozen integration files:

- `proposals.json`: 92 exact content attributes (source notation/display repairs, two source fraction tables, and nine authored domain/completeness changes).
- `completion-solutions.json`: 35 authored worked solutions.
- `missing-key-completions.json`: 39 completions using existing owned answers.
- `dependence-correct-link-repairs.json`: four wrong canonical links repointed to existing owned numeric answers.
- `dependence-bank-membership-proposals.json`: four unused prose contaminants detached from numeric banks.
- `duplicate-field-membership-proposals.json`: ten obsolete duplicate field memberships detached; all field and answer entities retained.
- `generator-candidates.json`: five successors with exact publisher descriptors and approved digests.

The q334121 type changes and two duplicate choice detachments were already committed by root at T9129. They are applied only in the local validation snapshot and excluded from the integration files above. No learner keystrokes, responses, history, or entity identities are rewritten.

Coverage: 1,012 questions in 15 topics, 34 tutorials across 204 activity steps, plus 14 multistep contexts containing 25 scope questions. Original sources are retained for 475 of 621 source-identified questions; 146 originals are missing, and 391 generated records have no original question ID. See `coverage-by-topic.json` and `missing-source-ledger.json` for the complete membership ledger.

All 40 checkbox display labels were rendered with actual controls and independently checked mathematically. Twenty agree with retained original statements directly; one differs only in equivalent infinity notation; seven are Boolean none-of-above conclusions derived from the original statements; twelve lack retained original archives. No checkbox labels required speculative recovery. See `checkbox-key-coverage.json` and `wronskian-math-validation.json`.

Validation:

- Current release native grader: 959 field-bearing questions, 4,397 checks, all expected results; no remaining missing keys or duplicate field keys in the proposed snapshot.
- Strict actual renderer: 6,331 visible fields including contexts. The sole remaining failure is retained noncanonical learner input answer17592186577462 on q314194 containing `\placeholder{}`. Canonical authored content passes.
- Actual controls: 58 questions, all 40 checkbox labels, 25 selects and two math blanks; desktop and mobile, no overflow. Source fractions retain the numerator blank at row0/column1 in q167783 and denominator blank at row1/column2 in q355560.
- Existing scalar mathematical checks: 500 attempted records, 427 direct canonical passes, 24 apparent mismatches resolved through complete response frames, parent givens, and branch analysis. The 49 without a usable canonical at that stage are separately recorded. All 35 authored completion questions/39 keys have independent derivations and checks.
- Wronskian checks cover all 39 questions and all 40 checkbox truth values. Forty-four equilibrium candidates were reviewed. Two actual lost-equilibrium omissions and three positive-branch/domain omissions receive explicit authored repairs.
- Generator review covers all 31 registered packages: 583 fresh/template/API/source-evidence records; 580 gradable records pass 2,628 native checks. The separate scalar checker attempts 344 generator records, while 151 model/ellipse/curve calculations pass independent checks. The 22 scalar candidates are classified separately, including one preserved wrong raw source key.
- Final successor and relocation samples: 56 records, 238 native checks, 337 strict-rendered fields, all pass. Seven packages, including all three graph generators, preserve question/field/answer IDs and asset bytes across package and output-directory relocation. Nine fresh graph controls pass desktop/mobile rendering and image decoding. Content-addressed publication path rewrites preserve all IDs.

The five successor packages are KP92260, KP92261, KP78584, KP68842, and KP87839. Each contains the latest shared formatter and `repair-evidence.json`; source JSON bytes are unchanged. KP87839 fixes an absolute generated-image path entering its content UUID, using image bytes before identity instead. KP96698 and KP87840 already pass relocation without a successor.

Raw source evidence stays separate: q11816 replay preserves its historical wrong key and missing solution; four `\lnx` answer strings remain in raw combined-integral replays. Those are evidence-only outputs, not fresh learner banks. Three raw evidence records are fieldless or lack a key and are not graded. Latest fresh output passes strict rendering.

Limits: this is not an independent proof of every intermediate calculation in all 1,012 records. The scalar checker explicitly records 180 existing and 58 generator parser/method/graph limitations; qualitative graphs, fieldless canonical examples, and certain response fragments need additional human mathematical review beyond source/render agreement. No unproved numeric conclusion is represented as an automated pass. Source graph assets and meaningful teaching stages are retained.

See `handoff.json` for structured counts and SHA-256 hashes, `generator-candidates.json` for publication digests, and the validation files and screenshot folders for evidence. This child performed no live database writes or publication.
