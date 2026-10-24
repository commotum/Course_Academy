"""Independent choice-only shortcut audit; old banks must reproduce the failure."""
from collections import Counter
import json
from pathlib import Path
import sympy as s
from read_math import scalar,integral
H=Path(__file__).resolve().parent

def audit(rows):
 easy=[];ranks=[];counterparts=[];modal=[]
 for row in rows:
  q=row['question'];f=q[':question/answer-fields'][0]
  if f[':answer-field/type']!=':answer-field.type/radio':continue
  choices=f[':answer-field/choices'];cid=f[':answer-field/correct'][1];correct=next(i for i,a in enumerate(choices)if a[':answer/id']==cid)
  if q[':question/difficulty'].endswith('/easy'):
   fs=[integral(a[':answer/value'])[0]for a in choices];ratios=[s.simplify(v/fs[correct])for v in fs];rank=sum(bool(v<1)for v in ratios);ranks.append(rank)
   counterparts.append([i for i,v in enumerate(ratios)if v>0 and any(s.simplify(v+w)==0 for w in ratios)]==[correct])
   if 'bank_correct_rank'in row['generation']:assert rank==row['generation']['bank_correct_rank']
  else:
   values=[scalar(a[':answer/value'].removesuffix('+C'))for a in choices];components=[]
   for v in values:
    atoms=v.atoms(s.asin,s.atan,s.asec);assert len(atoms)==1;fn=next(iter(atoms));components.append((s.simplify(v/fn),fn.args[0]))
   a=Counter(c for c,arg in components);b=Counter(arg for c,arg in components);winners=[i for i,(c,arg)in enumerate(components)if a[c]==max(a.values())and b[arg]==max(b.values())];modal.append(winners==[correct])
 return {'easy_rank_counts':dict(Counter(ranks)),'easy_unique_sign_counterpart_successes':sum(counterparts),'easy_count':len(ranks),'inverse_component_mode_successes':sum(modal),'inverse_full_count':len(modal)}
def main():
 reports={};old_failure=0
 for d in sorted(H.glob('175*')):
  new=json.loads((d/'accepted-pool.json').read_text());old=json.loads((d/'publication/preparation.json').read_text())['records'];a=audit(new);b=audit(old)
  assert len(a['easy_rank_counts'])>=2 and max(a['easy_rank_counts'].values())<=4
  assert a['easy_unique_sign_counterpart_successes']<a['easy_count']
  if a['inverse_full_count']:assert a['inverse_component_mode_successes']<a['inverse_full_count']
  assert len(b['easy_rank_counts'])==1;old_failure+=1;reports[d.name]={'before':b,'after':a}
 (H/'bank-shortcut-verification.json').write_text(json.dumps({'passed':True,'prior_failure_reproduced_kps':old_failure,'knowledge_points':reports},indent=2)+'\n');print('Bank-only shortcut checks passed; prior rank shortcut reproduced for',old_failure,'KPs')
if __name__=='__main__':main()
