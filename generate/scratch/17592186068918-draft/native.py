"""Frozen native harness checks, with explicit substantive parser limitations."""
import importlib.util,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('private_quotient_native_g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def native_case(r,label):
    f=r['question'][':question/answer-fields'][0];ref=f.get(':answer-field/correct')
    if ref is None:return None
    checks=[]
    if f[':answer-field/type'].endswith('radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ref[1] else 'rejected','purpose':'owned radio choice ID; displayed mathematics checked separately'} for a in f[':answer-field/choices']]
        checks.extend([{'submitted':value,'expected':'unresolved','purpose':purpose} for value,purpose in [('999999','foreign numerical fixture ID: selected answer does not belong to this field'),('not-an-id','malformed radio input: answer ID expected'),(f[':answer-field/choices'][0][':answer/value'],'mathtext is not an owned radio answer ID')]])
    else:
        t=r['generation']['template'];m=r['generation']['parameters']['m'];raw=r['generation']['profile']=='observed'
        correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ref[1]);upper,lower=(6,5) if t=='q-350901' else (4,3)
        equivalent=str(m)+r'(\ln('+str(upper)+r')-\ln('+str(lower)+'))'
        checks=[{'submitted':a[':answer/value'],'expected':('rejected' if raw and a[':answer/id']!=ref[1] else 'accepted'),'purpose':'canonical stored answer; raw q350904 equivalent legacy alias rejected by round wording form restriction'} for a in f[':answer-field/choices']]
        checks.extend([{'submitted':equivalent,'expected':'rejected' if raw else 'unresolved','purpose':'genuine mathematically equivalent endpoint difference: raw round wording form restriction; normal symbolic-log limitation'}, {'submitted':str(m)+r'(\ln('+str(upper)+r')+\ln('+str(lower)+'))','expected':'rejected','purpose':'ordinary wrong endpoint addition'}, {'submitted':'0','expected':'rejected','purpose':'ordinary wrong zero'}, {'submitted':'('+correct+')+1','expected':'rejected','purpose':'ordinary wrong offset'}])
    return {'label':label,'record':r,'checks':checks}

def main():
    inputs=[]
    for level in g.LEVELS:
        for t,pr,params in g.domains(level):
            if pr=='observed' and params['m']!=1:continue
            r=g.generate(level,73,t,parameters=params,profile=pr);row=native_case(r,t+'-'+pr+'-'+str(params))
            if row:inputs.append(row)
    (HERE/'native-input.json').write_text(json.dumps(inputs,indent=2))
    subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
if __name__=='__main__':main()
