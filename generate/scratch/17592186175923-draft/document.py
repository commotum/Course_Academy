"""Produce private extraction artifacts; no registered/DB/shared writes."""
import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('perp_points_docs',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v):(H/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
classification='''# Classification — basis 2275

`latest_inventory.has_generator=true`; the manifest's working queue status is not registration. The registered numeric script and its entire 94-path / 86-file tree, including existing bytecode caches, are immutable. `registered-baseline.json` was captured before any source/generator import and is checked by path plus SHA256. Private imports set `sys.dont_write_bytecode=True` and load frozen formatter/parser by exact file path. No shared manifest, engine, database, registration or git writes.

Actual lesson linked order: Introduction → Finding the Equation of a Perpendicular Line (17592186175922) → this KP (17592186175923) → Finding the Equation of a Line Perpendicular to a Line in Standard Form (17592186175924). The introduction teaches negative reciprocals. This KP's direct key prerequisite is Calculating Slopes of Straight Lines (topic 396 / 17592186049061). Topic 3562 is Finding Equations of Perpendicular Lines; its preceding topic is Perpendicular Lines in the Coordinate Plane. Later related topics (Thales, differentiation, tangent lines, perpendicular bisectors, distances) are outside scope. Source, topic and actual lesson-step evidence are frozen in source.json, topic.json and lesson.json.

12 MA practice sources: five observed easy, five observed moderate, two unrated/incomplete. One existing nonMA easy inventory question is separately preserved using a `questions` array of standard `record` wrappers in nonma-inventory.json; it is not MA evidence. Canonical e-14363 informs scope and does not inflate practice counts. Source bank counts: six radio profiles (5 choices each), five present blank values, one missing blank value. Nine explicit-point complete sources reproduce normalized prompt/shared prose/ordered stages exactly at original parameters. Two incomplete sources have separate authored completions. q-167797 lacks its reference diagram and coordinates; its raw prompt/solution/bank remain exact evidence but ineligible. Its authored text repair explicitly supplies (0,0),(1,-3), chosen to realize the only evidenced reference slope -3, and adds the slope-formula computation needed by the two-point skill. Those points are not claimed to have been recovered from the missing graph.

Within each difficulty, source families remain peers, with a fixed workload per family and no ordering/progression. Easy explicit-point families use a y-axis target. The missing-graph repair retains the observed translated target role as its separately labeled easy family. Moderate uses a nonzero target x-coordinate. Hard has no observed evidence: authored counterparts of the moderate families preserve the same exact point/slope/point-slope method and workload; a new skill is not invented to justify the label. All E/M/H are normally generated. Finite nonzero reference slopes are the observed branch; horizontal/vertical sources would need a different worked-solution branch and are not silently added. The full-equation comparator supports axis lines regardless.

There are five easy and five moderate structural families (the two unrated repairs included at inferred levels), plus five authored hard counterparts. q-237224/q-237225 share one easy blank template; q-72567/q-72568 share one moderate radio template with two complete bank profiles. Public source aliases remain separate for exact replay and source-specific prose, not counted as extra structural templates. All families are text only after the explicit missing-graph repair.

| Source alias | Family | Level | Field | Bank | Plot |
|---|---|---|---|---|---|
'''
for s,q in g.SOURCES.items():
    f=q[':question/answer-fields'][0];classification+='|'+s+'|'+g.FAMILY[s]+'|'+g.source_level(s)+(' (inferred)' if s in g.INCOMPLETE else '')+'|'+g.field_type(s).split('/')[-1]+'|'+str(len(f.get(':answer-field/choices',[])))+'|'+('missing graph; text repair none' if s==g.GRAPH else 'none')+'|\n'
(H/'classification.md').write_text(classification)
extraction='''# Template extraction

Backbone: three supplied points with fixed roles (target P and reference endpoints A,B); compute m1=(By-Ay)/(Bx-Ax), take the negative reciprocal m=-1/m1, use P in point-slope form, expand and isolate y. Blank response is precisely the right-hand side after supplied y=; radio responses are entire line equations. Shared instructional prose is copied from each original family and all concrete point references are updated together. Source arithmetic/sign/evaluation stages are preserved even when successive equations are algebraically equal. Layout and mathematics are checked separately; normalized source displays remain exact at all recoverable originals.

Slots and constraints: A=(a,b) independently sampled in [-6,6]^2; nonzero dx,dy independently in [-8,8], B=A+(dx,dy). Both endpoint roles vary, reference orientation varies, and endpoints remain distinct. P_y independently [-8,8]. P_x=0 for explicit easy intercept families; P_x is a nonzero integer in [-8,8] for translated moderate/hard and the separately labeled missing-graph repair. Every occurrence in prompt, negative-reciprocal display, point-slope stages, key and whole bank derives from those slots. Explicit replay parameters permit integer coordinates of absolute magnitude at most 100. Original parameters are retained even when outside normal random samples. Real plane, no branch/domain restrictions beyond finite nonzero reference slopes. Intercepts 0 and 1 are eligible and tested. Moving only reference endpoints along a common orientation is not mathematical novelty; canonical task identity collapses that alias.

Whole-profile mapping: choose a source alias/profile before sampling. For every observed option y=t0*x+b0, with original perpendicular slope m0 and original target (h0,k0), define multiplier=t0/m0 and residual=b0-k0+t0*h0. At new slope m and target (h,k), t=multiplier*m and b=k-t*h+residual. Emit the full line y=t*x+b. Correct option has multiplier=1,residual=0. This exact equation transport retains every source choice, including compound wrongs and slopes whose psychological explanation is unknown. It is an authored conservative pattern extension, not a claim about learner misconceptions. The complete original banks and exact coefficients appear in choice-ledger.json below. No pooled distractors, first-valid recipes or mixed profiles. Reject the entire sampled instance if any required choices collide or extra answers become correct. Blanks have no distractor profile.

At original parameters, every present observed bank is mathematically matched one-to-one as complete lines up to nonzero scalar; captured correct refs are preserved. q-214038's missing RHS is authored as (5/2)x-20. q-22642's authored correct full equation is y=-(5/6)x+5; its entire captured bank is retained. Their missing solutions are authored using the canonical two-point/negative-reciprocal/point-slope sequence and are never described as captured text. q-167797's captured target (3,-5), correct RHS (1/3)x-6 and solution reference slope -3 support its separate authored textual repair, but not recovery of the original graph. All raw omissions remain omissions in ineligible raw-source-replay.json.

Per-source original descriptions and component mappings follow. A source alias is a runnable exact-replay template argument; grouped family names in classification describe the shared structure. `sourcecases.json` has standard source_id,difficulty,template,parameters,bank_profile keys and original+two changed variants for every alias, plus three examples of each hard alias. `review.md` shows each captured original followed by its normal original/repair and two changed variants.

'''
ledger=[]
for s,q in g.SOURCES.items():
    p=g.original(s);r,m,b=g.values(p);f=q[':question/answer-fields'][0]
    extraction+='## '+s+'\n\n'+q[':question/problem']+'\n\n'
    extraction+='Family: `'+g.FAMILY[s]+'`. Parameters: `'+json.dumps(p)+'`. Source reference slope '+str(r)+', perpendicular slope '+str(m)+', intercept '+str(b)+'. Field key/type: `'+f[':answer-field/key']+'` / `'+g.field_type(s)+'`.\n\n'
    entry={'source_id':s,'family':g.FAMILY[s],'difficulty':g.source_level(s),'parameters':p,'bank_profile':s if g.field_type(s).endswith('/radio') else None,'choices':[]}
    if g.field_type(s).endswith('/radio'):
        extraction+='| Full captured value | Slope multiplier | Incidence residual | Captured correct |\n|---|---|---|---|\n'
        h,k=p['P']
        for a in f.get(':answer-field/choices',[]):
            aa,bb,cc=g.line(a[':answer/value']);slope=-aa/bb;constant=-cc/bb;mult=slope/m;residual=constant-k+slope*h;correct=a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')
            entry['choices'].append({'answer_id':a[':answer/id'],'full_original_value':a[':answer/value'],'source_field':f[':answer-field/key'],'slope_multiplier':str(mult),'incidence_residual':str(residual),'recipe':'y=(multiplier*m)*x+k-(multiplier*m)*h+residual','captured_correct':correct,'interpretation':'exact observed pattern; misconception meaning unresolved'})
            extraction+='|`'+a[':answer/value']+'`|'+str(mult)+'|'+str(residual)+'|'+str(correct)+'|\n'
    else:
        extraction+='Captured RHS: '+('`'+f[':answer-field/choices'][0][':answer/value']+'`' if f.get(':answer-field/choices') else '**missing**; authored completion separate')+'.\n'
        entry['choices']=[{'answer_id':a[':answer/id'],'full_original_value':a[':answer/value'],'source_field':f[':answer-field/key'],'recipe':'m*x+(k-m*h)','captured_correct':True} for a in f.get(':answer-field/choices',[])]
    extraction+='\nCaptured ordered solution (absence stays absent):\n\n'+q.get(':question/worked-solution','**Missing. Authored completion is separate.**')+'\n\n'
    ledger.append(entry)
(H/'template-extraction.md').write_text(extraction);save('choice-ledger.json',{'basis':2275,'profiles':ledger})
(H/'plot-extraction.md').write_text('''# Plot extraction and generator — docs 5 and 7

q-167797 refers to AB via an absent graph. The snapshot contains whitespace where the figure would be, no image reference, coordinates or recoverable asset. Its solution states only slope -3; the original topology/axes/labels/scale cannot be verified. Raw evidence is retained ineligible rather than inventing recovered graph details. The separately authored repair supplies two explicit text reference points realizing slope -3 and uses no plot.

All other practice prompts, choices and worked solutions are algebraic text; plot rating none. Lesson introduction's perpendicular-line picture is context and is not a question plot. All generated families have rating none; no programmatic plots or assets are required.
''')
(H/'template-generator.md').write_text('''# Implementation and verification — doc 6

Entry point: ../17592186175923-draft.py. Public generate(level,seed,template,parameters,bank_profile), per-level helpers, batch, JSON and Markdown CLI previews. Templates accept source aliases. The selected complete bank profile is fixed before parameter sampling. SymPy exact arithmetic; seeded randomness; no writes on import. Frozen official math formatter and independent scalar parser are loaded by exact private paths; generate is decorated with checked_math_content. Every normal source-family variation retains all source arithmetic, negative-reciprocal and point-slope stages. Hard is explicitly authored at the same moderate-family workload because no observed hard source exists.

Content IDs hash normalized complete prompt, ordered solution, field key/type, full unordered rendered bank, and rendered correct value. Answer IDs belong to their field. Distinct full banks or solutions cannot collide under a prompt-only identity. Canonical task identity separately contains reference orientation, actual target point, perpendicular role, response shape and real plane; excludes seed, source endpoint translation/order/separation, scalar line aliases and bank ordering. Batches deduplicate canonical tasks, not just ID strings.

validate.py independently reads the printed target and BOTH reference points, reconstructs the reference direction, proves endpoint incidence and negative-reciprocal direction, compares all entire answer equations up to nonzero scale, checks every numerical slope stage and every point-slope/final stage, and verifies exact source-specific stage counts. It independently requires the actual reference endpoints in the numerical slope substitution and all actual point roles in solution prose. Five displayed-content mutations (wrong reference endpoint, wrong reciprocal sign, stale target, stale coefficient, erased algebraically equal stage) all fail. Changed target with reference data held fixed is checked separately. Vertical/horizontal line equivalence itself is tested, independent of the observed non-axis generation branch. Zero/one intercepts remain eligible. Exact original replay is compared separately from mathematical correctness.

450 distinct sampled questions (150 E/M/H each), 54 original/variant cases, all source profiles and full observed banks are checked. Slot coverage is reported explicitly in validation.json, including target/reference coordinates, dx/dy, slopes and selected profiles. The finite sample is representative, not an assertion of exhaustive Cartesian-product coverage. Normal hard samples cover each moderate source profile, no added skill or within-level progression.

Native check-engine SHA256 71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea is invoked in batches of at most 8 records; each report is retained in native/. All owned radio IDs (correct and all wrongs), canonical/expanded/single-fraction/point-slope blank RHS equivalents, ordinary wrong intercepts/signs, and separate foreign/malformed entries are exercised. Radio fields take an owned selection ID, so arbitrary equation text is not their learner response shape. Whole equation equivalence for their values is independently validated. A full equation supplied to an explicit y= blank is an unsupported response shape, not a genuine RHS-equivalence grading gap. Native counts are 153 accepted, 206 rejected and 198 explicitly unresolved, zero database writes. Valid normal mathematical answers are never pruned to accommodate the grader.

Run `.venv/bin/python generate/scratch/17592186175923-draft/validate.py`; exact unchanged batch reports may be reused after engine SHA and exact input comparison. CLI: `.venv/bin/python generate/scratch/17592186175923-draft.py --difficulty hard --count 3 --seed 2275 --format markdown`.
''')
(H/'README.md').write_text('''Private reviewed generator pair for KP17592186175923 at basis 2275. E/M/H implemented; hard is authored at moderate-family workload, with no observed hard evidence. Registered numeric script and full evidence/cache tree untouched (94 paths, 86 hashed files). No shared/DB/registration/engine/git writes.

See classification.md, template-extraction.md, choice-ledger.json, plot-extraction.md, template-generator.md, source-replay.json, sourcecases.json, review.md, validation.json and native-grading.json. Raw MA source attributes are exact and ineligible; nonMA inventory is separate. Two source records lacked keys/solutions; q-167797 lacks its graph. All three have explicitly authored normal completions/repairs, with evidence limitations stated rather than hidden.
''')
print('Documented 12 MA aliases, 10 structural families, 6 complete radio profiles.')
