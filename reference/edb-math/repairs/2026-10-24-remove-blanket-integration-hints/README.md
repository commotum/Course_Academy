# Remove blanket integration hints

The user approved the recommendation in `reference/edb-math/audits/2026-10-24-integration-hint-provenance/README.md`.

Scope: the four recently repaired trig-substitution KPs and the eight inverse-trig/exponential-substitution KPs that inherited the same blanket support policy. Ordinary full-calculation prompts will require retrieval of mastered primitive formulas and routine endpoint facts. Explicitly guided transformation tasks retain their given substitutions. Domain assumptions and complete worked solutions remain.

This is a prompt/support change. Mathematical instances, answer values/banks, field response types, difficulty bands and family selection stay fixed. Integration rules formerly shown before answering move into the worked solution where needed. Complete old records remain attached to saved work: superseded hinted generated questions are retired and replaced; imports and canonical examples are preserved.

Future generators and delivery guards will enforce the revised policy. The pipeline will distinguish unfamiliar, source-justified support from the routine use of mastered prerequisites. A generic requirement to make questions easier does not authorize blanket formula reminders.

Capture, approval-ready records, package manifests, validation, previews, exact requests, receipts and readbacks are retained here. Final counts and live verification will be recorded after publication.

## Publication and validation

All twelve generator replacements were committed at T6736–T6747. Each KP has eight unchanged guided transformation questions and sixteen reissued full calculations. In total, 192 hinted generated records were retired and 192 hint-free replacements were added. The resulting active generated pool has 288 questions. All 183 imported practice questions, 12 canonical examples and saved learner references were preserved.

The build verifies unchanged mathematical models, integrands, bounds, difficulty labels, response types, complete banks and correct-answer values for all 288 records. Independent printed-math checks verify the rules moved into the worked solutions, differential factors, bounds and final keys. The actual shared delivery filter accepts exactly sixteen new records per KP and skips the eight unchanged guided records.

Validation: **63 Python regression tests**, **1,246 native grading checks** (526 expected accepts and 720 expected rejects; zero unresolved outcomes), and **36 actual learner-UI previews**. Representative ordinary prompts and complete solutions were visually inspected. Exact transactions, source/basis checks, receipts, historical readbacks and saved-reference comparisons are retained per KP. The final active-pool and live-grading results are recorded in `completion.json` and `live-grading-verification.json`.

The three reported hinted question versions are retired, with their replacement identities in `replacement-map.json`. Question 17592186678309 remains active and unchanged: its supplied substitution belongs to the explicitly guided transformation task.

Final readback at **T6747** verified all 288 active generated questions and all twelve immutable registrations against the local mirrors. **102 live, read-only grading checks passed**, including −3 ln(cos(x)+2) on the replacement of 17592186678417. Question 17592186678309 remains active with its original identity.

Reported replacements:

| Retired hinted version | Current hint-free version |
|---|---|
|17592186678090|17592186682486|
|17592186678190|17592186682539|
|17592186678417|17592186682659|
