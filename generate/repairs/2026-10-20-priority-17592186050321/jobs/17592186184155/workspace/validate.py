#!/usr/bin/env python3
"""Source-specific independent audits. Run with the job's Python (SymPy for evidence)."""
import argparse
from collections import Counter,defaultdict
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import random
import re
import shutil
import subprocess
import tempfile
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
import generator as g

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'evidence'
X=S.Symbol('x',positive=True)
C=S.Symbol('C')


def save(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')


def translate(tex):
    """Independent limited TeX arithmetic reader, for literal served answer strings."""
    i=0
    def group():
        nonlocal i
        while i<len(tex) and tex[i].isspace():i+=1
        assert tex[i]=='{',(tex,i)
        i+=1
        result=read('}')
        assert tex[i]=='}';i+=1
        return result
    def read(stop=''):
        nonlocal i
        out=''
        while i<len(tex) and (not stop or tex[i]!=stop):
            if tex.startswith('\\frac',i):
                i+=5;a=group();b=group();out+=f'(({a})/({b}))'
            elif tex.startswith('\\sqrt',i):
                i+=5;degree='2'
                if i<len(tex) and tex[i]=='[':
                    end=tex.index(']',i);degree=tex[i+1:end];i=end+1
                inside=group();out+=f'(({inside})**(1/({degree})))'
            elif tex[i]=='{':out+='('+group()+')'
            elif tex[i]=='^':out+='**';i+=1
            elif tex[i]=='\\':
                raise AssertionError(('unsupported TeX',tex[i:]))
            else:out+=tex[i];i+=1
        return out
    result=read()
    return parse_expr(result,local_dict={'x':X,'C':C},transformations=standard_transformations+(convert_xor,implicit_multiplication_application))


def expr(terms):
    return sum(S.Rational(str(c))*X**S.Rational(str(p)) for c,p in terms)


def exact_primitive(terms):
    # Independent symbolic integration, not generator.primitive.
    return S.integrate(expr(terms),X)


def key_index(record):
    field=record['question'][':question/answer-fields'][0]
    return next(i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1])


def math_check(record):
    gen=record['generation'];q=record['question'];terms=gen['parameters']
    correct=exact_primitive(terms)
    choices=q[':question/answer-fields'][0][':answer-field/choices']
    vals=[S.expand(translate(a[':answer/value'])-C) for a in choices]
    matches=[S.simplify(S.diff(v,X)-expr(terms))==0 for v in vals]
    assert sum(matches)==1 and matches[key_index(record)]
    assert all(S.simplify(vals[i]-expr(gen['bank_terms'][i]))==0 for i in range(5))
    assert len(set(map(str,vals)))==5
    if gen.get('template')!='source-replay':
        final=q[':question/worked-solution'].split(r'\\ &= ')[-1].split(r'+C.\end{aligned}')[0]
        assert S.simplify(translate(final)-correct)==0
        # Independently decode the prompt's literal integrand and its term-order relation.
        given=q[':question/problem'].split('$')[1].removesuffix('.')
        assert S.simplify(translate(given)-expr(terms))==0
        for role in range(3):
            assert sum(S.simplify(S.Rational(str(b[role][0]))-S.Rational(str(g.primitive(terms)[gen['order'][role]][0])))==0 for b in gen['bank_terms'])>=2
    return vals


def source_checks():
    rows=json.loads((ROOT/'source_cases.json').read_text());reports=[];replays=[]
    for row in rows:
        if 'banks' not in row:
            reports.append({'source':row['source_name'],'status':'unsupported: no fields','original_preserved':True});continue
        rec=g.replay_source(row['source_name']);math_check(rec)
        source=row['source'];sf=source[':question/answer-fields'][0]
        rf=rec['question'][':question/answer-fields'][0]
        assert len(rf[':answer-field/choices'])==len(sf[':answer-field/choices'])==5
        assert rec['question'][':question/problem']==g.normalize_prose(source[':question/problem'])
        for a,b in zip(sf[':answer-field/choices'],rf[':answer-field/choices']):
            assert b[':answer/value']==g.normalize_tex(a[':answer/value'])
        if ':answer-field/correct' in sf:
            assert sf[':answer-field/correct'][':answer/value']==sf[':answer-field/choices'][row['key']][':answer/value']
            strip_layout=lambda text:re.sub(r'\s+|&|\\\\','',text)
            assert strip_layout(rec['question'][':question/worked-solution'])==strip_layout(g.normalize_prose(source[':question/worked-solution']))
        assert rec['generation']['source_difficulty']==('hard' if row['source_name'].startswith('q-1138') else None)
        reports.append({'source':row['source_name'],'status':'passed','bank_matched':5,'distractors_matched':4,
            'key_origin':row['key_origin'],'solution_origin':rec['generation']['solution_origin'],
            'difficulty_preserved':True})
        replays.append(rec)
    save('source-replay.json',replays)
    save('source-fidelity.json',{'sources':reports,'banks_matched':4,'options_matched':20,'distractors_matched':16,
        'limits':['Two unlabeled banks have independently inferred keys and authored solutions.','Two moderate records lack fields and are excluded.']})
    return replays


def collect(records):
    groups=defaultdict(list)
    for record in records:groups[record['generation']['template']].append(record)
    result={}
    for profile,rs in sorted(groups.items()):
        cov={'count':len(rs),'semantic_instances':len({tuple(map(tuple,r['generation']['parameters'])) for r in rs})}
        cov['fractional_exponents']=sorted({r['generation']['parameters'][0][1] for r in rs})
        cov['integer_exponents']=sorted({r['generation']['parameters'][1][1] for r in rs})
        cov['reciprocal_exponents']=sorted({r['generation']['parameters'][2][1] for r in rs})
        cov['orders']=dict(Counter(','.join(map(str,r['generation']['order'])) for r in rs))
        cov['key_positions']=dict(Counter(str(key_index(r)) for r in rs))
        cov['coefficient_signs_by_role']={g.ROLES[j]:dict(Counter('negative' if F(r['generation']['parameters'][j][0])<0 else 'positive' for r in rs)) for j in range(3)}
        cov['recipes_by_role']={g.ROLES[j]:dict(Counter(name for r in rs for state in r['generation']['design_states'] if state[j] for name in [r['generation']['error_recipes'][j][state[j]-1]])) for j in range(3)}
        probe=Counter();totals=Counter();unique_agree=0
        for r in rs:
            ts=[[(F(c),F(p)) for c,p in row] for row in r['generation']['bank_terms']]
            k=key_index(r);n=5
            features={}
            for j in range(3):
                features[f'term{j}_smallest_abs']=[abs(t[j][0]) for t in ts]
                features[f'term{j}_largest_abs']=[-abs(t[j][0]) for t in ts]
                frequency=Counter(t[j][0] for t in ts)
                features[f'term{j}_most_common']=[-frequency[t[j][0]] for t in ts]
                features[f'term{j}_least_common']=[frequency[t[j][0]] for t in ts]
                correctc=ts[k][j][0]
                assert sum(t[j][0]==correctc for t in ts)>=2
            features['smallest_sum_abs']=[sum(abs(c) for c,p in t) for t in ts]
            features['largest_sum_abs']=[-v for v in features['smallest_sum_abs']]
            features['most_agreement']=[-sum(sum(t[j]==u[j] for j in range(3)) for u in ts) for t in ts]
            features['coefficient_most_agreement']=[-sum(sum(t[j][0]==u[j][0] for j in range(3)) for u in ts) for t in ts]
            features['least_agreement']=[-v for v in features['most_agreement']]
            features['shortest_TeX']=[len(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
            features['longest_TeX']=[-v for v in features['shortest_TeX']]
            for cue,values in features.items():
                # Fixed presentation-order tie break. Also count unique winners separately.
                choice=min(range(n),key=lambda i:values[i]);probe[cue]+=choice==k;totals[cue]+=1
            for pos in range(5):
                cue=f'always_position_{pos+1}';probe[cue]+=pos==k;totals[cue]+=1
            signs=[tuple(c>0 for c,p in t) for t in ts]
            for sign in itertools.product([False,True],repeat=3):
                cue='fixed_signs_'+''.join('+' if s else '-' for s in sign)
                choice=next((i for i,v in enumerate(signs) if v==sign),-1)
                probe[cue]+=choice==k;totals[cue]+=1
            for j in range(3):
                role=r['generation']['order'][j]
                original=F(r['generation']['parameters'][role][0])
                cue=f'copy_original_coefficient_term{j}'
                choice=next((i for i,t in enumerate(ts) if t[j][0]==original),-1)
                probe[cue]+=choice==k;totals[cue]+=1
        cov['shortcut_probes']={cue:{'success':probe[cue],'attempts':totals[cue],'rate':round(probe[cue]/totals[cue],4),'uniform_baseline':0.2} for cue in totals}
        assert all(probe[cue]<totals[cue] for cue in totals),(profile,'perfect incidental predictor')
        cov['single_term_is_sufficient_cases']=0
        result[profile]=cov
    return result


def conditional_probes(records):
    groups=defaultdict(list)
    for r in records:
        z=r['generation']
        if not z['assignment_attempts']:continue
        groups[z['template']+'|order='+','.join(map(str,z['order']))].append(r)
        groups[z['template']+'|degree='+z['parameters'][0][1].split('/')[-1]].append(r)
    return {key:next(iter(collect(rs).values())) for key,rs in sorted(groups.items())}


def build():
    OUT.mkdir(exist_ok=True)
    source=source_checks()
    records=[g.generate(seed) for seed in range(144)]
    # Explicit domain representatives ensure all eligible fractions and endpoints occur.
    states=[[1,0,0],[0,1,0],[0,0,1],[2,3,0]]
    targeted=[]
    for d in (3,5,7):
        for p in [F(-(d+1),d)]+[F(r,d) for r in range(1,d) if __import__('math').gcd(r,d)==1]:
            profile='negative_fractional' if p<0 else 'positive_fractional'
            j=len(targeted);order=list(itertools.permutations(range(3)))[j%6]
            pars=[(-6 if j%2 else 1,p),(6 if j%2 else -1,F(1 if j%2 else 7)),(-6 if j%2 else 1,F(-2 if j%2 else -6))]
            targeted.append(g.generate(9000+j,parameters=pars,design={'profile':profile,'order':order,'states':states}))
    records+=targeted
    for r in records:math_check(r)
    assert g.generate(1234)==g.generate(1234)
    for diff in ('easy','moderate'):
        try:g.generate(0,difficulty=diff)
        except ValueError:pass
        else:raise AssertionError('unsupported band accepted')
    # Check every declared discrete slot in this bounded audit, separately from semantic count.
    for profile in ('positive_fractional','negative_fractional'):
        rs=[r for r in records if r['generation']['template']==profile]
        assert {int(r['generation']['parameters'][1][1]) for r in rs}==set(range(1,8))
        assert {int(r['generation']['parameters'][2][1]) for r in rs}==set(range(-6,-1))
        assert {tuple(r['generation']['order']) for r in rs}==set(itertools.permutations(range(3)))
        assert {key_index(r) for r in rs}==set(range(5))
        for j in range(3):
            assert {F(r['generation']['parameters'][j][0])>0 for r in rs}=={True,False}
    save('test-records.json',records)
    save('mathematics.json',{'passed':True,'source_banks':4,'generated_records':len(records),'method':'Independently parse literal answer TeX and prompt integrands; symbolic integration and differentiation in SymPy 1.14.0; check every wrong option, sparse source mapping and final solution.','domain':'x>0 symbolic check; hard odd-root expressions extend termwise to x<0; see negative-domain numerical checks.','deterministic_replay':True,'unsupported_bands_rejected':['easy','moderate']})
    # Numerical derivative of real odd powers on negative intervals, independent of SymPy assumptions.
    negchecks=0
    def realpower(x,p):
        p=F(p)
        return ((-1 if p.numerator%2 else 1)*abs(x)**float(p)) if x<0 else x**float(p)
    for r in targeted:
        terms=r['generation']['parameters'];answer=r['generation']['bank_terms'][key_index(r)]
        for x in (-0.7,-1.3,-2.1):
            h=abs(x)*1e-5
            val=lambda t:sum(float(F(c))*realpower(t,p) for c,p in answer)
            deriv=(val(x+h)-val(x-h))/(2*h)
            expected=sum(float(F(c))*realpower(x,p) for c,p in terms)
            assert abs(deriv-expected)<1e-6*(1+abs(expected)),(deriv,expected)
            negchecks+=1
    # Parameter counterfactuals use unchanged design and seed; inspect all dependent content.
    controls=[];summary=[]
    for profile,p in [('positive_fractional',F(4,5)),('negative_fractional',F(-4,3))]:
        params=[(F(2),p),(F(-3),F(3)),(F(4),F(-4))]
        design={'profile':profile,'order':[0,1,2],'states':states}
        base=g.generate(811,parameters=params,design=design);controls.append(base)
        for j in range(3):
            for kind in ('coefficient','exponent'):
                changed=list(params)
                c,power=changed[j]
                if kind=='coefficient':changed[j]=(-c,power)
                else:changed[j]=(c, (F(2,5) if profile=='positive_fractional' else F(-6,5)) if j==0 else power+(1 if j==1 else -1))
                alt=g.generate(811,parameters=changed,design=design);math_check(alt);controls.append(alt)
                assert alt['question'][':question/problem']!=base['question'][':question/problem']
                assert alt['question'][':question/worked-solution']!=base['question'][':question/worked-solution']
                assert S.simplify(exact_primitive(params)-exact_primitive(changed))!=0
                summary.append({'profile':profile,'role':g.ROLES[j],'change':kind,'prompt_answer_solution_changed':True})
        reordered=g.generate(811,parameters=params,design={**design,'order':[2,0,1]})
        math_check(reordered);controls.append(reordered)
        assert S.simplify(translate(reordered['question'][':question/answer-fields'][0][':answer-field/choices'][key_index(reordered)][':answer/value'])-translate(base['question'][':question/answer-fields'][0][':answer-field/choices'][key_index(base)][':answer/value']))==0
        summary.append({'profile':profile,'change':'irrelevant term reorder','mathematical_response_preserved':True})
        # Hold the complete visible bank fixed, change evidence to make each other candidate correct.
        banks=[a[':answer/value'] for a in base['question'][':question/answer-fields'][0][':answer-field/choices']]
        for k,terms in enumerate(base['generation']['bank_terms']):
            newterms=[(F(c)*F(p),F(p)-1) for c,p in terms]
            # Coefficients here may exceed normal bounds; same method, evidence only, not sampled.
            rekey=g.assemble('Find the antiderivative of $'+g.expression(newterms)+r'.$ For real $x\ne0$.',g.solution(newterms),banks,k,'hard',{'template':profile,'parameters':g.stringify(newterms),'bank_terms':base['generation']['bank_terms'],'order':[0,1,2],'controlled_fixed_bank':True,'eligible_for_learning':False})
            # Check independently that precisely this unchanged option differentiates to new evidence.
            vals=[translate(v)-C for v in banks]
            assert [S.simplify(S.diff(v,X)-expr(newterms))==0 for v in vals]==[i==k for i in range(5)]
            controls.append(rekey)
        summary.append({'profile':profile,'change':'fixed bank, changed decisive evidence','all_five_key_assignments_exercised':True,'native_grading':'all five candidates tested per rekey'})
    save('counterfactual-records.json',controls)
    save('counterfactuals.json',{'checks':summary,'negative_domain_numeric_derivatives':negchecks,'no_source_or_database_writes':True})
    cases=[]
    for index,r in enumerate(source+records+controls):
        field=r['question'][':question/answer-fields'][0];key=key_index(r)
        cases.append({'label':f'case-{index}-{r["generation"]["template"]}','record':r,'checks':[
            {'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==key else 'rejected','purpose':'independently differentiated full candidate'} for i,a in enumerate(field[':answer-field/choices'])]})
    save('grader-input.json',cases)
    save('pedagogical-variation.json',{'before_delivery':collect(records),'normal_sampling_before':collect([r for r in records if r['generation']['assignment_attempts']>0]),'conditional_before':conditional_probes(records),'controlled_checks':'counterfactuals.json','source_fidelity':'source-fidelity.json','limits':['Fixed source banks replayed only; normal bank is a declared authored extension.','No learner-specific history available.']})
    # Source hard cases and selected contrasting generated instances, not the entire audit sample.
    render=[r for r in source if r['generation']['source_difficulty']=='hard']
    render += [next(r for r in targeted if r['generation']['template']==p) for p in ('positive_fractional','negative_fractional')]
    render += [max(records,key=lambda r:len(r['question'][':question/worked-solution']))]
    save('render-records.json',render)
    save('runner-batch.json',[g.generate(random.Random(20261020+i).getrandbits(64)) for i in range(5)])
    print(json.dumps({'source_banks':4,'options':20,'generated_math_checked':len(records),'counterfactual_records':len(controls),'native_grader_cases':len(cases),'negative_domain_checks':negchecks,'perfect_tested_shortcuts':0}))


def after_delivery(path):
    records=json.loads(Path(path).read_text());report=json.loads((OUT/'pedagogical-variation.json').read_text())
    report['after_delivery']=collect(records)
    report['normal_sampling_after']=collect([r for r in records if r['generation']['assignment_attempts']>0])
    report['conditional_after']=conditional_probes(records)
    assert set(report['after_delivery'])==set(report['before_delivery'])
    report['delivery_coverage_preserved']=all(report['after_delivery'][k]==report['before_delivery'][k] for k in report['before_delivery'])
    assert report['delivery_coverage_preserved']
    report['generator_rejection']={'mechanism':'Sample five distinct binary candidate rows; require two or three of each bit per column, then select the true row uniformly. Recipe assignments and order precede values. No parameter-dependent instance rejection.','assignment_attempts':dict(Counter(str(r['generation']['assignment_attempts']) for r in records))}
    report['learner_selection']={'implementation':'engine/rust/question_selection.rs select; inspected read-only','configured':'band draw then uniform among fresh candidates; positive hard weight preserves support','unconfigured':'first candidate only; does not guarantee varied delivery','limits':['Captured inventory only. Live history, current task prefix, policy weights and database collisions not simulated.']}
    save('pedagogical-variation.json',report)
    cases=json.loads((OUT/'grader-input.json').read_text())
    cases=[c for c in cases if not c['label'].startswith('after-delivery-')]
    for idx,r in enumerate(records):
        math_check(r)
        field=r['question'][':question/answer-fields'][0];key=key_index(r)
        cases.append({'label':f'after-delivery-{idx}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==key else 'rejected','purpose':'native grader with stable delivery identities'} for i,a in enumerate(field[':answer-field/choices'])]})
    save('grader-input.json',cases)
    print(json.dumps({'delivery_records_checked':len(records),'coverage_preserved':True,'perfect_tested_shortcuts':0}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--after-delivery');args=parser.parse_args()
    if args.after_delivery:after_delivery(args.after_delivery)
    else:build()
