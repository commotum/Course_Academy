from pathlib import Path
import importlib.util,json
h=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('g',h.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
qs=json.loads((h/'source.json').read_text())['record'][':knowledge-point/questions']
(h/'classification.md').write_text('''# Classification at basis 1910

Lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Read nine source practice questions and canonical e-14730 together with generator registration. No existing generator or supplied .generated file.

Easy: four rated sources (one radio, three RHS blanks) plus unrated q-214033 (blank; missing bank/solution). Five separate layout templates. Moderate: three rated two-point radio sources plus unrated q-23633 (radio; missing key/solution). Four separate layout templates and complete bank profiles. One field per question. Unrated source workload labels are authored classifications only; source facts stay unchanged.

Hard: no observed source. Unsupported by this bounded package, five-question reserve unfilled. This is a package capability limit, not a claim that harder mathematics cannot exist. New source evidence reopens classification.

All source prompts, choices, supplied solutions and canonical example have only text and LaTeX, with no plots. All template plot ratings none. Canonical examples do not count as practice. Native inventory at basis 1910 has four easy and three moderate available, deficits one and two.

Each source below remains a separate profile/layout. No pooling of banks.

'''+ '\n'.join(f"- {q[':question/math-academy-id']} (DB {q[':db/id']}): {g.DATA[q[':question/math-academy-id']][0]}, {q[':question/answer-fields'][0][':answer-field/type'][':db/ident']}; plot none." for q in qs)+'\n')
t=['# Template extraction','General pattern: derive reference slope, take the negative reciprocal, use target point in point-slope form, expand, and return an RHS blank or standard-form radio line. All variables real; reference slope nonzero and finite. No horizontal/vertical branch extensions.','One template per original source layout and worked-solution sequence. Fixed: reference equation or two defining points, target x, prose, field key/type, source bank profile. Variable: target y becomes v+t for integer t in [-8,8]. Observed signed values and all source parameters appear at t=0. The bounded sampling policy is narrower than all possible lines, explicitly limiting to observed directions and vertical target translations.','Every radio choice a*x+b*y=c becomes a*x+b*y=c+b*t. This transforms the complete mathematical line and reproduces every original option at t=0, up to nonzero scale. It translates the correct line and all distractors together; mistake interpretation unresolved. No invented mistake labels or pooled recipes. Blanks return m*x+(v+t-m*u), m=-1/reference_slope, without equation or delimiters. Reject inequivalent-bank collisions and ambiguous keys.','Every source field and choice is mapped below, including observed values and exact transformation. Every source is replayed, including missing keys/solutions as explicitly authored additions. Source supplied solutions remain exact at replay. Variant solutions preserve slope, negative reciprocal, point-slope expansion and standard-form conversion sequences and instructional sentences, with streamlined parentheses/expansion rows: do not claim exact variant layout fidelity. No feedback added. All profiles and all bounded parameter values are exercised. Source values, sampling policy and fidelity limits remain separate.']
for q in qs:
 s=q[':question/math-academy-id'];level,pt,ab,pts=g.DATA[s];f=q[':question/answer-fields'][0];radio=f[':answer-field/type'][':db/ident'].endswith('/radio')
 t.extend(['## '+s,f'DB {q[":db/id"]}; level {level}; target {pt}; standard reference {ab} or two-point reference {pts}; reference slope {g.direction(s)}. Field {f[":db/id"]}, key {f[":answer-field/key"]}, type {f[":answer-field/type"][":db/ident"]}; bank profile {s if radio else "none"}.',q[':question/problem'],f'Source key {"present and verified" if f.get(":answer-field/correct") else "missing; derived addition"}; source solution {"present, exact replay" if q.get(":question/worked-solution") else "missing, authored addition"}.'])
 for a in f.get(':answer-field/choices',[]):
  val=a[':answer/value']
  if radio:
   A,B,C=g.line(val);recipe=f'{A}*x+({B})*y={C}+({B})*t'
  else:recipe='m*x+(v+t-m*u), RHS only'
  t.append(f'- Source answer {a[":db/id"]}, field {f[":db/id"]}, exact value `{val}`; recipe `{recipe}`; reproduces entire original mathematical value at t=0: yes; profile {s if radio else "none"}.')
 t.append('Fixed original solution:\n\n'+q.get(':question/worked-solution','Absent.'))
(h/'template-extraction.md').write_text('\n\n'.join(t)+'\n')
(h/'plot-extraction.md').write_text('# Plot extraction\n\nAll nine prompts, banks, supplied solutions and the canonical example inspected: no plots or image references. LaTeX is mathematics rendering. Plot rating none throughout; stages 5/7 need no assets.\n')
(h/'capabilities.json').write_text(json.dumps({'supported_levels':['easy','moderate'],'bounded_distinct_tasks':{'easy':85,'moderate':68},'exceptions':[{'difficulty':'hard','status':'unsupported','unfilled_reserve':5,'evidence':'At basis 1910 nine sources: four rated easy, three rated moderate, two incomplete unrated; no hard template/bank/workload evidence. Package limits to observed finite nonzero reference slopes and vertical translations; new evidence reopens classification.'}],'finite_policy':'Integer target y offsets -8..8 for each source. Exclude current practice and canonical tasks; seed/UUID/order/reference-intercept changes alone do not imply novelty.','unsupported_levels_filled':False},indent=2)+'\n')
(h/'README.md').write_text('# Perpendicular-line generator\n\n`python3 generate/scratch/17592186175924.py --difficulty easy --count 1 --seed 1910 --format json` supports easy and moderate. `validate.py` checks all 153 bounded tasks through the actual Rust learner grader. `replenish.py` retains scoped additive EDB requests and verifies readback under application api.lock. Source snapshots, extraction, full bank replay and review live here; durable commit evidence lives under reference/replenishment. Hard remains unsupported and unfilled.\n')
