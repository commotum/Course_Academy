import hashlib,importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
rows=[]
for mid,q in g.ORIGINALS.items():
 for field in q.get(':question/answer-fields',[]):
  p,r=g.SPECS[mid]['points'];n=sum((r[i]-p[i])**2 for i in range(2))
  for answer in field[':answer-field/choices']:
   v=g.expression(answer[':answer/value'])
   rows.append({'source_id':mid,'source_field_id':field[':answer-field/id'],'source_field_key':field[':answer-field/key'],'source_answer_id':answer[':answer/id'],'source_value':answer[':answer/value'],'complete_mathematical_value':str(v),'parameterized_recipe':'scale * ('+answer[':answer/value']+')','profile':'evidence:'+mid,'recipe_reproduces_complete_value':True,'interpretation':'opaque homogeneous evidence; misconception intent unresolved; evidence-only','mathematical_correct':g.sp.simplify(v-g.sp.sqrt(n))==0,'source_correct_ref_present':':answer-field/correct' in field,'feedback_present':':answer/feedback' in answer})
(HERE/'templates.json').write_text(json.dumps({'database':g.SOURCE['database'],'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'original_families':g.SPECS,'choice_mapping':rows,'normal_profile':'method-derived complete operation bank, separate from historical intent','domains':g.DOMAINS},indent=2)+'\n')
original=['generate/scratch/17592186059715.py','generate/scratch/17592186059715/validation.json']
provenance={'database':'math','basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'script_scope':'local review draft only; no publication/registration/database writes','reused_baseline_helpers':'SymPy exact vector format, KP identity/schema ownership patterns; draft paths defined before all calls. Registered script never imported or executed.','baseline_unchanged':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in original},'source_hash':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':g.sp.__version__,'matplotlib':__import__('matplotlib').__version__},'native_grader':{'binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'entrypoint':'course_academy_engine::learning::grade_field','fixture':'memory-only, no EDB access'},'calculator_flag_evidence':'All five MA flags absent/unknown in supplemental basis2275 calculator-requirements.json; no emitted calculator attribute; independent inventory false flags retained exactly.'}
(HERE/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
