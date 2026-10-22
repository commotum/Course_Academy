import sys,json,importlib.util,pathlib
sys.dont_write_bytecode=True
w=pathlib.Path(__file__).resolve().parent.parent/'workspace'
s=importlib.util.spec_from_file_location('g',w/'17592186119847.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
p={'name':'A','rows':4,'columns':7,'count':3,'kind':'non-pivot'};out=[]
for profile in g.PROFILES['moderate']:
 try:g.generate('moderate',17,parameters=p,bank_profile=profile);result='accepted'
 except ValueError as e:result=str(e)
 out.append({'profile':profile,'parameters':p,'recipe':g.recipes(profile,p),'result':result})
assert all(x['result']=='Parameters outside supported profile domain' for x in out)
json.dump({'source_id':'7cce27e9-e2b2-599c-9f4e-437caf1a23ae','expected_rank':4,'source_bank':'absent; no particular bank required','complete_valid_example_bank':[2,3,4,5,7],'cases':out,'reproduction':sys.executable+' -B audit-canonical.py'},open(pathlib.Path(__file__).resolve().parent/'canonical-rejection.json','w'),indent=2)
print('Canonical source stem rejected by all six moderate profiles.')
