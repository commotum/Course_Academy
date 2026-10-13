# Classification

Provenance: `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. source.json copies the complete captured wrapper without changes. topic.json and lesson.json copy the owning topic and lesson wrappers. No EDB reads/writes were required.

| Difficulty | Practice sources | Layout / value templates | Complete banks | Plot rating |
|---|---:|---|---|---|
| easy, observed | 3 | factored_blank (q-218516, q-222107); factored_radio (q-111597) | two singleton blank banks; one 5-choice radio bank | none |
| unrated | 1 | factored_radio (q-76246), no solution/key/level | one 5-choice radio bank | none |
| moderate, observed | 2 | factored_blank (q-222113, q-222116) | two singleton blank banks | none |
| hard, authored | 0 | factored_blank, factored_radio | authored singleton / 5-choice method bank | none |

One shared mathematical family has two answer layouts; its formatting conditionals handle a bare first variable factor, positive/negative shifts, exponent-one suppression, and captured punctuation. All rated sources share the exact same 12-paragraph solution route. The unrated source preserves its missing solution in raw replay, while its separately labeled completion uses that full route. Two observed radio bank profiles are kept distinct; the latter has underdetermined pattern interpretations.

The authoritative captured q-76246 widget in legacy-widget-q-76246.json confirms one radio field and five choices, including the mathematically correct 20(x+3)^2(y-1)^3. It supplies no answer designation or worked solution. Therefore the correct reference is an independently derived completion, never counted as an observed correct designation. The unrated source receives an explicitly authored moderate label: numerical LCM20 from shared nondividing contents4/10, two existing factor bases and maximum exponent3. The label is a design claim, not an observed source rating. No raw mathematical value or presentation repair is needed.

## Curriculum scope and missing-level claim

Lesson ordering was reconstructed from activity/first-step=17592186152992 and step/next: introduction → constant-factor KP17592186152116 → single-variable KP17592186152117 → this two-multivariable KP17592186152118 → three-polynomial KP17592186152119. The predecessor topic is the LCM of two monomials. The canonical example is 6(x+3)^2(y+1)^2 and9(x+3)(y+1)^4; it independently confirms exactly two factor bases and maximum exponents, plus integer content LCM.

Normal easy retains coprime small constants (2–9, LCM≤60) and input exponents1–5 as in the three rated easy sources. Moderate uses shared nondividing content4–20, at least one content≥9, maximum exponent3–6 and LCM≤120. The rated sources9/15 and12/20 have maximum exponents5–6; the unrated4/10 source supplies a separately authored moderate completion with maximum3. Shared nondividing content is the consistent distinguishing demand, and the same bounds apply to every normal and raw replay profile. Hard is an authored workload claim: constants12–30 with nondividing shared content, LCM121–180, all exponents≥2 and maximum7–9. This increases numerical LCM arithmetic and exponent-reading workload without changing factor count, formal method, domain, or prerequisites. The hard label is not inferred from source data. All variants within a level are unordered same-method practice, not a progression. Both shifted factors and one bare variable remain eligible at every level; at least one binomial remains present. No expansion/factorization, rational coefficients, extra independent factor, or third polynomial is introduced.

Moderate radio includes the authored-rated unrated original; default moderate and hard radio are layout extensions using exactly the same assessment as the observed blank. Easy normal radio uses a defensible authored complete bank because the one rated source bank has opaque scalar recipes. Source profiles remain available and replayed through the public API.

Substantive variety includes integer content pairs, exponent allocation/maxima, and polynomial shift roots; variable renaming or option order is not claimed as another skill. Mathematical fingerprints canonicalize the whole two-polynomial task, input order and variable-letter aliases and exclude banks/profiles/layouts. Numerical coefficient/shift/exponent changes actually affect the assessed LCM. Presentation identities include actual prompt, fixed solution, fields, correct designation and full bank.

## Native grading restriction

The real symbolic parser (engine/rust/symbolic.rs::lex) limits input to4096 bytes and512 tokens. One authored hard fully expanded equivalent exceeds512 tokens and yields an unresolved parser-limit error; canonical factored, partially expanded and unreduced quotient equivalents are tested as accepted. Large fully expanded forms are mathematically correct but cannot be claimed accepted. This is a substantive known grading limitation, recorded separately in engine-validation.json and validation.json; no engine change or level omission is made.
