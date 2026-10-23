"""Regression 16d8aab11f7bf5c7e3dd: current batches through real delivery.
Independent witnesses read visible equations and options, not bank metadata.
"""
import sys, json, subprocess, importlib.util
from collections import defaultdict, Counter
from pathlib import Path
sys.dont_write_bytecode = True
import check_repair as c
ROOT = c.ROOT
OUT = ROOT/'evidence/repair-2'
REPO = Path('/home/jake/Developer/Course_Academy')
spec = importlib.util.spec_from_file_location('witness', ROOT/'17592186059776/validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)

def save(name, data):
    (OUT/name).write_text(json.dumps(data, indent=2, default=str)+'\n')

def audit(records):
    groups = defaultdict(list)
    semantic = set()
    for r in records:
        q = r['question']; m = v.supplied(q)
        key = str((tuple(m[:, :2]), 'and then solve' in q[':question/problem']))
        groups[key].append(c.features(r))
        semantic.add(tuple(m[:,:2].inv()*m[:,2]))
    assert len(semantic)==len(records), 'Repeated solution task'
    result = {}
    for key, rows in groups.items():
        ranks=Counter(r['rank'] for r in rows); positions=Counter(r['position'] for r in rows)
        if len(rows)>1:
            assert len(ranks)>1, (key, 'fixed numerical rank', rows)
            assert len(positions)>1, (key, 'fixed authored position', rows)
        result[key]={'n':len(rows),'ranks':dict(ranks),'positions':dict(positions),
                     'second_largest_hits':sum(r['rank']==4 for r in rows)}
    return result

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    reports={}
    # Exact failing seed first; then small samples exercising both supported bands.
    for name, level, count, seed in [('exact','easy',5,3334594587),
                                   ('easy','easy',15,59776),('moderate','moderate',15,59776)]:
        records=c.g.batch(level,count,seed)
        save(name+'-records.json',records)
        before=audit(records)
        cmd=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),
             '--input',str(OUT/(name+'-records.json')),'--source','/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186059776/source/source.json',
             '--inventory','/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186059776/source/inventory.json','--difficulty',level,
             '--output',str(OUT/('delivery-'+name)),'--asset-root',str(OUT),
             '--math-root','/media/jake/SSD/EDB/math']
        p=subprocess.run(cmd,capture_output=True,text=True)
        save(name+'-delivery-command.json',{'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
        assert p.returncode==0, p.stderr
        accepted=json.loads((OUT/('delivery-'+name)/'accepted.json').read_text())
        assert len(accepted)==count, 'Delivery removed a required contrast'
        after=audit(accepted)
        reports[name]={'before':before,'after':after,'input':len(records),'accepted':len(accepted)}
    # Ensure the exact regression still exercises the reported visible subgroup.
    exact=json.loads((OUT/'delivery-exact/accepted.json').read_text())
    focused=[r for r in exact if '2x-4y &=' in r['question'][':question/problem']
             and '4x-7y &=' in r['question'][':question/problem']]
    assert len(focused)>=2, 'Reported family was avoided rather than contrasted'
    assert len({c.features(r)['rank'] for r in focused})>1
    # Keep the old isolated counterexamples: the fix is selection, not rewriting them.
    isolated=[c.g.generate('easy',3334594587,'q-73544',p) for p in [[2,3],[-1,1]]]
    save('isolated-counterexamples.json',isolated)
    assert all(c.features(r)['rank']==4 for r in isolated)
    save('batch-results.json',reports)
    print(json.dumps({'passed':True,'batches':{k:{'input':r['input'],'accepted':r['accepted'],'families':len(r['after'])} for k,r in reports.items()},
                      'exact_q73544_ranks':[c.features(r)['rank'] for r in focused]}))

if __name__=='__main__':main()
