# Staged vector/basis notation prevention fixes

Four publisher-ready replacements are listed in `generator-candidates.json`; package files are under `generator-notation-<kp>/`. `notation-generator.diff` is the exact entrypoint diff. Each package includes the latest shared `math_format.py` and `repair-evidence.json`.

- KP17592186119805: bold the vector labels a₁, a₂, b and the vector zero, preserving the scalar unknown’s ordinary font even for explicit labels a or b.
- KP17592186119806: restore source bold a, b, x on the easy/source-replay path. Scalar components xᵢ remain ordinary italic. Moderate/hard notation was already correct.
- KP17592186119854: bold only named vectors aᵢ and b in prompts and named-vector solution equations.
- KP17592186119857: bold aᵢ in prompts/solutions and restore calligraphic B in prompts, solutions and every basis choice. Visible escaped set braces remain present.

Notation changes occur before authored identities are computed. All four versions are bumped. KP19805’s UUID input now explicitly includes VERSION because its previous identity payload depended only on parameters and bank values. No existing database IDs, values, fields, memberships, history, domains or bank recipes were changed.

Validation covers 84 records: 24 fresh examples across every supported difficulty, 58 original-parameter source replays and two explicit scalar-label collision cases. Every new question UUID differs from the old package output. Fixed-instance mathematical prompts/solutions, whole banks and correct mathematical values match after stripping only font wrappers. Fresh pivot-basis batch balancing can choose different tasks because it predicts UI choice order from the new authored identities; its sampling domain and bank construction are unchanged.

All 415 native grading checks pass (83 accepted and 332 rejected; one canonical source example has no fields). `notation-generator-validation.json`, `notation-grading.json` and `notation-package-validation.json` retain the results. The four immutable-package digests and exact dependency closures were recomputed and verified. Browser results are in `notation-rendering.json`, with representative screens in `screens/notation-generator-*.png`.

Source replays are expressly recorded as authored presentation repairs to retained evidence, not byte-identical reproductions of original captured formatting. Only the parent may publish/register these packages; this agent performed no EDB writes or package publication.
