# Lesson progression tags

This document demonstrates how MathAcademy composes lessons as a progression of tightly scoped sections. Each line highlights how a problem type incrementally increases in complexity relative to the previous one. The focus is on identifying structural changes—such as added steps, reversals, representation shifts, or edge cases—rather than re-explaining concepts. Each topic moves from a base form to layered variants, showing how similar-looking problems diverge through small but meaningful increases in reasoning depth.

---

## Imaginary Numbers

**Introduction**  
base form / $\sqrt{-a}$ / factor $-1$ / rewrite as $i\sqrt{a}$ / core imaginary conversion

**Finding the Square Root of a Negative Number**  
perfect-square $a$ / direct $\sqrt{-a} = i\sqrt{a}$ / integer coefficient / no simplification

**Finding the Negative Square Root of a Negative Number**  
leading negative / $-\sqrt{-a}$ / convert + track sign / one extra step

**Finding the Square Root of a Negative Number With Simplifications**  
nonperfect $a$ / factor $a = k^2 m$ / simplify $\sqrt{m}$ / then attach $i$

**Finding the Square Root of a Negative Fraction**  
$\sqrt{-\frac{a}{b}}$ / split roots $\frac{\sqrt{a}}{\sqrt{b}}$ / simplify fraction / attach $i$ / multi-step

---

## The Nth Term of a Geometric Sequence

**Introduction**  
nth-term form / $a_n = a_1 r^{n-1}$ / identify $a_1, r, n$ / forward evaluation

**Finding a Particular Term Given the First Term and Common Ratio**  
$a_1, r$ given / direct substitution into $a_n$ / single output / minimal complexity

**Finding a Formula for the Nth Term**  
given later term $a_k$ + $r$ / solve for $a_1$ / build $a_n = a_1 r^{n-1}$ / reverse step added

**Finding a Particular Term Given a Non-First Term and Common Ratio**  
given $a_k$ + $r$ / recover $a_1$ / then compute $a_n$ / reverse then forward chain

---

## Complex Numbers

**Introduction**  
standard form $a + bi$ / real vs imaginary parts / notation $\mathrm{Re}, \mathrm{Im}$ / base structure

**Identifying Real and Imaginary Parts (Standard Form)**  
already $a + bi$ / read-off $a, b$ / sign preserved / direct extraction

**Identifying Parts from Nonstandard Form**  
reordered expression / combine like terms / rewrite to $a + bi$ / then extract

**Complex Numbers with Zero Real or Imaginary Part**  
$a + 0i$, $0 + bi$ / classification / real vs purely imaginary / edge structure

**Real Part of a Purely Imaginary Number**  
input $bi$ / interpret as $0 + bi$ / $\mathrm{Re} = 0$

**Imaginary Part of a Real Number**  
input $a$ / interpret as $a + 0i$ / $\mathrm{Im} = 0$

---

## Euler's Formula

**Introduction**  
$$e^{i\theta} = \cos\theta + i\sin\theta$$  
bridge exponential and trig / modulus-argument framework / base identity

**Writing a Complex Number in Exponential Form**  
given $x + iy$ / compute $r = \sqrt{x^2 + y^2}$ / compute $\theta = \tan^{-1}(y/x)$ / form $re^{i\theta}$

**Writing from an Argand Diagram**  
graph input / read $(x,y)$ / determine quadrant / compute $r, \theta$ / convert to $re^{i\theta}$

**Proving Sum Formulas for Sine and Cosine**  
use $e^{i(\alpha+\beta)} = e^{i\alpha} e^{i\beta}$ / expand both sides / match real + imaginary parts / derive identities