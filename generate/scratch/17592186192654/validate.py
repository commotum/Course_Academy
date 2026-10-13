#!/usr/bin/env python3
"""Independent checks read the rendered system, selected values and ALL stages."""
import copy, importlib.util, json, re, subprocess, sys, hashlib
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def algebra(s):
    s=s.replace('&','').strip().replace('\\{','').removeprefix('{')
    assert not '\\' in s,s
    return sp.expand(parse_expr(s,transformations=standard_transformations+(implicit_multiplication_application,)))
def equation(s):
    l,r=s.split('=');return algebra(l),algebra(r)
def printed_system(record):
    text=record['question'][':question/problem'];body=re.search(r'\n\$(.*?)\$\n',text).group(1)
    return [equation(row) for row in body.replace('\\{','').removeprefix('{').split('; ')]
def correct_value(field):return next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
def formatting(text):
    assert text.count('$')%2==0
    text=text.replace('\\{','').replace('{{field-1}}','').replace('{{field-2}}','')
    balance=0
    for c in text:
        if c=='{':balance+=1
        if c=='}':balance-=1
        assert balance>=0
    assert balance==0
    assert not re.search(r'--|\+-',text)
def validate_record(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];assert q[':question/difficulty'] in [':question.difficulty/'+level for level in ('easy','moderate','hard')]
    x,y=map(sp.Symbol,r['generation']['parameters']['variables'])
    rows=printed_system(r);fields=q[':question/answer-fields'];by_key={f[':answer-field/key']:f for f in fields}
    scalar=[sp.Rational(a[':answer/value']) for a in by_key['field-2'][':answer-field/choices']]
    assert len(scalar)==4 and len(set(scalar))==4
    valid=[(i,n) for i in (0,1) for n in scalar if sp.expand(n*rows[i][0]+rows[1-i][0]).coeff(x)==0]
    assert len(valid)==1,valid
    row,m=valid[0]
    assert correct_value(by_key['field-1'])==['first','second'][row]
    assert sp.Rational(correct_value(by_key['field-2']))==m
    for f in fields:
        assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
        assert f[':answer-field/type']==':answer-field.type/select'
        assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(f[':answer-field/choices'])
    s=q[':question/worked-solution'];formatting(q[':question/problem']);formatting(s)
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',s,re.S);assert len(blocks)==2
    # Explicit operation block: one row tagged with one multiplication; other unchanged.
    operation=blocks[0].replace('\\{','').split('; ');assert sum('\\cdot' in r for r in operation)==1
    for i,e in enumerate(operation):
        if i==row:
            mm=re.fullmatch(r'\((.*?)\)\\cdot \((-?\d+)\)',e);assert mm and int(mm[2])==m
            assert equation(mm[1])==rows[i]
        else:assert equation(e)==rows[i]
    stage=blocks[1].replace('\\begin{aligned}\n','').replace('\n\\end{aligned}','').split(' \\\\\n');assert len(stage)==4
    derived=[equation(e) for e in stage]
    expect=[(m*a,m*b) if i==row else (a,b) for i,(a,b) in enumerate(rows)]
    assert derived[:2]==expect
    sums=tuple(sp.expand(expect[0][i]+expect[1][i]) for i in (0,1))
    assert derived[2]==sums and derived[3]==sums
    assert derived[3][0].coeff(x)==0 and derived[3][0].coeff(y)!=0
    assert '(' in stage[2] and ')' in stage[2] and '(' not in stage[3]
    assert f'first equation is ${rows[0][0].coeff(x)}$' in s
    assert f'second equation it is ${rows[1][0].coeff(x)}$' in s
    assert f'turn into ${m*rows[row][0].coeff(x)}$' in s
    assert f'\\text{{{["first","second"][row]}}}' in s
    assert f'\\color{{blue}}{m}' in s
    # Solution set equivalence is independently checked, but eligibility means FIRST
    # variable removed by one scaling and adding, NOT merely equivalent full system.
    original=sp.solve([a-b for a,b in rows],(x,y))
    changed=sp.solve([a-b for a,b in expect],(x,y));assert original==changed
    assert sp.simplify((derived[3][0]-derived[3][1]).subs(original))==0
    assert not re.search(r'back|substitut|solution to the system',s,re.I)
    return row,m

def main():
    cases=json.loads((HERE/'source-cases.json').read_text());fidelity=[];records=[]
    for c in cases:
        r=g.generate('easy',parameters=c['parameters'],profile=c['bank_profile'],template=c['template'])
        original=g.ORIGINALS[c['source_id']]
        projected=copy.deepcopy(original)
        for f in projected[':question/answer-fields']:
            f[':answer-field/type']=f[':answer-field/type'][':db/ident']
            for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
        assert r['question']==projected, c['source_id']
        assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
        altered=copy.deepcopy(c['parameters']);altered['c1']+=1
        changed=g.generate('easy',parameters=altered,profile=c['bank_profile']);assert changed['question'][':question/problem']!=original[':question/problem']
        assert ':question/difficulty' not in changed['question'] and ':question/worked-solution' not in changed['question']
        assert all(':answer-field/correct' not in f for f in changed['question'][':question/answer-fields'])
        coefficients=copy.deepcopy(c['parameters'])
        coefficients.update(a2=-6,b2=4) if c['source_id']=='q-210858' else coefficients.update(a1=4,b1=6)
        coefficient_replay=g.generate('easy',parameters=coefficients,profile=c['bank_profile'])
        scalar_field=next(f for f in coefficient_replay['question'][':question/answer-fields'] if f[':answer-field/key']=='field-2')
        expected=['4','6','-6','-4'] if c['source_id']=='q-210858' else ['6','-4','4','-6']
        assert [a[':answer/value'] for a in scalar_field[':answer-field/choices']]==expected
        assert coefficient_replay['question'][':question/id']!=r['question'][':question/id']
        # Normal authored completion independently derives omitted correct refs.
        complete=g.generate('easy',parameters=c['parameters']);validate_record(complete);records.append(complete)
        fidelity.append({'source_id':c['source_id'],'question_all_attributes_exact_after_enum_projection':True,'bank_values_matched':6,'observed_correct_designations':0,'inferred_correct_designations':2,'worked_solution_presence_preserved':True})
    variety={};orientations={};signs={}
    for level in ('easy','moderate','hard'):
        seen=set();rr=set();ss=set()
        for seed in range(600):
            r=g.generate(level,seed);row,m=validate_record(r);seen.add(r['generation']['mathematical_fingerprint']);rr.add(row);ss.add(sp.sign(m))
            if seed<12:records.append(r)
            fixed=g.generate(level,seed+10000,parameters=r['generation']['parameters'])
            assert fixed['question'][':question/id']==r['question'][':question/id']
            assert fixed['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
        variety[level]=len(seen);orientations[level]=sorted(rr);signs[level]=[int(v) for v in sorted(ss)]
        # Exhaust the actual signed division operands, quotient bounds and row
        # choice; global sign aliases must collapse, nonunit operands remain.
        catalog=set()
        for small in ((1,) if level=='easy' else (2,3,4)):
            for ratio in (range(2,8) if level=='easy' else range(2,5) if level=='moderate' else range(5,8)):
                for reverse in (False,True):
                    for sign1 in (-1,1):
                        for sign2 in (-1,1):
                            aa=[small,small*ratio]
                            if reverse:aa.reverse()
                            p=dict(a1=sign1*aa[0],a2=sign2*aa[1],b1=1,b2=1,c1=1,c2=2,variables='xy')
                            record=g.generate(level,parameters=p);validate_record(record)
                            catalog.add(record['generation']['mathematical_fingerprint'])
        assert len(catalog)=={'easy':24,'moderate':36,'hard':36}[level]
        assert seen==catalog and rr=={0,1} and ss=={-1,1}
    # Reject invalid explicit workload and complete banks, never silently resample.
    bad=[('moderate',g.ANCHORS['q-210858']),('hard',dict(g.ANCHORS['q-210859'],a1=6,a2=2)),('easy',dict(g.ANCHORS['q-210858'],a1=-1,a2=-1)),('moderate',dict(a1=2,a2=6,b1=1,b2=3,c1=1,c2=2,variables='xy'))]
    for level,p in bad:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('accepted bad',level,p))
    # Equal row count but collapsed grouped addition must fail structural QA.
    mutation=copy.deepcopy(records[0]);s=mutation['question'][':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',s,re.S);st=blocks[1].split(' \\\\\n');st[-2]=st[-1].split('\n\\end')[0]
    mutation['question'][':question/worked-solution']=s.replace(blocks[1],' \\\\\n'.join(st))
    try:validate_record(mutation)
    except AssertionError:pass
    else:raise AssertionError('Collapsed source operation structure not rejected')
    native=[]
    for j,r in enumerate(records):
        checks=[]
        for fi,f in enumerate(r['question'][':question/answer-fields']):
            for a in f[':answer-field/choices']:
                checks.append(dict(field_index=fi,submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',purpose='owned choice; mathematics independently verified'))
        native.append(dict(label=f'completed-{j}',record=r,checks=checks))
    (HERE/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    report=json.loads((HERE/'engine-report.json').read_text())
    result=dict(status='passed',source_provenance={k:v for k,v in g.SOURCE.items() if k!='record'},source_questions=2,raw_exact_questions=2,raw_exact_complete_banks=4,matched_source_choices=12,source_correct_refs_present=0,inferred_correct_refs=4,observed_source_worked_solutions=0,source_correct_ref_fidelity='not observable; absent',source_raw_format='two unmatched literal braces retained only in evidence',normal_format_repaired=2,authored_levels=['easy','moderate','hard'],samples_per_level=600,meaningful_sampled_tasks=variety,finite_possible_assessed_tasks={'easy':24,'moderate':36,'hard':36},scaled_row_coverage=orientations,multiplier_sign_coverage=signs,independent_display_and_stage_checks='passed',mutation_regression='passed',native={k:v for k,v in report.items() if k!='records'},native_binary_sha256=hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),runtime={'python':sys.version.split()[0],'sympy':sp.__version__},unresolved_findings=['No source difficulty, correct designations or practice worked solutions are observed. Completed records and all level labels are authored, not recovered.'])
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    reviews=[{'label':'RAW ORIGINAL '+c['source_id'],'record':g.generate('easy',parameters=c['parameters'],profile=c['bank_profile'])} for c in cases]
    reviews+=[{'label':'AUTHORED completion at original '+c['source_id'],'record':g.generate('easy',parameters=c['parameters'])} for c in cases]
    reviews+=[{'label':f'AUTHORED {level} variant seed {seed}','record':g.generate(level,seed)} for level in ('easy','moderate','hard') for seed in (0,1)]
    # Each raw bank also has a visibly changed-parameter evidence variant.
    for c in cases:
        p=copy.deepcopy(c['parameters']);p['c1']+=2;p['c2']-=1
        p.update(a2=-6,b2=4) if c['source_id']=='q-210858' else p.update(a1=4,b1=6)
        reviews.append({'label':'RAW parameterized evidence variant '+c['source_id'],'record':g.generate('easy',parameters=p,profile=c['bank_profile'])})
    (HERE/'review.json').write_text(json.dumps(reviews,indent=2)+'\n')
    (HERE/'review.md').write_text('# First-variable elimination review\n\nRaw originals retain omitted keys and source brace anomaly; every completed record below is explicitly authored.\n\n'+'\n\n---\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in reviews)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
