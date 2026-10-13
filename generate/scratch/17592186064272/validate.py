#!/usr/bin/env python3
"""Independent displayed-string mathematics, replay, scope and native grader QA."""
import hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp_rate',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
RAW=json.loads((HERE/'source.json').read_text());SOURCES={q[':question/math-academy-id']:q for q in RAW['record'][':knowledge-point/questions']}
CASES=json.loads((HERE/'source-cases.json').read_text())
qv,dq,iv,lv,rv,dr=sp.symbols('q dq i l r dr')


def normalize(s):
 return s.replace('\\\\frac','\\frac').replace('\\\\cdot','\\cdot').replace('′',"'").replace('\u00a0',' ').replace(' ','')


def atom_expr(s,p):
 """Parse the actual shown component; no generation formula/recipe lookup."""
 s=normalize(s)
 for name,symbol in [(p['Q'],qv),(p.get('I'),iv),(p.get('L'),lv),(p.get('R'),rv)]:
  if name is None:continue
  for derivative in [f'{{{name}}}^{{\'}}({p["T"]})',f'{name}^{{\'}}({p["T"]})',f"{name}'({p['T']})"]:
   s=s.replace(derivative,'dq' if name==p['Q'] else 'dr')
  s=s.replace(f'{{{name}}}^{{2}}({p["T"]})',str(symbol)+'**2')
  s=s.replace(f'{name}({p["T"]})',str(symbol))
 s=s.replace(r'\cdot','*')
 s=re.sub(r'\\frac\{1\}\{([a-z]+)\}',r'(1/\1)',s)
 if not re.fullmatch(r'[a-z0-9()+*\-/]+',s):raise AssertionError('unparsed displayed math '+s)
 return sp.sympify(s,locals={'q':qv,'dq':dq,'i':iv,'l':lv,'r':rv,'dr':dr})


def residual(value,p):
 assert value.count('=')==1
 a,b=value.split('=');return sp.factor(atom_expr(a,p)-atom_expr(b,p))


def equivalent(a,b):
 r=sp.cancel(a/b)
 return r!=0 and not r.free_symbols


def format_check(s):
 assert '@' not in s
 assert s.count('$')%2==0
 depth=0
 for c in s:
  if c=='{':depth+=1
  if c=='}':depth-=1;assert depth>=0
 assert depth==0
 assert '\\\\frac' not in s and '\\\\cdot' not in s


def infer_prompt(prompt,p):
 """Determine correct relation from actual displayed physical rate definitions."""
 Q=p['Q'];T=p['T'];assert f'${Q}({T})$' in prompt
 entries=re.findall(r'- \$([A-Za-z])\(([tus])\)\$[^\n]*',prompt)
 assert len(entries) in (2,3) and entries[0]==(Q,T)
 assert all(t==T for _,t in entries)
 if len(entries)==2:
  name=entries[1][0];assert name==p['R']
  assert 'increasing' in prompt or 'increases' in prompt or 'decreasing' in prompt
  sign=-1 if 'decreasing' in prompt else 1
  return sign*rv,'single' if sign==1 else 'loss'
 assert entries[1][0]==p['I'] and entries[2][0]==p['L']
 assert any(w in prompt for w in ('enter','open an account','added'))
 assert any(w in prompt for w in ('leave','cancel their account','removed','removal'))
 return (iv+lv,'signed') if 'signed contribution' in prompt else (iv-lv,'net')


def independent_check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q,p=r['question'],r['generation']['parameters'];f=q[':question/answer-fields'][0]
 assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio'
 expected,kind=infer_prompt(q[':question/problem'],p)
 sols=q[':question/worked-solution'];format_check(q[':question/problem']);format_check(sols)
 assert 'time interval tends to zero' in sols
 # Check formal operator stage and both function/variable names from the prompt.
 formal=re.search(r'\$\$\s*(.*?)\s*\$\$',sols,re.S).group(1)
 assert f'{p["Q"]}({p["T"]})' in formal
 assert (r'\text{d}'+p['T']) in formal or (r'\textrm{d}'+p['T']) in formal
 assert 'Change in' in formal
 # All algebraic relation stages in the displayed solution are independently read.
 math_spans=re.findall(r'\$\$\s*(.*?)\s*\$\$|\$([^$]*?)\$',sols,re.S)
 checked=0
 for display,inline in math_spans:
  value=display or inline
  if '=' in value and '\\frac' not in value:
   val=value.rstrip('.')
   if val.count('=')==1:
    rr=residual(val,p);assert sp.simplify(rr.subs(dq,expected))==0,(val,expected);checked+=1
 assert checked>=1
 if kind in ('net','signed'):assert len(re.findall(r'\$\$',sols))==4
 else:assert len(re.findall(r'\$\$',sols))==2
 assert ':answer-field/correct' in f and f[':answer-field/correct'][0]==':answer/id'
 assert len(f[':answer-field/choices'])==5
 rs=[];valid=[]
 for a in f[':answer-field/choices']:
  format_check(a[':answer/value']);v=residual(a[':answer/value'],p);rs.append(v)
  # The request is a relationship valid at all times, not a special coincidence.
  truth=sp.simplify(v.subs(dq,expected))==0
  valid.append(truth)
  assert truth==(a[':answer/id']==f[':answer-field/correct'][1])
 assert sum(valid)==1
 for a,b in itertools.combinations(rs,2):assert not equivalent(a,b),(a,b)
 # Dimensional consistency of the correct answer: derivative and supplied rates
 # are amount/time; stock and rate derivative mistakes are distinct dimensions.
 assert kind in ('single','loss','net','signed')
 if 'context' in p:
  assert p['unit']==g.CONTEXTS[p['context']][2]
  assert ('per '+p['unit'][:-1]) in q[':question/problem']
  if kind=='signed':assert f"{p['L']}({p['T']})<0" in q[':question/problem']
 assert str(p['Q'])!=p.get('R') and p['Q']!=p.get('I')
 return checked


def main():
 records=[];coverage=[];raw_values=normalized_values=0;banks=refs=prompts=raw_solutions=0
 for case in CASES:
  sid=case['source_id'];source=SOURCES[sid];r=g.generate(case['level'],11,case['template'],parameters=case['parameters'],profile=case['bank_profile']);independent_check(r);records.append(r)
  q=r['question'];f=q[':question/answer-fields'][0];p=case['parameters']
  assert q[':question/problem']==source[':question/problem'];prompts+=1
  base=q[':question/worked-solution'].removesuffix('\n\n'+g.CLARIFIER)
  original=source.get(':question/worked-solution')
  if original:
   if base==original:raw_solutions+=1
   repaired=original
   if sid=='q-112519':repaired=repaired.replace('inside the park $t$ minutes','inside the playground $t$ hours')
   if sid=='q-72105':repaired=repaired.replace('after $t$ hours','after $t$ minutes')
   assert base==repaired
   assert re.findall(r'\$\$.*?\$\$',base,re.S)==re.findall(r'\$\$.*?\$\$',repaired,re.S)
  fs=source.get(':question/answer-fields',[])
  matches=[]
  if fs:
   assert len(fs)==1
   originals=fs[0][':answer-field/choices'];assert len(originals)==len(f[':answer-field/choices'])
   available=list(f[':answer-field/choices'])
   for a in originals:
    matching=[v for v in available if equivalent(residual(a[':answer/value'],p),residual(v[':answer/value'],p))]
    assert len(matching)==1
    v=matching[0];available.remove(v)
    raw_values+=int(a[':answer/value']==v[':answer/value']);normalized_values+=1;matches.append({'original':a[':answer/value'],'generated':v[':answer/value'],'mathematically_equal':True,'raw_exact':a[':answer/value']==v[':answer/value']})
   assert not available;banks+=1
   if ':answer-field/correct' in fs[0]:
    old=fs[0][':answer-field/correct'][':answer/value'];new=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equivalent(residual(old,p),residual(new,p));refs+=1
  coverage.append({'source_id':sid,'prompt_exact':True,'solution_raw_exact':base==original if original else None,'supported_solution_match':True if original else 'authored canonical-based repair','field_origin':r['generation']['field_origin'],'original_correct_designation_matched':bool(fs and ':answer-field/correct' in fs[0]),'choices':matches,'repairs':r['generation']['repairs']})
 # Every source family and complete source bank gets two changed-parameter examples.
 review=[]
 for case in CASES:
  for seed in (101,209):
   r=g.generate(case['level'],seed,case['template'],profile=case['bank_profile']);independent_check(r);review.append(r)
 # At least two authored samples per level; all authored templates and every context.
 for template,spec in g.TEMPLATES.items():
  if spec.get('source_id'):continue
  for idx,context in enumerate(g.CONTEXTS):
   p={'Q':'V','T':'t','unit':g.CONTEXTS[context][2],'context':context}
   if spec['kind'] in ('single','loss'):p['R']='r'
   else:p.update(I='E',L='L')
   r=g.generate(spec['level'],idx,template,parameters=p);independent_check(r);review.append(r)
 stress=[]
 for template,spec in g.TEMPLATES.items():
  for seed in range(40):
   r=g.generate(spec['level'],seed,template);independent_check(r);stress.append(r)
   r2=g.generate(spec['level'],seed+999,template,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
   assert r['question'][':question/id']==r2['question'][':question/id']
   assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
 # Alias/source profile spelling must not invent mathematical task diversity.
 assert len({r['generation']['mathematical_fingerprint'] for r in stress+review})==4
 # Profile changes may alter identities exactly when the complete displayed bank differs.
 a=g.generate_easy(1,'single_growth',parameters={'Q':'N','R':'r','T':'t','unit':'hours','context':'grain'})
 b=g.generate_easy(1,'single_growth',parameters=a['generation']['parameters'],profile='single_reciprocal')
 assert a['question'][':question/id']!=b['question'][':question/id']
 assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 for p,template,lev in [({'Q':'N','R':'t','T':'t','unit':'hours','context':'grain'},'single_growth','easy'),({'Q':'N','I':'E','L':'E','T':'t','unit':'minutes','context':'water'},'signed_net','hard'),({'Q':'N','I':'E','L':'L','T':'t','unit':'years','context':'water'},'net_magnitudes','moderate')]:
  try:g.generate(lev,template=template,parameters=p)
  except ValueError:pass
  else:raise AssertionError('invalid explicit parameters accepted')
 checks=[]
 for idx,r in enumerate(records+review+stress):
  f=r['question'][':question/answer-fields'][0]
  checks.append({'label':str(idx)+'/'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently verified complete displayed option'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
 engine=HERE.parents[1]/'runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 (HERE/'replay.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
 text=['# Source fidelity and generated peer review','Captured math basis 1356. Originals below are evidence; repaired and authored learner records are labeled.']
 for case in CASES:
  source=SOURCES[case['source_id']];text+=['## Original '+case['source_id'],source[':question/problem'],'### Original complete bank','\n'.join('- $'+a[':answer/value']+'$' for f in source.get(':question/answer-fields',[]) for a in f[':answer-field/choices']) or '(Field missing in capture.)','### Original solution',source.get(':question/worked-solution','(Solution missing in capture.)')]
  for r in review:
   if r['generation']['template']==case['template']:text+=['### Generated peer variant — source-template prose, documented repairs',g.markdown(r)]
 for r in review:
  if not r['generation']['source_ids']:text+=['### Authored level extension — not observed',g.markdown(r)]
 (HERE/'review.md').write_text('\n\n'.join(text)+'\n')
 report={'status':'passed','database_writes':0,'source':g.SOURCE,'source_practice_count':9,'source_prompts_exact':prompts,'source_complete_banks_matched':{'matched':banks,'total':6},'source_options_mathematically_matched':{'matched':normalized_values,'total':30},'source_options_raw_exact':{'matched':raw_values,'total':30},'source_observed_correct_designations_matched':{'matched':refs,'total':5},'missing_correct_designations_supported_repairs':1,'missing_field_supported_repairs':3,'source_solutions_raw_exact_before_clarifier':{'matched':raw_solutions,'total':8},'source_solutions_supported_replay_before_clarifier':{'matched':8,'total':8},'missing_solution_supported_repairs':1,'instantaneous_rate_clarification_appended':True,'coverage':coverage,'generated_reviews':len(review),'stress_questions':len(stress),'independently_checked_complete_displayed_options':5*len(checks),'native_grading':json.loads((HERE/'engine-report.json').read_text()),'finite_semantic_structure_count':4,'unresolved_findings':[],'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 print(f'PASS: {banks}/6 source banks, {normalized_values}/30 choices, {refs}/5 observed correct refs; {len(stress)} stress questions; {len(checks)*5} native option checks')
if __name__=='__main__':main()
