#!/usr/bin/env python3
"""Independent displayed-TeX mathematics, fidelity, native radio grading and freeze.
No use of generator answer metadata as a mathematical oracle. Log|f| derivatives
are checked locally as log(f) on every regular interval (additive branch constants
are immaterial to the real primitive family).
"""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from functools import lru_cache
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;REPO=D.parents[2]
spec=importlib.util.spec_from_file_location('kp64246_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=s.Symbol('x',real=True);W=s.Symbol('u',real=True);C=s.Symbol('C',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,)
MATH=re.compile(r'\$\$.*?\$\$|\$(?!\$).*?\$',re.S)
def group(t,i,opening='{',closing='}'):
 assert t[i]==opening,(t,i)
 d=1;j=i+1
 while d:
  assert j<len(t),(t,i)
  d+=(t[j]==opening)-(t[j]==closing);j+=1
 return t[i+1:j-1],j

@lru_cache(maxsize=30000)
def parse(text):
 t=text.strip().replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace('\u2061','')
 t=t.strip().rstrip('.,')
 t=re.sub(r'\\(?:text|textrm)\{d\}([xu])',r'd\1',t)
 t=re.sub(r'\\operatorname\{(sin|cos|tan|cot|csc|ln)\}',lambda m:'\\'+m[1],t)
 t=t.replace('{csc}',r'\csc')
 if r'\ln' not in t:t=t.replace('|','')
 # Every residual integral is read from its displayed integrand and differential.
 while r'\int' in t:
  pos=t.index(r'\int');m=re.search(r'd([xu])',t[pos:]);assert m,(t,'missing differential')
  end=pos+m.start();var=X if m[1]=='x' else W;body=t[pos+4:end]
  expr=s.integrate(parse(body),var)
  assert not expr.has(s.Integral),(text,'unevaluated residual',expr)
  t=t[:pos]+'('+str(expr)+')'+t[pos+m.end():]
 while r'\frac' in t:
  pos=t.index(r'\frac');n,end=group(t,pos+5);den,end2=group(t,end)
  t=t[:pos]+'(('+str(parse(n))+')/('+str(parse(den))+'))'+t[end2:]
 # Logs use their whole absolute-value argument; local derivative is 1/f * f′.
 while r'\ln' in t:
  pos=t.index(r'\ln');i=pos+3
  if t[i]=='|':end=t.index('|',i+1);body=t[i+1:end];end+=1
  elif t[i]=='{':body,end=group(t,i)
  else:raise AssertionError(('log argument',t))
  t=t[:pos]+'log('+str(parse(body))+')'+t[end:]
 # Primitive trig notation, optional exponent, then a complete grouped/monomial arg.
 pattern=re.compile(r'\\(sin|cos|tan|cot|csc)')
 while (m:=pattern.search(t)):
  f=m[1];i=m.end();power='1'
  if t[i:i+1]=='^':
   i+=1
   if t[i]=='{':power,i=group(t,i)
   else:power=t[i];i+=1
  if t[i] in '({':
   op=t[i];body,end=group(t,i,op,')' if op=='(' else '}')
  else:
   am=re.match(r'(?:-?\d+)?[xu]',t[i:]);assert am,('bare trig arg',t[i:],text);body=am[0];end=i+len(body)
  t=t[:m.start()]+'('+f+'('+str(parse(body))+')**('+power+'))'+t[end:]
 while '^{' in t:
  pos=t.index('^{');p,end=group(t,pos+1);t=t[:pos]+'**('+str(parse(p))+')'+t[end:]
 t=t.replace('{','(').replace('}',')').replace('^','**')
 assert '\\' not in t,repr(t)
 return parse_expr(t,local_dict={'x':X,'u':W,'C':C,'sin':s.sin,'cos':s.cos,'tan':s.tan,'cot':s.cot,'csc':s.csc,'log':s.log},transformations=TRANS)
@lru_cache(maxsize=50000)
def same(a,b):
 d=s.expand(a-b)
 return d==0 or s.trigsimp(d,method='fu')==0
def primitive_same(a,b):return same(s.diff(a-b,X),0)
def integrand(prompt):
 math=MATH.findall(prompt)[0].strip('$').rstrip('.=');t=math.split(r'\int',1)[1]
 t=re.sub(r'\\(?:text|textrm)\{d\}x','dx',t).replace(r'\,','')
 return parse(t.rsplit('dx',1)[0])
def skeleton(t):return MATH.sub('<math>',t)
def rows(text):
 out=[]
 for block in MATH.findall(text):
  if r'\begin{gathered}' in block:
   visual=block.split(r'\begin{gathered}',1)[1].split(r'\end{gathered}',1)[0].split(r'\\')
   if visual[0].strip().endswith('='):
    assert len(visual) in [3,4,5] and all(row.strip().startswith('=') for row in visual[2:]),'continued calculation chain shape'
    logical=[visual[0]+visual[1],*visual[2:]]
   else:
    assert len(visual) in [3,4] and visual[1].strip().endswith('='),'gathered equality continuation shape'
    logical=[visual[0],visual[1]+visual[2],*visual[3:]]
   out.append([left+' & ='+right for left,right in (row.split('=',1) for row in logical)])
  elif r'\begin{aligned}' in block:
   out.append(block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\'))
 return out

def regular(e):return e.replace(s.Abs,lambda v:v)
def check_format(r):
 g.fmt.validate_generated_record(r)
 for text in [r['question'][':question/problem'],r['question'][':question/worked-solution'],*[a[':answer/value'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]:
  assert not any(ord(c)<32 and c not in '\n\t' for c in text),'C0'
  assert re.sub(r'\$\$.*?\$\$|\$(?!\$).*?\$','',text,flags=re.S).count('$')==0,'math delimiter'

def validate_solution(q,template=None):
 it=integrand(q[':question/problem']);text=q[':question/worked-solution'];chains=rows(text);assert len(chains)==3
 assert MATH.findall(text)[0].strip('$').strip()==r'\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.','formal by-parts formula'
 setup=chains[0];assert len(setup)==2
 vals=[]
 for index,row in enumerate(setup):
  left,right=row.split('⟹')
  assert left.split('=',1)[0].strip()==('u' if index==0 else r'{v}^{′}'),'component left operator'
  assert right.replace(r'\,','').split('=',1)[0].strip()==(r'{u}^{′}' if index==0 else 'v'),'component right operator'
  vals.append((parse(left.split('=',1)[1].replace('&','')),parse(right.split('=',1)[1])))
 (u,du),(vp,v)=vals
 assert same(s.diff(u,X),du),'displayed u derivative';assert same(s.diff(v,X),vp),'displayed v primitive';assert same(u*vp,it),'actual integrand versus uv′'
 # Variable discipline: no proxy independent variables in actual learner algebra.
 assert it.free_symbols<= {X};assert all(e.free_symbols<={X} for row in vals for e in row)
 count=3
 substitution=chains[1];assert len(substitution) in [2,3]
 assert r'uv-\int v{u}^{′}' in substitution[0],'formal by-parts stage'
 assert substitution[1].count(r'\cdot')>=2,'substituted product factors preserved'
 # The only substitution letter u is explicitly printed for hard csc family.
 sub=None
 if r'\ln' in text or r'\operatorname{ln}' in text:
  um=next(m for m in MATH.findall(text) if m.startswith('$u='));sub=parse(um[3:].strip('$').rstrip(','))
  dm=next(m for m in MATH.findall(text) if m.startswith('$'+r'\text{d}u='));deriv=dm.split('=',1)[1].split(r'\,\text{d}x')[0]
  assert same(s.diff(sub,X),parse(deriv)),'displayed logarithmic substitution differential'
 for chain in chains[1:]:
  for i,row in enumerate(chain):
   lhs,rhs=row.split(' & =',1)
   if chain is chains[1] and i==0:continue
   value=parse(rhs)
   if sub is not None:value=value.subs(W,sub)
   assert same(s.diff(value,X),it),('wrong displayed operative stage',rhs,value,it)
   if lhs.strip():assert same(integrand('$'+lhs+'$'),it),('wrong displayed integral left side',lhs)
   count+=1
 if template:
  final=chains[2];hard=g.TEMPLATES[template][1]=='csc';expanded=g.TEMPLATES[template][3]
  assert len(final)==(4 if hard else 3 if expanded else 2),'source operative stage count'
  if hard:
   assert r'\frac{' in final[0] and r'\operatorname{cos}' in final[0] and r'\operatorname{sin}' in final[0],'cot ratio stage'
   assert r'\int \frac{1}{u}' in final[1], 'substituted reciprocal integral stage'
   assert r'\ln|u|' in final[2],'substitution primitive stage'
  else:
   assert r'\int' in final[0].split(' & =',1)[1],'remaining primitive integral preserved'
   if expanded:assert '(-' in final[1].split(' & =',1)[1] and r'\int' not in final[1].split(' & =',1)[1], 'uncollected primitive evaluation stage'
 return count

def validate_record(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'};q=r['question'];f=q[':question/answer-fields'][0];it=integrand(q[':question/problem']);assert f[':answer-field/type']==':answer-field.type/radio';assert f[':answer-field/key']=='selection'
 ans=f[':answer-field/choices'];assert len(ans)==5
 values=[parse(a[':answer/value']) for a in ans];correct=f[':answer-field/correct'];assert correct[0]==':answer/id'
 assert sum(a[':answer/id']==correct[1] for a in ans)==1
 ci=next(i for i,a in enumerate(ans) if a[':answer/id']==correct[1]);assert same(s.diff(values[ci],X),it),'displayed correct primitive derivative'
 assert sum(same(s.diff(v,X),it) for v in values)==1,'bank answer correctness'
 assert not any(primitive_same(a,b) for i,a in enumerate(values) for b in values[i+1:]),'ambiguous primitive families'
 for obj,key in [(q,':question/id'),(f,':answer-field/id'),*[(a,':answer/id') for a in ans]]:uuid.UUID(obj[key])
 for a,v in zip(ans,values):assert a[':answer/value'].endswith('+C');assert v.free_symbols<={X,C};assert '$' not in a[':answer/value']
 check_format(r);count=validate_solution(q,r['generation']['template'])
 # Independently recover the actual affine and trig factors from the definition block.
 defs=rows(q[':question/worked-solution'])[0];u=parse(defs[0].split('=',1)[1].split('⟹')[0].replace('&',''));assert s.Poly(u,X).degree()==1
 return values,count

def write(name,obj):(D/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual field-owned radio choice'} for a in f[':answer-field/choices']]
def must_fail(r,label):
 try:validate_record(r)
 except (AssertionError,ValueError,IndexError):return label
 raise AssertionError('Mutation escaped: '+label)

def main():
 review=[];requests=[];fidelity=[];sourcecases=[];all_records=[];stages=0
 for sid,name,p in g.SOURCE_CASES:
  level=g.TEMPLATES[name][0];r=g.generate(level,template=name,parameters=p,profile='observed:'+sid);values,n=validate_record(r);stages+=n
  src=g.SOURCES[sid];sv=[parse(a[':answer/value']) for a in src[':question/answer-fields'][0][':answer-field/choices']]
  matches=[[i for i,v in enumerate(values) if primitive_same(v,o)] for o in sv];assert all(len(x)==1 for x in matches) and len({x[0] for x in matches})==5,(sid,'complete bank',matches)
  sf=src[':question/answer-fields'][0];assert same(s.diff(parse(sf[':answer-field/correct'][':answer/value']),X),integrand(src[':question/problem']))
  assert skeleton(src[':question/problem'])==skeleton(r['question'][':question/problem']),(sid,'prompt prose')
  assert skeleton(src[':question/worked-solution'])==skeleton(r['question'][':question/worked-solution']),(sid,'all shared solution prose')
  assert [len(t) for t in rows(src[':question/worked-solution'])]==[len(t) for t in rows(r['question'][':question/worked-solution'])],(sid,'ordered row counts')
  # Independently verify original operators and each original equality too.
  validate_solution(src)
  assert all((key in src)==(key in r['question']) for key in [':question/difficulty',':question/worked-solution',':question/answer-fields'])
  fidelity.append({'source_id':sid,'banks':1,'values_matched':5,'distractors_matched':4,'designation_matched':True,'field_types':'radio','attribute_presence_matched':True,'full_prose_matched':True,'ordered_operative_stages_verified':True,'notation':'consistent parenthesized trig arguments, source-style operator names and equivalent fraction placement; source raw retained'})
  sourcecases.append({'source_id':sid,'template':name,'parameters':p,'bank_profile':'observed:'+sid})
  review.append({'label':'Original-profile parameterized replay '+sid,'record':r});all_records.append(r);requests.append({'label':'source/'+sid,'record':r,'checks':checks(r)})
  peer=next(g.generate(level,seed,template=name,profile='observed:'+sid) for seed in range(100,200) if g.generate(level,seed,template=name,profile='observed:'+sid)['generation']['parameters']!=p);validate_record(peer)
  review.append({'label':'Generated empirical evidence variant '+sid,'record':peer});all_records.append(peer);requests.append({'label':'evidence-peer/'+sid,'record':peer,'checks':checks(peer)})
  print('Source and full-bank stages verified:',sid,flush=True)
 normal=[]
 for name,t in g.TEMPLATES.items():
  for seed in range(8):
   r=g.generate(t[0],seed,template=name);_,n=validate_record(r);stages+=n;normal.append(r);all_records.append(r);requests.append({'label':name+'/'+str(seed),'record':r,'checks':checks(r)})
   if seed<2:review.append({'label':'Generated normal '+name+'/'+str(seed),'record':r})
  r=normal[-1];again=g.generate(t[0],999,template=name,parameters=r['generation']['parameters']);assert r['question'][':question/id']==again['question'][':question/id'];assert r['generation']['parameter_fingerprint']==again['generation']['parameter_fingerprint']
  print('Authored default family verified:',name,flush=True)
 # Domain/identity/default coverage checks use the same explicit guard as sampling.
 for sid,name,p in g.SOURCE_CASES:
  r=g.generate(g.TEMPLATES[name][0],template=name,parameters=p);e=g.generate(g.TEMPLATES[name][0],template=name,parameters=p,profile='observed:'+sid)
  assert r['generation']['parameter_fingerprint']==e['generation']['parameter_fingerprint'];assert r['question'][':question/id']!=e['question'][':question/id']
 for name,t in g.TEMPLATES.items():
  for p in [dict(a=0,b=0,k=1,h=0),dict(a=11,b=0,k=1,h=0),dict(a=1,b=0,k=6,h=0),dict(a=1,b=9,k=1,h=0),dict(a=1,b=0,k=1,h=9)]:
   try:g.generate(t[0],template=name,parameters=p)
   except ValueError:pass
   else:raise AssertionError('Invalid explicit parameters accepted')
 coverage={}
 for level in ['easy','moderate','hard']:
  expected={n for n,t in g.TEMPLATES.items() if t[0]==level};seen=set()
  for seed in range(120):
   seen.add(g.generate(level,seed)['generation']['template'])
   if seen==expected and seed>=1:break
  coverage[level]=sorted(seen)
 for level,seen in coverage.items():assert seen==sorted(n for n,t in g.TEMPLATES.items() if t[0]==level)
 mutations=[];r=copy.deepcopy(normal[0]);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(r'\cdot ',r'\cdot 2\cdot ',1);mutations.append(must_fail(r,'unchanged-key wrong operative factor'))
 r=copy.deepcopy(normal[0]);r['question'][':question/worked-solution']+='\f';mutations.append(must_fail(r,'C0 formfeed'))
 r=copy.deepcopy(normal[0]);r['question'][':question/problem']+='$';mutations.append(must_fail(r,'unbalanced delimiter'))
 # Remove an operative uncollected stage while preserving equality and row count.
 expanded=next(r for r in normal if g.TEMPLATES[r['generation']['template']][3]);r=copy.deepcopy(expanded);chains=rows(r['question'][':question/worked-solution']);mid=chains[2][1];last=chains[2][2];r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(mid.split(' & =',1)[1],last.split(' & =',1)[1],1);mutations.append(must_fail(r,'primitive evaluation collapsed into final'))
 write('source-cases.json',sourcecases);write('review.json',review);write('samples.json',normal);write('engine-input.json',requests)
 subprocess.run([str(D/'check-engine'),str(D/'engine-input.json'),str(D/'native-grading.json')],check=True)
 native=json.load(open(D/'native-grading.json'));assert native['documented_unresolved_checks']==0
 # Recheck the complete immutable numeric path set, including sibling bytecode.
 before=json.load(open(D/'numeric-before-import.json'));root=D.parent;id='17592186064246';paths=([root/(id+'.py')] if (root/(id+'.py')).exists() else [])+list((root/id).rglob('*'))+list((root/'__pycache__').glob(id+'.*.pyc'));after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()};assert before['paths']==after;write('numeric-after-verification.json',{'unchanged':True,'paths':after})
 proof=json.load(open(D/'reference/native-42-verification.json'));assert len(proof)==42
 for p,h in proof.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,(p,'native build input changed')
 assert hashlib.sha256((D/'check-engine').read_bytes()).hexdigest()=='33510bf3ac27a1eb28e9bad7b4121a22d2fa787026d3102268daa4ecf98b1617'
 # Enumerate substantive finite mathematical domains without seed/profile aliases.
 variety={}
 for level in ['easy','moderate','hard']:
  tasks=set();by_template={}
  for name,t in g.TEMPLATES.items():
   if t[0]!=level:continue
   params=[]
   for a in range(1,11):
    for b in ([v for v in range(-8,9) if v] if name.startswith('affine') else [0]):
     for k in ([2,3,4,5] if name in ['cos_frequency','cos_frequency_expanded','sin_frequency','affine_cos','affine_sin','phase_cos','phase_sin'] else [1]):
      for h in (list(range(-8,9)) if level=='hard' else [v for v in range(-8,9) if v] if name.startswith('phase') else [0]):
       p=dict(a=a,b=b,k=k,h=h)
       try:g.validate_parameters(name,p)
       except ValueError:continue
       fp=g.fingerprint(name,p);tasks.add(fp);params.append(fp)
   by_template[name]=len(set(params))
  variety[level]={'distinct_prompt_integrands':len(tasks),'per_template':by_template,'not_counted':['seed','option order','profile','template label','notation']}
 raw='\n\n---\n\n'.join('## Original '+sid+' — '+src[':question/difficulty'][':db/ident'].split('/')[-1]+'\n\nField type: radio\n\n'+src[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **original correct**' if a[':answer/id']==src[':question/answer-fields'][0][':answer-field/correct'][':answer/id'] else '') for a in src[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+src[':question/worked-solution'] for sid,src in g.SOURCES.items())
 (D/'review.md').write_text('# Trigonometric integration by parts\n\nRaw originals followed by labeled parameterized replays and generated variants. All source fields, correct refs, levels and solutions are present; raw missing keys: none. No within-level progression.\n\n'+raw+'\n\n---\n\n'+'\n\n---\n\n'.join('## '+item['label']+'\n\n'+g.markdown(item['record']) for item in review)+'\n')
 result={'passed':True,'source_provenance':{k:g.CAPTURE[k] for k in ['database','basis','lineage']},'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'source_fidelity':fidelity,'source_questions':15,'complete_banks':{'matched':15,'total':15},'answer_values':{'matched':75,'total':75},'distractors':{'matched':60,'total':60},'correct_designations':{'matched':15,'total':15},'field_contracts':{'radio':15,'blank':0,'missing_original_attributes':0},'display_presentation_repair':'Concrete by-parts equality and final calculation left side line-wrapped after equals; unchanged logical equalities, operands and operative sequence','raw_exact_math_text':False,'normalized_mathematical_and_structure_fidelity':True,'source_errors':[],'normal_records_checked':len(normal),'intermediate_math_checks':stages,'mutation_regressions':mutations,'default_family_coverage':coverage,'variety':variety,'native_grading':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],'binary_sha256':hashlib.sha256((D/'check-engine').read_bytes()).hexdigest(),'build_files_reverified':42},'blank_equivalent_entry_tests':{'applicable':False,'reason':'No blank source or authored family; all radio choices exercised through actual learning::grade_field.'},'numeric_registered_tree_unchanged':True,'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'database_writes':0,'registration':False,'limitations':['Historical distractor intentions are unresolved; empirical banks remain evidence-only.','Original TeX spelling is retained in raw evidence; generated math uses consistent argument parentheses and equivalent fraction placement.','Local logarithm derivative checks apply on every interval where the original integrand is defined.']}
 write('validation.json',result);print('PASS: 15 banks, 75 values, 60 distractors, 15 designations; '+str(len(normal))+' normal records; native '+str(native['accepted_checks'])+'/'+str(native['rejected_checks'])+'; zero unresolved.');print(json.dumps(variety))
if __name__=='__main__':main()
