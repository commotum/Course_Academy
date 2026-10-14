#!/usr/bin/env python3
"""Independent displayed-equation, component, stage, fidelity and native QA."""
import copy,hashlib,importlib.util,itertools,json,pathlib,re,subprocess,sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=pathlib.Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('hyperbolic',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z,t=sp.symbols('x y z t',real=True);env=dict(zip('xyzt',[x,y,z,t]));env.update({k:getattr(sp,k) for k in ['sec','tan','sin','cos','csc','sqrt']})
TRANS=standard_transformations+(implicit_multiplication_application,)

def parse(s):
 s=g.normalize(s).strip().rstrip('.').replace(r'\left','').replace(r'\right','')
 s=re.sub(r'\\(sec|tan|sin|cos|csc)\{\(t\s*\)\}',r'\\\1 t',s)
 def group(s,start):
  assert s[start]=='{',s
  depth=1;i=start+1
  while depth:
   depth+=(s[i]=='{')-(s[i]=='}');i+=1
  return s[start+1:i-1],i
 while '\\frac' in s:
  start=s.index('\\frac');a,i=group(s,start+5);b,j=group(s,i)
  s=s[:start]+'(('+str(parse(a))+')/('+str(parse(b))+'))'+s[j:]
 while '\\sqrt' in s:
  start=s.index('\\sqrt');a,i=group(s,start+5);s=s[:start]+'sqrt('+str(parse(a))+')'+s[i:]
 s=re.sub(r'\\(sec|tan|sin|cos|csc)\^\{?2\}?\s*t',r'\1(t)**2',s)
 s=re.sub(r'\\(sec|tan|sin|cos|csc)\s*\{?t\}?',r'\1(t)',s)
 s=s.replace('{','(').replace('}',')').replace('^','**').replace(r'\,','').replace(' ','')
 return parse_expr(s,local_dict=env,transformations=TRANS)


def displayed_task(r):
 q=r['question'];text=q[':question/problem']
 assert all(ord(c)>=32 or c in '\n\t' for c in text+q[':question/worked-solution'])
 eq=re.search(r'Cartesian coordinates as \$([^$]+)\$',text).group(1)
 lhs,rhs=eq.split('=');F=parse(lhs)-parse(rhs)
 sheet=re.search(r'for \$([xyz])\s*\\ge\s*(\d+)',text)
 assert sheet
 axis=env[sheet[1]];bound=sp.Integer(sheet[2])
 promptvec=re.search(r'f\(([^)]*)\)=⟨([^⟩]+)⟩',text.replace(' ','')).group(2).replace(r'\,','').split(',')
 assert len(promptvec)==3
 pos=next(i for i,v in enumerate(promptvec) if '_____' in v)
 ordinal=re.search(r'What is the (first|second|third) component',text).group(1)
 assert pos==g.ORD.index(ordinal)
 known={env[g.AXES[i]]:parse(v) for i,v in enumerate(promptvec) if i!=pos}
 assert len(known)==2
 return F,axis,bound,env[g.AXES[pos]],known


def good(expr,F,axis,bound,target,known):
 sub={**known,target:expr};res=sp.trigsimp(F.subs(sub,simultaneous=True))
 if res!=0:return False
 secvalue=sub[axis]
 if sp.simplify(secvalue.subs(t,0)-bound)!=0:return False
 # The exact identity plus pole-free sec/tan on (-pi/2,pi/2), and
 # tan's range R, establishes sheet and full coverage in these families.
 tanaxis=next(a for a in [x,y,z] if a!=axis and sub[a].has(t))
 ratio=sp.simplify(sub[tanaxis]/sp.tan(t))
 return bool(ratio.is_real and ratio!=0 and sp.simplify(secvalue/sp.sec(t))==bound)


def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];F,axis,bound,target,known=displayed_task(r)
 f=q[':question/answer-fields'][0];vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(vals)==5
 validity=[good(v,F,axis,bound,target,known) for v in vals]
 assert sum(validity)==1,(r['generation']['template'],r['generation']['parameters'],validity,F,known)
 for i,j in itertools.combinations(range(5),2):
  assert sp.simplify(vals[i]-vals[j])!=0
  # Parameter orientation is not assessed: two ±tan options that each
  # describe the full same sheet would be ambiguous even with unequal text.
  assert not(validity[i] and validity[j])
 correct=next(a for a,v in zip(f[':answer-field/choices'],validity) if v)
 assert f[':answer-field/correct']==[':answer/id',correct[':answer/id']]
 expr=parse(correct[':answer/value']);sub={**known,target:expr}
 solution=q[':question/worked-solution']
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
 assert len(blocks)==2
 arithmetic=blocks[0];rows=arithmetic.split('\\\\')
 expected=None
 name=r['generation']['template']
 assert len(rows)==(3 if name in ['equal_tan','supplied_base'] else 4)
 if name in ['equal_tan','supplied_base','equal_sec','offplane_tan']:
  assert '(' in rows[-2] and r'\sec^{2}' in rows[-2] and r'\tan^{2}' in rows[-2], 'Missing grouped identity stage'
 if name in ['radical_tan','unrated_tan','unit_sec']:
  assert r'\frac' in rows[0] and r'\frac' in rows[1], 'Missing substituted/evaluated fraction stages'
 for row in rows:
  sides=row.strip().replace('&','').split('=')
  if len(sides)==2 and sides[0].strip():expected=sp.trigsimp(parse(sides[0]).subs(sub,simultaneous=True))
  assert expected is not None
  value=sp.trigsimp(parse(sides[-1]).subs(sub,simultaneous=True))
  assert sp.simplify(value-expected)==0,(row,expected,value)
 vecs=re.findall(r'⟨([^⟩]+)⟩',blocks[1]);assert len(vecs)==2
 last=vecs[-1].replace(r'\,','').split(',')
 assert len(last)==3
 for a,v in zip([x,y,z],last):assert sp.simplify(parse(v)-sub[a])==0
 conclusion=re.search(r'Therefore, the (first|second|third) component of \$f\$ is \$([^$]+)\$',solution)
 assert conclusion and conclusion[1]==g.ORD[g.AXES.index(str(target))]
 assert sp.simplify(parse(conclusion[2])-expr)==0
 # Check actual f arguments: one t and exactly the free coordinate, with
 # the same order in the prompt and both source-style solution appearances.
 args=re.search(r'f\(([^)]*)\)',q[':question/problem']).group(1).replace(' ','')
 assert set(args.split(','))=={'t',str(next(a for a in [x,y,z] if sub[a]==a))}
 assert all(a.replace(' ','')==args for a in re.findall(r'f\(([^)]*)\)',solution))
 return len(rows)


def main():
 cases=[];fidelity=dict(normal_notation_normalized_solutions=0,questions=0,prompts=0,solutions=0,banks=0,values=0,designations=0,absent_designations=0,absent_ratings=0,absent_solutions=0)
 for name,s in g.SPECS.items():
  if name=='supplied_base':continue
  p=dict(a=s['a'],b2=s['b2'],axes='xyz');case=dict(source_id=s['source'],level=s['level'],template=name,parameters=p,bank_profile='raw_'+s['source']);cases.append(case)
  r=g.generate(s['level'],template=name,parameters=p,profile=case['bank_profile']);q=r['question'];old=g.SOURCES[s['source']]
  assert q[':question/problem']==old[':question/problem'];fidelity['prompts']+=1
  for key,count in [(':question/worked-solution','solutions'),(':question/difficulty',None)]:
   assert (key in q)==(key in old)
   if key in old and count:assert q[key]==old[key];fidelity[count]+=1
  fidelity['absent_solutions']+=(':question/worked-solution' not in old);fidelity['absent_ratings']+=(':question/difficulty' not in old)
  for f,of in zip(q[':question/answer-fields'],old[':question/answer-fields'],strict=True):
   assert f[':answer-field/key']==of[':answer-field/key'];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);fidelity['banks']+=1;fidelity['values']+=5
   assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:
    value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert value==of[':answer-field/correct'][':answer/value'];fidelity['designations']+=1
   else:fidelity['absent_designations']+=1
  if ':question/worked-solution' in old:
   normal=g.generate(s['level'],template=name,parameters=p)
   assert normal['question'][':question/worked-solution']==g.normalize(old[':question/worked-solution'],True)
   fidelity['normal_notation_normalized_solutions']+=1
  fidelity['questions']+=1
 (D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 records=[];rows=0;slots={};tasks={};checks=0
 for name,s in g.SPECS.items():
  seen=set();fingerprints=set()
  # Every role permutation, both arithmetic boundaries and source parameters.
  ps=[dict(a=s['a'],b2=s['b2'],axes=a) for a in ['xyz','xzy','yxz','yzx','zxy','zyx']]
  ps += [g.sample(name,__import__('random').Random(i)) for i in range(35)]
  for p in ps:
   r=g.generate(s['level'],template=name,parameters=p);rows+=check(r);checks+=1
   f=r['generation'];seen.add(p['axes']);fingerprints.add(f['parameter_fingerprint'])
   r2=g.generate(s['level'],seed=23,template=name,parameters=p)
   assert r['question'][':question/id']==r2['question'][':question/id']
   records.append(r)
  slots[name]=sorted(seen);tasks[name]=len(fingerprints)
  bad=dict(ps[0],a=10)
  try:g.generate(s['level'],template=name,parameters=bad);raise AssertionError('Missing explicit workload guard')
  except ValueError:pass
 # Displayed mutation regressions independently reject mathematically wrong
 # teaching stages, stale conclusions and forbidden invisible control bytes.
 r=g.generate_moderate(template='radical_tan',parameters={'a':3,'b2':2,'axes':'xyz'})
 for mutate in [lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('=1.', '=2.')),lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('Therefore, the second','Therefore, the first')),lambda q:q.__setitem__(':question/problem',q[':question/problem']+'\x0c')]:
  bad=copy.deepcopy(r);mutate(bad['question'])
  try:check(bad);raise RuntimeError('Mutation was accepted')
  except AssertionError:pass
 # Orientation equivalence is checked under the exact actual source criterion.
 F,axis,bound,target,known=displayed_task(r)
 assert good(sp.sqrt(2)*sp.tan(t),F,axis,bound,target,known)
 assert good(-sp.sqrt(2)*sp.tan(t),F,axis,bound,target,known)
 fixtures=[]
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0]
  fixtures.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'All owned choices after independent mathematical checks'} for a in f[':answer-field/choices']]})
 (D/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine.json')],check=True)
 engine=json.loads((D/'engine.json').read_text())
 report={'passed':True,'source_fidelity':fidelity,'normal_instances':checks,'displayed_arithmetic_rows':rows,'role_slots':slots,'sampled_meaningful_tasks':tasks,'native_grading':{k:engine[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'orientation_regressions':2,'mutation_regressions':3,'source_anomalies':{'pole_options_evidence_only':['q-103998','q-164387','q-164439','q-164457'],'doubled_answer_backslashes':'35/35 captured answer strings; repaired only in normal output','q-103998':'Duplicate selection field; legacy has no key','q-164387':'Unrated; key and solution absent. Normal completion inferred/authored.'},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'independent_parent_qa':'required'}
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
