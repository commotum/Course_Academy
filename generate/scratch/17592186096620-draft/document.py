"""Write private extraction evidence; never touches registered files."""
import hashlib,importlib.util,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('qd',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v):(H/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
save('independent-inventory.json',{'database':g.RAW['database'],'basis':g.RAW['basis'],'lineage':g.RAW['lineage'],'questions':[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Independent current inventory, not original MA evidence.'} for q in g.KP[':knowledge-point/questions'] if ':question/math-academy-id' not in q]})
rows=[];components=[]
for t,q in g.SOURCES.items():
 p=g.TEMPLATES[t]['p'];u,v=g.parts(t,p);du,dv=g.s.diff(u,g.X),g.s.diff(v,g.X)
 choice=[]
 profile='observed-'+t[2:] if g.TEMPLATES[t]['field']=='radio' else 'fragment'
 values,answer=g.bank(t,p,profile,u,v,g.TEMPLATES[t]['field'])
 recipes={'observed-11955':['-c*a/(-b)/v^2','-c/v^2','-c*a/v^2','-c/2/v^2','-a/v^2'],'observed-11966':['(-c*a*x+c*b)/v^2','(-2*c*a*x+c*b)/v^2','c*b/v^2','(c*b+c*a*x)/v^2','-c*b/v^2'],'fragment':['(uprime*v-u*vprime)/v^2']}[profile]
 for f in q.get(':question/answer-fields',[]):
  for i,a in enumerate(f[':answer-field/choices']):
   matches=[j for j,z in enumerate(values) if g.s.cancel(g.frozen('math_parser').parse(a[':answer/value'])-z)==0]
   assert len(matches)==1
   choice.append({'source_field':f[':answer-field/id'],'source_answer':a[':answer/id'],'exact_value':a[':answer/value'],'profile':profile,'expression_transport':recipes[matches[0]],'mathematically_correct':g.s.cancel(values[matches[0]]-answer)==0,'captured_correct_designation_present':':answer-field/correct' in f,'intent':'unresolved opaque historical expression transport' if len(values)>1 else 'exact derivative fragment'})
 components.append({'source_id':t,'source_record':q,'template':g.TEMPLATES[t],'numerator':str(u),'denominator':str(v),'numerator_derivative':str(du),'denominator_derivative':str(dv),'profile':profile,'choice_mapping':choice})
 rows.append('## '+t+'\n\n1. **Specific observation.** '+q[':question/problem']+'\n\nThe supplied polynomials are `'+str(u)+'` and `'+str(v)+'`; their ordered derivatives are `'+str(du)+'`, `'+str(dv)+'`. Source rating: '+str(q.get(':question/difficulty','absent'))+'. Field contract: '+g.TEMPLATES[t]['field']+' (captured presence: '+str(':question/answer-fields' in q)+'). Plot rating none.\n\n2. **Shared pattern.** Identify numerator/denominator, differentiate each using power/sum rules, substitute in the ordered quotient rule, preserve the family’s expansion/factor/cancellation stages, and supply the complete derivative expression.\n\n3. **Components.** Parameters `'+json.dumps(p)+'`; bank `'+profile+'`. Full prompt, worked prose, fields, exact choices, keys and every mapped expression are in source-components.json.\n\n'+ '\n'.join('- `'+a['exact_value']+'` → `'+a['expression_transport']+'`; '+a['intent']+'.' for a in choice)+'\n\n4. **Reusable backbone and slots.** Each declared nonzero integer coefficient is a complete polynomial-term coefficient slot. Numerator/denominator roles and degree patterns remain fixed; source q-104309 retains even a,d,c so its denominator-factor cancellation remains a real stage. Variable slots change all polynomial definitions, ordered derivatives, substituted factors, expansion terms, final fragments and all options together. Bounds ±12 include every anchor; complete-bank collisions reject the whole instance. Symbolic k remains a constant in q-128235. No independent-variable or function-name aliases inflate task counts.\n')
save('source-components.json',components)
(H/'template-extraction.md').write_text('# Four-stage source extraction\n\nMath basis2275, lineage '+g.RAW['lineage']+'. Exact immutable wrapper is source.json. Templates differ by polynomial form, response layout and operative chain; source positions of supplied numerator/denominator remain mathematical roles.\n\n'+'\n\n'.join(rows)+'''\n\n## Worked-chain contract

All source shared sentences identify u/v, state their derivatives, and introduce the quotient rule. The first formula keeps u′v−uv′ over v². The next formula displays all four ordered operands, including zero derivatives. q-11955/q-104305 then collect immediately (3 quotient rows). q-128235 separately expands the two products inside subtraction groups (4). q-128335 removes the zero term and retains a factored final numerator (4). q-104309 distributes four terms, collects while showing the denominator factor4, then cancels it (5). q-340290 cancels a power after collecting (4). q-340287 moves the minus sign outside (4). The remaining four-row chains show the individually distributed signed terms before collection. q-11966 has no captured worked solution; its four-row completion is authored from q-340297 and the canonical example. Normal formatting normalizes TeX and whitespace; raw evidence retains exact complete prose and omissions.

## Missing-level scope

The ordered activity route is 17592186097430 introduction → 97431 this KP → 97432 other-function quotients → 97433 Leibniz introduction → 97434 Leibniz KP → 97435 tangent justification. That order follows first-step/next, not collection position. This KP precedes the other-function and Leibniz branches; neither is introduced here. Prerequisite topic278 supplies sum/constant-multiple differentiation and the preceding topic1109 supplies product differentiation. Canonical e-3637 already differentiates a linear numerator over a two-term quadratic and simplifies several products.

Authored moderate uses an affine numerator over ax²+d with all four coefficients nonzero, |coefficient|≤4. It requires four nonzero polynomial products followed by collection. Authored hard uses cx²+ex over ax²+d, all coefficients nonzero and |coefficient|≤3: six nonzero products before collection. Degrees remain at most2, exactly the familiar power rule; no nested quotient, chain rule, root, trig, other variable or added task. Each band has one constant workload, no within-band progression. Source easy ratings remain observed facts even when an original has comparable collection demands; missing-band labels are conservative design claims rather than recovered MA labels. Normal easy serves all eleven supported source-shaped families.

## Banks and evidence limits

The q-11955 and q-11966 radio banks contain opaque scalar/expression patterns. Their entire five-member banks are transported within the declared bounded domain; the formulas reproduce every original value. Their misconception interpretation is unresolved. Public observed profiles are evidence_only=true, eligible_for_learning=false. Source keys are reproduced only where captured; q-11966’s correct value5/(2x−1)² is independently derived and its normal key is authored.

Normal radio defaults use separately authored complete method banks. Constant numerators: correct, reverse subtraction, omit denominator derivative, fail to square denominator, quotient of derivatives0. Nonconstant numerators: correct, reverse subtraction, add quotient-rule products, fail to square denominator, quotient of derivatives. These are operation-derived, selected as a complete family before parameters; collisions reject the whole bank. The zero distractor is preserved when valid. There is no first-valid distractor pool.

Raw profile is immutable evidence (including fieldless q-104305/q-104309, unrated/keyless/solutionless q-11966). It is deliberately restricted to original parameters and is ineligible; genuine parameterized observed profiles and source-shaped normal completions are separate. q-128235 and q-128335 lost their supplied function in captured prompt; normal completion restores it from the exact captured u/v worked definitions. q-104305/q-104309 normal completions use the supported blank contract; source fields remain absent in raw evidence.

Mathematical-task identity uses the actual supplied rational function and its square-free monic denominator zero-set, plus the requested derivative role. It excludes seed, field notation, choice profile/order, and scalar rescaling that defines the same function/domain. Content IDs include the actual prompt, fixed solution, level, field type and complete bank; unused profile aliases cannot change them. No plot is needed.
''')
(H/'classification.md').write_text('''# Classification

Immutable math basis2275; original MA practice count11; independently authored inventory count0. Original wrapper/source lineage is retained exactly.

| Observed band | Questions | Responses | Markdown/value families | Plots |
|---|---:|---|---:|---|
| easy | 10 | 1 radio, 7 blank, 2 fieldless |10|none|
| unrated |1|radio, missing correct ref/solution|1|none|
| moderate |0|none captured|0 observed,1 authored|none|
| hard |0|none captured|0 observed,1 authored|none|

Each original maps to its own source-specific operative chain, recorded in source-components.json; numerical overlap does not merge different stages. q-11955 and q-11966 each have a distinct complete five-choice bank. Blanks have one derivative fragment and no distractor profile. Every source is included in source-cases.json and exact raw evidence is available through generate(profile="raw"). These original defects remain explicit: q-11966 unrated/keyless/solutionless; q-104305/q-104309 fieldless; q-128235/q-128335 missing function graphic/definition. Supported normal completions are authored and do not fabricate captured attributes.

Difficulty rationale, lesson/prerequisite boundaries, variable slots and complete-bank policies are in template-extraction.md. All13 family templates are plot-free.
''')
(H/'plot-extraction.md').write_text('# Plot extraction\n\nAll11 original practice records, the canonical example, owning topic and ordered lesson route contain polynomial math text and no plot assets for this KP. q-128235/q-128335 have missing supplied function context; their exact u/v solution definitions recover the function. No graph needs to be guessed or drawn. Rating none; no image model, SVG, Matplotlib or TikZ operation required.\n')
(H/'README.md').write_text('''# Polynomial quotient draft

Private replacement draft at basis2275. Registered numeric script and its entire evidence/cache tree are preserved; registered-baseline.json is a path/SHA256 inventory captured before imports. This draft has no DB, registration, queue or engine mutation.

```sh
.venv/bin/python generate/scratch/17592186096620-draft.py --difficulty all --count 2 --seed 110 --format markdown
.venv/bin/python generate/scratch/17592186096620-draft/validate.py
```

Easy implements all11 source-shaped families. Moderate/hard are explicitly authored missing-band same-quotient-rule extensions. Exact raw omissions and opaque radio banks are evidence only, while normal completions/default banks are separately labeled. Frozen formatter/parser are loaded by explicit file path; no live question_capture import. A private frozen native grader binary tests all owned radio IDs, foreign/malformed/math-text submissions separately, canonical blank fragments, independent unreduced equivalents and ordinary wrong0/1 values.

Review.json/Review.md show every original, source-bank anchor and changed-parameter profile plus two examples each band. Validation.json reports fidelity, mathematics, native grading, omissions and limitations separately. Freeze.json records final bytes and actual runtime versions. No registration is authorized by this work.
''')
print('Private extraction documents written.')
