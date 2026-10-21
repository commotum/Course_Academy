"""Reproduce the positional strategy before/after on the same 24 seeds."""
import pathlib,sys,importlib.util
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r',ROOT/'checks/test_role_exchange.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
reports={}
for label,entry in [('before',ROOT/'evidence/generator-before.py'),('after',ROOT/'17592186229165.py')]:
 g=r.module(entry);records=[g.generate('hard',template='mixed',seed=i) for i in range(67031,67055)]
 report=r.coverage(records);reports[label]=report;r.save(ROOT/'evidence','shortcut-'+label+'-sampler.json',report)
 if label=='before':assert report['positions']=={'1':24}
 else:
  assert set(report['positions'])=={'1','2'}
  for cue,counts in report['cue_groups'].items():assert set(counts)=={'1','2'},('Incidental predictor',cue,counts)
print('Before: last term ordinary 24/24; after: '+str(reports['after']['last_term_ordinary_shortcut']['successes'])+'/24. Both roles occur in every tested sign/rate-order cue group.')
