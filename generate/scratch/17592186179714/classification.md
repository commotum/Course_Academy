# Calculating the Gradient Vector Field of a Function

Captured EDB basis: 2307. Immutable lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.
All nine practice questions and the canonical example were read together in
`reference/initial/kp.edn`; `source.json` retains the exact captured content.
No prior generator reference, UUID, script or scratch package existed. No job
`.generated` file existed at inspection. The scheduler's basis 1831 is stale.

| Difficulty | Field layout | Templates | Plot rating | Sources |
|---|---|---:|---|---|
| easy | one radio, key selection, five mathematical vector choices | 3 | none | q-122607, q-122599, q-122608 |
| moderate | same radio layout; three vector components | 5 | none | q-122404, q-122596, q-122600, q-122601, q-122617 |
| unclassified | one five-choice radio without correct reference | 1 tentative | none | q-122399 |
| hard | no observed template | 0 | none | none |

Each rated template has one complete observed bank profile. Every option is
mapped, without pooling distractors, in `source-bank-replay.json`. Source IDs,
original parameters, individual functions, answers and solution sequences remain
available in `source.json` and `reference/replay.json`.

The incomplete q-122399 asks for the gradient of x²-xy+3y²-4y. It has no
rating, worked solution or correct reference. Its mathematically correct option
is (2x-y)i+(6y-x-4)j, but it is excluded rather than repaired or silently rated.
It is distinct from the three rated easy backbones and has no generated family.

The q-122601 source's arctangent partial derivatives and correct choice agree.
Its final assembled solution incorrectly prints zz in the j numerator; xz is
required by partial differentiation. New variants assemble from the computed
partials and correct this typo locally. The historical source is untouched and
excluded from validated inventory because its solution is inconsistent.

Canonical e-9453 is an exponential example, not practice and not inventory.
It supports interpreting gradient notation but supplies no practice difficulty
or choice bank, so this generator does not extrapolate an exponential family.

Hard capability is unsupported by this package: no observed hard prompt,
solution, field or bank supports a same-backbone generalization at that level.
This is a bounded evidence exception, not a claim that hard gradient questions
are mathematically impossible. New source evidence reopens classification.
