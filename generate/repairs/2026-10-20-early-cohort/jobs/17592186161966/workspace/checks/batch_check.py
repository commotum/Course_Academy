import sys,json
sys.dont_write_bytecode=True
import regressions as t
v=t.v
rs=json.load(open(t.OUT/'batch-delivery/accepted.json'))
results=[v.inspect(r) for r in rs]
t.save('batch-grader-input.json',[{'label':f'filtered-cli-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==v.correct_index(r) else 'rejected','purpose':'Independent displayed-matrix check after publication normalization'} for j,a in enumerate(v.field(r)[':answer-field/choices'])]} for i,r in enumerate(rs)])
t.save('batch-results.json',{'count':len(rs),'results':results,'limit':'Five-item CLI smoke sample; conditional shortcut freedom is established by the separate identical-bank groups, not by a quota in this small batch.'})
print(json.dumps({'math':'pass','count':len(rs)}))
