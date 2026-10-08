import sys,json,copy,hashlib,shutil
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'scripts/question_capture'))
from capture import arguments
from database import Database,StaleBasis
from core import stable_id,atomic_json
from edn import dumps,loads,kw
p=Path('reference/mathacademy/question-capture-workers/differential/14039776').resolve()
r=Path('reference/mathacademy/mathematical-corrections/q-128452').resolve();r.mkdir(exist_ok=True)
args=arguments(['import-saved','--content',str(p/'content.json'),'--state-dir','.local/question_capture-workers/differential','--output','reference/mathacademy/question-capture-workers/differential','--capture-root','reference/mathacademy/question-capture-workers/linear','--capture-root','reference/mathacademy/question-capture-workers/multivariable'])
db=Database(args);content=json.loads((p/'content.json').read_text());original=next(q for q in content['questions'] if q['math_academy_id']=='q-128452');corrected=copy.deepcopy(original)
needle=r'\operatorname{ln}⁡(2t)';assert needle in original['problem'];corrected['problem']=original['problem'].replace(needle,r'\ln|2t|')
corrected['worked_solution']=r'''Since $t=-1$ lies in an open interval where $t<0$ and $3-t>0$, all components are differentiable there. In particular, $\ln|2t|=\ln(-2t)$ near $t=-1$, so its derivative is $1/t$.

Differentiate each vector component:

$$
\mathbf f'(t)=\left\langle-\frac{4}{\sqrt{3-t}},\pi\cos(\pi t),\frac1t\right\rangle,
\qquad
\mathbf g'(t)=\langle 2t-1,2\pi t,-2t\rangle.
$$

The sum and constant multiple rules give

$$
(2\mathbf f-\mathbf g)'(t)=2\mathbf f'(t)-\mathbf g'(t).
$$

At $t=-1$,

$$
\mathbf f'(-1)=\langle-2,-\pi,-1\rangle,
\qquad
\mathbf g'(-1)=\langle-3,-2\pi,2\rangle.
$$

Therefore,

$$
(2\mathbf f-\mathbf g)'(-1)
=2\langle-2,-\pi,-1\rangle-\langle-3,-2\pi,2\rangle
=\boxed{\langle-1,0,-4\rangle}.
$$'''
corrected['worked_solution']=corrected['worked_solution'].replace(chr(92)*2,chr(92))
corrected['answer_fields'][0]['correct_origin']='reviewed_mathematical_correction'
check=json.loads((p/'manual-recovery/mathematical-check.json').read_text());assert check['passed']
review={'question':'q-128452','source_capture':str(p),'original_content':original,'corrected_content':corrected,'rationale':'The original real-valued function uses ln(2t), undefined at the requested t=-1. Its derivative there therefore does not exist. The site accepts its formal derivative <-1,0,-4>. The explicitly authorized local repair replaces ln(2t) by ln|2t|, making that result valid on a neighborhood of -1. Original DOM, screenshot, uncertain solver result and accepted server answer remain preserved. New field and answer identities retain original historical definitions.','mathematical_check':check}
atomic_json(r/'review.json',review)
for attempt in range(3):
 basis=db.basis();before=db.questions(['q-128452'],r,'before',basis)['q-128452'];attrs=db.attributes(r,basis)
 qid=before[':db/id'];fields=before[':question/answer-fields'];assert len(fields)==1
 old=fields[0]; assert old[':answer-field/key']=='selection';prefix='q-128452/mathematical-correction-v1/selection'
 tx=[[kw('db/retract'),qid,kw('question/answer-fields'),old[':db/id']]];newchoices=[];correct=None
 for n,a in enumerate(old[':answer-field/choices']):
  token=prefix+'/answer-'+str(n);newchoices.append(token)
  arow={kw('db/id'):token,kw('answer/id'):stable_id('answer',token),kw('answer/type'):a[':answer/type'][':db/ident'],kw('answer/value'):a[':answer/value'],kw('db/ensure'):[kw('answer/validate')]}
  if ':answer/feedback' in a:arow[kw('answer/feedback')]=a[':answer/feedback']
  tx.append(arow)
  if a[':db/id']==old[':answer-field/correct'][':db/id']:correct=token
 assert correct and old[':answer-field/correct'][':answer/value']==corrected['answer_fields'][0]['correct_value']
 tx.extend([{kw('db/id'):prefix,kw('answer-field/id'):stable_id('field',prefix),kw('answer-field/key'):'selection',kw('answer-field/type'):old[':answer-field/type'][':db/ident'],kw('answer-field/choices'):newchoices,kw('answer-field/correct'):correct,kw('db/ensure'):[kw('answer-field/validate')]},{kw('db/id'):qid,kw('question/problem'):corrected['problem'],kw('question/worked-solution'):corrected['worked_solution'],kw('question/answer-fields'):[prefix],kw('db/ensure'):[kw('question/validate')]}])
 retractions=[[qid,kw('question/answer-fields'),old[':db/id']],[qid,kw('question/problem'),before[':question/problem']],[qid,kw('question/worked-solution'),before[':question/worked-solution']]]
 immutable_answers=[a[':db/id'] for a in old[':answer-field/choices']];immutable_fields=[(old[':db/id'],kw(a)) for a in ['answer-field/id','answer-field/key','answer-field/type','answer-field/correct']]
 (r/'guards.edn').write_text(dumps({'retractions':retractions,'immutable_answers':immutable_answers,'immutable_fields':immutable_fields}))
 (r/'transaction.edn').write_text(dumps(tx)+'\n');preview_text=db.command('with','--file',r/'transaction.edn');(r/'preview.edn').write_text(preview_text);preview=loads(preview_text)
 if preview[':edb/db-before-t']!=basis:continue
 db.validate_datoms(preview,attrs,retractions,immutable_answers,immutable_fields)
 digest=hashlib.sha256((r/'transaction.edn').read_bytes()).hexdigest();intent={'database':args.database,'endpoint':args.endpoint,'basis':basis,'sha256':digest,'request_key':f'ma-mathematical-correction-q-128452-{basis}-{digest}'};atomic_json(r/'commit-intent.json',intent)
 try:receipt=db._commit(intent,r/'transaction.edn',r);break
 except StaleBasis:
  if attempt==2:raise
else:raise RuntimeError('could not commit correction')
afterbasis=receipt[':edb/db-after-t'];db.validate_datoms(receipt,attrs,retractions,immutable_answers,immutable_fields)
after=db.questions(['q-128452'],r,'after',afterbasis)['q-128452'];newfield=after[':question/answer-fields'][0]
assert after[':question/problem']==corrected['problem'] and after[':question/worked-solution']==corrected['worked_solution']
assert newfield[':answer-field/correct'][':answer/value']==corrected['answer_fields'][0]['correct_value']
assert newfield[':db/id']!=old[':db/id'] and newfield[':answer-field/id']!=old[':answer-field/id']
assert not (set(a[':db/id'] for a in newfield[':answer-field/choices']) & set(immutable_answers))
retained=db.query('[:find (pull ?f [* {:answer-field/type [:db/ident]} {:answer-field/choices [* {:answer/type [:db/ident]}]} {:answer-field/correct [* {:answer/type [:db/ident]}]}]) :in $ ?f :where [?f :answer-field/id _]]',[old[':db/id']],r,'retained-original-field',afterbasis)
assert retained[0][0]==old
historic=db.questions(['q-128452'],r,'historical-original',basis)['q-128452'];assert historic==before
retention=db.query('[:find ?ident :in $ [?ident ...] :where [?a :db/ident ?ident] [?a :db/noHistory true]]',[[kw('question/problem'),kw('question/worked-solution'),kw('question/answer-fields')]],r,'history-retention',afterbasis);assert not retention
proof={'committed':True,'basis_before':basis,'basis_after':afterbasis,'mathematical_check_passed':True,'original_field_and_answer_retained':True,'historical_original_question_retained':True,'learner_and_engine_facts_unchanged':True,'verification_method':'committed_content_datoms_and_exact_question_readback','review_sha256':hashlib.sha256((r/'review.json').read_bytes()).hexdigest(),'transaction_sha256':digest,'correct_answer':newfield[':answer-field/correct'][':answer/value']}
atomic_json(r/'verification.json',proof)
# The registered correction must make the unchanged original-source reimport a no-op.
noop=db.import_content(content,r/'source-reimport-noop',apply=False);atomic_json(r/'source-reimport-noop.json',noop)
assert noop.get('already_complete') and noop.get('database_writes')==0,noop
proof['original_source_reimport_is_noop']=True;atomic_json(r/'verification.json',proof)
print(json.dumps(proof,indent=2))
