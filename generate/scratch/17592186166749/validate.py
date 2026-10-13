#!/usr/bin/env python3
"""Fail on actual-display mathematics, complete fidelity, native grading or scope."""
import importlib.util,json,re,sys,subprocess,hashlib,uuid,itertools
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
from math_reader import read,x,y,S as s,T as t
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('two_independent_generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
A,B,C,D,E=sp.symbols('A B C D E')
def write(n,v):(ROOT/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def proof(a,b,context):
 d=sp.cancel(sp.expand(a-b))
 if d==0:return
 # Canonicalize polynomial trig arguments independently; use one dummy per
 # primitive argument, preserving integer double-angle multipliers. This lets
 # CAS prove the source identity without expanding sums of unrelated angles.
 lookup={}
 def trig_atom(z):
  content,primitive=sp.Poly(z.args[0],s,t).primitive()
  key=sp.srepr(primitive.as_expr())
  if key not in lookup:lookup[key]=sp.Dummy(real=True)
  return z.func(content*lookup[key])
 normalized=d.replace(lambda z:z.func in (sp.sin,sp.cos),trig_atom)
 if sp.simplify(normalized)!=0:raise AssertionError((context,a,b))
def formatting(z):
 assert z.count('$')%2==0 and z.count('$$')%2==0,z
 assert z.count('{')==z.count('}'),z
 assert '--' not in z and '+-' not in z,z
 assert r'\u2061' not in z
 assert all(c not in z for c in ('\\\\frac','\\\\operatorname'))
def printed(r):
 p=r['question'][':question/problem'];m=re.search(r'f\(x,y\)\s*=\s*(.*?),\$',p);maps=re.search(r'where \$x\s*=\s*(.*?)\$ and \$y\s*=\s*(.*?)\.\$',p);var=re.search(r'∂f\}\{∂([st])\}',p)
 assert m and maps and var,p
 return read(m[1]),read(maps[1]),read(maps[2]),s if var[1]=='s' else t

def rows(sol,v):
 labels={g.derivative('f','x'):'A',g.derivative('f','y'):'B',g.derivative('x',str(v)):'C',g.derivative('y',str(v)):'D',g.derivative('f',str(v)):'E'}
 parsed=[]
 for bi,z in enumerate(re.findall(r'\$\$(.*?)\$\$',sol,flags=re.S)):
  for a,b in labels.items():z=z.replace(a,b)
  z=z.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');previous=None
  for row in z.split(r'\\'):
   for segment in row.split(r'\,'):
    sides=[a.strip().rstrip(',. ') for a in segment.strip().split('=')]
    assert len(sides)>=2,(bi,segment)
    if not sides[0]:sides[0]=previous
    previous=sides[0];parsed.append((bi,sides))
 return parsed

def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];m=r['generation'];F,X,Y,v=printed(r)
 assert F.free_symbols<={x,y} and X.free_symbols<={s,t} and Y.free_symbols<={s,t}
 assert (X.free_symbols|Y.free_symbols)=={s,t}
 aa=sp.diff(F,x).subs({x:X,y:Y},simultaneous=True);bb=sp.diff(F,y).subs({x:X,y:Y},simultaneous=True);cc=sp.diff(X,v);dd=sp.diff(Y,v);ee=sp.diff(F.subs({x:X,y:Y},simultaneous=True),v)
 eqs=0;formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
 rr=rows(q[':question/worked-solution'],v);assert {b for b,_ in rr}=={0,1,2,3,4}
 for bi,ss in rr:
  mapping={A:sp.diff(F,x),B:sp.diff(F,y),C:cc,D:dd,E:ee} if bi==1 else {A:aa,B:bb,C:cc,D:dd,E:ee}
  vv=[read(z).subs(mapping) for z in ss]
  for w in vv[1:]:proof(vv[0],w,(m['template'],bi,ss));eqs+=1
 f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];assert len(cs)==5;vs=[read(a[':answer/value']) for a in cs]
 for a in cs:formatting(a[':answer/value']);uuid.UUID(a[':answer/id'])
 for i,z in enumerate(vs):
  if cs[i][':answer/id']==f[':answer-field/correct'][1]:proof(z,ee,('correct answer',m['template']))
  for w in vs[:i]:assert not g.equal(z,w),('ambiguous bank',m['template'])
 assert len([a for a in cs if a[':answer/id']==f[':answer-field/correct'][1]])==1
 if not m['evidence_only']:
  U=aa*cc;V=bb*dd;other=s if v==t else t
  if m['template']=='zero_exponential':expected=[ee,sp.diff(F.subs({x:X,y:Y},simultaneous=True),other),bb,bb*sp.diff(Y,other),Y*dd]
  elif m['template']=='affine_two_maps':expected=[ee,sp.diff(F.subs({x:X,y:Y},simultaneous=True),other),U-V,U,V]
  else:expected=[ee,U,V,U-V,aa+bb]
  remaining=set(range(5))
  for target in expected:
   matches=[i for i in remaining if g.equal(vs[i],target)];assert len(matches)==1,(m['template'],'wrong recipe',target)
   proof(vs[matches[0]],target,('actual bank method recipe',m['template']));remaining.remove(matches[0])
 uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id']);assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 return eqs

def engine(r,label):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native owned radio selection; actual displayed mathematics checked independently'} for a in f[':answer-field/choices']]}
def main():
 review=[];native=[];cases=[];fidelity=[];eqs=0;instances=0;fingerprints={l:set() for l in ('easy','moderate','hard')}
 for name,sid in g.FAMILIES.items():
  print('Validating '+name,flush=True);level=g.TEMPLATES[name];q=g.SOURCES[sid];r=g.generate(level,template=name,parameters={'h':0,'k':0},profile='observed:'+sid);eqs+=check(r);instances+=1
  assert r['question'][':question/problem']==q[':question/problem'];assert r['question'][':question/worked-solution']==q[':question/worked-solution']
  assert set(r['question'])-{':question/id'}==set(q)-{':question/id',':db/id',':question/math-academy-id'}
  f=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
  assert set(rf)-{':answer-field/id'}==set(f)-{':answer-field/id',':db/id'}
  assert rf[':answer-field/key']==f[':answer-field/key'];assert rf[':answer-field/type']==f[':answer-field/type'][':db/ident']
  expect={(a[':answer/value'],a[':answer/id']==f[':answer-field/correct'][':answer/id']) for a in f[':answer-field/choices']};actual={(a[':answer/value'],a[':answer/id']==rf[':answer-field/correct'][1]) for a in rf[':answer-field/choices']};assert expect==actual
  # Source bytes, not serialized display: formal command has one slash.
  assert '\\\\frac' not in q[':question/worked-solution'];assert '\\\\operatorname' not in q[':question/worked-solution']
  cases.append({'source_id':sid,'template':name,'parameters':{'h':0,'k':0},'bank_profile':'observed:'+sid});fidelity.append({'source_id':sid,'complete_bank_exact':True,'values_matched':5,'correct_designation_matched':True,'prompt_exact':True,'worked_solution_exact':True,'attribute_presence_parity':True,'evidence_only':True})
  review.append({'label':'Original complete raw replay '+sid,'record':r});native.append(engine(r,'original/'+sid))
  for h,k in itertools.product(range(-2,3),repeat=2):
   p={'h':h,'k':k}
   for profile in ('operations:'+name,'observed:'+sid):
    rr=g.generate(level,template=name,parameters=p,profile=profile);eqs+=check(rr);instances+=1
    # Shared source prose/structural rows remain unchanged: only expressions vary.
    sol=rr['question'][':question/worked-solution'];original=q[':question/worked-solution']
    mask=lambda z:re.sub(r'\$\$.*?\$\$','<BLOCK>',z,flags=re.S)
    assert mask(sol)==mask(original)
    assert [len(ss) for _,ss in rows(sol,printed(rr)[3])]==[len(ss) for _,ss in rows(original,printed(r)[3])]
    if not rr['generation']['evidence_only']:fingerprints[level].add(rr['generation']['mathematical_fingerprint'])
    rr2=g.generate(level,seed=91,template=name,parameters=p,profile=profile);assert rr['question'][':question/id']==rr2['question'][':question/id']
   if (h,k) in ((-2,1),(1,-2)):
    review.append({'label':'Generated source-shaped normal '+name+' '+str(p),'record':rr if not rr['generation']['evidence_only'] else g.generate(level,template=name,parameters=p)});native.append(engine(review[-1]['record'],'normal/'+name+'/'+str(p)))
  normal=g.generate(level,template=name,parameters={'h':0,'k':0});assert normal['question'][':question/worked-solution']==q[':question/worked-solution']
 for seed in range(120):
  rr=g.generate_easy(seed);eqs+=check(rr);instances+=1;fingerprints['easy'].add(rr['generation']['mathematical_fingerprint'])
  if seed in (0,1):review.append({'label':'Authored missing-level easy '+str(seed),'record':rr});native.append(engine(rr,'easy/'+str(seed)))
 for level in ('moderate','hard'):
  reached={g.generate(level,seed=z)['generation']['template'] for z in range(100)}
  assert reached=={n for n,l in g.TEMPLATES.items() if l==level}
  for z in range(30):rr=g.generate(level,seed=z);eqs+=check(rr);instances+=1
 for level in ('moderate','hard'):
  name=next(n for n,l in g.TEMPLATES.items() if l==level)
  for p in ({'h':3,'k':0},{'h':0,'k':-3},{'h':True,'k':0},{'h':0,'k':0,'unused':1}):
   try:g.generate(level,template=name,parameters=p)
   except ValueError:pass
   else:raise AssertionError('Invalid explicit parameters accepted')
 for p in ({'a':0,'b':1,'c':1,'d':1,'e':1,'g':1,'variable':'s'},{'a':4,'b':1,'c':1,'d':1,'e':1,'g':1,'variable':'s'}):
  try:g.generate_easy(parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid easy workload accepted')
 write('source-cases.json',cases);write('source-fidelity.json',fidelity);write('review.json',review);write('engine-input.json',native)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
 report=json.loads((ROOT/'engine-validation.json').read_text())
 easy_catalog=set();easy_valid_presentations=0
 for aa,bb,cc,dd,ee,gg in itertools.product((-3,-2,-1,1,2,3),repeat=6):
  for v in ('s','t'):
   U,V=(aa*cc,bb*ee) if v=='s' else (aa*dd,bb*gg)
   other=aa*dd+bb*gg if v=='s' else aa*cc+bb*ee
   if len({U+V,other,U-V,U,V})!=5:continue
   easy_valid_presentations+=1
   easy_catalog.add((aa*cc+bb*ee,aa*dd+bb*gg,v))
 write('validation.json',{'passed':True,'source_basis':1356,'source_questions':10,'source_levels':{'moderate':5,'hard':5,'easy':0},'raw_complete_banks_exact':10,'raw_answer_values_exact':50,'raw_prompt_exact':10,'raw_solution_exact':10,'raw_correct_designations_matched':10,'attribute_presence_parity':10,'normal_source_chains_exact_at_original_parameters':10,'displayed_stage_equalities_checked':eqs,'mathematically_checked_instances':instances,'finite_observed_parameter_pairs_per_family':25,'meaningful_unique_observed_tasks':{l:len(fingerprints[l]) for l in ('moderate','hard')},'sampled_unique_easy_tasks':len(fingerprints['easy']),'exhaustive_easy_reduced_affine_tasks':len(easy_catalog),'exhaustive_easy_valid_coefficient_presentations':easy_valid_presentations,'native_report':'engine-validation.json','native_checks':len(native)*5,'review_records':len(review),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':g.package_version('matplotlib')},'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((ROOT/'source.json').read_bytes()).hexdigest(),'grader_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'unresolved_limits':['Source distractor intentions are not recovered; complete raw translated banks are evidence-only.','Authored easy difficulty is grounded in the held-coordinate tutorial, not an observed easy rating.','No typed-answer engine equivalence applies: all source and authored fields are radio.','Input translations form a deliberately bounded same-workload family; no claim of recovered original parameter samplers.'],'database_writes':0})
 lines=['# Review: two independent variables','Original replay banks are evidence-only. Normal variants retain every source solution stage and use authored complete method banks. Easy variants are explicitly authored.']
 for item in review:lines+=['## '+item['label'],g.markdown(item['record'])]
 (ROOT/'review.md').write_text('\n\n'.join(lines)+'\n')
 print('PASS: complete source replay, all displayed stages, all bounded source-shaped inputs, and native grading.')
if __name__=='__main__':main()
