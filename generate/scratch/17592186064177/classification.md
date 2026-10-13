# Classification and extraction

Math basis 1953, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The complete scoped Pull is retained in reference/initial/kp.edn and source.json; native inventory is retained at the same initial basis. No generator or supplied .generated file existed. Canonical example e-381 supports sum and exponential rules, and never counts as practice. All source text was read; no prompt, bank, or solution contains a plot asset. Plot extraction and generation therefore require no new plots.

Easy has one two-exponential Markdown/value family with two different source order/format layouts and two separately retained bank profiles. Moderate has three mathematical families (added power, constant, reciprocal), four Markdown/value templates and four banks. All complete fields are selection/radio with five mathematical choices. Two undefined-function blanks are separately documented as unsupported incomplete sources. Hard has no source templates. The narrow generator preserves all six supported source layouts separately.

## q-31311

Source database entity 17592186064733; difficulty unrated.

What is $\displaystyle \int(2^{x} - 10e^{x})dx$?

Excluded from generation and available inventory: q-31311 and q-51102 are unrated and lack correct designations and solutions; q-31261 has no answer fields; q-167332 and q-167786 have undefined f and g in their prompts and duplicate one solution. Preserved, excluded from inventory, never silently repaired. Full original fields, choices, and solution remain in source.json.

## q-51102

Source database entity 17592186064889; difficulty unrated.

What is $\displaystyle \int(2e^{x} + 4^{x} - 2x)dx$?

Excluded from generation and available inventory: q-31311 and q-51102 are unrated and lack correct designations and solutions; q-31261 has no answer fields; q-167332 and q-167786 have undefined f and g in their prompts and duplicate one solution. Preserved, excluded from inventory, never silently repaired. Full original fields, choices, and solution remain in source.json.

## q-31261

Source database entity 17592186233778; difficulty :question.difficulty/moderate.

$\int ({e}^{x}+{8}^{x}+\frac{3}{x})\,\text{d}x=$

Excluded from generation and available inventory: q-31311 and q-51102 are unrated and lack correct designations and solutions; q-31261 has no answer fields; q-167332 and q-167786 have undefined f and g in their prompts and duplicate one solution. Preserved, excluded from inventory, never silently repaired. Full original fields, choices, and solution remain in source.json.

## q-167332

Source database entity 17592186235436; difficulty :question.difficulty/moderate.

$\int (4f(x)+3g(x))\,\text{d}x\,=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$+\,C,\,$ where $C$ is an arbitrary constant.

Excluded from generation and available inventory: q-31311 and q-51102 are unrated and lack correct designations and solutions; q-31261 has no answer fields; q-167332 and q-167786 have undefined f and g in their prompts and duplicate one solution. Preserved, excluded from inventory, never silently repaired. Full original fields, choices, and solution remain in source.json.

## q-167786

Source database entity 17592186235485; difficulty :question.difficulty/moderate.

$\int (4f(x)+3g(x))\,\text{d}x\,=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$+C,\,$ where $C$ is an arbitrary constant.

Excluded from generation and available inventory: q-31311 and q-51102 are unrated and lack correct designations and solutions; q-31261 has no answer fields; q-167332 and q-167786 have undefined f and g in their prompts and duplicate one solution. Preserved, excluded from inventory, never silently repaired. Full original fields, choices, and solution remain in source.json.

## q-2277

Source database entity 17592186290437; difficulty :question.difficulty/easy.

$\int (5{e}^{x}+{2}^{x})\,\text{d}x=$

Shared pattern: integrate a sum term by term using constant multiples and the exponential rule; the moderate profiles additionally integrate the exact source power, constant, or reciprocal term. Field selection expects the complete primitive with C. Domain: all real x for nonreciprocal prompts; x != 0 for reciprocal prompts. Distractors with logarithms in x have their own restricted formula domains and are not global antiderivatives.

Observed base 2. Proposed base bounds 2..12 retain every observed base. Vary only the positive nonunit exponential base, its matched logarithm, and the explicitly mapped e-exponent in q-31254/q-31260. All other literals and polynomial exponents stay fixed. Wrong-choice expressions are observed parameterized patterns; psychological interpretations unresolved. Plot rating: none. Generalized prompt, solution, and complete bank are the explicit slots in templates.json. The fixed step sequence separates the sum, integrates each term, and adds C; no pedagogical prose changes.

- Field selection, original answer UUID 39f1030c-14e2-59e9-a189-ae72636d7cec; incorrect; exact value `2{e}^{x}+\frac{{5}^{x}}{ln⁡2}+C`; parameterized recipe `2{e}^{x}+\frac{{5}^{x}}{ln⁡@@B@@}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 831fe1aa-d1a9-59de-914e-66c8e45135cf; incorrect; exact value `5{e}^{x}+{2}^{x}ln⁡2+C`; parameterized recipe `5{e}^{x}+{@@B@@}^{x}ln⁡@@B@@+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID a92a1f84-319a-5ffc-912d-da344601d75d; incorrect; exact value `\frac{{e}^{x}}{5}+\frac{{2}^{x}}{ln⁡2}+C`; parameterized recipe `\frac{{e}^{x}}{5}+\frac{{@@B@@}^{x}}{ln⁡@@B@@}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID bfec5a66-eb21-510f-ac20-724d2da23f30; incorrect; exact value `5{e}^{x}+\frac{x}{ln⁡2}+C`; parameterized recipe `5{e}^{x}+\frac{x}{ln⁡@@B@@}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID f611671a-7317-5307-aefb-d9046cadfb32; correct; exact value `5{e}^{x}+\frac{{2}^{x}}{ln⁡2}+C`; parameterized recipe `5{e}^{x}+\frac{{@@B@@}^{x}}{ln⁡@@B@@}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

Worked solution (frozen wording and complete source sequence):

Here, we combine the sum rule and our exponential rules to get

$$
\begin{aligned}\begin{aligned}\int (5{e}^{x}+{2}^{x})\,\text{d}x & =5\int {e}^{x}\,\text{d}x+\int {2}^{x}\,\text{d}x \\  & =5{e}^{x}+\frac{{2}^{x}}{ln⁡2}+C.\end{aligned}\end{aligned}
$$

## q-2281

Source database entity 17592186290438; difficulty :question.difficulty/easy.

$\int ({9}^{x}+3{e}^{x})\,\text{d}x=$

Shared pattern: integrate a sum term by term using constant multiples and the exponential rule; the moderate profiles additionally integrate the exact source power, constant, or reciprocal term. Field selection expects the complete primitive with C. Domain: all real x for nonreciprocal prompts; x != 0 for reciprocal prompts. Distractors with logarithms in x have their own restricted formula domains and are not global antiderivatives.

Observed base 9. Proposed base bounds 2..12 retain every observed base. Vary only the positive nonunit exponential base, its matched logarithm, and the explicitly mapped e-exponent in q-31254/q-31260. All other literals and polynomial exponents stay fixed. Wrong-choice expressions are observed parameterized patterns; psychological interpretations unresolved. Plot rating: none. Generalized prompt, solution, and complete bank are the explicit slots in templates.json. The fixed step sequence separates the sum, integrates each term, and adds C; no pedagogical prose changes.

- Field selection, original answer UUID 25701e43-e3df-5d1e-8ac3-09bcc9dcf7bb; correct; exact value `\frac{{9}^{x}}{\operatorname{ln}⁡9}+3{e}^{x}+C`; parameterized recipe `\frac{{@@B@@}^{x}}{\operatorname{ln}⁡@@B@@}+3{e}^{x}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 5a21abb6-314e-594e-906a-fc211f164a2f; incorrect; exact value `\frac{\operatorname{ln}⁡9}{{9}^{x}}+{e}^{x}+C`; parameterized recipe `\frac{\operatorname{ln}⁡@@B@@}{{@@B@@}^{x}}+{e}^{x}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID ce26c9e7-48dc-50a0-bce8-7f40380eb504; incorrect; exact value `\frac{{x}^{9}}{\operatorname{ln}⁡9}-3{e}^{x}+C`; parameterized recipe `\frac{{x}^{9}}{\operatorname{ln}⁡@@B@@}-3{e}^{x}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID d1df1022-beed-5ec0-bcb0-27462f2a142b; incorrect; exact value `\frac{9}{\operatorname{ln}⁡x}+{e}^{3x}+C`; parameterized recipe `\frac{9}{\operatorname{ln}⁡x}+{e}^{3x}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID d501df4f-3f69-522d-8918-2f3e4ab83e19; incorrect; exact value `\frac{x}{\operatorname{ln}⁡9}-3{e}^{x}+C`; parameterized recipe `\frac{x}{\operatorname{ln}⁡@@B@@}-3{e}^{x}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

Worked solution (frozen wording and complete source sequence):

Here, we combine the sum rule and our exponential rules to get

$$
\begin{aligned}\begin{aligned}\int ({9}^{x}+3{e}^{x})\,\text{d}x & =\int {9}^{x}\,\text{d}x+3\int {e}^{x}\,\text{d}x \\  & =\frac{{9}^{x}}{\operatorname{ln}⁡9}+3{e}^{x}+C.\end{aligned}\end{aligned}
$$

## q-31252

Source database entity 17592186297342; difficulty :question.difficulty/moderate.

$\int (2{e}^{x}-{3}^{x}+{x}^{2})\,\text{d}x=$

Shared pattern: integrate a sum term by term using constant multiples and the exponential rule; the moderate profiles additionally integrate the exact source power, constant, or reciprocal term. Field selection expects the complete primitive with C. Domain: all real x for nonreciprocal prompts; x != 0 for reciprocal prompts. Distractors with logarithms in x have their own restricted formula domains and are not global antiderivatives.

Observed base 3. Proposed base bounds 2..12 retain every observed base. Vary only the positive nonunit exponential base, its matched logarithm, and the explicitly mapped e-exponent in q-31254/q-31260. All other literals and polynomial exponents stay fixed. Wrong-choice expressions are observed parameterized patterns; psychological interpretations unresolved. Plot rating: none. Generalized prompt, solution, and complete bank are the explicit slots in templates.json. The fixed step sequence separates the sum, integrates each term, and adds C; no pedagogical prose changes.

- Field selection, original answer UUID 1ddda862-700e-5259-8a9b-324825fe885d; incorrect; exact value `{e}^{x}+\frac{{3}^{x}}{ln⁡2}+\frac{{x}^{2}}{3}+C`; parameterized recipe `{e}^{x}+\frac{{@@B@@}^{x}}{ln⁡2}+\frac{{x}^{2}}{3}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 3b3aafd2-10f8-5647-aeef-217f0b123766; correct; exact value `2{e}^{x}-\frac{{3}^{x}}{ln⁡3}+\frac{{x}^{3}}{3}+C`; parameterized recipe `2{e}^{x}-\frac{{@@B@@}^{x}}{ln⁡@@B@@}+\frac{{x}^{3}}{3}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 4aaae1a6-c031-5bc5-a104-23401003f961; incorrect; exact value `\frac{{3}^{x}}{ln⁡3}+{x}^{2}+{e}^{x}+C`; parameterized recipe `\frac{{@@B@@}^{x}}{ln⁡@@B@@}+{x}^{2}+{e}^{x}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 531024e5-c103-583c-92eb-e4200ac7a6df; incorrect; exact value `2{e}^{3x}-\frac{{3}^{2x}}{ln⁡x}+\frac{{x}^{2}}{2}+C`; parameterized recipe `2{e}^{3x}-\frac{{@@B@@}^{2x}}{ln⁡x}+\frac{{x}^{2}}{2}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 56637843-7c20-5243-80d5-7c1405ee9de3; incorrect; exact value `\frac{{2}^{x}}{ln⁡2}+\frac{{x}^{2}}{2}-3{e}^{x}+C`; parameterized recipe `\frac{{2}^{x}}{ln⁡2}+\frac{{x}^{2}}{2}-3{e}^{x}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

Worked solution (frozen wording and complete source sequence):

Here, we combine the sum rule and our exponential rules to get

$$
\begin{aligned}\int (2{e}^{x}-{3}^{x}+{x}^{2})\,\text{d}x & =2\int {e}^{x}\,\text{d}x-\int {3}^{x}\,\text{d}x+\int {x}^{2}\,\text{d}x \\  & =2{e}^{x}-\frac{{3}^{x}}{ln⁡3}+\frac{{x}^{3}}{3}+C.\end{aligned}
$$

## q-31254

Source database entity 17592186297344; difficulty :question.difficulty/moderate.

$\int ({5}^{x}-2{e}^{x}+2)\,\text{d}x=$

Shared pattern: integrate a sum term by term using constant multiples and the exponential rule; the moderate profiles additionally integrate the exact source power, constant, or reciprocal term. Field selection expects the complete primitive with C. Domain: all real x for nonreciprocal prompts; x != 0 for reciprocal prompts. Distractors with logarithms in x have their own restricted formula domains and are not global antiderivatives.

Observed base 5. Proposed base bounds 2..12 retain every observed base. Vary only the positive nonunit exponential base, its matched logarithm, and the explicitly mapped e-exponent in q-31254/q-31260. All other literals and polynomial exponents stay fixed. Wrong-choice expressions are observed parameterized patterns; psychological interpretations unresolved. Plot rating: none. Generalized prompt, solution, and complete bank are the explicit slots in templates.json. The fixed step sequence separates the sum, integrates each term, and adds C; no pedagogical prose changes.

- Field selection, original answer UUID 49d14480-6ea8-53a7-8d9d-e4372b3c13d1; incorrect; exact value `\frac{{2}^{x}}{ln⁡|x|}-{e}^{2x}+x+C`; parameterized recipe `\frac{{2}^{x}}{ln⁡|x|}-{e}^{2x}+x+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 4b209e11-101c-567a-969b-9f779fc2d1b3; incorrect; exact value `2\frac{{e}^{5x}}{ln⁡5}-{e}^{x}+2x+C`; parameterized recipe `2\frac{{e}^{@@B@@x}}{ln⁡@@B@@}-{e}^{x}+2x+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID a3afa67c-3743-529b-80a1-f481ffdb27cf; incorrect; exact value `\frac{{5}^{3x}}{ln⁡x}+2{e}^{2x}+{x}^{2}+C`; parameterized recipe `\frac{{@@B@@}^{3x}}{ln⁡x}+2{e}^{2x}+{x}^{2}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID b65d0920-ff23-58e4-bde5-060a3ca311cf; incorrect; exact value `\frac{{e}^{3x}}{ln⁡5}+2{e}^{x}+x+C`; parameterized recipe `\frac{{e}^{3x}}{ln⁡@@B@@}+2{e}^{x}+x+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID fcd1d280-28cc-5226-a0a1-cc64b4710f4b; correct; exact value `\frac{{5}^{x}}{ln⁡5}-2{e}^{x}+2x+C`; parameterized recipe `\frac{{@@B@@}^{x}}{ln⁡@@B@@}-2{e}^{x}+2x+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

Worked solution (frozen wording and complete source sequence):

Here, we combine the sum rule and our exponential rules to get

$$
\begin{aligned}\int ({5}^{x}-2{e}^{x}+2)\,\text{d}x & =\int {5}^{x}\,\text{d}x-2\int {e}^{x}\,\text{d}x+\int 2\,\text{d}x \\  & =\frac{{5}^{x}}{ln⁡5}-2{e}^{x}+2x+C.\end{aligned}
$$

## q-31256

Source database entity 17592186297347; difficulty :question.difficulty/moderate.

$\int (-2{e}^{x}+{4}^{x}+\frac{1}{x})\,\text{d}x=$

Shared pattern: integrate a sum term by term using constant multiples and the exponential rule; the moderate profiles additionally integrate the exact source power, constant, or reciprocal term. Field selection expects the complete primitive with C. Domain: all real x for nonreciprocal prompts; x != 0 for reciprocal prompts. Distractors with logarithms in x have their own restricted formula domains and are not global antiderivatives.

Observed base 4. Proposed base bounds 2..12 retain every observed base. Vary only the positive nonunit exponential base, its matched logarithm, and the explicitly mapped e-exponent in q-31254/q-31260. All other literals and polynomial exponents stay fixed. Wrong-choice expressions are observed parameterized patterns; psychological interpretations unresolved. Plot rating: none. Generalized prompt, solution, and complete bank are the explicit slots in templates.json. The fixed step sequence separates the sum, integrates each term, and adds C; no pedagogical prose changes.

- Field selection, original answer UUID 585614dd-9ea9-5784-93b4-6914d0f259e1; correct; exact value `-2{e}^{x}+\frac{{4}^{x}}{ln⁡4}+ln⁡|x|+C`; parameterized recipe `-2{e}^{x}+\frac{{@@B@@}^{x}}{ln⁡@@B@@}+ln⁡|x|+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 81771957-0036-5c33-bdc4-df04751e4fa7; incorrect; exact value `-\frac{2}{{e}^{x}}+\frac{{2}^{x}}{ln⁡4}+3ln⁡|x|+C`; parameterized recipe `-\frac{2}{{e}^{x}}+\frac{{2}^{x}}{ln⁡@@B@@}+3ln⁡|x|+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 8598c747-3949-5f9e-8cb4-3d148fb0cdb1; incorrect; exact value `\frac{{e}^{x}}{2}+\frac{x}{ln⁡4}+3ln⁡|x|+C`; parameterized recipe `\frac{{e}^{x}}{2}+\frac{x}{ln⁡@@B@@}+3ln⁡|x|+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID aed107ef-e155-5c3a-86cd-e0c4ddc3690a; incorrect; exact value `{e}^{-2x}+\frac{{4}^{x}}{ln⁡|x|}+4ln⁡|x|+C`; parameterized recipe `{e}^{-2x}+\frac{{@@B@@}^{x}}{ln⁡|x|}+4ln⁡|x|+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID b9377cb5-4f12-5d35-bfa2-ab4190b617d1; incorrect; exact value `-{e}^{x}+\frac{{4}^{4x}}{ln⁡2}+2ln⁡|x|+C`; parameterized recipe `-{e}^{x}+\frac{{@@B@@}^{4x}}{ln⁡2}+2ln⁡|x|+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

Worked solution (frozen wording and complete source sequence):

Here, we combine the sum rule and our exponential rules to get

$$
\begin{aligned}\int (-2{e}^{x}+{4}^{x}+\frac{1}{x})\,\text{d}x & =-2\int {e}^{x}\,\text{d}x+\int {4}^{x}\,\text{d}x+\int \frac{1}{x}\,\text{d}x \\  & =-2{e}^{x}+\frac{{4}^{x}}{ln⁡4}+ln⁡|x|+C.\end{aligned}
$$

## q-31260

Source database entity 17592186297358; difficulty :question.difficulty/moderate.

$\int (2\cdot {5}^{x}-{e}^{x}+{x}^{3})\,\text{d}x=$

Shared pattern: integrate a sum term by term using constant multiples and the exponential rule; the moderate profiles additionally integrate the exact source power, constant, or reciprocal term. Field selection expects the complete primitive with C. Domain: all real x for nonreciprocal prompts; x != 0 for reciprocal prompts. Distractors with logarithms in x have their own restricted formula domains and are not global antiderivatives.

Observed base 5. Proposed base bounds 2..12 retain every observed base. Vary only the positive nonunit exponential base, its matched logarithm, and the explicitly mapped e-exponent in q-31254/q-31260. All other literals and polynomial exponents stay fixed. Wrong-choice expressions are observed parameterized patterns; psychological interpretations unresolved. Plot rating: none. Generalized prompt, solution, and complete bank are the explicit slots in templates.json. The fixed step sequence separates the sum, integrates each term, and adds C; no pedagogical prose changes.

- Field selection, original answer UUID 03eaae83-aa97-5d62-99ec-86500aa38887; incorrect; exact value `2\cdot \frac{x}{ln⁡5}+{e}^{x}+\frac{{x}^{3}}{3}+C`; parameterized recipe `2\cdot \frac{x}{ln⁡@@B@@}+{e}^{x}+\frac{{x}^{3}}{3}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 19e3e8af-7108-5d2e-854f-5d3554910a1e; incorrect; exact value `5\cdot \frac{{5}^{x}}{ln⁡5}+{e}^{x}+\frac{{x}^{3}}{2}+C`; parameterized recipe `5\cdot \frac{{@@B@@}^{x}}{ln⁡@@B@@}+{e}^{x}+\frac{{x}^{3}}{2}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID 8ef143b8-e3a9-5d16-af8b-ddc53392af90; incorrect; exact value `2\cdot \frac{{5}^{x}}{ln⁡|x|}-2{e}^{x}+\frac{{x}^{4}}{4}+C`; parameterized recipe `2\cdot \frac{{@@B@@}^{x}}{ln⁡|x|}-2{e}^{x}+\frac{{x}^{4}}{4}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID b91478a3-d7d5-51a3-b0f5-b450152d8c28; incorrect; exact value `\frac{{5}^{x}}{ln⁡5}-{e}^{5x}+\frac{{x}^{3}}{3}+C`; parameterized recipe `\frac{{@@B@@}^{x}}{ln⁡@@B@@}-{e}^{@@B@@x}+\frac{{x}^{3}}{3}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

- Field selection, original answer UUID be5397f5-2ec4-53e9-a9c8-ea1bdd02f904; correct; exact value `2\cdot \frac{{5}^{x}}{ln⁡5}-{e}^{x}+\frac{{x}^{4}}{4}+C`; parameterized recipe `2\cdot \frac{{@@B@@}^{x}}{ln⁡@@B@@}-{e}^{x}+\frac{{x}^{4}}{4}+C`. Recipe reproduces the complete original value exactly at the observed base. Observed expression pattern retained; cognitive error interpretation unresolved.

Worked solution (frozen wording and complete source sequence):

Here, we combine the sum rule and our exponential rules to get

$$
\begin{aligned}\int (2\cdot {5}^{x}-{e}^{x}+{x}^{3})\,\text{d}x & =2\int {5}^{x}\,\text{d}x-\int {e}^{x}\,\text{d}x+\int {x}^{3}\,\text{d}x \\  & =2\cdot \frac{{5}^{x}}{ln⁡5}-{e}^{x}+\frac{{x}^{4}}{4}+C.\end{aligned}
$$

## Validation and database scope

Validation tests all 66 allowed instances, full bank replay (30/30 values, 24/24 distractors, 6/6 banks), every rendered solution step on positive and negative x intervals, unique correct primitives modulo constants, deterministic identities, parameter boundaries, corruption controls, and every choice through the actual learner grader. Side-by-side originals and changed bases are in review.md. Fidelity, symbolic correctness and native grading are reported separately in validation.json.

Replenishment uses the existing Database integration, configured application/ca-engine contributor and native validation specs. It acquires api.lock, rechecks current inventory and basis, excludes presentations and reservations (including retained history), and deduplicates exact integrands across sources and generated content. Exact requests, preview, receipt, datom scope checks and exact db_after readback are retained in reference/replenishment. Only additive new questions and this KP generator registration are authorized. Source and learner history remain untouched. Bounded hard support remains short by five; it is never called filled.
