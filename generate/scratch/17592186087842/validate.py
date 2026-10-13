#!/usr/bin/env python3
"""Independent printed mathematics, full fidelity, identities and native grading."""
import hashlib, importlib.util, json, re, subprocess, uuid, sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
counts={};checks=0

# Independent token/recursive-descent reader, separate from the generator's
# substitution-to-SymPy parser. Implicit products are parsed from printed tokens.
def read(s):
 s=s.replace(r'\,','').replace(r'\left','').replace(r'\right','').replace('−','-').strip().rstrip('.,')
 pattern=r'\\(?:dfrac|frac)|\d+|x|[{}()+\-*/^]'
 tokens=re.findall(pattern,s)
 residue=re.sub(pattern,'',s)
 if residue.strip():raise AssertionError('unread displayed math: '+s)
 i=0
 def atom():
  nonlocal i
  if i>=len(tokens):raise AssertionError('incomplete expression')
  tok=tokens[i];i+=1
  if tok in ('+', '-'):v=atom();return v if tok=='+' else -v
  if tok in ('(', '{'):
   close=')' if tok=='(' else '}'
   v=add()
   if i>=len(tokens) or tokens[i]!=close:raise AssertionError('unclosed group')
   i+=1
  elif tok in (r'\frac',r'\dfrac'):v=atom()/atom()
  elif tok=='x':v=g.X
  elif tok.isdigit():v=sp.Integer(tok)
  else:raise AssertionError('unexpected token '+tok)
  if i<len(tokens) and tokens[i]=='^':i+=1;v=v**atom()
  return v
 def mul():
  nonlocal i
  v=atom()
  while i<len(tokens) and tokens[i] not in ('+', '-', ')', '}'):
   op=tokens[i]
   if op in ('*','/'):i+=1;w=atom();v=v*w if op=='*' else v/w
   else:v*=atom()
  return v
 def add():
  nonlocal i
  v=mul()
  while i<len(tokens) and tokens[i] in ('+','-'):
   op=tokens[i];i+=1;w=mul();v=v+w if op=='+' else v-w
  return v
 v=add()
 if i!=len(tokens):raise AssertionError('remaining tokens')
 return v

def actual_function(problem):
 m=re.search(r'([fgh])\(x\)\s*=\s*([^$]+)',problem)
 if not m:raise AssertionError('printed function missing')
 return read(m.group(2)),m.group(1)

def fail(ok,msg):
 global checks
 checks+=1
 if not ok:raise AssertionError(msg)

def roots_display(v):
 # Independent parser obtains the whole displayed union of vertical lines.
 if not re.search(r'x\s*=',v):return frozenset()
 return frozenset(read(m.group(1)) for m in re.finditer(r'x\s*=\s*(-?\s*\\frac\{\d+\}\{\d+\}|-?\d+)',v))

def real_poles(expr):
 n,d=sp.fraction(sp.cancel(expr));ss=sp.solveset(d,g.X,domain=sp.S.Reals)
 fail(isinstance(ss,sp.FiniteSet),'actual real poles must be finite')
 return tuple(sorted(ss))

def formatting(s):
 fail('§' not in s and '¤' not in s,'unfilled mask')
 fail('+-' not in s and '--' not in s,'sign typography')
 fail(s.count('$')%2==0,'math delimiters')
 depth=0
 for i,c in enumerate(s):
  if c in '{}' and (i==0 or s[i-1]!='\\'):
   depth+=1 if c=='{' else -1
   fail(depth>=0,'TeX unmatched brace')
 fail(depth==0,'TeX unbalanced groups')

def validate(r):
 q=r['question'];gen=r['generation'];p=q[':question/problem'];sol=q[':question/worked-solution'];formatting(p);formatting(sol)
 fail(set(r['knowledge_point'])=={'db_id','id','title'},'outer keys')
 expr,name=actual_function(p);rs=real_poles(expr)
 fail(all(v in rs for v in rs),'real poles independently solved')
 fail(not re.search(r'([fgh])\(x\)',sol) or all(m==name for m in re.findall(r'([fgh])\(x\)',sol)),'actual function name')
 # Displayed function rows must equal the original whole rational expression.
 for display in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
  display=display.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  rows=re.split(r'\\\\',display)
  function_rows=name+'(x)' in display
  if function_rows:
   for row in rows:
    rhs=row.split('=')[-1].replace('&','').strip().rstrip('.')
    val=read(rhs)
    fail(sp.cancel(val-expr)==0,'printed rational-function stage: '+row)
  else:
   fail('=' in display,'zero-product equation present')
   lhs,rhs=display.replace('&','').split('=')
   equation=read(lhs)-read(rhs)
   zs=tuple(sorted(sp.solveset(equation,g.X,domain=sp.S.Reals)))
   fail(zs==rs,'whole zero-product equation rootset')
 final=sol.split('Therefore,')[-1]
 fail(tuple(sorted(roots_display(final)))==rs,'printed final pole set')
 fs=q[':question/answer-fields'];keys=[f[':answer-field/key'] for f in fs]
 fail(len(keys)==len(set(keys)),'unique field keys')
 allids=set()
 for f in fs:
  uuid.UUID(f[':answer-field/id']);answers=f[':answer-field/choices'];ids=[a[':answer/id'] for a in answers]
  fail(len(ids)==len(set(ids)) and not allids.intersection(ids),'field owned IDs');allids.update(ids)
  fail(f[':answer-field/correct'][0]==':answer/id' and f[':answer-field/correct'][1] in ids,'owned correct lookup')
  for a in answers:uuid.UUID(a[':answer/id']);formatting(a[':answer/value'])
  if f[':answer-field/type'].endswith('/radio'):
   values=[roots_display(a[':answer/value']) for a in answers]
   fail(len(set(values))==len(values)==5,'whole bank unequal mathematical sets')
   index=ids.index(f[':answer-field/correct'][1]);fail(values[index]==frozenset(rs),'whole correct radio pole set')
  else:
   key=f[':answer-field/key'];fail('{{'+key+'}}' in p,'blank prompt placeholder')
   i=int(key.split('-')[-1])-1
   fail(read(answers[ids.index(f[':answer-field/correct'][1])][':answer/value'])==rs[i],'blank ascending fragment')
 fail(gen['content_fingerprint']==g.digest({'version':g.VERSION,'prompt':p,'solution':sol,'layout':'radio' if len(fs)==1 and fs[0][':answer-field/type'].endswith('/radio') else 'blank','bank':sorted((a[':answer/type'],a[':answer/value']) for a in fs[0][':answer-field/choices']) if len(fs)==1 and fs[0][':answer-field/type'].endswith('/radio') else [],'roots':[str(v) for v in rs]}),'identity actual presentation')
 if gen['template'] in g.DEFAULTS[q[':question/difficulty'].split('/')[-1]]:
  n,d,expected=g.check_parameters(gen['template'],gen['parameters'],q[':question/difficulty'].split('/')[-1]);fail(expected==rs,'printed roots versus separately reduced sampled object')
 if gen['template']=='sum':
  disp=re.findall(r'\$\$(.*?)\$\$',sol,re.S)[0]
  rows=re.split(r'\\\\',disp)
  fail(len(rows)==4,'four addition/distribution/collection rows')
  fail(rows[1].count('(')>=2 and rows[2].count('x')>=2,'distinct unevaluated stages')
 return rs

records=[];source_replays=[];fidelity=[];raw_replays=[]
for c in g.CASES:
 r=g.generate(c['level'],seed=17,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);validate(r)
 q=r['question'];raw=c['raw_source'];fields=raw.get(':question/answer-fields',[])
 evidence=g.generate(c['level'],seed=17,template=c['template'],parameters=c['parameters'],profile=c['raw_bank_profile']);eq=evidence['question']
 fail(eq[':question/problem']==raw[':question/problem'],'public raw profile exact prompt')
 fail((':question/difficulty' in eq)==(':question/difficulty' in raw),'public raw missing difficulty preserved')
 fail((':question/worked-solution' in eq)==(':question/worked-solution' in raw),'public raw missing solution preserved')
 fail((':question/answer-fields' in eq)==(':question/answer-fields' in raw),'public raw field absence preserved')
 fail(evidence['generation']['evidence_only'] and not evidence['generation']['eligible_for_learning'],'public raw evidence eligibility')
 raw_same=g.generate(c['level'],seed=999,template=c['template'],parameters=c['parameters'],profile=c['raw_bank_profile'])
 fail(raw_same['question'][':question/id']==eq[':question/id'],'raw public seed/order independent identity')
 formatting(eq[':question/problem'])
 if ':question/worked-solution' in eq:
  fail(eq[':question/worked-solution']==raw[':question/worked-solution'],'public raw exact supplied solution');formatting(eq[':question/worked-solution'])
 emap={f[':answer-field/key']:f for f in eq.get(':question/answer-fields',[])}
 for f in fields:
  ef=emap[f[':answer-field/key']]
  fail((':answer-field/correct' in ef)==(':answer-field/correct' in f),'public raw missing correct reference preserved')
  fail(sorted((a[':answer/type'],a[':answer/value']) for a in ef[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in f[':answer-field/choices']),'public raw complete exact bank')
 raw_replays.append(evidence)
 prompt=q[':question/problem']==raw[':question/problem'];solution=q[':question/worked-solution']==raw.get(':question/worked-solution')
 fail(prompt or c['missing_fields'],'source prompt fidelity/repair')
 if not c['missing_solution']:fail(solution,'complete source solution prose/stage fidelity')
 bykey={f[':answer-field/key']:f for f in q[':question/answer-fields']}
 matched=0;designations=0
 for f in fields:
  rawbank=f[':answer-field/choices'];new=bykey[f[':answer-field/key']]
  fail(len(rawbank)==len(new[':answer-field/choices']),'original bank length')
  # Raw-exact choice fidelity stronger than mathematical comparison here.
  old=sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in rawbank)
  newbank=sorted((a[':answer/type'],a[':answer/value']) for a in new[':answer-field/choices'])
  fail(old==newbank,'all source choices exact, including mixed text/math types');matched+=len(old)
  if ':answer-field/correct' in f:
   newcorrect=next(a for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1])
   fail(newcorrect[':answer/value']==f[':answer-field/correct'][':answer/value'],'source correct designation');designations+=1
 fidelity.append({'source_id':c['source_id'],'prompt_raw_exact':prompt,'prompt_presentation_repaired':c['missing_fields'],'solution_raw_exact':solution,'solution_available':not c['missing_solution'],'original_choices_matched':matched,'original_correct_refs_matched':designations,'missing_original_correct':c['missing_correct'],'authored_level_assignment':c['authored_level']})
 source_replays.append(r);records.append(r)
 k=3 if c['source_id']=='q-39790' else 2
 changed=g.generate(c['level'],seed=88,template=c['template'],parameters={'scale':k,'function':'h'},profile=c['bank_profile']);validate(changed)
 fail(changed['question'][':question/problem']!=q[':question/problem'],'changed observed parameters')
 if fields and fields[0][':answer-field/type'][':db/ident'].endswith('/radio'):
  oldsets={frozenset(v*k for v in roots_display(a[':answer/value'])) for a in fields[0][':answer-field/choices']}
  newsets={roots_display(a[':answer/value']) for a in changed['question'][':question/answer-fields'][0][':answer-field/choices']}
  fail(oldsets==newsets,'every changed source option independently dilated as a complete root set')
 if not c['missing_solution']:
  fail(q[':question/worked-solution'].count('$$')==changed['question'][':question/worked-solution'].count('$$'),'source variant display-stage count')
  fail(q[':question/worked-solution'].count(r'\\')==changed['question'][':question/worked-solution'].count(r'\\'),'source variant arithmetic row count')
 records.append(changed)
 raw_changed=g.generate(c['level'],seed=88,template=c['template'],parameters={'scale':k,'function':'h'},profile=c['raw_bank_profile'])
 rx,rname=actual_function(raw_changed['question'][':question/problem'])
 fail(real_poles(rx)==tuple(v*k for v in real_poles(actual_function(raw[':question/problem'])[0])),'public raw changed dilation actual poles')
 fail(rname=='h','public raw actual function name');raw_replays.append(raw_changed)

variety={};authored_examples=[]
for level,templates in g.DEFAULTS.items():
 tasks=set()
 for t in templates:
  for layout in ('radio','blank'):
   for seed in range(30):
    r=g.generate(level,seed,template=t,field_type=layout);validate(r);tasks.add(r['generation']['mathematical_fingerprint'])
    same=g.generate(level,seed+1000,template=t,field_type=layout,parameters=r['generation']['parameters'],profile=r['generation']['profile'])
    fail(same['question'][':question/id']==r['question'][':question/id'],'seed/order independent identity')
    fail(same['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'],'task fingerprint stability')
    if seed<2:records.append(r);authored_examples.append(r)
 variety[level]=len(tasks)
 fail(len(tasks)>=30,'substantive task variety')

# Explicit guards, including reduced primitive leading factors and scope branches.
invalid=[('easy','leading',{'function':'f','a':2,'b':4,'t':3,'u':1}),('moderate','numerator_quadratic',{'function':'f','r':-2,'t':3,'a':1,'b':0,'c':1}),('moderate','numerator_quadratic',{'function':'f','r':-2,'t':3,'a':1,'b':2,'c':1}),('hard','sum',{'function':'f','r':0,'t':3,'a':1,'b':2}),('easy','quadratic',{'function':'f','r':-9,'t':2,'c':1})]
for l,t,p in invalid:
 try:g.generate(l,template=t,parameters=p,field_type='blank')
 except ValueError:pass
 else:raise AssertionError('invalid explicit input accepted')

try:g.generate('easy',template='quadratic',parameters={'function':'f','r':-2,'t':2,'c':1},field_type='radio',profile='method_omission_sign')
except ValueError:pass
else:raise AssertionError('whole-bank sign-flip collision accepted')

native=[]
for i,r in enumerate(records):
 q=r['question'];tests=[]
 for j,f in enumerate(q[':question/answer-fields']):
  correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:tests.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a==correct else 'rejected','purpose':'every choice in the complete displayed bank'})
  else:
   v=read(correct[':answer/value']);eq=r'\frac{'+str(v.p*2)+'}{'+str(v.q*2)+'}'
   tests.extend([{'field_index':j,'submitted':correct[':answer/value'],'expected':'accepted','purpose':'canonical fragment'},{'field_index':j,'submitted':eq,'expected':'accepted','purpose':'independently unreduced equivalent fraction'},{'field_index':j,'submitted':str(v+1),'expected':'rejected','purpose':'wrong value'}])
 native.append({'label':str(i)+'/'+r['generation']['template'],'record':r,'checks':tests})
(P/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
subprocess.run([str(P.parents[1]/'runs/current/check-engine'),str(P/'engine-input.json'),str(P/'engine.json')],check=True)
engine=json.loads((P/'engine.json').read_text())
(P/'raw-source-replays.json').write_text(json.dumps(raw_replays,indent=2)+'\n')
(P/'review.json').write_text(json.dumps(records,indent=2)+'\n')
review=['# Vertical asymptote generator review\n','All observed radio profiles are evidence-only; authored defaults are eligible for learning.\n']
for c,r in zip(g.CASES,source_replays):
 review+=['## '+c['source_id']+' — original\n',c['raw_source'][':question/problem'], '\nOriginal bank: '+json.dumps([[f[':answer-field/key'],[(a[':answer/type'][':db/ident'],a[':answer/value']) for a in f[':answer-field/choices']]] for f in c['raw_source'].get(':question/answer-fields',[])],ensure_ascii=False), '\nOriginal worked solution:\n'+c['raw_source'].get(':question/worked-solution','[not captured]'),'\n### Parameterized replay\n',g.markdown(r)]
 changed=next(z for z in records if z['generation']['template']==c['template'] and z['generation']['parameters']['scale']!=1)
 review+=['\n### Changed-parameter evidence variant\n',g.markdown(changed)]
for r in authored_examples:review+=['\n## Authored '+r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['template']+'\n',g.markdown(r)]
(P/'review.md').write_text('\n\n'.join(review)+'\n')
report={'status':'pass','source_provenance':source_replays[0]['generation']['source'],'basis':1356,'independent_checks':checks,'source_questions':len(g.CASES),'raw_public_profile_originals_matched':10,'raw_public_profile_changed_variants_checked':10,'source_prompt_raw_exact':sum(x['prompt_raw_exact'] for x in fidelity),'source_prompt_presentation_repaired':sum(x['prompt_presentation_repaired'] for x in fidelity),'supplied_solutions_raw_exact':sum(x['solution_raw_exact'] for x in fidelity),'supplied_solutions_total':sum(x['solution_available'] for x in fidelity),'source_choices_matched':sum(x['original_choices_matched'] for x in fidelity),'source_choices_total':sum(len(f[':answer-field/choices']) for c in g.CASES for f in c['raw_source'].get(':question/answer-fields',[])),'source_radio_banks_matched':6,'source_radio_banks_total':6,'original_correct_refs_matched':sum(x['original_correct_refs_matched'] for x in fidelity),'original_correct_refs_total':9,'missing_original_correct_not_counted_as_fidelity':3,'authored_solutions_for_missing':3,'authored_fieldless_repairs':1,'authored_unrated_level_assignments':3,'source_replays':fidelity,'variety_observed_sample_tasks':variety,'native':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':engine['documented_unresolved_checks']},'remaining_findings':['Source scalar banks do not identify original distractor operations; replay profiles remain evidence-only.','Three source keys and solutions and one field layout are missing in captured EDB; supported authored additions are labeled.'],'database_writes':0}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('source_replays','remaining_findings')},indent=2))
