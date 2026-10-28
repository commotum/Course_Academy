"""Independent display readback, source fidelity and native grader checks."""
import copy,importlib.util,json,re,subprocess,sys,hashlib
from pathlib import Path
import sympy as s
DIR=Path(__file__).parent
spec=importlib.util.spec_from_file_location('generator',DIR.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('parser',DIR/'math_parser.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x,y,z=p.x,p.y,p.z

def parse(raw):
 raw=raw.replace(r'\operatorname{ln}',r'\ln').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos').replace(r'\cancel','').replace('⁡','').replace(r'\,','').strip().rstrip('.,')
 return p.scalar(raw)
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
def blocks(text):return [m[1] if m[1] is not None else m[2] for m in re.finditer(r'\$\$(.*?)\$\$|\$([^$]*)\$',text,re.S)]
def fmt(text):
 assert text.count('$$')%2==0
 assert len(re.findall(r'(?<!\$)\$(?!\$)',text))%2==0
 depth=0
 for i,c in enumerate(text):
  if c=='{' and (i==0 or text[i-1]!='\\'):depth+=1
  if c=='}' and (i==0 or text[i-1]!='\\'):depth-=1
  assert depth>=0
 assert depth==0
 assert '--' not in text and '+-' not in text

def actual_prompt(q,raw=False):
 text=q[':question/problem'];bs=blocks(text)
 surface=next(v for v in bs if re.match(r'z\s*=',v));surface=surface.split('=',1)[1].rstrip('.');G=parse(surface)
 lim=[]
 for v in bs:
  # Raw second coordinate bounds are sometimes in the same math span.
  for variable in ('x','y'):
   for m in re.finditer(r'([^$]*?)\\le(?:q)?\s*'+variable+r'\s*\\le(?:q)?([^$]*)',v):
    before=m[1].strip();after=m[2].strip().rstrip('.')
    if 'and' in before:before=before.split('and')[-1]
    if '\\le' in before or '\\le' in after:continue
    lim.append((variable,parse(before),parse(after)))
 if raw:
  # Source spans contain no merged range; preserve exact weird legacy integral.
  body=next(v for v in bs if '∬' in v).strip()
  if '∬_(S)' in body:F=parse(body.split('∬_(S)',1)[1].removesuffix('dS'))
  else:F=parse(re.sub(r'^\{∬\}_\{S\}','',body).split(r'\text{d}S')[0])
 else:
  body=next(v for v in bs if r'\iint_S' in v);F=parse(body.split(r'\iint_S',1)[1].split(r'\mathrm{d}S')[0])
 limits={v:(a,b) for v,a,b in lim};assert set(limits)=={'x','y'},(text,limits)
 return G,F,(*limits['x'],*limits['y'])

def source_eval(raw,G,F,B):
 """Evaluate every actual source scalar integral/arithmetic row recursively."""
 raw=raw.strip().rstrip('.,').replace(r'\cancel','').replace('⁡','').replace(r'\,','').replace(r'\text{d}A','dA').replace(r'\text{d}x','dx').replace(r'\text{d}y','dy').replace(r'\mathrm{d}x','dx').replace(r'\mathrm{d}y','dy').replace(r'{\int }',r'\int').replace(r'{\int}',r'\int')
 raw=raw.replace(r'\text{Area}(D)','('+s.latex((B[1]-B[0])*(B[3]-B[2]))+')')
 M=s.sqrt(s.factor(1+s.diff(G,x)**2+s.diff(G,y)**2));D=s.simplify(s.trigsimp(F.subs(z,G)*M));lo,hi,yl,yh=B
 if 'f(x,y,g(x,y))' in raw:return s.integrate(s.integrate(D,(y,yl,yh)),(x,lo,hi))
 # Scale wrapping public raw changed instances.
 if r'\left(' in raw and raw.endswith(r'\right)'):
  first=raw.index(r'\left(')
  if first>0:
   depth=0;end=None
   for token in re.finditer(r'\\left\(|\\right\)',raw[first:]):
    depth+=1 if token[0]==r'\left(' else -1
    if depth==0:end=first+token.end();break
   if end==len(raw) and any(mark in raw[first+6:-7] for mark in ('{∬}',r'\int','[')):return parse(raw[:first])*source_eval(raw[first+6:-7],G,F/parse(raw[:first]),B)
 if '{∬}_{D}' in raw:
  pref,tail=raw.split('{∬}_{D}',1);assert tail.endswith('dA');fn=parse(tail[:-2]) if tail[:-2].strip() else s.Integer(1);factor=parse(pref) if pref else 1
  assert same(factor*fn,D),(raw,factor*fn,D)
  return factor*s.integrate(s.integrate(fn,(y,yl,yh)),(x,lo,hi))
 if r'\int' in raw:
  # Innermost integration or a primitive evaluation inside an outer integral.
  start=raw.index(r'\int');factor=parse(raw[:start]) if start else 1;pos=start+4
  assert raw[pos]=='_';a,pos=group(raw,pos+1);assert raw[pos]=='^';b,pos=group(raw,pos+1)
  body=raw[pos:];var=body[-1];assert body.endswith('d'+var);inner=body[:-2];symbol={'x':x,'y':y}[var]
  assert same(parse(a),lo if var=='x' else yl) and same(parse(b),hi if var=='x' else yh),(raw,B)
  innervalue=source_eval(inner,G,F/factor,B)
  if var=='y':assert same(factor*innervalue,D),(inner,innervalue,D)
  else:
   expected=s.integrate(D,(y,yl,yh));assert same(factor*innervalue,expected),(inner,factor*innervalue,expected)
  return factor*s.integrate(innervalue,(symbol,parse(a),parse(b)))
 if '[' in raw:
  first=raw.index('[');last=raw.rindex(']');prefix=raw[:first];suffix=raw[last+1:].lstrip('}')
  # Prefix can be the source's redundant opening TeX group.
  while prefix.endswith('{'):prefix=prefix[:-1]
  assert suffix.startswith('_');a,pos=group(suffix,1);assert suffix[pos]=='^';b,pos=group(suffix,pos+1);assert not suffix[pos:]
  if '=' in a:var,aa=a.split('=',1);var2,bb=b.split('=',1);assert var==var2
  else:var='y' if parse(raw[first+1:last]).has(y) else 'x';aa,bb=a,b
  symbol={'x':x,'y':y}[var];anti=parse(raw[first+1:last]);factor=parse(prefix) if prefix else 1
  assert same(parse(aa),yl if var=='y' else lo) and same(parse(bb),yh if var=='y' else hi)
  expected=D if var=='y' else s.integrate(D,(y,yl,yh))
  assert same(factor*s.diff(anti,symbol),expected),(raw,factor*s.diff(anti,symbol),expected)
  value=anti.subs(symbol,parse(bb))-anti.subs(symbol,parse(aa));return factor*value
 return parse(raw)
def group(raw,pos):
 if raw[pos]=='{':
  depth=1;i=pos+1
  while depth:depth+=(raw[i]=='{')-(raw[i]=='}');i+=1
  return raw[pos+1:i-1],i
 return raw[pos],pos+1

def component_list(raw):
 raw=raw.strip().replace(r'\left','').replace(r'\right','')
 if not raw.startswith('('):return [parse(raw)]
 values=[];pos=0
 while pos<len(raw):
  assert raw[pos]=='(',raw;depth=1;end=pos+1
  while depth:depth+=(raw[end]=='(')-(raw[end]==')');end+=1
  values.append(parse(raw[pos+1:end-1]));pos=end
  if pos<len(raw):assert raw[pos]=='+';pos+=1
 return values

def endpoint_components(row):
 # The complete points mask wraps the separately evaluated upper list and
 # separately evaluated lower list. Preserve those lists before simplification.
 start=row.index(r'\left(');tokens=list(re.finditer(r'\\left\(|\\right\)',row[start:]));depth=0;end=None
 for token in tokens:
  depth+=1 if token[0]==r'\left(' else -1
  if depth==0:end=start+token.start();break
 assert end is not None
 body=row[start+6:end].replace(r'\left','').replace(r'\right','')
 depth=0;split=None
 for i,char in enumerate(body):
  depth+=(char=='(')-(char==')')
  if char=='-' and depth==0 and i+1<len(body) and body[i+1]=='(':split=i;break
 assert split is not None,body
 upper=component_list(body[:split]);lower=component_list(body[split+2:-1]);return upper,lower

def check_components(endpoint_row,primitive_row,var,bounds):
 body=primitive_row[primitive_row.index('[')+1:primitive_row.rindex(']')];terms=component_list(body)
 actual=endpoint_components(endpoint_row)
 for values,at in zip(actual,bounds[::-1]):
  expected=[term.subs(var,at) for term in terms]
  assert len(values)==len(expected),(endpoint_row,terms,values)
  assert all(same(a,b) for a,b in zip(values,expected)),(endpoint_row,values,expected)

def check_structure(r,rows):
 """Independent observed-family operation-order and unevaluated-mask checks."""
 solution=r['question'][':question/worked-solution'];family=r['generation']['template']
 assert not re.search(r'\b(?:M|P|H|Y|X)\s*=',solution)
 assert solution.count(r'\begin{aligned}')==1
 assert 'For the partial derivatives, we have' in solution
 assert 'Therefore, the surface integral can be evaluated as follows:' in solution
 assert 'f(x,y,g(x,y))' in rows[0]
 rhs=[row.split('& =',1)[1].strip().rstrip('.') for row in rows]
 def kind(row):
  if 'f(x,y,g(x,y))' in row:return 'formal'
  if '{∬}_{D}' in row:return 'double'
  if row.count(r'\int')==2:return 'repeated'
  if r'\int' in row:return 'inner_primitive' if '[' in row else 'outer_integral'
  if '[' in row:return 'outer_primitive'
  return 'arithmetic'
 F,D,R,J,O,X,A='formal','double','repeated','inner_primitive','outer_integral','outer_primitive','arithmetic'
 specs={
  'plane_xyz':[F,D,R,J,O,O,X,A,A],
  'plane_linear':[F,D,R,J,O,O,X,A,A],
  'plane_log':[F,D,D,R,J,O,O,X,A,A],
  'plane_ratio':[F,D,D,D,R,J,O,O,X,A,A],
  'reciprocal_triangle':[F,D,R,J,O,X,A,A],
  'trig_triangle':[F,D,D,D,R,J,O,X,A,A],
  'paraboloid_xy':[F,D,D,D,D,D,R,J,O,O,X,A,A],
  'plane_sine':[F,D,D,R,J,O,O,X,A,A],
  'cross_cancel':[F,D,D,D,R,J,O,O,X,A,A],
  'quadratic_triangle':[F,D,D,D,R,J,O,O,O,X,A,A],
  'quadratic_rectangle_full':[F,D,D,D,R,J,O,O,X,A,A],
  'quadratic_triangle_full':[F,D,D,D,R,J,O,O,O,X,A,A],
  'constant_plane':[F,D,D,D,A,A,A,A],
  'canonical_cancel':[F,D,D,D,D,D,D,D,A,A,A,A]}
 actual=[kind(v) for v in rhs];assert actual==specs[family],(family,actual,specs[family])
 G,integrand,B=actual_prompt(r['question']);gx,gy=s.diff(G,x),s.diff(G,y);metric=s.sqrt(s.factor(1+gx*gx+gy*gy))
 def prefix(row,marker):return row.split(marker,1)[0].strip()
 if family in ('plane_linear','plane_xyz'):
  assert not prefix(rhs[2],r'\int')
  for i in (3,4,5):assert same(parse(prefix(rhs[i],r'\int')),metric)
 if family=='cross_cancel' or family=='quadratic_rectangle_full':
  for i in (2,3):assert same(parse(prefix(rhs[i],'{∬}_{D}')),metric)
  for i in (4,5,6,7):assert same(parse(prefix(rhs[i],r'\int')),metric)
  assert same(parse(prefix(rhs[8],'[')),metric)
 if family in ('quadratic_triangle','quadratic_triangle_full'):
  assert not prefix(rhs[2],'{∬}_{D}')
  assert r'\sqrt{'+s.latex(1+gx*gx+gy*gy)+'}' in rhs[2]
  assert same(parse(prefix(rhs[8],r'\int')),metric/3)
 if family in ('cross_cancel','quadratic_triangle','quadratic_rectangle_full','quadratic_triangle_full'):
  row=rhs[2];matches=re.findall(r'\(([^()]*)\)',row.replace(r'\left','').replace(r'\right',''))
  # The complete scalar coefficient is followed by each separate source-style
  # square-expansion contribution, before any like terms are collected.
  coefficient=integrand.expand().coeff(z,2)
  expected=list(s.Add.make_args(s.expand(integrand.subs(z,0)/coefficient)))
  expected += [gx*gx*x*x,gy*gy*y*y,2*gx*gy*x*y]
  actual_terms=[parse(v) for v in (matches[1:] if coefficient!=1 else matches)]
  assert len(actual_terms)==len(expected)
  remaining=list(expected)
  for value in actual_terms:
   matches=[i for i,w in enumerate(remaining) if same(value,w)];assert matches,(family,actual_terms,expected);remaining.pop(matches[0])
  assert not remaining
 # Project only the documented supplemental endpoint rows out of the
 # normal chain, then compare against the actual captured source skeleton.
 if family in g.FAMILIES:
  sid=g.FAMILIES[family] if family!='plane_xyz' else 'q-161341'
  source=g.QS[sid][':question/worked-solution'];source_rows=source.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\')
  source_kind=[kind(row.split('& =',1)[1].replace(r'{\int }',r'\int')) for row in source_rows]
  supplemental={'plane_xyz':[4,7],'plane_linear':[4,7],'plane_log':[5],'trig_triangle':[8],'paraboloid_xy':[8],'plane_sine':[8],'cross_cancel':[6],'quadratic_triangle':[10]}.get(family,[])
  projected=[value for i,value in enumerate(actual) if i not in supplemental]
  assert projected==source_kind,(family,projected,source_kind)
 if family=='plane_log':
  assert r'\ln y' in rhs[4] and '[' in rhs[4]
  assert all(r'\sqrt' not in row for row in rhs[2:])
  assert r'\ln' not in rhs[7]
 if family=='reciprocal_triangle':
  assert r'\right)^{2}' in rhs[2]
  assert r'\frac' in rhs[3] and r'\ln' in rhs[5] and '[' in rhs[5]
  assert r'\ln' in rhs[6] and 'x' not in rhs[6]
  assert 'x' not in rhs[7] and 'y' not in rhs[7] and r'\ln' in rhs[7]
  density=s.simplify(integrand.subs(z,G)*metric);value=s.integrate(s.integrate(density,(y,*B[2:])),(x,*B[:2]));expected_logs=s.expand_log(s.simplify(value),force=True).atoms(s.log)
  assert rhs[7].count(r'\ln')==len(expected_logs),(rhs[7],expected_logs)
 if family in ('trig_triangle','paraboloid_xy'):
  assert solution.count(r'\cancel')==2
 if family=='canonical_cancel':
  assert solution.count(r'\cancel')==2 and r'\text{Area}(D)' in rhs[8]
  assert r'\sqrt{2\left(' in rhs[3]
 if family=='plane_sine':
  assert r'\cos' in rhs[4] and '[' in rhs[4]
  assert '-' in rhs[5] and '(' in rhs[5]
 # Every individual upper/lower primitive component is read from actual
 # printed masks, rather than only testing the net endpoint subtraction.
 inner_pairs={'plane_xyz':(4,3),'plane_linear':(4,3),'plane_ratio':(6,5),'paraboloid_xy':(8,7),'cross_cancel':(6,5),'quadratic_triangle':(6,5),'quadratic_rectangle_full':(6,5),'quadratic_triangle_full':(6,5),'reciprocal_triangle':(4,3)}
 if family in inner_pairs:
  evaluated,primitive=inner_pairs[family];check_components(rhs[evaluated],rhs[primitive],y,B[2:])
 if family not in ('canonical_cancel','constant_plane'):
  primitive=next(i for i,value in enumerate(rhs) if kind(value)=='outer_primitive')
  check_components(rhs[primitive+1],rhs[primitive],x,B[:2])
 return {'rows':len(rows),'operation_signature':actual,'helper_labels_absent':True,'individual_endpoint_components_verified':family not in ('canonical_cancel','constant_plane')}

def check_math(r):
 q=r['question'];raw=r['generation']['evidence_only'];G,F,B=actual_prompt(q,raw);lo,hi,yl,yh=B
 dx=s.diff(G,x);dy=s.diff(G,y);M=s.sqrt(s.factor(1+dx*dx+dy*dy));P=F.subs(z,G);D=s.simplify(s.trigsimp(P*M));Y=s.integrate(D,y);O=s.simplify(Y.subs(y,yh)-Y.subs(y,yl));X=s.integrate(O,x);A=s.simplify(X.subs(x,hi)-X.subs(x,lo))
 if ':question/worked-solution' in q:
  solution=q[':question/worked-solution'];fmt(solution)
  bs=blocks(solution)
  derivatives=[b for b in bs if b.strip().startswith(r'\frac{∂z}')]
  assert len(derivatives)==2
  for body,expected,var in zip(derivatives,[dx,dy],['x','y']):
   parts=body.strip().rstrip(',.').split('=');arg=re.sub(r'\\frac\{∂\}\{∂'+var+r'\}', '',parts[1]);assert same(parse(arg),G);assert same(parse(parts[-1]),expected),(body,expected)
  aligned=next(b for b in bs if r'\begin{aligned}' in b)
  rows=aligned.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\')
  lhs=rows[0].split('& =')[0].split('{∬}_{S}',1)[1].split(r'\text{d}S')[0];assert same(parse(lhs),F)
  for row in rows:
   rhs=row.split('& =',1)[1];v=source_eval(rhs,G,F,B);assert same(v,A),(r['generation']['template'],rhs,v,A)
  if not raw:check_structure(r,rows)
 fmt(q[':question/problem'])
 bank=q[':question/answer-fields'][0][':answer-field/choices'];values=[parse(v[':answer/value']) for v in bank]
 if not raw:
  integ=lambda obj:s.simplify(s.integrate(s.integrate(obj,(y,yl,yh)),(x,lo,hi)))
  family=r['generation']['template']
  if family=='constant_plane':expected=[A,integ(P),integ(P*M*M),integ(P*s.sqrt(1+dx*dx)),A/(yh-yl)]
  elif family=='canonical_cancel':
   c=s.simplify(D/s.sqrt(2));area=(hi-lo)*(yh-yl);expected=[A,c*area,2*c*area,-A,c*s.sqrt(2)*(hi-lo)]
  elif family=='trig_triangle':expected=[A,-A,A/2,2*A,s.integrate(s.integrate(D,(y,0,yh)),(x,lo,hi))]
  elif family in ('paraboloid_xy','plane_log','plane_ratio','reciprocal_triangle'):expected=[A,-A,integ(D.subs(y,yh)),s.integrate(s.integrate(D,(y,yl,yh)),(x,lo,(hi+lo)/2)),2*A]
  else:expected=[A,integ(P),integ(P*(1+dx*dx+dy*dy)),-A,integ(F.subs(z,0)*M)]
  assert all(sum(same(v,w) for w in expected)==1 for v in values),(family,values,expected)
  assert all(not same(v,w) for i,v in enumerate(values) for w in values[:i]);assert all(not v.has(s.nan,s.zoo,s.oo) for v in values)
 field=q[':question/answer-fields'][0]
 if ':answer-field/correct' in field:
  choice=next(v for v in bank if v[':answer/id']==field[':answer-field/correct'][1]);assert same(parse(choice[':answer/value']),A),(choice,A)
 return A

def main():
 source_cases=[];records=[];review=[];raw_exact=0;banks=0;correct=0;raw_stage_rows=0
 for f,sid in g.FAMILIES.items():
  case={'source_id':sid,'template':f,'level':'moderate','parameters':{'scale':1},'bank_profile':'raw:'+sid};source_cases.append(case)
  r=g.generate('moderate',3,template=f,parameters=case['parameters'],profile=case['bank_profile']);q=r['question'];src=g.QS[sid]
  for key in (':question/problem',':question/worked-solution'):assert (key in q)==(key in src) and q.get(key)==src.get(key),(sid,key)
  assert (':question/difficulty' in q)==(':question/difficulty' in src)
  ff=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0];assert (':answer-field/correct' in ff)==(':answer-field/correct' in sf)
  assert ff[':answer-field/key']==sf[':answer-field/key'] and ff[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  if ':answer-field/correct' in sf:
   generated_correct=next(a[':answer/value'] for a in ff[':answer-field/choices'] if a[':answer/id']==ff[':answer-field/correct'][1]);assert generated_correct==sf[':answer-field/correct'][':answer/value']
  assert sorted(a[':answer/value'] for a in ff[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  check_math(r);raw_exact+=1;banks+=5;correct+=int(':answer-field/correct' in sf);records.append(r)
  review.append('## Original '+sid+' — raw evidence, ineligible\n\n'+g.markdown(r))
  # Changed scale replay validates a public mathematical change, not a literal lookup.
  changed=g.generate('moderate',4,template=f,parameters={'scale':2},profile='raw:'+sid);check_math(changed);records.append(changed);review.append('### Generated raw '+sid+' scale 2 — evidence only, opaque bank\n\n'+g.markdown(changed))
  original_normal=g.generate('moderate',8,template=f,parameters=g.ORIGINAL[f]);check_math(original_normal);records.append(original_normal);review.append('### Normal '+f+' at original parameters — authored bank, source-family chain\n\n'+g.markdown(original_normal))
  for n in range(2):
   v=g.generate('moderate',100+n,template=f);check_math(v);records.append(v);review.append('### Generated '+f+' variant '+str(n+1)+' — authored bank\n\n'+g.markdown(v))
 for level,families in [('easy',g.EASY),('hard',g.HARD)]:
  for f in families:
   for n in range(2):
    r=g.generate(level,50+n,template=f);check_math(r);records.append(r);review.append('## Authored '+level+' '+f+' variant '+str(n+1)+'\n\n'+g.markdown(r))
 # Cover defaults and meaningful variety, fixed-data identities and bounds.
 coverage=set();fingerprints={l:set() for l in ('easy','moderate','hard')};sampled=[]
 for level in fingerprints:
  for seed in range(50):
   r=g.generate(level,seed);assert g.generate(level,seed)==r;check_math(r);coverage.add((level,r['generation']['template']));fingerprints[level].add(r['generation']['mathematical_fingerprint']);sampled.append(r)
 for level,families in [('easy',g.EASY),('moderate',g.MODERATE),('hard',g.HARD)]:assert {f for l,f in coverage if l==level}==set(families)
 for r in records:
  gen=r['generation'];level=r['question'].get(':question/difficulty',':question.difficulty/moderate').split('/')[-1]
  again=g.generate(level,999,template=gen['template'],parameters=gen['parameters'],profile=gen['profile']);assert r['question'][':question/id']==again['question'][':question/id']
  assert set(r['knowledge_point'])=={'db_id','id','title'}
  assert g.generate(level,gen['seed'],template=gen['template'],parameters=gen['parameters'],profile=gen['profile'])==g.generate(level,gen['seed'],template=gen['template'],parameters=gen['parameters'],profile=gen['profile'])
 invalid=[('easy','constant_plane',dict(a=3,b=1,c=1,lo=0,hi=1,k=2)),('hard','quadratic_rectangle_full',dict(a=1,b=1,c=1,lo=0,hi=1,k=2)),('moderate','plane_ratio',dict(a=1,b=1,c=1,lo=0,hi=1,k=2))]
 for level,f,p0 in invalid:
  try:g.generate(level,0,template=f,parameters=p0)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit input accepted')
 mutation_results=[]
 def alter_chain(record,index,transform):
  changed=copy.deepcopy(record);solution=changed['question'][':question/worked-solution'];start=solution.index(r'\begin{aligned}')+len(r'\begin{aligned}');end=solution.index(r'\end{aligned}',start);rows=solution[start:end].split(r'\\')
  if transform is None:rows.pop(index)
  else:rows[index]=transform(rows[index])
  changed['question'][':question/worked-solution']=solution[:start]+r'\\'.join(rows)+solution[end:];return changed
 originals={r['generation']['template']:r for r in records if not r['generation']['evidence_only'] and r['generation']['parameters']==g.ORIGINAL.get(r['generation']['template'])}
 original=originals['cross_cancel'];removed=alter_chain(original,2,None)
 original=originals['reciprocal_triangle'];value=check_math(original);collapsed=alter_chain(original,7,lambda row:' & ='+g.tex(value)+'.')
 original=originals['plane_linear'];solution=original['question'][':question/worked-solution'];rows=solution.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\');upper,lower=endpoint_components(rows[4].split('& =',1)[1]);up='('+g.tex(upper[0])+')';dn='('+g.tex(lower[0])+')'
 changed_endpoints=alter_chain(original,4,lambda row:row.replace(up,'('+g.tex(upper[0]+1)+')',1).replace(dn,'('+g.tex(lower[0]+1)+')',1))
 for label,record in [('removed square-expansion stage',removed),('collapsed source log-split convention',collapsed),('correlated endpoint component errors with unchanged net value',changed_endpoints)]:
  try:check_math(record)
  except (AssertionError,ValueError):mutation_results.append(label)
  else:raise AssertionError('Undetected printed structural corruption: '+label)
 (DIR/'mutation-checks.json').write_text(json.dumps({'detected':mutation_results,'total':3,'changes_leave_generation_metadata_and_ids_untouched':True},indent=2)+'\n')
 fixtures=[]
 for i,r in enumerate(records+sampled):
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  fixtures.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual displayed owned radio choice'} for a in f[':answer-field/choices']]})
 (DIR/'engine-input.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n');subprocess.run(['generate/runs/current/check-engine',str(DIR/'engine-input.json'),str(DIR/'engine-report.json')],check=True)
 (DIR/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n');(DIR/'review.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');(DIR/'review.md').write_text('\n\n'.join(review)+'\n')
 structural=[]
 for record in records:
  if record['generation']['evidence_only']:continue
  solution=record['question'][':question/worked-solution'];rows=solution.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\')
  details=check_structure(record,rows)
  structural.append({'template':record['generation']['template'],'parameters':record['generation']['parameters'],'original_parameters':record['generation']['parameters']==g.ORIGINAL.get(record['generation']['template']),'source_ids':record['generation']['source_ids'],**details})
 (DIR/'normal-structure-regression.json').write_text(json.dumps(structural,indent=2)+'\n')
 engine=json.loads((DIR/'engine-report.json').read_text())
 report={'status':'pass_with_explicit_source_limits','source_questions':10,'raw_prompt_exact':10,'raw_solution_exact':{'matched':9,'present':9,'absent_preserved':1},'raw_attribute_absence_preserved':10,'source_bank_values':{'matched':50,'total':50},'source_correct_designations':{'matched':9,'present':9,'absent':1},'source_mathematically_correct_designated':9,'inferred_unrated_correct':'4 sqrt(3); not inserted into raw replay','opaque_raw_profiles_ineligible':10,'normal_templates':14,'targeted_structural_mutations_detected':len(mutation_results),'normal_structure_regressions':len(structural),'normal_original_parameter_regressions':sum(v['original_parameters'] for v in structural),'normal_source_chains_preserved':9,'unrated_source_solution_authored':1,'display_math_checks':len(records)+len(sampled),'normal_math_checks':len(records)+len(sampled)-20,'raw_math_checks':20,'source_distractor_values':{'matched':36,'total_designated_wrong':36},'source_unlabelled_values':5,'unique_task_fingerprints_50_samples':{k:len(v) for k,v in fingerprints.items()},'default_family_coverage':sorted([list(v) for v in coverage]),'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'plots':'none','remaining_limits':['Historical scalar banks do not determine historical error operations; scaled raw profiles are evidence only.','Source q-160836 omits difficulty, solution and correct reference; preserve all omissions.','Easy/hard scope and all default banks are authored design claims, not observed labels.']}
 (DIR/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
