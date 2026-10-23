"""Strict regression: exits nonzero while this generated bank reveals its key.
Run with the job Python. Outputs remain under this file's evidence directory.
"""
import sys,os,pathlib,importlib.util,json,re
E=pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode=True
os.environ['MPLCONFIGDIR']=str(E/'mpl-cache')
entry=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else E.parent/'workspace/17592186129197.py'
spec=importlib.util.spec_from_file_location('tested_generator',entry);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
g.ROOT=E/'runtime/17592186129197'
r=g.generate('easy',8191,template='simple',parameters={'a':1,'h':1,'k':0})
def predict(q):
 bank=q[':question/answer-fields'][0][':answer-field/choices']
 norm=lambda z:re.sub(r'\s+','',z)
 neg={norm(a[':answer/value'])[1:] for a in bank if norm(a[':answer/value']).startswith('-')}
 candidates=[a[':answer/id'] for a in bank if norm(a[':answer/value']) in neg]
 return candidates[0] if len(candidates)==1 else None
q=r['question'];key=q[':question/answer-fields'][0][':answer-field/correct'][1]
# Negative control proves the detector is not a constant correct-key lookup.
import copy
control=copy.deepcopy(q)
for a in control[':question/answer-fields'][0][':answer-field/choices']:
 if a[':answer/value'].lstrip().startswith('-'):a[':answer/value']='-7'
assert predict(control) is None
(E/'regression-record.json').write_text(json.dumps(r,indent=2))
result={'entrypoint':str(entry),'seed':8191,'parameters':{'a':1,'h':1,'k':0},'strategy':'Choose the unique positive choice whose value occurs with a leading minus sign elsewhere in the bank.','predicted':predict(q),'correct':key,'negative_control_passed':True,'shortcut_blocked':predict(q)!=key}
(E/'regression-result.json').write_text(json.dumps(result,indent=2))
assert result['shortcut_blocked'], 'INCIDENTAL SHORTCUT: signed answer-pair reveals 4/3 without reading the prompt; revise the bank construction rule.'
