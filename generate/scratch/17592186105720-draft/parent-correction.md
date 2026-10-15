# Parent QA correction

The q-103603 mask originally varied the reciprocal coefficient and its printed `C = n ln K` definition, while one worked row retained the original `2 ln K` term. Differentiation erased that constant and failed to detect the stale parameter. The parent independently compared every primitive row with the designated K-family after applying the actual printed constant definition on both x > 0 and x < 0.

The missing coefficient is now a parameter slot throughout the solution. At the original n = 2 the source question remains exact. Changed parameters regenerate all dependent rows and content identities consistently. The private validator now checks exact primitive-family equalities under C = c ln K, with K positive and c the displayed integrand's nonzero reciprocal coefficient; a constant-only n = 3 mutation is an explicit regression. These checks supplement differentiation, complete bank checks and native radio selection tests.
