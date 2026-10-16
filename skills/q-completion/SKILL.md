---
name: q-completion
description: Complete incomplete Course Academy EDB question entries by extracting templates from nearby questions and the KP canonical example, authoring missing worked solutions, identifying correct answers, and validating and saving the repair. Use for missing correct-answer links, absent solutions, or incomplete answer fields on existing questions; generator creation belongs to generate/docs.
---

# Question Completion

Complete the requested existing question or explicit set of questions. Reuse the
template-extraction approach in `generate/docs`, then prepare and verify a narrow
EDB repair. The result is complete question content that the application can grade
and explain.

Resolve this skill directory's symlink before following repository links. Its
canonical location is `Course_Academy/skills/q-completion`; the repository root is
two levels above it. Use [$edb](../edb/SKILL.md) for database access and transactions.

## 1. Inspect the question and its teaching context

Resolve the supplied `:db/id`, UUID, or source identifier in the configured
database. Capture one database value for related reads; record its basis and
target identity. Batch the question, owning KP, canonical example, and nearby
practice questions with Datalog and Pull.

Read the complete problem, worked solution, difficulty if present, answer fields,
field types and keys, choices, canonical answers, and relevant assets. Identify
what is missing, what is inconsistent, and what is already complete. Reproduce a
reported grading error through the application's read-only preview when useful.

At a minimum, inspect the KP's `knowledge-point/canonical-example` and its worked
solution. Prefer nearby questions in that KP with matching mathematical structure,
field layout, and difficulty; numerical similarity alone does not establish a
matching family. If the canonical example is absent or incomplete, record that
gap and use other verified matching examples where available. Do not claim to
have recovered a canonical solution template without evidence.

## 2. Extract the matching template

Adapt [Template Extraction](../../generate/docs/4-template-extraction.md):

1. Describe the target and relevant examples individually: mathematical
   structure, parameter values and properties, domains, notation, Markdown,
   diagrams, answer-field layout, choice banks, and solution sequence.
2. State the family's shared mathematical pattern, required response, and
   instructional purpose.
3. Map the target's components to the examples: fixed wording, variable values,
   intermediate calculations, answer values, and optional or conditional steps.
4. Extract a reusable worked-solution template from the canonical example,
   supported by matching nearby solutions. Record the constraints that make it
   applicable to the target.

Preserve the teaching method, sentence structure, and step order when they fit.
For mixed fields or multiple parts, account for the entire response and how each
field maps to the problem. Treat different equation fragments, domains, branches,
and response structures as distinct templates.

Account for every existing choice as a complete mathematical value. Recover
distractor recipes only when needed to complete an incomplete bank; do not build
a new generator or expand the bank as part of ordinary answer-key completion.
Inspect any plot needed to solve the target rather than inferring its content
from surrounding prose. Reuse [Plot Extraction](../../generate/docs/5-plot-extraction.md)
when visual structure needs reconstruction.

## 3. Solve and complete the existing content

Solve the target independently. Nearby questions supply the template; the target
problem supplies its answer. Use exact calculations where applicable and check
domain restrictions, units, notation, and whether the question has a unique
answer under its response type.

Instantiate the recovered solution template with the target's names, values,
intermediate results, and conclusion. Check every substituted value, including
labels in prose and figures. Supply a worked solution for each question completed
by this workflow, even though ordinary questions allow it to be absent in schema.
Preserve a valid existing solution; correct inconsistent existing content only
within the requested repair scope.

Use the installed content representation:

- `question/worked-solution` holds Markdown with LaTeX for the whole problem.
- `answer-field/correct` points to an answer owned through that same field's
  `answer-field/choices`; it does not hold a string or a question-wide key.
- Radio/select: find the unique correct existing choice and reuse its identity.
  An absent or multiply matching choice is a content defect to resolve, not a
  reason to select an arbitrary option. Compare complete mathematical objects;
  matrix dimensions, for example, are an ordered row/column pair, not a product.
- Blank: store the expected expression or equation fragment as a field-owned
  answer, reuse an equivalent existing canonical value where appropriate, and
  link it as correct. Keep the field key and expected answer shape intact.
- Checkbox: follow the installed per-option field representation, with owned
  text answers `true` and `false` and a canonical answer for each field.
- Free: an optional field-owned reference answer does not enable automatic
  correctness grading. Preserve that interaction type.

Authored mathematical answer values are delimiter-free LaTeX; prose and solutions
use Markdown math delimiters. Preserve existing question, field, and answer IDs,
choice banks, source IDs, and referenced historical responses. If an essential
diagram, statement, bank, or interpretation cannot be recovered confidently,
leave dependent fields unresolved and report the specific missing evidence.

## 4. Validate the completion

Check the instantiated solution against the independently derived answer. Ensure
every required field has a correct answer belonging to its bank, field keys remain
consistent with the problem, and no distractor is also correct under the task's
semantics. Validate rendering when LaTeX, Markdown tables, or figures changed.

Use the application's actual read-only grader: accept the correct response and
reject plausible incorrect responses. For radio/select, check all choices when
practical; for blanks, check supported equivalent entries and incorrect entries.
Mathematical agreement or schema validation alone does not establish grading
compatibility. Do not create learner attempts, exposure, timing, XP, or progress
to test a repair. In this repository, `scripts/developer_preview.rs` implements
`preview-answer`, exposed through `/api/preview-answer` by the running app.

## 5. Prepare the database repair

Follow [$edb](../edb/SKILL.md) and the installed schema in
`schema/content/{4-question,5-answer-field,6-answer}.edn`. Save a compact evidence
package under `reference/` containing source entity IDs and basis, the extracted
template, target parameters and derivation, proposed changes, and complete EDN.
Use the project's supported authored-content reconciliation evidence format
when available so later imports can recognize the contribution.

Attribute locally derived answers and solutions to the established configured
contributor. A solution inferred from examples is authored completion, not an
observed Math Academy answer. Preserve that distinction in saved evidence.

Prepare only the necessary assertions and retractions. Guard absence or the
observed old value with CAS; use a basis guard when other read dependencies must
remain unchanged. Ensure the installed question, affected answer-field, and answer
specs. Do not invent difficulty, calculator requirements, source IDs, attributes,
or schema. Missing ordinary-question difficulty is outside this workflow unless
classification was explicitly requested.

## 6. Preview, commit, and verify

For review-only requests, deliver the prepared repair. Otherwise finish authorized
database changes and verification without adding a separate confirmation step.

Use the existing native preview helper for specs with application predicates.
The generic `edb with` executable may report `native/deployment-not-found` for
`course-academy.answer-field/valid?`. Reuse
`capture.scripts.database.preview.preview_executable(Config(), stop_event)` with
`capture.scripts.config.Config`; it selects the matching build and registers the
application predicates. Keep validation intact rather than omitting the spec.

Save the exact request, target identity, source, guards, and stable request key
before submitting through the configured writer. Reconcile an unknown outcome
using that identical request. After a confirmed commit, verify the changed values
at the report's exact database basis, check for unexpected content or learner
changes, and run the read-only application grading checks against saved content.
An already complete question should produce no content changes.

Report what was missing, the derived correct answer, the supplied solution, and
what was actually verified. Keep prepared, committed, verified, and unresolved
outcomes distinct. Do not claim the question is repaired while grading still
fails or essential fields remain incomplete.
