# Template extraction

## 1. Describe each source before generalizing

### q-1340 — let2_radio / observed_1340

Original prompt:

Let $u=⟨-3,2⟩$ and $v=⟨7,9⟩.$ Find $u\cdot v.$

Components: {"a": [-3, 2], "b": [7, 9], "names": ["u", "v"]}. One radio field. Original choices: 63, -6, 39, -3, 57. Original correct: -3.

Original full worked solution:

Summing up the products of corresponding components, we obtain:

$$
\begin{aligned}u\cdot v & ={u}_{x}\cdot {v}_{x}+{u}_{y}\cdot {v}_{y} \\  & =(-3)\cdot 7+2\cdot 9 \\  & =-21+18 \\  & =-3\end{aligned}
$$

### q-1355 — if3_radio / observed_1355

Original prompt:

If $a = ⟨ - 1, 0, 6⟩$ and $b = ⟨10, 2,-5⟩$, then $a \cdot b =$

Components: {"a": [-1, 0, 6], "b": [10, 2, -5]}. One radio field. Original choices: -20, -40, 10, 40, 20. Original correct: absent; inferred -40.

Original full worked solution:

[Absent in captured source; authored formal → substitution → individually evaluated products → final scalar.]

### q-168035 — dependent3_blank / observed_168035

Original prompt:

Find the dot product of the vectors $q$ and $r.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        $q\cdot r=\,$

                                    
                                
                                    
                            
                                        {{field-1}}

Components: {"a": [0, -3, 2], "b": [0, 4, 3]}. One blank field. Original choices: -6. Original correct: -6.

Original full worked solution:

The dot product of two vectors given in component form can be computed by summing up the products of corresponding components of vectors:

$$
\begin{aligned}q\cdot r & ={q}_{x}\cdot {r}_{x}+{q}_{y}\cdot {r}_{y}+{q}_{z}\cdot {r}_{z}\end{aligned}
$$

From part 1, we have $q=⟨0,-3,2⟩$ and $r=⟨0,4,3⟩.$ Therefore, the formula for the dot product gives

$$
\begin{aligned}q\cdot r & =0\cdot 0+(-3)\cdot 4+2\cdot 3 \\  & =0-12+6 \\  & =-6.\end{aligned}
$$

### q-101406 — let2_radio / observed_101406

Original prompt:

Let $p=⟨1,-2⟩$ and $q=⟨4,-1⟩.$ Find $p\cdot q.$

Components: {"a": [1, -2], "b": [4, -1], "names": ["p", "q"]}. One radio field. Original choices: -2, 6, 8, 2, -4. Original correct: 6.

Original full worked solution:

Summing up the products of corresponding components, we obtain:

$$
\begin{aligned}p\cdot q & ={p}_{x}\cdot {q}_{x}+{p}_{y}\cdot {q}_{y} \\  & =1\cdot 4+(-2)\cdot (-1) \\  & =4+2 \\  & =6\end{aligned}
$$

### q-1341 — if3_arrow_radio / observed_1341

Original prompt:

If $\overset{\to }{a}=⟨1,-2,4⟩$ and $\overset{\to }{b}=⟨11,4,-1⟩$, then $\overset{\to }{a}\cdot \overset{\to }{b}=$

Components: {"a": [1, -2, 4], "b": [11, 4, -1]}. One radio field. Original choices: 11, 7, 27, 15, -1. Original correct: -1.

Original full worked solution:

Summing up the products of corresponding components, we obtain:

$$
\begin{aligned}\overset{\to }{a}\cdot \overset{\to }{b} & ={a}_{x}\cdot {b}_{x}+{a}_{y}\cdot {b}_{y}+{a}_{z}\cdot {b}_{z} \\  & =1\cdot 11+(-2)\cdot 4+4\cdot (-1) \\  & =11+(-8)+(-4) \\  & =-1\end{aligned}
$$

### q-317910 — if2_blank / observed_317910

Original prompt:

If $a=⟨5,1⟩$ and $b=⟨2,4⟩,$ then $a\cdot b=${{field-1}}.

Components: {"a": [5, 1], "b": [2, 4]}. One blank field. Original choices: 14. Original correct: 14.

Original full worked solution:

Summing up the products of corresponding components, we obtain

$$
\begin{aligned}a\cdot b & ={a}_{x}\cdot {b}_{x}+{a}_{y}\cdot {b}_{y} \\  & =5\cdot 2+1\cdot 4 \\  & =10+4 \\  & =14.\end{aligned}
$$

### q-317911 — if2_blank / observed_317911

Original prompt:

If $u=⟨8,-2⟩$ and $v=⟨3,6⟩,$ then $u\cdot v=${{field-1}}.

Components: {"a": [8, -2], "b": [3, 6], "names": ["u", "v"]}. One blank field. Original choices: 12. Original correct: 12.

Original full worked solution:

Summing up the products of corresponding components, we obtain

$$
\begin{aligned}u\cdot v & ={u}_{x}\cdot {v}_{x}+{u}_{y}\cdot {v}_{y} \\  & =8\cdot 3+(-2)\cdot 6 \\  & =24-12 \\  & =12.\end{aligned}
$$

## 2. Shared mathematical pattern and response

Given complete component vectors, compute the scalar sum of products of corresponding components. The observed radio field has five delimiter-free scalar math choices; the blank contains a matching `{{field-1}}` placeholder and one exact scalar value. All source numerical products are integers. The canonical decimal example anchors exact noninteger authored arithmetic.

## 3. Map every source component and complete bank

Let `a_i,b_i` be corresponding input components, `t_i=a_i*b_i`, and `c=sum(t_i)`. The following tables account for every source answer. Every scalar reconstruction is an operation on actual inputs, not an answer lookup or unrelated perturbation. Original incorrect-choice intent is underdetermined, particularly compound expressions; these reconstructions are replay-only profiles and are not promoted to default learner banks. An exact reconstruction does not establish the original intended mistake.

### q-1340

| Original value | Reconstructed operation | Correct status |
|---|---|---|
| 63 | within_b_product | incorrect |
| -6 | double_dot | incorrect |
| 39 | reverse_first_product | incorrect |
| -3 | correct | correct |
| 57 | sum_within_vector_products | incorrect |

### q-1355

| Original value | Reconstructed operation | Correct status |
|---|---|---|
| -20 | reverse_first_omit_second | incorrect |
| -40 | correct | inferred correct |
| 10 | negate_first_only | incorrect |
| 40 | negate_dot | incorrect |
| 20 | reverse_third_omit_second | incorrect |

### q-168035

| Original value | Reconstructed operation | Correct status |
|---|---|---|
| -6 | correct | correct |

### q-101406

| Original value | Reconstructed operation | Correct status |
|---|---|---|
| -2 | reverse_first_product | incorrect |
| 6 | correct | correct |
| 8 | double_first_omit_second | incorrect |
| 2 | omit_first | incorrect |
| -4 | negate_first_omit_second | incorrect |

### q-1341

| Original value | Reconstructed operation | Correct status |
|---|---|---|
| 11 | only_first | incorrect |
| 7 | omit_second | incorrect |
| 27 | reverse_double_second_omit_third | incorrect |
| 15 | omit_second_reverse_third | incorrect |
| -1 | correct | correct |

### q-317910

| Original value | Reconstructed operation | Correct status |
|---|---|---|
| 14 | correct | correct |

### q-317911

| Original value | Reconstructed operation | Correct status |
|---|---|---|
| 12 | correct | correct |

Explicit profile formulas, in the same original bank order:

- observed_1340: `[b0*b1, 2*c, -t0+t1, c, a0*a1+b0*b1]` → `[63,-6,39,-3,57]`.
- observed_101406: `[t1-t0, c, 2*t0, t1, -t0]` → `[-2,6,8,2,-4]`.
- observed_1341: `[t0, t0+t2, t0-2*t1, t0-t2, c]` → `[11,7,27,15,-1]`.
- observed_1355: `[t2-t0, c, -t0, -c, t0-t2]` → `[-20,-40,10,40,20]`.
- observed blank profiles: `[c]` → `[-6]`, `[14]`, `[12]` respectively.

## 4. Reusable templates and constraints

Fixed prose and stage masks preserve each original's exact words, punctuation, arrow notation, component labels, row ordering, and evaluated-product signs. Slots are entire vectors, factors, names, sums, and final scalars. Normal output computes `c`, selects a complete eligible bank, computes every required option, and rejects the whole instance on equality. Radio options are shuffled deterministically only after field-owned answer identities and correct ref are recorded. A single worked solution is independent of any selected wrong option.

The four arithmetic stages are (1) formal corresponding-component formula, (2) actual ordered multiplication of signed grouped factors, (3) individually evaluated products in source addition/subtraction notation, (4) final scalar. The dependent template splits the formal block from the last three stages and includes its common explanatory paragraph. Arrow radio retains parenthesized negative evaluated terms. Blank solutions retain the omitted colon and final period. Source q-1355 has no worked solution, so the shared four-stage reconstruction is explicitly authored.

The authored default radio bank is complete: `[c, sum(a)+sum(b), sum(a)*sum(b), sum(t[1:]), sum(t[:-1])]`. These represent adding components in place of products, including all cross-coordinate products by multiplying the component sums, omitting the first corresponding product, and omitting the last corresponding product. All four are tied to the assessed operation. No random numerical perturbation, source-intent diagnosis, or mixed first-valid recipe pool is used. Exact rational duplicate/correct collisions reject the whole bank. Authored blanks use `[c]`.

Easy components are integral in [-12,12], for observed two/three-component layouts. Moderate components have absolute magnitude 2..12, exactly three nonzero integer products, at least one positive and one negative product. Hard components are nonzero exact tenths of absolute magnitude 1..6, exactly three products, at least two noninteger products, and mixed product signs. Within each level every sampled question has the same method and documented workload. The finite domains contain hundreds of directly checked distinct mathematical tasks at every level; only semantic component-pair tasks count toward variety. Normal radio banks are authored extensions while explicit `observed_*` profiles preserve all original banks.

Mathematical fingerprints sort corresponding factor pairs, quotienting multiplication-factor order and simultaneous coordinate permutations; labels, layouts, profiles, and option order do not inflate task variety. Full content identities hash generator version, difficulty, actual prompt, fixed solution, field kind, and complete sorted displayed bank. Changing a seed or unused profile spelling at fixed content does not change the identity. Full displayed changes produce different identities.

Source fidelity is separate from independent arithmetic and native grading: 7/7 complete banks and 23/23 displayed values match; 16/16 original distractors match; 6/6 present original correct designations match, with one separately inferred; 6/6 present full solution strings match, with one separately authored; 6/7 raw prompts match with one explicitly repaired standalone prompt. All seven practice records remain in `source-cases.json`. No source ambiguity or mathematical error remains hidden, and unknown original distractor intentions remain documented rather than claimed as recovered.
