#!/usr/bin/env python3
"""Reproducible author checks; uses no database and writes only local evidence."""
import json,re,sys,hashlib,itertools,collections,random,shutil,subprocess,tempfile
from pathlib import Path
import sympy as sp
import generator as g
from validation_math import displayed,equal,x,u,DY,DU,UX
E=Path('evidence'); E.mkdir(exist_ok=True)
def save(name,data): (E/name).write_text(json.dumps(data,indent=2,default=str)+'\n')
def field(rec):return rec['question'][':question/answer-fields'][0]
def key(rec):return next(a for a in field(rec)[':answer-field/choices'] if a[':answer/id']==field(rec)[':answer-field/correct'][1])
def independent(rec):
    q=rec['question']; f=field(rec); spec=g.TEMPLATES[rec['generation']['template']];p=rec['generation']['parameters']
    function=displayed(re.search(r'y\s*=\s*([^$]+)',q[':question/problem'])[1])
    # Parse the rendered input, not generation.exact or the generator's model.
    derivative=sp.diff(function,x);expected=derivative.subs(x,p['t']) if spec.get('slope') else derivative
    assert equal(displayed(key(rec)[':answer/value']),expected),(rec['generation'],expected)
    choices=[displayed(a[':answer/value']) for a in f[':answer-field/choices']]
    assert sum(equal(a,expected) for a in choices)==1
    assert all(not equal(a,b) for a,b in itertools.combinations(choices,2))
    inner=p['a']*x**spec['degree']+p['b']*(x if spec['degree']==2 else 1)+p.get('c',0)
    exponent=sp.Rational(1,2) if spec['family']=='sqrt' else -sp.Rational(1,2)
    outerd=sp.diff(u**exponent,u);innerd=sp.diff(inner,x)
    d_rad=sp.diff(inner**exponent,x)
    if spec.get('slope'):assert inner.subs(x,p['t'])>0
    math=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
    def expr(v):return displayed(v.replace('d}f','d}y'))
    assert equal(expr(math[0].split('=',1)[1]),DU*UX)
    for v in math[1].split('=')[1:]:assert equal(expr(v),outerd)
    assert equal(expr(math[2].split('=',1)[1]),innerd)
    for row in math[3].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
        v=expr(row.split('& =')[1]).subs({DU:outerd,UX:innerd}).subs(u,inner)
        assert equal(v,d_rad),(row,v,d_rad)
    if spec.get('sum'):assert equal(expr(math[4].split('=',1)[1]),derivative)
    if spec.get('slope'):
        assert ('x='+str(p['t'])) in q[':question/problem']
        rows=math[-1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
        for row in rows:
            rhs=row.split('& =')[1].strip().rstrip('.')
            if '|' in rhs:
                marker=rhs.index('|'); v=expr(rhs[1:marker].rstrip('}')).subs(x,p['t'])
            else:v=expr(rhs)
            assert equal(v,expected),(row,v,expected)
    return expected

def grading(rec,expected,label):
    f=field(rec)
    if f[':answer-field/type'].endswith('/radio'):
        return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(rec)[':answer/id'] else 'rejected','purpose':'complete bank, independently differentiated'} for a in f[':answer-field/choices']]}
    # Different notation; derivative power form exercises native symbolic comparison.
    equivalent=r'\frac{2}{2}\left('+key(rec)[':answer/value']+r'\right)' if expected.has(x) else str(expected)
    wrong=g.tex(expected+1)
    return {'label':label,'record':rec,'checks':[{'submitted':key(rec)[':answer/value'],'expected':'accepted','purpose':'computed canonical response'},{'submitted':equivalent,'expected':'accepted','purpose':'independent equivalent notation'},{'submitted':wrong,'expected':'rejected','purpose':'additive error'}]}

def coverage(records):
    groups=collections.defaultdict(list)
    for r in records:groups[r['generation']['template']+'|'+r['generation']['bank_profile']].append(r)
    report={}
    for group,rs in sorted(groups.items()):
        signs=collections.Counter(); positions=collections.Counter();ranks=collections.Counter();features=collections.defaultdict(collections.Counter)
        for r in rs:
            choices=field(r)[':answer-field/choices']; correct=key(r);p=r['generation']['parameters']; spec=g.TEMPLATES[r['generation']['template']]
            # Determine exact rank at a common positive-domain witness for symbolic answers.
            vals=[displayed(a[':answer/value']) for a in choices]
            if any(v.has(x) for v in vals):
                witness=next(t for t in list(range(-25,26))+[sp.Rational(k,16) for k in range(-15,16) if k] if all(v.subs(x,t).is_real and v.subs(x,t).is_finite for v in vals))
                vals=[v.subs(x,witness) for v in vals]
            ci=choices.index(correct); positions[ci]+=1
            order=sorted(range(len(vals)),key=lambda i:float(vals[i]));ranks[order.index(ci)]+=1
            for name,fun in {
                'shortest_tex':lambda a:len(a[':answer/value']),
                'longest_tex':lambda a:-len(a[':answer/value']),
                'no_leading_minus':lambda a:a[':answer/value'].startswith('-'),
                'leading_minus':lambda a:not a[':answer/value'].startswith('-'),
                'no_cube_in_radical':lambda a:'^{3}' in a[':answer/value'],
            }.items():
                scores=[fun(a) for a in choices];best=min(scores);ties=[i for i,v in enumerate(scores) if v==best]
                features[name]['attempts']+=1;features[name]['success_mass']+=(1/len(ties) if ci in ties else 0)
            sign=sp.sign(vals[ci]);signs[str(sign)]+=1
        radio=len(field(rs[0])[':answer-field/choices'])==5
        report[group]={'n':len(rs),'semantic_instances':len({r['generation']['parameter_fingerprint'] for r in rs}),'a_signs':dict(collections.Counter(str(sp.sign(r['generation']['parameters']['a'])) for r in rs)),'answer_signs_at_witness':dict(signs),'correct_positions':dict(positions),'correct_numeric_ranks':dict(ranks),'baseline':.2 if radio else None,'probes':{k:dict(v) for k,v in features.items()} if radio else {},'max_attempts':max(r['generation']['attempts'] for r in rs)}
    return report

def main():
    replays=g.replay_sources();cases=json.load(open('data/source-cases.json'));replay_report=[];graders=[]
    for c,r in zip(cases,replays):
        expected=independent(r);source=r['generation']['source_capture'];sf=source[':question/answer-fields'][0]
        # Input presentation matches except normal TeX normalization; source-history blanks aren't alternatives.
        assert g.normalize_prose(source[':question/problem'])==r['question'][':question/problem'],c['source_id']
        matches=[]
        if g.TEMPLATES[c['template']]['field']=='radio':
            actual=[displayed(a[':answer/value']) for a in field(r)[':answer-field/choices']]
            for a in sf[':answer-field/choices']:
                v=displayed(a[':answer/value']);match=[i for i,w in enumerate(actual) if equal(v,w)]
                assert len(match)==1,(c['source_id'],a[':answer/value'],actual)
                matches.append({'source_value':a[':answer/value'],'generated_value':field(r)[':answer-field/choices'][match[0]][':answer/value'],'recipe':r['generation']['recipes'][field(r)[':answer-field/choices'][match[0]][':answer/value']]})
        else:
            for a in sf[':answer-field/choices']:
                try:valid=equal(displayed(a[':answer/value']),expected)
                except Exception:valid=False
                matches.append({'source_value':a[':answer/value'],'role':'equivalent correct derivative/slope' if valid else 'historical partial or wrong learner submission; retained capture only'})
        sc=sf.get(':answer-field/correct')
        if sc: assert equal(displayed(sc[':answer/value']),expected),c['source_id']
        replay_report.append({'id':c['source_id'],'uuid':c['source_uuid'],'difficulty':source.get(':question/difficulty'),'correct':str(expected),'complete_choices':matches,'solution_stages_checked':True,'source_solution_present':':question/worked-solution' in source,'repairs':c['repairs']})
        graders.append(grading(r,expected,'source '+c['source_id']))
    save('source-replay.json',replay_report);save('source-records.json',replays)
    # Exercise each entire bank profile within every eligible layout, plus signed/domain boundaries.
    if '--resume' in sys.argv and (E/'probe-records.json').exists() and all(r['generation']['bank_profile'] in ['scale_bank','blank'] for r in json.load(open(E/'probe-records.json'))):
        records=json.load(open(E/'probe-records.json'))
        for r in records:
            if r['generation']['seed'] in [1000,1001]:
                graders.append(grading(r,independent(r),'regression '+r['generation']['template']))
    else:
        records=[]
        for name,spec in g.TEMPLATES.items():
            profiles=g.DEFAULT_PROFILES.get(name,['blank'])
            for profile in profiles:
                for seed in range(12):
                    r=g.generate(spec['level'],seed=1000+seed,template=name,profile=profile)
                    expected=independent(r);records.append(r)
                    if seed<2:graders.append(grading(r,expected,name+' '+profile+' '+str(seed)))
    save('probe-records.json',records)
    # Relevant target changes, fixed polynomial; positive/zero/negative branches and root 1 boundaries.
    cf=[]
    sets=[('slope_sqrt_quadratic_blank','easy',dict(a=-1,b=10,c=0),[2,5,8]),('slope_sqrt_linear_blank','easy',dict(a=2,b=1),[0,4]),('slope_reciprocal_blank','easy',dict(a=3,b=12,c=0),[-6,2])]
    for template,level,base,targets in sets:
        rs=[g.generate(level,seed=9,template=template,parameters={**base,'t':t},profile='blank') for t in targets]
        values=[independent(r) for r in rs]
        assert len(set(values))==len(values)
        for r,v in zip(rs,values):graders.append(grading(r,v,'counterfactual '+template))
        # Cross responses must fail, proving the actual grading changes with the point.
        for i,r in enumerate(rs):
            graders.append({'label':'changed-target rejects old response','record':r,'checks':[{'submitted':g.tex(values[(i+1)%len(rs)]),'expected':'rejected','purpose':'counterfactual stale response'}]})
        cf.extend(rs)
    # Change relevant coefficient with constant held fixed; both linear layouts and signs.
    for template,spec in g.TEMPLATES.items():
        if spec['degree']!=1 or spec.get('slope'):continue
        for a in [-8,-2,2,8]:
            r=g.generate(spec['level'],template=template,parameters=dict(a=a,b=5),profile='blank' if spec['field']=='blank' else 'scale_bank')
            graders.append(grading(r,independent(r),'coefficient counterfactual '+template));cf.append(r)
    # Constant change leaves u' invariant, but changes the derivative denominator.
    pairs=[g.generate('moderate',template='reciprocal_blank',parameters=dict(a=5,b=b),profile='blank') for b in [-1,1]]
    assert not equal(independent(pairs[0]),independent(pairs[1]));cf.extend(pairs)
    # Formatting-only irrelevant change preserves grading and expression.
    irrelevant=json.loads(json.dumps(pairs[0]));irrelevant['question'][':question/problem']=irrelevant['question'][':question/problem'].replace('Find ','Find  ')
    graders.append(grading(irrelevant,independent(irrelevant),'irrelevant spacing'))
    save('counterfactual-records.json',cf)
    # Invalid parameter boundaries must reject rather than serve undefined answers.
    invalid=[('slope_sqrt_linear_blank','easy',dict(a=2,b=0,t=0)),('slope_sqrt_quadratic_blank','easy',dict(a=-1,b=2,c=0,t=3)),('sqrt_linear_blank','hard',dict(a=0,b=2))]
    for t,l,p in invalid:
        try:g.generate(l,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError('invalid accepted')
    before=coverage(records);save('pedagogical-variation-before.json',before)
    save('grader-input.json',graders)
    # Five runner-style samples, deterministic command contract.
    cli=[sys.executable,'generator.py','--difficulty','moderate','--count','5','--seed','42','--format','json']
    first=subprocess.check_output(cli);assert first==subprocess.check_output(cli)
    save('sample.json',json.loads(first))
    # Copy only declared runtime files to a different folder, run without repository imports.
    manifest=json.load(open('package.json'))
    with tempfile.TemporaryDirectory(dir='/tmp') as tmp:
        dest=Path(tmp)
        for filename in manifest['files']:
            (dest/filename).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(filename,dest/filename)
        relocated=json.loads(subprocess.check_output([sys.executable,str(dest/'generator.py'),'--count','5','--seed','42','--format','json'],cwd=dest))
        assert relocated==json.loads(first)
    result={'source_cases':len(replays),'source_radio_banks':sum(g.TEMPLATES[c['template']]['field']=='radio' for c in cases),'source_radio_choices':sum(len(r['complete_choices']) for r,c in zip(replay_report,cases) if g.TEMPLATES[c['template']]['field']=='radio'),'generated_probe_records':len(records),'independent_mathematics':'passed including all displayed solution blocks','counterfactual_records':len(cf),'grader_cases':len(graders),'invalid_boundaries_rejected':len(invalid),'determinism':'passed','relocation':'passed','semantic_instances':len({r['generation']['parameter_fingerprint'] for r in records}),'normal_max_attempts':max(r['generation']['attempts'] for r in records)}
    save('validation.json',result);print(json.dumps(result))
if __name__=='__main__':main()
