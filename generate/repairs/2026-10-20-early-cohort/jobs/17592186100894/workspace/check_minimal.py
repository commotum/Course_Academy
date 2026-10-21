"""Exact retained review counterexample; predicts from visible content only."""
from audit_support import *
from collections import Counter

def probe(r):
    _, (abscissa, ordinate) = prompt_data(r)
    h = simplify(abscissa-S.pi/2)
    opts = field(r)[':answer-field/choices']
    coeffs = [S.expand(explicit(r, a[':answer/value'])-S.log(S.sin(x-h))).coeff(x, 2) for a in opts]
    repeated = [v for v, n in Counter(coeffs).items() if n > 1]
    qualifies = simplify(ordinate/S.pi**2).is_Rational is True and len(repeated) == 1
    indices = [i for i, v in enumerate(coeffs) if v == repeated[0]] if qualifies else []
    prediction = min(indices, key=lambda i: len(opts[i][':answer/value'])) if indices else None
    success = prediction is not None and opts[prediction][':answer/id'] == field(r)[':answer-field/correct'][1]
    return {'qualifies': qualifies, 'coefficients': list(map(str, coeffs)), 'shortcut_success': success,
            'predicted_value': opts[prediction][':answer/value'] if prediction is not None else None}

if __name__ == '__main__':
    E.mkdir(exist_ok=True)
    r = g.generate('easy', 492800, 'q-104065', {'h': 1, 'a': 4, 'c': '0'})
    save('minimal-record.json', [r])
    result = probe(r)
    save('minimal-result.json', result)
    print(json.dumps(result))
    assert not result['shortcut_success'], 'Incidental bank cue selects the correct answer without solving the IVP'
