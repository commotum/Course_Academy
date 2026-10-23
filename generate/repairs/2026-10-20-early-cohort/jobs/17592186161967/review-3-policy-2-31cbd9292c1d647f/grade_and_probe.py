import json,sys,pathlib,collections
sys.dont_write_bytecode=True
from helpers import check,ops,mats
R=pathlib.Path(__file__).resolve().parent
def save(n,x):(R/n).write_text(json.dumps(x,indent=2)+'\n')
probe=[];grades=json.load(open('grader-input.json'))
for label,file in [('batch','batch.json'),('delivered-batch','delivery-batch/accepted.json'),('cli','fresh-cli.json'),('delivered-cli','delivery-cli/accepted.json'),('fixed-bank','fixed-bank-records.json')]:
 rows=json.load(open(file)); groups=collections.defaultdict(list)
 for r in rows:
  ci=check(r);q=r['question'];f=q[':question/answer-fields'][0];bank=[tuple(o[2] for o in ops(a[':answer/value'])) for a in f[':answer-field/choices']];correct=bank[ci]
  mags=tuple(collections.Counter(abs(z[d]) for z in bank).most_common(1)[0][0] for d in (0,1));extra=next(z for z in bank if tuple(map(abs,z))!=mags)
  shape='unit-first' if abs(extra[1])==mags[1] else 'unit-second' if abs(extra[0])==mags[0] else 'swap'
  detail={'id':q[':question/id'],'correct':correct,'extra':extra,'position':ci,'bank':bank,'shape':shape,'input_file':file}
  groups['all'].append(detail);groups[shape].append(detail)
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==ci else 'rejected','purpose':'independent exact arithmetic for whole-row transformation'} for j,a in enumerate(f[':answer-field/choices'])]
  for d in (0,1):
   for polarity in (-1,1):
    # Compute the other coefficient independently, infer this coordinate from the extra option.
    A,B=mats(q[':question/problem']);p=next(i for i in range(3) if A[i]==B[i]);tt=[i for i in range(3) if i!=p];c=next(c for c in range(3) if A[p][c] and all(B[t][c]==0 for t in tt))
    pred=[-A[t][c]//A[p][c] for t in tt];pred[d]=polarity*(1 if extra[d]>0 else -1)*mags[d];ix=bank.index(tuple(pred))
    checks.append({'submitted_answer_id':f[':answer-field/choices'][ix][':answer/id'],'expected':'accepted' if ix==ci else 'rejected','purpose':f'Infer coordinate {d} from outlier sign polarity {polarity}; calculate other only'})
  if label in ['delivered-batch','delivered-cli']:grades.append({'label':label+'-'+q[':question/id'],'record':r,'checks':checks})
 for subgroup,items in groups.items():
  for d in (0,1):
   for polarity in (-1,1):
    hits=sum((i['extra'][d]*i['correct'][d]>0)==(polarity==1) for i in items)
    probe.append({'label':label,'subgroup':subgroup,'strategy':f'outlier sign coordinate {d}, polarity {polarity}, calculate other coefficient','correct':hits,'total':len(items),'baseline':0.5,'file':file})
  for pos in range(5):probe.append({'label':label,'subgroup':subgroup,'strategy':f'fixed stored position {pos+1}','correct':sum(i['position']==pos for i in items),'total':len(items),'baseline':0.2,'file':file})
  # Old modal shortcut is equivalent to same outlier sign in unchanged coordinate.
  for d in (0,1):
   modal=[]
   for i in items:
    cc=collections.Counter(z[d] for z in i['bank']);val,n=cc.most_common(1)[0]
    if list(cc.values()).count(n)==1:modal.append(val==i['correct'][d])
   if modal:probe.append({'label':label,'subgroup':subgroup,'strategy':f'modal signed coefficient {d}, calculate other','correct':sum(modal),'total':len(modal),'baseline':0.5,'file':file})
save('probes.json',probe);save('grader-combined-input.json',grades)
assert len(json.load(open('delivery-cli/accepted.json')))==len(json.load(open('fresh-cli.json')))
print(json.dumps({'grader_records':len(grades),'grader_checks':sum(len(z['checks']) for z in grades),'cli_survivors':len(json.load(open('delivery-cli/accepted.json'))),'batch_probes':[p for p in probe if p['label']=='delivered-batch' and p['subgroup']=='all']}))
