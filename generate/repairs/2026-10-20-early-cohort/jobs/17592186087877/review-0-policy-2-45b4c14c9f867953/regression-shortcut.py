"""Strict repair acceptance test. Current generator MUST fail this assertion.
Run with the job Python; optionally pass a replacement package entrypoint.
This strategy reads only answer choices. It never reads the ODE or key to choose.
"""
import argparse
import audit as a
p=argparse.ArgumentParser();p.add_argument('--entrypoint',default=str(a.PKG/'17592186087877.py'));args=p.parse_args()
g=a.module(args.entrypoint)
r=g.generate('easy',seed=99017,template='signed_constant_power',parameters={'a':'1','n':3})
q=r['question'];hits=a.cue(q)
a.save('minimal-failing-record.json',[r])
a.save('regression-shortcut-result.json',{'command':f'/home/jake/Developer/Course_Academy/.venv/bin/python regression-shortcut.py --entrypoint {args.entrypoint}','parameters':{'difficulty':'easy','seed':99017,'template':'signed_constant_power','a':'1','n':3},'strategy':'Select an exponential factor whose reciprocal and square also occur among the choices, without reading the prompt.','predicted_choice_ids':hits,'correct_choice_id':a.correct_id(q),'defect_reproduced':hits==[a.correct_id(q)],'acceptance_requirement':'The family-wide bank-construction rule must not uniquely identify the correct candidate by this answer-only signature.'})
assert hits != [a.correct_id(q)], 'INCIDENTAL SHORTCUT: choice with factor e^x is uniquely identified by offered factors e^-x and e^2x; ODE inspection is unnecessary.'
