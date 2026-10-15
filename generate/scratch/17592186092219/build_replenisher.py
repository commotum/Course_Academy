from pathlib import Path
H=Path(__file__).resolve().parent
base=(H.parent/'17592186087886/replenish.py').read_text()
base=base.replace("HERE / 'validate.py'","HERE / 'validation_support.py'")
base=base.replace('KP = g.KP_ID',"KP = g.KP[':db/id']")
base=base.replace("'1c0cdbe168dd474bc501573c04fd6e708d8f2e89a0d74434a30133322053144a'","'8476bd9aee7c8f77a73c15729045ff22a479566f11390dcd3a7ce2e67c390e03'")
base=base.replace("NATIVE = Path((HERE/'reference/learning-binary.txt').read_text())","NATIVE = ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'")
base=base.replace("elif level not in available:reason='Unrated or unsupported difficulty'","elif level not in available:reason='Unrated or unsupported difficulty'\n        elif q.get(':question/math-academy-id')=='q-276838':reason='Source solution incorrectly calls a point on the positive x-axis first-quadrant; source preserved unchanged'")
base=base.replace('try:v.solution_check(q)',"try:v.verify({'knowledge_point':{'db_id':KP,'id':str(g.KP[':knowledge-point/id']),'title':g.KP[':knowledge-point/title']},'question':normalize(q)})")
base=base.replace("return v.fingerprint(q[':question/problem'])","return v.fingerprint(q)")
base=base.replace("assert fingerprint(q) == rec['generation']['parameter_fingerprint']","assert fingerprint(q) == fingerprint(rec['question'])")
base=base.replace("'shortage_remaining':{**remaining,'moderate_nominal_unsupported':5,'hard_nominal_unsupported':5}","'shortage_remaining':remaining")
base=base.replace("HERE/'validation.json'","HERE/'release-validation.json'")
base=base.replace("'note':'Seven complete easy source practice questions validated mathematically and with actual radio grading. Only add fresh distinct ODE tasks if the current reserve is below five; retain all source content and learner history. The bounded easy generator is registered; absent moderate/hard source evidence leaves both bands unsupported by this package.'", "'note':'Positive-scaling source-bank profiles replay all source options. Easy is explicitly authored from the frozen curriculum. All original questions, incomplete unrated records, canonical example and learner history are preserved. Only fresh mathematical tasks replenish the reserve.'")
base=base.replace("(HERE/'validation.json')","(HERE/'release-validation.json')")
base=base.replace("g.KP_UUID", "str(g.KP[':knowledge-point/id'])")
start=base.index('        # The canonical uses')
end=base.index('        supplied_path=',start)
base=base[:start]+'''        canonical_question=copy.deepcopy(kp[':knowledge-point/canonical-example'])
        canonical_question[':question/problem']=canonical_question[':question/problem'].replace(r'\\left','').replace(r'\\right','').replace(r'\\dfrac',r'\\frac')
        used.add(fingerprint(canonical_question))
'''+base[end:]
base=base.replace("local=g.batch('easy',42,int(JOB.name[:8],16)) if any(needed.values()) else []", "local=[]\n        for level in g.SUPPORTED_LEVELS:\n            if needed[level]:\n                for rec in v.finite_records(level):\n                    if fingerprint(rec['question']) not in used:\n                        local.append(rec)\n                        if sum(r['question'][':question/difficulty'].endswith('/'+level) for r in local)>=needed[level]:break")
base=base.replace("[str(HERE/'check-engine')", "[str(ROOT/'generate/runs/current/check-engine')")
base=base.replace("'homogeneous-ode-inventory-17592186087886-'","'point-information-inventory-17592186092219-'")
# Actual grading of every usable pool question, not just new content.
needle="    save(path/'available-counts.json',counts)"
base=base.replace(needle,"""    fixtures=[]
    for level,rows in available.items():
        for q in rows:
            rec={'knowledge_point':{'db_id':KP,'id':str(g.KP[':knowledge-point/id']),'title':g.KP[':knowledge-point/title']},'question':normalize(q),'generation':{'template':q.get(':question/math-academy-id','committed-generated')}}
            fixtures.append({'label':str(q[':question/id']),'record':rec,'checks':v.checks(rec)})
    save(path/'available-native-input.json',fixtures)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True)
"""+needle)
(H/'replenish.py').write_text(base)
