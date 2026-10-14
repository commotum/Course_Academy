#!/usr/bin/env python3
"""Independent displayed math, complete raw replay, native memory-only grading."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('surfacegen',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
u,v,x,theta=g.u,g.v,g.x,g.theta
# Independent parsing reads actual rendered strings, not generator expressions.
def scalar(t):return g.parser.scalar(t.replace(r'\theta','t').replace('[','(').replace(']',')')).subs(g.parser.t,theta)
def vector(t):return sp.Matrix([scalar(z) for z in t[1:-1].replace(r'\,','').split(',')])
def equal(a,b):
 if isinstance(a,sp.MatrixBase):return all(sp.expand(z)==0 for z in a-b)
 z=sp.expand(a-b)
 return z==0 or sp.simplify(sp.trigsimp(z))==0
def formatting(t):
 assert all(ord(z)>=32 or z in '\n\t' for z in t),'C0 character'
 assert t.count('$')%2==0,'Math delimiter parity'
 balance=0
 for i,z in enumerate(t):
  if z in '{}' and (i==0 or t[i-1]!='\\'):
   balance+=1 if z=='{' else -1
   assert balance>=0,'Brace prefix'
 assert balance==0,'Brace parity'
 assert '--' not in t and '+-' not in t,'Ungrouped negative factor'
def read_surface(text):
 if '⟨' in text:return vector(re.search('⟨[^⟨⟩]*⟩',text)[0])
 coords=re.findall(r'[xyz]\s*=\s*(.*?)(?=,|\.|\$)',text);assert len(coords)==3,coords
 return sp.Matrix([scalar(z) for z in coords])
def small_matrices(text):
 stack=[];items=[]
 for m in re.finditer(r'\\(?:begin|end)\{aligned\}',text):
  if m[0].startswith(r'\begin'):stack.append(m)
  else:
   b=stack.pop();z=text[b.end():m.start()]
   if r'\begin{aligned}' not in z and '=' not in z and ' & ' in z:items.append(z)
 return items

def verify(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];meta=r['generation'];base=meta['template'].split(':')[-1]
 if meta['evidence_only']:
  assert not meta['eligible_for_learning'];return
 assert meta['eligible_for_learning'];assert q[':question/difficulty'].endswith('/'+g.TEMPLATES[meta['template']])
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:formatting(text)
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 ids=[a[':answer/id'] for a in f[':answer-field/choices']];assert len(set(ids))==len(ids)
 key=f[':answer-field/correct'];assert key[0]==':answer/id' and key[1] in ids
 prompt=q[':question/problem'];sol=q[':question/worked-solution']
 if base=='q-167648':
  supplied=vector(re.search('⟨[^⟨⟩]*⟩',prompt)[0]);want=sp.simplify(sp.sqrt(sp.trigsimp(supplied.dot(supplied))))
  assert '{{field-1}}' in prompt and f[':answer-field/type'].endswith('/blank')
  assert 'We first compute' not in sol and 'tangent vectors' not in prompt
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==1
  rows=blocks[0].split(r' & =')[1:];assert len(rows)==5
  stages=[]
  for row in rows:
   stage=row.split(r' \\')[0].split(r'.\end')[0].rstrip('.')
   stages.append(stage)
   assert equal(scalar(stage),want),('Norm stage',stage,want)
  assert stages[0].count(')^{2}')==3,'Three individually squared product components'
  assert '{cos}^{2}' in stages[1] and '{sin}^{2}' in stages[1] and '({cos}' not in stages[1],'Expanded squared components'
  assert '({cos}^{2}' in stages[2] and '+{sin}^{2}' in stages[2],'Trigonometric common-factor stage'
  assert '{6}' in stages[3] and '{4}' in stages[3] and 'cos' not in stages[3] and 'sin' not in stages[3],'Reduced radicand stage'
  assert 'sqrt' in stages[4] and '{6}' not in stages[4],'Collected square-root factor stage'
  # Real semantics independently checked both signs and the singular boundary.
  for xx in (-3,-1,0,1,2):
   assert want.subs(x,xx).is_nonnegative is True
 else:
  surface=read_surface(prompt);du=surface.diff(u);dv=surface.diff(v)
  want=du.cross(dv).applyfunc(sp.expand)
  assert f[':answer-field/type'].endswith('/radio')
  source=g.SOURCES[base].get(':question/worked-solution')
  if source:
   assert sol.split('We first compute')[0].split('In vector form')[0]==source.split('We first compute')[0].split('In vector form')[0]
  tangent=sol.split('We first compute')[1].split('Therefore, the fundamental')[0]
  args=re.findall(r'\\frac\{∂\}\{∂(u|v)\}\((.*?)\)(?=,|⟩)',tangent)
  assert len(args)==6,('Formal substitution stage missing',args)
  # First two original/source blocks preserve all 3 coordinate derivative demands.
  for i,(variable,arg) in enumerate(args):
   vv=u if i<3 else v;assert variable==str(vv)
   assert equal(sp.diff(scalar(arg),vv),sp.diff(surface[i%3],vv)),('Printed partial argument',arg)
  vals=[vector(m[0]) for m in re.finditer('⟨[^⟨⟩]*⟩',tangent) if '\\frac' not in m[0]]
  assert len(vals)==2 and equal(vals[0],du) and equal(vals[1],dv),'Tangent values'
  tail=sol.split('Therefore, the fundamental')[1]
  matrices=small_matrices(tail);assert len(matrices)==4
  big=next(z for z in matrices if len(z.split(r' \\ '))==3)
  rows=big.split(r' \\ ');assert rows[0]=='i & j & k'
  assert equal(sp.Matrix([scalar(z) for z in rows[1].split(' & ')]),du)
  assert equal(sp.Matrix([scalar(z) for z in rows[2].split(' & ')]),dv)
  minors=[z for z in matrices if len(z.split(r' \\ '))==2]
  # Captured inner determinants occur in mathematical left-to-right order.
  for minor,(j,k) in zip(minors,((1,2),(0,2),(0,1))):
   vals=[scalar(z) for row in minor.split(r' \\ ') for z in row.split(' & ')]
   assert all(equal(a,b) for a,b in zip(vals,[du[j],du[k],dv[j],dv[k]]))
  assert '⟩' in tail and '⟩' in sol
  stage_vectors=[vector(m[0]) for m in re.finditer('⟨[^⟨⟩]*⟩',tail) if '\\begin' not in m[0]]
  assert stage_vectors and all(equal(z,want) for z in stage_vectors),'Cross stages'
  if base=='q-105607':assert len(stage_vectors)==2 and '-[' in tail,'Unevaluated j cofactor stage absent'
  assert r',\,-|\begin{aligned}' in tail,'Cofactor middle sign absent'
 values=[scalar(a[':answer/value']) if base=='q-167648' else vector(a[':answer/value']) for a in f[':answer-field/choices']]
 assert all(not equal(a,b) for i,a in enumerate(values) for b in values[:i]),'Every-pair bank ambiguity'
 correct=[a[':answer/id'] for a,z in zip(f[':answer-field/choices'],values) if equal(z,want)]
 assert correct==[key[1]],'Correct answer from displayed math'
 if base!='q-167648':
  recipes=[want,-want,sp.Matrix([want[0],-want[1],want[2]]),du,dv]
  assert all(sum(equal(z,e) for z in values)==1 for e in recipes),'Complete method bank'
 return want

def main():
 replays=[];review=[];engine=[];normal=[]
 source_cases=[];designation=0;matched=0;distractors=0;inferred_keys=[]
 for base,q in g.SOURCES.items():
  p={'a':1,'b':1,'c':1};r=g.generate('easy',template=base,parameters=p,profile='observed:'+base);rq=r['question'];review.append(r)
  assert rq[':question/problem']==q[':question/problem']
  for attr in (':question/difficulty',':question/worked-solution'):
   assert (attr in rq)==(attr in q)
  assert rq.get(':question/worked-solution')==q.get(':question/worked-solution')
  if ':question/difficulty' in q:assert rq[':question/difficulty']==q[':question/difficulty'][':db/ident']
  assert len(rq[':question/answer-fields'])==len(q[':question/answer-fields'])
  for rf,sf in zip(rq[':question/answer-fields'],q[':question/answer-fields']):
   assert rf[':answer-field/key']==sf[':answer-field/key'] and rf[':answer-field/type']==sf[':answer-field/type'][':db/ident']
   rv=[a[':answer/value'] for a in rf[':answer-field/choices']];sv=[a[':answer/value'] for a in sf[':answer-field/choices']]
   assert rv==sv;matched+=len(sv)
   assert (':answer-field/correct' in rf)==(':answer-field/correct' in sf)
   if ':answer-field/correct' in sf:
    designation+=1;assert next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value'];distractors+=len(sv)-1
  # Independently identify the mathematical cross in every original whole bank,
  # including absent designations; this never changes raw evidence or fidelity refs.
  if base=='q-167648':
   ss=read_surface(q[':question/worked-solution']);aa=ss.diff(x);bb=ss.diff(theta);cc=aa.cross(bb).applyfunc(sp.expand)
   before=q[':question/worked-solution'].split('Therefore, the fundamental')[1].split('Finally, the corresponding')[0]
   cvs=[vector(mm[0]) for mm in re.finditer('⟨[^⟨⟩]*⟩',before) if '\\begin' not in mm[0]]
   assert len(cvs)==3 and all(all(sp.trigsimp(e)==0 for e in z-cc) for z in cvs),'Original norm cross stages'
   want=sp.simplify(sp.sqrt(sp.trigsimp(cc.dot(cc))))
  else:
   ss=read_surface(q[':question/problem']);want=ss.diff(u).cross(ss.diff(v)).applyfunc(sp.expand)
  for fi,f in enumerate(rq[':question/answer-fields']):
   vals=[scalar(a[':answer/value']) if base=='q-167648' else vector(a[':answer/value']) for a in f[':answer-field/choices']]
   assert all(not equal(a,b) for i,a in enumerate(vals) for b in vals[:i]),'Every original pair'
   indices=[i for i,z in enumerate(vals) if equal(z,want)];assert len(indices)==1
   if ':answer-field/correct' in f:assert f[':answer-field/choices'][indices[0]][':answer/id']==f[':answer-field/correct'][1],'Captured designation mathematics'
   if ':answer-field/correct' not in f:inferred_keys.append({'source_id':base,'field_index':fi,'answer':f[':answer-field/choices'][indices[0]][':answer/value'],'basis':'Independent printed-surface partials and ordered cross; not source designation evidence'})
  # Native fixtures include only genuinely captured keyed fields. No missing ref
  # is fabricated; duplicate legacy field remains in the public raw replay.
  fixture=copy.deepcopy(r);fixture['question'][':question/answer-fields']=[f for f in rq[':question/answer-fields'] if ':answer-field/correct' in f]
  checks=[]
  for fi,f in enumerate(fixture['question'][':question/answer-fields']):
   for a in f[':answer-field/choices']:
    if f[':answer-field/type'].endswith('/radio'):checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Captured keyed source choice in read-only fixture'})
    else:checks.extend([{'field_index':fi,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Captured norm scalar'},{'field_index':fi,'submitted':r'\sqrt{64x^6+4x^4}','expected':'unresolved','purpose':'Equivalent source norm under real x'},{'field_index':fi,'submitted':'0','expected':'rejected','purpose':'Wrong source norm scalar'}])
  if checks:engine.append({'label':'keyed-original:'+base,'record':fixture,'checks':checks})
  source_cases.append({'source_id':base,'template':base,'level':'easy','parameters':p,'bank_profile':'observed:'+base,'evidence_only':True})
  replays.append({'source_id':base,'prompt_exact':True,'solution_exact_or_absence_parity':True,'fields':len(rq[':question/answer-fields']),'values':sum(len(f[':answer-field/choices']) for f in rq[':question/answer-fields']),'correct_presence_parity':True,'eligible_for_learning':False})
  # Every raw bank is exercised through public API at changed parameters and
  # compared against an independent diagonal transform of the whole source vector.
  pp={'a':2,'b':3,'c':3 if base=='q-167648' else 2}
  raw=g.generate('easy',template=base,parameters=pp,profile='observed:'+base);review.append(raw)
  if base!='q-167648':
   scale=sp.diag(pp['b']*pp['c'],pp['a']*pp['c'],pp['a']*pp['b'])
   for f,sf in zip(raw['question'][':question/answer-fields'],q[':question/answer-fields']):
    for a,sa in zip(f[':answer-field/choices'],sf[':answer-field/choices']):assert equal(vector(a[':answer/value']),scale*vector(sa[':answer/value']))
  for pp in ({'a':1,'b':1,'c':1},{'a':2,'b':3,'c':3 if base=='q-167648' else 2}):
   r=g.generate('easy',template=base,parameters=pp);verify(r);review.append(r);normal.append(r)
 # Every family, level and its representative low/high arithmetic boundary.
 for level in ('moderate','hard'):
  lo,hi={'moderate':(2,4),'hard':(5,8)}[level]
  for base in g.CROSS:
   for p in ({'a':lo,'b':lo,'c':lo},{'a':hi,'b':hi-1,'c':lo}):
    r=g.generate(level,template=level+':'+base,parameters=p);verify(r);normal.append(r);review.append(r)
 # Exercise full meaningful bounded domains, identity, explicit-bound rejection.
 domain_counts={};fingerprints={}
 for level in ('easy','moderate','hard'):
  lo,hi={'easy':(1,3),'moderate':(2,4),'hard':(5,8)}[level];fps=set();count=0
  for template,l in g.TEMPLATES.items():
   if l!=level:continue
   base=template.split(':')[-1]
   for a,b,c in itertools.product(range(lo,hi+1),repeat=3):
    if base=='q-167648' and b!=c:continue
    r=g.generate(level,template=template,parameters={'a':a,'b':b,'c':c});verify(r);count+=1;fps.add(r['generation']['mathematical_fingerprint'])
  domain_counts[level]=count;fingerprints[level]=len(fps);assert len(fps)==count,(level,count,len(fps))
  for template,l in g.TEMPLATES.items():
   if l==level:
    try:g.generate(level,template=template,parameters={'a':lo-1,'b':lo,'c':lo})
    except ValueError:pass
    else:raise AssertionError('Bound not enforced')
 # Seed/order cannot create identity; changed complete bank is part of identity.
 for r in normal:
  m=r['generation'];s=g.generate(g.TEMPLATES[m['template']],seed=777,template=m['template'],parameters=m['parameters'],profile=m['profile'])
  assert r['question'][':question/id']==s['question'][':question/id']
  f=r['question'][':question/answer-fields'][0]
  checks=[]
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual field-owned complete choice'} for a in f[':answer-field/choices']]
  else:
   a,b=m['parameters']['a'],m['parameters']['b'];canonical=f[':answer-field/choices'][0][':answer/value']
   checks=[{'submitted':canonical,'expected':'accepted','purpose':'Canonical scalar norm'},
    {'submitted':rf'\sqrt{{{64*b**4}x^6+{4*a*a*b*b}x^4}}','expected':'unresolved','purpose':'Real equivalent uncollected norm'},
    {'submitted':rf'{2*b}x^2\sqrt{{{a*a}+{16*b*b}x^2}}','expected':'accepted','purpose':'Reordered equivalent scalar norm'},
    {'submitted':'0','expected':'rejected','purpose':'Wrong scalar entry'}]
  engine.append({'label':m['template']+':'+str(m['parameters']),'record':r,'checks':checks})
 # Fail closed against stale stages, missing signs, control bytes and content aliases.
 original=g.generate('easy',template='q-109912',parameters={'a':2,'b':3,'c':2});verify(original)
 for mut in ('cofactor','derivative','control','cofactor-structure'):
  r=copy.deepcopy(original)
  if mut=='cofactor':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(r',\,-|\begin{aligned}',r',\,|\begin{aligned}',1)
  elif mut=='cofactor-structure':
   text=r['question'][':question/worked-solution'];m=next(z for z in re.finditer('⟨[^⟨⟩]*⟩',text) if '\\begin{aligned}' in z[0]);r['question'][':question/worked-solution']=text[:m.start()]+g.vec(verify(original))+text[m.end():]
  elif mut=='derivative':r['question'][':question/worked-solution']=g.generate('easy',template='q-109912',parameters={'a':1,'b':1,'c':1})['question'][':question/worked-solution']
  else:r['question'][':question/problem']+='\f'
  try:verify(r)
  except AssertionError:pass
  else:raise AssertionError('Mutation not caught:'+mut)
 # Remove an operative norm stage while retaining algebraic equality and row count.
 n=g.generate('easy',template='q-167648',parameters={'a':2,'b':3,'c':3});verify(n)
 m=copy.deepcopy(n);text=m['question'][':question/worked-solution'];old=text.split(r' & =')[3].split(r' \\')[0]
 replacement=rf'\sqrt{{{64*3**4}{{x}}^{{6}}+{4*2**2*3**2}{{x}}^{{4}}}}'
 m['question'][':question/worked-solution']=text.replace(old,replacement,1)
 try:verify(m)
 except AssertionError:pass
 else:raise AssertionError('Algebraically equal norm stage omission escaped')
 default={l:set() for l in ('easy','moderate','hard')}
 for l in default:
  for seed in range(100):
   r=g.generate(l,seed);default[l].add(r['generation']['template'])
  assert default[l]=={t for t,ll in g.TEMPLATES.items() if ll==l}
 (HERE/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False))
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 report={'status':'pass','review_status':'awaiting parent independent QA','basis':g.SNAPSHOT['basis'],'lineage':g.SNAPSHOT['lineage'],'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'original_questions':'7/7','original_fields':'8/8','complete_banks':'8/8 (7 radio, 1 blank)','source_values':f'{matched}/36','original_correct_designations':f'{designation}/6; 2 absent retained','known_source_distractors':f'{distractors}/20; 10 unkeyed radio options accounted as unkeyed values','original_full_solutions':'6/6; 1 absence retained','raw_prompt_whitespace':'7/7 exact','inferred_original_keys_not_counted_as_source_designations':inferred_keys,'source_replays':replays,'bounded_domain_instances':domain_counts,'meaningful_tasks':fingerprints,'every_pair_whole_vector_bank_checked':True,'displayed_math_and_stages_independently_checked':True,'mutations_rejected':['middle-cofactor sign deletion','stale changed-parameter derivative solution','C0 formfeed','algebraically equal replacement of cofactor minors','algebraically equal replacement of norm trig-factor stage'],'default_family_coverage':{l:sorted(z) for l,z in default.items()},'native':json.loads((HERE/'engine-report.json').read_text()),'unresolved':['Opaque historical distractor intent remains unresolved; public complete parameterized evidence profiles are ineligible for learning.','q-105607 original lacks difficulty, correct reference and solution; normal level/key/solution are authored.','q-105606 duplicate legacy field has no key; normal output has one supported selection field.','Native scalar grader cannot establish the equivalent uncollected sqrt(64x^6+4x^4) norm; canonical/reordered factored forms pass and wrong scalars fail.','Native local lesson archive has no q-167648 ID; actual captured full solution supplies surface, derivatives and computed product; no answer-based reconstruction.','Calculator policy unknown in database snapshot. Missing moderate/hard labels use conservative arithmetic coefficient bands, not recovered progression.']}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');(HERE/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 pieces=[]
 for r in review:
  m=r['generation'];label=('ORIGINAL/CHANGED RAW EVIDENCE, not learner eligible' if m['evidence_only'] else 'NORMAL AUTHORED/SUPPORTED VARIANT')
  pieces.append('## '+label+' — '+m['template']+' — '+str(m['parameters'])+'\n\n'+g.markdown(r))
 (HERE/'review.md').write_text('\n\n---\n\n'.join(pieces)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('native','source_replays')},indent=2))
if __name__=='__main__':main()
