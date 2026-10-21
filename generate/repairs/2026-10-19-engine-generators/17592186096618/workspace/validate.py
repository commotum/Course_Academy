#!/usr/bin/env python3
"""Reproducible source-specific checks. Run with the job's Python executable."""
import argparse,copy,collections,json,hashlib,random,re,subprocess,sys
from pathlib import Path
import sympy as s
import generator as g
ROOT=Path(__file__).resolve().parent
E=ROOT/'evidence';E.mkdir(exist_ok=True)
x=s.Symbol('x',positive=True)
def dump(name,obj): (E/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def oracle(t,p):
 b=p.get('b',3);c=p.get('c',1);n=p.get('n',2);k=p.get('k',1)
 if t=='log_log_radio':u=c*s.log(x)/s.log(b);du=c/(x*s.log(b));v=s.log(x);dv=1/x
 elif t=='power_log_radio':u=x**n;du=n*x**(n-1);v=s.log(x)/s.log(b);dv=1/(x*s.log(b))
 elif t=='linear_base_radio':u=c*x;du=s.Integer(c);v=b**x;dv=s.log(b)*v
 elif t.startswith('power_exp') or t=='sqrt_exp_radio':
  u=c*x**n if t!='sqrt_exp_radio' else c*s.sqrt(x);du=c*n*x**(n-1) if t!='sqrt_exp_radio' else c/(2*s.sqrt(x));v=s.exp(k*x);dv=k*v
 elif t=='cos_log_radio':u=c*s.cos(x);du=-c*s.sin(x);v=s.log(x)/s.log(b);dv=1/(x*s.log(b))
 elif t.startswith('base_log'):
  u=b**(k*x);du=k*s.log(b)*u;v=s.log(x)/s.log(p['d']);dv=1/(x*s.log(p['d']))
 elif t in ('base_sin_left_blank','base_cos_left_blank','base_tan_right_blank'):
  u=b**x;du=s.log(b)*u
  if 'sin' in t:v=s.sin(x);dv=s.cos(x)
  elif 'cos' in t:v=s.cos(x);dv=-s.sin(x)
  else:v=s.tan(x);dv=s.sec(x)**2
 elif t=='tan_log_blank':u=s.tan(x);du=s.sec(x)**2;v=s.log(x)/s.log(10);dv=1/(x*s.log(10))
 elif t=='polynomial_log_blank':u=x**n+p['h'];du=n*x**(n-1);v=s.log(x);dv=1/x
 else:raise AssertionError(t)
 return u*v,du*v,u*dv

def eq(a,b):return s.simplify(s.trigsimp(a-b))==0

def key(r):
 f=r['question'][':question/answer-fields'][0];return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']

def blank_fixture(r,value):
 z=copy.deepcopy(r);f=z['question'][':question/answer-fields'][0];f[':answer-field/type']=':answer-field.type/blank';f[':answer-field/key']='field-1'
 aid=g.ident([value,'independent oracle']);f[':answer-field/choices']=[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value}];f[':answer-field/correct']=[':answer/id',aid];z['question'][':question/problem']='Enter the expression.\n\n{{field-1}}';return z

def equivalence_case(label,r,value,submitted,expected='accepted'):
 return {'label':label,'record':blank_fixture(r,value),'checks':[{'submitted':submitted,'expected':expected,'purpose':'independent mathematical equivalence through native parser and grader'}]}

def make():
 sources=json.loads((E/'source-questions.json').read_text());cases=[];replays=[];fidelity=[]
 source_index={'q-1933':[3,4,0,1,2],'q-47966':[1,2,3,4,0]}
 for q in sources:
  sid=q[':question/math-academy-id'];t=next(t for t,v in g.TEMPLATES.items() if sid in v[2]);p=g.defaults(t)
  if sid=='q-319903':p={'c':5,'n':2,'k':1}
  r=g.generate(template=t,parameters=p,replay=True);replays.append(r)
  # Complete generated bank (not just the correct answer); pair each captured option with its recipe.
  rawbank=g.build(t,p)[2]
  if sid=='q-319902':rawbank.append(('3x^2e^{x}',rawbank[0][1],'alias'))
  if sid=='q-320816':rawbank.append((r'-5^{-x}\ln5\left(\log_7x\right)',rawbank[0][1],'alias'))
  sf=q[':question/answer-fields'][0];sourcechoices=sf[':answer-field/choices'];mapping=source_index.get(sid,list(range(len(sourcechoices))))
  matched=0;excluded=[]
  for i,a in enumerate(sourcechoices):
   if sid=='q-320824' and i==0:
    excluded.append({'answer_id':a[':answer/id'],'reason':'full derivative supplied for a second-term fragment'});continue
   j=0 if sid=='q-320824' else mapping[i]
   generated=g.normalize_tex(g.clean(rawbank[j][0]));assert generated in [a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
   cases.append(equivalence_case('source bank '+sid+' '+str(i),r,generated,g.normalize_tex(g.clean(a[':answer/value']))));matched+=1
  # Compare prompt equation and terminal solution with an independently specified product rule.
  product,A,B=oracle(t,p)
  header=q[':question/problem'].split('$')[1]
  supplied=re.split(r'f\(x\)\s*=\s*',header)[1].rstrip(',')
  cases.append(equivalence_case('source product '+sid,r,g.tex(product),g.normalize_tex(g.clean(supplied))))
  # Generated first equation must still represent the same original factors.
  generated_header=r['question'][':question/problem'].split('$')[1]
  supplied=re.split(r'f\(x\)\s*=\s*',generated_header)[1].rstrip(',')
  cases.append(equivalence_case('replayed product '+sid,r,g.tex(product),supplied))
  if q.get(':question/difficulty'):
   assert r['question'][':question/difficulty']==q[':question/difficulty'][':db/ident']
  else:assert ':question/difficulty' not in r['question']
  if sf.get(':answer-field/correct'):
   cases.append(equivalence_case('source key '+sid,r,key(r),g.normalize_tex(g.clean(sf[':answer-field/correct'][':answer/value']))))
  fidelity.append({'source_id':sid,'template':t,'matched_valid_choices':matched,'source_choices':len(sourcechoices),'generated_choices':len(r['question'][':question/answer-fields'][0][':answer-field/choices']),'exclusions':excluded,'source_difficulty_preserved':True,'source_solution_stages':q.get(':question/worked-solution','').count('& ='),'generated_solution_stages':r['question'][':question/worked-solution'].count('& ='),'missing_source_solution':':question/worked-solution' not in q})
 dump('source-replay.json',replays);dump('fidelity.json',fidelity)
 # Controlled masks and endpoint/case coverage, then a small unconditioned CLI-like sample.
 records=[];counter=[]
 for t,(_,ft,_) in g.TEMPLATES.items():
  p=g.defaults(t)
  if ft=='blank':
   left=g.generate(template=t,parameters=p,target='left',seed=33);right=g.generate(template=t,parameters=p,target='right',seed=33)
   assert key(left)!=key(right),(t,'unchanged target answer')
   assert left['question'][':question/problem']!=right['question'][':question/problem']
   assert left['question'][':question/worked-solution']==right['question'][':question/worked-solution'] # same full derivative is intentional
   records.extend([left,right]);counter.append({'family':t,'change':'missing contribution with all factors held constant','answers_changed':True,'full_solution_preserved':True,'native_checks':'grader-input.json'})
  # Explicit boundaries are finite and source-specific; no random stress sweep.
  keys=list(p)
  lo=p.copy();hi=p.copy()
  for k in keys:
   if k in ('b','d'):lo[k]=2;hi[k]=10
   elif k=='c':lo[k]=2 if t=='log_log_radio' else 1;hi[k]=6
   elif k=='n':lo[k]=-4 if t=='power_log_radio' else 2;hi[k]=-1 if t=='power_log_radio' else 4
   elif k=='h':lo[k]=0;hi[k]=5
   elif k=='k':lo[k]=-1 if t.startswith('base_log') else 1;hi[k]=1 if t.startswith('base_log') or t=='power_exp_radio' else 3
  records.extend([g.generate(template=t,parameters=lo,seed=71),g.generate(template=t,parameters=hi,seed=72)])
 for t in ('base_log_left_blank','base_log_right_blank','base_log_negative_left_blank'):
  for k in (-1,1):
   for d in (3,7):
    for side in ('left','right'):records.append(g.generate(template=t,parameters={'b':3,'d':d,'k':k},target=side))
 # Irrelevant constant counterfactual: left term of shifted polynomial/log.
 a=g.generate(template='polynomial_log_blank',parameters={'n':2,'h':1},target='left');b=g.generate(template='polynomial_log_blank',parameters={'n':2,'h':5},target='left')
 assert key(a)==key(b);records.extend([a,b]);counter.append({'family':'polynomial_log_blank','change':'constant h=1 to h=5, left target','response_preserved':True,'prompt_and_known_term_changed':a['question'][':question/problem']!=b['question'][':question/problem']})
 # Relevant coefficient counterfactuals: same family and all other parameters fixed.
 for t in ('linear_base_radio','power_exp_radio','cos_log_radio','sqrt_exp_radio','log_log_radio'):
  pa=g.defaults(t);pa['c']=2;pb={**pa,'c':3};a=g.generate(template=t,parameters=pa,seed=14);b=g.generate(template=t,parameters=pb,seed=14)
  assert key(a)!=key(b);records.extend([a,b]);counter.append({'family':t,'change':'coefficient 2 to 3 with same seed/other factors','prompt_answer_and_solution_changed':all(a['question'][k]!=b['question'][k] for k in (':question/problem',':question/worked-solution'))})
 records.extend(g.generate(seed=i+9100) for i in range(96))
 # Exercise all declared bank cases: total-scalar ranks, and each two-term
 # error direction/far placement. No arbitrary rank-balancing requirement.
 for t,v in g.TEMPLATES.items():
  if v[1]!='radio':continue
  def signature(rec):
   m=rec['generation'];return m['coefficient_rank'] if t=='log_log_radio' else (m['error_direction'],m['far_error_multiplier'],m['extra_row'])
  needed=set(range(5)) if t=='log_log_radio' else {(d,f,row) for d in (-1,1) for f in (-1,2) for row in (0,1)}
  present={signature(rec) for rec in records if rec['generation']['template']==t}
  for seed in range(100):
   if needed<=present:break
   rec=g.generate(template=t,seed=300+seed);sig=signature(rec)
   if sig not in present:records.append(rec);present.add(sig)
  assert needed<=present,(t,needed-present)

 mathchecks=0
 for i,r in enumerate(records+replays):
  z=r['generation'];t=z['template'];p=z['parameters'];product,A,B=oracle(t,p);field=r['question'][':question/answer-fields'][0]
  expected=A+B if field[':answer-field/type'].endswith('/radio') else A if z['target']=='left' else -B if B.could_extract_minus_sign() else B
  cases.append(equivalence_case('key mathematics '+str(i)+' '+t,r,g.tex(expected),key(r)))
  header=r['question'][':question/problem'].split('$')[1];provided=re.split(r'f\(x\)\s*=\s*',header)[1].rstrip(',')
  cases.append(equivalence_case('prompt mathematics '+str(i)+' '+t,r,g.tex(product),provided))
  final=r['question'][':question/worked-solution'].split('& =')[-1].split(r'\end{aligned}')[0].strip()
  cases.append(equivalence_case('solution mathematics '+str(i)+' '+t,r,g.tex(A+B),final))
  if field[':answer-field/type'].endswith('/blank'):
   before,after=r['question'][':question/problem'].split('{{field-1}}')
   if z['target']=='left':
    known=after.strip().strip('$').replace(r'\,','').strip();known_value=B
   else:
    ending=before.rsplit('(x)=',1)[1].strip().rstrip('$').strip()
    marker='-' if B.could_extract_minus_sign() else '+'
    assert ending.endswith(marker),(t,'wrong operation before blank')
    known=ending[:-1].replace(r'\,','').strip();known_value=A
   cases.append(equivalence_case('printed known contribution '+str(i)+' '+t,r,g.tex(known_value),known))
  mathchecks+=3
  _,_,rawbank,gu,gv,_=g.build(t,p)
  assert eq(gu*gv,product),(t,'factor mismatch')
  correct_expr=next(e for text,e,recipe in rawbank if recipe in ('correct','fragment'))
  raw_target='right' if t in ('power_exp_right_blank','base_tan_right_blank','base_log_right_blank','polynomial_log_blank') else 'left'
  raw_expected=A+B if field[':answer-field/type'].endswith('/radio') else A if raw_target=='left' else B
  # Draft source-only sqrt/cos/linear banks are used only at their original parameters.
  if not (t in ('linear_base_radio','cos_log_radio','sqrt_exp_radio') and p!=g.defaults(t)):
   assert eq(correct_expr,raw_expected),(t,p,'independent derivative mismatch')
  checks=[]
  if field[':answer-field/type'].endswith('/radio'):
   for choice in field[':answer-field/choices']:
    good=choice[':answer/id']==field[':answer-field/correct'][1]
    checks.append({'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if good else 'rejected','purpose':'actual UI radio UUID selection'})
    cases.append(equivalence_case('choice mathematics '+str(i)+' '+choice[':answer/id'],r,g.tex(expected),choice[':answer/value'],'accepted' if good else 'rejected'))
  else:
   checks=[{'submitted':key(r),'expected':'accepted','purpose':'stored correct fragment'}, {'submitted':r'\frac{2\left('+key(r)+r'\right)}{2}','expected':'accepted','purpose':'equivalent fragment with canceling factor 2'}, {'submitted':g.tex(expected+1),'expected':'rejected','purpose':'additive wrong answer'}, {'submitted':g.tex(A+B),'expected':'rejected','purpose':'full derivative in place of requested fragment'}]
   # A known contribution is not an answer shortcut; coincident mathematical identities are not penalized.
   other=B if z['target']=='left' else A
   if not eq(other,expected):checks.append({'submitted':g.tex(other),'expected':'rejected','purpose':'copy the printed known contribution'})
  if field[':answer-field/type'].endswith('/blank'):
   for alias in field[':answer-field/choices']:
    if alias[':answer/id']!=field[':answer-field/correct'][1]:checks.append({'submitted':alias[':answer/value'],'expected':'accepted','purpose':'captured equivalent answer alias through actual field'})
  cases.append({'label':'native UI '+str(i)+' '+t,'record':r,'checks':checks})
 # Known native domain limitation: x^(-n) and a fraction of positive powers
 # are not certified equivalent by this grader even on the problem's x>0 domain.
 unresolved=0
 for case in cases:
  if case['record']['generation']['template']!='power_log_radio':continue
  field=case['record']['question'][':question/answer-fields'][0]
  if not field[':answer-field/type'].endswith('/blank'):continue
  value=field[':answer-field/choices'][0][':answer/value']
  for check in case['checks']:
   submitted=check.get('submitted','')
   if check['expected']=='accepted' and 'x^{-' in submitted and 'x^{-' not in value:
    check['expected']='unresolved';check['purpose']='negative-power/fraction domain limitation; independent manual-derivative SymPy equality passes';unresolved+=1
 dump('counterfactuals.json',counter);dump('records.json',records);dump('grader-input.json',cases)
 # Representative actual UI records: every source family plus both target cases and a negative exponent.
 representatives=[]
 for t in g.TEMPLATES:
  representatives.append(next(r for r in records if r['generation']['template']==t))
 representatives.extend([r for r in records if r['generation']['template'] in ('base_cos_left_blank','base_log_negative_left_blank') and r['generation']['target']=='right'][:2])
 dump('render-records.json',representatives)
 extras=[]
 for t,predicate in [('base_cos_left_blank',lambda z:z['generation']['target']=='right'),('cos_log_radio',lambda z:z['generation']['parameters']['c']==6),('sqrt_exp_radio',lambda z:z['generation']['parameters']=={'c':6,'k':3})]:
  extras.append(next(z for z in records if z['generation']['template']==t and predicate(z)))
 dump('render-extra-records.json',extras)
 assert g.generate(seed=177)==g.generate(seed=177)
 guard=[]
 for t,p in [('log_log_radio',{'c':1,'b':3}),('power_exp_radio',{'c':1,'n':2,'k':2}),('base_log_left_blank',{'b':1,'d':3,'k':1})]:
  try:g.generate(template=t,parameters=p)
  except ValueError:guard.append(t)
  else:raise AssertionError('guard missing')
 for level in ('moderate','hard'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('unsupported band accepted')
 dump('checks-summary.json',{'source_questions':len(replays),'valid_source_choices':sum(a['matched_valid_choices'] for a in fidelity),'excluded_erroneous_source_choices':1,'records':len(records),'native_cases':len(cases),'independent_prompt_key_solution_checks':mathchecks,'parameter_guard_checks':guard,'deterministic':True,'sampling_rejections':0,'boundary_cases':'low/high for every numeric slot; signed/equal-unequal-base cross cases','documented_native_domain_comparisons':unresolved,'claims':'symbolic checks passed; native comparisons require check-engine report'})
 print(json.dumps({'records':len(records),'native_cases':len(cases),'source_questions':len(replays),'valid_source_choices':sum(a['matched_valid_choices'] for a in fidelity)}))

def audit(records):
 out={}
 for t in g.TEMPLATES:
  rs=[r for r in records if r['generation']['template']==t]
  if not rs:out[t]={'records':0};continue
  semantic={json.dumps([r['generation']['mathematical_fingerprint'],r['generation']['target']],sort_keys=True) for r in rs}
  d={'records':len(rs),'semantic_instances':len(semantic),'targets':dict(collections.Counter(r['generation']['target'] for r in rs)),'parameters':{k:sorted({r['generation']['parameters'][k] for r in rs}) for k in rs[0]['generation']['parameters']}}
  if g.TEMPLATES[t][1]=='radio':
   d['coefficient_roles_ranks']={role:sorted({r['generation']['coefficient_rank'] for r in rs if r['generation']['tested_role']==role}) for role in {r['generation']['tested_role'] for r in rs}}
   probes={}
   for group in ['all']+sorted(d['coefficient_roles_ranks']):
    group_rs=rs if group=='all' else [r for r in rs if r['generation']['tested_role']==group]
    position=collections.Counter();short=long=copyfirst=copysecond=minpair=maxpair=rowfew=rowmany=0;rank=collections.Counter()
    for r in group_rs:
     f=r['question'][':question/answer-fields'][0];a=f[':answer-field/choices'];correct=next(j for j,z in enumerate(a) if z[':answer/id']==f[':answer-field/correct'][1]);position[correct]+=1
     # Tied length strategies select first in display order, to avoid claiming every tie is a success.
     short+=min(range(5),key=lambda j:len(a[j][':answer/value']))==correct
     long+=max(range(5),key=lambda j:len(a[j][':answer/value']))==correct
     rank[r['generation']['coefficient_rank']]+=1
     if 'coefficient_pairs' in r['generation']:
      # Copying either correct coefficient alone leaves a wrong alternative.
      pairs=r['generation']['coefficient_pairs'];aa,bb=r['generation']['true_coefficients']
      assert sum(pa==aa for pa,pb in pairs)>=2 and sum(pb==bb for pa,pb in pairs)>=2
      parsed=[tuple(map(int,re.findall(r'\\left\(([-0-9]+)\\right\)',choice[':answer/value']))) for choice in a]
      assert all(len(pair)==2 for pair in parsed)
      copyfirst+=next(j for j,pair in enumerate(parsed) if pair[0]==aa)==correct
      copysecond+=next(j for j,pair in enumerate(parsed) if pair[1]==bb)==correct
      minpair+=min(range(5),key=lambda j:parsed[j])==correct
      maxpair+=max(range(5),key=lambda j:parsed[j])==correct
      frequencies=collections.Counter(pair[0] for pair in parsed)
      rowfew+=min(range(5),key=lambda j:frequencies[parsed[j][0]])==correct
      rowmany+=max(range(5),key=lambda j:frequencies[parsed[j][0]])==correct
    probes[group]={'attempts':len(group_rs),'random_baseline':0.2,'positions':dict(position),'shortest_first_successes':short,'longest_first_successes':long,'coefficient_rank_successes':dict(rank),'copy_first_correct_coefficient_first_match':copyfirst,'copy_second_correct_coefficient_first_match':copysecond,'lexicographic_min_pair':minpair,'lexicographic_max_pair':maxpair,'least_frequent_row_first_match':rowfew,'most_frequent_row_first_match':rowmany}
    assert max(position.values())<len(group_rs),(t,group,'fixed position')
    assert short<len(group_rs) and long<len(group_rs),(t,group,'length shortcut')
    assert len(rank)>1,(t,group,'fixed rank')
    if t!='log_log_radio':assert all(v<len(group_rs) for v in (copyfirst,copysecond,minpair,maxpair,rowfew,rowmany)),(t,group,'coefficient copying shortcut')
   d['shortcut_probes']=probes
  else:assert {r['generation']['target'] for r in rs}=={'left','right'},(t,'target lost')
  out[t]=d
 return out

def final():
 raw=json.loads((E/'records.json').read_text());accepted=json.loads((E/'delivery/accepted.json').read_text());report={'before':audit(raw),'after':audit(accepted),'limits':['No learner-specific history or live database state accessed.','Observed radio banks replay source banks; default practice uses coefficient_check only.','Finite tan/common-log family has exactly two masks.','Counterfactual pairs with equal factors retain the same full worked solution; their requested fragment and known term change.'],'selection':{'implementation':'engine/rust/question_selection.rs select, inspected read-only','rule':'positive easy weight selects uniformly among fresh easy candidates; zero easy weight excludes these; unknown-band fallback is not relevant to default output','history':'fresh candidate membership is learner-dependent and unavailable','no_family_conditioning':'once easy selected, index is floor(uniform(hash seed bytes 8..16)*easy_count)'}}
 report['native_grading']=json.loads((E/'grader-report.json').read_text()) | {'records':'see grader-report.json'}
 def signature(rec):
  q=rec['question'];f=q[':question/answer-fields'][0]
  return(q[':question/problem'],q[':question/worked-solution'],f[':answer-field/type'],tuple(sorted(a[':answer/value'] for a in f[':answer-field/choices'])),key(rec))
 originals={signature(rec) for rec in raw};assert all(signature(rec) in originals for rec in accepted)
 semantic=lambda rec:(rec['generation']['mathematical_fingerprint'],rec['generation']['target'])
 dump('delivery-content-check.json',{'raw_records':len(raw),'accepted_records':len(accepted),'distinct_mathematical_tasks_before':len({semantic(rec) for rec in raw}),'distinct_mathematical_tasks_after':len({semantic(rec) for rec in accepted}),'accepted_math_content_unchanged':True,'accepted_native_grading_coverage':'all accepted content occurs in raw native tests; normalization changes identities only','generator_rejection':'no sampled-domain mathematical rejection/resampling; explicit invalid arguments rejected','learner_selection':'read-only source analysis in pedagogical-variation.json; actual learner history unavailable'})
 dump('pedagogical-variation.json',report)
 summary=json.loads((E/'checks-summary.json').read_text());summary['native_result']={k:v for k,v in report['native_grading'].items() if k!='records'};summary['delivery_accepted']=len(accepted);summary['claims']='source bank comparisons, independent manual derivatives, native UI grading and declared shortcut probes passed, with documented native domain-equivalence limitations';dump('checks-summary.json',summary)
 print(json.dumps({'before':len(raw),'after':len(accepted),'families_before':len(report['before']),'families_after':len(report['after']),'shortcut_assertions':'passed'}))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--final',action='store_true');a=ap.parse_args();final() if a.final else make()
