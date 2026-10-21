import sys;sys.dont_write_bytecode=True
from probe_tools import *
sel=load('selection-results.json');inv=load('../source/inventory.json');accepted=load('delivery/accepted.json');start=max(q[':db/id'] for q in inv['questions'])+100
pool={start+j:r for j,r in enumerate(accepted)}
stages={'raw':load('samples.json'),'delivered':accepted,'runner':load('runner-batch.json'),'runner_delivered':load('batch-delivery/accepted.json'),'controls_raw':load('role-controls.json'),'controls_delivered':load('controls-delivery/accepted.json')}
for s in sel['scenarios']:
 stages['selected_'+s['scenario']]=[pool[id] for id in s['draws'] if id in pool]
results={stage:probe(rs) for stage,rs in stages.items()};save('shortcut-stage-results.json',results)
def coverage(rs):
 out={}
 for p in 'PRB':
  rows=[r for r in rs if r['generation']['template']==p];pars=[r['generation']['parameters'] for r in rows]
  out[p]={'count':len(rows),'semantic_instances':len({(i['n'],i['s'],i['k']) for i in pars}),**{k:dict(collections.Counter(str(i[k]) for i in pars)) for k in ['n','s','k','variable','constant_first','omitted_row','omitted_col']}}
  if p!='B':out[p]['key_positions']=dict(collections.Counter(str(next(j for j,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==answer(r)[':answer/id'])) for r in rows))
 return out
save('coverage.json',{stage:coverage(rs) for stage,rs in stages.items()})
# Native exercise of cue-produced actions for fresh delivered and selected records.
cases=[]
for stage in ['delivered','runner_delivered','selected_positive_moderate']:
 rs=stages[stage];unique={r['question'][':question/id']:r for r in rs}
 for qid,r in unique.items():
  if field(r)[':answer-field/type'].endswith('/blank'):continue
  sts=strategies(r);key=answer(r)[':answer/id']
  cases.append({'label':stage+' incidental cue outcomes','record':r,'checks':[{'submitted_answer_id':s['selected'],'expected':'accepted' if s['selected']==key else 'rejected','purpose':cue} for cue,s in sts.items()]})
save('cue-grader-input.json',cases)
# Exact-control product is retained through actual shared delivery.
for row in results['controls_delivered']['summary']:
 if ':' in row['subgroup'] and row['cue'] in ['range6','eliminate_singleton','choose_singleton','min_constant','max_constant','shortest','longest','constant_then_max','constant_then_min','constant_then_most']:
  assert abs(row['tie_averaged_rate']-row['baseline'])<1e-12,row
summary={'captured_basis':inv['basis'],'stages':{stage:len(rs) for stage,rs in stages.items()},'delivery_reports':[load(d+'/delivery.json') for d in ['delivery','batch-delivery','controls-delivery']],
 'generator_rejection':'generate() constructs valid domains before building; no try/retry, rejection or resampling loop. Every requested draw is emitted; domain filtering for eligible errors is sampled side-first.',
 'selection':'Faithful previous independent reproduction rerun on current accepted records; numeric sort, actual SHA256 two-draw band/within-band rule; captured usable inventory plus synthetic appended IDs, seen/unconfigured/zero-weight cases.',
 'limits':sel['limits'],'controls_survive':True,'repro_commands':['job-python -B review.py','job-python -B probes.py','job-python -B selection_check.py','job-python -B delivery_analysis.py']}
save('delivery-selection-summary.json',summary)
print(json.dumps({'stage_counts':summary['stages'],'fresh_conditional_probes':[r for r in results['delivered']['summary'] if r['subgroup'] in ['P','R'] and r['cue'] in ['range6','eliminate_singleton','constant_then_max','constant_then_min']]}))
