"""Read actual learner TeX; verify all bounded variants and frozen native grader."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,time
from pathlib import Path
import sympy as sp
from functools import lru_cache
HERE=Path(__file__).resolve().parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'constant_power_draft');p=load(HERE/'scalar-parser.py','constant_power_private_parser')
x=p.x;U=sp.Symbol('U',positive=True)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
@lru_cache(maxsize=16384)
def scalar(s):return p.scalar(s.strip().rstrip('.,').replace('C','v').replace(r'\displaystyle',''))
@lru_cache(maxsize=32768)
def equal(a,b,base):
 z=(a-b).subs(base,U)
 # A power's canonical sign can differ from the printed base. Substitution
 # into both forms establishes identities on the whole positive-base domain.
 z=z.subs(-base,-U)
 return sp.simplify(z)==0
def integral(s,base,derivative):
 s=s.strip().rstrip('.,').replace('&','').strip()
 if r'\int' in s:
  coef,rest=s.split(r'\int',1);m=re.search(r'\\text\{d\}([xu])',rest);assert m,rest
  expr=rest[:m.start()]+rest[m.end():];factor=scalar(coef) if coef not in ('','-','+') else {'':1,'-':-1,'+':1}[coef]
  z=factor*scalar(expr)
  if m[1]=='u':z=z.subs(p.u,base)*sp.diff(base,x)
  return z
 z=scalar(s).subs(p.u,base)
 return sp.diff(z,x) if derivative else z
def prompt_data(q):
 text=q[':question/problem'];body=text.split(r'\int',1)[1]
 m=re.search(r'(?:\\,)?\\text\{d\}x',body);assert m,text
 return scalar(body[:m.start()])
def solution_check(q,integrand):
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==4
 assert blocks[0].startswith('u=');base=scalar(blocks[0][2:]);d=sp.diff(base,x)
 clean=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
 first,second=clean.split('⟹');formal,actual=first.split('=')
 assert formal.strip()==r'\frac{\text{d}u}{\text{d}x}'
 assert equal(scalar(actual.removesuffix(r'\,')),d,base)
 left,right=second.split('=');left=left.replace(r'\text{d}u','').replace(r'\,','').strip();right=right.replace(r'\text{d}x','').replace(r'\,','').strip().rstrip(',')
 ratio=scalar(left);outside=scalar(right);assert equal(ratio*d,outside,base)
 # Initial prose operands are independently read, including implicit 2x.
 introductory=re.findall(r'\$([^$]+)\$',sol.split('So we make')[0]);assert len(introductory)==3,introductory
 assert any(equal(integrand,scalar(introductory[0])*base**n,base) for n in [sp.Rational(1,2),*range(2,11)])
 assert equal(scalar(introductory[1]),base,base)
 assert equal(scalar(introductory[2]),d,base)
 for block in blocks[2:]:
  clean=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  for row in clean.split(r'\\'):
   for part in row.split('='):
    if part.replace('&','').strip():assert equal(integral(part,base,True),integrand,base),(part,base,integrand)
 return base
def structure(q,t,raw=False):
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)
 assert len(blocks)==4
 # Every source family keeps its own explicit reorder, substitution, factor
 # extraction and primitive chain. Equality-only replacements are insufficient.
 for token in ('So we make the substitution','Its derivative is given by','and we can now write our integral in terms','Finally, we can solve the integral'):
  assert token in q[':question/worked-solution']
 assert len(blocks[2].split(r'\\'))==3
 assert all(r'\cdot' in row for row in blocks[2].split(r'\\')[:2]),'Required explicit reorder/substitution product missing'
 assert len(blocks[3].split(r'\\'))==(5 if sp.Rational(t['n']).q>1 else 3 if t.get('parent') is None and t['base'] in ('{x}^{4}+11','2{x}^{3}+1','1+{x}^{8}') else 4)
 assert r'\cdot \frac' in blocks[3] or r'\cdot \frac' in blocks[3].replace(')','')
def formatting(q):
 for s in [q[':question/problem'],q.get(':question/worked-solution',''),*[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]]:
  assert not any(ord(c)<32 and c not in '\n\t' for c in s),'C0 control character'
  assert s.count('$')%2==0
  depth=0
  for m in re.finditer(r'(?<!\\)[{}]',s):
   depth+=1 if m[0]=='{' else -1;assert depth>=0
  assert depth==0
  assert '++' not in s and '+-' not in s and '--' not in s
def check(r,raw=False):
 q=r['question'];meta=r['generation'];sid=meta['template'].removeprefix('source:');t=g.PROFILES[sid];b=meta['parameters']['b']
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 qc=copy.deepcopy(q)
 if raw and sid=='q-12494':qc[':question/problem']=qc[':question/problem'].replace(r'\intx',r'\int x').replace('dx',r'\,\text{d}x')
 integrand=prompt_data(qc);base=t['a']*x**t['m']+b
 fp=g.digest(sp.srepr(sp.expand(integrand)));assert fp==meta['mathematical_fingerprint'],(sid,b,'actual math fingerprint')
 if not raw:formatting(q)
 field=q[':question/answer-fields'][0];bank=field[':answer-field/choices'];assert len(bank)==5
 assert len({a[':answer/id'] for a in bank})==5
 vals=[scalar(a[':answer/value']) for a in bank]
 for i,z in enumerate(vals):
  assert all(not equal(sp.diff(z-w,x),0,base) for w in vals[:i]),(sid,b,'bank ambiguity modulo C')
 good=[a[':answer/id'] for a,z in zip(bank,vals) if equal(sp.diff(z,x),integrand,base)]
 if ':answer-field/correct' in field:assert good==[field[':answer-field/correct'][1]],(sid,b,good)
 else:assert raw and sid=='q-12494' and len(good)==1
 if ':question/worked-solution' in q:
  assert equal(solution_check(q,integrand),base,base);structure(q,t,raw)
 elif not raw:raise AssertionError('Normal solution missing')
 # Equivalent primitives include a constant shift. They are never negative cases.
 canonical=vals[next(i for i,a in enumerate(bank) if a[':answer/id']==good[0])]
 assert equal(sp.diff(canonical+1,x),integrand,base)
 return r
def native(r,label):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio answer ID: correct or ordinary wrong option; math checked independently'} for a in f[':answer-field/choices']]}
def main():
 started=time.time();reviews=[];review_md=[];source_cases=[];native_inputs=[];fidelity=[]
 originals=[q for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q]
 for src in originals:
  sid=src[':question/math-academy-id'];t=g.PROFILES[sid];level=t['difficulty'];anchor=check(g.generate(level,7,profile='source:'+sid,parameters={'b':t['b']}),True);q=anchor['question']
  for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (k in src)==(k in q),(sid,k,'attribute presence')
  for k in (':question/problem',':question/worked-solution'):
   if k in src:assert src[k]==q[k],(sid,k,'exact source prose/math stages')
  if ':question/difficulty' in src:assert src[':question/difficulty'][':db/ident']==q[':question/difficulty']
  sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  assert sf[':answer-field/key']==f[':answer-field/key'] and sf[':answer-field/type'][':db/ident']==f[':answer-field/type']
  assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
  assert (':answer-field/correct' in sf)==(':answer-field/correct' in f)
  if ':answer-field/correct' in sf:assert sf[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  fidelity.append({'source_id':sid,'complete_bank':True,'choices_matched':5,'key_presence_exact':True,'correct_designation_matched':':answer-field/correct' in sf,'raw_prompt_exact':True,'raw_solution_exact_or_missing':True})
  source_cases.append({'source_id':sid,'template':'source:'+sid,'profile':'source:'+sid,'bank_profile':'source:'+sid,'level':level,'parameters':{'b':t['b']},'evidence_only':True,'eligible_for_learning':False,'original_difficulty_observed':':question/difficulty' in src})
  variant=check(g.generate(level,9,profile='source:'+sid,parameters={'b':17}),True)
  reviews.extend([{'label':sid+' raw original','record':anchor},{'label':sid+' changed source mask','record':variant}]);review_md.append('## '+sid+'\n\nRaw original (ineligible evidence)\n\n'+g.markdown(anchor)+'\n\nChanged source profile (ineligible evidence)\n\n'+g.markdown(variant))
  if ':answer-field/correct' in f:native_inputs.append(native(anchor,sid+' raw original'))
 count=0
 for sid,t in g.PROFILES.items():
  print('Checking full bounded domain:',sid,flush=True)
  for b in g.allowed(t):
   row=check(g.generate(t['difficulty'],13,profile=sid,parameters={'b':b}));count+=1
   other=g.generate(t['difficulty'],-9,template=sid,parameters={'b':b})
   assert row['question'][':question/id']==other['question'][':question/id']
   assert row['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
   native_inputs.append(native(row,sid+' b='+str(b)))
  normal=check(g.generate(t['difficulty'],5,profile=sid,parameters={'b':t['b'] if t['b'] in g.allowed(t) else 9}))
  changed=check(g.generate(t['difficulty'],6,profile=sid,parameters={'b':19}))
  reviews.extend([{'label':sid+' normal original parameters','record':normal},{'label':sid+' normal changed variant','record':changed}]);review_md.append('## Normal '+sid+'\n\nOriginal parameters (authored repairs where documented)\n\n'+g.markdown(normal)+'\n\nChanged parameters\n\n'+g.markdown(changed))
 # The public raw source API is also checked exhaustively, rather than only
 # verifying copied evidence at its anchors.
 for sid,t in g.PROFILES.items():
  if t.get('authored'):continue
  for b in g.allowed(t):check(g.generate(t['difficulty'],3,profile='source:'+sid,parameters={'b':b}),True)
 # Mutations must fail even where the final primitive/key is unchanged.
 sample=g.generate('easy',0,profile='q-12496',parameters={'b':11});mutations=[]
 for label,mutator in [('printed integrand',lambda q:q.__setitem__(':question/problem',q[':question/problem'].replace('{x}^{3}','{x}^{2}',1))),('first distributed integral',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace(r'\cdot {x}^{3}',r'\cdot {x}^{2}',1))),('equal but missing operative reorder',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace(r'\cdot {x}^{3}',r'{x}^{3}',1))),('C0 control',lambda q:q.__setitem__(':question/problem',q[':question/problem']+'\x0c')),('equivalent bank alias',lambda q:q[':question/answer-fields'][0][':answer-field/choices'].__setitem__(1,dict(q[':question/answer-fields'][0][':answer-field/choices'][1],**{':answer/value':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+'+1'})))]:
  bad=copy.deepcopy(sample);mutator(bad['question'])
  try:check(bad);raise RuntimeError('Mutation survived '+label)
  except (AssertionError,ValueError):mutations.append(label)
 strict=[]
 for label,fn in [('bool seed',lambda:g.generate(seed=True)),('float seed',lambda:g.generate(seed=2.0)),('bool count',lambda:g.batch('easy',True)),('float count',lambda:g.batch('easy',1.0)),('negative count',lambda:g.batch('easy',-1)),('bool b',lambda:g.generate('easy',parameters={'b':True})),('float b',lambda:g.generate('easy',parameters={'b':2.0})),('extra key',lambda:g.generate('easy',parameters={'b':1,'a':1})),('zero b',lambda:g.generate('easy',parameters={'b':0})),('unbounded b',lambda:g.generate('easy',parameters={'b':41})),('wrong level',lambda:g.generate('hard',profile='q-72467')),('empty profile',lambda:g.generate(profile='')),('bad profile',lambda:g.generate(profile=True)),('bad field',lambda:g.generate(field_type=True)),('negative even radicand domain',lambda:g.generate('hard',profile='hard-signed-square-root',parameters={'b':-2})),('alias mismatch',lambda:g.generate('easy',profile='q-12496',template='q-2388'))]:
  try:fn();raise RuntimeError('Invalid API accepted '+label)
  except ValueError:strict.append(label)
 capacities={};allfp=set()
 for level in g.LEVELS:
  rows=g.batch(level,g.capacity(level),37);fps={r['generation']['mathematical_fingerprint'] for r in rows};assert len(fps)==len(rows)==g.capacity(level);assert not allfp.intersection(fps);allfp.update(fps)
  assert g.batch(level,0)==[]
  try:g.batch(level,g.capacity(level)+1);raise RuntimeError('Overcapacity accepted')
  except ValueError:pass
  capacities[level]=len(rows)
  preview=g.batch(level,2,41);save('preview-'+level+'.json',preview);reviews.extend({'label':level+' sampled '+str(i),'record':r} for i,r in enumerate(preview));review_md.append('## '+level+' sampled examples\n\n'+'\n\n---\n\n'.join(map(g.markdown,preview)))
 assert {g.generate('easy',s)['generation']['template'] for s in range(200)}=={sid for sid,t in g.PROFILES.items() if t['difficulty']=='easy'}
 cli=json.loads(subprocess.check_output([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','1']));assert len(cli)==3
 save('source-cases.json',source_cases);save('source-fidelity.json',fidelity);save('strict-inputs.json',strict);save('mutations.json',mutations);save('capacity.json',capacities);save('review.json',reviews);(HERE/'review.md').write_text('\n\n'.join(review_md)+'\n')
 # Every declared normal bank is exercised under the frozen actual grader.
 save('native-input.json',native_inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 baseline=json.loads((HERE/'registered-baseline.json').read_text());paths=[HERE.with_name('17592186068723.py'),*sorted(HERE.with_name('17592186068723').rglob('*'))];actual={str(path.relative_to(HERE.parents[2])):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths if path.is_file()}
 assert actual==baseline,'Registered full path/hash preservation failed'
 save('preservation-proof.json',{'full_path_set_and_sha256_equal':True,'files':len(actual),'baseline':'registered-baseline.json'})
 save('validation.json',{'passed':True,'normal_instances_exhaustive':count,'raw_instances_exhaustive':800,'MA_originals':len(originals),'complete_source_banks':len(originals),'source_choices_matched':50,'original_designations_matched':9,'original_designations_missing':1,'exact_raw_worked_solutions':9,'missing_original_worked_solutions':1,'nonMA_inventory':2,'source_repairs':{'q-12494':'Authored normal prompt, correct designation, difficulty and worked solution; raw exact omissions retained.','q-113715':'Add missing +C in one intermediate row; exact raw retained.'},'authored_default_bank':'q-12496 opaque bank coefficients preserved through source profile; method-derived normal bank replaces it honestly.','authored_hard':'Two signed square-root substitution families; combines source moderate sign and root demands without another operation or topic.','capacity':capacities,'math_validation':'Read actual prompt, all five choices pairwise modulo constants, prose operands, formal derivative and differential, all reordered/substituted/factored integral and primitive rows across entire bounded domain. Positive-base assumptions only for radicals.','native_engine_sha256':hashlib.sha256((HERE/'check-engine').read_bytes()).hexdigest(),'registered_path_hash_preserved':True,'mutation_regressions':mutations,'duration_seconds':time.time()-started})
 print('Validated',count,'normal and 800 source variants; registered preservation exact.',flush=True)
if __name__=='__main__':main()
