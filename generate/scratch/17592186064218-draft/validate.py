"""Independent rendered math and native grading checks; read-only frozen engine."""
import copy,hashlib,importlib.util,json,re,subprocess,itertools,sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('inverse_sine_draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
p=importlib.util.spec_from_file_location('independent_inverse_sine_math',HERE/'math_parser.py');m=importlib.util.module_from_spec(p);p.loader.exec_module(m)
latex=m.latex;clean=m.clean;integrand=m.integrand;X=m.X;U=m.U;C=m.C
ENGINE=ROOT/'generate/runs/current/check-engine'
def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def normalized(old):
 q=copy.deepcopy(old);q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 return q

def check_question(q,solution=True,key='0'):
 e=integrand(q);shape=sp.Poly(sp.expand(sp.simplify(1/e**2)),X);assert shape.degree()==2 and shape.nth(0)>0 and shape.nth(2)<0 and e.subs(X,0)>0
 f=q[':question/answer-fields'][0]
 assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']==key
 values=[latex(a[':answer/value'])for a in f[':answer-field/choices']];assert len(values)==5
 assert len({a[':answer/id']for a in f[':answer-field/choices']})==5
 if key=='0':assert q[':question/problem'].count('{{0}}')==1
 correct=f[':answer-field/correct'][1];right=next(i for i,a in enumerate(f[':answer-field/choices'])if a[':answer/id']==correct)
 assert all(v.has(C) and sp.diff(v,C)==1 for v in values),'Arbitrary C must remain present'
 assert sp.simplify(sp.diff(values[right],X)-e)==0,('correct primitive',values[right],e)
 # Complete indefinite families: compare derivatives, so shifts in C never count as wrong.
 derivatives=[sp.diff(z,X)for z in values]
 for i,z in enumerate(derivatives):
  for j,w in enumerate(derivatives[:i]):
   difference=sp.simplify(z-w)
   assert difference!=0,('equivalent bank modulo C',i,j)
   # Distinguish nonzero exact symbolic expressions with real witnesses where
   # both functions are real. Different branch domains also preclude equivalence.
   found=False
   for sample in (sp.Rational(1,10007),sp.Rational(-1,7919),sp.Rational(1,97),sp.Rational(-1,89),sp.Rational(1,79),sp.Rational(1,5),sp.Rational(1,3),sp.Rational(2,5),sp.Rational(3,4),sp.Rational(3,2),sp.Rational(5,2)):
    a=sp.N(values[i].subs({X:sample,C:0}),20);b=sp.N(values[j].subs({X:sample,C:0}),20)
    if a.is_real!=b.is_real:found=True;break
    v=sp.N(difference.subs(X,sample),20)
    if v.is_real and v.is_finite and abs(float(v))>1e-10:found=True;break
   assert found,('unresolved bank equivalence',i,j,values)
 if solution:solution_check(q,e)
 return right

def solution_check(q,e=None):
 e=e if e is not None else integrand(q)
 # Extract the actual u-substitution; numerator and square coefficient alone
 # cannot establish that the rendered calculation is right.
 sol=q[':question/worked-solution'];m=re.search(r"substitute \$u=(.*?)\.\$",sol);assert m,sol
 substitution=latex(m[1]);slope=sp.diff(substitution,X);assert not slope.has(X)and slope>0
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);rows_checked=0
 for block in blocks:
  if r'\begin{aligned}'not in block:continue
  s=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  parts=s.split('& =')
  for part in parts:
   part=part.replace(r'\\','').strip().rstrip('.')
   if not part:continue
   if r'\int'in part:
    variable=U if r'\text{d}u'in part else X
    expression=latex(clean(part.replace(r'\int','')))
    if variable==U:expression=expression.subs(U,substitution)*slope
    assert sp.simplify(expression-e)==0,('solution integral',part,e,expression)
   else:
    expression=latex(part).subs(U,substitution)
    assert expression.has(C) and sp.diff(expression,C)==1,('primitive lost arbitrary C',part)
    assert sp.simplify(sp.diff(expression,X)-e)==0,('solution primitive',part)
   rows_checked+=1
 assert rows_checked>=6
 # du/dx and dx/du display must both agree with the parsed substitution.
 diff=next(b for b in blocks if r'\frac{\text{d}u}'in b)
 left,right=diff.split('⟹');displayed=latex(clean(left.split('=')[1]));assert displayed==slope
 inverse=latex(clean(right.split('=')[1]));assert sp.simplify(inverse-1/slope)==0

 # Check every inline identity, including the squared substitution in operative prose.
 for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S):
  text=inline.strip().rstrip('.')
  if '=' in text and not text.startswith('u='):
   left,right=text.split('=',1)
   assert sp.simplify(latex(left)-latex(right))==0,('prose identity',text)
 # Basic formula and any unaligned initial normalization are actual rendered expressions.
 for block in blocks:
  if r'\begin{aligned}'in block or '⟹'in block:continue
  if r'\int'not in block:continue
  parts=block.strip().rstrip('.').split('=')
  for part in parts:
   if r'\int'in part:
    var=U if r'\text{d}u'in part else X
    value=latex(clean(part.replace(r'\int','')))
    if var==U:assert sp.simplify(value-1/sp.sqrt(1-U**2))==0
    else:assert sp.simplify(value-e)==0
   else:
    value=latex(part)
    assert sp.simplify(sp.diff(value,U)-1/sp.sqrt(1-U**2))==0
 return rows_checked


def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'Native radio selection for every complete bank member'}for a in f[':answer-field/choices']]}

def rejected(fn):
 try:fn()
 except (ValueError,AssertionError,TypeError,KeyError,StopIteration):return
 raise AssertionError('Mutation/boundary was accepted')

def main():
 baseline=json.loads((HERE/'registered-baseline.json').read_text())
 registered=ROOT/'generate/scratch/17592186064218'
 paths=[registered.with_suffix('.py')]+[p for p in registered.rglob('*')if p.is_file()]
 assert {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}==baseline
 rows=[];originals=[];source_checks=[];engine=[];review=[];counts={l:set()for l in g.SUPPORTED_LEVELS}
 for sid,(level,template,base,_)in g.PROFILES.items():
  print('Validating source/profile',sid,flush=True)
  old=g.source_record(sid,raw=True);raw=g.generate(level,0,profile=sid,parameters={'t':base},replay=True);q=raw['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem']and q[':question/worked-solution']==old[':question/worked-solution']
  assert [a[':answer/value']for a in f[':answer-field/choices']]==[a[':answer/value']for a in of[':answer-field/choices']]
  assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  check_question(normalized(old),solution=sid!='q-49535',key='selection')
  if sid=='q-49535':rejected(lambda:solution_check(normalized(old)))
  originals.append({'source_id':sid,'record':raw,'raw_source':old,'eligible_for_learning':False,'reason':'Exact immutable MA source evidence; raw q-49535 contains the documented dropped numerator.'})
  source_checks.append({'source_id':sid,'bank_profile':sid,'complete_bank_matched':True,'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'exact_prompt':True,'exact_solution':True,'correct_designation_matched':True,'raw_evidence_only':True,'rendering_normalization':'Generated fields use natural key 0; original source key selection preserved in raw evidence.'})
  first=None
  for params in g.candidates(sid):
   rec=g.generate(level,7,profile=sid,parameters=params);check_question(rec['question']);g._fmt.validate_generated_record(rec)
   assert rec['question']==g.generate(level,999,profile=sid,parameters=params)['question']
   rows.append(rec);counts[level].add(rec['generation']['mathematical_fingerprint']);engine.append(native(sid+' '+str(params),rec))
   if params['t']!=base and first is None:first=rec
  review.append('## '+sid+'\n\n### Original complete bank and solution\n\n'+g.markdown(raw)+'\n\n### Changed parameters / supported repair\n\n'+g.markdown(first or g.generate(level,7,profile=sid,parameters={'t':base})))
 # Hard representative Cartesian boundaries plus independent one-slot changes.
 hard_cases=[dict(zip(g.HARD_DOMAIN,vs))for vs in itertools.product(*[(v[0],v[-1])for v in g.HARD_DOMAIN.values()])if vs[0]!=vs[1]]
 base={k:v[0]for k,v in g.HARD_DOMAIN.items()};base['m']=3
 for k,vs in g.HARD_DOMAIN.items():
  for value in vs:
   param={**base,k:value}
   if param['n']==param['m']:
    if k=='n':param['m']=2
    else:param['n']=4
   hard_cases.append(param)
 unique={json.dumps(p,sort_keys=True):p for p in hard_cases}
 for params in unique.values():
  rec=g.generate('hard',13,parameters=params);check_question(rec['question']);g._fmt.validate_generated_record(rec)
  assert rec['question']==g.generate('hard',999,parameters=params)['question']
  rows.append(rec);counts['hard'].add(rec['generation']['mathematical_fingerprint']);engine.append(native('authored hard '+str(params),rec))
 review.append('## Independently authored hard combination\n\n'+g.markdown(g.generate('hard',13,parameters=base))+'\n\n### Changed only the nonsquare quadratic coefficient\n\n'+g.markdown(g.generate('hard',13,parameters={**base,'m':7})))
 independent=[] # Frozen source contains no question without an MA identifier.
 assert all(q.get(':question/math-academy-id')for q in g.SOURCE['record'][':knowledge-point/questions'])
 save('independent-inventory.json',{'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'questions':independent})
 # Public interface, invalid builtin-int boundaries, deterministic CLI, task diversity.
 for level in g.SUPPORTED_LEVELS:
  for bad in (True,False,'0',0.0,None,sp.Integer(1)):
   rejected(lambda b=bad:g.generate(level,b));rejected(lambda b=bad:g.batch(level,b,1));rejected(lambda b=bad:g.batch(level,1,b))
  for bad in (0,-1):rejected(lambda b=bad:g.batch(level,b,1))
  rejected(lambda:g.batch(level,10000,1))
  previews=g.batch(level,5,2275);assert previews==g.batch(level,5,2275)
  save('preview-'+level+'.json',previews);(HERE/('preview-'+level+'.md')).write_text('\n\n---\n\n'.join(map(g.markdown,previews))+'\n')
 for bad in ('all','Hard',None,True):rejected(lambda b=bad:g.generate(b))
 for p,v in g.PROFILES.items():
  for bad in (-1,0,1,13,True,'2',sp.Integer(v[2])):rejected(lambda b=bad:g.generate(v[0],0,profile=p,parameters={'t':b}))
 rejected(lambda:g.generate('moderate',0,profile='q-49547',parameters={'t':9}))
 rejected(lambda:g.generate('hard',0,parameters={'n':2,'m':2,'a':2,'d':2}))
 rejected(lambda:g.generate('hard',0,template='different',profile=g.HARD_PROFILE))
 for key,domain in g.HARD_DOMAIN.items():
  for bad in (0,domain[-1]+1,True,sp.Integer(domain[0])):rejected(lambda k=key,b=bad:g.generate('hard',0,parameters={**base,k:b}))
 # Mutation tests act on rendered text and choices, independently of metadata.
 test=g.generate('hard',13,parameters=base);mutations=[]
 def mutation(name,alter):
  rec=copy.deepcopy(test);alter(rec['question']);rejected(lambda:check_question(rec['question']));mutations.append(name)
 mutation('wrong rendered prompt numerator',lambda q:q.__setitem__(':question/problem',q[':question/problem'].replace(r'\frac{2}',r'\frac{3}',1)))
 mutation('wrong rendered substitution',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace("substitute $u=",'substitute $u=2*',1)))
 mutation('wrong displayed du/dx',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace(r'\frac{\text{d}u}{\text{d}x}=',r'\frac{\text{d}u}{\text{d}x}=2*',1)))
 mutation('wrong transformed integral',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace(r'1-u^{2}',r'1-2*u^{2}')))
 mutation('missing arbitrary constant',lambda q:q[':question/answer-fields'][0][':answer-field/choices'][0].__setitem__(':answer/value',q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'].replace('+C','')))
 mutation('constant-shift distractor equals correct family',lambda q:q[':question/answer-fields'][0][':answer-field/choices'][1].__setitem__(':answer/value',q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+'+7'))
 mutation('two wrong families collide modulo C',lambda q:q[':question/answer-fields'][0][':answer-field/choices'][2].__setitem__(':answer/value',q[':question/answer-fields'][0][':answer-field/choices'][1][':answer/value']+'+7'))
 mutation('bad natural field key',lambda q:q[':question/answer-fields'][0].__setitem__(':answer-field/key','selection'))
 cli=[sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','2','--seed','2275','--format','json'];one=subprocess.check_output(cli);assert one==subprocess.check_output(cli);assert len(json.loads(one))==6
 cli[-1]='markdown';assert '{{0}}'in subprocess.check_output(cli,text=True)
 save('engine-input.json',engine);subprocess.run([str(ENGINE),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 save('source-cases.json',originals);save('review-cases.json',rows);save('source-replay.json',{'basis':2275,'complete_banks_matched':14,'complete_banks_total':14,'choices_matched':70,'choices_total':70,'distractors_matched':56,'distractors_total':56,'profiles':source_checks,'missing_or_extra_options':[]})
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 capacity={l:set()for l in g.SUPPORTED_LEVELS}
 for p,v in g.PROFILES.items():
  for t in g.domain(p):capacity[v[0]].add(g.mathematical_fingerprint(p,t))
 for vs in itertools.product(*g.HARD_DOMAIN.values()):
  n,mm,a,d=vs
  if n==mm:continue
  capacity['hard'].add(g.digest(sp.sstr(sp.Rational(a,d*n))+'|'+sp.sstr(sp.Rational(mm,n*n))))
 # Original mathematical tasks remain eligible; only duplicates within this batch are excluded.
 for level,expected in (('easy',60),('moderate',37)):
  full=g.batch(level,expected,2275)
  actual={r['generation']['mathematical_fingerprint']for r in full}
  assert actual==capacity[level] and len(full)==expected
  original_tasks={g.mathematical_fingerprint(p,v[2])for p,v in g.PROFILES.items()if v[0]==level}
  assert original_tasks<=actual
  rejected(lambda l=level,n=expected:g.batch(l,n+1,2275))
  assert all(r['generation']['eligible_for_learning']and not r['generation']['evidence_only']for r in full)
 corrected=[r for r in g.batch('easy',60,2275)if r['generation']['profile']=='q-49535']
 assert len(corrected)==1 and corrected[0]['generation']['repairs']==['opening-integral-numerator']
 check_question(corrected[0]['question'])
 save('capacity.json',{'bounded_unique_tasks':{l:len(v)for l,v in capacity.items()},'validated_instances':len(rows),'hard_sampled_parameters':list(unique.values()),'source_held_out_by_batch':False,'batch_deduplication':'Only mathematical tasks already selected within this batch are excluded; valid original-parameter tasks and supported repairs remain eligible','hard_level_policy':'Authored combined existing constant normalization and nonsquare linear scaling; same inverse-sine skill, no new function, operation or progression.'})
 assert {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}==baseline
 assert {str(p.relative_to(ROOT))for p in [registered.with_suffix('.py')]+[p for p in registered.rglob('*')if p.is_file()]}==set(baseline)
 save('validation.json',{'passed':True,'basis':2275,'lineage':g.SOURCE['lineage'],'MA_originals':14,'independently_authored_inventory':0,'source_banks':14,'source_choices':70,'source_distractors':56,'validated_instances':len(rows),'sampled_distinct_tasks':{l:len(v)for l,v in counts.items()},'mutation_checks':mutations,'registered_baseline_files_unchanged':len(baseline),'source_errors':['q-49535 opening worked-solution integral numerator 1 instead of 2; raw ineligible, generated one-character repair'],'grading_limits':['Radio grading checks actual answer selection; mathematical equivalence is independently checked. No observed blank fields, so no unsupported blank-equivalence claims.'],'branch_domain':'Strictly positive original radicand; positive square root; principal arcsin; arbitrary real C; derivative equality modulo C; real domain witnesses distinguish alternative functions.','native_runner':str(ENGINE.relative_to(ROOT))})
 print('Validated',len(rows),'instances; all registered paths and hashes unchanged',flush=True)
if __name__=='__main__':main()
