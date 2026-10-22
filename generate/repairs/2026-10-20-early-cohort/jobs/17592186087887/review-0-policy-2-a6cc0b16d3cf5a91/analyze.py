#!/usr/bin/env python3
import sys,json,pathlib,hashlib,re,copy,collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy');P=J/'workspace'
sys.path.insert(0,str(P));import generator as g
sys.path.insert(0,str(R));from scripts.generator_publish import stable_identities,content_fingerprint,enum

def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
s=load(J/'source/source.json');inv=load(J/'source/inventory.json');source=s['material']['kp'][':knowledge-point/questions']
rs=load(E/'independent-samples.json');batch=load(E/'runner-batch.json')
def norm(z):
 z=z.replace('\\ln(x^2)','\\ln x^2').replace('\\operatorname{ln}','\\ln').replace('\\mathrm{d}','d').replace('\\text{d}','d')
 for term in ('\\left','\\right','\u2061','{','}',' ','\n','.'):
  z=z.replace(term,'')
 return z.strip('$').replace(r'\ln(x^2)',r'\lnx^2')
replays=[]
for r in load(E/'source-replay-records.json'):
 q=r['question'];sid=r['generation']['source_question_ids'][0];sq=next(z for z in source if z[':question/id']==sid)
 bank=[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
 original=[a[':answer/value'] for a in sq[':question/answer-fields'][0][':answer-field/choices']]
 bankok=sorted(map(norm,bank))==sorted(map(norm,original))
 rhs=norm(q[':question/problem'].rsplit('=',1)[1]);srhs=norm(sq[':question/problem'].rsplit('=',1)[1])
 # math display close delimiters and punctuation already removed by norm
 ok=bankok and rhs==srhs
 replays.append({'template':r['generation']['template'],'source_id':sid,'all_five_bank_members_match':bankok,'generated_bank':bank,'source_bank':original,'generated_rhs':rhs,'source_rhs':srhs,'rhs_match':rhs==srhs,'passed':ok,'solution_review':'Same substitution, separation, integration and back-substitution stages; source algebra is condensed, not verbatim. Generated a=1 source identities are mathematical replay, not original UUID replay.'})
unsupported=[{'source_id':q[':question/id'],'reason':'Moderate arctangent family not implemented; outside requested easy scope.'} for q in source if q[':question/id'] not in g.SOURCES.values() and q[':question/id'] not in {r['source_id'] for r in replays}]
save('source-replay.json',{'cases':replays,'failures':[r for r in replays if not r['passed']],'unsupported':unsupported,'canonical_example':'Image canonical y\'= (x^2+y^2)/(2xy) is not directly supported by fixed coefficient 3 in power family; outside labelled easy source family. Source image read in source-images.png.','corrections':'Missing original q-8843 key independently inferred by integration. Easy source cubic stray differential after integrated expression removed. Moderate y=0 exclusions explicitly added for inverse-square and square-implicit.','requested_easy_replay_complete':all(r['passed'] for r in replays if r['template'] in ('cube_root','affine','linear_log'))})
# Exact reconstruction of captured generated inventory: UUIDs after actual publisher identity derivation.
normalized=[{**r,'question':stable_identities(r['question'],g.KP['id'])} for r in rs]
byid={r['question'][':question/id']:r for r in normalized}; affected=[];stored_records=[];untested=[]
for q in inv['questions']:
 if q.get(':question/math-academy-id'):continue # original instructional content never marked generated
 r=byid.get(q[':question/id'])
 if r is None:untested.append(q[':question/id']);continue
 fq=content_fingerprint(q);fr=content_fingerprint(r['question'])
 if fq!=fr:untested.append(q[':question/id']);continue
 stored_records.append(r)
 # Primary demonstrated defect applies to cubes. Other bank-only probe reported separately.
 if r['generation']['template'] in ('cube_root','linear_log','affine'):
  a=r['generation']['parameters']['a'];t=r['generation']['template'];affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':{'cube_root':'The unique cube-root choice is always correct without inspecting the ODE.','linear_log':'The sole choice with both x ln|x| and +Cx is always correct without inspecting the ODE.','affine':'Of the two Cx^2 plus linear-term choices, the smaller absolute linear coefficient is always correct without inspecting the ODE.'}[t],'reproduction':f"PYTHONDONTWRITEBYTECODE=1 {R}/.venv/bin/python audit.py; {R}/.venv/bin/python analyze.py; reconstructed generator.generate('{t}', {a}, seed=826031), then generator_publish.stable_identities. Run the bank-only strategy in reproduce_shortcut.py.",'evidence_path':'generated-records.json'})
save('generated-records.json',stored_records);save('affected-inventory.json',{'affected_questions':affected})
save('inventory-assessment.json',{'basis':inv['basis'],'original_source_count':sum(bool(q.get(':question/math-academy-id')) for q in inv['questions']),'generated_candidates':sum(not bool(q.get(':question/math-academy-id')) for q in inv['questions']),'exact_reconstructed_records':len(stored_records),'affected_generated_records':len(affected),'untested_generated_question_ids':untested,'matching':'Every reconstructed stored generated record has the stored question UUID and equal actual publisher content fingerprint. Metadata template/parameter follows matching full prompt, bank and solution. Captured inventory has no original generation seed; review reproduction uses seed 826031, which does not affect content. Original seed not asserted.','complete_reproduced_records':'generated-records.json'})
# Shape-only probes. No prompt or generation metadata passed to choose functions.
def shape_pick(r,strategy):
 f=r['question'][':question/answer-fields'][0]
 if strategy=='unique cube root':options=[a for a in f[':answer-field/choices'] if '\\sqrt[3]' in a[':answer/value']]
 elif strategy=='x log and Cx': options=[a for a in f[':answer-field/choices'] if 'x\\ln|x|' in a[':answer/value'] and a[':answer/value'].endswith('+Cx')]
 elif strategy=='smaller affine coefficient':
  matches=[(a,re.fullmatch(r'y=Cx\^2[+-](\d*)x',a[':answer/value'])) for a in f[':answer-field/choices']]
  hits=[(int(m.group(1) or 1),a) for a,m in matches if m]
  return min(hits,key=lambda z:z[0])[1][':answer/id'] if len(hits)==2 and hits[0][0]!=hits[1][0] else None
 return options[0][':answer/id'] if len(options)==1 else None
stages={name:rr for name,rr in [('raw',rs),('post_delivery',load(E/'delivery-independent/accepted.json')),('runner_raw',batch),('runner_post_delivery',load(E/'delivery-batch/accepted.json')),('stored_generated',stored_records)]}
probes=[];counts={}
for name,rr in stages.items():
 counts[name]=dict(collections.Counter((r['generation']['template']+(' positive' if r['generation']['parameters']['a']>0 else ' negative')) for r in rr))
 for family,strategy in [('cube_root','unique cube root'),('linear_log','x log and Cx'),('affine','smaller affine coefficient')]:
  subset=[r for r in rr if r['generation']['template']==family]
  if not subset:continue
  outcomes=[{'question_id':r['question'][':question/id'],'a':r['generation']['parameters']['a'],'selected_answer_id':shape_pick(r,strategy),'correct':shape_pick(r,strategy)==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]} for r in subset]
  probes.append({'stage':name,'subgroup':family,'strategy':strategy,'correct':sum(o['correct'] for o in outcomes),'total':len(outcomes),'baseline':0.2,'outcomes':outcomes})
save('shortcut-results.json',{'input':'Complete records in independent-samples.json, runner-batch.json, delivery-*/accepted.json, generated-records.json','baseline':'Uniform random one-of-five choice is 0.2; probes do not read ODE, coefficient, keyed answer, source ID or seed when producing a selection. Key is consulted only to score.','ui_position_caveat':'ui/learning.js choiceOrder uses per-item/field FNV sorting by UUID, so fixed author bank positions are not claimed as a delivered defect. Shape strategy is invariant to permutation.','probes':probes,'stage_counts':counts})
# Faithful read-only reproduction of native within-easy selection, hash algorithm from question_selection.rs.
# Candidate IDs sorted/deduplicated; reported inventory has no learner/history/weight snapshot.
def select(ids,seed):
 ids=sorted(set(ids));h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(h[8:16],'big')>>11)/(1<<53);return ids[int(u*len(ids))]
qbyid={q[':db/id']:q for q in inv['questions']};easyids=[eid for eid,q in qbyid.items() if enum(q.get(':question/difficulty'))==':question.difficulty/easy']
sel=[]
for i in range(32):
 seed='independent-review-826036-'+str(i);e=select(easyids,seed);sel.append({'seed':seed,'selected_entity':e,'question_id':qbyid[e][':question/id'],'affected':qbyid[e][':question/id'] in {a['question_id'] for a in affected}})
# Sequential nonreplacement selection demonstrates each stored candidate remains eligible until seen.
remaining=easyids[:];seq=[]
while remaining:
 e=select(remaining,'independent-review-history-'+str(len(seq)));remaining.remove(e);seq.append({'selected_entity':e,'question_id':qbyid[e][':question/id']})
save('selection.json',{'implementation':'Faithful within-easy pool branch of engine/rust/question_selection.rs::select: sorted distinct IDs, SHA-256 seed, second 53-bit draw. Seen-before and task prefix exclusion represented by sequential removal.','candidate_ids':easyids,'fresh_draws':sel,'sequential_history_exclusion':seq,'affected_draws':sum(z['affected'] for z in sel),'bounds':'Actual learner weights/history/task IDs not captured. Conditional on positively weighted easy band, each fresh usable easy candidate has positive probability; there is no shape/template filter. Unconfigured policy selects first sorted entity; after prior history exclusion affected entries remain possible. Actual policy proportions cannot be inferred. This examines applicable rule without claiming live learner frequencies.','post_delivery':'Captured inventory and new accepted records in easy band retain both cube roots and linear-log cases; deduplication does not filter bank shapes.'})
save('scope.json',{'requested_difficulty':'easy','families':{'cube_root':'F(v)=v+a/v^2 -> v^2 dv=a dx/x -> real cube root, same easy source operation.','affine':'F(v)=a+2v -> dv/(a+v)=dx/x -> power solution, same easy source operation.','linear_log':'F(v)=a+v -> dv=a dx/x -> linear-log solution, same easy source operation.'},'tested_a':list(range(-9,0))+list(range(1,10)),'reasoning_scope':'Negative coefficients do not add integration techniques or response stages. Real cube root and x,y nonzero intervals stated. Each of the 54 records is a same-method scalar coefficient variant. No free-entry grader or new operators introduced.','limitations':'Moderate extensions outside requested delivered band receive source replay only; this is not a full moderate-band certification.'})
(E/'session-state.md').write_text('Source reconstruction, 54-slot easy census, 59 independent math/bank checks, native grader (69 correct + 276 wrong), delivery filters and inventory reconstruction complete. 49/54 independent and 4/5 runner records survive basis-5449 deduplication. Confirmed cube-root bank-shape shortcut; 5 affected stored generated questions reproduced exactly. Renderer running; screenshots, final pedagogical report and package-integrity comparison remain.\n')
print(json.dumps({'replay_failures':len([r for r in replays if not r['passed']]),'inventory_reconstructed':len(stored_records),'affected_inventory':len(affected),'stage_counts':counts,'shortcut_summary':[{k:z[k] for k in ['stage','subgroup','correct','total']} for z in probes]}))
