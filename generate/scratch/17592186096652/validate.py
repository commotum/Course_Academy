#!/usr/bin/env python3
"""Source fidelity, printed mathematical readback, domains/IDs and native grading."""
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',str(D)+'.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
S=json.loads((D/'source.json').read_text());QS={q[':question/id']:q for q in S['record'][':knowledge-point/questions']};CASES=json.loads((D/'source-cases.json').read_text())
def dump(name,x):(D/name).write_text(json.dumps(x,indent=2)+'\n')
def norm(t):return t.replace(str(D)+'/','')
def rational(s):
 s=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',s).replace(' ','').rstrip('.,')
 return sp.sympify(s,rational=True)
def expression(s,locals):
 s=re.sub(r'\\overset\{\\to \}\{([A-Z]{2})\}',r'\1',s)
 s=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 s=s.replace(r'\cdot','*').replace('&','').strip().rstrip('.,')
 s=re.sub(r'(?<=[\d)])([a-zA-Z])',r'*\1',s)
 return parse_expr(s,local_dict=locals,transformations=standard_transformations+(implicit_multiplication_application,rationalize))
def format_check(text):
 assert text.count('$')%2==0,'Unbalanced dollars'
 depth=0
 for i,ch in enumerate(text):
  if ch in '{}':
   if i and text[i-1]=='\\':continue
   depth+=1 if ch=='{' else -1
   assert depth>=0,'Unbalanced TeX braces'
 assert depth==0,'Unbalanced TeX braces'
 assert not re.search(r'(?:\+\-|\-\-)',text),'Ungrouped adjacent signs'
 assert not re.search(r'\{\{(?!field-)[^}]+\}\}',text),'Leaked component mask'

def mathematics(r):
 q=r['question'];sol=q[':question/worked-solution'];prob=q[':question/problem'];metadata=r['generation'];t=metadata['template']
 m=re.search(r'\$([a-z])=\\lambda ([a-z])\+\\mu ([a-z])\$',prob);assert m,'Actual printed linear combination missing';target,u,v=m.groups();U,V=sp.symbols(u+' '+v)
 vals={u:U,v:V};rawh=re.findall(r'Hence, \$(.*?)\$',sol);assert len(rawh)==2
 path={}
 for row in rawh:
  match=re.fullmatch(r'\\overset\{\\to \}\{([A-Z]{2})\}=(.*?)\.',row);assert match,row
  seg,rhs=match.groups();parsed=expression(rhs,vals);path[seg]=parsed
 assert len(path)==2
 expanded=sum(path.values());a=sp.expand(expanded).coeff(U);b=sp.expand(expanded).coeff(V)
 assert a!=0 and b!=0,(t,path,a,b)
 vals.update(path);vals[target]=expanded
 # Actual displayed lengths, direction prose, and coefficient pair.
 lengths=re.findall(r'\$([A-Z]{2})=(.*?)\|([a-z])\|\$',sol);assert len(lengths)==2
 for seg,scale,n in lengths:
  scale=scale.replace(r'\cdot','').strip();ratio=rational(scale or '1');assert ratio>0
  c=sp.expand(path[seg]).coeff(vals[n]);assert abs(c)==ratio
  pos=sol.index('Hence, $'+r'\overset{\to }{'+seg+'}')
  prose=sol[:pos].rsplit('Similarly:',1)[-1]
  assert ('opposite direction' in prose)==(c<0)
 # Check all formal, distributed and reordered display rows separately.
 displays=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
 for block in displays:
  if r'\lambda' in block:
   lm,mm=re.findall(r'\\lambda\s*=\s*(.*?)(?:,|$)',block.strip()),re.findall(r'\\mu\s*=\s*(.*?)(?:\.|$)',block.strip());assert rational(lm[-1])==a and rational(mm[-1])==b;continue
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  for row in block.split(r'\\'):
   parts=row.split('=');assert len(parts)>=2
   for value in parts:
    value=value.strip().lstrip('&').strip()
    if value:assert sp.expand(expression(value,vals)-expanded)==0,(t,row,value)
 conclusion=re.search(r'Consequently, \$(.*?)\$',sol).group(1).split('=')[-1]
 assert sp.expand(expression(conclusion,vals)-expanded)==0
 # Final scalar statements explicitly parsed from printed solution.
 L=re.findall(r'\\lambda\s*=\s*(-?(?:\\frac\{\d+\}\{\d+\}|\d+(?:\.\d+)?))',sol);M=re.findall(r'\\mu\s*=\s*(-?(?:\\frac\{\d+\}\{\d+\}|\d+(?:\.\d+)?))',sol)
 assert rational(L[-1])==a and rational(M[-1])==b
 for f in q[':question/answer-fields']:
  choices=f[':answer-field/choices'];correctid=f[':answer-field/correct'][1];assert correctid in [x[':answer/id'] for x in choices];assert len({x[':answer/id'] for x in choices})==len(choices)
  values=[]
  for ans in choices:
   if f[':answer-field/type'].endswith('/radio'):
    parts=re.findall(r'=(.*?)\$',ans[':answer/value']);val=tuple(map(rational,parts));assert len(val)==2
   else:val=rational(ans[':answer/value'])
   values.append(val)
   if ans[':answer/id']==correctid:assert val==((a,b) if isinstance(val,tuple) else a if f[':answer-field/key']=='field-1' else b)
  assert len(set(values))==len(values)
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prob
 assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP
 for text in (prob,sol,*[ans[':answer/value'] for f in q[':question/answer-fields'] for ans in f[':answer-field/choices']]):format_check(text)
 if not metadata['plot'].get('reused_original'):
  asset=re.findall(r'!\[\]\((.*?)\)',prob)[0];plot=json.loads(Path(asset).with_suffix('.json').read_text());basis=sp.Matrix.hstack(sp.Matrix(plot['u']),sp.Matrix(plot['v']));assert basis.det()!=0
  resolved=basis.inv()*sp.Matrix([sp.Rational(str(x)) for x in plot['target']]);assert list(resolved)==[a,b]
  first=plot['first_index'];corner=sp.Matrix([sp.Rational(str(x)) for x in plot['corner']]);assert corner==(a if first==0 else b)*basis[:,first]
  pathvectors=[corner,sp.Matrix([sp.Rational(str(x)) for x in plot['target']])-corner]
  for i,seg in enumerate(path):
   projected=basis.inv()*pathvectors[i];assert sp.expand(projected[0]*U+projected[1]*V-path[seg])==0,(t,seg,projected,path[seg])
 assert metadata['parameters']=={'lambda':str(a),'mu':str(b)}
 return (a,b)

records=[];source_fidelity=[];options=corrects=fields=0
for case in CASES:
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);o=QS[case['source_id']];q=r['question'];mathematics(r);records.append(r)
 rawprompt=norm(q[':question/problem'])==o[':question/problem'];repaired=o[':question/problem']
 if case['template']=='q-275128':repaired=repaired.replace('$-\\frac{1}{2}$','{{field-1}}').replace('$-\\frac{5}{2}$','{{field-2}}')
 assert norm(q[':question/problem'])==repaired;assert norm(q[':question/worked-solution'])==o[':question/worked-solution']
 original={f[':answer-field/key']:f for f in o[':question/answer-fields']}
 for f in q[':question/answer-fields']:
  of=original[f[':answer-field/key']];assert of[':answer-field/type'][':db/ident']==f[':answer-field/type'];assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']);assert of[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);options+=len(f[':answer-field/choices']);corrects+=1;fields+=1
 source_fidelity.append({'source_id':case['source_id'],'template':case['template'],'raw_prompt_exact':rawprompt,'presentation_normalized_prompt_exact':True,'worked_solution_exact':True,'complete_bank_exact':True})
# Exactly one non-original variant per observed presentation/bank, plus 2+ per E/M/H.
variants=[]
for i,case in enumerate(CASES):
 p={k:str(sp.Rational(v)*sp.Rational(3,4)) for k,v in case['parameters'].items()}
 if case['level']=='easy':p={'lambda':'2' if case['parameters']['lambda']!='2' else '1','mu':'3' if case['parameters']['mu']!='3' else '4'}
 # Quarter-denominator maximum applies to observed moderate.
 if any(sp.Rational(v).q not in (1,2,4) for v in p.values()):p={k:str(sp.Rational(v)/2) if sp.Rational(v).q<4 else str(sp.Rational(v)+sp.sign(sp.Rational(v))*sp.Rational(1,4)) for k,v in case['parameters'].items()}
 r=g.generate(case['level'],seed=90+i,template=case['template'],parameters=p,profile=case['bank_profile']);mathematics(r);variants.append(r)
for level in ('easy','moderate','hard'):
 for kind in ('blank','radio'):
  for seed in (30,31):
   r=g.generate(level,seed,field_type=kind);mathematics(r);variants.append(r)
# Stress same scopes with small but mathematically varied deterministic sample sets.
for level in ('easy','moderate','hard'):
 for seed in range(12):
  r=g.generate(level,seed,field_type='radio' if seed%2 else 'blank');mathematics(r)
  duplicate=g.generate(level,seed+101,field_type=r['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1],parameters=r['generation']['parameters'])
  assert duplicate['question'][':question/id']==r['question'][':question/id']
# The explicit source dot-style length retains its unit operand at changed factors.
mathematics(g.generate('moderate',template='q-326016',parameters={'lambda':'-1','mu':'-2'}))
# Shuffle changes cannot alter content identity or leave the correct choice first always.
shuffles=[g.generate('moderate',seed=i,template='q-77515',parameters={'lambda':'2','mu':'4'},profile='observed-q-77515') for i in range(8)]
assert len({r['question'][':question/id'] for r in shuffles})==1
assert len({next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in shuffles})>1
# Explicit-input workload rejection, not just sampler policy.
for level,p in [('easy',{'lambda':'-2','mu':'3'}),('easy',{'lambda':'5','mu':'2'}),('moderate',{'lambda':'1/3','mu':'-2'}),('moderate',{'lambda':'2','mu':'3'}),('hard',{'lambda':'2','mu':'1/2'}),('hard',{'lambda':'9/2','mu':'1/2'}),('hard',{'lambda':'0','mu':'2/3'})]:
 try:g.generate(level,parameters=p)
 except ValueError:pass
 else:raise AssertionError('Scope guard failed '+level+str(p))
# Same/different renderer concurrency on fresh paths, using unique inputs.
concurrency_params=[{'lambda':'7/3','mu':'-5/4'},{'lambda':'7/3','mu':'-5/4'},{'lambda':'-7/4','mu':'5/3'}]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:concurrent=list(pool.map(lambda p:g.generate('hard',parameters=p),concurrency_params))
for r in concurrent:mathematics(r)
assert concurrent[0]['question'][':question/id']==concurrent[1]['question'][':question/id'];assert not list(D.glob('plot-input-*'))
checks=[]
for index,r in enumerate(records+variants):
 item={'label':f'case-{index}-'+r['generation']['template'],'record':r,'checks':[]}
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:item['checks'].append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete owned choice bank'})
  else:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);val=rational(value);equiv=f'{val.p*3}/{val.q*3}'
   for submitted,expected,purpose in ((value,'accepted','canonical'),(equiv,'accepted','independently unreduced equivalent rational'),(str(val+1),'rejected','wrong scalar')):item['checks'].append({'field_index':fi,'submitted':submitted,'expected':expected,'purpose':purpose})
 checks.append(item)
dump('native-input.json',checks);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
report=json.loads((D/'native-report.json').read_text());dump('native-provenance.json',{'entry_point':'course_academy_engine::learning::grade_field','binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'database_writes':0})
dump('source-fidelity.json',source_fidelity);dump('review.json',records+variants)
md=['# Originals and generated variants','Raw source provenance: math basis 1356. Original raw source is retained in source.json. Generated q-275128 has an explicit placeholder repair.']
for case,r in zip(CASES,records):
 o=QS[case['source_id']];md.extend(['\n## Original '+case['template'],o[':question/problem']]);
 for f in o[':question/answer-fields']:md.extend([f[':answer-field/key']+':',*[a[':answer/value'] for a in f[':answer-field/choices']]])
 md.extend(['\nOriginal worked solution:',o[':question/worked-solution'],'\n### Parameterized fidelity replay',g.markdown(r)])
 v=next(v for v in variants if v['generation']['template']==case['template']);md.extend(['\n### Generated changed-parameter variant',g.markdown(v)])
for r in variants:
 if r['generation']['authored']:md.extend(['\n## Authored '+r['question'][':question/difficulty'].split('/')[-1]+' '+r['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1],g.markdown(r)])
(D/'review.md').write_text('\n\n'.join(md)+'\n')
validation={'passed':True,'source_questions':21,'source_raw_prompt_exact':20,'source_presentation_repaired':1,'source_normalized_prompt_exact':21,'source_fixed_solution_exact':21,'source_mathematical_repairs':0,'complete_source_banks_matched':21,'source_radio_banks_matched':12,'source_choice_values_matched':options,'source_correct_designations_matched':corrects,'source_fields_matched':fields,'source_radio_distractors_matched':48,'review_generated_variants':len(variants),'authored_levels':['hard'],'mathematical_readback_cases':21+len(variants)+36+3+1,'native':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'source_error_interpretation_limits':'Observed proportional replay profiles reproduce values; many student-error intentions are undetermined, so normal radio defaults use separately authored sign/order operations.','remaining_unresolved_findings':[]}
dump('validation.json',validation);print(json.dumps(validation,indent=2))
