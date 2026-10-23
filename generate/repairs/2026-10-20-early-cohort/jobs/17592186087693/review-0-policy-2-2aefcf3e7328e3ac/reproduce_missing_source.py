"""Strict regression: current package must replay every supplied source profile.
Usage: repo/.venv/bin/python -B reproduce_missing_source.py --package PATH
Exit 1 preserves the demonstrated failure; no package files are modified.
"""
import sys,pathlib,argparse,json,re
sys.dont_write_bytecode=True
p=argparse.ArgumentParser();p.add_argument('--package',required=True);a=p.parse_args();sys.path.insert(0,a.package)
import generator as g
source=json.load(open(pathlib.Path(__file__).resolve().parent.parent/'source/source.json'))
q=next(q for q in source['material']['kp'][':knowledge-point/questions'] if q[':question/id']=='80862d10-12ca-5f6e-9209-5f8bf84be504')
r=g.generate(seed=20261022,profile='observed-q-139628')
body=lambda s: re.sub(r'\s+','',re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)[1])
assert body(q[':question/problem'])==body(r['question'][':question/problem'])
fs=sorted(r['question'][':question/answer-fields'],key=lambda f:f[':answer-field/key'])
assert len(fs)==2
for f in fs:
 assert f[':answer-field/type']==':answer-field.type/blank'
 assert next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])=='4'
assert '4' in r['question'][':question/worked-solution']
print('Source q-139628 is supported with the original matrix and two correct dimension blanks.')
