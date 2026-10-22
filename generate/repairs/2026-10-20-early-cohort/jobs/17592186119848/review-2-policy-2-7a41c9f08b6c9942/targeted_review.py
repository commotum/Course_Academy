"""Targeted independent sampler regression. Run with repo .venv/bin/python -B."""
import sys,json,importlib.util,hashlib,subprocess,random,collections
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';R=Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(W));s=importlib.util.spec_from_file_location('g',W/'17592186119848.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
from audit_delivery import info,matrices,rank
load=lambda p:json.loads(Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def group(r):
 x=info(r)
 return (x['profile'],x['target'],tuple(sorted(tuple(v) for v in x['shapes'].values())),tuple(x['excluded']),len(r['question'][':question/answer-fields']),r['generation']['choice_profile'])
def audit(rs):
 groups=collections.defaultdict(list)
 for r in rs:groups[group(r)].append(info(r))
 results=[]
 for k,rows in groups.items():
  forced=[lab for lab in rows[0]['eligible'] if len({lab in row['matches'] for row in rows})==1]
  results.append({'group':str(k),'count':len(rows),'truths':[x['matches'] for x in rows],'forced_labels':forced,'singleton':len(rows)==1,'failed':len(rows)>1 and bool(forced)})
 return {'groups':results,'failures':[r for r in results if r['failed']]}
cat=g.catalog();capacity=len({r['generation']['mathematical_fingerprint'] for r in cat});runs=[];allrecords=[]
# Small fresh seed controls, count edges, capacity and overcapacity. Catalog construction is unchanged.
for seed,count in [(1763,5),(5281,5),(14653,5),(62003,2),(91283,3),(134669,4),(5281,0),(1763,1),(5281,capacity)]:
 rows=g.batch('easy',count,seed);a=audit(rows);assert not a['failures'],(seed,count,a)
 assert len(rows)==count and len({r['generation']['mathematical_fingerprint'] for r in rows})==count
 assert rows==g.batch('easy',count,seed)
 runs.append({'seed':seed,'count':count,'audit':a,'record_ids':[r['question'][':question/id'] for r in rows]});allrecords.extend(rows)
# Exact prefix from prior independent failure with current constructor.
old=load(E/'previous-batch.json');oldids=[r['question'][':question/id'] for r in old]
def shuffle(_rng,rows):
 indexed={r['question'][':question/id']:r for r in rows};rows[:]=[indexed[k] for k in oldids]+[r for r in rows if r['question'][':question/id'] not in oldids]
with patch.object(g.random.Random,'shuffle',shuffle):repaired=g.batch('easy',5,0)
assert not audit(repaired)['failures'];assert all(r in cat for r in old)
save('exact-prefix-repaired.json',repaired)
controls=[g.generate('easy',38117,'q-139965',{'matches':m,'assignment':['C','A','B'],'scale':sc}) for m,sc in [(['A'],2),(['C'],2),(['A','C'],2),(['C'],1)]]
save('targeted-counterfactual-records.json',controls)
ms=[matrices(r['question']) for r in controls];assert all(m['B']==ms[0]['B'] for m in ms[:3]);assert all(tuple(info(r)['matches'])==tuple(m) for r,m in zip(controls,[['A'],['C'],['A','C'],['C']]))
assert all(ms[1][k]==[[2*v for v in row] for row in ms[3][k]] for k in 'ABC')
checks=[]
from review_helpers import expected
for label,rows in [('counterfactual',controls),('sampler',allrecords),('old-prefix',old),('repaired-prefix',repaired)]:
 for rec in rows:
  q=rec['question'];cs=[]
  for fi,f in enumerate(q[':question/answer-fields']):
   good=expected(q,f)
   for a in f[':answer-field/choices']:cs.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a in good else 'rejected','purpose':'Exact Fraction elimination from visible matrices'})
  checks.append({'label':label,'record':rec,'checks':cs})
save('targeted-grader-input.json',checks)
save('targeted-sampler-records.json',allrecords)
save('targeted-results.json',{'command':str(R/'.venv/bin/python')+' -B targeted_review.py','capacity':capacity,'fresh_runs':runs,'old_audit':audit(old),'current_audit':audit(load(E/'batch.json')),'exact_prefix_repaired':audit(repaired),'counterfactuals':{'relevant':{'params':'q-139965 seed38117 assignment[C,A,B],scale2, matches A / C / AC','excluded_B_unchanged':True,'shape_preservation':all({k:len(m[k]) for k in m}=={k:len(ms[0][k]) for k in ms[0]} for m in ms[:3]),'prompt_changed':controls[0]['question'][':question/problem']!=controls[1]['question'][':question/problem'],'solution_changed':controls[0]['question'][':question/worked-solution']!=controls[1]['question'][':question/worked-solution']},'irrelevant':{'change':'scale2 to scale1 on C-only','rank_preserved':True,'solution_preserved':controls[1]['question'][':question/worked-solution']==controls[3]['question'][':question/worked-solution']}}})
save('render-records.json',load(E/'batch.json')+controls+load(E/'counterfactual-records.json'))
(E/'session-state.md').write_text('Completed old failure reproduction, current batch pass, exact prefix repair, fresh sampler count/seed controls and independent math checks. Native main grader 337 checks passed. Delivery batch5/5, catalog39/39, fresh5/6 (one duplicate). Next targeted grader, actual UI inspection, evidence reports.\n')
print(json.dumps({'sampler_runs':len(runs),'capacity':capacity,'counterfactuals':len(controls),'grader_cases':len(checks),'prior_failure':len(audit(old)['failures']),'current_failures':len(audit(load(E/'batch.json'))['failures'])}))
