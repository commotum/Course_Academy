#!/usr/bin/env python3
"""Exhaustive private displayed content, fidelity and native selection checks."""
import hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));import independent_math as p
z=importlib.util.spec_from_file_location('reciprocal_sum',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
def dump(name,v):(HERE/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
source=g.Q;native=[];counts={'records':0,'choices':0,'rows':0,'sides':0};cases=[];replay=[];preview=[]
def check(r):
 q=r['question'];f=p.integrand(q[':question/problem']);field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];values=[p.scalar(a[':answer/value']) for a in choices];ders=[p.derivative(e) for e in values]
 matches=[i for i,v in enumerate(ders) if p.equal(v,f)];assert len(matches)==1,(r['generation'],matches,f,ders)
 assert choices[matches[0]][':answer/id']==field[':answer-field/correct'][1]
 assert all(not p.equal(d,z) for i,d in enumerate(ders) for z in ders[:i]),('family collision',r['generation'])
 rows=p.rows(q[':question/worked-solution']);assert rows
 for row in rows:
  for e in row:assert p.equal(p.derivative(e),f),(r['generation'],q[':question/worked-solution'],e,f,p.derivative(e))
  counts['rows']+=1;counts['sides']+=len(row)
 ids=[q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in choices];assert len(set(ids))==len(ids)
 for a in ids:uuid.UUID(a)
 for text in [q[':question/problem'],q[':question/worked-solution']]:g.fmt.validate_prose(text)
 for a in choices:g.fmt.validate_tex(a[':answer/value'])
 counts['records']+=1;counts['choices']+=len(choices)
 return f

for name,spec in g.TEMPLATES.items():
 r=g.generate(spec['level'],template=name,parameters=spec['original']);check(r);q=r['question'];o=source[name]
 prompt=g.fmt.normalize_prose(g.clean(o[':question/problem']));assert prompt==q[':question/problem'],(name,prompt,q[':question/problem'])
 solmatch=None
 if ':question/worked-solution' in o:
  sol=g.fmt.normalize_prose(g.clean(o[':question/worked-solution']));assert sol==q[':question/worked-solution'],(name,sol,q[':question/worked-solution']);solmatch=True
 old=[p.scalar(g.clean(a[':answer/value'])) for a in o[':question/answer-fields'][0][':answer-field/choices']];new=[p.scalar(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
 assert len(old)==len(new)==5
 # Equivalence of complete values with a fixed C, rather than only derivative,
 # establishes source-bank replay; family inequivalence is a separate check.
 assert all(sum(p.equal(a,b) for b in new)==1 for a in old),(name,old,new)
 of=o[':question/answer-fields'][0]
 if ':answer-field/correct' in of:
  expected=p.scalar(g.clean(of[':answer-field/correct'][':answer/value']));actual=next(p.scalar(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==q[':question/answer-fields'][0][':answer-field/correct'][1]);assert p.equal(expected,actual)
 cases.append({'source_id':name,'level':spec['level'],'template':name,'profile':name,'bank_profile':name,'parameters':spec['original'],'authored_calibration':spec.get('calibration'),'authored_solution':solmatch is None})
 replay.append({'source_id':name,'prompt_exact_after_math_normalization':True,'solution_exact_after_math_normalization':solmatch,'matched_values':5,'total_values':5,'complete_bank':True,'original_key_present':':answer-field/correct' in of})
 preview.extend([r,g.generate(spec['level'],template=name,parameters=next(t for t in g.DOMAINS[name] if t!=spec['original']))])

capacity={};profile_capacity={};coverage={}
for level in g.GENERATORS:
 tasks=set();seen=[]
 for name,t in g.TEMPLATES.items():
  if t['level']!=level:continue
  rendered=set();param_seen={key:set() for key in t['slots']}
  for params in g.DOMAINS[name]:
   r=g.generate(level,seed=41,template=name,parameters=params);f=check(r);tasks.add(p.s.srepr(p.s.expand(f)));rendered.add(r['question'][':question/problem']);seen.append(r)
   for key,value in params.items():param_seen[key].add(str(value))
   field=r['question'][':question/answer-fields'][0]
   native.append({'label':name+'/'+json.dumps(params,sort_keys=True),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'every owned option'} for a in field[':answer-field/choices']]})
  coverage[name]={k:sorted(v) for k,v in param_seen.items()};profile_capacity[name]={'parameter_instances':len(g.DOMAINS[name]),'rendered_givens':len(rendered)}
 capacity[level]={'semantic_tasks':len(tasks),'parameter_instances':len(seen)}
 for seed in range(12):assert g.generate(level,seed)==g.generate(level,seed)
 assert len({g.generate(level,seed)['generation']['mathematical_task_fingerprint'] for seed in range(12)})>=6
# Fail closed on public bounds, extra keys, wrong profiles, wrong field types.
for name,t in g.TEMPLATES.items():
 for bad in [{},dict(t['original'],extra=2),{**t['original'],next(iter(t['slots'])):999}]:
  try:g.generate(t['level'],template=name,parameters=bad)
  except ValueError:pass
  else:raise AssertionError(('invalid public parameters accepted',name,bad))
for kw in [{'profile':'foreign'},{'field_type':'blank'}]:
 try:g.generate('easy',**kw)
 except ValueError:pass
 else:raise AssertionError(kw)
# Separately labelled ownership diagnostics; never counted as math failures.
r=g.generate('easy',seed=5)
ownership=[{'label':'ownership diagnostics','record':r,'checks':[{'field_index':0,'submitted':'999999','expected':'unresolved','purpose':'foreign numeric ownership'},{'field_index':0,'submitted':'malformed','expected':'unresolved','purpose':'malformed learner selection'}]}]
dump('ownership-input.json',ownership)
subprocess.run([str(HERE/'check-engine'),str(HERE/'ownership-input.json'),str(HERE/'ownership-diagnostics.json')],check=True,timeout=60)
dump('source-cases.json',cases);dump('source-bank-fidelity.json',replay);dump('review.json',preview);(HERE/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in preview)+'\n')
dump('native-input.json',native)
subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-validation.json')],check=True,timeout=60)
cli=json.loads(subprocess.check_output([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--format','json','--seed','91'],text=True));assert isinstance(cli,list) and len(cli)==3
for r in cli:check(r)
dump('cli-preview.json',cli)
batch_checks={}
for level in g.GENERATORS:
 total=capacity[level]['semantic_tasks']
 rows=g.generate_batch(level,seed=17,count=total)
 keys=[p.s.srepr(p.s.expand(p.integrand(r['question'][':question/problem']))) for r in rows]
 assert len(keys)==len(set(keys))==total
 assert rows==g.generate_batch(level,seed=17,count=total)
 try:g.generate_batch(level,count=total+1)
 except ValueError:pass
 else:raise AssertionError('semantic batch exhaustion did not fail closed')
 batch_checks[level]={'full_capacity_batch':total,'independently_read_unique_integrands':len(set(keys)),'excess_count_rejected':True}
for bad in (True,False,1.5,'2',None):
 for api in (g.generate,g.generate_batch):
  try:api('easy',seed=bad)
  except ValueError:pass
  else:raise AssertionError(('noninteger seed accepted',api,bad))
for bad in (True,0,-1,1.5,'2'):
 try:g.generate_batch('hard',count=bad)
 except ValueError:pass
 else:raise AssertionError(('invalid batch count accepted',bad))
cli_many=json.loads(subprocess.check_output([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--format','json','--seed','18','--count','24'],text=True));assert len(cli_many)==72
for level in g.GENERATORS:
 keys=[p.s.srepr(p.s.expand(p.integrand(r['question'][':question/problem']))) for r in cli_many if r['question'][':question/difficulty']==':question.difficulty/'+level]
 assert len(keys)==len(set(keys))==24
excess=subprocess.run([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--format','json','--count','25'],text=True,capture_output=True);assert excess.returncode!=0 and 'exceeds semantic capacity' in excess.stderr
dump('batch-validation.json',batch_checks)
result={'status':'passed','source_basis':2275,'counts':counts,'source_fidelity':{'complete_banks':9,'values':45,'exact_prompts':9,'exact_observed_solutions':7,'authored_missing_solutions':2},'capacity':capacity,'profile_capacity':profile_capacity,'slot_coverage':coverage,'native_grader_sha256':hashlib.sha256((HERE/'check-engine').read_bytes()).hexdigest(),'antiderivative_semantics':'differentiate actual rendered answers and all formal integral rows on connected source domain; equivalence modulo constant checked independently of native radio selection','batch_validation':batch_checks,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0}
dump('validation.json',result);print(json.dumps(result,indent=2))
