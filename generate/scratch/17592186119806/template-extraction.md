# Template extraction

Solve p*a+c*x=b using componentwise scalar multiplication, subtraction, and
division by nonzero c. The supplied objects are a and b; x is the requested
vector, or its two named components are combined by the observed sum/difference.
The vector dimension, coefficient pair, operation, response shape, radio contract,
and ordered symbolic isolation stages remain fixed within each source profile.
Positive, signed-negative, and reverse-subtraction isolation presentations are
preserved rather than collapsed into a new solution sequence.

Observed profiles are enumerated below; original prompt, solution, field, and
every original option remain in source.json. choice-recipes.json maps every
choice to its source field, UUID, exact value, and complete observed offset recipe.
No profiles are pooled. Each profile must reproduce all five choices and the
correct designation at its original parameters.

Variable slots:

- `scale` is the uniform integer dilation k in {1,2,3} applied to a and b.
  x=(b-p*a)/c is computed first. Every supplied, intermediate, solved and choice
  vector changes coherently; integrality and source sign/zero patterns survive.
  k=1 replays the source. k=2,3 are conservative same-method generalizations.
  The upper bound keeps the same small-integer component workload; larger
  numbers are excluded by policy, not asserted mathematically impossible.
- `target` is absent for vector answers. For scalar answers it selects any two
  distinct eligible coordinates using the source operation. Sum pairs are
  unordered; difference pairs are ordered. All prompt names, final solution
  names, arithmetic and bank correct values derive from this slot. The number
  of coordinates requested and the full vector-solving stages stay fixed.
  Original target locations are retained for replay; location repetition alone
  is not a constraint. All target slots are covered exhaustively, including a
  changed-target case with all other supplied data held constant.

Bank recipe: requested_value + k*(source_option-source_correct_value).
At the source target this is exactly k*source_option. At another eligible target,
it translates the entire observed offset profile to the new correct value.
This target translation is an authored conservative extension. The underlying
mistake represented by a random-looking source offset is unresolved; no error
intent or feedback is invented. Every option is retained, and no bank mixing
occurs. Nonzero k preserves unique offsets and one correct option.

One concrete source-worded solution is rendered for each instance. All numeric
matrices are derived through the same dilation, and scalar final arithmetic
handles signed terms and parentheses. There are no branch/domain issues: finite
real integer vectors and nonzero scalar coefficients yield a unique x.

Mathematical novelty hashes the displayed supplied coefficients and relevant
coordinate data, with the operation. Scalar-query unused coordinates, target
labels, profile IDs, answer order, UUIDs and seeds cannot create new tasks.
All 156 declared tasks are distinct; 13 are source tasks, leaving 143 bounded
variants before considering learner presentations/reservations.

## q-105157

{"source": "q-105157", "template": "vector-4-positive-division", "profile": "q-105157", "coefficients": [2, 4], "a": [5, -3, 1, 6], "b": [14, 2, -2, 0], "x": [1, 2, -1, -3], "dimension": 4, "target": null, "response": "vector", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": null}, "plot_rating": "none"}

Find $x$, if $2a+4x=b$ and

$$
a=\begin{bmatrix}5 \\ -3 \\ 1 \\ 6\end{bmatrix},\,b=\begin{bmatrix}14 \\ 2 \\ -2 \\ 0\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get

$$
\begin{aligned}2a+4x & =b \\ 4x & =b-2a \\ x & =\frac{1}{4}(b-2a) \\ x & =\frac{1}{4}(\begin{bmatrix}14 \\ 2 \\ -2 \\ 0\end{bmatrix}-2\begin{bmatrix}5 \\ -3 \\ 1 \\ 6\end{bmatrix}) \\ x & =\frac{1}{4}\begin{bmatrix}4 \\ 8 \\ -4 \\ -12\end{bmatrix} \\ x & =\begin{bmatrix}1 \\ 2 \\ -1 \\ -3\end{bmatrix}.\end{aligned}
$$

## q-105159

{"source": "q-105159", "template": "vector-3-positive-division", "profile": "q-105159", "coefficients": [4, 3], "a": [3, -1, -4], "b": [3, 2, -1], "x": [-3, 2, 5], "dimension": 3, "target": null, "response": "vector", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": null}, "plot_rating": "none"}

Find $x$, if $4a+3x=b$ and

$$
a=\begin{bmatrix}3 \\ -1 \\ -4\end{bmatrix},\,b=\begin{bmatrix}3 \\ 2 \\ -1\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get

$$
\begin{aligned}4a+3x & =b \\ 3x & =b-4a \\ x & =\frac{1}{3}(b-4a) \\ x & =\frac{1}{3}(\begin{bmatrix}3 \\ 2 \\ -1\end{bmatrix}-4\begin{bmatrix}3 \\ -1 \\ -4\end{bmatrix}) \\ x & =\frac{1}{3}\begin{bmatrix}-9 \\ 6 \\ 15\end{bmatrix} \\ x & =\begin{bmatrix}-3 \\ 2 \\ 5\end{bmatrix}.\end{aligned}
$$

## q-105160

{"source": "q-105160", "template": "sum-3-signed-division", "profile": "q-105160", "coefficients": [3, -5], "a": [-6, 5, 4], "b": [-13, 5, -3], "x": [-1, 2, 3], "dimension": 3, "target": [0, 1, "+"], "response": "scalar", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": [0, 1, "+"]}, "plot_rating": "none"}

Find the value of ${x}_{1}+{x}_{2}$ given that $3a-5x=b$ and

$$
a=\begin{bmatrix}-6 \\ 5 \\ 4\end{bmatrix},\,x=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix},\,b=\begin{bmatrix}-13 \\ 5 \\ -3\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get

$$
\begin{aligned}3a-5x & =b \\ -5x & =b-3a \\ x & =-\frac{1}{5}(b-3a) \\ x & =-\frac{1}{5}(\begin{bmatrix}-13 \\ 5 \\ -3\end{bmatrix}-3\begin{bmatrix}-6 \\ 5 \\ 4\end{bmatrix}) \\ x & =-\frac{1}{5}\begin{bmatrix}5 \\ -10 \\ -15\end{bmatrix} \\ x & =\begin{bmatrix}-1 \\ 2 \\ 3\end{bmatrix}.\end{aligned}
$$

Therefore, ${x}_{1}+{x}_{2}=-1+2=1.$

## q-105161

{"source": "q-105161", "template": "difference-4-positive-division", "profile": "q-105161", "coefficients": [7, 4], "a": [1, 0, -1, 2], "b": [-1, 4, -3, -6], "x": [-2, 1, 1, -5], "dimension": 4, "target": [0, 1, "-"], "response": "scalar", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": [0, 1, "-"]}, "plot_rating": "none"}

Find the value of ${x}_{1}-{x}_{2}$ given that $7a+4x=b$ and

$$
a=\begin{bmatrix}1 \\ 0 \\ -1 \\ 2\end{bmatrix},\,x=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix},\,b=\begin{bmatrix}-1 \\ 4 \\ -3 \\ -6\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get

$$
\begin{aligned}7a+4x & =b \\ 4x & =b-7a \\ x & =\frac{1}{4}(b-7a) \\ x & =\frac{1}{4}(\begin{bmatrix}-1 \\ 4 \\ -3 \\ -6\end{bmatrix}-7\begin{bmatrix}1 \\ 0 \\ -1 \\ 2\end{bmatrix}) \\ x & =\frac{1}{4}\begin{bmatrix}-8 \\ 4 \\ 4 \\ -20\end{bmatrix} \\ x & =\begin{bmatrix}-2 \\ 1 \\ 1 \\ -5\end{bmatrix}.\end{aligned}
$$

Therefore, ${x}_{1}-{x}_{2}=-2-1=-3.$

## q-34052

{"source": "q-34052", "template": "sum-4-signed-division", "profile": "q-34052", "coefficients": [3, -5], "a": [0, -1, -4, -2], "b": [15, 2, -22, -1], "x": [-3, -1, 2, -1], "dimension": 4, "target": [0, 1, "+"], "response": "scalar", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": [0, 1, "+"]}, "plot_rating": "none"}

Find the value of ${x}_{1}+{x}_{2}$ given that $3a-5x=b$ and

$$
a=\begin{bmatrix}0 \\ -1 \\ -4 \\ -2\end{bmatrix},\,x=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix},\,b=\begin{bmatrix}15 \\ 2 \\ -22 \\ -1\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get

$$
\begin{aligned}3a-5x & =b \\ -5x & =b-3a \\ x & =-\frac{1}{5}(b-3a) \\ x & =-\frac{1}{5}(\begin{bmatrix}15 \\ 2 \\ -22 \\ -1\end{bmatrix}-3\begin{bmatrix}0 \\ -1 \\ -4 \\ -2\end{bmatrix}) \\ x & =-\frac{1}{5}\begin{bmatrix}15 \\ 5 \\ -10 \\ 5\end{bmatrix} \\ x & =\begin{bmatrix}-3 \\ -1 \\ 2 \\ -1\end{bmatrix}.\end{aligned}
$$

Therefore,${x}_{1}+{x}_{2}=-3-1=-4.$

## q-34247

{"source": "q-34247", "template": "sum-4-positive-division", "profile": "q-34247", "coefficients": [3, 2], "a": [4, -2, -1, 0], "b": [24, 8, -15, -2], "x": [6, 7, -6, -1], "dimension": 4, "target": [0, 1, "+"], "response": "scalar", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": [0, 1, "+"]}, "plot_rating": "none"}

Find the value of ${x}_{1}+{x}_{2}$ given that $3a+2x=b$ and

$$
a=\begin{bmatrix}4 \\ -2 \\ -1 \\ 0\end{bmatrix},\,x=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix},\,b=\begin{bmatrix}24 \\ 8 \\ -15 \\ -2\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get

$$
\begin{aligned}3a+2x & =b \\ 2x & =b-3a \\ x & =\frac{1}{2}(b-3a) \\ x & =\frac{1}{2}(\begin{bmatrix}24 \\ 8 \\ -15 \\ -2\end{bmatrix}-3\begin{bmatrix}4 \\ -2 \\ -1 \\ 0\end{bmatrix}) \\ x & =\frac{1}{2}\begin{bmatrix}12 \\ 14 \\ -12 \\ -2\end{bmatrix} \\ x & =\begin{bmatrix}6 \\ 7 \\ -6 \\ -1\end{bmatrix}.\end{aligned}
$$

Therefore, ${x}_{1}+{x}_{2}=6+7=13.$

## q-34248

{"source": "q-34248", "template": "vector-3-positive-division", "profile": "q-34248", "coefficients": [4, 6], "a": [-3, 0, -7], "b": [24, -6, -10], "x": [6, -1, 3], "dimension": 3, "target": null, "response": "vector", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": null}, "plot_rating": "none"}

Find $x$, if $4a+6x=b$ and

$$
a=\begin{bmatrix}-3 \\ 0 \\ -7\end{bmatrix},\,b=\begin{bmatrix}24 \\ -6 \\ -10\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get

$$
\begin{aligned}4a+6x & =b \\ 6x & =b-4a \\ x & =\frac{1}{6}(b-4a) \\ x & =\frac{1}{6}(\begin{bmatrix}24 \\ -6 \\ -10\end{bmatrix}-4\begin{bmatrix}-3 \\ 0 \\ -7\end{bmatrix}) \\ x & =\frac{1}{6}\begin{bmatrix}36 \\ -6 \\ 18\end{bmatrix} \\ x & =\begin{bmatrix}6 \\ -1 \\ 3\end{bmatrix}.\end{aligned}
$$

## q-34598

{"source": "q-34598", "template": "difference-3-positive-division", "profile": "q-34598", "coefficients": [4, 3], "a": [3, 3, 3], "b": [18, -15, -9], "x": [2, -9, -7], "dimension": 3, "target": [0, 1, "-"], "response": "scalar", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": [0, 1, "-"]}, "plot_rating": "none"}

Find the value of ${x}_{1}-{x}_{2}$ given that  $4a+3x=b$ and

$$
a=\begin{bmatrix}3 \\ 3 \\ 3\end{bmatrix},\,x=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix},\,b=\begin{bmatrix}18 \\ -15 \\ -9\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get

$$
\begin{aligned}4a+3x & =b \\ 3x & =b-4a \\ x & =\frac{1}{3}(b-4a) \\ x & =\frac{1}{3}(\begin{bmatrix}18 \\ -15 \\ -9\end{bmatrix}-4\begin{bmatrix}3 \\ 3 \\ 3\end{bmatrix}) \\ x & =\frac{1}{3}\begin{bmatrix}6 \\ -27 \\ -21\end{bmatrix} \\ x & =\begin{bmatrix}2 \\ -9 \\ -7\end{bmatrix}.\end{aligned}
$$

Therefore, ${x}_{1}-{x}_{2}=2-(-9)=11.$

## q-34601

{"source": "q-34601", "template": "difference-4-signed-division", "profile": "q-34601", "coefficients": [6, -2], "a": [4, -2, 6, 8], "b": [8, -6, -12, -10], "x": [8, -3, 24, 29], "dimension": 4, "target": [2, 3, "-"], "response": "scalar", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": [2, 3, "-"]}, "plot_rating": "none"}

Find the value of ${x}_{3}-{x}_{4}$ given that  $6a-2x=b$ and

$$
a=\begin{bmatrix}4 \\ -2 \\ 6 \\ 8\end{bmatrix},\,x=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix},\,b=\begin{bmatrix}8 \\ -6 \\ -12 \\ -10\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get

$$
\begin{aligned}6a-2x & =b \\ -2x & =b-6a \\ x & =-\frac{1}{2}(b-6a) \\ x & =-\frac{1}{2}(\begin{bmatrix}8 \\ -6 \\ -12 \\ -10\end{bmatrix}-6\begin{bmatrix}4 \\ -2 \\ 6 \\ 8\end{bmatrix}) \\ x & =-\frac{1}{2}\begin{bmatrix}-16 \\ 6 \\ -48 \\ -58\end{bmatrix} \\ x & =\begin{bmatrix}8 \\ -3 \\ 24 \\ 29\end{bmatrix}.\end{aligned}
$$

Therefore, ${x}_{3}-{x}_{4}=24-29=-5.$

## q-73931

{"source": "q-73931", "template": "vector-3-positive-division", "profile": "q-73931", "coefficients": [3, 2], "a": [1, 2, -5], "b": [9, -4, -3], "x": [3, -5, 6], "dimension": 3, "target": null, "response": "vector", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": null}, "plot_rating": "none"}

Find $x$, if $3a+2x=b$ and

$$
a=\begin{bmatrix}1 \\ 2 \\ -5\end{bmatrix},\,b=\begin{bmatrix}9 \\ -4 \\ -3\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get  

$$
\begin{aligned}3a+2x & =b \\ 2x & =b-3a \\ x & =\frac{1}{2}(b-3a) \\ x & =\frac{1}{2}(\begin{bmatrix}9 \\ -4 \\ -3\end{bmatrix}-3\begin{bmatrix}1 \\ 2 \\ -5\end{bmatrix}) \\ x & =\frac{1}{2}\begin{bmatrix}6 \\ -10 \\ 12\end{bmatrix} \\ x & =\begin{bmatrix}3 \\ -5 \\ 6\end{bmatrix}.\end{aligned}
$$

## q-73933

{"source": "q-73933", "template": "vector-3-reverse-subtraction", "profile": "q-73933", "coefficients": [5, -3], "a": [3, -6, 9], "b": [12, 18, -6], "x": [1, -16, 17], "dimension": 3, "target": null, "response": "vector", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": null}, "plot_rating": "none"}

Find $x$, if $5a-3x=b$ and

$$
a=\begin{bmatrix}3 \\ -6 \\ 9\end{bmatrix},\,b=\begin{bmatrix}12 \\ 18 \\ -6\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get  

$$
\begin{aligned}5a-3x & =b \\ 3x & =5a-b \\ x & =\frac{1}{3}(5a-b) \\ x & =\frac{1}{3}(5\begin{bmatrix}3 \\ -6 \\ 9\end{bmatrix}-\begin{bmatrix}12 \\ 18 \\ -6\end{bmatrix}) \\ x & =\frac{1}{3}\begin{bmatrix}3 \\ -48 \\ 51\end{bmatrix} \\ x & =\begin{bmatrix}1 \\ -16 \\ 17\end{bmatrix}.\end{aligned}
$$

## q-73936

{"source": "q-73936", "template": "vector-3-reverse-subtraction", "profile": "q-73936", "coefficients": [4, -2], "a": [2, 6, -4], "b": [12, -6, -10], "x": [-2, 15, -3], "dimension": 3, "target": null, "response": "vector", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": null}, "plot_rating": "none"}

Find $x$, if $4a-2x=b$ and

$$
a=\begin{bmatrix}2 \\ 6 \\ -4\end{bmatrix},\,b=\begin{bmatrix}12 \\ -6 \\ -10\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get  

$$
\begin{aligned}4a-2x & =b \\ 2x & =4a-b \\ x & =\frac{1}{2}(4a-b) \\ x & =\frac{1}{2}(4\begin{bmatrix}2 \\ 6 \\ -4\end{bmatrix}-\begin{bmatrix}12 \\ -6 \\ -10\end{bmatrix}) \\ x & =\frac{1}{2}\begin{bmatrix}-4 \\ 30 \\ -6\end{bmatrix} \\ x & =\begin{bmatrix}-2 \\ 15 \\ -3\end{bmatrix}.\end{aligned}
$$

## q-73937

{"source": "q-73937", "template": "vector-3-positive-division", "profile": "q-73937", "coefficients": [2, 5], "a": [5, -5, -10], "b": [15, -30, 20], "x": [1, -4, 8], "dimension": 3, "target": null, "response": "vector", "number_features": "exact integral vectors; mixed signs and zero components as observed; nonzero coefficient", "original_parameters": {"scale": 1, "target": null}, "plot_rating": "none"}

Find $x$, if $2a+5x=b$ and

$$
a=\begin{bmatrix}5 \\ -5 \\ -10\end{bmatrix},\,b=\begin{bmatrix}15 \\ -30 \\ 20\end{bmatrix}.
$$

Using the properties of addition/subtraction and scalar multiplication of vectors to isolate $x,$ we get

$$
\begin{aligned}2a+5x & =b \\ 5x & =b-2a \\ x & =\frac{1}{5}(b-2a) \\ x & =\frac{1}{5}(\begin{bmatrix}15 \\ -30 \\ 20\end{bmatrix}-2\begin{bmatrix}5 \\ -5 \\ -10\end{bmatrix}) \\ x & =\frac{1}{5}\begin{bmatrix}5 \\ -20 \\ 40\end{bmatrix} \\ x & =\begin{bmatrix}1 \\ -4 \\ 8\end{bmatrix}.\end{aligned}
$$

