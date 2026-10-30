import assert from 'node:assert/strict';
import { equationGroup } from './equation-groups.js';
const display = value => '$$' + value + '$$';
const yes = [
  String.raw`x=t(t-2)-1,\,y=t(1-t)-2,\,-2\le t\le2`,
  String.raw`x=3t-2,\,\,\,y=\frac{10}{t^2+1},\,-3\le t\le3,`,
  String.raw`x=-\frac{5t^3}{4}-\frac{4t^2}{3}-6,\,y=-\frac{3t^3}{4}-\frac{t^2}{3}+6,\,0\le t\le5.`,
  String.raw`x=f(s,t),\qquad y=g(s,t),\quad t\in[0,2)`,
  String.raw`x=\left\{1,2\right\}, y=\max(a,b)`,
  String.raw`{x}=2t;\quad {y}=t^2`,
  String.raw`x(t)=2t, y(t)=t^2`,
];
for (const body of yes) assert.ok(equationGroup(display(body)), body);
const no = [
  '$x=1,y=2$', String.raw`\(x=1,y=2\)`,
  display(String.raw`\begin{aligned}x&=t\\y&=t^2\end{aligned}`),
  display(String.raw`\begin{bmatrix}x=1,y=2\end{bmatrix}`),
  display('x=(1,2,3)'), display('x=1,2,3'), display('x=1, y=2, 3'),
  display('x=1, x=2'), display('x=1, y=2, therefore true'),
  display(String.raw`x=1, y=2, z=3=4`),
  display(String.raw`x=1, y=2, a+b=c`),
  display(String.raw`\color{blue}x=1, y=2`),
  display(String.raw`x={{field-1}}, y=2`),
  display(String.raw`x=\underbrace{\qquad}_{\text{answer 1}}, y=2`),
];
for (const tex of no) assert.equal(equationGroup(tex), null, tex);
assert.deepEqual(equationGroup(display('x=f(s,t), y=g(s,t), t\\in(0,1)')), ['x=f(s,t),', 'y=g(s,t),', String.raw`t\in(0,1)`]);
assert.deepEqual(equationGroup(String.raw`\[x=2t,\quad y=t^2\]`), ['x=2t,', 'y=t^2']);
console.log('Equation group boundaries: positive examples and ambiguous/nested/control exclusions passed.');
