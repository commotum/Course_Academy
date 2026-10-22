import sys,json,pathlib,importlib.util
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;W=E.parent/'workspace'
s=importlib.util.spec_from_file_location('g',W/'17592186119847.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
base=next(r for r in json.load(open(E/'source-replay-records.json')) if r['generation']['bank_profile']=='q-79409')
p={**base['generation']['parameters'],'rows':4};out=[]
for profile in g.PROFILES['moderate']:
 try:r=g.generate('moderate',17,parameters=p,bank_profile=profile);res='accepted'
 except ValueError as error:res=str(error)
 out.append({'profile':profile,'result':res})
assert all(x['result']=='Parameters outside supported profile domain' for x in out)
json.dump({'before':base,'after_parameters':p,'expected':'rank remains 7-3=4; rows=4 is feasible, prompt and explanation should update only row dimension','observed':'No after record can be constructed under any bank profile','attempts':out,'command':sys.executable+' -B audit-row-counterfactual.py'},open(E/'row-counterfactual.json','w'),indent=2)
print('Feasible irrelevant row change 5 -> 4 rejects the item under all profiles.')
