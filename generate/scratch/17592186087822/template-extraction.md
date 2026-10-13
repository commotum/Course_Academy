# Template extraction: four stages

## 1. Specific source descriptions

The five easy originals have integer bases 25,7,12,3,2 and shifts +10,-5,-3,-2,-3. Each shows its corresponding explicitly labeled asymptote and asks to determine c and find the equation; one five-choice radio presents complete y=… equations. Correct values are those supplied-base exponentials plus the plotted label. The shared solution first states the base curve's zero asymptote, then its vertical translation to y=c, then reads the label and concludes c. q-99775 alone opens with base2 instead of12 (raw evidence retained).

Moderate q-170593 supplies 13/6, shows y=-3/2 and presents five fractional shifted equations. Its solution has the same two paragraphs/four sentences and no algebraic computation rows. Actual decoded bytes confirm one backslash per fraction command in prompt, choices and solution.

The unrated q-26807 and q-7228 supply 17 and2 and explicitly label -4 and+1 respectively. Their choices retain spaced equation typography, but their captured solution and correct attributes are absent. Public raw replay preserves those omissions rather than synthesize authoritative fields. Their diagram labels and y=b^x+c independently determine the inferred values.

## 2. General pattern

For b>1, horizontal asymptote of b^x is zero; adding c translates it to c. Read exactly one horizontal level and select the full equation y=b^x+c. Bases are supplied, never solved for. Fixed one worked solution is independent of any distractor chosen.

## 3. Complete components and observed banks

`source-bank-map.json` enumerates EVERY source option with original rendered value, field ownership, recipe expression, exact computed complete equation and correct-presence designation. Bank definitions in the script are ordered whole profiles, not pooled distractors. For notation `S(a,d)` means y=b^x+(a*c+d); `M(a,d)` means y=(a*c+d)b^x; `B(1,-1)` means y=(b+1)^x+c-1. Thus every operation is parametric and source replay runs the normal API.

| Source/profile | complete observed bank in original order | interpretation limits |
|---|---|---|
| q-26807 | S(1,0), S(1,1), S(-1,1), S(-1,-1), S(-1,0) | shifts/sign and intercept offsets plausible; original intent not proved |
| q-7228 | S(1,1), S(1,0), M(1,2), S(0,0), M(1,1) | multiplier offsets underdetermined |
| q-170593 | S(1,5/6), S(1,1), S(1,11/6), S(1,0), S(1,7/3) | fractional offsets opaque; NOT default learning recipes |
| q-26804 | S(-1,0), S(-1,-1), S(1,1), S(1,0), S(1,5) | final +5 underdetermined; evidence profile only |
| q-99774 | S(-1,0), M(1,0), S(0,0), M(-1,0), S(1,0) | coherent sign/shift/stretch recognition mistakes |
| q-99775 | M(1,0), S(-1,0), S(1,0), M(-1,0), S(0,0) | same semantic bank with swapped order |
| q-7230 | M(1,-1), S(1,1), S(1,-1), S(1,0), M(1,0) | ±1 intercept confusion; mistaken stretch |
| q-7232 | S(1,1), M(1,0), S(1,0), B(1,-1), M(-1,0) | compound altered-base/shift option underdetermined |

The wrong equations with multipliers are distractors, not an assessed unknown stretch. The same supplied-base shifted equation remains the only valid response. Historical affine offsets are explicitly fitted observed patterns with unresolved intent; recovering exact numerical bank values does not establish original authoring logic. All raw historical profiles are flagged evidence-only/ineligible, including coherent ones, because their raw attribute omissions and source defects are preserved conservatively; the coherent q-26807 bank also serves normal source-shaped questions through the eligible `signed_intercept` profile. They still accept changed parameters and reject ambiguous whole banks.

## 4. Reusable masks, domains and authored defaults

The script constructs complete base components in source-specific spaced/compact/fraction styles, complete shifted or multiplied equation components, and source prose masks replacing complete exponential components and complete y=c/c=c mathematical sentences. Source ID does not dispatch to a copied payload: it selects a style, complete recipe bank and prose structure, all recomputed at explicit parameters. Raw original-image reuse occurs only at its exact original b,c; changed parameters invoke the shared renderer.

Fixed: one graph-before-prose prompt, one selection radio, five whole equations, source asymptote rule and two-paragraph solution. Variable: exact supplied base, c, graph geometry and every bank equation. Optional only for raw evidence: originally absent attributes. Conditional: source typography, raw q-99775 illustrative opener retained; normal solutions always name actual base. Parameter/domain guards are identical for explicit and sampled calls. Collision rejects the WHOLE chosen bank; no replacement from a pool.

Normal default bank profiles are chosen before parameters: `signed_intercept` directly retains the complete q-26807 source bank [c,c+1,-c+1,-c-1,-c], with sign and intercept confusion as a provisional interpretation; the other profiles are explicitly authored. `confuse_shift_stretch` uses [c,-c,0] shifts and c/-c multipliers; `intercept_offset` uses [c,c+1,c-1] shifts and c/(c-1) multipliers; `axis_reading` uses [c,c+step,c-step,-c,0] shifts. The errors come from reading the asymptote/intercept, reversing its sign, omitting the shift or confusing it with multiplication. `axis_reading` is eligible ONLY for hard and uses its actual calibration step. Easy/moderate have no artificial fractional-axis misread profile. Every bank is complete before parameter selection and all five expressions must be distinct and exactly one correct. No distractor diagnosis is added to learner content.

Normal worked solutions preserve the source's rule → translation → read level → conclusion sentences and exact paragraph count. Missing raw solutions remain absent; inferred values live only in generation metadata. The q-99775 base mismatch is kept in raw source evidence; the normal rule substitutes the actual base, an explicitly supported prose correction, with raw-exact and repaired mathematics counted separately.

Meaningful task enumeration excludes base aliases, whitespace, bank/profile/order changes and plot-window scaling. Labeled tasks are distinguished by c; hard tasks by c plus actual calibration step. Content identity separately includes generator version, actual difficulty presence/value, rendered prompt, fixed solution and COMPLETE sorted bank. Fixed displayed content keeps UUID identity across seeds/choice order; a different displayed bank changes it.
