import sys,pathlib,json,collections,math
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(E.parent/'workspace'));import generator as g
rs=[g.generate('moderate',s) for s in range(932611,932707)]
(E/'cue-control-records.json').write_text(json.dumps(rs,indent=2)+'\n')
out=[]
for label,rr in [('control all',rs),('control existing zero row',[r for r in rs if any(not any(row) for row in r['generation']['parameters']['matrix'])]),('control no zero row',[r for r in rs if all(any(row) for row in r['generation']['parameters']['matrix'])]),('initial',json.load(open(E/'independent-samples.json'))),('exact batch',json.load(open(E/'batch-records.json')))]:
 ranks=[]
 for r in rr:
  f=r['question'][':question/answer-fields'][0];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]);bank=r['generation']['parameters']['bank'];ranks.append(sorted(range(5),key=lambda i:bank[i]).index(ci))
 out.append({'group':label,'n':len(rr),'lex_ranks':dict(collections.Counter(ranks)),'median_hits':ranks.count(2),'binomial_uniform_tail':sum(math.comb(len(rr),k)*.2**k*.8**(len(rr)-k) for k in range(ranks.count(2),len(rr)+1))})
(E/'cue-control-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
