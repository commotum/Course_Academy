#!/usr/bin/env python3
"""Write local extraction/review evidence; never touches captured snapshots."""
from pathlib import Path
import importlib.util,json,re
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp33878',ROOT.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TABLE={
 'cubic':'Two-variable cubic plus linear term; integer endpoints; two nonzero final terms and zero initial value.',
 'cycloid':'Two signed polynomial products; familiar sine/cosine at 0 and pi; initial point is the origin.',
 'sqrt_product':'Polynomial product plus two linear terms; square-root upper parameter is a perfect square; initial value is nonzero.',
 'exponential':'Linear y factor times an exponential of a linear x input; initial y is zero; integer upper exponent.',
 'cos_linear':'Cosine product plus linear x term; two nonzero endpoint values at pi/2 and pi; negative difference.',
 'quadratic':'Linear y plus squared x; shifted second curve coordinate; nonzero initial value; evaluated-square sum preserved.',
 'zero_ellipse':'Polynomial/exponential product; ellipse endpoints each have a vanishing polynomial factor; result zero without computing an integral.',
 'trig3':'Three variables; two trigonometric products; upper inputs pi/2 and pi; signed cosine product retained before final simplification.',
 'helix':'Three variables; polynomial product and sine product; full-turn endpoints share x/y but z changes; vanished sine term remains visible.',
 'exp_sum':'Sum of three exponentials; polynomial coordinates with small integer upper inputs; three initial exponentials each equal one.',
 'exp_product':'y times exponential of xz; quadratic coordinates with z=0 at both endpoints; signed y values give a subtraction of a negative.',
 'monomial3':'Three-variable product with powers 1,2,3; polynomial curve powers 2,4,6; all initial factors vanish; simple upper products.',
}

def write():
    rows=[]
    for name,(level,sid,p) in g.TEMPLATES.items():
        rows.append(f'| {level} | `{name}` | {sid or "authored; e-8759 anchor"} | radio / selection / 5 scalar math choices | none |')
    classification='''# Classification

Provenance: immutable `math` snapshot basis 1356, lineage
`01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is the full capture
wrapper copied from `generate/runs/current/sources/17592186133878.json`.
All twelve practice questions are rated: seven easy, five moderate, no hard.
There are twelve observed Markdown/value families and twelve complete source
bank profiles. Each has one `selection` radio field, five delimiter-free scalar
math options, and one correct reference. No observed or generated plots/assets.
The canonical example is context evidence, not a thirteenth practice question.

| Level | Template | Source | Field / bank | Plot rating |
|---|---|---|---|---|
'''+ '\n'.join(rows)+'''

Source answer banks and correct designations are mathematically sound. Two
worked-solution defects are retained in the raw evidence and repaired minimally:
q-99008 says `f(r(pi))` in the theorem-substitution row instead of
`f(r(pi/2))`; its remaining coordinates and arithmetic use pi/2 correctly.
q-104637 opens `f((r(pi/2))` with an extra unmatched parenthesis. Neither repair
changes a bank value or designation. Exact raw solution sequences therefore
have denominator 12 and numerator 10; exact repaired sequences are 12/12.

The lesson route follows `activity/first-step` and `step/next`, never collection
order: 17592186134760 Introduction → 17592186134860 A Concrete Example →
17592186134824 this parametric KP → 17592186134850 Cartesian curves →
17592186134825 potential not given → 17592186134861 proof. The two sibling KPs
establish the boundary: parametrization from a Cartesian equation and recovering
a potential from a field are not part of this generator. Prerequisites are line
integrals over parametric curves (2108) and conservative Cartesian fields (3149).
'''
    (ROOT/'classification.md').write_text(classification)
    parts=['''# Template extraction

## Stage 1: observed instances, before generalization

Every source ID, original prompt, complete bank, original solution and declared
difficulty is retained in `source.json`. The source-case parameters are in
`source-cases.json`. No source is omitted, reassigned, or repaired silently.
''']
    for name,(level,sid,base) in g.TEMPLATES.items():
        if not sid:continue
        q=g.QS[sid];field=q[':question/answer-fields'][0]
        parts.extend([f'### {sid}: {name} ({level})\n',TABLE[name]+'\n',q[':question/problem']+'\n',
           'Original parameters: `'+json.dumps({'scale':1,**base},sort_keys=True)+'`.\n',
           'Correct scalar: $'+field[':answer-field/correct'][':answer/value']+'$.\n'])
    parts.append('''## Stage 2: shared pattern and instructional purpose

The learner receives a scalar potential f and an oriented parameter interval.
Evaluate the supplied curve at the two parameter endpoints, substitute both
coordinate tuples into f, and subtract the initial potential value from the
final one. The response is an exact scalar, never a gradient, an integral setup,
a parametrization, or a reconstructed potential. The full theorem statement,
endpoint table, endpoint-coordinate sentence and final equality chain remain.
Families remain distinct because the potential operators, curve forms,
simplification regimes and arithmetic rows differ. Numeric coefficients within
a family are variants of the same method, not new recovered templates.

## Stage 3: components and complete observed choice banks

Every bank below belongs to the source `selection` field. Its parameterized
component recipe is **lambda times the complete displayed scalar expression**;
the prompt potential is also lambda times the original potential. This is a
homogeneous potential-scaling replay profile. Its interpretation is intentionally
limited: one scalar distractor does not recover the original mistake algorithm.
These are observed component patterns, not claims of inferred author intent.
The curve and interval stay at their original values in `observed_scale`.
Changing them is rejected explicitly. No unrelated polynomial fit or random
perturbation is used. All five expressions travel together as one complete bank.
''')
    for name,(level,sid,base) in g.TEMPLATES.items():
        if not sid:continue
        field=g.QS[sid][':question/answer-fields'][0]
        parts.append(f'### {name} / observed_scale / {sid}\n\n| Source answer UUID | Original scalar | Recipe | Correct? |\n|---|---|---|---|\n')
        for i,a in enumerate(field[':answer-field/choices']):
            correct=a[':answer/id']==field[':answer-field/correct'][':answer/id']
            parts.append('| `'+a[':answer/id']+'` | $'+a[':answer/value']+'$ | $\\lambda('+a[':answer/value']+')$ | '+str(correct).lower()+' |')
        parts.append('\nReplay validates 5/5 mathematical option values and the designation.\n')
    parts.append('''## Stage 4: reusable Markdown/value recipes

The observed prompt has a slot for the **entire potential expression**; all
other observed prompt components are retained. The solution is split into its
original endpoint table and final equality-row components. The theorem row and
endpoint f-call row stay unscaled because f already names the scaled potential;
each numerical substitution/simplification row scales by lambda. This same
recipe runs at lambda=1, -2 and 3; there is no literal source-question return
branch and no answer lookup. Choice values are calculated from symbolic bank
expressions, with equivalent standard SymPy TeX normalization.

Normal generation uses authored complete operation banks. Its source families
vary the named curve parameters below while preserving familiar trigonometric
inputs, perfect-square root inputs, zero-product regimes and small integer
exponential arguments. Normal solution rows retain the family sequence: theorem
substitution → tuple substitution → expanded potential arithmetic → family
arithmetic simplification → final scalar. Zero ellipse has no redundant penultimate
zero row, as in its source. Cubic/quadratic retain their evaluated-power sums;
trig3 retains the cosine value -1 in its product; helix retains its zero sine
term; exp_sum collects equal exponentials and evaluates initial exponentials;
exp_product retains subtraction-of-negative simplification. All source sentence
blocks are reused, without distractor-specific feedback.

| Family | Authored parameter bounds (integers) |
|---|---|
''')
    for name,bounds in g.BOUNDS.items():parts.append('| '+name+' | '+', '.join(f'{k}={lo}..{hi}' for k,(lo,hi) in bounds.items())+' |')
    parts.append('''
All observed families additionally have nonzero integer scale in -4..4 for
explicit requests; normal random scale is ±1, ±2 or ±3. Hard random scale is
one; explicit hard scaling must still keep both **displayed** potential
coefficients in magnitude 1..3, including the product of scale with A/B.
Scale is a potential coefficient, not a cosmetic answer change: it appears in
the displayed potential and every numerical substitution. Signed magnitude
bounds are enforced on explicit parameters. Parameters with invalid complete
banks fail; random generation rejects the entire bank and resamples. It never
replaces a single invalid option from a pool. Some admissible mathematical
parameter tuples have colliding operation banks and are therefore ineligible.

The authored banks are separate from observed replay. Operations include reverse
orientation, use the initial point twice, omit a potential term/power, add
endpoint values instead of subtracting, change a power or exponential input, and confuse
parameter values with endpoint coordinates for the vanishing-product family.
`generation.distractor_recipes` records the exact resulting symbolic scalar and
the operation for every owned answer. These diagnoses are author metadata only.

### Authored hard scope and equal-level workload

The canonical example e-8759 supplies a two-term potential xy²+2xz on
<e^t,t,e^-t>. The hard authored families keep that supplied-potential theorem
method and its reciprocal exponential coordinates, with r=<e^t,t+h,e^-t>,
h=1..3 and interval [0,end], end=1 or 2. Potentials are Axy²+Byz and
Axy²+Bxyz, with 1≤|A|,|B|≤3. Both require the same two 3D endpoint
substitutions, **four nonzero additive contributions before cancellation**,
simple exponential/product simplification, and one signed endpoint difference.
The nonzero h and coefficients prevent a defining contribution from disappearing.
Both families are equal-level variants, not a progression. Each term is checked
independently at each endpoint in validation. These are authored difficulty
claims anchored to the canonical example, lesson route and prerequisites;
there are no observed hard source labels to replay. No direct integration,
potential reconstruction, implicit-curve parametrization, unfamiliar trig
evaluation or arbitrary large algebra is introduced to manufacture hard work.

### Domain and provenance limitations

All potentials are globally smooth on real coordinates. The square-root family
uses t≥0 and a perfect-square upper endpoint. Its geometric path admits the
smooth reparametrization u=sqrt(t), so the endpoint theorem remains applicable
even though the supplied square-root parameter derivative is unbounded at 0.
Observed distractor intentions remain underdetermined; only their mathematical
homogeneous component recipes are claimed. Source numeric/choice and full
solution-sequence fidelity are separate from independent displayed mathematics
and native ID grading. No plots occur, so steps 5 and 7 have no renderer.
''')
    (ROOT/'template-extraction.md').write_text('\n'.join(parts)+'\n')
    (ROOT/'plot-spec.md').write_text('# Plot extraction and generator\n\nAll original prompts, choices and solutions were inspected. They contain textual mathematics only, no image/plot references. Rating: none for every observed and authored family. No assets, renderer or new plots are required by steps 5 and 7.\n')
    review=json.loads((ROOT/'review.json').read_text())
    output=['# Originals and generated variants\n\nOriginal evidence is reproduced verbatim below, including the two documented solution defects. Generated records use minimal repaired notation. Native grading and independent displayed mathematics are reported separately in validation.json.']
    for name,(level,sid,base) in g.TEMPLATES.items():
        output.append('## '+name+' ('+level+')')
        if sid:
            q=g.QS[sid];field=q[':question/answer-fields'][0]
            output.extend(['### Original '+sid,q[':question/problem'],
              '\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==field[':answer-field/correct'][':answer/id'] else '') for a in field[':answer-field/choices']),
              q[':question/worked-solution']])
        else:output.append('Authored missing-hard template; method reference e-8759. There is no observed hard original.')
        for i,r in enumerate([r for r in review if r['generation']['template']==name]):
            meta=r['generation'];label='Observed-bank homogeneous variant' if meta['bank_profile']=='observed_scale' else 'Authored generated variant'
            output.extend(['### '+label+' '+str(i+1),'Parameters: `'+json.dumps(meta['parameters'],sort_keys=True)+'`; profile `'+meta['bank_profile']+'`.',g.markdown(r)])
    (ROOT/'review.md').write_text('\n\n'.join(output)+'\n')
    (ROOT/'README.md').write_text('''# Local generator evidence

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186133878/validate.py
.venv/bin/python generate/scratch/17592186133878/write_evidence.py
.venv/bin/python generate/scratch/17592186133878.py --difficulty all --seed 9 --count 2 --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), with generate_easy/generate_moderate/generate_hard wrappers.
`observed_scale` is the explicitly limited complete source bank replay profile;
`authored_endpoint_bank` is the normal default. Explicit parameters fail on
unknown keys, wrong levels, bounds, zero defining coefficients or bank collisions.
Source cases reproduce all twelve originals with symbolic mathematics and their
complete banks. Full prompt/solution prose and stage order are checked after
whitespace normalization, with two documented solution repairs. Review covers
each observed family/profile plus two examples for each of fourteen templates.
Question identity includes actual prompt, solution, complete displayed bank and
mathematical parameters; option shuffling/seed does not create a new identity.
Distinct task counts omit bank/profile/seed. Actual displayed TeX is parsed for
all endpoint, substituted-arithmetic, intermediate and final values; native
memory-only grading accepts the designated option and rejects all four others.

Source.json retains math basis 1356 and lineage unchanged. Hard difficulty and
normal operation banks are explicitly authored. Only steps 3–7 are implemented;
there are no database transactions, registration, shared edits or plots.
''')
if __name__=='__main__':write()
