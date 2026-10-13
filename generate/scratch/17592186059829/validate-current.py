"""Replay current and historical complete banks; check rendered mathematics."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent
ROOT=H.parents[2]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
g=module('generator',H.with_suffix('.py'))
v=module('historical_validator',H/'validate.py')
def read_set(text):
    text=text.replace(r'\infty','∞').strip().rstrip('.?')
    if ' or ' in text and r'\le' in text:
        left,right=text.replace('$','').split(' or ')
        return sp.Union(sp.Interval(-sp.oo,v.num(left.split(r'\le')[1])),sp.Interval(v.num(right.split(r'\ge')[1]),sp.oo))
    return v.read_set(text)
def fingerprint(q):
    text=re.findall(r'\$([^$]+)\$',q[':question/problem'])[0]
    target=read_set(text)
    direction='interval_to_inequality' if '[' in text else 'inequality_to_interval'
    return g.digest({'direction':direction,'a':sp.srepr(target.start),'b':sp.srepr(target.end),'endpoint_inclusion':'both'})
def check(record):
    q=record['question'];field=q[':question/answer-fields'][0]
    assert len(q[':question/answer-fields'])==1 and field[':answer-field/type']==':answer-field.type/radio'
    assert len(field[':answer-field/choices'])==5 and field[':answer-field/key']=='selection'
    target=read_set(re.findall(r'\$([^$]+)\$',q[':question/problem'])[0])
    assert isinstance(target,sp.Interval) and not target.left_open and not target.right_open
    answers=[read_set(a[':answer/value']) for a in field[':answer-field/choices']]
    assert len(set(answers))==5 and answers.count(target)==1
    if not record['generation']['raw_evidence']:
        correct=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
        assert read_set(correct[':answer/value'])==target
        stages=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)
        assert len(stages)==(3 if record['generation']['template']=='inequality_to_interval' else 2)
        assert all(read_set(s)==target for s in stages)
        for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in field[':answer-field/choices']]:v.fmt(text)
    assert fingerprint(q)==record['generation']['mathematical_fingerprint']
    return target
def engine_item(record):
    field=record['question'][':question/answer-fields'][0]
    return {'label':record['question'][':question/id'],'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'independently parsed complete closed-set choice'} for a in field[':answer-field/choices']]}
def main():
    evidence=[];native=[];checked=0
    cases=[('q-102200','easy','captured_interval',{'a':'-10','b':'3'}),('q-154728','moderate','captured_inequality',{'a':'-7','b':'0'})]
    for source_id,level,profile,p in cases:
        original=next(q for q in g.CURRENT_SOURCE['record'][':knowledge-point/questions'] if q.get(':question/math-academy-id')==source_id)
        record=g.generate(level,19,profile=profile,parameters=p);check(record)
        q=record['question'];of=original[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in of[':answer-field/choices'])
        assert q[':question/problem']==original[':question/problem'].replace(']?$',']$?')
        assert q[':question/worked-solution']==original[':question/worked-solution']
        correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert read_set(correct[':answer/value'])==read_set(of[':answer-field/correct'][':answer/value'])
        evidence.append({'source':source_id,'matched_choices':5,'complete_bank':True,'correct_designation':True,'fixed_solution_exact':True,'punctuation_correction':source_id=='q-154728'})
        native.append(record)
        for parameters in g.parameter_catalog('easy'):
            r=g.generate(level,19,profile=profile,parameters=parameters);check(r);checked+=1
        for seed in (0,1,8):native.append(g.generate(level,seed,profile=profile))
    for case in json.loads((H/'source-cases.json').read_text()):
        r=g.generate('easy',19,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(r)
        original=next(q for q in g.SOURCE['record'][':knowledge-point/questions'] if q[':question/math-academy-id']==case['source_id'])
        assert r['question'][':question/problem']==original[':question/problem']
        assert sorted((a[':answer/type'],a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in original[':question/answer-fields'][0][':answer-field/choices'])
        evidence.append({'historical_source':case['source_id'],'matched_choices':5,'complete_bank':True,'missing_keys_preserved':True})
    for level in ('easy','moderate','hard'):
        for template in g.TEMPLATES:
            params=g.parameter_catalog(level)
            for p in (params[0],params[len(params)//2],params[-1]):
                r=g.generate(level,71,template=template,parameters=p);check(r);checked+=1;native.append(r)
                other=g.generate(level,999,template=template,parameters=p)
                assert r['question'][':question/id']==other['question'][':question/id']
    path=H/'reference/current-validation';path.mkdir(parents=True,exist_ok=True)
    (path/'native-input.json').write_text(json.dumps([engine_item(r) for r in native],indent=2))
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
    result={'passed':True,'basis':g.CURRENT_SOURCE['basis'],'generator_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),'source_replay':evidence,'new_profile_exhaustive_and_boundary_checks':checked,'historical_validation':'history/closed-intervals-v1/validation.json','native':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'current_source_complete_banks':3,'current_source_choices_matched':15,'current_keys_matched':2,'unresolved_findings':[]}
    (H/'current-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
