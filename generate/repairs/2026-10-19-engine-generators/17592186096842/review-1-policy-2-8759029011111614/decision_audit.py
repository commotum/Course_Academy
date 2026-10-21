from audit import *
from collections import Counter,defaultdict
raw=json.loads(Path('samples-moderate.json').read_text());post=json.loads(Path('delivery-independent/accepted.json').read_text());runner=json.loads(Path('runner-batch.json').read_text());runnerpost=json.loads(Path('delivery-runner/accepted.json').read_text());allraw=json.loads(Path('samples.json').read_text());cf=json.loads(Path('counterfactual-records.json').read_text())
# Surface-only strategies: first, last, shortest/longest text, numeric rank after a common valid x.
def probe(records,label,ref):
 groups=defaultdict(list)
 for r in records:
  if field(r)[':answer-field/type'].endswith('/radio'):groups[r['generation']['template']].append(r)
 out=[]
 for name,rs in [('ALL',sum(groups.values(),[]))]+list(groups.items()):
  if not rs:continue
  strategies={'first':0,'last':0,'shortest TeX':0,'longest TeX':0,'numeric median':0}
  for r in rs:
   choices=field(r)[':answer-field/choices'];cid=field(r)[':answer-field/correct'][1]
   # numeric ranking is a cue probe, not a claim students can evaluate symbolic expressions without work
   vals=[untex(a[':answer/value']) for a in choices];point=0
   for point in [0,1,-1,2,-2,7,-7,19,-19]:
    vs=[v.subs(x,point) for v in vals]
    if all(v.is_real and v.is_finite for v in vs):break
   picks=[0,len(choices)-1,min(range(5),key=lambda i:len(choices[i][':answer/value'])),max(range(5),key=lambda i:len(choices[i][':answer/value'])),sorted(range(5),key=lambda i:float(vs[i]))[2]]
   for strategy,i in zip(strategies,picks):strategies[strategy]+=choices[i][':answer/id']==cid
  for strategy,hit in strategies.items():out.append({'stage':label,'cue':strategy,'subgroup':name,'scope':'overall' if name=='ALL' else 'within_template','strategy':'Choose '+strategy+' option, tie broken by first displayed','correct':hit,'total':len(rs),'baseline':.2,'disposition':'defect' if hit==len(rs) and len(rs)>=10 else 'not_predictive','conclusion':f'{hit}/{len(rs)} versus 1/5 uniform radio chance. '+('Perfect repeatable candidate predictor requires inspection.' if hit==len(rs) and len(rs)>=10 else 'No perfect cue in this bounded subgroup; small samples do not estimate a reliable long-run advantage.'),'sample_refs':[ref]})
 return out
probes=probe(allraw,'raw all bands','samples.json')+probe(post,'post delivery moderate','delivery-independent/accepted.json')+probe(runnerpost,'runner post delivery','delivery-runner/accepted.json')
save('shortcut-results.json',probes)
# Prepare an exact native in-memory selection snapshot from captured and accepted records.
inv=json.loads((ROOT.parent/'source/inventory.json').read_text());entities={};qids=[];inventoryids=[];mapping={};n=800000000

def enum(v):return v.get(':db/ident') if isinstance(v,dict) else v
for j,(kind,q,r) in enumerate([('inventory',q,None) for q in inv['questions']]+[('fresh',r['question'],r) for r in post]+[('runner',r['question'],r) for r in runnerpost]):
 qid=q.get(':db/id',900000000+j);qids.append(qid)
 if kind=='inventory':inventoryids.append(qid)
 fields=[]
 for f in q[':question/answer-fields']:
  n+=1;fid=n;fields.append(fid);ids=[];uuids={}
  for a in f[':answer-field/choices']:
   n+=1;ids.append(n);uuids[a[':answer/id']]=n;entities[n]={'answer/type':enum(a[':answer/type']).lstrip(':'),'answer/value':a[':answer/value']}
  c=f.get(':answer-field/correct');cid=c.get(':answer/id') if isinstance(c,dict) else c[1] if isinstance(c,list) else None
  entities[fid]={'answer-field/type':enum(f[':answer-field/type']).lstrip(':'),'answer-field/key':f[':answer-field/key'],'answer-field/choices':ids}
  if cid:entities[fid]['answer-field/correct']=uuids[cid]
 entities[qid]={'question/id':q[':question/id'],'question/problem':q[':question/problem'],'question/answer-fields':fields}
 if ':question/difficulty' in q:entities[qid]['question/difficulty']=enum(q[':question/difficulty']).lstrip(':')
 mapping[qid]={'kind':kind,'uuid':q[':question/id'],'template':r['generation']['template'] if r else q.get(':question/math-academy-id'),'a':r['generation']['parameters']['a'] if r else None}
for i,name in enumerate(['answer-field.type/radio','answer-field.type/blank','answer.type/math','question.difficulty/easy','question.difficulty/moderate','question.difficulty/hard'],1):entities[i]={'db/ident':name}
save('selection-input.json',{'entities':entities,'question_ids':qids,'inventory_ids':inventoryids});save('selection-map.json',mapping)
# Add controlled cross-grades to the previously collected native batch; regenerate one complete result.
gcases=json.loads(Path('grader-input.json').read_text())
for i,j in [(4,5),(5,4),(5,6),(6,5),(4,6),(6,4)]:
 gcases.append({'label':f'fixed-curve target {cf[i]["generation"]["parameters"]["t"]} rejects response for target {cf[j]["generation"]["parameters"]["t"]}','record':cf[i],'checks':[{'submitted':correct(cf[j]),'expected':'rejected','purpose':'changing only requested target changes actual learner outcome'}]})
save('grader-input.json',gcases)
# Record all commands rather than reconstructing them from tool logs.
commands=['PYTHON='+PY,'PYTHONDONTWRITEBYTECODE=1 '+PY+' -B audit.py',PY+' -B followup.py','python3 collect_native.py',PY+' -B decision_audit.py','./check-engine-collect grader-input.json grader-results.json',PY+' -B '+str(REPO/'generate/pipeline/check_delivery.py')+' --input samples-moderate.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output delivery-independent --asset-root ../workspace --math-root /media/jake/SSD/EDB/math',PY+' -B '+str(REPO/'generate/pipeline/check_delivery.py')+' --input ../samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output delivery-runner --asset-root ../workspace --math-root /media/jake/SSD/EDB/math',PY+' -B '+str(REPO/'generate/pipeline/render_preview.py')+' --input render-records.json --output render-all --asset-root ../workspace --math-root /media/jake/SSD/EDB/math --limit 19']
Path('commands.txt').write_text('\n'.join(commands)+'\n')
print('probes',len(probes),'perfect candidates',[(p['stage'],p['subgroup'],p['cue']) for p in probes if p['disposition']=='defect'])
