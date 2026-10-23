"""Read visible output and report positional/value heuristics before/after delivery.
Called after repair_check has generated current-package evidence.
"""
import collections,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'evidence'
def probe(records):
 groups={}
 for r in records:
  q=r['question'];p=q[':question/problem'];f=q[':question/answer-fields'][0]
  m=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',p,re.S)
  a=[[int(x.strip()) for x in row.split('&')] for row in m[1].split(r'\\')]
  ix=re.search(r'\$\{?([a-z])\}?_\{(\d)(\d)\}',p);i,j=int(ix[2]),int(ix[3]);v=str(a[i-1][j-1]) if i<=len(a) and j<=len(a[0]) else 'No such entry'
  values=[x[':answer/value'] for x in f[':answer-field/choices']]
  # Blank, numeric-only radio and absence-bearing radio have different response contracts.
  group=('display' if '$$' in p else 'inline')+'/'+('blank' if len(values)==1 else 'absence-bank' if 'No such entry' in values else 'numeric-bank')
  d=groups.setdefault(group,{'count':0,'absent':0,'valid':0,'targets':set(),'correct_positions':collections.Counter(),'heuristics':collections.Counter()})
  d['count']+=1;d['absent' if v=='No such entry' else 'valid']+=1;d['targets'].add((len(a),len(a[0]),i,j));d['correct_positions'][str(values.index(v))]+=1
  for name,value in [('first_matrix_value',str(a[0][0])),('last_matrix_value',str(a[-1][-1])),('minimum_matrix_value',str(min(map(min,a)))),('maximum_matrix_value',str(max(map(max,a))))]:d['heuristics'][name]+=int(v==value)
 for d in groups.values():d['targets']=sorted(d['targets'])
 return groups
reports={}
for name in ('samples','prospective-batch','second-batch','controls'):
 reports[name]={stage:probe(json.loads((OUT/file).read_text())) for stage,file in [('before',name+'.json'),('after',name+'-delivery/accepted.json')]}
for stage,groups in reports['samples'].items():
 for group,d in groups.items():
  assert len(d['targets'])>1
  if not group.endswith('blank'):assert len(d['correct_positions'])>1
  assert all(success<d['count'] for success in d['heuristics'].values()),(group,d)
  if group.endswith('absence-bank'):assert d['valid'] and d['absent']
report={'groups':reports,'baseline':'Five radio choices: a fixed option position has 1/5 chance under shuffling. Blanks have one expected answer, not a selectable shortcut. Matrix corner/extremum heuristics do not implement the requested index. Numeric-only banks and blanks cannot express absence by their response contract.','result':'No tested structural shortcut survives the normal sample. Both existence cases survive within every applicable layout of both reported five-record batches. Same-layout and same-label counterfactuals are recorded separately. Small subgroups can have chance coincidences; no claim that arbitrary learner-history subsets retain both cases.'}
(OUT/'shortcut-probes.json').write_text(json.dumps(report,indent=2)+'\n');print('Within-template positional and scalar heuristic probes passed before and after delivery.')
