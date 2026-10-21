"""Independent exhaustive subset checks for minimum-set generation and repairs."""
from pathlib import Path
import itertools, json, re, sys, subprocess
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'package'))
import generator as g

def parse(text):
    body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)[1]
    return [[int(v.strip()) for v in row.split('&')] for row in body.split(r'\\')]

def entries(text):
    return [[int(i)-1,int(j)-1] for i,j in re.findall(r'(?:\{a\}|a)_\{(\d)(\d)\}',text)]

def ref(matrix,removed):
    removed=set(map(tuple,removed));last=-1;zero=False
    for i,row in enumerate(matrix):
        remaining=[j for j,v in enumerate(row) if v and (i,j) not in removed]
        if not remaining:zero=True
        elif zero or remaining[0]<=last:return False
        else:last=remaining[0]
    return True

def brute_minima(matrix):
    cells=[(i,j) for i,row in enumerate(matrix) for j,v in enumerate(row) if v]
    for count in range(len(cells)+1):
        good=[list(map(list,b)) for b in itertools.combinations(cells,count) if ref(matrix,b)]
        if good:return good

def check(q):
    m=parse(q[':question/problem']);mins=brute_minima(m)
    assert len(mins)==1
    f=q[':question/answer-fields'][0]
    ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
    bank=[entries(a[':answer/value']) for a in f[':answer-field/choices']]
    assert [ref(m,b) for b in bank]==[i==ci for i in range(len(bank))]
    assert sorted(bank[ci])==mins[0]
    assert parse(q[':question/worked-solution'])==m
    bodies=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/worked-solution'],re.S)
    last=[[int(v.strip()) for v in row.split('&')] for row in bodies[-1].split(r'\\')]
    assert last==g.erase(m,mins[0])
    assert 'fewest replacements' in q[':question/problem']
    return ci

def main():
    cat=json.loads((HERE/'package/catalogue.json').read_text());pairs=0
    for role in cat:
        for mask in role['masks']:
            m=[[int(bool(mask & (1<<(4*i+j)))) for j in range(4)] for i in range(4)]
            assert brute_minima(m)==[role['targets']]==g.minimum_sets(m)
            pairs+=1
    records=[g.generate('moderate',915000+n) for n in range(120)]
    for r in records:
        check(r['question']);assert r==g.generate('moderate',r['generation']['seed'])
    regression_matrix=[[-3,4,0,-5],[0,0,-1,-2],[0,0,0,-8],[0,-4,5,0]]
    assert brute_minima(regression_matrix)==[[[3,1],[3,2]]]
    bad={'matrix':regression_matrix,'bank':[[[1,2],[3,1],[3,2]],[[1,3],[3,1],[3,2]],[[1,2],[1,3],[3,2]],[[1,2],[2,3],[3,2]],[[1,2],[1,3],[2,3]]]}
    try:g.generate('moderate',0,parameters=bad)
    except ValueError:pass
    else:raise AssertionError('Original padded key was accepted')
    repair_path=HERE/'repaired-records.json'
    if repair_path.exists():
        repairs=json.loads(repair_path.read_text())
        for r in repairs:check(r['question'])
        records+=repairs
    native=[]
    for n,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0]
        native.append({'label':f'minimum-{n}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Independently verified minimum set'} for a in f[':answer-field/choices']]})
    (HERE/'grader-input.json').write_text(json.dumps(native,indent=2)+'\n')
    ROOT=next(p for p in HERE.parents if (p/'Cargo.toml').exists())
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'grader-input.json'),str(HERE/'grader-report.json')],check=True)
    (HERE/'samples.json').write_text(json.dumps(records[:5]+records[120:],indent=2)+'\n')
    report={'passed':True,'catalogue_roles':len(cat),'all_catalogue_pairs_checked':pairs,'oracle':'Exhaustive subsets of every nonzero matrix entry, including first-row entries','fresh_samples':120,'repaired_records':len(records)-120,'original_padded_answer_rejected':True,'native_grader':json.loads((HERE/'grader-report.json').read_text())}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='native_grader'}))

if __name__=='__main__':main()
