# Template extraction

## Stage 1 — specific observed questions

| Source | Observed level | H, v, q, c, inflow, outflow | Time | Amount | Layout |
|---|---|---|---|---|---|
| q-336451 | easy | 300, 180, 54, 0.8, 6, 4 | 60 min | 207.6 lb | 2 radio field(s); solution present |
| q-336499 | unrated | 210, 120, 30, 0.5, 9, 6 | 30 min | 95.2 lb | 1 radio field(s); solution absent |
| q-336506 | easy | 210, 70, 20, 0.5, 21, 14 | 20 min | 103.3 lb | 1 radio field(s); solution present |
| q-336513 | easy | 150, 75, 25, 2/3, 9, 6 | 25 min | 93.8 lb | 1 radio field(s); solution present |
| q-336516 | easy | 200, 50, 10, 0.8, 15, 10 | 30 min | 158.1 lb | 1 radio field(s); solution present |
| q-336501 | easy | 180, 100, 20, 0.6, 15, 10 | 16 min | 95.7 lb | 1 radio field(s); solution present |
| q-336502 | easy | 160, 100, 25, 1.0, 6, 4 | 30 min | 130.7 lb | 1 radio field(s); solution present |

q-336451 lacks a rounding instruction and has a shorter initial-condition and factored-capacity sequence; its final endpoint ratio is 9/15, not fully reduced. q-336499 uses bare gal/lb notation, calculator note, no difficulty, no solution and no correct designation. The other five source solutions retain a subtraction-isolation row for C, the expanded capacity equation, and endpoint component evaluation before rounding. q-336513 supplies concentration 2/3; q-336502 preserves the lexical concentration 1.0. Those complete components are explicit slots, not blind numeric replacements.

## Stage 2 — shared pattern

Let V(t)=v+(rin−rout)t, with d=rin−rout>0, a=v/d, n=rout/d. Construct Q′=c·rin−rout·Q/V(t); then Q′+nQ/(a+t)=c·rin. The integrating factor is (a+t)^n, and integrating the product gives Q(t)=c·d(a+t)+C/(a+t)^n. Initial condition Q(0)=q gives C=(q−c·v)a^n. Capacity V(to)=H gives to=(H−v)/d. Evaluate only Q(to)=cH+(q−cv)(v/H)^n and round as requested. The requested response is the amount in pounds, not concentration, time, or a post-overflow expression.

## Stage 3 — complete source components and banks

`masks.json` contains each full prompt and full worked solution, with per-occurrence typed component slots. `extract.py` documents the audited positional roles in every display/prose block. Slot `np` is n+1, k=c·d, D=cv−q, cv=cv, cH=cH, gap=H−v, end=a+to. Source q-336451 endpoint fraction retains division of both offset/end by 10 (90/150 → 9/15), deliberately not gcd reduction. Literal step numbers, zero initial time, and the primitive numerator 1 remain fixed.

Historical numerical banks underdetermine their error intent. Each historical option below is preserved as an explicit opaque replay expression `round(Q(to),1)+offset`, with its original formatting suffix and supplied-key presence. This is a lexical evidence parameterization, **not** a claim that these offsets are method errors or appropriate new practice distractors. All observed and repaired opaque profiles are evidence-only. Normal learner sampling uses the operation bank in Stage 4.

| Source | Field | Numeric option | Offset from rounded amount | Supplied correct |
|---|---|---|---|---|
| q-336451 | 1 | 205.4 | -2.2 | designation absent |
| q-336451 | 1 | 206.2 | -1.4 | designation absent |
| q-336451 | 1 | 204.3 | -3.3 | designation absent |
| q-336451 | 1 | 201.0 | -6.6 | designation absent |
| q-336451 | 1 | 207.6 | 0 | designation absent |
| q-336451 | 2 | 201.0 | -6.6 | no |
| q-336451 | 2 | 204.3 | -3.3 | no |
| q-336451 | 2 | 207.6 | 0 | yes |
| q-336451 | 2 | 206.2 | -1.4 | no |
| q-336451 | 2 | 205.4 | -2.2 | no |
| q-336499 | 1 | 95.2 | 0 | designation absent |
| q-336499 | 1 | 94.7 | -0.5 | designation absent |
| q-336499 | 1 | 95.0 | -0.2 | designation absent |
| q-336499 | 1 | 93.5 | -1.7 | designation absent |
| q-336499 | 1 | 94.2 | -1 | designation absent |
| q-336506 | 1 | 102.5 | -0.8 | no |
| q-336506 | 1 | 103.3 | 0 | yes |
| q-336506 | 1 | 103.7 | 0.4 | no |
| q-336506 | 1 | 102.9 | -0.4 | no |
| q-336506 | 1 | 103.9 | 0.6 | no |
| q-336513 | 1 | 93.3 | -0.5 | no |
| q-336513 | 1 | 92.9 | -0.9 | no |
| q-336513 | 1 | 93.8 | 0 | yes |
| q-336513 | 1 | 94.5 | 0.7 | no |
| q-336513 | 1 | 94.1 | 0.3 | no |
| q-336516 | 1 | 158.5 | 0.4 | no |
| q-336516 | 1 | 157.2 | -0.9 | no |
| q-336516 | 1 | 158.1 | 0 | yes |
| q-336516 | 1 | 157.6 | -0.5 | no |
| q-336516 | 1 | 159.0 | 0.9 | no |
| q-336501 | 1 | 95.2 | -0.5 | no |
| q-336501 | 1 | 96.1 | 0.4 | no |
| q-336501 | 1 | 95.7 | 0 | yes |
| q-336501 | 1 | 96.4 | 0.7 | no |
| q-336501 | 1 | 94.9 | -0.8 | no |
| q-336502 | 1 | 130.7 | 0 | yes |
| q-336502 | 1 | 130.2 | -0.5 | no |
| q-336502 | 1 | 129.9 | -0.8 | no |
| q-336502 | 1 | 131.4 | 0.7 | no |
| q-336502 | 1 | 131.0 | 0.3 | no |

The captured source suffixes are reproduced byte for byte in raw profiles. `decoded-byte-evidence.json` is empty because no decoded source choice has adjacent backslash characters. Source and normal answers use valid single-backslash LaTeX commands; JSON display escaping is not a source anomaly.

Authoritative MA widget capture at `/home/jake/Developer/MA/DATA/Lessons/6700/Source/6700.json` was inspected; a private copy is widget-context.json. q-336451 has a single actual learner radio widget, confirming the legacy first field is an artifact rather than a second assessment demand. The EDB raw capture is retained unchanged. q-336451 prose calls salt minerals and declares kg/min while its actual prompt and cancellation rows use lb/min; the smallest normal repair changes minerals to salt and kg to lb. q-336499 missing key is inferred independently as 95.2 lb; its normal full solution is authored from the common source solution, with nutrient/tank prose. Its raw replay still omits all missing attributes.

## Stage 4 — reusable masks, domains and authored extensions

All seven prompt masks and six present solutions are instantiated through complete component slots. Shared source teaching prose and stage sequence remain fixed, including optional rows and omissions. When n≠2, the distributed product row explicitly displays (a+t)^(n−1), since the original implicit first power applies only to n=2. For changed q-336451 parameters with a nonexact one-decimal endpoint, the final equality becomes an approximation; the original exact endpoint equality is retained at source parameters. For q-336499 normal output completes the absent solution using the shared source mask and explicitly authored difficulty; no raw record invents observed fields or labels. The normal q-336451 adds the uniform rounding instruction and repairs its demonstrated unit/substance prose errors.

Parameters obey 0<v<H≤800, 0<q<cv, 0<c≤2, 0<rout<rin≤60. Authored d is 2–10, a is 5–100, and H/v≤4. Easy requires n=2 and integral a/to; moderate requires n=3 or4 and integral a/to; hard requires n=1/2 or3/2 and nonintegral a/to. Easy/moderate additionally require integral initial amount and cv, and k at most one decimal, preserving observed arithmetic. These checks apply to explicit calls as well as sampling. Incoming concentrations draw the observed/familiar forms 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5 and2/3; normal initial amounts are familiar fractions of cv. All remain positive and below incoming concentration; no incompatible stronger-brine prose is admitted.

The normal complete bank is selected before sampling and contains exactly: (1) correct cH−D(v/H)^n; (2) omit the transient term, cH; (3) use n+1 instead of n; (4) use n−1 instead of n; (5) omit initial q, giving cH−cv(v/H)^n. Each applies to the actual ODE/initial-condition/endpoint method. Every value is rounded to one decimal with the same pounds suffix. Reject the whole instance on rounded collisions or nonpositive choices; never replace a recipe from a pool. Correct positions are deterministically shuffled, and all five positions were exercised.

Meaningful parameters enter mathematical fingerprints; context, displayed-bank aliases, option order and seed do not inflate task counts. Content identity hashes complete rendered prompt, fixed solution, unordered bank, difficulty and version. Independently read displayed quantities, volume, inflow/outflow, IF, primitive, general solution, solved C, onset time, endpoint components and rounding before native grading. Every raw source bank and all source-key omissions are publicly replayable.
