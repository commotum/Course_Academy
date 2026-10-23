from review_helpers import *
records=read('samples.json')
replay=[]
for r in records:
 m=r['generation']; replay.append({'id':r['question'][':question/id'],'seed':m['seed'],'parameters':m['parameters'],'exact_replay':g.generate('easy',m['seed'],m['template'],m['parameters'])==r})
orig=g.generate;calls=[]
def traced(*args,**kw):
 r=orig(*args,**kw);calls.append(r);return r
g.generate=traced
out=g.batch('easy',5,3334594587)
assert out==records
save('batch-resampling-records.json',calls)
assert all(x['exact_replay'] for x in replay)
assert g.batch('easy',0,11)==[]
try:g.batch('easy',-1,11);raise AssertionError('negative count accepted')
except ValueError:pass
save('changed-path-results.json',{'exact_batch_replay':True,'generation_calls':len(calls),'output_count':len(out),'metadata_replay':replay,'zero_count':True,'negative_count_rejected':True,'ranks_before':[(r['generation'],ranks(r)[1]) for r in calls],'ranks_after':[(r['generation'],ranks(r)[1]) for r in out]})
print('Exact batch regenerated; all effective resampling seeds replay.')
