import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from printed import check,check_source,scalar,values,task,fingerprint
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,default=str)+'\n')
def engine_item(rec):
 f=rec['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned radio choice'} for a in f[':answer-field/choices']]
 else:
  r=task(rec['question'])[3][0]
  checks=[{'submitted':z,'expected':'accepted','purpose':'Equivalent exact numeric blank'} for z in {sp.latex(r),str(r),str(2*r.p)+'/'+str(2*r.q)}]
  checks +=[{'submitted':str(r+1),'expected':'rejected','purpose':'Incorrect root'},{'submitted':str(-r),'expected':'rejected','purpose':'Incorrect root sign'}]
 return {'label':rec['question'][':question/id'],'record':rec,'checks':checks}
def grade(records,path):
 path=Path(path);path.mkdir(parents=True,exist_ok=True)
 (path/'native-input.json').write_text(json.dumps([engine_item(r) for r in records],indent=2))
 subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
 r=json.loads((path/'native-report.json').read_text());assert r['documented_unresolved_checks']==0;return r

def main():
 sources={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
 originals=[];replay=[];reviews=[];allrecords=[];coverage={}
 for profile,p in g.CASES.items():
  rec=g.generate(profile=profile,parameters=p);check(rec);orig=sources[g.PROFILES[profile][2]];f,m,roots,ans,family=task(orig)
  assert task(rec['question'])==(f,m,roots,ans,family)
  oldfield=orig[':question/answer-fields'][0];newfield=rec['question'][':question/answer-fields'][0]
  old=[values(a[':answer/value']) for a in oldfield[':answer-field/choices']];new=[values(a[':answer/value']) for a in newfield[':answer-field/choices']]
  assert len(old)==len(new) and set(old)==set(new)
  designated=oldfield.get(':answer-field/correct')
  if designated:assert values(designated[':answer/value'])==ans
  replay.append({'profile':profile,'source_id':g.PROFILES[profile][2],'matched_choices':len(old),'total_choices':len(old),'missing':[],'extra':[],'original_designation_matched':bool(designated),'absent_key_inferred_from_math':not bool(designated),'same_polynomial_slope_branch':True,'prompt_typography':'standardized; blank fragment and explicit field placeholders retained','solution_fidelity':'Derivative, equation, solve and branch stages retained; expanded power-rule row added to abbreviated cubic source; q-343737 final slope typo corrected only in local authored completion'})
  originals.append(rec)
  lines=['## Source '+g.PROFILES[profile][2],orig[':question/problem'],'Bank: '+', '.join(a[':answer/value'] for a in oldfield[':answer-field/choices']),orig.get(':question/worked-solution','No source solution.'),'### Completed replay',g.markdown(rec)]
  fps=set();paramvals={k:set() for k in 'abcdm'}
  for seed in range(200):
   r=g.generate(seed=seed,profile=profile);check(r);fps.add(r['generation']['mathematical_fingerprint'])
   for k,z in r['generation']['parameters'].items():paramvals[k].add(z)
   # Real grading every sampled supported bank, including equivalent blank input.
   allrecords.append(r)
  assert len(fps)>=(8 if profile=='cubic_repeated' else 20 if g.PROFILES[profile][0]!='quadratic' else 80),(profile,len(fps))
  assert all(len(paramvals[k])>1 for k in 'bcdm')
  coverage[profile]={'unique_math_tasks_in_200':len(fps),'slot_values':{k:sorted(v) for k,v in paramvals.items()}}
  for seed in (32,77):
   r=g.generate(seed=seed,profile=profile);reviews.append(r);lines+=['### Variant '+str(seed),g.markdown(r)]
  (HERE/(profile+'-review.md')).write_text('\n\n'.join(lines)+'\n')
 # Determinism, seed/bank-order independence and conservative duplicate detection.
 for rec in originals+reviews:
  meta=rec['generation'];r=g.generate(seed=meta['seed'],profile=meta['bank_profile'],parameters=meta['parameters']);assert r==rec
  other=g.generate(seed=meta['seed']+9,profile=meta['bank_profile'],parameters=meta['parameters']);assert other['question'][':question/id']==rec['question'][':question/id'];assert fingerprint(other['question'])==fingerprint(rec['question'])
  p=dict(meta['parameters']);p['d']=str(sp.Rational(p['d'])+1);shift=g.generate(profile=meta['bank_profile'],parameters=p);assert fingerprint(shift['question'])==fingerprint(rec['question'])
 for level in ('easy','hard'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported level accepted')
 bad=[('quadratic_radio',dict(a=0,b=0,c=2,d=1,m=1)),('cubic_positive_blank',dict(a=1,b=-3,c=7,d=0,m=1))]
 for profile,p in bad:
  try:g.generate(profile=profile,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid domain accepted')
 native=grade(originals+allrecords,HERE)
 save('source-replay.json',replay);save('review.json',reviews)
 save('validation.json',{'status':'passed','source_basis':g.SOURCE['basis'],'source_banks':len(replay),'matched_options':sum(r['matched_choices'] for r in replay),'total_options':sum(r['total_choices'] for r in replay),'matched_original_designations':sum(r['original_designation_matched'] for r in replay),'missing_original_designations':2,'missing_options':[],'extra_options':[],'source_context_exclusion':['q-128236'],'independent_displayed_math_records':len(allrecords)+len(originals),'coverage':coverage,'native':{k:native[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'fidelity':'Mathematical content and complete banks exact at original parameters; normal typography/layout extensions documented in source-replay. No exact source prose/whitespace claim. q-343737 conclusion slope typo corrected locally.'})
 files=[HERE.with_suffix('.py'),HERE/'source.json',HERE/'source.edn',HERE/'validate.py',HERE/'printed.py',HERE/'check-engine.rs',HERE/'check-engine']
 save('freeze-hashes.json',{'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}})
 print(json.dumps({'status':'passed','banks':len(replay),'variants':len(allrecords),'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')}}))
if __name__=='__main__':main()
