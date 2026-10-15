Given that $y=\frac{8 \sin{\left(x \right)}}{x}$, find $\frac{\text{d}y}{\text{d}x}.$

Field `selection` (`:answer-field.type/radio`).

- $\frac{8 x \cos{\left(x \right)} + 8 \sin{\left(x \right)}}{x^{2}}$ — `2a363a3f-0e81-58a4-b66b-80f876a6ea6b`

- $\frac{8 \left(x \cos{\left(x \right)} - \sin{\left(x \right)}\right)}{x^{2}}$ [correct] — `26724b26-fb70-5a06-913d-b39825dadff0`

- $\frac{8 x \cos{\left(x \right)} - 8 \sin{\left(x \right)}}{x}$ — `f8198ea3-f427-56b4-9843-d195543ab7cb`

- $\frac{- 8 x \sin{\left(x \right)} + 8 \cos{\left(x \right)}}{x^{2}}$ — `d4a7f534-24d2-582c-9e55-b4d01608e4a8`

- $\frac{8 \left(- \sin{\left(x \right)} + \cos{\left(x \right)}\right)}{x}$ — `2bd2f99f-8b73-58b4-b865-52813761b917`

Let $u=8 \sin{\left(x \right)}$ and $v=x.$ Then

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x}&=8 \cos{\left(x \right)}\,\text{and}\,\frac{\text{d}v}{\text{d}x}=1.\end{aligned}
$$

Using the quotient rule, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{v\frac{\text{d}u}{\text{d}x}-u\frac{\text{d}v}{\text{d}x}}{v^{2}}\\ &=\frac{(x)\cdot (8 \cos{\left(x \right)})-(8 \sin{\left(x \right)})\cdot (1)}{(x)^{2}}\\ &=\frac{8 x \cos{\left(x \right)} - 8 \sin{\left(x \right)}}{x^{2}}.\end{aligned}
$$

```json
{
  "version": "leibniz-quotient-2026-10-14-v1",
  "template": "q-47994",
  "profile": "observed-47994",
  "bank_profile": "observed-47994",
  "seed": 110,
  "parameters": {
    "c": 8
  },
  "mathematical_fingerprint": "7c769c1a2ddd85542757aa2cc9bda7ab9b3a3cc531a7540342e0c630f619770e",
  "content_fingerprint": "08c7793a6aec730e2eb56bc70a40da7aeb144a7642ed4cfe094286eecc56f12f",
  "source_ids": [
    "q-47994"
  ],
  "source_basis": 2275,
  "source_lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1",
  "evidence_only": false,
  "eligible_for_learning": true,
  "authored_rating": false,
  "authored_solution": false,
  "presentation_repairs": [
    "normalize math notation"
  ],
  "domain": "x !=0",
  "plot_rating": "none",
  "sympy_version": "1.14.0",
  "math_format": "course-academy-tex-v1"
}
```

---

Given that $y=\frac{- 2 e^{x}}{x + 4}$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

Field `field-1` (`:answer-field.type/blank`).

- $- \frac{2 \left(x + 3\right) e^{x}}{\left(x + 4\right)^{2}}$ [correct] — `aefc96f0-5fbf-5f07-8483-7ac12e8610e9`

Let $u=- 2 e^{x}$ and $v=x + 4.$ Then

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x}&=- 2 e^{x}\,\text{and}\,\frac{\text{d}v}{\text{d}x}=1.\end{aligned}
$$

Using the quotient rule, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{v\frac{\text{d}u}{\text{d}x}-u\frac{\text{d}v}{\text{d}x}}{v^{2}}\\ &=\frac{(x + 4)\cdot (- 2 e^{x})-(- 2 e^{x})\cdot (1)}{(x + 4)^{2}}\\ &=\frac{- 2 e^{x}(x+4-1)}{(x + 4)^{2}}\\ &=- \frac{2 \left(x + 3\right) e^{x}}{\left(x + 4\right)^{2}}.\end{aligned}
$$

```json
{
  "version": "leibniz-quotient-2026-10-14-v1",
  "template": "q-340340",
  "profile": "fragment",
  "bank_profile": "fragment",
  "seed": 111,
  "parameters": {
    "c": -2,
    "b": 4
  },
  "mathematical_fingerprint": "15db98ae3f9163f3b3af21b3e7428a8765d18606aba924b1c3e30b9757c27af4",
  "content_fingerprint": "ef45c327cd5cd4ff8e613e43e76551c713ae0bf3015b44712a931011e8738524",
  "source_ids": [
    "q-340340"
  ],
  "source_basis": 2275,
  "source_lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1",
  "evidence_only": false,
  "eligible_for_learning": true,
  "authored_rating": false,
  "authored_solution": false,
  "presentation_repairs": [
    "normalize math notation"
  ],
  "domain": "x + 4 !=0",
  "plot_rating": "none",
  "sympy_version": "1.14.0",
  "math_format": "course-academy-tex-v1"
}
```

---

Given that $y=\frac{\log_{8}x}{x^{3}}$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}}
$)\cdot \frac{1}{x^{4} \ln{\left(8 \right)}}.$

Field `field-1` (`:answer-field.type/blank`).

- $1 - 3 \ln{\left(x \right)}$ [correct] — `caba951b-b58f-5553-95e7-b8b4dc2d95a9`

Let $u=\log_{8}x=\frac{\ln x}{\ln 8}$ and $v=x^{3}.$ Then

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x}&=\frac{1}{x \ln{\left(8 \right)}}\,\text{and}\,\frac{\text{d}v}{\text{d}x}=3 x^{2}.\end{aligned}
$$

Using the quotient rule, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{v\frac{\text{d}u}{\text{d}x}-u\frac{\text{d}v}{\text{d}x}}{v^{2}}\\ &=\frac{(x^{3})\cdot (\frac{1}{x \ln{\left(8 \right)}})-(\frac{\ln{\left(x \right)}}{\ln{\left(8 \right)}})\cdot (3 x^{2})}{(x^{3})^{2}}\\ &=\frac{\frac{x^{2}}{\ln{\left(8 \right)}}-\frac{3 x^{2} \ln{\left(x \right)}}{\ln{\left(8 \right)}}}{x^{6}}\\ &=\frac{x^{2}-3 x^{2} \ln{\left(x \right)}}{x^{6}\ln{\left(8 \right)}}\\ &=\frac{x^{2}(1 - 3 \ln{\left(x \right)})}{x^{6}\ln{\left(8 \right)}}\\ &=\frac{1 - 3 \ln{\left(x \right)}}{x^{4} \ln{\left(8 \right)}}\\ &=(1 - 3 \ln{\left(x \right)})\cdot \frac{1}{x^{4} \ln{\left(8 \right)}}.\end{aligned}
$$

```json
{
  "version": "leibniz-quotient-2026-10-14-v1",
  "template": "q-340343",
  "profile": "fragment",
  "bank_profile": "fragment",
  "seed": 110,
  "parameters": {
    "b": 8,
    "n": 3
  },
  "mathematical_fingerprint": "73508d52d35ef1a6a7bbdaba09cefc68f64c8cae132ec64b6dab1df286986034",
  "content_fingerprint": "309e9284773e7c5e188837d08123adb6063454d9de2b1487c69eae11f28d4419",
  "source_ids": [
    "q-340343"
  ],
  "source_basis": 2275,
  "source_lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1",
  "evidence_only": false,
  "eligible_for_learning": true,
  "authored_rating": false,
  "authored_solution": false,
  "presentation_repairs": [
    "normalize math notation"
  ],
  "domain": "x>0 and x^{3} !=0",
  "plot_rating": "none",
  "sympy_version": "1.14.0",
  "math_format": "course-academy-tex-v1"
}
```

---

Given that $y=\frac{- 2 x^{2}}{x^{2} + 4}$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

Field `field-1` (`:answer-field.type/blank`).

- $- \frac{16 x}{\left(x^{2} + 4\right)^{2}}$ [correct] — `f6fb61e6-f1dc-5d88-b950-76ec97f82a6b`

Let $u=- 2 x^{2}$ and $v=x^{2} + 4.$ Then

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x}&=- 4 x\,\text{and}\,\frac{\text{d}v}{\text{d}x}=2 x.\end{aligned}
$$

Using the quotient rule, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{v\frac{\text{d}u}{\text{d}x}-u\frac{\text{d}v}{\text{d}x}}{v^{2}}\\ &=\frac{(x^{2} + 4)\cdot (- 4 x)-(- 2 x^{2})\cdot (2 x)}{(x^{2} + 4)^{2}}\\ &=\frac{- 4 x^{3}+- 16 x-(- 4 x^{3})}{(x^{2} + 4)^{2}}\\ &=- \frac{16 x}{\left(x^{2} + 4\right)^{2}}.\end{aligned}
$$

```json
{
  "version": "leibniz-quotient-2026-10-14-v1",
  "template": "q-340332",
  "profile": "fragment",
  "bank_profile": "fragment",
  "seed": 111,
  "parameters": {
    "c": -2,
    "b": 4
  },
  "mathematical_fingerprint": "07c4a043bc0f4d6f8ed1ace84dec4f55ce50f9c1debd20306f95d5f9657683fc",
  "content_fingerprint": "7d151578e389fef689bd34a1267f471f7c855fb1e559d0844d32ed1a410b202e",
  "source_ids": [
    "q-340332"
  ],
  "source_basis": 2275,
  "source_lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1",
  "evidence_only": false,
  "eligible_for_learning": true,
  "authored_rating": false,
  "authored_solution": false,
  "presentation_repairs": [
    "normalize math notation"
  ],
  "domain": "x^{2} + 4 !=0",
  "plot_rating": "none",
  "sympy_version": "1.14.0",
  "math_format": "course-academy-tex-v1"
}
```

---

Given that $y=\frac{8 \cos{\left(x \right)} + 8}{\sin{\left(x \right)}}$, find $\frac{\text{d}y}{\text{d}x}.$

Field `selection` (`:answer-field.type/radio`).

- $\frac{8}{\sin^{2}{\left(x \right)}}$ — `9bacdd7a-dd8a-538b-a2d2-c7cfb1dd751c`

- $- \frac{8}{\sin^{2}{\left(x \right)}}$ — `210884dd-bce0-5603-9f45-c8cfdb2e0a89`

- $- \frac{8}{1 - \cos{\left(x \right)}}$ [correct] — `ed134e4a-90d0-5966-980a-66e29ad7529a`

- $- \frac{8}{\cos{\left(x \right)} + 1}$ — `74d49c4e-8010-54d2-bc6f-5915c90fe1a2`

- $\frac{8}{1 - \cos{\left(x \right)}}$ — `5f17c0c6-a608-5fd6-bc17-5d811b50675c`

Let $u=8 \cos{\left(x \right)} + 8$ and $v=\sin{\left(x \right)}.$ Then

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x}&=- 8 \sin{\left(x \right)}\,\text{and}\,\frac{\text{d}v}{\text{d}x}=\cos{\left(x \right)}.\end{aligned}
$$

Using the quotient rule, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{v\frac{\text{d}u}{\text{d}x}-u\frac{\text{d}v}{\text{d}x}}{v^{2}}\\ &=\frac{(\sin{\left(x \right)})\cdot (- 8 \sin{\left(x \right)})-(8 \cos{\left(x \right)} + 8)\cdot (\cos{\left(x \right)})}{(\sin{\left(x \right)})^{2}}\\ &=\frac{- 8 \sin^{2}{\left(x \right)} - 8 \cos^{2}{\left(x \right)} - 8 \cos{\left(x \right)}}{\sin^{2}x}\\ &=- \frac{8}{1 - \cos{\left(x \right)}}.\end{aligned}
$$

```json
{
  "version": "leibniz-quotient-2026-10-14-v1",
  "template": "q-9909",
  "profile": "observed-9909",
  "bank_profile": "observed-9909",
  "seed": 110,
  "parameters": {
    "c": 8
  },
  "mathematical_fingerprint": "1d55893804dc90c35ddda94b3692c345b2d760a2afa22dd4bccb12b8634d9473",
  "content_fingerprint": "5f2d5e489a10be8a16f4cd6c5f1a6906fbcbf5e3aba4bd8f0aea65400a09b301",
  "source_ids": [
    "q-9909"
  ],
  "source_basis": 2275,
  "source_lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1",
  "evidence_only": false,
  "eligible_for_learning": true,
  "authored_rating": true,
  "authored_solution": true,
  "presentation_repairs": [
    "normalize math notation"
  ],
  "domain": "\\sin{\\left(x \\right)} !=0",
  "plot_rating": "none",
  "sympy_version": "1.14.0",
  "math_format": "course-academy-tex-v1"
}
```

---

Given that $y=\frac{4 - 7 \sin{\left(x \right)}}{\sin{\left(x \right)}}$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

Field `field-1` (`:answer-field.type/blank`).

- $- 4 \cot{\left(x \right)} \csc{\left(x \right)}$ [correct] — `5fc75cd8-16e3-5565-ae90-8a145aec32a9`

Let $u=4 - 7 \sin{\left(x \right)}$ and $v=\sin{\left(x \right)}.$ Then

$$
\begin{aligned}\frac{\text{d}u}{\text{d}x}&=- 7 \cos{\left(x \right)}\,\text{and}\,\frac{\text{d}v}{\text{d}x}=\cos{\left(x \right)}.\end{aligned}
$$

Using the quotient rule, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x}&=\frac{v\frac{\text{d}u}{\text{d}x}-u\frac{\text{d}v}{\text{d}x}}{v^{2}}\\ &=\frac{(\sin{\left(x \right)})\cdot (- 7 \cos{\left(x \right)})-(4 - 7 \sin{\left(x \right)})\cdot (\cos{\left(x \right)})}{(\sin{\left(x \right)})^{2}}\\ &=\frac{\cos{\left(x \right)}(- 7 \sin{\left(x \right)}-4+7 \sin{\left(x \right)})}{\sin^{2} x}\\ &=\frac{\cos{\left(x \right)}\cdot (-4)}{\sin^{2} x}\\ &=-4\frac{1}{\sin{\left(x \right)}}\cdot \frac{\cos{\left(x \right)}}{\sin{\left(x \right)}}\\ &=- 4 \cot{\left(x \right)} \csc{\left(x \right)}.\end{aligned}
$$

```json
{
  "version": "leibniz-quotient-2026-10-14-v1",
  "template": "q-340335",
  "profile": "fragment",
  "bank_profile": "fragment",
  "seed": 111,
  "parameters": {
    "a": 4,
    "b": 7
  },
  "mathematical_fingerprint": "88814529dc108c436a325479514d0502a0658f3d2b04ac4c332eaece86b5350c",
  "content_fingerprint": "eca2d977661746ca049d5ab004957f880cf7538802e3f67ea5c1b260144c9d17",
  "source_ids": [
    "q-340335"
  ],
  "source_basis": 2275,
  "source_lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1",
  "evidence_only": false,
  "eligible_for_learning": true,
  "authored_rating": false,
  "authored_solution": false,
  "presentation_repairs": [
    "normalize captured function macros/unicode",
    "correct f(x)/dy mismatch to y"
  ],
  "domain": "\\sin{\\left(x \\right)} !=0",
  "plot_rating": "none",
  "sympy_version": "1.14.0",
  "math_format": "course-academy-tex-v1"
}
```
