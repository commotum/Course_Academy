#!/usr/bin/env python3
"""Normal-line intercepts: seven complete source templates, bounded scaling.

Positive integer coefficient scales 1..12 are an authored extension. Each bank
retains its complete source profile. No new plots or difficulty promotion.
"""
import argparse
import hashlib
import json
import random
import re
import uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    import os, sys
    runtime = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    os.execv(str(runtime), [str(runtime), str(Path(__file__).resolve()), *sys.argv[1:]])

HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186092385
KP_UUID = '3ba61258-92a9-511e-891f-9e6adce2edb0'
TITLE = SOURCE['record'][':knowledge-point/title']
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = '1.0.0'
SUPPORTED_LEVELS = ('easy', 'moderate')
x = sp.Symbol('x', real=True)
SPECS = {
    'q-10871': (2*x**2+x, 1, 'x', 'easy'),
    'q-11124': (2*sp.sqrt(x), 1, 'y', 'moderate'),
    'q-104073': (3*x**sp.Rational(2,3), 8, 'y', 'moderate'),
    'q-104075': (2*x**sp.Rational(3,2), 1, 'x', 'moderate'),
    'q-308823': (2/x+1, 1, 'x', 'moderate'),
    'q-342200': (4-x**2, 1, 'x', 'easy'),
    'q-342201': (3*x**2-6*x+5, 0, 'x', 'easy'),
}
ROWS = {q[':question/math-academy-id']: q for q in SOURCE['record'][':knowledge-point/questions']}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), value))

def fingerprint_expr(f, p, axis):
    # Prompt mathematics, including the target axis; independent of bank/order/seed.
    return digest({'curve': sp.srepr(sp.expand(sp.powdenest(f, force=True))), 'abscissa': str(p), 'axis': axis})

def task(mid, scale=1):
    original, p, axis, level = SPECS[mid]
    f = sp.expand(scale * original)
    p = sp.Integer(p)
    y = sp.simplify(f.subs(x, p))
    d = sp.diff(f, x)
    m = sp.simplify(d.subs(x, p))
    assert m != 0 and m.is_finite
    n = -1/m
    b = sp.simplify(y - n*p)
    a = sp.simplify(-b/n) if axis == 'x' else b
    return f, p, y, d, m, n, b, a

def bank(mid, scale):
    f, p, y, d, m, n, b, a = task(mid, scale)
    if mid == 'q-10871': return [-p, p, m, a, a/m]
    if mid == 'q-11124': return [1/m, y, y+1/(2*m), 1/(2*m), a]
    if mid == 'q-104073': return [-a, a, -p, y-p, -(y-p)]
    if mid == 'q-104075': return [m, 1/a, 1/m, p, a]
    return [a]

def curve(mid, s):
    f = task(mid, s)[0]
    if mid == 'q-11124': return str(2*s)+r'\sqrt{x}'
    if mid == 'q-104073': return str(3*s)+r'\sqrt[3]{x^{2}}'
    if mid == 'q-104075': return str(2*s)+r'\sqrt{x^{3}}'
    if mid == 'q-308823': return r'\frac{'+str(2*s)+r'}{x}+'+str(s)
    return sp.latex(f)

def rendered_blocks(mid, s):
    f,p,y,d,m,n,b,a = task(mid, s)
    L = sp.latex
    if SPECS[mid][3] == 'moderate':
        # Preserve the observed radical/reciprocal -> power -> derivative ->
        # radical/reciprocal sequence, including explicit constant-factor step.
        power = L(f, root_notation=False)
        exponent = d.as_powers_dict()[x]
        coefficient = sp.simplify(d/x**exponent)
        differentiated_power = L(coefficient)+r'x^{'+str(exponent)+'}'
        if mid == 'q-342222': raise ValueError('Incomplete source is unsupported')
        derivative = r"\begin{aligned}f'(x)&=\frac{\mathrm{d}}{\mathrm{d}x}("+curve(mid,s)+r')\\&=\frac{\mathrm{d}}{\mathrm{d}x}('+power+r')\\&='+differentiated_power+r'\\&='+L(d)+r'.\end{aligned}'
    else:
        derivative = r"f'(x)=\frac{\mathrm{d}}{\mathrm{d}x}("+L(f)+')='+L(d)+'.'
        if mid == 'q-10871': derivative=r'\begin{aligned}'+derivative+r'\end{aligned}'
    slope = "m=f'("+L(p)+')='+L(d.subs(x,p,evaluate=False))+'='+L(m)+','
    reciprocal = r"m'=-\frac{1}{m}=-\frac{1}{("+L(m)+')}='+L(n)+'.'
    line = r'\begin{aligned}y-('+L(y)+')&='+L(n)+'(x-('+L(p)+r'))\\y&='+L(n)+'x'+ ('+' if b>=0 else '')+L(b)
    if mid != 'q-342201':
        # Keep the three-stage point-slope, distributed, simplified sequence.
        distributed = 'y&='+L(n)+'x-('+L(n*p)+')+('+L(y)+')'
        first, last = line.split(r'\\')
        line = first+r'\\'+distributed+r'\\'+last
    line += r'.\end{aligned}'
    if SPECS[mid][2] == 'x':
        intercept = r'\begin{aligned}'+L(n)+'x'+('+' if b>=0 else '')+L(b)+'&=0'
        if mid in ('q-342200','q-342201'):
            intercept += r'\\'+L(n)+'x&='+L(-b)
        intercept += r'\\x&='+L(a)+r'.\end{aligned}'
    else:
        intercept = r'\begin{aligned}y&='+L(n)+r'\cdot0'+('+' if b>=0 else '')+L(b)+r'\\y&='+L(a)+r'.\end{aligned}'
    return [derivative, slope, reciprocal, line, intercept]

def generate_profile(mid, scale, seed=0):
    if mid not in SPECS or scale not in range(1,13): raise ValueError('Outside bounded catalog')
    original = ROWS[mid]
    f,p,y,d,m,n,b,a = task(mid, scale)
    vals = list(map(sp.simplify, bank(mid, scale)))
    if len(set(vals)) != len(vals) or vals.count(a) != 1: raise ValueError('Ambiguous bank')
    axis = SPECS[mid][2]
    fp = fingerprint_expr(f,p,axis)
    qid = uid('question:'+fp)
    problem, solution = original[':question/problem'], original[':question/worked-solution']
    if scale != 1:
        problem = re.sub(r'\$(?:f\(x\)|y)=.*?\$', lambda _: '$'+('f(x)' if '$f(x)=' in problem else 'y')+'='+curve(mid,scale)+'$', problem, count=1)
        problem = re.sub(r'at the point \$\(.*?\)\$', lambda _: 'at the point $('+sp.latex(p)+','+sp.latex(y)+')$', problem, count=1)
        blocks = list(re.finditer(r'\$\$\n.*?\n\$\$', solution, re.S))
        assert len(blocks) == 5
        for match,value in reversed(list(zip(blocks,rendered_blocks(mid,scale)))):
            solution = solution[:match.start()]+'$$\n'+value+'\n$$'+solution[match.end():]
        point = '('+sp.latex(a)+',0)' if axis=='x' else '(0,'+sp.latex(a)+')'
        solution = re.sub(r'(Therefore,.*? at\s+)\$.*?\$', lambda match: match[1]+'$'+point+'.$', solution, flags=re.S)
    fields=[]
    for of in sorted(original[':question/answer-fields'], key=lambda f:f[':answer-field/key']):
        key=of[':answer-field/key'];ft=of[':answer-field/type'][':db/ident'];fid=uid(qid+':'+key)
        values = vals if ft==':answer-field.type/radio' else [a if key=='field-1' else sp.Integer(0)]
        texts = [('('+sp.latex(v)+',0)' if axis=='x' else '(0,'+sp.latex(v)+')') if ft==':answer-field.type/radio' else sp.latex(v) for v in values]
        answers=[{':answer/id':uid(fid+':'+str(v)),':answer/type':':answer.type/math',':answer/value':t} for v,t in zip(values,texts)]
        correct=answers[values.index(a) if ft==':answer-field.type/radio' else 0][':answer/id']
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ft,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+SPECS[mid][3],':question/answer-fields':fields}
    return {'question':q,'knowledge_point':{'id':KP_UUID,'title':TITLE},'generation':{'version':VERSION,'template':mid,'profile':mid if len(vals)>1 else None,'parameters':{'scale':scale},'seed':seed,'parameter_fingerprint':fp,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'domain':'x>0' if mid in ('q-11124','q-104073','q-104075') else 'x!=0' if mid=='q-308823' else 'real x','sympy':sp.__version__}}

def batch(level,count,seed):
    if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: '+level)
    if count<1: return []
    catalog=[(mid,s) for mid in SPECS if SPECS[mid][3]==level for s in range(1,13)]
    random.Random(seed).shuffle(catalog)
    out=[];seen=set()
    for mid,s in catalog:
        try: r=generate_profile(mid,s,seed)
        except ValueError: continue
        fp=r['generation']['parameter_fingerprint']
        if fp in seen: continue
        out.append(r);seen.add(fp)
        if len(out)>=count: break
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',required=True)
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json','markdown'],default='json')
    args=parser.parse_args();rows=batch(args.difficulty,args.count,args.seed)
    print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in rows))
