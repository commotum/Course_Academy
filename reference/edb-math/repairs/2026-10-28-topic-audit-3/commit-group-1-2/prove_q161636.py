"""Independent real-domain and whole-bank proof; no EDB writes."""
import json,re
from pathlib import Path
import mpmath as mp
H=Path(__file__).resolve().parent;D=json.loads((H/'staged-current.json').read_text());q=next(q for q in D['questions']if q.get(':question/math-academy-id')=='q-161636');f=q[':question/answer-fields'][0];assert f[':db/id']==17592186367730
C=7
# Each model is independently read from its full displayed AFTER integral.
models={17592186367731:('cos','sin',1),17592186367732:('cos','sin',0),17592186367733:('minus_sin','sin',0),17592186367734:('cos','cos',1),17592186367735:('minus_sin','cos',1)}
mp.mp.dps=55
results=[]
for answer in f[':answer-field/choices']:
 aid=answer[':db/id'];Rkind,Lkind,p=models[aid]
 R=lambda th:6*mp.cos(th)if Rkind=='cos'else-6*mp.sin(th)
 L=lambda th:mp.sin(th)if Lkind=='sin'else mp.cos(th)
 # Integrate in z analytically, then independently integrate over a unit square.
 def angular(th):return mp.quad(lambda u:2*R(th)*(R(th)*u)**p*(mp.sqrt(C+6)-mp.sqrt(C+R(th)*u*L(th))),[0,1])
 value=mp.quad(angular,[-mp.pi/2,-mp.pi/4,0]);results.append({'answer':aid,'radial_upper':'6 cos(theta)'if Rkind=='cos'else'-6 sin(theta)','z_lower':'r sin(theta)'if Lkind=='sin'else'r cos(theta)','jacobian_power':p,'real_integral_value_55_digit_quadrature':str(value),'correct':aid==17592186367731})
# Cartesian reduction is independent of the polar Jacobian calculation.
cart=36*mp.quad(lambda ph:mp.cos(ph)**2*(mp.sqrt(13)-mp.sqrt(7-3*mp.sin(ph))),[0,mp.pi/2]);assert abs(cart-mp.mpf(results[0]['real_integral_value_55_digit_quadrature']))<mp.mpf('1e-45')
# Rigorous interval rectangle enclosures, with outward rounded arithmetic.
mp.iv.dps=30
intervals=None
for N in[32,64,128,256]:
 iv=mp.iv;theta_width=iv.pi/(2*N);u_width=iv.mpf(1)/N;sums=[iv.mpf(0)for _ in results]
 for j in range(N):
  lo=-iv.pi/2+iv.pi*j/(2*N);hi=-iv.pi/2+iv.pi*(j+1)/(2*N);th=iv.mpf([lo.a,hi.b]);co=iv.cos(th);si=iv.sin(th)
  for k in range(N):
   ulo=iv.mpf(k)/N;uhi=iv.mpf(k+1)/N;u=iv.mpf([ulo.a,uhi.b])
   for i,result in enumerate(results):
    Rkind,Lkind,p=models[result['answer']];radius=6*co if Rkind=='cos'else-6*si;low=si if Lkind=='sin'else co;r=radius*u;zlow=r*low
    # Covers all values in this rectangle, hence bounds its exact integral.
    v=2*radius*(r if p else 1)*(iv.sqrt(13)-iv.sqrt(7+zlow));sums[i]+=v*theta_width*u_width
 intervals=[{'answer':r['answer'],'lower':str(v.a),'upper':str(v.b)}for r,v in zip(results,sums)]
 distinct=all(sums[i].b<sums[j].a or sums[j].b<sums[i].a for i in range(5)for j in range(i))
 print('interval grid',N,'all_distinct',distinct,flush=True)
 if distinct:break
assert distinct,intervals
proof={'basis_t':9837,'expected_before':'Own committed T10057 source-format projection in staged-current.json; root CAS rechecks exact before values.','identity':'q-161636','question':q[':db/id'],'field':f[':db/id'],'full_before_question':q,'classification':'Authored original-source mathematical correction, not source recovery','old_domain_counterexample':{'point':['3','-2','-3/2'],'circle_value':'4 < 9','y_le_0':True,'z_bounds':'-2 < -3/2 < 6','z_plus_1':'-1/2 < 0','conclusion':'An open subset of the stated real solid has a nonreal kernel.'},'amendment':{'kernel':'1/sqrt(z+7)','original_solid_min_z':-3,'minimum_radicand_over_original_solid':4,'minimum_z_over_all_five_displayed_setups':-6,'minimum_radicand_over_all_five':1,'minimality':'7 is the smallest integer shift strictly positive over every preserved displayed setup; no change to solid/graph/limits/error recipes.'},'independent_change_of_variables':{'circle':'(x-3)^2+y^2<=9 -> r²-6r cos(theta)<=0','angular':'3pi/2<=theta<=2pi, since x>=0 and y<=0 on the depicted half-cylinder','radial':'0<=r<=6cos(theta)','vertical':'r sin(theta)<=z<=6','jacobian':'dV=r dz dr dtheta','correct_integrand':'r/sqrt(z+7)','canonical_answer':17592186367731},'circle_substitution_typo':'(r cos(theta)-3)^2+(r sin(theta))^2=9; a stored RHS3 contradicts both the original circle and the following expansion.','whole_after_bank':results,'independent_cartesian_value':str(cart),'interval_rectangle_grid':N,'outward_rounded_enclosures':intervals,'all_five_real_finite_and_pairwise_distinct':True,'region_graph_unchanged':True,'no_integral_evaluation_stored':'Task and worked solution derive the integral setup; the proof evaluations are QA only, no learner calculation is added.'}
(H/'q161636-independent-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
# Sweep the full stored sibling scope and every matching z+constant radical in all2614 records.
links={row[2]for row in D['links']if row[1]==17592186129268};sweep=[]
for candidate in D['questions']:
 text=candidate[':question/problem'];rad=re.search(r'\\sqrt\{z\s*\+\s*(\d+)\}',text)
 if candidate[':db/id']not in links and not rad:continue
 item={'entity':candidate[':db/id'],'identity':candidate.get(':question/math-academy-id'),'in_kp129268':candidate[':db/id']in links,'full_problem':text}
 if rad:
  c=int(rad[1]);circle=re.search(r'\(x-(\d+)\)\^\{2\}\+\{y\}\^\{2\}',text)
  if circle and r'y\le 0'in text and r'y\le z'in text:
   a=int(circle[1]);item.update(kernel_constant=c,cylinder_radius=a,actual_minimum_z=-a,minimum_radicand=c-a,status='defect'if c-a<=0 else'positive-real-on-stated-solid')
  else:item['status']='Other root frame retained for exact review'
 else:item['status']='Different integrand/root family; explicit source guard and full question retained, no z+C defect pattern.'
 sweep.append(item)
(H/'q161636-sibling-sweep.json').write_text(json.dumps({'basis_t':9837,'kp_records':len(links),'root_matched_records':sum('kernel_constant'in r for r in sweep),'records':sweep},indent=2)+'\n');print('values',[r['real_integral_value_55_digit_quadrature']for r in results],'siblings',len(links),'root matches',sum('kernel_constant'in r for r in sweep),flush=True)
# Minimal scalar CAS proposals, preserving all identities/links and the region diagram.
props=[]
def stage(entity,attribute,before,after,reason):
 assert before!=after;props.append({'entity':entity,'attribute':attribute,'before':before,'after':after,'reason':reason,'evidence':{'basis_t':9837,'identity':'q-161636','classification':'Authored original-source mathematical correction','proof':'q161636-independent-proof.json','sibling_sweep':'q161636-sibling-sweep.json','preservation':'Original solid, projection graph, bounds, field/answer IDs, canonical link and intended distractor operations retained.'},'confidence':'high'})
def kernel(value):
 after,n=re.subn(r'\\sqrt\{z\s*\+\s*1\}',lambda m:r'\sqrt{z+7}',value);assert n>=1,(value,n);return after
stage(q[':db/id'],'question/problem',q[':question/problem'],kernel(q[':question/problem']),'Amend the scalar kernel to remain real across the full unchanged solid and all preserved displayed setup alternatives.')
before=q[':question/worked-solution'];after=kernel(before);wrong=r'(r\operatorname{cos}⁡\theta -3)^{2}+(r\operatorname{sin}⁡\theta )^{2} & =3';right=wrong[:-1]+'9'
if wrong not in after:
 wrong=r'(r\operatorname{cos}\theta -3)^{2}+(r\operatorname{sin}\theta )^{2} & =3';right=wrong[:-1]+'9'
assert after.count(wrong)==1;after=after.replace(wrong,right);stage(q[':db/id'],'question/worked-solution',before,after,'Derive the amended kernel with the same limits/Jacobian and correct the inconsistent circle-substitution RHS3 to9.')
for answer in f[':answer-field/choices']:stage(answer[':db/id'],'answer/value',answer[':answer/value'],kernel(answer[':answer/value']),'Express this preserved correct/error setup with the amended positive-real kernel; retain its own bounds and Jacobian recipe.')
assert len(props)==7;(H/'supplemental-math-proposals.json').write_text(json.dumps(props,indent=2)+'\n')
