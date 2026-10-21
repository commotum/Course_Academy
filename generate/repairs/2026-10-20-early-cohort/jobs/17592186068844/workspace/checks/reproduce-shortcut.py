"""Strict regression: exits 1 when choices alone expose the correct relation.

Run with the context Python: python reproduce-shortcut.py
The only prompt-generation parameters are exp_linear, h=k=0, seed=101.
The attack itself reads neither the ODE nor generation/solution metadata.
"""
import json
import audit as a
r=a.g.generate_easy(seed=101,template='exp_linear',parameters={'h':0,'k':0})
picks=a.shortcut(r)
exposed=picks==[a.answer_id(a.field(r))]
out={'command':str(a.PY)+' reproduce-shortcut.py','record':r,
     'strategy':'Among choices with the same left side, choose L=R+C when both L=-R+C and L=2R+C are also offered.',
     'selected_answer_ids':picks,'shortcut_matches_key':exposed,
     'expected':'The answer bank must not uniquely expose its keyed equation through the fixed R,-R,2R construction.',
     'passed':not exposed}
(a.ROOT/'minimal-failure.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':not exposed,'shortcut_matches_key':exposed,'evidence':'minimal-failure.json'}))
raise SystemExit(1 if exposed else 0)
