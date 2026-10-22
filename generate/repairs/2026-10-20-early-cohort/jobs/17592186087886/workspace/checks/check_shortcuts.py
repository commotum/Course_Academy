"""Strict current-generator regression: a unique-shortest-answer cue must not solve a whole family."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('current_generator',ROOT/'17592186087886.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from math_reader import rate,prompt_rhs,x,y,v
import sympy as sp
SOURCE=ROOT.parent/'source';REPO=Path('/home/jake/Developer/Course_Academy')
def size(value):return len(re.sub(r'\\(?:left|right|operatorname)|[{}\s]|\u2061','',value))
def main():
    records=[g.generate('easy',37,'q-90600',{'k':k}) for k in [1,2,4,5,6]]
    path=ROOT/'evidence/shortcut-current-records.json';path.write_text(json.dumps(records,indent=2)+'\n')
    command=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(path),'--source',str(SOURCE/'source.json'),'--inventory',str(SOURCE/'inventory.json'),'--difficulty','easy','--output',str(ROOT/'evidence/shortcut-delivery'),'--asset-root',str(ROOT/'evidence'),'--math-root','/media/jake/SSD/EDB/math']
    subprocess.run(command,check=True,capture_output=True,text=True)
    accepted=json.loads((ROOT/'evidence/shortcut-delivery/accepted.json').read_text());assert len(accepted)==5
    witnesses=[]
    for r in accepted:
        q=r['question'];choices=q[':question/answer-fields'][0][':answer-field/choices'];sizes=[size(a[':answer/value']) for a in choices];m=min(sizes)
        if sizes.count(m)!=1:continue
        selected=choices[sizes.index(m)];expected=(prompt_rhs(q[':question/problem']).subs(y,v*x)-v)/x
        independently_correct=sp.cancel(rate(selected[':answer/value'])-expected)==0
        witnesses.append({'question_id':q[':question/id'],'parameters':r['generation']['parameters'],'chosen_by':'unique shortest mathematical text, without prompt inspection','selected_value':selected[':answer/value'],'math_correct':independently_correct})
    persists=len(witnesses)==5 and all(w['math_correct'] for w in witnesses)
    result={'status':'fail' if persists else 'pass','current_generator_tested':True,'template':'q-90600','input_records':len(records),'delivered_records':len(accepted),'shortcut_hits':sum(w['math_correct'] for w in witnesses),'witnesses':witnesses,'delivery_command':command,'construction_change':'The authored profile chooses a surviving linear role as well as k; retained exact seed/k calls now include shift=2. Separate check_roles.py tests every shift including zero, every family and both delivery stages. Source evidence is unchanged.'}
    (ROOT/'evidence/shortcut-regression.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','template','input_records','delivered_records','shortcut_hits')}))
    return 1 if persists else 0
if __name__=='__main__':sys.exit(main())
