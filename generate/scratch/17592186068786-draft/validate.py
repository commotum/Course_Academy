#!/usr/bin/env python3
"""Read every displayed formal operand, substitution and ordered integration row."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,functools
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('fractional_draft',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);P=g.PARSER

def save(n,v):(H/n).write_text(json.dumps(v,indent=2)+'\n')
@functools.lru_cache(maxsize=12000)
def zero(expr):return expr==0 or sp.simplify(expr)==0
def eq(a,b):
 if not zero(a-b):raise AssertionError((a,b))
def check(r,structural=True):
 q=r['question'];m=r['generation'];sid=m['template'];t=g.PROFILES[sid];b=m['parameters']['b'];z=P.SYMBOLS[t['variable']];u=P.SYMBOLS['u']
 problem=q[':question/problem'];sol=q[':question/worked-solution'];c,f,dv=P.prompt(problem);assert dv==z;actual=c*f
 expected=t['k']*z**(t['n']-1)/(b+t['sign']*z**t['n'])**sp.Rational(t['power']);eq(actual,expected)
 sub=P.scalar(re.search(r'Let \$u=([^$]+)\.\$',sol)[1]);eq(sub,b+t['sign']*z**t['n'])
 if sid=='authored-easy':
  givens=re.search(r'using \$u=([^$]+)\$ and \$\\text\{d\}u=([^$]+)\$',problem);assert givens
  eq(P.scalar(givens[1]),sub);eq(P.scalar(givens[2].replace(r'\text{d}x','')),sp.diff(sub,z))
 dertext=sol.split(r'\frac{\text{d}u}{\text{d}'+t['variable']+'}=')[1].split('⟹')[0];dertext=dertext.rstrip('\\, ');eq(P.scalar(dertext),sp.diff(sub,z))
 relation=sol.split('⟹')[1].split('$$')[0].strip().rstrip(',');left,right=relation.split('=');coef=left.split(r'\text{d}u')[0].replace(r'\,','').strip();coef=P.scalar(coef) if coef else 1
 rhs=right.replace(r'\text{d}'+t['variable'],'').replace(r'\,','').strip();eq(coef*sp.diff(sub,z),P.scalar(rhs))
 rows=P.rows(sol);formal=[];primitive=[]
 for row in rows:
  if r'\int' in row:
   c,f,v=P.integral(row);formal.append((v,c*f))
   if v==u:
    assert f.free_symbols<={u};eq(c*f,sp.Rational(t['k'],t['sign']*t['n'])*u**(-sp.Rational(t['power'])))
   else:assert v==z;eq(c*f,actual)
  else:
   val=P.scalar(row);primitive.append(val)
   if u in val.free_symbols:
    assert val.free_symbols<={u};eq(sp.diff(val,u),sp.Rational(t['k'],t['sign']*t['n'])*u**(-sp.Rational(t['power'])))
   else:assert val.free_symbols<={z};eq(sp.diff(val,z),actual)
 assert formal[0][0]==z and formal[1][0]==z and formal[2][0]==u
 assert primitive and z in primitive[-1].free_symbols
 # Required factorizations, coefficient extraction and original unsimplified rows
 # are structural obligations in addition to equality; an equivalent deletion fails.
 if structural:
  expected_sol=t['solution'].replace('@@B@@',str(b));assert P.rows(sol)==P.rows(expected_sol)
  assert sol==g.FORMAT.normalize_prose(expected_sol)
 assert rows[0].startswith(r'\int')
 field=q[':question/answer-fields'][0];assert field[':answer-field/type']==':answer-field.type/radio'and field[':answer-field/key']=='selection';bank=field[':answer-field/choices'];assert len(bank)==5
 vals=[P.scalar(a[':answer/value'])for a in bank];ds=[sp.diff(v,z)for v in vals];hits=[a[':answer/id']for a,d in zip(bank,ds)if zero(d-actual)]
 assert hits==[field[':answer-field/correct'][1]]
 for i,a in enumerate(ds):
  for other in ds[i+1:]:assert not zero(a-other)
 for s in [problem,sol,*[a[':answer/value']for a in bank]]:assert not any(ord(c)<32 and c not in '\n\t'for c in s)
 assert g.task_fingerprint(problem,t['level'])==m['mathematical_fingerprint']
 assert r==g.generate(t['level'],m['seed'],sid,m['parameters'],m['profile'],m['option_seed'])
 return {'formal_rows':len(formal),'primitive_rows':len(primitive),'ordered_rows':len(rows)}

def rejects(fn):
 try:fn()
 except (ValueError,TypeError,AssertionError):return True
 raise AssertionError('expected rejection')
def native(r,label):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];vals=f[':answer-field/choices'];checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'radio field authored identity contract'}for a in vals]
 canonical=next(a[':answer/value']for a in vals if a[':answer/id']==correct)
 checks +=[{'submitted':canonical,'expected':'unresolved','purpose':'valid canonical math text is not a radio selection identity'}, {'submitted':'('+canonical.replace('+C','')+')+C','expected':'unresolved','purpose':'equivalent primitive text follows same radio field contract'}, {'submitted':next(a[':answer/value']for a in vals if a[':answer/id']!=correct),'expected':'unresolved','purpose':'ordinary wrong mathematical text is not a radio choice identity'}, {'submitted':'999999','expected':'unresolved','purpose':'foreign choice identity; distinct from valid math text'}, {'submitted':'not math!','expected':'unresolved','purpose':'malformed identity; distinct from valid math text'}]
 return {'label':label,'record':r,'checks':checks}

def main():
 source=json.load(open(H/'source.json'));originals={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};replay=[];all_records=[];native_cases=[];review=[];rowcounts={}
 for sid,t in g.PROFILES.items():
  anchor=g.generate(t['level'],0,sid,{'b':t['parameters'][0]});check(anchor)
  if sid!='authored-easy':
   q=originals[sid];f=q[':question/answer-fields'][0];fresh=anchor['question'];assert fresh[':question/problem']==q[':question/problem'];assert fresh[':question/worked-solution']==q[':question/worked-solution']
   oldvals=sorted(a[':answer/value']for a in f[':answer-field/choices']);newvals=sorted(a[':answer/value']for a in fresh[':question/answer-fields'][0][':answer-field/choices']);assert oldvals==newvals
   assert f[':answer-field/correct'][':answer/value']==t['bank'][0].replace('@@B@@',str(t['parameters'][0]))
   replay.append({'source_id':sid,'prompt_exact':True,'solution_exact':True,'all_ordered_rows':len(P.rows(fresh[':question/worked-solution'])),'bank_count':5,'matched_distractors':4,'complete_bank':True,'correct_designation':True})
  changed=g.generate(t['level'],0,sid,{'b':12});review.append({'template':sid,'original':originals.get(sid),'anchor':anchor,'changed_shift':changed})
  for b in range(1,13):
   r=g.generate(t['level'],0,sid,{'b':b});rowcounts[sid]=check(r);all_records.append(r);native_cases.append(native(r,sid+' b='+str(b)))
   assert g.generate(t['level'],71,sid,{'b':b})['question']==r['question']
   shuffled=g.generate(t['level'],0,sid,{'b':b},option_seed=5)
   if b==1:check(shuffled)
   assert shuffled['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'];assert shuffled['question'][':question/id']==r['question'][':question/id']
 # Incomplete original remains exact immutable full Pull; no invented rating/key/solution.
 incomplete=originals['q-49636'];assert ':question/difficulty'not in incomplete and ':question/worked-solution'not in incomplete;assert ':answer-field/correct'not in incomplete[':question/answer-fields'][0]
 slots={};defaults={}
 for level in g.LEVELS:
  capacity=len(g.eligible(level))*12;records=g.batch(level,capacity,123);assert len({r['generation']['mathematical_fingerprint']for r in records})==capacity
  assert records==g.batch(level,capacity,123);rejects(lambda:g.batch(level,capacity+1,123));slots[level]={'capacity':capacity,'b_values':sorted({r['generation']['parameters']['b']for r in records}),'profiles':sorted({r['generation']['template']for r in records})}
  defaults[level]=sorted({g.generate(level,s)['generation']['template']for s in range(100)});assert defaults[level]==sorted(g.eligible(level))
 # Strict API and selected profiles are exercised outside the CLI parser.
 for val in [True,False,1.0,'1',None]:rejects(lambda:g.generate('easy',val))
 for val in [True,False,1.0,'1',None,-1]:rejects(lambda:g.batch('easy',val,0))
 for p in [{'b':True},{'b':0},{'b':13},{'b':1.0},{'b':'1'},[1],{'b':1,'extra':0},{}]:rejects(lambda:g.generate('easy',0,'authored-easy',p))
 for fn in [lambda:g.generate('easy',0,'q-2389',{'b':1}),lambda:g.generate('hard',0,'q-2389',{'b':1},profile='unknown'),lambda:g.batch('easy',1,0,option_seed=True)]:rejects(fn)
 assert g.batch('easy',0)==[]
 # Mathematical and structural mutations must fail independently of final/key correctness.
 r=g.generate('hard',0,'q-2389',{'b':2});mutations={}
 q=copy.deepcopy(r);q['question'][':question/worked-solution']=q['question'][':question/worked-solution'].replace(r'\frac{3}{3}\int',r'\frac{4}{3}\int');mutations['wrong_intermediate_coefficient']=rejects(lambda:check(q))
 q=copy.deepcopy(r);q['question'][':question/worked-solution']=q['question'][':question/worked-solution'].replace(r'3\int \frac{1}{\sqrt{u}}\cdot \frac{1}{3}',r'\int \frac{1}{\sqrt{u}}');mutations['equivalent_stage_removed']=rejects(lambda:check(q))
 q=copy.deepcopy(r);q['question'][':question/worked-solution']=q['question'][':question/worked-solution'].replace(r'\sqrt{u}',r'\sqrt{x}',1);mutations['formal_operand']=rejects(lambda:check(q))
 q=copy.deepcopy(r);q['question'][':question/problem']+='\x0c';mutations['control_character']=rejects(lambda:check(q))
 save('source-replay.json',{'basis':2275,'lineage':source['lineage'],'complete_banks_matched':9,'complete_banks_total':9,'distractors_matched':36,'distractors_total':36,'profiles':replay,'incomplete_original_references':['q-49636'],'raw_original_count':10,'independent_inventory_count':1})
 save('native-input.json',native_cases);assert hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'native-input.json'),str(H/'native-grading.json')],check=True)
 save('review.json',review);save('previews.json',[r for level in g.LEVELS for r in g.batch(level,3,2275)])
 for fmt in ['json','markdown','md']:
  p=subprocess.run([sys.executable,str(H.with_suffix('.py')),'--difficulty','all','--count','3','--format',fmt],capture_output=True,text=True,check=True)
  if fmt=='json':assert len(json.loads(p.stdout))==9
 baseline=json.load(open(H/'baseline-preservation.json'))['files'];actual={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [ROOT/'generate/scratch/17592186068786.py',*sorted((ROOT/'generate/scratch/17592186068786').rglob('*'))]if p.is_file()};assert baseline==actual
 save('validation.json',{'passed':True,'source_basis':2275,'exhaustive_instances':len(all_records),'profiles':rowcounts,'slot_coverage':slots,'default_profile_coverage':defaults,'source_replay':'9/9 complete banks;36/36 distractors;exact prompt/solution/banks/key; all ten MA records retained','native_entry_point':'course_academy_engine::learning::grade_field','native_checks':json.load(open(H/'native-grading.json'))|{'records':'see native-grading.json'},'mutation_regressions':mutations,'api_contract':'strict built-in int seed/count/option_seed and typed complete b mapping; wrong levels/profiles/out-of-bounds rejected','cli':'all/json/markdown/md: flat three records per level','baseline_preserved':True,'limitations':['No source easy label; easy is explicitly authored scaffolded reciprocal-square substitution.','Incomplete q-49636 remains reference only.','Radio grading accepts choice identities; valid mathematical text is unresolved rather than graded algebraically.']})
if __name__=='__main__':main()
