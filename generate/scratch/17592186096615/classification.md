# Classification at frozen math basis1356

Database `math`; lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Capture is `source.json`. The earlier basis1905 draft is preserved under `previous-basis1905/` and is not evidence for this cohort.

All12 practice questions are accounted for:9 easy,1 hard,2 unrated. The canonical example e3629 is separate. There are12 observed prompt/answer/solution backbones, since the layouts and operative sequences differ. Five observed radio banks have five choices each; six blank banks have one exact fragment each; one question is fieldless. Plots: none throughout.

| Source | Observed level | Template | Field | Distinct operative stages |
|---|---|---|---|---|
| q11903 | absent | linear-log-radio | radio; correct ref absent | solution absent; x minus scaled log |
| q11907 | absent | quadratic-log-radio | radio; correct ref absent | solution absent; x² minus scaled log |
| q101719 | easy | constant-log-slope | absent | differentiate constant/scaled log; substitute reciprocal ln base; cancel |
| q11900 | easy | scaled-log | radio | extract coefficient; insert reciprocal rule; combine |
| q105256 | easy | exp-explicit-radio | radio | exponential and explicit-base log rules; equivalent product row |
| q1921 | easy | exp-common-radio | radio | exponential and common-log rules; equivalent product row |
| q339989 | easy | quadratic-slope | blank | differentiate quadratic/log; substitute1; collect |
| q339997 | easy | log-minus-ln | blank | separate derivative operators; insert both log rules; combine coefficient |
| q339994 | easy | cubic-slope | blank | power rule and log rule; substitute3; evaluate and collect |
| q340105 | easy | exp-common-blank | blank | separate derivative operators; exponential/common-log rules |
| q340106 | easy | negative-exp-log | blank | separate operators; insert exponential/log rules; combine |
| q308866 | hard | log-ln-exp-slope | blank | three derivative rules; substitute1 into each; collect exact rate |

The two unrated questions receive explicitly authored easy levels only in normal output, supported by the neighboring scaled-log and sum-rule examples. Raw replay retains absent difficulty, absent solutions and absent correct refs. q101719 retains an absent field in raw replay; its normal blank field/key is an authored completion.

The original1116 lesson JSON confirms all five displayed choices on q11903 and q11907; it supplies neither a key nor a solution. Their normal keys are inferred independently from differentiation. Source values are mathematically valid and unambiguous. No mathematical repairs are needed.

Three banks contain an opaque historical member: q11907 contains3/(x ln5), unrelated to its prompt; q105256/q1921 replace the exponential base with4 without an explained operation. Those full profiles are evidence-only. Normal default sampling covers every supported easy family and uses explicitly authored, method-derived replacement banks for these three families.
