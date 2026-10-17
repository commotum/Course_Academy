At EDB basis 3429, **6 of the 53 selected topics fail fresh-lesson content readiness; 47 pass**.

The blockers are question shortages in 16 knowledge points. Each KP needs five usable questions not already seen or reserved. The deficient KPs need 44 additional usable question slots in total; this can include completing existing unusable questions, where possible, as well as adding questions. Missing correct-answer links are the main validation failure; one affected KP also has questions with no answer fields.

Every selected topic has exactly one lesson activity, and every lesson passed native route, tutorial, and canonical-example checks. None of the six blocked topics has a completed or resumable saved attempt. This is a content/supply check, not a simulation of every lifecycle/remediation or runtime condition. Explicit topic selection bypasses prerequisite/mastery gates.

All reads used the same immutable database value. The native check hydrated the learner’s 144 tasks and 431 history items once, then read one selected topic at a time. No global attribute scans, database writes, learner attempts, captures, or generation jobs were performed. The initial bounded metadata pull found 168 KPs and 2,260 question memberships, with at most 76 question memberships in one topic.

**Blocked topics**

| Topic ID | Topic | Deficient KPs | Additional usable questions needed |
|---|---|---:|---:|
| 17592186049053 | Solving Exponential Equations Using Logarithms | 3 | 6 |
| 17592186049195 | Combining the Laws of Logarithms | 3 | 9 |
| 17592186049879 | The Power Rule for Logarithms | 3 | 8 |
| 17592186050375 | The Product Rule for Logarithms | 2 | 6 |
| 17592186050542 | The Quotient Rule for Logarithms | 4 | 12 |
| 17592186050649 | Solving Equations Containing the Exponential Function | 1 | 3 |

**Deficient knowledge points**

| Topic ID | KP ID | KP | Usable unseen | Required |
|---|---|---|---:|---:|
| 17592186049053 | 17592186110593 | Finding Exact Solutions to Exponential Equations Using Logarithms | 2 | 5 |
| 17592186049053 | 17592186110594 | Finding Approximate Solutions to Exponential Equations Using Logarithms | 3 | 5 |
| 17592186049053 | 17592186110595 | Finding Solutions to Exponential Equations when Rearrangement is Required | 4 | 5 |
| 17592186049195 | 17592186054622 | Rewriting an Expression Using the Product and Power Rules of Logarithms | 2 | 5 |
| 17592186049195 | 17592186054624 | Rewriting an Expression Using the Product and Quotient Rules of Logarithms | 2 | 5 |
| 17592186049195 | 17592186054625 | Rewriting an Expression Using the Product, Quotient, and Power Rules of Logarithms | 2 | 5 |
| 17592186049879 | 17592186110596 | Simplifying the Logarithm of a Power Function Using the Power Rule | 2 | 5 |
| 17592186049879 | 17592186110597 | Writing an Expression as the Logarithm of a Power Function Using the Power Rule | 3 | 5 |
| 17592186049879 | 17592186110598 | Evaluating an Expression Using the Power Rule | 2 | 5 |
| 17592186050375 | 17592186110696 | Combining Logarithms Using the Product Rule | 2 | 5 |
| 17592186050375 | 17592186110699 | Evaluating an Expression Using the Product Rule | 2 | 5 |
| 17592186050542 | 17592186110589 | Separating a Logarithm Into Two Logarithms Using the Quotient Rule | 2 | 5 |
| 17592186050542 | 17592186110590 | Combining Logarithms Using the Quotient Rule | 2 | 5 |
| 17592186050542 | 17592186110591 | Combining Logarithms With Coefficients Using the Quotient Rule | 2 | 5 |
| 17592186050542 | 17592186110592 | Evaluating an Expression Using the Quotient Rule | 2 | 5 |
| 17592186050649 | 17592186087689 | Finding Exact Solutions to Exponential Equations Using the Natural Logarithm | 2 | 5 |

**All selected topics**

| Topic ID | Topic | Content readiness for fresh lesson | Saved attempt |
|---|---|---|---|
| 17592186048115 | Improper Integrals | Pass | — |
| 17592186048150 | Integrating Rational Functions Using Partial Fractions | Pass | — |
| 17592186048189 | Integration by Substitution With Inverse Trigonometric Functions | Pass | — |
| 17592186048191 | Selecting Procedures for Calculating Derivatives | Pass | — |
| 17592186048245 | Integrating Exponential Functions Using Substitution | Pass | — |
| 17592186048332 | Calculating Definite Integrals Using Substitution | Pass | — |
| 17592186048403 | Further Integration of Algebraic Functions Using Substitution | Pass | — |
| 17592186048470 | The Change of Base Formula for Logarithms | Pass | — |
| 17592186048489 | Slope Fields for Nonautonomous Differential Equations | Pass | — |
| 17592186048528 | Integrating Hyperbolic Functions Using Substitution | Pass | — |
| 17592186048557 | Integrating Linear Rational Functions Using Substitution | Pass | — |
| 17592186048569 | Solving First-Order Linear ODEs Using Integrating Factors | Pass | paused |
| 17592186048697 | Solving First-Order ODEs Using Separation of Variables | Pass | — |
| 17592186048777 | Integrating Trigonometric Functions | Pass | — |
| 17592186048813 | The Product Rule for Differentiation | Pass | paused |
| 17592186048842 | The Quotient Rule for Differentiation | Pass | — |
| 17592186049053 | Solving Exponential Equations Using Logarithms | Blocked: question supply | — |
| 17592186049119 | Calculating the Equation of a Normal Line Using Differentiation | Pass | — |
| 17592186049131 | Inhibited Decay Models With First-Order ODEs | Pass | — |
| 17592186049146 | Solving First-Order Linear ODEs With Exponential Forcing | Pass | — |
| 17592186049195 | Combining the Laws of Logarithms | Blocked: question supply | — |
| 17592186049332 | The Chain Rule With Logarithmic Functions | Pass | — |
| 17592186049380 | Solving First-Order ODEs Using Direct Integration | Pass | completed |
| 17592186049406 | Inhibited Growth Models With First-Order ODEs | Pass | — |
| 17592186049443 | Integrating the Reciprocal Function | Pass | paused |
| 17592186049481 | The Antiderivative | Pass | — |
| 17592186049486 | Verifying Solutions of Differential Equations | Pass | paused |
| 17592186049774 | Modeling Mixture Problems With First-Order Linear ODEs | Pass | — |
| 17592186049879 | The Power Rule for Logarithms | Blocked: question supply | — |
| 17592186049930 | Finding Equations of Parallel Lines | Pass | — |
| 17592186050101 | Integrating Exponential Functions Using Linear Substitution | Pass | — |
| 17592186050245 | Parallel Lines in the Coordinate Plane | Pass | — |
| 17592186050271 | The Chain Rule With Exponential Functions | Pass | — |
| 17592186050283 | Triangular Matrices | Pass | — |
| 17592186050375 | The Product Rule for Logarithms | Blocked: question supply | — |
| 17592186050409 | The Shortest Distance Between a Point and a Line | Pass | — |
| 17592186050420 | Differentiating Trigonometric Functions | Pass | paused |
| 17592186050473 | Finding Equations of Perpendicular Lines | Pass | — |
| 17592186050489 | Integrating Trigonometric Functions Using Substitution | Pass | — |
| 17592186050542 | The Quotient Rule for Logarithms | Blocked: question supply | — |
| 17592186050571 | Applying the Fundamental Theorem of Calculus to Exponential and Trigonometric Functions | Pass | — |
| 17592186050608 | Introduction to First-Order Linear ODEs | Pass | paused |
| 17592186050628 | Integrating Algebraic Functions Using Substitution | Pass | — |
| 17592186050649 | Solving Equations Containing the Exponential Function | Blocked: question supply | — |
| 17592186050771 | Integration Using Substitution | Pass | — |
| 17592186050783 | Integration Using Basic Trigonometric Identities | Pass | — |
| 17592186050789 | The Chain Rule With Trigonometric Functions | Pass | — |
| 17592186050898 | Integrating Logarithmic Functions Using Substitution | Pass | — |
| 17592186050902 | Second and Higher-Order Derivatives | Pass | — |
| 17592186050905 | Solving First-Order IVPs Using Separation of Variables | Pass | — |
| 17592186050985 | Differentiating Reciprocal Trigonometric Functions | Pass | — |
| 17592186051059 | Rewriting Radical Expressions Using the Laws of Exponents | Pass | — |
| 17592186051084 | The Chain Rule for Differentiation | Pass | completed |

Full counts, native validation reasons, read counters, and saved attempts are in [result.json](result.json). The reproducible read helper is [readiness.rs](readiness.rs), and its fixed input is [input.json](input.json).
