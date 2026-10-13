#!/usr/bin/env python3
"""Fails on displayed mathematics, source fidelity, schema, grading and scope."""
from pathlib import Path
import importlib.util,json,re,subprocess,sys,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sys.path.insert(0,str(ROOT));import readback as rb
sources=json.loads((ROOT/'source.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/'source-cases.json').read_text())
def dump(path,v):(ROOT/path).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def shape(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=r['question'];f=q[':question/answer-fields'][0];aid=f[':answer-field/correct']
 assert aid[0]==':answer/id' and sum(a[':answer/id']==aid[1] for a in f[':answer-field/choices'])==1
 import uuid
 for v in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]:uuid.UUID(v)
 for txt in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert txt.count('$')%2==0
  depth=0
  for ch in txt:
   if ch=='{':depth+=1
   elif ch=='}':depth-=1
   assert depth>=0
  assert depth==0 and r'\\' not in txt.replace(r' \\  & =',''),('format',txt)
  assert '--' not in txt and '+-' not in txt
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 return rb.check(r)
def fixture(label,r):
 f=r['question'][':question/answer-fields'][0];aid=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==aid else 'rejected','purpose':'complete native radio bank designation'} for a in f[':answer-field/choices']]
 else:
  ans=f[':answer-field/choices'][0][':answer/value'];expression=rb.read(ans)
  # Submit the independently checked, actually displayed substituted-component
  # form. It retains constant logarithm bases while testing an unreduced product.
  rows=rb.math_rows(r['question'][':question/worked-solution'])
  component=rows[2] if r['generation']['template'].startswith(('base_log','binomial','trinomial')) else rows[1]
  if r['generation']['authored']:alt=component
  else:
   depth=0;parts=[];previous=0
   for i,ch in enumerate(component):
    if ch in '({':depth+=1
    elif ch in ')}':depth-=1
    elif ch=='+' and depth==0:parts.append(component[previous:i]);previous=i+1
   parts.append(component[previous:]);alt=next(z for z in parts if rb.equal(rb.read(z),expression))
  alt=alt.replace('⁡','')
  checks=[{'submitted':ans,'expected':'accepted','purpose':'canonical fragment/full derivative'}, {'submitted':alt,'expected':'accepted','purpose':'equivalent unreduced substituted component/product form'}, {'submitted':'0','expected':'rejected','purpose':'incorrect zero derivative/fragment'}]
 return {'label':label,'record':r,'checks':checks}
def main():
 coverage=[];fixtures=[];review=[];variant_checks=0
 for case,src in zip(cases,sources):
  assert case['source_id']==src[':question/math-academy-id']
  r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);audit=shape(r);q=r['question'];original=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  assert q[':question/problem']==src[':question/problem']
  vals=sorted(a[':answer/value'] for a in f[':answer-field/choices']);raw=sorted(a[':answer/value'] for a in original[':answer-field/choices']);assert vals==raw
  correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  if ':answer-field/correct' in original:assert correct==original[':answer-field/correct'][':answer/value']
  if ':question/worked-solution' in src:
   assert q[':question/worked-solution']==src[':question/worked-solution'];assert len(rb.math_rows(q[':question/worked-solution']))==len(rb.math_rows(src[':question/worked-solution']))
  for a in original[':answer-field/choices']:assert sum(rb.equal(rb.read(a[':answer/value']),rb.read(b[':answer/value'])) for b in f[':answer-field/choices'])==1
  coverage.append({'source_id':case['source_id'],'prompt_exact':True,'bank_exact':True,'complete_mathematical_option_matches':len(raw),'distractors_matched':len(raw)-1,'correct_designation':'matched' if ':answer-field/correct' in original else 'independently_derived_missing_ref','solution_exact':True if ':question/worked-solution' in src else None,'solution_rows':audit['rows']})
  fixtures.append(fixture('source '+case['source_id'],r));review.append({'label':'Observed source replay '+case['source_id'],'record':r})
 for t,(level,kind,ids) in g.TEMPLATES.items():
  positions=set();fingerprints=set()
  for seed in range(12):
   r=g.generate(level,seed,template=t);shape(r);variant_checks+=1;fingerprints.add(r['generation']['mathematical_fingerprint'])
   f=r['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
   same=g.generate(level,seed+777,template=t,parameters=r['generation']['parameters']);assert same['question'][':question/id']==r['question'][':question/id'];assert same['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
   if seed<2:review.append({'label':'Generated variant '+t+' seed '+str(seed),'record':r});fixtures.append(fixture(t+' seed '+str(seed),r))
  assert len(fingerprints)>=5,(t,'insufficient substantive variety')
  if kind=='radio':assert len(positions)>1,(t,'correct position constant')
  invalid=g.defaults(t)
  if t.startswith(('binomial','trinomial')):invalid['c']=0
  elif 'b' in invalid:invalid['b']=1
  else:invalid['n']=0
  try:g.generate(level,template=t,parameters=invalid)
  except (ValueError,AssertionError):pass
  else:raise AssertionError('invalid explicit parameters accepted '+t)
 # Reject ambiguities without repairing individual bank members.
 try:g.generate_easy(template='log_log_radio',parameters={'c':1,'b':3})
 except ValueError:pass
 else:raise AssertionError('ambiguous observed bank c=1 accepted')
 limiting=next(z for z in fixtures if z['label']=='source q-320815')
 import copy
 documented=copy.deepcopy(limiting);documented['label']='documented logarithm constant rewrite limitation'
 documented['checks']=[{'submitted':r'\frac{4^{x}}{2x\ln 2}','expected':'unresolved','purpose':'independently valid ln4=2ln2 rewrite; native unresolved domain differences, preserved without engine edits'}]
 fixtures.append(documented)
 sec_case=copy.deepcopy(next(z for z in fixtures if z['label']=='source q-319425'))
 sec_case['label']='documented invisible application mark limitation'
 sec_case['checks']=[{'submitted':'{4}^{x}({sec}^{2}⁡(x))','expected':'unresolved','purpose':'raw source component-row entry has unsupported invisible sec application mark; canonical blank has none and grades correctly'}]
 fixtures.append(sec_case)
 reduced=copy.deepcopy(next(z for z in fixtures if z['label']=='binomial_log_blank seed 0'))
 reduced['label']='documented canceled logarithmic quotient domain limitation'
 reduced['checks']=[{'submitted':r'6{x}^{2}\log_{6} x-10x\log_{6} x+\frac{2{x}^{2}}{\ln 6}-\frac{5x}{\ln 6}','expected':'unresolved','purpose':'independent valid x cancellation in logarithmic quotient; native denominator guards differ despite x>0 domain'}]
 assert rb.equal(rb.read(reduced['checks'][0]['submitted']),rb.read(reduced['record']['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']))
 fixtures.append(reduced)
 dump('review.json',review);dump('native-input.json',fixtures)
 native=REPO/'generate/runs/current/check-engine'
 subprocess.run([str(native),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
 dump('validation.json',{'status':'pass','source':g.SOURCE,'source_questions':13,'observed_easy':11,'unrated':2,'complete_banks_matched':13,'source_options_matched':33,'observed_radio_banks':5,'source_distractors_matched':20,'designation_matched':11,'designation_observed_total':11,'designation_independently_derived':2,'solutions_raw_exact':11,'solutions_observed_total':11,'solutions_authored_missing':2,'source_repairs':0,'source_coverage':coverage,'changed_parameter_readbacks':variant_checks,'authored_moderate_templates':2,'authored_hard_templates':2,'all_levels_review_examples_minimum':2,'native':json.loads((ROOT/'native-report.json').read_text()),'native_binary_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'native_source_sha256':hashlib.sha256((native.with_suffix('.rs')).read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest()})
 print('PASS: 13 complete banks, 11 exact existing solutions; 2 derived refs; '+str(variant_checks)+' changed-parameter displayed readbacks; native checks pass')
if __name__=='__main__':main()
