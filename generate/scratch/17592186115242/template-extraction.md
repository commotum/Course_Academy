# Template extraction: four stages

Snapshot provenance is retained unchanged in source.json. Recipes are arithmetic patterns, not a reconstruction of proprietary authoring code. No scalar bank is promoted to normal default solely because it matches an isolated source.

## 1. Specific source descriptions

All systems use real x,y and a real parameter k; no determinants, eigenvalues, additional unknowns or higher-degree parameter branches are introduced. Exact integers/fractions are retained.

### q-32246

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 3x+4y=12 \\  & x+ky=4\end{aligned}
$$

Source database ID 17592186115753; observed hard; template `dependent_swap`; parameters `{'a': 3, 'b': 4, 'c': 12, 'd': 1, 'u': 1, 'v': 0, 'e': 4}`. Row swap: True; row-operation notation: plus_parenthesized. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a swapped matrix plus second operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-42059

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & 2x+3y=1 \\  & 6x+(k+3)y=-5\end{aligned}
$$

Source database ID 17592186115831; observed moderate; template `inconsistent_shift`; parameters `{'a': 2, 'b': 3, 'c': 1, 'd': 6, 'u': 1, 'v': 3, 'e': -5}`. Row swap: False; row-operation notation: plus_parenthesized. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-131726

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned} & -3x+2y=1 \\  & 6x+(k+9)y=5\end{aligned}
$$

Source database ID 17592186266116; observed moderate; template `inconsistent_shift`; parameters `{'a': -3, 'b': 2, 'c': 1, 'd': 6, 'u': 1, 'v': 9, 'e': 5}`. Row swap: False; row-operation notation: plus. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-131727

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned} & x-3y=-1 \\  & 4x+3ky=3\end{aligned}
$$

Source database ID 17592186266117; observed moderate; template `inconsistent_scaled`; parameters `{'a': 1, 'b': -3, 'c': -1, 'd': 4, 'u': 3, 'v': 0, 'e': 3}`. Row swap: False; row-operation notation: subtract. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-131728

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned} & -x+4y=-2 \\  & -3x+(3k+15)y=-4\end{aligned}
$$

Source database ID 17592186266118; observed moderate; template `inconsistent_scaled_shift`; parameters `{'a': -1, 'b': 4, 'c': -2, 'd': -3, 'u': 3, 'v': 15, 'e': -4}`. Row swap: False; row-operation notation: subtract. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-131729

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
{\begin{aligned} & -2x+7y=6 \\  & x+ky=-3\end{aligned}
$$

Source database ID 17592186266119; observed hard; template `dependent_swap`; parameters `{'a': -2, 'b': 7, 'c': 6, 'd': 1, 'u': 1, 'v': 0, 'e': -3}`. Row swap: True; row-operation notation: plus. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a swapped matrix plus second operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-131731

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
{\begin{aligned} & -2x+6y=-4 \\  & 5x+(k-6)y=10\end{aligned}
$$

Source database ID 17592186266120; observed hard; template `dependent_fractional`; parameters `{'a': -2, 'b': 6, 'c': -4, 'd': 5, 'u': 1, 'v': -6, 'e': 10}`. Row swap: False; row-operation notation: plus. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-32245

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & 2x-y=3 \\  & 4x+ky=4\end{aligned}
$$

Source database ID 17592186302109; observed moderate; template `inconsistent_bare`; parameters `{'a': 2, 'b': -1, 'c': 3, 'd': 4, 'u': 1, 'v': 0, 'e': 4}`. Row swap: False; row-operation notation: plus_parenthesized. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-32331

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned}-4x-y=2 \\ 8x+ky=5\end{aligned}
$$

Source database ID 17592186302143; observed moderate; template `inconsistent_bare`; parameters `{'a': -4, 'b': -1, 'c': 2, 'd': 8, 'u': 1, 'v': 0, 'e': 5}`. Row swap: False; row-operation notation: plus. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-74646

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned} & x+4y=2 \\  & 2x+(k+1)y=3\end{aligned}
$$

Source database ID 17592186344961; observed moderate; template `inconsistent_shift`; parameters `{'a': 1, 'b': 4, 'c': 2, 'd': 2, 'u': 1, 'v': 1, 'e': 3}`. Row swap: False; row-operation notation: plus_parenthesized. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-74688

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned} & x+2y=-4 \\  & 3x+2ky=-2\end{aligned}
$$

Source database ID 17592186344969; observed moderate; template `inconsistent_scaled`; parameters `{'a': 1, 'b': 2, 'c': -4, 'd': 3, 'u': 2, 'v': 0, 'e': -2}`. Row swap: False; row-operation notation: plus_parenthesized. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-74695

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
{\begin{aligned} & 4x+2y=-8 \\  & x+ky=-2\end{aligned}
$$

Source database ID 17592186344971; observed hard; template `dependent_swap`; parameters `{'a': 4, 'b': 2, 'c': -8, 'd': 1, 'u': 1, 'v': 0, 'e': -2}`. Row swap: True; row-operation notation: plus_parenthesized. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a swapped matrix plus second operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-74650

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
{\begin{aligned} & 2x+6y=4 \\  & x+(k+1)y=2\end{aligned}
$$

Source database ID 17592186398982; observed hard; template `dependent_fractional`; parameters `{'a': 2, 'b': 6, 'c': 4, 'd': 1, 'u': 1, 'v': 1, 'e': 2}`. Row swap: False; row-operation notation: plus_parenthesized. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-131730

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
{\begin{aligned} & 3x+2y=12 \\  & x+ky=4\end{aligned}
$$

Source database ID 17592186417082; observed hard; template `dependent_swap`; parameters `{'a': 3, 'b': 2, 'c': 12, 'd': 1, 'u': 1, 'v': 0, 'e': 4}`. Row swap: True; row-operation notation: subtract. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a swapped matrix plus second operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

### q-42021

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned}x+2y=3 \\ -3x-(k+1)y=-9\end{aligned}
$$

Source database ID 17592186425949; observed hard; template `dependent_negative`; parameters `{'a': 1, 'b': 2, 'c': 3, 'd': -3, 'u': -1, 'v': -1, 'e': -9}`. Row swap: False; row-operation notation: plus. The worked sequence has an initial augmented matrix, repeated initial matrix plus operation, a row-echelon matrix, corresponding two equations, classification rationale, special k value, and concluding sentence. Hard sources also remove the zero equation and identify basic x/free y.

## 2. Shared mathematical description

For a x+b y=c and d x+(u k+v)y=e, eliminate x. The second row is [0,u k+v-(d/a)b,e-(d/a)c], except the swap family first places the unit second row above the first and produces [0,b-a k,c-a e]. The parameter makes the remaining y coefficient zero: k=((d/a)b-v)/u. A nonzero residual yields inconsistency; zero residual yields one equation in two variables and dependence. The response is always the complete equation k=value. Fixed teaching prose follows each original with a single solution independent of the selected option.

## 3. Components and complete banks

Each source field is radio `selection`. Correct value is computed from the prompt before constructing the complete bank. In the tables r=d/a, t=((d/a)b-v)/u, h=e-r c. Expression-pattern intent is explicitly unresolved for opaque offsets; these are observed replay profiles only, never authored default recipes. Complete numeric reproduction alone is not an error-model claim.

### Bank q-32246

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 3248af5c-24d6-51a0-a62b-8d5ab0e0e782 | `k=0` | `k=0` | False |

| selection | 5ed5f31b-5757-56ca-ac90-622019b8d7e7 | `k=\frac{4}{3}` | `k=t` | True |

| selection | 6b3ca3f5-57b3-5b3c-b6b4-0772e9be135c | `k=\frac{3}{4}` | `k=1/t` | False |

| selection | 6f2681ec-b8ae-51dc-9094-2e2bcadf6d8a | `k=-4` | `k=-b` | False |

| selection | fad186f0-c1c8-5bcc-8cc3-09b1f4f1ed49 | `k=-\frac{4}{3}` | `k=-t` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-42059

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 359439f2-81e1-5ced-8482-b2cf08a71409 | `k=9` | `k=r*b` | False |

| selection | 478b28da-a8a3-51e4-963d-8ac53adc010e | `k=6` | `k=t` | True |

| selection | 545c0eb7-c35a-5d44-b8e2-b045ff203715 | `k=4` | `k=t-2` | False |

| selection | 684ddf9d-dd44-5397-b1a8-e6e3ca6a2f95 | `k=-2` | `k=-a` | False |

| selection | 9720657d-4e06-51f7-8e91-da074201b940 | `k=7` | `k=t+1` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-131726

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 188d8234-d927-5fa4-9649-52a3600a14ed | `k=-13` | `k=t` | True |

| selection | 59917889-7526-5cea-90f8-6ed9b5d31888 | `k=8` | `k=h+1` | False |

| selection | 84ec393a-992f-55d2-9044-1e362627ed1c | `k=-12` | `k=t+1` | False |

| selection | 9556b060-0b9f-5486-b05c-79753916db1d | `k=7` | `k=h` | False |

| selection | c483c739-bc7d-5f47-8dbf-09da12b3a0b2 | `k=-14` | `k=t-1` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-131727

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 2a4e76fd-e1c6-5cbe-93b0-49387b6d03cd | `k=-13` | `k=t-9` | False |

| selection | c2f1c78c-35e7-5dc3-a4ea-917746946f9c | `k=7` | `k=h` | False |

| selection | cad2e0cc-59d8-5847-8c17-7f7022f7428b | `k=-3` | `k=t+1` | False |

| selection | ddd34857-39b4-5a84-88c6-46284b56c129 | `k=-12` | `k=r*b` | False |

| selection | f74d0318-2803-55b8-bb5b-49c8150dea17 | `k=-4` | `k=t` | True |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-131728

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 8e3a6e2e-1b7a-5ad1-b366-2deecae63253 | `k=1` | `k=-t` | False |

| selection | 96b3aa58-5c89-5f3c-896e-547bdfeef87c | `k=-1` | `k=t` | True |

| selection | 9c0fed83-26f2-58cf-9e61-edca1345442b | `k=-2` | `k=t-1` | False |

| selection | bedfa238-a1cb-50f4-b26d-08ac9994d923 | `k=0` | `k=0` | False |

| selection | cffb3874-d3c5-58d9-9efc-875fe9730f23 | `k=2` | `k=-2*t` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-131729

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 427da7e5-15ac-51bd-a759-d90b6c65d454 | `k=-\frac{2}{7}` | `k=1/t` | False |

| selection | 538a47b2-6a0b-5a53-99e0-b4e09df09626 | `k=-7` | `k=-b` | False |

| selection | 7f383d71-c4b1-501b-823d-dfdddaac22d3 | `k=\frac{7}{2}` | `k=-t` | False |

| selection | b60949ed-65e4-5904-90e9-755392f2794a | `k=-\frac{7}{2}` | `k=t` | True |

| selection | d7266032-5cfb-59d1-b694-4b3ac335232b | `k=0` | `k=0` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-131731

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 5280ce29-a009-5d89-b11c-32a91956f88d | `k=-9` | `k=t` | True |

| selection | a8cf5fce-3112-5b03-8cf3-0d4a08494133 | `k=-6` | `k=v` | False |

| selection | bac8e055-43dd-52ec-b2ee-c1af2bc589d4 | `k=0` | `k=0` | False |

| selection | bf50ed27-034a-525d-8d4e-b76acf4ead2d | `k=9` | `k=-t` | False |

| selection | d2c3e1a0-f525-5859-8a97-2dbc90d7ad24 | `k=-12` | `k=t-3` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-32245

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 9eefeb35-a93a-5693-8a54-a335560cde62 | `k=0` | `k=0` | False |

| selection | a14a43e5-9b21-562f-aaa1-5f805da32173 | `k=-4` | `k=2*t` | False |

| selection | a2621a0b-e192-593d-b62d-8165fb69e7a9 | `k=2` | `k=-t` | False |

| selection | b3d7fb16-c926-51ed-a5b0-cbfd28c2fab5 | `k=-2` | `k=t` | True |

| selection | f15a5a0a-88a7-5b7b-9e41-9d091c25e2a8 | `k=4` | `k=-2*t` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-32331

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 39edf270-ef24-52e6-8a06-10a72874478d | `k=2` | `k=t` | True |

| selection | 441122b0-3b95-5e4c-ad49-ebd17ab5fd1b | `k=0` | `k=0` | False |

| selection | 7951ba97-6d77-594c-84f6-7b1ce6a00426 | `k=-5` | `k=-e` | False |

| selection | 8713309c-6e3b-5cbf-9236-a21b2e8d5efd | `k=-8` | `k=-d` | False |

| selection | 99ccc30d-db87-5ff3-b366-54bc530fc04c | `k=-2` | `k=-t` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-74646

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 6b9a3770-af37-58af-91e7-3430fd2463b3 | `k=5` | `k=t-2` | False |

| selection | 71cae964-c567-5585-ab23-7241fb114732 | `k=3` | `k=e` | False |

| selection | a8f3da90-4b17-5b45-af78-2746f79a0b95 | `k=1` | `k=v` | False |

| selection | ad97781e-f202-56a0-803a-f17ee1a49ca9 | `k=9` | `k=t+2` | False |

| selection | f0d5b11f-4138-5c57-8bc8-f9f3a404cfaa | `k=7` | `k=t` | True |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-74688

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 30949865-bcb4-5324-b20a-5013ed16ed8b | `k=-2` | `k=-u` | False |

| selection | b02857e6-f7e6-504c-84a4-ca08044eec2c | `k=-1` | `k=-1` | False |

| selection | bd377e49-f3f5-59d7-82a4-fcccc36aefd5 | `k=-3` | `k=-t` | False |

| selection | cffbe52d-faab-5e8d-a8c2-edecdb561a49 | `k=3` | `k=t` | True |

| selection | d763087a-bc9a-5f66-ac0e-8fa93b6ecd3b | `k=2` | `k=u` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-74695

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 0ba1e46b-dcb4-5f9e-b60f-f807d3ae1d2d | `k=\frac{1}{4}` | `k=t/2` | False |

| selection | 47f4259f-5c12-50a0-8a37-001fbf58b6db | `k=-\frac{1}{4}` | `k=-t/2` | False |

| selection | 761008e6-93b4-567d-8e13-46b3d3b90948 | `k=\frac{1}{2}` | `k=t` | True |

| selection | ec9c9c6a-7091-5c96-a5e5-dd27877f775b | `k=2` | `k=1/t` | False |

| selection | fa6d777f-a907-5d3e-9303-b5a3d04a19d9 | `k=\frac{1}{8}` | `k=t/4` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-74650

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | e3df6cd2-68c7-5027-b94c-cebc3edbefd0 | `k=\frac{1}{2}` | `k=1/t` | False |

| selection | 3d7403d1-9523-59ef-892c-8762070fc770 | `k=-\frac{1}{2}` | `k=-1/t` | False |

| selection | 43b3ca27-4022-5e94-91a9-05d77b4b0c3b | `k=-2` | `k=-t` | False |

| selection | 321a43c8-209e-53e7-bddf-716f4dd735c7 | `k=2` | `k=t` | True |

| selection | a9f1972b-cdc9-5bbd-bf68-8c034ebe8712 | `k=-4` | `k=-2*t` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-131730

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 0250b550-0b7c-5c05-b8f5-33da7345f93c | `k=2` | `k=b` | False |

| selection | 0e30254f-fef5-5030-ad74-62323657f390 | `k=0` | `k=0` | False |

| selection | 32810e7f-ad8d-5b1e-a7d2-839ff11f12a9 | `k=\frac{2}{3}` | `k=t` | True |

| selection | 5b0d5bd9-5c97-5445-afdc-58640864c07d | `k=-\frac{2}{3}` | `k=-t` | False |

| selection | e23cbcca-7092-5855-aeeb-dd2de6061a27 | `k=\frac{3}{2}` | `k=1/t` | False |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

### Bank q-42021

| Field | Original answer UUID | Original full value | Parameterized expression | Correct |
|---|---|---|---|---|

| selection | 17602323-8777-51fe-9a70-fac173438e8d | `k=1` | `k=-v` | False |

| selection | 3745dd5b-bc8f-5c5f-bfbb-0a70d0ee8eee | `k=-3` | `k=d` | False |

| selection | 8c1862b9-030a-5755-b668-e59ca4c9e456 | `k=-5` | `k=-t` | False |

| selection | a1294db0-0da9-5a02-b9e5-791ef34dcf11 | `k=2` | `k=b` | False |

| selection | cf6dc1f0-4ead-53bf-8e9f-9b57805aa51d | `k=5` | `k=t` | True |

Atomic mathematical components: `equation1`, `equation2`, `pivot_equation`, `reduced_equation`, `matrix0`, `matrix1`, `matrix2`, `rowop`, `answer`, `zero_equation`. The exact prompt and complete ordered solution masks are in recipes.json.

## 4. Reusable template and constraints

Fixed components: determine-k prompt, two aligned equations, augmented matrix, Gaussian elimination sentence, classification definition, final sentence; dependence adds the fixed removal/basic/free-variable paragraphs. Variable components are complete equations, whole matrices, full row operation, reduced equation, k equation and zero-row equation. Optional swapped stage belongs only to dependent_swap. All objects derive from the same a,b,c,d,u,v,e. Masks never replace a bare numeral or expression substring. Whitespace and per-source sentence differences are kept in masks.

The generator performs exact SymPy arithmetic and samples signed integers, preserving an integer multiplier for moderate and a fractional multiplier for dependent_fractional. Every bank is selected as a complete set before validating options; collisions reject the whole instance. Explicit input rejects invalid domains instead of resampling. Bounds are enforced in validate_parameters. Source replay profiles remain arithmetic expression patterns outside normal defaults. Authored default banks are method based:

- easy/bare/scaled: t, -t, b/u, -b/u, 0 (sign error, omitted elimination multiplier, sign plus omitted multiplier, setting parameter zero).
- shifted moderate: t, -t, r b/u, -v/u, (r b+v)/u (root sign, omitted shift, omitted row contribution, wrong shift sign).
- swap hard: t, -t, 1/t, b, 0 (sign, reciprocal ratio, omitted pivot coefficient, zero).
- other hard: t, -t, -v/u, (b-v)/u, 0 (sign, omitted row contribution, omitted multiplier, zero).

These banks are authored extensions and contain five unequal values. There is no learner-facing error diagnosis. Integers and reduced rationals are exact. No unused plot parameters exist. Mathematical identity uses the full symbolic augmented-system row space plus singular parameter, independent of level, excluding banks/profile. Presentation identity uses version, level, template, parameters, full prompt, full fixed solution and unordered full answer bank; changing seed only shuffles options.

## Source errors and repairs

q-74695: original corresponding system and remaining-equation prose say x+ky=2 while prompt, initial matrix and swapped pivot are x+ky=-2. Both incorrect occurrences are repaired to -2. Correct k and bank are unchanged.

q-42021: original initial augmented matrix says first RHS -3 while prompt and elimination matrix say +3; repair to +3. The corresponding first equation is printed 1-2y=3, incompatible with either row; repair to x+2y=3. Reduced row -(k-5)y=0 is preserved (equivalent to the matrix coefficient -k+5). Correct k and bank are unchanged.

Raw evidence remains in source.json and originals in review.md. Four of fifteen original prompt strings and three original solution strings are byte-exact. After escaping the malformed system braces, fifteen prompt strings and thirteen full source solution strings match; after the two mathematical repairs as well, all fifteen full solution strings match. Matrices and row operations retain their original stage count and notation. No incorrect teaching rules are copied to normal output. Raw source masks retain captured literal left-system braces as evidence. Rendering escapes every unescaped left-system brace in observed replays; authored masks already use escaped visible braces. This presentation repair prevents unclosed TeX groups. All remaining component groups and math delimiters must balance.

