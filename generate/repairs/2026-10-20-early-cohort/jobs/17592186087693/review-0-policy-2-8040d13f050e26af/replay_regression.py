"""Strict source coverage acceptance test; exits nonzero on the current omission."""
import argparse,sys,pathlib,json,re
p=argparse.ArgumentParser();p.add_argument('--package',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent/'workspace');a=p.parse_args()
sys.dont_write_bytecode=True;sys.path.insert(0,str(a.package.resolve()));import generator
source=json.loads((pathlib.Path(__file__).resolve().parent.parent/'source/source.json').read_text())
q=next(q for q in source['material']['kp'][':knowledge-point/questions'] if q[':question/math-academy-id']=='q-139628')
rec=generator.generate(seed=0,profile='observed-q-139628')
fs={f[':answer-field/key']:f for f in rec['question'][':question/answer-fields']}
assert set(fs)=={'field-1','field-2'}
for f in fs.values():
 cid=f[':answer-field/correct'][1]
 assert next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==cid)=='4'
body=lambda p:re.sub(r'\s','',re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',p,re.S)[1])
assert body(q[':question/problem'])==body(rec['question'][':question/problem'])
assert 'Chelsea' in rec['question'][':question/problem'], 'Preserve supported source stem or explicitly document its correction.'
print('q-139628 supported replay passed')
