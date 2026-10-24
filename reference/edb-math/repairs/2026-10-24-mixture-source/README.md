# Mixture source repair

Topic 17592186050422, KP 17592186092285, question q-10628
(entity 17592186092502, UUID 7155be1f-7c98-5780-9627-c6ea68ff27d4).

The original bank offered no correct ordered pair. Conservation gives
0.55x + 0.30(8-x) = 0.40(8), hence x = 3.2 tons of 55% steel and
8-x = 4.8 tons of 30% steel. The existing reversed-pair option was corrected
in place after verifying that no learner response referenced it. Its identity,
the other four options, field identity, question identity, and problem remain.
The missing answer key and worked solution were supplied as local authored
content under the established `:agent/codex` contributor.

Canonical example e-930 supplies the percentage–total–part table, conservation
equation, simplification, multiplication by 100, and conclusion. Its unknown
added volume becomes two complementary unknown masses because this question
specifies a fixed final total. `solution.md` instantiates that template.
All five complete choices were independently checked against both conservation
equations; exactly the corrected choice satisfies them.

`before.json` captures the original KP at basis 6395. `candidate.json`,
`math-verification.json`, `grader-verification.json`, and `render/` record
prepublication validation. `commit/` retains the native preview and exact guarded
request/receipt; `verification.json` and `after.json` record exact readback at
basis 6396, including verification that no learner or engine facts changed.

The generator's previous inventory-repair path only supports retiring proven
generated questions. This is an original source question and was repaired
separately. No generated-record proof or independent approval was fabricated.
`resume.py` archives the old capture, refreshes source and inventory, records
an explicit bounded recovery, and requeues the original cycle for a new
independent review. The reviewed candidate package and five samples are retained.
