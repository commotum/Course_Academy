Commands run from the supplied workspace, using the supplied Python 3.13.5 and
SymPy 1.14.0. Full current reproducible sequence:

```sh
bash reproduce.sh /home/jake/Developer/Course_Academy \
  /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-priority-17592186050321/jobs/17592186184154/source/source.json \
  /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-priority-17592186050321/jobs/17592186184154/source/inventory.json
```

This session's initial invocation, in evidence/reproduction.log, passed source
replay, independent math, both shared delivery filters and general probes, then
stopped on an overstrict internal-label assertion in the new conditional probe.
Two source polynomial components coincide mathematically; delivery can merge
their exchanged assignments. The corrected assertion requires all four distinct
polynomial components, rather than both equivalent internal labels. Every cue
probe remains unchanged. The focused continuation was:

```sh
bash evidence/resume-validation.sh /home/jake/Developer/Course_Academy \
  > evidence/resume-validation.log 2>&1
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py \
  --limit 7 --input evidence/render-records.json --output evidence/render \
  --asset-root evidence --math-root /media/jake/SSD/EDB/math \
  > evidence/render-final.log 2>&1
```

The continuation passed conditional before/after/selection probes, all three
batched native-grader inputs, relocation and the five-question CLI sample.
The final seven screenshots were visually inspected (visual-inspection.md).
The current reproduce.sh and continuation script both explicitly request seven
render cases. Previous author evidence is retained in ../evidence-author1/.

Source fidelity: five complete banks, 10 radio choices and 3 blank answers;
three blanks retain the documented self-contained f(x) context repair.
Mathematics: 461 controlled/regression records, 260 distinct integrands.
Decision variation: 14 internal reciprocal assignments represent 7 distinct
unordered banks at fixed a,b,p; 152 counterfactual/preservation cases, including
84 same-bank/same-denominator changed-polynomial cases. Do not count exchanged
identical components or bank shuffles as semantic instances.
Delivery: 350/467 combined and 160/160 normal records accepted. The review's
largest-visible-exponent shortcut succeeds on 18/64 raw denominator-4 cases,
15/43 delivered combined cases, 0/10 delivered normal cases, and 20/57 conditional
same-band selection draws. Every tested static cue fails at least once in every
combined denominator/p subgroup before and after delivery. The sampler's
p=4,denominator=4 subgroup contains one record; its incidental perfect sample
scores are not evidence of a structural predictor. The complete structural
cases separately cover that subgroup. No extra random sweep was needed.
Grading: 620 accepted / 2298 rejected before filtering; 411 / 1339 afterward;
53 / 131 for the review shortcut predictions. Zero unresolved outcomes.
Selection reproduction uses sorted question UUIDs as surrogate database ID
order, all candidates fresh/moderate, and a positive moderate band weight.
Real database ordering, history, policy, and future inventory remain unverified.
