"""Strict regression: a bank-only shape/sign selector must not solve the whole delivered batch."""
import sys
sys.dont_write_bytecode=True
from audit import *

def select(r):
 f=r['question'][':question/answer-fields'][0]
 choices=[(a,mat(a[':answer/value'])) for a in f[':answer-field/choices']]
 extra=[m for a,m in choices if len(m)==3 and len(m[0])==3 and m[2]==[0,0,0]]
 if len(extra)==1:
  hits=[a for a,m in choices if m==extra[0][:2]]
  if len(hits)==1:return hits[0][':answer/id']
 candidates=[(a,m) for a,m in choices if len(m)==2 and len(m[0])==3]
 if len(candidates)==4:
  for row in [0,1]:
   cnt=collections.Counter(sp.sign(m[row][0]) for a,m in candidates)
   if sorted(cnt.values())==[1,3]:
    return next(a[':answer/id'] for a,m in candidates if cnt[sp.sign(m[row][0])]==1)
 return None

def main():
 p=Path(sys.argv[1]) if len(sys.argv)>1 else E/'delivery-batch/accepted.json'
 records=load(p);results=[];native=[]
 for r in records:
  selected=select(r);q=r['question'];f=q[':question/answer-fields'][0]
  success=selected==f[':answer-field/correct'][1]
  results.append({'id':q[':question/id'],'seed':r['generation']['seed'],'selected_answer':selected,'success':success})
  if selected:native.append({'label':'bank-only-selector','record':r,'checks':[{'submitted_answer_id':selected,'expected':'accepted' if success else 'rejected','purpose':'verify actual learner outcome of bank-only answer-producing action'}]})
 save('shortcut-native-input.json',native);save('shortcut-regression.json',{'input':str(p),'results':results,'correct':sum(x['success'] for x in results),'total':len(records),'expected':'At least one record requires reconsidering the bank-only shortcut','status':'failed' if all(x['success'] for x in results) else 'passed'})
 print(json.dumps({'correct':sum(x['success'] for x in results),'total':len(records)}))
 assert not all(x['success'] for x in results),'Incidental bank-only selector answers every delivered batch member'
if __name__=='__main__':main()
