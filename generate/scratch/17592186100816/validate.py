"""Independent rendered-input/stage validation; no generator math metadata used.
LogAbs derivative g'/g applies separately to each connected nonzero domain.
Half-power identities are checked after substituting a positive log value, never
with force=True log expansion or a complex logarithm identity.
"""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
H=Path(__file__).parent;ROOT=H.parents[2]
def mod(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
G=mod('kp00816',H.with_suffix('.py'));E=mod('kp00816_readback',H/'rendered_reader.py');x,u,C=E.x,E.u,E.C

def zero(z,positive=False):
 if z==0 or s.cancel(z)==0:return True
 if positive:
  # The actual integrand declares nonnegative/positive inner log for real roots.
  replacements={a:s.Symbol('positive_log_'+str(i),positive=True)for i,a in enumerate(sorted(z.atoms(s.log),key=str))}
  return s.simplify(z.xreplace(replacements))==0
 return False

def check(rec):
 G.fmt.validate_generated_record(rec);q=rec['question'];sol=q[':question/worked-solution'];F,var=E.prompt(q[':question/problem']);assert var==x
 L=E.scalar(re.search(r'\$u\s*=([^$]+)\$',sol)[1].strip().rstrip('.'));D=s.diff(L,x)
 # Check every printed operand of the derivative and reciprocal differential.
 db=next(b for b in re.findall(r'\$\$(.*?)\$\$',sol,re.S)if r'\frac{\text{d}u}'in b)
 derivative,differential=re.split(r'\\quad\\Longrightarrow\\quad|⟹',db)
 dparts=derivative.split('=')[1:];assert dparts
 for part in dparts:assert zero(E.scalar(part.rstrip().rstrip(',.').replace(r'\,',''))-D),('false printed derivative operand',part)
 left,right=differential.split('=');left=left.strip().replace(r'\,','').replace(r'\quad','')
 coeff=left.replace(r'\text{d}u','').strip();coeff=E.scalar(coeff)if coeff else s.Integer(1)
 right=E.fraction_measure(right);right=re.sub(E.DIFF,'',right)
 assert zero(E.scalar(right)-coeff*D),('false reciprocal differential',db)
 half=any(a.exp.q==2 for a in F.atoms(s.Pow));counts=dict(integral_sides=0,primitive_sides=0,formal_inputs=0)
 for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
  if r'\int'not in block:continue
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','')
  for row in text.split(r'\\'):
   for part in row.split('='):
    if not part.strip():continue
    value,inputs=E.side(part,x,L)
    assert zero(value-F,half),('false integral or primitive operand',part,value,F)
    counts['integral_sides'if inputs else'primitive_sides']+=1;counts['formal_inputs']+=len(inputs)
 assert counts['primitive_sides']>=2
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];correct=field[':answer-field/correct'][1];good=[];parsed=[]
 for a in choices:
  v=E.scalar(a[':answer/value']);parsed.append(v)
  valid=zero(E.derivative(v,x)-F,half)and v.has(C)
  if valid:good.append(a[':answer/id'])
 assert good==[correct],('wrong or multiple correct complete primitive families',good,correct)
 for i,v in enumerate(parsed):
  for w in parsed[:i]:assert not zero(v-w,half),'equivalent duplicate choices'
 return counts

def write(name,z):(H/name).write_text(json.dumps(z,indent=2,ensure_ascii=False)+'\n')
source=[];replays=[];ledger=[];reviews=[];allrows=[];coverage={};stats=dict(integral_sides=0,primitive_sides=0,formal_inputs=0)
for sid,config in G.CONFIG.items():
 print('profile '+sid,flush=True)
 level=config[0];r=G.generate(level,template=sid,parameters=G.original(sid));counts=check(r);source.append({'source_id':sid,'record':r});q=G.QS[sid];c,a,n,p=G.parameters(sid,G.original(sid));L=s.log(a*G.x**n);recipes=G.bank(sid,c,a,n,p,L)
 sourcechoices=q[':question/answer-fields'][0][':answer-field/choices'];renderchoices=r['question'][':question/answer-fields'][0][':answer-field/choices']
 # Independent source parse versus the complete computed recipe bank, mapped
 # one-to-one; C is a real symbol and must be retained as a response role.
 unused=set(range(len(recipes)));mapping=[]
 for choice in sourcechoices:
  v=E.scalar(choice[':answer/value']);matches=[]
  for j in unused:
   w=recipes[j].xreplace({G.x:x,G.C:C});
   if zero(v-w,p.q==2):matches.append(j)
  assert len(matches)==1,('unmapped source choice',sid,choice[':answer/value'],matches,recipes)
  j=matches[0];unused.remove(j);mapping.append({'source_answer_id':choice[':answer/id'],'source_value':choice[':answer/value'],'recipe_index':j,'expression_at_original':str(recipes[j]),'matched':True})
 assert not unused
 srcfield=q[':question/answer-fields'][0];srckey=srcfield.get(':answer-field/correct',{}).get(':answer/id')
 expectedid='b74934d9-a8f9-51b9-8fd9-2c5d2d130f1d'if sid=='q-2202'else srckey
 sourcekey=next(z[':answer/value']for z in sourcechoices if z[':answer/id']==expectedid)
 genkey=next(z[':answer/value']for z in renderchoices if z[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]);assert zero(E.scalar(sourcekey)-E.scalar(genkey),p.q==2)
 ledger.append({'source_id':sid,'profile':sid,'choices':mapping});replays.append({'source_id':sid,'bank_matched':len(mapping),'bank_total':len(sourcechoices),'key_matched':True,'completion':sid=='q-2202','prompt_equal_normalized':r['question'][':question/problem']==G.fmt.normalize_prose(q[':question/problem']),'solution_equal_normalized':None if sid=='q-2202'else r['question'][':question/worked-solution']==G.fmt.normalize_prose(q[':question/worked-solution'].replace(r'\cdot  \\',r' \\'))})
 seen=set();cov={k:set()for k in G.original(sid)}
 # 30 deterministic cases per observed complete profile.
 for seed in range(30):
  v=G.generate(level,seed=seed,template=sid);cc=check(v);assert cc==counts,('operative stage layout changed',sid,cc,counts);allrows.append(v);seen.add(v['generation']['math_fingerprint'])
  for k,z in v['generation']['parameters'].items():cov[k].add(z)
  for k,z in cc.items():stats[k]+=z
  if seed in(0,1):reviews.append({'source_id':sid,'seed':seed,'record':v})
 coverage[sid]={'distinct_math_tasks_in_30':len(seen),'slots':{k:sorted(v)for k,v in cov.items()}}
# Mutation tests specifically defeat right-final-answer-only validators.
mutations=[]
base=next(z['record']for z in source if z['source_id']=='q-13807')
for label,old,new in [('wrong intermediate derivative',r'\cdot 2x',r'\cdot 3x'),('wrong transformed integral',r'\frac{1}{2}\text{d}u',r'\frac{1}{3}\text{d}u'),('false transformed integral operand',r'\int u\cdot',r'\int u^{2}\cdot'),('wrong primitive coefficient',r'\frac{1}{12}{u}^{2}',r'\frac{1}{13}{u}^{2}')]:
 v=copy.deepcopy(base);assert old in v['question'][':question/worked-solution'];v['question'][':question/worked-solution']=v['question'][':question/worked-solution'].replace(old,new,1)
 try:check(v)
 except(AssertionError,ValueError):mutations.append({'label':label,'caught':True})
 else:raise AssertionError('mutation missed '+label)
# Public deterministic and bounded guard contract.
for level in('easy','moderate','hard'):
 assert G.generate_batch(level,42,10)==G.generate_batch(level,42,10)
for kwargs in({'seed':True},{'seed':1.0}):
 try:G.generate('easy',**kwargs)
 except ValueError:pass
 else:raise AssertionError('seed guard')
for count in(True,1.0,0,-1,101):
 try:G.generate_batch('easy',count=count)
 except ValueError:pass
 else:raise AssertionError('count guard')
cli=subprocess.run([sys.executable,'-B',str(H.with_suffix('.py')),'--count','1'],capture_output=True,text=True,check=True);assert len(json.loads(cli.stdout))==3
write('source-cases.json',source);write('source-replay.json',replays);write('choice-ledger.json',ledger);write('review-cases.json',reviews)
engine=[]
for group,label in[(source,'source'),(reviews,'variant')]:
 for i,row in enumerate(group):
  rec=row['record'];f=rec['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==key else'rejected','purpose':'correct key'if a[':answer/id']==key else'wrong choice'}for a in f[':answer-field/choices']]
  engine.append({'label':label+' '+str(i)+' '+row['source_id'],'record':rec,'checks':checks})
write('native-input.json',engine)
report={'status':'rendered mathematics passed; native pending','sources':15,'rated_source_count':14,'unrated_completions':1,'source_banks':len(replays),'source_choices':sum(z['bank_total']for z in replays),'generated_cases':len(allrows),'distinct_math_tasks':len({z['generation']['math_fingerprint']for z in allrows}),'per_level_distinct_math_tasks':{l:len({z['generation']['math_fingerprint']for z in allrows if z['question'][':question/difficulty'].endswith('/'+l)})for l in('easy','moderate','hard')},'coverage':coverage,'rendered_stages':stats,'mutations':mutations,'CLI_all_count1_records':3,'blank_checks':'not applicable; all source and generated fields are radio','database_writes':0}
write('validation.json',report);print(json.dumps(report,indent=2))
