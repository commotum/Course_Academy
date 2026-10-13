"""Independent printed mathematics, whole-profile replay and actual grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
import math_parser as p
spec=importlib.util.spec_from_file_location('repeated_chain',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=p.s

def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def check(rec):
 q=rec['question'];meta=rec['generation'];t=meta['template'];a=meta['parameters']['a']
 assert rec['knowledge_point']['db_id']==g.KP_ID
 assert q==g.generate(q[':question/difficulty'].split('/')[-1],999,t,{'a':a})['question']
 f,point=p.given(q[':question/problem']);der=s.diff(f,p.x);expected=der if point is None else der.subs(p.x,point)
 field=q[':question/answer-fields'][0];bank=field[':answer-field/choices'];values=[p.scalar(b[':answer/value']) for b in bank]
 # Partial response shape belongs to source; interpret the printed surrounding math.
 if t=='q-312907':
  assert '{{field-1}}' in q[':question/problem']
  suffix=q[':question/problem'].split('{{field-1}}',1)[1].strip().strip('$')
  full=[v*p.scalar(suffix) for v in values]
 elif t=='q-342927':
  assert '{{field-1}}' in q[':question/problem'] and '| --- | --- | --- |' in q[':question/problem']
  denominator=re.search(r'\$([^$]+)\$ \|\s*$',q[':question/problem'])[1]
  full=[v/p.scalar(denominator) for v in values]
 else:full=values
 assert sum(p.equal(v,expected) for v in full)==1,('Ambiguous bank',t,a)
 ci=field[':answer-field/correct'][1];good=next(v for b,v in zip(bank,full) if b[':answer/id']==ci)
 assert p.equal(good,expected),('Incorrect key',t,a,good,expected)
 assert not any(p.equal(v,w) for i,v in enumerate(values) for w in values[:i]),('Duplicate options',t,a)
 assert p.equal(p.solution_final(q[':question/worked-solution']),expected)
 stages=p.solution_stages(q[':question/worked-solution'],q[':question/problem'])
 assert meta['mathematical_fingerprint']==g.fingerprint(q)
 assert not ':question/math-academy-id' in q
 return stages

def native(label,r):
 f=r['question'][':question/answer-fields'][0];ci=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ci else 'rejected','purpose':'Every whole-bank option'} for a in f[':answer-field/choices']]
 else:
  a=f[':answer-field/choices'][0][':answer/value']
  checks=[{'submitted':c,'expected':e,'purpose':purpose} for c,e,purpose in [(a,'accepted','Canonical'),('('+a+')+0','accepted','Equivalent'),('('+a+')/1','accepted','Equivalent quotient'),('('+a+')+1','rejected','Incorrect'),('('+a+')-1','rejected','Incorrect')]]
 return {'label':label,'record':r,'checks':checks}

def main():
 records=[];inputs=[];replays=[];review=[];stages=0;fps=set();counts={};components=[]
 for t,(lv,a) in g.DATA.items():
  print('Replay',t,flush=True)
  old=g.sources()[t];r=g.generate(lv,0,t,{'a':a});stages+=check(r);q=r['question'];of=old[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem']
  assert [b[':answer/value'] for b in f[':answer-field/choices']]==[b[':answer/value'] for b in of[':answer-field/choices']]
  if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution']
  if of.get(':answer-field/correct'):assert next(b[':answer/value'] for b in f[':answer-field/choices'] if b[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  replays.append({'source':t,'level':lv,'difficulty_authored':lv=='easy','complete_bank_matched':True,'matched_values':len(f[':answer-field/choices']),'matched_distractors':len(f[':answer-field/choices'])-1,'missing_extra':[],'solution_exact':bool(old.get(':question/worked-solution')),'solution_authored':not bool(old.get(':question/worked-solution')),'key_inferred':not bool(of.get(':answer-field/correct'))})
  # Every original option retained alongside its parameterized observed recipe.
  components.append({'source':t,'prompt':old[':question/problem'],'solution':old.get(':question/worked-solution'),'original_parameter':a,'profile':t if len(f[':answer-field/choices'])>1 else None,'choices':[{'original':b[':answer/value'],'field':of[':answer-field/key'],'recipe':g.transport(t,b[':answer/value'],s.Symbol('a')),'mapping':g.transport(t,b[':answer/value'],a),'correct':b[':answer/id']==of.get(':answer-field/correct',{}).get(':answer/id'),'interpretation':'Observed expression transport; intent not assumed'} for b in of[':answer-field/choices']]})
  inputs.append(native('source-'+t,r))
  if t!='q-28655':review.append({'source':old,'variant':g.generate(lv,0,t,{'a':2 if a!=2 else 3})})
 for lv in ('easy','moderate','hard'):
  print('Candidates',lv,flush=True)
  counts[lv]=0
  for t,pa in g.candidates(lv):
   r=g.generate(lv,1959,t,pa);stages+=check(r);fp=g.fingerprint(r['question']);assert fp not in fps;fps.add(fp)
   assert r['question']==g.generate(lv,0,t,pa)['question'],'Seed changed content'
   records.append(r);counts[lv]+=1;inputs.append(native(t+str(pa),r))
  try:g.batch(lv,counts[lv]+1)
  except ValueError:pass
  else:raise AssertionError('Finite limit ignored')
 for t,pa in [('q-48569',{'a':1}),('q-28655',{'a':6}),('q-31352',{'a':0}),('q-2397',{'a':True})]:
  try:g.generate(g.DATA[t][0],0,t,pa)
  except ValueError:pass
  else:raise AssertionError('Guard failed')
 fieldless=g.sources()['q-16699'];f,pt=p.given(fieldless[':question/problem']);assert p.equal(p.solution_final(fieldless[':question/worked-solution']),s.diff(f,p.x).subs(p.x,pt));stages+=p.solution_stages(fieldless[':question/worked-solution'],fieldless[':question/problem'])
 components.append({'source':'q-16699','prompt':fieldless[':question/problem'],'solution':fieldless[':question/worked-solution'],'field_missing':True,'excluded_from_grading':True,'printed_math_validated':True})
 save('source-replay.json',{'passed':True,'sources':replays,'complete_banks_matched':len(replays),'complete_banks_total':len(replays),'matched_values':sum(x['matched_values'] for x in replays),'matched_distractors':sum(x['matched_distractors'] for x in replays),'excluded_fieldless_source':'q-16699'})
 save('source-components.json',components);save('previews.json',records);save('native-input.json',inputs);save('review.json',review)
 (HERE/'review.md').write_text('\n\n'.join('## '+r['variant']['generation']['template']+'\n\nOriginal:\n\n'+r['source'][':question/problem']+'\n\n'+r['source'].get(':question/worked-solution','[No source solution]')+'\n\nVariant:\n\n'+g.markdown(r['variant']) for r in review))
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 files=[HERE.with_suffix('.py'),HERE/'source.json',HERE/'source.edn',HERE/'validate.py',HERE/'math_parser.py',HERE/'replenish.py',HERE/'db_support.py',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine.rs',ROOT/'generate/runs/current/check-engine']
 save('validation.json',{'passed':True,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'counts':counts,'source_banks':len(replays),'source_values':sum(x['matched_values'] for x in replays),'source_distractors':sum(x['matched_distractors'] for x in replays),'printed_solution_equalities':stages,'source_questions_analyzed':9,'distinctness_method':'Parsed function and point identities; complete banks checked for stable nonzero witnesses at rational arguments with 80/120-digit agreement; all correct derivative and solution equalities reduce symbolically to zero.','correctness':'Independent parser for printed functions, every choice, partial blank surrounding factors, derivative composition, component derivatives, product/substitution/evaluation solution rows and final values.','grading':'Real learning::grade_field; all source replays and every bounded variant, all options plus canonical/equivalent/wrong blank entries.','hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}})
 print(json.dumps({'validated':counts,'banks':len(replays),'stages':stages}),flush=True)
if __name__=='__main__':main()
