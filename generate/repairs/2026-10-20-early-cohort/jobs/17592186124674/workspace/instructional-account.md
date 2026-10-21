# Modeling inhibited growth

The learner identifies the changing quantity X and its equilibrium a, distinguishes
any initial stock from that equilibrium, then translates positive growth proportional
to the remaining gap into dX/dt=k(a-X), k>0. The response is one whole-equation
radio selection from five alternatives. Solutions state the general model and
substitute the equilibrium; integration and parameter fitting are outside this task.
The requested easy band is supported. Existing moderate/hard coefficient-placement
extensions are retained without a new source-fidelity claim for those bands.

Tutorial 9afedae3-a674-5a44-9d7a-4cdf57e66285 says the rate depends on distance
from the equilibrium and gives r(a-P), r>0, P<a. Its graph shows approach from
below to a horizontal equilibrium; it supplies no additional question data and
requires no generated plot. Canonical example a568fc63-e81c-5210-93f0-bcbd429a9e40
substitutes fish capacity 200. Deer question
54bac72f-651e-55b5-8b4b-fbc4e753ebc5 and factory question
19a4e47b-fcd5-50aa-804a-b275eeea23d5 contrast positive gap, reversed gap,
population factor, squared population factor, and negative sum at a shared capacity.
Tutoring question 5651275c-fd64-5799-85e0-52ab15ebd288 distinguishes initial 10
from capacity 95 among capacities 95,30,60,100,950. Computer question
3974627f-3801-52ea-b93f-3d1a3033e2cc distinguishes initial 320 from capacity
1000. Vehicle question 4108ce6a-5d28-540e-b8c0-e4b52161a458 also contrasts
capacities. All 14 captured practice banks remain replayable with original fields,
choices, solutions, keys and difficulty labels, including captured absences.

Normal easy samples source contexts and an authored direct-model context catalog.
Capacity-only banks use five distinct positive linear gaps; any candidate capacity
can be stated as the equilibrium. This preserves the source's legitimate capacity
selection exercise. New constants use instructional integer bounds rather than
requiring historical distractor ratios. Initial stocks remain positive and below
equilibrium and need not equal a distractor capacity.

Mixed banks are a conservative combination of the two observed bank types. Choose
the bank kind and eligible target rank before values/context. Draw two distinct
candidate capacities. For each c, include k(c-X) and k(X-c). The latter is exactly
the observed reversed-gap error -k(c-X), with equivalent presentation preventing a
leading-minus length cue. A fifth equation uses one independently chosen candidate
with the observed population factor, squared factor, or negative-sum error. Choose
its operation and candidate role independently of the target before drawing values.
Every equation is distinct; constants are intentionally shared. Both positive-gap
candidates can become correct with the complete bank held fixed. Thus numeral
matching leaves at least two choices, and choosing the shortest among them still
leaves both signs. Frequency of a constant and the fifth equation's capacity cannot
identify the target. Two candidate/sign pairs leave room for another observed wrong
operation within the five-choice contract. This is an authored extension, not an
assertion that these exact mixed banks appeared in the sources.

Fixed features have instructional reasons: positive k and stock below equilibrium
express growth; a whole derivative equation preserves the modeling response; one
correct choice and five options preserve the radio workload. Numeric values,
eligible equilibrium assignments, context, variable, units, initial stock and option
position can vary without changing the solution stages. Automatic sampling uses
same-digit-width constants to remove length cues. Explicit banks may cross digit
widths; mixed candidates still have equal-length reversed twins. Normal numerical
bounds are unchanged (direct capacity20..500; source-context10..5000), with two mixed
candidates or five capacity-only candidates. target_rank indexes the sorted candidate
list; all ranks are eligible. Positive initial-stock variation is irrelevant to the
ODE and must preserve its answer. No new learner operations are introduced.

The latest defect was reproduced before implementation: seed3/deer/capacity60 let
numeral copying identify the sole correct option. Earlier shortest-option and
capacity60/initial10 regressions passed at that milestone. The second-repair design
was written before runtime changes; the pre-implementation
specification is retained in evidence/instructional-account-design-history.md.
Current regressions parse the visible equations independently, exercise both mixed
targets in every structural context, all five capacity targets, all three extra
operations and both extra-capacity assignments. Controlled pairs hold the entire
bank fixed while equilibrium, key and solution change together. Changed initial
stock preserves the bank and response. Check numeral copying, lengths and their
composition, frequency cues, option positions and capacity ranks before/after the
shared delivery filter. Semantic instances are numerical equilibrium models, not
seeds, UUIDs, context aliases or shuffles. Actual native grading tests every option
in representative banks, including controlled pairs.

Source limitations: the canonical fish answer bank is absent; rehabilitation
bdadb029-2e6a-54b7-8c42-d0b37b92a134 lacks key, solution and difficulty. Replay
preserves those gaps; normal learning derives its unique model. Factory source
mixes stock units and units/day; served prompt and solution consistently use units,
while replay retains the original. Prerequisite snapshot is empty; the neighboring
identification example supports the positive linear-gap rule. Live learner history
and post-capture inventory are unavailable offline. No engine limitation was found
in the radio response contract.
