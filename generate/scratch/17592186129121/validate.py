#!/usr/bin/env python3
"""Validate current supported banks; retain v1 source/printed-math checker."""
import hashlib, importlib.util, json, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('amplitude_readback', HERE/'validate-v1.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
g=v.g
parse=v.parse
check_display=v.check_display
native_fixture=v.native_fixture
expression_from_prompt=v.expression_from_prompt
BANK_SOURCES={'coefficient_parameters':'q-117570','implicit_parameters':'q-117569','absolute_coefficient':'q-117574','numerator_division':'q-117576','signed_division':'q-43278'}

def fingerprint(q):
    expr=expression_from_prompt(q)
    atom=list(expr.atoms(sp.sin,sp.cos));assert len(atom)==1
    text=q[':question/problem']
    a=sp.expand(expr.xreplace({atom[0]:sp.Symbol('s')})).coeff(sp.Symbol('s'))
    if r'\frac{' in text:
        numerator,_=v.read_group(text,text.index(r'\frac{')+5)
        if 'sin' in numerator or 'cos' in numerator:
            return g.digest({'demand':'single-division','N':str(a.p),'Q':str(a.q)})
    return g.digest({'demand':'implicit' if a==1 else 'direct','A':str(a)})

def independent(rec):
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    assert rec['question'][':question/difficulty'].split('/')[-1] in g.SUPPORTED_LEVELS
    check_display(rec)
    assert fingerprint(rec['question'])==rec['generation']['parameter_fingerprint']
    profile=rec['generation']['bank_profile']; assert profile in BANK_SOURCES
    original=g.SPECS[BANK_SOURCES[profile]]
    expected=g.evaluate_recipes(original['bank'],g.decode(rec['generation']['parameters']))
    actual=[parse(a[':answer/value']) for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]
    assert set(actual)==set(expected) and len(actual)==len(expected)==5

def solution_check(q):
    expr=expression_from_prompt(q);atoms=list(expr.atoms(sp.sin,sp.cos));assert len(atoms)==1
    a=sp.expand(expr.xreplace({atoms[0]:sp.Symbol('s')})).coeff(sp.Symbol('s'))
    assert q.get(':question/worked-solution') and len(q[':question/answer-fields'])==1
    f=q[':question/answer-fields'][0]
    vals=[parse(c[':answer/value']) for c in f[':answer-field/choices']]
    assert len(vals)==len(set(vals))==5 and vals.count(abs(a))==1
    ref=f[':answer-field/correct']; ident=str(ref[':answer/id']) if isinstance(ref,dict) else ref[1]
    assert next(parse(c[':answer/value']) for c in f[':answer-field/choices'] if str(c[':answer/id'])==ident)==abs(a)

def checks(rec):return native_fixture(rec,'temporary')['checks']

def main():
    raws=[];native=[];coverage={};slots={}
    for sid,s in g.SPECS.items():
        r=g.generate(s['level'],profile='raw:'+sid)
        v.parity(r,g.QUESTIONS[sid]);check_display(r);raws.append(r)
        if (f:=native_fixture(r,sid)):native.append(f)
    for profile,sid in BANK_SOURCES.items():
        s=g.SPECS[sid];name=g.BANK_PROFILES[profile]['template']
        r=g.generate(s['level'],template=name,profile=profile,parameters={**s['params'],'trig':s['trig']})
        independent(r)
        original=g.QUESTIONS[sid][':question/answer-fields'][0]
        assert sorted(parse(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(parse(a[':answer/value']) for a in original[':answer-field/choices'])
        coverage[profile]={'source':sid,'complete_bank':'5/5','missing':[],'extra':[]}
    records=[]
    for level in g.SUPPORTED_LEVELS:
        for seed in range(80):
            rec=g.generate(level,seed);independent(rec);assert rec==g.generate(level,seed)
            records.append(rec)
            if seed<12:native.append(native_fixture(rec,f'{level}-{seed}'))
        batch=g.batch(level,12,9000);assert len({fingerprint(r['question']) for r in batch})==12
    # Every live profile, and its actual argument/constant slots, is exercised.
    for profile in BANK_SOURCES:
        level=g.BANK_PROFILES[profile]['level'];samples=[g.generate(level,s,profile=profile) for s in range(50)]
        for rec in samples:independent(rec)
        keys=samples[0]['generation']['parameters']
        slots[profile]={k:sorted({r['generation']['parameters'][k] for r in samples}) for k in keys}
        assert set(slots[profile]['trig'])=={'cos','sin'}
        assert len(slots[profile]['A' if 'A' in keys and profile!='implicit_parameters' else 'B' if profile=='implicit_parameters' else 'N'])>1
    for profile in ('coefficient_parameters','absolute_coefficient'):
        level=g.BANK_PROFILES[profile]['level'];r=g.generate(level,17,profile=profile);p=r['generation']['parameters']
        changed=g.generate(level,18,profile=profile,parameters={**p,'trig':'cos' if p['trig']=='sin' else 'sin'})
        independent(changed);assert fingerprint(r['question'])==fingerprint(changed['question'])
        assert r['question'][':question/problem']!=changed['question'][':question/problem']
    try:g.generate('hard',0)
    except ValueError:pass
    else:raise AssertionError('Hard must remain unsupported')
    output=HERE/'reference/current-validation';output.mkdir(parents=True,exist_ok=True)
    (output/'native-input.json').write_text(json.dumps(native,indent=2))
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(output/'native-input.json'),str(output/'native-report.json')],check=True)
    report=json.loads((output/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
    (output/'side-by-side.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in raws+[g.generate('easy',7,profile='coefficient_parameters'),g.generate('easy',8,profile='implicit_parameters'),g.generate('moderate',9,profile='absolute_coefficient'),g.generate('moderate',10,profile='numerator_division'),g.generate('moderate',11,profile='signed_division')]))
    caps={'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'exceptions':[{'level':'hard','reason':'No observed hard source template. V1 whole-numerator outer multiplication adds an operation and rewrite stage, outside the extracted source backbone. Excluded from generation and inventory.','nominal_shortage':5}],'source_anomalies':['q-43277/q-43278 lack difficulty/solution/correct refs','q-117568/q-117575 lack fields'],'source_preservation':'All nine originals unchanged; missing attributes remain absent.'}
    (HERE/'capabilities.json').write_text(json.dumps(caps,indent=2)+'\n')
    files=[HERE.with_suffix('.py'),HERE/'validate.py',HERE/'validate-v1.py',HERE/'source.json',HERE/'capabilities.json']
    result={'status':'pass','version':g.VERSION,'source_basis':g.PROVENANCE,'source_replay':{'prompts':'9/9','present_solutions':'7/7','complete_banks':'7/7','values':'35/35','present_correct_refs':'5/5','missing_correct_refs':2},'production_bank_replay':coverage,'sampled_math_checks':len(records)+250,'slot_coverage':slots,'native':report,'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'supported_levels':list(g.SUPPORTED_LEVELS),'hard_unsupported':True,'side_by_side':'reference/current-validation/side-by-side.md'}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','math_checks':result['sampled_math_checks'],'bank_profiles':len(coverage),'native':report}))
if __name__=='__main__':main()
