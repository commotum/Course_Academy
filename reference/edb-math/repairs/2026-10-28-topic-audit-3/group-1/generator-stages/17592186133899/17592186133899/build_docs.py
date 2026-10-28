#!/usr/bin/env python3
"""Private evidence/review builder; frozen source is never modified."""
import hashlib,importlib.util,json,re
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

GEOMETRY={
 'q-126558':('circle','C2 circular NE; C3 circular SW; both tangent to coordinate axes; radius one quarter outer radius'),
 'q-126654':('circle','C2 circular E; C3 circular W; centers on horizontal axis, radius one quarter outer radius'),
 'q-126862':('circle','C2 square W; C3 square E; centers on horizontal axis, side one half outer radius'),
 'q-126863':('circle','C2 circular NW; C3 circular SE; both tangent to coordinate axes; radius one quarter outer radius'),
 'q-126865':('square','C2 square S; C3 square N; centered on vertical axis, side one quarter outer side'),
 'q-126867':('circle','C2 circular NE; C3 circular SW; larger tangent holes with radius one third outer radius'),
 'q-126870':('circle','C2 square NW, its bottom edge on horizontal axis; C3 square SE, its top edge on horizontal axis'),
 'q-126868':('circle','C2 square SW, its right edge on vertical axis; C3 square NE, its left edge on vertical axis'),
 'q-126864':('square','C2 circular W; C3 circular E; centers on horizontal axis, diameters one quarter outer side'),
 'q-126855':('square','C2 square W; C3 square E; centers on horizontal axis, side one quarter outer side'),
 'q-126861':('circle','C2 square SW, its top edge on horizontal axis; C3 square NE, its bottom edge on horizontal axis'),
}

def value_bank(q):
 f=q[':question/answer-fields'][0];correct=f.get(':answer-field/correct',{}).get(':answer/id')
 return '\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==correct else '') for a in f[':answer-field/choices'])

def main():
 provenance='Database `math`, basis1356, lineage `'+g.WRAPPER['lineage']+'`. Source/topic/lesson wrappers copied without changes. Canonical example e-9557 is contextual evidence, not a practice question.'
 classification=['# Classification','',provenance,'','Four rated easy sources, six rated moderate sources, one unrated source, no observed hard sources. All11 use one radio field named `selection`, five scalar math choices. The unrated q-126558 lacks a correct ref and solution.','', '| Level | Families | Workload | Plot requirement |','|---|---|---|---|','| Easy observed | `positive` | Three signed integer operands; outer CCW, two holes CW | None: unchanged assets |','| Unrated; authored easy completion | `positive_legacy` | Same sum; legacy inline notation | Light: one missing solution orientation diagram |','| Moderate observed | Six named reversal arrangements | Three signed integer operands; one, two or three orientation reversals | None: unchanged assets |','| Hard authored | Same six moderate masks | All three operands noninteger halves/thirds; both denominators required; mixed signs | None: same unchanged assets |','', 'Normal easy and moderate use source shaped prompts and fixed walkthroughs, with authored complete operation banks. Legacy completion borrows the identical all-positive walkthrough and renders its own matching geometry. Hard has a common-denominator bookkeeping demand while retaining the same three boundary terms and orientation decision, adding an explicit common-denominator row. |operand|≤10 and reduced numerator≤29 keep small exact arithmetic. The canonical example and preceding tutorial establish signed circulation summation; prerequisite is Circulation. The sibling Green’s theorem KPs assess curl/area integration and are excluded.','', 'Lesson route is reconstructed from `:activity/first-step` and `:step/next`: Introduction → circulation tutorial → this KP → Extending Green’s Theorem to Regions With Holes → Intuition Behind the Choice of Orentations → Green’s theorem KP → A Note About Double Integrals Over Regions With Holes → advanced holes KP → final illustration. Pull array order is ignored.','', 'The sampler chooses an eligible family and whole bank before choosing operands. Defaults cover all eight source prompt families at their supported levels, and hard covers all six reversal families. Hard is an authored difficulty claim, with no new boundary shape or number of holes.','', 'No source arithmetic error was found in the ten supplied solutions. q-126558’s inferred result is10−4−2=4; raw replay omits its absent attributes. All historical profiles are explicit evidence-only, while defaults complete the missing record and are eligible for learning.']
 (HERE/'classification.md').write_text('\n'.join(classification)+'\n')
 extraction=['# Template extraction','',provenance,'','## 1. Specific source descriptions','', '| Source | Label | Family | Supplied values | Orientation corrections | Solution rows |','|---|---|---|---|---|---|']
 for sid,q in g.QUESTIONS.items():
  fam=g.SOURCE_FAMILY[sid];extraction.append('| '+sid+' | '+q.get(':question/difficulty',{}).get(':db/ident','unrated')+' | '+fam+' | '+', '.join(map(str,g.ANCHORS[sid]))+' | '+str(g.FAMILIES[fam]['signs'])+' | '+('absent' if ':question/worked-solution' not in q else 'symbolic positive sum → signed substitution → collected scalar')+' |')
 extraction+=['','All original supplied numbers are nonzero integers of magnitude≤10. C1 is the outer curve; C2/C3 are distinct holes. The vector field is arbitrary, defined on the shown region; no formula for it is used. Every modern prompt has one display equation block with three supplied circulations, then an orientation sentence and a requested boundary circulation. The legacy prompt uses one inline math expression and malformed parenthesized underscore notation; raw replay preserves it exactly, while normal completion uses canonical braced subscripts and the differential text command.','', '## 2. Shared pattern','', 'Add the circulations along the positively oriented components of the boundary: outer CCW and holes CW. Each supplied circulation is kept or negated according to its stated traversal. The response is one exact scalar. Geometry distinguishes the outer curve and hole labels; shape/size has no role in the arithmetic.','', '## 3. Components and complete bank mappings','', 'The following recipes instantiate every option through the normal public generator. A coefficient triple means c1*a+c2*b+c3*c, with a,b,c the actual displayed circulation operands in order. The matched numeric scalar underdetermines author intent even when a natural sign-mask recipe exists. Correct-ref fidelity is counted separately from inferred mathematics. Opaque scaled values are restricted to common scaling of the complete displayed source operand triple; this is a transparent evidence parameterization, not a recovered mistake model. These profiles are never selected by default.']
 for sid,q in g.QUESTIONS.items():
  f=q[':question/answer-fields'][0];correct=f.get(':answer-field/correct',{}).get(':answer/id')
  extraction+=['','### '+sid,'','Profile `observed:'+sid+'`, radio `selection`, exactly five choices.','', '| Original value | Designation | Parameterized recipe |','|---|---|---|']
  for a,op in zip(f[':answer-field/choices'],g.OBSERVED_RECIPES[sid]):
   recipe=str(op) if isinstance(op[0],int) else {'q-126558':'2π*k, values=k*(10,-4,-2)','q-126865':'−5*k, values=k*(7,-9,1)','q-126855':'12*k, values=k*(4,9,-5)'}[sid]
   extraction.append('| $'+a[':answer/value']+'$ | '+('correct' if a[':answer/id']==correct else ('original key absent' if correct is None else 'incorrect'))+' | '+recipe+' |')
 extraction+=['','## 4. Reusable masks and constraints','', 'Fixed: all shared prose, variable/curve notation, diagram geometry and placement, per-family orientation sentences, reversal notices, radio shape, number of choices, and three ordered worked-solution stages. Variable: complete RHS circulation scalars, the signed substitution operands, and collected scalar. Conditional: parentheses around each negative operand, omission of legacy raw difficulty/key/solution, and authored completion for default legacy output. Original source prefixes/suffixes are operative masks; numeric RHS slots are replaced only after complete circulation equations, never globally across text.','', 'Every family’s symbolic sum keeps its own ordered signs. Default solutions retain the entire corresponding source prose and reversal notice at changed values; they do not introduce helper letters or collapse the sum. Hard keeps the three source stages and adds an explicit common-denominator row with each individually scaled signed numerator before final collection.','', 'Authored banks are selected whole: `method_signs` = correct plus individually reversed C1/C2/C3 contribution signs and complete traversal reversal; `method_omissions` = correct plus each individually omitted component and complete traversal reversal. All five results must be pairwise unequal, and exactly one must equal the positive sum; otherwise the whole parameter instance is rejected. No individual option replacement or distractor diagnoses.','', 'Easy: mixed signed nonzero integers |v|≤10 and all-positive supplied traversals. Moderate: same numeric bounds and six observed reversal arrangements. Hard: all operands reduced noninteger halves/thirds, both denominators represented, mixed signs, |v|≤10 and |numerator|≤29. Public explicit inputs enforce the same guards. Raw profiles are separate evidence and permit bounded rational scaling, preserving original attribute presence.','', 'Presentation identity includes actual prompt, solution, difficulty presence, correct-ref presence and sorted complete bank. Mathematical fingerprints retain the outer operand/orientation and the unordered hole operand/orientation pairs; diagram, profile, aliases and simultaneous C2/C3 relabeling are excluded. Finite eligible counts appear in validation.json.']
 (HERE/'template-extraction.md').write_text('\n'.join(extraction)+'\n')
 plot=['# Plot extraction and reusable specification','',provenance,'','## 1. Individual inspection','', 'All21 original practice rasters were independently viewed at original resolution, composited on white for inspection under `/tmp/33999-source`. Originals remain unchanged and are linked from the frozen record. White inspection makes early transparent C1 labels visible. Axis arrows indicate coordinate axes; problem boundary curves have no traversal arrows.','', '| Source | Outer | Hole shape, placement and labels | Positive-solution boundary colors |','|---|---|---|---|']
 assets=[]
 for sid,q in g.QUESTIONS.items():
  outer,desc=GEOMETRY[sid];sign=g.FAMILIES[g.SOURCE_FAMILY[sid]]['signs'];colors=', '.join('C'+str(i+1)+': '+('pink (reversed)' if s<0 else 'orange (already positive)') for i,s in enumerate(sign))
  plot.append('| '+sid+' | '+outer+' C1 | '+desc+' | '+('missing solution in source; authored all-orange completion' if sid=='q-126558' else colors)+' |')
  for role,key in [('problem',':question/problem'),('solution',':question/worked-solution')]:
   for ref in re.findall(r'!\[\]\(([^)]+)\)',q.get(key,'')):
    p=g.ASSET_ROOT/ref;im=Image.open(p)
    assets.append({'source_id':sid,'role':role,'source_ref':ref,'asset':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dimensions':im.size,'mode':im.mode,'outer':outer,'holes':desc,'boundary_arrows':'none' if role=='problem' else {'C1':'CCW','C2':'CW','C3':'CW'},'solution_colors':colors if role=='solution' else 'all orange','inspected_original_resolution':True,'inspection_composite':'/tmp/33999-source/'+p.name})
 plot+=['','## 2. Shared visual purpose','', 'A light-blue planar region lies inside C1 and outside two white holes C2/C3. The position and curve labels identify the three boundary components. Every supplied circulation is textual; no circulation scalar is embedded in the figure. A positive-orientation solution figure uses outer CCW and both holes CW, regardless of stated question orientations. Pink boundaries show traversals that must reverse relative to the question; orange means already positive.','', '## 3. Components','', 'White/transparent background; black x/y axes with arrowheads and italic labels; orange outer and hole edges in problem; D inside the shaded region; C1 adjacent to the outer top/right edge; C2/C3 adjacent to their individual holes. Solution adds small black directional arrows to each boundary, and selectively recolors reversed curves pink. Region shading and holes remain identical. Source labels and hole placements are retained individually; no generic replacement diagram is used for modern families.','', '## 4. Reusable specification','', 'Circulation values vary while geometry, traversal statements and orientation corrections remain fixed for a selected family/diagram, so all21 source assets are reused unchanged. Parameter values never appear in these rasters. Hard adds no geometry demand and reuses each corresponding solution’s source color cue. Only the missing legacy solution is newly rendered in Matplotlib: circular C1 radius1 centered at origin; circular C2 radius1/4 centered(1/4,1/4); circular C3 radius1/4 centered(−1/4,−1/4). Axes, labels, region shading and tangencies match the inspected original. It adds outer CCW/inner CW arrows and keeps all three edges orange. No SVG creation or image model is used.','', 'Rendered `plots/legacy-positive.png` was viewed at original resolution: C1, C2, C3, D and axis labels are visible; each arrow direction follows positive traversal; hole tangencies and placements match the source. Sidecar records exact recipe and actual Matplotlib version. Writes use unique temporary files and atomic replacement; a cache hit requires PNG and JSON sidecar. No geometry-changing variants are supported, hence no parameter-dependent rendering is needed.']
 (HERE/'plot-extraction.md').write_text('\n'.join(plot)+'\n');(HERE/'plot-spec.json').write_text(json.dumps({'assets':assets,'legacy_completion':json.loads((HERE/'plots/legacy-positive.json').read_text())},indent=2))
 review=['# Source and generated review','',provenance,'', 'Raw originals are shown in full, including absent attributes. Raw variants retain historical evidence profiles and are labeled ineligible for learning. Authored default variants use complete method banks while preserving family walkthroughs. No source arithmetic repair was necessary.']
 records=[]
 for index,(sid,q) in enumerate(g.QUESTIONS.items()):
  family=g.SOURCE_FAMILY[sid];level=g.FAMILIES[family]['level']
  review+=['','## '+sid+' — original','',g.replace_assets(q[':question/problem']),'',value_bank(q),'',g.replace_assets(q.get(':question/worked-solution','[Worked solution absent; original correct designation and difficulty also absent.]'))]
  values=[str(v*sp.Rational(3,2)) for v in g.ANCHORS[sid]]
  raw=g.generate(level,template=family,parameters={'values':values,'diagram':sid},profile='observed:'+sid,seed=42)
  shown=json.loads(json.dumps(raw));shown['question'][':question/problem']=g.replace_assets(shown['question'][':question/problem'])
  if ':question/worked-solution' in shown['question']:shown['question'][':question/worked-solution']=g.replace_assets(shown['question'][':question/worked-solution'])
  review+=['','### Generated evidence variant — 3/2 common scaling; ineligible','',g.markdown(shown)]
  records.append({'label':'evidence scaled '+sid,'kind':'raw observed replay','record':raw})
  for profile in g.METHOD_PROFILES:
   seed=index+55
   # Keep the individually inspected diagram while changing eligible values.
   example=g.generate(level,seed,template=family,profile=profile)
   example=g.generate(level,seed,template=family,profile=profile,parameters={**example['generation']['parameters'],'diagram':sid})
   review+=['','### Generated authored default — '+level+', '+profile,'',g.markdown(example)];records.append({'label':'default '+sid+' '+profile,'kind':'authored normal practice','record':example})
 for family in [f for f,s in g.FAMILIES.items() if s['level']=='moderate']:
  for profile in g.METHOD_PROFILES:
   record=g.generate_hard(seed=71,template=family,profile=profile)
   review+=['','## Generated authored hard — '+family+', '+profile,'',g.markdown(record)];records.append({'label':'hard '+family+' '+profile,'kind':'authored missing-level practice','record':record})
 (HERE/'review.md').write_text('\n'.join(review)+'\n');(HERE/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
 (HERE/'README.md').write_text('''# Circulation over holes generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186133899/validate.py
.venv/bin/python generate/scratch/17592186133899.py --difficulty all --count 2 --format json
.venv/bin/python generate/scratch/17592186133899/build_docs.py
```

Scope: three supplied boundary circulations, outer CCW/inner CW positive orientation, signed summation. All three levels are implemented; hard is an explicitly authored extension using noninteger halves and thirds. Normal defaults serve all supported source families with complete method-derived banks. No curl/area integration, engine changes, registration or EDB writes.

Public raw replay: use `generate(level, template=case["template"], parameters=case["parameters"], profile=case["bank_profile"])` for each entry in source-cases.json. All11 original prompts and55 bank values reproduce exactly. Ten existing solutions and correct keys reproduce; one original solution/key/difficulty are absent and stay absent. Opaque historical responses remain explicit evidence-only scaling profiles. Normal legacy completion has inferred correct value4 and authored solution/easy label.

Validation independently reads the displayed operands, orientation clauses, all symbolic signs, three ordered substitution components, authored hard common-denominator components, collected scalar and every complete bank before actual native radio grading. It also checks full source prose/presence fidelity, difficulty guards, family coverage, identity, mutations and finite semantic variation. Review contains originals, changed raw examples and labeled normal defaults including two examples for every hard family.

The21 original rasters are referenced unchanged; plot-spec.json records their hashes and independent original-resolution inspection. A missing legacy orientation solution figure is completed in Matplotlib. No raster contains circulation numbers, so changed numeric operands require no changed geometry. Stop after step7; parent QA remains required.
''')

if __name__=='__main__':
 import sympy as sp
 main()
