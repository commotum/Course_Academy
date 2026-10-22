"""Recreate bounded affected-family probes and delivery inputs from the candidate."""
import json
from check_repair import E,g,save

def main():
    probes=json.loads((E/'probe-records.json').read_text())
    restrictions=json.loads((E/'root-cause/restriction-records.json').read_text())
    requested=g.batch('easy',5,0);save('root-cause/requested-five.json',requested)
    controls=[]
    for level,profiles in g.PROFILES.items():
        for profile in profiles:
            for seed in (0,1,2,3):
                for count in (2,3,4):
                    p=dict(name='A',rows=6,columns=8,count=count,kind='pivot' if level=='easy' else 'non-pivot')
                    controls.append(g.generate(level,seed,parameters=p,bank_profile=profile))
    save('root-cause/collision-probes.json',controls)
    for level in ['easy','moderate']:
        records=[r for r in probes+restrictions+controls+requested if r['question'][':question/difficulty'].endswith('/'+level)]
        save('root-cause/'+level+'-delivery-input.json',records)
        for profile in g.PROFILES[level]:
            group=[r for r in records if r['generation']['bank_profile']==profile and r['generation']['bank_extension'].startswith('collision')]
            if group:save('root-cause/isolated-'+profile+'.json',group)
    print(json.dumps({'cue_controls':len(controls),'requested':len(requested)}))

if __name__=='__main__':main()
