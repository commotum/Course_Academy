#!/usr/bin/env python3
"""Seeded surface-area-integrand practice; no services or repository imports."""
import argparse
import hashlib
import itertools
import json
import random
import uuid
import sympy as S
import source_models as legacy
from math_format import normalize_prose, normalize_tex, validate_generated_record

U, V = legacy.U, legacy.V
KP_ID, KP_UUID, TITLE = legacy.KP_ID, legacy.KP_UUID, legacy.TITLE
VERSION = 'surface-integrand-v3'
FAMILIES = {
    'easy': ['plane'],
    'moderate': ['plane', 'graph', 'q-109941', 'q-109943'],
    'hard': ['q-105613', 'q-109948', 'q-110019', 'q-109947', 'q-109951'],
}
tex = lambda x: normalize_tex(S.latex(x))
vec = lambda xs: r'\langle ' + r',\,'.join(tex(x) for x in xs) + r'\rangle'
display = lambda x: '$$\n' + x + '\n$$'
aligned = lambda rows: display(r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}')


def ident(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), VERSION + ':' + value))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def instance(family, p):
    """Keep the source's operator inputs and nonnegative-radius domain."""
    a, b = S.Integer(p['a']), S.Integer(p.get('b', 1))
    if family == 'plane':
        r = S.Matrix([U, V, a*U+b*V])
        answer = S.sqrt(1+a*a+b*b)
        bounds = (2, 1)
    elif family == 'graph':
        r = S.Matrix([U, V, a*U**2+b*V**2])
        answer = S.sqrt(1+4*a*a*U**2+4*b*b*V**2)
        bounds = (1, 2)
    else:
        r, answer, _ = legacy.model(family, p)
        if family == 'q-105613' and 'b' in p:
            r=S.Matrix([a*U*S.sin(V),b*U*S.cos(V),U])
            answer=U*S.sqrt((b*b-a*a)*S.sin(V)**2+a*a*(1+b*b))
        bounds = legacy.TEMPLATES[family]['bounds']
        if family == 'q-110019':
            bounds = (2, S.pi)  # Retain the source displayed domain, not its inconsistent prose.
            if p.get('axis_swap'):
                r = S.Matrix([U**2, U*S.sin(V), a*U*S.cos(V)])
                answer = U*S.sqrt(a*a+4*U**2+4*(a*a-1)*U**2*S.sin(V)**2)
    if p.get('parameter_swap'):
        r = r.subs({U: V, V: U}, simultaneous=True)
        answer = answer.subs({U: V, V: U}, simultaneous=True)
        bounds = bounds[::-1]
    if p.get('translation'):
        r += S.Matrix([p['translation'], 0, 0])
    return r, answer, tuple(map(S.sympify, bounds))


def parameters(family):
    if family in ('plane', 'graph'):
        limit=5 if family=='plane' else 3
        base = [{'a': a, 'b': b} for a in range(-limit,limit+1) if a for b in range(1,limit+1)]
    else:
        base = [dict(p) for p in legacy.TEMPLATES[family]['domain']]
        if family == 'q-109943':
            base += [{'a':a,'b':a} for a in (2,3,4)] + [{'a':2,'b':3}]
        if family == 'q-110019':
            base += [{'a':1}]
        if family == 'q-105613':
            base += [{'a':a,'b':a} for a in (1,2,3)]
    return [dict(p, parameter_swap=swap, axis_swap=axis)
            for p in base for swap in (False,True)
            for axis in ((False, True) if family == 'q-110019' else (False,))]


# Complete authored error profiles. Each wrong norm comes from its own explicit
# component-count mistake: retain only one component; omit one and count another
# twice (two variants); add magnitudes or forget to square the components.
# Varying the component assignments and whole-norm error avoids a fixed rank and
# prevents the key from being the sole modal coefficient combination.
PROFILES = [
    {'singleton': i, 'mixed': (j,k), 'whole': whole}
    for i in range(3)
    for j,k in itertools.combinations(list(itertools.permutations((0,1,2))), 2)
    for whole in (S.Rational(1,2), S.Integer(2))
]

PROFILES += [dict(profile, whole_component=i) for profile in list(PROFILES) for i in range(3)]

PROFILES += [{'norm_errors': (i,j,k)} for i in range(3) for j in range(3) for k in range(3)]

PROFILES += [{'norm_overcounts': (i,j,k)} for i in range(3) for j in range(3) for k in range(3)]

def bank_from_profile(cross, answer, profile):
    terms = [S.expand(x*x) for x in cross]
    if 'norm_overcounts' in profile:
        i,j,k=profile['norm_overcounts']
        h=sum(terms)
        return [answer,S.sqrt(terms[i]),S.sqrt(S.factor(h+terms[j])),S.sqrt(S.factor(h+3*terms[k])),answer**2], [('singleton',i),('duplicated',j),('doubled-component',k),('missing-root',)]
    if 'norm_errors' in profile:
        i,j,k=profile['norm_errors']
        h=sum(terms)
        return [answer,S.sqrt(terms[i]),S.sqrt(S.factor(h-terms[j])),S.sqrt(S.factor(h+terms[k])),answer**2], [('singleton',i),('omitted',j),('duplicated',k),('missing-root',)]
    weights = [tuple(int(j == profile['singleton']) for j in range(3)),
               *profile['mixed'], (profile['whole'],)*3]
    vals = [answer]
    for index,weight in enumerate(weights):
        if index==3:
            if 'whole_component' in profile:
                # Double a component before taking the norm; its energy is
                # quadrupled. This keeps a full radicand without fixing rank.
                vals.append(S.sqrt(S.factor(sum(terms)+3*terms[profile['whole_component']])))
            else:
                total=sum(S.sqrt(term) for term in terms)
                vals.append(total if profile['whole']==2 else S.sqrt(total))
            continue
        h = sum(w*t for w,t in zip(weight,terms))
        value = S.sqrt(S.factor(S.expand(h)))
        vals.append(value)
    return vals, [*weights[:3], ('doubled-component' if 'whole_component' in profile else 'sum-magnitudes' if profile['whole']==2 else 'forgot-squares',)]


def distinct_bank(vals):
    # Interior point signatures are rejection witnesses, not an equivalence CAS.
    points = [(S.Rational(2,5),S.Rational(3,7)), (S.Rational(4,5),S.Rational(1,5)),
              (S.Rational(1,3),S.Rational(7,8))]
    signatures = [tuple(round(float(x.subs({U:u,V:v}).evalf()),9) for u,v in points) for x in vals]
    return len(set(signatures)) == 5 and all(all(x > 0 for x in sig) for sig in signatures)


def worked_solution(r, answer, bounds):
    ru, rv = r.diff(U), r.diff(V)
    raw = ru.cross(rv)
    cross = raw.applyfunc(S.trigsimp)
    norm = r'\left\|\mathbf r_u\times\mathbf r_v\right\|'
    sol = 'The surface-area integrand is the magnitude of the fundamental vector product:\n\n'
    sol += display(r'A(S)=\iint_D '+norm+r'\,\mathrm dA.')
    sol += '\n\nDifferentiate each coordinate with respect to each parameter:\n\n'
    sol += aligned([r'\mathbf r_u&='+vec(ru), r'\mathbf r_v&='+vec(rv)])
    determinant = legacy.det([[r'\mathbf i',r'\mathbf j',r'\mathbf k'],list(map(tex,ru)),list(map(tex,rv))])
    sol += '\n\nExpand the determinant to find the cross product:\n\n'
    sol += display(r'\mathbf r_u\times\mathbf r_v='+determinant)
    if raw != cross:
        # Keep each unsimplified component on its own row: a full expanded
        # trigonometric vector can overflow the actual learning card.
        sol += '\n\n'+aligned([r'c_'+str(i+1)+'&='+tex(raw[i])+('='+tex(cross[i]) if raw[i]!=cross[i] else '') for i in range(3)])
    sol += '\n\n'+display(r'\mathbf r_u\times\mathbf r_v='+vec(cross))
    if r.has(S.sin) or r.has(S.cos):
        angular = U if r.has(S.sin(U),S.cos(U)) else V
        sol += '\n\nUse $'+tex(S.sin(angular)**2)+'+'+tex(S.cos(angular)**2)+r'=1$ to combine the squared trigonometric terms.'
    sol += '\n\nSquare the components, add, and take the nonnegative square root:\n\n'
    square_terms = [r'\left('+tex(x)+r'\right)^2' for x in cross]
    sol += aligned([norm+r'^2&='+square_terms[0]+'+'+square_terms[1],r'&\quad+'+square_terms[2]])+'\n\n'
    collected = S.expand(answer**2)
    rows = [norm+r'&=\sqrt{'+tex(collected)+'}']
    # Display the actual factor extraction before its simplified final form.
    factored = S.factor(collected)
    if factored != collected:
        rows.append(r'&=\sqrt{'+tex(factored)+'}')
    rows.append(r'&='+tex(answer))
    sol += aligned(rows)
    extracted=[]
    for var in (U,V):
        if answer.has(var) and answer.subs(var,0)==0:
            extracted.append('$\\sqrt{'+str(var)+'^2}=|'+str(var)+'|='+str(var)+'$')
    if extracted:
        sol += '\n\nOn $D$, both parameters are nonnegative, so '+ ' and '.join(extracted)+'.'
    if answer.has(S.exp):
        sol += '\n\nExponential factors are positive, so their squared factors have positive square roots.'
    sol += '\n\nThus the required integral is\n\n'+display(r'A(S)=\iint_D '+tex(answer)+r'\,\mathrm dA.')
    sol += '\n\nThe missing expression is $'+tex(answer)+'$. The integral does not need to be evaluated.'
    return normalize_prose(sol), cross


def generate(difficulty='moderate', seed=0, template=None, parameters=None, profile=None, replay=False):
    rng = random.Random(seed)
    family = template or rng.choice(FAMILIES[difficulty])
    if family not in FAMILIES[difficulty]:
        raise ValueError('Family/difficulty mismatch')
    p = dict(parameters or rng.choice(globals()['parameters'](family)))
    r, answer, bounds = instance(family,p)
    solution, cross = worked_solution(r,answer,bounds)
    if replay:
        if family not in legacy.TEMPLATES or p != legacy.TEMPLATES[family]['base']:
            raise ValueError('Replay requires original source parameters')
        _, _, vals = legacy.model(family,p)
        weights, profile_id = [], 'observed-expression-pattern:'+family
    else:
        profiles = list(range(len(PROFILES))) if profile is None else [int(profile)]
        rng.shuffle(profiles)
        for profile_id in profiles:
            vals, weights = bank_from_profile(cross,answer,PROFILES[profile_id])
            # A cancellation must not make the key the bank's only trig-free
            # expression. Include a whole-component error that preserves that
            # cancellation (e.g. doubling the radial cross-product component).
            # Derive its energy from this instance, rather than adding filler.
            if r.has(S.sin, S.cos) and not answer.has(S.sin, S.cos):
                if sum(not x.has(S.sin, S.cos) for x in vals) == 1:
                    h = S.expand(answer**2)
                    energies = [S.trigsimp(S.expand(x*x)) for x in cross]
                    candidates = [S.sqrt(S.factor(h+3*e)) for e in energies
                                  if e != 0 and not e.has(S.sin, S.cos)]
                    rng.shuffle(candidates)
                    replacement = next((x for x in candidates
                                        if distinct_bank(vals[:4]+[x])), None)
                    if replacement is None:
                        continue
                    vals[-1] = replacement
                    weights[-1] = ('doubled-component-before-norm',)
            # Keep a plausible full-norm error when the correctly combined
            # radicand would otherwise be the sole longest displayed option.
            # Existing omission/duplication profiles supply such alternatives;
            # reject the complete profile instead of padding a choice.
            lengths = [len(tex(x)) for x in vals]
            key_is_unique_longest = lengths[0] > max(lengths[1:])
            if key_is_unique_longest:
                # Two components doubled before taking the norm is another
                # identifiable error. It avoids rejecting valid densities just
                # because their canonical radical happens to be longer.
                h=S.expand(answer**2)
                energies=[S.trigsimp(S.expand(x*x)) for x in cross]
                candidates=[S.sqrt(S.factor(h+3*(h-e))) for e in energies]
                rng.shuffle(candidates)
                replacement=next((x for x in candidates
                                  if len(tex(x))>=lengths[0]
                                  and (answer.has(S.sin,S.cos) or not r.has(S.sin,S.cos)
                                       or not x.has(S.sin,S.cos))
                                  and distinct_bank(vals[:4]+[x])),None)
                if replacement is not None:
                    vals[-1]=replacement
                    weights[-1]=('doubled-two-components-before-norm',)
                    key_is_unique_longest=False
            if distinct_bank(vals) and not key_is_unique_longest:
                break
        else:
            raise ValueError('No complete distinct bank for this instance')
    values = [tex(x) for x in vals]
    ci = next(i for i,x in enumerate(vals) if S.simplify(x-answer)==0)
    prompt = display(r'\iint_D\boxed{\phantom{AAAAAAAA}}\,\mathrm dA')
    prompt += '\n\n'+display(r'D=\{(u,v):0\le u\le '+tex(bounds[0])+r',\ 0\le v\le '+tex(bounds[1])+r'\}')
    prompt += '\n\nThe integral above gives the surface area of the parametric surface\n\n'
    prompt += display(r'\mathbf r(u,v)='+vec(r))
    prompt += '\n\nfor $(u,v)\\in D$.'
    if difficulty == 'easy':
        prompt += '\n\nThe tangent vectors are\n\n'+aligned([r'\mathbf r_u&='+vec(r.diff(U)),r'\mathbf r_v&='+vec(r.diff(V))])
    prompt += '\n\nWhat is the missing expression?'
    prompt = normalize_prose(prompt)
    squared=S.expand(answer**2)
    renamed=S.expand(squared.subs({U:V,V:U},simultaneous=True))
    # Bounds which do not change sign, parameter renaming, and translations do
    # not create new missing-integrand work. Count density functions conservatively.
    semantic = digest({'squared_area':min(str(squared),str(renamed)), 'domain_sign':'nonnegative'})
    content = digest([prompt,solution,sorted(values),values[ci],difficulty])
    qid = ident('question:'+content)
    fid = ident('field:'+qid)
    choices = [{':answer/id':ident(fid+':'+val),':answer/type':':answer.type/math',':answer/value':val} for val in values]
    correct = choices[ci][':answer/id']
    rng.shuffle(choices)
    rec = {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
           'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
                       ':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[
                           {':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
                            ':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},
           'generation':{'version':VERSION,'template':family,'seed':seed,'parameters':p,'bank_profile':str(profile_id),
                         'source_question':legacy.QS[family][':db/id'] if family in legacy.QS else None,
                         'source_basis':legacy.SOURCE['basis'],'mathematical_task_fingerprint':semantic,
                         'error_weights':[[str(x) for x in row] for row in weights],
                         'correct_expression':str(answer),'plot_rating':'none'}}
    return validate_generated_record(rec)


def batch(difficulty, count, seed):
    rng = random.Random(seed)
    pools = {f:parameters(f) for f in FAMILIES[difficulty]}
    for pool in pools.values():
        rng.shuffle(pool)
    rows, seen = [], set()
    families = list(pools)
    while any(pools.values()) and len(rows)<count:
        rng.shuffle(families)
        for family in families:
            while pools[family]:
                p = pools[family].pop()
                try:
                    r = generate(difficulty,rng.getrandbits(63),family,p)
                except ValueError as err:
                    if 'No complete distinct bank' in str(err):
                        continue
                    raise
                semantic = r['generation']['mathematical_task_fingerprint']
                if semantic in seen:
                    continue
                seen.add(semantic)
                rows.append(r)
                break
            if len(rows)==count:
                break
    if len(rows)<count:
        raise ValueError(f'Requested {count}; finite semantic pool supplied only {len(rows)}')
    # A small practice pool must not be answered by a single numerical rank.
    # Change the complete error profile, preserving each mathematical instance,
    # rather than choosing a new seed or hand-picking replacement questions.
    def rank(record):
        field = record['question'][':question/answer-fields'][0]
        key = field[':answer-field/correct'][1]
        vals = field[':answer-field/choices']
        # Every authored choice was derived from the live symbolic instance.
        # Reconstruct its bank from its profile to rank before publication.
        family = record['generation']['template']
        r, answer, _ = instance(family,record['generation']['parameters'])
        hvals, _ = bank_from_profile(r.diff(U).cross(r.diff(V)).applyfunc(S.trigsimp), answer,
                                    PROFILES[int(record['generation']['bank_profile'])])
        # Cancellation repairs may replace the final option; use its displayed
        # value via the canonical SymPy printer map generated above when needed.
        values = {tex(x): x for x in hvals}
        for term in r.diff(U).cross(r.diff(V)):
            energy=S.trigsimp(S.expand(term*term))
            if not energy.has(S.sin,S.cos):
                x=S.sqrt(S.factor(S.expand(answer**2)+3*energy)); values[tex(x)]=x
            x=S.sqrt(S.factor(S.expand(answer**2)+3*(S.expand(answer**2)-energy))); values[tex(x)]=x
        scores=[float(values[a[':answer/value']].subs({U:S.Rational(2,5),V:S.Rational(3,7)}).evalf()) for a in vals]
        ci=next(i for i,a in enumerate(vals) if a[':answer/id']==key)
        return sorted(range(5),key=lambda i:scores[i]).index(ci)
    groups = {}
    for index, record in enumerate(rows):
        groups.setdefault(record['generation']['template'], []).append(index)
    groups['__all__'] = list(range(len(rows)))
    for indices in groups.values():
        if len(indices)<2 or len({rank(rows[i]) for i in indices})>1:
            continue
        index=indices[-1];old_rank=rank(rows[index]);original=rows[index]['generation']
        for _ in range(128):
            candidate=generate(difficulty,rng.getrandbits(63),original['template'],original['parameters'])
            if rank(candidate)!=old_rank:
                rows[index]=candidate
                break
        else:
            raise ValueError('Could not construct varied error-profile ranks for the batch')
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=list(FAMILIES), default='moderate')
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    if args.count < 1:
        parser.error('--count must be positive')
    print(json.dumps(batch(args.difficulty,args.count,args.seed),indent=2,ensure_ascii=False))
