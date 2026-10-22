import pathlib,json,sys
E=pathlib.Path(__file__).resolve().parent
ns={'__file__':str(E/'audit.py')};exec(compile((E/'audit.py').read_text().split('source=json.load')[0],'audit.py','exec'),ns)
rows=[]
for stage in ['batch','moderate','hard']:rows.extend(json.loads((E/f'delivery-{stage}/accepted.json').read_text()))
cases=json.loads((E/'native-input.json').read_text());cases.extend(ns['native'](rows));ns['save']('native-input.json',cases)
results=[ns['parse'](r) for r in rows];ns['save']('delivered-math-results.json',{'count':len(results),'failures':[r for r in results if r['errors']],'cases':results});assert not any(d['errors'] for d in results)
print('Native cases',len(cases),'response checks',sum(len(x['checks']) for x in cases),'normalized records',len(rows))
