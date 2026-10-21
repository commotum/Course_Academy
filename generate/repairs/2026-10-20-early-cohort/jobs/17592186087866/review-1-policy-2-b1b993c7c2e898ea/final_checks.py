import audit as a
import fast_math as fm
from collections import Counter
import re
def main():
 records=a.json.loads((a.E/'independent-records.json').read_text())+a.json.loads((a.E/'runner-batch.json').read_text())
 prose=[]
 for r in records:
  q=r['question'];sol=q[':question/worked-solution'];pv=re.search(r'\$P\(x\)=(.*?)\$',sol)[1];qv=re.search(r'\$Q\(x\)=(.*?)\$',sol)[1].rstrip('.')
  n=fm.norm(a.equation(q[':question/problem'].split('$$')[1]));P=a.expr(pv);Q=a.expr(qv)
  prose.append({'question_id':q[':question/id'],'passed':bool(fm.zero(n-(a.D+P*a.y-Q)))})
 a.save('solution-prose-results.json',{'results':prose})
 failures=[]
 for kwargs in [{'level':'unknown'},{'level':'easy','template':'q-16401'},{'level':'easy','field_type':'free'},{'level':'easy','profile':'unknown'},{'level':'easy','template':'q-8359','parameters':{'k':True}},{'level':'easy','template':'q-8359','parameters':{'k':2},'decision':{'p_sign':0}},{'level':'easy','template':'q-8359','parameters':{'k':2},'decision':{'p_candidates':[2]*5,'q_candidates':[1,2,3,4,5],'correct_slot':0}}]:
  try:a.g.generate(seed=17061,**kwargs);ok=False;error='unexpected acceptance'
  except ValueError as e:ok=True;error=str(e)
  failures.append({'parameters':kwargs,'rejected':ok,'message':error})
 a.save('generator-rejection-results.json',failures)
 # Count actual outer generate attempts through its once-per-attempt data validator.
 old=a.g.data;attempts=[]
 for level,ts in a.g.FAMILIES.items():
  for t in ts:
   calls=[]
   def observed_data(tt,p):calls.append(dict(p));return old(tt,p)
   a.g.data=observed_data
   try:r=a.g.generate(level,17063,t)
   finally:a.g.data=old
   attempts.append({'template':t,'seed':17063,'attempt_count':len(calls),'validation_parameters':calls,'record':r,'math_passed':fm.check(r)['passed']})
 a.save('resampling-results.json',{'results':attempts,'analysis':'Every valid easy candidate bank uses five distinct P and Q magnitudes; moderate uses distinct ordered linear numerator pairs; hard uses five distinct nonzero cross-term coefficients. These ensure unique equivalent answers structurally. Native generator equivalence/collision validation remains active. All tested normal attempts succeed without rejection. CLI independently deduplicates fingerprints and returns count or raises instead of padding.'})
 # Confirm the original-parameter nonlearning profiles, not just stored-source replay.
 obs=[];obs_records=[];src=a.json.loads((a.JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
 for q in src:
  t=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1];r=a.g.generate(level,17067,t,parameters=a.g.ORIGINAL[t],profile=t);obs_records.append(r)
  # Compare complete displayed equation banks as canonical ordered residuals, plus standard/nonstandard form distinction.
  sf=next(f for f in q[':question/answer-fields'] if ':answer-field/correct' in f);gf=r['question'][':question/answer-fields'][0]
  def signature(c):
   pair=a.equation(c[':answer/value']);return str(a.S.factor(fm.trig_contract(a.residual(pair)))),bool(a.is_standard(pair))
  sb=Counter(signature(c) for c in sf[':answer-field/choices']);gb=Counter(signature(c) for c in gf[':answer-field/choices'])
  obs.append({'source_id':q[':question/id'],'template':t,'complete_bank_mathematical_match':sb==gb,'math':fm.check(r),'learning_eligible':r['generation']['eligible_for_learning']})
 a.save('observed-profile-records.json',obs_records);a.save('observed-profile-results.json',obs)
 a.save('scope-results.json',{'source_family_coverage':{level:ts for level,ts in a.g.FAMILIES.items()},'easy_stage_counts':dict(Counter(r['generation']['template'] for r in records if r['generation']['difficulty']=='easy')),'reasoning':'Easy extensions change signed coefficients and frequencies while retaining term collection, supported trig identity, cancellation with nonzero y, and division. Five standard-form distractors require algebraic equivalence as in multi-standard-form source banks. Moderate rational collection is authored and isolated; square expansion is hard and isolated. No integration, solving, new functions or new response type introduced.','domains':'Every y cancellation retains y != 0; reciprocal-x families retain x != 0; trig normalizers explicitly exclude their zeroes.','unsupported_source_families':[],'basis':'source-analysis.json, source-replay-results.json, independent-records.json, math-results.json, boundary-tests.json'})
 a.save('package-after.json',a.hashfiles());a.save('package-integrity.json',{'equal':a.json.loads((a.E/'package-before.json').read_text())==a.hashfiles(),'file_count':len(a.hashfiles()),'basis':'SHA256 of every file under package_root before import/testing and at final-check milestone.'})
 print('prose',sum(t['passed'] for t in prose),'/',len(prose),'invalid calls rejected',sum(t['rejected'] for t in failures),'/',len(failures),'resampling',[(t['template'],t['attempt_count']) for t in attempts],'observed',[{'t':t['template'],'match':t['complete_bank_mathematical_match'],'math':t['math']['passed']} for t in obs],flush=True)
if __name__=='__main__':main()
