"""Independent boundary checks using the private rendered-math validator."""
import sys
sys.dont_write_bytecode=True
import validate as v
import json,subprocess
counts={};boundary=[];checked=[]
for sid,t in v.g.PROFILES.items():
 cs=v.g.candidates(sid);bs=sorted({p[1]for p in cs});maxscale=[p for p in cs if p[1]==bs[-1]]
 counts[sid]={'eligible_complete_profile_tuples':len(cs),'denominator_values':bs,'numerators':sorted({p[0]for p in cs})}
 for p in [maxscale[0],maxscale[-1]]:
  r=v.g.generate(t['difficulty'],2275,sid,p);v.check(r);boundary.append(v.engine_item('boundary '+sid+' '+str(p),r));checked.append({'profile':sid,'parameters':p})
v.save('boundary-native-input.json',boundary)
subprocess.run([str(v.HERE/'check-engine'),str(v.HERE/'boundary-native-input.json'),str(v.HERE/'boundary-native-grading.json')],check=True)
v.save('boundary-checks.json',{'passed':True,'rendered_instances':len(boundary),'tested':checked,'complete_profile_candidate_inventory':counts,'hard_tuples':17*8*11,'hard_boundaries_checked_in_main_validation':[[1,2,2],[17,9,12]]})
print('Boundary rendered/native checks',len(boundary))
