"""Source replay, visible math, controlled witnesses, inventory and packaging."""
import sys
sys.dont_write_bytecode=True
import copy,json,os,shutil,subprocess
from pathlib import Path
from collections import Counter,defaultdict
from audit import matrices,answer,field,check
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence'
sys.path.insert(0,str(ROOT))
import generator as g
PY=sys.executable
REPO=Path('/home/jake/Developer/Course_Academy')
def read(p):return json.loads(p.read_text())
def save(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def main():
    source=read(ROOT.parent/'source/source.json')['material']['kp']
    assert g.KP[':knowledge-point/id']==source[':knowledge-point/id']
    # Captured source now uses scalable fraction parentheses; compare complete
    # mathematical stages and banks below, not incidental TeX delimiters.
    replays=[];results=[]
    for q in source[':knowledge-point/questions']:
        r=g.source_replay(q[':question/math-academy-id']);replays.append(r)
        assert matrices(q[':question/problem'])==matrices(r['question'][':question/problem'])
        assert matrices(q[':question/worked-solution'])==matrices(r['question'][':question/worked-solution'])
        sf=q[':question/answer-fields'][0]
        assert sorted(x[':answer/value'] for x in sf[':answer-field/choices'])==sorted(x[':answer/value'] for x in field(r)[':answer-field/choices'])
        assert int(sf[':answer-field/correct'][':answer/value'])==answer(r)
        results.append({'source_id':q[':question/id'],'passed':True})
    save('source-replays.json',replays);save('source-replay-results.json',results)
    # Retain review's exact controlled relevant/irrelevant witnesses; regenerate
    # them against the current runtime rather than trusting old results.
    old=read(ROOT.parent/'review-0-policy-2-aac6b6dace0e282d/counterfactual-records.json')
    cf=[g.generate(seed=r['generation']['seed'],template=r['generation']['template'],parameters=r['generation']['parameters']) for r in old]
    assert [answer(r) for r in cf]==[2,3,3,3]
    a,b,c,d=[matrices(r['question'][':question/problem'])[0] for r in cf]
    assert sum(x!=y for x,y in zip(a,b))==1
    assert b==c and b!=d
    save('counterfactual-records.json',cf)
    save('counterfactual-results.json',{'relevant_single_cell_change':[answer(cf[0]),answer(cf[1])],'irrelevant_label_change':[answer(cf[1]),answer(cf[2])],'irrelevant_nonzero_row_scale':[answer(cf[1]),answer(cf[3])],'passed':True})
    controls=read(OUT/'regression-controls.json');batch=read(OUT/'delivery/accepted.json')
    # Fill only missing permitted rank cases for each workload.
    extra=[];coverage=[]
    for i,(t,info) in enumerate(g.TEMPLATES.items()):
        rs=[r for r in controls if r['generation']['template']==t]
        seen={answer(r) for r in rs}
        m=info['states'][0].rows;k=len(info['operations'])
        for rank in g.permitted_ranks(info):
            if rank not in seen:
                active=next(a for a in range(max(3,min(g.permitted_ranks(info))+1),m+1) if a-k<=rank<=a)
                r=g.generate(seed=7010+i,template=t,decision=(rank,active));rs.append(r);extra.append(r)
        coverage.append({'template':t,'ranks':dict(Counter(answer(r) for r in rs)),'allowed_ranks':g.permitted_ranks(info),'profiles':sorted({r['generation']['profile'] for r in rs})})
    # A missing-rank boundary may introduce another active-row group: retain a
    # contrasting rank there too, so its conditional probe is meaningful.
    groups=defaultdict(list)
    for r in controls+extra:
        a=matrices(r['question'][':question/problem'])[0]
        groups[(r['generation']['template'],sum(any(a.row(i)) for i in range(a.rows)))].append(answer(r))
    for gi,((t,active),values) in enumerate(groups.items()):
        if len(set(values))==1:
            k=len(g.TEMPLATES[t]['operations'])
            other=next(r for r in g.permitted_ranks(g.TEMPLATES[t]) if active-k<=r<=active and r!=values[0])
            extra.append(g.generate(seed=7053+gi,template=t,decision=(other,active)))
    save('coverage.json',coverage);save('extra-decision-records.json',extra)
    all_records=replays+cf+controls+batch+extra
    checks=[check(r) for r in all_records];assert not any(r['errors'] for r in checks),[r for r in checks if r['errors']]
    save('math-results.json',{'checked':len(checks),'failures':[],'cases':checks})
    save('control-records.json',controls+extra+cf)
    grader=[]
    # Correct and every incorrect radio choice, including counterfactual reversal.
    for r in all_records:
        rank=int(matrices(r['question'][':question/problem'])[0].rank())
        grader.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if int(c[':answer/value'])==rank else 'rejected','purpose':'Independent exact visible-matrix rank'} for c in field(r)[':answer-field/choices']]})
    save('grader-input.json',grader)
    inv=read(ROOT.parent/'source/inventory.json');facts=[]
    for q in inv['questions']:
        r={'question':q};a=matrices(q[':question/problem'])[0]
        facts.append({'id':q[':question/id'],'entity_id':q[':db/id'],'rank':int(a.rank()),'rows':a.rows,'original_source':bool(q.get(':question/math-academy-id'))})
    newids={r['question'][':question/id'] for r in read(OUT/'original-delivered.json')}
    assert not newids.intersection(q['id'] for q in facts)
    assert not all(q['rank']==q['rows']-1 for q in facts)
    stored_generated=[q for q in facts if not q['original_source']]
    assert not all(q['rank']==q['rows']-1 for q in stored_generated)
    (ROOT/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2)+'\n')
    save('inventory-assessment.json',{'basis':inv['basis'],'tested':len(facts),'source_tested':len(facts)-len(stored_generated),'generated_tested':len(stored_generated),'shortcut_successes':sum(q['rank']==q['rows']-1 for q in facts),'generated_shortcut_successes':sum(q['rank']==q['rows']-1 for q in stored_generated),'facts':facts,'conclusion':'All captured items tested for the retained batch predicate. Neither stored whole pool nor generated subset has the all-corank-one defect. Old delivered IDs are absent. A single corank-one item is not defective. No generation metadata invented; original sources not reclassified. This verifies absence of this specific pool defect at captured basis, not absence of all possible defects.'})
    manifest=read(ROOT/'package.json')
    assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':g.s.__version__}}
    assert (ROOT/'requirements.txt').read_text().strip()=='sympy=='+g.s.__version__
    relocated=OUT/'relocated';relocated.mkdir(exist_ok=True)
    for name in manifest['files']:shutil.copyfile(ROOT/name,relocated/name)
    env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(OUT/'assets'),'PYTHONDONTWRITEBYTECODE':'1'}
    command=[PY,'-E','-s','-B',str(relocated/'generator.py'),'--difficulty','moderate','--count','5','--seed','315106964','--format','json']
    relocated_batch=json.loads(subprocess.run(command,cwd='/tmp',env=env,text=True,capture_output=True,check=True).stdout)
    assert relocated_batch==read(OUT/'repaired-batch.json')
    save('packaging-results.json',{'relocation_command':command,'identical':True,'dependencies':manifest['dependencies'],'assets':'No generated or referenced images; no asset writes needed.'})
    # Keep actual UI verification small: two conflicting delivered cases plus
    # widest six-column source replay. No changed rendering implementation.
    first=batch[0];second=next(r for r in batch if answer(r)!=answer(first))
    wide=next(r for r in replays if matrices(r['question'][':question/problem'])[0].cols==6)
    save('render-input.json',[first,second,wide])
    print(json.dumps({'source_replays':len(replays),'math_checked':len(checks),'grader_responses':len(grader)*5,'missing_rank_cases_added':len(extra),'inventory_tested':len(facts),'relocation':'passed'}))
if __name__=='__main__':main()
