# Classification

Capture: math database, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; `source.json` is the unchanged wrapper. KP 17592186087822 / 79daf9dd-814d-562b-b3bc-b066bd2dfb90, topic 17592186049660 (MA817). All eight captured practice questions are accounted for. The canonical example e-1220 is context, never counted as practice.

| Observed label | Practice sources | Field shape | Markdown/value templates | Complete banks | Plot rating |
|---|---|---|---:|---:|---|
| Easy | q-26804, q-99774, q-99775, q-7230, q-7232 | one radio; five complete equations | 2 (shared normal solution; mismatched-base opener q-99775) | 5 | heavy |
| Moderate | q-170593 | one radio; five complete equations | 1, fractional base and shift | 1 | heavy |
| Unrated | q-26807, q-7228 | one radio; five equations, correct ref absent | 1, spaced equations and missing solution | 2 | heavy |
| Hard | no observed question | authored one-radio extension | 1 | 1 retained coherent source bank and 3 authored banks | heavy |

Every original prompt supplies the base in `y=b^x+c`; every source plot directly **labels** the dashed asymptote. The required response is the complete equation, despite prose also asking for c. All sources use `selection`; neither blanks nor multi-field demands are invented. The two unrated sources get an explicitly authored easy assignment only in metadata; public raw replay omits original absent difficulty, worked solution and correct designation.

Easy varies integer asymptote levels -12..12 except zero (observed -5,-3,-2,+10), integer bases 2..25 (observed 2,3,7,12,17,25). Moderate preserves the observed fractional read, extending denominators through 6 and noninteger shifts of magnitude at most 12. Base is supplied and incidental to the assessed read; no logarithm or exponential calculation is required.

Hard is a design claim: the SAME c-only identification uses a calibrated fractional vertical axis, with alternate ticks named and the asymptote's tick unnamed. Noninteger signed c is within eight increments of zero; increments 1/2,1/3,1/4. All hard instances do one coordinate read and apply the same y=c asymptote rule. Sign, denominator and curve-base variants are unordered peers, not a progression. No unknown stretch k, curve selection, horizontal translation, or neighboring KP task is assessed.

The canonical example identifies c=2 using the horizontal asymptote. The route is reconstructed from `activity/first-step` and `step/next`: introduction → KP87821 → this KP87822 → stretch introduction → KP87823 → KP87824. The preceding introduction explicitly establishes the movement of y=0 to y=c, and (0,1) to (0,c+1). Owning original MA817 capture lists **Graphing Exponential Growth Functions (1530)** as the topic prerequisite and no extra key prerequisite for this step. Reading calibrated coordinates is used solely to obtain the same asymptote level; the stretch material occurs AFTER this KP and is excluded. Missing hard is not represented as recovered MA difficulty.

Source findings: q-99775's first sentence refers to y=2^x while its prompt and translation refer to y=12^x. This true but mismatched illustrative statement is preserved in evidence; normal solutions consistently use the printed base. Two missing original designations are independently inferred from labels (-4,+1), never counted as matched designations or given fabricated raw correct refs. q-170593 fractions have SINGLE actual slash bytes: explicit adjacent-character ord checks establish no escaping anomaly and no TeX normalization is claimed.
