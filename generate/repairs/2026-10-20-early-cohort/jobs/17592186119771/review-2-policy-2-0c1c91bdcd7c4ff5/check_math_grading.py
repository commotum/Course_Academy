import json,pathlib,re,importlib.util,sys
E=pathlib.Path(__file__).resolve().parent;sys.dont_write_bytecode=True
src=(E/'review_checks.py').read_text().split('manifest=json.load')[0];exec(compile(src,str(E/'review_checks.py'),'exec'))
rs=json.load(open(E/'focused-support-records.json'));results=[]
for r in rs:
 q=r['question'];m=mat(q);exp=label(m);sol=q[':question/worked-solution'];sm=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',sol,re.S);sm=[[int(x.strip()) for x in row.split('&')] for row in sm[1].split(r'\\')];w=re.search(r'_\{(\d)(\d)\}=(-?\d+)',sol)
 good=answer(q)==exp and sm==m and ('it is '+('an ' if exp.startswith('Upper') else 'a ')+exp.lower()+'.') in sol
 if w:
  i,j,v=map(int,w.groups());good=good and m[i-1][j-1]==v!=0 and ((i>j)==exp.startswith('Lower'))
 else:good=good and exp=='Diagonal matrix'
 results.append({'id':q[':question/id'],'expected':exp,'passed':bool(good)})
save('focused-math-results.json',{'count':len(results),'cases':results,'failures':[r for r in results if not r['passed']]});assert all(x['passed'] for x in results)
batch=json.load(open(E/'runner-batch.json'))
def shortcut(r):
 m=mat(r['question']);return 'Diagonal matrix' if len(m)==2 else 'Upper triangular matrix' if m[0][0]<0 else 'Lower triangular matrix'
# Independent controlled irrelevant edit to an actual batch matrix.
before=batch[0];m=mat(before['question']);m[0][0]=-m[0][0];p={'matrix':m,'letter':'C','layout':'bmatrix'};after=g.generate('easy',seed=before['generation']['seed'],parameters=p)
save('batch-shortcut-counterfactual.json',[before,after]);assert answer(before['question'])==answer(after['question'])=='Upper triangular matrix';assert shortcut(before)!=shortcut(after)
checks=json.load(open(E/'grader-input.json'))
for i,r in enumerate([after]+[r for r in rs if len(mat(r['question']))==3 and sum(v!=0 for i,row in enumerate(mat(r['question'])) for j,v in enumerate(row) if i!=j)==1][:7]):
 exp=label(mat(r['question']));checks.append({'label':'sparse-or-sign-control-'+str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==exp else 'rejected','purpose':'independent support classification and rejection of incidental diagonal-sign strategy'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
for i,r in enumerate(batch):
 pred=shortcut(r);f=r['question'][':question/answer-fields'][0];checks.append({'label':'batch-shortcut-'+str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==pred),'expected':'accepted','purpose':'demonstrated incidental size/diagonal-sign answer-producing strategy'}]})
save('grader-input.json',checks)
save('shortcut-results.json',{'rule':'If size is 2 choose Diagonal matrix; otherwise choose Upper triangular matrix when the top-left diagonal entry is negative, and Lower triangular matrix otherwise.','batch':[{'id':r['question'][':question/id'],'matrix':mat(r['question']),'prediction':shortcut(r),'actual':answer(r['question']),'correct':shortcut(r)==answer(r['question'])} for r in batch],'batch_correct':sum(shortcut(r)==answer(r['question']) for r in batch),'batch_total':len(batch),'independent_correct':sum(shortcut(r)==answer(r['question']) for r in json.load(open(E/'independent-records.json'))),'independent_total':30,'counterfactual':'batch-shortcut-counterfactual.json','interpretation':'Batch-selection failure only; no claim this is a universal generator rule. The sign of a diagonal entry does not determine triangularity. Baseline uniform five-label guessing is .2; best constant label in this batch is 2/5.'})
save('render-records.json',batch+json.load(open(E/'counterfactual-records.json'))+[after])
print(json.dumps({'focused_math':len(results),'math_failures':0,'grader_cases':len(checks),'batch_shortcut_correct':5,'batch_shortcut_total':5}))
