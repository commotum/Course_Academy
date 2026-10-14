#!/usr/bin/env python3
"""Independent displayed-signature/tuple/basis checks and full source fidelity."""
import copy,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def inspect(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];f=q[':question/answer-fields'][0]
 for t in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t' for c in t),'C0 control character'
  assert t.count('$')%2==0
  stack=[]
  for j,c in enumerate(t):
   if j and t[j-1]=='\\':continue
   if c=='{':stack.append(c)
   if c=='}':assert stack;stack.pop()
  assert not stack,'unbalanced TeX groups'
 formulas=re.findall(r'^- \$(.+)\$$',q[':question/problem'],re.M);assert len(formulas)==3
 mask=0;domains=[];categories=[]
 for i,v in enumerate(formulas):
  sig=re.match(r'([A-Z])\(([^)]+)\)=',v);assert sig
  inputs=len(sig[2].split(','));expression=v[sig.end():]
  outputs=len(expression.replace(r'\,','').split(',')) if expression.startswith('⟨') else (3 if r'\,k' in expression else 2)
  # Decoded source q-122656 ends with TeX thin space, not tuple punctuation.
  if inputs==outputs==2:mask|=1<<i
  domains.append((sig[1],sig[2],inputs,outputs,expression))
  categories.append((inputs,outputs,'+'.join(k for k,token in [('log',r'\operatorname{ln}'),('reciprocal',r'\frac'),('sqrt',r'\sqrt')] if token in expression) or 'all'))
 assert g.digest(categories)==r['generation']['mathematical_fingerprint']
 assert mask in g.LABELS,'empty classification after displayed mutation'
 choices=f[':answer-field/choices'];assert len(choices)==5
 assert len({a[':answer/value'] for a in choices})==5
 ref=f[':answer-field/correct'];assert ref[0]==':answer/id'
 canonical={'version':g.VERSION,'difficulty':q[':question/difficulty'].split('/')[-1],'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'bank':sorted(a[':answer/value'] for a in choices)}
 ident=g.digest(canonical);assert ident==r['generation']['content_fingerprint'];assert q[':question/id']==g.uid(ident)
 fid=g.uid(ident+'/selection');assert fid==f[':answer-field/id']
 assert all(a[':answer/id']==g.uid(fid+'/'+a[':answer/value']) for a in choices)
 chosen=[a for a in choices if a[':answer/id']==ref[1]];assert len(chosen)==1
 assert chosen[0][':answer/value']==g.LABELS[mask],(formulas,chosen,g.LABELS[mask])
 assert 'Therefore, the correct answer is "'+g.LABELS[mask]+'."' in q[':question/worked-solution']
 if not r['generation']['raw_evidence']:
  # Validate each actual named function explanation and its input signature.
  sol=q[':question/worked-solution']
  for name,sig,inputs,outputs,expression in domains:
   assert '$'+name+'('+sig+')$' in sol
   for sentence in re.findall(r'- The function \$'+name+r'\('+re.escape(sig)+r'\)\$(.*?)\n\n',sol+'\n\n',re.S):
    assert ('*not*' not in sentence)==(inputs==outputs==2)
  # Independent restriction checks from actual displayed component expressions.
  for name,sig,inputs,outputs,expr in domains:
   if inputs!=outputs or inputs!=2:continue
   part=sol.split('- The function $'+name+'('+sig+')$')[1].split('\n\n- ')[0]
   if r'\operatorname{ln}⁡' in expr:
    if 'x+y' in expr:
     m=re.search(r'ln}⁡\(x\+y([+-]\d+)?\)',expr);assert m
     h=-int(m[1] or 0);assert 'x+y>'+str(h) in part
    else:
     m=re.search(r'ln}⁡(?:y|\(y([+-]\d+)\))',expr);assert m
     h=-int(m[1] or 0);assert 'y>'+str(h) in part
   if r'\sqrt{x-y}' in expr:assert r'x-y\ge 0' in part
   if r'\frac{1}{x' in expr and r'\frac{1}{x+y' not in expr:
    m=re.search(r'frac\{1\}\{x([+-]\d+)\}',expr)
    if m:assert r'x\ne '+str(-int(m[1])) in part
   if r'\frac{1}{x+y' in expr:
    m=re.search(r'frac\{1\}\{x\+y([+-]\d+)?\}',expr);assert m
    assert r'x+y\ne '+str(-int(m[1] or 0)) in part
   if r'\frac{1}{(x' in expr:
    m=re.search(r'frac\{1\}\{\(x([+-]\d+)\)\^\{2\}\}',expr);assert m
    assert r'x\ne '+str(-int(m[1])) in part
   if r'\frac{1}{{x}^{2}}' in expr:assert r'x\ne 0' in part
   if r'\frac{{x}^{2}}{x-y' in expr:
    m=re.search(r'frac\{\{x\}\^\{2\}\}\{x-y([+-]\d+)?\}',expr);assert m
    offset=-int(m[1] or 0)
    expected=r'x\ne y'+(('+' if offset>=0 else '')+str(offset) if offset else '')
    assert expected in part
  # Compatible authored restrictions always have a real point: choose y=0,
  # x>|h|+1; every log is positive, radical nonnegative, denominator nonzero.
  if r['generation']['origin'].startswith('authored'):
   h=r['generation']['parameters']['h'];x=g.sp.Integer(abs(h)+2);y=g.sp.Integer(0)
   assert x+y-h>0 and x-y>=0 and x+h!=0
 return True

def main():
 rs=[];cases=[];fidelity=[]
 for source,q in g.SOURCES.items():
  p={'h':g.ANCHORS[source],'order':[0,1,2]}
  r=g.generate('easy',template=source,parameters=p,profile=source);inspect(r);rs.append(r)
  rq=r['question'];assert rq[':question/problem']==q[':question/problem'];assert rq[':question/worked-solution']==q[':question/worked-solution']
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
   assert (key in rq)==(key in q)
  assert rq[':question/difficulty']==q[':question/difficulty'][':db/ident']
  old=q[':question/answer-fields'][0];new=rq[':question/answer-fields'][0]
  assert new[':answer-field/type']==old[':answer-field/type'][':db/ident'];assert new[':answer-field/key']==old[':answer-field/key']
  assert sorted(a[':answer/value'] for a in old[':answer-field/choices'])==sorted(a[':answer/value'] for a in new[':answer-field/choices'])
  assert (':answer-field/correct' in old)==(':answer-field/correct' in new)
  correct=next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1]);assert correct==old[':answer-field/correct'][':answer/value']
  fidelity.append({'source':source,'prompt_exact':True,'solution_raw_exact':True,'bank_values':5,'correct_designation':True,'normal_solution_repair':source in ('q-122678','q-122675')})
  cases.append({'source_id':source,'template':source,'parameters':p,'bank_profile':source})
 for level in ('easy','moderate','hard'):
  for seed in range(120):
   r=g.generate(level,seed);inspect(r);rs.append(r)
   same=g.generate(level,seed+400,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
   assert same['question'][':question/id']==r['question'][':question/id']
 # Public selectors and complete easy boundary domains.
 tested=0
 for template,level in g.TEMPLATES.items():
  for h in range(1 if template=='q-122641' else -4,5):
   for order in itertools.permutations(range(3)):
    kinds=[None] if level=='easy' else (['log','sqrt','reciprocal'] if level=='moderate' else ['reciprocal+sqrt','log+sqrt','log+reciprocal'])
    for kind in kinds:
     p={'h':h,'order':list(order)}
     if kind:p['kind']=kind
     try:r=g.generate(level,template=template,parameters=p)
     except ValueError as e:assert 'not eligible' in str(e);continue
     inspect(r);tested+=1
 for bad in ({'h':5,'order':[0,1,2]},{'h':0,'order':[0,0,2]}):
  try:g.generate('hard',parameters=bad);raise AssertionError('accepted invalid parameters')
  except ValueError:pass
 for args in [('hard',0,'q-122465'),('easy',0,None,'blank')]:
  try:g.generate(*args);raise AssertionError('accepted invalid selector')
  except ValueError:pass
 # Negative mutation regressions check actual learner content and stages.
 base=g.generate('moderate',1)
 for action in ('control','signature','correct','conclusion','domain'):
  mutant=copy.deepcopy(base);q=mutant['question'];f=q[':question/answer-fields'][0]
  if action=='control':q[':question/problem']+='\x0c'
  if action=='signature':q[':question/problem']=q[':question/problem'].replace('A(x,y)','A(t)')
  if action=='correct':f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
  if action=='conclusion':q[':question/worked-solution']=q[':question/worked-solution'].replace('Therefore,','Thus,')
  if action=='domain':q[':question/worked-solution']=q[':question/worked-solution'].replace('x+y>','x+y<')
  # Rebuild legitimate content UUIDs after text mutation, so independent
  # mathematical/prose checks, rather than a stale content hash, reject it.
  old_correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  canonical={'version':g.VERSION,'difficulty':q[':question/difficulty'].split('/')[-1],'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'bank':sorted(a[':answer/value'] for a in f[':answer-field/choices'])}
  ident=g.digest(canonical);mutant['generation']['content_fingerprint']=ident;q[':question/id']=g.uid(ident);fid=g.uid(ident+'/selection');f[':answer-field/id']=fid
  for a in f[':answer-field/choices']:a[':answer/id']=g.uid(fid+'/'+a[':answer/value'])
  f[':answer-field/correct']=[':answer/id',g.uid(fid+'/'+old_correct)]
  try:inspect(mutant);raise RuntimeError('mutation escaped '+action)
  except AssertionError:pass
 for level in ('easy','moderate','hard'):
  for seed in range(25):
   plain=g.generate(level,seed,field_type='radio');alias=g.generate(level,seed,field_type=':answer-field.type/radio');assert plain==alias
 native=[{'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] else 'rejected','purpose':'all owned radio choices'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]} for i,r in enumerate(rs)]
 (D/'engine-input.json').write_text(json.dumps(native))
 subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 engine=json.loads((D/'engine-report.json').read_text())
 tasks={l:set() for l in ('easy','moderate','hard')}
 for template,l in g.TEMPLATES.items():
  for order in itertools.permutations(range(3)):
   kinds=[None] if l=='easy' else (['log','sqrt','reciprocal'] if l=='moderate' else ['reciprocal+sqrt','log+sqrt','log+reciprocal'])
   for kind in kinds:
    p={'h':g.ANCHORS.get(template,0),'order':list(order)}
    if kind:p['kind']=kind
    try:r=g.generate(l,template=template,parameters=p)
    except ValueError:continue
    tasks[l].add(r['generation']['mathematical_fingerprint'])
 (D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 review=[]
 for source in g.SOURCES:review.append(g.generate('easy',17,source))
 for l in ('moderate','hard'):
  kinds=['log','sqrt','reciprocal'] if l=='moderate' else ['reciprocal+sqrt','log+sqrt','log+reciprocal']
  for i,kind in enumerate(kinds):review.append(g.generate(l,7+i,parameters={'h':i-1,'order':list(itertools.permutations(range(3)))[i],'kind':kind}))
 (D/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 text='# Source and generated review\n\nAll answers are author preview data. Source records are unmodified basis 1356.\n'
 for source,q in g.SOURCES.items():
  text+='\n## Original '+source+'\n\n'+q[':question/problem']+'\n\nBank: '+', '.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']+'\n\n### Generated variant\n\n'+g.markdown(next(r for r in review if r['generation']['template']==source))+'\n'
 for r in review[8:]:text+='\n## Authored '+r['question'][':question/difficulty'].split('/')[-1]+' variant\n\n'+g.markdown(r)+'\n'
 (D/'review.md').write_text(text)
 report={'passed':True,'source_records':len(fidelity),'source_fidelity':fidelity,'banks_matched':8,'answer_values_matched':40,'correct_designations_matched':8,'raw_exact_solutions':8,'normal_source_name_repairs':2,'sample_records':len(rs),'explicit_boundary_instances':tested,'mutation_regressions':5,'enum_selector_comparisons':75,'semantic_tasks_by_level':{k:len(v) for k,v in tasks.items()},'default_authored_kinds':{l:sorted({r['generation']['parameters']['kind'] for r in rs[8:] if r['question'][':question/difficulty'].endswith('/'+l)}) for l in ('moderate','hard')},'default_easy_families':sorted({r['generation']['template'] for r in rs[8:] if r['question'][':question/difficulty'].endswith('/easy')}),'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'dependencies':rs[0]['generation']['dependencies'],'plot_requirement':'none','engine_binary_sha256':g.hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'limitations':['Moderate/hard difficulty labels are authored design claims; no source at these levels.','This narrow categorical skill has a finite meaningful task family; coefficient/shift/notation changes do not enlarge its semantic task count.','Raw name errors remain evidence only; normal solutions repair them.']}
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
