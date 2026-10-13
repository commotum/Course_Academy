# Verified inventory replenishment

Committed 10 distinct questions at math basis 1839 from basis 1838: 1 easy,
4 moderate, and 5 hard. Inventory recheck has no remaining KP jobs.
The stable generator UUID is `dfffdbe0-55bc-5179-afd6-8833cf35d3d2`, registered
with repository-relative script `generate/scratch/17592186087819.py`.

The original frozen generator and all 114 frozen evidence files remain unchanged.
All seven source questions and the canonical example were preserved. The durable
transaction has only additive content datoms for this KP and its new content,
attributed to `:application/ca-engine`; learner and engine history are unchanged.

`replenishment/prepared/` contains local generated instances, independent table,
edge and solution checks, native grading (15 accepted, 39 rejected, 0 unresolved),
and the ten-plot visual review. Distinctness canonicalizes all station renamings
and excludes seed, identity, choice order, geometry and heading permutations.

`replenishment/basis-1838/` retains exact EDN, the complete durable request,
preview, receipt, exact-basis readback, image hashes and inventory verification.
The application lock was held from the fresh basis read through submission and
readback. Images were published through the existing content-addressed store.
No capability exceptions were needed. The hard family is the previously validated
authored four-station template with independently reordered table headings.

To recover the exact saved submission and verification without creating new intent:

```sh
.venv/bin/python generate/scratch/17592186087819/replenish.py commit
```
