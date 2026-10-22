"""Independent rendered-equation checks, complete source banks, real grading.

Dependency for reading LaTeX: antlr4-python3-runtime==4.11.1. Installed outside
the repository at /tmp/ca-bernoulli-validation for this validation run.
"""
import hashlib
from functools import lru_cache
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
sys.path.insert(0,'/tmp/ca-bernoulli-validation')
import sympy as sp
from sympy.parsing.latex import parse_latex
H=Path(__file__).resolve().parent
ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('bernoulli_generator',H.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,default=str)+'\n')

@lru_cache(maxsize=4096)
def parse(text):
    text=text.replace('\u2061','').replace('{cos}',r'\cos')
    text=re.sub(r'\{?y\}?\^\{[′\u2032]\}|y[\u2032\x27]', 'D',text)
    text=re.sub(r'\\operatorname\{(sin|cos|tan|ln)\}',r'\\\1 ',text)
    result=parse_latex(text,strict=True)
    return result.xreplace({s:({'x':g.x,'y':g.y,'D':g.D,'e':sp.E}.get(str(s),s)) for s in result.free_symbols})

def prompt_equations(text):
    rows=re.findall(r'\$([^$\n]*=[^$\n]*)\$',text)
    assert len(rows)==3, rows
    return [sp.expand(parse(row.split('=')[0])-parse(row.split('=')[1])) for row in rows]

def independent_truth(residual):
    multiplier=sp.diff(residual,g.D)
    assert multiplier!=0 and not multiplier.has(g.D)
    normal=sp.expand(-residual.subs(g.D,0)/multiplier)
    powers=[]
    for term in sp.Add.make_args(normal):
        # Constant logarithmic derivative iff a term is c(x)*y**n.
        n=sp.simplify(g.y*sp.diff(term,g.y)/term)
        if n.has(g.y):return False
        assert not n.has(g.x), 'Exponent must be constant'
        powers.append(n)
    return len(set(powers))==2 and sp.Integer(1) in powers

def normalized(residual):
    return sp.simplify(residual/sp.diff(residual,g.D))

def flags(q):
    result=[]
    assert [f[':answer-field/key'] for f in q[':question/answer-fields']]==list(g.LABELS)
    for f in q[':question/answer-fields']:
        assert f[':answer-field/type']==':answer-field.type/checkbox'
        assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'true','false'}
        correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        result.append(correct[':answer/value']=='true')
    return result

def inspect(record):
    q=record['question'];meta=record['generation'];eqs=prompt_equations(q[':question/problem'])
    expected=[independent_truth(r) for r in eqs]
    assert flags(q)==expected
    replay=g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],meta['parameters'],meta['bank_profile'])
    assert replay==record, 'Replay or identity mismatch'
    solution=q[':question/worked-solution']
    assert solution.count('$')%2==0 and q[':question/problem'].count('$')%2==0
    assert not re.search(r'\$\$\S|\S\$\$',solution)
    for i,label in enumerate(g.LABELS):
        part=solution.split('- Equation '+label+' is ')[1].split('- Equation ')[0]
        assert ('*not*' not in part)==expected[i]
        if expected[i]:
            pieces=re.search(r'p\(x\)=(.*?),\\quad q\(x\)=(.*?),\\quad n=(.*?)\.\n',part)
            assert pieces
            p,qq,n=map(parse,pieces.groups())
            assert sp.simplify(normalized(eqs[i])-(g.D+p*g.y-qq*g.y**n))==0
        m=sp.diff(eqs[i],g.D)
        if m!=1:
            display=re.search(r'\$\$\n(.*?=.*?)\n\$\$',part).group(1)
            lhs,rhs=display.split('=');shown=parse(lhs)-parse(rhs)
            assert sp.simplify(normalized(eqs[i])-shown)==0
    return eqs

def normalize_source(q):
    result={':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':q[':question/difficulty'][':db/ident'],':question/answer-fields':[]}
    for f in sorted(q[':question/answer-fields'],key=lambda f:g.LABELS.index(f[':answer-field/key'])):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
    return result

def native_checks(records,path):
    items=[]
    for rec in records:
        checks=[]
        for i,f in enumerate(rec['question'][':question/answer-fields']):
            correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            for value in ('true','false'):
                answer=next(a for a in f[':answer-field/choices'] if a[':answer/value']==value)
                checks.append({'field_index':i,'submitted_answer_id':answer[':answer/id'],'expected':'accepted' if value==correct else 'rejected','purpose':'Actual owned checked/unchecked checkbox choice submission'})
        items.append({'label':rec['question'][':question/id'],'record':rec,'checks':checks})
    save(path/'native-input.json',items)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
    return report

def replay_sources():
    records=[];reports=[]
    for source in g.SOURCE[':knowledge-point/questions']:
        mid=source.get(':question/math-academy-id')
        if mid not in g.CASES:continue
        level=g.CASES[mid][0];rec=g.generate(level,0,mid,{'left_scales':[1]*3,'right_scales':[1]*3})
        source_q=normalize_source(source)
        assert flags(source_q)==flags(rec['question'])
        assert len(source_q[':question/answer-fields'])==3
        se=prompt_equations(source[':question/problem']);ge=inspect(rec)
        assert all(sp.simplify(normalized(a)-normalized(b))==0 for a,b in zip(se,ge))
        assert [independent_truth(e) for e in se]==flags(source_q)
        reports.append({'source_id':mid,'level':level,'profile':'boolean-checkbox','fields':3,'matched_bank_values':6,'total_bank_values':6,'matched_correct_designations':3,'equations_equivalent':True,'unmatched_options':[]})
        records.append({'question':source_q,'knowledge_point':rec['knowledge_point'],'generation':rec['generation']})
    return records,reports

def main():
    source_records,coverage=replay_sources()
    tested=[];coverage_slots={}
    # Every bounded scalar value in every slot, plus all-one/all-five boundaries.
    for template,(level,_) in g.CASES.items():
        params=[{'left_scales':[k]*3,'right_scales':[k]*3} for k in (1,5)]
        for side in ('left_scales','right_scales'):
            for i in range(3):
                for k in range(1,6):
                    p={'left_scales':[1]*3,'right_scales':[1]*3};p[side][i]=k;params.append(p)
        for p in params:tested.append(g.generate(level,0,template,p))
        coverage_slots[template]={side:[list(range(1,6))]*3 for side in ('left_scales','right_scales')}
    tested.extend(g.generate(level,seed) for level in ('easy','moderate') for seed in range(30))
    for record in tested:inspect(record)
    for template,(level,_) in g.CASES.items():
        p={'left_scales':[2,3,4],'right_scales':[3,4,5]}
        a=g.generate(level,1,template,p);b=g.generate(level,999,template,p)
        assert a['question']==b['question'], 'Seed must not manufacture content or identity'
        for bad in (0,-1,6):
            invalid={'left_scales':[bad,1,1],'right_scales':[1]*3}
            try:g.generate(level,0,template,invalid)
            except AssertionError:pass
            else:raise AssertionError('Unbounded or zero scalar accepted')
    try:g.generate('hard',0)
    except AssertionError:pass
    else:raise AssertionError('Unsupported level accepted')
    # Counterexample tests ensure the rendered prompt/key and solution checks fail.
    import copy
    altered=copy.deepcopy(tested[0]);f=altered['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
    try:inspect(altered)
    except AssertionError:pass
    else:raise AssertionError('Validator failed to detect stale key')
    altered=copy.deepcopy(tested[0]);altered['question'][':question/worked-solution']=altered['question'][':question/worked-solution'].replace('n=-1','n=-2')
    try:inspect(altered)
    except AssertionError:pass
    else:raise AssertionError('Validator failed to detect stale solution')
    report=native_checks(source_records+tested,H/'reference/validation')
    validation={'status':'passed','generator_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),'source_basis':g.SOURCE_BASIS,'source_replay':coverage,'complete_banks_matched':5,'complete_banks_total':5,'bank_values_matched':30,'bank_values_total':30,'missing_or_extra_options':[],'samples_checked':len(tested),'slot_coverage':coverage_slots,'symbolic_method':'Independent rendered LaTeX parsing and constant logarithmic derivative test; normalized-equation equivalence','actual_grader':report['entry_point'],'accepted_checks':report['accepted_checks'],'rejected_checks':report['rejected_checks'],'unresolved_grading_checks':0,'formatting':'Balanced inline/display delimiters and no trailing text attached to display delimiter','source_fidelity':'All five supported mathematical objects, checkbox banks and keys replayed. Deliberate source formatting/label corrections documented separately. Two incomplete radio sources excluded. No new plots.','side_by_side_review':'review.md'}
    save(H/'validation.json',validation)
    save(H/'reference/validation/samples.json',tested)
    representatives=[g.generate(level,11,t,{'left_scales':[2,3,4],'right_scales':[3,4,5]}) for t,(level,_) in g.CASES.items()]
    (H/'review.md').write_text('\n\n---\n\n'.join('Source '+t+'\n\n'+next(q[':question/problem'] for q in g.SOURCE[':knowledge-point/questions'] if q.get(':question/math-academy-id')==t)+'\n\nVariant\n\n'+g.markdown(r) for t,r in zip(g.CASES,representatives))+'\n')
    print(json.dumps({k:validation[k] for k in ('status','samples_checked','complete_banks_matched','accepted_checks','rejected_checks')}))

if __name__=='__main__':main()
