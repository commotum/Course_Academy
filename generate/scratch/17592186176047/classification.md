# Classification

Captured database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is an unchanged copy of the capture wrapper, including all eight practice questions and canonical e-11002. No database operations were performed.

| Captured difficulty | Questions | Field layout | Prompt/value templates | Complete banks | Plot rating |
|---|---:|---|---:|---:|---|
| Easy | 0 | None observed | 0 | 0 | None |
| Moderate | 6 | Five one-field text radio; one five-field math blank | 6 | Five radio banks; one five-field singleton bank set | None: unchanged rasters reused |
| Hard | 0 | None observed | 0 | 0 | None |
| Unrated | 2 | One text radio per question | 2 | Two complete radio banks | None |

Prompt structures and full solution sequences remain separate even when their categorical answer lists overlap. There are **eight observed layout/value templates**, seven complete five-option radio bank profiles and one five-field blank layout (12 fields, 40 displayed answer values). q-27015 and q-27021 have neither captured solutions nor captured correct refs. They receive an explicitly authored moderate routing assignment, supported by their three-statement structure and comparison with moderate q-70666/q-103233. Their two inferred correct refs cannot count as matched original designations.

| Source | Template / observed bank | Statement kinds | Truth vector | Solution form |
|---|---|---|---|---|
| q-27015 | q-27015 / observed-q-27015 | General maxima; local zero; range | F,T,F | Absent: authored three verdicts |
| q-27021 | q-27021 / observed-q-27021 | Complete zeros; general maxima; range | T,F,F | Absent: authored three verdicts |
| q-167631 | q-167631 / observed-q-167631 | Domain; range; period, five math fragments | All valid for its displayed sine | Plot → domain → range extrema → period |
| q-103230 | q-103230 / observed-q-103230 | Local zero; range; possible output | T,F,F | Plot → I → grouped II/III |
| q-103233 | q-103233 / observed-q-103233 | Complete zeros; point; general maxima | F,T,F | Plot → I → II → III |
| q-27009 | q-27009 / observed-q-27009 | Local zero; minimum; y-intercept | T,F,F | Plot with guides → I → II → III |
| q-70666 | q-70666 / observed-q-70666 | General maxima; local zero; range | F,T,F | Plot → I → II → III |
| q-70667 | q-70667 / observed-q-70667 | y-intercept; minimum; range | T,T,F | Plot → I → II → III |

The five-field q-167631 is a **sine question mislinked to the cosine KP**. Its exact original prompt, valid source answers and sine raster are preserved through the public observed replay profile. The normal q-167631 profile minimally changes sine to cosine and uses the cosine raster; its domain, range and period fragments remain mathematically valid. Inspection of answer string bytes confirms single backslashes in `\infty`/`\pi`; JSON display escaping is not a source error.

## Curriculum boundary and missing levels

The owning activity route was reconstructed from `:activity/first-step` and `:step/next`, not collection order:

17592186176855 Introduction → 17592186176856 **this KP** → 17592186176857 Periodicity tutorial → 17592186176858 periodicity KP → 17592186176895 Evenness tutorial → 17592186176875 evenness KP.

The preceding introduction establishes complete zero, maximum and minimum sets: `π/2+nπ`, `2nπ`, `π+2nπ`. The canonical example checks range, completeness of minima (`nπ` is false), and complete zeros. Key prerequisites are **Local Extrema of Functions** and **Graphing Sine and Cosine**. Even and Odd Functions is a topic prerequisite, but not a key prerequisite to this KP. Neither later sibling is imported as an extra generator branch. Domain/range/period factual descriptors occur in captured q-167631; no shifted expression evaluations are generated.

- Authored **easy** asks three local facts about three distinct unit-graph landmarks, using zero, maximum, minimum and y-intercept claims. Every instance has exactly three independent facts and a five-option categorical radio bank. There are 32 semantic claim sets: choose three of four distinct landmarks (0, π/2, π, 3π/2), with one true or false local claim at each. No difficulty progression occurs inside the catalog.
- Default authored **moderate** asks exactly one local zero claim, one complete maximum-family claim and one range claim. Its 72 claim sets retain the observed mixture of local and global reasoning, using four familiar angle residues, six distinct input families and three range endpoint-position claims. This is a labeled authored complete bank extension, not a claim that source banks were recovered for these new outcomes.
- Authored **hard** asks exactly three complete input-family claims, one each for zeros, maxima and minima. All 216 claim sets have the same three completeness/classification demands. The extra demand over local facts is distinguishing the full set from a proper subset or union containing wrong extrema. No inverse trigonometry, algebraic coefficients, transformations, periodic expression calculations, evenness evaluation or new skills are introduced.

The categorical structure is finite. Claims are deduplicated modulo the stated family step, and local landmarks modulo `2π`; naming a variable, shifting an equivalent family, changing seed, statement order or the answer bank does not inflate mathematical-task counts. The 32/72/216 counts describe the three authored default catalogs; observed replay templates are separately tracked, not added as unlimited diversity. The five-field untransformed domain/range/period template has one normal cosine mathematical object.

Incorrect symmetric range bounds 2, 3 and π are incidental magnitudes in a truth-classification task: their lower/upper endpoint positions are identical relative to [-1,1], so they share a mathematical fingerprint. Similarly, output magnitudes outside the range share the below/above classification fingerprint. Their actual displayed values still affect complete content identity and source-bank fidelity.
