# Template extraction

Backbone: three supplied points with fixed roles (target P and reference endpoints A,B); compute m1=(By-Ay)/(Bx-Ax), take the negative reciprocal m=-1/m1, use P in point-slope form, expand and isolate y. Blank response is precisely the right-hand side after supplied y=; radio responses are entire line equations. Shared instructional prose is copied from each original family and all concrete point references are updated together. Source arithmetic/sign/evaluation stages are preserved even when successive equations are algebraically equal. Layout and mathematics are checked separately; normalized source displays remain exact at all recoverable originals.

Slots and constraints: A=(a,b) independently sampled in [-6,6]^2; nonzero dx,dy independently in [-8,8], B=A+(dx,dy). Both endpoint roles vary, reference orientation varies, and endpoints remain distinct. P_y independently [-8,8]. P_x=0 for explicit easy intercept families; P_x is a nonzero integer in [-8,8] for translated moderate/hard and the separately labeled missing-graph repair. Every occurrence in prompt, negative-reciprocal display, point-slope stages, key and whole bank derives from those slots. Explicit replay parameters permit integer coordinates of absolute magnitude at most 100. Original parameters are retained even when outside normal random samples. Real plane, no branch/domain restrictions beyond finite nonzero reference slopes. Intercepts 0 and 1 are eligible and tested. Moving only reference endpoints along a common orientation is not mathematical novelty; canonical task identity collapses that alias.

Whole-profile mapping: choose a source alias/profile before sampling. For every observed option y=t0*x+b0, with original perpendicular slope m0 and original target (h0,k0), define multiplier=t0/m0 and residual=b0-k0+t0*h0. At new slope m and target (h,k), t=multiplier*m and b=k-t*h+residual. Emit the full line y=t*x+b. Correct option has multiplier=1,residual=0. This exact equation transport retains every source choice, including compound wrongs and slopes whose psychological explanation is unknown. It is an authored conservative pattern extension, not a claim about learner misconceptions. The complete original banks and exact coefficients appear in choice-ledger.json below. No pooled distractors, first-valid recipes or mixed profiles. Reject the entire sampled instance if any required choices collide or extra answers become correct. Blanks have no distractor profile.

At original parameters, every present observed bank is mathematically matched one-to-one as complete lines up to nonzero scalar; captured correct refs are preserved. q-214038's missing RHS is authored as (5/2)x-20. q-22642's authored correct full equation is y=-(5/6)x+5; its entire captured bank is retained. Their missing solutions are authored using the canonical two-point/negative-reciprocal/point-slope sequence and are never described as captured text. q-167797's captured target (3,-5), correct RHS (1/3)x-6 and solution reference slope -3 support its separate authored textual repair, but not recovery of the original graph. All raw omissions remain omissions in ineligible raw-source-replay.json.

Per-source original descriptions and component mappings follow. A source alias is a runnable exact-replay template argument; grouped family names in classification describe the shared structure. `sourcecases.json` has standard source_id,difficulty,template,parameters,bank_profile keys and original+two changed variants for every alias, plus three examples of each hard alias. `review.md` shows each captured original followed by its normal original/repair and two changed variants.

## q-214038

What is the equation of the line that passes through the point $(6,-5)$ and is perpendicular to the line passing through the points $(2, 5)$ and $(7, 3)$?$y =$
{{field-1}}

Family: `translated-blank-three-slope-rows`. Parameters: `{"P": [6, -5], "A": [2, 5], "B": [7, 3]}`. Source reference slope -2/5, perpendicular slope 5/2, intercept -20. Field key/type: `field-1` / `:answer-field.type/blank`.

Captured RHS: **missing**; authored completion separate.

Captured ordered solution (absence stays absent):

**Missing. Authored completion is separate.**

## q-22642

Find the equation of the line that passes through the point $(0, 5)$ and is perpendicular to the line passing through the points $(-2,-4)$ and $(3, 2)$.

Family: `easy-intercept-radio-three-slope-rows`. Parameters: `{"P": [0, 5], "A": [-2, -4], "B": [3, 2]}`. Source reference slope 6/5, perpendicular slope -5/6, intercept 5. Field key/type: `selection` / `:answer-field.type/radio`.

| Full captured value | Slope multiplier | Incidence residual | Captured correct |
|---|---|---|---|
|`y =-\frac{1}{5}x + 5`|6/25|0|False|
|`y = \frac{6}{5}x + 5`|-36/25|0|False|
|`y =-\frac{6}{5}x + 5`|36/25|0|False|
|`y = \frac{5}{6}x + 5`|-1|0|False|
|`y =-\frac{5}{6}x + 5`|1|0|False|

Captured ordered solution (absence stays absent):

**Missing. Authored completion is separate.**

## q-167797

Write the equation of the line that passes through the point $(3,-5)$ and is perpendicular to $\overset{↔}{AB}.$

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        The slope-intercept form of the equation is $y\,=\,$

                                    
                                
                                    
                            
                                        {{field-1}}

Family: `easy-missing-diagram-text-repair`. Parameters: `{"P": [3, -5], "A": [0, 0], "B": [1, -3]}`. Source reference slope -3, perpendicular slope 1/3, intercept -6. Field key/type: `field-1` / `:answer-field.type/blank`.

Captured RHS: `\frac{1}{3}x-6`.

Captured ordered solution (absence stays absent):

Perpendicular lines have slopes that are negative reciprocals of each other. Therefore, since $\overset{↔}{AB}$ has the slope $m=-3,$ our perpendicular line must have a slope of 

$$
{m}_{1}=-\frac{1}{m}=-\frac{1}{(-3)}=\frac{1}{3}.
$$

So, our perpendicular line has the slope ${m}_{1}=\frac{1}{3}$ and passes through the point $({x}_{1},{y}_{1})=(3,-5).$ 

Finally, using point-slope form and simplifying, we obtain the following equation:

$$
\begin{aligned}y-{y}_{1} & ={m}_{1}(x-{x}_{1}) \\ y-(-5) & =\frac{1}{3}(x-3) \\ y+5 & =\frac{1}{3}x-1 \\ y & =\frac{1}{3}x-6\end{aligned}
$$

## q-103440

Find the equation of the line that passes through the point $(2,3)$ and is perpendicular to the line passing through the points $(1,4)$ and $(-4,6).$

Family: `translated-radio-three-slope-rows`. Parameters: `{"P": [2, 3], "A": [1, 4], "B": [-4, 6]}`. Source reference slope -2/5, perpendicular slope 5/2, intercept -2. Field key/type: `selection` / `:answer-field.type/radio`.

| Full captured value | Slope multiplier | Incidence residual | Captured correct |
|---|---|---|---|
|`y=-\frac{2}{5}x+\frac{19}{5}`|-4/25|0|False|
|`y=\frac{5}{2}x-2`|1|0|True|
|`y=-\frac{5}{2}x+8`|-1|0|False|
|`y=\frac{1}{2}x+2`|1/5|0|False|
|`y=\frac{2}{5}x+\frac{11}{5}`|4/25|0|False|

Captured ordered solution (absence stays absent):

Perpendicular lines have slopes that are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(1,4)$ and $(-4,6):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{6-4}{-4-1} \\  & =-\frac{2}{5}\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (-\frac{2}{5})=-1\,⇒\,m=\frac{5}{2}.
$$

We know that the line passes through the point $(2,3).$ Using point-slope form and simplifying, we obtain the equation of the line:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-3 & =\frac{5}{2}(x-2) \\ y-3 & =\frac{5}{2}x-5 \\ y & =\frac{5}{2}x-2\end{aligned}
$$

## q-103455

Find the equation of the line that passes through the point $(8,-1)$ and is perpendicular to the line passing through the points $(-4,1)$ and $(1,-3).$

Family: `translated-radio-sign-stage`. Parameters: `{"P": [8, -1], "A": [-4, 1], "B": [1, -3]}`. Source reference slope -4/5, perpendicular slope 5/4, intercept -11. Field key/type: `selection` / `:answer-field.type/radio`.

| Full captured value | Slope multiplier | Incidence residual | Captured correct |
|---|---|---|---|
|`y=-\frac{4}{5}x+9`|-16/25|18/5|False|
|`y=\frac{5}{4}x-11`|1|0|True|
|`y=-\frac{5}{2}x+19`|-2|0|False|
|`y=\frac{4}{5}x-9`|16/25|-8/5|False|
|`y=-\frac{5}{4}x+9`|-1|0|False|

Captured ordered solution (absence stays absent):

Perpendicular lines have slopes that are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(-4,1)$ and $(1,-3):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{-3-1}{1-(-4)} \\  & =\frac{-3-1}{1+4} \\  & =-\frac{4}{5}\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (-\frac{4}{5})=-1\,⇒\,m=\frac{5}{4}.
$$

We know that the line passes through the point $(8,-1).$ Using point-slope form and simplifying, we obtain the equation of the line:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-(-1) & =\frac{5}{4}(x-8) \\ y+1 & =\frac{5}{4}x-10 \\ y & =\frac{5}{4}x-11\end{aligned}
$$

## q-215768

What is the equation of the line that passes through the point $(0,4)$ and is perpendicular to the line passing through the points $(-5,1)$ and $(-6,2)?$

$y=$
{{field-1}}

Family: `easy-intercept-blank-five-slope-rows`. Parameters: `{"P": [0, 4], "A": [-5, 1], "B": [-6, 2]}`. Source reference slope -1, perpendicular slope 1, intercept 4. Field key/type: `field-1` / `:answer-field.type/blank`.

Captured RHS: `x+4`.

Captured ordered solution (absence stays absent):

Perpendicular lines have slopes that are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(-5,1)$ and $(-6,2):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{2-1}{-6-(-5)} \\  & =\frac{2-1}{-6+5} \\  & =\frac{1}{-1} \\  & =-1\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (-1)=-1\,⇒\,m=1.
$$

We know that the line passes through the point $(0,4).$ Using point-slope form and simplifying, we obtain the equation of the line in slope-intercept form:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-4 & =1(x-0) \\ y-4 & =x \\ y & =x+4\end{aligned}
$$

## q-23453

Find the equation of the line that passes through the point $(0,-3)$ and is perpendicular to the line passing through the points $(1,7)$ and $(-5,-1).$

Family: `easy-intercept-radio-four-slope-rows`. Parameters: `{"P": [0, -3], "A": [1, 7], "B": [-5, -1]}`. Source reference slope 4/3, perpendicular slope -3/4, intercept -3. Field key/type: `selection` / `:answer-field.type/radio`.

| Full captured value | Slope multiplier | Incidence residual | Captured correct |
|---|---|---|---|
|`y=\frac{7}{3}x-3`|-28/9|0|False|
|`y=-\frac{3}{4}x-3`|1|0|True|
|`y=5x-3`|-20/3|0|False|
|`y=-2x-3`|8/3|0|False|
|`y=\frac{4}{3}x-3`|-16/9|0|False|

Captured ordered solution (absence stays absent):

Perpendicular lines have slopes which are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(1,7)$ and $(-5,-1):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{-1-7}{-5-1} \\  & =\frac{-8}{-6} \\  & =\frac{4}{3}.\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (\frac{4}{3})=-1\,⇒\,m=-\frac{3}{4}.
$$

We know that the line passes through the point $(0,-3).$ Using point-slope form and simplifying, we obtain the equation of the line:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-(-3) & =-\frac{3}{4}(x-0) \\ y+3 & =-\frac{3}{4}x \\ y & =-\frac{3}{4}x-3\end{aligned}
$$

## q-237036

Find the equation of the line that passes through the point $(-5,5)$ and is perpendicular to the line passing through the points $(-4,-3)$ and $(2,3).$

$y=$
{{field-1}}

Family: `translated-blank-difference-and-point-sign`. Parameters: `{"P": [-5, 5], "A": [-4, -3], "B": [2, 3]}`. Source reference slope 1, perpendicular slope -1, intercept 0. Field key/type: `field-1` / `:answer-field.type/blank`.

Captured RHS: `-x`.

Captured ordered solution (absence stays absent):

Perpendicular lines have slopes that are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(-4,-3)$ and $(2,3):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{3-(-3)}{2-(-4)} \\  & =\frac{6}{6} \\  & =1\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (1)=-1\,⇒\,m=-1.
$$

We know that the line passes through the point $(-5,5).$ Using point-slope form and simplifying, we obtain the equation of the line in slope-intercept form:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-5 & =-1(x-(-5)) \\ y-5 & =-1(x+5) \\ y-5 & =-x-5 \\ y & =-x\end{aligned}
$$

## q-237224

What is the equation of the line that passes through the point $(0,-2)$ and is perpendicular to the line passing through the points $(-2,4)$ and $(4,-1)?$

$y=$
{{field-1}}

Family: `easy-intercept-blank-sign-stage`. Parameters: `{"P": [0, -2], "A": [-2, 4], "B": [4, -1]}`. Source reference slope -5/6, perpendicular slope 6/5, intercept -2. Field key/type: `field-1` / `:answer-field.type/blank`.

Captured RHS: `\frac{6}{5}x-2`.

Captured ordered solution (absence stays absent):

Perpendicular lines have slopes that are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(-2,4)$ and $(4,-1):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{-1-4}{4-(-2)} \\  & =\frac{-1-4}{4+2} \\  & =-\frac{5}{6}\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (-\frac{5}{6})=-1\,⇒\,m=\frac{6}{5}.
$$

We know that the line passes through the point $(0,-2).$ Using point-slope form and simplifying, we obtain the equation of the line in slope-intercept form:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-(-2) & =\frac{6}{5}(x-0) \\ y+2 & =\frac{6}{5}x \\ y & =\frac{6}{5}x-2\end{aligned}
$$

## q-237225

What is the equation of the line that passes through the point $(0,-5)$ and is perpendicular to the line passing through the points $(1,-3)$ and $(3,4)?$

$y=$
{{field-1}}

Family: `easy-intercept-blank-sign-stage`. Parameters: `{"P": [0, -5], "A": [1, -3], "B": [3, 4]}`. Source reference slope 7/2, perpendicular slope -2/7, intercept -5. Field key/type: `field-1` / `:answer-field.type/blank`.

Captured RHS: `-\frac{2}{7}x-5`.

Captured ordered solution (absence stays absent):

Perpendicular lines have slopes that are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(1,-3)$ and $(3,4):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{4-(-3)}{3-1} \\  & =\frac{4+3}{3-1} \\  & =\frac{7}{2}\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (\frac{7}{2})=-1\,⇒\,m=-\frac{2}{7}.
$$

We know that the line passes through the point $(0,-5).$ Using point-slope form and simplifying, we obtain the equation of the line in slope-intercept form:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-(-5) & =-\frac{2}{7}(x-0) \\ y+5 & =-\frac{2}{7}x \\ y & =-\frac{2}{7}x-5\end{aligned}
$$

## q-72567

Find the equation of the line that passes through the point $(-6,5)$ and is perpendicular to the line passing through the points $(-2,6)$ and $(0,-6).$

Family: `translated-radio-difference-and-point-sign`. Parameters: `{"P": [-6, 5], "A": [-2, 6], "B": [0, -6]}`. Source reference slope -6, perpendicular slope 1/6, intercept 6. Field key/type: `selection` / `:answer-field.type/radio`.

| Full captured value | Slope multiplier | Incidence residual | Captured correct |
|---|---|---|---|
|`y=-3x-13`|-18|0|False|
|`y=3x+6`|18|-17|False|
|`y=\frac{1}{6}x+6`|1|0|True|
|`y=-\frac{1}{6}x+4`|-1|0|False|
|`y=\frac{1}{6}x-3`|1|-9|False|

Captured ordered solution (absence stays absent):

Perpendicular lines have slopes which are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(-2,6)$ and $(0,-6):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{-6-6}{0-(-2)} \\  & =\frac{-12}{2} \\  & =-6\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (-6)=-1\,⇒\,m=\frac{1}{6}.
$$

We know that the line passes through the point $(-6,5).$ Using point-slope form and simplifying, we obtain the equation of the line:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-5 & =\frac{1}{6}(x-(-6)) \\ y-5 & =\frac{1}{6}(x+6) \\ y-5 & =\frac{1}{6}x+1 \\ y & =\frac{1}{6}x+6\end{aligned}
$$

## q-72568

Find the equation of the line that passes through the point $(-2,5)$ and is perpendicular to the line passing through the points $(6,1)$ and $(4,5).$

Family: `translated-radio-difference-and-point-sign`. Parameters: `{"P": [-2, 5], "A": [6, 1], "B": [4, 5]}`. Source reference slope -2, perpendicular slope 1/2, intercept 6. Field key/type: `selection` / `:answer-field.type/radio`.

| Full captured value | Slope multiplier | Incidence residual | Captured correct |
|---|---|---|---|
|`y=2x+9`|4|0|False|
|`y=x+3`|2|-4|False|
|`y=\frac{1}{2}x+6`|1|0|True|
|`y=x+7`|2|0|False|
|`y=\frac{1}{2}x-3`|1|-9|False|

Captured ordered solution (absence stays absent):

Perpendicular lines have slopes which are negative reciprocals of each other.

First, let's find the slope ${m}_{1}$ of the line passing through the points $(6,1)$ and $(4,5):$

$$
\begin{aligned}{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}} \\  & =\frac{5-1}{4-6} \\  & =\frac{4}{-2} \\  & =-2\end{aligned}
$$

Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy

$$
m\cdot (-2)=-1\,⇒\,m=\frac{1}{2}.
$$

We know that the line passes through the point $(-2,5).$ Using point-slope form and simplifying, we obtain the equation of the line:

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-5 & =\frac{1}{2}(x-(-2)) \\ y-5 & =\frac{1}{2}(x+2) \\ y-5 & =\frac{1}{2}x+1 \\ y & =\frac{1}{2}x+6\end{aligned}
$$

