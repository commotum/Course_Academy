# Classification

Frozen math database basis 1356; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Capture copied byte-for-byte to source.json.

Nine practice questions, all easy, one radio field keyed selection with five math choices and a designated correct option. No missing attributes or duplicate assessment fields. Nine distinct worked-solution/value families; one full observed bank per family. No plots in these sources or the canonical example. Moderate and hard have no observed practice labels.

| Source | Family | Prompt | Worked stages |

|---|---|---|---|

| q-94588 | sine_power | If $f(x,y)=\operatorname{sin}⁡({x}^{2}+y)$ and $y={x}^{2},$ compute $\frac{\text{d}f}{\text{d}x}.$ | 5 display blocks; 8 approximate equation rows |

| q-95121 | x_log_sum | If $f(x,y)=x\operatorname{ln}⁡(x+y)$ and $y={x}^{2},$ compute $\frac{\text{d}f}{\text{d}x}.$ | 5 display blocks; 9 approximate equation rows |

| q-170670 | y_log_power | If $f(x,y)=y\operatorname{ln}⁡({x}^{2}+1)$ and $y={x}^{2}+1,$ compute $\frac{\text{d}f}{\text{d}x}.$ | 5 display blocks; 7 approximate equation rows |

| q-95088 | reciprocal_exp | If $f(x,y)=\frac{1}{x+y}$ and $y={e}^{-x},$ compute $\frac{\text{d}f}{\text{d}x}.$ | 5 display blocks; 7 approximate equation rows |

| q-95114 | radial_power | If $f(x,y)=\sqrt{{x}^{2}+{y}^{2}}$ and $y={x}^{3},$ compute $\frac{\text{d}f}{\text{d}x}.$ | 5 display blocks; 14 approximate equation rows |

| q-95117 | x_exp_sine | If $f(x,y)=x{e}^{y}$ and $y=\operatorname{sin}⁡x,$ compute $\frac{\text{d}f}{\text{d}x}.$ | 5 display blocks; 7 approximate equation rows |

| q-95118 | polynomial_sine | If $f(x,y)={x}^{2}+yx$ and $y=\operatorname{sin}⁡x,$ compute $\frac{\text{d}f}{\text{d}x}.$ | 5 display blocks; 6 approximate equation rows |

| q-95119 | cosine_reciprocal | If $f(x,y)=\operatorname{cos}⁡({x}^{2}+y)$ and $y=\frac{1}{x},$ compute $\frac{\text{d}f}{\text{d}x}.$ | 5 display blocks; 8 approximate equation rows |

| q-95122 | quotient_power | If $f(x,y)=\frac{y}{x+1}$ and $y={x}^{3},$ compute $\frac{\text{d}f}{\text{d}x}.$ | 5 display blocks; 10 approximate equation rows |



## Curriculum boundary

The captured activity route, followed through first-step and next, is Introduction → general one-independent-variable KP → A Special Case of the Multivariable Chain Rule → this KP → two-independent-variable tutorial/KP → generalized chain rule/KP. The preceding tutorial explicitly reduces dx/dx to 1 and yields df/dx=f_x+f_y y′. The canonical e-8257 is 2 sqrt(x+y), y=cos x. This generator keeps x independent, f(x,y), and exactly one dependency y(x). It introduces no independent t, s, z or general tree diagrams. Incoming topic edges include Computing Partial Derivatives Using the Rules of Differentiation and double-angle formulas. Product rule, elementary power/trig/exp/log derivatives and substitution are already used by the captured examples.

Moderate (authored): two source-adjacent families, a x²+bxy with y=c sin(kx), and a x exp(by) with y=c sin(kx). Nonzero signed |a,b,c|≤4 and k=2..4 require nonunit-frequency and coefficient tracking through both partials, substitution and the two contributions.

Hard (authored): the same polynomial/exponential outer families, with y=c x sin(kx) or c x cos(kx). This adds exactly one two-term product derivative in y′ and distributes both terms through the unchanged special-case rule. The level is an equal-workload design, not an inferred original label. Every hard instance requires both factors; c≠0 and k≥2 prevent collapse.

Easy: nine observed families, scaled whole f by signed nonzero integer |a|≤5. The added scalar changes every partial/final stage but never creates a new template or skill. Each source family retains its original dependency and its entire original chain.

No plots: steps 5/7 are explicitly not applicable; no rendering environment or raster measurements are claimed.
