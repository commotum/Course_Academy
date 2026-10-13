#!/usr/bin/env python3
"""Independent actual-printed math, source omissions, bank/stage fidelity and grader QA.
No source database transactions. Run from repository using .venv/bin/python.
"""
import copy, hashlib, importlib.util, importlib.metadata, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('component_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
I,J,A,B,C=sp.symbols('i j a b c');LOCAL=dict(i=I,j=J,a=A,b=B,c=C)
TRANS=standard_transformations+(implicit_multiplication_application,)

def math(s):
 s=s.strip().rstrip('.').replace(' ','')
 assert re.fullmatch(r'[0-9ijabc()+\-]*',s),s
 assert '--' not in s and '+-' not in s,s
 s=re.sub(r'(?<=\d)(?=[ijabc])','*',s) # prevent Python's 6j complex-literal token
 return sp.expand(parse_expr(s,local_dict=LOCAL,transformations=TRANS))

def pair(x):
 assert not x.free_symbols-{I,J},x
 assert sp.Poly(x,I,J).total_degree()<=1 and x.subs({I:0,J:0})==0,x
 return tuple(int(x.coeff(v)) for v in (I,J))

def printed(q):
 formulas=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'])
 assert len(formulas) in (3,4),formulas
 op=math(formulas[0]);subs={}
 for f in formulas[1:]:
  var,val=f.split('=',1);assert var.strip() in ('a','b','c');subs[LOCAL[var.strip()]]=math(val)
 assert set(subs)==op.free_symbols
 expected=sp.expand(op.subs(subs));return op,subs,expected

def balanced(text):
 assert text.count('$')%2==0
 depth=0
 for char in text:
  if char=='{':depth+=1
  if char=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert '--' not in text and '+-' not in text
 assert not re.search(r'\\\\(?:begin|end)',text)


def inspect(rec,require_fields=True):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=rec['question'];op,subs,expected=printed(q);correct=pair(expected)
 uuid.UUID(q[':question/id']);balanced(q[':question/problem'])
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];balanced(sol)
  opening=re.search(r'To compute \$(.*?),\$',sol);assert opening and math(opening[1])==op
  body=sol.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
  rows=body.split(chr(92)*2);lhs,rhs=rows[0].split('&',1);assert math(lhs)==op
  rights=[rhs]+[row.split('&',1)[1] for row in rows[1:]]
  strings=[]
  for rhs in rights:
   assert rhs.strip().startswith('=');s=rhs.strip()[1:];strings.append(s)
   assert sp.expand(math(s).subs(subs)-expected)==0,(s,expected)
  # Structural substitution/distribution/collection/final boundaries, beyond equality.
  t=rec['generation']['template'];n=len(subs)
  assert len(strings)==(5 if t=='nested_three' else 4)+(1 if 0 in correct else 0)
  assert len(re.findall(r'\([^)]+[ij][^)]*\)',strings[0]))>=n
  idx=2 if t=='nested_three' else 1
  distributed=strings[idx];collected=strings[idx+1]
  assert distributed.count('i')==distributed.count('j')==n
  assert collected.count('i')==collected.count('j')==n
  assert collected.count('(')==2 and collected.count(')')==2
  # Read each distributed term from the printed output; compare in input order.
  toks=re.findall(r'[+-]?\d*[ij]',distributed.replace(' ',''))
  assert ''.join(toks)==distributed.replace(' ','').lstrip('+')
  weights=[int(op.coeff(v)) for v in (A,B,C) if v in subs]
  want=[w*pair(subs[v])[d] for w,v in zip(weights,[v for v in (A,B,C) if v in subs]) for d in (0,1)]
  got=[int(math(tok).coeff(I if tok.endswith('i') else J)) for tok in toks]
  assert got==want,(got,want)
  assert pair(math(strings[-1]))==correct
 if ':question/answer-fields' not in q:
  assert not require_fields and rec['generation']['evidence_only'];return correct
 fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio';uuid.UUID(f[':answer-field/id'])
 assert '{{' not in q[':question/problem'];choices=f[':answer-field/choices'];assert len(choices)==5
 vals=[pair(math(a[':answer/value'])) for a in choices];assert len(set(vals))==5
 for a in choices:uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value']
 assert vals.count(correct)==1
 if ':answer-field/correct' in f:
  ref=f[':answer-field/correct'];assert ref[0]==':answer/id'
  assert [a[':answer/id'] for a,v in zip(choices,vals) if v==correct]==[ref[1]]
 else:assert not require_fields and rec['generation']['evidence_only']
 # Independently check complete authored error operations, derived from PRINTED operands.
 profile=rec['generation']['bank_profile'];t=rec['generation']['template']
 if profile=='authored-operations' or (profile.startswith('completed-') and t in ('right_scale','both_scale')):
  vs=[pair(subs[v]) for v in (A,B,C) if v in subs];ws=[int(op.coeff(v)) for v in (A,B,C) if v in subs];x,y=correct
  if t=='add':
   (ax,ay),(bx,by)=vs;want=[correct,(ax-bx,ay-by),(x,-y),(ax-bx,y),(x,ay-by)]
  elif t=='nested_three':
   # Recover the actual nested coefficients from the prompt; do not use parameter metadata.
   txt=re.findall(r'\$(.*?)\$',q[':question/problem'])[0]
   m=re.fullmatch(r'(-?\d+)a-(\d+)\(b-(?:\((-?\d+)c\)|(-?\d+)c)\)',txt);assert m,txt
   h,j,k=int(m[1]),int(m[2]),int(m[3] or m[4]);a,b,c=vs
   want=[correct,tuple(h*a[d]-j*b[d]-j*k*c[d] for d in (0,1)),tuple(h*a[d]-j*b[d]+k*c[d] for d in (0,1)),tuple(h*a[d]-j*b[d]+j*c[d] for d in (0,1)),(x,sum(v[1] for v in vs))]
  else:
   idx=next(i for i,w in enumerate(ws) if abs(w)>1);w=ws[idx];v=vs[idx]
   want=[correct,(x+(1-w)*v[0],y+(1-w)*v[1]),(x-2*ws[-1]*vs[-1][0],y-2*ws[-1]*vs[-1][1]),(x,sum(v[1] for v in vs)),(sum(v[0] for v in vs),y)]
  assert set(vals)==set(want)
 return correct

def checks(rec):
 f=rec['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'real radio selection of independently checked displayed vector'} for a in f[':answer-field/choices']]

def write(name,obj):(D/name).write_text(json.dumps(obj,indent=2)+'\n')
def fingerprint_printed(rec):
 op,subs,_=printed(rec['question']);t=rec['generation']['template']
 vals=[pair(subs[v]) for v in (A,B,C) if v in subs]
 if t=='nested_three':
  # Compare grouping/task shape independently, not flattened coefficients.
  txt=re.findall(r'\$(.*?)\$',rec['question'][':question/problem'])[0]
  m=re.fullmatch(r'(-?\d+)a-(\d+)\(b-(?:\((-?\d+)c\)|(-?\d+)c)\)',txt);assert m
  operator=('nested',int(m[1]),int(m[2]),int(m[3] or m[4]))
 else:operator=('flat',[int(op.coeff(v)) for v in (A,B,C) if v in subs])
 return g.digest({'operands':vals,'operator':operator})

def main():
 review=[];native=[];cases=[];fidelity=[];math_count=0;source_option_count=0;source_dist_count=0
 for sid,(t,p) in g.ANCHORS.items():
  case={'source_id':sid,'template':t,'parameters':p,'bank_profile':'raw-'+sid,'level':'easy','level_origin':'observed' if sid.startswith('q-125') else 'authored unrated replay routing'};cases.append(case)
  raw=g.generate('easy',template=t,parameters=p,profile=case['bank_profile']);inspect(raw,False);old=g.SOURCES[sid];q=raw['question']
  # Exact attribute absence parity on all public question content attributes.
  for key in (':question/problem',':question/difficulty',':question/answer-fields',':question/worked-solution'):
   assert (key in q)==(key in old),(sid,key)
  assert q[':question/problem']==old[':question/problem']
  assert q.get(':question/worked-solution')==old.get(':question/worked-solution')
  if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
  if ':question/answer-fields' in old:
   f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
   assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
   assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
   source_option_count+=5;source_dist_count+=4
  fidelity.append({'source_id':sid,'exact_prompt':True,'exact_available_solution':':question/worked-solution' in old,'key_presence_parity':True,'complete_bank_match':':question/answer-fields' in old,'correct_designation_available':False,'source_correct_inferred_vector':g.vector(*inspect(raw,False),True)})
  review.append({'label':'Original '+sid+' (raw omissions preserved)','record':raw,'raw_capture':old})
  completed=g.generate('easy',template=t,parameters=p,profile='completed-'+sid);inspect(completed);native.append({'label':'Completed anchor '+sid,'record':completed,'checks':checks(completed)});review.append({'label':'Authored/inferred completion '+sid,'record':completed});math_count+=2
  # Explicit changed parameters through normal public raw profiles: no literal replay.
  changed={k:-v if k in ('ax','ay') else v for k,v in p.items()}
  try:variant=g.generate('easy',template=t,parameters=changed,profile='raw-'+sid)
  except ValueError:changed['bx']+=1;variant=g.generate('easy',template=t,parameters=changed,profile='raw-'+sid)
  inspect(variant,False);assert variant['question'][':question/problem']!=q[':question/problem'];review.append({'label':'Changed raw evidence recipe '+sid,'record':variant})
  normal=g.generate('easy',seed=41,template=t);inspect(normal);review.append({'label':'Eligible normal family variant '+t,'record':normal})
 # Broad bounded SAME-WORKLOAD variety: 160 per family; whole-bank collision rejection
 # exercised by both samplers and explicit-boundary calls. Counts are lower bounds,
 # never a claim of exhaustive millions-of-coordinate-combinations validation.
 fps={l:set() for l in g.SUPPORTED_LEVELS};family_profiles={};identities=set();records=[]
 for t,level in g.TEMPLATES.items():
  profiles=['observed-add','authored-operations'] if t=='add' else ['authored-operations']
  for profile in profiles:
   family_profiles[t+'/'+profile]=0
   for seed in range(160):
    rec=g.generate(level,seed=seed+800,template=t,profile=profile);inspect(rec);math_count+=1;records.append(rec)
    assert rec['generation']['mathematical_fingerprint']==fingerprint_printed(rec)
    assert rec==g.generate(level,seed=seed+800,template=t,profile=profile)
    alt=g.generate(level,seed=seed+801,template=t,profile=profile,parameters=rec['generation']['parameters']);assert alt['question'][':question/id']==rec['question'][':question/id']
    assert sorted(a[':answer/id'] for a in alt['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices'])
    fps[level].add(fingerprint_printed(rec));identities.add(rec['question'][':question/id']);family_profiles[t+'/'+profile]+=1
    native.append({'label':t+'/'+profile+'/'+str(seed),'record':rec,'checks':checks(rec)})
    if seed<2:review.append({'label':'Generated '+level+' '+t+' '+profile+' seed '+str(seed),'record':rec})
 # All eligible families/banks reached in unrestricted default sampling.
 defaults={l:set() for l in g.SUPPORTED_LEVELS};default_banks=set();correct_positions=set()
 for level in g.SUPPORTED_LEVELS:
  for seed in range(160):
   r=g.generate(level,seed);inspect(r);defaults[level].add(r['generation']['template']);default_banks.add((r['generation']['template'],r['generation']['bank_profile']))
   f=r['question'][':question/answer-fields'][0];correct_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 for l in g.SUPPORTED_LEVELS:assert defaults[l]=={t for t,v in g.TEMPLATES.items() if v==l}
 assert ('add','observed-add') in default_banks and ('add','authored-operations') in default_banks
 assert correct_positions==set(range(5))
 # Whole-bank collision must reject, no first-valid replacement or silent sampling.
 invalid=[('easy','add',dict(ax=2,ay=2,bx=1,by=-2)),('moderate','flat_three',dict(ax=1,ay=1,bx=2,by=2,cx=3,cy=3,p=1,q=2,r=3)),('hard','nested_three',dict(ax=1,ay=1,bx=2,by=2,cx=3,cy=3,p=2,q=2,r=1))]
 rejected=0
 for l,t,p in invalid:
  try:g.generate(l,template=t,parameters=p)
  except ValueError:rejected+=1
  else:raise AssertionError('Invalid parameters accepted')
 unit_raw=g.generate('easy',template='both_scale',parameters=dict(ax=1,ay=2,bx=3,by=4,p=1,q=1),profile='raw-q-125088');inspect(unit_raw,False);assert ':question/answer-fields' not in unit_raw['question']
 # Same printed task under different banks has the same math fingerprint but a
 # different content ID when its displayed bank is different.
 p=dict(ax=7,ay=-6,bx=3,by=2)
 rr=[g.generate('easy',template='add',parameters=p,profile=profile) for profile in ('observed-add','authored-operations')]
 assert rr[0]['generation']['mathematical_fingerprint']==rr[1]['generation']['mathematical_fingerprint']
 assert rr[0]['question'][':question/id']!=rr[1]['question'][':question/id']
 # Parameter aliases/unused scalar fail rather than inflating task variety.
 try:g.generate('easy',template='add',parameters={**p,'p':1})
 except ValueError:rejected+=1
 else:raise AssertionError('Unused scalar accepted')
 # Actual-display mutation controls must be caught by independent parser/stage QA.
 controls=0
 r=next(r for r in records if r['generation']['template']=='both_scale')
 for key,mutator in [(':question/worked-solution',lambda s:s.replace('& =','& =1+',1)),(':question/problem',lambda s:s.replace('$a=','$a=1+',1)),(':question/worked-solution',lambda s:s.replace("$i$'s","$k$'s").replace('& =','& =1+',1))]:
  bad=copy.deepcopy(r);bad['question'][key]=mutator(bad['question'][key])
  try:inspect(bad)
  except (AssertionError,ValueError):controls+=1
  else:raise AssertionError('Corrupted actual printed math undetected')
 write('source-cases.json',cases);write('fidelity.json',fidelity);write('review.json',review)
 (D/'review.md').write_text('\n\n---\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review)+'\n')
 write('engine-input.json',native)
 binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 engine=json.loads((D/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 write('validation.json',{'passed':True,'basis':1356,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib_installed':importlib.metadata.version('matplotlib'),'renderer_used':None},'source_coverage':{'practice_sources':4,'exact_prompts':4,'exact_available_worked_solutions':2,'available_worked_solutions':2,'raw_omission_parity':4,'complete_observed_banks_matched':2,'observed_banks':2,'displayed_values_matched':source_option_count,'displayed_values':10,'inferred_wrong_values_matched':source_dist_count,'inferred_wrong_values':8,'captured_correct_designations':0,'matched_captured_correct_designations':0,'independently_inferred_correct_values':4,'authored_field_completions':2,'authored_solution_completions':2},'bounded_math_records_checked':math_count,'sampled_distinct_tasks_lower_bound':{l:len(v) for l,v in fps.items()},'family_bank_samples':family_profiles,'default_family_coverage':{l:sorted(v) for l,v in defaults.items()},'all_radio_positions_reached':True,'invalid_inputs_rejected':rejected,'negative_math_controls_detected':controls,'review_records':len(review),'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'plots':'none; assessment sources have no raster/diagram references','limitations':['Historical q70402 wrong-operation intentions unresolved; raw and completed historical bank ineligible for default learning.','All four original correct designations absent; no designation-match claim.','Two original answer-field layouts absent; completed radio fields are authored.','Moderate/hard levels are same-method authored designs, not observed labels.','Coordinate domain is large; sampled lower bounds are reported, not an exhaustive finite-domain claim.'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (D.with_suffix('.py'),Path(__file__),D/'source.json',D/'original-widgets.json',binary,ROOT/'generate/runs/current/check-engine.rs')}})
 print('PASS',math_count,'math records;',source_option_count,'source values; distinct task lower bounds:',{l:len(v) for l,v in fps.items()})
if __name__=='__main__':main()
