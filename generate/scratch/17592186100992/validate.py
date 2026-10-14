"""Independent rendered-matrix checks and actual application grading."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path

H=Path(__file__).resolve().parent
ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('distributivity',H.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sp=g.sp
ENGINE=ROOT/'generate/runs/current/check-engine'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def parse_matrix(text):
    m=re.fullmatch(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)
    assert m,'Not a delimiter-free matrix value'
    rows=[[sp.Integer(c.strip()) for c in row.split('&')] for row in m[1].split('\\\\')]
    assert len(rows)==2 and all(len(row)==2 for row in rows)
    return sp.Matrix(rows)

def parameters(problem):
    assert problem.startswith('Find $(A+B)-C-(B-C)$, if\n\n$$\n')
    matches=re.findall(r'([ABC])=(\\begin\{bmatrix\}.*?\\end\{bmatrix\})',problem,re.S)
    assert [name for name,_ in matches]==list('ABC')
    return {n:[[int(x) for x in row] for row in parse_matrix(m).tolist()] for n,m in matches}

def format_check(text):
    assert text.count('$$')%2==0 and text.replace('$$','').count('$')%2==0
    depth=0
    for c in text:
        depth+=(c=='{')-(c=='}');assert depth>=0
    assert depth==0

def check(r):
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question'];meta=r['generation'];p=parameters(q[':question/problem'])
    assert q[':question/difficulty']==':question.difficulty/moderate'
    assert p==meta['parameters'] and all(0<=x<=9 for name in 'ABC' for row in p[name] for x in row)
    a,b,c=[sp.Matrix(p[n]) for n in 'ABC']
    # Derive independently from actual displayed expression and matrices.
    value=(a+b)-c-(b-c);assert value==a
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    answers=f[':answer-field/choices'];assert len(answers)==5 and len({x[':answer/id'] for x in answers})==5
    assert all(x[':answer/type']==':answer.type/math' for x in answers)
    bank=[parse_matrix(x[':answer/value']) for x in answers]
    assert len({tuple(m) for m in bank})==5
    target=sp.Matrix([[a[0,0]-1,a[0,1]],[a[0,1],a[1,1]]])
    assert {tuple(m) for m in bank}=={tuple(m) for m in [a,b,c,sp.zeros(2),target]}
    answer=next(x for x in answers if x[':answer/id']==f[':answer-field/correct'][1])
    assert parse_matrix(answer[':answer/value'])==value
    solution=q[':question/worked-solution']
    assert r'=(A+B)' not in solution
    assert r'(A+B)-C-(B-C) & =A+B-C-B+C' in solution
    assert r'=A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C}' in solution
    assert r'& =A\end{aligned}' in solution
    final=re.search(r'\\begin\{aligned\}A & =(.*?)\\end\{aligned\}',solution,re.S)
    assert final and parse_matrix(final[1])==value
    format_check(q[':question/problem']);format_check(solution)
    assert meta['mathematical_key']==g.mathematical_key(p)
    assert meta['bank_profile']==g.PROFILE and meta['recipes']==list(g.RECIPES)
    replay=g.generate('moderate',meta['seed'],parameters=p)
    def ordered(question):
        x=copy.deepcopy(question)
        for field in x[':question/answer-fields']:
            field[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
        return x
    assert ordered(replay['question'])==ordered(q) and replay['generation']==meta,'Deterministic full-record replay failed'
    return True

def engine_item(label,r):
    f=r['question'][':question/answer-fields'][0]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned option from independently validated whole matrix bank'} for a in f[':answer-field/choices']]}

def main():
    source=json.loads((H/'reference/source.json').read_text())
    src=next(q for q in source['record'][':knowledge-point/questions'] if q[':question/math-academy-id']=='q-13536')
    r=g.generate(parameters=g.ORIGINAL);check(r)
    assert all(r['question'][k]==src[k] for k in (':question/problem',':question/worked-solution'))
    replay=[]
    for f in src[':question/answer-fields']:
        expected=sorted(a[':answer/value'] for a in f[':answer-field/choices'])
        got=sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
        assert expected==got
        if ':answer-field/correct' in f:assert parse_matrix(f[':answer-field/correct'][':answer/value'])==sp.Matrix(g.ORIGINAL['A'])
        replay.append({'field_id':f[':answer-field/id'],'choices_matched':5,'choices_total':5,'distractors_matched':4,'distractors_total':4,'missing_options':[],'extra_options':[],'complete_bank':True,'source_correct_ref_present':':answer-field/correct' in f,'normal_route': 'complete field' if ':answer-field/correct' in f else 'excluded duplicate incomplete field; mathematical answer independently A'})
    (H/'source-replay.json').write_text(json.dumps({'passed':True,'prompt_exact':True,'solution_exact':True,'banks_matched':2,'banks_total':2,'distractors_matched':8,'distractors_total':8,'fields':replay},indent=2))
    records=[g.generate(seed=i) for i in range(300)]
    for item in records:check(item)
    coverage={n:[[sorted({r['generation']['parameters'][n][i][j] for r in records}) for j in range(2)] for i in range(2)] for n in 'ABC'}
    assert all(values==list(range(10)) for name in 'ABC' for row in coverage[name] for values in row)
    # Fixed A: canceled inputs may change content identity but never task count.
    p=copy.deepcopy(g.ORIGINAL);p['B'][0][0]=9
    canceled=g.generate(seed=73,parameters=p);check(canceled)
    assert canceled['generation']['mathematical_key']==r['generation']['mathematical_key']
    assert canceled['question'][':question/id']!=r['question'][':question/id']
    p=copy.deepcopy(g.ORIGINAL);p['A'][0][0]=9
    changed=g.generate(seed=73,parameters=p);check(changed)
    assert changed['generation']['mathematical_key']!=r['generation']['mathematical_key']
    assert changed['question'][':question/worked-solution']!=r['question'][':question/worked-solution']
    shuffled=g.generate(seed=917,parameters=g.ORIGINAL)
    assert shuffled['question'][':question/id']==r['question'][':question/id']
    assert shuffled['generation']['mathematical_key']==r['generation']['mathematical_key']
    for value in (-1,10):
        p=copy.deepcopy(g.ORIGINAL);p['A'][0][0]=value
        try:g.generate(parameters=p)
        except ValueError:pass
        else:raise AssertionError('Sampling boundary violated')
    for name in 'ABC':
        for i in range(2):
            for j in range(2):
                for value in (0,9):
                    p=copy.deepcopy(g.ORIGINAL);p[name][i][j]=value
                    check(g.generate(parameters=p))
    p=copy.deepcopy(g.ORIGINAL);p['B']=p['A']
    try:g.generate(parameters=p)
    except ValueError:pass
    else:raise AssertionError('Entire invalid source profile must reject')
    for level in ('easy','hard'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unsupported level emitted')
    for kind in ('correct','solution','bank','prompt'):
        bad=copy.deepcopy(r);q=bad['question'];f=q[':question/answer-fields'][0]
        if kind=='correct':f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
        elif kind=='solution':q[':question/worked-solution']=q[':question/worked-solution'].replace('6 & 7','9 & 7')
        elif kind=='bank':f[':answer-field/choices'][0][':answer/value']='999'
        else:q[':question/problem']=q[':question/problem'].replace('6 & 7','9 & 7')
        try:check(bad)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('Mutation escaped '+kind)
    grading=[r,canceled,changed]+records
    (H/'reference/native-input.json').write_text(json.dumps([engine_item(str(i),x) for i,x in enumerate(grading)],indent=2))
    subprocess.run([str(ENGINE),str(H/'reference/native-input.json'),str(H/'native-report.json')],check=True)
    review=[{'label':'q-13536 original parameter replay, duplicate incomplete field excluded','record':r},{'label':'Same method with changed A, all canceled matrices held constant','record':changed},{'label':'Both canceled matrices sampled within the declared numeric slots','record':records[4]}]
    (H/'review.json').write_text(json.dumps(review,indent=2));(H/'review.md').write_text('\n\n---\n\n'.join('## '+x['label']+'\n\n'+g.markdown(x['record']) for x in review))
    native=json.loads((H/'native-report.json').read_text())
    files=[H.with_suffix('.py'),Path(__file__),H/'db_support.py',H/'classification.md',H/'template-extraction.md',H/'source-components.json',H/'capability.json',H/'source-replay.json',H/'native-report.json',H/'reference/source.edn',H/'reference/source.json',H/'review.json']
    result={'passed':True,'source_basis':source['status'],'supported_levels':['moderate'],'source_fidelity':{'exact_prompt':True,'exact_solution':True,'banks':2,'distractors':8,'field_layout_correction':'one complete selection field; excluded duplicate key without correct ref'},'normal_records':len(records),'distinct_tasks':len({x['generation']['mathematical_key'] for x in records}),'slot_coverage':coverage,'mathematical_validation':'independent actual-display exact matrix expression and full choice-bank comparison','actual_grading':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_harness':{'path':str(ENGINE.relative_to(ROOT)),'sha256':sha(ENGINE),'source_sha256':sha(ENGINE.with_suffix('.rs'))},'runtime':{'sympy':sp.__version__},'checks':['source complete banks and correct designation','all 12 scalar slots exercise 0..9','each slot 0 and 9 boundary cases','changed surviving matrix updates prompt solution and answer','canceled matrices excluded from task identity','seed and order stable identity','whole-profile collision rejection','four intentional corruptions rejected'],'files':{str(p.relative_to(ROOT)):sha(p) for p in files}}
    (H/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps({'passed':True,'normal_records':len(records),'native_grading':result['actual_grading']}))

if __name__=='__main__':main()
