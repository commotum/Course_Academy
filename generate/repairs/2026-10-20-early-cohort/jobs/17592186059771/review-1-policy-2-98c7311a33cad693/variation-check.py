"""Decision coverage after actual delivery and read-only learner-selection reproduction."""
from independent_helpers import *
import html
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
inv=json.loads((J/'source/inventory.json').read_text())
def question(r):return r.get('question',r)
def classify(r):
 p=question(r)[':question/problem']
 if '\\leftrightarrow' in p or '↔' in p:return 'swap'
 if 'following row operations' in p:
  op=ops(p);return 'shared-target' if op[0][1]==op[1][1] else 'shared-donor'
 return 'scale' if len(re.findall(r'\{R\}',p))==2 else 'addition'
def profile(r):return r.get('generation',{}).get('profile',classify(r))
# Deterministic ties are first stored/displayed option; these are simple cue strategies.
strategies={
 'first_position':lambda ms:0,
 'largest_norm':lambda ms:max(range(5),key=lambda i:sum(abs(v) for row in ms[i] for v in row)),
 'smallest_norm':lambda ms:min(range(5),key=lambda i:sum(abs(v) for row in ms[i] for v in row)),
 'most_zero_entries':lambda ms:max(range(5),key=lambda i:sum(v==0 for row in ms[i] for v in row)),
 'most_unchanged_cells':None,
}
probes=[];stage_results={}
for stage,filename in [('batch_raw','batch-records.json'),('batch_delivered','delivery-batch/accepted.json'),('easy_raw','easy-records.json'),('easy_delivered','delivery-easy/accepted.json'),('moderate_raw','moderate-records.json'),('moderate_delivered','delivery-moderate/accepted.json'),('hard_raw','hard-records.json'),('hard_delivered','delivery-hard/accepted.json')]:
 rs=json.loads((E/filename).read_text());stage_results[stage]={'count':len(rs),'cases':dict(collections.Counter(classify(r) for r in rs)),'profiles':dict(collections.Counter(profile(r) for r in rs))}
 groups=[('overall',rs,'overall')]+[(p,[r for r in rs if profile(r)==p],'within_template') for p in sorted(set(profile(r) for r in rs))]
 for p,group,scope in groups:
  for cue,strategy in strategies.items():
   successes=0;observations=[]
   for r in group:
    q=question(r);choices=q[':question/answer-fields'][0][':answer-field/choices'];ms=[mat(a[':answer/value']) for a in choices]
    if strategy is None:
     original=mat(q[':question/problem']);picked=max(range(5),key=lambda i:sum(a==b for row,orig in zip(ms[i],original) for a,b in zip(row,orig)))
    else:picked=strategy(ms)
    correct=choices[picked][':answer/id']==key(q)[':answer/id'];successes+=correct
    observations.append({'id':q[':question/id'],'chosen_position':picked+1,'correct':correct})
   probes.append({'cue':cue,'subgroup':stage+':'+p,'scope':scope,'correct':successes,'total':len(group),'baseline':.2,'sample_file':filename,'observations':observations})
# Answer-producing actions: ignore the printed pair and always perform a fixed row swap.
for stage,filename in [('batch_raw','batch-records.json'),('batch_delivered','delivery-batch/accepted.json'),('easy_raw','easy-records.json'),('easy_delivered','delivery-easy/accepted.json')]:
 rs=[r for r in json.loads((E/filename).read_text()) if classify(r)=='swap']
 for prof in sorted(set(profile(r) for r in rs)):
  group=[r for r in rs if profile(r)==prof]
  for a,b in [(0,1),(0,2),(1,2)]:
   observations=[]
   for r in group:
    q=question(r);guess=mat(q[':question/problem']);guess[a],guess[b]=guess[b],guess[a]
    observations.append({'id':q[':question/id'],'correct':guess==mat(key(q)[':answer/value'])})
   probes.append({'cue':'always_swap_'+str(a+1)+str(b+1),'subgroup':stage+':'+prof,'scope':'within_template','correct':sum(x['correct'] for x in observations),'total':len(group),'baseline':.2,'sample_file':filename,'observations':observations})
save('shortcut-results.json',{'stages':stage_results,'probes':probes,'comparison':'Uniform guessing among five unique choices: 0.2. Raw bank positions are followed by an additional actual UI reordering. Ties choose first stored/displayed choice.'})
# Faithful translation of select() after usability/freshness filtering; no database writes.
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v
def select(candidates,weights,seed):
 ids=sorted(set(candidates))
 if weights is None:return ids[0] if ids else None
 bands=[[] for _ in range(3)];unrated=[]
 for eid in ids:
  d=enum(candidates[eid].get(':question/difficulty','')).split('/')[-1]
  if d in ['easy','moderate','hard']:bands[['easy','moderate','hard'].index(d)].append(eid)
  else:unrated.append(eid)
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 unit=lambda offset:(int.from_bytes(digest[offset:offset+8],'big')>>11)/(1<<53)
 total=sum(w for b,w in zip(bands,weights) if b)
 if total>0:
  draw=unit(0)*total;chosen=None
  for i,w in enumerate(weights):
   if not bands[i] or w==0:continue
   chosen=i
   if draw<w:break
   draw-=w
  pool=bands[chosen]
 else:pool=unrated
 return pool[int(unit(8)*len(pool))] if pool else None
base={q[':db/id']:q for q in inv['questions']};accepted=json.loads((E/'delivery-batch/accepted.json').read_text())
# Future IDs unknown: explicit surrogate IDs for illustrative future draws only.
prospective={**base,**{max(base)+1+i:question(r) for i,r in enumerate(accepted)}}
selection=[]
for label,pool in [('captured',base),('prospective_surrogate_ids',prospective)]:
 for weights in [[1,0,0],[0,1,0],[0,0,1],[1,1,1],None]:
  # Test fresh, one seen exclusion, exhausted easy band, and repeated stable draws.
  for hist in ['fresh','exclude_one','exclude_easy']:
   seen=set() if hist=='fresh' else {min(pool)} if hist=='exclude_one' else {i for i,q in pool.items() if enum(q[':question/difficulty']).endswith('/easy')}
   available={i:q for i,q in pool.items() if i not in seen};counts=collections.Counter();draws=[]
   for seed in range(128):
    eid=select(available,weights,'review-current/'+str(seed));assert eid not in seen
    assert eid==select(available,weights,'review-current/'+str(seed))
    tag=classify(available[eid]) if eid is not None else 'none';counts[tag]+=1;draws.append({'seed':'review-current/'+str(seed),'entity_id':eid,'case':tag})
   selection.append({'pool':label,'weights':weights,'history_case':hist,'eligible_count':len(available),'counts':dict(counts),'draws':draws})
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs select and seen_before_task','engine_sha256':hashlib.sha256((R/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'basis':inv['basis'],'captured_candidates':[{'entity_id':i,'question_id':q[':question/id'],'case':classify(q),'difficulty':enum(q[':question/difficulty'])} for i,q in base.items()],'prospective_batch_categories':dict(collections.Counter(classify(r) for r in accepted)),'trials':selection,'limits':['Live policy weights and learner histories are absent. All rated bands and zero-weight/exhausted cases tested conditionally; no guarantee of live task order.','Future accepted items lack database IDs; prospective draws use explicit surrogate IDs and do not predict eventual hash positions.','Unconfigured policy uses minimum entity ID. With weighted bands, sorted IDs are uniformly hashed within chosen fresh rated band. Seen questions are excluded before select.','Usability is confirmed for batch by native grading/actual UI; all captured source-bank candidates are treated as usable for this read-only distribution test.']})
# Inventory is inspected for the demonstrated omissions; no existing item proves an omission.
non_source=[q for q in inv['questions'] if ':question/math-academy-id' not in q]
save('inventory-inspection.json',{'basis':inv['basis'],'captured_questions':len(base),'source_bank_questions':len(base)-len(non_source),'non_source_questions':len(non_source),'non_source_keys':sorted(set(k for q in non_source for k in q)),'generation_metadata_present':any('generation' in k for q in non_source for k in q),'question_ids':[q[':question/id'] for q in non_source],'assessment':'Prior demonstrated findings are absent construction/replay families, now repaired; they do not establish erroneous stored items. No new item defect demonstrated. Inventory questions inspected for identity/difficulty/operation-family distribution; no claim of complete math/grading verification of non-source inventory. Capture lacks original generation metadata, so matching regeneration of existing non-source questions is untested.'})
save('affected-inventory.json',{'affected_questions':[]})
# Parse actual rendered radio ordering instead of assuming the generator bank order.
class Radios(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='input' and a.get('type')=='radio':self.ids.append(a.get('value'))
def rendered_matrices(fragment):
 out=[]
 for fragment in re.findall(r'<mjx-assistive-mml[^>]*>(.*?)</mjx-assistive-mml>',fragment,re.S):
  root=ET.fromstring(fragment); ns={'m':'http://www.w3.org/1998/Math/MathML'}
  for table in root.findall('.//m:mtable',ns):
   rows=table.findall('m:mtr',ns)
   if len(rows)!=3 or any(len(row.findall('m:mtd',ns))!=3 for row in rows):continue
   try:out.append([[F(''.join(cell.itertext()).replace('−','-')) for cell in row.findall('m:mtd',ns)] for row in rows])
   except ValueError:pass # expanded expressions verified exactly in math-results and inspected visually
 return out
rendered=[]
for directory in ['render-batch','render-changed']:
 records=json.loads((E/directory/'input.json').read_text())
 report=json.loads((E/directory/'rendering.json').read_text())
 for n,r in enumerate(records[:len(report['cases'])]):
  p=Radios();p.feed((E/directory/f'question-{n+1:03}.html').read_text());q=question(r)
  assert len(p.ids)==5 and len(set(p.ids))==5,(directory,n,p.ids)
  by_id={a[':answer/id']:a for a in q[':question/answer-fields'][0][':answer-field/choices']}
  assert set(p.ids)==set(by_id)
  pos=p.ids.index(key(q)[':answer/id'])+1
  body=(E/directory/f'question-{n+1:03}.html').read_text()
  labels=re.findall(r'<label class="choice">(.*?)</label>',body,re.S)
  visible=[rendered_matrices(label)[0] for label in labels]
  assert visible==[mat(by_id[i][':answer/value']) for i in p.ids]
  matrices=rendered_matrices(body)
  assert matrices[0]==mat(q[':question/problem']) and matrices[-1]==calc(q)
  rendered.append({'file':directory+f'/question-{n+1:03}.html','record_file':directory+'/input.json','index':n,'profile':profile(r),'display_order':p.ids,'correct_display_position':pos,'rendered_matrices_match_choices':visible==[mat(by_id[i][':answer/value']) for i in p.ids],'rendered_prompt_matrix_correct':matrices[0]==mat(q[':question/problem']),'rendered_solution_final_correct':matrices[-1]==calc(q)})
save('rendered-choice-results.json',{'cases':rendered,'batch_positions':[r['correct_display_position'] for r in rendered if r['file'].startswith('render-batch/')],'limits':'Preview activity IDs determine actual deterministic UI order; eventual live item IDs can change that order.'})
print(json.dumps({'stages':stage_results,'batch_perfect_cues':[{k:v for k,v in p.items() if k!='observations'} for p in probes if p['subgroup'].startswith('batch_delivered') and p['correct']==p['total']],'rendered_cases':len(rendered),'batch_display_positions':[r['correct_display_position'] for r in rendered if r['file'].startswith('render-batch/')],'inventory_non_source':len(non_source)}))
