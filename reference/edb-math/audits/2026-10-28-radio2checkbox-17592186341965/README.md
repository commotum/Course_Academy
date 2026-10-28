# Checkbox suitability assessment — 17592186341965

Recommendation: convert the imported Math Academy question `q-73401` to three independently selectable x-values: `$x=0$`, `$x=2$`, `$x=6$`. The correct subset remains `{0}`.

At x=0 the graph has a horizontal tangent (a stationary inflection point). At x=2 it has a sharp corner, which is critical but not stationary. At x=6 it crosses the x-axis with nonzero slope. Both question and solution images were visually inspected, and these observations agree with the existing database key and worked solution.

Every old radio option has an unambiguous subset mapping, retained in `case-ledger.json`. One saved correct learner response maps to true/false/false; its grade, time and other history must be preserved in a subsequent migration. The graph stays in the prompt; complete x-values become field keys. Add “Select all that apply.” once. The question is not a canonical example.

This run is assessment only: no transaction prepared, previewed or committed. The live state was captured at basis 9855. The old discovery audit had already detected combination options, but its parser did not decode the x-value subsets; the live case ledger now resolves them explicitly. See `capture.json`, `case-ledger.json` and `status.json` for complete evidence and the future migration handoff.
