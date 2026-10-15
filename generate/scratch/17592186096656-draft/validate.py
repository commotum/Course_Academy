#!/usr/bin/env python3
"""Read actual displayed operands independently; no live generator dependencies."""
import sys,hashlib,importlib.util,itertools,json,re,subprocess,copy
from pathlib import Path
from functools import lru_cache
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=g.s;x=g.x;u=s.Symbol('u');C=s.Symbol('C')
def save(name,value):(P/name).write_text(json.dumps(value,indent=2)+'\n')
@lru_cache(maxsize=65536)
def eq(a,b):
 d=s.cancel(s.expand_log(s.expand_power_exp(a-b),force=True))
 return d==0 or s.simplify(d)==0

@lru_cache(maxsize=32768)
def integral_parts(text):
 text=text.replace(r'{\int }',r'\int');start=text.index(r'\int');tail=text[start+4:].lstrip();limits=None
 if tail.startswith('_'):
  low,j=g.parser.group(tail,1);assert tail[j]=='^';high,k=g.parser.group(tail,j+1);limits=(g.parser.scalar(low),g.parser.scalar(high));tail=tail[k:]
 match=re.search(r'\\(?:text|textrm)\{d\}([xu])|d([xu])',tail)
 assert match,tail
 body=tail[:match.start()].strip().removesuffix(r'\,');var=match[1]or match[2]
 return text[:start],g.parser.scalar(body),limits,(x if var=='x'else u),tail[match.end():]

@lru_cache(maxsize=32768)
def expression(text):
 text=text.strip().rstrip('.,').replace(r'\,','').replace('{|}','|')
 if r'\int'in text:
  prefix,f,limits,var,suffix=integral_parts(text)
  # Independent integration of each actual printed RHS integral.
  primitive=s.integrate(f,var)
  value=primitive if limits is None else primitive.subs(var,limits[1])-primitive.subs(var,limits[0])
  return g.parser.scalar(prefix+'('+g.tex(value)+')'+suffix)
 if '|'in text:
  main,ends=text.rsplit('|',1);assert ends.startswith('_');lo,j=g.parser.group(ends,1);assert ends[j]=='^';hi,k=g.parser.group(ends,j+1);assert k==len(ends)
  value=g.parser.scalar(main);return value.subs(u,g.parser.scalar(hi))-value.subs(u,g.parser.scalar(lo))
 return g.parser.scalar(text)

def rows_of(solution):
 match=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert match
 return [row.split('=',1)for row in match[1].split(chr(92)*2)]
def stage_signature(rows):
 return ['integral'if r'\int'in rhs else'evaluated_primitive'if'|'in rhs else'powers'if re.search(r'\^\{',rhs)else'collected'for _,rhs in rows]

def audit(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];meta=r['generation'];t=meta['template'];raw=meta['evidence_only'];f=q[':question/answer-fields'][0]
 if not raw:g.fmt.validate_generated_record(r)
 for z in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value']for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in'\n\t'for c in z),'control character'
  assert z.count('$')%2==0,'math delimiter parity'
  depth=0
  for c in z:
   if c=='{':depth+=1
   elif c=='}':depth-=1
   assert depth>=0
  assert depth==0
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}'in q[':question/problem']
 _,actual,limits,var,_=integral_parts(q[':question/problem']);assert var==x
 p=meta['parameters'];formula,expected=g.exact_math(p);assert eq(actual,formula),'printed prompt'
 assert limits==(s.Integer(p['L']),s.Integer(p['H']))if'L'in p else limits is None
 vals=[g.parser.scalar(v[':answer/value'])for v in f[':answer-field/choices']]
 def same(a,b):return eq(a,b)if limits is not None else eq(s.diff(a-b,x),0)
 correct=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if same(v,expected)]
 assert len(correct)==1,'mathematically unique bank key'
 for i,a in enumerate(vals):
  for b in vals[:i]:assert not same(a,b),'equivalent wrong options'
 if ':answer-field/correct'in f:assert f[':answer-field/correct']==[':answer/id',correct[0]]
 else:assert raw and t in('q-31405','q-31418')
 # Independently derive the complete presentation identity from actual public fields.
 kind=f[':answer-field/type'].split('/')[-1];values=[a[':answer/value']for a in f[':answer-field/choices']]
 assert len(values)==(5 if kind=='radio'else 1)
 has_correct=':answer-field/correct'in f
 cv=next((a[':answer/value']for a in f[':answer-field/choices']if has_correct and a[':answer/id']==f[':answer-field/correct'][1]),None)
 presence={'difficulty':':question/difficulty'in q,'solution':':question/worked-solution'in q,'correct':has_correct}
 level=q[':question/difficulty'].split('/')[-1]if presence['difficulty']else None
 content=g.digest([g.VERSION,q[':question/problem'],q.get(':question/worked-solution'),kind,sorted(values),presence,level,cv])
 assert content==meta['content_hash']and q[':question/id']==g.uid(content),'content identity'
 assert f[':answer-field/id']==g.uid(q[':question/id']+'/field')
 for answer in f[':answer-field/choices']:assert answer[':answer/id']==g.uid(f[':answer-field/id']+'/'+answer[':answer/value'])
 rate=s.cancel(s.expand_log(s.simplify(s.diff(actual,x)/actual),force=True));amp=s.cancel(actual.subs(x,0))
 fp=g.digest([s.srepr(rate),s.srepr(amp),[int(v)for v in limits]if limits is not None else None,'real'])
 assert fp==meta['math_fingerprint'],'actual printed mathematical identity'
 # Arbitrary-constant shifts are valid indefinite antiderivative families.
 if limits is None:assert same(expected+C+7,expected+C)
 sol=q.get(':question/worked-solution')
 if sol is None:assert raw and t in('q-31405','q-31418');return
 zmatch=re.search(r'If we let \$u=(.*?)\$',sol);assert zmatch
 z=g.parser.scalar(zmatch[1].rstrip(', '));assert eq(z,s.Rational(p['k'])*x+p['b'])
 assert eq(s.diff(z,x),s.Rational(p['k']))
 formal=re.search(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)[1]
 # Verify the actual first derivative operand and differential relation.
 formal=formal.replace(r'\frac{\text{d}u}{\text{d}x}','D')
 first,relation=re.split(r'\\quad\\Longrightarrow\\quad|\\,⟹\\,',formal)
 left,right=first.split('=',1);assert left=='D';assert eq(g.parser.scalar(right),s.diff(z,x))
 relation=relation.strip().rstrip('.')
 relation=relation.replace(r'\text{d}u','('+g.tex(s.diff(z,x))+')').replace(r'\text{d}x','1')
 aa,bb=relation.split('=',1);assert eq(g.parser.scalar(aa),g.parser.scalar(bb))
 if limits is not None:
  table=re.search(r'\| \$x\$ \| \$(.*?)\$ \| \$(.*?)\$ \|.*?\| \$u\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.S);assert table
  L,H,lo,hi=map(g.parser.scalar,table.groups());assert (L,H)==limits;assert eq(lo,z.subs(x,L));assert eq(hi,z.subs(x,H))
 rows=rows_of(sol);sig=stage_signature(rows)
 if t in g.CA and not(t in('q-31405','q-31418')and not raw):
  source_rows=rows_of(g.MASKS[t]['solution']);assert sig==stage_signature(source_rows),'ordered operative source stages'
 elif limits is None:assert sig==['integral','integral','powers','powers']
 else:assert sig==['integral','integral','evaluated_primitive','powers','collected','collected'],'ordered authored operative stages'
 firstleft=rows[0][0].replace('&','').strip();_,left_f,leftlim,leftvar,_=integral_parts(firstleft);assert eq(left_f,actual)and leftlim==limits
 for i,(_,rhs)in enumerate(rows):
  value=expression(rhs.strip());value=value.subs(u,z)
  assert same(value,expected),(t,p,i,rhs,value,expected)
 # Actual final expression also agrees with the independently read prompt.
 assert same(expression(rows[-1][1]).subs(u,z),expected)

def fidelity():
 total_choices=total_keys=0
 for c in g.CASES:
  source=next(q for q in g.KP[':knowledge-point/questions']if q.get(':question/math-academy-id')==c['source_id']);q=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='observed_raw')['question'];f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
  assert source[':question/problem']==q[':question/problem']
  for key in(':question/difficulty',':question/worked-solution'):
   assert(key in source)==(key in q)
  assert source.get(':question/worked-solution')==q.get(':question/worked-solution')
  assert [sf[':answer-field/key'],sf[':answer-field/type'][':db/ident']]==[f[':answer-field/key'],f[':answer-field/type']]
  assert(':answer-field/correct'in sf)==(':answer-field/correct'in f)
  assert sorted(v[':answer/value']for v in sf[':answer-field/choices'])==sorted(v[':answer/value']for v in f[':answer-field/choices'])
  total_choices+=len(sf[':answer-field/choices'])
  if ':answer-field/correct'in sf:
   selected=next(v for v in f[':answer-field/choices']if v[':answer/id']==f[':answer-field/correct'][1]);assert selected[':answer/value']==sf[':answer-field/correct'][':answer/value'];total_keys+=1
  audit(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='observed_raw'))
 inv=json.loads((P/'independent-inventory.json').read_text());assert all(inv[k]==g.SOURCE[k]for k in('database','basis','lineage'))
 assert [r['record']for r in inv['questions']]==[q for q in g.KP[':knowledge-point/questions']if ':question/math-academy-id'not in q]
 return {'original_ma_questions':11,'exact_prompt':11,'exact_worked_solution_presence_and_bytes':11,'complete_banks':11,'displayed_values':total_choices,'existing_correct_designations':total_keys,'raw_incomplete':2,'independent_inventory':len(inv['questions'])}

def domain(full=True):
 counts={};rejects={};defaultfamilies=set();seen={l:set()for l in g.SUPPORTED_LEVELS};samples=[]
 for c in g.CASES:
  for n in range(2,10):
   for profile in('observed_raw','method'):
    key=c['template']+'/'+profile
    try:r=g.generate(c['level'],template=c['template'],parameters={'n':n},profile=profile)
    except ValueError as exc:
     assert '4096'in str(exc),str(exc);rejects[key]=rejects.get(key,0)+1;continue
    audit(r);counts[key]=counts.get(key,0)+1
 print('all source base domains passed',flush=True)
 for level in g.SUPPORTED_LEVELS:
  space=itertools.product(range(2,7),(-3,-2,-1,1,2,3),range(-3,4),[1]if level=='easy'else range(1,4),[(None,None)]if level=='easy'else[(0,1),(0,2),(0,3),(1,2),(1,3)])
  for n,k,b,a,(L,H)in space:
   p=dict(n=n,k=k,b=b,a=a)
   if L is not None:p.update(L=L,H=H)
   try:g.authored_bounds(level,p)
   except ValueError:continue
   r=g.generate(level,template='affine',parameters=p);audit(r);counts['affine/'+level]=counts.get('affine/'+level,0)+1;seen[level].add(r['generation']['math_fingerprint'])
  print('full authored domain passed:',level,counts.get('affine/'+level),flush=True)
  for seed in range(120):defaultfamilies.add((level,g.generate(level,seed)['generation']['template']))
 for c in g.CASES:assert(c['level'],c['template'])in defaultfamilies
 for l in g.SUPPORTED_LEVELS:assert(l,'affine')in defaultfamilies
 return {'audited_instances':sum(counts.values()),'by_family_profile':counts,'whole_instance_arithmetic_rejections':rejects,'authored_unique_math_tasks':{l:len(v)for l,v in seen.items()},'default_family_coverage':sorted([list(v)for v in defaultfamilies])}

def api_regressions():
 rejected=0
 for bad in(True,1.0,'1',None):
  try:g.generate('easy',seed=bad)
  except ValueError:rejected+=1
  else:raise AssertionError('noninteger seed accepted')
 for level,p in [('easy',dict(n=True,k=2,b=1,a=1)),('easy',dict(n=3,k=1,b=1,a=1)),('moderate',dict(n=3,k=2,b=1,a=2,L=0,H=1)),('hard',dict(n=3,k=2,b=0,a=2,L=0,H=1)),('hard',dict(n=3,k=2,b=1,a=1,L=0,H=1))]:
  try:g.generate(level,template='affine',parameters=p)
  except ValueError:rejected+=1
  else:raise AssertionError('invalid explicit workload accepted')
 r=g.generate('hard',seed=1,template='affine',parameters=dict(n=3,k=-2,b=3,a=2,L=0,H=1));r2=g.generate('hard',seed=100,template='affine',parameters=dict(n=3,k=-2,b=3,a=2,L=0,H=1));assert r['question'][':question/id']==r2['question'][':question/id']
 assert sorted(a[':answer/id']for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id']for a in r2['question'][':question/answer-fields'][0][':answer-field/choices'])
 mutated=copy.deepcopy(r);mutated['question'][':question/worked-solution']=mutated['question'][':question/worked-solution'].replace('If we let','If\x0cwe let')
 try:audit(mutated)
 except AssertionError:rejected+=1
 else:raise AssertionError('control mutation escaped')
 # Same row count and equal mathematics cannot hide a missing extracted-integral stage.
 mutated=copy.deepcopy(r);sol=mutated['question'][':question/worked-solution'];rows=rows_of(sol);old=rows[1][0]+'='+rows[1][1];replacement=' & ='+rows[-1][1];mutated['question'][':question/worked-solution']=sol.replace(old,replacement)
 # Rebuild identities from mutated displayed content so this regression proves
 # the stage checker itself, rather than merely detecting a stale digest.
 mf=mutated['question'][':question/answer-fields'][0]
 mutated=g.record('hard',1,'affine','method',mutated['generation']['parameters'],mutated['question'][':question/problem'],mutated['question'][':question/worked-solution'],[a[':answer/value']for a in mf[':answer-field/choices']],0,'blank')
 try:audit(mutated)
 except AssertionError as exc:
  assert str(exc)=='ordered authored operative stages',str(exc)
  rejected+=1
 else:raise AssertionError('operative-stage deletion escaped')
 # Prime-base and reciprocal-slope aliases are one assessed mathematical task.
 alias_a=g.generate('moderate',template='affine',parameters=dict(n=4,k=1,b=1,a=1,L=0,H=1))
 alias_b=g.generate('moderate',template='affine',parameters=dict(n=2,k=2,b=2,a=1,L=0,H=1))
 assert alias_a['generation']['math_fingerprint']==alias_b['generation']['math_fingerprint']
 assert alias_a['question'][':question/id']!=alias_b['question'][':question/id']
 assert g.task_fingerprint(8**(x/3),None)==g.task_fingerprint(2**x,None)
 assert g.task_fingerprint(4**(-x/2),None)==g.task_fingerprint(2**(-x),None)
 try:g.batch('easy',9,template='q-31417')
 except ValueError:rejected+=1
 else:raise AssertionError('finite capacity overflow accepted')
 out={}
 for level in g.SUPPORTED_LEVELS:
  rs=g.batch(level,30,918);assert len({r['generation']['math_fingerprint']for r in rs})==30;out[level]=len(rs)
 return {'invalid_or_mutated_cases_rejected':rejected,'deduplicated_batch_counts':out,'prime_base_and_reciprocal_slope_alias_regressions':3}

def review_records():
 rows=[];md=['# Private general-base integral review','Raw originals are evidence. Method variants and hard scope are authored, not recovered difficulty evidence.']
 for c in g.CASES:
  t=c['template'];n=c['parameters']['n'];original=g.generate(c['level'],template=t,parameters={'n':n},profile='observed_raw')
  changed=next(g.generate(c['level'],template=t,parameters={'n':v},profile='observed_raw')for v in range(2,10)if v!=n and _source_valid(t,v))
  normal=g.generate(c['level'],template=t,parameters={'n':n},profile='method')
  changed_normal=g.generate(c['level'],template=t,parameters={'n':changed['generation']['parameters']['n']},profile='method')
  for label,r in [('original raw',original),('changed-base raw',changed),('authored method bank at anchor',normal),('changed-base authored method bank',changed_normal)]:
   rows.append({'label':t+' '+label,'record':r});md+=['## '+t+' '+label,g.markdown(r)]
 for l in g.SUPPORTED_LEVELS:
  for r in g.batch(l,2,500,template='affine'):
   rows.append({'label':l+' expanded authored example','record':r});md+=['## '+l+' expanded authored example',g.markdown(r)]
 save('review.json',rows);(P/'review.md').write_text('\n\n'.join(md)+'\n');return rows

def _source_valid(t,n):
 try:g.params_for_source(t,{'n':n});return True
 except ValueError:return False


def native(rows):
 inputs=[];measurements=[]
 for i,item in enumerate(rows):
  r=item['record'];q=r['question'];f=q[':question/answer-fields'][0]
  if ':answer-field/correct'not in f:continue
  aid=f[':answer-field/correct'][1];correct=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==aid);checks=[]
  if f[':answer-field/type'].endswith('/radio'):
   checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted'if a[':answer/id']==aid else'rejected',purpose='field-owned radio identity; math audited separately')for a in f[':answer-field/choices']]
   checks +=[dict(submitted=correct,expected='unresolved',purpose='radio rejects mathematical text as nonidentity'),dict(submitted='999999',expected='unresolved',purpose='radio rejects foreign field ID'),dict(submitted='malformed',expected='unresolved',purpose='radio rejects malformed identity')]
  else:
   p=r['generation']['parameters'];n=p['n'];k=s.Rational(p['k']);a=p['a'];lo=k*p['L']+p['b'];hi=k*p['H']+p['b'];equiv='('+str(a)+')*('+str(n)+'^('+str(hi)+')-'+str(n)+'^('+str(lo)+'))/(('+str(k)+')*ln('+str(n)+'))';val=g.parser.scalar(correct)
   checks=[dict(submitted=correct,expected='accepted',purpose='canonical blank value'),dict(submitted=equiv,expected='accepted',purpose='uncollected independent endpoint equivalent')]+[dict(submitted=z,expected='rejected',purpose='ordinary mathematically incorrect scalar')for z in['0','1','('+correct+')+1']]
   if 'round'in q[':question/problem'].lower():checks[1]['expected']='rejected';checks[1]['purpose']='valid endpoint equivalent rejected by captured round/form restriction (known limitation)'
  inputs.append({'label':item['label']+' '+str(i),'record':r,'checks':checks})
 save('native-input.json',inputs)
 proc=subprocess.run([str(P/'check-engine'),str(P/'native-input.json'),str(P/'native-report.json')],capture_output=True,text=True)
 if proc.returncode:raise AssertionError(proc.stderr)
 report=json.loads((P/'native-report.json').read_text())
 # Known expected nonidentity errors are separate from mathematical blank limitations.
 report['classification']={'radio_nonidentity_errors':'Expected native errors for text, foreign IDs and malformed submissions; never mathematics passes','raw_blank_form_rejections':'Valid equivalents with the preserved round instruction are measured as rejected','normal_blank_equivalents':'All native requests above, independent endpoint forms, including wrong0/wrong1 checks'}
 save('native-summary.json',report);return {k:report[k]for k in('accepted_checks','rejected_checks','documented_unresolved_checks')}

def baseline():
 old=json.loads((P/'registered-baseline.json').read_text());paths=[Path('generate/scratch/17592186096656.py')]+sorted(Path('generate/scratch/17592186096656').rglob('*'));now=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size}for p in paths if p.is_file()];assert now==old,'registered baseline changed';return len(old)
if __name__=='__main__':
 report={'status':'running','source_fidelity':fidelity()};save('validation.json',report)
 report['api']=api_regressions();print('fidelity and API passed',flush=True)
 report['domain']=domain();print('entire bounded displayed domain passed',flush=True)
 rows=review_records();report['native']=native(rows);report['registered_baseline_unchanged_files']=baseline();report['dependencies']={'python':sys.version.split()[0],'sympy':s.__version__};report['status']='passed_with_documented_raw_source_limitations';save('validation.json',report);print(json.dumps(report,indent=2))
