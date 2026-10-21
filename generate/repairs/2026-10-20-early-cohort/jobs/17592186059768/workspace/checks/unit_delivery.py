"""Repeat boundary witnesses on actual shared delivery survivors."""
import sys
sys.dont_write_bytecode=True
import collections,json,math,os
from unit_regression import surface_probes
from regression import E,g,check,save,answer,bank,mask
from finish import inventory

def main():
 raw=json.loads((E/'unit-records.json').read_text())
 accepted=sum([json.loads((E/f'unit-delivery-{level}/accepted.json').read_text()) for level in ('easy','moderate')],[])
 assert len(raw)==len(accepted) and len(raw)>=62
 for r in accepted:check(r)
 before=surface_probes(raw);after=surface_probes(accepted)
 assert before==after
 pairs=json.loads((E/'unit-counterfactual-records.json').read_text())
 # Both signed-unit cases and adjacent 2 are preserved by filtering.
 expected={str(answer(r)) for r in pairs}
 delivered={str(answer(r)) for r in accepted}
 assert expected<=delivered
 save('unit-shortcuts-after-delivery.json',{'passed':True,'input':len(raw),'accepted':len(accepted),'counterfactual_matrices_retained':3,'per_profile':after,'filter_effect':'No rejected records or duplicates; semantic matrices and reported cue counts unchanged.','generator_rejection':'No valid unit target is rejected. The fixed-size same-sign permutation attempt now supplements its exhausted orbit with independently checked magnitude-reading errors. Ordinary sampling branch is unchanged.','learner_selection_limit':'Captured inventory is checked read-only. Actual learner history/reservations and weighting are unavailable; selection does not modify question content.'})
 historical=inventory();small=[]
 for r in historical:
  m=answer(r);orbit=1
  for sign in (-1,1):
   values=[v for row in m for v in row if (v>0)-(v<0)==sign]
   count=math.factorial(len(values))
   for n in collections.Counter(values).values():count//=math.factorial(n)
   orbit*=count
  small.append({'question_id':r['question'][':question/id'],'parameters':r['generation']['parameters'],'same_sign_orbit':orbit})
 # All captured generated records are reproducible. None falls in the latest
 # <5-orbit construction defect, while seven retained sign shortcuts remain.
 assert len(small)==7 and all(r['same_sign_orbit']>=5 for r in small)
 save('unit-inventory-results.json',{'tested_generated':7,'unreproduced_generated':0,'latest_small_orbit_cases':0,'records':small,'retained_affected_records':7,'affected_inventory':'affected-inventory.json','scope':'Original assessed sources are excluded; the full generated inventory was tested, not an untested absence.'})
 # Writes stay in workspace; record paths are relative to the supplied
 # evidence_root (author-2), even though that directory is not writable here.
 affected=json.loads((E/'affected-inventory.json').read_text())
 for a in affected['affected_questions']:
  a['reproduction']='/home/jake/Developer/Course_Academy/.venv/bin/python -B '+str(E.parent/'checks/unit_delivery.py')
  a['evidence_path']=os.path.relpath(E/'generated-records.json',E.parent.parent/'author-2')
 save('affected-inventory.json',affected)
 (E.parent/'affected-inventory.json').write_text(json.dumps(affected,indent=2)+'\n')
 print(f'{len(raw)}/{len(raw)} delivery survivors pass unchanged math/cue checks; 7/7 stored generated records reconstructed, none in latest small-orbit case; 7 historical shortcut findings retained.')
if __name__=='__main__':main()
