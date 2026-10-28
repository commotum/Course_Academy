"""Complete mathematical component masks for source-style calculation chains.

The caller supplies exact objects. This file does not sample, select banks, or
introduce learner-facing helper variables. Stage labels remain author metadata.
"""
import sympy as s

def build(f,p,g,F,B,data,tex,signed_sum,component_sum,x,y):
 dx,dy,M,P,D,*rest=data;A=data[-1];lo,hi,yl,yh=B
 a=s.sympify(p.get('a',1));b=s.sympify(p.get('b',1));c=s.sympify(p.get('c',1));k=s.sympify(p.get('k',1))
 group=lambda v:r'\left('+v+r'\right)'
 metric=r'\sqrt{1+'+group(tex(dx))+r'^{2}+'+group(tex(dy))+r'^{2}}'
 dbl=lambda body,pref='':pref+r'{∬}_{D}'+body+r'\,\text{d}A'
 ix=lambda body,pref='':pref+r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'+body+r'\,\text{d}x'
 repeated=lambda body,pref='':ix(r'\int_{'+tex(yl)+'}^{'+tex(yh)+'}'+group(body)+r'\,\text{d}y',pref)
 bracket=lambda body,var,L,H:r'['+body+r']_{'+var+'='+tex(L)+'}^{'+var+'='+tex(H)+'}'
 points=lambda terms,var,L,H:group(signed_sum([v.subs(var,H) for v in terms])+'-'+group(signed_sum([v.subs(var,L) for v in terms])))
 formal=r'{∬}_{D}f(x,y,g(x,y))\sqrt{1+{(\frac{∂z}{∂x})}^{2}+{(\frac{∂z}{∂y})}^{2}}\,\text{d}A'
 rows=[('formal',formal)]
 def add(tag,value):rows.append((tag,value))
 def integral_tail(body,pref='',inner_endpoint=True):
  """The plane/expanded-polynomial source chain, keeping metric outside."""
  density=s.expand(body);iy=component_sum(density,y)
  O=s.simplify(sum(v.subs(y,yh)-v.subs(y,yl) for v in iy));ox=component_sum(O,x)
  add('repeated',repeated(tex(density),pref))
  add('inner_primitive',ix(bracket(signed_sum(iy),'y',yl,yh),pref))
  if inner_endpoint:add('inner_endpoints',ix(points(iy,y,yl,yh),pref))
  add('inner_reduced',ix(group(tex(O)),pref))
  add('outer_primitive',pref+bracket(signed_sum(ox),'x',lo,hi))
  add('outer_endpoints',pref+points(ox,x,lo,hi))
  add('final',tex(A))
 if f in ('canonical_cancel','constant_plane'):
  if f=='canonical_cancel':
   numerator=tex(c);rad=1+2*y*y
   add('substitution',dbl(r'\frac{'+numerator+r'}{\sqrt{'+group(tex(g))+'-x+y^{2}}}'+metric))
   add('metric_expansion',dbl(r'\frac{'+numerator+r'}{\sqrt{'+tex(rad)+r'}}\sqrt{'+tex(2*rad)+'}'))
   add('root_factoring',dbl(r'\frac{'+numerator+r'}{\sqrt{'+tex(rad)+r'}}\sqrt{2'+group(tex(rad))+'}'))
   add('root_split',dbl(r'\frac{'+numerator+r'}{\sqrt{'+tex(rad)+r'}}\sqrt{2}\sqrt{'+tex(rad)+'}'))
   add('cancellation',dbl(r'\frac{'+numerator+r'}{\cancel{\sqrt{'+tex(rad)+r'}}}\sqrt{2}\cancel{\sqrt{'+tex(rad)+'}}'))
  else:add('substitution',dbl(tex(c)+metric))
  add('constant_density',dbl(tex(D)))
  add('outside_constant',dbl('',tex(D)))
  add('area',tex(D)+r'\cdot\text{Area}(D)')
  add('endpoint_widths',tex(D)+r'\cdot'+group(tex(hi)+'-'+group(tex(lo)))+r'\cdot'+group(tex(yh)+'-'+group(tex(yl))))
  add('evaluated_widths',tex(D)+r'\cdot'+group(tex(hi-lo))+r'\cdot'+group(tex(yh-yl)))
  add('final',tex(A))
 elif f=='plane_log':
  # Source: numerator cancellation, reciprocal-y primitive, natural-log endpoints.
  numerator=group(tex(a*x+b*y))+'-'+group(tex(b*y))
  add('substitution',dbl(r'\frac{'+('' if c==1 else group(tex(c)))+group(numerator)+'}{'+group(tex(M))+r'y}'+metric))
  add('cancellation',dbl(tex(D)))
  add('repeated',repeated(tex(D)))
  add('inner_primitive',ix(group(tex(c*a*x))+bracket(r'\ln y','y',yl,yh)))
  add('inner_endpoints',ix(group(tex(c*a*x))+group(tex(s.log(yh))+'-'+group(tex(s.log(yl))))))
  O=s.simplify(c*a*x*k);ox=component_sum(O,x)
  add('inner_reduced',ix(tex(O)))
  add('outer_primitive',bracket(signed_sum(ox),'x',lo,hi))
  add('outer_endpoints',points(ox,x,lo,hi))
  add('final',tex(A))
 elif f=='reciprocal_triangle':
  add('substitution',dbl(r'\frac{'+tex(c)+r'}{\sqrt{3}'+group(tex(g))+r'^{2}}'+metric))
  add('repeated',repeated(r'\frac{'+tex(c)+'}{'+group(tex(g))+r'^{2}}'))
  iy=-c/(k+x+y)
  add('inner_primitive',ix(bracket(tex(iy),'y',yl,yh)))
  add('inner_endpoints',ix(points([iy],y,yl,yh)))
  ox=[-c*s.log(k+x),c*x/k]
  add('outer_primitive',bracket(signed_sum(ox),'x',lo,hi))
  add('outer_endpoints',points(ox,x,lo,hi))
  terms=list(s.Add.make_args(s.expand_log(A,force=True)));logs=[v for v in terms if v.has(s.log)];constants=[v for v in terms if not v.has(s.log)]
  logs.sort(key=lambda v:(bool(v.as_coeff_Mul()[0]<0),str(v)))
  output=''
  for term in logs+constants:
   negative=term.could_extract_minus_sign();body=tex(-term if negative else term);output+=('-' if negative else '+' if output else '')+body
  add('log_split',output)
 elif f=='trig_triangle':
  rad=1+2*s.cos(x+y)**2
  add('substitution',dbl(r'\frac{'+tex(c*s.sin(x+y))+r'}{\sqrt{'+tex(rad)+'}}'+metric))
  add('cancellation',dbl(r'\frac{'+tex(c*s.sin(x+y))+r'}{\cancel{\sqrt{'+tex(rad)+r'}}}\cancel{\sqrt{'+tex(rad)+'}}'))
  add('reduced',dbl(tex(D)))
  add('repeated',repeated(tex(D)))
  iy=-c*s.cos(x+y);O=s.simplify(iy.subs(y,yh)-iy.subs(y,yl));ox=[c*x,-c*s.sin(2*x)/2]
  add('inner_primitive',ix(bracket(tex(iy),'y',yl,yh)))
  add('inner_reduced',ix(group(tex(O))))
  add('outer_primitive',bracket(signed_sum(ox),'x',lo,hi))
  add('outer_endpoints',points(ox,x,lo,hi))
  add('final',tex(A))
 elif f=='paraboloid_xy':
  rad=1+4*x*x+4*y*y
  add('substitution',dbl(r'\frac{'+tex(c*x*y)+r'}{\sqrt{'+tex(g)+'}}'+metric))
  add('metric_expansion',dbl(r'\frac{'+tex(c*x*y)+r'}{\sqrt{'+tex(g)+r'}}\sqrt{'+tex(rad)+'}'))
  add('root_factoring',dbl(r'\frac{'+tex(2*c*x*y)+r'}{\sqrt{'+tex(rad)+r'}}\sqrt{'+tex(rad)+'}'))
  add('cancellation',dbl(r'\frac{'+tex(2*c*x*y)+r'}{\cancel{\sqrt{'+tex(rad)+r'}}}\cancel{\sqrt{'+tex(rad)+'}}'))
  add('reduced',dbl(tex(D)))
  integral_tail(D)
 elif f=='plane_ratio':
  add('substitution',dbl(r'\frac{'+tex(c)+group(tex(g))+'}{'+group(tex(a*M))+r'x}'+metric))
  add('numerator_factoring',dbl(group(tex(M))+r'\frac{'+group(tex(c*a))+group('x+'+group(tex(b/a))+r'y')+'}{'+group(tex(a*M))+r'x}'))
  add('cancellation',dbl(r'\frac{'+group(tex(c))+group('x+'+group(tex(b/a))+r'y')+'}{x}'))
  integral_tail(D)
 elif f=='plane_sine':
  add('substitution',dbl(tex(P)+metric))
  add('outside_metric',dbl(tex(P),tex(M)))
  add('repeated',repeated(tex(P),tex(M)))
  iy=-c*a*x*s.cos(y);O=s.simplify(iy.subs(y,yh)-iy.subs(y,yl));ox=component_sum(O,x)
  add('inner_primitive',ix(bracket(tex(iy),'y',yl,yh),tex(M)))
  add('inner_endpoints',ix(group(tex(-c*a*x))+group(tex(s.cos(yh))+'-'+group(tex(s.cos(yl)))),tex(M)))
  add('inner_reduced',ix(tex(O),tex(M)))
  add('outer_primitive',tex(M)+bracket(signed_sum(ox),'x',lo,hi))
  add('outer_endpoints',tex(M)+points(ox,x,lo,hi))
  add('final',tex(A))
 elif f in ('cross_cancel','quadratic_triangle','quadratic_rectangle_full','quadratic_triangle_full'):
  pieces=([tex(2*a*b*x*y)] if f=='cross_cancel' else [tex(x*x)])
  if f.endswith('_full'):pieces.append(tex(x*y))
  pieces += [tex(a*a*x*x),tex(b*b*y*y),tex(-2*a*b*x*y)]
  expanded=('' if c==1 else group(tex(c)))+group('+'.join('('+v+')' for v in pieces))
  add('substitution',dbl(group(tex(P))+metric))
  if f in ('quadratic_triangle','quadratic_triangle_full'):
   add('square_expansion',dbl(expanded+r'\sqrt{'+tex(1+a*a+b*b)+'}'))
  else:add('square_expansion',dbl(expanded,tex(M)))
  body=s.expand(P)
  add('cross_cancellation' if f=='cross_cancel' else 'collection',dbl(group(tex(body)),tex(M)))
  if f in ('quadratic_triangle','quadratic_triangle_full'):
   iy=component_sum(body,y);O=s.simplify(sum(v.subs(y,yh)-v.subs(y,yl) for v in iy))
   add('repeated',repeated(tex(body),tex(M)))
   add('inner_primitive',ix(bracket(signed_sum(iy),'y',yl,yh),tex(M)))
   add('inner_endpoints',ix(points(iy,y,yl,yh),tex(M)))
   add('inner_reduced',ix(group(tex(O)),tex(M)))
   add('constant_collection',ix(tex(3*O),tex(M/3)))
   ox=component_sum(3*O,x)
   add('outer_primitive',tex(M/3)+bracket(signed_sum(ox),'x',lo,hi))
   add('outer_endpoints',tex(M/3)+points(ox,x,lo,hi))
   add('final',tex(A))
  else:integral_tail(body,tex(M))
 else:
  # q-160836 lacks a source solution; its authored polynomial chain follows
  # q-161341. Linear-plane metric moves outside only at the primitive stage.
  add('substitution',dbl(group(tex(P))+metric))
  add('repeated',repeated(tex(s.expand(P)*M)))
  iy=component_sum(s.expand(P),y);O=s.simplify(sum(v.subs(y,yh)-v.subs(y,yl) for v in iy));ox=component_sum(O,x)
  add('inner_primitive',ix(bracket(signed_sum(iy),'y',yl,yh),tex(M)))
  add('inner_endpoints',ix(points(iy,y,yl,yh),tex(M)))
  add('inner_reduced',ix(group(tex(O)),tex(M)))
  add('outer_primitive',tex(M)+bracket(signed_sum(ox),'x',lo,hi))
  add('outer_endpoints',tex(M)+points(ox,x,lo,hi))
  add('final',tex(A))
 lhs=r'{∬}_{S}'+integrand_tex(f,p,F,data,tex,x,y)+r'\,\text{d}S'
 aligned=r'\begin{aligned}'+lhs+' & ='+rows[0][1]+''.join(r'\\ & ='+value for _,value in rows[1:])+r'.\end{aligned}'
 return aligned,[tag for tag,_ in rows]

def integrand_tex(f,p,F,data,tex,x,y):
 z=s.Symbol('z',real=True);c=s.sympify(p.get('c',1));a=s.sympify(p.get('a',1));b=s.sympify(p.get('b',1));M=data[2]
 group=lambda value:r'\left('+value+r'\right)'
 scaled=lambda value:value if c==1 else tex(c)+group(value)
 if f=='trig_triangle':return r'\frac{'+tex(c*z)+r'}{\sqrt{'+tex(1+2*s.cos(x+y)**2)+'}}'
 if f=='paraboloid_xy':return r'\frac{'+tex(c*x*y)+r'}{\sqrt{z}}'
 if f=='plane_log':return r'\frac{'+scaled('z-'+group(tex(b*y)))+'}{'+group(tex(M))+r'y}'
 if f=='plane_ratio':return r'\frac{'+tex(c*z)+'}{'+group(tex(a*M))+r'x}'
 if f=='reciprocal_triangle':return r'\frac{'+tex(c)+r'}{\sqrt{3}z^{2}}'
 if f=='canonical_cancel':return r'\frac{'+tex(c)+r'}{\sqrt{z-x+y^{2}}}'
 return group(tex(F)) if f in ('cross_cancel','quadratic_triangle','quadratic_rectangle_full','quadratic_triangle_full') else tex(F)
