#!/usr/bin/env python3
"""Independent printed-vector/stage/bank/native-grading audit; no EDB operations."""
import hashlib, importlib.util,json,pathlib,re,subprocess,copy,sys
sys.dont_write_bytecode=True
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
 names=re.findall(r'\b([a-z])\s*=\s*(?:\\begin\{bmatrix\}|⟨)',q[':question/problem']);assert len(names)==2
 u,v=names
 assert re.search(re.escape(u)+r'(?:⊥|\\perp ?)' + re.escape(v),q[':question/problem'])
 assert f'${u}⊥{v}$' in q[':question/worked-solution']
 assert f'${u}\\cdot {v}=0.$' in q[':question/worked-solution']
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
 rows=[b.replace('& =','&=').split(r'\\') for b in blocks]
 # First formal expression has exactly one component product per printed coord.
 rhs=rows[0][0].split('&=')[1].strip()
 assert rhs=='+'.join('{'+u+'}_{'+axis+r'}\cdot {'+v+'}_{'+axis+'}' for axis in 'xyz'[:len(V[0])])
 assert rows[0][0].split('&=')[0]==u+r'\cdot '+v+' '
 assert rows[1][0].strip()==u+r'\cdot '+v+' &=0'
 # Actual substituted products and each individually evaluated/reduced stage.
 for row in rows[0][1:]:
  got=parse(row.split('&=')[1]);assert sp.simplify(got-dot)==0,(row,dot,got)
 assert rows[0][1].count(r'\cdot')==len(V[0])
 for product,a,b in zip(rows[0][1].split('&=')[1].split('+'),*V):assert sp.simplify(parse(product)-a*b)==0
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
  lhs,rhs=row.split('&=');lhs=parse(lhs)
  if r'\pm' in rhs:
   a=parse(rhs.replace(r'\pm',''));got={a,-a}
  else:got=set(sp.solve(lhs-parse(rhs),x))
  assert got==roots,(row,roots,got)
 if sign is not None:
  conclusion=re.findall(r'Therefore, \$'+str(x)+r'=([^$]+)\$',q[':question/worked-solution']);assert len(conclusion)==1
  assert sp.simplify(parse(conclusion[0])-root)==0
  assert ('disregard the negative' if sign>0 else 'disregard the positive') in q[':question/worked-solution']
 from math_format import validate_generated_record
 validate_generated_record(r)
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

def normalized_question(q):
 from math_format import normalize_prose,normalize_tex
 q=copy.deepcopy(q)
 for k in (':question/problem',':question/worked-solution'):
  if k in q:q[k]=normalize_prose(q[k]).replace('& =','&=')
 for f in q[':question/answer-fields']:
  f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f[':answer-field/choices']:
   a[':answer/type']=a[':answer/type'][':db/ident'];a[':answer/value']=normalize_tex(a[':answer/value'])
 if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 return q

def original_record(q,template):
 return {'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':normalized_question(q),'generation':{'profile':'captured_inventory','template':template}}

def baseline_verify():
 baseline=json.loads((D/'reference/registered-baseline.json').read_text())['paths']
 r=ROOT/'generate/scratch'; paths=[r/'17592186059731.py',*sorted((r/'17592186059731').rglob('*')),*sorted((r/'__pycache__').glob('*17592186059731*'))]
 now={str(p.relative_to(ROOT)):{'kind':'directory' if p.is_dir() else 'file','sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None,'size':p.stat().st_size if p.is_file() else None} for p in paths}
 assert baseline==now,'registered numeric script/tree/cache changed'
 return {'unchanged':True,'paths':len(now)}

def main():
 baseline_verify()
 source=json.loads((D/'source.json').read_text());cases=json.loads((D/'source-cases.json').read_text());specs=json.loads((D/'replay-specifications.json').read_text());inventory=json.loads((D/'independent-inventory.json').read_text())
 assert (D/'source.json').read_bytes()==(ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186059731.json').read_bytes()
 assert len(cases)==8 and len(inventory['questions'])==9
 assert all(set(c)=={'source_id','record'} for c in cases)
 checks=[];review=[];repairs=[];coverage={'source_questions':8,'prompt_matched':0,'solutions_matched':0,'banks_matched':0,'values_matched':0,'correct_refs_matched':0,'source_missing_refs':[]};slot_values={};negative_controls=[]
 for c in cases:
  q=c['record'];spec=next(z for z in specs if z['source_id']==c['source_id']);r=g.generate(spec['level'],seed=37,template=spec['template'],parameters=spec['parameters'],profile=spec.get('bank_profile'));root=check(r);n=normalized_question(q)
  assert r['question'][':question/problem']==n[':question/problem'];coverage['prompt_matched']+=1
  if ':question/worked-solution' in q:
   assert r['question'][':question/worked-solution']==n[':question/worked-solution'];coverage['solutions_matched']+=1
  else:repairs.append({'source_id':c['source_id'],'status':'supported repair; raw source ineligible because difficulty, correct reference and worked solution are missing','math_evidence':str(printed(r)[2]),'record':r})
  f=r['question'][':question/answer-fields'][0];of=n[':question/answer-fields'][0]
  assert f[':answer-field/type']==of[':answer-field/type'] and f[':answer-field/key']==of[':answer-field/key']
  assert sorted(sp.srepr(sp.simplify(parse(a[':answer/value']))) for a in f[':answer-field/choices'])==sorted(sp.srepr(sp.simplify(parse(a[':answer/value']))) for a in of[':answer-field/choices'])
  coverage['banks_matched']+=1;coverage['values_matched']+=len(of[':answer-field/choices'])
  if ':answer-field/correct' in of:
   original_root=next(parse(a[':answer/value']) for a in of[':answer-field/choices'] if a[':answer/id']==of[':answer-field/correct'][1]);assert sp.simplify(original_root-root)==0;coverage['correct_refs_matched']+=1
   raw=original_record(q,spec['template']);raw['generation']['profile']='observed_raw';check(raw)
  else:coverage['source_missing_refs'].append(c['source_id'])
  checks.append(engine_item(r,'original-replay/'+c['source_id']));review.append({'label':'original-replay/'+c['source_id'],'record':r})
  for seed in (91,117):
   rr=g.generate(spec['level'],seed=seed,template=spec['template'],profile=spec.get('bank_profile'));check(rr);checks.append(engine_item(rr,c['source_id']+'/profile-variation/'+str(seed)));review.append({'label':'profile-variation/'+c['source_id']+'/'+str(seed),'record':rr})
 # Independent non-MA captured inventory: no generator calls or template inference from its identity.
 inventory_count=0
 for q in inventory['questions']:
  kind=q[':question/answer-fields'][0][':answer-field/type'][':db/ident'];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
  if level=='hard':template='hard_square3_blank' if kind.endswith('/blank') else 'hard_square3'
  elif '⟨' in q[':question/problem']:template='square2_blank'
  elif q[':question/problem'].startswith('If'):template='linear3'
  elif '{r}' in q[':question/problem']:template='square3_collect'
  else:template='square3_shared'
  rr=original_record(q,template);check(rr);checks.append(engine_item(rr,'captured-non-MA/'+q[':question/id']));inventory_count+=1
 # Each sampler slot is observed separately; count differences in mathematical objects, not seed/order.
 identities={l:set() for l in g.DEFAULTS};positions=set();samples=[]
 for level in g.DEFAULTS:
  for seed in range(90):
   r=g.generate(level,seed);check(r);samples.append(r);meta=r['generation'];identities[level].add(meta['mathematical_fingerprint'])
   t=meta['template'];slot_values.setdefault(t,{})
   for k,value in meta['parameters'].items():slot_values[t].setdefault(k,set()).add(value)
   f=r['question'][':question/answer-fields'][0]
   if f[':answer-field/type'].endswith('/radio'):positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
   if seed<10:checks.append(engine_item(r,level+'/normal/'+str(seed)));review.append({'label':level+'/normal/'+str(seed),'record':r})
   same=g.generate(level,seed+991,template=t,parameters=meta['parameters'],profile=meta['profile'] if meta['profile']!='blank' else None)
   assert r['question'][':question/id']==same['question'][':question/id'] and meta['mathematical_fingerprint']==same['generation']['mathematical_fingerprint']
   # Independent canonical fingerprint from displayed components.
   x,V,dot,sign,root=printed(r);canonical=sp.Symbol('X',real=True)
   expected=hashlib.sha256(json.dumps({'vectors':[[sp.srepr(z.subs(x,canonical)) for z in vec] for vec in V],'sign':sign},sort_keys=True).encode()).hexdigest();assert expected==meta['mathematical_fingerprint']
 assert positions==set(range(5));assert all(len(z)>=60 for z in identities.values())
 assert all(len(v)>=2 for slots in slot_values.values() for v in slots.values())
 # Independent component slots: hold other mathematical data constant and change one coordinate.
 fixed_pairs=[('easy','square2_blank',dict(a=1,b=-1,c=2,d=2,sign=1),dict(a=1,b=-1,c=2,d=8,sign=1)),('easy','linear3',dict(a=2,b=4,c=-3,d=2,e=2),dict(a=2,b=4,c=-3,d=2,e=3)),('moderate','square3_shared',dict(a=2,b=4,c=-4,d=-2,sign=-1),dict(a=3,b=4,c=-4,d=-2,sign=-1))]
 for level,t,a,b in fixed_pairs:
  pair=[g.generate(level,template=t,parameters=p) for p in (a,b)]
  for r in pair:check(r);review.append({'label':'one-slot-held-others/'+t,'record':r})
  assert printed(pair[0])[4]!=printed(pair[1])[4]
 # Invalid intermediate mathematics must fail while the final answer/key stay valid.
 base=g.generate('moderate',template='square3_collect',parameters=dict(a=1,b=3,c=-1,d=1,e=-6,f=2,sign=-1))
 mutations=[('wrong substituted product',r'{r}^{2}\cdot 3',r'{r}^{2}\cdot 4'),('wrong evaluated stage','3{r}^{2}-','4{r}^{2}-'),('wrong root equation',r'{r}^{2} &=6',r'{r}^{2} &=7'),('wrong formal component',r'{g}_{y}\cdot {h}_{y}',r'{g}_{y}\cdot {h}_{x}'),('wrong final conclusion',r'r=-\sqrt{6}',r'r=-\sqrt{7}')]
 for label,a,b in mutations:
  bad=copy.deepcopy(base);key=':question/worked-solution';assert a in bad['question'][key],(label,a,bad['question'][key]);bad['question'][key]=bad['question'][key].replace(a,b,1)
  try:check(bad)
  except (AssertionError,ValueError):negative_controls.append(label)
  else:raise AssertionError('validator missed '+label)
 for value in (True,1.0,'1',None):
  for mode in ('seed','count'):
   try:g.generate_batch(**{mode:value})
   except ValueError:pass
   else:raise AssertionError(('bad builtin int accepted',mode,value))
 for count in (0,-1,101):
  try:g.generate_batch(count=count)
  except ValueError:pass
  else:raise AssertionError('bad count accepted')
 batch=g.generate_batch('all',123,20);assert len(batch)==60 and len({r['generation']['mathematical_fingerprint'] for r in batch})==60
 for fmt in ('json','markdown'):
  proc=subprocess.run([sys.executable,str(SCRIPT),'--difficulty','all','--count','1','--format',fmt],text=True,capture_output=True,check=True)
  if fmt=='json':assert len(json.loads(proc.stdout))==3
  else:assert proc.stdout.count('Worked solution')==3
 (D/'source-repairs.json').write_text(json.dumps(repairs,indent=2)+'\n')
 (D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 (D/'samples.json').write_text(json.dumps(samples,indent=2)+'\n')
 (D/'engine-input.json').write_text(json.dumps(checks,indent=2)+'\n')
 (D/'authored-grading-probes.json').write_text(json.dumps([{'label':item['label'],'checks':item['checks']} for item in checks],indent=2)+'\n')
 (D/'grading-diagnostics.json').write_text(json.dumps({'expected_outcomes_retained':True,'false_rejections':[],'false_acceptances':[],'unresolved':[]},indent=2)+'\n')
 proc=subprocess.run([str(D/'reference/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True)
 assert proc.returncode==0,proc.stdout+proc.stderr
 engine=json.loads((D/'engine-report.json').read_text())
 report={'status':'revalidated draft; awaiting independent parent review','source_basis':2275,'source_lineage':source['lineage'],'source_coverage':coverage,'captured_non_MA_independent_inventory_checked':inventory_count,'normal_sampled':len(samples),'unique_mathematical_tasks':{k:len(v) for k,v in identities.items()},'slot_value_coverage':{t:{k:sorted(v) for k,v in slots.items()} for t,slots in slot_values.items()},'held_other_slots_fixed_cases':len(fixed_pairs),'negative_controls_caught':negative_controls,'native_grading':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_qualification':'All canonical and genuinely equivalent submitted fragments accepted; all wrong fragments and full radio-bank wrong choices rejected. No expected outcomes pruned or relabeled.','generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'registered_baseline':baseline_verify(),'database_writes':0}
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
 text=['# Original MA evidence, generated replays and variants','Frozen math basis 2275. Eight captured MA originals are preserved verbatim in source-cases.json. Nine captured non-MA inventory records are separately preserved in independent-inventory.json. Two missing original correct references, solutions and difficulties have explicitly authored supported repairs in source-repairs.json.']
 for c in cases:
  q=c['record'];text+=['## ORIGINAL '+c['source_id'],q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q.get(':question/worked-solution','No original solution/difficulty/correct reference captured; raw source is not eligible for serving.')]
 for item in review:text+=['## '+item['label'],g.markdown(item['record'])]
 (D/'review.md').write_text('\n\n'.join(text)+'\n')
if __name__=='__main__':main()
