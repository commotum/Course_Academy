#!/usr/bin/env python3
"""Current frozen inventory, API contracts, adversarial displayed-readback, native probes."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,hashlib,copy,subprocess,re
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('isolated_validation',H/'validate.py'); v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
write=lambda n,x:(H/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Immutable captured wrappers and unchanged registered numeric pair including caches.
F=v.ROOT/'generate/runs/current/refresh-2026-10-14'
assert (H/'source.json').read_bytes()==(F/'sources/17592186059730.json').read_bytes()
for row in json.loads((H/'reference/registered-baseline.json').read_text())['files']:
 p=v.ROOT/row['path'];assert p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],str(p)
paths=[v.ROOT/'generate/scratch/17592186059730.py',v.ROOT/'generate/scratch/17592186059730']
assert {str(p.relative_to(v.ROOT)) for base in paths for p in ([base] if base.is_file() else base.rglob('*')) if p.is_file()}=={r['path'] for r in json.loads((H/'reference/registered-baseline.json').read_text())['files']}
# Build source replay records (only seven original Math Academy questions).
case_specs=v.read(H/'source-replay-specs.json'); cases=[]; repairs=[]
for case in case_specs:
 r=g.generate(case['difficulty'],17,case['template'],parameters=case['parameters'],profile=case['bank_profile']);v.check_record(r)
 entry={'source_id':case['source_id'],'record':r};cases.append(entry)
 if case['source_id']in ('q-1355','q-168035'):repairs.append(entry)
write('source-cases.json',cases);write('source-repairs.json',repairs)
# Existing generated inventory is an independent dedup/readback target, never MA evidence.
inventory=v.read(H/'independent-inventory.json');assert type(inventory['relationship'])is str
inventory_records=[]
for raw in inventory['questions']:
 q=copy.deepcopy(raw); level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 for f in q[':question/answer-fields']:
  f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
 q[':question/difficulty']=':question.difficulty/'+level
 m=re.findall(r'⟨([^⟩]+)⟩',q[':question/problem']);a,b=[[str(v.eval_math(z)) for z in x.split(',')]for x in m]
 f=q[':question/answer-fields'][0];template='components3_'+f[':answer-field/type'].split('/')[-1]
 made=g.generate(level,0,template,parameters={'a':a,'b':b});assert made['question'][':question/problem']==q[':question/problem']
 assert made['question'][':question/worked-solution']==q[':question/worked-solution']
 assert sorted(z[':answer/value']for z in made['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(z[':answer/value']for z in f[':answer-field/choices'])
 v.check_record(made);inventory_records.append(made)
write('inventory-readback.json',inventory_records)
# Every role slot is a complete corresponding pair; vary one supplied component independently.
base=g.generate_easy(template='if2_blank',parameters={'a':[5,1],'b':[2,4]})
changed=g.generate_easy(template='if2_blank',parameters={'a':[6,1],'b':[2,4]});assert v.check_record(base)==14 and v.check_record(changed)==16
write('changed-slot-cases.json',[base,changed])
# Deliberately preserve final correct scalar while corrupting intermediate terms, targets, or bank.
negative=[]
radio=g.generate_easy(template='let2_radio',parameters={'a':[5,1],'b':[2,4]})
for name,original,mutate in [
 ('stale_requested_vector',base,lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace(r'a\cdot b',r'a\cdot v'))),
 ('stale_solution_operand',base,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'a\cdot b',r'a\cdot v'))),
 ('compensating_intermediate_products',base,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('10+4','11+3'))),
 ('compensating_factor_products',base,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'5\cdot 2+1\cdot 4',r'4\cdot 2+1.5\cdot 4'))),
 ('wrong_formal_coordinate',base,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('{b}_{x}','{b}_{y}'))),
 ('wrong_distractor_correct_key_unchanged',radio,lambda r:next(a for a in r['question'][':question/answer-fields'][0][':answer-field/choices']if a[':answer/id']!=r['question'][':question/answer-fields'][0][':answer-field/correct'][1]).__setitem__(':answer/value','999')),
 ('blank_placeholder_lost',base,lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('{{field-1}}','{{field-2}}')))
]:
 bad=copy.deepcopy(original);mutate(bad)
 try:v.check_record(bad)
 except AssertionError:negative.append({'name':name,'rejected':True,'final_correct_key_unchanged':True})
 else:raise AssertionError(name)
write('negative-controls.json',negative)
# Strict API inputs including bool and int subclasses; finite count guards.
class IntSubclass(int):pass
bad_calls=0
for bad in [True,False,1.5,'1',None,IntSubclass(2)]:
 for call in [lambda:g.generate_easy(seed=bad),lambda:g.generate_batch(seed=bad),lambda:g.generate_batch(count=bad)]:
  try:call()
  except (ValueError,TypeError):bad_calls+=1
  else:raise AssertionError(('bad api type',bad))
for count in [0,-1,1001,10**100]:
 try:g.generate_batch(count=count)
 except ValueError:bad_calls+=1
 else:raise AssertionError(count)
batch=g.generate_batch('all',55,100);assert len(batch)==300 and len({r['generation']['canonical_task_key']for r in batch})==300
for r in batch:v.check_record(r)
# Actual CLI contracts and reproducibility.
cmd=[str(v.ROOT/'.venv/bin/python'),str(H.with_suffix('.py')),'--count','1','--difficulty','all']
a=subprocess.run(cmd+['--format','json'],check=True,text=True,capture_output=True).stdout
assert len(json.loads(a))==3
assert subprocess.run(cmd+['--format','json'],check=True,text=True,capture_output=True).stdout==a
md=subprocess.run(cmd+['--format','markdown'],check=True,text=True,capture_output=True).stdout;assert md.count('\n\n---\n\n')==2
(H/'cli-all.json').write_text(a);(H/'cli-all.md').write_text(md)
# Genuine equivalents go through frozen native engine; retain all observations unaltered.
inputs=[v.engine_item('original '+c['source_id'],c['record'])for c in cases]
inputs.extend(v.engine_item('inventory '+str(i),r)for i,r in enumerate(inventory_records))
for i,r in enumerate(batch[:8]):inputs.append(v.engine_item('batch '+str(i),r))
for level in ['easy','moderate','hard']:
 r=g.generate(level,99,template='if2_blank'if level=='easy'else'components3_blank');item=v.engine_item('latex equivalent '+level,r);c=v.check_record(r)
 item['checks'].append({'submitted':r'\frac{'+str(c.numerator*7)+'}{'+str(c.denominator*7)+'}','expected':'accepted','purpose':'genuine unreduced TeX rational equivalent; retained even if engine false rejects'})
 inputs.append(item)
# Canonical stays raw canonical prose; synthetic field only supplies its independently checked scalar.
canonical=g.RAW['record'][':knowledge-point/canonical-example'];q=copy.deepcopy(base['question']);q[':question/problem']=canonical[':question/problem'];q[':question/worked-solution']=canonical[':question/worked-solution'];q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='20'
rec={'knowledge_point':g.KP,'question':q,'generation':{'template':'canonical-probe','origin':'canonical context, not practice source'}}
ci=v.engine_item('canonical e-4323',rec);inputs.append(ci)
write('native-probe-input.json',inputs)
result=subprocess.run([str(H/'reference/check-engine'),str(H/'native-probe-input.json'),str(H/'native-probe-report.json')],capture_output=True,text=True)
(H/'native-probe-output.txt').write_text(result.stdout+result.stderr)
assert result.returncode==0,result.stderr
report={'passed':True,'basis':2275,'lineage':g.RAW['lineage'],'original_MA':7,'rated_easy_MA':6,'unrated_MA':1,'nonMA_inventory_only':len(inventory_records),'source_existing_solution_matches':6,'source_existing_designation_matches':6,'source_complete_banks':7,'source_values':23,'source_distractors':16,'raw_eligible_originals':5,'supported_repairs':2,'changed_slot_cases':2,'rendered_negative_controls':negative,'strict_input_rejections':bad_calls,'batch_distinct_actual_tasks':300,'cli_all_count1_list_length':3,'native':v.read(H/'native-probe-report.json'),'registered_baseline_files_unchanged':len(v.read(H/'reference/registered-baseline.json')['files']),'source_wrapper_byte_exact':True,'database_writes':0,'generator_sha256':sha(H.with_suffix('.py'))}
write('revalidation.json',report)
print(json.dumps({k:v for k,v in report.items()if k!='native'},indent=2))
