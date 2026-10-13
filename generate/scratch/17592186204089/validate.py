"""Source replay, independent algebra and actual checkbox grading; no writes."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')

def parse(problem):
    equations=re.findall(r'\$([^$]*=[^$]*)\$',problem)
    assert len(equations)==3
    variable=re.search('[xuyzwv]',equations[0])[0]
    x=sp.Symbol(variable)
    rows=[]
    for equation in equations:
        sides=[]
        for side in equation.split('='):
            expression=sp.sympify(re.sub(r'(\d)([xuyzwv])',r'\1*\2',side),locals={variable:x})
            assert sp.Poly(expression,x).degree()<=1
            a,b=expression.coeff(x),expression.subs(x,0)
            assert a.is_Integer and b.is_Integer
            sides.extend([int(a),int(b)])
        rows.append(sides)
    return {'variable':variable,'equations':rows}

def independent(rec):
    q=rec['question'];meta=rec['generation'];p=parse(q[':question/problem'])
    assert p==meta['parameters'] and q[':question/difficulty']==':question.difficulty/easy'
    assert meta['parameter_fingerprint']==g.fingerprint(p)
    x=sp.Symbol(p['variable'],real=True)
    fields=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
    assert [f[':answer-field/key'] for f in fields]==list(g.KEYS)
    assert q[':question/problem'].count('Select all that apply.')==1
    uuids=[]
    for e,f in zip(p['equations'],fields):
        a,b,c,d=e
        solutions=sp.solveset(sp.Eq(a*x+b,c*x+d),x,domain=sp.S.Reals)
        truth='true' if solutions==sp.S.EmptySet else 'false'
        assert f[':answer-field/type']==':answer-field.type/checkbox'
        answers=f[':answer-field/choices'];byid={a[':answer/id']:a for a in answers}
        assert len(answers)==2 and {a[':answer/value'] for a in answers}=={'true','false'}
        assert all(a[':answer/type']==':answer.type/text' for a in answers)
        assert f[':answer-field/correct'][0]==':answer/id' and byid[f[':answer-field/correct'][1]][':answer/value']==truth
        uuids += [f[':answer-field/id']]+list(byid)
    assert len(set(uuids))==len(uuids)
    for value in [q[':question/id']]+uuids: uuid.UUID(value)
    # Check every worked algebra row independently against the input equation.
    if meta['template']!='summary-spaced':
        displays=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
        assert len(displays)==3
        for e,display in zip(p['equations'],displays):
            expected=sp.solveset(sp.Eq(e[0]*x+e[1],e[2]*x+e[3]),x,domain=sp.S.Reals)
            for line in display.split(r'\\'):
                left,right=line.replace('&','').rstrip('.').split('=')
                def convert(s):
                    s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1)/(\2)',s)
                    return sp.sympify(re.sub(r'(\d)([xuyzwv])',r'\1*\2',s),locals={p['variable']:x})
                actual=sp.solveset(sp.Eq(convert(left),convert(right)),x,domain=sp.S.Reals)
                assert expected==actual,(line,e)
    for text in (q[':question/problem'],q[':question/worked-solution']):
        assert text.count('$')%2==0 and text.count('{')==text.count('}')
    replay=g.generate('easy',seed=meta['seed'],parameters=p,template=meta['template'],profile=meta['bank_profile'])
    assert rec==replay

structural=independent

def checks(rec):
    result=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        result.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==correct else 'rejected','purpose':'Actual learner checkbox grading by owned boolean choice ID'} for a in f[':answer-field/choices'])
    return result

def main():
    source=json.loads((HERE/'reference/initial/source.json').read_text())
    cases=[];replays=[];variants=[];mappings=[]
    for src in source['record'][':knowledge-point/questions']:
        mid=src[':question/math-academy-id'];p=parse(src[':question/problem'])
        template='summary-spaced' if mid in ('q-287964','q-288058') else 'detailed-unit' if mid=='q-288073' else 'detailed-scaled'
        case={'source_id':mid,'parameters':p,'template':template,'level':'easy','difficulty_origin':'observed' if ':question/difficulty' in src else 'local easy assignment for replay; stored source remains unrated','bank_profile':'boolean-per-equation'}
        rec=g.generate('easy',parameters=p,template=template);independent(rec)
        assert rec['question'][':question/problem']==src[':question/problem'],mid
        assert rec['question'][':question/worked-solution']==src[':question/worked-solution'],mid
        for original,generated in zip(sorted(src[':question/answer-fields'],key=lambda f:f[':answer-field/key']),rec['question'][':question/answer-fields']):
            assert original[':answer-field/type'][':db/ident']==generated[':answer-field/type']
            assert sorted(a[':answer/value'] for a in original[':answer-field/choices'])==sorted(a[':answer/value'] for a in generated[':answer-field/choices'])
            value=next(a[':answer/value'] for a in generated[':answer-field/choices'] if a[':answer/id']==generated[':answer-field/correct'][1])
            assert value==original[':answer-field/correct'][':answer/value']
            mappings.append({'source':mid,'key':original[':answer-field/key'],'equation_parameters':p['equations'][g.KEYS.index(original[':answer-field/key'])],'choices':[{'value':a[':answer/value'],'recipe':'literal boolean checkbox state','reproduced':True} for a in original[':answer-field/choices']],'correct_recipe':'a=c and b!=d','correct_value':value,'bank_profile':'boolean-per-equation'})
        cases.append(case);replays.append(rec)
    for template in ('detailed-scaled','detailed-unit','summary-spaced'):
        for seed in range(160):
            rec=g.generate('easy',seed,template);independent(rec);variants.append(rec)
    # Signed/zero constants, equal/unequal slopes, integer/rational solutions and
    # each observed pattern are covered above; enumerate every affine row separately.
    for a in (-9,-1,1,9):
        for b in (-9,0,9):
            for c in (-9,-1,1,9):
                for d in (-9,0,9):
                    x=sp.Symbol('x',real=True)
                    assert (g.kind([a,b,c,d])=='N')==(sp.solveset(sp.Eq(a*x+b,c*x+d),x,domain=sp.S.Reals)==sp.S.EmptySet)
    assert {''.join(g.kind(e) for e in r['generation']['parameters']['equations']) for r in variants}==set(g.DOMAIN['patterns'])
    batch=g.batch('easy',100,733)
    assert len({r['generation']['parameter_fingerprint'] for r in batch})==100
    for rec in batch: independent(rec)
    a=g.generate('easy',parameters=cases[2]['parameters']);p=copy.deepcopy(cases[2]['parameters']);p['variable']='x'
    assert g.fingerprint(p)==a['generation']['parameter_fingerprint']
    assert a==g.generate('easy',parameters=cases[2]['parameters'])
    for level in ('moderate','hard'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unsupported band generated')
    for field in ('correct','value','solution'):
        bad=copy.deepcopy(a)
        if field=='correct':bad['question'][':question/answer-fields'][0][':answer-field/correct'][1]=str(uuid.uuid4())
        elif field=='value':bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='maybe'
        else:bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('4 & =-1','4 & =4')
        try:independent(bad)
        except (AssertionError,KeyError):pass
        else:raise AssertionError('Corrupt '+field+' passed')
    records=replays+variants+batch
    save('source-cases.json',cases);save('choice-mapping.json',mappings)
    save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)])
    executable=ROOT/'generate/runs/current/check-engine'
    result=subprocess.run([str(executable),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
    (HERE/'engine.log').write_text(result.stdout+result.stderr)
    assert result.returncode==0,result.stderr
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    save('review.json',{'original_replays':replays,'generated_variants':[g.generate('easy',811+i,template) for i,template in enumerate(('detailed-scaled','detailed-unit','summary-spaced'))]})
    (HERE/'review.md').write_text('\n\n'.join(['# Source and variant review']+[f'## Replay {c["source_id"]}\n\n'+g.markdown(r) for c,r in zip(cases,replays)]+['## Changed-coefficient variant\n\n'+g.markdown(g.generate('easy',811+i,t)) for i,t in enumerate(('detailed-scaled','detailed-unit','summary-spaced'))])+'\n')
    report={'status':'pass','supported_levels':['easy'],'provenance':{k:source[k] for k in ('database','basis','lineage')},'source_coverage':{'practice_questions':7,'exact_prompts':7,'exact_solutions':7,'complete_field_banks':21,'complete_question_banks':7,'matched_values':42,'total_values':42,'matched_correct_designations':21,'missing_options':[],'extra_options':[]},'mathematics':{'independently_validated_records':len(records),'boundary_rows':144,'distinct_batch_tasks':100,'negative_controls':5},'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(HERE.with_suffix('.py').relative_to(ROOT)):hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()},'engine_binary_sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),'limitations':['Only easy is validated; absent levels have no validated higher-demand template.','Two legacy questions remain unrated in EDB.','Generated signed coefficients extend observed positions, retaining the same cancellation method.']}
    save('validation.json',report)
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
