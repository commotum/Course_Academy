"""Run bounded independent visible-record checks; never changes runtime files."""
import collections
import copy
import itertools
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
sys.dont_write_bytecode=True
from regressions import W, generator as g, matrix, coords, ref_after, check_record
E=W/'evidence'
def save(name, data): (E/name).write_text(json.dumps(data,indent=2)+'\n')
def selected(r):
    f=r['question'][':question/answer-fields'][0]
    return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
def bank(r): return [coords(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
def features(records):
    def all_cells_nonzero(m,b): return all(m[i][j]!=0 for i,j in b)
    sizes=collections.Counter();positions=collections.Counter();sets=set();masks=set();extra=zero_correct=zero_wrong=creates=bottom=0
    probes=collections.defaultdict(lambda:[0,0]); by_pattern=collections.defaultdict(set)
    for r in records:
        q=r['question'];m=matrix(q[':question/problem']);bs=bank(r);ci=selected(r);c=bs[ci]
        sizes[len(c)]+=1;positions[ci]+=1;sets.add(tuple(map(tuple,c)))
        mask=tuple(v!=0 for row in m for v in row);masks.add(mask);by_pattern[str(mask)].add(str(c))
        zero_correct+=not all_cells_nonzero(m,c)
        zero_wrong+=sum(not all_cells_nonzero(m,b) for j,b in enumerate(bs) if j!=ci)
        bottom+=any(not any(row) for row in m)
        a=copy.deepcopy(m)
        for i,j in c:a[i][j]=0
        creates+=sum(not any(row) for row in a)>sum(not any(row) for row in m)
        extra+=any(ref_after(m,list(sub)) for n in range(len(c)) for sub in itertools.combinations(c,n))
        strategies={'first serialized option':0,'lexicographically first set':min(range(5),key=lambda i:bs[i]),
                    'lexicographically last set':max(range(5),key=lambda i:bs[i]),
                    'shortest option first tie':min(range(5),key=lambda i:len(bs[i])),
                    'longest option first tie':max(range(5),key=lambda i:len(bs[i])),
                    'fewest already-zero coordinates':min(range(5),key=lambda i:sum(m[a][b]==0 for a,b in bs[i])),
                    'fewest first-row coordinates':min(range(5),key=lambda i:sum(a==0 for a,b in bs[i]))}
        for group in ['all','first leading column '+str(next(j for j,v in enumerate(m[0]) if v)),'bottom zero row '+str(any(not any(row) for row in m))]:
            for strategy,answer in strategies.items():
                p=probes[group+' / '+strategy];p[0]+=answer==ci;p[1]+=1
    return {'records':len(records),'semantic_instances':len({(tuple(v!=0 for row in matrix(r['question'][':question/problem']) for v in row),tuple(map(tuple,bank(r)[selected(r)]))) for r in records}),
            'zero_structures':len(masks),'correct_coordinate_sets':len(sets),'correct_option_sizes':dict(sizes),'serialized_correct_positions':dict(positions),
            'correct_with_redundant_coordinate':extra,'correct_with_already_zero_coordinate':zero_correct,'distractors_with_already_zero_coordinate':zero_wrong,
            'preexisting_zero_row':bottom,'creates_zero_rows':creates,'probes':dict(probes),'baseline':0.2,
            'same_zero_pattern_different_correct_set':sum(len(x)>1 for x in by_pattern.values())}

def main():
    source=json.loads((W.parent/'source/source.json').read_text())
    replay=[];replay_records=[]
    for q in source['material']['kp'][':knowledge-point/questions']:
        f=q[':question/answer-fields'][0];bs=[coords(a[':answer/value']) for a in f[':answer-field/choices']]
        expected=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
        r=g.generate('moderate',9100,profile=q[':question/id'],replay=True);check_record(r)
        assert matrix(r['question'][':question/problem'])==matrix(q[':question/problem'])
        assert bank(r)==bs and selected(r)==expected
        assert q[':question/problem'].split('$$')[0].strip()==r['question'][':question/problem'].split('$$')[0].strip()
        replay.append({'source_id':q[':question/id'],'matched_choices':5,'complete_bank':True,'key_matches':True,'prompt_prose_matches':True})
        replay_records.append(r)
    save('source-replay.json',replay);save('source-records.json',replay_records)
    canon=source['material']['kp'][':knowledge-point/canonical-example']
    assert ref_after(matrix(canon[':question/problem']),[[2,1],[3,1],[3,2]])
    save('canonical-check.json',{'source_id':canon[':question/id'],'stated_transform_valid':True,'bank_absent':True})
    rs=[g.generate('moderate',i) for i in range(702311,702343)]
    for r in rs: check_record(r)
    save('fresh-records.json',rs)
    batch=json.loads(subprocess.check_output([sys.executable,str(W/'generator.py'),'--difficulty','moderate','--seed','702311','--count','5','--format','json'],text=True))
    for r in batch:check_record(r)
    save('batch-records.json',batch)
    # Exact reviewed fixed-matrix counterexample: change only the successful offered operation.
    source_p=json.loads((W/'checks/source-cases.json').read_text())[0]['parameters']
    nonmin=json.loads((W/'checks/nonminimum-case.json').read_text())['parameters']
    cfs=[g.generate('moderate',8801,parameters=p) for p in [source_p,nonmin]]
    assert matrix(cfs[0]['question'][':question/problem'])==matrix(cfs[1]['question'][':question/problem'])
    assert bank(cfs[0])[selected(cfs[0])]!=bank(cfs[1])[selected(cfs[1])]
    # Change only one matrix entry, keeping every option unchanged; key must switch.
    pair=None
    operations=[list(map(list,b)) for n in (1,2,3) for b in itertools.combinations(itertools.product(range(4),repeat=2),n)]
    # Construct a bank exposing the change, rather than depending on a random
    # bank to contain both decisive operations.
    for r in replay_records+rs:
        original=matrix(r['question'][':question/problem'])
        for i,j in itertools.product(range(4),repeat=2):
            changed=copy.deepcopy(original);changed[i][j]=0 if changed[i][j] else 1
            before_only=[b for b in operations if ref_after(original,b) and not ref_after(changed,b)]
            after_only=[b for b in operations if not ref_after(original,b) and ref_after(changed,b)]
            both_wrong=[b for b in operations if not ref_after(original,b) and not ref_after(changed,b)]
            if before_only and after_only and len(both_wrong)>=3 and not ref_after(changed,[]):
                bs=[before_only[0],after_only[0]]+both_wrong[:3]
                pair=[g.generate('moderate',8802,parameters={'matrix':m,'bank':bs}) for m in [original,changed]]
                cell=[i,j];break
        if pair:break
    assert pair,'No same-bank decision counterfactual found'
    cfs+=pair
    p=copy.deepcopy(pair[0]['generation']['parameters']);ij=next((i,j) for i,j in itertools.product(range(4),repeat=2) if p['matrix'][i][j]);p['matrix'][ij[0]][ij[1]]*=-2
    ir=g.generate('moderate',pair[0]['generation']['seed'],parameters=p)
    assert bank(ir)==bank(pair[0]) and selected(ir)==selected(pair[0]);cfs.append(ir)
    for r in cfs:check_record(r)
    save('counterfactual-records.json',cfs)
    save('counterfactual-results.json',{'fixed_matrix_changed_operation':{'before':bank(cfs[0])[selected(cfs[0])],'after':bank(cfs[1])[selected(cfs[1])]},'fixed_bank_changed_matrix':{'cell_zero_based':cell,'before_key':selected(pair[0]),'after_key':selected(pair[1]),'bank_unchanged':bank(pair[0])==bank(pair[1])},'irrelevant_nonzero_rescale':{'cell_zero_based':ij,'response_preserved':True},'all_visible_records_checked':True})
    save('sampling-summary.json',features(rs));save('math-results.json',{'fresh_checked':len(rs),'source_banks':len(replay),'source_options':75,'batch_checked':len(batch),'counterfactuals_checked':len(cfs),'failures':0,'method':'Parse rendered matrices, coordinates, transformed matrices, and keys; independent lower-pivot-column and zero-row witness.'})
    # All original profiles plus both counterexamples, fresh output and every dependency pair.
    cases=[]
    for n,r in enumerate(replay_records+batch+cfs+rs[:4]):
        f=r['question'][':question/answer-fields'][0];ci=selected(r)
        cases.append({'label':str(n),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==ci else 'rejected','purpose':'independent visible-operation echelon witness'} for i,a in enumerate(f[':answer-field/choices'])]})
    save('grader-input.json',cases)
    save('render-records.json',[replay_records[5],cfs[1],pair[1],batch[0]])
    # Pin installed interpreter; check relocation, reproducibility and requested CLI failure cases.
    manifest=json.loads((W/'package.json').read_text());assert manifest['dependencies']=={'python':platform.python_version(),'packages':{}}
    rel=E/'relocated';rel.mkdir(exist_ok=True)
    for name in manifest['files']+['package.json']:shutil.copyfile(W/name,rel/name)
    args=['--difficulty','moderate','--seed','702311','--count','5','--format','json']
    out=json.loads(subprocess.check_output([sys.executable,str(rel/'generator.py')]+args,text=True,cwd='/tmp'))
    assert out==batch
    invalid=[]
    for args in [['--difficulty','easy'],['--difficulty','moderate','--count','0']]:
        p=subprocess.run([sys.executable,str(W/'generator.py')]+args,capture_output=True,text=True);assert p.returncode!=0;invalid.append({'args':args,'exit':p.returncode})
    save('packaging-results.json',{'python':platform.python_version(),'dependency_shape_matches':True,'relocation_identical':True,'invalid_arguments':invalid,'runtime_files':manifest['files']})
    print(json.dumps({'source_banks':len(replay),'matched_options':75,'fresh':len(rs),'batch':len(batch),'counterfactuals':len(cfs),'native_cases_prepared':len(cases),'sample':features(rs)},indent=2))
if __name__=='__main__': main()
