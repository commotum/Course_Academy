#!/usr/bin/env python3
"""Independent printed-value, stage/prose, full-source and real-native QA.

Parses actual learner strings; does not trust generation parameter mathematics.
Missing original correct refs are not fabricated or counted as designation matches.
"""
import hashlib,importlib.util,json,re,subprocess,sys,copy
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
D=Path(__file__).resolve().parent; ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
src=json.loads((D/'source.json').read_text());qs=src['record'][':knowledge-point/questions'];cases=json.loads((D/'source-cases.json').read_text());byid={q[':question/math-academy-id']:q for q in qs}
y,P,k,a,y0=sp.symbols('y P k a y0',real=True)
LOC={'y':y,'P':P,'k':k,'a':a,'y0':y0,'P0':y0}
TRANS=standard_transformations+(implicit_multiplication_application,rationalize)
def expr(st):
 st=st.strip().rstrip('.,');st=st.replace(r'\,','').replace('^{2}','**2').replace('^','**').replace('{y}_{0}','y0').replace('{P}_{0}','P0').replace('{','').replace('}','')
 assert re.fullmatch(r'[0-9a-zA-Z+\-().* /]+',st),st
 return parse_expr(st,local_dict=LOC,transformations=TRANS)
def option(st):
 m=re.fullmatch(r'\\frac\{d([yP])\}\{dt\}=(.*)',st.replace(' ',''));assert m,st
 v=LOC[m[1]]; parts=m[2].split(r',\,');rhs=expr(parts[0]);initial=None
 if len(parts)==2:
  mm=re.fullmatch(m[1]+r'\(0\)=(.*)',parts[1]);assert mm;initial=expr(mm[1]);assert initial.is_number
 assert len(parts)<=2;return v,sp.expand(rhs),initial

def equivalent(x,z):return x[0]==z[0] and sp.simplify(x[1]-z[1])==0 and x[2]==z[2]
def eligible(o,cap=None):
 v,rhs,n=o
 if sp.degree(rhs,v)!=1:return False
 b=rhs.coeff(v);c=rhs.subs(v,0)
 if not b<0:return False
 equilibrium=-c/b
 if n is not None:return bool(n<equilibrium)
 return sp.simplify(equilibrium-cap)==0

def formatting(st):
 assert st.count('$')%2==0
 # No doubled raw TeX command escapes, bare two-sign arithmetic, unbalanced groups.
 assert '\\\\' not in st
 depth=0
 for ch in st:
  if ch=='{':depth+=1
  if ch=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert '--' not in st and '+-' not in st

def printed_check(r,completed=True):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'};assert r['knowledge_point']['db_id']==g.KP_ID
 prompt=q[':question/problem'];formatting(prompt)
 capmatch=re.search(r'\$y\s*<\s*([0-9.]+)\$',prompt);cap=expr(capmatch[1]) if capmatch else None
 fields=q[':question/answer-fields'];expected_var=y if capmatch or '\\frac{dy}{dt}' in fields[0][':answer-field/choices'][0][':answer/value'] else P
 correctobjects=[]
 for f in fields:
  assert f[':answer-field/type']==':answer-field.type/radio' and len(f[':answer-field/choices'])==5
  objects=[];ids=[]
  for ch in f[':answer-field/choices']:
   formatting(ch[':answer/value']);o=option(ch[':answer/value']);objects.append(o);ids.append(ch[':answer/id']);assert o[0]==expected_var
  assert len(set(ids))==5
  for ix,o in enumerate(objects):
   for z in objects[:ix]:assert not equivalent(o,z),'Equivalent printed options'
  good=[i for i,o in enumerate(objects) if eligible(o,cap)];assert len(good)==1,(prompt,objects,good)
  if ':answer-field/correct' in f:
   ref=f[':answer-field/correct'];assert ref[0]==':answer/id';assert ref[1]==ids[good[0]]
  elif completed:raise AssertionError('Normal field missing correct ref')
  correctobjects.append(objects[good[0]])
 sol=q.get(':question/worked-solution')
 if sol is None:
  assert not completed;return
 formatting(sol)
 co=correctobjects[-1];v,rhs,n=co; b=rhs.coeff(v); c=rhs.subs(v,0);kk=-b;aa=-c/b
 # Actual numerical statements must agree with the printed chosen model.
 for regex,value in [(r'\$k=([^,$]+)',kk),(r'[,\$]a=([^,$]+)',aa),(r'\$\{y\}_\{0\}=([^,$]+)',n),(r'\$\{P\}_\{0\}=([^,$]+)',n)]:
  matches=re.findall(regex,sol.replace(r"\,",""))
  if value is not None and matches:assert expr(matches[0])==value,(regex,matches,value)
 # Every displayed derivative chain is read back and checked term-by-term.
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
 assert len(blocks)==({'factored_equation':2,'expanded_equation':3,'factored_ivp':3}.get(r['generation']['template'],None) or (6 if r['generation']['profile'].endswith('_3') or r['generation']['profile']=='observed_37177' else 5))
 printed_numeric=[]
 for block in blocks:
  first,*init=block.split(r',\,')
  mm=re.match(r'\\frac\{d([yP])\}\{dt\}=(.*)',first.strip().replace(' ',''));assert mm,block
  vv=LOC[mm[1]]; chain=mm[2].split('=');values=[expr(st) for st in chain]
  assert all(sp.simplify(values[0]-z)==0 for z in values[1:]),block
  if not values[0].has(k,a):
   ni=None
   if init:
    mi=re.match(r'[yP]\(0\)=(.*)',init[0].rstrip('.,'));assert mi,init;ni=expr(mi[1])
   cand=(vv,sp.expand(values[0]),ni); printed_numeric.append(cand)
   # Factor-only identification row has no initial component.
   assert any(cand[0]==z[0] and sp.simplify(cand[1]-z[1])==0 and (ni is None or ni==z[2]) for z in [option(ch[':answer/value']) for ch in fields[-1][':answer-field/choices']]),block
  elif completed:assert vv==expected_var,'Generic teaching row uses wrong named variable'
 # Independently check EVERY printed initial/cap numerical inequality.
 for nst,ast in re.findall(r'\$\{[yP]\}_\{0\}=([^>$]+)>a=([^,$]+)',sol.replace(r'\,','')):assert expr(nst)>expr(ast),(nst,ast)
 for m in re.finditer(r'\$y<([0-9.]+)\$',sol):assert expr(m[1])==aa
 assert printed_numeric

native=[];source_results=[];counts={'source_questions':len(qs),'source_banks':0,'source_options':0,'source_distractors_with_designation':0,'source_correct_designations':0,'source_solutions':0,'unrated':0,'missing_correct_refs':0}
raw_records=[]
for case in cases:
 q=byid[case['source_id']];r=g.generate(case['level'],seed=11,template=case['template'],profile=case['bank_profile'],parameters=case['parameters']);raw_records.append(r);printed_check(r,False);gg=r['question']
 assert q[':question/problem']==gg[':question/problem']
 presence_keys=[':question/difficulty',':question/worked-solution',':question/answer-fields']
 for key in presence_keys:assert (key in q)==(key in gg)
 if ':question/difficulty' in q:assert q[':question/difficulty'][':db/ident']==gg[':question/difficulty']
 else:counts['unrated']+=1
 if ':question/worked-solution' in q:assert q[':question/worked-solution']==gg[':question/worked-solution'];counts['source_solutions']+=1
 assert len(q[':question/answer-fields'])==len(gg[':question/answer-fields'])
 for i,(sf,gf) in enumerate(zip(q[':question/answer-fields'],gg[':question/answer-fields'])):
  counts['source_banks']+=1;counts['source_options']+=len(sf[':answer-field/choices'])
  assert sf[':answer-field/key']==gf[':answer-field/key'];assert sf[':answer-field/type'][':db/ident']==gf[':answer-field/type']
  assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
  assert (':answer-field/correct' in sf)==(':answer-field/correct' in gf)
  if ':answer-field/correct' in sf:
   designated=next(ch[':answer/value'] for ch in gf[':answer-field/choices'] if ch[':answer/id']==gf[':answer-field/correct'][1]);assert designated==sf[':answer-field/correct'][':answer/value'];counts['source_correct_designations']+=1;counts['source_distractors_with_designation']+=4
   # Project just the authoritative gradable field; raw legacy missing correct
   # fields cannot be graded by the native application and remain raw evidence.
   projection=copy.deepcopy(r);projection['question'][':question/answer-fields']=[gf];native.append({'label':case['source_id']+f'-original-field-{i}','record':projection,'checks':[{'submitted_answer_id':ch[':answer/id'],'expected':'accepted' if ch[':answer/id']==gf[':answer-field/correct'][1] else 'rejected','purpose':'native original present designation'} for ch in gf[':answer-field/choices']]})
  else:counts['missing_correct_refs']+=1
 source_results.append({'source_id':case['source_id'],'raw_exact_prompt':True,'raw_exact_solution':(':question/worked-solution' in q),'attribute_presence_parity':True,'bank_exact_fields':len(q[':question/answer-fields'])})
 # Replay must actually generalize each profile, not return literal source objects.
 altered=g.generate(case['level'],seed=21,template=case['template'],profile=case['bank_profile']);printed_check(altered,False)
 assert altered['question']!=r['question']

records=[]
for profile,template in g.PROFILES.items():
 for seed in range(25):
  r=g.generate(g.TEMPLATES[template],seed=seed,template=template,profile=profile);printed_check(r,not profile.startswith('observed_'));records.append(r)
  r2=g.generate(g.TEMPLATES[template],seed=seed+1234,template=template,profile=profile,parameters=r['generation']['parameters'])
  assert r['question'][':question/id']==r2['question'][':question/id'];assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
  if not profile.startswith('observed_'):
   native.append({'label':profile+'-'+str(seed),'record':r,'checks':[{'submitted_answer_id':ch[':answer/id'],'expected':'accepted' if ch[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] else 'rejected','purpose':'native generated choice grading'} for ch in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
# Explicit-input guards and lexical-equivalent parameter identities.
invalid=[('easy','factored_equation',{'a':1,'k':1}),('easy','factored_equation',{'a':10,'k':10}),('moderate','expanded_equation',{'a':'2.5','k':2}),('moderate','expanded_equation',{'a':500,'k':21}),('hard','factored_ivp',{'a':250,'k':3,'initials':[200,200,150,50,100]}),('hard','factored_ivp',{'a':250,'k':3,'initials':[200,400,350,50,100]})]
for level,t,p in invalid:
 try:g.generate(level,template=t,parameters=p)
 except ValueError:pass
 else:raise AssertionError('Explicit invalid input admitted')
for level,t in [('easy','factored_equation'),('moderate','expanded_equation')]:
 r=g.generate(level,template=t,parameters={'a':80,'k':5});z=g.generate(level,template=t,parameters={'a':'80.0','k':'5.00'});assert r['question'][':question/id']==z['question'][':question/id']
# Corrupt actual printed math/prose/stages and require the independent checker fail.
r=g.generate('moderate',seed=42);corrupt=copy.deepcopy(r);corrupt['question'][':question/worked-solution']=corrupt['question'][':question/worked-solution'].replace('k=','k=99',1)
try:printed_check(corrupt)
except (AssertionError,ValueError,TypeError):pass
else:raise AssertionError('Prose-corruption readback failed')
corrupt=copy.deepcopy(r);f=corrupt['question'][':question/answer-fields'][0];ch=next(ch for ch in f[':answer-field/choices'] if ch[':answer/id']==f[':answer-field/correct'][1]);ch[':answer/value']=ch[':answer/value'].replace('-','+',1)
try:printed_check(corrupt)
except AssertionError:pass
else:raise AssertionError('Choice-corruption readback failed')
(D/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
review=[]
for profile,template in g.PROFILES.items():
 for seed in [42,73]:review.append(g.generate(g.TEMPLATES[template],seed,template=template,profile=profile))
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
parts=['# Source and generated review','Labels distinguish raw evidence from authored/default questions. Raw records retain source omissions and duplicate legacy fields; grader fixtures only project fields whose original designation exists.']
for case,r in zip(cases,raw_records):parts+=['\n## ORIGINAL '+case['source_id']+' — '+r['question'].get(':question/difficulty','unrated').split('/')[-1]+' — raw parameterized replay',g.markdown(r)]
for r in review:parts+=['\n## GENERATED '+r['generation']['profile']+' / '+g.TEMPLATES[r['generation']['template']]+' / seed '+str(r['generation']['seed']),g.markdown(r)]
(D/'review.md').write_text('\n\n'.join(parts)+'\n')
# Inspect decoded bytes, not JSON repr: source has single TeX command slashes.
strings=[q.get(':question/problem','') for q in qs]+[q.get(':question/worked-solution','') for q in qs]+[a[':answer/value'] for q in qs for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
byte_report={'decoded_strings':len(strings),'adjacent_backslash_pairs':sum(st.count('\\\\') for st in strings),'slash_codepoint':ord('\\'),'string_lengths':[len(st) for st in strings],'source_spacing_anomaly':'q-37180 option 2 has decoded single-backslash thin space in 1\\,23; mathematical value123; preserved raw, ordinary123 authored'}
(D/'decoded-bytes.json').write_text(json.dumps(byte_report,indent=2)+'\n')
nr=json.loads((D/'native-report.json').read_text())
report={'status':'pass','counts':counts,'source_fidelity':source_results,'generated_records_checked':len(records),'profiles_checked':len(g.PROFILES),'source_exact_full_solutions':'5/5 present','source_exact_banks':'7/7','source_exact_options':'35/35','source_present_correct_designations':'5/5;2 missing refs remain missing','unrated_level':'easy authored; raw difficulty absent','normal_source_format_repairs':['q106661 completion (difficulty/solution/correct) authored independently','q106662 legacy duplicated field suppressed in default'],'raw_key_presence':'6/6 questions plus7/7 fields','native':{k:nr[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'native_missing_designation_fields_not_graded':2,'independent_displayed_math_and_prose_readback':True,'mutation_checks':2,'plot_rating':'none','remaining_findings':['Original q106661 has no observed difficulty/solution/correct; cannot count missing designation as matched','Original q106662 duplicated legacy field has no correct ref; preserved raw public replay, suppressed normal','Heterogeneous banks parameterize independent affine IVP objects; original numerical distractor intent not identifiable','q37180 raw option 1\\,23 means123; nonstandard grouping preserved raw and normalized normal'],'database_writes':0}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
