# Current inventory classification

Current read: math basis 2669, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
The eight source questions in source.json retain their full prompt, solution,
answer bank and identities (UUID decoding differs between JSON and native EDN).
Four later captured practice sources add the following distinct backbones. All
are selection/radio fields with five scalar mathematical options, no plots,
and the same six ordered chain-rule solution stages. None is a canonical example.

| Source | Band | Supplied gradient and path | Point | Complete bank (correct marked *) |
|---|---|---|---|---|
| q-65864 | easy | (2x/(x²+y²),2y/(x²+y²)); (sin t,cos t) | pi/4 | 1; 0*; 2; 2sqrt(2); sqrt(2) |
| q-94871 | moderate | (y exp(xy),x exp(xy)+2y); (t+1,t-1) | -1 | exp(-1)+3; -6*; 4e+7; 2; 3-2exp(-1) |
| q-94874 | easy | (ln(x+y)+x/(x+y),x/(x+y)); (2t,1-2t) | sqrt(2) | 3sqrt(2); sqrt(2)-1; ln(2)/2-1; 0*; ln(sqrt(2)+1) |
| q-94880 | easy | (atan y,x/(1+y²)); (t²+1,t) | 1 | 0; pi²+1; 1; (pi+2)/2*; pi/2 |

The first and third new backbones have derivatives identically zero along their
paths. The second composes a product exponential along an affine path; the
fourth composes arctan with a polynomial path. Each has its own observed scalar
bank profile, whose distractor intent remains underdetermined. Original banks
and every printed solution stage are checked directly by the package's independent
TeX reader and native learner grader before inclusion in available inventory.
Complete captured records remain in reference/replenishment/initial-read/kp.edn.

Bounded generator scope: the four newly observed templates are audited source
instances, without claimed parameterized generation or inferred error recipes.
The existing version v1 retains its eight replay families and ten authored
sampling families. Filling a band uses validated families in that band, not a
claim that every observed template is parameterized. Existing validation records
8/8 complete original replay banks and 40/40 options. No generated question is
made by changing source IDs, choice order, seed alone, or copying opaque banks.

q-94878 retains its erroneous i/i velocity dot-product row. It is preserved in
storage and excluded from the validated available pool. No source question or
learner history is edited. Authored hard support remains grounded in the saved
canonical example and prerequisite/route evidence, not absence of hard sources.
