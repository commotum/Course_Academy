# Source templates and complete banks

All variables are real. A straight line with two distinct points is tested by substituting both points into each candidate equation. Mathematical equivalence compares complete linear equations, allowing multiplication by a nonzero constant.

## Hard: q-71837, all three equations correct

Observed graph: slope -3, y-intercept 6, x-intercept 2. Prompt precedes three Roman-labelled equations, followed by one radio field `selection`. Equations: I `y+3x=6`; II `(1/3)y+x=2`; III `y=-3x+6`. Each equation describes the same line. Solution chooses A=(0,6), B=(2,0), shows the annotated graph, explains the two-point test, substitutes both points into I, II and III in that order, and concludes all three.

Template parameters: positive integers k and t, b=kt, graph y=-kx+b. I `y+kx=b`; II `(1/k)y+x=t`; III `y=-kx+b`. Correct values and intermediate calculations are derived before rendering. For I both point residuals are zero. For II b/k=t, 0+t=t. For III -kt+b=0. Fixed wording, Markdown math displays, alignment sequence, field key and choice count replay exactly at k=3,t=2.

The complete observed profile is five text values: `II and III only`, `I only`, `I, II and III`, `I and III only`, `III only`. Correct: `I, II and III`. Each incorrect value is the exact finite subset of equation labels named by its text; these are fixed labels, not numerical distractor transformations. All four distractors are mapped and replayed. No options are added, deleted, or borrowed from the other profile.

Validated sampling is an explicit bounded extension: k in {2,3,4,5}, t in {1,2,3,4}. Observed k=3,t=2 is included. Every line has positive integral intercepts and negative integer slope. Sixteen profile instances.

## Hard: q-54293, only equation II correct

Observed graph: slope -1/2, y-intercept 2, x-intercept 4. Equations: I `y=-2x+1/2`; II `y=-(1/2)x+2`; III `y=(1/2)x+2`. Solution uses A=(0,2), B=(4,0). I fails at A; II passes at both points; III passes at A and fails at B. Preserve this different worked sequence, field layout and final answer.

Template parameters: positive integers b,t, c=b/t. Graph y=-cx+b. I `y=-bx+c` (the observed slope magnitude/intercept swap); II `y=-cx+b` (correct); III `y=cx+b` (slope sign reversed). These recipes reproduce the entire original equations. The labels describe observed algebraic patterns; learner-error motives are inferred and are not shown as feedback. At A, Equation I requires b=c and fails because t>1. At B, Equation III requires 0=2b and fails because b>0. Exact residuals validate every displayed substitution and simplification. The source coefficient typo -1 is corrected to -2 only in generated instances.

Complete profile: `II only`, `II and III only`, `I only`, `I and II only`, `III only`. Correct: `II only`. Every original text value is mapped to its subset and replayed, ignoring option order. No mixed banks. Complete mathematical equations, rather than independently compared sides, establish the true subset.

Validated bounded extension: b in {1,2,3,4}, t in {2,3,4,6,8}; includes b=2,t=4. Twenty profile instances. Positive integer intercepts and negative exact rational slopes include integer/fractional cases. All domains enforce t>1 and b>0.

## Unrated exclusions

q-54285 uses a graph y=x/2+2 and equations I `y=x+1/2`, II `y=x/2+2`, III `y=x/2+1/2`. Boolean keys are false,true,false; each field bank is exactly {false,true}. A possible pattern is to double the slope and replace the intercept by the slope in I, preserve both in II, and replace the intercept by the slope in III. Sparse evidence does not establish a rated sampling contract, so this profile is excluded from generation.

q-59732 uses y=4-x and equations I `x+2y=4`, II `y=2-x`, III `y=4-x`. Boolean keys are false,false,true; each field bank is exactly {false,true}. Observed transformations are coefficient 2 on y in I and half the intercept in II. A rated generalized contract is not claimed. Both source checkbox questions remain unchanged and unrated.

## Identities and distinctness

Generator identity is UUIDv5 of the existing KP UUID and `question-generator`. Question identities bind version, profile, exact line, rendered equations and complete bank; field and answer UUIDs belong to the question and field. Seeds affect selection only. Pool deduplication is stricter: the exact pair (slope,y-intercept) is the task key across profiles. The 36 validated profile instances contain 35 distinct lines; the shared line is counted once. Source and canonical graph lines are excluded from new inventory. No source content IDs are assigned to generated records.
