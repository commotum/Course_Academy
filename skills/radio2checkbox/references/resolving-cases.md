# Resolving cases

## Candidate scope and evidence

Discovery heuristics suggest questions to inspect; they do not prove suitability or a correct key. Separate practice questions from canonical examples, and check reverse canonical membership even for a practice question. Prior discovery excluded canonical-only examples; that exclusion is scope, not a mathematical reason to retain radio.

For each candidate, inspect the full problem, solution, complete field banks and keys, difficulty, all KP/topic links, canonical links, option-specific feedback, and incoming uses. “Easy to handle” means low conversion ambiguity, independently of its easy/moderate/hard difficulty rating.

The strict historical cohort required explicit selectable statements, a complete unambiguous database key, one ordinary field, a difficulty, a stored solution supporting the key, and no unresolved images, labels, or metadata. Looser candidates need case-specific evidence. Do not infer missing fields from truncated Pulls.

## Choose the representation

| Observed structure | Decision |
| --- | --- |
| A listed finite universe; options such as “I and III only” | Usually convert after decoding every option and checking the solution |
| A listed universe with only one correct case | Still eligible; the question asks which cases apply |
| “None” or “All of the above” among combination options | Expand to empty subset or the actual full universe |
| Finite roots/points offered as combinations | May convert if selecting individual roots/points preserves the requested answer |
| Two ordered roots required in blanks; coordinates or an ordered tuple | Preserve the requested response structure; membership is not ordering |
| Single numerical/formula answer containing “and” or “or” | Not sufficient evidence of a subset task |
| One mutually exclusive category or a single best answer | Usually retain radio |
| Identity valid for every real parameter; answer “any real number” | Retain radio unless the prompt explicitly supplies finite cases to select |
| Multiple fields, duplicate fields, or no fields | Investigate ownership and intended response before constructing a replacement |

Build an explicit universe in source order. For each object record its source label, complete display content/text or image identity, independent truth value, and evidence. Keep the source label separate from the new displayed field key; it is the mapping token for old responses, not the checkbox caption. For **every** old answer record the selected subset. Check the database correct answer against that subset and the worked solution. An option referring to an absent case is an unresolved source defect, not a license to silently invent one.

A zero-selection answer must remain possible when mathematically correct or represented by an old option. Do not add a separate “None” checkbox merely to represent it. If learners need guidance, “If none apply, leave all boxes unchecked.” can accompany the selection instruction. Confirm the renderer submits explicit false responses for unchecked fields; an absent response is not automatically false in grading.

## Establish keys

1. Use an existing database key and preserve its semantics. Check that it belongs to its own field's bank; malformed or conflicting keys need investigation.
2. For a missing key, inspect the worked solution and original capture evidence before consulting `/home/jake/Developer/study/MA`.
3. Treat study keys as fallible LLM output. Record file, section/line, relevant content and hash, then solve independently with exact algebra/calculus or direct inspection. A matching study key alone is insufficient proof.
4. If mathematics conflicts with an existing database key or solution, document the discrepancy and resolve it as an explicit content repair. Do not let response-format conversion conceal a key change.

Useful evidence includes exact symbolic identities and roots with domain restrictions, determinant/rank calculations, limit or continuity conditions, point substitution, graph features, and counterexamples to false statements. Show the decisive calculation per class and retain per-question results. Numerical approximations can support inspection but do not settle exact equality or excluded endpoints.

For image **answer options**, recover the first answer filename from original capture ordering using the user's stated capture convention. Match it to the actual image and answer entity; rendered shuffling is irrelevant. Never treat the first returned reference, smallest entity ID, or current first displayed image as the key. Inspect images to establish what their contents mean and how each option maps to a subset. If the original ordering is missing, record that gap rather than guessing. A diagram in the problem can coexist with ordinary text answers and does not invoke the image-option convention. Some diagrams contain four cases even when an incomplete option bank omits IV.

## Labels, text, and metadata

- Recover Roman labels from original text/image evidence when OCR has produced `l` or `ll`. Do not normalize arbitrary letters by guesswork.
- Preserve named objects and source order. Use stable unique field keys after resolving repeated or missing labels. Missing source objects require evidence, not an extrapolation from the option bank.
- Inspect duplicated or multiple fields independently: they may be repeated captures or distinct parts. Audit answer ownership, feedback, incoming references, and existing learner selections before detaching anything.
- Translate option feedback only when its meaning applies to the new field. Question-level mathematical explanations remain unchanged unless an explicit repair is justified. Flag metadata that has no faithful translation.
- Add “Select all that apply.” only if an equivalent instruction is absent. Move the full selectable objects into their checkbox field keys and remove their list from the prompt. This applies equally to prose statements, equations, named matrices, roots, points, and other list items. Keep shared givens in the prompt: for example, a matrix whose properties are being tested remains there while the property statements move into fields. When the matrices themselves are the options, each complete matrix moves into its own field.
- Preserve mathematical names when useful: a field may show `$A=\begin{bmatrix}...\end{bmatrix}$` so the explanation can still discuss `$A$`. Remove presentation-only numerals and replace solution references such as “Statement II” or “II only” with the corresponding content. Retain complete multiline math and inspect it in the actual renderer; do not flatten several matrices into one horizontal expression.
- A source label alone is acceptable only when the selectable object cannot be independently displayed without losing a shared diagram/image's meaning. Record that exception per object with the captured image evidence and reason, and verify the visible image actually identifies each option. Prefer a meaningful caption such as “Graph I”. Separate matrix/equation text is not a shared-image exception; an unrelated image elsewhere in the question does not justify labels-only choices.
- Compare the latest prompt/solution against the audited version. Preserve intervening rendering corrections, including escaped set and piecewise braces. Re-review changed mathematical content or keys; do not overwrite them from an old snapshot.

## Learner meaning and unresolved decisions

An old choice “I and III only” maps to true for I/III and false for all other fields, even if that choice was wrong. “None” maps to false for every field. Preserve status, grading/progress, scores, XP, and timestamps. Do not fill unattempted task items with the correct response. Malformed/multiple old selections or a recorded grade inconsistent with the equivalent mapping require review.

Record `convert`, `retain_radio`, `repair_key`, or `needs_evidence` with a rationale. A missing key in an all-values identity question can warrant a key repair while retaining radio; this is a legitimate resolved case. Historical examples are q-9852 (`17592186060456`) and q-130626 (`17592186265945`) in the prior remaining-case ledger.
