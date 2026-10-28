import collections,difflib,json
from pathlib import Path
H=Path(__file__).resolve().parent;ns={'__file__':str(H/'prepare_source_proposals.py')};exec((H/'prepare_source_proposals.py').read_text().split('options=collections')[0],ns);R=[]
for unresolved in json.loads((H/'source-proposal-unresolved.json').read_text()):
 key=(unresolved['entity'],unresolved['attribute']);stored=ns['F'][key]['value'];old=ns['mathvalues'](stored);ss=[r for r in ns['S']if(r['entity'],r['attribute'])==key];row={**unresolved,'current':stored,'variants':[]}
 for s in ss:
  new=s['formulas'];changes=[]
  for i,x in enumerate(old):
   ys={y for y in new if ns['core'](x)==ns['core'](y)and ns['role_missing'](x,y)}
   if len(ys)==1:changes.append({'index':i,'before':x,'after':next(iter(ys))})
  row['variants'].append({'path':s['path'],'source_identity':s['source_identity'],'source_formulas':new,'stored_count':len(old),'source_count':len(new),'style_restoration_candidates':changes})
 R.append(row)
(H/'source-conflict-details.json').write_text(json.dumps(R,indent=2));print('conflicts',len(R))
for r in R:
 print('\nENTITY',r['entity'],'currentformulas',r['variants'][0]['stored_count']);seen=set()
 for v in r['variants']:
  formulas=json.dumps(v['source_formulas'])
  if formulas in seen:continue
  seen.add(formulas);print('SOURCE',v['source_identity'],Path(v['path']).name,'formulacount',v['source_count']);print('styles',[(c['index'],c['before'][:95],c['after'][:95])for c in v['style_restoration_candidates']]);print('formulas tail',v['source_formulas'][-3:])
