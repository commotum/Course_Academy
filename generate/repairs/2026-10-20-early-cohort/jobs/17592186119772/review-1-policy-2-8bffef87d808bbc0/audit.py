#!/usr/bin/env python3
"""Independent, read-only repair review. All output stays beside this script."""
import copy, hashlib, importlib.util, itertools, json, platform, re, shutil, subprocess, sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode = True
E=Path(__file__).resolve().parent
J=E.parent
W=J/'workspace'
OLD=J/'review-0-policy-2-51f6015bc2a9aef6'
R=Path('/home/jake/Developer/Course_Academy')
PY=R/'.venv/bin/python'
sys.path.insert(0,str(W))
def save(name,value):
    p=E/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,default=str)+'\n')
def load(name):return json.loads((E/name).read_text())
def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(W.rglob('*')) if p.is_file()}
def enum(x):return x.get(':db/ident') if isinstance(x,dict) else x
def aid(x):return x[':answer/id'] if isinstance(x,dict) else x[1] if isinstance(x,list) else x
def correct(f):return next(a for a in f[':answer-field/choices'] if a[':answer/id']==aid(f[':answer-field/correct']))
RX=re.compile(r'([A-E])\s*=\s*(?:\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}|\[\\begin\{aligned\}(.*?)\\end\{aligned\}\])',re.S)
def parse(text):
    out={}
    for m in RX.finditer(text):
        a=[[Fraction(v.strip()) for v in row.split('&')] for row in (m[2] if m[2] is not None else m[3]).split(r'\\')]
        assert a and all(len(row)==len(a) for row in a)
        assert m[1] not in out or out[m[1]]==a
        out[m[1]]=a
    return out
def target(q):return 'upper' if 'upper triangular' in q[':question/problem'] else 'lower'
def visible(q):
    text=q[':question/problem']
    for f in q.get(':question/answer-fields',[]):
        text+='\n'+f.get(':answer-field/key','')+'\n'+'\n'.join(a[':answer/value'] for a in f[':answer-field/choices'])
    return parse(text)
def good_labels(mats,t):
    return tuple(l for l,a in sorted(mats.items()) if all(v==0 for i,row in enumerate(a) for j,v in enumerate(row) if (i>j if t=='upper' else i<j)))
def inspect(record):
    q=record['question'];mats=visible(q);t=target(q);good=good_labels(mats,t)
    fields=q[':question/answer-fields'];kind=enum(fields[0][':answer-field/type'])
    if kind.endswith('/checkbox'):
        actual=tuple(sorted(next(iter(parse(f[':answer-field/key']))) for f in fields if correct(f)[':answer/value']=='true'))
    else:
        c=correct(fields[0])[':answer/value']
        actual=tuple(sorted(parse(c))) if parse(c) else tuple(sorted(re.findall(r'\$([A-E])\$',c)))
        choices=[]
        for a in fields[0][':answer-field/choices']:
            v=a[':answer/value'];labels=tuple(sorted(parse(v))) if parse(v) else tuple(sorted(re.findall(r'\$([A-E])\$',v)))
            if labels==good:choices.append(a[':answer/id'])
        assert choices==[aid(fields[0][':answer-field/correct'])],('ambiguous/wrong radio',q[':question/id'])
    assert actual==good,(actual,good)
    solution=q[':question/worked-solution'];named=tuple(sorted(re.findall(r'\$([A-E])\$',solution.split('\n\n')[0])))
    assert named==good,('solution attribution',named,good)
    for l,a in parse(solution).items():assert mats[l]==a
    for l,i,j,v in re.findall(r'\{([a-e])\}_\{([1-4])([1-4])\}\s*&\s*=(-?\d+(?:\.\d+)?)\\ne 0',solution):
        i,j=int(i)-1,int(j)-1
        assert (i>j if t=='upper' else i<j)
        assert mats[l.upper()][i][j]==Fraction(v)!=0
    return {'id':q[':question/id'],'profile':record.get('generation',{}).get('profile'),'target':t,'good':good,
            'dimensions':tuple(len(a) for _,a in sorted(mats.items())),
            'correct_position':None if len(fields)>1 else next(i for i,a in enumerate(fields[0][':answer-field/choices']) if a[':answer/id']==aid(fields[0][':answer-field/correct'])),
            'semantic':str((t,sorted((len(a),tuple((i,j) for i,row in enumerate(a) for j,v in enumerate(row) if i!=j and v)) for a in mats.values())))}
def run(cmd,name):
    result=subprocess.run(list(map(str,cmd)),cwd=E,capture_output=True,text=True)
    save(name,{'command':list(map(str,cmd)),'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    assert result.returncode==0,(name,result.stderr[-1500:],result.stdout[-1500:])
    return result
def field_signature(f):
    return (f.get(':answer-field/key'),enum(f[':answer-field/type']),sorted((enum(a[':answer/type']),a[':answer/value']) for a in f[':answer-field/choices']),correct(f)[':answer/value'])

def main():
    save('package-before.json',hashes())
    g=module(W/'17592186119772.py','current_target')
    source=json.loads((J/'source/source.json').read_text())
    qs=source['material']['kp'][':knowledge-point/questions']
    batch=json.loads((J/'samples.json').read_text());save('batch-records.json',batch)
    replay=[];replays=[];records=[];index=[]
    for n,q in enumerate(qs):
        sid=q[':question/math-academy-id'];level=enum(q[':question/difficulty']).split('/')[-1]
        raw=g.generate(level,seed=69127,profile='raw:'+sid);rq=raw['question'];inspect(raw)
        assert all(rq[k]==q[k] for k in [':question/problem',':question/worked-solution'])
        assert enum(rq[':question/difficulty'])==enum(q[':question/difficulty'])
        assert sorted(map(field_signature,rq[':question/answer-fields']))==sorted(map(field_signature,q[':question/answer-fields']))
        replays.append(raw);replay.append({'source_id':q[':question/id'],'profile':sid,'level':level,'passed':True,'choices_compared':sum(len(f[':answer-field/choices']) for f in rq[':question/answer-fields'])})
        for k in range(10 if level=='easy' else 4):
            seed=86203711+n*101+k
            r=g.generate(level,seed=seed,profile=sid);inspect(r);records.append(r)
            index.append({'profile':sid,'difficulty':level,'seed':seed,'record_index':len(records)-1})
    save('source-replay-records.json',replays);save('source-replay.json',{'cases':replay,'passed':len(replay),'total':len(qs),'exact_choices_compared':sum(x['choices_compared'] for x in replay),'canonical_gap':'Canonical e-4395 has no captured answer bank. Its visible matrices classify B only by the same independent zero-side predicate.'})
    canonical=source['material']['kp'][':knowledge-point/canonical-example']
    assert good_labels(parse(canonical[':question/problem']),target(canonical))==('B',)
    easy=[r for r in records if r['question'][':question/difficulty'].endswith('/easy')]
    save('independent-records.json',records);save('sample-index.json',index);save('easy-records.json',easy)

    # Reuse the exact prior failing parameter assignment, independently check it.
    minimal=json.loads((OLD/'minimal-failing-case.json').read_text());save('retained-minimal-case.json',minimal)
    p=minimal['parameters'];swap=g.generate_easy(seed=minimal['seed'],profile=minimal['source_profile'],parameters=p)
    assert inspect(swap)['good']==('A',) and 'Notice that $A$' in swap['question'][':question/worked-solution']
    oldg=module(OLD/'relocated-package/17592186119772.py','old_target')
    histories=[]
    for label,mod in [('old',oldg),('current',g)]:
        for case,level,profile,params in [('role_swap','easy',minimal['source_profile'],p),('missing_easy_68743','easy','raw:q-68743',None),('missing_easy_68748','easy','raw:q-68748',None),('missing_decimal','moderate','raw:q-42111',None),('missing_mixed','moderate','raw:q-126346',None),('missing_subset_radio','moderate','raw:q-42141',None)]:
            try:
                rr=mod.generate(level,seed=minimal['seed'],profile=profile,parameters=params)
                histories.append({'version':label,'case':case,'accepted':True,'good':inspect(rr)['good']})
            except Exception as ex:histories.append({'version':label,'case':case,'accepted':False,'error':str(ex)})
    oldbatch=json.loads((OLD/'delivery-batch/accepted.json').read_text())
    for label,rs in [('old',oldbatch),('current',batch)]:
        histories.append({'version':label,'case':'batch_has_multiple_qualifying_labels','passed':len({inspect(r)['good'] for r in rs})>1,'labels':[inspect(r)['good'] for r in rs]})
    assert all(not x['accepted'] for x in histories if x['version']=='old' and 'accepted' in x)
    assert all(x['accepted'] for x in histories if x['version']=='current' and 'accepted' in x)
    save('retained-finding-regressions.json',{'findings':[x['id'] for x in json.loads((J/'repair-history.json').read_text())['findings']],'preflight_claim':json.loads((J/'repair-preflight.json').read_text()),'method':'Independently rerun exact retained failing input, every omitted source profile and exact old/current batch assertions. Old executable is retained manifest-only relocation from previous review. No author checks executed because their output directory is inside the protected package.','cases':histories,'command':str(PY)+' -B audit.py'})

    # All answer-bearing roles at fixed source-profile dimensions.
    controlled=[];roles=[]
    for q in qs:
        sid=q[':question/math-academy-id'];level=enum(q[':question/difficulty']).split('/')[-1];mats=visible(q)
        subsets=[(x,) for x in sorted(mats)] if level=='easy' else [c for n in (1,2) for c in itertools.combinations(sorted(mats),n)]
        for good in subsets:
            changed={}
            for l,a in mats.items():
                n=len(a);b=[[0]*n for _ in range(n)]
                for i in range(n):b[i][i]=ord(l)-63
                b[0][-1]=3
                if l not in good:b[-1][0]=5
                changed[l]=b
            rr=g.generate(level,seed=78411,profile=sid,parameters={'criterion':'upper','matrices':changed})
            assert inspect(rr)['good']==good
            controlled.append(rr);roles.append({'profile':sid,'good':good,'record_index':len(controlled)-1})
    save('controlled-role-records.json',controlled);save('controlled-role-results.json',roles)

    # Hold complete matrix evidence fixed and change target; both answers unique.
    p={'criterion':'upper','matrices':{'A':[[1,3],[0,2]],'B':[[1,0],[4,2]],'C':[[1,5],[6,2]],'D':[[2,7],[8,1]],'E':[[3,9],[10,1]]}}
    before=g.generate_easy(seed=93071,profile='q-126354',parameters=p)
    p2=copy.deepcopy(p);p2['criterion']='lower'
    after=g.generate_easy(seed=93071,profile='q-126354',parameters=p2)
    p3=copy.deepcopy(p)
    for a in p3['matrices'].values():a[0][0]=-11;a[1][1]=0;a[0][1]=-7
    irrelevant=g.generate_easy(seed=93071,profile='q-126354',parameters=p3)
    assert [inspect(r)['good'] for r in [before,after,irrelevant]]==[('A',),('B',),('A',)]
    cf=[before,after,irrelevant,swap];save('counterfactual-records.json',cf)
    save('counterfactual-results.json',{'same_matrices_different_target':{'before':inspect(before),'after':inspect(after),'same_matrices':visible(before['question'])==visible(after['question']),'expected':'A becomes B when upper changes to lower. Prompt, explanation and native grader must follow.'},'irrelevant_diagonal_allowed_side':{'before':inspect(before),'after':inspect(irrelevant),'expected':'Upper answer A preserved after diagonal and allowed-side edits.'},'retained_role_swap':inspect(swap),'native_and_render_evidence':'To be completed by run_pipeline.py and visual inspection.'})

    allrecords=records+batch+replays+controlled+cf
    cases=[inspect(r) for r in allrecords]
    save('math-results.json',{'method':'Independent Fraction parser of prompt/field/answer TeX; all forbidden-side entries; unique radio response or full checkbox truth set; independent solution label and nonzero witness checks; repeated solution matrices must match displayed input. No generator metadata or classifier used to decide correctness.','records_checked':len(cases),'failures':[],'cases':cases})
    save('scope-results.json',{'requested':'easy','sample_count':len(easy)+len(batch),'source_refs':[q[':question/id'] for q in qs if enum(q[':question/difficulty']).endswith('/easy')],'sizes':sorted({n for r in easy+batch for n in inspect(r)['dimensions']}),'field_contract':'Each sampled easy record has five matrix radio choices and exactly one qualifies; entries integers in [-11,11]; no arithmetic, matrix operator or extra response requirement.','check':all(len(r['question'][':question/answer-fields'])==1 and len(r['question'][':question/answer-fields'][0][':answer-field/choices'])==5 and len(inspect(r)['good'])==1 for r in easy+batch),'limits':'Hard authored extension retained unchanged and outside requested easy delivery; no new hard certification.'})

    reject=[]
    invalid=[]
    z=copy.deepcopy(p);z['matrices']['A'][0].append(0);invalid.append(('nonsquare',z))
    z=copy.deepcopy(p);z['matrices']['A'][0][0]=12;invalid.append(('outside_numeric_bounds',z))
    z=copy.deepcopy(p);z['matrices']['A'][1][0]=1;invalid.append(('no_correct',z))
    z=copy.deepcopy(p);z['matrices']['B'][1][0]=0;invalid.append(('two_correct',z))
    z=copy.deepcopy(p);z['matrices']['B']=copy.deepcopy(z['matrices']['A']);invalid.append(('duplicate_matrices',z))
    for name,z in invalid:
        try:g.generate_easy(seed=93071,profile='q-126354',parameters=z);reject.append({'case':name,'rejected':False})
        except ValueError as ex:reject.append({'case':name,'rejected':True,'error':str(ex),'parameters':z})
    assert all(x['rejected'] for x in reject)
    bound=copy.deepcopy(p);bound['matrices']['A'][0][0]=-11;bound['matrices']['B'][0][0]=11
    boundary=g.generate_easy(seed=93071,profile='q-126354',parameters=bound);inspect(boundary);save('boundary-records.json',[boundary])
    deterministic=all(g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed'],profile=r['generation']['profile'])==r for r in records)
    assert deterministic
    save('runtime-results.json',{'actual_python':platform.python_version(),'actual_sympy':g.sp.__version__,'deterministic_cases':len(records),'deterministic_replay':deterministic,'rejections':reject,'boundary':'Exact numeric endpoints accepted; profile dimensions and exactly-one constraints retained.','sampling_inspection':'candidate_support chooses orientation, qualifying label(s) before support and values; no label-bound source support counts. All forbidden coordinates sampled uniformly; nonzero support count bounded by source profile maxima and matrix capacity. fill_values preserves off-diagonal zeros. Whole instances retry up to 100 only if validation fails. Nonempty checkbox policy cannot remove any easy radio case. Easy exactly-one allocation means no empty-answer resampling.','limits':'Fresh bounded seeds and explicit boundaries, not exhaustive numerical seed enumeration.'})
    # Grader expectations are derived from visible matrices above, never just stored keys.
    grader=[]
    for i,r in enumerate(replays+controlled+cf+batch):
        stats=inspect(r);checks=[]
        for fi,f in enumerate(r['question'][':question/answer-fields']):
            for a in f[':answer-field/choices']:
                if enum(f[':answer-field/type']).endswith('/checkbox'):
                    l=next(iter(parse(f[':answer-field/key'])));ok=(a[':answer/value']=='true')==(l in stats['good'])
                else:
                    v=a[':answer/value'];labs=tuple(sorted(parse(v))) if parse(v) else tuple(sorted(re.findall(r'\$([A-E])\$',v)));ok=labs==stats['good']
                checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if ok else 'rejected','purpose':'Visible zero-side predicate, all valid and plausible wrong bank selections'})
            if not enum(f[':answer-field/type']).endswith('/checkbox'):
                checks.append({'field_index':fi,'submitted':'A','expected':'rejected','purpose':'Literal text does not substitute for a radio answer identity'})
        grader.append({'label':f'independent-{i}-{r["generation"]["profile"]}','record':r,'checks':checks})
    save('grader-input.json',grader)
    render=cf+batch+[next(r for r in records if r['generation']['profile']==sid) for sid in ['q-42111','q-42141','q-68743','q-68748']]
    save('render-input.json',render)
    # Manifest-only relocation, exact declared dependency versions, external cwd.
    manifest=json.loads((W/'package.json').read_text());rel=E/'relocated-package';rel.mkdir(exist_ok=True)
    for name in manifest['files']+['package.json']:
        dst=rel/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,dst)
    args=['--difficulty','easy','--seed','720113','--count','2','--format','json']
    relocated=run([PY,'-B',rel/manifest['entrypoint'],*args],'relocation-command.json')
    original=run([PY,'-B',W/manifest['entrypoint'],*args],'original-cli-command.json')
    save('relocated-records.json',json.loads(relocated.stdout));assert json.loads(original.stdout)==json.loads(relocated.stdout)
    assert set(manifest['dependencies'])=={'python','packages'}
    assert manifest['dependencies']['python']==platform.python_version()
    assert manifest['dependencies']['packages']=={'sympy':g.sp.__version__}
    save('packaging-results.json',{'manifest':manifest,'relocated_matches_original':True,'exact_dependency_contract':True,'actual_python':platform.python_version(),'actual_sympy':g.sp.__version__,'external_output':'CLI pure JSON; no image or filesystem output paths; all required source data resolves relative to entrypoint. Relocated package contains only manifest files and package.json.','deterministic':deterministic})
    save('package-after-sampling.json',hashes());assert hashes()==load('package-before.json')
    (E/'session-state.md').write_text('Source verification, exact retained failures on old/current executables, 13 source banks/69 choices, 100 fresh instances, 70 controlled role assignments, target/irrelevant counterfactuals, invalid/boundary cases and manifest relocation completed. Package hashes unchanged. Next: delivery, native grader, renderer/visual inspection, stage and shortcut reports.\n')
    print(json.dumps({'source_banks':len(replays),'fresh_samples':len(records),'controlled_roles':len(controlled),'math_records':len(cases),'batch_labels':[inspect(r)['good'] for r in batch],'retained_tests':histories}))
if __name__=='__main__':main()
