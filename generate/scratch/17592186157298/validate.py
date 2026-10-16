#!/usr/bin/env python3
"""Source-bank replay, independent geometry/Jacobian checks, real learner grading."""
import copy, hashlib, importlib.util, json, os, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
os.environ.setdefault('MPLCONFIGDIR',str(HERE/'reference/mpl-cache'))
spec=importlib.util.spec_from_file_location('polar_caps',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def group(z,i):
 assert z[i]=='{',(z,i)
 depth=1;j=i+1
 while depth:
  if z[j]=='{':depth+=1
  if z[j]=='}':depth-=1
  j+=1
 return z[i+1:j-1],j

def expression(z):
 z=z.replace('\u2061','').replace('π',r'\pi').replace('θ',r'\theta').replace(r'\theta','t').replace(r'\pi','pi')
 z=z.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace(r'\cdot','*')
 z=re.sub(r'\\operatorname\{(sin|cos|tan|sec|csc)\}',r'\1',z)
 z=re.sub(r'\{(sin|cos|tan|sec|csc)\}',r'\1',z)
 z=re.sub(r'\\(sin|cos|tan|sec|csc)',r'\1',z)
 for macro,nargs in [(r'\frac',2),(r'\sqrt',1)]:
  while macro in z:
   i=z.index(macro);j=i+len(macro);args=[]
   for _ in range(nargs):
    while z[j].isspace():j+=1
    a,j=group(z,j);args.append(expression(a))
   replacement='('+str(args[0])+')/('+str(args[1])+')'if nargs==2 else'sqrt('+str(args[0])+')'
   z=z[:i]+replacement+z[j:]
 # Consume only balanced function arguments; never swallow a surrounding sum's bracket.
 z=re.sub(r'\s+','',z)
 z=re.sub(r'(sin|cos|tan|sec|csc)(?:\^\{([^{}]+)\}|\^(-?\d+))?(?:\{\(t\)\}|\{t\}|\(t\)|t)',lambda m:'('+m[1]+'(t))'+('^('+str(m[2]or m[3])+')'if m[2]or m[3]else''),z)
 z=z.replace('{','(').replace('}',')')
 z=z.strip()
 return parse_expr(z,local_dict=g.LOC,transformations=standard_transformations+(implicit_multiplication_application,convert_xor))if z else sp.Integer(1)

def bounds(z,start):
 i=z.index('_',start)+1;lo,i=group(z,i)
 assert z[i]=='^';hi,i=group(z,i+1)
 return expression(lo),expression(hi),i

def parse_integral(z):
 z=z.replace(r'{\int }',r'\int').replace(r'\displaystyle ','')
 first=z.index(r'\int');a,b,j=bounds(z,first);second=z.index(r'\int',j);h=expression(z[j:second]);lo,hi,k=bounds(z,second)
 radial=re.split(r'\\(?:text|mathrm)\{d\}r',z[k:])[0]
 radial=radial.replace(r'\,','').strip()
 return [a,b,lo,hi,sp.trigsimp(h*expression(radial))]

def same(a,b):return len(a)==len(b)and all(g.eq(x,y)for x,y in zip(a,b))
def signature(sid,k):
 C,R,N,d,ab,f,lo,hi=g.model(sid,k)
 return g.digest([list(map(str,C)),str(R),list(map(str,N)),str(d),list(map(str,ab)),str(f)])

def native(r,label):
 f=r['question'][':question/answer-fields'][0];ci=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==ci else'rejected','purpose':'real learner radio selection'}for a in f[':answer-field/choices']]}

def check(rec,rendered=True):
 sid=rec['generation']['template'];scale=rec['generation']['parameters']['scale'];q=rec['question'];field=q[':question/answer-fields'][0]
 assert rec['knowledge_point']['db_id']==g.KP and q[':question/difficulty']==':question.difficulty/moderate'
 assert field[':answer-field/key']=='selection'and field[':answer-field/type']==':answer-field.type/radio'and len(field[':answer-field/choices'])==5
 replay=g.generate('moderate',rec['generation']['seed'],sid,scale,plots=bool(rec['generation']['assets']))
 assert replay==rec,'Exact instance replay failed'
 options=[parse_integral(a[':answer/value'])for a in field[':answer-field/choices']]
 assert len({a[':answer/id']for a in field[':answer-field/choices']})==5
 for i,row in enumerate(options):
  for other in options[:i]:assert not same(row,other),'Duplicate formal integral options'
 ci=next(i for i,a in enumerate(field[':answer-field/choices'])if a[':answer/id']==field[':answer-field/correct'][1]);got=options[ci]
 C,R,N,d,ab,f,lo,hi=g.model(sid,scale)
 # Independent polar boundary derivation from Cartesian equation; r>0 branch.
 rr=sp.Symbol('rr',positive=True);theta=sp.Symbol('theta',real=True)
 xx=rr*sp.cos(theta);yy=rr*sp.sin(theta)
 poly=sp.expand((xx-C[0])**2+(yy-C[1])**2-R**2)
 polar_hi=hi.subs(g.t,theta)
 assert sp.trigsimp(poly.subs(rr,polar_hi))==0,'Wrong radial circle root'
 polar_lo=sp.solve(N[0]*xx+N[1]*yy-d,rr)[0]
 assert g.eq(polar_lo,lo.subs(g.t,theta))
 density=sp.trigsimp(f.subs({g.x:xx,g.y:yy},simultaneous=True)*rr)
 assert same(got,[*ab,lo,hi,density.subs({rr:g.r,theta:g.t})]),'Correct bank does not match domain and Jacobian'
 for a in [ab[0]+(ab[1]-ab[0])*sp.Rational(j,8)for j in range(9)]:
  low=sp.simplify(lo.subs(g.t,a));high=sp.simplify(hi.subs(g.t,a))
  assert float(low)>0 and float(high-low)>-1e-9
  for radius in [low,(low+high)/2,high]:
   X=radius*sp.cos(a);Y=radius*sp.sin(a)
   assert float(sp.simplify((X-C[0])**2+(Y-C[1])**2-R**2))<1e-8
   assert float(sp.simplify(N[0]*X+N[1]*Y-d))>-1e-8
 # Independently read rendered equations, region bounds and final answer.
 if rendered:
  prompt=q[':question/problem'];sol=q[':question/worked-solution'];assert prompt.count('$')%2==0 and sol.count('$')%2==0
  curve=re.search(r'curve \$(.*?)\$',prompt)[1];lhs,rhs=curve.split('=');assert g.eq(expression(lhs)-expression(rhs),(g.x-C[0])**2+(g.y-C[1])**2-R**2)
  line=re.search(r'line \$(.*?)\$',prompt)[1];lhs,rhs=line.split('=');assert g.eq(expression(lhs)-expression(rhs),N[0]*g.x+N[1]*g.y-d)
  assert integral_in_solution(q,field[':answer-field/choices'][ci][':answer/value'])
  for asset in rec['generation']['assets'].values():assert (ROOT/asset).is_file()
 return signature(sid,scale)
def integral_in_solution(q,answer):return answer in q[':question/worked-solution']

def main():
 engine=[];coverage=[];components=[];review=[];fingerprints=set();slot_values=set()
 for sid,source in g.ORIGINALS.items():
  print('Validating '+sid,flush=True)
  r=g.generate('moderate',0,sid,1);check(r)
  field=source[':question/answer-fields'][0];original=[parse_integral(a[':answer/value'])for a in field[':answer-field/choices']];generated=[parse_integral(a[':answer/value'])for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  mapped=[]
  for i,a in enumerate(original):
   matches=[j for j,b in enumerate(generated)if same(a,b)];assert len(matches)==1,(sid,i,matches,a,generated);mapped.append(matches[0])
   components.append({'source_id':sid,'field_id':field[':answer-field/id'],'field_key':'selection','choice_id':field[':answer-field/choices'][i][':answer/id'],'value':field[':answer-field/choices'][i][':answer/value'],'profile':sid+':complete-bank','recipe':g.BANKS[sid][matches[0]],'recipe_order':'theta lower, theta upper, radial lower, radial upper, angular factor, radial power','complete_mathematical_value_replayed':True,'interpretation':'Observed compound tuple preserved; no invented error diagnosis'})
  assert len(set(mapped))==5 and mapped[g.CORRECT[sid]]==g.CORRECT[sid]
  coverage.append({'source_id':sid,'template':sid,'profile':sid+':complete-bank','distractors_matched':4,'distractors_total':4,'complete_banks_matched':1,'complete_banks_total':1,'missing':[],'extra':[],'correct_designation_preserved':True})
  review.append({'source':source,'replay':r,'variant':g.generate('moderate',9,sid,3)})
  engine.append(native(r,sid+'-replay'))
  # Exhaustive bounded scale domain; exact first-principles validation at boundaries
  # and interior representative values, plus deterministic replay for all slots.
  for scale in range(1,13):
   rr=g.generate('moderate',11,sid,scale,plots=False);fp=signature(sid,scale);assert fp not in fingerprints;fingerprints.add(fp);slot_values.add(scale)
   assert rr['question']==g.generate('moderate',999,sid,scale,plots=False)['question'],'Seeds created identity aliases'
   for answer in rr['question'][':question/answer-fields'][0][':answer-field/choices']:parse_integral(answer[':answer/value'])
   if scale in (1,2,7,12):check(rr);engine.append(native(rr,sid+'-scale-'+str(scale)))
  # Controlled change: only scale changes, all prompt/solution/key/diagram values agree.
  changed=g.generate('moderate',8,sid,2);check(changed);engine.append(native(changed,sid+'-controlled-scale-2'))
 (HERE/'components.json').write_text(json.dumps(components,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 md=[]
 for row in review:
  md.extend(['# '+row['replay']['generation']['template'],'## Source',row['source'][':question/problem'],row['source'][':question/worked-solution'],'## Scale 1 replay',row['replay']['question'][':question/problem'],row['replay']['question'][':question/worked-solution'],'## Scale 3 variant',row['variant']['question'][':question/problem'],row['variant']['question'][':question/worked-solution']])
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n');subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 report={'status':'passed','source_basis':g.SNAP['basis'],'source_questions':11,'field_types':{'moderate':['radio']},'supported_levels':['moderate'],'capability_exceptions':[{'levels':['easy','hard'],'status':'unsupported','reason':'All 11 practice questions at captured basis are moderate; no evidence supports different difficulty or workload. No relabeling. Shortage remains explicit.'}],'source_bank_coverage':coverage,'total_source_distractors_matched':44,'total_source_distractors':44,'complete_banks_matched':11,'complete_banks_total':11,'scale_domain_coverage':sorted(slot_values),'distinct_mathematical_tasks':len(fingerprints),'finite_policy_limit':132,'normal_policy_excludes_scale_1':True,'normal_new_candidates':121,'controlled_changed_scale_cases':11,'target_slot':'none: region orientation, sector and integrand fixed per template; arbitrary rotation changes source recipes and is outside verified domain','correctness':'Independent Cartesian circle/line substitution; exact Jacobian; rendered equations parsed; boundary/interior checks','grading':'Real application learning::grade_field, every choice in each fixture','fidelity':'Complete formal integral domains and integrands compared symbolically; formatting normalized separately','source_errors':[{'source_id':'q-161101','error':'Intermediate integral lower denominator sin(theta)-sin(theta) is zero','correction':'sin(theta)-cos(theta), supported by line equation, region and final key'},{'source_id':'q-83975','error':'Intermediate substitution shows sin(theta)^2 for x^2','correction':'cos(theta)^2, supported by x=r cos(theta) and final key'},{'source_id':'q-85062','error':'Diagram uses positive-looking 3/4 tick and y=3 label below origin','correction':'Coordinates and line y=-3 derive from equation and exact source solution; generated diagrams label signed equation'}],'generator_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(__file__),'engine_binary_sha256':sha(HERE/'check-engine'),'dependencies':{'python':sys.version,'sympy':sp.__version__},'database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ['status','source_questions','total_source_distractors_matched','complete_banks_matched','distinct_mathematical_tasks','supported_levels']}))
if __name__=='__main__':main()
