"""Reapply only verified transaction projections to the frozen audit and rerun checks."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
rows=json.loads((P/'content.json').read_text());repaired={r[':db/id']:r for r in json.loads((P/'repaired-records.json').read_text())}
def apply(v):
 if isinstance(v,dict):
  if v.get(':db/id') in repaired and (':question/id' in v or ':tutorial/id' in v):return repaired[v[':db/id']]
  return {k:apply(x) for k,x in v.items()}
 if isinstance(v,list):return [apply(x) for x in v]
 return v
rows=apply(rows)
s=(P/'structural.py').read_text();s=s[:s.index('priority=[]')];s=s.replace("rows=json.loads((P/'content.json').read_text());",'rows=post_rows;');s=s.replace("(P/(name+'.json')).write_text(json.dumps(obj,indent=2))","(P/('after-'+name+'.json')).write_text(json.dumps(obj,indent=2)) if name in ['structure-summary','structure-findings'] else None")
exec(compile(s,str(P/'structural.py'),'exec'),{'__file__':str(P/'structural.py'),'post_rows':rows})
for t in rows:
 if t[':topic/math-academy-id'] in [862,146,232]:(P/(str(t[':topic/math-academy-id'])+'-priority-after.json')).write_text(json.dumps(t,indent=2))
s=(P/'priority_math.py').read_text().replace("str(topic)+'-priority.json'","str(topic)+'-priority-after.json'")
s=s.replace("proposals={(x['entity'],x['attribute']):x['new'] for x in json.loads((P/'source-proposals.json').read_text())}",'proposals={}')
s=s.replace("       if table:\n", "       if not table and 'matrix-answer' in prompt:\n        import html\n        tbody=re.search(r'<tbody>([\\s\\S]*?)</tbody>',prompt)[1];table_cells=[html.unescape(v).strip('$').strip() for v in re.findall(r'<td[^>]*>([\\s\\S]*?)</td>',tbody)];assert len(table_cells)==target.rows*target.cols;expected=target[table_cells.index('{{'+key+'}}')]\n       elif table:\n")
s=s.replace("else:raise ValueError('Matrix blank has no explicit supported row mapping')", "else:raise ValueError('Matrix blank has no explicit supported row mapping')")
for name in ['priority-math-report','priority-math-issues','key-proposals','solution-proposals']:s=s.replace("P/'"+name+".json'","P/'after-"+name+".json'")
exec(compile(s,str(P/'priority_math.py'),'exec'),{'__file__':str(P/'priority_math.py')})
