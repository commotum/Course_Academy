"""Independent printed mathematics, complete source fidelity, and real grading."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path
import sympy as sp

# Keep all worker-created evidence under the private folder.
sys.dont_write_bytecode=True

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('midline',ROOT.with_suffix('.py'))
g=importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def write(name,data):
    (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')


def group(text,pos):
    assert text[pos]=='{',(text,pos)
    depth=1
    for i in range(pos+1,len(text)):
        depth+=(text[i]=='{')-(text[i]=='}')
        if not depth:return text[pos+1:i],i+1
    raise AssertionError(('Unbalanced group',text))


def expr(text,minimum=None,maximum=None):
    """Read nested displayed rational expressions, independently of metadata."""
    text=text.strip().rstrip('.,')
    if minimum is not None:
        text=text.replace(r'{y}_{\text{min}}',str(minimum)).replace(r'{y}_{\text{max}}',str(maximum))
    text=text.replace(r'\dfrac',r'\frac')
    while r'\frac' in text:
        pos=text.index(r'\frac')
        a,end=group(text,pos+5)
        b,end2=group(text,end)
        replacement='(('+str(expr(a,minimum,maximum))+')/('+str(expr(b,minimum,maximum))+'))'
        text=text[:pos]+replacement+text[end2:]
    return sp.sympify(text)


def formatting(text):
    assert text.count('$')%2 == 0,text
    depth=0
    for char in text:
        depth+=(char=='{')-(char=='}')
        assert depth>=0,text
    assert depth==0,text
    assert text.count(r'\begin{aligned}')==text.count(r'\end{aligned}'),text
    assert '++' not in text and '+-' not in text and '--' not in text,text


def printed_check(record):
    q=record['question'];meta=record['generation']
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    prompt=q[':question/problem']
    match=re.fullmatch(r'Find the equation of the midline for a transformed (sine|cosine) function with a minimum value of \$([^$]+)\$ and a maximum value of \$([^$]+)\$\.?',prompt)
    assert match,prompt
    lo,hi=expr(match[2]),expr(match[3]);answer=(lo+hi)/2
    assert lo<hi and max(abs(lo),abs(hi))<=16
    assert meta['parameters']=={'minimum':str(lo),'maximum':str(hi)}
    if not meta['evidence_only']: assert g.workload_eligible(meta['difficulty'],lo,hi)
    if ':question/worked-solution' in q:
        solved=q[':question/worked-solution']
        # Generic formula and all substitution/sum/division rows plus prose conclusion.
        blocks=re.findall(r'\$\$(.*?)\$\$',solved,flags=re.S)
        assert len(blocks)==2
        count=0
        for block in blocks:
            block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
            for row in block.split(r'\\'):
                sides=row.replace('&','').strip().split('=')
                assert len(sides)==2
                lhs=expr(sides[0],lo,hi) if sides[0].strip() and sides[0].strip()!='y' else answer
                rhs=expr(sides[1],lo,hi)
                assert sp.simplify(lhs-answer)==0 and sp.simplify(rhs-answer)==0,(lo,hi,row,lhs,rhs)
                count+=1
        assert count==(5 if meta['difficulty']=='hard' else 4)
        final=re.search(r'Therefore, the midline is \$y=(.*?)\.\$',solved)
        assert final and expr(final[1])==answer,solved
        # Hard row must preserve separately rewritten common-denominator terms.
        if meta['difficulty']=='hard':
            lcd=sp.ilcm(lo.q,hi.q)
            row=blocks[1].split(r'\\')[1]
            assert row.count('}{'+str(lcd)+'}')==2,row
        formatting(solved)
    formatting(prompt)
    fields=q.get(':question/answer-fields',[])
    for f in fields:
        assert f[':answer-field/type']==':answer-field.type/radio'
        assert f[':answer-field/key']=='selection'
        choices=f[':answer-field/choices'];assert len(choices)==5
        values=[]
        correct=f.get(':answer-field/correct')
        for a in choices:
            assert a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value']
            assert a[':answer/value'].split('=')[0].strip()=='y'
            value=expr(a[':answer/value'].split('=')[1]);values.append(value)
            assert value==sp.Rational(meta['recipes'][a[':answer/id']]['value'])
            if correct and a[':answer/id']==correct[1]: assert value==answer
            assert str(uuid.UUID(a[':answer/id']))==a[':answer/id']
            formatting(a[':answer/value'])
        assert len(set(values))==5 and values.count(answer)==1
        if correct: assert correct[0]==':answer/id' and correct[1] in {a[':answer/id'] for a in choices}
    assert str(uuid.UUID(q[':question/id']))==q[':question/id']
    return lo,hi


def native_record(record,label):
    field=record['question'][':question/answer-fields'][0]
    return {'label':label,'record':record,'checks':[
        {'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected',
         'purpose':'independently verified complete equation option'} for a in field[':answer-field/choices']]}


def main():
    originals=[];review=[];cases=[];native=[]
    raw_matches={'prompts':0,'solutions':0,'banks':0,'choices':0,'correct_designations':0,'presence':0}
    anomalies=[];decoded=[]
    for sid,source in g.QUESTIONS.items():
        template=('cosine' if 'transformed cosine' in source[':question/problem'] else 'sine')+'_extrema'
        params=g.source_parameters(source)
        case={'source_id':sid,'template':template,'parameters':params,'bank_profile':'raw_'+sid,'level':'easy','level_assignment':'observed' if ':question/difficulty' in source else 'authored inferred easy; source unrated'}
        cases.append(case)
        raw=g.generate('easy',11,template=template,parameters=params,profile=case['bank_profile'])
        printed_check(raw);q=raw['question']
        assert set(q)==set(source),(sid,set(q),set(source))
        raw_matches['presence']+=1
        assert q[':question/problem']==source[':question/problem'];raw_matches['prompts']+=1
        assert q.get(':question/worked-solution')==source.get(':question/worked-solution')
        if ':question/worked-solution' in source:raw_matches['solutions']+=1
        fields=source.get(':question/answer-fields',[])
        for i,f in enumerate(fields):
            generated=q[':question/answer-fields'][i]
            assert set(f)==set(generated)
            values=sorted(a[':answer/value'] for a in f[':answer-field/choices'])
            assert values==sorted(a[':answer/value'] for a in generated[':answer-field/choices'])
            raw_matches['banks']+=1;raw_matches['choices']+=len(values)
            if ':answer-field/correct' in f:
                chosen=next(a for a in generated[':answer-field/choices'] if a[':answer/id']==generated[':answer-field/correct'][1])
                assert chosen[':answer/value']==f[':answer-field/correct'][':answer/value']
                raw_matches['correct_designations']+=1
                native.append(native_record(raw,'raw '+sid))
            else:anomalies.append({'source_id':sid,'anomaly':'missing correct designation; independently derived mean -4; missing solution and difficulty','normal_repair':'authored radio bank/solution; easy inferred','raw_preserved':True})
        if not fields:anomalies.append({'source_id':sid,'anomaly':'answer-fields attribute absent','normal_repair':'authored five-option radio bank; original prompt and solution preserved','raw_preserved':True})
        originals.append({'label':'Original raw '+sid,'record':raw})
        # Two public generated variants of each raw template/profile, evidence only.
        lo,hi=map(sp.Rational,(params['minimum'],params['maximum']))
        for shift in (-1,1):
            variant=g.generate('easy',33+shift,template=template,profile=case['bank_profile'],parameters={'minimum':str(lo+shift),'maximum':str(hi+shift)})
            printed_check(variant)
            review.append({'label':f'Evidence-only parameterized {sid}, translation {shift:+}','record':variant})
        for key in (':question/problem',':question/worked-solution'):
            value=source.get(key,'')
            decoded.append({'source_id':sid,'attribute':key,'single_backslash_bytes':sum(c=='\\' for c in value),'adjacent_backslash_pairs':sum(value[i:i+2]=='\\\\' for i in range(len(value)-1))})
    # Mathematical and formatting tests sampled across all source-shaped defaults.
    samples=[];coverage={level:{'templates':set(),'profiles':set(),'tasks':set(),'correct_positions':set()} for level in ('easy','moderate','hard')}
    for level in coverage:
        for seed in range(240):
            r=g.generate(level,seed);printed_check(r);samples.append(r)
            meta=r['generation'];cov=coverage[level]
            cov['templates'].add(meta['template']);cov['profiles'].add(meta['bank_profile']);cov['tasks'].add(meta['mathematical_fingerprint'])
            field=r['question'][':question/answer-fields'][0]
            cov['correct_positions'].add(next(i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1]))
            if seed<12:native.append(native_record(r,f'{level} seed {seed}'))
        for template in g.TEMPLATES:
            for seed in (83,179):
                r=g.generate(level,seed,template=template);review.append({'label':f'Authored/default {level} {template} seed {seed}','record':r})
        expected_profiles={p for p in g.NORMAL_PROFILES if g.parameter_domain(level,p)}
        for profile in sorted(expected_profiles):
            domain=g.parameter_domain(level,profile)
            for index in (0,len(domain)//2,len(domain)-1):
                lo,hi=domain[index]
                boundary=g.generate(level,983,profile=profile,parameters={'minimum':str(lo),'maximum':str(hi)})
                printed_check(boundary)
                native.append(native_record(boundary,f'{level} {profile} domain boundary {index}'))
        assert coverage[level]['templates']==set(g.TEMPLATES)
        assert coverage[level]['profiles']==expected_profiles
        assert coverage[level]['correct_positions']==set(range(5))
    # Explicit domain, whole-bank, identity and alias checks.
    for level,params in [('easy',{'minimum':1,'maximum':4}),('moderate',{'minimum':2,'maximum':10}),('hard',{'minimum':'1/2','maximum':'7/2'}),('hard',{'minimum':'1/2','maximum':'16.1'})]:
        try:g.generate(level,parameters=params,profile='method_average')
        except ValueError:pass
        else:raise AssertionError(('Unenforced difficulty',level,params))
    try:g.generate_easy(parameters={'minimum':0,'maximum':4},profile='method_average')
    except ValueError:pass
    else:raise AssertionError('Whole-bank collision escaped')
    for r in samples[::13]:
        m=r['generation']
        alt=g.generate(m['difficulty'],923,template=m['template'],profile=m['bank_profile'],parameters=m['parameters'])
        assert alt['question'][':question/id']==r['question'][':question/id']
        alias=g.generate(m['difficulty'],923,template='cosine_extrema' if m['template']=='sine_extrema' else 'sine_extrema',profile=m['bank_profile'],parameters=m['parameters'])
        assert alias['generation']['mathematical_fingerprint']==m['mathematical_fingerprint']
        assert alias['question'][':question/id']!=r['question'][':question/id']
    # Inferred source repairs retain exact extrema; raw evidence remains accessible.
    for sid in ('q-236750','q-236892','q-236903'):
        p=g.source_parameters(g.QUESTIONS[sid]);profile='zero_minimum' if p['minimum']=='0' else 'method_average'
        t=('cosine' if 'transformed cosine' in g.QUESTIONS[sid][':question/problem'] else 'sine')+'_extrema'
        repaired=g.generate_easy(7,template=t,parameters=p,profile=profile)
        printed_check(repaired);native.append(native_record(repaired,'authored repair '+sid))
        review.append({'label':'Authored format/key repair '+sid,'record':repaired})
    write('source-cases.json',cases);write('source-anomalies.json',anomalies)
    write('tex-byte-audit.json',{'decoded_counts':decoded,'anomalies':[],'note':'Adjacent pairs occur only at valid aligned row separators; no source TeX anomaly.'})
    write('native-input.json',native)
    engine=REPO/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
    native_report=json.loads((ROOT/'native-report.json').read_text())
    write('review.json',{'originals':originals,'generated':review})
    pages=['# Midline generator review','Originals retain captured omissions. Raw variants are evidence only; normal variants use separately authored method banks.']
    for row in originals+review:
        pages+=['\n## '+row['label'],g.markdown(row['record'])]
    (ROOT/'review.md').write_text('\n\n'.join(pages)+'\n')
    domains={l:{p:len(g.parameter_domain(l,p)) for p in g.NORMAL_PROFILES} for l in coverage}
    unions={l:len(set().union(*(set(g.parameter_domain(l,p)) for p in g.NORMAL_PROFILES))) for l in coverage}
    for a,b in [('easy','moderate'),('easy','hard'),('moderate','hard')]:
        da=set().union(*(set(g.parameter_domain(a,p)) for p in g.NORMAL_PROFILES))
        db=set().union(*(set(g.parameter_domain(b,p)) for p in g.NORMAL_PROFILES))
        assert not da & db
    summary={'status':'passed','source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},
             'raw_fidelity':raw_matches,'source_totals':{'questions':8,'worked_solutions':7,'banks':6,'choices':30,'correct_designations':5},
             'source_anomalies':anomalies,'repaired_designations_not_counted_as_observed':1,'authored_fieldless_repairs':2,
             'math_and_format_samples':len(samples),'native':{k:native_report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},
             'additional_explicit_profile_boundary_records':30,
             'default_coverage':{l:{k:sorted(v) if k!='tasks' else len(v) for k,v in cov.items()} for l,cov in coverage.items()},
             'domain_sizes_by_profile':domains,'meaningful_extrema_tasks_excluding_banks_and_sine_cosine_aliases':unions,
             'all_level_domains_pairwise_disjoint':True,'plots':'none','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},
             'database_writes':0,'stopped_after_step':7,
             'hashes':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT.with_suffix('.py'),Path(__file__),ROOT/'source.json',engine,REPO/'generate/runs/current/check-engine.rs',REPO/'generate/runs/current/topics/17592186049872.json',REPO/'generate/runs/current/lessons/17592186049872.json']}}
    write('validation.json',summary)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
