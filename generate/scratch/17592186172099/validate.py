"""Independent printed-region and boundary-flux validation, plus native grading inputs."""
import copy, importlib.util,json,re
from pathlib import Path
import sympy as s
HERE=Path(__file__).parent
sp=importlib.util.spec_from_file_location('flux_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
x,y=g.x,g.y

def region(problem):
 tail=problem.split('through the boundary of ',1)[1]
 if tail.startswith('the triangle'):
  pairs=re.findall(r'\((-?\d+),(-?\d+)\)',tail)
  assert len(pairs)==3 and pairs[0]==('0','0')
  pts=[tuple(map(s.Integer,p)) for p in pairs]
  assert pts[1][1]==pts[2][1]>0
  h=pts[1][1];return x,min(pts[1][0],pts[2][0])*y/h,max(pts[1][0],pts[2][0])*y/h,y,s.Integer(0),h
 if 'enclosed by the curve $y=' in tail:
  upper=g.scalar(tail.split('curve $y=',1)[1].split('$',1)[0]);assert 'lines $y=0$' in tail
  b=g.scalar(re.search(r'\$x=(.*?)\.\$',tail)[1]);return y,s.Integer(0),upper,x,s.Integer(0),b
 if 'enclosed by the curves $x=' in tail:
  strings=re.findall(r'\$(?:\\,)?x=(.*?)\$[,$]?',tail)
  assert len(strings)==2,(tail,strings)
  bounds=[g.scalar(t.rstrip(',$ ')) for t in strings]
  b=g.scalar(re.search(r'line \$y=(.*?)\.\$',tail)[1]);a=s.Integer(0)
  bounds.sort(key=lambda z:float(z.subs(y,b/2)))
  assert s.simplify(bounds[0].subs(y,a)-bounds[1].subs(y,a))==0
  return x,bounds[0],bounds[1],y,a,b
 raise ValueError('Unrecognized fixed-region prose')

def boundary_flux(P,Q,r):
 inner,lo,hi,outer,a,b=r
 # P(y)dy and -Q(x)dx are exact differentials; their closed integrals
 # vanish. Remove them algebraically before parametrizing the four arcs.
 P=s.expand(P-P.subs(x,0));Q=s.expand(Q-Q.subs(y,0))
 if inner==y:
  edge=s.simplify(Q.subs(y,hi)-P.subs(y,hi)*s.diff(hi,x)-Q.subs(y,lo)+P.subs(y,lo)*s.diff(lo,x))
  return s.simplify(s.integrate(edge,(x,a,b))+s.integrate(P.subs(x,b),(y,lo.subs(x,b),hi.subs(x,b)))-s.integrate(P.subs(x,a),(y,lo.subs(x,a),hi.subs(x,a))))
 edge=s.simplify(P.subs(x,hi)-Q.subs(x,hi)*s.diff(hi,y)-P.subs(x,lo)+Q.subs(x,lo)*s.diff(lo,y))
 return s.simplify(s.integrate(edge,(y,a,b))-s.integrate(Q.subs(y,a),(x,lo.subs(y,a),hi.subs(y,a)))+s.integrate(Q.subs(y,b),(x,lo.subs(y,b),hi.subs(y,b))))

def normalize(q):
 q=copy.deepcopy(q)
 for k in list(q):
  if k not in (':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):del q[k]
 if isinstance(q[':question/difficulty'],dict):q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  for k in list(f):
   if k==':db/id':del f[k]
  if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  if isinstance(f[':answer-field/correct'],dict):f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  for a in f[':answer-field/choices']:
   a.pop(':db/id',None)
   if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
 return json.loads(json.dumps(q,default=str))

def record(q):return {'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':normalize(q),'generation':{'template':'current-source'}}

def check_math(rec,generated=True):
 q=normalize(rec['question']);P,Q=g.components(q[':question/problem']);r=region(q[':question/problem'])
 inner,lo,hi,outer,a,b=r
 div=s.expand(s.diff(P,x)+s.diff(Q,y))
 value=s.simplify(s.integrate(s.integrate(div,(inner,lo,hi)),(outer,a,b)))
 assert s.simplify(value-boundary_flux(P,Q,r))==0,'Independent parametric boundary flux mismatch'
 fs=q[':question/answer-fields'];assert len(fs)==1
 f=fs[0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 choices=f[':answer-field/choices'];assert len(choices)==5
 values=[g.scalar(z[':answer/value']) for z in choices]
 assert len({z[':answer/id'] for z in choices})==5
 assert all(s.simplify(z-w)!=0 for i,z in enumerate(values) for w in values[i+1:])
 selected=[z for z in choices if z[':answer/id']==f[':answer-field/correct'][1]]
 assert len(selected)==1 and s.simplify(g.scalar(selected[0][':answer/value'])-value)==0,'Incorrect canonical answer'
 sol=q[':question/worked-solution']
 if generated:
  m=re.search(r'We have that \$P\(x,y\)=(.*?)\$ and \$Q\(x,y\)=(.*?)\.\$',sol);assert m
  assert s.simplify(g.scalar(m[1])-P)==0 and s.simplify(g.scalar(m[2])-Q)==0
  m=re.search(r'\\frac\{\\partial P\}\{\\partial x\}=(.*?),\\qquad \\frac\{\\partial Q\}\{\\partial y\}=(.*?)\.',sol);assert m
  assert s.simplify(g.scalar(m[1])-s.diff(P,x))==0 and s.simplify(g.scalar(m[2])-s.diff(Q,y))==0
  # Read all four printed bounds independently of the generator's region table.
  m=re.search(r'D=\\\{\(x,y\):(.*?)\\\}',sol);assert m
  parts=m[1].split(r',\quad ');assert len(parts)==2
  for text,expected in zip(parts,[(a,outer,b),(lo,inner,hi)]):
   z=text.split(r'\leq ');assert len(z)==3
   assert all(s.simplify(g.scalar(t)-w)==0 for t,w in zip(z,expected))
  primitives=re.findall(r'\\left\[(.*?)\\right\]',sol);assert len(primitives)==2
  prim,anti=map(g.scalar,primitives)
  assert s.simplify(s.diff(prim,inner)-div)==0,'Incorrect inner primitive'
  integrated=s.simplify(prim.subs(inner,hi)-prim.subs(inner,lo))
  assert s.simplify(s.diff(anti,outer)-integrated)==0,'Incorrect outer primitive'
  integrands=[re.search(r'\\left\((.*)\\right\)',line)[1] for line in sol.split(r'\\') if line.startswith(r'&=\int_') and r'\left(' in line and r'\left[' not in line]
  assert len(integrands)==2 and s.simplify(g.scalar(integrands[0])-div)==0 and s.simplify(g.scalar(integrands[1])-integrated)==0
  last=re.search(r'&=(.*?)\.\\end\{aligned\}',sol.split(r'\\')[-1]);assert last
  assert s.simplify(g.scalar(last[1])-value)==0,'Stale printed final flux'
  assert sol.count('$$')%2==0 and q[':question/problem'].count('$$')%2==0
 return {'flux':str(value),'boundary_flux':str(boundary_flux(P,Q,r)),'fingerprint':g.signature(q)}

def engine_checks(rec):
 q=normalize(rec['question']);f=q[':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete five-option bank'} for a in f[':answer-field/choices']]

def main():
 reports=[];native=[];reviews=[];mappings=[];mutation_count=0
 for key,source in sorted(g.SOURCES.items()):
  if key in g.EXCLUDED:
   reports.append({'source':key,'excluded':True,'reason':g.EXCLUDED[key]});continue
  level=source[':question/difficulty'][':db/ident'].split('/')[-1]
  original=record(source);check_math(original,False)
  native.append({'label':key+'-source','record':original,'checks':engine_checks(original)})
  for scale in (1,2,7,50):
   rec=g.generate(level,42,template=key,parameters={'scale':scale});res=check_math(rec)
   assert rec==g.generate(level,42,template=key,parameters={'scale':scale})
   other=g.generate(level,99,template=key,parameters={'scale':scale})
   assert rec['question']==other['question'],'Seed-only duplicate identity'
   vals=[g.scalar(a[':answer/value']) for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]
   assert all(sum(s.simplify(v-scale*z)==0 for v in vals)==1 for z in g.bank(source))
   if scale==1:
    assert g.signature(source)==g.signature(rec['question'])
    reports.append({'source':key,'level':level,'choices_matched':5,'distractors_matched':4,'complete_bank':True,'correct_designation_matched':True,'missing':[],'extra':[],'notation':'Unicode source vector converted to explicit LaTeX angle brackets; standard scalar TeX notation retained; same scalar response and ordered theorem/region/integral stages'})
   native.append({'label':key+'-scale-'+str(scale),'record':rec,'checks':engine_checks(rec)})
   if scale in (1,7):reviews.append({'source_id':key,'source_problem':source[':question/problem'],'source_solution':source[':question/worked-solution'],'generated':rec})
  for bad in ('key','primitive','bound','final'):
   rec=g.generate(level,42,template=key,parameters={'scale':7});q=rec['question'];f=q[':question/answer-fields'][0]
   if bad=='key':f[':answer-field/correct'][1]=next(z[':answer/id'] for z in f[':answer-field/choices'] if z[':answer/id']!=f[':answer-field/correct'][1])
   if bad=='primitive':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\left[',r'\left['+str(region(q[':question/problem'])[0])+'+',1)
   if bad=='bound':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'D=\{(x,y):',r'D=\{(x,y):99+',1)
   if bad=='final':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'.\end{aligned}',r'+1.\end{aligned}')
   try:check_math(rec)
   except (AssertionError,ValueError):mutation_count+=1
   else:raise AssertionError('Mutation not caught: '+bad)
  mappings.append({'source_id':key,'template':key,'profile':key,'original_field':source[':question/answer-fields'][0][':answer-field/id'],
   'components':[{ 'source_answer_id':a[':answer/id'],'original_exact_value':a[':answer/value'],'expression':str(g.scalar(a[':answer/value'])),'recipe':'scale * ('+str(g.scalar(a[':answer/value']))+')','correct':a[':answer/id']==source[':question/answer-fields'][0][':answer-field/correct'][':answer/id'],'interpretation':'Retained observed mathematical pattern; cognitive error unresolved'} for a in source[':question/answer-fields'][0][':answer-field/choices']]})
 # The canonical example participates in duplicate exclusion but not inventory.
 canonical=g.CAPTURE['kp'][':knowledge-point/canonical-example']
 P,Q=g.components(canonical[':question/problem']);r=region(canonical[':question/problem'])
 assert s.simplify(boundary_flux(P,Q,r)+20)==0
 assert g.signature(canonical)
 # Parameter boundaries and unsupported contracts must reject before output.
 boundary_rejections=0
 for bad in (0,-1,True,1.5):
  try:g.generate('moderate',template='q-126817',parameters={'scale':bad})
  except ValueError:boundary_rejections+=1
  else:raise AssertionError('Invalid scale accepted')
 for kwargs in ({'level':'easy'},{'level':'moderate','template':'q-127316'}, {'level':'moderate','profile':'wrong-bank'},{'level':'moderate','field_type':'blank'},{'level':'moderate','parameters':{'scale':2,'target':'new'}}):
  try:g.generate(**kwargs)
  except ValueError:boundary_rejections+=1
  else:raise AssertionError('Unsupported contract accepted')
 # Default seeded sampling must choose every eligible profile, not only first.
 coverage={level:{} for level in g.LEVELS}
 for level in g.LEVELS:
  for seed in range(100):
   rec=g.generate(level,seed);coverage[level].setdefault(rec['generation']['profile'],set()).add(rec['generation']['parameters']['scale'])
  assert set(coverage[level])=={k for k,q in g.SOURCES.items() if k not in g.EXCLUDED and q[':question/difficulty'][':db/ident'].endswith('/'+level)}
 variation={l:{k:sorted(v) for k,v in d.items()} for l,d in coverage.items()}
 for name,value in [('bank-mapping.json',mappings),('review.json',reviews),('engine-input.json',native),('validation.json',{'pass':True,'source_basis':g.CAPTURE['basis'],'source_practice_count':11,'supported_source_banks':9,'complete_supported_banks_matched':9,'matched_source_options':45,'total_supported_source_options':45,'matched_distractors':36,'excluded_profiles':g.EXCLUDED,'replay':reports,'mathematical_method':'Printed field differentiation, printed region, exact double integration, independent parametric boundary flux','generated_checks':36,'invalid_parameter_and_contract_rejections':boundary_rejections,'mutation_failures_caught':mutation_count,'slot_coverage':variation,'fixed_slots':'All original regions, target flux, 2D components, radio selection key and five options; source diagrams reused','unsupported_levels':['easy'],'grading':'See engine-report.json, actual native grade_field; correctness separate from ID-selection'})]:
  (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
 print('Validated 9 complete source banks; 36 scale replays; 36 key/primitive/bound/final mutations rejected.')
if __name__=='__main__':main()
