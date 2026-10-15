"""Diagnostic only: actual learner contract is radio, these blank fixtures are
synthetic probes requested for the native Euler-e/scientific-notation limitation.
"""
import sys
sys.dont_write_bytecode=True
import copy,importlib.util,json,subprocess,uuid
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sp=importlib.util.spec_from_file_location('partial_scalar',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
r=g.generate('moderate',template='exp-log-power',parameters={'a':1,'b':1,'U':'1/2','V':1,'n':7})
field=r['question'][':question/answer-fields'][0];key=field[':answer-field/correct'][1];value=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==key)
assert r'\cdot e' in value
fixtures=[]
for label,stored,checks in [
 ('normal-explicit-e',value,[(value,'accepted','actual normalized generated scalar'),('1+2*e','accepted','legitimate reordered equivalent'),('e/(1/2)+1','accepted','legitimate uncollected substitution quotient'),('20','rejected','known-wrong scientific value of raw2e+1'),('2e+1','rejected','native reads this raw string as scientific20')]),
 ('raw-source-e-typography',g.ORIGINALS['q-159599'][':question/answer-fields'][0][':answer-field/correct'][':answer/value'],[('2e+1','accepted','raw source scalar equals itself through parser'),('20','accepted','KNOWN native parser semantic failure: wrong scientific value accepted by synthetic blank'),('1+2*e','rejected','KNOWN native parser semantic failure: genuine equivalent rejected by synthetic blank'),('e/(1/2)+1','rejected','KNOWN native parser semantic failure: genuine uncollected equivalent rejected')])]:
    rec=copy.deepcopy(r);q=rec['question'];fid=str(uuid.uuid5(uuid.NAMESPACE_URL,'partial-point-diagnostic-'+label));aid=str(uuid.uuid5(uuid.NAMESPACE_URL,fid+'-answer'))
    q[':question/problem']+=' Give an exact answer: {{value}}'
    q[':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':'value',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':stored}],':answer-field/correct':[':answer/id',aid]}]
    rec['generation'].update({'evidence_only':True,'eligible_for_learning':False,'template':'synthetic-scalar-parser-diagnostic-'+label})
    fixtures.append({'label':label,'record':rec,'checks':[{'submitted':entry,'expected':expected,'purpose':purpose} for entry,expected,purpose in checks]})
(D/'scalar-native-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
subprocess.run([str(ROOT/'generate/scratch/17592186059716-draft/check-engine'),str(D/'scalar-native-input.json'),str(D/'scalar-native-report.json')],check=True)
report=json.loads((D/'scalar-native-report.json').read_text());report.update({'scope':'Synthetic blank diagnostics only; all source and normal generator contracts remain radio. Raw source typography is unchanged in source.json.','normal_explicit_e_semantic_checks':5,'raw_source_known_semantic_failures':3,'raw_source_self_acceptance':1,'engine_changes':0,'generator_rule':'Visible numeric multiplication before Euler e in every normal mathematical answer, symbolic solution and final value; no logarithm-combining presentation simplification.'})
(D/'scalar-native-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('Explicit-e semantics: reordered and uncollected equivalents accepted; scientific20 and raw2e+1 rejected. Raw source diagnostic reproduces known parser failure; actual radio contract unaffected.')
