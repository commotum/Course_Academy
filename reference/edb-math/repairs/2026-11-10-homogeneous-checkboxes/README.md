# Homogeneous-equation checkbox conversion

Converted all **eight** homogeneous/inhomogeneous classification questions in **Introduction to Second-Order Linear ODEs** (`17592186050677`), including both questions requested by the user. Each now asks:

> Select all homogeneous second-order linear differential equations.

Each complete equation appears beside its own checkbox. All three classifications remain necessary: leaving an inhomogeneous equation unchecked expresses the same judgment as choosing “inhomogeneous” in its former dropdown. There is no separate “None” option.

Committed atomically at **13734 → 13735**, source **`:agent/codex`**, database lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The request and exact transaction hash are in [commit-intent.json](commit-intent.json); the confirmed writer report is [receipt.edn](receipt.edn).

| Question | Source ID | Homogeneous equations, in original order |
| --- | --- | --- |
| 17592186152571 | q-337919 | First |
| 17592186152572 | q-337990 | First |
| 17592186311903 | q-337996 | Second |
| 17592186311905 | q-338006 | First and third |
| 17592186311909 | q-338023 | Second |
| 17592186311914 | q-338087 | First and second |
| 17592186397097 | q-338004 | First |
| 17592186397107 | q-338082 | Second |

## Verification

- Independently checked all 24 equations by identifying their forcing terms after moving terms independent of the unknown function to the right. Existing correct keys agree in every case.
- Created 24 fields with complete equation labels and 48 separately owned Boolean answers. Retained all original field and answer entities unchanged.
- Mapped all eight possible old answer tuples per question. All **64 original tuples** and **64 converted subsets** passed the live read-only grading API. Native speculative grading also checked each Boolean answer, all canonical subsets, every single-checkbox flip, and rejection of incomplete responses.
- Preserved all **three saved attempts**, including the incorrect attempt, with equivalent selections and unchanged status, timing and other task-item state. Preserved explanations, difficulty and topic/KP memberships.
- Proposed, actual speculative and committed presentation lints passed. Exercised the actual player renderer and controls for all eight questions at 1100px, 708px and 390px: 24 renders, 144 selection toggles, and 24 saved-answer feedback checks. Zero MathJax errors or outer card overflows. At phone width, genuinely wider equations retain the application's existing math scrolling; no spurious short-formula scrolling was found.
- Verified exact committed records and material transaction datoms against the native preview, unchanged remaining questions across the complete 46-question lesson, historical reads at the original basis, and continued study availability.

See [verification.json](verification.json), [case-ledger.json](case-ledger.json), [status.json](status.json), and [screenshots](visual/).

The affected KP is `17592186152274`. Its October discovery source snapshot predates this conversion. No active generator for this KP was found under `generate/scratch` or `generate/runs`; archived source captures were retained as historical evidence.
