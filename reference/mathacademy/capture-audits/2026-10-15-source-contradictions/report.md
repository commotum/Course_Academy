# Source-contradiction capture repairs — 2026-10-15

The earlier diagnostic, editor-notation, and response-owned answer repairs have committed. At this check, the only remaining capture-gap warnings were q-340513 (Foundations activity 14227287) and q-138860 (Multivariable review 14220846). Their prompts, controls, choices, solutions, and learner outcomes were captured. Their concluding source answers matched none of the choices.

## Cause and correction

The final-judgment protocol preserved the concluding answer as Math Academy's only answer claim. It did not clearly permit an earlier complete result in the same solution to support an available choice. This made contradictions look like missing capture evidence even where the solution itself supplied the required answer.

The protocol now requires review of the complete solution. An earlier completed calculation or explicit judgments of every statement may supply `worked_solution` evidence if it unambiguously determines a current choice. The agent must quote one exact contiguous source span, explain equivalence, retain `source_error`, and identify the bad conclusion. Problem premises, mathematical plausibility alone, or the first API choice cannot establish source support. Unsupported cases remain omissions. A worked-solution interpretation is not a confirmed observation of the site's grading key.

Final-judgment caching now includes the interpretation-policy hash. A prior cached conclusion-only judgment cannot prevent the revised source review. Changed source interpretations preserve existing structured source claims where present. Original capture packages and all prior judgments remain archived.

## Repaired questions

- **q-340513, Introduction to Fourier Series:** the source explicitly marks I and II true and III false. The correct available choice is **I and II only**. The last sentence incorrectly says **I only**. The new judgment cites the complete statement analysis. The original last sentence is unchanged.
- **q-138860, Further Logarithmic Differentiation:** the earlier completed derivative is equivalent to `g(x)=\sqrt[3]{(3x+6)^4}`. The final equality and conclusion incorrectly change `+6` to `−6`. The new judgment quotes the derivative calculation before the typo. The original erroneous equality and conclusion are unchanged. With `t^3=3x+6`, differentiating `(x²+2)²/t` gives `(x²+2)(11x²+24x−2)/t⁴`; hence `g=t⁴`. Exact rational checks on six points covered both real domain components.

Both actual submitted wrong choices and their Incorrect grades remain unchanged. Neither alternative has been relabeled as an observed correct submission. No completed activity was replayed, and no assessment or diagnostic was interrupted.

## Verification and publication

Both complete packages passed source validation and source-aware native previews at basis **2681**:

- Foundations: 15 practice questions and 3 canonical examples; 31 assertions, no retractions, no unresolved omissions.
- Multivariable: 5 practice questions and the complete review structure; 56 assertions, no retractions, no unresolved omissions.

[Source preservation checks](source-preservation.json) confirm that prompts, solutions, choices, actual attempts, policy, completion, and account checkpoints remain unchanged.

The complete activities entered the normal 200-question batch queue. An admission-only placeholder with no manifest, immutable request, or receipt was archived and retired so the earlier repairs could be included when the worker reconsidered the queue. No committed or unresolved request was changed; no undersized flush or padding was used. All paused ordinary runners resumed with the revised policy.

All 167 targeted regressions passed. The full 201-question, 32-activity batch committed at basis **2683** from basis **2682**, and source-aware readback verified it as a no-op on re-preparation. Both repaired outbox entries are verified. The receipt contains 4,111 assertions and 126 retractions, with learner and engine facts unchanged. Pinned reads confirm both repaired keys, owning KP memberships, and the original erroneous conclusions. Final fleet integrity has **zero gap items and zero gap activities**. All four runners are active.

Evidence: [publication](published-repairs.json), [native previews](native-preview/), [regression output](verification/tests.txt), [receipt validation](receipt-validation.json), [pinned answer readback](pinned-readback/result.json), [verified imports](verified-imports.json), and [final fleet health](final-health.json).
