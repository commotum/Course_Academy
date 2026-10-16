"""Independent actual printed prompt/partial/stages/banks, source fidelity/native QA."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
from functools import lru_cache
D=Path(__file__).resolve().parent;REPO=D.parents[2]
spec=importlib.util.spec_from_file_location('kp_partial_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SYMS={'x':S.Symbol('x',real=True),'y':S.Symbol('y',real=True),'e':S.E,'sin':S.sin,'cos':S.cos,'tan':S.tan,'sec':S.sec,'csc':S.csc,'ln':S.log,'log':S.log,'asin':S.asin,'atan':S.atan,'arcsin':S.asin,'arctan':S.atan,'sqrt':S.sqrt}
def dump(name,obj):(D/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def group(s,i,left='{',right='}'):
 assert s[i]==left,(s,i,left)
 n=1;j=i+1
 while n:
  if s[j]==left:n+=1
  if s[j]==right:n-=1
  j+=1
 return s[i+1:j-1],j
@lru_cache(maxsize=20000)
def parse(t):
 t=t.strip().rstrip('.').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,',' ').replace(r'\!','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
 t=re.sub(r'\\operatorname\{(sin|cos|tan|ln|arcsin|arctan|sec|csc)\}',lambda m:' '+m[1]+' ',t)
 t=re.sub(r'\{(sec|csc)\}\^\{(\d+)\}([xy])',r'\1(\3)^\2',t)
 t=re.sub(r'\\(sin|cos|tan|sec|csc)\^\{(\d+)\}\s*([xy])',r'\1(\3)^\2',t)
 t=re.sub(r'\\(arcsin|arctan|sin|cos|tan|sec|csc|ln|log)\b',r' \1 ',t)
 t=re.sub(r'(sec|csc|sin|cos|tan)\s*\^\{(\d+)\}\s*\{([^{}]+)\}',r'\1(\3)^\2',t)
 t=re.sub(r'\b(sin|cos|tan|sec|csc|ln|log|arcsin|arctan)\s*([xy]|[0-9]+)',r'\1(\2)',t)
 out='';i=0
 while i<len(t):
  d=re.match(r'\\frac\{∂\}\{∂([xy])\}\s*\(',t[i:])
  if d:
   a,j=group(t,i+len(d[0])-1,'(',')');out+='('+str(S.diff(parse(a),SYMS[d[1]]))+')';i=j
  elif t.startswith(r'\frac',i):
   a,j=group(t,i+5);b,i=group(t,j);out+='(('+str(parse(a))+')/('+str(parse(b))+'))'
  elif t.startswith(r'\sqrt',i):
   a,i=group(t,i+5);out+='sqrt('+str(parse(a))+')'
  elif t[i]=='{':
   a,i=group(t,i);out+='('+str(parse(a))+')'
  else:out+=t[i];i+=1
 out=out.replace('E','e')
 try:return parse_expr(out,local_dict=SYMS,transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
 except Exception as e:raise ValueError((t,out)) from e
@lru_cache(maxsize=40000)
def eq(a,b):
 d=S.expand(S.expand_power_exp(a-b))
 if d==0:return True
 if d.has(S.tan,S.sec,S.csc):return S.trigsimp(d)==0
 return S.cancel(d)==0

def printed(q):
 prompt=q[':question/problem'];parts=re.findall(r'\$(.*?)\$',prompt);assert len(parts)==2
 target=re.search(r'∂([xy])\}',parts[0]) or re.search(r'_\{([xy])\}',parts[0]);assert target,parts[0]
 u=SYMS[target[1]];v=SYMS['y' if str(u)=='x' else 'x']
 formula=parts[1].split('=',1)[1];F=parse(formula)
 assert F.free_symbols=={SYMS['x'],SYMS['y']}
 return u,v,F,S.diff(F,u)
def split_terms(text):
 depth=0;start=0;terms=[]
 for i,c in enumerate(text):
  if c in '{(':depth+=1
  elif c in '})':depth-=1
  elif c in '+-' and depth==0 and text[start:i].strip():
   terms.append(text[start:i]);start=i
 terms.append(text[start:]);return terms

def rows(q):
 b=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S);assert len(b)==1
 return [z.split('=',1)[1].strip() for z in b[0].split(r'\\')]
def mathcheck(r,full=True):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 u,v,F,C=printed(q)
 assert r['generation']['target_variable']==str(u) and r['generation']['held_constant_variable']==str(v)
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio'
 bank=[parse(z[':answer/value']) for z in f[':answer-field/choices']];assert len(bank)==5
 for i,a in enumerate(bank):
  assert not a.has(S.zoo,S.oo,S.nan)
  for b in bank[:i]:assert not eq(a,b),'wrong/wrong or correct/wrong collision'
 correct=[a[':answer/id'] for a,e in zip(f[':answer-field/choices'],bank) if eq(e,C)]
 assert len(correct)==1
 if ':answer-field/correct' in f:assert correct==[f[':answer-field/correct'][1]]
 assert len(set(z[':answer/id'] for z in f[':answer-field/choices']))==5
 for s in [q[':question/problem'],q.get(':question/worked-solution',''),*[a[':answer/value'] for a in f[':answer-field/choices']]]:
  assert not any(ord(c)<32 and c not in '\n\t' for c in s)
 if full and ':question/worked-solution' in q:
  solution=q[':question/worked-solution'];rs=rows(q);assert len(rs)==5
  assert 'with respect to $'+str(u)+',$ treating all other variables as constants.' in solution
  assert len(re.findall(r'\\frac\{∂\}\{∂'+str(u)+r'\}',rs[0]))==1
  count=3 if q[':question/difficulty'].endswith('/hard') else 2
  assert [len(re.findall(r'\\frac\{∂\}\{∂'+str(u)+r'\}',rs[i])) for i in (1,2)]==[count,count]
  assert '∂' not in rs[3] and '∂' not in rs[4]
  for z in rs:assert eq(parse(z),C),(z,parse(z),C)
  formula=re.findall(r'\$(.*?)\$',q[':question/problem'])[1].split('=',1)[1].rstrip('.')
  component_derivatives=[S.diff(parse(t),u) for t in split_terms(formula)]
  assert len(component_derivatives)==count
  for stage in rs[1:4]:
   printed_components=split_terms(stage);assert len(printed_components)==count,(stage,printed_components)
   for component,expected in zip(printed_components,component_derivatives):assert eq(parse(component),expected),('ordered component',component,expected)
  # Row2 each derivative acts on a complete target-only component or a held
  # variable/1 for a source constant term. No mixed component may survive.
  for z in re.findall(r'\\frac\{∂\}\{∂'+str(u)+r'\}\(',rs[2]):pass
  for m in re.finditer(r'\\frac\{∂\}\{∂'+str(u)+r'\}\(',rs[2]):
   operand,_=group(rs[2],m.end()-1,'(',')');e=parse(operand)
   assert len(e.free_symbols)<=1,'held data was left inside a mixed derivative'
  # Ordered arithmetic products must survive into evaluated row before collection.
  assert rs[3].count(r'\cdot')>=count-(1 if r['generation']['template']=='asin' else 0)
  if r['generation']['template']=='exp_sum':
   assert r'\cdot' in rs[1] and rs[1].count('e^{')==2,'exponential factorization stage missing'
  if r['generation']['template']=='tan_power':assert r'\cdot' in rs[1],'base factorization stage missing'
 return {'target':str(u),'held':str(v),'function':str(F),'derivative':str(C)}

def sourcecheck():
 cases=[];maps=[];records=[];counts={'questions':0,'banks':0,'choices':0,'distractors':0,'correct_designations':0,'solutions':0,'omitted_keys':0,'missing_original_attributes':3}
 for name,(sid,level,p) in g.SPECS.items():
  if sid is None:continue
  src=g.ORIGINALS[sid];r=g.raw_replay(name);q=r['question'];mathcheck(r)
  su,sv,sF,sC=printed(src);u,v,F,C=printed(q);assert su==u and eq(F,sF)
  sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  matches=[]
  for a in sf[':answer-field/choices']:
   hits=[z for z in f[':answer-field/choices'] if eq(parse(a[':answer/value']),parse(z[':answer/value']))];assert len(hits)==1,(sid,a)
   matches.append({'source_id':a[':answer/id'],'source_value':a[':answer/value'],'recipe_value':hits[0][':answer/value'],'matched':True})
  for k in (':question/difficulty',':question/worked-solution'):assert (k in src)==(k in q)
  assert (':answer-field/correct' in sf)==(':answer-field/correct' in f)
  if ':answer-field/correct' in sf:
   orig=sf[':answer-field/correct'][':answer/value'];new=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert eq(parse(orig),parse(new));counts['correct_designations']+=1
  else:counts['omitted_keys']+=1
  if ':question/worked-solution' in src:
   sr=rows(src);nr=rows(q);assert len(sr)==len(nr)==5
   assert g.MF.normalize_prose(src[':question/worked-solution'].split('$$')[0])==q[':question/worked-solution'].split('$$')[0]
   for a,b in zip(sr,nr):assert eq(parse(a),parse(b)),(sid,a,b)
   # Independent stage fingerprints count ordered partial calls at each row.
   for a,b in zip(sr[:3],nr[:3]):assert a.count(r'\frac{∂}{∂')==b.count(r'\frac{∂}{∂')
   counts['solutions']+=1
  cases.append({'source_id':sid,'template':name,'level':level,'parameters':p,'bank_profile':'raw','raw_omissions':[k for k in (':question/difficulty',':question/worked-solution') if k not in src]})
  maps.append({'source_id':sid,'template':name,'profile':'complete observed bank','choices':matches,'original_correct_present':':answer-field/correct' in sf,'original_solution_present':':question/worked-solution' in src})
  records.append(r);counts['questions']+=1;counts['banks']+=1;counts['choices']+=5;counts['distractors']+=4
 dump('source-cases.json',cases);dump('source-choice-map.json',maps);dump('source-replays.json',records)
 return counts,records

def baseline():
 saved=json.loads((D/'registered-baseline.json').read_text());base=REPO/'generate/scratch';kp='17592186124639'
 paths=[base/(kp+'.py')];t=base/kp
 if t.exists():paths+=list(t.rglob('*'))
 paths+=list((base/'__pycache__').glob(kp+'.*.pyc')) if (base/'__pycache__').exists() else []
 current={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
 assert current==saved['files'],'numeric baseline pathset/hash changed'
 report={'pathset_and_sha256_unchanged':True,'files':current,'script_absent':not paths[0].exists(),'tree_absent':not t.exists(),'matching_sibling_pyc_absent':not any((base/'__pycache__').glob(kp+'.*.pyc')),'frozen_manifest_registration':saved['manifest_registration']};dump('registered-baseline-verification.json',report)
 return report

def native(records):
 ref=D/'reference/grader-build-current.json';info=json.loads(ref.read_text());hashes={info['source']:info['source_sha256'],info['library']:info['library_sha256'],info['binary']:info['binary_sha256'],**info['engine_sources'],**info['dependencies']}
 for path,expected in hashes.items():assert hashlib.sha256((REPO/path).read_bytes()).hexdigest()==expected,path
 dump('native-provenance.json',{'verified_hashes':len(hashes),'binary_sha256':info['binary_sha256'],'reference':str(ref.relative_to(REPO)),'files':hashes})
 input=[]
 for i,r in enumerate(records):
  if ':answer-field/correct' not in r['question'][':question/answer-fields'][0]:continue
  f=r['question'][':question/answer-fields'][0];checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete five-option bank'} for a in f[':answer-field/choices']]
  input.append({'label':str(i),'record':r,'checks':checks})
 dump('engine-input.json',input)
 result=subprocess.run([str(REPO/info['binary']),str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True)
 assert result.returncode==0,result.stderr
 print(result.stdout.strip());return json.loads((D/'engine-report.json').read_text())

def mutation_tests(r):
 passed=[]
 def reject(label,z):
  try:mathcheck(z)
  except (AssertionError,ValueError):passed.append(label);return
  raise AssertionError('mutation escaped '+label)
 z=copy.deepcopy(r);z['question'][':question/problem']=z['question'][':question/problem'].replace('∂x','∂y');reject('target variable with held data fixed',z)
 z=copy.deepcopy(r);z['question'][':question/problem']=z['question'][':question/problem'].replace('f(x,y)=','f(x,y)=2*');reject('printed coefficient',z)
 z=copy.deepcopy(r);z['question'][':question/worked-solution']=z['question'][':question/worked-solution'].replace(r'\cdot','\x0c',1);reject('C0 formfeed',z)
 z=copy.deepcopy(r);f=z['question'][':question/answer-fields'][0];wrong=[a for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1]];wrong[1][':answer/value']=wrong[0][':answer/value'];reject('wrong-wrong bank collision',z)
 z=copy.deepcopy(r);rs=rows(z['question']);z['question'][':question/worked-solution']=z['question'][':question/worked-solution'].replace(rs[2],rs[3]);reject('operative derivative extraction removed',z)
 return passed

def main():
 assert (D/'source.json').read_bytes()==(REPO/'generate/runs/current/refresh-2026-10-14/sources/17592186124639.json').read_bytes()
 counts,originals=sourcecheck();review=[];samples=[];roles=set();coverage={};fps={};defaults=set();boundary_rejections=[]
 for name,(sid,level,p) in g.SPECS.items():
  coverage[name]=0;fps[name]=set()
  # Anchors, both target roles with other data held fixed, integer scope boundaries,
  # two genuinely changed samples for every original family and authored hard.
  params=[dict(p),dict(p,target='y' if p['target']=='x' else 'x')]
  for bound in ('low','high'):
   z={k:('x' if bound=='low' else 'y') if k=='target' else (2 if k in ('n','m','k','base') else 1) if bound=='low' else (4 if k in ('n','m','k','base') else 9) for k in p}
   if name=='exp_sum':z['b']=3 if bound=='low' else 8
   params.append(z)
  for seed in range(8):
   r=g.generate(level,seed+31,template=name);params.append(r['generation']['parameters'])
  for i,z in enumerate(params):
   try:r=g.generate(level,seed=i,template=name,parameters=z)
   except ValueError as e:
    assert i in (2,3) and str(e)=='colliding complete bank';boundary_rejections.append({'template':name,'parameters':z,'reason':str(e)});continue
   mathcheck(r);coverage[name]+=1;samples.append(r);roles.add((name,z['target']));fps[name].add(r['generation']['mathematical_fingerprint'])
   other=g.generate(level,seed=i+999,template=name,parameters=z)
   assert other['question'][':question/id']==r['question'][':question/id'];assert other['question'][':question/answer-fields'][0][':answer-field/id']==r['question'][':question/answer-fields'][0][':answer-field/id']
   if i in (4,5):review.append({'kind':'generated variant' if sid else 'authored missing hard','record':r})
  # Explicit domain guard parity with sampler and strict level boundary.
  for k in p:
   if k=='target':continue
   z=dict(p);z[k]=0
   try:g.generate(level,template=name,parameters=z)
   except ValueError:pass
   else:raise AssertionError('invalid boundary admitted')
 for level in ['easy','moderate','hard']:
  for seed in range(70):
   r=g.generate(level,seed);defaults.add(r['generation']['template'])
 assert defaults==set(g.SPECS),'default family coverage'
 assert len(roles)==2*len(g.SPECS)
 # Semantic dedup ignores source notation/bank aliases but includes actually
 # printed function and partial target. All aliases at fixed parameters same fp.
 r=g.generate('easy',template='sin_poly',parameters=g.SPECS['sin_poly'][2]);mutations=mutation_tests(r)
 for name,key in [('constant_sin','a'),('asin','b')]:
  level=g.SPECS[name][1];p=dict(g.SPECS[name][2]);a=g.generate(level,template=name,parameters=p);p[key]=9;b=g.generate(level,template=name,parameters=p);assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 p=dict(g.SPECS['sin_poly'][2]);a=g.generate('easy',template='sin_poly',parameters=p);p['target']='y';b=g.generate('easy',template='sin_poly',parameters=p);assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 cli=subprocess.run([sys.executable,'-B',str(D.with_suffix('.py')),'--difficulty','all','--format','json'],capture_output=True,text=True,check=True);assert isinstance(json.loads(cli.stdout),list)
 cli_md=subprocess.run([sys.executable,'-B',str(D.with_suffix('.py')),'--difficulty','all','--format','markdown'],capture_output=True,text=True,check=True).stdout
 for level in ('easy','moderate','hard'):assert '### '+level+' — ' in cli_md
 assert cli_md.count('Bank profile: `')==3 and cli_md.count('**correct**')==3
 assert '**correct**' not in g.markdown(g.raw_replay('cos_poly'))
 dump('samples.json',samples);dump('review.json',review)
 native_result=native(originals+samples)
 base=baseline()
 result={'passed':True,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'source':counts,'generated_math_records':len(samples),'complete_bank_pair_checks_per_record':10,'family_coverage':coverage,'target_roles':sorted([list(x) for x in roles]),'sampled_meaningful_tasks':{k:len(v) for k,v in fps.items()},'default_family_coverage':sorted(defaults),'seed_option_order_identity_invariance_records':len(samples),'mutation_regressions':mutations,'native':{k:v for k,v in native_result.items() if k!='records'},'baseline_unchanged':True,'whole_bank_boundary_rejections':boundary_rejections,'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'limits':['One source has no original key/solution/difficulty; inferred completion separately labeled.','Native radio selections establish ID grading only; mathematical option semantics checked independently.','No blank fields or plots occur in originals.','Source worked stages match semantically and retain source prose; TeX and redundant multiplicative parentheses normalized.']}
 dump('validation.json',result)
 md=['# Original Math Academy sources and generated variants','Immutable basis '+str(g.SOURCE['basis'])+'; all original records retained in source.json.']
 for name,(sid,level,p) in g.SPECS.items():
  if sid:
   src=g.ORIGINALS[sid];md+=['## Original '+sid,src[':question/problem'],json.dumps(src.get(':question/answer-fields'),ensure_ascii=False,indent=2),src.get(':question/worked-solution','Original solution absent; not counted as matched.')]
  md += [g.markdown(x['record']) for x in review if x['record']['generation']['template']==name]
 (D/'review.md').write_text('\n\n'.join(md)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k in ('passed','source','generated_math_records','native')},indent=2))
if __name__=='__main__':main()
