# Remaining parametric KPs: readability audit and repairs

Completed on 2026-10-30. Audited lesson **17592186087892 — Graphing Curves Defined Parametrically**, topic **17592186048293**. The source lesson confirms four KP steps: the already repaired graphing KP plus the three below.

Initial shared snapshot: **T11773**. Repairs committed at **T11800** and **T11801**; fresh readback and grading verified at **T11801**.

## Findings and action

| KP | Finding | Action |
|---|---|---|
| 17592186087717 — Filling a Table of Values for a Parametric Curve | No plotter. On a phone, the wide generated table could hide a requested letter/cell beyond the visible columns. The final aligned substitution could also be wider than the panel. | Generated tables now use at most three parameter columns per panel, repeating t/x/y headings. Global parameter/target associations stay intact. The final substitution uses separate centered lines. Published version `parametric-table-3`; 17 unused questions retired and 15 replacements added. |
| 17592186087722 — Determining the Range of a Parametric Equation | No plots; fresh equations, interval responses and worked bounds displayed correctly. | No generator change, question retirement or refill needed. Its existing registration and pool membership were verified unchanged. |
| 17592186087736 — Determining the Range of a Parametric Equation Defined in Terms of Trigonometric Functions | No plotter. Both coordinate formulas occupied one wide gathered row, and empty bounds controls could wrap away from the rest of their inequality. | Each coordinate formula and the domain now has its own display. Bounds entries begin in their own paragraph. Published version `2.0.2`; 13 unused questions retired and 15 replacements added. |

Thus the automatic plot-tick flaw was confined to the graphing KP repaired earlier. The remaining lesson audit found and repaired two related presentation problems without changing their mathematics.

## Preservation and availability

- **30 unused generated questions retired; 30 new unused questions published**, five easy, five moderate and five hard for each repaired KP.
- Used table question **17592186557691** remains unchanged, including its saved responses and prior presentation. No used question was retired or rewritten.
- All imported questions and canonical examples remain unchanged. Initial inventory covered 57 imports, three canonical examples and 49 active generated questions across these three KPs, 109 question records in total.
- Sampled parameters, requested cells, given values, signs, derivations, keyed answers and difficulty definitions are preserved at identical seeds. Only presentation and the resulting new question identities change.
- Old question/field/answer entities and ownership links remain intact; retirement only excludes future selection. No learner or engine facts were changed.

## Prevention

`generate/parametric_layout_policy.py` checks the delivered content at publication: small table panels, independently visible trigonometric formulas and bounds inputs starting on their own line. `generate/docs/7-plot-generator.md` now explicitly includes readability of companion tables and defining formulas. The learning service was reloaded to use the checks.

The local scratch entrypoints delegate to the same immutable packages now registered in production:

- Table KP: `generators/4c/4c9fe9749cdac4cfc8fd9d4b82afb05541e87580c19d1e80c9d1e81ae916d9de/generator.py`
- Trigonometric range KP: `generators/e2/e2478e678f31b037427dc6d99ace378950f184639a80db63b16798d5a178202e/generator.py`

## Verification

- All captured prompts, solutions and answer values scanned: no stored graph assets in any of the three remaining KPs. All three registered packages inspected; none contains a plot renderer.
- Eighteen fresh baseline questions generated, two per band per KP. Nine baseline desktop renders and three phone renders established the display findings.
- Thirty replacements compared with the preceding generators at identical seeds: every table cell/target association, parameter set, answer value and mathematical derivation preserved. See `repair-verification.json`.
- Final six representative questions, one per repaired band/KP, passed desktop, phone and active-phone rendering. Screenshots were visually inspected. All twelve table panels in both phone review states fit without horizontal overflow; empty input controls remain visible. Evidence: `repaired-desktop/`, `repaired-phone/`, `repaired-phone-active/`.
- **25 regression tests passed:** `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_parametric_layout_policy tests.test_parametric_plot_policy tests.test_matrix_product_prompt_policy`.
- Exact previews, stable requests, source-aware receipts, normalized delivery identities and readbacks verified. Requests are archived in each repaired KP's `publication/requests/` directory; none remains pending.
- Installed package closure and local/package byte agreement verified.
- **60 live grading checks passed:** a complete correct response and a complete response with one wrong numeric field for every replacement question. Verification recorded no learner attempts. See `completion.json`.

`audit.json` records the initial plot-usage scan; the findings above include the subsequent UI review. Exact retired/new entity IDs are in `publication-verification.json` and each repaired KP's `verification.json`.
