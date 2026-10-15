# Frozen native grader compatibility evidence

Actual served records use the observed radio answer type. `native-report.json` tests all five field-owned choice IDs on every bounded instance, separately from foreign and malformed IDs. These are selection tests, not symbolic-math tests.

`native-math-input.json`, `native-math-report.json` and `engine-limitations.json` separately exercise real math comparisons through diagnostic blank fixtures over all 306 bounded instances. These fixtures do not replace the served radio format. Both arbitrary-constant representations describe the same interval-wise primitive family.

With the original `K` inside the logarithm, all 306 canonical entries and all equivalent explicit-product, constant-shift, log-power and argument-scale entries return `unclosed group`; even the ordinary wrong primitive with an added x cannot be compared. This is a parser compatibility limitation, not evidence that a wrong answer is accepted.

With the same family written using an external additive C, all 306 canonical entries and 306 explicit-product equivalents are accepted; all 306 ordinary wrong primitives obtained by adding x are rejected. However, all 306 valid primitives shifted by 1 are rejected, all 306 valid positive log-argument scalings are rejected, and all 306 valid log-power rewrites return unresolved domain differences. K|x| and |x| are positive on each declared interval, so those log-power rewrites are real identities there. Additive shifts and positive scaling inside the logarithm only change the arbitrary constant. Their validity was independently differentiated before native checks. No valid parameter was excluded to hide any gap.

The report contains 612 accepted, 918 rejected and 2754 unresolved outcomes across 4284 diagnostic checks. Those aggregate outcomes include malformed entries and the documented valid-math failures; they must not be read as 4284 mathematical grading passes. Per-case initial expected-versus-actual mismatch evidence is retained. No engine modification is made or proposed by this draft.
