"""Grade the captured rated source records with their original mathematical strings."""
import copy,importlib.util,json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('v',P/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
out=[]
for source in v.g.QS.values():
 if not source.get(':question/difficulty'):continue
 v.validate_existing(source)
 q=copy.deepcopy(source);q[':question/difficulty']=q[':question/difficulty'][':db/ident'];f=q[':question/answer-fields'][0];f[':answer-field/type']=f[':answer-field/type'][':db/ident'];correct=f[':answer-field/correct'];f[':answer-field/correct']=[':answer/id',correct[':answer/id']]
 for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
 if f[':answer-field/type'].endswith('/radio'):
  checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==correct[':answer/id'] else 'rejected',purpose='Original field-owned source bank') for a in f[':answer-field/choices']]
 else:
  val=correct[':answer/value'];checks=[dict(submitted=val,expected='accepted',purpose='Original canonical value'),dict(submitted='('+val+')*2/2',expected='accepted',purpose='Equivalent original blank'),dict(submitted='('+val+')+1',expected='rejected',purpose='Incorrect original blank')]
 out.append(dict(label=q[':question/math-academy-id'],record=dict(question=q,knowledge_point=dict(title=v.g.TITLE),generation=dict(template='original-source')),checks=checks))
v.save(P/'source-native-input.json',out)
subprocess.run([str(P/'check-current-engine'),str(P/'source-native-input.json'),str(P/'source-native-report.json')],check=True)
