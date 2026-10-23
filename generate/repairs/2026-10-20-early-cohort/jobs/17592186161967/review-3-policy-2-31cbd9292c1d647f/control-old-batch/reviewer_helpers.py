# Parsers and arithmetic checker reused from previous independent audit.py.
import json, re, pathlib, importlib.util, sys, hashlib, shutil, platform, collections

def mats(s):
    return [[[int(x.strip()) for x in row.split('&')] for row in raw.split('\\\\')] for raw in re.findall('\\\\begin\\{bmatrix\\}(.*?)\\\\end\\{bmatrix\\}', s, re.S)]

def ops(s):
    s = s.replace('{R}', 'R')
    return [(int(i) - 1, int(j) - 1, (1 if sign == '+' else -1) * int(n or 1), int(p) - 1) for i, j, sign, n, p in re.findall('R_\\{(\\d)\\}:=R_\\{(\\d)\\}\\s*([+-])\\s*(\\d*)\\s*R_\\{(\\d)\\}', s)]

def apply(A, o):
    B = [r[:] for r in A]
    for i, j, k, p in o:
        assert i == j and i != p
        B[i] = [v + k * w for v, w in zip(B[i], B[p])]
    return B

def check(r):
    q = r['question']
    A, B = mats(q[':question/problem'])
    f = q[':question/answer-fields'][0]
    validity = [apply(A, ops(c[':answer/value'])) == B for c in f[':answer-field/choices']]
    assert sum(validity) == 1
    ix = validity.index(True)
    assert f[':answer-field/choices'][ix][':answer/id'] == f[':answer-field/correct'][1]
    ss = mats(q[':question/worked-solution'])
    oo = ops(q[':question/worked-solution'])
    assert len(ss) == 3 and ss[0] == A and (ss[1] == apply(A, oo[:1])) and (ss[2] == B) and (apply(A, oo[:2]) == B)
    return ix
