# Converting a radical to a unit fraction exponent

The account below describes the earlier source recovery and square-root repair.
The 2026-10-18 indexed-root repair supersedes its statements about unchanged
indexed practice. See `../README.md` and `indexed_repair_checks.py` for the current
indexed-grid specification and combined checks. Earlier evidence is retained as
history; it is not approval of version 1.3.0.

This account was written before implementation and revised after the feedback repair. The current specification below supersedes the first pass's claim that decimal radicands alone removed the square-root shortcut.

## Instructional evidence and operation

Tutorial 3293 (ace9adb3-54cf-5410-b2e4-d0e8ae4fb000), Introduction, states: “Given a radical $\sqrt[n]{x},$ we can write an equivalent expression using the fractional exponent $x^{1/n}.$” Its final note identifies square roots with n=2. Canonical e-4959 (87e686a5-7b8a-529b-a8fa-17445c52e012) identifies x=4, n=5 and concludes 4^(1/5). Adjacent e-4958 assesses the reverse direction; e-4903 additionally uses exponent laws for nonunit numerators. Those operations are outside this generator. No prerequisite records or images were supplied; the tutorial supplies the root definition.

The learner must inspect the radicand, distinguish it from the index, infer 2 when the index is omitted, and select the same base with exponent 1/index. The solution states the identity, identifies x and n, substitutes, and concludes. It never requires evaluating roots, manipulating decimal values, applying exponent laws, or analyzing signs/branches. The response contract is one radio field, key `selection`, five mathematical choices and exactly one correct response. Plot classification: none.

## Observed templates and banks

All original complete fields and canonical text are preserved in source_cases.json, checked against immutable source.json.

| Source | Prompt/available evidence | Complete bank |
| --- | --- | --- |
| q-69158 / a6a09e66-f069-5046-85e4-002d5b3571d6 | What is the seventh root of 2? Key, solution and difficulty absent. | 2^(1/7), 1^(2/7), 2^(7/1), 7^(2/1), 7^(1/2) |
| q-69218 / fe9954e2-d8b5-5670-b2ae-c502beed2e2e | cube root of 5 followed by equals; easy; key 5^(1/3). Solution identifies x=5,n=3. | 1^(5/3), 5^(3/1), 3^(5/1), 3^(1/5), 5^(1/3) |
| q-69219 / 5ecc3edc-ec35-5d73-a402-e0e102dfec06 | square root of 10 followed by equals; easy; key 10^(1/2). Solution explicitly identifies index 2. | 2^(10/1), 2^(1/10), 10^(2/1), 10^(1/2), 5 |

There are three presentation/solution templates: indexed What-is, indexed equation and implicit-square equation. The two indexed presentations share the observed **unit-base** profile: x^(1/n) (key), n^(1/x), x^(n/1), n^(x/1), 1^(x/n). The last recipe's psychological interpretation is unresolved; its complete mathematical form is preserved. The observed **square-division** profile replaces only the last recipe by x/n. No observed recipe is pooled or silently dropped in source replay. Replay checks complete banks, prompts and both available normalized solutions. For q-69158, infer the key from the tutorial and supply the same instructional stages; do not claim replay of absent fields. The canonical example has no captured answer bank.

## Supported domain and constraints

Easy is the sole supported/default difficulty; moderate and hard lack source justification. Original labels, including their absence, remain in captured evidence/provenance. Normal practice uses positive integer radicands 2..15 and explicit indices 3..10, plus implicit square roots with n=2. Square radicands additionally include exactly 1.2,1.4,1.5,1.6,1.8,2.5,3.5,4.5,7.5. These are conservative extensions of source values 2,5,10 and indices 2,3,7 under the tutorial's general identity. Decimal conversion adds no arithmetic: copy the written base unchanged.

For indexed source-style banks only, retain x!=n and exclude (2,4): these cases merge choices. For square source replay only, exclude x=2 and x=4: role-swapped or division choices merge. Normal square practice permits both 2 and 4; source-bank degeneracies do not constrain a different practice bank. Positive bases >1 avoid branches and trivial base 1; small indices >=2 represent genuine roots. No prime/nonperfect-power restriction is imposed.

Fixed numerator 1 is the assessed conversion rule. A single radical and one substitution preserve workload; five choices and one key preserve the captured radio contract. Implicit n=2 is mathematical notation. The particular source numbers, answer positions and UUIDs have no instructional reason to stay fixed. Choices are shuffled. Batch sampling without replacement in (x,n) preserves 126 distinct numerical instances across the generator; wording, bank variants and shuffles do not increase this count. Requests beyond that capacity are rejected explicitly. Normal sampling uses already-valid domains without a rejection loop.

## Feedback repair: authored square practice profile

The review's strategy—decimal-base numerator-1 power when present, otherwise the larger-base numerator-1 power—solved every prior square item. Decimal variation alone was insufficient. Normal square generation now uses the explicitly authored **square-index-confusion** profile, while source replay explicitly retains **square-division**.

Repair 3 specification, written before changing code: choose distractor-index case first: m=1 (below 2) or m in {3,4,5} (above 2). Choose the other base's direction below/above x and independently which base receives the inverted-power foil; then choose the radicand case/value. For each integer or decimal domain separately, form unordered neighboring pairs in numerical order. Choose an eligible direction before a compatible target; b is the neighboring domain value in that direction. Both orientations of every pair are allowed. At the minimum or maximum, only the inward direction is eligible. This prevents foils outside the target domain (including decimal gaps) from becoming recognizable never-correct bases. Both bases have the same integer/decimal appearance, remain >1 and differ. Neighboring domain values keep choices compact without requiring root evaluation; the pair spacing is an authored presentation choice, not a new learner operation. The fifth option's base c independently equals x or b. The complete practice bank is:

- x^(1/2), the key;
- b^(1/2), correct index but wrong base;
- x^(1/m), correct base but wrong index;
- b^(1/m), wrong base and index;
- c^(2/1), inverted exponent.

This extension preserves one-step conversion and source-style exponent notation; denominator 1 already occurs in observed distractors. It changes distractor discrimination, not the learner's method. No new feedback or solution steps are invented. Each plausible base appears twice among written numerator-1 powers; either may appear a third time in the full bank. Therefore base frequency, decimal appearance and base magnitude do not uniquely identify the key. Both base and index must agree. Keeping only m>2 would create an exponent-rank cue, so both m cases are included. Selecting exponent 1/2 for a square root is the tutorial's taught rule, rather than an incidental predictor.

## Answer-bearing assignments and validation

The decisive roles are radicand/base and index/denominator. Indexed x<n and x>n cases allow swapping numeric roles with the same complete bank and a changed key. Square n=2 is fixed by notation; the qualifying base can be the lower or higher displayed base, more or less frequent in the bank. m and the inverted foil's base do not change the correct response. Their variation must preserve prompt/key/solution while changing the complete bank and identity.

Check all 23 square radicands, 4 m values, eligible inward/neighbor directions, and 2 inverted-base assignments: 336 bank configurations, representing 23 numerical conversion tasks. The count stays 336 because four outward boundary directions are removed while targets 2 and 4 are added. For each same-bank pair, swap the target and inverted-base assignment and verify the other half-power becomes correct. Every displayed square-practice base must be observed as both target and foil, including within each recognizable complete bank and foil-index/inversion group. Probe the reported avoid-4 strategy before and after delivery and grade its attempts natively; also check each other displayed value for never-correct status. Ordinary seeds include the review seed 92718 and a directly observed seed reaching target 4. A small ordinary seeded regression exercises unchanged indexed behavior and every sampled square slot; seed 7 closes the initial sample's missing m=3 case. Exact independent rational-power checks read the served prompt, all choices and solution. Source banks are checked separately from practice extensions.

Controlled tests swap x,n; change only index; change only radicand; reorder choices; and vary only distractors. An additional same-bank square pair changes the prompt from sqrt(7) to sqrt(8), reverses the key and rejects the former key with the native grader. Check delivery with the shared filter, then repeat within-template and integer/decimal/foil-index/base-direction probes for fixed positions, numeric ranks, numerator-1 order, base-size/decimal cues and base frequency. Intermediate repairs revealed rank and frequency predictors; both were repaired before final delivery. Reports distinguish fidelity, correctness, grading and decision variation. Numerical ordering deductions that actually use the root/base relationships remain valid mathematical eliminations; these tests do not claim absence of every possible strategy.

All 336 square configurations must survive delivery. The captured inventory is basis 3777. Read-only selection code inspection shows history exclusion, weighted band choice and uniform hash choice within a positive-weight band, with a first-candidate branch for unconfigured policies. Live learner history, actual weights and future entity identities are unavailable: no actual learner distribution or publication is claimed. Representative application UI screenshots are inspected visually after the shared renderer completes. No database or published-image changes are part of this work.

Repair 3 evidence is saved under evidence/repair-3; earlier evidence remains intact. The tutorial square-root identity and e-4959 radicand 4 justify admitting 4; q-69219 justifies preserving its original square-division bank solely in source replay. This repair changes eligible assignments and distractor compatibility, not prompts, response contract, solution stages, or easy workload. No source errors were discovered; q-69158 still lacks its original key, solution and difficulty.

Repair 3 completed validation: 3 complete source banks and all 15 choices replay; independent arithmetic passes for 336 square configurations (23 tasks), 45 seeded regression records and controls. All 168 complete-bank target pairs survive delivery and native grading rejects the former response in both directions. Avoid-4 changes from 16/16 in preserved prior delivered evidence to 16/32 in repaired delivered evidence. All nine actual UI screenshots were visually inspected. See evidence/repair-3/summary.json for separate fidelity, correctness, grading and decision-variation claims, and commands.md for reproduction.
