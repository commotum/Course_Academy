"""Acceptance regression: fail if this pool is solved by row count minus one."""
import argparse,json,sys
sys.dont_write_bytecode=True
from audit import matrices,answer
p=argparse.ArgumentParser();p.add_argument('--input',required=True);a=p.parse_args()
records=json.load(open(a.input));results=[]
for r in records:
    matrix=matrices(r['question'][':question/problem'])[0]
    assert int(matrix.rank())==answer(r), 'Incorrect math must not defeat the shortcut test'
    results.append({'id':r['question'][':question/id'],'rows':matrix.rows,'rank':int(matrix.rank()),'shortcut':matrix.rows-1})
print(json.dumps({'cases':results,'shortcut_successes':sum(x['rank']==x['shortcut'] for x in results),'total':len(results)}))
if records and all(x['rank']==x['shortcut'] for x in results):
    print('FAIL: every delivered member is answered by matrix row count minus one.',file=sys.stderr)
    sys.exit(1)
