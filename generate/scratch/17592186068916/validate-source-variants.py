"""Independently read complete observed-bank variants through the public API."""
from pathlib import Path
import importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).parent
def mod(n,p):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=mod('kp_source_variants',HERE.with_suffix('.py'));v=mod('kp_source_variant_readback',HERE/'readback.py')
records=[]
for sid,c in g.CONFIG.items():
 if sid=='q-113983':continue
 for seed in (321,654):
  r=g.generate(c[0],seed,template=sid,profile='observed');g.fmt.validate_generated_record(r);v.validate(r['question']);v.structure(r['question'],sid);records.append(r)
(HERE/'observed-bank-variants.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
(HERE/'observed-bank-variant-validation.json').write_text(json.dumps({'status':'passed','records':len(records),'source_profiles':9,'independently_read_prompt_substitution_differential_bounds_ordered_stages_full_bank':True,'excluded_reference_only':['q-113983']},indent=2)+'\n')
print('Observed-bank changed-parameter public-output checks passed:',len(records))
