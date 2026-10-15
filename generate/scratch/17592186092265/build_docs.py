import sys
sys.dont_write_bytecode=True
import importlib.util,json,hashlib,collections,shutil
from pathlib import Path
H=Path(__file__).resolve().parent
z=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
def dump(name,v):(H/name).write_text(json.dumps(v,indent=2)+'\n')
source=json.loads((H/'source-cases.json').read_text());counts=collections.Counter(q.get(':question/difficulty',{}).get(':db/ident','unrated') for q in g.ROWS.values())
classification={'database':'math','basis':2275,'lineage':g.SOURCE['lineage'],'source_counts':dict(counts),'non_ma_count':0,'source_specific_layouts':16,'mathematical_backbones':{'easy':['affine logarithm derivative'],'moderate':['power logarithm derivative','affine logarithm tangent slope'],'hard':['square-root logarithm derivative']},'observed_radio_profiles':6,'plot_rating':'none','field_anomalies':{'q-1948':['unrated','missing correct reference','missing worked solution'],'q-48008':['unrated','missing correct reference','missing worked solution'],'q-1949':['absent answer-field contract'],'q-48001':['absent answer-field contract'],'q-71479':['absent answer-field contract'],'q-341686':['blank has neither choices nor correct reference']},'actual_lesson_order':[17592186093122,17592186093123,17592186093124],'prerequisite_topics':[17592186050690,17592186051084]};dump('classification.json',classification)
recipes={
'q-1948':['1/(sqrt(a*x)*L)','a/(2*sqrt(a*x)*L)','1/(2*x*L) correct','1/(x*L)','1/(2*x)'],
'q-48008':['a/((-c*x-a)*L)','1/((a*x+c)*ln(a))','a/((a*x+c)*ln(a))','a/((a*x+c)*L) correct','a/(a*x+c)'],
'q-48559':['1/(x^n*L)','n/x','n/(x*L) correct','n/x^(n-1)','1/(n*x*L)'],
'q-48656':['a/L','a/(b*L)','b/(a*L)','a/((a*t+c)*L) correct','b/L'],
'q-51317':['-1/((c-x)*L) correct','b/(c-x)','-1/(c-x)','(c-x)*L','L/(c-x)'],
'q-71478':['1/(x*L)','1/(2*x)','2/x','2/(x*L)','1/(2*x*L) correct']}
extraction={'basis':2275,'original_parameters':{t:g.original(t) for t in g.TEMPLATES},'source_cases':source,'recipe_profiles':recipes,'recipe_notation':'L=ln(b); the whole profile is chosen before parameters; all five choices used, pairwise collisions reject whole instance. Recipes are observed expression patterns, not claims about learner misconceptions.','slots':{'base':'integer 2..10; common-log conversion q51317 fixed10','affine_coefficient':'nonzero signed integer -9..9; radio q48008 positive2..9; q51317 fixed -1','shift':'integer -12..12 including0; zero-shift cancellation families remain c=0','power':'integer2..7, c=0 monomial or nonzero shift family; odd/even checked for nonempty real domain','radicand':'a*x, a signed nonzero -9..9 including1; no added shifts/operators','tangent_point':'rational t=(positive rational inner value-c)/a, independent signed a,c,k; original1 and7/15 retained; shifted curve k integer -9..9'},'authored_completions':'Unrated sqrt q1948 classified hard from observed radical method; unrated affine q48008 classified easy. Missing fields become a single blank RHS, missing blank key completed symbolically, missing solutions authored with same three source chain-rule stages. Source f-prime composite typos are corrected to f(x).','fixed_components':'Logarithm outer function and exactly one inner-function rule; same response shape for complete sources; polynomial number of terms and root radicand structure fixed; tangent targets change with evaluation and answer. No progression within levels.','domain':'log argument strictly positive; sqrt(a*x) implies a*x>0, signed monomial preserved (e.g. -3x^3 gives x<0); b>0,b!=1; denominator roots retained in excluded_holes.','identity':'Mathematical fingerprint uses canonical SymPy function plus real domain and tangent point, independent of seed, source alias, bank and order. Separate question content ID includes complete rendered prompt, worked solution, field contract and unordered complete banks; field-owned answer IDs derive from content identity.'};dump('extraction.json',extraction)
(H/'classification.md').write_text('''# Classification, basis 2275

Sixteen MA practice records: 7 easy, 5 moderate, 2 hard, 2 unrated. There are no non-MA records. All source records are retained unchanged in `source.json`; raw replay includes absent attributes.

The actual lesson follows first-step 17592186093122 → 17592186093123 (natural logarithm KP) → 17592186093124 (this general logarithm KP). Its prerequisite topics are Differentiating Logarithmic Functions and The Chain Rule for Differentiation. The method is decomposition, outer and inner differentiation, chain multiplication/substitution/cancellation; tangent questions add evaluation. It does not require logarithmic differentiation, product/quotient rules or new branches.

The 16 source-specific layouts retain their prompts, response contracts and ordered mathematical stages as replayable parameterized cases. Their four mathematical backbones are affine, polynomial, square root and affine tangent slope. The two unrated originals are classified from their method: q1948 as hard radical and q48008 as easy affine. Six complete observed radio banks remain separate profiles; blank profiles have no distractors. Missing response contracts receive an explicitly authored one-blank completion.

No practice item contains a plot. Canonical e731 contains six raster formula fragments, inspected visually: y=log₂(ln x), requested dy/dx, y, decomposition, differentiation, and chain solution 1/(x ln x ln2). These are standalone math, not plots. Canonical content is context evidence rather than an extra practice count; no new plot is needed.
''')
(H/'template-extraction.md').write_text('''# Template extraction

`extraction.json` records every original parameter set, field, exact source choice, generated counterpart and recipe index. `source-cases.json` is the executable mapping ledger. `source.json` is the immutable full record, including missing metadata and source typos.

Each instance supplies an outer general logarithm and its inner argument. The response is its derivative RHS, or the slope at a supplied tangent point. Stable stages are: express the composite function; display both derivatives (including the radical derivative equality where observed); display formal chain rule; insert the outer and inner derivative factors; substitute the original inner argument; retain observed fraction combination, cancellation and final equal-valued simplification stages; evaluate at the supplied point where applicable. Numerical cancellation is shown even when two successive expressions are equal. The source-specific sequence lengths are tested independently of correctness.

Signed coefficients, bases, affine shifts, polynomial powers and eligible tangent points vary only within those slots. Monomial and shifted-polynomial layouts remain distinct; root radicands remain a*x. Negative root coefficients use the same derivative rule with domain x<0. Zero shifts and unit scales are legitimate parameters. Complete radio profiles are chosen before sampling, and the whole bank is rejected upon collisions. A rejected radio instance remains available as a blank with the same valid mathematics.

q1948 and q48008 omit solutions and correct references. q1949, q48001 and q71479 omit all fields. q341686 has an empty blank. The served versions explicitly author only the missing key, solution or single RHS blank. Raw replay preserves every omission. q310148, q341686, q341688 and q48001 incorrectly label the composite function f′(x)=log(u); served content uses f(x). Captured plain ln/log, Unicode application markers and nested aligned wrappers are presentation defects, normalized to canonical TeX. Canonical e731 incorrectly labels the outer derivative dy/dx rather than dy/du in its differentiation image; raw evidence remains intact.

The source recipe interpretations are intentionally conservative expression patterns, including the exchanged operand in q48008 and base/coefficient-swapped slope fractions in q48656. No new inferred bank is pooled from these patterns. All original banks must map every choice exactly once, preserving counts and correct designations where present.
''')
(H/'plot-extraction.md').write_text('# Plot extraction and generation\n\nRating: **none** for every practice template. Canonical images are six inspected formula rasters, not graphs or diagrams. No plot or diagram generator is required. Original image references remain in immutable source evidence.\n')
review=json.loads((H/'review.json').read_text()) if (H/'review.json').exists() else None
if review:
 sections=[]
 for i,t in enumerate(g.TEMPLATES):
  raw=review['originals'][i]['question'];served=review['served_replays'][i]['question'];vs=[r for r in review['normal_examples'] if r['generation']['template']==t]
  parts=['## '+t+' — '+g.SPECS[t][1], '### Captured original',raw[':question/problem'],raw.get(':question/worked-solution','[No worked solution captured.]'),'### Served original parameters',served[':question/problem'],served[':question/worked-solution']]
  for j,r in enumerate(vs,1):parts.extend(['### Variant '+str(j),r['question'][':question/problem'],r['question'][':question/worked-solution'],'Parameters: `'+json.dumps(r['generation']['parameters'],sort_keys=True)+'`'])
  sections.append('\n\n'.join(parts))
 (H/'review.md').write_text('# Original and two same-method variants per source family\n\n'+'\n\n'.join(sections)+'\n')
(H/'README.md').write_text('''# General logarithm chain-rule generator

Private, unregistered numeric pair. No EDB, registration, engine, shared QA or git mutations. The absent-pair baseline is in `registered-baseline.json`.

Run `.venv/bin/python generate/scratch/17592186092265.py --difficulty all --count 3 --seed 7` for JSON, or add `--format markdown`. Public API: `generate(level, seed=0, template=None, parameters=None, profile="source", field_type=None)`. `source_replay(source_id,"observed_raw")` returns immutable original records; `"observed_served"` returns corrected/completed originals. Supported levels are easy, moderate and hard.

`validate.py` independently reads printed prompts and every operative math stage, replays all original banks, rejects mutation regressions and exercises the frozen native engine in small batches. `review.md` and `review.json` contain every original plus two meaningful variants per source-specific family. Normal instances carry exact parameters, domain, excluded poles, version, source basis, whole-bank profile and task identity. The source cannot calibrate a finer difficulty progression; none is asserted.

`private_readback.py`, `private_scalar.py` and `private_math_format.py` are private frozen dependencies loaded by explicit path. All file SHA-256 hashes are sealed in `frozen-manifest.json` after validation. Any native equivalence gaps are reported in `engine-validation.json` without excluding valid mathematics.
''')
print('Wrote docs3–7 extraction and review artifacts')
for name in ('README.md','review.md'):
 with (H/name).open('a') as f:f.write('\n\nNative-equivalence limitation: the frozen engine accepts canonical keys, but broader valid equivalents can return “answer comparison has unresolved domain differences.” This includes the original unreduced radical chain 7/(2 sqrt(7x) sqrt(7x) ln4) on x>0 and logarithm-power rewrites ln4=2ln2, ln8=3ln2, ln9=2ln3. `equivalent-probe-validation.json` records the mathematical expectation separately from the actual grader result. All valid parameters and outputs remain available.\n')
