"""Full-answer choice support without disclosing the substitution.

Candidates encode differential-factor, argument and primitive mistakes. Reject
equivalent antiderivatives (including additive constants) before sampling.
"""
import random
import sympy as s


def answer_bank(correct, primitive_u, inner, x, u, fingerprint, render,
                *, lower=None, upper=None, max_number=None):
    definite = lower is not None
    rng = random.Random('complete-integral-bank-v1:' + fingerprint)
    def signature(value):
        return s.simplify(s.diff(value, x) if not definite else value)
    key_signature = signature(correct)
    seen = [key_signature]
    pools = {'factor': [], 'structure': []}
    candidates = [(correct*c, label, 'factor') for c, label in (
        (-1, 'wrong_sign'), (s.Rational(1, 2), 'extra_half'),
        (2, 'double_factor'), (s.Rational(1, 3), 'extra_third'),
        (3, 'triple_factor'), (-2, 'negative_double'))]
    if definite:
        # Omitting either endpoint and using a sum are different FTC errors.
        first, last = (primitive_u.subs(u, inner.subs(x, v)) for v in (lower, upper))
        candidates += [(last, 'omit_lower_endpoint', 'structure'),
                       (-first, 'omit_upper_endpoint', 'structure'),
                       (last+first, 'add_endpoint_values', 'structure')]
        candidates += [(correct+v, 'endpoint_offset_'+str(v), 'structure') for v in (1, -1, 2)]
    else:
        for arg, label in ((x, 'omit_inner'), (2*inner, 'double_inner'),
                           (inner/2, 'half_inner'), (inner+1, 'shift_inner')):
            # Replace before simplification: log(2u) may differ only by a
            # constant. The derivative check below removes that distractor.
            candidates.append((primitive_u.subs(u, arg), label, 'structure'))
        candidates.append((inner, 'return_substitution', 'structure'))
    rng.shuffle(candidates)
    for value, label, kind in candidates:
        sig = signature(value)
        if any(s.simplify(sig-old) == 0 for old in seen):
            continue
        text = render(value) + ('' if definite else '+C')
        if max_number is not None:
            import re
            if any(int(n) > max_number for n in re.findall(r'\d+', text)):
                continue
        seen.append(sig)
        pools[kind].append((text, label))
    # Vary the bank profile. Both factor and structural mistakes must remain
    # plausible; a fixed majority argument must not reveal the correct choice.
    nfactor = rng.choice((1, 2, 3))
    nfactor = max(1, min(nfactor, len(pools['factor'])))
    nstructure = 4-nfactor
    if nstructure > len(pools['structure']):
        nstructure = len(pools['structure']); nfactor = 4-nstructure
    if nstructure < 1 or nfactor > len(pools['factor']):
        raise ValueError('Insufficient distinct complete-answer distractors')
    bank = [(render(correct)+('' if definite else '+C'), 'correct')]
    bank += pools['factor'][:nfactor] + pools['structure'][:nstructure]
    rng.shuffle(bank)
    return bank
