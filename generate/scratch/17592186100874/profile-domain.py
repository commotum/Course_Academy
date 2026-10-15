"""Bounded observed-profile domains and actual selected-profile accounting."""
import importlib.util,json,sys,collections
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('profile_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
proofs=[];total=0
for t in ('q-49610','q-49613','q-49622','q-17103'):
 source=g.allowed(t,g.defaults(t));params=[]
 if t=='q-17103':
  params=[dict(a=a,b=1,c=c,l='0',h='2' if a==1 else '1') for a in (1,8) for c in range(1,10)]
 else:
  params=[dict(a=a,b=b,c=1,l=str((source['L']-b)/a),h=str((source['H']-b)/a)) for a in range(2,11) for b in range(-6,8)]
 for v in params:
  m=g.allowed(t,v);assert m['L']==source['L'] and m['H']==source['H']
  bank,names=g.recipes(t,m,'observed');g.check_bank(bank,m['A']-m['B'])
  originals,_=g.recipes(t,source,'observed');ratio=m['k']/source['k']
  assert all(g.s.simplify(z-ratio*y)==0 for z,y in zip(bank,originals))
 total+=len(params);proofs.append({'template':t,'selected_complete_profile':'observed','parameter_instances':len(params),'original_transformed_bounds':[str(source['L']),str(source['H'])],'all_options_scaled_one_to_one':True,'unique_correct_and_no_collisions':True,'zero_shift_cases':sum(v['b']==0 for v in params)})
records=json.loads((H/'review-records.json').read_text());selected=collections.Counter((r['generation']['template'],r['generation']['profile']) for r in records)
for t in g.SPECS:
 field=g.SPECS[t][3]
 assert selected[(t,'blank' if field=='blank' else 'observed')]>0
 if field=='radio':assert selected[(t,'method-scaled')]>0
assert selected[('q-17103','method-unit')]>0
report={'bounded_instances':total,'observed_domains':proofs,'actual_selected_profiles':[{'template':t,'profile':profile,'rendered_instances':n} for (t,profile),n in sorted(selected.items())],'conclusion':'All supported complete source profiles are eligible and selected. Numeric profiles use exact multiplier homogeneity at fixed transformed endpoints; no arbitrary interval interpolation. Authored profiles remain separately labeled.'}
(H/'profile-coverage.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
