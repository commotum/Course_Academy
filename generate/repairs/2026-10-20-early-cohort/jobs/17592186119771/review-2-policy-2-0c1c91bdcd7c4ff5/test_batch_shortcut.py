"""Strict acceptance check for the demonstrated batch-only incidental cue.
Run with an optional JSON-array path to test replacement delivery records.
"""
import json,pathlib,re,sys
E=pathlib.Path(__file__).resolve().parent
path=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else E/'batch-delivery/accepted.json'
records=json.load(open(path))
def prediction(r):
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',r['question'][':question/problem'],re.S)[1]
 m=[[int(v.strip()) for v in row.split('&')] for row in body.split(r'\\')]
 return 'Diagonal matrix' if len(m)==2 else 'Upper triangular matrix' if m[0][0]<0 else 'Lower triangular matrix'
def answer(r):
 f=r['question'][':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[1] if isinstance(c,list) else c[':answer/id']
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
hits=sum(prediction(r)==answer(r) for r in records)
print(json.dumps({'input':str(path),'correct':hits,'total':len(records),'rule':'2x2 => diagonal; else top-left negative => upper; else lower'}))
assert hits<len(records),'Incidental size/diagonal-sign rule answers every delivered member; revise batch selection.'
