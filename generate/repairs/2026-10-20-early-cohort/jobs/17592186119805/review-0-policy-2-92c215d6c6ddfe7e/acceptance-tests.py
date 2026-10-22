"""Strict retained counterexamples. Exit 1 means demonstrated failures remain."""
exec(compile(open('audit.py').read().split('records=[];domain_report=[]')[0],'audit.py','exec'))
checks=[]
# The ordinary sampler must not make an incidental cue perfectly answer its subgroup.
for sid in g.LEVELS['easy']:
 rows=[g.generate('easy',seed,sid) for seed in [11027,84533,230219,330721,984311,1234579]]
 successes=sum(shortcut(r['question'])[0]==key(r['question']) for r in rows)
 checks.append({'case':'vector-blind shortcut '+sid,'passed':successes<len(rows),'successes':successes,'attempts':len(rows)})
# Source families: future repair may rename profile IDs, but must offer equivalent replay.
for sid in ['q-34572','q-105153','q-105156']:
 checks.append({'case':'complete source replay profile '+sid,'passed':sid in g.PROFILES})
p=copy.deepcopy(g.CASES['q-34570']);p['u'][0]=1
try:
 r=g.generate('moderate',64193,'q-34570',p);ok=scalar(key(r['question']))==-6
except Exception:ok=False
checks.append({'case':'consistent homogeneous counterfactual 3[2,4]+k[1,2]=0','passed':ok,'expected':'-6 or supported same-skill replay with justified difficulty; never silently forbid this decision case'})
p=copy.deepcopy(g.CASES['q-34241']);p['c']=2
try:
 r=g.generate('easy',64193,'q-34241',p);ans,_=solve(r['question']);ok=(key(r['question'])==ans if ans=='No solution' else scalar(key(r['question']))==ans)
except (AssertionError,ValueError):ok=True
checks.append({'case':'subtraction c=2 is rejected or accurately rendered and keyed','passed':ok})
save('acceptance-results.json',{'checks':checks,'passed':all(x['passed'] for x in checks)})
print(json.dumps({'passed':all(x['passed'] for x in checks),'failures':[x['case'] for x in checks if not x['passed']]}))
raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
