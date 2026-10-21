import json,pathlib,sys,copy,collections,hashlib,re,importlib.util
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;W=E.parent/'workspace'
spec=importlib.util.spec_from_file_location('decision',E/'decision_audit.py');d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
# Measure actual sampler rejection in memory; preserve the unmodified implementation.
import bank_sampler
original=bank_sampler.compatible_masks;attempts=[]
def measured(bank,bottom):
 result=original(bank,bottom)
 attempts.append({'size':len(bank[0]),'bottom_zero':bottom,'accepted_bank':result is not None,'witness_counts':list(map(len,result)) if result is not None else None})
 return result
bank_sampler.compatible_masks=measured
fresh=json.loads((E/'fresh-control-records.json').read_text());last=0;rows=[]
for r in fresh:
 seed=r['generation']['seed'];new=d.g.generate('moderate',seed);assert new==r
 rows.append({'seed':seed,'attempt_count':len(attempts)-last,'accepted_count':sum(x['accepted_bank'] for x in attempts[last:]),'size':len(d.bank(r)[0]),'bottom_zero':not any(d.strict.matrix(r['question'][':question/problem'])[-1])});last=len(attempts)
bank_sampler.compatible_masks=original
save('sampler-rejection-results.json',{'records':rows,'attempts':attempts,'key_assignment':'Key is drawn uniformly after rejection of whole bank. Every accepted bank has witnesses for all five roles under its preselected size and bottom-zero condition.','records_unchanged':True})
batch=json.loads((E/'batch-records.json').read_text());assert all(d.g.generate('moderate',r['generation']['seed'])==r for r in batch)
delivery=[]
for source,stage in [('batch-records.json','delivery-batch'),('independent-samples.json','delivery-independent'),('cli-control-records.json','delivery-cli'),('fresh-control-records.json','delivery-fresh'),('fixed-bank-records.json','delivery-controls'),('counterfactual-records.json','delivery-cf')]:
 before=json.loads((E/source).read_text());after=json.loads((E/stage/'accepted.json').read_text())
 for r in after:d.strict.check_record(r)
 bp=d.probes(before);ap=d.probes(after)
 assert set(bp)==set(ap) and all(bp[k]['hits']==ap[k]['hits'] and bp[k]['n']==ap[k]['n'] for k in bp)
 assert all(a['key']==b['key'] and a['predictions']==b['predictions'] for a,b in zip(bp['overall']['trials'],ap['overall']['trials']))
 delivery.append({'stage':stage,'input':len(before),'accepted':len(after),'probes_identical':True,'batch_exact_seed_replay':True if stage=='delivery-batch' else None})
save('delivery-comparison.json',delivery)
# Source fidelity independently parsed from rendered strings, not generation metadata.
replays=json.loads((E/'source-replay.json').read_text());source_results=[]
original_source=json.loads((E.parent/'source/source.json').read_text())
source_questions={q[':question/id']:q for q in original_source['material']['kp'][':knowledge-point/questions']}
for case in replays:
 r=case['record'];d.strict.check_record(r)
 original=source_questions[case['source_id']]
 orig_matrices=re.findall(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',original[':question/worked-solution'],re.S)
 new_matrices=re.findall(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',r['question'][':question/worked-solution'],re.S)
 assert d.strict.matrix(orig_matrices[-1])==d.strict.matrix(new_matrices[-1])
 before_words=re.sub(r'\s+','',original[':question/problem'].split('$$')[0]);after_words=re.sub(r'\s+','',r['question'][':question/problem'].split('$$')[0]);assert before_words==after_words
 assert d.strict.matrix(r['question'][':question/problem'])==case['matrix'] and d.bank(r)==case['bank'] and d.ci(r)==case['expected']
 source_results.append({'source_id':case['source_id'],'complete_bank_matches':True,'matrix_matches':True,'key_matches':True,'source_solution_transformation_matches':True})
save('source-fidelity-results.json',source_results)
prior=json.loads((E/'prior-selection-analysis.json').read_text());prior['provenance']['reused_from']=str(E.parent/'review-1-policy-2-e842d7500966db6b/selection-analysis.json');prior['provenance']['current_verification']='Read current question_selection.rs select/seen_before_task; source/inventory/engine review bindings unchanged. Actual delivered batch and controls updated below.'
prior['new_batch']='All five exact batch members survive requested difficulty and inventory deduplication; all are moderate. Median cue succeeds 0/5. Positive moderate weight gives uniform sampling within eligible moderate candidates. Unconfigured policy takes minimum fresh entity ID. No post-publication entity IDs or learner history supplied; these conditional limits are retained.'
prior['control_survivors']={'count':64,'median_successes':9,'conditional_uniform_success_rate':9/64}
prior['applicable_rules']={'rated_band':'all new records moderate','positive_moderate_weight':'uniform over eligible moderate pool','zero_moderate_weight':'new records excluded, not a relative case bias','history':'can remove cases; no history-specific coverage guarantee','default':'lowest eligible entity ID; no claim of profile balance'}
save('selection-analysis.json',prior)
scope={'source_contract':'Select the unique offered successful replacement; no global minimum, no arithmetic or pivot normalization.','observed':'All 15 replays, exact batch, fresh samples, and nonminimum regression retain this task. Four-by-four ordinary integer matrices and five radio choices are preserved.','fixed_fresh_features':{'operation_size_2_or_3':'All source keys have two or three named entries; source replay retains mixed-size banks.','initial_nonzero_rows_at_least_3':'Source multirow workload preserved.','remaining_nonzero_rows_at_least_2':'Source multirow workload preserved.','already_zero_coordinates':'Legal per q-73149; not silently excluded.','bank_only_target':'Unfixed: independently found every one of five roles for each of four tested banks.'},'source_references':['5da4a360-a207-5df6-9d38-99e7b8b5a765','2ab2c24d-7d61-5976-acd1-acab7ad4094a','3458fbf5-87c4-5bfc-9974-f949a6151b73','tutorial 3896 / 137b0909-9a5e-5edf-8019-24e803307903'],'supported_source_corrections':'Normalize captured Unicode arrow to TeX; no mathematical corrections found.','unsupported_source_families':[],'canonical_limitation':'No captured canonical answer bank; its stated operation is checked separately.'}
save('scope-results.json',scope)
save('sampling-summary.json',{'groups':{n:{k:{'n':v['n'],'hits':v['hits']} for k,v in d.probes(json.loads((E/f).read_text())).items()} for n,f in [('batch','batch-records.json'),('fresh','fresh-control-records.json'),('cli','cli-control-records.json')]},'named_targets':len({tuple(map(tuple,d.bank(r)[d.ci(r)])) for r in fresh}),'input_masks':len({tuple(tuple(int(v!=0) for v in row) for row in d.strict.matrix(r['question'][':question/problem'])) for r in fresh}),'observed_nonzero_values':sorted({v for r in fresh for row in d.strict.matrix(r['question'][':question/problem']) for v in row if v})})
print(json.dumps({'batch_replay':5,'source_fidelity':len(source_results),'bank_attempts':len(attempts),'rejected_banks':sum(not x['accepted_bank'] for x in attempts),'delivery':delivery}))
