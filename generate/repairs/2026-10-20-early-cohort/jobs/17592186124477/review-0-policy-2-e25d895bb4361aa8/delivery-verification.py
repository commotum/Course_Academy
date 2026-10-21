#!/usr/bin/env python3
"""Independent keys and native grader inputs after actual delivery normalization."""
import json,pathlib,re
E=pathlib.Path(__file__).resolve().parent
def load(p):return json.loads((E/p).read_text())
def save(p,x):(E/p).write_text(json.dumps(x,indent=2)+'\n')
def target(q):
    body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
    a=[[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\')]
    return tuple(next(i+1 for i,x in enumerate(row) if x) for row in a if any(row)),len(a[0])
def cols(s,n):return tuple(range(1,n+1)) if s=='All the columns are pivot' else tuple(map(int,re.findall(r'\$(\d+)\$(?:st|nd|rd|th)',s)))
results=[];grader=load('grader-input.json')
# Idempotent: retain original test cases, replace earlier delivered cases.
grader=[x for x in grader if not x['label'].startswith('delivered-')]
for dataset in ['delivery-batch/accepted.json','delivery-independent/accepted.json']:
    for index,r in enumerate(load(dataset)):
        q=r['question'];wanted,n=target(q);selected=[];checks=[]
        for fi,f in enumerate(q[':question/answer-fields']):
            correct=f[':answer-field/correct'][1];cv=next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==correct)
            if f[':answer-field/type'].endswith('/checkbox'):
                col=int(re.match(r'Column (\d+):',f[':answer-field/key'])[1])
                if cv=='true':selected.append(col)
                good=lambda c:(c[':answer/value']=='true')==(col in wanted)
            else:
                selected=list(cols(cv,n));good=lambda c:cols(c[':answer/value'],n)==wanted
            for c in f[':answer-field/choices']:
                checks.append({'field_index':fi,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if good(c) else 'rejected','purpose':'Independent visible-matrix answer after publisher normalization and stable-identity remapping'})
        assert tuple(selected)==wanted,(q[':question/id'],selected,wanted)
        results.append({'dataset':dataset,'id':q[':question/id'],'selected':selected,'passed':True})
        if dataset.startswith('delivery-batch/'):
            grader.append({'label':f'delivered-batch-{index}','record':r,'checks':checks})
save('delivery-math-results.json',{'count':len(results),'failures':[],'cases':results})
save('grader-input.json',grader)
print(json.dumps({'independent_delivered_key_checks':len(results),'batched_native_grader_cases':len(grader)}))
