# Classification — Computing Higher Order Derivatives

Status: working; local draft pending independent parent QA. Immutable math basis 2275, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json`, `topic.json`, `lesson.json` are byte-for-byte copies of refresh-2026-10-14 wrappers. No generator was registered and neither numeric script nor evidence directory existed at initial inspection. See baseline.json. No EDB reads/writes or shared-file changes are required.

All 11 captured practice questions have Math Academy IDs. Independent inventory is empty. The canonical example e-3655 demonstrates exactly three successive derivatives after rewriting a quotient into powers. The topic distinguishes this KP from Computing Second Order Derivatives and Evaluating Higher Order Derivatives. Supplied points/evaluation targets are therefore absent: the requested object is the entire derivative function. The lesson route follows activity/first-step and step/next (not collection order); its introductory definition builds successive derivatives, and the fourth-order examples justify exactly four stages at hard. Key prerequisite: Differentiating Exponential Functions, with predecessor context Differentiating Trigonometric Functions and Differentiating Logarithmic Functions. Neither chain/product-rule compositions nor arbitrary-order pattern induction is introduced.

| Level | Original sources | Field contract | Templates | Plots |
|---|---|---|---|---|
| easy | q-104294, q-343075, q-343089, q-343114 | one radio bank of5; three scalar blanks | log/radical; two monomials; exponential/reciprocal; log/polynomial | none |
| moderate | q-28546,q-28551,q-310170,q-343086; q-28550 unrated | observed radio5; blank1; one fieldless source; unrated radio5 lacks correct | quadratic/linear/reciprocal; cubic/reciprocal; quadratic/constant/reciprocal; quotient sum | none |
| hard | q-310171,q-343120 | scalar blank1 | cosine/log; sine/exponential | none |

Template keys distinguish the observed radio/blank presentations of quadratic/linear/reciprocal even where their mathematical backbone agrees. q-28550 is assigned moderate as an explicit authored classification: its third derivative of a cubic plus reciprocal has the same three power-rule operations and no new skill beyond the observed moderate power rewrites. All three difficulty levels have observed anchors; none is an invented missing level or an internal progression.

Plots are absent in prompts, banks and solutions. Scalar math rendered from TeX is not a plot; docs5/7 do not require plot assets here.

Source defects retained in public raw replay:

- q-28550 omits difficulty, correct designation and worked solution. Its fifth option is independently verified as the third derivative. Normal served output supplies an authored moderate level, correct lookup and three-stage solution; the missing designation does not count as recovered fidelity.
- q-28551 omits answer fields. Its first solution block labels the supplied y as h(x). Normal output repairs this label and supplies one authored scalar blank. Raw omits the original fields rather than inventing an empty list.
- Several captured answer strings contain actual doubled backslashes. Normal scalar expressions reduce them to TeX command backslashes; aligned row separators are retained. U+2061 invisible function application is removed in normal scalar fragments. These are notation normalizations, retained byte-exact in raw records.
