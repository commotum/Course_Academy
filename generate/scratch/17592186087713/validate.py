#!/usr/bin/env python3
"""Independent displayed-array parser, whole-source fidelity, and real grading."""
import collections,copy,hashlib,importlib.util,itertools,json,pathlib,re,subprocess,uuid
import sympy as sp
HERE=pathlib.Path(__file__).resolve().parent;REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('matrix_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Retained basis-1356 source fidelity checks explicitly exercise legacy radio.
g.generate=g.generate_radio
def write(name,data): (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def h(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def numeric(token):
 if re.fullmatch(r'\\sqrt\{[23]\}',token):return sp.sqrt(int(token[-2]))
 return sp.Rational(token)
def parse_prompt(prompt):
 req=re.search(r'Which of the following is a \$(\d+)\s*\\(?:times|cdot)\s*(\d+)\$ matrix\?',prompt);assert req,'Requested dimensions missing'
 target=tuple(map(int,req.groups()))
 arrays=[]
 for m in re.finditer(r'([A-Z])\s*=\s*(?:\[)?\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\2\}(?:\])?',prompt,re.S):
  rows=[[v.strip() for v in row.split('&')] for row in re.split(r'\\\\',m[3])]
  assert rows and all(len(row)==len(rows[0]) for row in rows),'Nonrectangular displayed array'
  nums=[[numeric(v) for v in row] for row in rows]
  arrays.append((m[1],(len(rows),len(rows[0])),nums))
 assert len(arrays)==3 and len({a[0] for a in arrays})==3
 return target,arrays

def format_check(text):
 # All brace groups and $ pairs must be balanced, including actual array bodies.
 depth=0
 for i,c in enumerate(text):
  if c in '{}' and (i==0 or text[i-1]!='\\'):
   depth+=1 if c=='{' else -1;assert depth>=0,'Bad TeX group'
 assert depth==0
 rest=text.replace('$$','');assert rest.count('$')%2==0
 assert text.count('$$') in (0,2)
 assert len(re.findall(r'\\begin\{aligned\}',text))==len(re.findall(r'\\end\{aligned\}',text))
 assert len(re.findall(r'\\begin\{bmatrix\}',text))==len(re.findall(r'\\end\{bmatrix\}',text))

def validate_record(rec):
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=rec['question'];meta=rec['generation'];target,arrays=parse_prompt(q[':question/problem'])
 labels=[a[0] for a in arrays];ds=[a[1] for a in arrays]
 assert all(1<=v<=4 for d in ds for v in d)
 match={a[0] for a in arrays if a[1]==target};assert len(match) in (1,2)
 if meta['template'].startswith('peer_'):
  level=meta['level']
  if level=='easy':
   r,c=target;assert r!=c and max(target)<=3 and len(match)==1
   assert sorted(ds) in (sorted([target,(c,r),(r,r)]),sorted([target,(c,r),(c,c)]))
  if level=='hard':
   assert min(target)>=3
   assert all(min(d)>=2 and sum(abs(x-y) for x,y in zip(d,target))==1 for d in ds if d!=target)
  assert len(match)==(2 if meta['template'].endswith('multiple') else 1)
 f=q[':question/answer-fields'];assert len(f)==1;f=f[0]
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 assert f[':answer-field/correct'][0]==':answer/id';choices=f[':answer-field/choices'];assert len(choices)==5
 assert len({a[':answer/id'] for a in choices})==5
 true=[];subsets=[]
 for a in choices:
  assert a[':answer/type']==':answer.type/text'
  subset=re.findall(r'\$([A-Z])\$',a[':answer/value']);assert 1<=len(subset)<=2 and len(set(subset))==len(subset) and set(subset)<=set(labels)
  assert a[':answer/value']==' and '.join('$'+l+'$' for l in subset)+' only'
  subsets.append(frozenset(subset))
  if set(subset)==match:true.append(a[':answer/id'])
 assert len(set(subsets))==5 and true==[f[':answer-field/correct'][1]],'Displayed correct subset mismatch'
 sol=q[':question/worked-solution']
 bullets=re.findall(r'- The matrix \$([A-Z])\$ has \$(\d+)\$ (rows?) and \$(\d+)\$ (columns?)\. So, its dimensions are \$(\d+)\\times (\d+)\.\$ (.*?)\n(?:\n|$)',sol+'\n\n')
 assert len(bullets)==3,'Missing solution stage'
 for (label,r,rword,c,cword,dr,dc,mark),(al,d,_) in zip(bullets,arrays):
  r,c,dr,dc=map(int,(r,c,dr,dc));assert label==al and (r,c)==d and (dr,dc)==d
  assert rword==('row' if r==1 else 'rows') and cword==('column' if c==1 else 'columns')
  assert ('✓' in mark)==(label in match)
 ending=sol.split('Therefore, only ')[1];endlabels=set(re.findall(r'\$([A-Z])\$',ending));assert endlabels==match
 endtarget=re.search(r'\$(\d+)\\times (\d+)\$',ending);assert tuple(map(int,endtarget.groups()))==target
 for text in (q[':question/problem'],sol,*[a[':answer/value'] for a in choices]):format_check(text)
 for value in (q[':question/id'],f[':answer-field/id'],*[a[':answer/id'] for a in choices]):uuid.UUID(value)
 actual=g.digest({'version':g.VERSION,'prompt':q[':question/problem'],'solution':sol,'bank':sorted(a[':answer/value'] for a in choices),'type':'radio'})
 assert actual==meta['content_hash'] and q[':question/id']==g.uid(actual)
 assert meta['mathematical_task_fingerprint']==g.digest({'criterion':'ordered-row-column-dimensions','target':list(target),'candidate_dimensions':sorted(list(d) for d in ds)})
 return target,arrays

def main():
 source=json.loads((HERE/'source.json').read_text());cases=json.loads((HERE/'source-cases.json').read_text());byid={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 engine=[];review=[];fidelity=[];bank_count=choice_count=wrong_count=solutions=designations=0
 def check(rec,label):
  validate_record(rec);f=rec['question'][':question/answer-fields'][0]
  engine.append({'label':label,'record':rec,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual displayed subset '+a[':answer/value']} for a in f[':answer-field/choices']]})
 for case in cases:
  sid=case['source_id'];original=byid[sid]
  rec=g.generate(case['level'],parameters=case['parameters'],template=case['template'],profile=case['bank_profile']);check(rec,sid+' original replay');review.append({'label':sid+' original parameter replay','source':original,'record':rec})
  q=rec['question'];f=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0]
  assert q[':question/problem']==original[':question/problem'],'Full prompt fidelity'
  assert collections.Counter(a[':answer/value'] for a in f[':answer-field/choices'])==collections.Counter(a[':answer/value'] for a in of[':answer-field/choices'])
  bank_count+=1;choice_count+=len(of[':answer-field/choices']);wrong_count+=4
  if ':answer-field/correct' in of:
   cv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert cv==of[':answer-field/correct'][':answer/value'];designations+=1
  if ':question/worked-solution' in original:assert q[':question/worked-solution']==original[':question/worked-solution'];solutions+=1
  fidelity.append({'source_id':sid,'exact_prompt':True,'complete_bank':True,'matched_choices':5,'matched_distractors':4,'correct_designation':'matched' if ':answer-field/correct' in of else 'derived repair, absent in original','worked_solution':'exact' if ':question/worked-solution' in original else 'authored absent solution'})
  # Changed targets/shapes through normal API, same original profile and stage type.
  match_positions=tuple(i for i,a in enumerate(case['parameters']['matrices']) if [len(a),len(a[0])]==case['parameters']['target'])
  for j,(r,c) in enumerate(((2,3),(3,4))):
   p=copy.deepcopy(case['parameters']);p['target']=[r,c]
   dims=[[r,c] if i in match_positions else ([c,r] if i==next(k for k in range(3) if k not in match_positions) else [r,r]) for i in range(3)]
   p['matrices']=[[[str((i+row+col)%7-3) for col in range(dc)] for row in range(dr)] for i,(dr,dc) in enumerate(dims)]
   variant=g.generate('moderate',seed=j+21,parameters=p,template=case['template'],profile=sid);check(variant,sid+f' changed-parameter bank variant {j+1}');review.append({'label':sid+f' generated variant {j+1}','record':variant})
 generated={};fingerprints={}
 for level in ('easy','moderate','hard'):
  fps=set()
  for seed in range(120):
   rec=g.generate(level,seed);check(rec,f'{level} seed {seed}');fps.add(rec['generation']['mathematical_task_fingerprint'])
   if seed<2:review.append({'label':f'Authored {level} example {seed+1}','record':rec})
   # Seed/option-order independent identity for fixed content/profile.
   alt=g.generate(level,seed+1000,parameters=rec['generation']['parameters'],template=rec['generation']['template'],profile=rec['generation']['profile'])
   assert alt['question'][':question/id']==rec['question'][':question/id'];validate_record(alt)
  generated[level]=120;fingerprints[level]=len(fps)
 # Explicit invalid input rejection and level workload guards.
 guard_count=0
 def rejects(**kw):
  nonlocal guard_count
  try:g.generate(**kw)
  except ValueError:guard_count+=1;return
  raise AssertionError('Invalid explicit input accepted')
 e=g.generate_easy(0)['generation']['parameters'];bad=copy.deepcopy(e);bad['matrices'][0][0].append('0');rejects(level='easy',parameters=bad)
 bad=copy.deepcopy(e);bad['matrices']=[e['matrices'][0]]*3;rejects(level='easy',parameters=bad)
 bad=copy.deepcopy(e);bad['target']=[4,4];rejects(level='easy',parameters=bad)
 bad=copy.deepcopy(e);bad['labels']=['A','A','C'];rejects(level='easy',parameters=bad)
 bad=copy.deepcopy(e);bad['matrices'][0][0][0]='x';rejects(level='easy',parameters=bad)
 rejects(level='hard',parameters=e,template='peer_single')
 rejects(level='moderate',template='legacy_bmatrix')
 rejects(level='easy',profile='unknown');rejects(level='easy',field_type='checkbox')
 # Canonical assessed-task identity excludes incidental entries and labels/order.
 rec=g.generate_hard(9);p=copy.deepcopy(rec['generation']['parameters']);p['labels']=['X','Y','Z'];p['matrices']=[[[str(9) for _ in row] for row in a] for a in p['matrices']]
 other=g.generate('hard',parameters=p,template=rec['generation']['template'],profile=rec['generation']['profile'])
 assert other['generation']['mathematical_task_fingerprint']==rec['generation']['mathematical_task_fingerprint'] and other['question'][':question/id']!=rec['question'][':question/id']
 p['labels'].reverse();p['matrices'].reverse();other=g.generate('hard',parameters=p,template=rec['generation']['template'])
 assert other['generation']['mathematical_task_fingerprint']==rec['generation']['mathematical_task_fingerprint']
 # Different eligible whole banks must produce different content identities.
 for level in ('easy','moderate','hard'):
  rec=g.generate(level,71,template='peer_single');p=rec['generation']['parameters'];m=tuple(i for i,a in enumerate(p['matrices']) if g.dimensions(a)==p['target']);eligible=[k for k in ('omit01','omit02','omit12') if m in g.PROFILES[k]]
  ids={g.generate(level,parameters=p,template='peer_single',profile=k)['question'][':question/id'] for k in eligible};assert len(ids)==3
 # Enumerate finite semantic shape catalog, without incidental numerical entries.
 catalog={}
 for level in ('easy','moderate','hard'):
  tasks=set()
  for r in range(1,5):
   for c in range(1,5):
    target=(r,c)
    if level=='easy':
     if r==c or max(target)>3:continue
     for sq in ((r,r),(c,c)):tasks.add((target,tuple(sorted((target,(c,r),sq)))))
    else:
     if level=='hard' and min(target)<3:continue
     foils=[(a,b) for a in range(1,5) for b in range(1,5) if (a,b)!=target and (level!='hard' or min(a,b)>=2 and abs(a-r)+abs(b-c)==1)]
     for a,b in itertools.combinations(foils,2):tasks.add((target,tuple(sorted((target,a,b)))))
     for a in foils:tasks.add((target,tuple(sorted((target,target,a)))))
  catalog[level]=len(tasks)
  # Exercise every member of the actual finite structural domain, including
  # one/two matches and each eligible whole bank, through displayed-text QA.
  for number,(target,shapes) in enumerate(sorted(tasks)):
   params={'target':list(target),'labels':['A','B','C'],'matrices':[[[str((row+col)%3-1) for col in range(c)] for row in range(r)] for r,c in shapes]}
   multiple=sum(d==target for d in shapes)==2
   template='peer_multiple' if multiple else 'peer_single'
   matches=tuple(i for i,d in enumerate(shapes) if d==target)
   for profile in ('omit01','omit02','omit12'):
    if matches in g.PROFILES[profile]:
     instance=g.generate(level,seed=number,template=template,parameters=params,profile=profile)
     check(instance,f'{level} structural catalog {number} {profile}')
 write('native-input.json',engine)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 native=json.loads((HERE/'native-report.json').read_text())
 assert native['accepted_checks']==len(engine) and native['rejected_checks']==4*len(engine) and native['documented_unresolved_checks']==0
 write('review.json',review)
 md=['# Matrix identification review\n','Original replays retain observed prompts and banks. Two missing source solutions/correct refs are explicitly derived. Every variant is generated through the public API.']
 for item in review:
  md+=['\n## '+item['label'],'\n'+g.markdown(item['record'])]
  if 'source' in item:md+=['\nRaw worked solution: '+item['source'].get(':question/worked-solution','**Absent in original. Displayed explanation above is authored.**')]
 (HERE/'review.md').write_text('\n'.join(md)+'\n')
 report={'passed':True,'source':g.SOURCE,'source_questions':len(cases),'exact_prompt_matches':bank_count,'complete_original_banks':{'matched':bank_count,'total':len(cases)},'source_choices':{'matched':choice_count,'total':40},'source_distractors':{'matched':wrong_count,'total':32},'observed_correct_designations':{'matched':designations,'total':6},'derived_correct_designation_repairs':2,'observed_full_solutions':{'exact':solutions,'total':6},'authored_missing_solutions':2,'unrated_level_assignments':2,'source_format_repairs':0,'canonical_missing_arrays':'raw evidence retained; cannot reconstruct absent B/C from source, not a practice fidelity denominator','per_source':fidelity,'generated_checks':generated,'sampled_distinct_mathematical_tasks':fingerprints,'finite_semantic_catalog':catalog,'explicit_rejection_checks':guard_count,'independent_displayed_arrays_and_solution_stages':'passed','identity_checks':'passed','native_records':len(engine),'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'native_unresolved':0,'database_writes':0,'grader_sha256':h(REPO/'generate/runs/current/check-engine'),'generator_sha256':h(HERE.with_suffix('.py'))}
 write('validation.json',report)
 print(json.dumps(report,indent=2))
 # Freeze artifact hashes only after all checks/grade reports/reviews exist.
 artifacts=[HERE.with_suffix('.py'),*[p for p in HERE.iterdir() if p.is_file() and p.name!='artifact-hashes.json']]
 write('artifact-hashes.json',{'source_basis':1356,'validation_passed':True,'sha256':{str(p.relative_to(REPO)):h(p) for p in sorted(artifacts)}})
if __name__=='__main__':main()
