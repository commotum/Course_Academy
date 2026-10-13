# Source originals and generated variants

Raw originals are evidence only. Generated source variants below use explicitly repaired profiles; defaults and blanks are authored.

## Original q-65163

**unrated (original difficulty absent) · raw source evidence · source_q-65163**

Simplify the trigonometric expression $\cos^{3} θ + \cos θ\sin^{2} θ$.
- $-2\cos^{2} θ$
- $2\cos θ$
- $\cos θ$
- $-\cos θ$
- $\cos^{2} θ$

Original correct designation: **absent**.

### Generated repaired variant {'angle': '\\alpha', 'swap': False}

**easy · repaired source · source_q-65163**

Simplify the trigonometric expression $\cos^{3}{\alpha} + \cos{\alpha}\sin^{2}{\alpha}$.
- $\cos{\alpha}$ **(correct)**
- $-2\cos^{2}{\alpha}$
- $2\cos{\alpha}$
- $\cos^{2}{\alpha}$
- $-\cos{\alpha}$

First, we factor the expression:

$$
\sin^{2}{\alpha}\cos{\alpha}+\cos^{3}{\alpha}=\cos{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\cos{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =\cos{\alpha}\cdot 1 \\  & =\cos{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
\sin^{2}{\alpha}\cos{\alpha}+\cos^{3}{\alpha}=\cos{\alpha}.
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': True}

**easy · repaired source · source_q-65163**

Simplify the trigonometric expression $\sin^{3}{\alpha} + \sin{\alpha}\cos^{2}{\alpha}$.
- $\sin^{2}{\alpha}$
- $-\sin{\alpha}$
- $-2\sin^{2}{\alpha}$
- $\sin{\alpha}$ **(correct)**
- $2\sin{\alpha}$

First, we factor the expression:

$$
\sin^{3}{\alpha}+\sin{\alpha}\cos^{2}{\alpha}=\sin{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\sin{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =\sin{\alpha}\cdot 1 \\  & =\sin{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
\sin^{3}{\alpha}+\sin{\alpha}\cos^{2}{\alpha}=\sin{\alpha}.
$$

## Original q-65193

**unrated (original difficulty absent) · raw source evidence · source_q-65193**

Simplify the trigonometric expression $\sin^{2} x\cos^{3} x + \sin^{4} x\cos x$.
- $\sin^{2} x + 1$
- $\sin x\cos x$
- $\sin^{2} x + \cos x$
- $\sin^{2} x\cos x$
- $\sin x - \cos x$

Original correct designation: **absent**.

### Generated repaired variant {'angle': '\\alpha', 'swap': False}

**easy · repaired source · source_q-65193**

Simplify the trigonometric expression $\sin^{2}{\alpha}\cos^{3}{\alpha} + \sin^{4}{\alpha}\cos{\alpha}$.
- $\sin^{2}{\alpha} + \cos{\alpha}$
- $\sin^{2}{\alpha} + 1$
- $\sin{\alpha}\cos{\alpha}$
- $\sin{\alpha} - \cos{\alpha}$
- $\sin^{2}{\alpha}\cos{\alpha}$ **(correct)**

First, we factor the expression:

$$
\sin^{4}{\alpha}\cos{\alpha}+\sin^{2}{\alpha}\cos^{3}{\alpha}=\sin^{2}{\alpha}\cos{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\sin^{2}{\alpha}\cos{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =\sin^{2}{\alpha}\cos{\alpha}\cdot 1 \\  & =\sin^{2}{\alpha}\cos{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
\sin^{4}{\alpha}\cos{\alpha}+\sin^{2}{\alpha}\cos^{3}{\alpha}=\sin^{2}{\alpha}\cos{\alpha}.
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': True}

**easy · repaired source · source_q-65193**

Simplify the trigonometric expression $\cos^{2}{\alpha}\sin^{3}{\alpha} + \cos^{4}{\alpha}\sin{\alpha}$.
- $\cos{\alpha} - \sin{\alpha}$
- $\cos^{2}{\alpha}\sin{\alpha}$ **(correct)**
- $\cos^{2}{\alpha} + 1$
- $\cos^{2}{\alpha} + \sin{\alpha}$
- $\cos{\alpha}\sin{\alpha}$

First, we factor the expression:

$$
\sin^{3}{\alpha}\cos^{2}{\alpha}+\sin{\alpha}\cos^{4}{\alpha}=\sin{\alpha}\cos^{2}{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\sin{\alpha}\cos^{2}{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =\sin{\alpha}\cos^{2}{\alpha}\cdot 1 \\  & =\sin{\alpha}\cos^{2}{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
\sin^{3}{\alpha}\cos^{2}{\alpha}+\sin{\alpha}\cos^{4}{\alpha}=\sin{\alpha}\cos^{2}{\alpha}.
$$

## Original q-119362

**easy · raw source evidence · source_q-119362**

Simplify the trigonometric expression ${cos}^{3}⁡\theta {sin}^{2}⁡\theta +{cos}^{5}⁡\theta .$
- $2+{cos}^{3}⁡\theta $
- $-{cos}^{3}⁡\theta $
- $2{cos}^{3}⁡\theta $
- ${cos}^{3}⁡\theta $ **(correct)**
- ${cos}^{3}⁡\theta +1$

First, we factor the expression:

$$
{cos}^{3}⁡\theta {sin}^{2}⁡\theta +{cos}^{5}⁡\theta ={cos}^{3}⁡\theta ({sin}^{2}⁡\theta +{cos}^{2}⁡\theta )
$$

Then, we use ${sin}^{2}⁡\theta +{cos}^{2}⁡\theta =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}{cos}^{2}⁡\theta ({sin}^{2}⁡\theta +{cos}^{2}⁡\theta ) & ={cos}^{3}⁡\theta \cdot 1 \\  & ={cos}^{3}⁡\theta \end{aligned}
$$

Hence, we conclude that

$$
{cos}^{3}⁡\theta {sin}^{2}⁡\theta +{cos}^{5}⁡\theta ={cos}^{3}⁡\theta .
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': False}

**easy · repaired source · source_q-119362**

Simplify the trigonometric expression $\cos^{3}{\alpha} \sin^{2}{\alpha} +\cos^{5}{\alpha} .$
- $2\cos^{3}{\alpha} $
- $2+\cos^{3}{\alpha} $
- $-\cos^{3}{\alpha} $
- $\cos^{3}{\alpha} +1$
- $\cos^{3}{\alpha} $ **(correct)**

First, we factor the expression:

$$
\cos^{3}{\alpha} \sin^{2}{\alpha} +\cos^{5}{\alpha} =\cos^{3}{\alpha} (\sin^{2}{\alpha} +\cos^{2}{\alpha} )
$$

Then, we use $\sin^{2}{\alpha} +\cos^{2}{\alpha} =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\cos^{3}{\alpha} (\sin^{2}{\alpha} +\cos^{2}{\alpha} ) & =\cos^{3}{\alpha} \cdot 1 \\  & =\cos^{3}{\alpha} \end{aligned}
$$

Hence, we conclude that

$$
\cos^{3}{\alpha} \sin^{2}{\alpha} +\cos^{5}{\alpha} =\cos^{3}{\alpha} .
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': True}

**easy · repaired source · source_q-119362**

Simplify the trigonometric expression $\sin^{3}{\alpha} \cos^{2}{\alpha} +\sin^{5}{\alpha} .$
- $\sin^{3}{\alpha} +1$
- $\sin^{3}{\alpha} $ **(correct)**
- $2+\sin^{3}{\alpha} $
- $2\sin^{3}{\alpha} $
- $-\sin^{3}{\alpha} $

First, we factor the expression:

$$
\sin^{3}{\alpha} \cos^{2}{\alpha} +\sin^{5}{\alpha} =\sin^{3}{\alpha} (\cos^{2}{\alpha} +\sin^{2}{\alpha} )
$$

Then, we use $\cos^{2}{\alpha} +\sin^{2}{\alpha} =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\sin^{3}{\alpha} (\cos^{2}{\alpha} +\sin^{2}{\alpha} ) & =\sin^{3}{\alpha} \cdot 1 \\  & =\sin^{3}{\alpha} \end{aligned}
$$

Hence, we conclude that

$$
\sin^{3}{\alpha} \cos^{2}{\alpha} +\sin^{5}{\alpha} =\sin^{3}{\alpha} .
$$

## Original q-119367

**moderate · raw source evidence · source_q-119367**

Simplify the trigonometric expression $2\operatorname{sin}⁡\theta -{cos}^{3}⁡\theta -\operatorname{cos}⁡\theta {sin}^{2}⁡\theta .$
- $\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta $
- $2\operatorname{sin}⁡\theta \operatorname{cos}⁡\theta $
- $2\operatorname{sin}⁡\theta -1$
- $2\operatorname{sin}⁡\theta +\operatorname{cos}⁡\theta $
- $2\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta $ **(correct)**

First, we factor the expression:

$$
2\operatorname{sin}⁡\theta -{cos}^{3}⁡\theta -\operatorname{cos}⁡\theta {sin}^{2}⁡\theta =2\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )
$$

Then, we use ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}2\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta ({cos}^{2}⁡\theta +{sin}^{2}⁡\theta ) & =2\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta \cdot 1 \\  & =2\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta \end{aligned}
$$

Hence, we conclude that

$$
2\operatorname{sin}⁡\theta -{cos}^{3}⁡\theta -\operatorname{cos}⁡\theta {sin}^{2}⁡\theta =2\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta .
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': False}

**moderate · repaired source · source_q-119367**

Simplify the trigonometric expression $2\sin{\alpha} -\cos^{3}{\alpha} -\cos{\alpha} \sin^{2}{\alpha} .$
- $2\sin{\alpha} -1$
- $\sin{\alpha} -\cos{\alpha} $
- $2\sin{\alpha} \cos{\alpha} $
- $2\sin{\alpha} -\cos{\alpha} $ **(correct)**
- $2\sin{\alpha} +\cos{\alpha} $

First, we factor the expression:

$$
2\sin{\alpha} -\cos^{3}{\alpha} -\cos{\alpha} \sin^{2}{\alpha} =2\sin{\alpha} -\cos{\alpha} (\cos^{2}{\alpha} +\sin^{2}{\alpha} )
$$

Then, we use $\cos^{2}{\alpha} +\sin^{2}{\alpha} =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}2\sin{\alpha} -\cos{\alpha} (\cos^{2}{\alpha} +\sin^{2}{\alpha} ) & =2\sin{\alpha} -\cos{\alpha} \cdot 1 \\  & =2\sin{\alpha} -\cos{\alpha} \end{aligned}
$$

Hence, we conclude that

$$
2\sin{\alpha} -\cos^{3}{\alpha} -\cos{\alpha} \sin^{2}{\alpha} =2\sin{\alpha} -\cos{\alpha} .
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': True}

**moderate · repaired source · source_q-119367**

Simplify the trigonometric expression $2\cos{\alpha} -\sin^{3}{\alpha} -\sin{\alpha} \cos^{2}{\alpha} .$
- $2\cos{\alpha} -\sin{\alpha} $ **(correct)**
- $2\cos{\alpha} +\sin{\alpha} $
- $\cos{\alpha} -\sin{\alpha} $
- $2\cos{\alpha} -1$
- $2\cos{\alpha} \sin{\alpha} $

First, we factor the expression:

$$
2\cos{\alpha} -\sin^{3}{\alpha} -\sin{\alpha} \cos^{2}{\alpha} =2\cos{\alpha} -\sin{\alpha} (\sin^{2}{\alpha} +\cos^{2}{\alpha} )
$$

Then, we use $\sin^{2}{\alpha} +\cos^{2}{\alpha} =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}2\cos{\alpha} -\sin{\alpha} (\sin^{2}{\alpha} +\cos^{2}{\alpha} ) & =2\cos{\alpha} -\sin{\alpha} \cdot 1 \\  & =2\cos{\alpha} -\sin{\alpha} \end{aligned}
$$

Hence, we conclude that

$$
2\cos{\alpha} -\sin^{3}{\alpha} -\sin{\alpha} \cos^{2}{\alpha} =2\cos{\alpha} -\sin{\alpha} .
$$

## Original q-119371

**moderate · raw source evidence · source_q-119371**

Simplify the trigonometric expression ${sin}^{3}⁡\theta +\operatorname{sin}⁡\theta {cos}^{2}⁡\theta +\operatorname{sin}⁡\theta .$
- $2\operatorname{sin}⁡\theta $ **(correct)**
- $1-\operatorname{sin}⁡\theta $
- $\operatorname{sin}⁡\theta +1$
- $2\operatorname{sin}⁡\theta +1$
- $\operatorname{sin}⁡\theta $

First, we factor the expression:

$$
{sin}^{3}⁡\theta +\operatorname{sin}⁡\theta {cos}^{2}⁡\theta +\operatorname{sin}⁡\theta =\operatorname{sin}⁡\theta ({sin}^{2}⁡\theta +{cos}^{2}⁡\theta )+\operatorname{sin}⁡\theta 
$$

Then, we use ${sin}^{2}⁡\theta +{cos}^{2}⁡\theta =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\operatorname{sin}⁡\theta ({sin}^{2}⁡\theta +{cos}^{2}⁡\theta )+\operatorname{sin}⁡\theta  & =\operatorname{sin}⁡\theta \cdot 1+\operatorname{sin}⁡\theta  \\  & =\operatorname{sin}⁡\theta +\operatorname{sin}⁡\theta  \\  & =2\operatorname{sin}⁡\theta \end{aligned}
$$

Hence, we conclude that

$$
{sin}^{3}⁡\theta +\operatorname{sin}⁡\theta {cos}^{2}⁡\theta +\operatorname{sin}⁡\theta =2\operatorname{sin}⁡\theta .
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': False}

**moderate · repaired source · source_q-119371**

Simplify the trigonometric expression $\sin^{3}{\alpha} +\sin{\alpha} \cos^{2}{\alpha} +\sin{\alpha} .$
- $\sin{\alpha} +1$
- $2\sin{\alpha} $ **(correct)**
- $1-\sin{\alpha} $
- $\sin{\alpha} $
- $2\sin{\alpha} +1$

First, we factor the expression:

$$
\sin^{3}{\alpha} +\sin{\alpha} \cos^{2}{\alpha} +\sin{\alpha} =\sin{\alpha} (\sin^{2}{\alpha} +\cos^{2}{\alpha} )+\sin{\alpha} 
$$

Then, we use $\sin^{2}{\alpha} +\cos^{2}{\alpha} =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\sin{\alpha} (\sin^{2}{\alpha} +\cos^{2}{\alpha} )+\sin{\alpha}  & =\sin{\alpha} \cdot 1+\sin{\alpha}  \\  & =\sin{\alpha} +\sin{\alpha}  \\  & =2\sin{\alpha} \end{aligned}
$$

Hence, we conclude that

$$
\sin^{3}{\alpha} +\sin{\alpha} \cos^{2}{\alpha} +\sin{\alpha} =2\sin{\alpha} .
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': True}

**moderate · repaired source · source_q-119371**

Simplify the trigonometric expression $\cos^{3}{\alpha} +\cos{\alpha} \sin^{2}{\alpha} +\cos{\alpha} .$
- $\cos{\alpha} $
- $2\cos{\alpha} +1$
- $2\cos{\alpha} $ **(correct)**
- $\cos{\alpha} +1$
- $1-\cos{\alpha} $

First, we factor the expression:

$$
\cos^{3}{\alpha} +\cos{\alpha} \sin^{2}{\alpha} +\cos{\alpha} =\cos{\alpha} (\cos^{2}{\alpha} +\sin^{2}{\alpha} )+\cos{\alpha} 
$$

Then, we use $\cos^{2}{\alpha} +\sin^{2}{\alpha} =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\cos{\alpha} (\cos^{2}{\alpha} +\sin^{2}{\alpha} )+\cos{\alpha}  & =\cos{\alpha} \cdot 1+\cos{\alpha}  \\  & =\cos{\alpha} +\cos{\alpha}  \\  & =2\cos{\alpha} \end{aligned}
$$

Hence, we conclude that

$$
\cos^{3}{\alpha} +\cos{\alpha} \sin^{2}{\alpha} +\cos{\alpha} =2\cos{\alpha} .
$$

## Original q-65229

**easy · raw source evidence · source_q-65229**

Simplify the trigonometric expression $\operatorname{sin}⁡\theta {cos}^{2}⁡\theta +{sin}^{3}⁡\theta .$
- $\operatorname{sin}⁡\theta +1$
- $\operatorname{sin}⁡\theta -1$
- $2\operatorname{sin}⁡\theta $
- $\operatorname{sin}⁡\theta $ **(correct)**
- $-\operatorname{sin}⁡\theta $

First, we factor $\operatorname{sin}⁡\theta $ from the expression:

$$
\operatorname{sin}⁡\theta {cos}^{2}⁡\theta +{sin}^{3}⁡\theta =\operatorname{sin}⁡\theta \cdot ({sin}^{2}⁡\theta +{cos}^{2}⁡\theta )
$$

Then, we use ${cos}^{2}⁡\theta +{sin}^{2}⁡\theta =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\operatorname{sin}⁡\theta \cdot ({sin}^{2}⁡\theta +{cos}^{2}) & =\operatorname{sin}⁡\theta \cdot 1 \\  & =\operatorname{sin}⁡\theta \end{aligned}
$$

We conclude that

$$
\operatorname{sin}⁡\theta {cos}^{2}⁡\theta +{sin}^{3}⁡\theta =\operatorname{sin}⁡\theta .
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': False}

**easy · repaired source · source_q-65229**

Simplify the trigonometric expression $\sin{\alpha} \cos^{2}{\alpha} +\sin^{3}{\alpha} .$
- $2\sin{\alpha} $
- $\sin{\alpha} +1$
- $\sin{\alpha} -1$
- $-\sin{\alpha} $
- $\sin{\alpha} $ **(correct)**

First, we factor $\sin{\alpha} $ from the expression:

$$
\sin{\alpha} \cos^{2}{\alpha} +\sin^{3}{\alpha} =\sin{\alpha} \cdot (\sin^{2}{\alpha} +\cos^{2}{\alpha} )
$$

Then, we use $\cos^{2}{\alpha} +\sin^{2}{\alpha} =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\sin{\alpha} \cdot (\sin^{2}{\alpha} +\cos^{2}{\alpha} ) & =\sin{\alpha} \cdot 1 \\  & =\sin{\alpha} \end{aligned}
$$

We conclude that

$$
\sin{\alpha} \cos^{2}{\alpha} +\sin^{3}{\alpha} =\sin{\alpha} .
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': True}

**easy · repaired source · source_q-65229**

Simplify the trigonometric expression $\cos{\alpha} \sin^{2}{\alpha} +\cos^{3}{\alpha} .$
- $-\cos{\alpha} $
- $\cos{\alpha} $ **(correct)**
- $\cos{\alpha} +1$
- $2\cos{\alpha} $
- $\cos{\alpha} -1$

First, we factor $\cos{\alpha} $ from the expression:

$$
\cos{\alpha} \sin^{2}{\alpha} +\cos^{3}{\alpha} =\cos{\alpha} \cdot (\cos^{2}{\alpha} +\sin^{2}{\alpha} )
$$

Then, we use $\sin^{2}{\alpha} +\cos^{2}{\alpha} =1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\cos{\alpha} \cdot (\cos^{2}{\alpha} +\sin^{2}{\alpha} ) & =\cos{\alpha} \cdot 1 \\  & =\cos{\alpha} \end{aligned}
$$

We conclude that

$$
\cos{\alpha} \sin^{2}{\alpha} +\cos^{3}{\alpha} =\cos{\alpha} .
$$

## Original q-65241

**easy · raw source evidence · source_q-65241**

Simplify the trigonometric expression $\operatorname{sin}⁡x{cos}^{3}⁡x+{sin}^{3}⁡x\operatorname{cos}⁡x.$
- $-\operatorname{sin}⁡x\operatorname{cos}⁡x$
- $2\operatorname{sin}⁡x\operatorname{cos}⁡x-1$
- $2\operatorname{sin}⁡x\operatorname{cos}⁡x$
- $\operatorname{sin}⁡x\operatorname{cos}⁡x$ **(correct)**
- $-2\operatorname{sin}⁡x\operatorname{cos}⁡x+1$

First, we factor $\operatorname{sin}⁡x\operatorname{cos}⁡x$ from the expression:

$$
\operatorname{sin}⁡x{cos}^{3}⁡x+{sin}^{3}⁡x\operatorname{cos}⁡x=\operatorname{sin}⁡x\operatorname{cos}⁡x\cdot ({cos}^{2}⁡x+{sin}^{2}⁡x)
$$

Then, we use ${cos}^{2}⁡x+{sin}^{2}⁡x=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\operatorname{sin}⁡x\operatorname{cos}⁡x\cdot ({sin}^{2}⁡x+{cos}^{2}⁡x) & =\operatorname{sin}⁡x\operatorname{cos}⁡x\cdot 1 \\  & =\operatorname{sin}⁡x\operatorname{cos}⁡x\end{aligned}
$$

We conclude that

$$
\operatorname{sin}⁡x{cos}^{3}⁡x+{sin}^{3}⁡x\operatorname{cos}⁡x=\operatorname{sin}⁡x\operatorname{cos}⁡x.
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': False}

**easy · repaired source · source_q-65241**

Simplify the trigonometric expression $\sin{\alpha}\cos^{3}{\alpha}+\sin^{3}{\alpha}\cos{\alpha}.$
- $2\sin{\alpha}\cos{\alpha}$
- $-\sin{\alpha}\cos{\alpha}$
- $2\sin{\alpha}\cos{\alpha}-1$
- $-2\sin{\alpha}\cos{\alpha}+1$
- $\sin{\alpha}\cos{\alpha}$ **(correct)**

First, we factor $\sin{\alpha}\cos{\alpha}$ from the expression:

$$
\sin{\alpha}\cos^{3}{\alpha}+\sin^{3}{\alpha}\cos{\alpha}=\sin{\alpha}\cos{\alpha}\cdot (\cos^{2}{\alpha}+\sin^{2}{\alpha})
$$

Then, we use $\cos^{2}{\alpha}+\sin^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\sin{\alpha}\cos{\alpha}\cdot (\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =\sin{\alpha}\cos{\alpha}\cdot 1 \\  & =\sin{\alpha}\cos{\alpha}\end{aligned}
$$

We conclude that

$$
\sin{\alpha}\cos^{3}{\alpha}+\sin^{3}{\alpha}\cos{\alpha}=\sin{\alpha}\cos{\alpha}.
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': True}

**easy · repaired source · source_q-65241**

Simplify the trigonometric expression $\cos{\alpha}\sin^{3}{\alpha}+\cos^{3}{\alpha}\sin{\alpha}.$
- $-2\cos{\alpha}\sin{\alpha}+1$
- $\cos{\alpha}\sin{\alpha}$ **(correct)**
- $-\cos{\alpha}\sin{\alpha}$
- $2\cos{\alpha}\sin{\alpha}$
- $2\cos{\alpha}\sin{\alpha}-1$

First, we factor $\cos{\alpha}\sin{\alpha}$ from the expression:

$$
\cos{\alpha}\sin^{3}{\alpha}+\cos^{3}{\alpha}\sin{\alpha}=\cos{\alpha}\sin{\alpha}\cdot (\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\cos{\alpha}\sin{\alpha}\cdot (\cos^{2}{\alpha}+\sin^{2}{\alpha}) & =\cos{\alpha}\sin{\alpha}\cdot 1 \\  & =\cos{\alpha}\sin{\alpha}\end{aligned}
$$

We conclude that

$$
\cos{\alpha}\sin^{3}{\alpha}+\cos^{3}{\alpha}\sin{\alpha}=\cos{\alpha}\sin{\alpha}.
$$

## Original q-65242

**easy · raw source evidence · source_q-65242**

Simplify the trigonometric expression ${sin}^{5}⁡x+{cos}^{2}⁡x{sin}^{3}⁡x.$
- ${sin}^{2}⁡x$
- $-{sin}^{3}⁡x$
- ${sin}^{3}⁡x$ **(correct)**
- $\operatorname{sin}⁡x$
- $-{sin}^{2}⁡x$

First, we factor ${sin}^{3}⁡x$ from the expression:

$$
{sin}^{5}⁡x+{cos}^{2}⁡x{sin}^{3}⁡x={sin}^{3}⁡x\cdot ({sin}^{2}⁡x+{cos}^{2}⁡x)
$$

Then, we use ${sin}^{2}⁡x+{cos}^{2}⁡x=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}{sin}^{3}⁡x\cdot ({sin}^{2}⁡x+{cos}^{2}⁡x) & ={sin}^{3}⁡x\cdot 1 \\  & ={sin}^{3}⁡x\end{aligned}
$$

We conclude that

$$
{sin}^{5}⁡x+{cos}^{2}⁡x{sin}^{3}⁡x={sin}^{3}⁡x.
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': False}

**easy · repaired source · source_q-65242**

Simplify the trigonometric expression $\sin^{5}{\alpha}+\cos^{2}{\alpha}\sin^{3}{\alpha}.$
- $\sin^{3}{\alpha}$ **(correct)**
- $\sin^{2}{\alpha}$
- $-\sin^{3}{\alpha}$
- $-\sin^{2}{\alpha}$
- $\sin{\alpha}$

First, we factor $\sin^{3}{\alpha}$ from the expression:

$$
\sin^{5}{\alpha}+\cos^{2}{\alpha}\sin^{3}{\alpha}=\sin^{3}{\alpha}\cdot (\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\sin^{3}{\alpha}\cdot (\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =\sin^{3}{\alpha}\cdot 1 \\  & =\sin^{3}{\alpha}\end{aligned}
$$

We conclude that

$$
\sin^{5}{\alpha}+\cos^{2}{\alpha}\sin^{3}{\alpha}=\sin^{3}{\alpha}.
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': True}

**easy · repaired source · source_q-65242**

Simplify the trigonometric expression $\cos^{5}{\alpha}+\sin^{2}{\alpha}\cos^{3}{\alpha}.$
- $-\cos^{2}{\alpha}$
- $\cos{\alpha}$
- $\cos^{2}{\alpha}$
- $\cos^{3}{\alpha}$ **(correct)**
- $-\cos^{3}{\alpha}$

First, we factor $\cos^{3}{\alpha}$ from the expression:

$$
\cos^{5}{\alpha}+\sin^{2}{\alpha}\cos^{3}{\alpha}=\cos^{3}{\alpha}\cdot (\cos^{2}{\alpha}+\sin^{2}{\alpha})
$$

Then, we use $\cos^{2}{\alpha}+\sin^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\cos^{3}{\alpha}\cdot (\cos^{2}{\alpha}+\sin^{2}{\alpha}) & =\cos^{3}{\alpha}\cdot 1 \\  & =\cos^{3}{\alpha}\end{aligned}
$$

We conclude that

$$
\cos^{5}{\alpha}+\sin^{2}{\alpha}\cos^{3}{\alpha}=\cos^{3}{\alpha}.
$$

## Original q-65243

**moderate · raw source evidence · source_q-65243**

Simplify the trigonometric expression ${sin}^{2}⁡x{cos}^{2}⁡x+{cos}^{4}⁡x+{sin}^{2}⁡x.$
- $1$ **(correct)**
- $0$
- $2$
- $-2$
- $-1$

First, we factor ${cos}^{2}⁡x$  from the first two terms:

$$
{sin}^{2}⁡x{cos}^{2}⁡x+{cos}^{4}⁡x+{sin}^{2}⁡x={cos}^{2}⁡x\cdot ({sin}^{2}⁡x+{cos}^{2}⁡x)+{sin}^{2}⁡x
$$

Then, we use ${cos}^{2}⁡x+{sin}^{2}⁡x=1$ to simplify the given expression:

$$
\begin{aligned}{cos}^{2}⁡x\cdot ({sin}^{2}⁡x+{cos}^{2}⁡x)+{sin}^{2}⁡x & ={cos}^{2}⁡x\cdot 1+{sin}^{2}⁡x \\  & ={cos}^{2}⁡x+{sin}^{2}⁡x \\  & =1\end{aligned}
$$

We conclude that

$$
{sin}^{2}⁡x{cos}^{2}⁡x+{cos}^{4}⁡x+{sin}^{2}⁡x=1.
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': False}

**moderate · repaired source · source_q-65243**

Simplify the trigonometric expression $\sin^{2}{\alpha}\cos^{2}{\alpha}+\cos^{4}{\alpha}+\sin^{2}{\alpha}.$
- $2$
- $1$ **(correct)**
- $0$
- $-1$
- $-2$

First, we factor $\cos^{2}{\alpha}$  from the first two terms:

$$
\sin^{2}{\alpha}\cos^{2}{\alpha}+\cos^{4}{\alpha}+\sin^{2}{\alpha}=\cos^{2}{\alpha}\cdot (\sin^{2}{\alpha}+\cos^{2}{\alpha})+\sin^{2}{\alpha}
$$

Then, we use $\cos^{2}{\alpha}+\sin^{2}{\alpha}=1$ to simplify the given expression:

$$
\begin{aligned}\cos^{2}{\alpha}\cdot (\sin^{2}{\alpha}+\cos^{2}{\alpha})+\sin^{2}{\alpha} & =\cos^{2}{\alpha}\cdot 1+\sin^{2}{\alpha} \\  & =\cos^{2}{\alpha}+\sin^{2}{\alpha} \\  & =1\end{aligned}
$$

We conclude that

$$
\sin^{2}{\alpha}\cos^{2}{\alpha}+\cos^{4}{\alpha}+\sin^{2}{\alpha}=1.
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': True}

**moderate · repaired source · source_q-65243**

Simplify the trigonometric expression $\cos^{2}{\alpha}\sin^{2}{\alpha}+\sin^{4}{\alpha}+\cos^{2}{\alpha}.$
- $-1$
- $-2$
- $1$ **(correct)**
- $2$
- $0$

First, we factor $\sin^{2}{\alpha}$  from the first two terms:

$$
\cos^{2}{\alpha}\sin^{2}{\alpha}+\sin^{4}{\alpha}+\cos^{2}{\alpha}=\sin^{2}{\alpha}\cdot (\cos^{2}{\alpha}+\sin^{2}{\alpha})+\cos^{2}{\alpha}
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the given expression:

$$
\begin{aligned}\sin^{2}{\alpha}\cdot (\cos^{2}{\alpha}+\sin^{2}{\alpha})+\cos^{2}{\alpha} & =\sin^{2}{\alpha}\cdot 1+\cos^{2}{\alpha} \\  & =\sin^{2}{\alpha}+\cos^{2}{\alpha} \\  & =1\end{aligned}
$$

We conclude that

$$
\cos^{2}{\alpha}\sin^{2}{\alpha}+\sin^{4}{\alpha}+\cos^{2}{\alpha}=1.
$$

## Original q-72711

**moderate · raw source evidence · source_q-72711**

Simplify the trigonometric expression $\operatorname{sin}⁡x+2{cos}^{3}⁡x+2{sin}^{2}⁡x\operatorname{cos}⁡x.$
- $\operatorname{sin}⁡x+3\operatorname{cos}⁡x$
- $\operatorname{sin}⁡x-\operatorname{cos}⁡x$
- $-2\operatorname{sin}⁡x+\operatorname{cos}⁡x$
- $-\operatorname{sin}⁡x+\operatorname{cos}⁡x$
- $\operatorname{sin}⁡x+2\operatorname{cos}⁡x$ **(correct)**

First, we factor the expression:

$$
\operatorname{sin}⁡x+2{cos}^{3}⁡x+2{sin}^{2}⁡x\operatorname{cos}⁡x=\operatorname{sin}⁡x+2\operatorname{cos}⁡x({cos}^{2}⁡x+{sin}^{2}⁡x)
$$

Then, we use ${cos}^{2}⁡x+{sin}^{2}⁡x=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\operatorname{sin}⁡x+2\operatorname{cos}⁡x({cos}^{2}⁡x+{sin}^{2}⁡x) & =\operatorname{sin}⁡x+2\operatorname{cos}⁡x\cdot 1 \\  & =\operatorname{sin}⁡x+2\operatorname{cos}⁡x\end{aligned}
$$

Hence, we conclude that

$$
\operatorname{sin}⁡x+2{cos}^{3}⁡x+2{sin}^{2}⁡x\operatorname{cos}⁡x=\operatorname{sin}⁡x+2\operatorname{cos}⁡x.
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': False}

**moderate · repaired source · source_q-72711**

Simplify the trigonometric expression $\sin{\alpha}+2\cos^{3}{\alpha}+2\sin^{2}{\alpha}\cos{\alpha}.$
- $-2\sin{\alpha}+\cos{\alpha}$
- $\sin{\alpha}+3\cos{\alpha}$
- $\sin{\alpha}-\cos{\alpha}$
- $\sin{\alpha}+2\cos{\alpha}$ **(correct)**
- $-\sin{\alpha}+\cos{\alpha}$

First, we factor the expression:

$$
\sin{\alpha}+2\cos^{3}{\alpha}+2\sin^{2}{\alpha}\cos{\alpha}=\sin{\alpha}+2\cos{\alpha}(\cos^{2}{\alpha}+\sin^{2}{\alpha})
$$

Then, we use $\cos^{2}{\alpha}+\sin^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\sin{\alpha}+2\cos{\alpha}(\cos^{2}{\alpha}+\sin^{2}{\alpha}) & =\sin{\alpha}+2\cos{\alpha}\cdot 1 \\  & =\sin{\alpha}+2\cos{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
\sin{\alpha}+2\cos^{3}{\alpha}+2\sin^{2}{\alpha}\cos{\alpha}=\sin{\alpha}+2\cos{\alpha}.
$$

### Generated repaired variant {'angle': '\\alpha', 'swap': True}

**moderate · repaired source · source_q-72711**

Simplify the trigonometric expression $\cos{\alpha}+2\sin^{3}{\alpha}+2\cos^{2}{\alpha}\sin{\alpha}.$
- $\cos{\alpha}+2\sin{\alpha}$ **(correct)**
- $-\cos{\alpha}+\sin{\alpha}$
- $\cos{\alpha}+3\sin{\alpha}$
- $-2\cos{\alpha}+\sin{\alpha}$
- $\cos{\alpha}-\sin{\alpha}$

First, we factor the expression:

$$
\cos{\alpha}+2\sin^{3}{\alpha}+2\cos^{2}{\alpha}\sin{\alpha}=\cos{\alpha}+2\sin{\alpha}(\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}\cos{\alpha}+2\sin{\alpha}(\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =\cos{\alpha}+2\sin{\alpha}\cdot 1 \\  & =\cos{\alpha}+2\sin{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
\cos{\alpha}+2\sin^{3}{\alpha}+2\cos^{2}{\alpha}\sin{\alpha}=\cos{\alpha}+2\sin{\alpha}.
$$

## Generated authored :question.difficulty/easy :answer-field.type/radio

**easy · authored extension · one_gcf**

Simplify the trigonometric expression $-5\sin^{3}{\alpha}\cos{\alpha}-5\sin{\alpha}\cos^{3}{\alpha}.$
- $5\sin{\alpha}\cos{\alpha}$
- $-10\sin{\alpha}\cos{\alpha}$
- $-5\sin{\alpha}\cos{\alpha}$ **(correct)**
- $-5\sin^{3}{\alpha}\cos{\alpha}+5\sin{\alpha}\cos^{3}{\alpha}$
- $-5\sin^{3}{\alpha}\cos{\alpha}-5\sin{\alpha}\cos^{3}{\alpha}+5\sin{\alpha}\cos{\alpha}$

First, we factor the expression:

$$
-5\sin^{3}{\alpha}\cos{\alpha}-5\sin{\alpha}\cos^{3}{\alpha}=-5\sin{\alpha}\cos{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}-5\sin{\alpha}\cos{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =-5\sin{\alpha}\cos{\alpha}\cdot 1 \\  & =-5\sin{\alpha}\cos{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
-5\sin^{3}{\alpha}\cos{\alpha}-5\sin{\alpha}\cos^{3}{\alpha}=-5\sin{\alpha}\cos{\alpha}.
$$

## Generated authored :question.difficulty/easy :answer-field.type/radio

**easy · authored extension · one_gcf**

Simplify the trigonometric expression $-\sin^{5}{\theta}-\sin^{3}{\theta}\cos^{2}{\theta}.$
- $\sin^{3}{\theta}$
- $-\sin^{5}{\theta}-\sin^{3}{\theta}\cos^{2}{\theta}+\sin^{3}{\theta}$
- $-\sin^{5}{\theta}+\sin^{3}{\theta}\cos^{2}{\theta}$
- $-\sin^{3}{\theta}$ **(correct)**
- $-2\sin^{3}{\theta}$

First, we factor the expression:

$$
-\sin^{5}{\theta}-\sin^{3}{\theta}\cos^{2}{\theta}=-\sin^{3}{\theta}\cdot(\sin^{2}{\theta}+\cos^{2}{\theta})
$$

Then, we use $\sin^{2}{\theta}+\cos^{2}{\theta}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}-\sin^{3}{\theta}\cdot(\sin^{2}{\theta}+\cos^{2}{\theta}) & =-\sin^{3}{\theta}\cdot 1 \\  & =-\sin^{3}{\theta}\end{aligned}
$$

Hence, we conclude that

$$
-\sin^{5}{\theta}-\sin^{3}{\theta}\cos^{2}{\theta}=-\sin^{3}{\theta}.
$$

## Generated authored :question.difficulty/easy :answer-field.type/blank

**easy · authored extension · one_gcf**

Simplify the trigonometric expression $-4\sin^{3}{\theta}-4\sin{\theta}\cos^{2}{\theta}.$

{{selection}}
- $-4\sin{\theta}$ **(correct)**

First, we factor the expression:

$$
-4\sin^{3}{\theta}-4\sin{\theta}\cos^{2}{\theta}=-4\sin{\theta}\cdot(\sin^{2}{\theta}+\cos^{2}{\theta})
$$

Then, we use $\sin^{2}{\theta}+\cos^{2}{\theta}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}-4\sin{\theta}\cdot(\sin^{2}{\theta}+\cos^{2}{\theta}) & =-4\sin{\theta}\cdot 1 \\  & =-4\sin{\theta}\end{aligned}
$$

Hence, we conclude that

$$
-4\sin^{3}{\theta}-4\sin{\theta}\cos^{2}{\theta}=-4\sin{\theta}.
$$

## Generated authored :question.difficulty/easy :answer-field.type/blank

**easy · authored extension · one_gcf**

Simplify the trigonometric expression $3\sin^{3}{\alpha}\cos^{2}{\alpha}+3\sin{\alpha}\cos^{4}{\alpha}.$

{{selection}}
- $3\sin{\alpha}\cos^{2}{\alpha}$ **(correct)**

First, we factor the expression:

$$
3\sin^{3}{\alpha}\cos^{2}{\alpha}+3\sin{\alpha}\cos^{4}{\alpha}=3\sin{\alpha}\cos^{2}{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}3\sin{\alpha}\cos^{2}{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =3\sin{\alpha}\cos^{2}{\alpha}\cdot 1 \\  & =3\sin{\alpha}\cos^{2}{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
3\sin^{3}{\alpha}\cos^{2}{\alpha}+3\sin{\alpha}\cos^{4}{\alpha}=3\sin{\alpha}\cos^{2}{\alpha}.
$$

## Generated authored :question.difficulty/moderate :answer-field.type/radio

**moderate · authored extension · gcf_residual**

Simplify the trigonometric expression $3\sin^{3}{\alpha}+3\sin{\alpha}\cos^{2}{\alpha}+\sin{\alpha}.$
- $-4\sin{\alpha}$
- $2\sin{\alpha}$
- $4\sin{\alpha}$ **(correct)**
- $5\sin{\alpha}$
- $3\sin^{3}{\alpha}-3\sin{\alpha}\cos^{2}{\alpha}+\sin{\alpha}$

First, we factor the expression:

$$
3\sin^{3}{\alpha}+3\sin{\alpha}\cos^{2}{\alpha}+\sin{\alpha}=3\sin{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})+\sin{\alpha}
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}3\sin{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})+\sin{\alpha} & =3\sin{\alpha}\cdot 1+\sin{\alpha} \\  & =3\sin{\alpha}+\sin{\alpha} \\  & =4\sin{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
3\sin^{3}{\alpha}+3\sin{\alpha}\cos^{2}{\alpha}+\sin{\alpha}=4\sin{\alpha}.
$$

## Generated authored :question.difficulty/moderate :answer-field.type/radio

**moderate · authored extension · gcf_residual**

Simplify the trigonometric expression $-3\sin^{2}{\alpha}\cos{\alpha}-3\cos^{3}{\alpha}-3\sin{\alpha}.$
- $-3\sin{\alpha}+3\cos{\alpha}$
- $-3\sin^{2}{\alpha}\cos{\alpha}-3\sin{\alpha}+3\cos^{3}{\alpha}$
- $-3\sin{\alpha}-6\cos{\alpha}$
- $-3\sin{\alpha}-3\cos{\alpha}$ **(correct)**
- $3\sin{\alpha}-3\cos{\alpha}$

First, we factor the expression:

$$
-3\sin^{2}{\alpha}\cos{\alpha}-3\cos^{3}{\alpha}-3\sin{\alpha}=-3\cos{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})-3\sin{\alpha}
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}-3\cos{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})-3\sin{\alpha} & =-3\cos{\alpha}\cdot 1-3\sin{\alpha} \\  & =-3\cos{\alpha}-3\sin{\alpha} \\  & =-3\sin{\alpha}-3\cos{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
-3\sin^{2}{\alpha}\cos{\alpha}-3\cos^{3}{\alpha}-3\sin{\alpha}=-3\sin{\alpha}-3\cos{\alpha}.
$$

## Generated authored :question.difficulty/moderate :answer-field.type/blank

**moderate · authored extension · gcf_residual**

Simplify the trigonometric expression $-3\sin^{3}{x}-3\sin{x}\cos^{2}{x}+2\cos{x}.$

{{selection}}
- $-3\sin{x}+2\cos{x}$ **(correct)**

First, we factor the expression:

$$
-3\sin^{3}{x}-3\sin{x}\cos^{2}{x}+2\cos{x}=-3\sin{x}\cdot(\sin^{2}{x}+\cos^{2}{x})+2\cos{x}
$$

Then, we use $\sin^{2}{x}+\cos^{2}{x}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}-3\sin{x}\cdot(\sin^{2}{x}+\cos^{2}{x})+2\cos{x} & =-3\sin{x}\cdot 1+2\cos{x} \\  & =-3\sin{x}+2\cos{x} \\  & =-3\sin{x}+2\cos{x}\end{aligned}
$$

Hence, we conclude that

$$
-3\sin^{3}{x}-3\sin{x}\cos^{2}{x}+2\cos{x}=-3\sin{x}+2\cos{x}.
$$

## Generated authored :question.difficulty/moderate :answer-field.type/blank

**moderate · authored extension · gcf_residual**

Simplify the trigonometric expression $4\sin^{2}{x}\cos{x}+4\cos^{3}{x}-\cos{x}.$

{{selection}}
- $3\cos{x}$ **(correct)**

First, we factor the expression:

$$
4\sin^{2}{x}\cos{x}+4\cos^{3}{x}-\cos{x}=4\cos{x}\cdot(\sin^{2}{x}+\cos^{2}{x})-\cos{x}
$$

Then, we use $\sin^{2}{x}+\cos^{2}{x}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}4\cos{x}\cdot(\sin^{2}{x}+\cos^{2}{x})-\cos{x} & =4\cos{x}\cdot 1-\cos{x} \\  & =4\cos{x}-\cos{x} \\  & =3\cos{x}\end{aligned}
$$

Hence, we conclude that

$$
4\sin^{2}{x}\cos{x}+4\cos^{3}{x}-\cos{x}=3\cos{x}.
$$

## Generated authored :question.difficulty/hard :answer-field.type/radio

**hard · authored extension · two_gcf**

Simplify the trigonometric expression $3\sin^{5}{\alpha}+3\sin^{3}{\alpha}\cos^{2}{\alpha}-4\sin^{2}{\alpha}\cos^{3}{\alpha}-4\cos^{5}{\alpha}.$
- $-3\sin^{3}{\alpha}-4\cos^{3}{\alpha}$
- $3\sin^{3}{\alpha}+4\cos^{3}{\alpha}$
- $3\sin^{3}{\alpha}-4\cos^{3}{\alpha}$ **(correct)**
- $3\sin^{3}{\alpha}-4\sin^{2}{\alpha}\cos^{3}{\alpha}+4\cos^{5}{\alpha}$
- $3\sin^{5}{\alpha}-3\sin^{3}{\alpha}\cos^{2}{\alpha}-4\cos^{3}{\alpha}$

First, we factor the expression:

$$
3\sin^{5}{\alpha}+3\sin^{3}{\alpha}\cos^{2}{\alpha}-4\sin^{2}{\alpha}\cos^{3}{\alpha}-4\cos^{5}{\alpha}=3\sin^{3}{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})-4\cos^{3}{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}3\sin^{3}{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})-4\cos^{3}{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =3\sin^{3}{\alpha}\cdot 1-4\cos^{3}{\alpha}\cdot 1 \\  & =3\sin^{3}{\alpha}-4\cos^{3}{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
3\sin^{5}{\alpha}+3\sin^{3}{\alpha}\cos^{2}{\alpha}-4\sin^{2}{\alpha}\cos^{3}{\alpha}-4\cos^{5}{\alpha}=3\sin^{3}{\alpha}-4\cos^{3}{\alpha}.
$$

## Generated authored :question.difficulty/hard :answer-field.type/radio

**hard · authored extension · two_gcf**

Simplify the trigonometric expression $-3\sin^{3}{x}-3\sin{x}\cos^{2}{x}+\sin^{2}{x}\cos^{3}{x}+\cos^{5}{x}.$
- $3\sin{x}+\cos^{3}{x}$
- $-3\sin^{3}{x}+3\sin{x}\cos^{2}{x}+\cos^{3}{x}$
- $\sin^{2}{x}\cos^{3}{x}-3\sin{x}-\cos^{5}{x}$
- $-3\sin{x}+\cos^{3}{x}$ **(correct)**
- $-3\sin{x}-\cos^{3}{x}$

First, we factor the expression:

$$
-3\sin^{3}{x}-3\sin{x}\cos^{2}{x}+\sin^{2}{x}\cos^{3}{x}+\cos^{5}{x}=-3\sin{x}\cdot(\sin^{2}{x}+\cos^{2}{x})+\cos^{3}{x}\cdot(\sin^{2}{x}+\cos^{2}{x})
$$

Then, we use $\sin^{2}{x}+\cos^{2}{x}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}-3\sin{x}\cdot(\sin^{2}{x}+\cos^{2}{x})+\cos^{3}{x}\cdot(\sin^{2}{x}+\cos^{2}{x}) & =-3\sin{x}\cdot 1+\cos^{3}{x}\cdot 1 \\  & =-3\sin{x}+\cos^{3}{x}\end{aligned}
$$

Hence, we conclude that

$$
-3\sin^{3}{x}-3\sin{x}\cos^{2}{x}+\sin^{2}{x}\cos^{3}{x}+\cos^{5}{x}=-3\sin{x}+\cos^{3}{x}.
$$

## Generated authored :question.difficulty/hard :answer-field.type/blank

**hard · authored extension · two_gcf**

Simplify the trigonometric expression $-3\sin^{5}{\theta}-3\sin^{3}{\theta}\cos^{2}{\theta}-3\sin^{2}{\theta}\cos{\theta}-3\cos^{3}{\theta}.$

{{selection}}
- $-3\sin^{3}{\theta}-3\cos{\theta}$ **(correct)**

First, we factor the expression:

$$
-3\sin^{5}{\theta}-3\sin^{3}{\theta}\cos^{2}{\theta}-3\sin^{2}{\theta}\cos{\theta}-3\cos^{3}{\theta}=-3\sin^{3}{\theta}\cdot(\sin^{2}{\theta}+\cos^{2}{\theta})-3\cos{\theta}\cdot(\sin^{2}{\theta}+\cos^{2}{\theta})
$$

Then, we use $\sin^{2}{\theta}+\cos^{2}{\theta}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}-3\sin^{3}{\theta}\cdot(\sin^{2}{\theta}+\cos^{2}{\theta})-3\cos{\theta}\cdot(\sin^{2}{\theta}+\cos^{2}{\theta}) & =-3\sin^{3}{\theta}\cdot 1-3\cos{\theta}\cdot 1 \\  & =-3\sin^{3}{\theta}-3\cos{\theta}\end{aligned}
$$

Hence, we conclude that

$$
-3\sin^{5}{\theta}-3\sin^{3}{\theta}\cos^{2}{\theta}-3\sin^{2}{\theta}\cos{\theta}-3\cos^{3}{\theta}=-3\sin^{3}{\theta}-3\cos{\theta}.
$$

## Generated authored :question.difficulty/hard :answer-field.type/blank

**hard · authored extension · two_gcf**

Simplify the trigonometric expression $4\sin^{3}{\alpha}+4\sin{\alpha}\cos^{2}{\alpha}+4\sin^{2}{\alpha}\cos{\alpha}+4\cos^{3}{\alpha}.$

{{selection}}
- $4\sin{\alpha}+4\cos{\alpha}$ **(correct)**

First, we factor the expression:

$$
4\sin^{3}{\alpha}+4\sin{\alpha}\cos^{2}{\alpha}+4\sin^{2}{\alpha}\cos{\alpha}+4\cos^{3}{\alpha}=4\sin{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})+4\cos{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})
$$

Then, we use $\sin^{2}{\alpha}+\cos^{2}{\alpha}=1$ to simplify the expression in the parentheses:

$$
\begin{aligned}4\sin{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha})+4\cos{\alpha}\cdot(\sin^{2}{\alpha}+\cos^{2}{\alpha}) & =4\sin{\alpha}\cdot 1+4\cos{\alpha}\cdot 1 \\  & =4\sin{\alpha}+4\cos{\alpha}\end{aligned}
$$

Hence, we conclude that

$$
4\sin^{3}{\alpha}+4\sin{\alpha}\cos^{2}{\alpha}+4\sin^{2}{\alpha}\cos{\alpha}+4\cos^{3}{\alpha}=4\sin{\alpha}+4\cos{\alpha}.
$$
