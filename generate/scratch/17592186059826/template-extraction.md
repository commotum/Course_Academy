# Current template extraction

The original basis-1356 four-stage extraction is preserved in `reference/legacy-basis-1356/template-extraction.md`. `current-source.json` preserves every source parameter, prompt, answer value/type, field key/type, correct ref where available, and fixed worked solution at basis 2091.

1. q-102204 has a=3,b=7,x and a spaced strict inequality prompt; q-59294 has a=3,b=4,x and an interval-membership prompt. Both lack difficulty, key and solution. q-1256 has a=-3,b=-1,x, a compact strict inequality prompt, easy rating, five math intervals and a three-stage plain-punctuation solution. q-154704 has a=-sqrt(2),b=sqrt(2),x with the same compact prompt and plain three-stage solution; its rating is also easy. All endpoints are finite, ordered, exact, and excluded. No arithmetic or simplification is requested.
2. For a<b, convert a<x<b to (a,b) or conversely; preserve both endpoints and their exclusion. Separate directions, prompt spacing and source solution layouts remain explicit.
3. Every source choice belongs to the radio field `selection`. Each source bank is reproduced as one complete profile, ignoring choice order only.

| Source/profile | Correct recipe | Four wrong recipes |
|---|---|---|
| q-102204 / original_bank | (a,b), math | (-∞,b); [a,b]; (a,b]; [a,b), all math |
| q-59294 / original_bank | a<x<b, math | a≤x<b; a<x≤b; text `$x<a$ or $x>b$`; a≤x≤b |
| q-1256 / signed_source | (a,b), math | [a,b]; (a,b]; [a,b); (-b,-a), all math |
| q-154704 / surd_source | (a,b), math | [a,b]; (a,b]; [a,b); (-∞,b), all math |

All 20 options are direct parameterized recipes; none is unmapped. The reflected signed distractor reverses and negates both endpoints, rather than copying (1,3). It is eligible only for two negative integers and cannot equal the open answer. The surd profile requires symmetric squarefree radical endpoints. Its omitted-bound option preserves original TeX infinity spacing. Generic profiles retain their complete five-option banks; no mixed profiles are sampled.

4. Fixed components: original prompt sentences, five-option field layout and `selection` key, text/math types, bracket and inequality relations, solution prose and displayed stage order. Variables: complete exact endpoint expressions and variable x/y/t/z. Conditions: signed and surd profile guards, TeX radical rendering, and sampling catalog. The source_raw profile preserves absent original keys/ratings/solutions. Normal generic output supplies independently derived keys and authored colored solutions anchored in canonical wording. New compact profiles reproduce their fixed source solutions byte for byte at original parameters and preserve all three displayed stages for variants. The generic reverse solution has three displayed stages; interval-to-inequality has two. Current canonical whitespace differs from the earlier normalized capture; it is retained unchanged and not claimed byte-identical to authored solutions. Set semantics validates each displayed stage.

No images occur in prompts, options or solutions; steps 5 and 7 need no plot extraction, construction, publication, or assets. Complete-bank fidelity is 4/4, all options 20/20; captured keys and practice solutions are 2/2, with the other two absent rather than credited as matched. Exact replay, independent set semantics, source profile boundary coverage, deterministic identities and actual native grading are recorded in current-validation.json.
