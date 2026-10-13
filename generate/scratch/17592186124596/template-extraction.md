# Template extraction

Evidence: math basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; unchanged wrapper in source.json. No plots. Every source answer is a complete scalar derivative expression in one five-choice radio field keyed `selection`.

## 1. Specific sources

| Template | Source | Level | Cartesian function, at original parameters | Target | Math block row counts |
|---|---|---|---|---|---|
| z_mixed | q-95047 / 17592186125248 | easy | xy+y²z+xz² | z | 2,1,1 |
| z_square_cross | q-95171 / 17592186360581 | easy | x²z²+x²y²+xyz | z | 2,1,2 |
| z_single | q-95174 / 17592186360583 | easy | 2x²+y²+4x²z² | z | 2,1,1 |
| z_square_linear | q-165284 / 17592186367921 | easy | y²z²+xz | z | 2,1,1 |
| theta_cancellation | q-94770 / 17592186125243 | moderate | x²+y²+2yz | theta | 2,1,2,3 |
| theta_linear | q-95172 / 17592186360582 | moderate | 2y−xz | theta | 2,1,2,2 |
| r_cubic | q-95173 / 17592186368892 | moderate | x³z⁴+y³z² | r | 2,1,2,2 |

The functions are polynomials in independent Cartesian coordinates, use small integer coefficients and exact trig identities after substitution, and do not require numerical evaluation. The unchanged coordinate z is independent of r/theta. Every original prompt, five-option bank and complete worked solution is preserved in source.json and shown in review.md.

## 2. Shared mathematical pattern

Write the three-coordinate chain rule using x=r cos(theta), y=r sin(theta), z=z. Reduce zero coordinate derivative contributions. Calculate the relevant Cartesian partials before substitution, then substitute complete products into cylindrical variables. Preserve the source's distribution/collection order and exact number of rows. The z cases have three mathematical blocks, and r/theta cases have four. In authored default z output, an added sentence states which coordinates are held fixed on each side before substitution.

## 3. Component accounting

The complete bank tables below account for all 35 displayed original values and their correct designations. They are parameterized expression patterns in the observed profile. The underlying authoring intent of wrong choices is underdetermined; the pattern is preserved without pretending an arbitrary algebraic formula recovers an original misconception. There are no unmapped options. p/q are variable powers in the radial implementation; its table uses observed p=4,q=2 for readable formulas.

## 4. Reusable masks and calculations

Fixed components: coordinate roles, three-term generic chain and zero-term reduction, every source prose segment, five radio options and field key, and ordered mathematical block/row sequence. Variable components: whole polynomial RHS, function labels, complete Cartesian derivatives, cylindrical substitutions, distribution terms, collected result and complete option values. Conditional stages follow the table above; no redundant substituted rows are inserted in the source linear or cubic families.

Slots are complete `$f(x,y,z)=...,$` components and entire mathematical blocks. Function labels are replaced separately in prose and derivative notation; coordinate tuples, TeX commands and variable roles are protected. Printed multiplication is explicit, including xy/xyz and products of powers. Original notation is normalized to balanced standard TeX in mathematical blocks; unchanged prose retains its captured coordinate notation. q-95172 requires the separately documented minimal chain-factor symbol repair. No fields or banks are repaired.

Observed profile recipes are the whole banks below. Authored easy profile: correct Cartesian z derivative after substitution; reverse its sign; swap x/y cylindrical substitutions; omit radial factors by substituting x=cos(theta), y=sin(theta); add an erroneous factor 2. Authored moderate/hard profile: correct two-path sum; reverse the x-path sign; retain only x path; retain only y path; omit coordinate derivative factors, using substituted F_x+F_y. Those are operation-based authored banks and are never labeled recovered source errors. No learner-facing error diagnosis is invented.

Select a whole eligible bank before construction. Derive the correct derivative first. Reject the entire tuple if any required option is nonfinite or any pair is mathematically equivalent. Never fill from a first-valid pool. Both observed and authored profiles are tested with changed signed coefficients and powers. Bounds are enforced on explicit and sampled inputs; invalid explicit inputs raise.

Classification.md documents every level separately and anchors both missing-hard families to the canonical cylindrical example, lesson route and prerequisites. Hard templates require nonzero cross coefficients, unequal square coefficients and four nonzero distributed products before collection. No spherical, inverse-transform or higher-derivative branch is introduced. Plot extraction/generator requirement is none; the preceding tutorial's plane-polar tree is not a question asset.

The mathematical fingerprint contains target and the Cartesian partials required by the method. Unused easy coefficients, names, seed, choice order and banks are excluded. Content identity hashes actual displayed prompt, fixed solution, complete bank and correct value plus version. Changing seed/order alone cannot change identity. Incidental input changes may affect content identity without inflating task counts.

Finite meaningful parameter domains at the documented bounds: z_single has 10 surviving-coefficient tasks; other easy families have 100 derivative-coefficient tuples each. Moderate templates have 100, 100 and 600 tuples, respectively. Hard angular has 2700 and hard radial 6300 tuples. These are domain counts rather than claims of global inequivalence across templates. Sampled mathematical fingerprints are reported separately in validation.json.


## Complete observed bank profiles

### z_mixed

| Original answer ID | Captured value | Parameterized expression | Designation |
|---|---|---|---|
| 50fa9289-6d41-5d28-b208-877cbdbfa6c5 | ${r}^{2}\operatorname{sin}⁡\theta +2r\operatorname{cos}⁡\theta $ | $b\cdot r^{2}\cdot \sin\theta+2\cdot c\cdot r\cdot \cos\theta$ | incorrect; original intent unresolved |
| 667d2986-4910-56e6-9ed3-8f27b9abd76f | $r\operatorname{cos}⁡\theta +2rz\operatorname{sin}⁡\theta $ | $a\cdot r\cdot \cos\theta+2\cdot c\cdot r\cdot z\cdot \sin\theta$ | incorrect; original intent unresolved |
| add72146-efe2-5a0e-abaa-a3a2463c3158 | ${r}^{2}{sin}^{2}⁡\theta +2rz\operatorname{cos}⁡\theta $ | $b\cdot r^{2}\cdot \sin^{2}\theta+2\cdot c\cdot r\cdot z\cdot \cos\theta$ | correct |
| e28e7362-9db3-53ed-accd-873077451494 | ${r}^{2}\operatorname{sin}⁡(2\theta )+r{z}^{2}\operatorname{cos}⁡\theta $ | $b\cdot r^{2}\cdot \sin(2\cdot \theta)+c\cdot r\cdot z^{2}\cdot \cos\theta$ | incorrect; original intent unresolved |
| ef656522-486e-50e0-b47a-5e62e587789f | $r\operatorname{sin}⁡\theta +{z}^{2}$ | $c\cdot z^{2}+a\cdot r\cdot \sin\theta$ | incorrect; original intent unresolved |


### z_square_cross

| Original answer ID | Captured value | Parameterized expression | Designation |
|---|---|---|---|
| 12192e9d-666e-5c58-ae9b-549a795d8bed | ${r}^{2}(2z\operatorname{cos}⁡2\theta +\frac{1}{2}{sin}^{2}⁡\theta )$ | $r^{2}\cdot (\frac{1}{2}\cdot c\cdot \sin^{2}\theta+2\cdot a\cdot z\cdot \cos(2\cdot \theta))$ | incorrect; original intent unresolved |
| 2313e01f-d71c-5200-a515-ee826a71b2c1 | $2{r}^{2}(z{cos}^{2}⁡\theta +\operatorname{sin}⁡2\theta )$ | $2\cdot r^{2}\cdot (c\cdot \sin(2\cdot \theta)+a\cdot z\cdot \cos^{2}\theta)$ | incorrect; original intent unresolved |
| 3838a62b-71f1-5444-8110-29c7f4dcb528 | $2z{cos}^{2}⁡\theta +\frac{1}{2}\operatorname{sin}⁡2\theta $ | $\frac{1}{2}\cdot c\cdot \sin(2\cdot \theta)+2\cdot a\cdot z\cdot \cos^{2}\theta$ | incorrect; original intent unresolved |
| 6d65b027-234d-52ec-b21e-4cda093023c3 | $\operatorname{cos}⁡2\theta +{r}^{2}z\operatorname{sin}⁡2\theta $ | $a\cdot \cos(2\cdot \theta)+c\cdot z\cdot r^{2}\cdot \sin(2\cdot \theta)$ | incorrect; original intent unresolved |
| a2650aa0-1dde-559a-991a-ef66b1ee74bf | ${r}^{2}(2z{cos}^{2}⁡\theta +\frac{1}{2}\operatorname{sin}⁡2\theta )$ | $r^{2}\cdot (2\cdot a\cdot z\cdot \cos^{2}\theta+\frac{1}{2}\cdot c\cdot \sin(2\cdot \theta))$ | correct |


### z_single

| Original answer ID | Captured value | Parameterized expression | Designation |
|---|---|---|---|
| 129511e1-8153-5e51-95ae-9c26ed91e829 | $8z$ | $2\cdot c\cdot z$ | incorrect; original intent unresolved |
| 22e04b8b-94b1-5f23-a25d-237f08e39a4c | $8z+{r}^{2}{cos}^{2}⁡\theta $ | $2\cdot c\cdot z+b\cdot r^{2}\cdot \cos^{2}\theta$ | incorrect; original intent unresolved |
| 8a775666-2516-5e21-bf4d-75577316d96d | $8{r}^{2}z{cos}^{2}⁡\theta $ | $2\cdot c\cdot z\cdot r^{2}\cdot \cos^{2}\theta$ | correct |
| b5f0ea0f-66cb-5c73-84ba-025ec83912b9 | $8z+{r}^{2}{sin}^{2}⁡\theta $ | $2\cdot c\cdot z+b\cdot r^{2}\cdot \sin^{2}\theta$ | incorrect; original intent unresolved |
| d256b0d6-11fb-52fc-a283-8f751fba045a | $8{r}^{2}z{sin}^{2}⁡\theta $ | $2\cdot c\cdot z\cdot r^{2}\cdot \sin^{2}\theta$ | incorrect; original intent unresolved |


### z_square_linear

| Original answer ID | Captured value | Parameterized expression | Designation |
|---|---|---|---|
| 41de3643-e918-53d1-8cb0-5b8e949652ce | $r({sin}^{2}⁡\theta +\operatorname{cos}⁡\theta )$ | $r\cdot (a\cdot \sin^{2}\theta+b\cdot \cos\theta)$ | incorrect; original intent unresolved |
| 92a45346-b02e-5a67-a6a4-d289bad3bacb | $2{r}^{2}z{sin}^{2}⁡\theta +r\operatorname{cos}⁡\theta $ | $b\cdot r\cdot \cos\theta+2\cdot a\cdot z\cdot r^{2}\cdot \sin^{2}\theta$ | correct |
| 899dd257-9509-5c24-b797-073d1ba2f7db | $2z+{r}^{2}{cos}^{2}⁡\theta $ | $2\cdot a\cdot z+b\cdot r^{2}\cdot \cos^{2}\theta$ | incorrect; original intent unresolved |
| 0e78e572-1929-583c-ac2f-64dd21622fd6 | $2{r}^{2}z{cos}^{2}⁡\theta +\operatorname{sin}⁡\theta $ | $b\cdot \sin\theta+2\cdot a\cdot z\cdot r^{2}\cdot \cos^{2}\theta$ | incorrect; original intent unresolved |
| 28a698cf-cd11-5929-8167-bd140fb45ce8 | ${r}^{2}\operatorname{cos}⁡\theta +{sin}^{2}⁡\theta $ | $a\cdot \sin^{2}\theta+b\cdot r^{2}\cdot \cos\theta$ | incorrect; original intent unresolved |


### theta_cancellation

| Original answer ID | Captured value | Parameterized expression | Designation |
|---|---|---|---|
| 30dcc952-87b3-5c50-8329-877474c9cc37 | $2rz{sin}^{2}⁡\theta $ | $b\cdot r\cdot z\cdot \sin^{2}\theta$ | incorrect; original intent unresolved |
| 7b26dce8-c86e-5f4c-be68-35bd9babb814 | ${r}^{2}\operatorname{sin}⁡2\theta -r\operatorname{cos}⁡\theta $ | $a\cdot r^{2}\cdot \sin(2\cdot \theta)-a\cdot r\cdot \cos\theta$ | incorrect; original intent unresolved |
| c4f856b1-f69a-596f-91ca-6e69e6d25660 | $2rz\operatorname{cos}⁡\theta +{r}^{2}\operatorname{sin}⁡\theta $ | $a\cdot r^{2}\cdot \sin\theta+b\cdot r\cdot z\cdot \cos\theta$ | incorrect; original intent unresolved |
| d48510a2-a1cc-5ccc-a78d-0f55b5682108 | ${r}^{2}\operatorname{sin}⁡\theta $ | $a\cdot r^{2}\cdot \sin\theta$ | incorrect; original intent unresolved |
| ede18e52-59dd-5738-903a-565892bb8bab | $2rz\operatorname{cos}⁡\theta $ | $b\cdot r\cdot z\cdot \cos\theta$ | correct |


### theta_linear

| Original answer ID | Captured value | Parameterized expression | Designation |
|---|---|---|---|
| 010406ea-8191-5e47-ac06-dceff2ff745b | $2r\operatorname{sin}⁡\theta +z\operatorname{cos}⁡\theta $ | $a\cdot r\cdot \sin\theta+b\cdot z\cdot \cos\theta$ | incorrect; original intent unresolved |
| 282feee2-ff23-53af-9799-8744c554abd6 | $z\operatorname{cos}⁡2\theta +2r{sin}^{2}⁡\theta $ | $a\cdot r\cdot \sin^{2}\theta+b\cdot z\cdot \cos(2\cdot \theta)$ | incorrect; original intent unresolved |
| 49f1c912-9ed3-5d04-8e7b-747744cb437f | $rz\operatorname{sin}⁡\theta +2r\operatorname{cos}⁡\theta $ | $b\cdot r\cdot z\cdot \sin\theta+a\cdot r\cdot \cos\theta$ | correct |
| 6830d01d-5239-5816-9b25-ca0834b037fb | $z{cos}^{2}⁡\theta +2r\operatorname{sin}⁡2\theta $ | $a\cdot r\cdot \sin(2\cdot \theta)+b\cdot z\cdot \cos^{2}\theta$ | incorrect; original intent unresolved |
| a16444c4-1302-5cfc-815a-cb0ecda9bea3 | $z{sin}^{2}⁡\theta +2r{cos}^{2}⁡\theta $ | $a\cdot r\cdot \cos^{2}\theta+b\cdot z\cdot \sin^{2}\theta$ | incorrect; original intent unresolved |


### r_cubic

| Original answer ID | Captured value | Parameterized expression | Designation |
|---|---|---|---|
| d7772675-d258-5d51-b29d-b3396a5e5001 | $3{r}^{2}({z}^{2}{cos}^{2}⁡\theta +{sin}^{2}⁡\theta )$ | $3\cdot r^{2}\cdot (b\cdot \sin^{2}\theta+a\cdot z^{2}\cdot \cos^{2}\theta)$ | incorrect; original intent unresolved |
| 2c7da375-0431-5f66-8543-0491e4f293c9 | $3{r}^{2}{z}^{2}(\operatorname{cos}⁡3\theta +\operatorname{sin}⁡3\theta )$ | $3\cdot r^{2}\cdot z^{2}\cdot (a\cdot \cos(3\cdot \theta)+b\cdot \sin(3\cdot \theta))$ | incorrect; original intent unresolved |
| 43eedeea-a30d-5b9a-ba7b-6945237b5a90 | ${z}^{2}{cos}^{3}⁡\theta +{sin}^{3}⁡\theta $ | $b\cdot \sin^{3}\theta+a\cdot z^{2}\cdot \cos^{3}\theta$ | incorrect; original intent unresolved |
| b844a28f-f811-5210-9c5f-949a6a5243b2 | ${r}^{2}z({z}^{3}{cos}^{3}⁡\theta +z{sin}^{3}⁡\theta )$ | $z\cdot r^{2}\cdot (a\cdot z^{3}\cdot \cos^{3}\theta+b\cdot z\cdot \sin^{3}\theta)$ | incorrect; original intent unresolved |
| eab23144-3264-5367-8737-fc9bde1fca89 | $3{r}^{2}{z}^{2}({z}^{2}{cos}^{3}⁡\theta +{sin}^{3}⁡\theta )$ | $3\cdot r^{2}\cdot z^{2}\cdot (a\cdot z^{2}\cdot \cos^{3}\theta+b\cdot \sin^{3}\theta)$ | correct |

