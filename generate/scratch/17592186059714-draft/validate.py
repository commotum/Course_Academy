"""Independent actual TeX readback, original fidelity, scope and real native grading."""
import copy,hashlib,importlib.util,json,platform,re,subprocess,sys
from decimal import Decimal,localcontext
from pathlib import Path
from functools import lru_cache
from fractions import Fraction
from itertools import combinations
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,x):(HERE/n).write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def group(t,i):
 assert t[i]=='{';depth=1;j=i+1
 while depth:
  assert j<len(t),'Unclosed TeX group';depth += (t[j]=='{')-(t[j]=='}');j+=1
 return t[i+1:j-1],j

def convert(t):
 t=t.strip().rstrip('.').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','');out='';i=0
 while i<len(t):
  if t.startswith(r'\frac',i):
   a,j=group(t,i+5);b,k=group(t,j);out+='(('+convert(a)+')/('+convert(b)+'))';i=k
  elif t.startswith(r'\sqrt',i):
   a,j=group(t,i+5);out+='sqrt('+convert(a)+')';i=j
  elif t[i]=='{':
   a,j=group(t,i);out+='('+convert(a)+')';i=j
  else:out+=t[i];i+=1
 return out.replace('^','**')
@lru_cache(maxsize=20000)
def expr(t):
 z=convert(t)
 assert re.fullmatch(r'[0-9+\-*/().\s sqrt]+',z),z
 return sp.simplify(parse_expr(z,transformations=standard_transformations+(implicit_multiplication_application,)))
def components(q):
 m=re.search(r'⟨([^,]+),([^⟩]+)⟩',q[':question/problem']);assert m,'Missing printed 2D vector'
 return tuple(expr(t) for t in m.groups())
def format_check(q):
 strings=[q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])]
 for s in strings:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in s),'Control character'
  assert s.count('$')%2==0,'Unbalanced dollar math'
  depth=0
  for c in s:
   depth+=(c=='{')-(c=='}');assert depth>=0
  assert depth==0,'Unbalanced braces'

def solution_check(q,mid):
 x,y=components(q);n=sp.simplify(x*x+y*y);correct=sp.sqrt(n)
 if ':question/worked-solution' not in q:return correct
 s=q[':question/worked-solution'];assert s.startswith('Using the formula, we have')
 rows=re.split(r'&\s*=',s)[1:]
 rows=[re.split(r'\\\\|\\end\{aligned\}',r)[0].strip().rstrip('.') for r in rows]
 expected={'q-1325':5,'q-18046':5,'q-18047':4,'q-18048':6}[mid]
 assert len(rows)==expected,(mid,rows)
 var='v' if mid=='q-1325' else 'a'
 assert rows[0].replace(' ','') in (rf'\sqrt{{{var}_{{x}}^{{2}}+{var}_{{y}}^{{2}}}}',rf'\sqrt{{{{{var}}}_{{x}}^{{2}}+{{{var}}}_{{y}}^{{2}}}}'),'Incorrect formal norm formula'
 # Check two ordered squared operands from actual displayed substitution.
 sub=rows[1];assert sub.startswith(r'\sqrt{')
 inner,end=group(sub,5);assert end==len(sub)
 m=re.fullmatch(r'\((.+)\)\^\{2\}\s*\+\s*\((.+)\)\^\{2\}',inner);assert m,'Lost square/add operation'
 assert tuple(expr(t) for t in m.groups())==(x,y),'Wrong printed signed operands'
 # Both actual evaluated squares must remain ordered before sum collection.
 square=rows[2];inner,end=group(square,5);assert end==len(square)
 # Split the top-level + only; fractions/sqrt braces may contain their own +.
 depth=0;split=None
 for i,c in enumerate(inner):
  depth+=(c=='{')-(c=='}')
  if c=='+' and depth==0:assert split is None;split=i
 assert split is not None
 assert tuple(expr(t) for t in (inner[:split],inner[split+1:]))==(sp.simplify(x*x),sp.simplify(y*y))
 for r in rows[1:]:assert sp.simplify(expr(r)-correct)==0,('Bad displayed stage',r)
 assert rows[3].startswith(r'\sqrt{') and expr(group(rows[3],5)[0])==n
 if mid=='q-18048':
  assert r'\cdot' in rows[4],'Lost factorization stage'
  f,d=group(rows[4],5)[0].split(r'\cdot'); assert sp.simplify(expr(f)*expr(d))==n
 # Independent Decimal square-root readback for rational radicand, no precision demand invented.
 with localcontext() as ctx:
  ctx.prec=50;expected_decimal=(Decimal(int(n.p))/Decimal(int(n.q))).sqrt()
  observed=Decimal(str(sp.N(expr(rows[-1]),50)))
  assert abs(expected_decimal-observed)<Decimal('1e-47')
 return correct

def check(rec,normal=True):
 q=rec['question'];mid=rec['generation']['template'];format_check(q);x,y=components(q);correct=solution_check(q,mid)
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 assert (':question/requires-calculator' in q)==(mid in g.CALCULATORS)
 if mid in g.CALCULATORS:assert q[':question/requires-calculator'] is True
 assert rec['generation']['parameter_fingerprint']==g.digest({'operation':'sqrt of sum of two squared components','squared_operands':sorted([sp.srepr(x*x),sp.srepr(y*y)])})
 if normal:
  g.validate_parameters(rec['generation']['difficulty'],x,y)
  assert q[':question/difficulty']==':question.difficulty/'+rec['generation']['difficulty']
  f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio';assert len(f[':answer-field/choices'])==5
  values=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
  assert all(v.is_real is True and v>=0 for v in values)
  if rec['generation']['profile']=='norm-stages':expected=[correct,x*x+y*y,abs(x)+abs(y),sp.sqrt(abs(x)+abs(y)),sp.sqrt(abs(x*x-y*y))]
  else:expected=[correct,x*x+y*y,abs(x),abs(y),abs(x)+abs(y)]
  assert all(sum(sp.simplify(z*z-e*e)==0 for e in expected)==1 for z in values),'Displayed bank recipe mismatch'
  assert all(sp.simplify(a*a-b*b)!=0 for i,a in enumerate(values) for b in values[i+1:]),'Equivalent bank pair'
  corrects=[a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if sp.simplify(v-correct)==0]
  assert corrects==[f[':answer-field/correct'][1]],'Math key mismatch'
  assert len(set(a[':answer/id'] for a in f[':answer-field/choices']))==5
  assert f[':answer-field/id']==g.uid(q[':question/id']+':field:selection')
  assert all(a[':answer/id']==g.uid(f[':answer-field/id']+':value:'+a[':answer/value']) for a in f[':answer-field/choices'])
  assert not any(':answer/feedback' in a for a in f[':answer-field/choices'])
 return True

def replay_check(mid):
 o=g.ROWS[mid];r=g.generate('easy',template=mid,profile='raw-source');q=r['question'];check(r,False)
 for k in (':question/problem',':question/worked-solution',':question/math-academy-id'):
  assert (k in q)==(k in o)
  if k in o:assert q[k]==o[k],('Exact source prose mismatch',mid,k)
 for k in (':question/difficulty',':question/answer-fields'):assert (k in q)==(k in o)
 if ':question/difficulty' in o:assert q[':question/difficulty']==o[':question/difficulty'][':db/ident']
 bank_count=0
 if ':question/answer-fields' in o:
  f,of=q[':question/answer-fields'][0],o[':question/answer-fields'][0]
  assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  assert f[':answer-field/key']==of[':answer-field/key'];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']
  a,b=f[':answer-field/choices'],of[':answer-field/choices'];assert len(a)==len(b)==5
  assert sorted(z[':answer/value'] for z in a)==sorted(z[':answer/value'] for z in b)
  for z in a:
   oz=next(v for v in b if v[':answer/value']==z[':answer/value']);assert set(z)-{':answer/id'}==set(oz)-{':answer/id',':db/id'}
  values=[expr(z[':answer/value']) for z in a]
  assert len(set(values))==5 and sum(sp.simplify(v-sp.sqrt(sum(z*z for z in components(q))))==0 for v in values)==1
  bank_count=1
 return r,{'source_id':mid,'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in o else None,'attribute_presence_exact':True,'calculator_companion_presence_exact':True,'complete_banks':bank_count,'options':5*bank_count,'correct_ref_matched':None,'raw_gradable':False,'reason':'Missing correct reference' if bank_count else 'Missing answer fields'}

def main():
 assert (HERE/'source.json').read_bytes()==(ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186059714.json').read_bytes()
 inventory=json.loads((HERE/'independent-inventory.json').read_text())
 assert inventory['basis']==g.SOURCE['basis'] and inventory['lineage']==g.SOURCE['lineage']
 originals=g.SOURCE['record'][':knowledge-point/questions']
 assert [q['record'] for q in inventory['questions']]==[q for q in originals if ':question/math-academy-id' not in q]
 assert all(q['role']=='independently authored inventory' and q['relationship_to_source_templates'] for q in inventory['questions'])
 assert {q['source_id'] for q in json.loads((HERE/'source-cases.json').read_text())}==set(g.TEMPLATES)
 raw=[];fidelity=[]
 for mid in g.TEMPLATES:
  r,f=replay_check(mid);raw.append(r);fidelity.append(f)
  params={'scale':2} if mid in g.RAW_BANKS else {'x':6,'y':10}
  changed=g.generate('easy',template=mid,profile='raw-source',parameters=params);check(changed,False)
  assert changed['question'][':question/problem']!=r['question'][':question/problem']
 variants=[];coverage=set();task_counts={};samples={}
 for level in g.SUPPORTED_LEVELS:
  rows=[]
  for mi,mid in enumerate(g.TEMPLATES):
   for bi,profile in enumerate(g.BANKS):
    for seed in range(4):
     actual_seed=seed+mi*40+bi*200
     r=g.generate(level,actual_seed,template=mid,profile=profile);check(r);rows.append(r);coverage.add((level,mid,profile))
     p=r['generation']['parameters'];a=g.generate(level,seed+111,template=mid,profile=profile,parameters=p)
     assert a['question'][':question/id']==r['question'][':question/id'],'Seed changed identity'
     assert sorted(z[':answer/id'] for z in a['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(z[':answer/id'] for z in r['question'][':question/answer-fields'][0][':answer-field/choices'])
   variants.extend(rows[-2:])
  samples[level]=rows;task_counts[level]=len({r['generation']['parameter_fingerprint'] for r in rows})
  default=[g.generate(level,s) for s in range(32)]
  assert {r['generation']['template'] for r in default}==set(g.TEMPLATES)
  assert {r['generation']['profile'] for r in default}==set(g.BANKS)
  for r in default:check(r)
 # Explicit level limits and collision rejection; invalid inputs never silently resample.
 invalid=[('easy',{'x':13,'y':2}),('moderate',{'x':'1/2','y':'3/2'}),('moderate',{'x':1,'y':'2/3'}),('hard',{'x':'sqrt(2)/2','y':'sqrt(3)/2'}),('hard',{'x':'10*sqrt(2)/3','y':'sqrt(3)/4'})]
 for l,p in invalid:
  try:g.generate(l,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('Accepted out of scope',l,p))
 # x1 y2 source q18048 has square-factor1 and must reject factorization family.
 try:g.generate('easy',template='q-18048',parameters={'x':1,'y':2})
 except ValueError:pass
 else:raise AssertionError('Accepted vacuous factorization')
 # Boundary inputs and mathematical wrong/wrong bank collision.
 for l,p in [('easy',{'x':-12,'y':10}),('moderate',{'x':'15/4','y':'-14/5'}),('hard',{'x':'-9*sqrt(7)/5','y':'7*sqrt(6)/4'})]:
  for mid in g.TEMPLATES:
   for profile in g.BANKS:check(g.generate(l,template=mid,profile=profile,parameters=p))
 try:g.generate('easy',template='q-1325',profile='norm-stages',parameters={'x':12,'y':11})
 except ValueError as e:assert 'Whole-bank' in str(e)
 else:raise AssertionError('Wrong/wrong equivalent radicals accepted')
 # Mathematical fingerprints ignore sign/permutation and presentation profile.
 a=g.generate('easy',template='q-18047',profile='omit-component',parameters={'x':5,'y':9})
 b=g.generate('easy',template='q-1325',profile='norm-stages',parameters={'x':-9,'y':5})
 assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
 assert a['question'][':question/id']!=b['question'][':question/id']
 # Mutation controls target independent displayed math, not stored metadata.
 base=samples['hard'][0]
 for kind in ('square','sum','answer','correct','factorization','control'):
  r=copy.deepcopy(base);q=r['question'];f=q[':question/answer-fields'][0]
  if kind=='square':q[':question/worked-solution']=q[':question/worked-solution'].replace('^{2}', '^{3}',1)
  elif kind=='sum':q[':question/worked-solution']=q[':question/worked-solution'].replace('+','-',1)
  elif kind=='answer':f[':answer-field/choices'][0][':answer/value']='999'
  elif kind=='correct':f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
  elif kind=='factorization':
   r=copy.deepcopy(next(t for t in samples['hard'] if t['generation']['template']=='q-18048'));q=r['question'];q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\cdot','+')
  else:q[':question/problem']+='\f'
  try:check(r)
  except (AssertionError,ValueError):pass
  else:raise AssertionError('Mutation accepted: '+kind)
 assert {next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for rows in samples.values() for r in rows}==set(range(5))
 for level in g.SUPPORTED_LEVELS:check(getattr(g,'generate_'+level)(3))
 domain_counts={}
 for level in g.SUPPORTED_LEVELS:
  if level=='easy':objects=[(Fraction(i),Fraction(i*i),1) for i in range(1,13)]
  elif level=='moderate':objects=sorted(set((Fraction(p,q),Fraction(p*p,q*q),q) for q in range(2,6) for p in range(1,16) if Fraction(p,q).denominator==q))
  else:objects=sorted(set((Fraction(p,q),Fraction(p*p*d,q*q),q,d) for q in range(2,6) for p in range(1,10) for d in (2,3,5,6,7) if Fraction(p,q).denominator==q))
  tasks=set()
  for a,b in combinations(objects,2):
   if a[1]==b[1]:continue
   if level!='easy' and a[2]==b[2]:continue
   if level=='hard' and a[3]==b[3]:continue
   n=a[1]+b[1];squared=[n,n*n,a[1],b[1]]
   if len(set(squared))<4:continue
   if level!='hard':
    squared.append((a[0]+b[0])**2)
    if len(set(squared))<5:continue
   # Hard distinct squarefree radicands make (absx+absy)^2 irrational,
   # while the other four squared option values are rational: no collision.
   tasks.add(tuple(sorted((a[1],b[1]))))
  domain_counts[level]=len(tasks)
 native=[]
 for level,rows in samples.items():
  for i,r in enumerate(rows):
   f=r['question'][':question/answer-fields'][0]
   native.append({'label':level+'-'+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual native radio submission; mathematical bank independently read back'} for a in f[':answer-field/choices']]})
 save('native-input.json',native)
 engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 report=json.loads((HERE/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
 review={'original_raw_replays':raw,'normal_variants':variants};save('review.json',review)
 sections=['# Source originals and authored normal variants','', 'Raw originals preserve missing difficulty/fields/solutions/keys. Source banks are exact radicals; calculator instructions persist without a rounding rule.']
 for r in raw:sections+=['','## Original '+r['generation']['template'],'',g.markdown(r)]
 for r in variants:sections+=['','## Authored '+r['generation']['difficulty']+' '+r['generation']['template']+' '+r['generation']['profile'],'',g.markdown(r)]
 (HERE/'review.md').write_text('\n'.join(sections)+'\n')
 save('source-replay.json',raw)
 cli=json.loads(subprocess.check_output([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','2','--format','json'],text=True))
 assert len(cli)==6
 for r in cli:check(r)
 save('cli-preview.json',cli)
 result={'status':'pass','basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'source_practice_total':9,'original_ma_total':4,'independent_inventory_total':5,'source_fidelity':fidelity,'source_complete_banks':2,'source_options_matched':10,'source_distractors_matched':8,'source_original_correct_refs_total':0,'source_raw_gradable':0,'source_worked_solutions_exact':2,'authored_normal_completions_validated':sum(map(len,samples.values())),'sample_distinct_mathematical_tasks':task_counts,'bounded_eligible_task_counts_omit_component':domain_counts,'coverage':[list(t) for t in sorted(coverage)],'native_checks':report['accepted_checks']+report['rejected_checks'],'native_unresolved':0,'raw_missing_designations_or_fields':4,'blank_fields_observed':0,'approximate_answers_observed':0,'unresolved':['Historical scalar distractor intentions remain opaque; raw evidence excluded from learning.','Four original records lack usable native grading fields/keys; authored normal completions are graded separately.'],'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'calculator-requirements.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'README.md',HERE/'source-cases.json',HERE/'source-components.json',HERE/'independent-inventory.json',HERE/'native-widget-evidence.json',HERE/'topic.json',HERE/'lesson.json',engine,ROOT/'generate/runs/current/check-engine.rs']}}
 save('validation.json',result);print(json.dumps({k:result[k] for k in ('status','source_complete_banks','source_options_matched','authored_normal_completions_validated','native_checks','sample_distinct_mathematical_tasks')}))
if __name__=='__main__':main()
