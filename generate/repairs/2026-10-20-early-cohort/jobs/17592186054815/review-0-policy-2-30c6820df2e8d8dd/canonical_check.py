import sys,json,pathlib
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(E.parent/'workspace'));import generator as g
r=g.generate('Q-',[g.number('sqrt',-1,3),g.number('decimal',-2),g.number('integer',0),g.number('sqrt',-1,4)],seed=13139)
(E/'canonical-records.json').write_text(json.dumps([r],indent=2)+'\n')
checks=[];expected=[False,True,False,True,False]
for i,f in enumerate(r['question'][':question/answer-fields']):
 for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if (a[':answer/value']=='true')==expected[i] else 'rejected','purpose':'Canonical e-13139 independently derived: -0.2 and -sqrt4 only'})
cases=[{'label':'canonical-e-13139','record':r,'checks':checks}]
(E/'canonical-grader-input.json').write_text(json.dumps(cases,indent=2)+'\n')
(E/'canonical-checks.json').write_text(json.dumps({'source_id':'ce8a56c1-709e-50e8-ac10-d3f92bf15db0','displayed_numbers':[f[':answer-field/key'] for f in r['question'][':question/answer-fields'][:4]],'expected_members':['-0.2','-sqrt4'],'observed_members':[f[':answer-field/key'] for f in r['question'][':question/answer-fields'] if f[':answer-field/correct'][1]==next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']=='true')],'gap':'Canonical source has no captured answer-field bank; independently constructed checkbox display verifies numeric classification, not exact response-bank replay.'},indent=2)+'\n')
print('Canonical source values instantiated; two correct numeric members.')
