import json,sys
from pathlib import Path
sys.dont_write_bytecode=True
from independent_oracle import s,parse,probe,correct
E=Path(__file__).resolve().parent
summary=[];grader=[]
for band in ['easy','moderate','hard']:
 records=json.loads((E/('delivery-'+band)/'accepted.json').read_text())
 groups={}
 for r in records:
  q=r['question'];f=q[':question/answer-fields'][0];values=[parse(a[':answer/value'].strip('$')) for a in f[':answer-field/choices']];key=parse(correct(q)[':answer/value'].strip('$'))
  assert not probe(r)['success']
  name=r['generation']['template'];group=groups.setdefault(name,{'banks':{},'ranks':set(),'positions':set(),'areas':set()})
  group['ranks'].add(sum(float(z)<float(key)-1e-10 for z in values));group['areas'].add(str(key));group['positions'].add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==correct(q)[':answer/id']))
  bank=tuple(sorted(map(str,values)));group['banks'].setdefault(bank,set()).add(str(key))
  grader.append({'label':'delivery-'+q[':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if s.simplify(parse(a[':answer/value'].strip('$'))-key)==0 else 'rejected','purpose':'Check localized identity and owned key after delivery normalization'} for a in f[':answer-field/choices']]})
 for name,g in groups.items():
  largest=max(map(len,g['banks'].values()));assert largest==5,(name,largest)
  assert g['ranks']==set(range(5)) and g['positions']==set(range(5)),name
  summary.append({'band':band,'family':name,'surviving_same_bank_distinct_answers':largest,'ranks':sorted(g['ranks']),'positions':sorted(g['positions']),'semantic_areas':len(g['areas'])})
(E/'post-delivery-shortcuts.json').write_text(json.dumps(summary,indent=2))
(E/'delivery-grader-input.json').write_text(json.dumps(grader,indent=2))
print('All eight families retain five target roles in identical banks after actual delivery filters.')
