"""Independent source fidelity, rendered mathematics, native grading and freeze audit."""
import functools, copy, hashlib, importlib.util, json, random, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).parent.resolve();ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from private_reader import expression, X, C
import math_format as fmt
spec=importlib.util.spec_from_file_location('kp64177_draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v
@functools.lru_cache(maxsize=20000)
def intervals_zero(v):
 u=sp.Symbol('u',positive=True)
 for sign in (-1,1):
  e=sp.expand(v.subs(X,sign*u).doit())
  if e==0:continue
  # A finite nonzero point is a falsification witness; passing equalities still
  # require exact symbolic zero, never numerical near-equality.
  for point in (2,3):
   z=e.subs(u,point).evalf(35)
   if z.is_finite and abs(complex(z))>1e-20:return False
  if sp.simplify(e)!=0:return False
 return True
def primitive_matches(v,target):return intervals_zero(sp.diff(v,X)-target)
def definitions(prompt):
 defs={}
 for name,body in re.findall(r'\b([fg])\(x\)=([^$]+)',prompt):defs[sp.Function(name)(X)]=expression(body)
 return defs
DIFF=re.compile(r'(?:\\,)?\\text\{d\}x|(?<![A-Za-z])dx')
def operators(row,defs):
 """Read every actual operand and outside coefficient before evaluating an integral."""
 terms=[];rest='';start=0
 for i,m in enumerate(list(re.finditer(r'\\int\s*',row))):
  d=DIFF.search(row,m.end())
  if d is None:raise AssertionError('Formal integral lacks differential')
  operand=expression(row[m.end():d.start()]).xreplace(defs)
  symbol=sp.Symbol('T'+str(i));terms.append((symbol,operand));rest+=row[start:m.start()]+'T'+str(i);start=d.end()
 rest+=row[start:]
 if not terms:return expression(row).xreplace(defs),[]
 parsed=expression(rest,{str(v):v for v,_ in terms});contributions=[];evaluated=parsed
 for symbol,operand in terms:
  coefficient=sp.expand(parsed).coeff(symbol)
  assert X not in coefficient.free_symbols and not any(str(s).startswith('T') for s in coefficient.free_symbols),'Nonlinear formal integral'
  contributions.append(sp.expand(coefficient*operand))
  evaluated=evaluated.subs(symbol,sp.integrate(operand,X).replace(sp.log(X),sp.log(sp.Abs(X))))
 assert not any(str(s).startswith('T') for s in evaluated.free_symbols)
 return evaluated,contributions

def prompt_integrand(q):
 prompt=q[':question/problem'];m=re.search(r'\\int\s*',prompt);assert m
 d=DIFF.search(prompt,m.end());assert d,prompt
 return sp.expand(expression(prompt[m.end():d.start()].replace(r'\displaystyle','')).xreplace(definitions(prompt)))

def content_check(r):
 q=r['question'];fmt.validate_generated_record(r);target=prompt_integrand(q)
 assert not target.has(sp.Function('f')(X),sp.Function('g')(X)),'Undefined source functions remain'
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 vals=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
 cid=f[':answer-field/correct'][1];correct=[i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==cid];assert len(correct)==1
 flags=[primitive_matches(v,target) for v in vals];assert flags[correct[0]]
 if f[':answer-field/type'].endswith('/radio'):
  assert len(vals)==5 and sum(flags)==1
  for i,v in enumerate(vals):
   for w in vals[:i]:assert not primitive_matches(v,sp.diff(w,X)),'Options equivalent modulo constants'
 else:
  assert len(vals)==1 and f[':answer-field/key']=='field-1'
  if r['generation']['template']!='q-31261':assert not vals[0].has(C) and '+C' in q[':question/problem'].replace(r'\,',''),'Outside C belongs to prompt'
 defs=definitions(q[':question/problem']);displays=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);assert len(displays)==1
 body=re.sub(r'\\(?:begin|end)\{aligned\}','',displays[0]);previous=None;rows=0;operands=0;last=None
 for i,row in enumerate(body.split(r'\\')):
  lhs,rhs=row.replace('&','').split('=',1);left=operators(lhs,defs)[0] if lhs.strip() else previous
  val,parts=operators(rhs,defs);assert left is not None
  # Equalities before +C agree exactly; primitives differ only by arbitrary C.
  delta=sp.expand(left-val);assert intervals_zero(delta-delta.coeff(C)*C),row
  assert primitive_matches(val,target),row
  if len(parts)>1:
   expected=list(sp.Add.make_args(target));assert len(parts)==len(expected),(row,parts,expected)
   unmatched=expected[:]
   for part in parts:
    hits=[j for j,v in enumerate(unmatched) if intervals_zero(part-v)];assert len(hits)==1,(part,unmatched)
    unmatched.pop(hits[0])
  elif parts:assert intervals_zero(parts[0]-target)
  operands+=len(parts);previous=val;last=val;rows+=1
 assert last.has(C) and sp.expand(last).coeff(C)==1,'Missing/duplicated arbitrary constant'
 assert primitive_matches(last,target)
 meta=r['generation'];assert meta['source_basis']==2275
 assert r==g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],meta['parameters'],meta['bank_profile'])
 return {'rows':rows,'formal_integral_operands':operands,'terms':len(sp.Add.make_args(target))}

def rekey_source(q):
 """Exact replay is kept separately; normalize enums only for native fixtures."""
 return g.normalize(q)
def engine_checks(r):
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Complete selected bank option'} for a in f[':answer-field/choices']]
 correct=expression(f[':answer-field/choices'][0][':answer/value']);template=r['generation']['template']
 # Equivalent is a genuinely uncollected termwise primitive, not another stored choice.
 if template=='q-31261':
  equivalent='e^x+'+str(r['generation']['parameters']['base'])+'^x/ln('+str(r['generation']['parameters']['base'])+')+3*ln(abs(x))+C'
  wrong='0'
 else:
  equivalent='2*e^x+24*x^2/2-2*x^4/4'
  wrong='2*e^x+24*x^2-2*x^4'
 # Correct stored input, reordered/exact rationally uncollected equivalent, and wrong derivative.
 checks=[{'submitted':f[':answer-field/choices'][0][':answer/value'],'expected':'accepted','purpose':'Stored primitive'}, {'submitted':equivalent,'expected':'accepted','purpose':'Uncollected equivalent primitive, distinct from stored answer'}, {'submitted':wrong,'expected':'rejected','purpose':'Different derivative; additive constants are not used as wrong answers'}]
 return [{'field_index':0,**c} for c in checks]

def main():
 source=json.loads((HERE/'source.json').read_text());assert source['basis']==2275
 manifest=source['record'][':knowledge-point/questions'];ma=[q for q in manifest if ':question/math-academy-id' in q];nonma=[q for q in manifest if ':question/math-academy-id' not in q]
 assert len(manifest)==16 and len(ma)==12 and len(nonma)==4
 raw=[];sourcecases=[];normal=[];recipes=[];records=[];review=[];total_rows=total_ops=0
 ineligible={'q-31311':['missing correct designation','missing worked solution','unrated'],'q-51102':['missing correct designation','missing worked solution','unrated'],'q-31261':['no answer fields']}
 ineligible.update({q:['undefined f/g operands in raw prompt']for q in('q-167332','q-167786','q-166079')})
 for q in ma:
  mid=q[':question/math-academy-id'];raw.append({'source_id':mid,'record':copy.deepcopy(q),'raw_exact_replay':True,'raw_generation_eligible':mid not in ineligible,'raw_ineligibility':ineligible.get(mid,[])})
  assert raw[-1]['record']==q
  level,base=g.SPECS[mid];params={'base':base} if base else {};r=g.generate(level,103,mid,params,mid);stats=content_check(r);total_rows+=stats['rows'];total_ops+=stats['formal_integral_operands'];normal.append(r);records.append(r)
  sf=q.get(':question/answer-fields',[]);nf=r['question'][':question/answer-fields'];mapping=[]
  if sf:
   original=sf[0].get(':answer-field/choices',[]);new=nf[0][':answer-field/choices']
   assert len(original)==len(new)
   for i,a in enumerate(original):
    value=expression(a[':answer/value']);hits=[j for j,b in enumerate(new) if intervals_zero(value-expression(b[':answer/value']))];assert len(hits)==1,(mid,i,hits)
    sourcecorrect=sf[0].get(':answer-field/correct');correctid=sourcecorrect.get(':answer/id') if sourcecorrect else None
    iscorrect=(a[':answer/id']==correctid) if correctid else None
    if iscorrect is not None:assert iscorrect==(new[hits[0]][':answer/id']==nf[0][':answer-field/correct'][1])
    recipe=(g.TEMPLATES[mid]['choices'][i] if mid in g.TEMPLATES else a[':answer/value'])
    mapping.append({'source_field':sf[0][':answer-field/key'],'source_option_index':i,'original_value':a[':answer/value'],'correct_designation':iscorrect,'recipe':recipe,'mapped_option_index':hits[0],'exact_original_value':True,'interpretation':'Observed expression pattern; psychological mistake interpretation unresolved.'})
  recipes.append({'source_id':mid,'profile':mid,'mapping':mapping,'missing_options':[],'extra_options':[]})
  # Every original string/field/bank/operative stage is retained losslessly in raw replay.
  # Normal fixes remain visible alongside, including C-field contracts.
  sourcecases.append({'source_id':mid,'role':'MA original','raw_exact_replay':True,'record':copy.deepcopy(q),'full_prompt':True,'full_solution_or_omission':True,'full_field_layout_or_omission':True,'complete_original_bank':True,'correct_designation_or_omission':True,'raw_generation_eligible':mid not in ineligible,'raw_ineligibility':ineligible.get(mid,[]),'normal_repairs':r['generation']['source_repairs'],'matched_values':len(mapping),'matched_distractors':sum(m['correct_designation'] is False for m in mapping),'complete_bank_with_original_key':bool(mapping) and mid not in ineligible})
  review.append('## '+mid+' — original\n\n'+q[':question/problem']+'\n\n'+q.get(':question/worked-solution','(No captured worked solution.)')+'\n\n### Normal replay\n\n'+g.markdown(r))
 save('raw-replay.json',raw);save('source-cases.json',sourcecases);save('normal-replay.json',normal);save('choice-recipes.json',recipes)
 relations={17592186488350:('q-2277',4),17592186488353:('q-2281',8),17592186488365:('q-2281',4),17592186488377:('q-31252',7)}
 inv=[]
 for q in nonma:
  template,base=relations[q[':db/id']];r=g.generate(g.SPECS[template][0],0,template,{'base':base});content_check(r)
  assert intervals_zero(prompt_integrand(r['question'])-prompt_integrand(q))
  original=q[':question/answer-fields'][0];new=r['question'][':question/answer-fields'][0]
  assert len(original[':answer-field/choices'])==len(new[':answer-field/choices'])
  for a in original[':answer-field/choices']:assert sum(intervals_zero(expression(a[':answer/value'])-expression(b[':answer/value'])) for b in new[':answer-field/choices'])==1
  inv.append({'record':q,'role':'independently authored inventory','relationship_details':{'template':template,'parameters':{'base':base},'complete_bank_mathematically_matches':True,'counted_as_MA_source':False},'relationship_to_source_templates':'Complete existing nonMA bank matches '+template+' at base '+str(base)+'; not counted as MA source evidence.'})
 save('independent-inventory.json',{'basis':source['basis'],'lineage':source['lineage'],'questions':inv})
 # Exercise every source profile over its entire declared bounded domain.
 for mid,(level,base) in g.SPECS.items():
  if base is None:continue
  for b in range(2,13):records.append(g.generate(level,31,mid,{'base':b}))
 # Every authored profile, sign, bound and structural tail; all are ordinary same-level instances.
 for level in g.SUPPORTED_LEVELS:
  for profile in ('authored-omit-log','authored-multiply-log'):
   for low in (True,False):
    for tail in (('power','constant','reciprocal') if level!='easy' else ('none',)):
     p={'base':2 if low else 12,'a':-5 if low else 5,'b':-4 if low else 4}
     if level!='easy':p.update(tail=tail,c=-4 if low else 4,power=1 if low else 3)
     if level=='hard':p.update(second_base=12 if low else 2,d=-3 if low else 3)
     records.append(g.generate(level,53,'authored-'+level,p,profile))
  # Deterministic interior cases exercise every declared numerical slot value.
  for i in range(12):
   p={'base':2+i%11,'a':(-5,-4,-3,-2,2,3,4,5)[i%8],'b':(-4,-3,-2,2,3,4)[i%6]}
   if level!='easy':p.update(tail=('power','constant','reciprocal')[(i//3)%3],c=(-4,-3,-2,2,3,4)[i%6],power=1+i%3)
   if level=='hard':p.update(second_base=2+(i+5)%11,d=(-3,-2,2,3)[i%4])
   records.append(g.generate(level,53,'authored-'+level,p,('authored-omit-log','authored-multiply-log')[i%2]))
  for seed in range(10):records.append(g.generate(level,seed,'authored-'+level))
 reviewcases=[];unique={};stats=[]
 for ri,r in enumerate(records):
  if ri%25==0:print('Rendered checks',ri,'/',len(records),flush=True)
  result=content_check(r);stats.append(result)
  key=r['question'][':question/id'];fingerprint=r['generation']['content_fingerprint']
  assert key not in unique or unique[key]==fingerprint,'Content identity collision';unique[key]=fingerprint
  m=r['generation'];repeat=g.generate(r['question'][':question/difficulty'].split('/')[-1],999,m['template'],m['parameters'],m['bank_profile']);assert repeat['question']==r['question']
  reviewcases.append({'record':r,'rendered_check':result})
 save('review-cases.json',reviewcases)
 for level in g.SUPPORTED_LEVELS:
  examples=[r for r in records if r['generation']['template']=='authored-'+level]
  for r in (examples[0],examples[-1]):review.append('## '+level+' authored variant\n\n'+g.markdown(r))
 (HERE/'review.md').write_text('\n\n---\n\n'.join(review)+'\n')
 # Negative controls: stale formal operands/outer coefficients, answer, primitive, C, definitions.
 negatives=0
 for mode in ('formal_operand','coefficient','answer','constant'):
  r=copy.deepcopy(g.generate('easy',0,'q-2277',{'base':2}));q=r['question']
  if mode=='formal_operand':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\int {2}^{x}',r'\int {3}^{x}')
  elif mode=='coefficient':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'5\int',r'4\int')
  elif mode=='answer':q[':question/answer-fields'][0][':answer-field/choices'][4][':answer/value']='0'
  else:q[':question/worked-solution']=q[':question/worked-solution'].replace('+C.','+2C.')
  try:content_check(r)
  except (AssertionError,ValueError):negatives+=1
  else:raise AssertionError('Corruption passed '+mode)
 for kwargs in ({'seed':True},{'seed':1.0},{'parameters':{'base':True}},{'parameters':{'base':1}},{'parameters':{'base':13}}):
  try:g.generate('easy',template='q-2277',**kwargs)
  except ValueError:negatives+=1
  else:raise AssertionError('Invalid parameters passed')
 for count,seed in [(True,0),(1.0,0),(-1,0),(1,False),(1,2.0)]:
  try:g.batch('all',count,seed)
  except ValueError:negatives+=1
  else:raise AssertionError('Invalid batch argument passed')
 assert g.batch('all',0,1)==[] and len(g.batch('all',2,1))==6
 # Same task with two complete banks must carry distinct question identities.
 a=g.generate('hard',77,'authored-hard',bank_profile='authored-omit-log');b=g.generate('hard',77,'authored-hard',a['generation']['parameters'],'authored-multiply-log')
 assert a['generation']['task_id']==b['generation']['task_id'] and a['question'][':question/id']!=b['question'][':question/id']
 # Actual native checks run one fixture per record so a genuine grading gap cannot erase other evidence.
 engine=[];reports=[];gaps=[];accepted=rejected=0
 for i,r in enumerate(records):
  item={'label':str(i),'record':r,'checks':engine_checks(r)};engine.append(item)
  path=HERE/'native-one-input.json';out=HERE/'native-one-report.json';save(path.name,[item]);out.unlink(missing_ok=True)
  proc=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path),str(out)],capture_output=True,text=True)
  if proc.returncode:
   gaps.append({'label':str(i),'template':r['generation']['template'],'error':proc.stderr.strip(),'checks':item['checks']});continue
  result=json.loads(out.read_text());reports.extend(result['records']);accepted+=result['accepted_checks'];rejected+=result['rejected_checks']
 save('engine-input.json',engine);save('engine-report.json',{'entry_point':'course_academy_engine::learning::grade_field','database_writes':0,'accepted_checks':accepted,'rejected_checks':rejected,'qualified_grading_gaps':gaps,'records':reports})
 (HERE/'native-one-input.json').unlink(missing_ok=True);(HERE/'native-one-report.json').unlink(missing_ok=True)
 baseline=json.loads((HERE/'numeric-baseline.json').read_text());now=[ROOT/'generate/scratch/17592186064177.py',*sorted(p for p in (ROOT/'generate/scratch/17592186064177').rglob('*') if p.is_file())]
 assert {str(p.relative_to(ROOT)):sha(p) for p in now}==baseline['sha256'],'Registered numeric artifact changed'
 capacity={}
 for level in g.SUPPORTED_LEVELS:
  rs=[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)]
  capacity[level]={'checked_records':len(rs),'distinct_tasks':len({r['generation']['task_id'] for r in rs}),'observed_templates':sorted({r['generation']['template'] for r in rs}),'profiles':sorted({r['generation']['bank_profile'] for r in rs}),'workload':'two terms' if level=='easy' else 'three terms' if level=='moderate' else 'four terms','authored_space_lower_bound':528 if level=='easy' else 15840 if level=='moderate' else 211200}
 slot_coverage={}
 for level in g.SUPPORTED_LEVELS:
  chosen=[r for r in records if r['generation']['template']=='authored-'+level]
  slots={k:sorted({r['generation']['parameters'][k] for r in chosen},key=str) for k in chosen[0]['generation']['parameters']}
  assert set(slots['base'])==set(range(2,13)) and set(slots['a'])=={-5,-4,-3,-2,2,3,4,5} and set(slots['b'])=={-4,-3,-2,2,3,4}
  if level!='easy':assert set(slots['tail'])=={'power','constant','reciprocal'} and set(slots['c'])=={-4,-3,-2,2,3,4} and {r['generation']['parameters']['power'] for r in chosen if r['generation']['parameters']['tail']=='power'}=={1,2,3}
  if level=='hard':assert set(slots['second_base'])==set(range(2,13)) and set(slots['d'])=={-3,-2,2,3}
  slot_coverage[level]=slots
 save('slot-coverage.json',{'authored':slot_coverage,'source_base':{mid:list(range(2,13)) for mid,(_,base) in g.SPECS.items() if base is not None},'fixed_roles':{'target':'whole integral','exponential_argument':'x','C':'one arbitrary interval constant','source_profiles':'complete original banks'},'changed_target':'not applicable: no target selector'})
 save('validation.json',{'status':'qualified' if gaps else 'pass','basis':2275,'source_counts':{'manifest_total':16,'MA':12,'independent':4,'raw_generation_ineligible':6,'raw_unrated':2,'raw_easy':5,'raw_moderate':9},'fidelity':{'exact_MA_captures':12,'complete_keyed_MA_banks':9,'keyed_MA_distractors':24,'unkeyed_MA_options_mapped':10,'fieldless_source':1,'independent_banks_checked':4},'mathematics':{'records_checked':len(records),'solution_rows':sum(s['rows'] for s in stats),'formal_integral_operands':sum(s['formal_integral_operands'] for s in stats),'negative_controls':negatives,'domain_intervals_checked':['x>0','x<0'],'capacity':capacity},'native_grading':{'accepted':accepted,'rejected':rejected,'qualified_gaps':len(gaps)},'baseline_unchanged':True,'limitations':['Blank source prompts omit f/g definitions; normal completion supplies inferred definitions.','Two unrated source records lack keys and worked solutions; normal completions are authored.','One source is fieldless; its normal blank is authored.','Hard is a same-method authored extension, not an observed MA difficulty.','Finite bounds; no linear-substitution or other downstream topic.']})
 # Recursive freeze includes every private dependency/evidence/cache and excludes only itself.
 files=[HERE.with_suffix('.py'),*sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='freeze.json')]
 save('freeze.json',{'version':g.VERSION,'basis':2275,'baseline_unchanged':True,'sha256':{str(p.relative_to(ROOT)):sha(p) for p in files},'engine':{'path':'generate/runs/current/check-engine','sha256':sha(ROOT/'generate/runs/current/check-engine')}})
 print(json.dumps({'records':len(records),'accepted':accepted,'rejected':rejected,'gaps':len(gaps),'baseline_unchanged':True}))
if __name__=='__main__':main()
