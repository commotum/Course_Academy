# Source and served variants

Nine rated source anchors match complete prompt, solution, field contract, ordered banks and correct designation exactly. Each variant uses the same operational named-slot renderer. The legacy unrated record is reference-only. See validation.json for the separate valid-math engine limitations.

## q-132982

Captured source

$\int \frac{-16t}{2{t}^{2}+3}\,\text{d}t=\,$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$+\,K.$

Let $u=2{t}^{2}+3.$ Then

$$
\frac{\text{d}u}{\text{d}t}=4t\,⟹\,\frac{1}{4}\text{d}u=t\,\text{d}t.
$$

We can solve the required integral as follows:

$$
\begin{aligned}\int \frac{-16t}{2{t}^{2}+3}\,\text{d}t & =-16\int \frac{1}{2{t}^{2}+3}\cdot t\,\text{d}t \\  & =-16\int \frac{1}{u}\cdot \frac{1}{4}\,\text{d}u \\  & =-4\int \frac{1}{u}\,\text{d}u \\  & =-4\operatorname{ln}⁡|u|+K \\  & =-4\operatorname{ln}⁡(2{t}^{2}+3)+K\end{aligned}
$$

Choices: ["-4\\operatorname{ln}(2{t}^{2}+3)"]

Served anchor

$\int \frac{-16t}{2{t}^{2}+3}\,\text{d}t=\,$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$+\,K.$

Let $u=2{t}^{2}+3.$ Then

$$
\frac{\text{d}u}{\text{d}t}=4t\,⟹\,\frac{1}{4}\text{d}u=t\,\text{d}t.
$$

We can solve the required integral as follows:

$$
\begin{aligned}\int \frac{-16t}{2{t}^{2}+3}\,\text{d}t & =-16\int \frac{1}{2{t}^{2}+3}\cdot t\,\text{d}t \\  & =-16\int \frac{1}{u}\cdot \frac{1}{4}\,\text{d}u \\  & =-4\int \frac{1}{u}\,\text{d}u \\  & =-4\operatorname{ln}⁡|u|+K \\  & =-4\operatorname{ln}⁡(2{t}^{2}+3)+K\end{aligned}
$$

Choices: ["-4\\operatorname{ln}(2{t}^{2}+3)"]

Served variant

$\int \frac{-16t}{2 t^{2} + 2}\,\text{d}t=\,$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$+\,K.$

Let $u=2 t^{2} + 2.$ Then

$$
\frac{\text{d}u}{\text{d}t}=4t\,⟹\,\frac{1}{4}\text{d}u=t\,\text{d}t.
$$

We can solve the required integral as follows:

$$
\begin{aligned}\int \frac{-16t}{2 t^{2} + 2}\,\text{d}t & =-16\int \frac{1}{2 t^{2} + 2}\cdot t\,\text{d}t \\  & =-16\int \frac{1}{u}\cdot \frac{1}{4}\,\text{d}u \\  & =-4\int \frac{1}{u}\,\text{d}u \\  & =-4\operatorname{ln}⁡|u|+K \\  & =-4\operatorname{ln}⁡(2 t^{2} + 2)+K\end{aligned}
$$

Choices: ["-4\\operatorname{ln}(2 t^{2} + 2)"]

## q-12501

Captured source

Calculate the integral of $\frac{{x}^{2}}{{x}^{3}+10}$ with respect to $x.$

Let $u={x}^{3}+10.$ Then

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\frac{1}{3}\text{d}u={x}^{2}\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{{x}^{2}}{{x}^{3}+10}\,\text{d}x & =\int \frac{1}{{x}^{3}+10}\cdot {x}^{2}\,\text{d}x \\  & =\int \frac{1}{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{1}{3}\int \frac{1}{u}\,\text{d}u \\  & =\frac{1}{3}\operatorname{ln}⁡|u|+C \\  & =\frac{1}{3}\operatorname{ln}⁡|{x}^{3}+10|+C\end{aligned}
$$

Choices: ["\\frac{1}{3}\\operatorname{ln}\u2061|{x}^{3}+10|+C", "\\operatorname{ln}\u2061|{x}^{3}+10|+C", "\\frac{1}{2}\\operatorname{ln}\u2061|{x}^{3}+10|+C", "\\frac{1}{10}\\operatorname{ln}\u2061|{x}^{3}+10|+C", "3\\operatorname{ln}\u2061|{x}^{3}+10|+C"]

Served anchor

Calculate the integral of $\frac{{x}^{2}}{{x}^{3}+10}$ with respect to $x.$

Let $u={x}^{3}+10.$ Then

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\frac{1}{3}\text{d}u={x}^{2}\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{{x}^{2}}{{x}^{3}+10}\,\text{d}x & =\int \frac{1}{{x}^{3}+10}\cdot {x}^{2}\,\text{d}x \\  & =\int \frac{1}{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{1}{3}\int \frac{1}{u}\,\text{d}u \\  & =\frac{1}{3}\operatorname{ln}⁡|u|+C \\  & =\frac{1}{3}\operatorname{ln}⁡|{x}^{3}+10|+C\end{aligned}
$$

Choices: ["\\frac{1}{3}\\operatorname{ln}\u2061|{x}^{3}+10|+C", "\\operatorname{ln}\u2061|{x}^{3}+10|+C", "\\frac{1}{2}\\operatorname{ln}\u2061|{x}^{3}+10|+C", "\\frac{1}{10}\\operatorname{ln}\u2061|{x}^{3}+10|+C", "3\\operatorname{ln}\u2061|{x}^{3}+10|+C"]

Served variant

Calculate the integral of $\frac{{x}^{2}}{x^{3} + 11}$ with respect to $x.$

Let $u=x^{3} + 11.$ Then

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\frac{1}{3}\text{d}u={x}^{2}\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{{x}^{2}}{x^{3} + 11}\,\text{d}x & =\int \frac{1}{x^{3} + 11}\cdot {x}^{2}\,\text{d}x \\  & =\int \frac{1}{u}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{1}{3}\int \frac{1}{u}\,\text{d}u \\  & =\frac{1}{3}\operatorname{ln}⁡|u|+C \\  & =\frac{1}{3}\operatorname{ln}⁡|x^{3} + 11|+C\end{aligned}
$$

Choices: ["\\frac{1}{3}\\operatorname{ln}\u2061|x^{3} + 11|+C", "\\operatorname{ln}\u2061|x^{3} + 11|+C", "\\frac{1}{2}\\operatorname{ln}\u2061|x^{3} + 11|+C", "\\frac{1}{11}\\operatorname{ln}\u2061|x^{3} + 11|+C", "3\\operatorname{ln}\u2061|x^{3} + 11|+C"]

## q-49451

Captured source

$\int \frac{4x}{{x}^{2}+1}\,\text{d}x=$

Let $u={x}^{2}+1.$ Then

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{4x}{{x}^{2}+1}\,\text{d}x & =4\int \frac{1}{{x}^{2}+1}\cdot x\,\text{d}x \\  & =4\int \frac{1}{u}\cdot \frac{1}{2}\,\text{d}u \\  & =2\int \frac{1}{u}\,\text{d}u \\  & =2\operatorname{ln}⁡|u|+C \\  & =2\operatorname{ln}⁡({x}^{2}+1)+C\end{aligned}
$$

Choices: ["\\frac{1}{2}\\operatorname{ln}\u2061({x}^{2}+1)+C", "\\frac{1}{4}\\operatorname{ln}\u2061({x}^{2}+1)+C", "\\frac{1}{({x}^{2}+1)^{2}}+C", "2\\operatorname{ln}\u2061({x}^{2}+1)+C", "\\frac{2}{({x}^{2}+1)^{2}}+C"]

Served anchor

$\int \frac{4x}{{x}^{2}+1}\,\text{d}x=$

Let $u={x}^{2}+1.$ Then

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{4x}{{x}^{2}+1}\,\text{d}x & =4\int \frac{1}{{x}^{2}+1}\cdot x\,\text{d}x \\  & =4\int \frac{1}{u}\cdot \frac{1}{2}\,\text{d}u \\  & =2\int \frac{1}{u}\,\text{d}u \\  & =2\operatorname{ln}⁡|u|+C \\  & =2\operatorname{ln}⁡({x}^{2}+1)+C\end{aligned}
$$

Choices: ["\\frac{1}{2}\\operatorname{ln}\u2061({x}^{2}+1)+C", "\\frac{1}{4}\\operatorname{ln}\u2061({x}^{2}+1)+C", "\\frac{1}{({x}^{2}+1)^{2}}+C", "2\\operatorname{ln}\u2061({x}^{2}+1)+C", "\\frac{2}{({x}^{2}+1)^{2}}+C"]

Served variant

$\int \frac{4x}{x^{2} + 11}\,\text{d}x=$

Let $u=x^{2} + 11.$ Then

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{4x}{x^{2} + 11}\,\text{d}x & =4\int \frac{1}{x^{2} + 11}\cdot x\,\text{d}x \\  & =4\int \frac{1}{u}\cdot \frac{1}{2}\,\text{d}u \\  & =2\int \frac{1}{u}\,\text{d}u \\  & =2\operatorname{ln}⁡|u|+C \\  & =2\operatorname{ln}⁡(x^{2} + 11)+C\end{aligned}
$$

Choices: ["\\frac{1}{2}\\operatorname{ln}\u2061(x^{2} + 11)+C", "\\frac{1}{4}\\operatorname{ln}\u2061(x^{2} + 11)+C", "\\frac{1}{(x^{2} + 11)^{2}}+C", "2\\operatorname{ln}\u2061(x^{2} + 11)+C", "\\frac{2}{(x^{2} + 11)^{2}}+C"]

## q-49572

Captured source

Calculate $\int \frac{{x}^{9}}{{x}^{10}+9}\,\text{d}x.$

Let $u={x}^{10}+9.$ Then

$$
\frac{\text{d}u}{\text{d}x}=10{x}^{9}\,⟹\,\frac{1}{10}\text{d}u={x}^{9}\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{{x}^{9}}{{x}^{10}+9}\,\text{d}x & =\int \frac{1}{{x}^{10}+9}\cdot {x}^{9}\,\text{d}x \\  & =\int \frac{1}{u}\cdot \frac{1}{10}\,\text{d}u \\  & =\frac{1}{10}\int \frac{1}{u}\,\text{d}u \\  & =\frac{1}{10}\operatorname{ln}⁡|u|+C \\  & =\frac{1}{10}\operatorname{ln}⁡|{x}^{10}+9|+C\end{aligned}
$$

Choices: ["10\\operatorname{ln}\u2061|{x}^{10}+9|+C", "\\frac{1}{{({x}^{10}+9)}^{2}}+C", "\\frac{1}{2}\\operatorname{ln}\u2061|{x}^{10}+9|+C", "\\frac{1}{10}\\operatorname{ln}\u2061|{x}^{10}+9|+C", "9\\operatorname{ln}\u2061|{x}^{10}+9|+C"]

Served anchor

Calculate $\int \frac{{x}^{9}}{{x}^{10}+9}\,\text{d}x.$

Let $u={x}^{10}+9.$ Then

$$
\frac{\text{d}u}{\text{d}x}=10{x}^{9}\,⟹\,\frac{1}{10}\text{d}u={x}^{9}\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{{x}^{9}}{{x}^{10}+9}\,\text{d}x & =\int \frac{1}{{x}^{10}+9}\cdot {x}^{9}\,\text{d}x \\  & =\int \frac{1}{u}\cdot \frac{1}{10}\,\text{d}u \\  & =\frac{1}{10}\int \frac{1}{u}\,\text{d}u \\  & =\frac{1}{10}\operatorname{ln}⁡|u|+C \\  & =\frac{1}{10}\operatorname{ln}⁡|{x}^{10}+9|+C\end{aligned}
$$

Choices: ["10\\operatorname{ln}\u2061|{x}^{10}+9|+C", "\\frac{1}{{({x}^{10}+9)}^{2}}+C", "\\frac{1}{2}\\operatorname{ln}\u2061|{x}^{10}+9|+C", "\\frac{1}{10}\\operatorname{ln}\u2061|{x}^{10}+9|+C", "9\\operatorname{ln}\u2061|{x}^{10}+9|+C"]

Served variant

Calculate $\int \frac{{x}^{9}}{x^{10} + 11}\,\text{d}x.$

Let $u=x^{10} + 11.$ Then

$$
\frac{\text{d}u}{\text{d}x}=10{x}^{9}\,⟹\,\frac{1}{10}\text{d}u={x}^{9}\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{{x}^{9}}{x^{10} + 11}\,\text{d}x & =\int \frac{1}{x^{10} + 11}\cdot {x}^{9}\,\text{d}x \\  & =\int \frac{1}{u}\cdot \frac{1}{10}\,\text{d}u \\  & =\frac{1}{10}\int \frac{1}{u}\,\text{d}u \\  & =\frac{1}{10}\operatorname{ln}⁡|u|+C \\  & =\frac{1}{10}\operatorname{ln}⁡|x^{10} + 11|+C\end{aligned}
$$

Choices: ["10\\operatorname{ln}\u2061|x^{10} + 11|+C", "\\frac{1}{{(x^{10} + 11)}^{2}}+C", "\\frac{1}{2}\\operatorname{ln}\u2061|x^{10} + 11|+C", "\\frac{1}{10}\\operatorname{ln}\u2061|x^{10} + 11|+C", "11\\operatorname{ln}\u2061|x^{10} + 11|+C"]

## q-72605

Captured source

$\int \frac{10{x}^{4}}{2-5{x}^{5}}\,\text{d}x=$

Let $u=2-5{x}^{5}.$ Then

$$
\frac{\text{d}u}{\text{d}x}=-25{x}^{4}\,⟹\,(-\frac{1}{25})\text{d}u={x}^{4}\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{10{x}^{4}}{2-5{x}^{5}}\,\text{d}x & =10\int \frac{1}{2-5{x}^{5}}\cdot {x}^{4}\,\text{d}x \\  & =10\int \frac{1}{u}\cdot (-\frac{1}{25})\text{d}u \\  & =-\frac{10}{25}\int \frac{1}{u}\,\text{d}u \\  & =-\frac{2}{5}\int \frac{1}{u}\,\text{d}u \\  & =-\frac{2}{5}\operatorname{ln}⁡|u|+C \\  & =-\frac{2}{5}\operatorname{ln}⁡|2-5{x}^{5}|+C\end{aligned}
$$

Choices: ["-2\\operatorname{ln}\u2061|2-5{x}^{5}|+C", "\\frac{2}{5(2-5{x}^{5})^{2}}+C", "-\\frac{5}{2(2-5{x}^{5})^{2}}+C", "\\frac{5}{2}\\operatorname{ln}\u2061|2-5{x}^{5}|+C", "-\\frac{2}{5}\\operatorname{ln}\u2061|2-5{x}^{5}|+C"]

Served anchor

$\int \frac{10{x}^{4}}{2-5{x}^{5}}\,\text{d}x=$

Let $u=2-5{x}^{5}.$ Then

$$
\frac{\text{d}u}{\text{d}x}=-25{x}^{4}\,⟹\,(-\frac{1}{25})\text{d}u={x}^{4}\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{10{x}^{4}}{2-5{x}^{5}}\,\text{d}x & =10\int \frac{1}{2-5{x}^{5}}\cdot {x}^{4}\,\text{d}x \\  & =10\int \frac{1}{u}\cdot (-\frac{1}{25})\text{d}u \\  & =-\frac{10}{25}\int \frac{1}{u}\,\text{d}u \\  & =-\frac{2}{5}\int \frac{1}{u}\,\text{d}u \\  & =-\frac{2}{5}\operatorname{ln}⁡|u|+C \\  & =-\frac{2}{5}\operatorname{ln}⁡|2-5{x}^{5}|+C\end{aligned}
$$

Choices: ["-2\\operatorname{ln}\u2061|2-5{x}^{5}|+C", "\\frac{2}{5(2-5{x}^{5})^{2}}+C", "-\\frac{5}{2(2-5{x}^{5})^{2}}+C", "\\frac{5}{2}\\operatorname{ln}\u2061|2-5{x}^{5}|+C", "-\\frac{2}{5}\\operatorname{ln}\u2061|2-5{x}^{5}|+C"]

Served variant

$\int \frac{10{x}^{4}}{- 5 x^{5} + 11}\,\text{d}x=$

Let $u=- 5 x^{5} + 11.$ Then

$$
\frac{\text{d}u}{\text{d}x}=-25{x}^{4}\,⟹\,(-\frac{1}{25})\text{d}u={x}^{4}\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{10{x}^{4}}{- 5 x^{5} + 11}\,\text{d}x & =10\int \frac{1}{- 5 x^{5} + 11}\cdot {x}^{4}\,\text{d}x \\  & =10\int \frac{1}{u}\cdot (-\frac{1}{25})\text{d}u \\  & =-\frac{10}{25}\int \frac{1}{u}\,\text{d}u \\  & =-\frac{2}{5}\int \frac{1}{u}\,\text{d}u \\  & =-\frac{2}{5}\operatorname{ln}⁡|u|+C \\  & =-\frac{2}{5}\operatorname{ln}⁡|- 5 x^{5} + 11|+C\end{aligned}
$$

Choices: ["-2\\operatorname{ln}\u2061|- 5 x^{5} + 11|+C", "\\frac{2}{5(- 5 x^{5} + 11)^{2}}+C", "-\\frac{5}{2(- 5 x^{5} + 11)^{2}}+C", "\\frac{5}{2}\\operatorname{ln}\u2061|- 5 x^{5} + 11|+C", "-\\frac{2}{5}\\operatorname{ln}\u2061|- 5 x^{5} + 11|+C"]

## q-72566

Captured source

$\int \frac{3{x}^{2}-1}{{x}^{3}-x}\,\text{d}x=$

Let $u={x}^{3}-x.$ Then

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}-1\,⟹\,\text{d}u=(3{x}^{2}-1)\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{3{x}^{2}-1}{{x}^{3}-x}\,\text{d}x & =\int \frac{1}{{x}^{3}-x}\cdot (3{x}^{2}-1)\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|{x}^{3}-x|+C\end{aligned}
$$

Choices: ["\\operatorname{ln}\u2061|3{x}^{2}-1|+C", "\\operatorname{ln}\u2061|{x}^{3}-1|+C", "\\operatorname{ln}\u2061|{x}^{3}-x|+C", "\\operatorname{ln}\u2061|3{x}^{2}-x|+C", "\\operatorname{ln}\u2061|\\frac{1}{{x}^{3}-1}|+C"]

Served anchor

$\int \frac{3{x}^{2}-1}{{x}^{3}-x}\,\text{d}x=$

Let $u={x}^{3}-x.$ Then

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}-1\,⟹\,\text{d}u=(3{x}^{2}-1)\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{3{x}^{2}-1}{{x}^{3}-x}\,\text{d}x & =\int \frac{1}{{x}^{3}-x}\cdot (3{x}^{2}-1)\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|{x}^{3}-x|+C\end{aligned}
$$

Choices: ["\\operatorname{ln}\u2061|3{x}^{2}-1|+C", "\\operatorname{ln}\u2061|{x}^{3}-1|+C", "\\operatorname{ln}\u2061|{x}^{3}-x|+C", "\\operatorname{ln}\u2061|3{x}^{2}-x|+C", "\\operatorname{ln}\u2061|\\frac{1}{{x}^{3}-1}|+C"]

Served variant

$\int \frac{3 x^{2} - 6}{x^{3} - 6 x}\,\text{d}x=$

Let $u=x^{3} - 6 x.$ Then

$$
\frac{\text{d}u}{\text{d}x}=3 x^{2} - 6\,⟹\,\text{d}u=(3 x^{2} - 6)\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{3 x^{2} - 6}{x^{3} - 6 x}\,\text{d}x & =\int \frac{1}{x^{3} - 6 x}\cdot (3 x^{2} - 6)\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|x^{3} - 6 x|+C\end{aligned}
$$

Choices: ["\\operatorname{ln}\u2061|3 x^{2} - 6|+C", "\\operatorname{ln}\u2061|x^{3} - 6|+C", "\\operatorname{ln}\u2061|x^{3} - 6 x|+C", "\\operatorname{ln}\u2061|3 x^{2} - 6 x|+C", "\\operatorname{ln}\u2061|\\frac{1}{x^{3} - 6}|+C"]

## q-113719

Captured source

Calculate $\int \frac{1-4{x}^{3}}{1+x-{x}^{4}}\,\text{d}x.$

Let $u=1+x-{x}^{4}.$ Then

$$
\frac{\text{d}u}{\text{d}x}=1-4{x}^{3}\,⟹\,\text{d}u=(1-4{x}^{3})\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{1-4{x}^{3}}{1+x-{x}^{4}}\,\text{d}x & =\int \frac{1}{1+x-{x}^{4}}\cdot (1-4{x}^{3})\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|1+x-{x}^{4}|+C\end{aligned}
$$

Choices: ["\\frac{\\operatorname{ln}\u2061|1+x-{x}^{4}|}{1-4{x}^{3}}+C", "\\operatorname{ln}\u2061|\\frac{1-4{x}^{3}}{1+x-{x}^{4}}|+C", "\\operatorname{ln}\u2061|1+x-{x}^{4}|+C", "\\operatorname{ln}\u2061|\\frac{1+x-{x}^{4}}{1-4{x}^{3}}|+C", "\\operatorname{ln}\u2061|1-4{x}^{3}|+C"]

Served anchor

Calculate $\int \frac{1-4{x}^{3}}{1+x-{x}^{4}}\,\text{d}x.$

Let $u=1+x-{x}^{4}.$ Then

$$
\frac{\text{d}u}{\text{d}x}=1-4{x}^{3}\,⟹\,\text{d}u=(1-4{x}^{3})\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{1-4{x}^{3}}{1+x-{x}^{4}}\,\text{d}x & =\int \frac{1}{1+x-{x}^{4}}\cdot (1-4{x}^{3})\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|1+x-{x}^{4}|+C\end{aligned}
$$

Choices: ["\\frac{\\operatorname{ln}\u2061|1+x-{x}^{4}|}{1-4{x}^{3}}+C", "\\operatorname{ln}\u2061|\\frac{1-4{x}^{3}}{1+x-{x}^{4}}|+C", "\\operatorname{ln}\u2061|1+x-{x}^{4}|+C", "\\operatorname{ln}\u2061|\\frac{1+x-{x}^{4}}{1-4{x}^{3}}|+C", "\\operatorname{ln}\u2061|1-4{x}^{3}|+C"]

Served variant

Calculate $\int \frac{1-4{x}^{3}}{- x^{4} + x + 11}\,\text{d}x.$

Let $u=- x^{4} + x + 11.$ Then

$$
\frac{\text{d}u}{\text{d}x}=1-4{x}^{3}\,⟹\,\text{d}u=(1-4{x}^{3})\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{1-4{x}^{3}}{- x^{4} + x + 11}\,\text{d}x & =\int \frac{1}{- x^{4} + x + 11}\cdot (1-4{x}^{3})\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|- x^{4} + x + 11|+C\end{aligned}
$$

Choices: ["\\frac{\\operatorname{ln}\u2061|- x^{4} + x + 11|}{1-4{x}^{3}}+C", "\\operatorname{ln}\u2061|\\frac{1-4{x}^{3}}{- x^{4} + x + 11}|+C", "\\operatorname{ln}\u2061|- x^{4} + x + 11|+C", "\\operatorname{ln}\u2061|\\frac{- x^{4} + x + 11}{1-4{x}^{3}}|+C", "\\operatorname{ln}\u2061|1-4{x}^{3}|+C"]

## q-113720

Captured source

Calculate $\int \frac{5{x}^{4}-1}{{x}^{5}-x}\,\text{d}x.$

Let $u={x}^{5}-x.$ Then

$$
\frac{\text{d}u}{\text{d}x}=5{x}^{4}-1\,⟹\,\text{d}u=(5{x}^{4}-1)\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{5{x}^{4}-1}{{x}^{5}-x}\,\text{d}x & =\int \frac{1}{{x}^{5}-x}\cdot (5{x}^{4}-1)\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|{x}^{5}-x|+C\end{aligned}
$$

Choices: ["\\frac{\\operatorname{ln}\u2061|{x}^{5}-x|}{5{x}^{4}-1}+C", "\\operatorname{ln}\u2061|\\frac{{x}^{5}-x}{5{x}^{4}-1}|+C", "\\operatorname{ln}\u2061|5{x}^{4}-1|+C", "\\operatorname{ln}\u2061|\\frac{5{x}^{4}-1}{{x}^{5}-x}|+C", "\\operatorname{ln}\u2061|{x}^{5}-x|+C"]

Served anchor

Calculate $\int \frac{5{x}^{4}-1}{{x}^{5}-x}\,\text{d}x.$

Let $u={x}^{5}-x.$ Then

$$
\frac{\text{d}u}{\text{d}x}=5{x}^{4}-1\,⟹\,\text{d}u=(5{x}^{4}-1)\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{5{x}^{4}-1}{{x}^{5}-x}\,\text{d}x & =\int \frac{1}{{x}^{5}-x}\cdot (5{x}^{4}-1)\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|{x}^{5}-x|+C\end{aligned}
$$

Choices: ["\\frac{\\operatorname{ln}\u2061|{x}^{5}-x|}{5{x}^{4}-1}+C", "\\operatorname{ln}\u2061|\\frac{{x}^{5}-x}{5{x}^{4}-1}|+C", "\\operatorname{ln}\u2061|5{x}^{4}-1|+C", "\\operatorname{ln}\u2061|\\frac{5{x}^{4}-1}{{x}^{5}-x}|+C", "\\operatorname{ln}\u2061|{x}^{5}-x|+C"]

Served variant

Calculate $\int \frac{5 x^{4} - 6}{x^{5} - 6 x}\,\text{d}x.$

Let $u=x^{5} - 6 x.$ Then

$$
\frac{\text{d}u}{\text{d}x}=5 x^{4} - 6\,⟹\,\text{d}u=(5 x^{4} - 6)\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{5 x^{4} - 6}{x^{5} - 6 x}\,\text{d}x & =\int \frac{1}{x^{5} - 6 x}\cdot (5 x^{4} - 6)\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|x^{5} - 6 x|+C\end{aligned}
$$

Choices: ["\\frac{\\operatorname{ln}\u2061|x^{5} - 6 x|}{5 x^{4} - 6}+C", "\\operatorname{ln}\u2061|\\frac{x^{5} - 6 x}{5 x^{4} - 6}|+C", "\\operatorname{ln}\u2061|5 x^{4} - 6|+C", "\\operatorname{ln}\u2061|\\frac{5 x^{4} - 6}{x^{5} - 6 x}|+C", "\\operatorname{ln}\u2061|x^{5} - 6 x|+C"]

## q-113721

Captured source

Calculate $\int \frac{2x+2}{{x}^{2}+2x}\,\text{d}x.$

Let $u={x}^{2}+2x.$ Then

$$
\frac{\text{d}u}{\text{d}x}=2x+2\,⟹\,\text{d}u=(2x+2)\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{2x+2}{{x}^{2}+2x}\,\text{d}x & =\int \frac{1}{{x}^{2}+2x}\cdot (2x+2)\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|{x}^{2}+2x|+C\end{aligned}
$$

Choices: ["\\frac{\\operatorname{ln}\u2061|{x}^{2}+2x|}{2x+2}+C", "\\operatorname{ln}\u2061|2x+2|+C", "\\operatorname{ln}\u2061|{x}^{2}+2x|+C", "\\operatorname{ln}\u2061|\\frac{{x}^{2}+2x}{2x+2}|+C", "\\operatorname{ln}\u2061|\\frac{2x+2}{{x}^{2}+2x}|+C"]

Served anchor

Calculate $\int \frac{2x+2}{{x}^{2}+2x}\,\text{d}x.$

Let $u={x}^{2}+2x.$ Then

$$
\frac{\text{d}u}{\text{d}x}=2x+2\,⟹\,\text{d}u=(2x+2)\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{2x+2}{{x}^{2}+2x}\,\text{d}x & =\int \frac{1}{{x}^{2}+2x}\cdot (2x+2)\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|{x}^{2}+2x|+C\end{aligned}
$$

Choices: ["\\frac{\\operatorname{ln}\u2061|{x}^{2}+2x|}{2x+2}+C", "\\operatorname{ln}\u2061|2x+2|+C", "\\operatorname{ln}\u2061|{x}^{2}+2x|+C", "\\operatorname{ln}\u2061|\\frac{{x}^{2}+2x}{2x+2}|+C", "\\operatorname{ln}\u2061|\\frac{2x+2}{{x}^{2}+2x}|+C"]

Served variant

Calculate $\int \frac{2 x + 6}{x^{2} + 6 x}\,\text{d}x.$

Let $u=x^{2} + 6 x.$ Then

$$
\frac{\text{d}u}{\text{d}x}=2 x + 6\,⟹\,\text{d}u=(2 x + 6)\,\text{d}x,
$$

and we can solve the resulting integral as follows:

$$
\begin{aligned}\int \frac{2 x + 6}{x^{2} + 6 x}\,\text{d}x & =\int \frac{1}{x^{2} + 6 x}\cdot (2 x + 6)\,\text{d}x \\  & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|x^{2} + 6 x|+C\end{aligned}
$$

Choices: ["\\frac{\\operatorname{ln}\u2061|x^{2} + 6 x|}{2 x + 6}+C", "\\operatorname{ln}\u2061|2 x + 6|+C", "\\operatorname{ln}\u2061|x^{2} + 6 x|+C", "\\operatorname{ln}\u2061|\\frac{x^{2} + 6 x}{2 x + 6}|+C", "\\operatorname{ln}\u2061|\\frac{2 x + 6}{x^{2} + 6 x}|+C"]