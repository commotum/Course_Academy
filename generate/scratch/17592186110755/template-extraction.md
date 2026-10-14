# Templates and complete source banks

The concrete original prompts, solution sentences, field layout, and all original
choice entities are retained in `source.json`. `source-bank-replay.json` maps every
supported original choice to one complete recipe and reports full-value replay.
The parameterized renderer changes simultaneous exact arithmetic slots in those
captured prompt/solution templates; this preserves their wording and sequence.

Easy slots: reduced ratio m/n, 0<m<n, first quadrant, D=n²-m², C=sqrt(D)/n.
Observed (m,n): q-124625=(6,7), q-37899=(3,7), q-64681=(1,2), q-65059=(5,9).
Normal sampling bounds 2<=n<=12 with integer coprime m,n. Profiles may reject a
pair if their complete five choices collide. The x-coordinate, sine target,
point P, quadrant, and five-choice radio contract remain fixed because they are
roles in this observed easy backbone. Changing to another quadrant or a tangent
query would change branch reasoning or operations and is outside this package.

Ordered solution stages: relate x=cos theta, y=sin theta; equate the supplied x
with cosine; isolate sin²=1-cos²; take ±sqrt; substitute m/n; square the supplied
fraction; subtract to D/n²; simplify the radical; choose positive in quadrant I.
All numeric fractions and the final equation change together. The blank-free
radio prompt and field key selection are preserved.

| Complete profile | Recipes, including correct answer | Evidence / restriction |
|---|---|---|
| q-124625 | -sqrt(D-10)/n; sqrt(D-8)/n; -sqrt(D-3)/n; 1/n; C | D>10. Signed radicands are observed offset patterns; their misconception interpretation is unresolved. Constants 10,8,3 are retained as explicit empirical offsets, not claimed as known cognitive errors. |
| q-37899 | (m+1)/n; C; C/2; C/sqrt(8); m/n | Preserve all five together. The two scaled-root and altered-numerator patterns replay 4/7, 2sqrt(10)/7, sqrt(10)/7, sqrt(5)/7, 3/7. |
| q-64681 | -m/n; -C; C; C²; m/n | Signed branch, supplied ratio and squared-complement bank; exactly replays both ±1/2, both ±sqrt(3)/2, 3/4. |
| q-65059 | (D-1)/n; (m-1)/n; D/n²; C; D/n | Includes altered radicand/denominator and numerator patterns; exactly replays 55/9, 4/9, 56/81, 2sqrt(14)/9, 56/9. Interpretation of altered constants is unresolved. |

These are explicit conservative same-method generalizations from single-bank
observations; they are not evidence about Math Academy's original samplers.
No option-specific feedback or distractor explanations are added to presentation.
Never merge recipes across banks or generate several banks for the same task
merely to count additional inventory.

Moderate slots: squarefree integer a, integer b, supplied y=sqrt(a)/b with
1<a<b²; observed (a,b)=(10,4), normal 3<=b<=9, with squarefree a preserving the source's single unsimplified radical numerator. The requested quantity remains
2cos² theta. Let S=a/b² and T=2(1-S). Complete q-37915 bank:
T/2, T, 1/T, T/S, 2T. This exactly replays 3/8, 3/4, 4/3, 6/5, 3/2.
Solution stages: relate coordinates to ratios; identify sine; isolate cos²;
multiply by fixed 2; substitute sqrt(a)/b; square to a/b²; multiply to 2a/b²;
subtract and simplify T. Reject any complete-bank collision.

The scale 2 stays fixed as part of the source's requested expression and solution
stages. Changing a,b keeps the same number of steps and response contract.
All points and both diagram labels derive from the same given value.

The two incomplete banks remain evidence-only: q-37821 has ±3/4, ±sqrt(7)/4,
sqrt(3)/4 and given x=sqrt(7)/4; q-64731 has 1/4,1/3,1/2,sqrt(3)/2,sqrt(2)/2
and given y=sqrt(3)/2. Their images show quadrant I, suggesting answers 3/4 and
1/2, but no complete worked-solution/rating evidence supports enrollment into
either band. They are excluded, not silently completed. No source facts are edited.

Distinctness uses the displayed coordinate value, its role, target expression,
and quadrant; it ignores seed, identity, bank, wording, and option order.
Stable question identity includes the frozen version and complete authored bank;
fields and answers use field-owned UUIDs. Identity collision checks occur before
commit. All choices are delimiter-free exact mathematical expressions.
