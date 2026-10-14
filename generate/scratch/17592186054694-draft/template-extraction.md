# Four-stage extraction

## 1. Each original specifically

q-54397 supplies y=x-2, x=0,1,2,3, four blank y cells, unaligned Markdown headings, one selection radio with five images. Shared solution opens “First, we fill the table.” Its “Therefore,” remains on the opening paragraph; four bullets compute (0)-2=-2 through (3)-2=1, with “and” after the third. A completed table follows, then “We plot these $(x,y)$ pairs on the $xy$-plane:”, points-only plot, “Finally, connecting the points gives us a straight line. This is the graph of”, and line plot.

q-71695 supplies y=2x+2 with the same empty table and field. Its solution omits the comma after “$x$”, places “Therefore, we obtain” on the next line, evaluates 2(0)+2=2 through 2(3)+2=8, then table, “Plotting these $(x,y)$ pairs on the $xy$-plane: ”, points-only plot and the same final stage with two spaces before the formula. These differences are preserved in normal parameterization.

q-59676 supplies $y =-x + 1$ with its punctuation outside math and right-aligned numeric table columns. The field is a five-image radio. Correct ref, difficulty, and solution are absent. Raw replay retains those omissions; normal solution is a clearly authored parameterization of q-54397.

## 2. Generalized backbone

Copy and compute the four-column value table from a supplied linear formula, then select the line containing the resulting four coordinate pairs. Fixed roles: equation is supplied, x values are supplied, y values are requested, graph is selected. m and b vary within level bounds; x=0,1,2,3 are fixed to preserve the observed four evaluations. Plotting and connecting follow the evaluated table, not an already-filled prompt. No feedback or choice-dependent solution exists.

## 3. Complete original components/banks

Each original choice's field UUID, answer UUID, source asset, SHA, full equation, four marked points, axis/grid calibration and recipe is in source-choice-mapping.json. Whole original banks in source order are:

| Profile | m,b anchor | Five (slope,constant) recipes | Correct slot |
|---|---|---|---|
| q-54397 | 1,-2 | (-m,0); (m,b); (-m,-b/2); (m,-b); (m,0) | 2 |
| q-59676 | -1,1 | (m,2b); (-m,-2b); (-m,-b); (2m,4b); (m,b) | 5 (authored inference; source key absent) |
| q-71695 | 2,2 | (m,-b); (-m,b/2); (-m/2,b); (m,b); (m/2,b) | 4 |

Recipes are applied to the equation's product and constant operations, then independently evaluated into each graph's four points. Sign reversal, omitted constant, or halved product are clear operation variants. Compound reverse/halve-constant and double-product/quadruple-constant patterns are empirical parameterizations with inferred error interpretations; psychological intent is not recoverable from these images. They are not arbitrary perturbations of unrelated values. There are no unmapped original options. The q-71695 second option must use b/2, not b.

## 4. Reusable templates/slots

Prompt and solution are source-specific masks. Slots m,b jointly control displayed formula, every substitution bullet, evaluated result, completed y row, final prose formula, points and line. Preserve table alignment and each original shared sentence. Arithmetic rows remain unsimplified substitution followed by one evaluated value, just as in the originals; no extra invented teaching rows. Special unit coefficients omit a literal 1, negative unit coefficient uses -(i), and half coefficients render exact fractions. Conditional sign suffixes never emit bare +- or --.

Choose the complete profile before parameters; derive the correct line first and every wrong line via that profile. Reject the entire bank on equivalent whole equations, multiple correct members, or insufficient rendered scale. Never select five members from a pooled candidate list. Easy defaults serve all three observed banks; moderate/hard use authored complete operation bank (m,b),(-m,b),(m,-b),(m,0),(2m,b): product sign, constant sign, omitted constant, doubled product. No distractor diagnoses are shown to the learner. Authored level limits are in classification.md and task_domain; normal positive easy constants are even so every source-shaped bank has integer marker ordinates.

Raw public replay requires source_replay=true with original m,b, template and profile. It uses the same formula/table/solution masks, preserves original raster references, and also renders every mathematical recipe into separate recreated_assets. Attribute-presence parity is tested independently. Normal outputs contain completed field/key/solution/difficulty, with missing negative-family elements marked authored in generation metadata.

Task fingerprints describe the reduced equation, four inputs, requested operation and relevant grid increment. They exclude profiles, templates and bank order. Content identity includes difficulty, actual prompt, fixed concrete solution, complete displayed bank and correct asset, excludes seed and shuffle, and owns all answer UUIDs under its field. All sampled records have plain outer knowledge_point keys and colon-prefixed schema-shaped records.
