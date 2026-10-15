# 4. Template extraction

The stable backbone is the source's exact integrand structure and response contract, followed by its ordered trigonometric identity rewrites, substitution declaration, differential conversion, any limit table, transformed integral, primitive, and final reciprocal/log/endpoint rewrites. A template uses only stages present in its own source. Some sources start directly with substitution; q-49256/q-49280/q-49281 use the linear argument substitution after normalization. That distinction is retained.

Two authored conservative slots are declared before implementation. Let the original integrand be f(x). Generate k f(a x), dividing each finite x endpoint by a. Here a is a builtin integer 1..6; k is an independently chosen builtin integer from -6..-1 or 1..6. Original parameters are a=k=1. The source coefficients, 0/1 endpoints, exponents, any additive 1, radical structure and field fragments remain eligible. k is an outside multiplier, not tied to a or a numerator already inside f. a changes every x argument, original domain component, limit endpoint, substitution reference and du relation together. Fixed argument-space endpoints preserve the original elementary endpoint arithmetic; allowing unrelated endpoints would change that workload. Exponents, identity structure, radical form, operator mix and number of stages are fixed because they determine the method and level, not simply because one example used them. No new operations, question forms or progression are introduced within a level.

For every original collected answer D(x)+C, the complete recipe is (k/a)D(a x)+C. For definite answers D, it is (k/a)D. Every compound mistake, unusual coefficient, wrong function argument and nested function in each observed bank is retained in D, rather than replaced by a plausible distractor. A complete source profile is selected before slots are sampled. All five recipes are emitted together. There is no pooled list, first-valid option filling, fallback profile or authored mixed bank. This invertible variable/scalar transformation preserves distinctness and correctness designation; the validator also reads the rendered values and derivatives. The seed is not part of task identity. Mathematical task identity is the canonical actual integrand/bounds and original domain-hole contract, independent of source profile, bank, field shape, choice order and seed. Content IDs retain full field/bank distinctions. Batch deduplication is local to the requested batch and does not suppress source parameter values.

The solution renderer keeps original prose sentences and every source mathematical operand. It scales x-integrals by k, u-integrals and primitives by k/a, and updates the derivative and reciprocal differential coefficients by a and 1/a respectively. The arbitrary constant stays C. The changed solution retains formal operands and intermediate expressions even where algebra could simplify them. Original replay is the normalized captured solution verbatim. Fidelity is checked separately from exact mathematics and native learner grading.

All identities are valid on each original domain component. Positive a preserves component orientation. q-49280 excludes original sin(4ax)=0 holes even after cancellation; q-49281 excludes original cos(2ax)=0 holes even though its simplified integrand is a cosine. Root profiles require cos(ax)>0; the original tangent excludes zero boundaries. Log absolute values are preserved. An indefinite C is arbitrary on each connected interval; unrelated intervals may have independent constants. Logarithms are never forcibly expanded and roots are never forcibly denested. Antiderivatives differing by a constant or by a nonzero constant inside a log absolute value are equivalent on each component and cannot serve as distractors merely for that difference.

No source mathematical error was found. Eleven source profiles contain a presentation capture defect: bare brace-group trigonometric function names, such as `{sec}`, render as italic letter products. Their exact raw normalized replays remain in source-cases.json with eligible_for_serving=false. Normal generation uses a separately supported operatorname repair, with those eleven original repairs included in review-cases.json and detailed in source-errors-and-repairs.json. The mixed operatorname forms already present in the same source identities/substitutions establish the intended functions; no operand, stage, bank member or correct designation changes. q-352797 has two equivalent collected blank values with different answer IDs; preserve both. The generic reciprocal identity in q-49281 uses x rather than the instance's 2x, and is universally valid. No missing image assets are guessed.

## q-2622

Source DB ID 17592186064673. Prompt: Calculate $\int \operatorname{tan}⁡x\sqrt{\operatorname{cos}⁡x}\,\text{d}x.$

Field `selection` is radio, with 5 collected values. Source substitution `u=cos(x)`, transformed integrand `-1/sqrt(u)`, primitive `-2*sqrt(u)`. Indefinite; include C. Domain: `cos(x)>0; original tan poles excluded`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-49259

Source DB ID 17592186064856. Prompt: $\int \operatorname{cot}⁡x\,\text{d}x=$

Field `selection` is radio, with 5 collected values. Source substitution `u=sin(x)`, transformed integrand `1/u`, primitive `log(Abs(u))`. Indefinite; include C. Domain: `sin(x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-114294

Source DB ID 17592186250228. Prompt: $\int \operatorname{tan}⁡x{sec}^{3}⁡x\,\text{d}x=$

Field `selection` is radio, with 5 collected values. Source substitution `u=cos(x)`, transformed integrand `-1/u**4`, primitive `1/(3*u**3)`. Indefinite; include C. Domain: `cos(x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-347941

Source DB ID 17592186319212. Prompt: Evaluate the following integral. Do not round the answer.

${\int }_{\pi /9}^{\pi /6}\frac{3\operatorname{cos}⁡(3x)}{{sin}^{2}⁡(3x)}\,\text{d}x=$
{{field-1}}

Field `field-1` is blank, with 1 collected values. Source substitution `u=sin(3*x)`, transformed integrand `1/u**2`, primitive `-1/u`. Original bounds `['pi/9', 'pi/6']`. Domain: `sin(3*x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-352786

Source DB ID 17592186321040. Prompt: Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /3}{sec}^{3}\,x\,\operatorname{tan}⁡x\,\text{d}x=$
{{field-1}}

Field `field-1` is blank, with 1 collected values. Source substitution `u=sec(x)`, transformed integrand `u**2`, primitive `u**3/3`. Original bounds `['0', 'pi/3']`. Domain: `cos(x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-352797

Source DB ID 17592186321041. Prompt: Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /12}\frac{2\operatorname{cos}⁡(2x)}{1+\operatorname{sin}⁡(2x)}\,\text{d}x=$
{{field-1}}

Field `field-1` is blank, with 2 collected values. Source substitution `u=1+sin(2*x)`, transformed integrand `1/u`, primitive `log(Abs(u))`. Original bounds `['0', 'pi/12']`. Domain: `1+sin(2*x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-352798

Source DB ID 17592186321042. Prompt: Evaluate the following integral. Do not round the answer.

${\int }_{\pi /12}^{\pi /6}\frac{2\operatorname{cos}⁡(2x)}{\operatorname{sin}⁡(2x)}\,\text{d}x=$
{{field-1}}

Field `field-1` is blank, with 1 collected values. Source substitution `u=sin(2*x)`, transformed integrand `1/u`, primitive `log(Abs(u))`. Original bounds `['pi/12', 'pi/6']`. Domain: `sin(2*x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-362157

Source DB ID 17592186323768. Prompt: Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /3}\operatorname{tan}⁡(x)\sqrt{\operatorname{cos}⁡(x)}\,\text{d}x=$
{{field-1}}

Field `field-1` is blank, with 1 collected values. Source substitution `u=cos(x)`, transformed integrand `-1/sqrt(u)`, primitive `-2*sqrt(u)`. Original bounds `['0', 'pi/3']`. Domain: `cos(x)>0; original tan poles excluded`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-49256

Source DB ID 17592186332684. Prompt: Calculate $\int \frac{\operatorname{sec}⁡3x}{\operatorname{cos}⁡3x}\,\text{d}x.$

Field `selection` is radio, with 5 collected values. Source substitution `u=3*x`, transformed integrand `sec(u)**2/3`, primitive `tan(u)/3`. Indefinite; include C. Domain: `cos(3*x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-49257

Source DB ID 17592186332685. Prompt: Evaluate ${\int }_{\pi /8}^{\pi /4}\frac{2\operatorname{cos}⁡(2x)}{{sin}^{2}⁡(2x)}\,\text{d}x.$

Field `selection` is radio, with 5 collected values. Source substitution `u=sin(2*x)`, transformed integrand `1/u**2`, primitive `-1/u`. Original bounds `['pi/8', 'pi/4']`. Domain: `sin(2*x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-49277

Source DB ID 17592186332689. Prompt: $\int \operatorname{sin}⁡x{sec}^{2}⁡x\,\text{d}x=$

Field `selection` is radio, with 5 collected values. Source substitution `u=cos(x)`, transformed integrand `-1/u**2`, primitive `1/u`. Indefinite; include C. Domain: `cos(x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-49278

Source DB ID 17592186332690. Prompt: $\int \operatorname{sin}⁡3x\operatorname{sec}⁡3x\,\text{d}x=$

Field `selection` is radio, with 5 collected values. Source substitution `u=cos(3*x)`, transformed integrand `-1/(3*u)`, primitive `-log(Abs(u))/3`. Indefinite; include C. Domain: `cos(3*x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-49280

Source DB ID 17592186332691. Prompt: Calculate $\int \frac{\operatorname{tan}⁡4x}{\operatorname{cos}⁡4x\operatorname{sin}⁡4x}\,\text{d}x.$

Field `selection` is radio, with 5 collected values. Source substitution `u=4*x`, transformed integrand `sec(u)**2/4`, primitive `tan(u)/4`. Indefinite; include C. Domain: `cos(4*x)!=0 AND sin(4*x)!=0; retain cancelled sine holes`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-49281

Source DB ID 17592186332692. Prompt: Calculate $\int \frac{1}{{sec}^{2}⁡2x\operatorname{cos}⁡2x}\,\text{d}x.$

Field `selection` is radio, with 5 collected values. Source substitution `u=2*x`, transformed integrand `cos(u)/2`, primitive `sin(u)/2`. Indefinite; include C. Domain: `cos(2*x)!=0; retain holes of original sec expression`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-10040

Source DB ID 17592186431115. Prompt: ${\int }_{0}^{1}\operatorname{tan}⁡x\,\text{d}x=$

Field `selection` is radio, with 5 collected values. Source substitution `u=cos(x)`, transformed integrand `-1/u`, primitive `-log(Abs(u))`. Original bounds `['0', '1']`. Domain: `cos(x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-49279

Source DB ID 17592186431116. Prompt: ${\int }_{\pi /6}^{\pi /3}\frac{{tan}^{2}⁡x}{{cos}^{2}⁡x}\,\text{d}x=$

Field `selection` is radio, with 5 collected values. Source substitution `u=tan(x)`, transformed integrand `u**2`, primitive `u**3/3`. Original bounds `['pi/6', 'pi/3']`. Domain: `cos(x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-362158

Source DB ID 17592186431119. Prompt: Evaluate the following integral. Do not round the answer.

${\int }_{\pi /24}^{\pi /8}\operatorname{cot}⁡(4x)\,\text{d}x=$
{{field-1}}

Field `field-1` is blank, with 1 collected values. Source substitution `u=sin(4*x)`, transformed integrand `1/(4*u)`, primitive `log(Abs(u))/4`. Original bounds `['pi/24', 'pi/8']`. Domain: `sin(4*x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-114295

Source DB ID 17592186431120. Prompt: $\int \operatorname{tan}⁡(\frac{x}{2})\text{d}x=$

Field `selection` is radio, with 5 collected values. Source substitution `u=cos(x/2)`, transformed integrand `-2/u`, primitive `-2*log(Abs(u))`. Indefinite; include C. Domain: `cos(x/2)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-73371

Source DB ID 17592186505780. Prompt: ${\int }_{\pi /12}^{\pi /4}\frac{\operatorname{cot}⁡(2x)}{{sin}^{4}⁡(2x)}\,\text{d}x=$

Field `selection` is radio, with 5 collected values. Source substitution `u=sin(2*x)`, transformed integrand `1/(2*u**5)`, primitive `-1/(8*u**4)`. Original bounds `['pi/12', 'pi/4']`. Domain: `sin(2*x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.

## q-347942

Source DB ID 17592186505828. Prompt: Evaluate the following integral. Do not round the answer.

${\int }_{\pi /18}^{\pi /6}\frac{\operatorname{cot}⁡(3x)}{{sin}^{4}⁡(3x)}\,\text{d}x=$
{{field-1}}

Field `field-1` is blank, with 1 collected values. Source substitution `u=sin(3*x)`, transformed integrand `1/(3*u**5)`, primitive `-1/(12*u**4)`. Original bounds `['pi/18', 'pi/6']`. Domain: `sin(3*x)!=0`.

Complete choices and recipes are recorded one-to-one by answer ID in choice-ledger.json. The exact source prose and ordered equality operands, including all intermediate reciprocal/root/log forms, are retained by the renderer; source-and-changed.md presents the full chain beside a changed instance.
