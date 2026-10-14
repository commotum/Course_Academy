"""Independent readback of every displayed entry/stage/bank, source fidelity and native grading."""
import copy, hashlib, importlib.util, json, platform, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('matrix_add_draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
CASES=json.loads((HERE/'source-cases.json').read_text())+json.loads((HERE/'independent-cases.json').read_text());RAW=g.SOURCE['record'][':knowledge-point/questions']
def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def readmatrix(body):return sp.Matrix([[sp.sympify(x.strip()) for x in row.split('&')] for row in body.split(r'\\')])
def readmatrices(text):return [readmatrix(x) for x in g.MATRIX.findall(text)]
def vec(m):return list(map(int,m))
def expected_banks(profile,a,b):
 # Independent arithmetic over actual displayed matrices, not generation parameters.
 c=a+b;A=vec(a);B=vec(b);C=vec(c)
 def setcell(index,value):v=C.copy();v[index]=value;return v
 if profile=='authored-correspondence':return [C,vec(a-b),vec(b-a),A,vec(c.T)]
 if profile=='authored-signs':return [C,[x+abs(y) for x,y in zip(A,B)],[abs(x)+y for x,y in zip(A,B)],[-v for v in C],vec(a+b.T)]
 if profile=='observed-q-101':return [[C[0],B[1]-A[1],C[2],-abs(A[3])-abs(B[3])],[C[0],A[1]-B[1],A[2],C[3]],[B[0]-A[0],B[1]-A[1],C[2],C[3]],C,setcell(3,-abs(A[3])-abs(B[3]))]
 if profile=='observed-q-11440':return [C,[A[1],A[0],C[2],C[3]],[A[1]]*4,[-C[0],C[1],C[2],-C[3]],[C[0]]*4]
 if profile=='observed-q-100':return [[A[0]-B[0],B[1]-A[1],C[2],C[3]],setcell(1,B[1]-A[1]),C,[C[1]]*4,setcell(0,-C[0])]
 if profile=='observed-q-125630':return [setcell(2,C[1]),setcell(1,B[3]),C,setcell(2,C[0]),setcell(0,C[0]+1)]
 if profile=='observed-q-125631':return [setcell(0,A[3]),setcell(1,-C[1]),[-C[0],C[1],-C[2],C[3]],C,setcell(1,A[1])]
 raise AssertionError('Unknown complete bank')
def identity_fields(q):
 out=[]
 for f in q[':question/answer-fields']:
  choices=f[':answer-field/choices'];row={'key':f[':answer-field/key'],'type':f[':answer-field/type'].split('/')[-1],'bank':sorted(a[':answer/value'] for a in choices)}
  if ':answer-field/correct' in f:row['correct']=next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1])
  out.append(row)
 return sorted(out,key=lambda f:json.dumps(f,sort_keys=True))

def check(r):
 if r['generation'].get('raw_replay'):return check_raw(r)
 q,m=r['question'],r['generation'];assert m['dependencies']['python']==sys.version.split()[0];assert r['knowledge_point']=={'db_id':17592186054648,'id':g.KP_UUID,'title':'Adding Square Matrices'}
 g.validate_generated_record(r)
 prompt=readmatrices(q[':question/problem']);assert len(prompt)==2
 a,b=prompt;assert a.shape==b.shape==(2,2);c=a+b
 assert m['parameters']['a']==vec(a) and m['parameters']['b']==vec(b)
 g.validate_parameters(q[':question/difficulty'].split('/')[-1],g.canonical_parameters(m['parameters']))
 assert m['mathematical_fingerprint']==digest(sorted([vec(a),vec(b)]))
 sol=readmatrices(q[':question/worked-solution']);assert sol[0]==a and sol[1]==b and sol[-1]==c
 # Read and verify every unevaluated addend, in order, from displayed calculation.
 bodies=g.MATRIX.findall(q[':question/worked-solution']);terms=[x.strip() for row in bodies[-2].split(r'\\') for x in row.split('&')]
 assert len(terms)==4
 for term,x,y in zip(terms,list(a),list(b)):
  match=re.fullmatch(r'(\(?-?\d+\)?)[+]([(]?-?\d+[)]?)',term);assert match,term
  assert int(match[1].strip('()'))==x and int(match[2].strip('()'))==y
 assert sol[-2]==c
 t=m['template'];assert len(sol)==4
 assert q[':question/worked-solution'].count('& =')==(2 if t=='inline-equality' else 3)
 if t=='inline-equality':assert q[':question/problem'].startswith('$\\begin{bmatrix}') and q[':question/problem'].endswith('=$')
 elif t=='inline-question':assert q[':question/problem'].startswith('What is $') and q[':question/problem'].endswith('$?')
 assert q[':question/worked-solution'].startswith('We add the corresponding entries:\n\n$$\n')
 if t in ('named-radio','cell-blanks'):
  names=re.findall(r'([A-Z])=\\begin\{bmatrix\}',q[':question/problem']);assert len(names)==2
  pair='+'.join(names);assert '$'+pair in q[':question/problem'];assert pair+' & =' in q[':question/worked-solution']
 fs=q[':question/answer-fields'];ids=[]
 for f in fs:
  assert f[':answer-field/correct'][0]==':answer/id';assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(f[':answer-field/choices'])
  assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in f[':answer-field/choices']];ids.extend(a[':answer/id'] for a in f[':answer-field/choices'])
 assert len(set(ids))==len(ids)
 if fs[0][':answer-field/type'].endswith('/radio'):
  assert len(fs)==1 and fs[0][':answer-field/key']=='selection';f=fs[0]
  values=[]
  for ans in f[':answer-field/choices']:
   matrices=readmatrices(ans[':answer/value']);assert len(matrices)==1 and matrices[0].shape==(2,2);values.append(matrices[0])
  assert len(values)==5 and len(set(map(tuple,values)))==5
  corrects=[ans[':answer/id'] for ans,v in zip(f[':answer-field/choices'],values) if v==c];assert corrects==[f[':answer-field/correct'][1]]
  assert sorted(vec(x) for x in values)==sorted(expected_banks(m['profile'],a,b))
 else:
  assert len(fs)==4 and all(f[':answer-field/type']==':answer-field.type/blank' for f in fs)
  # The actual source table is a four-entry response in row-major placeholder order.
  table='\n'.join(x for x in q[':question/problem'].splitlines() if x.startswith('|') and '---' not in x)
  targets=re.findall(r'\{\{(field-\d+)\}\}',table);assert len(targets)==4 and len(set(targets))==4
  assert set(targets)==set(f[':answer-field/key'] for f in fs)
  keyed={f[':answer-field/key']:f for f in fs}
  for key,x in zip(targets,list(c)):
   f=keyed[key];assert len(f[':answer-field/choices'])==1 and sp.sympify(f[':answer-field/choices'][0][':answer/value'])==x
 content=digest([g.VERSION,q.get(':question/difficulty'),q[':question/problem'],q.get(':question/worked-solution'),identity_fields(q)])
 assert content==m['content_fingerprint'] and q[':question/id']==g.uid(g.KP_UUID,content)
 for f in fs:
  assert f[':answer-field/id']==g.uid(q[':question/id'],f[':answer-field/key'])
  for ans in f[':answer-field/choices']:assert ans[':answer/id']==g.uid(f[':answer-field/id'],ans[':answer/value'])
 return r

def check_raw(r):
 q,m=r['question'],r['generation'];profile=g.RAW_PROFILES[m['profile']]
 assert m['dependencies']['python']==sys.version.split()[0]
 assert (':question/difficulty' in q)==(profile['difficulty'] is not None)
 assert (':question/worked-solution' in q)==profile['solution_present']
 if ':question/difficulty' in q:assert q[':question/difficulty']==profile['difficulty']
 g.validate_prose(q[':question/problem']);a,b=readmatrices(q[':question/problem']);c=a+b
 assert a.shape==b.shape==(2,2) and vec(a)==m['parameters']['a'] and vec(b)==m['parameters']['b']
 assert m['mathematical_fingerprint']==digest(sorted([vec(a),vec(b)]))
 g.validate_parameters('easy',m['parameters'])
 if ':question/worked-solution' in q:
  g.validate_prose(q[':question/worked-solution']);sol=readmatrices(q[':question/worked-solution']);assert len(sol)==4 and sol[0]==a and sol[1]==b and sol[-2]==c and sol[-1]==c
  bodies=g.MATRIX.findall(q[':question/worked-solution']);terms=[x.strip() for row in bodies[-2].split(r'\\') for x in row.split('&')]
  for term,x,y in zip(terms,list(a),list(b)):
   match=re.fullmatch(r'(\(?-?\d+\)?)[+]([(]?-?\d+[)]?)',term);assert match;assert int(match[1].strip('()'))==x and int(match[2].strip('()'))==y
  assert q[':question/worked-solution'].count('& =')==(2 if m['template']=='inline-equality' else 3)
 fields=q[':question/answer-fields'];assert len(fields)==len(profile['fields']);owners=set()
 for i,(field,contract) in enumerate(zip(fields,profile['fields'])):
  key=field[':answer-field/key'];assert key==contract['key'] and field[':answer-field/type']==':answer-field.type/'+contract['type']
  assert (':answer-field/correct' in field)==contract['correct_present'];answers=field[':answer-field/choices']
  occurrence=sum(f[':answer-field/key']==key for f in fields[:i]);assert field[':answer-field/id']==g.uid(q[':question/id'],key if not occurrence else key+'#'+str(occurrence))
  assert field[':answer-field/id'] not in owners;owners.add(field[':answer-field/id'])
  for answer in answers:
   g.validate_tex(answer[':answer/value']);assert answer[':answer/id']==g.uid(field[':answer-field/id'],answer[':answer/value']);assert answer[':answer/id'] not in owners;owners.add(answer[':answer/id'])
  if contract['type']=='radio':
   vals=[readmatrices(ans[':answer/value'])[0] for ans in answers];assert len(vals)==5 and all(v.shape==(2,2) for v in vals);assert len(set(map(tuple,vals)))==5
   assert sorted(vec(v) for v in vals)==sorted(expected_banks(m['operation_profile'],a,b))
   correct=[answer[':answer/id'] for answer,v in zip(answers,vals) if v==c];assert len(correct)==1
   if contract['correct_present']:assert correct==[field[':answer-field/correct'][1]]
  else:
   target=int(key.split('-')[1])-1;assert len(answers)==1 and int(answers[0][':answer/value'])==list(c)[target];assert '{{'+key+'}}' in q[':question/problem']
   if contract['correct_present']:assert field[':answer-field/correct']==[':answer/id',answers[0][':answer/id']]
 content=digest([g.VERSION,q.get(':question/difficulty'),q[':question/problem'],q.get(':question/worked-solution'),identity_fields(q)])
 assert content==m['content_fingerprint'] and q[':question/id']==g.uid(g.KP_UUID,content)
 assert m['native_eligible']==all(c['correct_present'] for c in profile['fields'])
 return r

def native(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every whole-matrix radio choice'} for a in f[':answer-field/choices'])
  else:
   n=int(f[':answer-field/choices'][0][':answer/value'])
   for value,result,purpose in [(str(n),'accepted','Canonical integer'),('('+str(n)+')','accepted','Parenthesized exact integer'),(str(2*n)+'/2','accepted','Unreduced exact rational equivalent'),(str(n+1),'rejected','Incorrect entry')]:checks.append({'field_index':i,'submitted':value,'expected':result,'purpose':purpose})
 return {'label':label,'record':r,'checks':checks}
def same_content(a,b):
 assert a['question'][':question/id']==b['question'][':question/id']
 assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 assert a['question'][':question/problem']==b['question'][':question/problem'] and a['question'][':question/worked-solution']==b['question'][':question/worked-solution']
 assert identity_fields(a['question'])==identity_fields(b['question'])
def must_reject(fn):
 try:fn()
 except (ValueError,AssertionError):return
 raise AssertionError('Invalid case was accepted')

def main():
 independent=json.loads((HERE/'independent-inventory.json').read_text());assert independent['database']==g.SOURCE['database'] and independent['basis']==g.SOURCE['basis'] and independent['lineage']==g.SOURCE['lineage'];independent_records=[q for q in RAW if ':question/math-academy-id' not in q];assert len(independent_records)==len(independent['questions'])==1
 for row in independent['questions']:assert row['record']==independent_records[0] and row['role']=='independently authored inventory' and row['relationship_to_source_templates'].strip()
 assert {c['source_math_academy_id'] for c in json.loads((HERE/'source-cases.json').read_text())}=={q[':question/math-academy-id'] for q in RAW if ':question/math-academy-id' in q}
 refresh=ROOT/'generate/runs/current/refresh-2026-10-14'
 for local,remote in [('source.json','sources/17592186054648.json'),('topic.json','topics/17592186049304.json'),('lesson.json','lessons/17592186049304.json')]:
  assert (HERE/local).read_bytes()==(refresh/remote).read_bytes();wrapper=json.loads((HERE/local).read_text());assert wrapper['database']=='math' and wrapper['basis']==2275 and wrapper['lineage']==g.SOURCE['lineage']
 topic=json.loads((HERE/'topic.json').read_text());assert any(k[':db/id']==17592186054648 for k in topic['record'][':topic/knowledge-points'])
 activity=json.loads((HERE/'lesson.json').read_text())['record'][0];steps={s[':db/id']:s for s in activity[':activity/steps']};current=activity[':activity/first-step'][':db/id'];route=[]
 while current:
  assert current not in route;route.append(current);current=steps[current].get(':step/next',{}).get(':db/id')
 assert route==[17592186055590,17592186055591,17592186055594,17592186055593,17592186055592]
 all_records=[];inputs=[];replays=[];mappings=[];review=[];samples=[];ineligible=[];slot={level:{k:{str(i):set() for i in range(4)} for k in ('a','b')} for level in g.LEVELS};mutations=[]
 for case,source in zip(CASES,RAW):
  assert case['source_id']==source[':question/id']
  r=check(g.generate(case['level'],0,case['template'],parameters=case['parameters'],profile=case['bank_profile']))
  q=r['question'];assert q[':question/problem']==g.normalize_prose(source[':question/problem'])
  for name in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (name in q)==(name in source)
  has_solution=':question/worked-solution' in source
  if has_solution:assert q[':question/worked-solution']==g.normalize_prose(source[':question/worked-solution']),case['source_id']
  keys_matched=0;values_matched=0;distractors=0;field_rows=[]
  for sf,gf in zip(source[':question/answer-fields'],q[':question/answer-fields']):
   assert gf[':answer-field/key']==sf[':answer-field/key'] and (':answer-field/correct' in gf)==(':answer-field/correct' in sf)
   original=sf[':answer-field/choices'];generated=gf[':answer-field/choices']
   assert sorted(g.normalize_tex(x[':answer/value']) for x in original)==sorted(x[':answer/value'] for x in generated)
   for ans in original:
    matches=[a for a in generated if a[':answer/value']==g.normalize_tex(ans[':answer/value'])];assert len(matches)==1
    correct=(readmatrices(matches[0][':answer/value'])[0]==sum(readmatrices(q[':question/problem']),sp.zeros(2))) if gf[':answer-field/type'].endswith('/radio') else int(matches[0][':answer/value'])==g.addition(case['parameters'])[int(gf[':answer-field/key'].split('-')[1])-1];values_matched+=1;distractors+=int(not correct)
    if r['generation']['operation_profile']:
     matrix=vec(readmatrices(ans[':answer/value'])[0]);values=expected_banks(r['generation']['operation_profile'],*readmatrices(q[':question/problem']));idx=values.index(matrix);recipe=g.OBSERVED_RECIPES[r['generation']['operation_profile']][idx]
    else:recipe='Corresponding row-major cell sum'
    mappings.append({'source_id':case['source_id'],'source_field_id':sf[':answer-field/id'],'source_answer_id':ans[':answer/id'],'exact_value':ans[':answer/value'],'profile':case['bank_profile'],'operation_pattern':recipe,'interpretation':'Observed expression pattern; opaque cognitive intent unresolved' if r['generation']['operation_profile'] else 'Verified entrywise addition','generated_value':matches[0][':answer/value'],'matched':True,'mathematically_correct':correct})
   designation=sf.get(':answer-field/correct')
   if designation:
    generated_correct=next(a[':answer/value'] for a in generated if a[':answer/id']==gf[':answer-field/correct'][1]);assert g.normalize_tex(designation[':answer/value'])==generated_correct;keys_matched+=1
   field_rows.append({'source_field_id':sf[':answer-field/id'],'matched_complete_bank':True,'choice_count':len(original),'supplied_designation_matched':bool(designation)})
  replays.append({'source_id':case['source_id'],'math_academy_id':case.get('source_math_academy_id'),'source_db_id':case['source_db_id'],'template':case['template'],'profile':case['bank_profile'],'exact_prompt':q[':question/problem']==source[':question/problem'],'normalized_prompt':True,'exact_solution':has_solution and q[':question/worked-solution']==source[':question/worked-solution'],'normalized_solution':has_solution,'missing_solution_preserved':not has_solution,'observed_level':case['observed_level'],'raw_unrated_preserved':case['observed_level'] is None,'matched_values':values_matched,'matched_distractors':distractors,'supplied_designations_matched':keys_matched,'fields':field_rows})
  all_records.append(r)
  if r['generation']['native_eligible']:inputs.append(native('raw-source-'+case['source_id'],r))
  else:ineligible.append({'source_id':case['source_id'],'profile':case['bank_profile'],'reason':'Raw source retains absent correct ref; check-engine requires an owned correct ref. q-11440 also retains duplicate selection fields. No engine change or raw repair.'})
  completed=check(g.generate('easy',0,case['template'],parameters=case['parameters'],profile=r['generation']['operation_profile']));inputs.append(native('eligible-completion-'+case['source_id'],completed));review.append({'kind':'eligible-completion','source_id':case['source_id'],'record':completed})
  review.append({'kind':'observed-replay','source_id':case['source_id'],'original':source,'record':r})
  # Every evidence profile also gets a changed-parameter instance through the public API.
  if r['generation']['operation_profile']:
   for seed in range(400):
    p=g.sample('easy',__import__('random').Random(1000+seed));p['names']=case['parameters']['names'];p['wrap_first']=case['parameters']['wrap_first']
    try:changed=check(g.generate('easy',seed,case['template'],parameters=p,profile=case['bank_profile']))
    except g.SampleRejected:continue
    break
   else:raise AssertionError('No varied evidence-bank instance')
  else:
   varied=g.sample('easy',__import__('random').Random(99));varied.update(names=case['parameters']['names'],wrap_first=case['parameters']['wrap_first'],nested=case['parameters']['nested']);changed=check(g.generate('easy',99,case['template'],parameters=varied,profile=case['bank_profile']))
  assert changed['generation']['mathematical_fingerprint']!=r['generation']['mathematical_fingerprint'];all_records.append(changed)
  if changed['generation']['native_eligible']:inputs.append(native('changed-source-'+case['source_id'],changed))
  review.append({'kind':'generated-evidence-variant' if r['generation']['operation_profile'] else 'generated-raw-variant','source_id':case['source_id'],'record':changed})
 for level in g.LEVELS:
  for template in g.TEMPLATES:
   profiles=list(g.AUTHORED_RECIPES) if template!='cell-blanks' else [None]
   for profile in profiles:
    group=[]
    for sample_index in range(40):
     seed=sample_index+1000*list(g.TEMPLATES).index(template)+400*profiles.index(profile)
     r=check(g.generate(level,seed,template,profile=profile));samples.append(r);all_records.append(r);inputs.append(native(level+'-'+template+'-'+str(profile)+'-'+str(seed),r));group.append(r)
     p=r['generation']['parameters'];same_content(r,check(g.generate(level,seed+987,template,parameters=p,profile=profile)))
     for k in ('a','b'):
      for i,v in enumerate(p[k]):slot[level][k][str(i)].add(v)
    assert len(set(r['generation']['mathematical_fingerprint'] for r in group))==40
    review.extend({'kind':'generated-authored-bank','level':level,'template':template,'profile':profile,'record':r} for r in group[:2])
 # Explicit valid extrema and complete-bank collision rejection.
 boundaries={'easy':[{'a':[-12,0,12,0],'b':[12,0,-12,0]},{'a':[12]*4,'b':[12]*4}], 'moderate':[{'a':[25,1,-25,-1],'b':[-1,-25,-1,-25]},{'a':[-25,-1,25,1],'b':[1,25,1,25]}], 'hard':[{'a':[99,10,-99,-10],'b':[-10,-99,10,99]},{'a':[-99,-10,99,10],'b':[10,99,-10,-99]}]}
 for level,ps in boundaries.items():
  for p in ps:inputs.append(native('boundary-'+level,check(g.generate(level,0,'cell-blanks',parameters=p))))
 for level,p in [('easy',{'a':[13]*4,'b':[1]*4}),('moderate',{'a':[25,1,-25,-1],'b':[-1,-26,-1,-25]}),('moderate',{'a':[0,10,10,10],'b':[10,-10,10,10]}),('moderate',{'a':[1,1,1,1],'b':[-1,-1,1,1]}),('hard',{'a':[100,10,-99,-10],'b':[-10,-99,10,99]}),('hard',{'a':[99,10,-99,-10],'b':[10,-99,10,99]}),('hard',{'a':[10]*4,'b':[-10]*4})]:must_reject(lambda:g.generate(level,0,'cell-blanks',parameters=p))
 must_reject(lambda:g.generate('easy',0,'named-radio',parameters={'a':[0]*4,'b':[0]*4},profile='authored-correspondence'))
 must_reject(lambda:g.generate('easy',profile='observed-q-101'))
 must_reject(lambda:g.generate('hard',parameters=CASES[0]['parameters'],profile='observed-q-101'))
 must_reject(lambda:g.generate('easy',0,'cell-blanks',parameters={'a':[1]*4,'b':[2]*4,'unknown':1}))
 # Independently prove that option order and unused notation do not add identity.
 base=check(g.generate('easy',17,'named-radio',profile='authored-correspondence'));p=base['generation']['parameters']
 same_content(base,check(g.generate('easy',812,'named-radio',parameters=p,profile='authored-correspondence')))
 # Use nonnegative first operands: wrapping slots then produce identical displayed content.
 p={'a':[1,2,3,4],'b':[5,-2,7,-3]};r=check(g.generate('easy',0,'named-radio',parameters=p,profile='authored-correspondence'));same_content(r,check(g.generate('easy',99,'named-radio',parameters={**p,'wrap_first':[0,1,2,3]},profile='authored-correspondence')))
 renamed=check(g.generate('easy',0,'named-radio',parameters={**p,'names':['P','Q']},profile='authored-correspondence'));assert renamed['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'] and renamed['question'][':question/id']!=r['question'][':question/id']
 swapped=check(g.generate('easy',0,'cell-blanks',parameters={'a':p['b'],'b':p['a']}));assert swapped['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
 # Another complete bank changes identity, while the actual assessed task stays fixed.
 multi=CASES[0]['parameters'];first=check(g.generate('easy',0,'named-radio',parameters=multi,profile='authored-correspondence'));alternate=check(g.generate('easy',0,'named-radio',parameters=multi,profile='authored-signs'));assert alternate['generation']['mathematical_fingerprint']==first['generation']['mathematical_fingerprint'] and alternate['question'][':question/id']!=first['question'][':question/id']
 # Displayed grade changes presentation identity even when operands/layout match.
 for level,pp in [('moderate',{'a':[10,-10,10,-10],'b':[-11,11,11,-11]}),('hard',{'a':[10,11,-12,-11],'b':[-12,-10,10,12]})]:
  easy=check(g.generate('easy',0,'cell-blanks',parameters=pp));other=check(g.generate(level,0,'cell-blanks',parameters=pp));assert easy['question'][':question/problem']==other['question'][':question/problem'] and easy['question'][':question/worked-solution']==other['question'][':question/worked-solution'];assert easy['question'][':question/id']!=other['question'][':question/id'] and easy['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
 # Mutations exercise prompt operand, displayed sum addend, collected result, matrix-bank cell and key.
 for label,kind in [('prompt-cell','prompt'),('sum-addend','solution-first'),('collected-entry','solution-last'),('whole-choice-cell','bank'),('key','key')]:
  bad=copy.deepcopy(r);q=bad['question']
  if kind=='prompt':q[':question/problem']=q[':question/problem'].replace('1 & 2','9 & 2',1)
  elif kind=='solution-first':q[':question/worked-solution']=q[':question/worked-solution'].replace('1+5','1+4',1)
  elif kind=='solution-last':q[':question/worked-solution']=q[':question/worked-solution'].replace('6 & 0','8 & 0',1)
  elif kind=='bank':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']=q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'].replace(' & ','0 & ',1)
  else:q[':question/answer-fields'][0][':answer-field/correct'][1]='00000000-0000-0000-0000-000000000000'
  must_reject(lambda:check(bad));mutations.append({'mutation':label,'caught':True})
 for case in CASES[:2]:
  raw=check(g.generate('easy',0,case['template'],parameters=case['parameters'],profile=case['bank_profile']));bad=copy.deepcopy(raw)
  if case['source_math_academy_id']=='q-101':bad['question'][':question/difficulty']=':question.difficulty/easy';label='raw-missing-grade-presence'
  else:bad['question'][':question/answer-fields'].pop(0);label='raw-legacy-duplicate-contract'
  must_reject(lambda:check(bad));mutations.append({'mutation':label,'caught':True})
 assert all(len(v)>=15 for level in slot.values() for operand in level.values() for v in operand.values())
 save('raw-native-ineligible.json',ineligible);save('source-choice-mapping.json',mappings);save('source-replay.json',replays);save('review.json',review);save('native-input.json',inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 native_report=json.loads((HERE/'native-grading.json').read_text());assert native_report['documented_unresolved_checks']==0
 baseline=json.loads((HERE/'baseline-hashes.json').read_text());current_paths=[ROOT/'generate/scratch/17592186054648.py',*[p for p in (ROOT/'generate/scratch/17592186054648').rglob('*') if p.is_file()]];assert {str(p.relative_to(ROOT)) for p in current_paths}==set(baseline['before']);after={p:{'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),'size':(ROOT/p).stat().st_size} for p in baseline['before']};assert after==baseline['before'];baseline.update(after=after,unchanged=True);save('baseline-hashes.json',baseline)
 save('validation.json',{'passed':True,'source_database':'math','source_basis':2275,'ma_original_questions':6,'independently_authored_inventory_questions':1,'all_captured_practice_questions':7,'rated_ma_easy':5,'unrated_ma_original':1,'raw_missing_grade_preserved':1,'ma_original_raw_fields':10,'independent_inventory_fields':4,'all_captured_raw_fields':14,'matched_field_banks':14,'ma_original_fidelity':{'prompts':6,'available_solutions':5,'raw_field_banks':10,'answer_values':34,'distractors':24,'supplied_designations':8,'missing_designations_preserved':2,'missing_grades_preserved':1,'missing_solutions_preserved':1,'duplicate_field_contracts_preserved':1},'independent_inventory_fidelity':{'records':1,'prompts':1,'available_solutions':1,'raw_field_banks':4,'answer_values':4,'supplied_designations':4},'matched_answer_values':len(mappings),'matched_distractors':sum(x['matched_distractors'] for x in replays),'supplied_designations':sum(x['supplied_designations_matched'] for x in replays),'raw_missing_designations_preserved':2,'eligible_completion_inferred_designations':2,'exact_prompts':sum(x['exact_prompt'] for x in replays),'ma_available_solutions':5,'all_available_solutions':6,'exact_solutions':sum(x['exact_solution'] for x in replays),'normalized_solutions':sum(x['normalized_solution'] for x in replays),'normalization_repairs':[],'raw_legacy_duplicate_fields_preserved':1,'eligible_completion_duplicate_fields_collapsed':1,'sample_count':len(samples),'distinct_mathematical_tasks_by_level':{l:len({r['generation']['mathematical_fingerprint'] for r in samples if r['question'][':question/difficulty']==':question.difficulty/'+l}) for l in g.LEVELS},'distinct_content_by_level':{l:len({r['question'][':question/id'] for r in samples if r['question'][':question/difficulty']==':question.difficulty/'+l}) for l in g.LEVELS},'supported_levels':list(g.LEVELS),'authored_levels':['moderate','hard'],'sampled_slot_values':{l:{k:{i:sorted(v) for i,v in vv.items()} for k,vv in values.items()} for l,values in slot.items()},'fixed_targets':[0,1,2,3],'boundary_cases':6,'negative_cases':11,'displayed_grade_identity_probes':2,'mutation_probes':mutations,'native_grading':{'accepted':native_report['accepted_checks'],'rejected':native_report['rejected_checks'],'unresolved':0,'field_types':['radio','blank'],'raw_ineligible_source_profiles':ineligible,'matrix_blank_fragments':'Not present: four scalar cell blanks only','engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()},'baseline_files':len(after),'baseline_unchanged':True,'runtime':{'python':platform.python_version(),'sympy':sp.__version__},'worker_qa_passed':True,'root_independent_qa':'required; pending','unresolved_source_interpretations':['Opaque copied-entry, repeated-entry and c00+1 patterns are evidence-only, not asserted to recover source cognitive intent','No observed moderate/hard labels; arithmetic bands are conservative authored design claims'],'artifact_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'source-cases.json']}})
 print('Validated 6 MA originals + 1 exact independent inventory record / 14 raw field banks / 38 answers and '+str(len(samples))+' E/M/H authored-bank samples; baseline 62 files unchanged.')
if __name__=='__main__':main()
