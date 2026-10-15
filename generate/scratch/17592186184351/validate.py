#!/usr/bin/env python3
"""Private independent rendered-math, source, bounded-domain and native checks."""
import collections, copy, functools, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('generator17592186184351',HERE.with_suffix('.py'))
p=module('independent_scalar',HERE/'reference/separable-ode-parser.py')
x,z,u=p.p.x,p.p.z,p.p.u
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
@functools.lru_cache(maxsize=16000)
def scalar(raw):return p.scalar(raw.strip().rstrip('.,'))
@functools.lru_cache(maxsize=16000)
def derivative(F,var):
 logs={node:s.Dummy('real_log_absolute_'+str(i)) for i,node in enumerate(s.preorder_traversal(F)) if node.func==s.log and node.args[0].func==s.Abs}
 held=F.xreplace(logs);result=s.diff(held,var)
 for node,symbol in logs.items():
  inner=node.args[0].args[0]
  result+=s.diff(held,symbol)*s.diff(inner,var)/inner
 return result.xreplace({symbol:node for node,symbol in logs.items()})
@functools.lru_cache(maxsize=24000)
def reduced(expr):return s.simplify(s.powdenest(expr,force=False))
@functools.lru_cache(maxsize=24000)
def simple(expr,U,var):
 # After differentiation, replace the source exponential with a positive
 # coordinate. Negative-shift roots are checked on U>0, not outside domain.
 positive=s.Symbol('_domain_u',positive=True)
 exponentials=[node for node in s.preorder_traversal(U) if node.func==s.exp or node.is_Pow and node.exp.has(var) and not node.base.has(var)]
 if exponentials:
  E=exponentials[0];rest=s.simplify(U-E)
  if not rest.has(var):expr=expr.subs(E,positive-rest)
 return reduced(expr)
def equal(a,b,U,var):
 difference=a-b
 if difference==0:return True
 # The derivative-ratio U has U(0)=1, so its real logarithm is analytic on
 # an open interval about zero for every supported k,c. A nonzero exact
 # derivative jet there proves inequality without forcing log(abs(U)) into
 # a complex logarithm on negative-denominator intervals.
 E=[node for node in s.preorder_traversal(U) if node.func==s.exp]
 if E and (U-E[0]).has(var) and U.subs(var,0)==1:
  jet=difference
  for _ in range(3):
   witness=s.simplify(jet.subs(var,0))
   if witness.is_zero is False:return False
   jet=derivative(jet,var)
 return simple(difference,U,var)==0
def read_integral(raw):
 raw=raw.strip().rstrip('.,').replace(r'\text{d}','d').replace(r'\,','').replace(r'\cdot','*')
 m=re.fullmatch(r'(.*?)\\int\s*(.*?)\s*d([xzu])',raw,re.S)
 assert m,('Unrecognized actual integral',raw)
 prefix=m[1].strip().rstrip('*');coef=scalar(prefix) if prefix else s.Integer(1)
 return coef*scalar(m[2].rstrip('*')),{'x':x,'z':z,'u':u}[m[3]]
def control(text):assert not any(ord(c)<32 and c not in '\n\t\r' for c in text),'C0 control byte'
def check(r):
 q=r['question'];meta=r['generation'];name=meta['template'];sid=g.TEMPLATES[name]
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 prompt=q[':question/problem'];control(prompt)
 raw=next(v for v in p.blocks(prompt) if r'\int' in v).replace(r'\displaystyle','')
 integrand,var=read_integral(raw)
 f,=q[':question/answer-fields'];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 bank=f[':answer-field/choices'];assert len(bank)==5 and len({a[':answer/id'] for a in bank})==5
 values=[]
 for a in bank:
  control(a[':answer/value']);assert a[':answer/type']==':answer.type/math'
  values.append(scalar(re.sub(r'\+\s*C\s*$', '',a[':answer/value'])))
 complete=meta['eligible_for_learning']
 if complete:
  sol=q[':question/worked-solution'];control(sol);g.mf.validate_generated_record(r)
  block=next(v for v in p.blocks(sol) if re.match(r'\s*u\s*=',v));U=scalar(block.split('=',1)[1])
  # Reconstruct the displayed substitution and every displayed primitive, not
  # generator internal symbolic values or answer positions.
  correct=[i for i,v in enumerate(values) if equal(derivative(v,var),integrand,U,var)]
  assert len(correct)==1,(name,meta['parameters'],'No unique mathematical primitive',correct)
  assert bank[correct[0]][':answer/id']==f[':answer-field/correct'][1],'Incorrect field designation'
  for i,a in enumerate(values):
   for b in values[i+1:]:assert not equal(derivative(a-b,var),0,U,var),'Bank collision modulo C'
  # Canonical, reordered/equivalent, constant-shift equivalent and ordinary
  # wrong primitive checks under the actual antiderivative response criterion.
  v=values[correct[0]]
  assert equal(derivative(v+7,var),integrand,U,var)
  assert equal(derivative(s.together(v),var),integrand,U,var)
  assert not equal(derivative(v+var,var),integrand,U,var)
  assert not equal(derivative(v-var,var),integrand,U,var)
  # Read the du/dvariable derivative displayed before the substitution arrow.
  derivative_block=next(b for b in p.blocks(sol) if r'\frac{\text{d}u}' in b)
  cleaned=p.clean(derivative_block)
  rhs=cleaned.split('=',1)[1].split('⟹',1)[0].strip().rstrip(r'\,')
  for part in rhs.split('='):
   assert equal(scalar(part),derivative(U,var),U,var),'Wrong displayed substitution derivative/factorization'
  proportional=cleaned.split('⟹',1)[1].replace(r'\,','').strip().rstrip('.')
  differential=re.fullmatch(r'(.*?)\\text\{d\}u=(.*?)\\text\{d\}([xz])',proportional,re.S)
  assert differential,('Unrecognized proportional differential',proportional)
  scalar_multiplier=scalar(differential[1]) if differential[1].strip() else s.Integer(1)
  assert {'x':x,'z':z}[differential[3]]==var,'Stale integration variable'
  assert equal(scalar_multiplier*derivative(U,var),scalar(differential[2]),U,var),'Wrong displayed du proportional relation'
  stage_rows=[]
  for block in p.blocks(sol):
   if r'\begin{aligned}' not in block or r'\int' not in block:continue
   for row in p.clean(block).split(r'\\'):
    if '=' not in row:continue
    lhs,rhs=row.split('=',1);rhs=rhs.strip().rstrip('.,');rhs=re.sub(r'\+\s*C\s*$', '',rhs)
    if r'\int' in rhs:
     val,vvar=read_integral(rhs)
     d=val.subs(u,U)*derivative(U,var) if vvar==u else val
    else:
     val=scalar(rhs);d=derivative(val,u).subs(u,U)*derivative(U,var) if val.has(u) else derivative(val,var)
    assert equal(d,integrand,U,var),(name,meta['parameters'],'Invalid displayed stage',row,d,integrand)
    if lhs.strip():
     lval,lvar=read_integral(lhs)
     ld=lval.subs(u,U)*derivative(U,var) if lvar==u else lval
     assert equal(ld,integrand,U,var),'Stale integral LHS'
    stage_rows.append(row)
  assert len(stage_rows)=={'positive_integer_power':5,'natural_positive_root':6,'base_inverse_root':5,'shifted_base_positive_root':8,'derivative_ratio':4,'base_ratio_linear_bank':6,'base_ratio_log_bank':6,'shifted_base_inverse_root':4}[name]
  # Independent source stage obligations, beyond row counts or equality. A
  # power-form row cannot replace the source's preceding root-form row.
  required={
   'positive_integer_power':{0:[r'\cdot'],1:[r'\int {u}^{3}'],2:[r'\int {u}^{3}'],3:[r'\frac{{u}^{4}}{4}']},
   'natural_positive_root':{0:[r'\cdot'],1:[r'\sqrt{u}'],2:[r'{u}^{1/2}'],3:[r'{u}^{3/2}'],4:[r'\sqrt{{u}^{3}}']},
   'base_inverse_root':{0:[r'\cdot'],1:[r'\frac{1}{\sqrt{u}}'],2:[r'{u}^{-1/2}'],3:[r'{u}^{1/2}',r'(\frac{1}{2})']},
   'shifted_base_positive_root':{0:[r'\cdot'],1:[r'\cdot'],2:[r'\sqrt{u}',r'\cdot'],3:[r'{u}^{1/2}'],4:[r'{u}^{3/2}',r'(\frac{3}{2})'],5:[r'\frac{2}{3}'],6:[r'\sqrt{{u}^{3}}']},
   'derivative_ratio':{0:[r'\cdot'],1:[r'\frac{1}{u}',r'\cdot'],2:[r'|u|'],3:['|']},
   'base_ratio_linear_bank':{0:[r'\cdot'],1:[r'\frac{1}{u}',r'\cdot'],2:[r'\int \frac{1}{u}'],3:[r'|u|'],4:['|']},
   'base_ratio_log_bank':{0:[r'\cdot'],1:[r'\frac{1}{u}',r'\cdot'],2:[r'\int \frac{1}{u}'],3:[r'|u|'],4:['|']},
   'shifted_base_inverse_root':{0:[r'\frac{1}{\sqrt{u}}',r'\cdot'],1:[r'\int u^{-1/2}'],2:[r'\sqrt{u}']}
  }[name]
  for index,fragments in required.items():
   actual_rhs=stage_rows[index].split('=',1)[1]
   assert all(fragment in actual_rhs for fragment in fragments),('Operative stage replaced',name,index,actual_rhs)
 else:
  assert sid=='q-113876' and ':answer-field/correct' not in f and ':question/worked-solution' not in q and ':question/difficulty' not in q
 return r
def native(label,r):
 f=r['question'][':question/answer-fields'][0];ref=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ref else 'rejected','purpose':'actual radio whole-bank canonical/right and ordinary wrong choices'} for a in f[':answer-field/choices']]}
def source_fidelity(sid,r):
 q=r['question'];o=g.SOURCES[sid];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0]
 for k in (':question/problem',':question/worked-solution'):
  assert q.get(k)==o.get(k),(sid,k,'Full source mask mismatch')
 assert (':question/difficulty' in q)==(':question/difficulty' in o)
 if ':question/difficulty' in o:assert q[':question/difficulty']==o[':question/difficulty'][':db/ident']
 assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
 assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
 if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
 return {'source_id':sid,'prompt':True,'worked_solution':':question/worked-solution' in o,'bank_values_matched':5,'complete_bank_matched':True,'correct_ref':':answer-field/correct' in of}
def reject(call):
 try:call()
 except (ValueError,AssertionError,KeyError):return
 raise AssertionError('Mutation incorrectly passed')
def main():
 fidelity=[];sourcecases=[];review=[];native_inputs=[];bounded=[];capacity={};slots={};fingerprints=set()
 for sid,o in g.SOURCES.items():
  name=g.STYLE[sid];level=g.DIFFICULTY[sid];params=g.ANCHORS[sid];r=check(g.generate(level,template=name,parameters=params,profile='observed:'+sid))
  fidelity.append(source_fidelity(sid,r));sourcecases.append({'source_id':sid,'template':name,'parameters':params,'profile':'observed:'+sid,'level':level,'record':r,'level_origin':'observed' if ':question/difficulty' in o else 'authored API placement only; raw unrated attribute absent'})
  normal=check(g.generate(level,template=name,parameters=params,profile='completed:'+sid));changed=next(p for p in reversed(g.parameters_for(name)) if p!=params);variant=check(g.generate(level,template=name,parameters=changed,profile='completed:'+sid))
  review.append({'source_id':sid,'original':o,'source_replay':r,'normal_anchor':normal,'changed_parameters':variant})
 for name,sid in g.TEMPLATES.items():
  print('Checking complete bounded domain:',name,flush=True)
  level=g.DIFFICULTY[sid];count=0;observed_slots=collections.defaultdict(set)
  for i,params in enumerate(g.parameters_for(name)):
   r=check(g.generate(level,i,template=name,parameters=params));bounded.append(r);native_inputs.append(native(name+'-'+str(i),r));count+=1
   for k,v in params.items():observed_slots[k].add(v)
   fp=r['generation']['mathematical_fingerprint'];fingerprints.add(fp)
   assert r['question'][':question/id']==g.generate(level,i+99,template=name,parameters=params)['question'][':question/id']
  capacity[name]=count;slots[name]={k:sorted(v) for k,v in observed_slots.items()}
  if name in g.OPAQUE:
   for i,params in enumerate(g.parameters_for(name)):
    empirical=check(g.generate(level,i,template=name,parameters=params,profile='completed:'+sid))
    native_inputs.append(native('empirical-'+name+'-'+str(i),empirical))
 sampled={}
 for level in g.LEVELS:
  records=[check(g.generate(level,seed)) for seed in range(160)];families=collections.Counter(r['generation']['template'] for r in records)
  assert set(families)==set(g.level_templates(level));sampled[level]=dict(families)
 # Keep ownership diagnostics independent of mathematical and valid radio
 # evidence; no claim that radios accept typed equivalent TeX submissions.
 diag=[]
 for r in bounded[:1]:
  a=copy.deepcopy(r);f=a['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
  diag.append({'label':'radio-wrong-interface','record':a,'checks':[{'submitted':'10000','expected':'unresolved','purpose':'foreign entity rejected by field ownership'},{'submitted':'x+1','expected':'unresolved','purpose':'radio requires choice identity; not a typed-math field'}]})
 r=copy.deepcopy(bounded[0]);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(r'\cdot','',1)
 # Removal of a visible multiplication sign is mathematically equivalent and
 # preserves the same stage; deleting the substitution row does not.
 mutant=copy.deepcopy(bounded[0]);mutant['question'][':question/worked-solution']=mutant['question'][':question/worked-solution'].replace(r'\int {u}^{3}',r'\int {u}^{2}')
 reject(lambda:check(mutant))
 mutant=copy.deepcopy(bounded[0]);mutant['question'][':question/problem']+='\x0c';reject(lambda:check(mutant))
 root_record=next(r for r in bounded if r['generation']['template']=='natural_positive_root')
 mutant=copy.deepcopy(root_record);mutant['question'][':question/worked-solution']=mutant['question'][':question/worked-solution'].replace(r'\sqrt{u}',r'{u}^{1/2}',1);reject(lambda:check(mutant))
 reject(lambda:g.generate('easy',template='positive_integer_power',parameters=dict(a=3,k=3,b=2)))
 reject(lambda:g.generate('hard',template='derivative_ratio',parameters=dict(k=0,c=1)))
 save('source-cases.json',sourcecases);save('review.json',review);save('bounded-records.json',bounded);save('native-input.json',native_inputs);save('ownership-input.json',diag)
 engine=HERE/'reference/check-engine';assert hashlib.sha256(engine.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 subprocess.run([str(engine),str(HERE/'ownership-input.json'),str(HERE/'ownership-report.json')],check=True)
 nr=json.loads((HERE/'native-report.json').read_text());save('capacity.json',{'complete_bounded_domain':capacity,'by_level':{level:len({r['generation']['mathematical_fingerprint'] for r in bounded if r['question'][':question/difficulty']==':question.difficulty/'+level}) for level in g.LEVELS},'distinct_mathematical_prompts':len(fingerprints),'distinct_bounded_profile_records':len(bounded),'slot_coverage':slots,'default_sampler_coverage':sampled,'question_identity_deterministic':True,'capacity_basis':'distinct substituted functions/proportional scales; repeated base-ratio bank profiles, authored choice banks and cosmetic order do not add mathematical capacity'})
 save('validation.json',{'status':'passed','database_writes':0,'basis':g.CAPTURE['basis'],'source_fidelity':fidelity,'source_prompts':8,'source_solutions':7,'complete_source_banks':8,'source_values_matched':40,'source_distractors_matched':32,'source_correct_references':7,'source_missing_ref_and_solution':1,'bounded_instances':len(bounded),'native_accepted_checks':nr['accepted_checks'],'native_rejected_checks':nr['rejected_checks'],'native_unresolved_checks':nr['documented_unresolved_checks'],'rendered_math':'every prompt integrand, all five choices modulo C, displayed du derivative/factorization/proportional relation and every ordered integration row differentiated independently over the declared domain; explicit operative-stage obligations','equivalence_probes':4*len(bounded),'actual_field_contract':'all radio; canonical and wrong choice identities checked, typed equivalent math is not its input contract','ownership_diagnostics':'separate ownership-report.json','mutation_regressions':5,'python':sys.version.split()[0],'sympy':s.__version__,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'mutable_dependencies':False})
 lines=['# Source and generated review','']
 for row in review:
  lines+=['## '+row['source_id'],'','### Original source','',''+row['original'][':question/problem'],'',row['original'].get(':question/worked-solution','(Source has no worked solution.)'),'','### Served anchor','',g.markdown(row['normal_anchor']),'','### Changed parameters','',g.markdown(row['changed_parameters']),'']
 (HERE/'review.md').write_text('\n'.join(lines))
 print('Passed',len(bounded),'bounded cases;',nr['accepted_checks'],'accepted and',nr['rejected_checks'],'rejected native checks')
if __name__=='__main__':main()
