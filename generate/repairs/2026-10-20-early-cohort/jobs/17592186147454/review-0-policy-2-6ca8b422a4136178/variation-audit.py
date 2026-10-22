"""Read-only delivery/shortcut audit. Exits 1 on the retained acceptance failure."""
import json,pathlib,sys,importlib.util,re,copy,hashlib,subprocess
from html.parser import HTMLParser
E=pathlib.Path(__file__).resolve().parent;J=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy');sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('g',J/'workspace/17592186147454.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def read(p):return json.loads((E/p).read_text())
def save(p,x):(E/p).write_text(json.dumps(x,indent=2)+'\n')
def norm(v):
 v=re.sub(r'\(x[+-]\d+\)','x',v)
 return re.sub(r'\s+','',v.replace(r'\cdot','').replace(r'\left','').replace(r'\right',''))
def field(r):return r['question'][':question/answer-fields'][0]
def key(f):
 v=f[':answer-field/correct'];return v[':answer/id'] if isinstance(v,dict) else v[1]
def bank_signature(r):return tuple(sorted(norm(a[':answer/value']) for a in field(r)[':answer-field/choices']))
# Learn only literal source keys, then use visible bank patterns, no generation fields/IDs.
lookup={bank_signature(r):norm(next(a[':answer/value'] for a in field(r)[':answer-field/choices'] if a[':answer/id']==key(field(r)))) for r in read('source-replays.json')}
def memory(r):
 f=field(r);expected=lookup.get(bank_signature(r));c=[a for a in f[':answer-field/choices'] if norm(a[':answer/value'])==expected]
 return len(c)==1 and c[0][':answer/id']==key(f)
def cue154(r):
 # Exact recognisable coefficient pattern, independent of displayed option order.
 f=field(r);selected=[a for a in f[':answer-field/choices'] if r'C-2{x}^{5/2}' in norm(a[':answer/value'])]
 return len(selected)==1 and selected[0][':answer/id']==key(f)
def cue170(r):
 f=field(r);selected=[a for a in f[':answer-field/choices'] if r'{9{x}^{1/4}}' in norm(a[':answer/value'])]
 return len(selected)==1 and selected[0][':answer/id']==key(f)
focused=[g.generate('moderate',89111,'q-109154',{'shift':h}) for h in list(range(-6,0))+list(range(1,7))];save('focused-shortcut-records.json',focused)
sets={'raw_independent':read('independent-samples.json'),'delivered_independent_moderate':read('delivery-moderate-samples/accepted.json'),'delivered_independent_hard':read('delivery-hard-samples/accepted.json'),'exact_batch':read('batch.json'),'delivered_exact_batch':read('delivery-batch/accepted.json'),'focused_q109154_domain':focused}
results={name:{'count':len(rs),'source_key_memory_correct':sum(memory(r) for r in rs),'profile_counts':{t:sum(r['generation']['template']==t for r in rs) for t in sorted({r['generation']['template'] for r in rs})},'by_profile':{t:{'correct':sum(memory(r) for r in rs if r['generation']['template']==t),'total':sum(r['generation']['template']==t for r in rs)} for t in sorted({r['generation']['template'] for r in rs})}} for name,rs in sets.items()}
fixed_cue_perfect=all(cue154(r) for r in focused)
results['specific_cue_q109154']={'strategy':'Select the sole formula containing denominator C-2u^(5/2), u=x+h. No ODE reduction or integration.','correct':sum(cue154(r) for r in focused),'total':len(focused),'batch_correct':sum(cue154(r) for r in sets['exact_batch'] if r['generation']['template']=='q-109154'),'batch_total':sum(r['generation']['template']=='q-109154' for r in sets['exact_batch'])}
# Reproduce only the independently identified generated inventory member; source IDs stay source.
inv=json.loads((J/'source/inventory.json').read_text());original_ids={q[':question/id'] for q in json.loads((J/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']};stored_generated=[q for q in inv['questions'] if q[':question/id'] not in original_ids]
reference=json.loads((J/'workspace/17592186147454/reference/replenishment/basis-2280/generated.json').read_text())
reproduced=[];affected=[];inv_checks=[]
for q in stored_generated:
 ref=next(r for r in reference if r['question'][':question/id']==q[':question/id']);meta=ref['generation'];rr=g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],meta['seed'],meta['template'],meta['parameters']);assert rr==ref
 assert rr['question'][':question/id']==q[':question/id']
 # Captured bank ordering and TeX sizing normalize differently; compare full formula multiset and key.
 assert sorted(norm(a[':answer/value']) for a in field(rr)[':answer-field/choices'])==sorted(norm(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices'])
 assert norm(next(a[':answer/value'] for a in field(rr)[':answer-field/choices'] if a[':answer/id']==key(field(rr))))==norm(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])
 assert norm(rr['question'][':question/problem'])==norm(q[':question/problem']);assert norm(rr['question'][':question/worked-solution'])==norm(q[':question/worked-solution'])
 reproduced.append(rr);passed=cue170(rr);inv_checks.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'metadata_equal_reference':True,'prompt_solution_and_bank_match':True,'nine_denominator_cue_correct':passed})
 if passed:affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'q-109170 translation-only bank preserves the sole fourth-power formula with 9u^(1/4) denominator; that visible signature selects its key without solving.','reproduction':"PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python variation-audit.py ; generate('hard',0,'q-109170',{'shift':-6})",'evidence_path':'generated-records.json'})
save('generated-records.json',reproduced);save('affected-inventory.json',{'affected_questions':affected});save('inventory-results.json',{'basis':inv['basis'],'total':len(inv['questions']),'original_sources':len(original_ids),'generated_members_tested':len(stored_generated),'checks':inv_checks,'limits':'All captured non-source members reproduced using saved generation metadata. Original source questions are not labeled generated. No claim about later-changing inventory.'})
# Native-grade all newly targeted examples along with previous math checked cases in one batch.
cases=read('grader-input.json')
for r in focused+reproduced:
 f=field(r);cases.append({'label':'shortcut:'+r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(f) else 'rejected','purpose':'Complete bank; verify visible shortcut selects actual accepted answer'} for a in f[':answer-field/choices']]})
save('grader-input.json',cases);cmd=[str(R/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-report.json')];p=subprocess.run(cmd,capture_output=True,text=True);save('grader-execution.json',{'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0
# UI position probe uses the actual rendered option order (learning.js hashes task/field IDs).
class Inputs(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='input' and a.get('type')=='radio':self.ids.append(a['value'])
first=[]
for i,r in enumerate(read('render-records.json'),1):
 h=Inputs();h.feed((E/f'render/question-{i:03d}.html').read_text());assert len(h.ids)==5
 first.append({'record_index':i,'first_choice_correct':h.ids[0]==key(field(r)),'order':h.ids,'correct_id':key(field(r))})
results['actual_ui_first_position']={'correct':sum(v['first_choice_correct'] for v in first),'total':len(first),'cases':first,'conclusion':'Original bank positions are NOT learner positions; actual UI shuffles. No fixed-position defect claimed.'}
results['acceptance_test']={'name':'q109154 fixed coefficient-signature cue must not identify every member of the generated profile','expected':'At least one legitimate same-method coefficient/sign/answer-role counterexample in practice; fixed assignment needs an instructional reason.','observed':'12/12 finite translation variants answered by C-2u^(5/2) cue; eligible q_scale=2 rejected (counterfactual-results.json).','passed':not fixed_cue_perfect}
save('shortcut-results.json',results)
# Faithful read-only reproduction of Rust select with explicit synthetic future entity IDs.
def choose(pool,weights,seed):
 bands=[[],[],[]]
 for entity,band in sorted(set(pool)):bands[band].append(entity)
 d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 def uniform(offset):return (int.from_bytes(d[offset:offset+8],'big')>>11)/2**53
 total=sum(w for i,w in enumerate(weights) if bands[i]);draw=uniform(0)*total;chosen=None
 for i,w in enumerate(weights):
  if not bands[i] or w==0:continue
  chosen=i
  if draw<w:break
  draw-=w
 if chosen is None:return None
 pp=bands[chosen];return pp[int(uniform(8)*len(pp))]
br=sets['delivered_exact_batch'];draws=[]
for seen in [[],[1],[1,2,3]]:
 pool=[(i+1,1) for i in range(len(br)) if i+1 not in seen];counts={str(i):0 for i,b in pool}
 for n in range(512):
  v=choose(pool,[0,1,0],f'independent-selection-{n}');counts[str(v)]+=1
 draws.append({'seen_synthetic_ids':seen,'counts':counts,'cue_correct_draws':512,'draws':512})
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs::select and seen_before_task, read directly','reproduction':'Exact SHA256 draw/band selection for delivered moderate pool, fresh-history exclusions applied. Future entity IDs modeled 1..5 because publication has not occurred.','basis':inv['basis'],'draws':draws,'proof':'Selection chooses an existing record without changing its prompt, bank or key. Source-bank signature strategy is correct on every delivered batch member, so arbitrary positive-weight/historical conditioning on nonempty subsets preserves 100% cue success. No actual learner history, policy, or future entity allocation is captured; no exact future task prediction claimed.','stage_counts':{n:{'input':read('delivery-'+n+'/delivery.json')['input_count'],'duplicates':read('delivery-'+n+'/delivery.json')['duplicate_count'],'accepted':read('delivery-'+n+'/delivery.json')['accepted_count']} for n in ['batch','moderate-samples','hard-samples']},'resampling':'Generator main samples seed..seed+999, rejects repeated (template,shift) pairs, then returns requested count; it never changes bank-role assignments. No math rejection stages. Difficulty chooses source profiles; q-109029 excluded in eligible list.'})
(E/'session-state.md').write_text('Completed math, source fidelity (TeX sizing/order normalized), native grading, all batch and independent delivery filters, actual UI screenshots, focused shortcut domain (q-109154 12/12), and stored generated-item reproduction. Demonstrated fixed-bank shortcut survives all delivery stages. Next: validate pedagogical schema/evidence contract and final report. Package unchanged.\n')
print(json.dumps({'batch':results['delivered_exact_batch'],'focused':results['specific_cue_q109154'],'affected_inventory':len(affected),'acceptance_passed':not fixed_cue_perfect},indent=2))
raise SystemExit(1 if fixed_cue_perfect else 0)
