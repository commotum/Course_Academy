# Native equivalent-form restriction

The canonical source and generated blank fragments, equivalent expanded polynomial/exponent forms, and wrong submissions are checked in `engine-validation.json`. Those required grading checks pass.

One additional mathematically equivalent form is unsupported by the application's current symbolic rules: for q-355562 with h=-2, `e^(2) e^(2x) e^(x²/2)` equals the expected `e^((x+2)²/2)`, but `learning::grade_field` returns “symbolic equivalence is not established by the supported rules.” The independent displayed parser and SymPy prove this equality; the extra native capability check reproduces the restriction in `engine-equivalence-limitation.json`. It is not counted as an accepted submission or a source-fidelity match.

The supported equivalent submission `e^(x²/2+2x+2)` passes native grading. Generator answer fragments retain source notation and use the supported form; the restriction on additional learner product-form entries remains an application limitation. No engine change is attempted in this per-KP assignment.
