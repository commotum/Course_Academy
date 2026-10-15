# Linear template extraction

Source q-122699 supplies f(x,y)=2y-x, at three anchors (-2,2), (2,2), (2,-2). Its only field is radio key selection, with five image answers; the second image is correct. The complete original question, solution, field identities and image paths are retained in reference/initial/source.json. reference/source-bank-mapping.json accounts for every source choice and exact vector value.

The reusable backbone asks which of five three-arrow diagrams represents the gradient of a linear potential ax+by. Its concrete solution finds both partial derivatives, forms a i+b j, substitutes all three anchors, and displays the correct diagram. It always has one five-choice image radio field. Fixed anchors keep the observed bank's three locations and reasoning workload; this version makes no claim of target-position variation. Function coefficients are the two declared slots. No additive constants are sampled because they leave the assessed gradient unchanged.

Observed a=-1,b=2. Conservative generalization: nonzero integer a,b in {-3,-2,-1,1,2,3}, with a!=b. These signs and values preserve differentiation and three vector substitutions. The exclusion a=b is necessary: the first and fourth observed recipes then collide. This yields 30 distinct gradient tasks, one of which is the source. After source and current mathematical-content exclusions at most 29 new tasks remain. Difficulty stays easy; changing a difficulty label does not create a moderate or hard task.

Profile q-122699-observed contains the following entire bank in its captured order. At each anchor (x,y), draw displacement:

1. (a*x,a), originally (2,-1),(-2,-1),(-2,-1).
2. (a,b), originally (-1,2) at all anchors; correct.
3. (a,0), originally (-1,0) at all anchors.
4. (a*x,b), originally (2,2),(-2,2),(-2,2).
5. (0,b), originally (0,2) at all anchors.

These are exact observed vector patterns. The first and fourth retain an undifferentiated x term; no stronger learner-error attribution is claimed. Bank construction selects the entire profile before rendering. No permutations, seed-only identities, or alternate distractor banks create distinct tasks. Identity is derived from both gradient coefficients and the frozen version; mathematical deduplication disregards identities and image bytes.

Original and generated solution stage order matches. Generated LaTeX is normalized and explicit parentheses surround signed coefficients; this is not literal source text or pixel replay. Full mathematical bank fidelity is 4/4 distractors and 1/1 complete supported bank. No fidelity claim is made for the excluded nonlinear families.
