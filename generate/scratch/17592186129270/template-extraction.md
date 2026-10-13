# Template extraction — four stages

## 1. Specific observed questions

All original parameters use h=k=l=0; functions are continuously differentiable on R³ except q-161815 (u>0) and q-161813 (u≠0). Coefficients are small exact integers; source q-161818 has rational plane offset 3/4. All input coordinates are u,v,w and output components x,y,z. Each source has its own complete derivative/cofactor stage masks.


### q-161819

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{u}^{2}-{w}^{2} \\ w{e}^{u} \\ u-v\end{aligned}].
$$

Field count: 2. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161819 section of review.md.


### q-39709

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{u}^{2}-v \\ {u}^{2}+v \\ {e}^{w}\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-39709 section of review.md.


### q-161809

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}uv \\ u+v \\ w\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161809 section of review.md.


### q-161812

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u \\ {v}^{3}+{w}^{3} \\ v+w\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161812 section of review.md.


### q-161815

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\sqrt{u} \\ vw \\ u+w\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161815 section of review.md.


### q-161817

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u \\ v{e}^{w} \\ 2u+v+3w\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161817 section of review.md.


### q-161818

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u+3w \\ v+2w \\ {v}^{2}-u\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161818 section of review.md.


### q-161813

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}\frac{1}{u} \\ {v}^{2}+w \\ vw\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161813 section of review.md.


### q-161814

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u+2w \\ v-u \\ uw\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161814 section of review.md.


### q-161816

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{u} \\ {e}^{u+w} \\ uv+w\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161816 section of review.md.


### q-161810

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}u+vw \\ {v}^{2} \\ w+v\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161810 section of review.md.


### q-161811

Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as

$$
T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}{e}^{u}+v \\ v+w \\ vw\end{aligned}].
$$

Field count: 1. Captured difficulty: moderate. Complete worked solution: see the Original replay q-161811 section of review.md.


## 2. Shared generalized descriptions

Each observed family computes all nine partials of its specific polynomial, exponential, radical or reciprocal map, expands the determinant along a sparse row/column, sets it to zero, removes known nonzero factors on the C¹ domain, and identifies the complete plane/parabolic-cylinder/pair-of-planes locus. Templates retain source-specific omitted arithmetic rows and fixed worked prose; merging into a single expanded CAS solution would lose observed stages.


## 3. Components and complete bank profiles

Each bank below is an observed expression-pattern profile, not a recovered psychological error recipe. Its parameterization translates every full algebraic component by u→u−h, v→v−k, w→w−l. Coordinate labels, function argument labels, derivative labels and the input vector are protected; explicit geometric plane names become the appropriate translated plane. This is a genuine symbolic translation recipe, used identically at zero and changed parameters. Every original answer value is listed, with its source field and exact designation. Historical values remain evidence-only because one example cannot establish distractor authoring intent.


### q-161819 — observed profile

Field 1, id 4d271abc-b1d9-5284-9062-68834149c800, key `selection`; correct attribute **absent**.

- The critical points lie on the plane $u = 2v$. — undesignated legacy value; recipe: complete coordinate-translation of this exact relation; original UUID a9ef2524-c316-5f5c-bb17-9410d6df7855.

- The critical points lie on the parabolic cylinder $u =-w^{2}$. — undesignated legacy value; recipe: complete coordinate-translation of this exact relation; original UUID af21f9b2-947b-5b4b-9b83-b2324aabe6c2.

- The critical points lie on the plane $u = w$. — undesignated legacy value; recipe: complete coordinate-translation of this exact relation; original UUID b8ef1406-0abe-5cfe-bc04-7ae04a77ecf5.

- The critical points lie on the $vw -$plane. — undesignated legacy value; recipe: complete coordinate-translation of this exact relation; original UUID e90dd075-4fb2-51bb-9367-44b42c15619d.

- The critical points lie on the parabolic cylinder $u = 2w^{2}$. — undesignated legacy value; recipe: complete coordinate-translation of this exact relation; original UUID 0cffeeef-f100-51b5-ac9e-aa76adbf7807.

Field 2, id 17caa721-6c88-5948-86f1-24aa0f77f9b9, key `selection`; correct attribute present.

- The critical points lie on the $vw-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 59ecd82e-c85b-5221-81f4-5aa437d23a7f.

- The critical points lie on the parabolic cylinder $u=2{w}^{2}.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 1680c5f5-1c51-52cd-a03a-ad30d3c07c77.

- The critical points lie on the plane $u=2v.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 92c1139b-4ea6-5a6e-91ff-1cd1ee2688f2.

- The critical points lie on the parabolic cylinder $u=-{w}^{2}.$ — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID 9ea440aa-4bbc-5828-a750-3ec0ce76a35d.

- The critical points lie on the plane $u=w.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID b1928d32-8a83-5bc0-a68f-3b8d2a17bd07.

Normal authored method profile (same family, separate five-option bank):

- `$u + w^{2}=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u - w^{2}=0$` — wrong sign in second cofactor. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u + w=0$` — omit one w factor in second cofactor. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$w=0$` — omit first cofactor. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u=0$` — omit second cofactor. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-39709 — observed profile

Field 1, id ec45c948-28d5-5ad6-a116-f2bf6a3a31b0, key `selection`; correct attribute present.

- The critical points lie on the $vw-$plane. — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID 89f2fafa-94fa-537a-9de2-cde9b153270f.

- The critical points lie on the sphere ${u}^{2}+{v}^{2}+{w}^{2}=1.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 06b7dea6-5d67-5db6-9562-564a467e6927.

- The critical points lie on the parabolic cylinder ${w}^{2}=2u.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 5cdabe0b-331f-59b0-be6a-e0b333cf7d10.

- The critical points lie on the plane $w=u.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID edca51bc-5f25-52b9-81ee-5e945aaea583.

- The critical points lie on the $uv-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 2daa5374-5e80-5f12-9e7f-d5612c496bb5.

Normal authored method profile (same family, separate five-option bank):

- `$u=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$w=0$` — set exponential exponent to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v=0$` — use wrong independent coordinate. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u^{2} - v=0$` — equate first component to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u^{2} + v=0$` — equate second component to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-161809 — observed profile

Field 1, id 73950424-d736-5015-94bb-837d8bf513c9, key `selection`; correct attribute present.

- The critical points lie on the cylinder ${v}^{2}+{u}^{2}=1.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 1b1e167f-c36b-51bb-8f7d-1c5abfba9d3c.

- The critical points lie on the $uv-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 398d98c4-80d9-5695-9ad1-7904a7156b87.

- The critical points lie on the plane $v=u.$ — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID 50abbce6-3f16-512e-a087-34dc285e7cbe.

- The critical points lie on the parabolic cylinder $v={u}^{2}.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID cc12c5cd-4583-53a4-9f13-8cababa0d611.

- The critical points lie on the $uw-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID de43abc5-071a-5046-a899-84beee7c637b.

Normal authored method profile (same family, separate five-option bank):

- `$- u + v=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u + v=0$` — add minor products. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v=0$` — omit second minor product. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u=0$` — omit first minor product. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u v=0$` — equate first component to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-161812 — observed profile

Field 1, id bcf9576c-0ce8-5723-bb46-cfba69aeb672, key `selection`; correct attribute present.

- The critical points lie on the parabolic cylinder $v={w}^{2}.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 710d7d7d-97b4-592f-b30c-acf388d38859.

- The critical points lie on the $vw-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 76ca4acf-773c-501c-ba6e-25239ada0435.

- The critical points lie on the plane $v=2w.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 7b363e77-7f40-535f-a3a7-6bd580690682.

- The critical points lie on the planes $v=\pm w.$ — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID 88ce4141-06f6-5738-b4cf-0fb6b9a3a05e.

- The critical points lie on the plane $v=u.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID eaed37b4-3321-5a47-9faa-28666138fd1b.

Normal authored method profile (same family, separate five-option bank):

- `$v^{2} - w^{2}=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v^{2} + w^{2}=0$` — add minor products. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v - w^{2}=0$` — drop power in v derivative. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v^{2} - w=0$` — drop power in w derivative. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v=0$` — omit second minor product. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-161815 — observed profile

Field 1, id 55be6ad3-d866-57e2-8467-8385c57eb9ce, key `selection`; correct attribute present.

- The critical points lie on the parabolic cylinder $v={w}^{2}.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 0e5c045a-d984-5c99-8fa3-0129ac115c4f.

- The critical points lie on the $vw-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 2d089752-d1ca-57d4-aaad-39bd60fd867f.

- The critical points lie on the $uv-$plane. — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID 768c6810-e6a9-5693-b6ba-88bee24c33f4.

- The critical points lie on the sphere ${u}^{2}+{v}^{2}+{w}^{2}=2.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 9f89b797-8be9-5dae-9e56-f0b7e9d1b9f1.

- The critical points lie on the plane $u=w.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID bc5b203f-69ef-5d8b-b9f1-3986949f0305.

Normal authored method profile (same family, separate five-option bank):

- `$w=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v=0$` — differentiate product with wrong held coordinate. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u=0$` — equate derivative denominator to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v w=0$` — equate second component to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u + w=0$` — equate third component to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-161817 — observed profile

Field 1, id b0414cad-2a72-50dc-8e82-0bf67299254f, key `selection`; correct attribute present.

- The critical points lie on the sphere ${u}^{2}+{v}^{2}+{w}^{2}=3.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 012e5e71-30c4-576f-9027-84673f0cec11.

- The critical points lie on the plane $v=3.$ — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID 1ca3f8ee-ee06-5aa0-b1ee-b1a91215f89a.

- The critical points lie on the cylinder ${v}^{2}+{w}^{2}=0.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID aedf9c47-b56b-5e71-845a-05c0a9e74384.

- The critical points lie on the $uw-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID f4e3d435-b0b0-5133-a7de-47ee24110c94.

- The critical points lie on the $uv-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID f7242b75-d7a6-5b47-a2a4-a6f542bd4ba3.

Normal authored method profile (same family, separate five-option bank):

- `$3 - v=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v + 3=0$` — add minor products. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v=0$` — omit first minor product. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$w=0$` — set exponential exponent to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$3 - w=0$` — differentiate product with wrong held coordinate. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-161818 — observed profile

Field 1, id 0966bd13-e522-5f74-88dd-66c421ecae33, key `selection`; correct attribute present.

- The critical points lie on the parabolic cylinder $w=\frac{{v}^{2}}{2}.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 0360b3bf-0e11-5644-974a-fb91e4539e1f.

- The critical points lie on the planes $v=\pm w.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 40d23535-8e40-5b39-96da-dc0c5913b017.

- The critical points lie on the plane $v=u.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 4d4e4c43-7095-567c-8087-ac111d00d4b2.

- The critical points lie on the $uw-$ plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID a24f7a5b-f9c2-51ab-bfe8-2b6ef54faa12.

- The critical points lie on the plane $v=\frac{3}{4}.$ — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID c0ca341c-0372-5300-8b3a-24814e46f956.

Normal authored method profile (same family, separate five-option bank):

- `$3 - 4 v=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$4 v + 3=0$` — wrong minor sign. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$3 - 2 v=0$` — omit derivative factor two. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v=0$` — omit last cofactor. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$3 - 4 w=0$` — differentiate with wrong held coordinate. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-161813 — observed profile

Field 1, id 88cb516a-a7eb-5761-97af-05385415c8d5, key `selection`; correct attribute present.

- The critical points lie on the $wv-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 07b9f18b-ec2f-51d5-ae14-92461f9907ea.

- The critical points lie on the plane $w=v.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 5bacd98b-62c2-5e98-a210-80793aec69cd.

- The critical points lie on the parabolic cylinder $w=2{v}^{2}.$ — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID 13bfe028-f756-50dc-a99d-e4bd7e879772.

- The critical points lie on the plane $w=-2v.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 8ad07193-94a4-5bd2-b02f-54c7365c5656.

- The critical points lie on the $uv-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 69b5ad50-abba-5674-a016-be9139fe02be.

Normal authored method profile (same family, separate five-option bank):

- `$2 v^{2} - w=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$2 v^{2} + w=0$` — add minor products. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v^{2} - w=0$` — omit derivative factor two. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v=0$` — omit second minor product. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$w=0$` — omit first minor product. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-161814 — observed profile

Field 1, id 65676948-b2fa-585d-8619-ca89f50c6f34, key `selection`; correct attribute present.

- The critical points lie on the plane $u+v-2w=0.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 53f14d31-90ea-5326-97dc-45022d0835ee.

- The critical points lie on the elliptic cylinder ${u}^{2}+2{w}^{2}=1.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID b740b568-485c-5311-a423-33ea2f3eeffb.

- The critical points lie on the parabolic cylinder $v={u}^{2}.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID a6795027-5482-5bff-8214-2dd2cc097fe2.

- The critical points lie on the $vw-$ plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 5adbc1f1-362c-537c-bb50-2cdecc09b123.

- The critical points lie on the plane $u=2w.$ — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID f3a89ced-7070-57be-88cf-4d4b894bd3f7.

Normal authored method profile (same family, separate five-option bank):

- `$u - 2 w=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u + 2 w=0$` — wrong last cofactor sign. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u - w=0$` — omit first-row coefficient two. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u=0$` — omit last cofactor. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$w=0$` — omit first cofactor. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-161816 — observed profile

Field 1, id 175d9200-8100-5e54-b984-b7451df1967c, key `selection`; correct attribute present.

- The critical points lie on the $vw-$plane. — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID b76c85a4-c631-5c36-941d-c14613479d8a.

- The critical points lie on the parabolic cylinder $w=-2{v}^{2}.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 10a3627e-14c0-553d-8005-b8e65337d0b7.

- The critical points lie on the plane $2u+v+w=0.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID b1ffd8d2-f852-57f7-9970-8454309f0281.

- The critical points lie on the plane $w=-2u.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID a8fe9b5d-4fbe-56d7-9627-c5c1df64a715.

- The critical points lie on the parabolic cylinder $w={u}^{2}.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID e3cbb05e-806b-56aa-8136-04b088a6dc5f.

Normal authored method profile (same family, separate five-option bank):

- `$u=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v=0$` — differentiate product with wrong held coordinate. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$w=0$` — set second exponential exponent w term to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$2 u + w=0$` — set final exponential exponent to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u v + w=0$` — equate third component to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-161810 — observed profile

Field 1, id 06a97003-66fd-5b44-944b-7b4ac3d8364b, key `selection`; correct attribute present.

- The critical points lie on the $uw-$plane. — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID 06cfa4e4-4978-5d07-b498-b67163d323ba.

- The critical points lie on the sphere ${x}^{2}+{y}^{2}+{z}^{2}=1.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 47f0e73b-3fcc-5922-ac4c-5cbbb15dc078.

- The critical points lie on the $vw-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 4cd27081-6df8-5fcc-87e8-0b763e12dd24.

- The critical points lie on the plane $v=1.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID bdd4d236-b060-5654-b754-6a3374d3448b.

- The critical points lie on the plane $v=u.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID ddaabaf5-f0e8-54a9-9f5a-d6c4751feaf2.

Normal authored method profile (same family, separate five-option bank):

- `$v=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u=0$` — differentiate with wrong independent coordinate u. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$w=0$` — differentiate with wrong independent coordinate w. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$u + v w=0$` — equate first component to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v + w=0$` — equate third component to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


### q-161811 — observed profile

Field 1, id d0a37030-5cd9-5e43-a291-e19dfc94c67f, key `selection`; correct attribute present.

- The critical points lie on the parabolic cylinder $v=2{w}^{2}.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 2e37282e-8869-5ad2-9f01-e062a7d21846.

- The critical points lie on the plane $v=w.$ — correct designation; recipe: complete coordinate-translation of this exact relation; original UUID 4a31e95b-7336-5699-a485-0b22a7563452.

- The critical points lie on the $vw-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 56201c08-96c0-58d8-9ed7-c9a2a6ecea11.

- The critical points lie on the $uv-$plane. — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 7447254c-742a-5c7f-adb1-193a3168832a.

- The critical points lie on the sphere ${x}^{2}+{y}^{2}+{z}^{2}=4.$ — wrong designation; recipe: complete coordinate-translation of this exact relation; original UUID 7473d403-04c8-5521-92cd-20ba6d10f904.

Normal authored method profile (same family, separate five-option bank):

- `$v - w=0$` — correct. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v + w=0$` — add minor products. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v=0$` — omit second minor product. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$w=0$` — omit first minor product. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.

- `$v w=0$` — equate third component to zero. At changed parameters substitute complete coordinates before expansion. A squared single-coordinate zero is reduced to its equivalent plane; sums of squares retain intersection semantics.


## 4. Reusable masks, constraints, extensions and calculations

Observed template renderer: split complete inline/display math components; protect formal labels and independent input vector; translate algebraic variable factors with derivative-one coordinate substitutions; conditionally render coordinate-plane names; preserve all literal prose/row structure at h=k=l=0. One fixed worked solution is independent of selected option. Observed/repaired profiles reproduce all historical banks; method profiles replace the entire bank with a predeclared five-operation family, never mix a first-valid pool. Historical expressions are not promoted as inferred method errors.

Translation constraints: signed integer h,k,l∈[−3,3]. These are authored workload bounds, enforced on explicit parameters. The family and operative translated zero condition define mathematical-task identity, excluding shifts that merely alter nonzero exponential factors or additive constants. Actual prompt/solution/difficulty/complete bank define content identity, excluding seed/shuffle/profile aliases.

Easy diagonal: T has one component (coordinate−h)² and the other two unchanged, h∈{±1,…,±5}, three orientations. Exactly one nonlinear partial and one nonzero cofactor; 30 meaningful tasks. The bank uses the correct coordinate plane, either wrong independent-coordinate plane, reversed shift and omitted shift.

Moderate product block: T=(uv,au+bv,w), distinct coprime a,b∈[2,8]. Exactly two surviving 2×2 minor products, critical plane bv−au=0. The complete bank uses addition instead of subtraction, omitted b, omitted a, and swapped held coordinates. This additional template has 28 meaningful coefficient-ratio tasks. Normal moderate also samples the twelve source function families with their explicitly authored method banks and bounded translations, retaining plane, cylinder and union demands.

Hard: T=(u+av+bw,cu²+v,du²+ku+w), signed nonzero integer a,b,c,d,k of magnitude≤4, ac≠bd, ac+bd≠0, 1−bk≠0. Three nonzero first-row cofactors and two unequal signed coefficient products; J=1−2ac u−b(2du+k). All normal options are entire affine loci. Guards retain all three terms and nonzero rational plane offset; complete bank errors omit middle cofactor, omit last cofactor, reverse middle sign and omit constant cofactor. This is determinant bookkeeping already established immediately before this KP, not an inverse-Jacobian, volume or rotated-surface task.

Observed solution fidelity is established first at zero shifts, before changed translation and authored bank checks. The independent validator reads the actual printed map and every displayed intermediate expression; metadata-only answer checks are insufficient. Original q-161819 legacy field remains missing-correct; authentic widget screenshot and verify-input establish the one-field repaired layout. Missing designation is not inferred as a raw match. q-161809 has extra punctuation after v=u; repaired/method output removes one period. q-161815/q-161813 original prompts omit necessary C¹ domains; raw exact retains omission, normal/repaired adds restrictions. No wrong mathematical worked-solution value was found.

Plots: none; see plot-extraction.md. Dependency/runtime source metadata appears in generation; native engine source/binary provenance belongs to validation evidence. No database writes.
