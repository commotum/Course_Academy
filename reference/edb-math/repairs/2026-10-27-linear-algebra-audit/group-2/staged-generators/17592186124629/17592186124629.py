"""Relocatable, source-backed invertible-matrix-theorem sentence generator."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
from generator_policy import nonempty_checkbox
from math_format import normalize_prose, validate_generated_record

HERE = Path(__file__).resolve().with_suffix('')
SOURCE = json.loads((HERE / 'source-current.json').read_text())
KP_ID = 17592186124629
KP_UUID = 'bb90e5b9-03fe-51cf-bc16-a293befacebc'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = '2.0.2-content-identity'
SUPPORTED_LEVELS = ('moderate',)
CASES = {q[':question/math-academy-id']: q for q in SOURCE[':knowledge-point/questions']
         if q.get(':question/difficulty') and q.get(':question/worked-solution')}
EXCLUDED = {'q-47586': 'No difficulty, key or worked solution; true subset absent from bank.'}
# The order is the order of the three implications in each source solution.
SLOTS = {
 'q-47599': ('det', 'col', 'pivot'), 'q-142475': ('inv', 'rank', 'col'),
 'q-142476': ('det', 'col', 'pivot'), 'q-47587': ('inv', 'rank', 'pivot'),
 'q-79334': ('inv', 'rank', 'col'), 'q-139978': ('inv', 'nullity', 'pivot'),
 'q-141215': ('det', 'null', 'rank'), 'q-142479': ('inv', 'basis', 'det'),
 'q-141341': ('inv', 'det', 'rank'), 'q-141342': ('basis', 'inv', 'pivot'),
 'q-141205': ('inv', 'pivot', 'null'), 'q-141217': ('nullity', 'null', 'det'),
 'q-142478': ('null', 'rank', 'null-solution'), 'q-47604': ('rank', 'nullity', 'pivot'),
 'q-141214': ('basis', 'col', 'nullity')}
DIMENSIONS = {'q-47599': '7', 'q-142476': '8', 'q-139978': '5',
              'q-141215': '6', 'q-142478': '3'}
LABELS = ('I', 'II', 'III')
ORIGINAL = r'\text{nullity}(A)=0'
PREMISES = {'nullity-zero': ORIGINAL, 'nonzero-determinant': r'det(A)\ne 0',
 'full-rank': r'\text{rank}(A)=n', 'trivial-null-space': r'\text{Null}(A)=\{0\}',
 'full-column-space': r'\text{Col}(A)={R}^{n}',
 'full-column-dimension': r'\text{dim(Col}(A))=n'}
DEFAULTS = {sid: {'premise': 'replay'} for sid in CASES}

def subset(value):
    import re
    return tuple(bool(re.search(r'\b' + label + r'\b', value)) for label in LABELS)

def mask_name(bits):
    selected = [label for label, b in zip(LABELS, bits) if b]
    return ', '.join(selected[:-1]) + ', and ' + selected[-1] if len(selected) == 3 else ' and '.join(selected) + ' only'

def checkbox(sid):
    return len(CASES[sid][':question/answer-fields']) == 3

def masks(sid):
    if checkbox(sid):
        return [list(b) for b in itertools.product((False, True), repeat=3) if any(b)]
    return [list(subset(a[':answer/value'])) for a in CASES[sid][':question/answer-fields'][0][':answer-field/choices']]

def hypothesis_concepts(sid):
    # Nullity and null-space solution statements are the same concept for copying.
    used = set(SLOTS[sid])
    if 'null-solution' in used: used.add('null')
    return [c for c in ('inv', 'det', 'rank', 'col', 'null', 'nullity') if c not in used]

def domain(sid):
    return [{'premise': 'decision', 'invertible': state, 'hypothesis': hyp, 'truths': bits}
            for bits in masks(sid) for state in (False, True) for hyp in hypothesis_concepts(sid)]

def proposition(concept, positive, n):
    """Positive means full-rank side, except basis (every subspace has one)."""
    return {
      'inv': ('$A$ is invertible', '$A$ is **not** invertible'),
      'det': (r'$\det(A)\ne 0$', r'$\det(A)=0$'),
      'rank': (rf'$\operatorname{{rank}}(A)={n}$', rf'$\operatorname{{rank}}(A)<{n}$'),
      'col': (rf'$\operatorname{{Col}}(A)=\mathbb{{R}}^{{{n}}}$', rf'$\operatorname{{Col}}(A)\subsetneq\mathbb{{R}}^{{{n}}}$'),
      'null': (r'$\operatorname{Null}(A)=\{0\}$', r'$\operatorname{Null}(A)\ne\{0\}$'),
      'nullity': (r'$\operatorname{nullity}(A)=0$', r'$\operatorname{nullity}(A)>0$'),
      'pivot': (f'$A$ has ${n}$ pivot columns', f'$A$ has fewer than ${n}$ pivot columns'),
      'basis': (r'$\operatorname{Null}(A)$ has a basis', r'$\operatorname{Null}(A)$ has no basis'),
      'null-solution': ('$Ax=0$ has only the trivial solution', '$Ax=0$ has a non-trivial solution'),
    }[concept][0 if positive else 1]

def theorem(n):
    return ("The invertible matrix theorem states the following:\n\n"
     r'$$\begin{gathered}A\text{ is invertible}\\\Updownarrow\\\begin{aligned}'
     + rf'\operatorname{{Col}}(A)&=\mathbb{{R}}^{{{n}}}\\'
     + rf'\dim(\operatorname{{Col}}(A))&={n}=\operatorname{{rank}}(A)\\'
     + r'\operatorname{Null}(A)&=\{0\}\\'
     + r'\dim(\operatorname{Null}(A))&=0=\operatorname{nullity}(A)\end{aligned}\end{gathered}$$')

def assemble(sid, prompt, solution, specs, parameters, seed):
    q = {':question/problem': normalize_prose(prompt), ':question/worked-solution': normalize_prose(solution),
         ':question/difficulty': ':question.difficulty/moderate'}
    content = [q[':question/problem'], q[':question/worked-solution'], [(key, kind, sorted(values), correct) for key, kind, values, correct in specs]]
    fp = hashlib.sha256(json.dumps(content, ensure_ascii=False).encode()).hexdigest()
    qid = uuid.uuid5(uuid.UUID(GENERATOR_UUID), fp)
    q[':question/id'] = str(qid)
    fields = []
    for key, kind, values, correct in specs:
        fid = uuid.uuid5(qid, 'field:' + key)
        choices = [{':answer/id': str(uuid.uuid5(fid, v)), ':answer/type': ':answer.type/text', ':answer/value': v} for v in values]
        fields.append({':answer-field/id': str(fid), ':answer-field/key': key, ':answer-field/type': kind,
                       ':answer-field/choices': choices, ':answer-field/correct': [':answer/id', str(uuid.uuid5(fid, correct))]})
    q[':question/answer-fields'] = fields
    return validate_generated_record({'question': q, 'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': SOURCE[':knowledge-point/title']},
      'generation': {'generator_id': GENERATOR_UUID, 'version': VERSION, 'seed': seed,
        'template': sid, 'profile': sid, 'parameters': parameters, 'mathematical_fingerprint': fp,
        'domain': 'real square matrices, positive integer n', 'source_basis': 5418, 'plots': 'none'}})

def replay(sid, seed=0, premise='replay'):
    old = CASES[sid]
    prompt, sol = old[':question/problem'], old[':question/worked-solution']
    if sid == 'q-141342':
        # Correct the three quoted conditionals, not the theorem's zero-nullity equivalence.
        sol = sol.replace(ORIGINAL + ',$ then', r'\text{nullity}(A)\ne 0,$ then')
    if premise not in ('replay', 'source', 'nullity-zero'):
        if ORIGINAL not in prompt: raise ValueError('This source does not have the nullity-zero premise')
        replacement = PREMISES[premise]
        if any(c in ' '.join(f[':answer-field/key'] for f in old[':question/answer-fields']) for c in (replacement,)):
            raise ValueError('Hypothesis would copy a conclusion')
        prompt, sol = prompt.replace(ORIGINAL, replacement), sol.replace(ORIGINAL, replacement)
    # The source's side-by-side equivalence clips in the real UI. Reflow only
    # the recalled theorem; retain all three source implication paragraphs.
    sol = theorem(DIMENSIONS.get(sid, 'n')) + '\n\nWith that in mind' + sol.split('With that in mind', 1)[1]
    specs = [(f[':answer-field/key'], f[':answer-field/type'][':db/ident'],
              [a[':answer/value'] for a in f[':answer-field/choices']], f[':answer-field/correct'][':answer/value'])
              for f in old[':question/answer-fields']]
    return assemble(sid, prompt, sol, specs, {'premise': premise}, seed)

@nonempty_checkbox
def generate(difficulty='moderate', seed=0, template=None, parameters=None):
    if difficulty not in SUPPORTED_LEVELS: raise ValueError('Only moderate is supported')
    rng = random.Random(seed)
    sid = template or rng.choice(sorted(CASES))
    if sid not in CASES: raise ValueError('Unsupported source profile')
    p = parameters if parameters is not None else rng.choice(domain(sid))
    if p.get('premise') != 'decision': return replay(sid, seed, p['premise'])
    if p not in domain(sid): raise ValueError('Outside validated decision domain')
    inv, bits, hyp = p['invertible'], p['truths'], p['hypothesis']
    n = DIMENSIONS.get(sid, 'n')
    premise = proposition(hyp, inv, n)
    # 'A is invertible' is prose rather than embedded mathematics.
    stem = f'If $A$ is a ${n}\\times {n}$ matrix and {premise}, then'
    statements = [proposition(c, b if c == 'basis' else (b == inv), n) for c, b in zip(SLOTS[sid], bits)]
    prompt = ('Consider the following sentence:\n\n*' + stem + r' $\underline{\phantom{xxxxxx}}$.*'
              + '\n\nWhich of the following can be placed into the blank space to make a true statement?')
    if checkbox(sid):
        prompt += '\n\nSelect all that apply.'
        specs = [(s, ':answer-field.type/checkbox', ['false', 'true'], str(b).lower()) for s, b in zip(statements, bits)]
    else:
        prompt += '\n\n' + '\n\n'.join(l + '. ' + s for l, s in zip(LABELS, statements))
        values = [a[':answer/value'] for a in CASES[sid][':question/answer-fields'][0][':answer-field/choices']]
        rng.shuffle(values)
        correct = next(v for v in values if subset(v) == tuple(bits))
        specs = [('selection', ':answer-field.type/radio', values, correct)]
    fact = (rf'$\operatorname{{rank}}(A)={n}$ and $\operatorname{{nullity}}(A)=0$' if inv
            else rf'$\operatorname{{rank}}(A)<{n}$ and $\operatorname{{nullity}}(A)>0$')
    sol = theorem(n) + '\n\nWith that in mind, let\'s examine each of the options separately.'
    for c, s, b in zip(SLOTS[sid], statements, bits):
        if c == 'basis':
            reason = 'Every finite-dimensional subspace has a basis. The zero subspace has the empty basis.'
        else:
            actual = proposition(c, inv, n)
            reason = f'The given condition implies {fact}. Thus {actual}.'
        sol += '\n\n- The following statement is ' + str(b).lower() + ':\n\n*' + stem + ' ' + s + '.* ' + ('✓' if b else '×') + '\n\n' + reason
    answer = '; '.join(s for s, b in zip(statements, bits) if b) if checkbox(sid) else correct
    sol += '\n\nTherefore, the correct answer is ' + answer + '.'
    return assemble(sid, prompt, sol, specs, p, seed)

@nonempty_checkbox
def batch(difficulty='moderate', count=5, seed=0):
    if difficulty not in SUPPORTED_LEVELS: raise ValueError('Only moderate is supported')
    if count < 0: raise ValueError('Count must be nonnegative')
    rng = random.Random(seed)
    # Sample decision roles before rendering; deduplicate semantic instances.
    candidates = [(sid, p) for sid in sorted(CASES) for p in domain(sid)]
    rng.shuffle(candidates)
    rows, seen = [], set()
    while candidates and len(rows) < count:
        assigned, deferred = set(), []
        for sid, p in candidates:
            if len(rows) >= count: break
            # Dimensions are incidental here: the same concept triplet should
            # not always ask for the same subset in a short practice batch.
            decision = (SLOTS[sid], checkbox(sid), tuple(p['truths']))
            if decision in assigned:
                deferred.append((sid, p))
                continue
            r = generate(difficulty, seed, sid, p)
            q = r['question']
            semantic = (q[':question/problem'], tuple(sorted(f[':answer-field/key'] for f in q[':question/answer-fields'])))
            if semantic in seen: continue
            rows.append(r); seen.add(semantic); assigned.add(decision)
        # Keep all compatible values and premise cases available after the
        # first pass; this changes order, never the supported finite domain.
        candidates = deferred
    return rows

def markdown(rec):
    q = rec['question']
    return q[':question/problem'] + '\n\n' + '\n'.join(f[':answer-field/key'] for f in q[':question/answer-fields']) + '\n\n' + q[':question/worked-solution']

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--difficulty', default='moderate')
    ap.add_argument('--count', type=int, default=5)
    ap.add_argument('--seed', type=int, default=24629)
    ap.add_argument('--format', choices=('json', 'markdown'), default='json')
    ap.add_argument('--markdown', action='store_true')
    args = ap.parse_args()
    rows = batch(args.difficulty, args.count, args.seed)
    print('\n\n---\n\n'.join(map(markdown, rows)) if args.markdown or args.format == 'markdown' else json.dumps(rows, indent=2))
