# Classification

Database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The unchanged wrapper/record is in `source.json`; canonical example is e-2480 and is not counted as practice.

There are 13 observed practice questions, all rated: easy 4, moderate 5, hard 4. Every source response is a five-choice math radio. q-32353 has two captured fields but original lesson widget evidence confirms one learner response. All prompts, choices, and solutions contain text mathematics; no plots or parameter-dependent assets occur.

| Level | Template | Source | Field style | Complete banks | Plot |
|---|---|---|---|---|---|
| easy | `scalar_log` | q-128586 | radio; tuple math | 1 observed; 1 authored default | none |
| easy | `scalar_power` | q-128587 | radio; tuple math | 1 observed; 1 authored default | none |
| easy | `scalar_exp` | q-128894 | radio; tuple math | 1 observed; 1 authored default | none |
| easy | `scalar_base` | q-33446 | radio; tuple math | 1 observed; 1 authored default | none |
| moderate | `dot_polynomial` | q-32298 | radio; basis math | 1 observed; 1 authored default | none |
| moderate | `dot_self_cubic` | q-32804 | radio; basis math | 1 observed; 1 authored default | none |
| moderate | `dot_self_shifted` | q-32835 | radio; tuple math | 1 observed; 1 authored default | none |
| moderate | `dot_self_evaluate` | q-32837 | radio; basis math | 1 observed; 1 authored default | none |
| moderate | `dot_log_reciprocal` | q-33336 | radio; basis math | 1 observed; 1 authored default | none |
| hard | `cross_matrix` | q-32353 | radio; matrix math | 2 (active + legacy) observed; 1 authored default | none |
| hard | `cross_monomials` | q-128896 | radio; tuple math | 1 observed; 1 authored default | none |
| hard | `cross_shifted` | q-32347 | radio; tuple math | 1 observed; 1 authored default | none |
| hard | `cross_self` | q-32836 | radio; tuple math | 1 observed; 1 authored default | none |

Changed coefficients do not count as new recovered templates. The polynomial/exponential scalar structures, direct/self/evaluated dot products, and vector representations have distinct prompt or solution structure and remain separately implemented. No practice level is missing; no unrated source is present.

The lesson route was read from `:activity/first-step` then `:step/next`: Introduction → sum/constant example → scalar multiple example → chain tutorial/example → product tutorial → product example. The product tutorial explicitly includes dot and ordered cross products and warns about anticommutativity. The owning topic follows componentwise vector differentiation and component dot products. The canonical example uses a two-component dot product with a root, reciprocal, polynomial, and exponential. Easy scalar-product questions overlap the preceding scalar-multiple KP in this capture; moving or replacing them would violate observed fidelity.

Within-level authored variation preserves those demands. Easy retains one scalar product and component derivatives, with power/exponential/cancellation structures. Moderate retains one dot-product rule, including observed first/second derivatives or one evaluation. Hard retains two ordered cross-product expansions (or the observed self-cross zero term). Coefficient/shift variation and monomial powers within small bounds do not introduce a new branch, progression, or skill.

Source anomalies are supported repairs, not invisible exclusions. See `template-extraction.md`. Every displayed original value is retained and replayed, including the legacy bank; the nonexistent correct designation is not counted as matched.
