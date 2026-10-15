"""Verify existing source inventory independently of generative radio support."""
import copy,json,subprocess
from pathlib import Path
import validate as v
HERE=Path(__file__).resolve().parent
def main():
 records=[];accepted=[];excluded=[]
 for t,q in v.g.SOURCES.items():
  fs=q[':question/answer-fields'];keys=[f[':answer-field/key'] for f in fs]
  if len(set(keys))!=len(keys) or not q.get(':question/worked-solution') or ':question/difficulty' not in q or not all(':answer-field/correct' in f for f in fs):
   excluded.append({'source':t,'id':q[':db/id'],'reason':'Duplicate/unkeyed fields, missing solution, or unrated; preserved unchanged'});continue
  A,B,C=v.printed(q[':question/problem']);AB=v.mul(A,B);BC=v.mul(B,C);R=v.mul(AB,C)
  assert R==v.mul(A,BC)
  seq=v.printed(q[':question/worked-solution']);left='product $AB$' in q[':question/worked-solution']
  expected=[A,B,AB,AB,C,R] if left else [B,C,BC,A,BC,R]
  if t=='q-320021':expected[2:2]=[AB,AB]
  if t=='q-319943':expected[2:2]=[BC]
  assert seq==expected,t
  out={':question/id':q[':question/id'],':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':q[':question/difficulty'][':db/ident'],':question/answer-fields':[]}
  checks=[]
  for i,f in enumerate(fs):
   c=f[':answer-field/correct'];a=[{':answer/id':a[':answer/id'],':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]
   out[':question/answer-fields'].append({':answer-field/id':f[':answer-field/id'],':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':a,':answer-field/correct':[':answer/id',c[':answer/id']]})
   if f[':answer-field/type'][':db/ident'].endswith('/radio'):
    assert v.printed(c[':answer/value'])==[R]
    assert sum(v.printed(x[':answer/value'])==[R] for x in a)==1
    for x in a:checks.append({'field_index':i,'submitted_answer_id':x[':answer/id'],'expected':'accepted' if x[':answer/id']==c[':answer/id'] else 'rejected','purpose':'Full source bank real selection grading'})
   else:
    cell=int(f[':answer-field/key'].split('-')[-1])-1
    assert c[':answer/value']==str(sum(R,[])[cell])
    for val,exp in [(c[':answer/value'],'accepted'),(c[':answer/value']+'+0','accepted'),(str(int(c[':answer/value'])+1),'rejected')]:checks.append({'field_index':i,'submitted':val,'expected':exp,'purpose':'Source blank grading'})
  records.append({'label':'source-'+t,'record':{'knowledge_point':{'title':v.g.S['record'][':knowledge-point/title']},'question':out,'generation':{'template':t}},'checks':checks})
  accepted.append({'source':t,'id':q[':db/id'],'difficulty':out[':question/difficulty'].split('/')[-1],'mathematical_fingerprint':v.g.fingerprint(q)})
 v.save('source-native-input.json',records)
 subprocess.run([str(HERE/'check-engine'),str(HERE/'source-native-input.json'),str(HERE/'source-native-report.json')],check=True)
 v.save('source-inventory-validation.json',{'basis':v.g.S['basis'],'accepted':accepted,'excluded':excluded,'source_question_count':len(v.g.SOURCES),'passed':True})
if __name__=='__main__':main()
