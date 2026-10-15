#!/usr/bin/env python3
"""Frozen-source replay, exhaustive rendered-math checks and actual native grading."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
g=module('unknown_parameter_generator',HERE.with_suffix('.py'));parser=module('parameter_display_parser',HERE/'display_parser.py')
def write(name,v):(HERE/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def equivalent(a,b):return sp.expand(a-b)==0

def independent(rec):
 q=rec['question'];meta=rec['generation'];level=q[':question/difficulty'].split('/')[-1]
 assert meta['eligible'] and not meta['evidence_only']
 g.fmt.validate_generated_record(copy.deepcopy(rec))
 prompt=q[':question/problem'];xname=re.search(r'in the variable \$([xyzt]),\$',prompt)[1]
 pname=re.search(r'value of \$([pqr])\?\$',prompt)[1]
 X=parser.SYMBOLS[xname];P=parser.SYMBOLS[pname]
 assert xname!=pname and '$'+pname+'$ is a constant' in prompt
 pb=parser.blocks(prompt);assert len(pb)==1
 left,right=parser.equation(pb[0]);assert not right.free_symbols and right!=0
 polynomial=sp.Poly(sp.expand(left),X);assert polynomial.degree()==1 and polynomial.coeff_monomial(1)==0
 coefficient=polynomial.coeff_monomial(X);poly=sp.Poly(coefficient,P)
 assert poly.degree()==1 and not (coefficient.free_symbols-{P})
 c=poly.coeff_monomial(P);s=sp.cancel(poly.coeff_monomial(1)/c);target=-s
 assert c!=0 and c.is_Integer and s.is_Integer and right.is_Integer
 p={'c':int(c),'s':int(s),'b':int(right)}
 assert p==meta['parameters'],'Rendered givens disagree with sampled parameters'
 assert (level=='easy' and s==0 and abs(c)>=2) or (level=='moderate' and c==1 and s!=0) or (level=='hard' and abs(c)>=2 and s!=0)
 g.parameters(level,p)
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 options=[parser.value(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(options)==5 and len(set(options))==5
 refs=[a[':answer/id'] for a in f[':answer-field/choices']];assert len(set(refs))==5 and f[':answer-field/correct'][0]==':answer/id'
 assert refs[options.index(target)]==f[':answer-field/correct'][1] and options.count(target)==1
 # Independent contradiction/unique-solution test of the whole displayed equation
 # for EVERY member of the bank, including wrong answers with plausible signs.
 for v in options:
  av=coefficient.subs(P,v)
  if v==target:assert av==0 and right!=0
  else:assert av!=0 and equivalent(left.subs({P:v,X:right/av}),right)
 sol=q[':question/worked-solution'];assert f'form $a{xname}=b.$' in sol and f'Solving this for ${pname},$' in sol
 assert '$b\\ne 0.$' in sol and '$a=0,$' in sol
 sb=parser.blocks(sol);assert len(sb)==4
 aa,bb=parser.equation(sb[0]);assert aa==parser.SYMBOLS['a']*parser.SYMBOLS['x'] and bb==parser.SYMBOLS['b']
 assignments=sb[1].replace(r'\,','').rstrip('.').split(',');assert len(assignments)==2
 a1,a2=parser.equation(assignments[0]);b1,b2=parser.equation(assignments[1])
 assert a1==parser.SYMBOLS['a'] and equivalent(a2,coefficient) and b1==parser.SYMBOLS['b'] and equivalent(b2,right)
 condition,zero=parser.equation(sb[2]);assert equivalent(condition,coefficient) and zero==0
 rr=parser.rows(sb[3]);assert len(rr)=={'easy':1,'moderate':2,'hard':4}[level]
 for i,row in enumerate(rr):
  lhs,rhs=parser.equation(row)
  # Check every intermediate complete relation, and preserve ordered operations.
  expected=[P] if level=='easy' else ([P+s,P] if level=='moderate' else [coefficient,P+s,P+s,P])
  assert equivalent(lhs,expected[i]) and equivalent(rhs,target if i==len(rr)-1 else 0),'Wrong displayed intermediate'
  assert equivalent((lhs-rhs).subs(P,target),0) and sp.Poly(sp.expand(lhs-rhs),P).degree()==1
  if level=='hard' and i==1:
   fracs=re.findall(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',row);assert len(fracs)==2
   assert all(parser.value(den)==c for _,den in fracs),'Illegal/stale division multiplier'
   assert equivalent(parser.expression(fracs[0][0]),coefficient) and parser.value(fracs[1][0])==0
 assert meta['mathematical_fingerprint']==g.fingerprint(level,p)
 return {'c':int(c),'s':int(s),'b':int(right),'target':int(target)}

def checks(rec):
 f=rec['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every owned five-choice radio option through native learning::grade_field'} for a in f[':answer-field/choices']]
def native(label,rec):return {'label':label,'record':rec,'checks':checks(rec)}

def negative_controls():
 rec=g.generate('hard',9,profile='q-288143',parameters={'c':-3,'s':4,'b':6});independent(rec)
 tests=[]
 for label,mutate in [
  ('stale prompt shift',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('(q+4)','(q+2)'))),
  ('wrong displayed RHS assignment',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('b=6','b=4'))),
  ('wrong intermediate division denominator',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'\frac{-3(q+4)}{-3}',r'\frac{-3(q+4)}{-2}'))),
  ('stale target key',lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id',r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']])),
  ('stale final parameter value',lambda r:r['question'].__setitem__(':question/worked-solution',re.sub(r'q &\s*=\s*-4', 'q &=-2', r['question'][':question/worked-solution']))),
 ]:
  bad=copy.deepcopy(rec);mutate(bad)
  try:independent(bad)
  except (AssertionError,ValueError):tests.append({'mutation':label,'caught':True,'other_data_held_fixed':True})
  else:raise AssertionError('Negative control escaped: '+label)
 return tests

def main():
 assert g.FROZEN==json.loads((ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186204090.json').read_text())
 engine=ROOT/'generate/runs/current/check-engine';engine_sha=hashlib.sha256(engine.read_bytes()).hexdigest();assert engine_sha=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 replay=[];case_rows=[];mapping=[];native_inputs=[];review=[];coverage={};total=0
 for sid,(level,recipes) in g.PROFILES.items():
  original=g.CASES[sid];p=g.DEFAULTS[sid];raw=g.observed_raw(sid,p)
  assert raw['question']==original and raw['generation']['evidence_only'] and not raw['generation']['eligible']
  rec=g.generate(level,0,profile=sid,parameters=p);independent(rec);q=rec['question'];f=q[':question/answer-fields'][0];old=original[':question/answer-fields'][0]
  assert q[':question/problem']==g.fmt.normalize_prose(original[':question/problem']) and q[':question/worked-solution']==g.fmt.normalize_prose(original[':question/worked-solution'])
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[g.fmt.normalize_tex(a[':answer/value']) for a in old[':answer-field/choices']]
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==old[':answer-field/correct'][':answer/value']
  assert set(old)=={':db/id',':answer-field/choices',':answer-field/correct',':answer-field/id',':answer-field/key',':answer-field/type'} and all(':answer/feedback' not in a for a in old[':answer-field/choices'])
  replay.append({'source_id':sid,'prompt_exact':True,'solution_exact':True,'answer_values_exact':True,'correct_designation':True,'matched_bank':5,'matched_distractors':4,'missing':[],'extra':[],'raw_full_pull_exact':True})
  case_rows.append({'source_id':sid,'level':level,'template':sid,'bank_profile':sid,'parameters':p,'record':original})
  for answer,recipe in zip(old[':answer-field/choices'],recipes):mapping.append({'source_id':sid,'field':'selection','profile':sid,'source_answer_id':answer[':answer/id'],'value':answer[':answer/value'],'recipe':recipe,'interpretation':'observed value-expression pattern; source error mechanism unresolved','reproduces_source':True})
  cs=set();ss=set();bs=set();targets=set();distinct=set()
  for c,s,b in g.domain(level,sid):
   rec=g.generate(level,0,profile=sid,parameters={'c':c,'s':s,'b':b});independent(rec);total+=1
   cs.add(c);ss.add(s);bs.add(b);targets.add(-s);distinct.add(rec['generation']['mathematical_fingerprint']);native_inputs.append(native(sid+' '+str((c,s,b)),rec))
  coverage[sid]={'level':level,'valid_domain_instances':len(g.domain(level,sid)),'substantive_tasks':len(distinct),'multiplier_values':sorted(cs),'shift_values':sorted(ss),'rhs_values':sorted(bs),'target_values':sorted(targets),'target_role':'parameter whose coefficient vanishes; easy target 0 is mathematically forced','eligible_slots_missing':[]}
  varied=next(p for p in g.domain(level,sid) if dict(zip(('c','s','b'),p))!=g.DEFAULTS[sid]);var=g.generate(level,7,profile=sid,parameters=dict(zip(('c','s','b'),varied)))
  review.append('## '+sid+' ('+level+')\n\nSource replay\n\n'+g.markdown(g.generate(level,0,profile=sid,parameters=g.DEFAULTS[sid]))+'\n\nVariant\n\n'+g.markdown(var))
 write('source-cases.json',case_rows);write('choice-recipes.json',mapping);write('source-fidelity.json',{'passed':True,'basis':2275,'lineage':g.FROZEN['lineage'],'sources':replay,'complete_banks_matched':7,'complete_banks_total':7,'distractors_matched':28,'distractors_total':28,'source_errors':[],'presentation_changes':'canonical normalization only; raw full Pulls preserve exact omissions and identities'})
 write('slot-coverage.json',coverage);write('negative-controls.json',negative_controls())
 # Hold equation multiplier and RHS fixed while changing eligible shift/target.
 fixed=[g.generate('hard',0,profile='q-288143',parameters={'c':-3,'s':s,'b':6}) for s in (4,-4)]
 for r in fixed:independent(r)
 assert fixed[0]['generation']['parameters']['c']==fixed[1]['generation']['parameters']['c'] and fixed[0]['generation']['parameters']['b']==fixed[1]['generation']['parameters']['b']
 review.append('## Changed parameter target with multiplier and RHS held fixed\n\n'+'\n\n'.join(g.markdown(r) for r in fixed))
 caps=g.capacity();write('capacity.json',{'counts':caps,'total':sum(caps.values()),'policy':'Mathematical fingerprint ignores letters, seeds, profile, bank/order, and nonzero uniform equation scaling','profile_domains':coverage})
 for lev in g.LEVELS:
  assert len(g.batch(lev,0))==0
  try:g.batch(lev,caps[lev]+1)
  except ValueError:pass
  else:raise AssertionError('Capacity overflow admitted')
  one=g.batch(lev,3,11);assert one==g.batch(lev,3,11)
 for args in [('easy',0,{'c':0,'s':0,'b':3}),('hard',0,{'c':-3,'s':4,'b':0}),('moderate',0,{'c':2,'s':1,'b':4}),('hard',0,{'c':-3,'s':30,'b':6})]:
  try:g.generate(args[0],args[1],parameters=args[2])
  except ValueError:pass
  else:raise AssertionError('Invalid domain admitted')
 for lev in (*g.LEVELS,'all'):
  for form in ('json','markdown'):
   cli=subprocess.run([sys.executable,str(HERE.with_suffix('.py')),'--difficulty',lev,'--count','2','--format',form],check=True,capture_output=True,text=True)
   if form=='json':assert len(json.loads(cli.stdout)['instances'])==2
   else:assert 'Given that this equation has no solution' in cli.stdout
 write('native-input.json',native_inputs)
 subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 # Foreign/malformed response diagnostics are separate from ordinary wrong choices.
 malformed=native('malformed/foreign selection diagnostics',fixed[0]);malformed['checks']=[{'submitted':'','expected':'unresolved','purpose':'empty selection diagnostic'},{'submitted':'999999','expected':'unresolved','purpose':'foreign numeric entity selection diagnostic'},{'submitted':'not-an-id','expected':'unresolved','purpose':'malformed selection diagnostic'}]
 write('native-diagnostic-input.json',[malformed]);subprocess.run([str(engine),str(HERE/'native-diagnostic-input.json'),str(HERE/'native-diagnostics.json')],check=True)
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 write('previews.json',g.batch('all',9,204090))
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'display_parser.py',HERE/'math_format.py',HERE/'source.json',HERE/'topic.json',HERE/'lesson.json',engine)}
 native_report=json.loads((HERE/'native-grading.json').read_text());write('validation.json',{'status':'pass','passed':True,'basis':2275,'supported_levels':list(g.LEVELS),'exhaustive_profile_domain_instances':total,'substantive_capacity':caps,'source_fidelity':{'complete_banks':'7/7','distractors':'28/28','full_raw_Pulls':'7/7'},'native':{'entry_point':native_report['entry_point'],'accepted':native_report['accepted_checks'],'rejected':native_report['rejected_checks'],'unresolved':native_report['documented_unresolved_checks'],'engine_sha256':engine_sha},'negative_controls':5,'equations':'All printed givens, coefficient/RHS assignments, every complete intermediate equation, explicit divisors, all five bank members, parameter conditions and final targets independently read and checked','baseline':'numeric generator did not exist; manifest latest inventory reported has_generator=false at source basis 2275; original files preserved','database_writes':0,'registration_changes':0,'limitations':['Observed distractor mechanisms are unresolved; exact pattern recipes are retained as observed profiles.','Finite integer domain only; no constants on both sides or variables on both sides.'],'hashes':hashes})
 write('freeze.json',{'version':g.VERSION,'generator_sha256':hashes[str(HERE.with_suffix('.py').relative_to(ROOT))],'frozen_runtime':hashes,'validation':'validation.json','status':'working; awaiting root approval QA'})
 print(json.dumps({'validated_profile_domain_instances':total,'capacity':caps,'sha256':hashes[str(HERE.with_suffix('.py').relative_to(ROOT))]}))
if __name__=='__main__':main()
