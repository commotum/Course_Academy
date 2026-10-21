"""Strict regression: every captured bank profile must be replayable in full."""
import sys,json,pathlib,re
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;sys.path.insert(0,str(J/'workspace'));import generator as g
source=json.load(open(J/'source/source.json'))
for q in source['material']['kp'][':knowledge-point/questions']:
 p=q[':question/problem'];body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',p,re.S)[1]
 m=[[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\')]
 rows=[int(n)-1 for n in re.findall(r'\$(\d)\$(?:st|nd|rd|th)',p.split('rows')[0])]
 try:r=g.generate(seed=817,profile=q[':question/math-academy-id'],parameters={'matrix':m,'rows':rows},replay=True)
 except Exception as ex:raise AssertionError(f"Source {q[':question/id']} ({q[':question/math-academy-id']}) cannot replay: {ex}") from ex
 bank=lambda field:sorted(int(a[':answer/value']) for a in field[':answer-field/choices'])
 assert bank(r['question'][':question/answer-fields'][0])==bank(q[':question/answer-fields'][0])
print('All captured source banks replay.')
