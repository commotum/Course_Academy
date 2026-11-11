"""Retain the pre-fix ordinary-bank coverage counterexample as a visible-output test."""

def check(generate, givens, vector):
    result={}
    for band in ('moderate','hard'):
        kinds=set()
        for seed in range(820,832):
            for record in generate(band,6,seed):
                q=record['question'];M=givens(q[':question/problem'])
                candidates=[vector(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices']]
                first=[sum(M[0][j]*v[j] for j in range(3))==M[0][3] for v in candidates]
                second=[sum(M[1][j]*v[j] for j in range(3))==M[1][3] for v in candidates]
                assert all(first), 'Fresh solve bank must preserve its common first equation'
                kinds.add('last-constraint' if all(second) else 'two-constraints')
        assert kinds=={'last-constraint','two-constraints'}, 'Ordinary sampler lost an observed support/response demand'
        result[band]={'ordinary_records':72,'visible_support_families':sorted(kinds)}
    return result
