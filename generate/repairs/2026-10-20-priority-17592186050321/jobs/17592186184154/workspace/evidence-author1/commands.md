All commands run from the supplied workspace. Full reproducible sequence:

```sh
bash reproduce.sh /home/jake/Developer/Course_Academy \
  /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-priority-17592186050321/jobs/17592186184154/source/source.json \
  /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-priority-17592186050321/jobs/17592186184154/source/inventory.json \
  > evidence/reproduction.log 2>&1
```

`reproduce.sh` contains the exact source replay, mathematical checks, normal and
controlled delivery-filter checks, before/after shortcut probes, batched native
grader checks, package relocation, five-record CLI sample and actual UI-renderer
commands. It performs no publication or database operations. `verify_package.py`
copies only manifest-declared files into a temporary directory under this
workspace and runs from a different working directory.

Validation scope: all five moderate source banks; 91 controlled records plus 160
normal records (232 distinct mathematical integrands before delivery); 68
counterfactual/response-preservation checks. Normal sampling accepts 160 of 174
attempts, rejecting 14 repeated prompts. Combined delivery accepts 245/257,
removing 12 inventory/batch duplicates; separately filtered normal sampling
accepts 160/160. Native grading passes 327 accepted and 1037 rejected checks
before delivery, then 307 accepted and 918 rejected checks on accepted records;
zero unresolved outcomes. Five UI screenshots passed DOM checks and were
visually inspected. Relocated output exactly matches the original five records.

The native grader tests every radio choice, canonical and independently formed
equivalent blanks, wrong reciprocal signs, zero answers and unwanted extra C.
Changed-key checks additionally submit the formerly correct radio choice.
The specific source median-coefficient strategy succeeds on 14/30 normal
sqrt-product records, instead of being fixed as in source-only replay; it never
succeeds on the 22 reciprocal-product records. Every permitted radio role and
all five correct positions occur before and after delivery. Other tested cues
(position, length and static exponent preferences) have no perfect predictor.
These are tested claims, not exhaustive certification against every strategy.
