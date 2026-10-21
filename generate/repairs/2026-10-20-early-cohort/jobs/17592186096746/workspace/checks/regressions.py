"""Executable source-fidelity and decision-shortcut regressions against current runtime."""
import collections, copy, json, re, sys
from pathlib import Path
W=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(W))
import generator as g
from visible_math import analyze,equations,matrix,vector_parts,scalar,rref
from shortcut import measure
E=W/'evidence'; E.mkdir(exist_ok=True)
def save(name,value): (E/name).write_text(json.dumps(value,indent=2,ensure_ascii=False))
def keyvalue(r):
    f=r['question'][':question/answer-fields'][0]
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def norm(s,easy):
    s=s.replace('\\\\begin','\\begin').replace('\\\\end','\\end').replace('\\\\\\\\','\\\\')
    return s if s=='No solution' else str(matrix(s) if easy else vector_parts(s))
def operations(r):
    current=pending=None;steps=0
    for b in re.findall(r'\$\$(.*?)\$\$',r['question'][':question/worked-solution'],re.S):
        if '\\begin{array}' in b:
            nxt=matrix(b)
            if current is not None:
                assert pending, 'missing displayed row operation'
                a=copy.deepcopy(current);op=pending.replace(' ','')
                sw=re.fullmatch(r'R_(\d)\\leftrightarrowR_(\d)',op)
                add=re.fullmatch(r'R_(\d):=R_\1\+\((.*?)\)R_(\d)',op)
                scale=re.fullmatch(r'R_(\d):=\((.*?)\)R_\1',op)
                if sw:
                    i,j=(int(v)-1 for v in sw.groups());a[i],a[j]=a[j],a[i]
                elif add:
                    i,f,j=add.groups();i=int(i)-1;j=int(j)-1;a[i]=[x+scalar(f)*y for x,y in zip(a[i],a[j])]
                elif scale:
                    i,f=scale.groups();i=int(i)-1;a[i]=[scalar(f)*x for x in a[i]]
                else: raise AssertionError('unparsed operation '+op)
                assert a==nxt, 'operation does not produce displayed matrix'
                steps+=1
            current=nxt;pending=None
        elif b.strip().startswith('R_'): pending=b.strip()
    assert current==rref(equations(r['question'][':question/problem']))
    return steps

def main():
    source=json.loads((W.parent/'source/source.json').read_text())['material']['kp']
    replay=g.replay();mapped={r['generation']['parameters']['source_id']:r for r in replay}
    source_results=[]
    for q in source[':knowledge-point/questions']:
        sid=q[':question/id'];assert sid in mapped, 'missing supplied source '+sid
        r=mapped[sid];easy=q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy'
        sf=q[':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0]
        sb=[norm(a[':answer/value'],easy) for a in sf[':answer-field/choices']];gb=[norm(a[':answer/value'],easy) for a in gf[':answer-field/choices']]
        assert sb==gb, 'complete bank mismatch '+sid
        assert equations(q[':question/problem'])==equations(r['question'][':question/problem'])
        sk=sf.get(':answer-field/correct')
        if sk:
            ai=next(i for i,a in enumerate(sf[':answer-field/choices']) if a[':answer/id']==sk[':answer/id'])
            assert gf[':answer-field/choices'][ai][':answer/id']==gf[':answer-field/correct'][1]
        expected=q.get(':question/difficulty',{}).get(':db/ident')
        assert r['question'].get(':question/difficulty')==expected
        source_results.append({'id':sid,'bank_choices_matched':len(sb),'key_inferred':sk is None})
    missing=mapped['693512da-f45c-5aae-999f-b43069296756']
    assert 'R_3:=R_3+(-16)R_1' in missing['question'][':question/worked-solution']
    assert operations(missing)==3
    cp=dict(profile='q-74536',source_id=source[':knowledge-point/canonical-example'][':question/id'],difficulty='easy',b=-3,c=1,d=4,scales=[2,-6,4],plan='normalize')
    canonical=g.build(cp,source_replay=True)
    assert equations(source[':knowledge-point/canonical-example'][':question/problem'])==equations(canonical['question'][':question/problem'])
    save('source-replay.json',replay);save('source-replay-results.json',{'passed':True,'banks':source_results,'matched':len(source_results),'total':len(source[':knowledge-point/questions']),'choices':sum(x['bank_choices_matched'] for x in source_results),'canonical_prompt_math':True,'missing_source_operation_correction':True})
    minimal=g.generate('easy',1,913771);batch=g.generate('easy',5,4221100018)
    easy=g.generate('easy',24,913771);moderate=g.generate('moderate',8,557291)
    save('minimal.json',minimal);save('batch.json',batch);save('fresh-easy.json',easy);save('fresh-moderate.json',moderate)
    probes={k:measure(rs) for k,rs in [('minimal',minimal),('batch',batch),('fresh',easy)]}
    assert all(x['successes']==x['same_absolute_bank']==0 for x in probes.values()), 'sign-only shortcut persists'
    for r in easy+moderate:
        f=r['question'][':question/answer-fields'][0]
        vs=[matrix(a[':answer/value'])[0][1:] if r in easy else vector_parts(a[':answer/value'])[0] for a in f[':answer-field/choices']]
        sig=lambda v:tuple((x>0)-(x<0) for x in v)
        assert len({sig(v) for v in vs})==1, 'sign cue separates a candidate'
        assert len({str(v) for v in vs})==5
    # Exact original offending parameters, replacing the old signs-only rule.
    p=dict(profile='normalize-all',difficulty='easy',scales=[-8,7,4],plan='normalize')
    triples=[[-10,-3,-14],[-7,-4,-12],[-8,-5,-10],[-9,-6,-16],[-6,-7,-18]]
    original=g.numerical_bank(p,triples,0);assert not measure([original])['successes']
    save('exact-parameter-repair.json',[original])
    # Fixed banks: every numerical candidate must be eligible to become correct.
    counter=[];relations=[]
    for band in ('easy','moderate'):
        for target in ('b','c','d','all'):
            bank=[[2,3,4],[4,5,6],[6,7,8],[8,9,10],[10,1,12]]
            if target!='all':
                j=('b','c','d').index(target)
                bank=[[v if k==j else (2,3,4)[k] for k,v in enumerate(t)] for t in bank]
            bank=[[v*(-1 if k!=1 else 1) for k,v in enumerate(t)] for t in bank]
            p=dict(profile='normalize-'+target,difficulty=band,scales=[-8,7,4],plan='normalize')
            rs=[g.numerical_bank(p,bank,i) for i in range(5)]
            first=rs[0];values=lambda r:[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
            assert all(values(r)==values(first) for r in rs)
            assert len({keyvalue(r) for r in rs})==5
            assert len({r['question'][':question/problem'] for r in rs})==5
            assert len({r['question'][':question/worked-solution'] for r in rs})==5
            scaled=copy.deepcopy(p);scaled['scales']=[s*2 for s in p['scales']]
            irrelevant=g.numerical_bank(scaled,bank,0);assert keyvalue(irrelevant)==keyvalue(first)
            assert irrelevant['question'][':question/problem']!=first['question'][':question/problem']
            counter+=rs+[irrelevant]
            relations.append({'band':band,'profile':p['profile'],'fixed_bank_eligible_members':5,'changed_prompts_solutions_keys':True,'scale_only_preserves_response':True,'record_start':len(counter)-6})
    save('counterfactual-records.json',counter)
    records=replay+[canonical]+batch+easy+moderate+counter+[original]
    math=[]
    for r in records:
        result=analyze(r);assert not result['errors'],result
        result['displayed_operations_checked']=operations(r);math.append(result)
    save('math-results.json',{'passed':True,'count':len(math),'records':math})
    save('shortcut-results.json',probes)
    save('counterfactual-results.json',relations)
    coverage={band:dict(collections.Counter(r['generation']['profile'] for r in rs)) for band,rs in [('easy',easy),('moderate',moderate)]}
    assert len(coverage['easy'])==4
    groups={}
    for r in easy:
        name=r['generation']['profile']+'/'+str((equations(r['question'][':question/problem'])[0][0]>0)*2-1)
        groups.setdefault(name,[]).append(r)
    save('conditional-shortcuts.json',{k:measure(v) for k,v in groups.items()})
    save('pedagogical-variation.json',{'coverage':coverage,'controlled_banks':relations,'claims':{'fidelity':'16 complete source banks, 80 choices; missing key inferred only for unclassified capture','correctness':'independent visible exact RREF/substitution and annotation execution','grading':'grader-cases.json requires separate native run','decision_variation':'all five candidates eligible within each of four fixed numerical bank profiles, both bands; signs/rank identical'},'limits':['Exact replay banks preserve original source shortcuts; ordinary sampling uses explicitly authored numerical extensions.','Finite samples cannot exclude every conceivable strategy.','Learner history, policy weights and live inventory unavailable.']})
    cases=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
        cases.append({'label':str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'visible exact arithmetic verifies unique correct choice'} for a in f[':answer-field/choices']]})
    save('grader-cases.json',cases)
    # Render the repaired batch, restored source, and controlled changed member.
    save('render-records.json',[batch[0],batch[2],missing,counter[0],counter[4]])
    print(json.dumps({'passed':True,'source_banks':len(source_results),'choices':80,'math_records':len(math),'counterfactuals':len(counter),'coverage':coverage,'sign_shortcut_success':{k:v['successes'] for k,v in probes.items()}}))
if __name__=='__main__': main()
