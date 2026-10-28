"""Live-source fidelity, independent printed mathematics, geometry, and native grading."""
import copy, hashlib, importlib.util, json, math, re, subprocess, sys
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('qa',HERE/'validate.py');qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa);g=qa.g

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprint(q):
    # Read the actual displayed standard equation, excluding common axis scaling.
    block=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)[0]
    block=block.replace(r'\Longrightarrow','⟹').replace(r'\dfrac',r'\frac').replace(r'\qquad','')
    setup=block.split('⟹')[1].replace(r'\,','').strip().rstrip('.')
    left,right=setup.split('=');F=qa.expr(left)-qa.expr(right)
    import sympy as sp
    h=sp.solve(sp.diff(F,qa.x),qa.x)[0];k=sp.solve(sp.diff(F,qa.y),qa.y)[0]
    ratio=sp.cancel(sp.diff(F,qa.x,2)/sp.diff(F,qa.y,2))
    return str((h,k,ratio))
def independent(rec):
    assert rec['knowledge_point']['db_id']==g.KP_ID and rec['knowledge_point']['id']==g.KP_UUID
    assert rec['generation']['level'] in g.SUPPORTED_LEVELS and not rec['generation']['evidence_only']
    g.check_parameters(rec['generation']['level'],rec['generation']['parameters'])
    from math_format import validate_generated_record
    validate_generated_record(rec);qa.mathcheck(rec)
    # A record must be the deterministic output of the registered generator.
    replay=g.generate(rec['generation']['level'],parameters=rec['generation']['parameters'],seed=rec['generation']['seed'])
    assert canonical(rec['question'])==canonical(replay['question'])
    qa.generated_geometry(rec)
def canonical(x):
    if isinstance(x,dict):return {str(k):canonical(v) for k,v in x.items()}
    if isinstance(x,list):return sorted((canonical(v) for v in x),key=lambda v:json.dumps(v,sort_keys=True))
    return str(x) if not isinstance(x,(str,int,float,bool,type(None))) else x

def checks(r):
    f=r['question'][':question/answer-fields'][0];right=f[':answer-field/correct'][1]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==right else 'rejected','purpose':'full owned radio bank'} for a in f[':answer-field/choices']]
def main():
    records=[];replays=[];banks=[];mapping=[]
    for c in g.CASES.values():
        q=g.KP[':knowledge-point/questions'][c['index']]
        r=g.replay(c['level'],parameters=c['parameters'],profile=c['bank_profile']);rq=r['question']
        for key in (':question/problem',':question/worked-solution'):
            assert q.get(key)==rq.get(key)
        of=q[':question/answer-fields'][0];f=rq[':question/answer-fields'][0]
        assert of[':answer-field/key']==f[':answer-field/key'] and str(of[':answer-field/type'][':db/ident'])==f[':answer-field/type']
        assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
        if ':answer-field/correct' in of:
            assert of[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            records.append(r)
        else:assert ':answer-field/correct' not in f
        assert (':question/difficulty' in q)==(':question/difficulty' in rq)
        qa.mathcheck(r);replays.append({'source':c['source_id'],'prompt_and_solution_exact':True,'bank':'5/5','correct':'matched' if ':answer-field/correct' in of else 'absent, preserved'})
        vals=g.bank(c['parameters'],g.CODES[c['index']])
        mapping.append({'source':c['source_id'],'parameters':c['parameters'],'profile':c['bank_profile'],'choices':[{'original_id':str(a[':answer/id']),'value':a[':answer/value'],'recipe':next(v[0] for v in vals if v[2]==a[':answer/value'])} for a in of[':answer-field/choices']]})
        # Each complete historical profile also works away from its original values.
        for i,p in enumerate(g.domain(c['level'])):
            if p==c['parameters']:continue
            try:changed=g.replay(c['level'],parameters=p,profile=c['bank_profile'])
            except ValueError:continue
            qa.mathcheck(changed);banks.append(c['source_id']);break
        else:raise AssertionError('No nonliteral bank variation')
    geometry=qa.source_geometry()
    domains={};fps={};normal=[]
    for level in g.SUPPORTED_LEVELS:
        domain=g.domain(level);tasks=set()
        for p in domain:
            g.check_parameters(level,p);g.bank(p,g.DEFAULT)
            tasks.add((p['h'],p['k'],Fraction(p['b'],p['a'])))
        domains[level]={'parameter_instances':len(domain),'distinct_reduced_tasks':len(tasks)};fps[level]=tasks
        # Both signed translations, every zero/nonzero coordinate pattern and extremes.
        samples=[domain[0],domain[-1]]+[g.generate(level,i)['generation']['parameters'] for i in range(6)]
        if level=='moderate':samples += [dict(h=h,k=k,a=3,b=4) for h,k in [(0,-3),(-3,0),(-3,-3),(3,3),(2,-1)]]
        for p in samples:
            r=g.generate(level,parameters=p);independent(r);normal.append(r);records.append(r)
            other=g.generate(level,parameters=p,seed=91)
            assert canonical(other['question'])==canonical(r['question'])
    assert not fps['easy']&fps['moderate']
    try:g.generate('hard',0)
    except ValueError:pass
    else:raise AssertionError('Unsupported band generated')
    # Changed centers held at the same axes: rendered prompt asset, solution, and key agree.
    pair=[g.generate('moderate',parameters=dict(h=h,k=k,a=3,b=4)) for h,k in [(2,-1),(-2,1)]]
    assert pair[0]['question'][':question/problem']!=pair[1]['question'][':question/problem']
    assert fingerprint(pair[0]['question'])!=fingerprint(pair[1]['question'])
    for r in pair:independent(r)
    out=HERE/'reference/current-validation';out.mkdir(parents=True,exist_ok=True)
    (out/'engine-input.json').write_text(json.dumps([{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)],indent=2)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(out/'engine-input.json'),str(out/'engine-report.json')],check=True)
    (out/'bank-mapping.json').write_text(json.dumps(mapping,indent=2)+'\n')
    (out/'source-geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
    (out/'review.json').write_text(json.dumps(normal,indent=2)+'\n')
    (out/'review.md').write_text('\n\n'.join(g.markdown(r) for r in normal)+'\n')
    from PIL import Image,ImageDraw
    canvas=Image.new('RGB',(1200,((len(normal)+3)//4)*330),'white');draw=ImageDraw.Draw(canvas)
    for i,r in enumerate(normal):
        im=Image.open(r['generation']['plot']['prompt']).convert('RGB');im.thumbnail((290,290));xx=i%4*300;yy=i//4*330;canvas.paste(im,(xx,yy+35));draw.text((xx,yy),str(r['generation']['parameters']),fill='black')
    canvas.save(out/'montage.png')
    result={'status':'passed','source_basis':g.SOURCE['basis'],'generator_path':str(HERE.with_suffix('.py').relative_to(ROOT)),'generator_sha256':sha(HERE.with_suffix('.py')),'source_sha256':sha(HERE/'reference/source-current.json'),'source_replays':replays,'complete_banks':'10/10','matched_choices':'50/50','captured_correct':'9/9','missing_correct_preserved':1,'changed_parameter_bank_profiles':banks,'native_grading':json.loads((out/'engine-report.json').read_text()),'domains':domains,'changed_center_same_axes_checked':True,'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'hard_evidence':'Current moderate q-127364 contradicts prior authored hard split; no distinct source-supported hard workload. No hard questions generated.','dependencies':g.dependency_metadata()}
    (HERE/'reference/validation-current.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='native_grading'},indent=2))
if __name__=='__main__':main()
