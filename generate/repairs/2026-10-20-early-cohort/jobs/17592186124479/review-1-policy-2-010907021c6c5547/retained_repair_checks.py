"""Retained finding 9fc5bf8959a070427459: test current CLI and delivered pool.

No network, database writes, or runtime-file mutations. Writes evidence only.
"""
import sys
sys.dont_write_bytecode=True
import argparse,json,subprocess
from pathlib import Path
from collections import defaultdict
from audit import matrices,answer,check
ROOT=Path(__file__).resolve().parent.parent/'workspace'
sys.path.insert(0,str(ROOT))
import generator as g
REPO=Path('/home/jake/Developer/Course_Academy')
OUT=Path(__file__).resolve().parent/'author-check';OUT.mkdir(exist_ok=True)

def save(name,value): (OUT/name).write_text(json.dumps(value,indent=2)+'\n')

def assert_varied(records):
    assert records
    groups=defaultdict(list)
    for r in records:
        result=check(r);assert not result['errors'],result
        a=matrices(r['question'][':question/problem'])[0]
        groups[(a.rows,a.cols)].append(answer(r))
        groups[(r['generation']['template'],sum(any(a.row(i)) for i in range(a.rows)))].append(answer(r))
    # Stronger than the original predicate: no constant count within a selected
    # shape or workload/active-row group, even if rows-minus-one happens to fail.
    for cue,values in groups.items():assert len(set(values))>=2,(cue,values)
    assert not all(answer(r)==matrices(r['question'][':question/problem'])[0].rows-1 for r in records)
    return [{'cue':list(cue),'ranks':values} for cue,values in groups.items()]

def cli(seed,count=5,template=None):
    command=[sys.executable,'-B',str(ROOT/'generator.py'),'--difficulty','moderate','--count',str(count),'--seed',str(seed),'--format','json']
    if template:command+=['--template',template]
    result=subprocess.run(command,capture_output=True,text=True,check=True)
    records=json.loads(result.stdout);assert len(records)==count
    return records

def main():
    assert cli(0,0)==[]
    assert cli(19,1)==[g.generate(seed=19)]
    bad=subprocess.run([sys.executable,'-B',str(ROOT/'generator.py'),'--count','-1'],capture_output=True,text=True)
    assert bad.returncode!=0
    runs=[];primary=cli(315106964);save('repaired-batch.json',primary)
    runs.append({'seed':315106964,'count':5,'coverage':assert_varied(primary)})
    assert primary==cli(315106964),'nondeterminism'
    # Small independent seed/count checks; no hundreds-of-seeds search.
    controls=[]
    for seed,count in [(0,2),(42,3),(1009,6)]:
        rs=cli(seed,count);runs.append({'seed':seed,'count':count,'coverage':assert_varied(rs)});controls+=rs
    # Every retained source workload must still deliver both survival outcomes.
    for i,t in enumerate(g.TEMPLATES):
        rs=g.generate_batch(count=2,seed=8840+i,template=t)
        runs.append({'template':t,'coverage':assert_varied(rs)});controls+=rs
    save('regression-controls.json',controls)
    save('regression-results.json',{'finding':'9fc5bf8959a070427459','runs':runs,'passed':True})
    command=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(OUT/'repaired-batch.json'),'--source',str(ROOT.parent/'source/source.json'),'--inventory',str(ROOT.parent/'source/inventory.json'),'--difficulty','moderate','--output',str(OUT/'delivery'),'--asset-root',str(ROOT),'--math-root','/media/jake/SSD/EDB/math']
    result=subprocess.run(command,capture_output=True,text=True,check=True)
    accepted=json.loads((OUT/'delivery/accepted.json').read_text())
    assert len(accepted)==len(primary),'Filtering removed required decision contrasts'
    coverage=assert_varied(accepted)
    save('post-delivery-regression.json',{'command':command,'stdout':result.stdout,'coverage':coverage,'passed':True})
    print(json.dumps({'finding':'9fc5bf8959a070427459','passed':True,'batches':len(runs),'delivered':len(accepted)}))

if __name__=='__main__':main()
