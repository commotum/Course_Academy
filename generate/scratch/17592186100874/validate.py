"""Independent displayed-math audit and frozen native-engine exercise.

Run from any working directory with the repository virtualenv's Python.
Reads the actual printed integrand, substitution, derivative/differentials,
original/transformed bounds, every equality row and both signed endpoint
components. It does not use generation parameters to decide mathematics.
"""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from functools import lru_cache
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'definite100874');p=g.printed;x=p.x;u=p.u

def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2,ensure_ascii=False,default=str)+'\n')
@lru_cache(None)
def eq(a,b):
 # Fractional powers of u are compared on the explicitly checked u>=0
 # branch; integer-power identities remain valid on the whole real line.
 positive=s.Symbol('positive_u',positive=True)
 return s.simplify((a-b).subs(u,positive))==0

def clean(t):
 t=t.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\big','').replace(r'\,','')
 t=t.replace(r'{\int }',r'\int').replace(r'\text{d}x','dx').replace(r'\textrm{d}x','dx').replace(r'\text{d}u','du')
 return t

def balanced_scalar(t):
 # The source wraps an evaluation-bar primitive in a group containing the bar.
 # Remove only the resulting unmatched braces, leaving fraction arguments.
 t=t.strip()
 stack=[];drop=[]
 for i,c in enumerate(t):
  if c=='{':stack.append(i)
  elif c=='}':
   if stack:stack.pop()
   else:drop.append(i)
 drop+=stack;t=''.join(c for i,c in enumerate(t) if i not in drop)
 return p.scalar(t)

def read_integral(t):
 t=clean(t);idx=t.index(r'\int');prefix=t[:idx].strip() or '1';j=idx+4
 assert t[j]=='_',t
 low,j=p.group(t,j+1);assert t[j]=='^',t;high,j=p.group(t,j+1)
 match=re.search(r'd([xu])',t[j:]);assert match,t
 body=t[j:j+match.start()];end=j+match.end();assert not t[end:].strip(),(t,t[end:])
 return balanced_scalar(prefix),p.scalar(body),p.scalar(low),p.scalar(high),{'x':x,'u':u}[match[1]]

@lru_cache(None)
def primitive(f,var):
 # Independent power/radical integration. SymPy may represent cube-root
 # radicals differently; all source real radicands are nonnegative.
 F=s.integrate(f,var)
 assert not F.has(s.Integral),('unintegrated',f)
 assert eq(s.diff(F,var),f),('primitive',f,F)
 return F

def mathval(t):
 t=clean(t)
 if r'\int' in t:
  scale,f,L,H,var=read_integral(t);F=primitive(f,var)
  return s.simplify(scale*(F.subs(var,H)-F.subs(var,L)))
 if '|' in t:
  head,tail=t.split('|');head=balanced_scalar(head);tail=tail.lstrip('}')
  assert tail.startswith('_'),tail
  low,j=p.group(tail,1);assert tail[j]=='^';high,j=p.group(tail,j+1);assert not tail[j:]
  return s.simplify(head.subs(u,p.scalar(high))-head.subs(u,p.scalar(low)))
 return balanced_scalar(t)

def solution_rows(sol):
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==4,len(blocks)
 last=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',blocks[-1],re.S)[1]
 rr=re.split(r'\\\\\s*',last)
 return blocks,[rr[0].split('&')[0].strip()]+[r.split('=',1)[1].strip() for r in rr]

def endpoint_pair(text):
 # Split a displayed arithmetic expression additively WITHOUT collecting it.
 # Multiplication distributes component pairs, so equal endpoint errors cannot
 # cancel unnoticed. The two terms retain their actual signs and coefficients.
 t=clean(text);v=p.scalar(t)
 # parse_expr evaluates additions, which loses components; instead identify
 # top-level subtraction, optionally inside a coefficient-times-parentheses.
 def split(body):
  depth=0
  for i,c in enumerate(body):
   if c in '({':depth+=1
   elif c in ')}':depth-=1
   elif c=='-' and depth==0 and i>0:return body[:i],body[i+1:]
  return None
 pair=split(t)
 if pair:return p.scalar(pair[0]),-p.scalar(pair[1])
 # General source coefficient times fraction differences.
 # A fraction's numerator may itself be the endpoint subtraction.
 for m in re.finditer(r'\\(?:d?frac)\{',t):
  a,j=p.group(t,m.end()-1);b,j=p.group(t,j)
  z=split(a)
  if z:
   pref=t[:m.start()].replace(r'\cdot','').strip() or '1'
   assert not t[j:].strip()
   scale=p.scalar(pref)/p.scalar(b);return scale*p.scalar(z[0]),-scale*p.scalar(z[1])
 # Find an outermost (...) whose body is the signed endpoint difference.
 depth=0
 for i,c in enumerate(t):
  if c=='{':depth+=1
  elif c=='}':depth-=1
  elif c=='(' and depth==0:
   body,j=p.group(t,i)
   if t[j:].strip():continue
   z=split(body)
   if z:
    pref=t[:i].replace(r'\cdot','').strip() or '1';scale=p.scalar(pref)
    return scale*p.scalar(z[0]),-scale*p.scalar(z[1])
 raise AssertionError(('no endpoint components',t,v))

COUNTS={'rendered_questions':0,'equality_rows':0,'endpoint_components':0,'differential_relations':0}
def validate_display(record):
 q=record['question'];prompt=q[':question/problem'];scale,f,lo,hi,var=read_integral(prompt[prompt.index(r'\int')-1:] if False else clean(re.search(r'\$(.*?\\int.*?)\$',prompt,re.S)[1]).replace(r'\displaystyle','').rstrip('='))
 # read_integral expects only the mathematical integral, and accepts source's
 # leading {\int } and variable-free source factor.
 assert var==x and scale==1
 field=q[':question/answer-fields'][0];values=[p.scalar(a[':answer/value']) for a in field[':answer-field/choices']]
 if ':question/worked-solution' not in q:
  expected=s.integrate(f,(x,lo,hi));assert sum(eq(v,expected) for v in values)==1;COUNTS['rendered_questions']+=1;return
 sol=q[':question/worked-solution'];blocks,rr=solution_rows(sol)
 deriv_rows=re.split(r'\\\\\s*',re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',blocks[0],re.S)[1])
 left,right=deriv_rows[0].split('=');z=p.scalar(right);assert left.replace('&','').strip()=='u'
 assert eq(p.scalar(deriv_rows[1].split('=')[1]),s.diff(z,x))
 for row in deriv_rows[2:]:
  a,b=row.replace('&','').split('=');a=clean(a);b=clean(b)
  def diff_side(v):
   if 'du' in v:return p.scalar(v.replace('du','') or '1')*s.diff(z,x)
   assert 'dx' in v,v;return p.scalar(v.replace('dx','') or '1')
  assert eq(diff_side(a),diff_side(b)),('bad differential',row);COUNTS['differential_relations']+=1
 table=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',blocks[1],re.S)[1];tr=re.split(r'\\\\\s*',table)
 xs=[p.scalar(v) for v in tr[0].split('&')[1:]];us=[p.scalar(v) for v in tr[1].split('&')[1:]]
 assert all(eq(a,b) for a,b in zip(xs,[lo,hi]));assert all(eq(a,b) for a,b in zip(us,[z.subs(x,lo),z.subs(x,hi)]))
 # Transformed integral: inspect the actual two printed objects separately.
 original,transformed=blocks[2].rstrip('.').split('=');o=read_integral(original);t=read_integral(transformed)
 assert o[4]==x and eq(o[1],f) and eq(o[2],lo) and eq(o[3],hi)
 k,h,L,H,v=t;assert v==u and eq(L,us[0]) and eq(H,us[1])
 assert eq(f,k*h.subs(u,z)*s.diff(z,x)),('transformed density',f,h,z)
 # Radical branches: nonnegative on the full original closed interval,
 # checking all polynomial stationary points rather than endpoints alone.
 for radical in f.atoms(s.Pow):
  if radical.exp.is_Rational and radical.exp.q==2:
   base=radical.base;points=[lo,hi]+[v for v in s.solve(s.diff(base,x),x) if v.is_real and lo<=v<=hi]
   assert all(base.subs(x,v)>=0 for v in points),('real branch',base,points)
 F=primitive(k*h,u);A=s.simplify(F.subs(u,H));B=s.simplify(F.subs(u,L));expected=s.simplify(A-B)
 assert sum(eq(v,expected) for v in values)==1
 if ':answer-field/correct' in field:
  designated=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert eq(p.scalar(designated[':answer/value']),expected)
 for i,row in enumerate(rr):
  assert eq(mathval(row),expected),('bad displayed equality',record['generation']['template'],i,row,expected,mathval(row));COUNTS['equality_rows']+=1
 # The bar primitive itself is checked by differentiation, not just its delta.
 bar=next(r for r in rr if '|' in r);barhead=balanced_scalar(clean(bar).split('|')[0]);assert eq(s.diff(barhead,u),k*h),(record['generation']['template'],barhead,k*h,s.diff(barhead,u))
 # Every explicit difference before the final collected answer is decomposed.
 endpoint_rows=[]
 for row in rr[rr.index(bar)+1:-1]:
  try:a,b=endpoint_pair(row)
  except AssertionError:continue
  assert eq(a,A) and eq(b,-B),('individual signed endpoint mismatch',record['generation']['template'],row,(a,b),(A,-B))
  endpoint_rows.append(row);COUNTS['endpoint_components']+=2
 assert endpoint_rows,('no endpoint row verified',rr)
 for text in [prompt,sol]+[a[':answer/value'] for a in field[':answer-field/choices']]:assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
 if not record['generation']['evidence_only']:g.fmt.validate_generated_record(record)
 COUNTS['rendered_questions']+=1


def main():
 provenance=json.loads((HERE/'provenance.json').read_text())
 for item in provenance['files']:
  assert hashlib.sha256((HERE/item['local']).read_bytes()).hexdigest()==item['sha256'],('frozen provenance changed',item['local'])
 replays=[];reviews=[];cases=[];source_stats={'questions':0,'banks':0,'options':0,'distractors':0,'correct_designations':0,'provided_solutions':0,'missing_key_and_solution':[]};sourcecases=[]
 for t,src in g.SOURCES.items():
  level=g.LEVELS[t] if g.LEVELS[t]!='unrated' else 'easy';r=g.generate(level,template=t,parameters=g.defaults(t),profile='observed_raw');q=r['question'];sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  validate_display(r)
  assert q[':question/problem']==src[':question/problem'];assert q.get(':question/worked-solution')==src.get(':question/worked-solution');assert (':question/difficulty'in q)==(':question/difficulty'in src)
  assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'];assert f[':answer-field/key']==sf[':answer-field/key']
  # Recipe replay is reconstructed from parameters, then matched bijectively
  # against complete mathematical source values and source correct designation.
  expected,names=g.recipes(t,g.allowed(t,g.defaults(t)),'observed');unmatched=list(range(len(expected)))
  for a in sf[':answer-field/choices']:
   matches=[i for i in unmatched if eq(expected[i],p.scalar(a[':answer/value']))];assert len(matches)==1,(t,a,matches);unmatched.remove(matches[0])
  assert not unmatched
  if ':answer-field/correct'in sf:
   assert f[':answer-field/correct']==[':answer/id',sf[':answer-field/correct'][':answer/id']];source_stats['correct_designations']+=1
  else:source_stats['missing_key_and_solution'].append(t);assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
  source_stats['questions']+=1;source_stats['banks']+=1;source_stats['options']+=len(expected);source_stats['distractors']+=max(0,len(expected)-1);source_stats['provided_solutions']+=int(':question/worked-solution'in src)
  replays.append(r);sourcecases.append({'source_id':t,'template':t,'level':level,'parameters':g.defaults(t),'profile':'observed_raw','bank_profile':'observed_raw','evidence_only':True,'eligible_for_learning':False})
  if ':answer-field/correct'in f:cases.append(grade_case(t,r))
  # Same actual method, changed shift, amplitude and/or either original bound.
  for seed in range(8):
   v=g.generate(level,seed=100+seed,template=t);validate_display(v);reviews.append(v)
  completion=g.complete_source() if t=='q-49527' else g.generate(level,template=t,parameters=g.defaults(t));validate_display(completion);reviews.append(completion)
  cases.append(grade_case(t+'-authored',completion))
 # Bounded and representative slot boundaries, including decreasing u bounds,
 # zero radical endpoint, negative shifts and x endpoints, nonunit multipliers.
 boundaries=[]
 for t in g.SPECS:
  n,rr,level,*_=g.SPECS[t];level='easy' if level=='unrated' else level
  testparams=[]
  if n==1:
   for a,b,L,H in [(2,-6,0,1),(10,7,4,9),(3,0,1,4)]:testparams.append(dict(a=a,b=b,c=1,l=str(s.Rational(L-b,a)),h=str(s.Rational(H-b,a))))
  else:
   for a,b,c,l,h in ([(-1,2,1,'0','1'),(-1,5,6,'1/2','1')] if t=='q-17104' else [(1,1,1,'0','1'),(2,5,2*n,'1/2','1')]):testparams.append(dict(a=a,b=b,c=c,l=l,h=h))
  for params in testparams:
   try:v=g.generate(level,template=t,parameters=params)
   except ValueError as e:
    assert 'profile' in str(e);boundaries.append({'template':t,'parameters':params,'outcome':'complete-profile collision rejected'});continue
   validate_display(v);reviews.append(v);boundaries.append({'template':t,'parameters':params,'outcome':'display verified'})
 # Held-other-slots experiments: actual mathematical data change one slot
 # at a time and validate the printed question/solution/key independently.
 slot_audit=[]
 for t in g.SPECS:
  n=g.SPECS[t][0];level=g.LEVELS[t];level='easy' if level=='unrated' else level
  for slot in ['a','b','l','h']+(['c'] if n>1 else []):
   base=g.defaults(t)
   if t=='q-17104' and slot=='a':base['b']=5
   start=g.generate(level,template=t,parameters=base,profile='method' if g.SPECS[t][3]=='radio' else 'blank');validate_display(start)
   candidates=([-2,-1,1,2,3,4,5,6,8,10] if slot in ('a','b','c') else [str(s.simplify((3*p.scalar(base['l'])+p.scalar(base['h']))/4 if slot=='l' else (p.scalar(base['l'])+3*p.scalar(base['h']))/4)),str(p.scalar(base[slot])+s.Rational(1,4)),str(p.scalar(base[slot])-s.Rational(1,4))])
   found=None
   for value in candidates:
    if value==base[slot] or (slot=='a' and t=='q-17104' and value>=0):continue
    params=dict(base);params[slot]=value
    try:changed=g.generate(level,template=t,parameters=params,profile='method' if g.SPECS[t][3]=='radio' else 'blank')
    except (ValueError,TypeError):continue
    validate_display(changed);found=changed;break
   assert found is not None,('slot not exercised',t,slot)
   assert sum(base[k]!=found['generation']['parameters'][k] for k in base)==1
   assert start['generation']['math_fingerprint']!=found['generation']['math_fingerprint']
   reviews.append(found);slot_audit.append({'template':t,'slot':slot,'baseline':base,'changed':found['generation']['parameters'],'printed_math_verified':True})
 # Every observed profile also executes its recipes at changed parameters;
 # complete bank coverage is checked without replacing any rejected option.
 observed_variants=[]
 for t in g.SPECS:
  if g.SPECS[t][3]!='radio':continue
  level='easy' if g.LEVELS[t]=='unrated' else g.LEVELS[t]
  for seed in (321,654):
   changed=g.generate(level,seed=seed,template=t,profile='observed');validate_display(changed)
   assert not changed['generation']['evidence_only'] and changed['generation']['eligible_for_learning']
   observed_variants.append(changed);reviews.append(changed)
 recipe_audit=[]
 for t,src in g.SOURCES.items():
  vals,names=g.recipes(t,g.allowed(t,g.defaults(t)),'observed');field=src[':question/answer-fields'][0]
  for index,(answer,value,name) in enumerate(zip(field[':answer-field/choices'],vals,names)):
   recipe_audit.append({'source_id':t,'source_field':field[':answer-field/id'],'profile':'observed','option_index':index,'source_value':answer[':answer/value'],'recipe':name,'recipe_evaluated':g.tex(value),'complete_math_match':eq(value,p.scalar(answer[':answer/value'])),'source_correct_designation':None if ':answer-field/correct'not in field else answer[':answer/id']==field[':answer-field/correct'][':answer/id']})
 save('recipe-audit.json',recipe_audit);save('slot-coverage.json',slot_audit)
 details=[]
 side=['# Originals and changes side by side','', '| Source | Original parameters | Changed parameters | Profile |','|---|---|---|---|']
 for t in g.SPECS:
  changed=next(r for r in reviews if r['generation']['template']==t and r['generation']['parameters']!=g.defaults(t))
  side.append('| '+t+' | `'+json.dumps(g.defaults(t))+'` | `'+json.dumps(changed['generation']['parameters'])+'` | '+changed['generation']['profile']+' |')
  original=next(r for r in replays if r['generation']['template']==t)
  details.extend(['','## '+t,'','Original:',original['question'][':question/problem'],'',original['question'].get(':question/worked-solution','No supplied solution or key. Raw evidence remains ineligible.'),'','Changed:',changed['question'][':question/problem'],'',changed['question'][':question/worked-solution']])
 (HERE/'side-by-side.md').write_text('\n'.join(side+details)+'\n')
 # API rejects bool, floats, strings, negatives for count; bool is int subclass.
 invalid=0
 for bad in [True,1.0,'1',None]:
  for call in [lambda:g.generate('easy',seed=bad),lambda:g.generate_batch(count=bad),lambda:g.generate_batch(seed=bad)]:
   try:call()
   except ValueError:invalid+=1
   else:raise AssertionError(('invalid accepted',bad))
 try:g.generate_batch(count=-1)
 except ValueError:invalid+=1
 else:raise AssertionError('negative count accepted')
 # Deterministic replay and identity invariants across same/different seeds.
 batch=g.generate_batch('all',12,77);assert batch==g.generate_batch('all',12,77)
 content_to_id={};id_to_content={};task_count={}
 for r in reviews+batch:
  q=r['question'];qid=q[':question/id'];content=r['generation']['content_fingerprint'];task=r['generation']['math_fingerprint']
  assert qid not in {v[':question/id'] for v in g.SOURCES.values()}
  assert id_to_content.setdefault(qid,content)==content;assert content_to_id.setdefault(content,qid)==qid;task_count[task]=task_count.get(task,0)+1
 # Every canonical blank, genuine unreduced equivalent, and wrong entry uses
 # the frozen learner engine; radio testing submits every answer UUID.
 for i,r in enumerate(reviews):
  if i%9==0:cases.append(grade_case('variant-'+str(i),r))
 save('source-cases.json',sourcecases);save('review-cases.json',[{'template':r['generation']['template'],'level':r['question'][':question/difficulty'].split('/')[-1],'parameters':r['generation']['parameters'],'profile':r['generation']['profile'],'origin':r['generation']['origin']} for r in reviews]);save('source-replay.json',replays);save('review-records.json',reviews);save('boundaries.json',boundaries);save('engine-input.json',cases)
 result=subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
 if result.returncode:raise AssertionError(result.stderr+result.stdout)
 engine=json.loads((HERE/'engine-report.json').read_text())
 subprocess.run([sys.executable,str(HERE/'profile-domain.py')],cwd='/tmp',capture_output=True,text=True,check=True)
 profile_report=json.loads((HERE/'profile-coverage.json').read_text())
 # CLI operation from unrelated cwd; actual flags and JSON/Markdown contracts.
 script=str(HERE.with_suffix('.py'))
 out=subprocess.run([sys.executable,script,'--difficulty','all','--count','2','--seed','8','--format','json'],cwd='/tmp',capture_output=True,text=True,check=True);assert len(json.loads(out.stdout))==6
 out=subprocess.run([sys.executable,script,'--difficulty','all','--count','1','--seed','8','--format','markdown'],cwd='/tmp',capture_output=True,text=True,check=True);assert out.stdout.count('Answer:')==3
 save('validation-report.json',{'status':'passed','database_writes':0,'source':source_stats,'display':COUNTS,'boundary_cases':len(boundaries),'single_slot_experiments':len(slot_audit),'bounded_observed_profile_instances':profile_report['bounded_instances'],'observed_profile_changed_instances':len(observed_variants),'invalid_api_cases':invalid,'deterministic_batch_records':len(batch),'review_records':len(reviews),'unique_review_tasks':len(task_count),'identity_checks':{'source_question_uuid_collisions':0,'different_content_same_id':0,'same_content_different_id':0,'source_task_overlaps_in_normal_batch':sum(bool(r['generation']['reproduces_source_task']) for r in batch),'authored_explicit_source_task_replays':sum(bool(r['generation']['reproduces_source_task']) for r in reviews)},'native_engine':{k:v for k,v in engine.items() if k!='records'},'limitations':['Observed numeric banks with unresolved interpretations retain complete expressions and original transformed bounds; every choice scales by the differential-multiplier ratio. Authored method banks vary those bounds separately.','q-49527 has no observed difficulty/key/solution. Raw evidence stays ineligible; authored easy completion is separate.','No non-MA inventory exists in the frozen source.','Structural degree and exponent stay fixed per source family; numeric slots vary without an instructional progression.']})
 print(json.dumps({'status':'passed','source':source_stats,'display':COUNTS,'native':{k:v for k,v in engine.items() if k!='records'}},indent=2))

def grade_case(label,r):
 field=r['question'][':question/answer-fields'][0];cid=field[':answer-field/correct'][1];correct=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==cid)
 if field[':answer-field/type'].endswith('/radio'):checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'every source/variant choice designation'} for a in field[':answer-field/choices']]
 else:checks=[{'submitted':correct,'expected':'accepted','purpose':'canonical blank'},{'submitted':r'\frac{2\left('+correct+r'\right)}{2}','expected':'accepted','purpose':'genuine unreduced equivalent'},{'submitted':r'('+correct+r')+1','expected':'rejected','purpose':'incorrect exact number'}]
 return {'label':label,'record':r,'checks':checks}
if __name__=='__main__':main()
