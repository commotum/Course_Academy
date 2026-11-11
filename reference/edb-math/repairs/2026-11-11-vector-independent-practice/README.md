# Independent vector decomposition practice

This repair removes the supplied construction from ordinary easy practice for **Finding a Scalar Factor When Direction Reverses** (KP `17592186235285`). The learner sees only the three original vectors and a uniform grid, then constructs the known multiple of **b**, finds the residual parallel to **a**, counts its relative length, and determines the negative scalar. Easy keeps its axis-aligned reference vector and integer coefficients; the moderate and hard mathematical domains and response formats are preserved.

The [sibling audit](sibling-audit.json) examined all 27 stored pool questions at basis 14216: 14 imported records and 13 authored records. Only question `17592186735164` supplied the auxiliary path and residual length. Its [proposed repair](stored/proposed.json) moves the construction to the worked solution, retaining the question, fields, answer UUIDs, key, difficulty, and choices. The other 26 records remain unchanged.

The new plot renderer places **a** and **b** labels outside their angular wedge using the sign of their determinant, preserving coordinates while keeping labels associated with their arrows. Prompt diagrams show no auxiliary point or path; solution diagrams retain the worked construction.

Validation is recorded in [preflight-verification.json](preflight-verification.json):

- All 36 ordinary samples (12 per band) survive actual publication filtering and pass isolated package-bound refill checks plus native grading. Relocated execution preserves exact identities and all referenced PNG bytes.
- All 14 source replays preserve their original mathematical content and response structures ([report](source-replay-verification.json)).
- Four retained mutations are rejected: auxiliary path prose, a solution image substituted into the prompt, a changed visible known coefficient, and a wrong key ([report](refill-regressions.json)).
- The exact normalized delivery survivors have 24 actual player cases: two representatives per band, active/completed states, and 390/1100 pixel widths. Raw-record UI evidence is retained separately. The repaired stored question has four additional actual player cases and native checks accepting only its unchanged `-1` key.

[The guarded publication script](publish.py) requires the independent accepted report and explicit `--apply`. It holds the existing worker KP lock, refreshes the complete pool and registration, uses the native durable CAS/outbox transport, verifies the exact receipt and retained historical snapshot, then publishes a replacement immutable generator registration and all-band approval. It adds no questions and preserves the prior generator package/entity. Unknown outcomes retain their exact request for recovery.

## Confirmed publication

Both writes completed under the existing worker KP lock with contributor `:agent/codex`:

| Change | Basis | Receipt |
| --- | --- | --- |
| Target prompt and solution CAS | 14218 → 14219 | [Stored repair receipt](stored/apply/requests/capture-8fa95add-77aa-485a-9ac0-3b4d7b836cc2/receipt.edn) |
| Immutable generator registration | 14219 → 14220 | [Registration receipt](publication/1/requests/capture-8de22e73-21e8-413d-9849-c1d4684a17d0/receipt.edn) |

Final [current readback](final-verification.json) at basis **14220** confirms the target matches the reviewed proposal exactly, the other 12 authored questions and all 14 imported questions are unchanged, the old generator entity and package bytes remain intact, and all three new approval bands resolve. The retained historical snapshot and every question field, answer ID, choice, and key are verified unchanged. Receipt datoms contain no learner or engine changes. No extra questions were published.

Current registration:
`generators/61/61c2af93a404592ba4e52ae454bbf307eefacb918697db13dc1dfb6087486e12/generator.py`

[Installation verification](installation-verification.json) records both durable request keys and the actual approval path. The [independent accepted review](review/report.json) binds the final package and evidence; the approval retains its byte hash and the byte-identical source-only checkpoint. No global service setting or generation toggle was changed.
