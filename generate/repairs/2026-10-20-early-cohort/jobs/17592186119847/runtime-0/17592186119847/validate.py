"""Read rendered counts and solutions independently; exercise application radio grading."""
import copy, hashlib, importlib.util, json, re, subprocess, uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('rank_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q[':question/problem'] if isinstance(q,dict) else q)
def solution_check(q):
    text=q[':question/problem'];name,rows,cols,count=re.search(r'\$([A-Z])\$.*?\$(\d+)\s*\\(?:times|cdot)\s*(\d+)\$.*?\$(\d+)\$',text).groups()
    rows,cols,count=map(int,(rows,cols,count));kind='non-pivot' if '**non-pivot**' in text else 'pivot'
    rank=cols-count if kind=='non-pivot' else count
    assert 0<=rank<=min(rows,cols),'Impossible matrix rank'
    fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0]
    enum=f[':answer-field/type'];assert (enum.get(':db/ident') if isinstance(enum,dict) else enum)==':answer-field.type/radio'
    assert f[':answer-field/key']=='selection'
    values=[int(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(values)==len(set(values))==5 and values.count(rank)==1
    correct=f[':answer-field/correct'];cid=str(correct[':answer/id']) if isinstance(correct,dict) else correct[1]
    assert str(f[':answer-field/choices'][values.index(rank)][':answer/id'])==cid
    sol=q[':question/worked-solution']
    assert re.search(r'\\text\{rank\}\('+name+r'\)='+str(rank)+r'\.',sol),'Stale rank or matrix name'
    assert 'number of pivot columns' in sol
    if kind=='non-pivot':
        assert (f'${cols}$ columns and ${count}$ of them are non-pivots' if count!=1 else f'${cols}$ columns and $1$ of them is a non-pivot') in sol
        assert f'{cols}-{count}={rank}.' in sol
    else:assert (f'${name}$ has ${count}$ pivot columns' if count!=1 else f'${name}$ has $1$ pivot column') in sol
    assert set(re.findall(r'\\text\{rank\}\(([A-Z])\)',sol))=={name}
    for t in [text,sol]+[a[':answer/value'] for a in f[':answer-field/choices']]:assert t.count('{')==t.count('}') and t.count('$')%2==0
    return {'name':name,'rows':rows,'columns':cols,'count':count,'kind':kind}
def independent(r):
    q=r['question'];meta=r['generation'];level=q[':question/difficulty'].split('/')[-1]
    assert level in g.SUPPORTED_LEVELS and r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
    assert solution_check(q)==meta['parameters']
    assert fingerprint(q)==meta['parameter_fingerprint']
    assert r==g.generate(level,meta['seed'],parameters=meta['parameters'],bank_profile=meta['bank_profile'])
    ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
    assert len(ids)==len(set(ids));[uuid.UUID(i) for i in ids]
def checks(r):
    f=r['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every source-profile choice through actual learner grader'} for a in f[':answer-field/choices']]
def main():
    replay=[];records=[];review=[]
    for level,profiles in g.PROFILES.items():
        for profile in profiles:
            source=g.SOURCES[profile];p=g.source_parameters(source);r=g.generate(level,parameters=p,bank_profile=profile);independent(r);solution_check(source)
            sf=source[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0]
            assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
            assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
            assert r['question'][':question/problem']==source[':question/problem'] and r['question'][':question/worked-solution']==source[':question/worked-solution']
            replay.append({'source':profile,'difficulty':level,'matched_options':5,'total_options':5,'matched_distractors':4,'total_distractors':4,'complete_bank':True,'exact_prompt_solution_replay':True,'missing_options':[],'extra_options':[]})
            records.append(r);review.append('## '+profile+' original and exact replay\n\n'+g.markdown(r))
    incomplete=g.SOURCES['q-34825'];p=g.source_parameters(incomplete)
    assert sorted(map(str,g.recipes('q-34825',p)))==sorted(a[':answer/value'] for a in incomplete[':question/answer-fields'][0][':answer-field/choices'])
    replay.append({'source':'q-34825','matched_options':5,'total_options':5,'excluded':True,'reason':'Unrated; correct link and worked solution absent. No source mutation or generated profile.'})
    sampled=[]
    for level in g.SUPPORTED_LEVELS:
        for seed in range(300):
            r=g.generate(level,20261015+seed);independent(r);sampled.append(r)
        for r in sampled[-3:]:review.append('## '+level+' variant\n\n'+g.markdown(r))
    records+=sampled
    coverage={level:{slot:sorted({r['generation']['parameters'][slot] for r in sampled if r['question'][':question/difficulty'].endswith('/'+level)}) for slot in ('name','rows','columns','count')} for level in g.SUPPORTED_LEVELS}
    for level in g.SUPPORTED_LEVELS:
        rs=[r for r in sampled if r['question'][':question/difficulty'].endswith('/'+level)]
        assert {r['generation']['bank_profile'] for r in rs}==set(g.PROFILES[level])
        for slot in ('rows','columns'):assert coverage[level][slot]==list(range(3,16))
    # Exhaustively establish bounded mathematical task capacity, independent of
    # random seeds, bank shuffles, names, and irrelevant row counts.
    capacities={};boundary=[]
    for level in g.SUPPORTED_LEVELS:
        domain=set()
        for m in range(3,16):
            for n in range(3,16):
                for c in range(1,13):
                    p={'name':'A','rows':m,'columns':n,'count':c,'kind':'pivot' if level=='easy' else 'non-pivot'}
                    for profile in g.PROFILES[level]:
                        if g.valid(p,level,profile):
                            domain.add((c,) if level=='easy' else (n,c))
                            if (m,n,c) in [(3,3,1),(15,15,12),(3,15,12),(15,3,1)]:
                                r=g.generate(level,parameters=p,bank_profile=profile);independent(r);boundary.append(r)
        capacities[level]={'distinct_tasks':len(domain),'tasks':[list(t) for t in sorted(domain)]}
    # Changing the supplied count must update arithmetic, prose, and key.
    stale_controls=0
    for level in g.SUPPORTED_LEVELS:
        a=g.generate(level,parameters={'name':'A','rows':10,'columns':12,'count':5,'kind':'pivot' if level=='easy' else 'non-pivot'},bank_profile=g.PROFILES[level][0])
        b=g.generate(level,parameters={**a['generation']['parameters'],'count':6 if level=='easy' else 4},bank_profile=g.PROFILES[level][0]);independent(b)
        broken=copy.deepcopy(b);broken['question'][':question/worked-solution']=a['question'][':question/worked-solution']
        try:solution_check(broken['question'])
        except AssertionError:stale_controls+=1
        else:raise AssertionError('Stale solution accepted')
        assert fingerprint(a['question'])!=fingerprint(b['question'])
        assert g.generate(level,999,parameters=a['generation']['parameters'],bank_profile=g.PROFILES[level][0])['question']==a['question']
        review.append('## Count change with dimensions held constant\n\n'+g.markdown(a)+'\n\n'+g.markdown(b))
        records += [a,b]
    try:g.generate('hard')
    except ValueError:pass
    else:raise AssertionError('Unsupported difficulty accepted')
    records+=boundary
    save('engine-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    save('source-bank-replay.json',replay);save('slot-coverage.json',{'sampled':coverage,'profile_coverage':g.PROFILES,'finite_capacity':capacities,'stale_solution_negative_controls':stale_controls,'boundary_instances':len(boundary)})
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('capabilities.json',{'supported_levels':list(g.SUPPORTED_LEVELS),'finite_capacity':{l:v['distinct_tasks'] for l,v in capacities.items()},'exceptions':[{'level':'hard','status':'unsupported','reason':'No rated hard source or distinct hard instructional backbone. Increasing counts does not justify relabeling the same rank-reading/subtraction templates hard.'},{'source':'q-34825','status':'unclassified','reason':'Source has no difficulty, correct link, or worked solution; excluded and preserved.'}],'policy':'Finite conservative positive-count domain; reclassify on new evidence; do not count new seeds, bank order, names or irrelevant dimensions as new tasks.'})
    save('validation.json',{'status':'pass','basis':json.loads((HERE/'source.json').read_text())['basis'],'source_fidelity':{'complete_supported_banks':8,'matched_options':40,'total_options':40,'matched_distractors':32,'total_distractors':32,'exact_prompt_and_solution_replays':8,'incomplete_unrated_source_preserved':True},'mathematics':{'instances':len(records),'exhaustive_parameter_capacity':{l:v['distinct_tasks'] for l,v in capacities.items()},'stale_solution_controls':stale_controls},'grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':0},'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',ROOT/'generate/runs/current/check-engine']}})
if __name__=='__main__':main()
