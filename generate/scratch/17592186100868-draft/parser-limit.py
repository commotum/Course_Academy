"""Preserve a real native parser limitation and verify the generator's disambiguation."""
import sys
sys.dont_write_bytecode=True
import copy,importlib.util,json,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[2]
spec=importlib.util.spec_from_file_location('draft100868',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
r=g.generate('hard',template='q-318591',parameters={'scales':{'m':1,'n':1,'p':1},'names':{'m':'m','n':'n','p':'l'}})
f=r['question'][':question/answer-fields'][1];a=f[':answer-field/choices'][0];assert a[':answer/value']==r'l\cdot n'
fixed={'label':'explicit l-times-n polynomial product','record':r,'checks':[{'field_index':1,'submitted':r'l\cdot n','expected':'accepted','purpose':'supported disambiguated product'},{'field_index':1,'submitted':'(m)(1)+(n)(l)+(-m)(1)','expected':'accepted','purpose':'genuine uncollected equivalent'}]}
bad=copy.deepcopy(r);bad['question'][':question/answer-fields'][1][':answer-field/choices'][0][':answer/value']='ln'
raw={'label':'unspaced ln is reserved by native parser','record':bad,'checks':[{'field_index':1,'submitted':'ln','expected':'unresolved','purpose':'reproduce reserved-function parser limitation'}]}
(D/'parser-limit-input.json').write_text(json.dumps([fixed,raw],indent=2)+'\n');subprocess.run([str(R/'generate/scratch/17592186059716-draft/check-engine'),str(D/'parser-limit-input.json'),str(D/'parser-limit-report.json')],check=True)
