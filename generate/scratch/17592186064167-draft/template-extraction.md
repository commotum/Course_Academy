# Template and complete bank extraction

The immutable raw records are in source-cases.json. The original MA banks contain 25 choices across five profiles, including three captured keys and two absent keys. Full raw strings, fields, and solutions are replayed at source parameters. Canonical is a separate ninth replay.

The direct solution begins “We apply the power rule with n=…”, displays integral = x^(n+1)/(n+1)+C = simplified primitive, and follows “Let's check by differentiating:” with derivative of primitive+C; split derivatives; factor out reciprocal; evaluate power derivative; final integrand. The function wrapper first preserves the inverse-differentiation prose and three formal F'=f/integrate/F=integral rows, then substitutes x^n and uses the same rule/check. Constant 1 rewrites as x^0 before the rule, with four derivative rows. Unicode-prime and derivative thin-space differences are retained as presentation profiles. Canonical retains its observed notation. No new operation or solution stage is authored for variety.

Let m=n+1. Every bank is chosen in full before rendering; an invalid instance is rejected without pooling recipes. All expressions below include +C unless explicitly marked.

| Profile | Complete bank in captured order | Original n | Conditions |
| --- | --- | --- | --- |
| observed_2005 | m*x^m without C; x^m/m+C; m+C; x^m/m without C; x^m+C | 1 | n>=1 |
| observed_2022 | x^m+C; n*x^(n-1)+C; x^n/n+C; x^m/m+C; x^(n-1)+C | 4 | n>=2 |
| observed_113665 | x^m/m+C; m*x^(n-1)+C; x^m/(n-1)+C; x^(n-1)/(n-1)+C; n*x^m+C | 20 | n>=2 |
| observed_113668 | x^(n-1)/n+C; x^m/m+C; x^(n-1)/(n-1)+C; x^m+C; n*x^m+C | 13 | n>=2 |
| observed_29994 | n*x^m+C; x^n/n+C; m*x^m+C; x^m/m+C; x^n/m+C | 4 | n>=2 |
| authored_power | x^m/m+C; x^m+C; x^n/m+C; x^(m+1)/(m+1)+C; m*x^m+C | authored | n>=1 |

Correctness compares full primitive families: equal x derivatives plus nonzero C derivative. Pairwise comparisons operate modulo arbitrary integration constants, including rescaling C; missing C is a fixed primitive rather than the requested full family. The legacy observed_2005 normal prompt explicitly asks to include arbitrary C, preserving its two distinct source options. Full-field textual entries include any supplied suffix; this generator's blank has no suffix and expects the entire primitive including C.

At n=0, omission of division would duplicate the answer. The constant template selects a blank before constructing a bank; radio requests fail. Other bank guards exclude n<2 where predecessor recipes divide by zero or collide. Normal sampling picks a complete profile, then derives every option. None of the finite domains imply calibrated progression.

Raw legacy TeX commands, missing keys/solutions, and field absence are retained as evidence. Normal output separates the integral command from its argument, infers missing keys mathematically, authors missing solutions using the observed direct sequence, and authors fields for formerly fieldless cases. These repairs are explicit in source-repairs.json. The original evidence is never overwritten. Native blank grading's arbitrary-C limitation is preserved in validation.json, not treated as a source error.

Content IDs preserve the previous valid easy version, full question prose, complete banks, and field layout. New profiles include their complete displayed values in identity. Mathematical dedup uses only the assessed integrand and full-family response, excluding seed, shuffle, profile, layout, and difficulty aliases. Only 21 mathematical tasks exist in the declared finite scope.
