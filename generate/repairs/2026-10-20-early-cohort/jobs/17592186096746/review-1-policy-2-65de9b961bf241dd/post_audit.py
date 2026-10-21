import sys, json, collections, hashlib, copy, importlib.util, re
sys.dont_write_bytecode=True
import review as t
from shortcut import measure,sign_strategy
E=t.E;J=t.J;W=t.W;save=t.save

def field(r):return r['question'][':question/answer-fields'][0]
def key(r):return field(r)[':answer-field/correct'][1]
def triples(r):
 if r['question'][':question/difficulty']==':question.difficulty/easy':return [t.matrix(a[':answer/value'])[0][1:] for a in field(r)[':answer-field/choices']]
 return [[-v[1],-v[2],v[3]] for a in field(r)[':answer-field/choices'] for v in [t.vector_parts(a[':answer/value'])[0]]]
def profile(r):
 vs=triples(r);vary=[j for j in range(3) if len({v[j] for v in vs})>1];return 'all' if len(vary)==3 else ('b','c','d')[vary[0]]
def sign(v):return (v>0)-(v<0)
def sign_candidates(r):
 row=t.equations(r['question'][':question/problem'])[0];want=[sign(v)*sign(row[0]) for v in row[1:]]
 return [i for i,vs in enumerate(triples(r)) if [sign(v) for v in vs]==want]
def probes(rs,name,ref):
 rows=[];groups={'overall':rs}
 for r in rs:
  band=r['question'][':question/difficulty'].split('/')[-1];p=profile(r);eq=t.equations(r['question'][':question/problem']);unit=any(row[0]==1 for row in eq)
  groups.setdefault('profile/'+band+'/'+p,[]).append(r)
  groups.setdefault('profile-pivot/'+band+'/'+p+'/'+str(sign(eq[0][0])),[]).append(r)
  groups.setdefault('unit-row/'+str(unit),[]).append(r)
 for group,sub in groups.items():
  strategies={**{'position-'+str(i+1):lambda r,i=i:i for i in range(5)},'unique-signs':lambda r:sign_candidates(r)[0] if len(sign_candidates(r))==1 else None,'signs-first-tie':lambda r:sign_candidates(r)[0] if sign_candidates(r) else None}
  for rank in range(5):
   def by_rank(r,rank=rank):
    vs=triples(r);j=next(j for j in range(3) if len({v[j] for v in vs})>1)
    return sorted(range(5),key=lambda i:abs(vs[i][j]))[rank]
   strategies['magnitude-rank-'+str(rank+1)]=by_rank
  # Raw first row copying ignores required normalization; unit-row matching is an intended simplification.
  def rawcopy(r):
   raw=t.equations(r['question'][':question/problem'])[0];vs=triples(r);hits=[i for i,v in enumerate(vs) if v==raw[1:]]
   return hits[0] if raw[0]==1 and len(hits)==1 else None
  strategies['copy-first-raw-row']=rawcopy
  for strategy,fn in strategies.items():
   outcomes=[]
   for r in sub:
    guess=fn(r);ci=next(i for i,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==key(r));outcomes.append({'id':r['question'][':question/id'],'guess_index':guess,'correct_index':ci,'correct':guess==ci})
   n=sum(x['correct'] for x in outcomes);rows.append({'set':name,'subgroup':group,'strategy':strategy,'correct':n,'total':len(sub),'baseline':0.2,'outcomes':outcomes,'sample_ref':ref})
 return rows

sets={'batch':json.load(open(E/'batch.json')),'fresh-easy':json.load(open(E/'fresh-easy.json')),'fresh-moderate':json.load(open(E/'fresh-moderate.json')),'delivered-batch':json.load(open(E/'delivery-batch/accepted.json')),'delivered-fresh':json.load(open(E/'delivery-fresh/accepted.json'))}
refs={'batch':'batch.json','fresh-easy':'fresh-easy.json','fresh-moderate':'fresh-moderate.json','delivered-batch':'delivery-batch/accepted.json','delivered-fresh':'delivery-fresh/accepted.json'}
rows=[]
for name,rs in sets.items():rows+=probes(rs,name,refs[name])
save('shortcut-results.json',{'command':str(t.PY)+' '+str(E/'post_audit.py'),'rules':'Strategies pre-defined using position, signs, smallest/middle/largest magnitudes or raw copying, evaluated overall, per visible differing-coordinate template, per first-pivot sign and per presence of unit row. Magnitude rank uses choices only; it never reads input coefficient magnitudes. Unknown prediction counts as wrong. Chance baseline is 1/5. Exact batch assessed separately; singleton conditional hits are descriptive, not a learned reliable predictor.','results':rows,'construction_analysis':'correct_index is drawn from all five before independently sampling distinct candidate magnitudes, signs and row scales. Fixed-bank tests rotate every candidate through correctness for each template and band. No tested incidental cue determines the response family-wide. First/second/third-row unit copying is mathematical use of an already normalized source row, not a defect.'})
# Actual renderer choice ordering differs from raw bank order: inspect saved DOM.
ui=[]
for folder in ('render','render-extra'):
 report=json.load(open(E/folder/'rendering.json'));records=json.load(open(E/('render-records.json' if folder=='render' else 'render-extra-records.json')))
 for c in report['cases']:
  i=c['index'];r=records[i];html=(E/folder/('question-%03d.html'%(i+1))).read_text();ids=re.findall(r'<input type="radio"[^>]* value="([^"]+)"',html)
  assert len(ids)==5;pos=ids.index(key(r));ui.append({'file':folder+'/question-%03d.html'%(i+1),'id':r['question'][':question/id'],'display_order':ids,'keyed_display_position':pos+1,'first_position_success':pos==0})
save('ui-position-probes.json',{'positions':ui,'batch_count':5,'batch_first_choice_success':sum(x['first_position_success'] for x in ui[:5]),'baseline':0.2,'limitation':'UI hashes item ID and choice UUID. Offline item IDs are fixture-specific; actual task item IDs can differ. Raw fixed-position strategy already fails on exact batch; rendered first-position strategy also fails. Hash ordering inspected in ui/learning.js:690-702.'})
# Compare full visible content across actual stable-identity normalization.
normal=[]
for raw_name,out_name in [('batch','delivered-batch'),('fresh-easy','delivered-fresh')]:
 a=sets[raw_name];b=sets[out_name];assert len(a)==len(b)
 for x,y in zip(a,b):
  assert x['question'][':question/problem']==y['question'][':question/problem']
  assert x['question'][':question/worked-solution']==y['question'][':question/worked-solution']
  assert triples(x)==triples(y)
  xv=next(v[':answer/value'] for v in field(x)[':answer-field/choices'] if v[':answer/id']==key(x));yv=next(v[':answer/value'] for v in field(y)[':answer-field/choices'] if v[':answer/id']==key(y));assert xv==yv
 normal.append({'raw':raw_name,'delivered':out_name,'count':len(a),'prompt_bank_key_solution_preserved':True,'decision_profiles_before':dict(collections.Counter(profile(r) for r in a)),'decision_profiles_after':dict(collections.Counter(profile(r) for r in b))})
save('delivery-comparison.json',normal)
# Reproduce historical inventory weakness with actual preserved original runtime.
sys.path.insert(0,str(t.R));from scripts.generator_publish import stable_identities,normalized_question
src=json.load(open(J/'source/source.json'))['material']['kp'];originals={q[':question/id'] for q in src[':knowledge-point/questions']};originals.add(src[':knowledge-point/canonical-example'][':question/id'])
inv=json.load(open(J/'source/inventory.json'));spec=importlib.util.spec_from_file_location('before_generator',W/'evidence/before-package/generator.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
records=[];inventory_results=[]
for q in inv['questions']:
 if q[':question/id'] in originals:continue
 eqs=t.equations(q[':question/problem']);rf=t.rref(eqs);b,c,d=map(int,rf[0][1:]);f=q[':question/answer-fields'][0];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id']);sb=[[sign(v) for v in t.matrix(a[':answer/value'])[0][1:]] for a in f[':answer-field/choices']]
 plan='swap2' if 'leftrightarrow R_2' in q[':question/worked-solution'] else 'swap3' if 'leftrightarrow R_3' in q[':question/worked-solution'] else 'normalize'
 p=dict(profile='authored-sign-comparison',difficulty='easy',b=b,c=c,d=d,scales=[int(row[0]) for row in eqs],plan=plan)
 r=old.authored(p,sb,ci);r['question']=stable_identities(r['question'],src[':knowledge-point/id']);a=normalized_question(q);out=normalized_question(r['question']);a.pop(':question/worked-solution',None);out.pop(':question/worked-solution',None);assert a==out
 assert sign_strategy(r)==key(r)
 r['generation'].update(sign_bank=sb,correct_index=ci,reproduction='Explicit parameters inferred from stored prompt/bank, reproduced using preserved 1.0.0 runtime. Original seed/draw/version metadata not present in capture, not invented.',original_generation_metadata=None)
 records.append(r);inventory_results.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'stable_id_prompt_bank_key_equal':True,'historical_sign_shortcut':True,'original_generation_metadata_available':False})
save('generated-records.json',records);save('stored-records.json',[q for q in inv['questions'] if q[':question/id'] not in originals]);save('affected-inventory.json',{'affected_questions':[dict(question_id=x['question_id'],entity_id=x['entity_id'],finding='Historical sign-only bank: identical absolute entries and a unique correct normalized sign pattern. Reproduced prompt, bank, key and stable publication ID from explicit parameters; current ordinary sampling no longer has this rule.',reproduction=str(t.PY)+' '+str(E/'post_audit.py'),evidence_path='generated-records.json') for x in inventory_results]})
save('inventory-assessment.json',{'basis':inv['basis'],'captured_questions':len(inv['questions']),'source_questions_excluded':len(inv['questions'])-len(records),'non_source_tested':len(records),'historically_affected':len(records),'records':inventory_results,'limits':['All five captured non-source questions tested; original source questions were excluded and never marked generated.','Original generation metadata absent. Explicit inferred replay parameters and actual reconstructed runtime metadata are retained, without asserting seed/draw provenance.','This is a historical pool defect already demonstrated in review 0, not a new current-generator finding. Existing bank remediation lies outside this review; no DB writes.']})
# Learner selection: reproduce uniform per-band SHA256 branch on captured pool + new survivors.
# New DB IDs not assigned offline: use rank-preserving synthetic IDs after captured IDs and expose that limit.
new=sets['delivered-batch'];pool=[]
for q in inv['questions']:
 band=q.get(':question/difficulty',{});band=band.get(':db/ident') if isinstance(band,dict) else band
 pool.append({'entity':q[':db/id'],'id':q[':question/id'],'band':band.split('/')[-1] if band else None,'new':False})
base=max(q['entity'] for q in pool)+1
pool += [{'entity':base+i,'id':r['question'][':question/id'],'band':'easy','new':True} for i,r in enumerate(new)]
def select(pool,distribution,seed):
 pool=sorted(pool,key=lambda q:q['entity'])
 if distribution is None:return pool[0] if pool else None
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=lambda off:(int.from_bytes(digest[off:off+8],'big')>>11)/(1<<53)
 bands=[[q for q in pool if q['band']==b] for b in ('easy','moderate','hard')];total=sum(w for w,qs in zip(distribution,bands) if qs)
 if total>0:
  draw=u(0)*total;chosen=None
  for i,w in enumerate(distribution):
   if not bands[i] or w==0:continue
   chosen=i
   if draw<w:break
   draw-=w
  qs=bands[chosen]
 else:qs=[q for q in pool if q['band'] is None]
 return qs[int(u(8)*len(qs))] if qs else None
selection={}
for label,distribution in [('positive_easy',[1,0,0]),('zero_easy',[0,1,0]),('mixed',[2,1,0]),('unconfigured',None)]:
 counts=collections.Counter();new_counts=collections.Counter();sampled=[]
 for i in range(120):
  seed='review-20261021/'+str(i);q=select(pool,distribution,seed)
  if q:
   counts[q['id']]+=1
   if q['new']:new_counts[q['id']]+=1
   sampled.append({'seed':seed,'id':q['id'],'new':q['new']})
 selection[label]={'distribution':distribution,'draws':len(sampled),'counts':dict(counts),'new_counts':dict(new_counts),'draw_records':sampled}
# Freshness exclusions remove prior/current items. Exercise without replacement through every new member.
sequences=[]
for learner in range(3):
 remaining=[q for q in pool if q['new']];seq=[]
 while remaining:
  seed=f'new-only-{learner}/prefix-{len(seq)}';q=select(remaining,[1,0,0],seed);seq.append(q['id']);remaining=[x for x in remaining if x['entity']!=q['entity']]
 sequences.append(seq)
save('selection-analysis.json',{'command':str(t.PY)+' '+str(E/'post_audit.py'),'policy_source':'engine/rust/question_selection.rs:111-218; seen_before_task excludes previous task items; caller excludes current prefix; select deduplicates entity IDs, selects positive-weight nonempty band, then uniform SHA256 within band. No policy chooses within a band by template or answer.','inventory_basis':inv['basis'],'candidate_pool':pool,'simulations':selection,'freshness_sequences':sequences,'analytic_conclusion':'At any positive easy weight each fresh easy survivor is equally eligible, so no source-dependent selection gate removes a numerical decision case. Existing inventory includes five historically weak sign banks; mixed pool is not certified free of those old items. Zero easy weight excludes this new easy batch. Unconfigured policy deterministically picks lowest entity ID.','limitations':['Actual future DB entity IDs, learner histories and configured weights unavailable. New IDs are synthetic to run representative orderings; uniform eligibility is independent of within-band ordering.','Seen histories can leave arbitrary nonempty subsets; no finite five-item pool promises all templates after arbitrary exclusions.','Publication absent: faithfully reproduced normalization and filtering against captured basis 5370. No publication or DB writes.']})
save('delivery-boundary-records.json',[new[0],new[0],records[0]])
(E/'session-state.md').write_text('Completed current native grader (635 outcomes, zero mismatches), actual delivery batch 5/5 and fresh 40/40, conditional shortcut measurements, fixed-bank/scale counterfactuals, actual UI renders and screenshot inspection, selection reproduction and five historical affected inventory reconstructions. Final evidence contract and package-unchanged check remain.\n')
print(json.dumps({'new_batch_unique_sign_success':sum(x['correct'] for x in rows if x['set']=='delivered-batch' and x['subgroup']=='overall' and x['strategy']=='unique-signs'),'delivered_batch_position_success':{x['strategy']:x['correct'] for x in rows if x['set']=='delivered-batch' and x['subgroup']=='overall'},'old_inventory_affected':len(records),'ui_batch_first_success':sum(x['first_position_success'] for x in ui[:5])}))
