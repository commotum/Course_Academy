import json,pathlib,sys,os,importlib.util,random
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'workspace';sys.dont_write_bytecode=True;sys.path.insert(0,str(P));os.environ.update(COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(E/'assets'),MPLCONFIGDIR=str(E/'mplconfig'))
spec=importlib.util.spec_from_file_location('boundary_generator',P/'17592186172039.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Retain a valid all-false mathematical case as both an explicit rejection and selectable None case.
p={'c':1,'a':1,'b':1,'quadrants':[1,2,3],'claims':[-1,1,-1]}
try:g.generate('moderate',seed=441,parameters=p,include_none=False)
except ValueError as e:rejection={'parameters':p,'include_none':False,'exception':str(e),'expected':'explicit empty selection cannot be silently resampled'}
else:raise AssertionError('Unselectable empty response accepted')
seed=next(s for s in range(101,151) if g.truth_mask(g.sample('moderate',random.Random(s),'authored_sign_errors'))==0)
r=g.generate('moderate',seed=seed,include_none=False);assert r['generation']['seed']!=seed and r['generation']['truth_mask']!=0;assert r==g.generate('moderate',seed=seed,include_none=False)
with_none=g.generate('moderate',seed=seed);assert with_none['generation']['seed']==seed and with_none['generation']['truth_mask']==0
canonical=g.generate('moderate',seed=881,parameters={'c':-2,'a':1,'b':1,'quadrants':[2,3,4],'claims':[-1,-1,1]},include_none=False);assert canonical['generation']['truth_mask']==6
result={'explicit_rejection':rejection,'seeded_retry':{'initial_seed':seed,'returned_seed':r['generation']['seed'],'returned_truth_mask':r['generation']['truth_mask'],'deterministic':True,'record':r},'same_initial_seed_with_default_none':with_none,'canonical_source':{'source_id':'0444de80-19f1-5251-b159-5dc55756bb19','record':canonical,'ordinary_truths':[False,True,True],'bank_limit':'Canonical-example object lacks full bank; three checkbox true/false banks are inferred from the eight current source practice contracts. Mathematics and solution sign progression agree.'}}
(E/'boundary-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('Explicit all-false rejection, deterministic resampling, default preservation and canonical sign case passed.')
