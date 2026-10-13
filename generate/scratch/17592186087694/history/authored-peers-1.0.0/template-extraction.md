# Template extraction

Source provenance: database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Raw question/field/answer identities and strings remain in source.json.

## 1. Specific source descriptions

- q-7810: 3×1; entries `[["5"], ["-9"], ["2"]]`; name G; template legacy_column; profile legacy_column_observed; unrated (authored easy assignment), missing correct and solution.
- q-7812: 1×1; entries `[["3"]]`; name J; template legacy_singleton; profile legacy_singleton_observed; unrated (authored easy assignment), missing correct and solution.
- q-125543: 1×1; entries `[["\\sqrt{2}"]]`; name Y; template aligned_radio; profile singleton_root_observed; observed easy with complete solution and designation.
- q-319329: 4×1; entries `[["2"], ["-\\sqrt{7}"], ["0"], ["4"]]`; name S; template double_blank; profile blank_observed; observed easy with complete solution and designation.
- q-319338: 5×1; entries `[["\\frac{2}{3}"], ["-\\sqrt{3}"], ["5"], ["0"], ["-4"]]`; name E; template double_blank; profile blank_plural_observed; observed easy with complete solution and designation.
- q-7809: 1×4; entries `[["3", "5", "2", "7"]]`; name F; template aligned_radio; profile row_observed; observed easy with complete solution and designation.
- q-7813: 1×1; entries `[["0"]]`; name K; template aligned_radio; profile singleton_zero_observed; observed easy with complete solution and designation.

All counts are exact nonnegative integers in choices and positive integers in the correct ordered dimension. Matrix entries can be negative, zero, rational, or irrational and need no arithmetic. Singleton integer/zero/root matrices stay 1×1. The legacy column uses bmatrix; legacy singleton uses bare brackets. Other matrices use bracketed aligned arrays. Dual blanks supply × in the prompt and expect individual delimiter-free row/column integer fragments. All existing worked solutions contain one sentence with row count, column count and ordered dimensions; there is no optional computational stage.

## 2. Generalized family

Count the visible rows and columns of the displayed rectangular array, guaranteed to have exactly one row or one column; respond in row-first order. Radio and dual-blank response layouts remain separate. Every fixed solution reports those same two counts and the ordered pair. No operation on the numerical entries occurs.

## 3. Components and complete observed banks

Below, n is the non-singleton length; v is the actual scalar integer entry in the legacy singleton source. Parameterized recipes reproduce every displayed original answer, rather than returning a copied source payload. Descriptions of possible errors are author analysis only, never learner-facing diagnosis. The final arbitrary two-count options in q-7810 and q-7809 have unresolved error intent; their affine n patterns preserve explicit replay profiles and are excluded from the normal authored default bank.

### q-7810 / legacy_column_observed

Prompt parameters: `{"name": "G", "entries": [["5"], ["-9"], ["2"]]}`. Prompt and complete original solution are reproduced verbatim at these parameters. Missing solution is authored using the common one-sentence counting solution; no exact source solution match is claimed.

| Original answer identity | Field | Exact value | Parameter recipe | Correct designation |
|---|---|---|---|---|
| 8fb6036d-2f45-5e42-a66d-a17b7f581049 | selection | `1 \cdot 3` | (1,n), reverse correct order | missing; derived independently |
| b23ce2f4-0139-596f-917f-dc1501f12b60 | selection | `3 \cdot 1` | (n,1), correct | missing; derived independently |
| 272c8629-b522-55c3-af51-9f85d9a857d0 | selection | `1 \cdot 1` | (1,1), treat as singleton | missing; derived independently |
| 4f983ecc-373f-542a-ade6-8fa1b364ddc1 | selection | `3 \cdot 3` | (n,n), repeat count | missing; derived independently |
| 63d88fd8-d123-5d16-ab5f-7b24ea945f03 | selection | `5 \cdot 2` | (n+2,n−1), observed affine count pattern; intent unresolved | missing; derived independently |

### q-7812 / legacy_singleton_observed

Prompt parameters: `{"name": "J", "entries": [["3"]]}`. Prompt and complete original solution are reproduced verbatim at these parameters. Missing solution is authored using the common one-sentence counting solution; no exact source solution match is claimed.

| Original answer identity | Field | Exact value | Parameter recipe | Correct designation |
|---|---|---|---|---|
| b573ea9e-f98d-51ac-ab07-8c9da2128ca0 | selection | `3 \cdot 3` | (v,v), repeat actual integer entry v | missing; derived independently |
| 0aaa29ba-c358-5618-bb62-ff32cf60ea37 | selection | `0 \cdot 1` | (0,1), omit row | missing; derived independently |
| 1ea3c471-87ad-5e26-940e-5a46295df2c6 | selection | `1 \cdot 1` | (1,1), correct | missing; derived independently |
| 6ce14289-1e38-500d-959d-daa5474f83d7 | selection | `1 \cdot 0` | (1,0), omit column | missing; derived independently |
| 75bbb3a3-fc36-5d5b-9414-5b190e86d827 | selection | `0 \cdot 0` | (0,0), omit both | missing; derived independently |

### q-125543 / singleton_root_observed

Prompt parameters: `{"name": "Y", "entries": [["\\sqrt{2}"]]}`. Prompt and complete original solution are reproduced verbatim at these parameters. 

| Original answer identity | Field | Exact value | Parameter recipe | Correct designation |
|---|---|---|---|---|
| 3be42067-2933-5795-a1a2-3b432fbdef93 | selection | `2\times 0` | (2,0), fixed singleton confusion pattern | incorrect |
| 4849906e-b655-574f-8189-1c2c0e744b8e | selection | `0\times 2` | (0,2), fixed singleton confusion pattern | incorrect |
| 908e00be-d907-5375-a64b-aff0e8f2ce6b | selection | `1\times 2` | (1,2), add column | incorrect |
| ad6fcd54-0c51-54bd-8ea7-6a63e6966a71 | selection | `1\times 0` | (1,0), omit column | incorrect |
| d703c571-a647-53a7-b8fd-08309f9c4f5f | selection | `1\times 1` | (1,1), correct | correct |

### q-319329 / blank_observed

Prompt parameters: `{"name": "S", "entries": [["2"], ["-\\sqrt{7}"], ["0"], ["4"]]}`. Prompt and complete original solution are reproduced verbatim at these parameters. 

| Original answer identity | Field | Exact value | Parameter recipe | Correct designation |
|---|---|---|---|---|
| a83ce5d2-ae50-5da8-8996-6422c7c0a2d2 | field-2 | `1` | column count c | correct |
| 5fb2a1a9-c3cd-5a18-98b2-04f3e7a3fdfb | field-1 | `4` | row count r | correct |

### q-319338 / blank_plural_observed

Prompt parameters: `{"name": "E", "entries": [["\\frac{2}{3}"], ["-\\sqrt{3}"], ["5"], ["0"], ["-4"]]}`. Prompt and complete original solution are reproduced verbatim at these parameters. 

| Original answer identity | Field | Exact value | Parameter recipe | Correct designation |
|---|---|---|---|---|
| dea3c616-7e99-5761-bcb9-6479e1463e61 | field-2 | `1` | column count c | correct |
| 87555767-370d-5023-baf3-c1a8898dfd85 | field-1 | `5` | row count r | correct |

### q-7809 / row_observed

Prompt parameters: `{"name": "F", "entries": [["3", "5", "2", "7"]]}`. Prompt and complete original solution are reproduced verbatim at these parameters. 

| Original answer identity | Field | Exact value | Parameter recipe | Correct designation |
|---|---|---|---|---|
| 084d51f3-27f2-5017-9b38-8362f1786e68 | selection | `0\times 4` | (0,n), omit row | incorrect |
| 1f19011d-f9d7-51a2-b47b-062470e495ec | selection | `4\times 0` | (n,0), transpose/omit | incorrect |
| 7b5ee179-ea1e-5b7b-8108-6d7ffb3f3335 | selection | `4\times 1` | (n,1), reverse order | incorrect |
| 7f7b8f9f-5bd0-5fbb-946c-210bcc263174 | selection | `1\times 4` | (1,n), correct | correct |
| ddc997d2-fa6c-5774-9ee3-84c1a35725c3 | selection | `3\times 7` | (n−1,2n−1), observed affine count pattern; intent unresolved | incorrect |

### q-7813 / singleton_zero_observed

Prompt parameters: `{"name": "K", "entries": [["0"]]}`. Prompt and complete original solution are reproduced verbatim at these parameters. 

| Original answer identity | Field | Exact value | Parameter recipe | Correct designation |
|---|---|---|---|---|
| 6566e598-cb1c-51c3-a8e3-4ec7612e30d1 | selection | `0\times 1` | (0,1), omit row | incorrect |
| 7282b7d2-2397-5aef-930b-783a51a6848d | selection | `0\times 0` | (0,0), omit both | incorrect |
| 9db5d0c8-7adf-5e26-8910-e951b18b1e7d | selection | `1\times 0` | (1,0), omit column | incorrect |
| 9dc46cde-97a9-5275-8bc5-579368638c4a | selection | `1\times 1` | (1,1), correct | correct |
| e282d817-00e6-5042-8940-b22a7b71761e | selection | `2\times 1` | (2,1), add row | incorrect |

## 4. Reusable templates, fixed/variable/conditional parts

The script renders each matrix from an actual nested array, joins entries with ` & ` and rows with ` \\ `, and fills the whole array and a single uppercase matrix-name slot. It never performs uncontrolled string replacement. The `prompt`, `render_array` and `solution` helpers hold the fixed grammar. Counts, row/column inflection, name and dimension factors are variable. Source-profile whitespace and connectors (So/Hence/Therefore) are fixed. q-319338 alone retains captured “1 columns” in its explicit observed prose profile; this grammar anomaly does not change mathematics, and raw-exact solution fidelity still counts it. The two absent legacy solutions receive authored common prose; absent correct refs receive independent ordered-count derivations. They are separately counted from matched existing designations.

The public generate API accepts explicit template/profile/object parameters for replay and rejects unsupported names, scalar grammar, magnitude, shape, length, response layout or profile constraints. The complete profile is selected before values are constructed; any duplicate ordered pair or nonunique correct answer rejects the whole bank. Seed shuffles choices after owned IDs are computed. Choices are ordered pairs, even if labeled with historical `\cdot`; commutative scalar product comparison is prohibited.

Normal authored non-singleton bank: (r,c), (c,r), (n,n), (0,c), (r,0). Normal singleton bank: (1,1), (0,1), (1,0), (0,0), (2,2). Zero counts are deliberate “no row/column” distractors consistent with the observed practice. No arbitrary-offset fifth distractor or entry-value arithmetic is used in normal defaults. Blank fields have no distractors. All profile variants use one fixed worked solution regardless of the chosen option.

Sampling and explicit calls share bounds: nine ordered shapes of lengths 1..5, scalar magnitudes at most nine, numeric integers/fractions/roots only. Legacy singleton observed bank additionally requires an integer entry 2..9 so its repeat-entry option remains distinct from (1,1). No source practice falls outside these bounds. Normal levels use exactly the same bounds; moderate/hard labels are authored peers because this narrow skill has no evidenced harder branch.

Mathematical fingerprint uses ordered dimensions only: entries, letter aliases, bank/prose profile and field layout are incidental to the assessed count. Content identity additionally uses version, actual prompt (thus actual entries), fixed full solution and complete displayed field/bank content; seed, option order and profile aliases do not create content identities. Two displayed matrices with changed entries share a mathematical count fingerprint but have different content identities.

Plots: none; TeX matrix arrays do not require raster rendering. Native radio grading tests every choice UUID; independent prompt parsing verifies each displayed ordered pair. Dual blanks test the actual engine with canonical scalar counts, unevaluated equivalent sums and incorrect counts. Exact original prompt, full source solution and every bank string are checked separately from mathematical correctness and grading.
