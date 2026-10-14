# Extraction and sampling contract

The row-by-row original descriptions and evidence are in classification.md and
source.json. source-choice-mapping.json records every supported original choice,
its field, complete value, profile and correct designation. The Boolean profiles
have true/false literal alternatives owned by each statement field. Radio profiles
retain their exact five statement-subset strings, including which subsets are
absent. There are no inferred numerical distractors or mixed banks.

The mathematical backbone is a square real matrix, one sufficient given about
its nullspace, a nonzero homogeneous solution, determinant, or full rank; three
statements; the invertible matrix theorem; examining I, II and III in order; and
one concrete concluding subset. In the nullspace templates, extracting one or
two independent spanning vectors precedes the three theorem consequences. A
nonzero solution only establishes singularity, not exact rank or nullity.

The source's exact Markdown, checkbox keys or radio selection key, answer banks,
theorem display and repeated step-by-step solution sentences are reused as
parameterized strings. The generated correct answer is computed from the given
first using exact SymPy rank and theorem predicates. Domain constraints preserve
which statements are true for each observed profile; rendered source solution
judgments remain valid and an independent validator reads them back.

## Slots

- Square size n for determinant/full-rank templates: integers 3–7; observed sizes
  are 4, 5 and 6. This is a conservative same-method extension. Every matrix size,
  exponent, full-rank claim, pivot count and theorem reference changes together.
  The false rank=4 claim in q-79349 is specifically rank=n−1. Its n−1 reference
  changes independently of full-rank n references.
- Determinant d: fixed zero for q-141198; ±1..±4, excluding zero, for the other
  determinant profiles. Source values -1 and 1 remain replayable. Changing d
  among nonzero values alone is not a new task for inventory.
- Nonzero homogeneous vector: n fixed at its source value (4 or 5); each integer
  component in [-4,4]; reject the zero vector. Any direction is eligible because
  no source reasoning relies on a particular zero coordinate. The zero/nonzero
  pattern and signs vary. Scalar multiples are the same assessed relation and
  are deduplicated by their exact normalized span.
- Explicit nullspace coefficient matrix: retain source ambient dimension, one
  or two free parameters, zero pattern and disjoint nonempty column supports.
  Every nonzero coefficient ranges over ±1..±4. Exact full column rank is required.
  These coefficients affect both the given symbolic vector and every vector in
  its worked-solution decomposition. Independent spans vary; a change of basis
  within the same span is deduplicated. Source coefficients, including -2, 2,
  and 3, remain replayable.

The number of statements, supplied object roles, mathematical operators, source
claim predicates and ordering, field layout, nullspace free-parameter count and
solution stages are fixed. Holding these fixed preserves the source method and
workload. There is no arbitrary matrix calculation, determinant computation,
new answer fragment or added reasoning stage.

Each template has one full observed bank profile. The allowed constraints ensure
the independently calculated subset belongs to that bank. source-replay.json
reports exact prompt/solution matches and matched/total choices and distractors;
every option maps once, ignoring order. q-142367's `lI only` label has unresolved
intent and is excluded rather than silently corrected. q-34936 lacks enough data
to replay a complete bank and remains explicitly incomplete.

## Distinctness and limits

The fingerprint reads rendered givens and claims. It includes ambient dimension,
given type, canonical exact row space of the spanning-vector transpose, and the
unordered substantive claims. It excludes answer order, field layout, seed,
identity, equivalent vector scaling or basis changes, and determinant magnitude
within the same zero/nonzero class. Stable UUIDs hash the full authored content;
changing seed without changing content preserves every question/field/answer ID.
Content comparison rejects mathematical duplicates even when their full authored
renderings differ. Existing originals and canonical examples are always excluded
at Preparation; no new identities are attached to source questions.

Domains are bounded. Each scalar template has at most five distinct tasks (one
per n), irrespective of nonzero determinant choices. Vector templates have at
most 9ⁿ−1 parameter tuples before equivalent-direction reduction. A nullspace
profile with m nonzero slots has at most 8ᵐ tuples before basis-equivalence
reduction. These are upper bounds, not promises of fresh supply. Bounded seeded
sampling fails explicitly if it cannot satisfy the requested distinct count.
Inventory freshness is established against the database, not implied by sampling.

review.md pairs every supported original with a changed mathematical given.
validation.json records per-slot boundary, sign and size coverage, rendered math
checks, deterministic replay, duplicate reduction and actual learner grading.
