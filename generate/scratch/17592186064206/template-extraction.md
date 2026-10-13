# Extraction and sampling bounds

The exact per-source descriptions, original answer-to-recipe mappings, field ownership, parameters, prompts and solutions are in template-extraction.json. Contract.json retains separate prompt/solution templates, fixed instructional sentences and conditional source-specific substitution layouts. No choices are pooled across bank profiles.

The numerator is a positive integer; the denominator is affine in real x. Source coefficient cases have n=2 or 3, a=1 and positive integer b. Source unit-slope cases have n=a=1 with b=-1 or 3. The negative-slope case has n=1, a=-3, b=2, displayed constant first. The canonical example has n=3, a=5, b=2. The incomplete legacy case has n=2, a=3, b=5 and a separate incomplete bank.

Explicit bounded extensions: coefficient n=2..9, b=1..12; negative slope a=-9..-2, b=1..12; unit negative shift b=-12..-1; unit positive shift b=2..12. The restrictions avoid zero slopes, zero shifts, unit-coefficient reciprocal collisions and duplicate/correct distractors. No unsupported sign or structural extension is silently sampled. Observed valid source parameters are included in these bounds.

Correctness is checked by differentiating every rendered answer independently. Antiderivatives are equivalent up to an additive constant on each connected domain interval; checking derivatives prevents scalar multiples inside a logarithm from creating spurious novelty. The novelty key uses normalized n/a and b/a, excluding the seed, profile, prompt wording, choice order and identities. Authored identities additionally bind the exact bank and rendering layout to avoid a same-ID content conflict.

The unchanged source-specific worked solutions are replayed exactly. New instances follow the same sentence order and substitution/integration rows, including the source's cosmetic empty multiplication dot for unit numerators. No graphical assets exist, so plot extraction/generation is inapplicable.
