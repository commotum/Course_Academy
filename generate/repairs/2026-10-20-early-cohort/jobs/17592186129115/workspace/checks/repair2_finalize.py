"""Assemble current delivery/grader/render evidence without runtime mutations."""
import collections, copy, hashlib, importlib.util, itertools, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
from regressions import W, generator as g, check_record, matrix, coords, ref_after
from validate import features, selected, bank
E=W/'evidence/repair2'
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
# Reproduce exact latest minimal case against preserved pre-change code.
spec=importlib.util.spec_from_file_location('pre_repair',E/'generator-before.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);old.HERE=W
r=old.generate('moderate',431440325);check_record(r);b=bank(r);key=selected(r);m=matrix(r['question'][':question/problem'])
assert sorted(range(5),key=lambda k:b[k])[2]==key
correct=b[key];zc=sum(m[i][j]==0 for i,j in correct)
wrong=[list(map(list,op)) for op in itertools.combinations(itertools.product(range(4),repeat=2),len(correct)) if sum(m[i][j]==0 for i,j in op)==zc and not ref_after(m,op)]
lo=[op for op in wrong if op<correct][-12:];hi=[op for op in wrong if op>correct][:12];assert len(lo)==len(hi)==12
save('reported-seed-before.json',[r]);save('exact-reproduction.json',{'seed':431440325,'median_is_correct':True,'lower_pool':12,'upper_pool':12,'exact_old_probability':.375,'guessing_baseline':.2,'current_record':'regression/reported-seed-current.json','method':'Independently parse full prompt and options, apply replacements, enumerate matched incorrect coordinate sets.'})
# Retain source native cases and dependency cases; test delivered examples too.
cases=json.loads((W/'evidence/grader-input.json').read_text())
cli=json.loads((E/'regression/delivery-cli/accepted.json').read_text());controls=json.loads((E/'regression/delivery-controls/accepted.json').read_text())
for n,r in enumerate(controls):
 check_record(r);f=r['question'][':question/answer-fields'][0];key=selected(r)
 cases.append({'label':'fixed-bank five-role control '+str(n),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==key else 'rejected','purpose':'Independent visible-matrix echelon test; bank held constant, key changed by matrix evidence'} for i,a in enumerate(f[':answer-field/choices'])]})
for n,r in enumerate(cli):
 check_record(r);f=r['question'][':question/answer-fields'][0];b=bank(r);pred=sorted(range(5),key=lambda i:b[i])[2]
 cases.append({'label':'delivered matrix-blind median '+str(n),'record':r,'checks':[{'field_index':0,'submitted_answer_id':f[':answer-field/choices'][pred][':answer/id'],'expected':'accepted' if pred==selected(r) else 'rejected','purpose':'Actual delivered coordinate-order regression'}]})
# The runner's exact five-record seed range is a separate small sample.
requested=json.loads((E/'delivery-requested/accepted.json').read_text())
assert len(requested)==5
for n,r in enumerate(requested):
 check_record(r);f=r['question'][':question/answer-fields'][0];key=selected(r)
 cases.append({'label':'requested batch '+str(n),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==key else 'rejected','purpose':'Independent visible-operation check on runner seed range'} for i,a in enumerate(f[':answer-field/choices'])]})
comparisons={}
for label,rawname in [('batch','batch-records.json'),('cf','counterfactual-records.json')]:
 raw=json.loads((W/'evidence'/rawname).read_text());accepted=json.loads((E/('delivery-'+label)/'accepted.json').read_text())
 assert features(raw)==features(accepted)
 for r in accepted:check_record(r)
 comparisons[label]={'raw':features(raw),'accepted':features(accepted),'preserved':True}
save('delivery-comparisons.json',comparisons);save('grader-input.json',cases)
# Source zero-coordinate bank, new CLI matrix, two different keys with same bank.
source=json.loads((W/'evidence/source-records.json').read_text())
zero_source=next(r for r in source if r['generation']['profile']=='5da4a360-a207-5df6-9d38-99e7b8b5a765')
save('render-records.json',[zero_source,cli[0],controls[0],controls[1]])
# Captured inventory: observed cues versus certified reproductions are distinct.
inv=json.loads((W.parent/'source/inventory.json').read_text());src=json.loads((W.parent/'source/source.json').read_text());ids={q[':question/id'] for q in src['material']['kp'][':knowledge-point/questions']};rows=[];attempts=[]
sys.path.insert(0,'/home/jake/Developer/Course_Academy');from scripts.generator_publish import stable_identities
for q in inv['questions']:
 if q[':question/id'] in ids:continue
 f=q[':question/answer-fields'][0];b=[coords(a[':answer/value']) for a in f[':answer-field/choices']];p={'matrix':matrix(q[':question/problem']),'bank':b}
 rr=old.generate('moderate',0,parameters=p);rr['question']=stable_identities(rr['question'],g.KP_UUID);attempts.append(rr)
 cid=f[':answer-field/correct'][':answer/id'];key=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==cid)
 rows.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'median_selects_stored_key':sorted(range(5),key=lambda k:b[k])[2]==key,'prior_optimization_wording':'fewest' in q[':question/problem'].lower(),'historical_generation_metadata_present':any('generat' in k for k in q),'reconstructed_id':rr['question'][':question/id'],'identity_matches':rr['question'][':question/id']==q[':question/id']})
assert len(rows)==5 and not any(r['identity_matches'] or r['historical_generation_metadata_present'] for r in rows)
save('inventory-attempt-records.json',attempts);save('inventory-inspection.json',{'basis':inv['basis'],'all_captured_records_inspected':len(inv['questions']),'original_source_records_excluded':len(ids),'candidates':rows,'certified_reproductions':0,'limitation':'2/5 stored medians happen to be correct, but this alone cannot establish the distributional bank-construction defect. Captured historical optimization wording is observed. No historical generator metadata or matching identity was recovered; empty affected-inventory means no certified reproduction, not verified absence.'})
save('generated-records.json',[]);(W/'affected-inventory.json').write_text('{"affected_questions": []}\n')
manifest=json.loads((W/'package.json').read_text());save('runtime-hashes.json',{p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in manifest['files']+['package.json']})
print(json.dumps({'native_records':len(cases),'native_checks':sum(len(c['checks']) for c in cases),'delivery_comparisons':list(comparisons),'inventory_inspected':20,'certified_inventory_reproductions':0,'renders_prepared':4}))
