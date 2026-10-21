"""Review the complete non-bare-label cohort, preserving shared matrix setup."""
import copy,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
def main():
 qs=json.loads((HERE/'questions.json').read_text());cases=[];ledger=[]
 nonbare={x['question'] for x in json.loads((HERE/'nonbare-audit.json').read_text())}
 for q in qs:
  if q[':db/id'] not in nonbare:continue
  a=copy.deepcopy(q);fields=a[':question/answer-fields'];objects=[]
  if all(re.fullmatch('Column [1-6]',f[':answer-field/key'])for f in fields):
   matrices=list(re.finditer(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S));assert len(matrices)==1,q[':db/id']
   rows=[[c.strip()for c in row.split('&')]for row in matrices[0][1].split('\\\\')]
   assert len({len(r) for r in rows})==1 and len(rows[0])==len(fields)
   for f in fields:
    label=f[':answer-field/key'];n=int(label.split()[-1]);column='\\begin{bmatrix}'+r' \\ '.join(row[n-1]for row in rows)+'\\end{bmatrix}'
    f[':answer-field/key']=label+': $'+column+'$'
    objects.append({'source_label':label,'field_id':f[':db/id'],'content':f[':answer-field/key'],'evidence':'Column extracted verbatim in row order from the current shared source matrix; its full matrix remains necessary to determine pivot positions.'})
   kind='complete-column-objects'
  elif q[':db/id']==17592186493109:
   expected={'answer-c1':'True','answer-c2':'False'}
   for f in fields:
    label=f[':answer-field/key'];f[':answer-field/key']=expected[label]
    objects.append({'source_label':label,'field_id':f[':db/id'],'content':expected[label],'source_fragment':('c1. True: {{answer-c1}}'if label=='answer-c1'else'c2. False: {{answer-c2}}')})
   a[':question/problem']=q[':question/problem'].split('\n\nc1. True:')[0]
   assert '{{answer-'not in a[':question/problem']
   kind='move-placeholder-choices'
  else:
   ledger.append({'question':q[':db/id'],'status':'already-complete','keys':[f[':answer-field/key']for f in fields],'evidence':'Every checkbox contains the full matrix or independently testable statement; prompt contains only shared setup.'});continue
  cases.append({'question':q[':db/id'],'before':q,'after':a,'objects':objects,'method':kind})
  ledger.append({'question':q[':db/id'],'status':'repair-prepared','method':kind})
 (HERE/'other-cases.json').write_text(json.dumps({'cases':cases},ensure_ascii=False,indent=2)+'\n')
 (HERE/'other-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
 print({'repairs':len(cases),'already_complete':len(ledger)-len(cases)})
if __name__=='__main__':main()
