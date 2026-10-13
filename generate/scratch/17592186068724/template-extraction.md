# Template extraction

Integrate a numerator proportional to a polynomial denominator’s derivative, substituting u for the denominator and using ln|u|. Easy profiles use k*x^(n-1)/(a*x^n+c). Moderate profiles use (a*n*x^(n-1)+b)/(a*x^n+b*x+c). These are integrated separately over connected real intervals where the denominator is nonzero. The blank uses a strictly positive quadratic and expects the expression without the printed +K.

classification.json records every original prompt, parameter, field, choice, complete recipe, source bank, and solution. Fixed elements are field layouts, instructional sentences, template, degree, a, numerator coefficient k, variable, and coefficient signs. The bounded sampling extension varies positive constants 1–20 for easy and q-113719, or the signed linear coefficient magnitude 1–12 for other moderate profiles. Original parameters remain within these bounds. Whole banks with equivalent antiderivatives are rejected.

Bank formulas are implemented in bank() in the scoped script. q-72566 preserves altered polynomial expressions rather than inferring a learner mistake. The incomplete q-12500 bank is mapped but excluded. TeX ordering is normalized separately from mathematical replay. No plots require extraction or generation.

The blank profile’s certified constant range is 1–19. The engine accepts canonical and equivalent entries and rejects wrong-sign and wrong-factor entries throughout that range. At c=20 it returns unresolved for a wrong-sign entry; blank-domain-audit.json retains that exact result, and the sampler excludes c=20. The radio q-49572 retains absolute bars even when its denominator is positive, matching the observed source notation.
