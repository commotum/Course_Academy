import argparse, collections, hashlib, importlib.util, json, pathlib, re, subprocess, sys
sys.dont_write_bytecode = True
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
ROOT = pathlib.Path(__file__).resolve().parent
JOB = ROOT.parent
REPO = pathlib.Path('/home/jake/Developer/Course_Academy')
def save(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, ensure_ascii=False))
def read(p): return json.loads(pathlib.Path(p).read_text())
def load(package):
    spec=importlib.util.spec_from_file_location('reviewed',pathlib.Path(package)/'17592186064206.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def coeff(v):
    v=v.strip()
    if v in ('','-'): return s.Integer(-1 if v=='-' else 1)
    m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',v)
    if m:return (-1 if m[1] else 1)*s.Rational(m[2],m[3])
    return s.Rational(v)
def log(v):
    m=re.fullmatch(r'(.*?)\\operatorname\{ln\}\u2061?\|([^|]+)\|\+C',v)
    if not m: raise ValueError(v)
    return coeff(m[1]),m[2]
def expr(v):return parse_expr(v, transformations=standard_transformations+(implicit_multiplication_application,))
def field(r):return r['question'][':question/answer-fields'][0]
def key(f):
    v=f[':answer-field/correct'];return v[1] if isinstance(v,list) else v[':answer/id']
def shortcut(r):
    # No prompt, generation metadata, key, position or IDs consulted for the decision.
    choices=field(r)[':answer-field/choices']; parts=[log(a[':answer/value']) for a in choices]
    if len(set(arg for c,arg in parts))==1:
        if sum(bool(c<0) for c,arg in parts)==3:
            eligible=[i for i,(c,arg) in enumerate(parts) if -1<c<0];cue='same argument; three negatives: choose negative proper fraction'
        else:
            largest=max(c for c,arg in parts)
            eligible=[i for i,(c,arg) in enumerate(parts) if c==largest];cue='same argument; two negatives: choose largest positive coefficient'
    else:
        eligible=[i for i,(c,arg) in enumerate(parts) if c==1 and arg!='x'];cue='mixed arguments: choose positive unit coefficient with shifted argument'
    return (choices[eligible[0]][':answer/id'] if len(eligible)==1 else None),cue
def probe(records):
    rows=[]
    for r in records:
        chosen,cue=shortcut(r)
        rows.append({'id':r['question'][':question/id'],'template':r['generation']['template'],'cue':cue,'selected':chosen,'correct':chosen==key(field(r))})
    groups={}
    for attr in ['cue','template']:
        for value in sorted(set(row[attr] for row in rows)):
            sub=[row for row in rows if row[attr]==value]
            groups[attr+':'+value]={'correct':sum(row['correct'] for row in sub),'total':len(sub),'baseline':0.2}
    return {'correct':sum(row['correct'] for row in rows),'total':len(rows),'groups':groups,'records':rows}
