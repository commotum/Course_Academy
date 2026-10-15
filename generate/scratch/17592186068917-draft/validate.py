"""Read actual displayed math independently; compare full raw banks/prose/keys.

Bounded domains are exhausted. No generator metadata is used to determine the
integrand, its argument, derivative, endpoint values, or displayed stage values.
"""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from functools import lru_cache
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'draft_g');p=g.printed;x=p.x;u=p.u;C=p.C

def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str)+'\n')
@lru_cache(None)
def eq(a,b):return g.exact_zero(a-b)

@lru_cache(None)
def canonical_primitive(f,v):
 # Derive from actual operator argument; source families have exactly one
 # trig argument. Constants and derivative ratios come from printed factors.
 atoms=[a for a in f.atoms(s.sin,s.cos,s.sec,s.csc,s.tan,s.cot)]
 assert atoms and len({a.args[0] for a in atoms})==1,('argument structure',f)
 z=atoms[0].args[0];w=s.Symbol('w',real=True);h=f.subs(z,w)
 for operator,H in [(s.sin(w),-s.cos(w)),(s.cos(w),s.sin(w)),(s.sec(w)**2,s.tan(w)),(s.csc(w)**2,-s.cot(w)),(s.sec(w)*s.tan(w),s.sec(w))]:
  ratio=s.cancel(f/(operator.subs(w,z)*s.diff(z,v)))
  if v not in ratio.free_symbols and w not in ratio.free_symbols:
   assert eq(s.diff(ratio*H.subs(w,z),v),f)
   return ratio*H.subs(w,z)
 raise AssertionError(('not substitution scope',f))

@lru_cache(None)
def mathval(text):
 text=text.strip().rstrip('.,').replace(r'\big','').replace(r'\,','').replace('{|}','|')
 text=text.replace(r'{\int }',r'\int').replace(r'\text{d}x','dx').replace(r'\text{d}u','du')
 text=text.replace(r'\intx',r'\int x').replace(r'\text{d}u','du')
 if r'\int' in text:
  idx=text.index(r'\int');prefix=text[:idx].strip() or '1';start=idx+4;lo=hi=None
  if text[start:start+1]=='_':
   a,start=p.group(text,start+1);assert text[start]=='^';b,start=p.group(text,start+1);lo=p.scalar(a);hi=p.scalar(b)
  match=re.search(r'd([xu])',text[start:]);assert match,('missing differential',text)
  end=start+match.start();var={'x':x,'u':u}[match[1]];arg=text[start:end];suffix=text[end+2:]
  # Source reciprocal substitution places (-du) inside the integrand factor.
  if arg.rstrip().endswith('(-') and suffix.startswith(')'):arg=arg.rstrip()[:-2]+'(-1)';suffix=suffix[1:]
  integrand=p.scalar(arg);F=canonical_primitive(integrand,var);out=F if lo is None else s.simplify(F.subs(var,hi)-F.subs(var,lo))
  if prefix!='1':out=(-1 if prefix=='-' else p.scalar(prefix))*out
  return out+(p.scalar(suffix) if suffix.strip() else 0)
 if '|' in text:
  idx=text.index('|');left=p.scalar(text[:idx]);rest=text[idx+1:];assert rest.startswith('_')
  a,j=p.group(rest,1);assert rest[j]=='^';b,j=p.group(rest,j+1);assert not rest[j:].strip()
  return s.simplify(left.subs(u,p.scalar(b))-left.subs(u,p.scalar(a)))
 return p.scalar(text)

def rows(solution):
 m=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert m
 body=m[1].replace(r'\begin{aligned}','');rr=re.split(r'\\\\\s*',body)
 return [rr[0].split('&')[0].strip()]+[r.split('=',1)[1].strip() for r in rr]

def endpoint_components(text):
 # Read two displayed endpoint components BEFORE collecting their difference.
 # A common error added at both endpoints must not disappear in aggregate QA.
 text=text.strip().replace(r'\left','').replace(r'\right','').replace(r'\,','')
 factor=s.Integer(1);body=text
 brace=0
 for i,c in enumerate(text):
  if c=='{':brace+=1
  elif c=='}':brace-=1
  elif c=='(' and brace==0:
   prefix=text[:i]
   try:scale=p.scalar(prefix or '1')
   except Exception:break
   if scale.free_symbols or scale.has(s.sin,s.cos,s.tan,s.cot,s.sec,s.csc):break
   inner,end=p.group(text,i)
   if end==len(text):factor=scale;body=inner
   break
 depth=0
 for i,c in enumerate(body):
  if c in '({':depth+=1
  elif c in ')}':depth-=1
  elif c=='-' and depth==0 and i>0:
   return factor*p.scalar(body[:i]),factor*p.scalar(body[i+1:])
 raise AssertionError(('no individual endpoint difference',text))

def validate_display(r):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 prompt=q[':question/problem'];f,lo,hi=p.integral(prompt);F=canonical_primitive(f,x)
 answer=F if lo is None else s.simplify(F.subs(x,hi)-F.subs(x,lo))
 fields=q[':question/answer-fields'];assert len(fields)==1
 field=fields[0];vals=[p.scalar(a[':answer/value']).subs(C,0) for a in field[':answer-field/choices']]
 for i,a in enumerate(vals):
  for b in vals[:i]:assert not eq(s.diff(a-b,x) if lo is None else a-b,0),('ambiguous',vals)
 correct=[i for i,a in enumerate(vals) if eq(s.diff(a-answer,x) if lo is None else a-answer,0)];assert len(correct)==1
 if ':answer-field/correct' in field:assert field[':answer-field/correct']==[':answer/id',field[':answer-field/choices'][correct[0]][':answer/id']]
 if ':question/worked-solution' not in q:return
 sol=q[':question/worked-solution'];rr=rows(sol);z=p.scalar(re.search(r'\$u=(.*?)\$',sol).group(1))
 # Independently evaluate *every* ordered stage from its displayed string.
 for index,cell in enumerate(rr):
  value=mathval(cell).subs(C,0).subs(u,z)
  assert eq(s.diff(value-answer,x) if lo is None else value-answer,0),('wrong actual stage',index,cell,value,answer)
 # Check derivative/differential block, initial substitution and table.
 z=p.scalar(re.search(r'\$u=(.*?)\$',sol).group(1));block=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)[0]
 deriv=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(.*?)(?:\\,⟹|\.)',block).group(1)
 assert eq(p.scalar(deriv),s.diff(z,x))
 if '⟹' in block:
  tail=block.split('⟹')[1].replace(r'\,','').rstrip('.')
  left,right=tail.split('=');coef=p.scalar(left.replace(r'\text{d}u','')+'1' if left.replace(r'\text{d}u','')=='-' else left.replace(r'\text{d}u','') or '1');out=p.scalar(right.replace(r'\text{d}x',''))
  assert eq(coef*s.diff(z,x),out)
 if lo is not None:
  cells={m[1]:(p.scalar(m[2]),p.scalar(m[3])) for m in re.finditer(r'\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol)}
  assert all(eq(a,b) for a,b in zip(cells['x'],(lo,hi)))
  assert all(eq(a,b) for a,b in zip(cells['u'],(z.subs(x,lo),z.subs(x,hi))))
 # Source-specific operation sequence: ratio integral cannot replace split or
 # substituted product rows, even though both would be algebraically equal.
 t=r['generation']['template'];assert r'\cdot' in rr[1],('missing explicit split product',t)
 if t in ('q-13474','q-13464','q-13533','q-13537','q-3038','q-13461','authored-easy'):
  assert r'\int' in rr[2] and r'\cdot' in rr[2],('missing substituted differential factor',t)
  assert r'\int' in rr[3] and r'\cdot' not in rr[3],('missing extracted coefficient stage',t)
 if lo is not None:
  assert '|' in rr[-4 if t=='q-13533' else -5 if t=='q-13537' else -4],('endpoint stage',t)
 if lo is not None:
  # The source cosine-zero family has only an evaluated delta row; all other
  # definite families display both evaluated primitive components distinctly.
  endpoint_index=5 if t in ('q-13533','q-13537') else 4
  expected_upper=F.subs(x,hi);expected_lower=F.subs(x,lo)
  for index in [endpoint_index]+([] if t=='q-13533' else [endpoint_index+1]):
   upper,lower=endpoint_components(rr[index])
   assert eq(upper,expected_upper) and eq(lower,expected_lower),('wrong individual endpoint',t,index,rr[index])
 for text in [prompt,sol]+[a[':answer/value'] for a in field[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
 if not r['generation']['evidence_only']:g.fmt.validate_generated_record(r)

def main():
 cases=[];replays=[];source_stats={'questions':0,'provided_solutions':0,'bank_values':0,'provided_correct_designations':0,'unrated_originals':0}
 for t,src in g.SOURCES.items():
  r=g.generate(g.LEVELS[t],template=t,parameters=g.defaults(t),profile='observed_raw');q=r['question'];sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in src),(t,'presence',key)
  assert q[':question/problem']==src[':question/problem'];assert q.get(':question/worked-solution')==src.get(':question/worked-solution')
  assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'];assert f[':answer-field/key']==sf[':answer-field/key']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  if ':answer-field/correct' in f:
   correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct[':answer/value']==sf[':answer-field/correct'][':answer/value']
  validate_display(r);source_stats['questions']+=1;source_stats['provided_solutions']+=int(':question/worked-solution'in src);source_stats['bank_values']+=len(sf[':answer-field/choices']);source_stats['provided_correct_designations']+=int(':answer-field/correct'in sf);source_stats['unrated_originals']+=int(':question/difficulty'not in src)
  cases.append(dict(source_id=t,template=t,parameters=g.defaults(t),bank_profile='observed_raw',profile='observed_raw',level=g.LEVELS[t],evidence_only=True,eligible_for_learning=False));replays.append(r)
 save('source-cases.json',cases);save('source-replay.json',replays)
 inventory={k:v for k,v in g.SOURCE.items() if k!='record'};inventory['questions']=[dict(record=q,role='independently authored inventory',relationship_to_source_templates='Amplitude variant of '+('q-13464 quadratic csc-squared' if 'csc' in q[':question/problem'] else 'q-13461 quadratic sine' if 'sin' in q[':question/problem'] else 'q-13474 cubic sec-squared')+' family; shortened generic solution and independently chosen bank. Excluded as evidence of original MA difficulty/templates.') for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q];save('independent-inventory.json',inventory)
 counts={};review=[];allrecs=[];rejections={};slots={};identities={}
 for t,level in g.LEVELS.items():
  counts[t]=0;rejections[t]=0;slots[t]=set()
  for params in g.domain(t):
   try:r=g.generate(level,template=t,parameters=params)
   except ValueError as e:
    assert str(e)=='whole-bank ambiguity',(t,params,e);rejections[t]+=1;continue
   validate_display(r);counts[t]+=1;slots[t].add((params['A'],params['k'],params.get('kind')));allrecs.append(r)
   fp=r['generation']['mathematical_fingerprint'];identities.setdefault(level,set()).add(fp)
   # Seed changes only order, never identity/key ownership.
   if counts[t] in (1,2):
    z=g.generate(level,seed=91,template=t,parameters=params)
    assert z['question'][':question/id']==r['question'][':question/id'];review.append(r)
  assert counts[t]>=2,(t,counts[t]);assert len(slots[t])==counts[t]
  print(t,counts[t],'valid;',rejections[t],'whole banks rejected',flush=True)
 raw_counts={}
 for t in g.SOURCES:
  raw_counts[t]=0
  for params in g.domain(t,True):
   z=g.generate(g.LEVELS[t],template=t,parameters=params,profile='observed_raw');validate_display(z);raw_counts[t]+=1
  print(t,raw_counts[t],'raw evidence parameter sets verified',flush=True)
 # Exercise all default-supported family samplers (family selected before params).
 default_seen={g.generate(level,seed)['generation']['template'] for level in g.SUPPORTED_LEVELS for seed in range(36)}
 assert default_seen==set(g.LEVELS)
 # Strict inputs and finite batch uniqueness/capacity.
 for level in g.SUPPORTED_LEVELS:
  b=g.batch(level,4,23);assert len({r['generation']['mathematical_fingerprint'] for r in b})==4
 for kwargs in [dict(level='hard',template='q-13464'),dict(level='easy',parameters={'A':2,'k':2,'kind':'cos'}),dict(level='moderate',template='q-13474',parameters={'A':3,'k':1}),dict(level='hard',template='q-3038',parameters={'A':1,'k':0}),dict(level='easy',parameters={'A':2,'k':1,'kind':'cos','unused':0}),dict(level='easy',field_type='blank')]:
  try:g.generate(**kwargs)
  except ValueError:pass
  else:raise AssertionError(('invalid public call accepted',kwargs))
 # Native JSON parameter types must be exact, excluding float and bool aliases.
 for params in [dict(A=1.0,k=1),dict(A=True,k=1),dict(A=1,k=1.0)]:
  try:g.generate('moderate',template='q-13461',parameters=params)
  except ValueError:pass
  else:raise AssertionError('noninteger parameter accepted')
 # Mutation regressions: remove a required operation while preserving equality,
 # alter signed endpoint component, and inject forbidden control bytes.
 r=next(r for r in review if r['generation']['template']=='q-13474');mut=copy.deepcopy(r);sol=mut['question'][':question/worked-solution'];rr=rows(sol);mut['question'][':question/worked-solution']=sol.replace(rr[2],rr[3],1)
 try:validate_display(mut)
 except AssertionError:pass
 else:raise AssertionError('stage mutation undetected')
 mut=copy.deepcopy(r);mut['question'][':question/problem']+='\x0c'
 try:validate_display(mut)
 except AssertionError:pass
 else:raise AssertionError('control mutation undetected')
 endpoint=copy.deepcopy(next(z for z in review if z['generation']['template']=='q-350203'));ss=endpoint['question'][':question/worked-solution'];chain=rows(ss);endpoint['question'][':question/worked-solution']=ss.replace(chain[-2],chain[-2]+'+1',1)
 try:validate_display(endpoint)
 except AssertionError:pass
 else:raise AssertionError('endpoint mutation undetected')
 correlated=copy.deepcopy(next(z for z in review if z['generation']['template']=='q-350203'));ss=correlated['question'][':question/worked-solution'];chain=rows(ss);upper,lower=endpoint_components(chain[-2]);bad=g.tex(upper+1)+r'-\left('+g.tex(lower+1)+r'\right)';correlated['question'][':question/worked-solution']=ss.replace(chain[-2],bad,1)
 try:validate_display(correlated)
 except AssertionError:pass
 else:raise AssertionError('correlated endpoint errors undetected')
 save('validation-review.json',review);save('full-domain-records.json',allrecs)
 # Native grading: all owned radio IDs / scalar blanks. Radio mathtext,
 # malformed and foreign identifiers are separate checks, not semantic proof.
 native=[]
 for r in allrecs:
  field=r['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1];choices=field[':answer-field/choices'];checks=[]
  if field[':answer-field/type'].endswith('/radio'):
   checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==correct else 'rejected',purpose='owned-ID selection') for a in choices]
   checks.extend([dict(submitted='ffffffff-ffff-4fff-8fff-ffffffffffff',expected='unresolved',purpose='foreign UUID'),dict(submitted='not-an-answer',expected='unresolved',purpose='malformed radio submission'),dict(submitted=choices[0][':answer/value'],expected='unresolved',purpose='radio mathtext does not select an owned answer ID')])
  else:
   a=choices[0][':answer/value'];v=p.scalar(a).subs(C,0)
   checks=[dict(submitted=a,expected='accepted',purpose='canonical blank'),dict(submitted=tex_equiv(v,lo=('C' not in a)),expected='accepted',purpose='independently unreduced equivalent blank'),dict(submitted=g.tex(v+1)+('+C' if 'C'in a else ''),expected='rejected',purpose='wrong blank')]
  native.append(dict(label=r['question'][':question/id'],record=r,checks=checks))
 # Faithful exact-answer wording has a known form restriction. Raw answers
 # are integers here: canonical spelling passes; unreduced equivalent fails.
 for r in replays:
  field=r['question'][':question/answer-fields'][0]
  if field[':answer-field/type'].endswith('/blank'):
   a=field[':answer-field/choices'][0][':answer/value'];native.append(dict(label='raw-'+r['generation']['template'],record=r,checks=[dict(submitted=a,expected='accepted',purpose='observed canonical blank'),dict(submitted=r'\frac{'+str(2*int(a))+'}{2}',expected='rejected',purpose='observed round wording form restriction')]))
 save('native-input.json',native)
 command=[str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')];subprocess.run(command,check=True)
 baseline=json.loads((HERE/'registered-baseline.json').read_text());now=[Path('generate/scratch/17592186068917.py')]+sorted(Path('generate/scratch/17592186068917').rglob('*'));actual={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in now if p.is_file()};assert actual==baseline,'registered package changed'
 result=dict(status='passed',source_fidelity=source_stats,independent_inventory_records=len(inventory['questions']),full_bounded_domain_valid=counts,full_raw_bounded_domain_valid=raw_counts,whole_bank_rejections=rejections,unique_mathematical_tasks={k:len(v) for k,v in identities.items()},default_family_coverage=sorted(default_seen),registered_baseline_files=len(baseline),registered_byte_path_parity=True,dependencies={'python':sys.version.split()[0],'sympy':s.__version__},limitations=['Observed historical scalar banks carry no proven error interpretation; all observed_raw profiles are evidence_only/ineligible.','q-13461 omits difficulty, solution and correct ref in faithful raw replay; normal moderate completion is authored.','Do not round the answer. in two original blank prompts rejects equivalent unreduced forms; faithful raw wording retained and normal wording says Give an exact answer.','Easy band is authored from immediate nonlinear-product tutorial, not an observed MA practice rating.','No plots are present or generated.'])
 save('validation.json',result);print(json.dumps(result,indent=2))
def tex_equiv(v,lo=True):
 # Deliberately preserve an unsimplified factor-two quotient in the string.
 return r'\frac{2\left('+g.tex(v)+r'\right)}{2}'+('' if lo else '+C')
if __name__=='__main__':main()
