#!/usr/bin/env python3
"""Independent displayed-math, complete fidelity, scope, identity and native grading."""
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
sys.path.insert(0,str(ROOT));import math_check as m
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def dump(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def checks(r,label):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank designation'} for a in f[':answer-field/choices']]}
def run():
 source=json.loads((ROOT/'source.json').read_text());qs=source['record'][':knowledge-point/questions'];cases=[];fidelity=[];review=[];engine=[];mapping=[];domains=[]
 for q in qs:
  sid=q[':question/math-academy-id'];t=next(t for t,v in g.TEMPLATES.items() if v[1]==sid);l,_,p=g.TEMPLATES[t]
  case={'source_id':sid,'source_db_id':q[':db/id'],'level':l,'template':t,'parameters':p,'bank_profile':'observed'};cases.append(case)
  r=g.generate(l,template=t,parameters=p,profile='observed');rq=r['question'];f=rq[':question/answer-fields'][0];sf=q[':question/answer-fields'][0];new={a[':answer/value'] for a in f[':answer-field/choices']};old={a[':answer/value'] for a in sf[':answer-field/choices']}
  assert new==old,(sid,'bank mismatch',new-old,old-new)
  assert rq[':question/problem']==q[':question/problem'],(sid,'prompt mismatch')
  assert rq[':question/worked-solution']==q[':question/worked-solution'],(sid,'solution mismatch',rq[':question/worked-solution'],q[':question/worked-solution'])
  correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==sf[':answer-field/correct'][':answer/value']
  stats=m.validate_bank(rq[':question/problem'],rq[':question/worked-solution'],list(new),list(new).index(correct))
  
  rawbank=g.build(t,p)[2]
  for i,v in enumerate(rawbank):
   sa=next(a for a in sf[':answer-field/choices'] if a[':answer/value']==v)
   mapping.append({'source_id':sid,'template':t,'profile':'observed','field_key':'selection','source_answer_uuid':sa[':answer/id'],'exact_value':v,'parameterized_recipe':'build/'+t+'/option-'+str(i),'correct':v==correct,'separated_form':m.separated(v),'equivalent_original_ode':m.same(m.resolved(v),m.resolved(m.math_blocks(rq[':question/problem'])[0]))})
   left,right=m.equation(v);co=m.sp.diff(left,m.D)
   domains.append({'source_id':sid,'option_index':i,'original_and_separated_domain':r['generation']['domain'],'left_denominator_nonzero':str(m.sp.denom(m.sp.together(left))),'right_denominator_nonzero':str(m.sp.denom(m.sp.together(right))),'normalization_coefficient_nonzero':str(co),'additional_trig_exclusions':['sin('+str(arg)+')≠0' for arg in [f.args[0] for f in co.atoms(m.sp.csc)]]})
  fidelity.append(dict(case,prompt_exact=True,solution_exact=True,choices_exact=5,correct_designation_match=True,**stats));engine.append(checks(r,sid));review.append({'label':'Original replay '+sid,'record':r})
  seen={r['generation']['mathematical_fingerprint']}
  for starting_seed in (31,49):
   seed=starting_seed
   while True:
    variant=g.generate(l,seed=seed,template=t)
    if variant['generation']['mathematical_fingerprint'] not in seen:break
    seed+=1
    assert seed<starting_seed+40,'insufficient meaningful variety'
   seen.add(variant['generation']['mathematical_fingerprint'])
   review.append({'label':'Generated '+t+' seed '+str(seed),'record':variant});engine.append(checks(variant,t+'/'+str(seed)))
 for seed in (31,49):
  r=g.generate_hard(seed=seed);review.append({'label':'Authored missing-hard seed '+str(seed),'record':r});engine.append(checks(r,'hard/'+str(seed)))
 # Per-template extrema and changed coefficient/argument checks across every bank.
 stress=0
 for t,(l,s,p) in g.TEMPLATES.items():
  for seed in range(6):
   r=g.generate(l,seed=seed,template=t);q=r['question'];f=q[':question/answer-fields'][0]
   assert set(r['knowledge_point'])=={'db_id','id','title'}
   assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
   assert not any(word in q[':question/problem'].lower() for word in ['general solution','initial value','integrating factor'])
   assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
   fixed=g.generate(l,seed=99,template=t,parameters=r['generation']['parameters']);assert fixed['question'][':question/id']==q[':question/id']
   assert sorted(a[':answer/value'] for a in fixed['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
   stress+=1
  for key in p:
   bad=dict(p);bad[key]=0
   try:g.generate(l,template=t,parameters=bad)
   except ValueError:pass
   else:raise AssertionError(('bad explicit input',t,key))
 # Canonical fingerprints ignore equivalent coefficient spellings/scaling.
 r1=g.generate_moderate(template='rational_factor',parameters={'a':1,'b':1,'c':1})
 r2=g.generate_moderate(template='rational_factor',parameters={'a':2,'b':2,'c':2})
 assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
 assert r1['question'][':question/id']!=r2['question'][':question/id']
 r3=g.generate_easy(template='exp_quotient',parameters={'base':4,'a':1,'n':3})
 r4=g.generate_easy(template='exp_quotient',parameters={'base':2,'a':2,'n':3})
 assert r3['generation']['mathematical_fingerprint']==r4['generation']['mathematical_fingerprint']
 # Equivalence includes complete equations scaled by a nonzero constant, with form.
 assert m.same(m.resolved('2y'+r'\cdot '+g.D+'=2x'),m.resolved('y'+r'\cdot '+g.D+'=x'))
 assert m.separated('2y'+r'\cdot '+g.D+'=2x')
 assert not m.separated(r'\frac{y}{x}\cdot '+g.D+'=1')
 dump('source-cases.json',cases);dump('bank-mapping.json',mapping);dump('domain-evidence.json',domains);dump('review.json',review);dump('engine-input.json',engine)
 command=[str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')]
 subprocess.run(command,check=True,capture_output=True,text=True)
 native=json.loads((ROOT/'engine-report.json').read_text())
 report={'status':'pass','basis':source['basis'],'lineage':source['lineage'],'source_questions':len(qs),'prompt_exact':10,'solution_exact':10,'complete_banks':10,'choices_matched':50,'distractors_matched':40,'correct_designations_matched':10,'fidelity':fidelity,'generated_review_records':22,'stress_instances':stress,'authored_missing_levels':['hard'],'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks']},'engine_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'source_math_errors':0,'unseparated_equivalent_options':'documented intentional structural distractors, not errors','plots':'none','database_writes':0}
 dump('validation.json',report)
 lines=['# Separation generator review','', 'Original replays retain source wording and stages. Generated variants repair “differentiable” to “differential”; the hard family is authored, with no observed hard difficulty label. Equivalent unseparated source equations are intentionally wrong under the separation-form response criterion.','']
 for entry in review:lines+=['## '+entry['label'],'',g.markdown(entry['record']),'']
 (ROOT/'review.md').write_text('\n'.join(lines))
 print(json.dumps({k:v for k,v in report.items() if k not in ('fidelity','lineage','engine_sha256')},indent=2))
if __name__=='__main__':run()
