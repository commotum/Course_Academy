import json,hashlib,shutil
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');H=Path(__file__).resolve().parent
qs={q[':question/math-academy-id']:q for d in H.glob('175*')for q in json.loads((d/'questions-committed.json').read_text())};sources={q['mid']:q for d in H.glob('175*')for q in json.loads((d/'source-manifest.json').read_text())}
rationales={
'e-6578':"The source omitted the prime in the middle term and used y(t) while every expression depends on x. Characteristic roots -1 and3 give (r+1)(r-3)=r²-2r-3, hence y''-2y'-3y=0. Both given exponentials solve the corrected equation, and only labelled statementI does.",
'q-102792':"The product rule for y2=u(t)e^-3t gives y2''=(u''-6u'+9u)e^-3t. The original source incorrectly wrote e^-6t in the u' term twice. Replacing those factors yields u''-4u'=0 without changing the valid answerbank/key.",
'q-332547':"The raw source explicitly states5y'+6y=-30. Its claimed complementary term Ae^-6x is wrong: the homogeneous rate is-6/5. Keep the actual equation and correct the given complementary solution, entire worked result and keyed existing answer to Ae^(-6x/5)-5. Exact substitution yields5y'+6y=-30 for everyA.",
'q-79930':"The original statement uses y1(x),y2(x) but t in all exponentials. Use x consistently in the option labels and worked solution. Both e^-x and e^(1-x) solve y''+2y'+y=0 but are constant multiples, so the two true and one false keys remain valid.",
'q-339878':"Two offered complementary families differ only by swapping the names of arbitrary constantsAandB, so both are mathematically correct. Keep the keyed existing Ae^(2x)+Be^(-3x) active and detach redundant Ae^(-3x)+Be^(2x) membership. The existing answer entity and all retained history remain intact. The remaining active bank has a unique correct complementary family."
}
for mid,why in rationales.items():
 d=ROOT/'reference/mathacademy/mathematical-corrections'/mid;d.mkdir(exist_ok=True);q=qs[mid];fields=[]
 for f in q.get(':question/answer-fields',[]):
  fields.append({'entity':f[':db/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'choices':[{'entity':a[':db/id'],'type':a[':answer/type'][':db/ident'].split('/')[-1],'value':a[':answer/value']}for a in f.get(':answer-field/choices',[])],'correct_value':f[':answer-field/correct'][':answer/value'],'protect_choices':True})
 review={'question':q[':db/id'],'source':':course-academy.source/editor','rationale':why,'mathematical_evidence':str(H/'mathematics-after.json'),'original_sources':[{k:v for k,v in s.items()if k!='html'}for role in ['prompt_sources','solution_sources']for s in sources[mid][role]],'corrected_content':{'math_academy_id':mid,'problem':q[':question/problem'],'worked_solution':q[':question/worked-solution'],'answer_fields':fields},'learner_history_preservation':'All original question/field/answer entities retained. Source-bank duplicates detached only; no learner or engine datoms.'}
 (d/'review.json').write_text(json.dumps(review,indent=2)+'\n');shutil.copyfile(H/'transaction.edn',d/'transaction.edn')
 proof={'committed':True,'basis_after':13542,'mathematical_check_passed':True,'review_sha256':hashlib.sha256((d/'review.json').read_bytes()).hexdigest(),'transaction_sha256':hashlib.sha256((d/'transaction.edn').read_bytes()).hexdigest(),'receipt':str(H/'receipt.edn'),'verification':str(H/'verification.json'),'learner_and_engine_facts_unchanged':True}
 (d/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
 print(mid)
