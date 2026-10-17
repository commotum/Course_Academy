# Slope-intercept classification duplicate repair

KP `17592186198347`, generator version `1.0.1`.

The copied package in `../../generators/17592186198347/` replaces verbatim
duplicate equations with the original lesson's two term orders. A coincident
system such as `y = 4x + 9; y = 4x + 9` now displays
`y = 9 + 4x; y = 4x + 9`. Slopes, intercepts, classification, answer banks,
difficulty, and worked solution remain unchanged. Both original source replays
produce the same question content and identities as before.

For coincident lines with zero intercept, reordering cannot produce distinct
equations. Random sampling therefore excludes these 16 cases, and explicit
requests raise `ValueError`. Zero intercepts remain supported for parallel and
intersecting systems. The finite sampling domain contains 46,344 unordered line
pairs: 43,320 intersecting, 2,736 parallel, and 288 coincident. The first equation
uses intercept-first order for every supported coincident system, regardless of
the caller's requested order.

Target question `17592186567796` needs only the first row of its prompt changed
from `y &=4x + 9` to `y &=9 + 4x`; its second row, solution, fields, answer keys,
difficulty, and saved responses remain valid. Question `17592186567774` already
uses distinct term orders and requires no change.

Validation was run with:

```bash
.venv/bin/python -B reference/edb-math/repairs/2026-10-16-classification-duplicates/generator-evidence/17592186198347/validate.py
```

`verification.json` records 1,559 checked records, both source replays, every
supported coincident coefficient pair under both ordering inputs, rejection of
all zero-intercept coincident inputs, 24 random seeds, both CLI difficulty aliases,
and traversal of the complete finite sampling domain. The independent equation
parser verifies classification and all three answer fields. The application
grading engine accepted 4,677 correct selections and rejected 9,354 incorrect
selections with no unresolved checks. This validation performs no database writes.

The immutable prior package was read only. `math_format.py` and `source_data.json`
are byte-for-byte copies of that package. Generator SHA-256:
`dabef14b01943d731c0982f05b4fdeb864f5d36e5fc5f1690be2e0b88e01a2f0`.
