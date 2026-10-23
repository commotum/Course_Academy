"""Retained cf8dcbf41937f26e0c48: current generator, visible math, real grading."""
import json, os, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
from visible_math import g, s, parse, key, mathcheck
W = Path(__file__).resolve().parent
REPO = next(p for p in W.parents if (p/'generate/pipeline/check_delivery.py').is_file())
ENGINE = REPO/'generate/runs/current/check-engine'

def save(name, data):
    (W/name).write_text(json.dumps(data, indent=2))

def run(args):
    result = subprocess.run([str(x) for x in args], capture_output=True, text=True)
    with (W/'regression-commands.jsonl').open('a') as f:
        f.write(json.dumps({'command':[str(x) for x in args], 'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})+'\n')
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)

def cases(records):
    out=[]
    for r in records:
        # Read the rendered prompt, independently differentiate it and check the key/solution.
        mathcheck(r)
        m=parse(key(r))
        valid=str(m).replace('**','^')
        checks=[{'submitted':v,'expected':e} for v,e in [
            (key(r),'accepted'), (valid,'accepted'),
            ('-('+valid+')','rejected'), ('2*('+valid+')','rejected'),
            ('('+valid+')*exp(1/2)','rejected')]]
        if r['generation']['parameters']=={'a':1,'b':1,'c':1,'u':2}:
            # Exact retained counterexample and equivalent reductions/split exponent.
            checks += [{'submitted':v,'expected':'accepted'} for v in [
                r'\frac{8}{5\sqrt{5}\exp(1/2)}',
                '8/(5*sqrt(5)*exp(1/2))',
                '8*exp(-1/2)/(5*sqrt(5))',
                '8/(5*sqrt(5)*exp(2/4))',
                '8*exp(-1/6)*exp(-1/3)/(5*sqrt(5))']]
            checks += [{'submitted':v,'expected':'rejected'} for v in [
                '8/(5*sqrt(5)*exp(-1/2))',
                '8/(5*sqrt(5)*exp(1/3))']]
        out.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
    return out

def main():
    ps=[dict(a=1,b=1,c=1,u=2),dict(a=1,b=1,c=1,u=3),
        dict(a=1,b=1,c=1,u=4),dict(a=5,b=2,c=-1,u=3),
        dict(a=1,b=2,c=2,u=5),dict(a=5,b=3,c=4,u=6)]
    records=[g.generate('hard',917+i,'reciprocal_exp_root_blank',parameters=p) for i,p in enumerate(ps)]
    # A current source replay; compare every original field value, without trusting metadata.
    source=json.loads((W.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
    replays=[]
    for ma in ['q-363490','q-353363']:
        q=next(q for q in source if q[':question/math-academy-id']==ma)
        r=g.generate('hard',918,'reciprocal_exp_root_blank',parameters=g.PARAMETERS[ma],profile='observed')
        f=q[':question/answer-fields'][0]
        assert len(f[':answer-field/choices'])==len(r['question'][':question/answer-fields'][0][':answer-field/choices'])==1
        assert s.simplify(parse(f[':answer-field/correct'][':answer/value'])-parse(key(r)))==0
        replays.append(r)
    records+=replays
    save('regression-records.json',records)
    save('regression-math.json',[mathcheck(r) for r in records])
    save('regression-grader-input.json',cases(records))
    run([ENGINE,W/'regression-grader-input.json',W/'regression-grader-result.json'])
    run([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',W/'regression-records.json',
         '--source',W.parent/'source/source.json','--inventory',W.parent/'source/inventory.json',
         '--difficulty','hard','--output',W/'delivery-hard','--asset-root',W/'assets',
         '--math-root','/media/jake/SSD/EDB/math'])
    accepted=json.loads((W/'delivery-hard/accepted.json').read_text())
    assert accepted and any(r['generation']['parameters']==ps[0] for r in accepted)
    save('regression-delivered-grader-input.json',cases(accepted))
    run([ENGINE,W/'regression-delivered-grader-input.json',W/'regression-delivered-grader-result.json'])
    save('regression-result.json',{'finding':'cf8dcbf41937f26e0c48','current_records':len(records),
         'delivered_records':len(accepted),'source_replays':len(replays),'result':'passed'})
    print('Fractional exp regression passed:',len(records),'current records;',len(accepted),'delivered')
if __name__=='__main__':main()
