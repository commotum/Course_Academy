# Lesson-Title / Sections Progression Notes

This document demonstrates how MathAcademy composes lessons as progressions of tightly scoped sections, and how that structure should be represented in the step-identification schema for this stage: each entry should still look like `{ "lesson-title": "...", "sections": [{ "step-title": "...", "step-type": "tutorial" }, { "step-title": "...", "step-type": "example" }] }`. The difference here is that the progression notes are written in very concise natural English rather than slash-separated tags. For each section, the actual practice questions are listed, followed by a few short bullets that explain how the section extends the previous one.

## Table of Contents

- [Imaginary Numbers](#imaginary-numbers)
  - Introduction to Imaginary Numbers
  - Finding the Square Root of a Negative Number
  - Finding the Negative Square Root of a Negative Number
  - Finding the Square Root of a Negative Number With Simplifications
  - Finding the Square Root of a Negative Fraction
- [The Nth Term of a Geometric Sequence](#the-nth-term-of-a-geometric-sequence)
  - Introduction to The Nth Term of a Geometric Sequence
  - Finding a Particular Term Given the First Term and Common Ratio
  - Finding a Formula for the Nth Term
  - Finding a Particular Term Given a Non-First Term and Common Ratio
- [Complex Numbers](#complex-numbers)
  - Introduction to Complex Numbers
  - Identifying Real and Imaginary Parts (Standard Form)
  - Identifying Parts from Nonstandard Form
  - Complex Numbers with Zero Real or Imaginary Part
  - Real Part of a Purely Imaginary Number
  - Imaginary Part of a Real Number
- [Euler's Formula](#eulers-formula)
  - Introduction to Euler's Formula
  - Writing a Complex Number in Exponential Form
  - Writing from an Argand Diagram
  - Proving Sum Formulas for Sine and Cosine

---

<a id="imaginary-numbers"></a>
## `lesson-title`: Imaginary Numbers

**`step-title`: Introduction to Imaginary Numbers**  
**`step-type`: tutorial**  
- Questions in this section: none.
- This step introduces \(i = \sqrt{-1}\) and shows the base rewrite from \(\sqrt{-a}\) to \(i\sqrt{a}\).
- Every later example changes one detail of that same move.

**`step-title`: Finding the Square Root of a Negative Number**  
**`step-type`: example**  
- Questions in this section:
  - What is \(\sqrt{-49}\)?
  - What is \(\sqrt{-25}\)?
- This is the first direct application of the rule.
- The radicands are perfect squares, so students only need to convert the expression into a whole-number multiple of \(i\).

**`step-title`: Finding the Negative Square Root of a Negative Number**  
**`step-type`: example**  
- Questions in this section:
  - What is \(-\sqrt{-64}\)?
  - What is \(-\sqrt{-16}\)?
- The core conversion stays the same, but now there is a negative sign outside the radical.
- The new wrinkle is carrying that outside sign correctly after the imaginary rewrite.

**`step-title`: Finding the Square Root of a Negative Number With Simplifications**  
**`step-type`: example**  
- Questions in this section:
  - What is \(\sqrt{-44}\)?
  - What is \(\sqrt{-28}\)?
- The numbers no longer simplify in one step.
- Students must first factor out a perfect square, then simplify the radical, and only then attach \(i\).

**`step-title`: Finding the Square Root of a Negative Fraction**  
**`step-type`: example**  
- Questions in this section:
  - What is \(-\sqrt{-\frac{36}{25}}\)?
  - What is \(\sqrt{-\frac{4}{9}}\)?
- The same imaginary-number idea now appears inside a fraction.
- Students split the square root across numerator and denominator, simplify the fraction, and keep track of the imaginary factor and any outside sign.

---

<a id="the-nth-term-of-a-geometric-sequence"></a>
## `lesson-title`: The Nth Term of a Geometric Sequence

**`step-title`: Introduction to The Nth Term of a Geometric Sequence**  
**`step-type`: tutorial**  
- Questions in this section: none.
- This step introduces the formula \(a_n = a_1 r^{n-1}\) and uses it in the forward direction.
- Students identify \(a_1\), \(r\), and the target index before substituting.

**`step-title`: Finding a Particular Term Given the First Term and Common Ratio**  
**`step-type`: example**  
- Questions in this section:
  - The first term of a geometric sequence is \(4\), and the common ratio is \(3\). What is the \(6\)th term?
  - The first term of a geometric sequence is \(32\) and the common ratio is \(-\frac{1}{4}\). The \(7\)th term of this sequence is \(\underline{\hspace{1.5cm}}\).
  - The first term of a geometric sequence is \(5\), and the common ratio is \(2\). What is the \(10\)th term?
- This is straight substitution once the first term and ratio are given.
- The questions vary the index and even use a negative fractional ratio, but the reasoning still goes only forward through the formula.

**`step-title`: Finding a Formula for the Nth Term**  
**`step-type`: example**  
- Questions in this section:
  - Find the formula for the \(n\)th term of a sequence if the \(4\)th term is \(-135\) and the common ratio is \(-3\). \(a_n = \underline{\hspace{1.5cm}}\)
  - Consider the following geometric sequence: \(6, -2, \frac{2}{3}, \ldots\). The formula for the \(n\)th term of this sequence is \(a_n = \underline{\hspace{1.5cm}}\).
  - Find the formula for the \(n\)th term of the following geometric sequence: \(\frac{1}{3}, -1, 3, \ldots\).
- This step reverses the usual direction.
- Instead of being given \(a_1\), students use a later term or a listed sequence to recover the starting value and then write the full formula.
- The algebra is a little heavier because signs and exponents now have to be managed carefully.

**`step-title`: Finding a Particular Term Given a Non-First Term and Common Ratio**  
**`step-type`: example**  
- Questions in this section:
  - If the fifth term of a geometric sequence is \(\frac{1}{8}\) and the common ratio is \(\frac{1}{4}\), then the eighth term of this sequence is \(\underline{\hspace{1.5cm}}\).
  - Given that the \(8\)th term of a geometric sequence is \(8\), and the common ratio is \(\frac{1}{2}\), find the fifteenth term.
  - Find the formula for the \(n\)th term of a geometric sequence if the fourth term is \(-\frac{2}{3}\) and the common ratio is \(-2\). \(a_n = \underline{\hspace{1.5cm}}\)
- This combines the previous two moves.
- Students first work backward to recover the starting term and then move forward again to a requested later term.
- The last question checks that the same backward setup can also end with a formula instead of a single numerical term.

---

<a id="complex-numbers"></a>
## `lesson-title`: Complex Numbers

**`step-title`: Introduction to Complex Numbers**  
**`step-type`: tutorial**  
- Questions in this section: none.
- This step defines the standard form \(a + bi\) and names the real and imaginary parts.
- The later examples mainly vary how obvious those two parts are.

**`step-title`: Identifying Real and Imaginary Parts (Standard Form)**  
**`step-type`: example**  
- Questions in this section:
  - What is the imaginary part of the complex number \(20 - 25i\)?
  - What is the real part of the complex number \(-\frac{5}{4} + \frac{7}{2}i\)?
- Students can read the two parts directly because the number is already in standard form.
- The only wrinkle is preserving the sign on the coefficient of \(i\).

**`step-title`: Identifying Parts from Nonstandard Form**  
**`step-type`: example**  
- Questions in this section:
  - What is the real part of the complex number \(\pi + 2i - 1\)?
  - What is the imaginary part of the complex number \(\sqrt{2}i + 1 - \sqrt{5}\)?
- Now the complex number is not written as \(a + bi\) yet.
- Students must first reorder or combine terms before they can extract the real and imaginary parts.

**`step-title`: Complex Numbers with Zero Real or Imaginary Part**  
**`step-type`: tutorial**  
- Questions in this section: none.
- This section introduces the edge cases \(a + 0i\) and \(0 + bi\).
- It explains why real numbers and purely imaginary numbers still fit inside the same complex-number framework.

**`step-title`: Real Part of a Purely Imaginary Number**  
**`step-type`: example**  
- Questions in this section:
  - What is the real part of the complex number \(9i\)?
  - What is the real part of the complex number \(\sqrt{3}i\)?
- Students now apply the zero-real-part idea to numbers that look like just \(bi\).
- The new wrinkle is noticing the hidden \(0\) in the real part.

**`step-title`: Imaginary Part of a Real Number**  
**`step-type`: example**  
- Questions in this section:
  - What is the imaginary part of the complex number \(8\)?
  - What is the imaginary part of the complex number \(-\sqrt{5}\)?
- This mirrors the previous step in the other direction.
- Students treat an ordinary real number as \(a + 0i\) and identify the hidden imaginary part.

---

<a id="eulers-formula"></a>
## `lesson-title`: Euler's Formula

**`step-title`: Introduction to Euler's Formula**  
**`step-type`: tutorial**  
- Questions in this section: none.
- This step introduces \(e^{i\theta} = \cos\theta + i\sin\theta\) and connects Cartesian, polar, and exponential forms.
- It frames modulus and argument as the two quantities needed for later conversions.

**`step-title`: Writing a Complex Number in Exponential Form**  
**`step-type`: example**  
- Questions in this section:
  - Write the complex number \(z = -1 + 2i\) in the form \(re^{i\theta}\), giving \(\theta\) in radians to \(3\) decimal places.
  - Write the complex number \(z = -1 + i\) in exponential form.
- Students convert from \(x + iy\) to \(re^{i\theta}\) by computing magnitude and argument.
- One question needs a decimal angle from a calculator, while another lands on a familiar exact angle.

**`step-title`: Writing from an Argand Diagram**  
**`step-type`: example**  
- Questions in this section:
  - Write the complex number \(z\), shown on the Argand diagram above, in the form \(re^{i\theta}\), giving \(\theta\) in radians to three decimal places.
  - Write the complex number \(z\), shown on the Argand diagram above, in exponential form.
- The same conversion now starts from a picture instead of from coordinates.
- Students must first read the point from the diagram and determine the correct quadrant before finding the angle.

**`step-title`: Proving Sum Formulas for Sine and Cosine**  
**`step-type`: tutorial**  
- Questions in this section: none.
- The lesson now shifts from computation to proof.
- The final wrinkle is multiplying exponential forms, expanding with Euler's formula, and then matching real and imaginary parts to derive the sine and cosine sum formulas.
