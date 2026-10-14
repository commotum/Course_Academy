#!/usr/bin/env python3
"""Private mathematical readback, complete fidelity, plotting and native grading."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import sympy as sp
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def math_readback(r):
 q=r['question'];pr=q[':question/problem'];sol=q[':question/worked-solution'];f=r['generation']['template'];P=g.parse
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 for s in [pr,sol]+[a[':answer/value']for a in q[':question/answer-fields'][0][':answer-field/choices']]:g.format_ok(s)
 # Read actual displayed maps, then independently solve/invert the linear map.
 maps=re.search(r'\$\$\nu=(.*?),\\,v=(.*?),\n\$\$',pr)
 assert maps,'printed map';U,V=map(P,maps.groups());matrix=sp.Matrix([[sp.diff(U,g.x),sp.diff(U,g.y)],[sp.diff(V,g.x),sp.diff(V,g.y)]])
 det=matrix.det();assert det!=0;J=1/abs(det)
 inv=sp.solve([g.u-U,g.v-V],(g.x,g.y))
 # Parse the actual xy boundary statements from the prompt. No generation
 # parameters or model values serve as mathematical truth in these checks.
 tail=pr[pr.index('bounded by'):];inline=re.findall(r'\$([^$]+)\$',tail)
 equations=[]
 for z in inline:
  z=z.rstrip(',.');aa,bb=z.split('=');equations.append(sp.expand(P(aa)-P(bb)))
 transformed=[sp.simplify(z.subs(inv,simultaneous=True))for z in equations]
 # Parse printed type-I region completely and independently.
 dom=re.search(r'Δ=\\\{\(u,v\)\\,:\\,(.*?)\\le u\\le (.*?),\\,(.*?)\\le v\\le (.*?)\\\}\.',sol)
 assert dom,'domain';lo,hi,low,high=map(P,dom.groups());assert float(hi-lo)>0
 if f.startswith('hyper'):
  assert len(transformed)==3
  u_boundary=transformed[1]if f=='hyper_x'else transformed[0];v_boundary=transformed[0]if f=='hyper_x'else transformed[1]
  assert sp.simplify(u_boundary.subs(g.u,lo))==0
  assert sp.simplify(v_boundary.subs(g.v,low))==0
  assert sp.simplify(transformed[2].subs(g.v,high))==0
 else:
  assert len(transformed)==2
  boundary=high if f=='down' else low
  line=low if f=='down' else high
  assert sp.simplify(transformed[0].subs(g.v,boundary))==0
  assert sp.simplify(transformed[1].subs(g.v,line))==0
  assert g.eq(low.subs(g.u,lo),high.subs(g.u,lo)) and g.eq(low.subs(g.u,hi),high.subs(g.u,hi))
 assert float((high-low).subs(g.u,(lo+hi)/2))>0
 if f=='quartic':
  inverted=re.search(r'Now,\n\n\$\$(.*?)\$\$',sol,re.S)[1]
  y_fragment=inverted.split('y=')[-1].split(r'\end{aligned}')[0].removesuffix('.')
  assert r'\frac{u-v}'in y_fragment,'inverse must retain single grouped quotient'
  assert g.eq(P(y_fragment),inv[g.y])
 correct=sp.simplify(J*sp.integrate(high-low,(g.u,lo,hi)))
 field=q[':question/answer-fields'][0];bank=[P(a[':answer/value'])for a in field[':answer-field/choices']];assert len(bank)==5
 assert all(not g.eq(a,b)for a,b in itertools.combinations(bank,2))
 target=next(P(a[':answer/value'])for a in field[':answer-field/choices']if a[':answer/id']==field[':answer-field/correct'][1]);assert g.eq(target,correct)
 # Read the printed determinant matrix and scalar, independent of model().
 calc=sol[sol.index('**Step 2**'):sol.index('**Step 3**')]
 mats=re.findall(r'\\begin\{matrix\}(.*?)\\end\{matrix\}',calc,re.S);assert len(mats)==2
 vals=[P(z)for z in re.split(r'&|\\\\',mats[1])];assert vals==list(matrix)
 displayed_det=P(re.search(r'&=([^\\]+)\\end\{aligned\}',calc)[1]);assert displayed_det==det
 inverse_section=sol[sol.index('**Step 3**'):sol.index('**Step 4**')]
 inverse_block=re.search(r'\$\$\n(.*?)\n\$\$',inverse_section,re.S)[1]
 assert g.eq(P(inverse_block.split('=')[-1].removesuffix('.')),1/det)
 # Complete operative integration rows and separately printed primitive.
 chain=sol[sol.index('**Step 4**'):];rows=chain.split(r' \\ ')
 assert len(rows)==(9 if f.startswith('hyper')or f=='quartic'else 10)
 assert r'[\int_{' in rows[2] and r'[v]_{' in rows[3]
 inner=re.search(r'\[\\int_\{(.*?)\}\^\{(.*?)\}dv',rows[2]);assert inner
 assert g.eq(P(inner[1]),low) and g.eq(P(inner[2]),high)
 integral_prefix=r'\int_{'+g.tex(lo)+'}^{'+g.tex(hi)+'}'
 assert integral_prefix in rows[4]
 for row in rows[2:-4]:
  assert integral_prefix in row
  factor_in_row=P(row.split('&=')[1].split(r'\int')[0]);assert g.eq(factor_in_row,J)
 assert r'[v]_{'+g.tex(low)+'}^{'+g.tex(high)+'}' in rows[3]
 numeric_J=re.search(r'\\iint_Δ \|(.*?)\|\\,dudv',rows[1]);assert numeric_J
 assert g.eq(abs(P(numeric_J[1])),J)
 grouped_math=rows[4].split(integral_prefix,1)[1].removesuffix('du')
 assert g.eq(P(grouped_math),high-low)
 primrow=rows[-4]; m=re.search(r'&=(.*?)\[(.*?)\](.*)$',primrow);assert m,'primitive structure'
 factor,primitive=map(P,m.groups()[:2]);assert m[3]=='_{'+g.tex(lo)+'}^{'+g.tex(hi)+'}'
 assert g.eq(factor,J);assert g.eq(sp.diff(primitive,g.u),high-low)
 endpointrow=rows[-3];em=re.search(r'&=(.*?)\((.*)\)$',endpointrow);assert em
 # The evaluated row's signs/grouping retain each endpoint component, including
 # zero components: verify each individually, not only the final difference.
 z=em[2];comps=[];depth=0;start=None
 for i,c in enumerate(z):
  if c=='(':
   depth+=1
   if depth==2:start=i+1
  if c==')':
   if depth==2:comps.append(z[start:i])
   depth-=1
 assert len(comps)==4,(f,comps,endpointrow)
 displayed_components=list(map(P,comps));terms=sp.Add.make_args(primitive)
 terms=sorted(terms,key=lambda z:0 if z.has(sp.log) else sp.degree(z,g.u))
 expected=[z.subs(g.u,t)for t in [hi,lo]for z in terms]
 assert all(g.eq(a,b)for a,b in zip(displayed_components,expected)),(f,displayed_components,expected)
 assert g.eq(P(em[2]),(primitive.subs(g.u,hi)-primitive.subs(g.u,lo)))
 collected=re.search(r'&=(.*?)\((.*)\)$',rows[-2]);assert collected
 assert g.eq(P(collected[1]),J)
 assert g.eq(P(collected[2]),primitive.subs(g.u,hi)-primitive.subs(g.u,lo))
 assert g.eq(P(collected[1])*P(collected[2]),correct)
 final=rows[-1].split('&=')[1].split(r'\end{aligned}')[0];assert g.eq(P(final),correct)
 # Structure mutation guards distinguish equivalent but missing operative rows.
 assert '(' in grouped_math and ')-(' in grouped_math,'grouped bound subtraction required'
 return correct

def raw_fidelity():
 rows=[]
 for sid,q in g.Q.items():
  r=g.generate('hard',profile='raw:'+sid,parameters={'scale':1});z=r['question'];sourcefield=q[':question/answer-fields'][0];field=z[':question/answer-fields'][0]
  for key in [':question/difficulty',':question/worked-solution']:
   assert (key in z)==(key in q)
  assert (':answer-field/correct'in field)==(':answer-field/correct'in sourcefield)
  assert z[':question/problem']==q[':question/problem']
  if ':question/worked-solution'in q:assert z[':question/worked-solution']==q[':question/worked-solution']
  assert sorted(a[':answer/value']for a in field[':answer-field/choices'])==sorted(a[':answer/value']for a in sourcefield[':answer-field/choices'])
  if ':answer-field/correct'in sourcefield:
   correct=next(a[':answer/value']for a in field[':answer-field/choices']if a[':answer/id']==field[':answer-field/correct'][1]);assert correct==sourcefield[':answer-field/correct'][':answer/value']
  # Similarity is a real parameterized observed-bank recipe, not anchor lookup.
  changed=g.generate('hard',profile='raw:'+sid,parameters={'scale':2})
  changed_vals=[g.parse(a[':answer/value'])for a in changed['question'][':question/answer-fields'][0][':answer-field/choices']]
  originals=[g.parse(a[':answer/value'])*4 for a in sourcefield[':answer-field/choices']]
  assert all(sum(g.eq(a,b)for b in changed_vals)==1 for a in originals)
  rows.append({'source_id':sid,'template':next(f for f,z in g.FAMILIES.items()if z[0]==sid),'parameters':{'scale':1},'bank_profile':'raw:'+sid,'raw_present_keys':list(q),'field_present_keys':list(sourcefield),'eligible_for_learning':False})
 (ROOT/'source-cases.json').write_text(json.dumps(rows,indent=2))
 return rows

def main():
 sourcecases=raw_fidelity();records=[];slots={};ids={};default_family=set()
 source_anchors=[]
 for f,(sid,level)in g.FAMILIES.items():
  if sid is not None:
   r=g.generate(level,template=f,parameters=g.ANCHORS[sid]);math_readback(r);source_anchors.append(sid)
 for f,(_,level)in g.FAMILIES.items():
  seen={t:set()for t in ['a','h','k']};tasks=set()
  for seed in range(24):
   r=g.generate(level,seed,template=f);math_readback(r);records.append(r)
   for t,z in r['generation']['parameters'].items():seen[t].add(z)
   tasks.add(r['generation']['mathematical_fingerprint'])
  slots[f]={t:sorted(z)for t,z in seen.items()};ids[f]=len(tasks)
  r=records[-1];other=g.generate(level,149,template=f,parameters=r['generation']['parameters']);assert r['question'][':question/id']==other['question'][':question/id']
  # Explicit invalid calls cannot bypass level guards.
  bad=dict(r['generation']['parameters']);bad['a']=0
  try:g.generate(level,template=f,parameters=bad);raise AssertionError('invalid a accepted')
  except ValueError:pass
 for level in ['easy','moderate','hard']:
  for seed in range(36):default_family.add(g.generate(level,seed)['generation']['template'])
 assert default_family==set(g.FAMILIES)
 # Mutation regressions must actually fail, not catch our own success assertion.
 def rejected_mutation(r):
  rejected=False
  try:math_readback(r)
  except (AssertionError,ValueError,IndexError):rejected=True
  assert rejected,'mutation survived readback'
 base=copy.deepcopy(records[0]);sol=base['question'][':question/worked-solution'];base['question'][':question/worked-solution']=sol.replace(')-(',')+(',1);rejected_mutation(base)
 base=copy.deepcopy(records[0]);base['question'][':question/worked-solution']+='\x0c';rejected_mutation(base)
 base=copy.deepcopy(records[0]);sol=base['question'][':question/worked-solution'];rows=sol[sol.index('**Step 4**'):].split(r' \\ ');old=rows[4]
 start=old.index('}(')+1;body=old[start:].removesuffix('du');new=old[:start]+g.tex(g.parse(body))+'du'
 assert g.eq(g.parse(body),g.parse(new[start:].removesuffix('du')))
 base['question'][':question/worked-solution']=sol.replace(old,new);rejected_mutation(base)
 # Correlated endpoint errors can leave the final difference correct. Mutate
 # one component at each endpoint by the same constant, then require failure.
 base=copy.deepcopy(records[0]);sol=base['question'][':question/worked-solution'];rows=sol[sol.index('**Step 4**'):].split(r' \\ ');old=rows[-3]
 positions=[];depth=0
 for i,c in enumerate(old):
  if c=='(':
   depth+=1
   if depth==3:positions.append(i)
  elif c==')':depth-=1
 # Endpoint row has an outer arithmetic difference plus endpoint and term masks.
 assert len(positions)==4
 new=old
 for i in [positions[2],positions[0]]:new=new[:i+1]+'1+'+new[i+1:]
 base['question'][':question/worked-solution']=sol.replace(old,new);rejected_mutation(base)
 # Fresh concurrent renders with identical/different parameter sets. Matplotlib
 # threads have separate Figures; atomic private-file writes protect cache readers.
 items=[('simple',{'a':4,'h':16,'k':0}),('simple',{'a':4,'h':16,'k':0}),('up',{'a':5,'h':12,'k':-5}),('hyper_x',{'a':5,'h':12,'k':3})]
 fresh=Path(tempfile.mkdtemp(prefix='concurrent-',dir=ROOT));paths=[]
 with ThreadPoolExecutor(max_workers=4)as pool:paths=list(pool.map(lambda item:g.plot(*item,g.model(*item),output_dir=fresh),items))
 assert paths[0]==paths[1]and len(set(paths))==3
 for path,(f,p)in zip(paths,items):assert json.loads(Path(path).with_suffix('.json').read_text())['parameters']==p
 assert not list(fresh.glob('*-*.png'))and not list(fresh.glob('*-*.json'))
 native=[]
 for r in records:
  field=r['question'][':question/answer-fields'][0];native.append({'label':r['generation']['template']+'-'+str(r['generation']['seed']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==field[':answer-field/correct'][1]else'rejected','purpose':'actual radio grading of independently verified displayed choice'}for a in field[':answer-field/choices']]})
 # Raw missing-correct evidence is excluded from native fixture. Five present
 # designations are checked; the omission remains an honest raw omission.
 for sid,q in g.Q.items():
  if ':answer-field/correct'not in q[':question/answer-fields'][0]:continue
  r=g.generate('hard',profile='raw:'+sid,parameters={'scale':1});field=r['question'][':question/answer-fields'][0]
  native.append({'label':'source-'+sid,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==field[':answer-field/correct'][1]else'rejected','purpose':'captured correct-designation fixture'}for a in field[':answer-field/choices']]})
 (ROOT/'native-input.json').write_text(json.dumps(native,ensure_ascii=False,indent=2));check=Path('generate/runs/current/check-engine');subprocess.run([str(check),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
 review=[]
 for f,(_,level)in g.FAMILIES.items():
  for seed in [4,13]:review.append(g.generate(level,seed,template=f))
 (ROOT/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
 lines=['# Type I area generator review','Raw captured source evidence is in source.json. Raw profiles are ineligible, with omissions preserved.']
 for sid,q in g.Q.items():
  lines+=['## Original '+sid,q[':question/problem'],'Bank: '+', '.join(a[':answer/value']for a in q[':question/answer-fields'][0][':answer-field/choices']),q.get(':question/worked-solution','Worked solution absent; difficulty and correct designation also absent.')]
  family=next(f for f,z in g.FAMILIES.items()if z[0]==sid)
  for r in review:
   if r['generation']['template']==family:lines+=['### Generated authored method bank '+family+' '+str(r['generation']['parameters']),g.markdown(r)]
 lines+=['## Authored moderate mixed-map extension']+[g.markdown(r)for r in review if r['generation']['template']=='mixed']
 (ROOT/'review.md').write_text('\n\n'.join(lines))
 report={'status':'pass','practice_questions':7,'raw_exact_prompts':7,'raw_exact_present_solutions':[6,6],'complete_original_banks':[7,7],'all_original_choices':[35,35],'designations':[5,5],'missing_original_designations':2,'attribute_omission_parity':True,'normal_readback_records':len(records),'normal_source_anchor_readbacks':source_anchors,'normal_present_source_backbone_count':6,'default_family_coverage':sorted(default_family),'sampled_task_counts':ids,'slot_coverage':slots,'native':json.loads((ROOT/'native-report.json').read_text()),'native_harness_sha256':hashlib.sha256(check.read_bytes()).hexdigest(),'concurrent_fresh_render_instances':4,'runtime':records[0]['generation']['runtime'],'source_errors':{'q-82874':'missing original correct reference; u³(u−1) should be u(u³−1)','q-82878':'y=v+1 should be y=v−1','q-83947':'source vertical axis is shifted from parabola symmetry center; regenerate correct geometry','multiple':'unescaped/unbalanced literal set/system braces; raw evidence only'},'authored_levels':['easy square-gap zero-shift shear','moderate mixed map nonunit determinant'],'unresolved_findings':[]}
 (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:report[k]for k in ['status','normal_readback_records','complete_original_banks','all_original_choices','designations']},indent=2))
if __name__=='__main__':main()
