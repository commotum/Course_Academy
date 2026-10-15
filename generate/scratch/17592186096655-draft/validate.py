#!/usr/bin/env python3
"""Independent read-back of displayed prompts, substitutions and every formal row.
Raw evidence mathematics defects are separately measured, never learning passes.
"""
import sys,hashlib,importlib.util,itertools,json,re,subprocess,copy
from pathlib import Path
from functools import lru_cache
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('natural',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=g.s;x=g.x;u=s.Symbol('u');C=s.Symbol('C')
def save(n,v):(P/n).write_text(json.dumps(v,indent=2)+'\n')
@lru_cache(maxsize=65536)
def eq(a,b):return s.cancel(s.expand_power_exp(a-b))==0

def scalar(z):return g.parser.scalar(z.replace('z','x'))
@lru_cache(maxsize=32768)
def integral_parts(text):
 text=text.replace(r'{\int }',r'\int');start=text.index(r'\int');tail=text[start+4:].lstrip();limits=None
 if tail.startswith('_'):
  lo,j=g.parser.group(tail,1);assert tail[j]=='^';hi,k=g.parser.group(tail,j+1);limits=(scalar(lo),scalar(hi));tail=tail[k:]
 m=re.search(r'\\(?:text|textrm)\{d\}([xuz])|d([xuz])',tail);assert m,tail
 body=tail[:m.start()].strip().removesuffix(r'\,');var=m[1]or m[2];suffix=tail[m.end():]
 missing=body.count('(')-body.count(')')
 if missing>0 and suffix.startswith(')'*missing):body+=')'*missing;suffix=suffix[missing:]
 return text[:start],scalar(body),limits,var,suffix
@lru_cache(maxsize=32768)
def expression(text):
 text=text.strip().rstrip('.,').replace(r'\,','').replace('{|}','|')
 if r'\int'in text:
  prefix,f,limits,var,suffix=integral_parts(text);v=u if var=='u'else x
  rate=s.cancel(s.diff(f,v)/f)
  assert rate!=0 and rate.free_symbols.isdisjoint({v}),('nonlinear/unsubstituted integral operand',text)
  F=f/rate;value=F if limits is None else F.subs(v,limits[1])-F.subs(v,limits[0])
  return scalar(prefix+'('+g.tex(value)+')'+suffix)
 if '|'in text:
  body,ends=text.rsplit('|',1);assert ends.startswith('_');lo,j=g.parser.group(ends,1);assert ends[j]=='^';hi,k=g.parser.group(ends,j+1);assert k==len(ends);value=scalar(body);return value.subs(u,scalar(hi))-value.subs(u,scalar(lo))
 return scalar(text)

def rows_of(solution):
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert blocks
 block=blocks[-1].replace(r'\begin{aligned}','')
 return [z.split('=',1)for z in block.split(chr(92)*2)]
def signature(rows):
 # Preserve extraction/substitution, primitive operator and endpoint operations.
 out=[]
 for _,rhs in rows:
  if r'\int'in rhs:
   pre,body,lim,var,_=integral_parts(rhs);out.append(['integral',var,'coefficient_outside'if pre.strip()else'coefficient_inside','u_operand'if u in body.free_symbols else'independent_operand','log_limit'if lim and any(z.has(s.log)for z in lim)else'ordinary_limit'])
  elif '|'in rhs:out.append(['primitive_operator'])
  elif 'C'in rhs:out.append(['primitive_u'if 'u'in rhs else'primitive_original'])
  elif re.search(r'\^\{',rhs):out.append(['endpoint_exponent'])
  else:out.append(['arithmetic'])
 return out

def format_audit(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 for text in[q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value']for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in'\n\t'for c in text),'control character'
  assert text.count('$')%2==0
  depth=0
  for c in text:
   if c=='{':depth+=1
   elif c=='}':depth-=1
   assert depth>=0
  assert depth==0
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}'in q[':question/problem']

def audit(r,raw_math=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}and r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];meta=r['generation'];t=meta['template'];raw=meta['evidence_only'];f=q[':question/answer-fields'][0]
 assert meta['eligible_for_learning']==(not raw)
 format_audit(r)
 if not raw:g.fmt.validate_generated_record(r)
 _,actual,limits,var,_=integral_parts(q[':question/problem'])
 if t in g.CA:formula,expected,wantlimits,wantvar,z=g.source_math(t,meta['parameters']['shift']);formula=formula.subs(wantvar,x);expected=expected.subs(wantvar,x);z=z.subs(wantvar,x)
 else:formula,expected,wantlimits,z=g.authored_math(meta['parameters'])
 assert eq(actual,formula),'printed prompt integrand';assert limits==wantlimits,'printed supplied bounds'
 assert var==('z'if t=='q-51160'else'x')
 assert meta['math_fingerprint']==g.task_fingerprint(actual,limits),'task identity from actual printed math'
 vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']]
 def same(a,b):return eq(a,b)if limits else eq(s.diff(a-b,x),0)
 correct=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if same(v,expected)]
 assert len(correct)==1
 for i,a in enumerate(vals):
  for b in vals[:i]:assert not same(a,b),'ambiguous whole bank'
 if ':answer-field/correct'in f:assert f[':answer-field/correct']==[':answer/id',correct[0]]
 else:assert raw and t=='q-13733'
 if not limits:assert same(expected+C+1,expected+C),'arbitrary integration constant shift'
 kind=f[':answer-field/type'].split('/')[-1];assert len(vals)==(5 if kind=='radio'else 1)
 cv=next((a[':answer/value']for a in f[':answer-field/choices']if ':answer-field/correct'in f and a[':answer/id']==f[':answer-field/correct'][1]),None)
 presence={'difficulty':':question/difficulty'in q,'solution':':question/worked-solution'in q,'correct':':answer-field/correct'in f};level=q[':question/difficulty'].split('/')[-1]if presence['difficulty']else None
 content=g.digest([g.VERSION,q[':question/problem'],q.get(':question/worked-solution'),kind,sorted(a[':answer/value']for a in f[':answer-field/choices']),presence,level,cv]);assert content==meta['content_hash']and q[':question/id']==g.uid(content)
 if raw and not raw_math:return
 sol=q.get(':question/worked-solution')
 if sol is None:assert raw and t=='q-13733';return
 sub=re.search(r'If we let \$u=(.*?)\$',sol);assert sub
 printedz=scalar(sub[1].rstrip(', '));assert eq(printedz,z),'u operand from printed prompt'
 formal=re.search(r'If we let.*?\$\$\s*(.*?)\s*\$\$',sol,re.S)[1]
 formal=formal.replace(r'\frac{\text{d}u}{\text{d}'+var+'}','D')
 first,relation=re.split(r'\\quad\\Longrightarrow\\quad|\\,⟹\\,',formal);a,b=first.split('=');assert a.strip()=='D';assert eq(scalar(b),s.diff(z,x))
 relation=relation.strip().rstrip('.').replace(r'\text{d}u','('+g.tex(s.diff(z,x))+')').replace(r'\text{d}'+var,'1');a,b=relation.split('=');assert eq(scalar(a),scalar(b)),'formal differential relation'
 if limits:
  table=re.search(r'\| \$'+var+r'\$ \| \$(.*?)\$ \| \$(.*?)\$ \|.*?\| \$u\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.S);assert table
  L,H,lo,hi=map(scalar,table.groups());assert(L,H)==limits;assert eq(lo,z.subs(x,L))and eq(hi,z.subs(x,H))
 rows=rows_of(sol)
 firstleft=rows[0][0].replace('&','').strip();_,leftf,leftlimits,leftvar,_=integral_parts(firstleft)
 assert eq(leftf,actual)and leftlimits==limits,'initial formal integral operand'
 if t in g.CA and not(t=='q-13733'and not raw):
  # Compare normal anchor and changed-coordinate structures against the same
  # family-specific operative recipe, including repaired intermediate operands.
  ref=g.source_render(t,0,normal=not raw)[1]
  assert signature(rows)==signature(rows_of(ref)),'ordered operative source stages'
 else:
  if limits:
   sig=signature(rows)
   assert [rr[0]for rr in sig[:4]]==['integral','integral','integral','primitive_operator'],'ordered authored formal stages'
   assert [rr[1]for rr in sig[:3]]==['x','u','u'],'ordered authored independent/substituted integral operands'
   assert len(rows)==7 and '('in rows[1][1]and r'\cdot'in rows[1][1],'substituted differential factor retained'
  else:assert [rr[0]for rr in signature(rows)]==['integral','integral','primitive_u','primitive_original'],'ordered authored indefinite stages'
 if limits:
  opindex=next(i for i,row in enumerate(rows)if '|'in row[1]);endpointrow=rows[opindex+1][1]
  exponents=[]
  for match in re.finditer(r'(?:\{e\}|e)\^',endpointrow):
   argument,end=g.parser.group(endpointrow,match.end());exponents.append(scalar(argument))
  assert len(exponents)==2,'individual upper/lower endpoint exponent components'
  assert eq(exponents[0],z.subs(x,limits[1]))and eq(exponents[1],z.subs(x,limits[0])),'individual upper/lower endpoint exponents'
 for i,(_,rhs)in enumerate(rows):
  if '|'in rhs:
   primitive=scalar(rhs.replace('{|}','|').split('|',1)[0])
   inverse=s.solve(z-u,x)[0]
   assert eq(s.diff(primitive,u),actual.subs(x,inverse)/s.diff(z,x)),'displayed primitive derivative'
   independent_primitive=actual/s.diff(z,x)
   for endpoint in limits:
    assert eq(primitive.subs(u,z.subs(x,endpoint)),independent_primitive.subs(x,endpoint)),'individually scaled upper/lower primitive component'
  value=expression(rhs).subs(u,z);assert same(value,expected),(t,'displayed formal row',i,rhs,value,expected)
 assert same(expression(rows[-1][1]).subs(u,z),expected)
 if t=='q-51160':
  # Independently check product preprocessing before the substitution stage.
  pre=re.search(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)[1].rstrip('.')
  aa,bb=pre.split('=');assert same(expression(aa),expression(bb))
 if t=='affine'and limits:
  # Each signed primitive endpoint must individually agree, not only difference.
  components=re.fullmatch(r'\s*\((.*?)\)-\((.*?)\)\s*',rows[-2][1]);assert components
  k=s.Rational(meta['parameters']['kn'],meta['parameters']['kd']);primitive=actual/k
  assert eq(scalar(components[1]),primitive.subs(x,limits[1]))
  assert eq(scalar(components[2]),primitive.subs(x,limits[0]))

def fidelity():
 choices=keys=0;defects=[]
 for c in g.CASES:
  source=g.QS[c['template']];r=g.generate(c['level'],template=c['template'],parameters={'shift':0},profile='observed_raw');q=r['question'];sf=source[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  for key in(':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert(key in source)==(key in q),'attribute-presence parity'
  assert q[':question/problem']==source[':question/problem'];assert q.get(':question/worked-solution')==source.get(':question/worked-solution')
  assert sf[':answer-field/key']==f[':answer-field/key']and sf[':answer-field/type'][':db/ident']==f[':answer-field/type']
  assert(':answer-field/correct'in sf)==(':answer-field/correct'in f)
  assert sorted(a[':answer/value']for a in sf[':answer-field/choices'])==sorted(a[':answer/value']for a in f[':answer-field/choices']);choices+=len(sf[':answer-field/choices'])
  if ':answer-field/correct'in sf:
   keys+=1;assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  audit(r)
  try:audit(r,True)
  except(AssertionError,ValueError)as exc:defects.append({'source_id':c['template'],'first_detected_failure':str(exc)})
 inv=json.loads((P/'independent-inventory.json').read_text());assert all(inv[k]==g.SOURCE[k]for k in('database','basis','lineage'));assert[rr['record']for rr in inv['questions']]==[q for q in g.KP[':knowledge-point/questions']if ':question/math-academy-id'not in q]
 assert {z['source_id']for z in defects}=={'q-13775','q-30922','q-51160'},defects
 return {'original_ma_questions':len(g.CASES),'exact_prompts':len(g.CASES),'exact_worked_solution_bytes_and_presence':len(g.CASES),'complete_banks':len(g.CASES),'displayed_values':choices,'existing_correct_designations':keys,'missing_correct_solution_difficulty':1,'independent_inventory':len(inv['questions']),'raw_worked_solution_defects':defects,'spurious_tex_repairs':0}

def domain():
 counts={};seen={level:set()for level in g.SUPPORTED_LEVELS};families=set()
 for c in g.CASES:
  for shift in range(-4,5):
   for profile in('observed_raw','method'):
    r=g.generate(c['level'],template=c['template'],parameters={'shift':shift},profile=profile);audit(r);key=c['template']+'/'+profile;counts[key]=counts.get(key,0)+1
 print('all source coordinate/profile domains passed',flush=True)
 # Full bounded Cartesian domain is rendered and independently read below.
 for level in g.SUPPORTED_LEVELS:
  for seed in range(100):
   r=g.generate(level,seed,template='affine');audit(r);seen[level].add(r['generation']['math_fingerprint']);counts['affine/'+level]=counts.get('affine/'+level,0)+1
  for seed in range(180):families.add((level,g.generate(level,seed)['generation']['template']))
  print('authored rendered domain samples passed',level,flush=True)
 expected={(c['level'],c['template'])for c in g.CASES}|{(l,'affine')for l in g.SUPPORTED_LEVELS};assert expected<=families
 # Exhaustive reduced same-method integer/reciprocal-slope coefficient domain.
 finite={};rejections={}
 for level in g.SUPPORTED_LEVELS:
  fs=set();eligible=0;bankrejected=0
  for a,kn,kd,b in itertools.product([z for z in range(-6,7)if z],[-4,-3,-2,-1,1,2,3,4],range(1,5),range(-3,4)):
   pairs=[None]if level=='easy'else[(L,H)for L in range(-2,2)for H in range(L+1,3)]
   for pair in pairs:
    p=dict(a=a,kn=kn,kd=kd,b=b)
    if pair:p.update(L=pair[0],H=pair[1])
    try:g.authored_bounds(level,p)
    except ValueError:continue
    if level=='easy'and abs(s.Rational(kn,kd))==1:bankrejected+=1;continue
    # These five complete bank functions can coincide only at unit slope or
    # the opposite-exponent function z=0 identically (excluded nonzero slope).
    r=g.generate(level,template='affine',parameters=p);audit(r);eligible+=1;fs.add(r['generation']['math_fingerprint'])
  finite[level]={'eligible_parameter_records':eligible,'unique_mathematical_tasks':len(fs)};rejections[level]=bankrejected;print('complete rendered finite domain passed',level,eligible,flush=True)
 return {'rendered_instances':sum(counts.values())+sum(v['eligible_parameter_records']for v in finite.values()),'source_and_sampler_instances':sum(counts.values()),'full_finite_domain_rendered_instances':sum(v['eligible_parameter_records']for v in finite.values()),'by_family_profile':counts,'finite_domain':finite,'whole_bank_degenerate_rejections':rejections,'default_family_coverage':sorted([list(v)for v in families])}

def api():
 rejected=0
 for bad in(True,1.,'1',None):
  try:g.generate('easy',seed=bad)
  except ValueError:rejected+=1
  else:raise AssertionError('strict seed')
 for bad in(True,1.,'1'):
  try:g.generate('easy',template='q-13732',parameters={'shift':bad})
  except ValueError:rejected+=1
  else:raise AssertionError('strict source slot')
 for p,l in[(dict(a=1,kn=True,kd=1,b=0),'easy'),(dict(a=1,kn=1,kd=1,b=0),'easy'),(dict(a=2,kn=2,kd=1,b=1,L=1,H=2),'moderate'),(dict(a=2,kn=2,kd=1,b=1,L=0,H=2),'hard')]:
  try:g.generate(l,template='affine',parameters=p)
  except ValueError:rejected+=1
  else:raise AssertionError('explicit workload rejected')
 p=dict(a=-3,kn=-2,kd=1,b=3,L=-2,H=-1);r=g.generate('hard',template='affine',parameters=p);audit(r);r2=g.generate('hard',seed=19,template='affine',parameters=p);assert r['question'][':question/id']==r2['question'][':question/id']
 # Coefficient-spelling aliases represent one mathematical task.
 f1=s.exp(x/2);f2=s.exp(2*x/4);assert g.task_fingerprint(f1,None)==g.task_fingerprint(f2,None)
 # Detect changed upper/lower components independently and deleted operations.
 for mutate in('control','endpoint','stage','u'):
  rr=copy.deepcopy(r);sol=rr['question'][':question/worked-solution'];rows=rows_of(sol)
  if mutate=='control':sol=sol.replace('If we let','If\x0cwe let')
  elif mutate=='endpoint':sol=sol.replace(rows[-2][1],rows[-2][1].replace(')-(',')+('))
  elif mutate=='stage':sol=sol.replace(rows[2][1],rows[-1][1])
  else:sol=sol.replace('If we let $u=','If we let $u=1+')
  f=rr['question'][':question/answer-fields'][0];values=[a[':answer/value']for a in f[':answer-field/choices']]
  try:
   rr=g.record('hard',0,'affine','method',p,rr['question'][':question/problem'],sol,values,0,'blank');audit(rr)
  except(AssertionError,ValueError):rejected+=1
  else:raise AssertionError('mutation escaped '+mutate)
 return {'invalid_inputs_and_mutations_rejected':rejected,'arbitrary_constant_shift_is_valid':True,'seed_and_option_order_identity':True,'coefficient_alias_task_identity':True}

def review():
 rows=[];md=['# Private natural exponential integral review','Raw original and translated-coordinate replay is evidence only. Normal source families include documented repairs and method-derived complete banks.']
 for c in g.CASES:
  for label,shift,profile in[('original raw',0,'observed_raw'),('changed raw',2,'observed_raw'),('normal at anchor',0,'method'),('changed normal',2,'method')]:
   r=g.generate(c['level'],template=c['template'],parameters={'shift':shift},profile=profile);rows.append({'label':c['template']+' '+label,'record':r});md+=['## '+c['template']+' '+label,g.markdown(r)]
 for level in g.SUPPORTED_LEVELS:
  for r in g.batch(level,2,500,template='affine'):
   rows.append({'label':level+' authored affine','record':r});md+=['## '+level+' authored affine',g.markdown(r)]
 r=g.generate('moderate',template='affine',parameters=dict(a=3,kn=1,kd=1,b=0,L=0,H=1));rows.append({'label':'explicit Euler coefficient semantics','record':r});md+=['## Explicit Euler coefficient semantics',g.markdown(r)]
 save('review.json',rows);(P/'review.md').write_text('\n\n'.join(md)+'\n');return rows

def native(rows):
 inputs=[]
 for i,item in enumerate(rows):
  r=item['record'];q=r['question'];f=q[':question/answer-fields'][0]
  if ':answer-field/correct'not in f:continue
  aid=f[':answer-field/correct'][1];correct=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==aid)
  if f[':answer-field/type'].endswith('/radio'):
   checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted'if a[':answer/id']==aid else'rejected',purpose='field-owned radio ID; mathematics separate')for a in f[':answer-field/choices']]
   checks +=[dict(submitted=v,expected='unresolved',purpose=purpose)for v,purpose in[(correct,'math text is not a radio ID'),('999999','foreign field ID'),('malformed','malformed ID')]]
  else:
   _,fexpr,limits,var,_=integral_parts(q[':question/problem']);rate=s.cancel(s.diff(fexpr,x)/fexpr);primitive=fexpr/rate
   hi=g.tex(primitive.subs(x,limits[1]));lo=g.tex(primitive.subs(x,limits[0]));equiv='('+hi+')-('+lo+')'
   # A genuinely uncollected endpoint form independent of stored final answer.
   if equiv==correct:equiv='('+g.tex(fexpr.subs(x,limits[1]))+'-('+g.tex(fexpr.subs(x,limits[0]))+'))/('+g.tex(rate)+')'
   checks=[dict(submitted=correct,expected='accepted',purpose='canonical blank'),dict(submitted=equiv,expected='accepted',purpose='independently uncollected endpoint equivalent')]+[dict(submitted=v,expected='rejected',purpose='ordinary mathematically wrong scalar')for v in['0','1','('+correct+')+1']]
   if item['label']=='explicit Euler coefficient semantics':checks.append(dict(submitted='0.003',expected='rejected',purpose='wrong scientific interpretation of unseparated 3e-3'))
   if 'round'in q[':question/problem'].lower():checks[1].update(expected='rejected',purpose='valid endpoint equivalent: captured round/form restriction known limitation')
  inputs.append({'label':item['label']+' '+str(i),'record':r,'checks':checks})
 save('native-input.json',inputs);proc=subprocess.run([str(P/'check-engine'),str(P/'native-input.json'),str(P/'native-report.json')],capture_output=True,text=True)
 if proc.returncode:raise AssertionError(proc.stderr)
 report=json.loads((P/'native-report.json').read_text());save('native-summary.json',{**report,'classification':{'radio_errors':'nonidentity submissions separated from mathematics','raw_equivalent_form_restriction':'preserved source round wording restricts correct equivalents; raw is ineligible','normal_equivalent_failures':'reported per native case; no engine changes'}})
 return{k:report[k]for k in('accepted_checks','rejected_checks','documented_unresolved_checks')}

def baseline():
 old=json.loads((P/'registered-baseline.json').read_text());paths=[Path('generate/scratch/17592186096655.py'),*sorted(Path('generate/scratch/17592186096655').rglob('*'))];now=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size=p.stat().st_size)for p in paths if p.is_file()];assert now==old,'registered full tree changed';return len(now)
if __name__=='__main__':
 report={'status':'running','source_fidelity':fidelity()};save('validation.json',report);report['api']=api();print('source fidelity and API passed',flush=True);report['domain']=domain();save('validation.json',report);rows=review();report['native']=native(rows);report['registered_baseline_unchanged_files']=baseline();report['dependencies']={'python':sys.version.split()[0],'sympy':s.__version__};report['status']='passed_with_documented_raw_source_limitations';save('validation.json',report);print(json.dumps(report,indent=2))
