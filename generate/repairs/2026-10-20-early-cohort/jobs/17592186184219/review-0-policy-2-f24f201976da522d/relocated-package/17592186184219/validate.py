"""Independent rendered-content checks, full bank replay and native grading."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('rank_nullity',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read_prompt(q):
    s=q[':question/problem'];m,n=map(int,re.search(r'\$(\d+)\s*\\times\s*(\d+)',s).groups())
    # Independent capture of the supplied integer; role determined by final query.
    k=int(re.search(r'=(\d+)',s).group(1));target='rank' if s.endswith(r'\text{rank}(A)=$') else 'nullity'
    return {'m':m,'n':n,'k':k,'target':target}
def task_key(q):
    p=read_prompt(q);return g.digest([p['target'],p['n'],p['k']])
def independent(r):
    q=r['question'];p=read_prompt(q);assert p==r['generation']['parameters']
    m,n,k,t=(p[x] for x in ('m','n','k','target'));c=n-k;rank=k if t=='nullity' else c
    assert 0<=rank<=min(m,n) and c>=0
    assert q[':question/difficulty']==':question.difficulty/easy'
    f,=q[':question/answer-fields'];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    values=[int(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(values))==len(values)==5 and min(values)>=0
    correct,=[int(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]];assert correct==c
    assert sorted(values)==[c+o for o in g.PROFILES[r['generation']['profile']]]
    s=re.sub(r'\s','',q[':question/worked-solution']);assert f'$n={n}.$' in s
    lhs=(r'\text{rank}(A)+'+str(k)) if t=='rank' else (str(k)+r'+\text{nullity}(A)')
    assert lhs+f'&={n}' in s and r'\text{'+t+r'}(A)&='+f'{n}-{k}' in s and f'&={c}.' in s
    assert 'rank-nullitytheorem' in s and not any(ord(c)<32 and c not in '\n\t\r' for c in q[':question/worked-solution'])
    assert task_key(q)==r['generation']['mathematical_fingerprint'];assert r['knowledge_point']['db_id']==g.KP_ID
    return c

def checks(r):
    independent(r);f=r['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete five-choice radio bank'} for a in f[':answer-field/choices']]
def mask(s):return re.sub(r'\s','',s)
def source_validate(q):
    mid=q[':question/math-academy-id'];p=read_prompt(q);assert p==g.ORIGINAL[mid]
    r=g.generate('easy',template=mid,parameters=p);independent(r);f=q[':question/answer-fields'][0]
    assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
    assert int(f[':answer-field/correct'][':answer/value'])==p['n']-p['k']
    assert mask(q[':question/problem'])==mask(r['question'][':question/problem']),('prompt',mid)
    assert mask(q[':question/worked-solution'])==mask(r['question'][':question/worked-solution']),('solution',mid)
    return r

def main():
    records=[];replay=[];mapping=[];review=[]
    for mid,q in g.SOURCES.items():
        r=source_validate(q);records.append(r);replay.append({'source':mid,'complete_banks_matched':1,'distractors_matched':4,'choices_matched':5,'correct_designation':True,'prompt_and_solution':'exact except whitespace'})
        p=g.ORIGINAL[mid];c=p['n']-p['k'];mapping.append({'source':mid,'parameters':p,'profile':mid,'field':'selection','choices':[{'answer_id':a[':answer/id'],'value':a[':answer/value'],'recipe':'c'+f'{int(a[":answer/value"])-c:+}','reproduced':True,'interpretation':'observed answer-relative offset; misconception unresolved'} for a in q[':question/answer-fields'][0][':answer-field/choices']]})
        review.append({'kind':'original','source':mid,'record':r})
    domain_counts={};coverage={}
    for profile in g.PROFILES:
        t=g.ORIGINAL[profile]['target'];keys=set();slots={x:set() for x in ('m','n','k')}
        for m,n,k in itertools.product(range(2,13),range(2,13),range(13)):
            p={'m':m,'n':n,'k':k,'target':t}
            if g.valid(p,profile):
                r=g.generate('easy',template=t,profile=profile,parameters=p);independent(r);keys.add(task_key(r['question']))
                for x in slots:slots[x].add(p[x])
        domain_counts[profile]=len(keys);coverage[profile]={x:sorted(v) for x,v in slots.items()}
        for seed in range(20):
            r=g.generate('easy',seed,template=t,profile=profile);independent(r);assert r==g.generate('easy',seed,template=t,profile=profile);records.append(r)
        review.append({'kind':'variant','source':profile,'record':r})
    # Same supplied n,k,m, changed requested role: both prompt and solution must update.
    pair=[]
    for t in ('rank','nullity'):
        profile=next(x for x in g.PROFILES if g.ORIGINAL[x]['target']==t)
        pair.append(g.generate('easy',template=t,profile=profile,parameters={'m':8,'n':8,'k':3,'target':t}));independent(pair[-1])
    assert pair[0]['question'][':question/problem']!=pair[1]['question'][':question/problem']
    assert pair[0]['question'][':question/worked-solution']!=pair[1]['question'][':question/worked-solution']
    bad=copy.deepcopy(pair[0]);bad['question'][':question/worked-solution']=pair[1]['question'][':question/worked-solution']
    try:independent(bad)
    except AssertionError:pass
    else:raise AssertionError('stale-target solution accepted')
    records+=pair
    for level in ('moderate','hard'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('unsupported level emitted')
    def save(path,x):path.write_text(json.dumps(x,indent=2)+'\n')
    save(HERE/'source-choice-mapping.json',mapping);save(HERE/'source-replay.json',replay);save(HERE/'side-by-side.json',review)
    (HERE/'side-by-side.md').write_text('\n\n---\n\n'.join(x['kind']+' '+x['source']+'\n\n'+g.markdown(x['record']) for x in review))
    save(HERE/'engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    grader=json.loads((HERE/'engine-report.json').read_text());assert grader['accepted_checks']==len(records) and grader['rejected_checks']==4*len(records) and grader['documented_unresolved_checks']==0
    report={'status':'pass','generator_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(Path(__file__)),'source_basis':g.SNAPSHOT['basis'],'source_questions':11,'source_banks_matched':11,'source_choices_matched':55,'source_distractors_matched':44,'correct_designations_matched':11,'profiles':11,'templates':['rank','nullity'],'plot_rating':'none','bounded_distinct_tasks_per_profile':domain_counts,'slot_coverage':coverage,'target_swap_mutation_rejected':True,'native_accepted':grader['accepted_checks'],'native_rejected':grader['rejected_checks'],'native_unresolved':0,'native_binary_sha256':sha(ROOT/'generate/runs/current/check-engine'),'unsupported_levels':['moderate','hard'],'fidelity':'all eleven full source banks and solution stages replayed; bank offsets are an explicitly narrow interpretation of sparse evidence'}
    save(HERE/'validation.json',report);print(json.dumps(report))
if __name__=='__main__':main()
