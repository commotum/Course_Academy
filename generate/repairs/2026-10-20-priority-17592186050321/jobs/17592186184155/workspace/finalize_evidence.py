"""Summarize final saved evidence and independently inspect the actual five-item batch."""
import hashlib,json
from pathlib import Path
import generator,validate
root=Path(__file__).resolve().parent
load=lambda name:json.loads((root/'evidence'/name).read_text())
raw=load('runner-batch.json');accepted=load('runner-delivery/accepted.json')
assert len(raw)==len(accepted)==5
for rec in raw+accepted:validate.math_check(rec)
assert generator.generate(30,difficulty='unclassified')==generator.generate(30,difficulty='hard')
rel=load('relocation.json')
assert rel['runtime_sha256']=={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in rel['runtime_files']}
variation=load('pedagogical-variation.json')
assert variation['conditional_before']==variation['conditional_after']
assert variation['normal_sampling_before']==variation['normal_sampling_after']
assert load('render/rendering.json')['passed']
runner={'count':5,'raw_and_filtered_math_passed':True,'templates':{},'key_positions':[],
        'limits':['Five records are the runner-sized smoke sample; broad variation claims use the 159-record audit.']}
for rec in accepted:
    name=rec['generation']['template'];runner['templates'][name]=runner['templates'].get(name,0)+1
    runner['key_positions'].append(validate.key_index(rec)+1)
validate.save('runner-analysis.json',runner)
summary={'status':'ready for independent review','default_difficulty':'hard',
 'fidelity':{'source_banks':4,'matched_options':20,'matched_distractors':16,'source_keys_inferred':2,
             'layout':'Mathematical tokens retained; alignment reflowed after visual clipping was found.'},
 'correctness':{'independently_checked_generated_semantic_instances':159,'negative_domain_numeric_derivatives':45,
                'counterfactual_records':26,'runner_raw_and_filtered_records_checked':5},
 'grading':{k:v for k,v in load('native-grading.json').items() if k!='records'},
 'decision_variation':{'delivery_coverage_preserved':variation['delivery_coverage_preserved'],
   'conditional_groups_preserved':len(variation['conditional_before']),
   'normal_sample_max_tested_shortcut_rate':max(v['rate'] for p in variation['normal_sampling_before'].values() for v in p['shortcut_probes'].values()),
   'uniform_choice_baseline':0.2,'perfect_tested_incidental_predictors':0},
 'delivery':load('delivery/delivery.json'),'runner_delivery':load('runner-delivery/delivery.json'),
 'rendering':{'DOM_passed':True,'representatives':5,'visual_inspection':'See visual-inspection.json'},
 'relocation':{'passed':rel['passed'],'only_declared_runtime_files':True,'runtime_assets':0},
 'limitations':['Only hard sampling supported: moderate has missing answer fields; easy lacks evidence.',
  'Two unlabeled source banks require inferred keys and authored solutions; source labels retained.',
  'Normal bank is an explicitly documented same-method extension, not a literal source-bank sampler.',
  'Captured-inventory filtering was tested; live learner histories and policy configuration were not available.'],
 'database_writes':0,'published_assets':0}
validate.save('final-results.json',summary)
print(json.dumps({'math_instances':159,'native_responses':summary['grading']['accepted_checks']+summary['grading']['rejected_checks'],
                  'delivery_accepted':summary['delivery']['accepted_count'],'runner_accepted':5,'relocation':True}))
