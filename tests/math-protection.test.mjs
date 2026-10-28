import test from 'node:test';
import assert from 'node:assert/strict';
import {protectMath} from '../ui/math-protection.js';
import {marked} from '../ui/vendor/marked/marked.esm.js';

test('bare nested environments keep complete rows and paragraphs out of Markdown', () => {
  const tex = String.raw`\begin{align*}
x &= 1 \\[5pt]

&= \begin{aligned}2 \\ 3\end{aligned}
\end{align*}`;
  const saved = [];
  const protectedText = protectMath('Before.\n\n' + tex + '\n\nAfter.', s => { saved.push(s); return 'MATHTOKEN'; });
  assert.deepEqual(saved, [tex]);
  assert.equal(marked.parse(protectedText), '<p>Before.</p>\n<p>MATHTOKEN</p>\n<p>After.</p>\n');
});

test('delimited math, escaped currency and widget keys retain their exact bytes', () => {
  const source = String.raw`Price \$5. $x_1$ and $$\begin{aligned}x&=1\\y&=2\end{aligned}$$ then {{entry}}.`;
  const saved = [];
  protectMath(source, s => { saved.push(s); return ''; });
  assert.deepEqual(saved, ['$x_1$', String.raw`$$\begin{aligned}x&=1\\y&=2\end{aligned}$$`]);
});

test('unclosed or mismatched environments are left for validation', () => {
  for (const tex of [String.raw`\begin{align}x`, String.raw`\begin{align}x\end{matrix}`]) {
    assert.equal(protectMath(tex, () => 'BAD'), tex);
  }
});

test('literal dollars inside currency formulas do not close their math spans', () => {
  const formulas = [String.raw`$\$450\,000$`, String.raw`$- \$72.25$`, String.raw`$V(4)=\$409.60$`, String.raw`$$P=P_0e^{rt}$$`];
  const saved = [];
  protectMath(formulas.join(' and '), s => { saved.push(s); return 'MATH'; });
  assert.deepEqual(saved, formulas);
});

test('quoted display math keeps its callout without rendering container markers', () => {
  const saved = [];
  const source = '> Rule\n>\n> $$\n> A \\cdot I_n = I_n \\cdot A = A.\n> $$';
  const text = protectMath(source, s => { saved.push(s); return 'MATHTOKEN'; });
  assert.deepEqual(saved, ['$$\nA \\cdot I_n = I_n \\cdot A = A.\n$$']);
  assert.equal(marked.parse(text), '<blockquote>\n<p>Rule</p>\n<p>MATHTOKEN</p>\n</blockquote>\n');
});

test('quote depth preserves real inequalities and unquoted greater-than symbols', () => {
  const saved = [];
  protectMath('> > $$\n> > > x\n> > $$\n\n$$\n> y\n$$', s => { saved.push(s); return 'MATH'; });
  assert.deepEqual(saved, ['$$\n> x\n$$', '$$\n> y\n$$']);
});
