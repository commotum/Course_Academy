"""User-authorized authored key, retaining the original prompt and option bank."""
from pathlib import Path
import threading,uuid,hashlib,math,json
from decimal import Decimal,localcontext
from scripts.config import Config
from scripts.storage import atomic_json,file_lock,read_json
from scripts.database.client import EDBClient
from scripts.database.commit import Committer
from scripts.database.prepare import Plan,Snapshot,source_uuid,digest
from scripts.database.edn import kw,loads
from scripts.database.math_content import prose,value
ROOT=Path(__file__).resolve().parent
AUTHOR=':agent/codex'; MID='q-130051'
RAW=read_json(ROOT/'source-question.json')
QUESTION=source_uuid('question',MID)
FIELD=source_uuid('answer-field',str(QUESTION)+':'+digest(['selection','radio']))
CHOICES=[{'type':c['type'],'value':value(c['type'],c['value'])}for c in RAW['fields'][0]['choices']]
for c in CHOICES:c['uuid']=source_uuid('answer',str(FIELD)+':'+digest([c['type'],c['value']]))
assert len(CHOICES)==5 and len({c['value']for c in CHOICES})==5
CORRECT=next(c for c in CHOICES if c['value']=='0.0738')
SOLUTION=prose(r'''If $X\sim\operatorname{Po}(\lambda)$, then its probability mass function is

$$
f(x)=\frac{\lambda^x e^{-\lambda}}{x!}.
$$

Here $\lambda=1.1$, so

$$
f(x)=\frac{1.1^x e^{-1.1}}{x!}.
$$

Therefore,

$$
\begin{aligned}
P(X=3)&=f(3)\\
&=\frac{1.1^3e^{-1.1}}{3!}\\
&\approx 0.0738425664.
\end{aligned}
$$

Rounded to four decimal places, the answer is $0.0738$.
''')
SOLUTION_BEFORE_PRECISION_CHECK=SOLUTION
with localcontext()as ctx:
 ctx.prec=50
 probability=(-Decimal('1.1')).exp()*Decimal('1.1')**3/Decimal(6)
 SOLUTION=SOLUTION.replace('0.0738425664',format(probability,'.10f'))


def freeze_check():
 p=read_json(ROOT/'original-checkpoint-hash.json');assert hashlib.sha256(Path(p['file']).read_bytes()).hexdigest()==p['sha256']


def snapshot(client,directory,basis):
 data=client.snapshot({'questions':[RAW],'canonical_examples':[{'math_academy_id':'e-8465','topic_id':RAW['topic_id']}]},directory,basis)
 rows=client.query('[:find (pull ?a [*]) :in $ [?id ...] :where [?a :answer/id ?id]]',[[c['uuid']for c in CHOICES]],directory,'original-options',basis)
 known={e[':db/id']for e in data['entities']};extra=[r[0]for r in rows if r[0][':db/id']not in known];data['entities'].extend(extra)
 if extra:data['facts'].extend(client.query('[:find ?e ?a ?v ?s :in $ [?e ...] :where [?e ?a ?v _ ?s]]',[[e[':db/id']for e in extra]],directory,'option-provenance',basis))
 return data


def one(snap,attr,val):
 matches=snap.find(attr,val);assert len(matches)<=1;return matches[0]if matches else None


def prepare(phase,data):
 s=Snapshot(data);assert AUTHOR in s.idents
 p=Plan(s,source=AUTHOR if phase in ('02-authored-key','04-checked-approximation')else':org/Math-Academy')
 old=one(s,'question/math-academy-id',MID)
 if phase=='04-checked-approximation':
  assert old[':question/worked-solution']in(SOLUTION_BEFORE_PRECISION_CHECK,SOLUTION)
  p.set(old[':db/id'],old,'question/worked-solution',SOLUTION)
  return p.finish()
 if phase=='01-originals':
  assert old is None
  q=p.entity('question',QUESTION)
  p.set(q,None,'question/math-academy-id',MID);p.set(q,None,'question/problem',prose(RAW['problem']))
  for c in CHOICES:
   assert one(s,'answer/id',c['uuid'])is None
   a=p.entity('answer',c['uuid']);p.set(a,None,'answer/type',kw('answer.type/'+c['type']));p.set(a,None,'answer/value',c['value'])
 else:
  assert old and old[':question/id']==QUESTION and old[':question/problem']==prose(RAW['problem'])
  previous=(old.get(':question/answer-fields')or[None])[0]
  options=[one(s,'answer/id',c['uuid'])for c in CHOICES];assert all(options)
  correct=one(s,'answer/id',CORRECT['uuid'])
  f=p.entity('answer-field',FIELD,previous)
  if phase=='02-authored-key':
   assert previous is None and ':question/worked-solution'not in old
   p.set(f,None,'answer-field/correct',correct[':db/id'])
   p.set(old[':db/id'],old,'question/worked-solution',SOLUTION)
  else:
   assert phase=='03-original-controls'and previous and previous[':answer-field/id']==FIELD
   assert previous[':answer-field/correct'][':db/id']==correct[':db/id']
   example=one(s,'question/math-academy-id','e-8465');owners=example[':knowledge-point/_canonical-example'];assert len(owners)==1
   point=s.entities[owners[0][':db/id']]
   p.set(point[':db/id'],point,'knowledge-point/questions',[old[':db/id']],many=True)
  p.set(f,previous,'answer-field/key','selection');p.set(f,previous,'answer-field/type',kw('answer-field.type/radio'))
  p.set(f,previous,'answer-field/choices',[a[':db/id']for a in options],many=True)
  p.set(old[':db/id'],old,'question/answer-fields',[f],many=True)
 return p.finish()


def run_phase(c,client,phase):
 folder=ROOT/phase;committer=Committer(c,client,folder);request=committer.pending()
 done=read_json(folder/'verification.json',{})
 if not request and done.get('status')=='verified':return done
 if request:assert request['content_sha256']==digest([RAW,SOLUTION,phase])
 else:
  data=snapshot(client,folder/'before',client.basis());batch=prepare(phase,data)
  committer.preview(batch,data);request=committer.save_request(batch,data,digest([RAW,SOLUTION,phase]))
 receipt=committer.submit(request);proof=committer.verify_receipt(request,receipt)
 after=receipt[':edb/db-after-t'];data=snapshot(client,folder/'after',after);s=Snapshot(data)
 batch=loads(request['batch_edn']);temp=receipt.get(':edb/tempids',{});types={str(r[1]):str(r[2])for r in data['attributes']}
 def resolve(v):return temp.get(v,s.idents.get(str(v),v))if isinstance(v,str)else v
 for e,a,v in batch['assertions']:
  assert s.sourced(resolve(e),str(a).lstrip(':'),resolve(v)if types[str(a)]==':db.type/ref'else v,batch['source']),(e,a,v)
 result={'status':'verified','basis_before':request['basis'],'basis_after':after,'receipt':proof}
 atomic_json(folder/'verification.json',result);committer.retire(request,'verified',result);print(phase,result,flush=True);return result


def main():
 freeze_check()
 with localcontext()as ctx:
  ctx.prec=50;exact=(-Decimal('1.1')).exp()*Decimal('1.1')**3/Decimal(6)
  assert exact.quantize(Decimal('0.0001'))==Decimal('0.0738')
  assert abs(float(exact)-math.exp(-1.1)*1.1**3/math.factorial(3))<1e-16
  atomic_json(ROOT/'mathematical-evidence.json',{'lambda':'1.1','x':3,'computed_probability':str(exact),'rounded_answer':'0.0738','answer_source':AUTHOR,'template_source':'e-8465; context/questions.edn','template':'Poisson PMF, substitute lambda, evaluate at x, round to four decimal places.','nearby_verified_questions':['q-130048','q-130050'],'all_original_choices':[c['value']for c in CHOICES]})
 c=Config();client=EDBClient(c,threading.Event())
 with file_lock(c.database_lock):
  phases=[run_phase(c,client,p)for p in ('01-originals','02-authored-key','03-original-controls','04-checked-approximation')]
  basis=phases[-1]['basis_after'];data=snapshot(client,ROOT/'final',basis);s=Snapshot(data)
  q=one(s,'question/math-academy-id',MID);f,=q[':question/answer-fields'];answer=f[':answer-field/correct']
  assert q[':question/worked-solution']==SOLUTION and answer[':answer/value']=='0.0738'
  assert len(f[':answer-field/choices'])==5
  for attr,v in [('answer-field/correct',answer)]:
   assert s.sourced(f[':db/id'],attr,v,AUTHOR)and not s.sourced(f[':db/id'],attr,v,':org/Math-Academy')
  assert s.sourced(q[':db/id'],'question/worked-solution',SOLUTION,AUTHOR)
  assert not s.sourced(q[':db/id'],'question/worked-solution',SOLUTION,':org/Math-Academy')
  assert s.sourced(q[':db/id'],'question/problem',prose(RAW['problem']),':org/Math-Academy')
  for c0 in CHOICES:
   a=one(s,'answer/id',c0['uuid']);assert s.sourced(a[':db/id'],'answer/value',c0['value'],':org/Math-Academy')
  assert not prepare('03-original-controls',data)['forms']
  freeze_check()
  result={'status':'verified','basis':basis,'question_id':MID,'question_eid':q[':db/id'],'field_eid':f[':db/id'],'correct_answer_eid':answer[':db/id'],'correct_answer':'0.0738','correct_key_source':AUTHOR,'worked_solution_source':AUTHOR,'prompt_and_option_text_source':':org/Math-Academy','original_choices':5,'checkpoint_unchanged':True,'learner_facts_unchanged':True,'repeat_original_controls_noop':True,'phases':phases}
  atomic_json(ROOT/'verification.json',result);print(json.dumps(result))

if __name__=='__main__':main()
