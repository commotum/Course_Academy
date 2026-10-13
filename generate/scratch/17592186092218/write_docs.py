import json,pathlib
D=pathlib.Path(__file__).parent
R=json.loads((D/'recipes.json').read_text());Q=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((D/'source-cases.json').read_text())
classification='''# Classification at math basis 1356

Database math; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Frozen wrapper retained verbatim in source.json. Twelve practice questions: ten moderate, two unrated. Nine radio fields have five complete coordinate-tuple options each; three questions have two coordinate-component blanks. No plots in any assigned prompt, answer or worked solution; plot rating **none**. The lesson tutorial diagram belongs to context, not this question family; steps 5 and 7 require no assets.

The broad assessed move is one prose-to-polar interpretation followed by two exact products. Fine masks remain distinct wherever original prompt layout, per-coordinate row prefixes, multiplication grouping, wording or answer layouts differ. The legacy pair lack both worked solutions and correct designations; their raw profiles remain public evidence only with omission parity. Normal variants retain their observed prompt masks, use an authored full source-style solution and independently computed correct references, and choose the authored method bank. No missing attribute is synthesized into raw replay.

| Template | Source | Label | Fields | Solution |
|---|---|---|---|---|
'''
for c in cases:
 rec=R[c['template']];classification+=f"| {c['template']} | {c['source_id']} | {'moderate' if rec['difficulty_present'] else 'unrated'} | {', '.join(f['key']+' '+f['type'].split('/')[-1] for f in rec['fields'])} | {'four rows for each coordinate' if 'solution_mask' in rec else 'absent'} |\n"
classification+='''
## Authored level boundaries

Easy (missing observed label): radius exactly 1, familiar nonaxis angle; interpreting the prose and looking up two exact signed trigonometric values. Twelve substantive tasks across the familiar nonaxis angles; degrees/radians and fields are presentation aliases, not extra tasks.

Moderate (observed): nonunit positive rational radius, familiar angle; interpret prose, evaluate cosine/sine, scale both values, simplify exact rational/radical products. Random domain includes integer 2..12, reciprocals 1/2..1/6 and 3/2, 5/2, 7/3. The same finite radius catalog is enforced on explicit calls. Axis source templates retain their observed moderate label and require their original axis orientation. This heterogeneous observed level is reported honestly; the axis variants have simpler trigonometric evaluation than the nonaxis variants.

Hard (missing observed label): positive radius k sqrt(2) at 45-degree reference angles or k sqrt(3) at 30/60-degree reference angles, k=1..6; same prose interpretation, familiar trigonometric lookup and two products, now simplifying a positive radical product. No unfamiliar identity, radius recovery, negative-radius convention, angle inference, diagram or additional point is assessed. These boundaries apply to sampling and explicit calls.

Curriculum anchor: lesson first step 17592186093050 introduces x=r cos(theta), y=r sin(theta); next links give direct tuple conversion (93051), this prose conversion (93052), another-point radius recovery (93053), then diagram angle inference (93133). Order was read from first-step/next, not pull collection order. Topic prerequisites are Introduction to Polar Coordinates and Evaluating Trigonometric Expressions. The canonical example radius 2 at 135 degrees anchors the two signed products. Sibling canonical e-5385 already evaluates positive sqrt(3)-radius products; hard supplies that radius directly and stops at this KP's conversion. All variants within each authored level have the same method, with no staged progression.
'''
(D/'classification.md').write_text(classification)
ex='''# Template extraction

## Stage 1: specific observed questions

All numbers are exact. Radius is a positive integer except q-17124 (1/3); angles are familiar unit-circle values, expressed in degrees, radians, or zero. x/y are Cartesian output coordinates, P the described point, r/theta the interpreted polar quantities. Original punctuation and all worked-solution row prefixes/groupings are preserved by complete-component masks. Decoded-byte inspection shows no adjacent backslashes in answer commands; ord samples contain a single byte 92 before commands. JSON output escaping is not a TeX defect. Source row separators are genuine double-backslash TeX, retained.

'''
for q,c in zip(Q,cases):
 ex+=f"### {c['source_id']} / {c['template']}\n\nOriginal: {q[':question/problem']}\n\nParameters: `{json.dumps(c['parameters'])}`. Field attributes: `{json.dumps(R[c['template']]['fields'])}`.\n\n"
ex+='''## Stage 2: shared mathematical pattern

Read the given distance as r and the given angle from the positive x-axis as theta. Compute x=r cos(theta) and y=r sin(theta), returning a complete coordinate tuple (radio) or its two scalar fragments (paired blanks). The solution states the interpreted polar coordinates, the conversion formulas, then four rows for x and four for y: formal component, substituted trigonometric expression, evaluated trigonometric product, simplified coordinate. It finishes with the complete Cartesian tuple. Source-specific punctuation, repeated x/y row prefixes, multiplication-dot/grouping choices and omitted words remain separate masks.

## Stage 3: component and complete-bank map

R is the radius; X=R cos(theta), Y=R sin(theta). Each expression below computes a complete displayed tuple from those quantities. Scalar-factor patterns in opaque historical banks are evidence component patterns, not recovered learner mistakes. No independent random perturbation or polynomial fitting is used. All nine historical banks remain public raw profiles and evidence only, including the banks also used in eligible normal variants. The four defensible bank shapes (sign/root substitution, sign/half-factor, down-axis, right-axis) are separately identified as source profiles in normal generation; their original-angle constraints and whole-bank collision checks apply. The remaining radio masks receive a separately authored method-sign-scale bank for normal practice.

'''
# Avoid importing generator bytecode; parse literal bank dict from AST.
import ast
s=ast.parse(D.with_suffix('.py').read_text());banks=next(ast.literal_eval(n.value) for n in s.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RAW_BANKS' for t in n.targets))
for q,c in zip(Q,cases):
 ex+=f"### Complete bank raw-{c['source_id']}\n\n"
 for i,f in enumerate(q[':question/answer-fields']):
  for j,a in enumerate(f[':answer-field/choices']):
   recipe=banks[c['source_id']][j] if c['source_id'] in banks else ('X' if i==0 else 'Y')
   correct=f.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id']
   ex+=f"- Field `{f[':answer-field/key']}`, choice `{a[':answer/id']}`: `{a[':answer/value']}` -> `{recipe}`; original designation {'correct' if correct else 'incorrect' if ':answer-field/correct' in f else 'absent'}.\n"
ex+='''
## Stage 4: reusable masks, domains, and repairs

recipes.json records all complete prompt/solution masks, fields and attribute-presence bits. build_extraction.py creates slots only for the complete radius, angle, tuple, substituted component, evaluated product and final coordinate; it never globally replaces short numerals. The historical option rendering retains per-source comma spaces. The normal solution masks use the source trigonometric notation and fixed full sentences, independent of selected mistake.

For nonunit nonaxis defaults, the complete authored method bank is (X,Y), (-X,Y), (X,-Y), (-X,-Y), (cos(theta),sin(theta)): reverse one or both quadrant signs and omit radius scaling. At authored unit-radius easy, omitting the radius would duplicate the correct tuple, so the final distractor interchanges sine/cosine; equal-magnitude angles instead use the explicitly eligible doubled-radius product (2X,2Y). The complete bank is selected by this mathematical condition before construction; no first-valid replacement pool is used. These easy bank shapes are authored method mistakes, not recovered historical recipes.

Source-normal profiles: q-17126 reverses signs or substitutes sqrt(3)/2 for the negative sine at 315 degrees; q-17134 reverses signs and halves the y scaling at 240 degrees; q-17128 interchanges the axes, reverses direction, or omits radius in the positive-axis distractor; q-17137 interchanges axes, replaces zero by one, omits radius, or reverses x. Profiles stay intact; duplicates reject the entire instance.

Unrated q-17133 and q-8522 have mathematically unique correct options (1/2,-sqrt(3)/2) and (5sqrt(3)/2,-5/2), independently derived; raw replay leaves absent refs/difficulty/solution absent and marks evidence_only. They cannot enter native grading fixtures without authored refs, so no native pass is claimed for these original records. An authored evidence level assignment moderate indexes their replay only; it is not a recovered label.

q-17128's second heading says x-coordinate although every y-stage equation and conclusion are correct. Raw replay preserves that original wording; normal output changes only that heading to y-coordinate. This is a prose repair, not a mathematical or TeX repair. Exact raw solution count and normal repaired prose are reported separately. No other source error was found.

Profiles require source angles in raw evidence replay but radius varies exactly; the complete bank components are recomputed. No raw branch returns a captured question or answer lookup payload. Normal sampling includes the legacy degree/radian prompt masks with explicitly authored solutions and inferred correct references, while raw omissions stay intact. It selects every eligible source-shaped family at each level before radius sampling, with opaque historical profiles excluded from learner defaults. All output is local review JSON, never transaction EDN.
'''
(D/'template-extraction.md').write_text(ex)
(D/'plot-extraction.md').write_text('# Plot extraction / steps 5 and 7\n\nNone of the 12 assigned practice records or their choices/worked solutions contains a plot. No parameter-dependent asset is required. The topic tutorial diagram is context only; no renderer or external image model is used.\n')
(D/'README.md').write_text('''# Described radius/angle to Cartesian coordinates

Run `.venv/bin/python generate/scratch/17592186092218/validate.py` for independent printed-math checks, exact source fidelity, level guards, deterministic identity and real native grading. Preview with `.venv/bin/python generate/scratch/17592186092218.py --difficulty all --seed 42 --count 2 --format markdown` (or json).

API: generate / generate_easy / generate_moderate / generate_hard with seed, template, field_type, parameters, profile. Radian angle parameters are rational multiples of pi (e.g. angle="7/4", unit="radians"). Raw profiles require explicit parameters and preserve missing source attributes. source-cases.json enumerates all 12 public replay calls. Normal source profiles and authored method banks are described in extraction.

Source math basis 1356 is frozen unchanged. Easy unit-radius lookup and hard positive radical-radius products are authored missing-level designs. Moderate follows the observed prose interpretation and two exact component products, with original axis masks also covered. No diagrams, unfamiliar trigonometric identities, radius recovery, additional point, database writes or registration. Native grading limitations on the two missing-reference raw sources remain documented rather than passed. Steps 3–7 only.
''')
