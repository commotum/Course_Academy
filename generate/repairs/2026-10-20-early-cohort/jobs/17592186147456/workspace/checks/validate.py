"""Read visible equations independently; verify source banks, keys and solutions.
Validation-only parser: checks/vendor/antlr4-python3-runtime 4.11.1.
Run with the supplied Python; no services or runtime-file writes.
"""
import copy
from functools import lru_cache
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
H=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(H/'checks/vendor'))
sys.path.insert(0,str(H))
import sympy as sp
from sympy.parsing.latex import parse_latex
spec=importlib.util.spec_from_file_location('generator',H/'17592186147456.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=H.parent/'source/source.json'
REPO=next(p for p in H.parents if (p/'generate/pipeline/check_delivery.py').exists())
E=H/'evidence'

def save(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,default=str)+'\n')

def correct_value(f):
    ref=f[':answer-field/correct']
    aid=ref[':answer/id'] if isinstance(ref,dict) else ref[1]
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)

def flags(q):
    fields=q[':question/answer-fields']
    if len(fields)==1 and 'radio' in str(fields[0][':answer-field/type']):
        v=correct_value(fields[0])
        return [bool(re.search(r'(?<![IV])'+label+r'(?![IV])',v)) for label in g.LABELS]
    return [correct_value(f)=='true' for f in fields[:3]]

@lru_cache(maxsize=4096)
def parse(text):
    text=text.replace('\u2061','')
    text=re.sub(r'\{?y\}?\^\{[′\u2032]\}|y[\u2032\x27]', 'D',text)
    text=re.sub(r'\\operatorname\{?(sin|cos|tan|ln|sec)\}?',r'\\\1 ',text)
    text=text.replace('{cos}',r'\cos')
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

def inspect(record):
    q=record['question'];meta=record['generation'];eqs=prompt_equations(q[':question/problem'])
    expected=[independent_truth(r) for r in eqs]
    assert flags(q)==expected
    if len(q[':question/answer-fields'])>3:
        assert correct_value(q[':question/answer-fields'][-1])==str(not any(expected)).lower()
    replay=g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],meta['parameters'],meta['bank_profile'],replay=meta.get('replay',False))
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


def source_equations(q):
    text=q[':question/problem']
    rows=re.findall(r'\$([^$\n]*=[^$\n]*)\$',text)
    if not rows:
        rows=[f[':answer-field/key'].strip('$') for f in q[':question/answer-fields'] if '=' in f[':answer-field/key']]
    assert len(rows)==3
    return [sp.expand(parse(row.split('=')[0])-parse(row.split('=')[1])) for row in rows]

def source_replay():
    source=json.loads(SOURCE.read_text())['material']['kp'][':knowledge-point/questions']
    records=[];report=[]
    for q in source:
        t=q.get(':question/math-academy-id')
        if t not in g.CASES:continue
        level=q[':question/difficulty'][':db/ident'].split('/')[-1]
        r=g.generate(level,0,t,{'left_scales':[1]*3,'right_scales':[1]*3},replay=True)
        visible=inspect(r); original=source_equations(q)
        assert all(any(sp.simplify(normalized(a)-normalized(b))==0 for b in visible) for a in original)
        fs=q[':question/answer-fields'];new=r['question'][':question/answer-fields']
        assert len(fs)==len(new)
        if len(fs)==1:
            assert [a[':answer/value'] for a in fs[0][':answer-field/choices']]==[a[':answer/value'] for a in new[0][':answer-field/choices']]
            assert correct_value(fs[0])==correct_value(new[0])
        else:
            for f in fs:
                assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'}
                if '=' not in f[':answer-field/key']:
                    assert correct_value(f)==str(not any(independent_truth(a) for a in original)).lower()
                else:
                    text=f[':answer-field/key'].strip('$');a,b=text.split('=');res=parse(a)-parse(b)
                    assert (correct_value(f)=='true')==independent_truth(res)
                    j=next(j for j,v in enumerate(visible) if sp.simplify(normalized(res)-normalized(v))==0)
                    assert correct_value(new[j])==correct_value(f)
        records.append(r)
        report.append({'template':t,'source_question_id':q[':question/id'],'equations':3,'fields':len(fs),'bank_values':sum(len(f[':answer-field/choices']) for f in fs),'bank_and_key_match':True})
    assert len(records)==8
    save(E/'source-replay.json',records);save(E/'source-replay-report.json',report)
    return records

def feasible_cases(t):
    # Derive feasible role assignments independently from rendered source equations
    # and the captured response bank, rather than generator decision metadata.
    p={'left_scales':[1]*3,'right_scales':[1]*3}
    base=g.generate(g.CASES[t][0],0,t,p)
    possible=[]
    for residual in prompt_equations(base['question'][':question/problem']):
        normal=sp.expand(-residual.subs(g.D,0)/sp.diff(residual,g.D))
        powers=[sp.simplify(g.y*sp.diff(term,g.y)/term) for term in sp.Add.make_args(normal)]
        possible.append(all(not n.has(g.y) for n in powers))
    data=json.loads((H/'source-data.json').read_text())['profiles'][t]
    values=data['bank']
    masks=[]
    for mask in itertools.product((False,True),repeat=3):
        if any(flag and not ok for flag,ok in zip(mask,possible)):continue
        if data['type']=='radio':
            # Parse actual choice text rather than use selection_text.
            subsets=[tuple(bool(re.search(r'(?<![IV])'+label+r'(?![IV])',v)) for label in g.LABELS) for v in values]
            if mask not in subsets:continue
        masks.append(mask)
    return masks

def native(records):
    cases=[]
    for r in records:
        checks=[]
        for i,f in enumerate(r['question'][':question/answer-fields']):
            correct=correct_value(f)
            for a in f[':answer-field/choices']:
                checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==correct else 'rejected','purpose':'Owned source Boolean/radio choice; key checked independently from visible equation'})
        cases.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
    save(E/'native-input.json',cases)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'native-input.json'),str(E/'native-report.json')],check=True)

def coverage(records):
    groups={}
    for r in records:
        t=r['generation']['template'];mask=tuple(flags(r['question']))
        groups.setdefault(t,set()).add(mask)
    return {t:[list(m) for m in sorted(v)] for t,v in sorted(groups.items())}

def main():
    sources=source_replay(); records=[]; counterfactuals=[]
    for t,(level,_) in g.CASES.items():
        expected=feasible_cases(t)
        for mask in expected:
            p={'left_scales':[2,3,4],'right_scales':[3,4,5],'decisions':list(mask)}
            r=g.generate(level,10,t,p);inspect(r)
            assert tuple(flags(r['question']))==mask
            records.append(r)
        # Every one-row truth change with all other mathematical data held fixed.
        local=[r for r in records if r['generation']['template']==t]
        for i in range(3):
            pair=next(((a,b) for a in local for b in local if sum(x!=y for x,y in zip(flags(a['question']),flags(b['question'])))==1 and flags(a['question'])[i]!=flags(b['question'])[i]),None)
            if pair:
                a,b=pair;ae=prompt_equations(a['question'][':question/problem']);be=prompt_equations(b['question'][':question/problem'])
                assert ae[i]!=be[i]
                assert all(ae[j]==be[j] for j in range(3) if j!=i)
                assert a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']
                counterfactuals.append({'template':t,'changed_row':i,'before':a['question'][':question/id'],'after':b['question'][':question/id']})
        # Irrelevant coefficients preserve selection, and both source boundaries.
        original=g.generate(level,0,t,{'left_scales':[1]*3,'right_scales':[1]*3})
        boundary=g.generate(level,0,t,{'left_scales':[5]*3,'right_scales':[5]*3})
        inspect(boundary);assert flags(original['question'])==flags(boundary['question'])
        records.append(boundary)
    sample=[g.generate(level,seed) for level in ('easy','moderate') for seed in range(5)]
    for r in sample:inspect(r)
    records+=sample
    # Mutation witnesses ensure this validator catches wrong keys and solutions.
    mutation=copy.deepcopy(records[0]);f=mutation['question'][':question/answer-fields'][0]
    f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
    try:inspect(mutation)
    except AssertionError:pass
    else:raise AssertionError('Stale-key mutation was missed')
    mutation=copy.deepcopy(sources[0]);mutation['question'][':question/worked-solution']=mutation['question'][':question/worked-solution'].replace('n=-1','n=-2')
    try:inspect(mutation)
    except AssertionError:pass
    else:raise AssertionError('Stale-solution mutation was missed')
    for bad in (0,-1,6):
        try:g.generate('easy',0,'q-108911',{'left_scales':[bad,1,1],'right_scales':[1]*3})
        except AssertionError:pass
        else:raise AssertionError('Invalid scalar accepted')
    try:g.generate('hard')
    except AssertionError:pass
    else:raise AssertionError('Hard silently remapped')
    save(E/'records.json',records)
    save(E/'counterfactuals.json',counterfactuals)
    save(E/'coverage-before.json',coverage(records))
    native(sources+records)
    reps=[next(r for r in records if r['generation']['template']==t) for t in ('q-108911','q-108916','q-108912','q-108920')]
    save(E/'render-records.json',reps)
    report={'status':'passed','source_families':8,'generated_records_checked':len(records),'counterfactual_pairs':len(counterfactuals),'mathematics':'Visible LaTeX parsed; independent logarithmic-derivative test; solution p,q,n and normalized equations verified','coverage':coverage(records),'mutation_checks':['stale key detected','stale solution detected'],'limits':'Fixed nonpower functions are intended mathematical evidence. No claim to exhaustive cognitive shortcut detection.'}
    save(E/'validation.json',report)
    print(json.dumps({k:report[k] for k in ('status','source_families','generated_records_checked','counterfactual_pairs')}))

if __name__=='__main__':main()
