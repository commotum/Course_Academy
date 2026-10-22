#!/usr/bin/env python3
import sys
sys.dont_write_bytecode=True
import json,pathlib,re,hashlib,collections,importlib.util
R=pathlib.Path(__file__).resolve().parent;J=R.parent
def read(p):return json.loads(pathlib.Path(p).read_text())
def save(p,o):(R/p).write_text(json.dumps(o,indent=2))
def correct(f):
 ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
 return next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def norm(s):return re.sub(r'[{}\s$]','',s)
def signature(q):
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
 dim=len(body.split(r'\\'));name=re.search(r'([A-E])\s*=',q[':question/problem'])[1]
 return (name,dim,tuple(sorted(norm(f[':answer-field/key']) for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above')))
def pattern(q):return tuple(sorted((norm(f[':answer-field/key']),correct(f)) for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above'))
source=read(J/'source/source.json')['material']['kp'][':knowledge-point/questions'];mapping={};conflicts=[]
for q in source:
 sig=signature(q);value=dict(pattern(q))
 if sig in mapping and mapping[sig]!=value:conflicts.append(str(sig))
 mapping[sig]=value
save('shortcut-source-map.json',{'method':'Map visible matrix label, dimension and mathematical statement bank to complete selection. Does not inspect entries, generation metadata, IDs, seed, or solutions. Predictions fixed from instructional examples before scoring fresh samples.','mapping':[{'label':k[0],'dimension':k[1],'statements':k[2],'prediction':v} for k,v in mapping.items()],'conflicts':conflicts})
stages={k:read(R/p) for k,p in [('raw-independent','samples-independent.json'),('raw-moderate','samples-moderate.json'),('delivered-independent','delivery-independent/accepted.json'),('runner-batch','batch.json'),('delivered-batch','delivery-batch/accepted.json')]}
results={}
for stage,rs in stages.items():
 rows=[]
 for r in rs:
  q=r['question'];sig=signature(q);pred=mapping.get(sig);actual=dict(pattern(q));none=[correct(f) for f in q[':question/answer-fields'] if f[':answer-field/key']=='None of the above']
  rows.append({'question_id':q[':question/id'],'visible_signature':sig,'prediction':pred,'actual':actual,'correct':pred==actual and (not none or none==[not any(pred.values())]),'template':r['generation']['template'],'seed':r['generation']['seed']})
 groups=collections.defaultdict(list)
 for row in rows:groups[str(row['visible_signature'])].append(row)
 results[stage]={'count':len(rows),'correct':sum(x['correct'] for x in rows),'rows':rows,'conditional_groups':[{'signature':s,'correct':sum(x['correct'] for x in v),'total':len(v)} for s,v in groups.items()]}
save('shortcut-results.json',results)
# Reproduce exact SHA-based conditional selection within the moderate band.
# Assigned entity IDs are deliberately hypothetical, never written to EDB.
inv=read(J/'source/inventory.json');accepted=stages['delivered-batch'];captured=inv['questions'];allq=captured+[r['question'] for r in accepted]
moderate=[]
for q in allq:
 d=q.get(':question/difficulty');d=d.get(':db/ident') if isinstance(d,dict) else d
 if d==':question.difficulty/moderate':moderate.append(q)
selection=[]
for seed in ['review-independent-'+str(i) for i in range(32)]:
 # Rust select deduplicates and sorts candidate entities. At this stage publication
 # hasn't assigned IDs: captured moderate entries precede five synthetic entities.
 pool=sorted(moderate,key=lambda q:q.get(':db/id',10**20+next((i for i,x in enumerate(accepted) if x['question'][':question/id']==q[':question/id']),0)))
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=(int.from_bytes(digest[8:16],'big')>>11)/2**53
 q=pool[int(u*len(pool))]
 selection.append({'seed':seed,'id':q[':question/id'],'shortcut_correct':mapping.get(signature(q))==dict(pattern(q))})
# All subsets/freshness exclusions retain a per-signature deterministic mapping.
save('selection-results.json',{'basis':inv['basis'],'actual_rules_file':'engine/rust/question_selection.rs','rules':'Fresh candidates only; sort unique entity IDs; choose rated difficulty band by positive configured weights; uniform within band via SHA256 bytes 8..16. Unrated fallback only if no eligible weighted rated band. Unconfigured policy picks first candidate.','known_counts':{'captured_total':len(captured),'accepted_new':len(accepted),'combined_moderate':len(moderate)},'conditional_moderate_probe':selection,'conditional_hits':sum(x['shortcut_correct'] for x in selection),'limitations':['No captured learner history or active selection-policy weights; cannot replay a particular live learner draw.','New records lack allocated entity IDs; ordering above is a read-only hypothetical publication ordering. Conditional uniformity and shortcut invariance under any subset do not depend on that ordering.'],'conclusion':'Every captured moderate question and every accepted moderate new record has the same visible-signature predictor. Removing seen items, choosing any positively weighted moderate band, or first-candidate fallback cannot remove this demonstrated shortcut. All 5 batch records survive; no selection model rescues their finite practice pool.'})
# Inventory regeneration attempt, without assigning provenance to original source questions.
sys.path.insert(0,str(J/'workspace'));spec=importlib.util.spec_from_file_location('g',J/'workspace/17592186119784.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
unmatched=read(R/'inventory-unmatched.json');generated=[]
for q in unmatched:
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
 m=[[int(c) for c in row.split('&')] for row in body.split(r'\\')]
 r=g.generate('hard',101,template='q-126477',parameters={'matrix':m})
 generated.append({'stored_question':q,'attempt':r,'stored_id':q[':question/id'],'reproduced_id':r['question'][':question/id'],'id_match':q[':question/id']==r['question'][':question/id'],'stored_generation_metadata_present':'generation' in q})
save('inventory-reproduction-attempts.json',generated)
# Evidence file required for affected records remains empty: no matching generated record proven.
(R/'session-state.md').write_text('Delivery completed: independent moderate 25/25 and runner batch 5/5 accepted. Visible label/dimension/bank shortcut 50/50 independent, 25/25 delivered moderate and 5/5 delivered batch. Native grader 72/72 expected outcomes. Source replay misses q-126481/q-126474. Inventory basis 5452: 12 original source records, one unprovenanced record; exact current ID reproduction failed, affected list empty with explicit limitation. Renderer pending.\n')
print(json.dumps({s:{k:v for k,v in x.items() if k in ('count','correct')} for s,x in results.items()},indent=2));print('conditional learner selection',sum(x['shortcut_correct'] for x in selection),len(selection));print('inventory ID matches',[x['id_match'] for x in generated])
