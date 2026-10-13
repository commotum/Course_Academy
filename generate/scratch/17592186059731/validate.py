#!/usr/bin/env python3
"""Independent printed-vector/stage/bank/native-grading audit; no EDB operations."""
import hashlib, importlib.util,json,pathlib,re,subprocess
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
D=pathlib.Path(__file__).resolve().parent;ROOT=D.parents[2];SCRIPT=D.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SYMS={v:sp.Symbol(v,real=True) for v in ('x','k','n','r','a')}

def parse(s):
 s=s.strip().rstrip('.').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','')
 def group(i):
  assert s[i]=='{';depth=1;j=i+1
  while depth:
   if s[j]=='{':depth+=1
   elif s[j]=='}':depth-=1
   j+=1
  return s[i+1:j-1],j
 def expand(t):
  nonlocal s
  old=s;s=t;out='';i=0
  while i<len(s):
   if s.startswith(r'\frac',i):
    aa,j=group(i+5);bb,i=group(j);out+='(('+expand(aa)+')/('+expand(bb)+'))'
   elif s.startswith(r'\sqrt',i):
    aa,i=group(i+5);out+='sqrt('+expand(aa)+')'
   elif s[i]=='{':
    aa,i=group(i);out+='('+expand(aa)+')'
   else:out+=s[i];i+=1
  s=old;return out
 return parse_expr(expand(s),local_dict=SYMS,transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def printed(r):
 q=r['question'];prompt=q[':question/problem'];arrays=[]
 for m in re.finditer(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',prompt):arrays.append([parse(s) for s in m[1].split(r'\\')])
 if not arrays:arrays=[[parse(s) for s in m[1].split(',')] for m in re.finditer('⟨(.*?)⟩',prompt)]
 assert len(arrays)==2 and len(arrays[0])==len(arrays[1]) in (2,3)
 unknowns=set().union(*(z.free_symbols for V in arrays for z in V));assert len(unknowns)==1
 x=unknowns.pop();dot=sp.expand(sum(a*b for a,b in zip(*arrays)))
 sign=1 if re.search(r'\$'+str(x)+r'\s*>\s*0',prompt) else -1 if re.search(r'\$'+str(x)+r'\s*<\s*0',prompt) else None
 roots=sp.solve(dot,x);eligible=[z for z in roots if z.is_real and (sign is None or z*sign>0)];assert len(eligible)==1,(prompt,roots)
 return x,arrays,dot,sign,eligible[0]

def formatcheck(s):
 assert s.count('$$')%2==0
 assert s.replace('$$','').count('$')%2==0
 depth=0
 for c in s:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert '--' not in s and '+-' not in s

def check(r):
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=r['question'];f=q[':question/answer-fields'][0];x,V,dot,sign,root=printed(r)
 formatcheck(q[':question/problem']);formatcheck(q[':question/worked-solution'])
 vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(vals)==(1 if f[':answer-field/type'].endswith('/blank') else 5)
 assert len(set(a[':answer/id'] for a in f[':answer-field/choices']))==len(vals)
 for i,z in enumerate(vals):
  assert z.is_real and not z.free_symbols
  for w in vals[:i]:assert sp.simplify(z-w)!=0
 valid=[a[':answer/id'] for a,z in zip(f[':answer-field/choices'],vals) if sp.simplify(dot.subs(x,z))==0 and (sign is None or z*sign>0)]
 assert valid==[f[':answer-field/correct'][1]]
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S);assert len(blocks)==2
 rows=[b.split(r'\\') for b in blocks]
 # First formal expression has exactly one component product per printed coord.
 rhs=rows[0][0].split(' & =')[1]
 assert rhs.count(r'\cdot')==len(V[0]); assert all('_{'+s+'}' in rhs for s in 'xyz'[:len(V[0])])
 # Actual substituted products and each individually evaluated/reduced stage.
 for row in rows[0][1:]:
  got=parse(row.split(' & =')[1]);assert sp.simplify(got-dot)==0,(row,dot,got)
 assert rows[0][1].count(r'\cdot')==len(V[0])
 for product,a,b in zip(rows[0][1].split(' & =')[1].split('+'),*V):assert sp.simplify(parse(product)-a*b)==0
 # Independently enforce normal difficulty arithmetic from displayed objects.
 if not r['generation']['profile'].startswith('observed_'):
  level=q[':question/difficulty'].split('/')[-1];rad=sp.simplify(root**2)
  if level=='hard':
   coeffs=[sp.Poly(z,x).LC() for vec in V for z in vec];assert all(2<=abs(z)<=12 for z in coeffs)
   assert 2<=abs(sp.Poly(dot,x).LC())<=6 and 2<=rad.p<=30 and 2<=rad.q<=6 and sp.sqrt(rad).is_rational is False
  elif sp.degree(dot,x)==2 and r['generation']['template']!='repeated3':
   assert rad.q==1 and rad<=64
   if level=='easy':assert root.is_integer
 # Equation-solving stages preserve the unfiltered root set until sign selection.
 roots=set(sp.solve(dot,x))
 for row in rows[1][1:]:
  lhs,rhs=row.split(' & =');lhs=parse(lhs)
  if r'\pm' in rhs:
   a=parse(rhs.replace(r'\pm',''));got={a,-a}
  else:got=set(sp.solve(lhs-parse(rhs),x))
  assert got==roots,(row,roots,got)
 return root

def engine_item(r,label):
 root=check(r);f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  for a in f[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned complete-bank choice'})
 else:
  correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  checks.append({'submitted':correct,'expected':'accepted','purpose':'canonical exact unknown fragment'})
  if root.is_Rational:
   equivalent=r'\frac{'+str(root.p*3)+'}{'+str(root.q*3)+'}'
  else:
   square=sp.simplify(root**2);equivalent=('-' if root<0 else '')+r'\sqrt{\frac{'+str(square.p)+'}{'+str(square.q)+'}}'
  checks.append({'submitted':equivalent,'expected':'accepted','purpose':'unreduced fraction or rational-radicand equivalent unknown fragment'})
  checks.append({'submitted':g.tex(root+1),'expected':'rejected','purpose':'wrong scalar substituted into printed vectors'})
 return {'label':label,'record':r,'checks':checks}

def main():
 source=json.loads((D/'source.json').read_text());originals=source['record'][':knowledge-point/questions'];cases=json.loads((D/'source-cases.json').read_text());checks=[];review=[]
 prompts=solutions=designations=banks=distractors=0
 for c in cases:
  r=g.generate(c['level'],seed=37,template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile'))
  q=next(z for z in originals if z[':question/math-academy-id']==c['source_id']);root=check(r);f=r['question'][':question/answer-fields'][0];of=q[':question/answer-fields'][0]
  assert q[':question/problem']==r['question'][':question/problem'];prompts+=1
  if ':question/worked-solution' in q:assert q[':question/worked-solution']==r['question'][':question/worked-solution'];solutions+=1
  assert sorted(sp.srepr(sp.simplify(parse(a[':answer/value']))) for a in of[':answer-field/choices'])==sorted(sp.srepr(sp.simplify(parse(a[':answer/value']))) for a in f[':answer-field/choices']);banks+=1
  assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']
  if ':answer-field/correct' in of:assert sp.simplify(parse(of[':answer-field/correct'][':answer/value'])-root)==0;designations+=1
  distractors+=len(of[':answer-field/choices'])-1
  checks.append(engine_item(r,c['source_id']));review.append({'label':'source replay '+c['source_id'],'record':r})
  # Each evidence profile is exercised with changed mathematical parameters.
  for seed in (91,117):
   rr=g.generate(c['level'],seed=seed,template=c['template'],profile=c.get('bank_profile'));checks.append(engine_item(rr,c['source_id']+' variant '+str(seed)));review.append({'label':'GENERATED observed-template variant '+c['source_id']+' '+str(seed),'record':rr})
 # All three levels, all normal templates, sampling, identity and native engine.
 positions=set();identities={l:set() for l in g.DEFAULTS};mathids={l:set() for l in g.DEFAULTS};sample_count=0
 for level in g.DEFAULTS:
  for seed in range(90):
   r=g.generate(level,seed);check(r);sample_count+=1;
   ff=r['question'][':question/answer-fields'][0]
   if ff[':answer-field/type'].endswith('/radio'):positions.add(next(i for i,a in enumerate(ff[':answer-field/choices']) if a[':answer/id']==ff[':answer-field/correct'][1]))
   identities[level].add(r['question'][':question/id']);mathids[level].add(r['generation']['mathematical_fingerprint'])
   if seed<8:checks.append(engine_item(r,level+' default '+str(seed)));review.append({'label':'GENERATED '+level+' authored/default '+str(seed),'record':r})
   same=g.generate(level,seed+991,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'] if r['generation']['profile']!='blank' else None)
   assert r['question'][':question/id']==same['question'][':question/id'];assert r['generation']['mathematical_fingerprint']==same['generation']['mathematical_fingerprint']
 assert positions==set(range(5)),positions
 observed=cases[0];a=g.generate('easy',template=observed['template'],parameters=observed['parameters'],profile=observed['bank_profile']);b=g.generate('easy',template=observed['template'],parameters=observed['parameters'])
 assert a['question'][':question/id']!=b['question'][':question/id'] and a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 assert all(len(v)>=60 for v in mathids.values()),{l:len(s) for l,s in mathids.items()}
 # Guard tests exercise invalid explicit parameters without silently resampling.
 invalid=[('hard','hard_square3',dict(a=1,b=3,c=-1,d=1,e=-6,f=2,sign=-1)),('moderate','square3_collect',dict(a=1,b=3,c=-1,d=1,e=-7,f=1,sign=-1)),('easy','linear2',dict(a=9,b=4,c=-4)),('easy','square2_blank',dict(a=2,b=-3,c=8,d=4,sign=1))]
 for l,t,p in invalid:
  try:g.generate(l,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('guard accepted invalid',l,t,p))
 (D/'engine-input.json').write_text(json.dumps(checks,indent=2)+'\n')
 proc=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True)
 assert proc.returncode==0,proc.stdout+proc.stderr
 (D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 text=['# Original evidence and generated variants','Source: math basis 1356. Originals preserve raw captured records; variants are generator output. Opaque source-profile variants are evidence-only, not default authored practice.']
 for q in originals:
  text+=['## ORIGINAL '+q[':question/math-academy-id'],q[':question/problem'], '\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q.get(':question/worked-solution','No source solution captured; no original correct designation captured.')]
 for item in review:text+=['## '+item['label'],g.markdown(item['record'])]
 (D/'review.md').write_text('\n\n'.join(text)+'\n')
 engine=json.loads((D/'engine-report.json').read_text())
 result={'passed':True,'source_provenance':g.SOURCE,'source_coverage':{'questions':8,'prompt_exact':prompts,'complete_answer_banks':banks,'distractors':{'matched':distractors,'total':24},'correct_designations':{'matched':designations,'captured_total':6,'missing_originals':2,'independently_inferred':2},'worked_solutions':{'exact':solutions,'captured_total':6,'missing_originals':2,'authored':2}},'sampled_normal_records':sample_count,'unique_mathematical_tasks':{l:len(s) for l,s in mathids.items()},'native_grading':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'formatting':True,'displayed_vector_and_stage_math':True,'ambiguity_and_identity':True,'invalid_explicit_parameters_rejected':len(invalid),'remaining_findings':['Opaque source scalar distractor intent is unrecovered; complete evidence profiles are isolated from authored default banks.','Two unrated source questions lack captured correct refs, difficulty and solutions; inferred answers do not count as original designation matches.','Hard difficulty is an authored rational-radicand scope claim, not an observed label.'],'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'database_writes':0}
 (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
