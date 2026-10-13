"""Write private extraction evidence from parameterized recipes, not database data."""
import importlib.util,json
from pathlib import Path
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
recipes={
'q-39800':['remaining pole b','residual numerator zero c','original denominator roots {b,a}','cancelled root a','observed pattern {−|c|,+|c|,a}; intent unresolved'],
'q-39801':['cancelled root a','original denominator roots {b,a}','observed sign-reflection shape {a,−b}; intent unresolved','independent opaque evidence slots {opaque[0],opaque[1]}; not a recovered error operation','remaining pole b'],
'q-80690':['original denominator roots {a,b}','cancelled root a','remaining pole b','empty set','observed reflected set {−b,b}; intent unresolved'],
'q-39804':['remaining pole b','independent opaque slot with reflected pole {opaque[0],−b}; intent unresolved','original denominator roots {b,a}','cancelled root a','observed shape {b,−a,a}; intent unresolved'],
'q-39931':['independent opaque singleton opaque[1]','empty set','independent opaque pair {opaque[0],opaque[1]}','independent opaque singleton opaque[2] (the correct 0 at source)','independent opaque singleton opaque[0]'],
'q-80691':['observed reflected cancelled root −a','original denominator roots {0,a}','remaining pole 0','empty set','cancelled root a'],
}
md=['# Four-stage template extraction',
'## 1. Specific source analysis',
'Every source is described below, including its exact prompt, primitive parameters, answer types, full observed choice mapping and ordered mathematical rows. source.json preserves every raw field; review.md preserves full original solution prose. No source question is omitted. The source-case order here has no pedagogical progression.',
'## 2. Shared pattern',
'Factor the numerator and denominator, cancel their greatest common polynomial factor, and identify the entire set of real zeros of the reduced denominator. The original domain excludes all original denominator zeros. A removed zero is a hole only when no denominator factor remains there. Responses are numeric root fragments in blank fields or complete root sets in radio fields. Every supported family has a nontrivial common factor and at least one surviving real pole.',
'## 3. Components and bank profiles',
'Each per-source specialization preserves its exact Markdown mask: complete math blocks are slots, prose and delimiters are fixed. Every source choice is retained in its source field and value type. The six complete observed radio banks have evidence_only=true and eligible_for_learning=false, even where a plausible root operation can describe several members. Independent opaque slots make interpretation limits explicit; they are not fitted distractor formulas and never enter normal sampling. Profiles are chosen whole before parameter sampling; all five required values are computed and any root-set equivalence/collision rejects the entire instance.',
'## 4. Reusable mask and calculations',
'The generator builds ordered unsimplified numerator/denominator components, factored components, explicit cancellation components and reduced components. For grouping, it preserves six rows: original cubic; common-binomial grouping; difference-of-squares grouping; complete linear factors; cancellation; reduced quotient. The cube family preserves five rows, including splitting its cube into one cancelled factor and a remaining square. The easy supplied-factors family preserves three rows. All other families preserve four rows. Only the final reduced expression uses CAS cancellation; structural masks carry the preceding teaching operations.',
'Fixed prose comes from each source solution, including omission of “solve for x” in q-39931 and trailing spaces in q-269990/q-278545. Source solutions absent in the three unrated captures use the canonical factor/cancel/set-denominator/solve wording with all intermediate rows. Source prompt math, denominator equation and every prose root occurrence derive from the same parameters; no substring replacement touches function arguments or arbitrary prose.',
'### Scope and finite sampling policy',
'All independent variables/function names remain actual source x and f. Easy supplied-factors: cancellation and remaining roots are integers |a|≤6, |b|≤8, distinct; the literal x-factor variant fixes a=0. Moderate monic quadratics retain nonzero constant and middle terms; monomial family retains exactly x² as common factor and a nonzero surviving root |b|≤8. Moderate nonmonic common factors m x+n have 2≤m≤4, 1≤|n|≤5, gcd(m,n)=1; remaining integer root has 1≤|b|≤6, differs from −n/m and preserves a nonzero middle coefficient. Thus nonunit coefficients cannot reduce to a monic/integer-root task.',
'Moderate cubic grouping fixes denominator (x²−a²)(x−b), 1≤a≤4, 1≤|b|≤8, b≠±a, and linear numerator x+a. Hard cubic grouping uses the same bounded cubic plus quadratic numerator (x−c)(x+a), 1≤|c|≤6, c distinct from all denominator roots and nonzero numerator middle coefficient. Hard quadratic ratios use three distinct nonzero integer roots |a|,|c|≤6, |b|≤8, with nonzero middle terms in both quadratics. Hard cube retains a nonzero cubic perfect-power root 1≤|a|≤4 and distinct nonzero repeated pole 1≤|b|≤8. Hard difference-of-squares family preserves x² as surviving denominator, with 1≤a≤6. These guards apply identically to explicit calls and random sampling, including primitive/reduced requirements.',
'No difficulty is missing in the capture. Extensions provide deterministic signed/root choices and separate normal complete radio banks; they do not introduce complex roots, discriminants, holes-coordinate calculations, higher degrees or a within-level progression. Narrow zero-pole families have genuinely finite variation (six meaningful square magnitudes for q-39931; sixteen nonzero shifts in the zero-pole linear family). Variable aliases and opaque evidence slots do not inflate mathematical-task counts.',
'### Normal method bank',
'The five root-set operations are: the full reduced denominator zero set; all removed original-domain zeros; all original denominator zeros; the empty set; sign-reversed surviving roots. When the surviving set is {0}, the final member is the sign-reversed removed-root set. Every whole bank must have five distinct sets and exactly one correct set, otherwise the entire instance is rejected. This is an authored default bank, not claimed recovered source intent. Displayed complete sets are independently re-read in validation and native grade checks submit every option. Blank checks submit an independently unevaluated linear or quadratic root formula and a wrong number.',
'### Evidence versus completions',
'Public raw profile keeps q-39800/q-39801/q-80690 without refs and solutions, and q-39802 without fields. Completed observed profile derives the missing correct root sets and adds q-39802 two ascending-order blanks. These changes have distinct denominators: original refs 10/10 matched, inferred refs 3/3 correct; original solutions 10/10 exact, authored missing solutions 3; raw prompts/layouts 13/13 exact, fieldless completion 1. No mathematical source error or proven escape anomaly exists. q-39804 uses balanced but unconventional parenthesis brace placement, exactly retained for replay and normalized in normal output.',
]
for t,(level,family,p) in g.TEMPLATES.items():
 q=g.SOURCES[t];z=g.math_parts(t,p,True)
 md+=['\n## '+t+' — '+family, 'Original label: '+str(q.get(':question/difficulty',{}).get(':db/ident','unrated'))+'. Generator level: '+level+(' (authored assignment)' if ':question/difficulty' not in q else '')+'. Plot rating: none.',q[':question/problem'],'Primitive parameters: `'+json.dumps(p,sort_keys=True)+'`.','Original domain exclusions: '+', '.join(g.tex(v) for v in z['domain'])+'. Remaining pole set: '+', '.join(g.tex(v) for v in z['poles'])+'. Removed zeros/holes: '+', '.join(g.tex(v) for v in z['holes'])+'.']
 if ':question/worked-solution' in q:
  md.append('Observed ordered rational-expression stages:')
  md += [str(i+1)+'. $'+row+'$' for i,row in enumerate(z['rows'])]
 else:md.append('No captured worked solution; the same stages listed in review.md are authored from the canonical method.')
 for f in q.get(':question/answer-fields',[]):
  md+=['Field `'+f[':answer-field/key']+'` — '+f[':answer-field/type'][':db/ident'], '| Original complete value | Value type | Recipe/slot | Original designation |','|---|---|---|---|']
  for i,a in enumerate(f[':answer-field/choices']):
   role=recipes[t][i] if t in recipes else 'ordered remaining numeric root fragment '+f[':answer-field/key']
   designation='correct' if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id') else 'wrong' if ':answer-field/correct' in f else 'absent; not a matched designation'
   md.append('| `'+a[':answer/value']+'` | '+a[':answer/type'][':db/ident']+' | '+role+' | '+designation+' |')
 if not q.get(':question/answer-fields'):md.append('Original field layout is empty. Raw profile preserves it. Authored completion supplies field-1 (minimum pole) and field-2 (maximum pole), with a minimal ascending-order instruction.')
(P/'template-extraction.md').write_text('\n\n'.join(md)+'\n')
