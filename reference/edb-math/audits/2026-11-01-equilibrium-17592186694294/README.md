# Generated equilibrium question: excess algebra and incoherent solution path

Read-only review at math **T12103**. Question **17592186694294**, marked moderate, belongs to KP **17592186166788 — Identifying Equilibrium Solutions of a Differential Equation**, topic **17592186051068 — Equilibrium Solutions of First-Order ODEs**.

The registered generator is `generators/c5/c5e9f7bf83b7546d40cb21cc7a1766b4b127a2fd0daff1588261776b6b009ebe/generator.py`, version 1.0.1. Reconstructing its logarithmic model reproduces the exact prompt, worked solution and response contract. Applying the publisher's standard identity normalization also reproduces the served question UUID. This is current generated output, not an imported Math Academy question.

The bank is mathematically keyed correctly: after cancelling y+1 from both sides, f(c)=(c−1)²ln(c−1)+e⁻². The domain is c>1. For the three supplied candidates, f(2)=e⁻²≠0, f(1+e)=e²+e⁻²≠0 and f(1+e⁻¹)=−e⁻²+e⁻²=0. Only y=1+e⁻¹ is an equilibrium among the listed choices. No demand to find every root of this nonlinear equation is made.

The presentation defect is reproducible in the generator:

1. The moderate sampler deliberately adds an arbitrary linear expression to both sides of an already constructed residual. Here it adds y+1. This manufactures an extra cancellation step.
2. The solution printer computes `factor_terms(expand(rhs-lhs))`, spreading (y−1)²ln(y−1) across three terms and hiding the helpful shifted structure.
3. It then leaves that isolated derivative form unused and returns to separate L(c)/R(c) calculations for every candidate, repeatedly evaluating terms that cancel. The result is a long, changing presentation of a short equilibrium test.

All six imported practice questions and the canonical example were checked. Five practice questions are labeled easy; one is unclassified and incomplete. No imported moderate/hard difficulty anchors are present. Source q-96072 legitimately uses a logarithm: y′+e²=y²ln(y), with candidates 1, e and 2. Its worked solution rearranges once and evaluates one residual f(c). Therefore the objection is not to logarithms as a family; it is to the generator's added wrapping and its solution's unnecessary expansion and change of method. The shifted/negative-exponent version is authored extension, not a replay of that source instance.

A repair should preserve the given useful factor structure, rearrange only as necessary, and follow one argument: set y′=0, respect the original domain, then test f(c)=0. Difficulty should be calibrated from the required decisions and arithmetic, rather than adding a term merely to cancel it. This review changes no generator or database record.
