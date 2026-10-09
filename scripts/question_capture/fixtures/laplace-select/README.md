# Laplace custom-select retry fixture

`rejected.json` is the unchanged saved DOM extraction from lesson 14042893,
question 340719, diagnostics/1791455218970094765. `record.json` retains its
prepared retry and the original intentional wrong submission.

`select-list.js` is the original public Math Academy widget saved during the
October 7 recovery of lesson 14040950 (manual-recovery/select-list.js). Tests
use its unmodified mouse handlers and a layout-only Core shim. They do not
read correct-answer configuration or call widget selection methods to enter
the answer. A native frame-padding click must leave the actual option visible.
