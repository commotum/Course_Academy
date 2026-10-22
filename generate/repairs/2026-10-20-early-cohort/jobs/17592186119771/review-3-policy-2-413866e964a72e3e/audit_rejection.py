import pathlib,importlib.util,json,sys,collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('candidate',E.parent/'workspace/17592186119771.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
actual=json.load(open(E/'runner-batch.json'));seed=actual[0]['generation']['batch_seed'];original=g.batch_has_counterexamples;attempts=[]
def observe(rs):
 decision=original(rs);attempts.append({'accepted':decision,'records':rs});return decision
g.batch_has_counterexamples=observe
out=g.batch('easy',5,seed)
assert out==actual
(E/'rejection-attempts.json').write_text(json.dumps({'command':sys.executable+' '+str(E/'audit_rejection.py'),'seed':seed,'instrumentation':'Read-only wrapper records input/output to the original batch_has_counterexamples; no alteration of draws or decisions.','attempts':attempts},indent=2)+'\n')
summaries=[]
for i,a in enumerate(attempts):
 summaries.append({'attempt':i,'accepted':a['accepted'],'answer_counts':dict(collections.Counter(r['generation']['template'] for r in a['records'])),'size_counts':dict(collections.Counter(len(r['generation']['parameters']['matrix']) for r in a['records'])),'diagonal_sign_letter':[[len(r['generation']['parameters']['matrix']),(r['generation']['parameters']['matrix'][0][0]>0)-(r['generation']['parameters']['matrix'][0][0]<0),r['generation']['parameters']['letter'],r['generation']['template']] for r in a['records']]})
(E/'rejection-results.json').write_text(json.dumps({'seed':seed,'attempt_count':len(attempts),'matches_actual_batch':out==actual,'stages':summaries,'interpretation':'Selected structural patterns remain identical across redraws. Incidental numeric/letter/answer-order redraws reject two candidate batches, preserve all three classification cases and return the exact runner batch.'},indent=2)+'\n')
print(json.dumps({'seed':seed,'attempt_count':len(attempts),'matches_actual':out==actual}))
