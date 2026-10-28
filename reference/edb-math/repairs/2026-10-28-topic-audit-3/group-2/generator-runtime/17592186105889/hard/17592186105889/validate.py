#!/usr/bin/env python3
"""Fail-closed source fidelity, independent displayed mathematics, scope and engine QA."""
from pathlib import Path
import importlib.util,json,re,subprocess,hashlib,sys,copy
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
G=module('surface_generator',HERE.with_suffix('.py'))
P=module('independent_reader',REPO/'generate/runs/current/ode-scalar-parser.py')
x,y,z=P.x,P.y,P.z

def equal(a,b):
 assert s.simplify(a-b)==0,(a,b)
def scalar(t):
 v=P.scalar(t)
 assert v.free_symbols<={x,y,z},t
 return v

def formatting(t):
 assert t.count('$$')*2<=t.count('$')
 assert t.replace('$$','').count('$')%2==0,'unbalanced inline math'
 d=0
 for c in t:
  d+=(c=='{')-(c=='}');assert d>=0
 assert d==0,'unbalanced braces'
 assert '--' not in t and '+-' not in t

def read_prompt(q):
 p=q[':question/problem']
 f=scalar(re.search(r'\$f\(x,\s*y,\s*z\)\s*=(.*?)(?:,?\$)',p)[1].rstrip(','))
 g=scalar(re.search(r'\$z\s*=(.*?)\$',p)[1])
 bx=re.search(r'(-?\d+)\s*\\le(?:q)?\s*x\s*\\le(?:q)?\s*(-?\d+)',p)
 by=re.search(r'(-?\d+)\s*\\le(?:q)?\s*y\s*\\le(?:q)?\s*(-?\d+)',p)
 bounds=[int(bx[1]),int(bx[2]),int(by[1]),int(by[2])]
 return f,g,bounds

def read_math(r,raw=False):
 q=r['question'];f,g,bounds=read_prompt(q);dx=s.diff(g,x);dy=s.diff(g,y)
 pref=s.expand(f.subs(z,g));metric=s.sqrt(1+dx*dx+dy*dy);answer=pref*metric
 assert bounds[0]<bounds[1] and bounds[2]<bounds[3]
 for t in (q[':question/problem'],q.get(':question/worked-solution','')):formatting(t)
 # Source odd integral markup remains explicitly raw and ineligible.
 if not raw:
  shown=re.findall(r'\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}',q[':question/problem'])
  assert len(shown)==1 and [int(i) for i in shown[0]]==bounds
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution']
  formal=re.findall(r'\\frac\{∂z\}\{∂([xy])\}=\\frac\{∂\}\{∂\1\}\((.*?)\)=([^\n]+)',sol)
  assert len(formal)==2
  for var,arg,val in formal:
   equal(scalar(arg),g);equal(scalar(val),dx if var=='x' else dy)
  assert G.OPENING in sol and 'For the partial derivatives, we have' in sol and 'Therefore, the surface integral can be written as' in sol
  # Independently read every displayed RHS row, including symbolic generic f
  # rows and metric substitution. Same UUID or matching metadata cannot pass it.
  aligned=sol.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
  rows=aligned.split(' & =',1)[1].split(r' \\  & =')
  template=r['generation']['template']
  assert len(rows)==(5 if template=='plane_xyz' or (not raw and (template not in G.BASE or template=='plane_xz')) else 4)
  for row in rows:
   row=row.rstrip('.')
   is_def=row.startswith(r'{\int }')
   if is_def:
    m=re.match(r'\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}',row)
    assert m and [int(v) for v in m.groups()]==bounds
    body=row[m.end():].split(r'\text{d}y',1)[0].rstrip('\\,')
   else:
    assert row.startswith(r'{∬}_{D}');body=row[len(r'{∬}_{D}'):].split(r'\text{d}A',1)[0].rstrip('\\,')
   body=body.replace('f(x,y,g(x,y))','('+G.tex(pref)+')')
   body=body.replace(r'\frac{∂z}{∂x}','('+G.tex(dx)+')').replace(r'\frac{∂z}{∂y}','('+G.tex(dy)+')')
   equal(scalar(body),answer)
 # Check complete bank expressions independently from actual displayed f,g.
 field=q[':question/answer-fields'][0];bank=[scalar(a[':answer/value']) for a in field[':answer-field/choices']]
 if ':answer-field/correct' in field:
  cid=field[':answer-field/correct'][1];correct=next(i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==cid)
  equal(bank[correct],answer)
 else:
  assert sum(s.simplify(value-answer)==0 for value in bank)==1,'unrated source lacks unique independently inferred option'
 if not raw:
  assert len(bank)==5
  assert ':question/difficulty' in q and ':question/worked-solution' in q
  assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
  for i in range(5):
   for j in range(i):assert s.simplify(bank[i]-bank[j])!=0,'equivalent complete options'
  # No radical denominator or branch is undefined: normal banks are constructed
  # from sums of real squares; read those complete structures back as method set.
  expected=[answer,pref,pref*metric**2,pref/metric,pref*s.sqrt(dx**2+dy**2)]
  remaining=list(bank)
  for wanted in expected:
   hits=[i for i,b in enumerate(remaining) if s.simplify(b-wanted)==0]
   assert len(hits)==1;remaining.pop(hits[0])
  assert not remaining
 return f,g,answer

def native_item(label,r):
 field=r['question'][':question/answer-fields'][0];cid=field[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'complete owned radio choice'} for a in field[':answer-field/choices']]}

def main():
 records=[];review=[];cases=[];native=[];source_report=[]
 # Every original, including the unrated malformed question, via public API.
 for template,b in G.BASE.items():
  source_id=b['source'];p=G.original_parameters(template);r=G.generate('easy',template=template,parameters=p,profile='raw:'+source_id)
  q=r['question'];expected=G.shape(G.QUESTIONS[source_id]);assert set(q)==set(expected)
  for key in expected:
   if key==':question/answer-fields':continue
   assert q[key]==expected[key],(source_id,key)
  f=q[':question/answer-fields'][0];of=expected[':question/answer-fields'][0]
  assert set(f)==set(of)
  assert all(f[k]==of[k] for k in f if k!=':answer-field/choices')
  assert sorted(f[':answer-field/choices'],key=lambda a:a[':answer/id'])==sorted(of[':answer-field/choices'],key=lambda a:a[':answer/id'])
  assert not r['generation']['eligible_for_learning'] and r['generation']['evidence_only']
  read_math(r,raw=True)
  if ':answer-field/correct' in f:native.append(native_item(source_id,r))
  cases.append({'source_id':source_id,'level':'easy','template':template,'parameters':p,'bank_profile':'raw:'+source_id,'authored_replay_level':':question/difficulty' not in q})
  review.append({'label':'ORIGINAL '+source_id,'kind':'original','record':r})
  source_report.append({'source_id':source_id,'exact_prompt':True,'exact_solution_or_absence':True,'exact_bank_options':len(f[':answer-field/choices']),'exact_attribute_presence':True,'original_correct_designation':':answer-field/correct' in f,'eligible_for_learning':False})
  # Original profile is genuinely parameterized: changed scalar and rectangle,
  # all teaching rows re-read; opaque distractors remain evidence-only.
  for scale in (-2,2):
   changed=copy.deepcopy(p);changed['k']=str(scale*G.number(p['k']));changed['bounds']=[0,2,-1,1]
   variant=G.generate('easy',seed=scale,template=template,parameters=changed,profile='raw:'+source_id)
   read_math(variant,raw=True)
   assert variant['question'][':question/id']!=r['question'][':question/id']
   assert variant['generation']['content_id']!=r['generation']['content_id']
   review.append({'label':f'RAW PROFILE VARIANT {source_id} scale {scale}','kind':'evidence-only variant','record':variant})
 # Two independent generated examples for every template at every level.
 for template,level in G.TEMPLATES.items():
  for seed in (31,72):
   r=G.generate(level,seed,template=template);read_math(r);records.append(r);native.append(native_item(template+str(seed),r));review.append({'label':f'GENERATED {level} {template} seed {seed}','kind':'authored bank variant','record':r})
   # Fixed parameter content/meaning identities ignore seed, order and aliases.
   r2=G.generate(level,seed+1,template=template,parameters=r['generation']['parameters'],profile='measure_conversion')
   assert r['generation']['content_id']==r2['generation']['content_id'] and r['question'][':question/id']==r2['question'][':question/id']
   changed=copy.deepcopy(r['generation']['parameters']);changed['bounds']=[0,1,0,1]
   r3=G.generate(level,seed,template=template,parameters=changed)
   assert r3['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
   if changed['bounds']!=r['generation']['parameters']['bounds']:assert r3['generation']['content_id']!=r['generation']['content_id']
 # Actual default family coverage, separate from explicit-template support.
 seen=set()
 for seed in range(40):seen.add(G.generate('easy',seed)['generation']['template'])
 assert seen==set(G.BASE)
 for level in ('moderate','hard'):
  seen_level={G.generate(level,seed)['generation']['template'] for seed in range(6)}
  assert seen_level=={t for t,l in G.TEMPLATES.items() if l==level}
 # Explicit bounds guard and coefficient sign/magnitude boundaries.
 rejection_count=0
 for template,level in G.TEMPLATES.items():
  good=G.sample(template,__import__('random').Random(91))
  for key in [k for k in good if k!='bounds']:
   bad=copy.deepcopy(good);bad[key]='0'
   try:G.generate(level,template=template,parameters=bad)
   except ValueError:rejection_count+=1
   else:raise AssertionError('zero workload-defining component admitted')
  bad=copy.deepcopy(good);bad['a']='-3'
  try:G.generate(level,template=template,parameters=bad)
  except ValueError:rejection_count+=1
  else:raise AssertionError('negative magnitude bypass')
 # Malformed source preserves missing attrs and cannot be selected as a raw
 # default; repaired plane_xz is a completed authored record instead.
 raw323=G.generate_easy(profile='raw:q-161323')['question']
 assert ':question/difficulty' not in raw323 and ':question/worked-solution' not in raw323
 assert ':answer-field/correct' not in raw323[':question/answer-fields'][0]
 assert G.generate_easy(template='plane_xz')['generation']['eligible_for_learning']
 # Outer local shape and UUID/field ownership checked on every normal record.
 import uuid
 for r in records:
  assert set(r['knowledge_point'])=={'db_id','id','title'}
  q=r['question'];uuid.UUID(q[':question/id'])
  for f in q[':question/answer-fields']:
   uuid.UUID(f[':answer-field/id']);ids=[a[':answer/id'] for a in f[':answer-field/choices']]
   assert len(set(ids))==5 and f[':answer-field/correct'][1] in ids
   for aid in ids:uuid.UUID(aid)
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 (HERE/'review.md').write_text('# Source originals and generated setup variants\n\nRaw historical profiles are evidence-only; authored normal variants are eligible.\n\n'+'\n\n---\n\n'.join('## '+item['label']+'\n\n'+G.markdown(item['record']) for item in review))
 (HERE/'engine-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
 engine=REPO/'generate/runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 report=json.loads((HERE/'engine-report.json').read_text())
 summary={'status':'passed','version':G.VERSION,'source':{k:G.SOURCE[k] for k in ('database','basis','lineage')},'source_questions':8,'exact_complete_prompts':8,'exact_solutions_present':7,'exact_missing_solution':1,'exact_complete_banks':8,'matched_choices':40,'original_correct_designations':7,'missing_original_designations':1,'source_attribute_presence_parity':8,'raw_profiles_evidence_only':8,'authored_completed_unrated_records':1,'normal_variants':len(records),'templates_by_level':{level:sum(l==level for l in G.TEMPLATES.values()) for level in ('easy','moderate','hard')},'authored_missing_levels':['moderate','hard'],'default_easy_family_coverage':sorted(seen),'explicit_parameter_rejections':rejection_count,'native_accepted':report['accepted_checks'],'native_rejected':report['rejected_checks'],'native_unresolved':report['documented_unresolved_checks'],'independent_displayed_readback':'every original, changed raw profile and normal review example: printed f,g,formal partials,all scalar integral rows,metric factors,products,bounds,complete banks','complete_definite_integral_choice_checks':'not applicable; all answers are integrand fragments, so scalar integral equality is not the requested response criterion','source_errors':{'q-161323':'missing rating, solution and correct ref; malformed AAAAAAA placeholder; raw preserved, authored completion separate','opaque_banks':'historical interpretation remains unresolved; all raw profiles ineligible','nonreal_source_options':['q-161321 choice2 sqrt(5x) nonreal for x<0','q-161325 choices2 and5 have nonpositive radicand on part of rectangle','q-161314 choice5 sqrt(3x) nonreal for x<0']},'source_rows':source_report,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'database_reads':0,'database_writes':0}
 if (HERE/'boundary-validation.json').exists():
  boundary=json.loads((HERE/'boundary-validation.json').read_text());assert boundary['status']=='passed'
  for item in boundary['checks']:
   actual=G.generate(item['level'],template=item['template'],parameters=item['parameters']);read_math(actual)
   assert actual['generation']['content_id']==item['content_id']
  summary['explicit_boundary_readbacks']=len(boundary['checks'])
 if (HERE/'variety.json').exists():summary['canonical_unique_tasks_by_level']=json.loads((HERE/'variety.json').read_text())['unique_tasks_by_level']
 (HERE/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({k:summary[k] for k in ('status','source_questions','matched_choices','normal_variants','native_accepted','native_rejected','native_unresolved')},indent=2))
if __name__=='__main__':main()
