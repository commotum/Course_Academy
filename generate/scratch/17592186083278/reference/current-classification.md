# Current source classification and bounded replenishment

Database math; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1; captured basis 2682. Exact current records are in initial/kp.edn. The original source.json at basis 1356 remains immutable evidence; validation.json reports that historical fidelity separately. Current bank: 12 practice questions, six easy, five moderate, one unrated; no observed hard. Canonical e-6240 remains separate.

| Level | Source | Mathematical backbone and field shape | Plot rating |
|---|---|---|---|
| easy | q-20853 | linear x, quadratic y; one parameter, five math radio options | none |
| unrated | q-21206 | linear x, cubic y; five math radio options; missing key/solution/difficulty | none |
| easy | q-21072 | shifted/scaled sine-cosine; closed half period; five text parameter-set radio options | none |
| easy | q-350359 | quadratic x, cubic y with two rational roots; two ordered blanks | none |
| easy | q-350368, q-357255 | exponential times sine/cosine, horizontal; product rule and quarter angles; two ordered blanks | none |
| moderate | q-21081 | sine-cosine full right-open period, vertical; four checkbox propositions I–IV | none |
| moderate | q-122726, q-122472 | power x, linear y, vertical; five math radio options; distinct complete banks | none |
| moderate | q-350382 | exponential cos/sin, vertical; two ordered blanks | none |
| moderate | q-350373 | cubic x with repeated derivative root, quadratic y; one blank | none |
| easy | q-133288 | eagle flight contextual subpart, positive time, one radical blank; setup absent from standalone prompt | none in subpart |
| hard | authored paired_cubics | two cubics, two distinct requested roots and two nonconstant companion checks; two ordered blanks | none |

The current collection has eleven source templates: eight historical families, with vertical circle now a distinct checkbox contract replacing the historical duplicate-radio representation; three added backbones (vertical spiral, repeated-root cubic/quadratic blank, contextual eagle). The power family's exponent parity is a slot in the same differentiation/solve/nonzero-check backbone; its even-power bank is a separate profile. Easy uses radio and paired blanks plus the contextual single blank. Moderate uses radio, checkbox, single blank and paired blanks. Hard is authored, with two blanks and no observed calibration.

## New and changed source extraction

q-122472 specifically supplies x=3t^4,y=8t on the reals; dx=12t^3,dy=8; root t=0. Complete radio values are 12,3,0,-8,8, with 0 correct. Generalized template x=a(t-s)^n,y=bt has nonzero a,b; differentiate, solve isolated power, check b. Its complete observed bank at the anchor is {an,a,s,-b,b}; this is a separate profile from q-122726's {an,a,b,-1,s}. Intent of coefficient distractors remains uncertain. The validated historical generator conservatively samples only odd n in {3,5,7}; the even-power profile is classified and mathematically checked but is not a newly implemented generator profile.

q-350382 supplies x=e^t cos(t),y=e^t sin(t), [0,2pi], vertical, ascending fields 1 and 2 (captured pull order 2 then 1). Product differentiation gives dx=e^t(cos-sin),dy=e^t(sin+cos); solve tan(t)=1, obtain pi/4,5pi/4, and check dy=±sqrt(2)e^t. This is distinct from the horizontal spiral contract. No distractors. Its fixed variable roles, product-rule stages, domain and ordering are retained in current-source validation. No new normal sampler for this source is claimed.

q-350373 supplies x=t^3-6t^2+12t,y=4t^2-3t on the reals, vertical, one blank equal to 2. dx=3(t-2)^2,dy=8t-3; factor, solve the repeated root and check dy(2)=13. General form dx=a(t-r)^2 with linear companion derivative would preserve its backbone. This single-blank contract is separate from paired_cubics' two-root hard contract. No new sampler is claimed.

q-21081 currently supplies x=4sin(t)+7,y=4cos(t)+10 on [0,2pi), vertical. Proposition slots are pi/4,pi/2,3pi/4,3pi/2 with boolean key false,true,false,true. Each field owns exactly text true and false. Different field layouts are not merged: historical radio replay remains historical only. The solution's derivatives, full roots and nonzero checks are unchanged. This replenishment does not emit variants from the obsolete radio circle family; it can replenish moderate from the unchanged power-line family.

q-133288 asks only for a flight-path time; its worked solution references prior parts and gives dx=5/(25+t^2),dy=t^2-2, domain t>0, answer sqrt(2). This is insufficient standalone prompt context for independent generation. It is preserved and conservatively excluded from this job's validated inventory. No missing setup is invented, and no shared context or assets are altered.

## Validation and capability boundaries

Existing generator source replay: all eight historical prompts, seven worked solutions, twelve complete field banks, 36 exact values; explicit source omissions remain evidence-only. Existing validation rerun checks 315 samples, boundaries, mutation rejection, deterministic identities, and actual native grading including accepted equivalent and rejected incorrect blank entries. Current complete source mathematics is separately read from displayed equations: solve the requested derivative on the displayed domain, check every companion derivative, compare every key and complete radio set, read the current checkbox propositions, and compare displayed derivatives. Native grading exercises each current source field's complete radio/checkbox bank and each canonical/incorrect blank value.

Replenishment is bounded to existing validated polynomial_two (easy), power_line (moderate), paired_cubics (hard) samplers. This does not claim implementation or current-source fidelity for the new/migrated families. All three difficulty bands have validated generation capability. The hard label is an authored workload claim documented in classification.md. Finite candidate sampling is capped at 20 attempts per level; any remaining shortage is explicit in the result rather than filled with aliases. No new plots are needed by the selected samplers.

Distinctness normalizes nonzero derivative scalars and constant translations, includes requested orientation and domain, and compares against every parseable source and canonical example, including the unrated cubic. A new seed, UUID, option order, translation or scaling alone cannot satisfy the target. Current shown/reserved questions are excluded using the existing learner/activity schema. The contextual eagle cannot collide with selected polynomial tasks: its derivative is rational and its domain is positive time, whereas selected tasks use polynomial companions on all reals.
