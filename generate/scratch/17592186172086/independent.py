"""Independent displayed TeX parser and domain/option eligibility checks.

No import from the generator and no domain metadata used for correctness.
Converts only this family's deliberately bounded mathematical grammar.
"""
import copy, json, math, re, hashlib
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
X,Y=sp.symbols('x y',real=True)

def group(s,i):
 assert s[i]=='{';depth=1;j=i+1
 while depth:
  assert j<len(s),'unbalanced TeX';depth+=(s[j]=='{')-(s[j]=='}');j+=1
 return s[i+1:j-1],j

def expr(s):
 s=s.replace('⁡','').replace(r'\,','').replace(r'\left','').replace(r'\right','')
 s=s.replace(r'\operatorname{ln}',r'\ln').replace(r'\operatorname{arctan}',r'\arctan')
 out='';i=0
 while i<len(s):
  if s.startswith(r'\frac',i):
   i+=5;a,i=group(s,i);b,i=group(s,i);out+='(('+convert(a)+')/('+convert(b)+'))';continue
  if s.startswith(r'\sqrt',i):
   i+=5;a,i=group(s,i);out+='sqrt('+convert(a)+')';continue
  out+=s[i];i+=1
 out=out.replace(r'\ln','log').replace(r'\arctan','atan').replace('{e}','E').replace('^','**').replace('{','(').replace('}',')')
 out=re.sub(r'\|([^|]+)\|',r'Abs(\1)',out)
 out=re.sub(r'([xy\)])(?=(?:log|sqrt|atan|Abs)\()',r'\1*',out)
 assert '\\' not in out,'unsupported TeX '+out
 return parse_expr(out,local_dict={'x':X,'y':Y,'E':sp.E,'sqrt':sp.sqrt,'log':sp.log,'atan':sp.atan,'Abs':sp.Abs},transformations=standard_transformations+(implicit_multiplication_application,),evaluate=False)
def convert(s):return str(expr(s))

def restrictions(e):
 cs=[]
 for z in sp.preorder_traversal(e):
  if z.func==sp.log:cs.append(sp.Gt(z.args[0],0))
  if isinstance(z,sp.Pow):
   base,power=z.args
   if power.is_Rational:
    if power.q%2==0:cs.append(sp.Ge(base,0))
    if power<0:cs.append(sp.Ne(base,0))
 return cs

def relation(c):
 c=c.strip().rstrip('.');c=c.removeprefix(r'\,')
 c=c.replace(r'\geq',r'\ge').replace(r'\leq',r'\le').replace(r'\neq',r'\ne')
 if c.startswith('(x,y)'+r'\ne '):return [sp.Ne(X*X+Y*Y,0)]
 if r'\text{all real }' in c:return []
 # Chained scalar relation; pm is simultaneous exclusion of both lines.
 if r'\pm ' in c:
  if r'\ne \pm ' in c:
   a,b=c.split(r'\ne \pm ');return [sp.Ne(expr(a),expr(b)),sp.Ne(expr(a),-expr(b))]
  a,b=c.split(r'=\pm ');return [sp.Or(sp.Eq(expr(a),expr(b)),sp.Eq(expr(a),-expr(b)))]
 parts=re.split(r'(\\ge|\\le|\\ne|>|<|=)',c);assert len(parts)>=3,'no relation '+c
 cs=[]
 for i in range(1,len(parts),2):
  a,b=expr(parts[i-1]),expr(parts[i+1]);cs.append({'\\ge':sp.Ge,'\\le':sp.Le,'\\ne':sp.Ne,'>':sp.Gt,'<':sp.Lt,'=':sp.Eq}[parts[i]](a,b))
 return cs

def set_constraints(s):
 if '|' not in s and r'\text{all real }' in s:return []
 c=s.split('|',1)[1].rstrip('.').strip();c=c[:-1] if c.endswith('}') else c;return [z for part in c.split(r',\,') for z in relation(part)]

def truth(cs,a,b):
 try:return all(bool(c.subs({X:a,Y:b})) for c in cs)
 except TypeError as e:raise AssertionError('nonreal or unresolved predicate') from e

def test_points(cslist):
 pts={(sp.Rational(i,2),sp.Rational(j,2)) for i in range(-8,9) for j in range(-8,9)}
 # Include exact zero-boundary intersections; random-grid checks alone miss
 # open/closed boundaries with irrational circle radii.
 for cs in cslist:
  for c in [atom for cc in cs for atom in (list(cc.atoms(sp.core.relational.Relational)) if isinstance(cc,sp.Basic) else [])]:
   if c in (True,False,sp.true,sp.false):continue
   f=c.lhs-c.rhs
   for val in [0,1,-1,2,-2,sp.Rational(1,2),sp.Rational(-1,2)]:
    for var,other in [(X,Y),(Y,X)]:
     try:roots=sp.solve(f.subs(other,val),var)
     except (NotImplementedError,ValueError):continue
     for root in roots:
      if root.is_real is True and root.is_number:
       for offset in [sp.Rational(-1,2),0,sp.Rational(1,2)]:pts.add((root+offset,val) if var==X else (val,root+offset))
 return sorted(pts,key=str)

def equivalent(a,b,pts):return all(truth(a,*p)==truth(b,*p) for p in pts)

def graph_cs(g):
 r=X*X+Y*Y
 if g['shape']=='rectangle':
  lo=-g['b'] if g.get('lower') is None else g['lower'];return [(sp.Le if g['cx'] else sp.Lt)(sp.Abs(X),g['a']),(sp.Ge if g.get('lower_closed',g['cy']) else sp.Gt)(Y,lo),(sp.Le if g['cy'] else sp.Lt)(Y,g['b'])]
 if g['shape']=='plane':return [sp.Ne(r,0)] if g.get('puncture') else ([sp.Ne(Y,g['line']*X)] if g.get('line') else [])
 if g['shape']=='halfplane':return [sp.Gt(Y,g['m']*X)]
 if g['shape']=='strip_x':return [sp.Lt(X*X,g['a']**2)]
 if g['shape']=='strip_y':return [sp.Le(sp.Abs(Y),g['b'])]
 cs=[(sp.Le if g['closed'] else sp.Lt)(r,g['r2'])]
 if g.get('puncture'):cs.append(sp.Ne(r,0))
 if g.get('line'):cs.append(sp.Ne(Y,g['line']*X))
 if g.get('side'):
  op,m=g['side'];cs.append({'ge':sp.Ge,'gt':sp.Gt,'lt':sp.Lt}[op](Y,m*X))
 return cs

def balanced(s):
 assert all(ord(c)>=32 or c in '\n\t' for c in s),'C0 character in learner content'
 assert s.count('$')%2==0,'unbalanced math delimiters'
 depth=0
 for i,c in enumerate(s):
  if c in '{}' and (i==0 or s[i-1]!='\\'):
   depth+=1 if c=='{' else -1;assert depth>=0
 assert depth==0,'unbalanced TeX groups'

def components(prompt):
 equation=re.findall(r'\$\$\s*(.*?)\s*\$\$',prompt,re.S)[0]
 body=equation.split('F(x,y)=',1)[1];P,Q=body.split(r'\,i+',1);Q=Q.split(r'\,j',1)[0]
 return expr(P),expr(Q)

def check_record(r,allow_source=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];f=q[':question/answer-fields'][0];a=f[':answer-field/choices']
 for s in [q[':question/problem'],q.get(':question/worked-solution','')]+[z[':answer/value'] for z in a]:balanced(s)
 assert f[':answer-field/type']==':answer-field.type/radio' and len(a)==5
 assert len({z[':answer/id'] for z in a})==5
 assert f[':answer-field/correct'][0]==':answer/id'
 correct=next(z for z in a if z[':answer/id']==f[':answer-field/correct'][1])
 P,Q=components(q[':question/problem']);actual=restrictions(P)+restrictions(Q)
 displayed=[]
 for choice in a:
  if choice[':answer/type']==':answer.type/math':displayed.append(set_constraints(choice[':answer/value']))
  else:
   side=Path(choice[':answer/value']).with_suffix('.json');assert side.exists(),'generated graph sidecar missing';data=json.loads(side.read_text());g=data['geometry'];assert hashlib.sha256(Path(choice[':answer/value']).read_bytes()).hexdigest()==data['png_sha256'];visual_check(choice[':answer/value'],data);displayed.append(graph_cs(g))
 pts=test_points([actual]+displayed)
 # Numerical predicate evaluation does not assume symbolic simplification.
 signatures=[tuple(truth(cs,*p) for p in pts) for cs in displayed]
 assert len(set(signatures))==5,'equivalent complete choices'
 eligible=[i for i,cs in enumerate(displayed) if equivalent(actual,cs,pts)]
 assert len(eligible)==1,'actual displayed domain eligibility is not unique'
 assert a[eligible[0]][':answer/id']==correct[':answer/id'],'wrong correct designation'
 sol=q[':question/worked-solution'];rows=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
 comp=next(row for row in rows if row.startswith('P(x,y)='));pp,qq=comp.split(r',\,Q(x,y)=');pp=pp.split('=',1)[1];qq=qq.rstrip('.')
 assert sp.simplify(expr(pp)-P)==0 and sp.simplify(expr(qq)-Q)==0,'displayed component mismatch'
 if any(row.startswith('{D}_{1}=') for row in rows) and any(row.startswith('{D}_{2}=') for row in rows):
  d1=set_constraints(next(row.split('=',1)[1] for row in rows if row.startswith('{D}_{1}=')))
  d2=set_constraints(next(row.split('=',1)[1] for row in rows if row.startswith('{D}_{2}=')))
  pts2=test_points([restrictions(P),restrictions(Q),d1,d2]);assert equivalent(d1,restrictions(P),pts2) and equivalent(d2,restrictions(Q),pts2),'component domain stage incorrect'
 final=next((row for row in rows if row.startswith('D=')),None)
 if final:
  domain=set_constraints(final.split('=',2)[2].replace(r'\,.',''));pts3=test_points([actual,domain]);assert equivalent(actual,domain,pts3),'final domain incorrect'
 else:
  ims=re.findall(r'!\[\]\(([^)]+)\)',sol);assert len(ims)==3,'source diagram stage count changed'
  for path,cs in zip(ims,[restrictions(P),restrictions(Q),actual]):
   g=json.loads(Path(path).with_suffix('.json').read_text())['geometry'];pts3=test_points([cs,graph_cs(g)]);assert equivalent(cs,graph_cs(g),pts3),'solution graph domain incorrect'
 # Each operative solved row must be equivalent on its two displayed sides.
 for row in rows:
  if '⟹' in row:
   left,right=row.split('⟹');left=left.removesuffix(r'\,');right=right.removeprefix(r'\,').rstrip('.')
   aa,bb=relation(left),relation(right);pp=test_points([aa,bb]);assert equivalent(aa,bb,pp),'incorrect displayed solved condition'
 # Operative sequence must include the two stated component conditions before
 # the intersection; a mutation removing these stages is detected independently.
 assert sol.count('\n\n- The')==2 and sol.startswith('The function $F$ can be expressed')
 assert 'We first find the domain of each component function. Then, we compute their intersection' in sol
 assert 'Finally, the domain $D$ of $F$ is given by' in sol
 assert sol.count('solve the following inequality:')+sol.count('set it equal to zero and solve:')>= (1 if r'{D}_{2}={R}^{2}' in sol else 2)
 return {'points':len(pts),'unique_eligible_choice':True,'component_stage_match':True}


def visual_check(path,data):
 from PIL import Image
 image=Image.open(path).convert('RGB');g=data['geometry'];lim=data['limits'][1];bx,by,bw,bh=data['axes_bbox'];cs=graph_cs(g)
 scale=math.sqrt(g['r2']) if g['shape']=='disk' else max(g.get('a',1),g.get('b',1))
 xs=[scale*t for t in [-1.3,-.6,-.3,.3,.6,1.3]]
 ys=xs if g['shape']!='rectangle' else [g['b']*t for t in [-1.3,-.6,-.3,.3,.6,1.3]]
 tested=0
 for a in xs:
  for b in ys:
   # Ignore locations near any curve/axis stroke; compare interior shading.
   if abs(a)<.05 or abs(b)<.05:continue
   if g['shape']=='disk' and abs(a*a+b*b-g['r2'])<.12*scale:continue
   if g.get('line') and abs(b-g['line']*a)<.1*scale:continue
   if g.get('side') and abs(b-g['side'][1]*a)<.1*scale:continue
   if g['shape']=='rectangle' and (abs(abs(a)-g['a'])<.08 or abs(abs(b)-g['b'])<.08):continue
   u=round(bx+(a+lim)/(2*lim)*bw);vv=round(image.height-(by+(b+lim)/(2*lim)*bh))
   if not(2<=u<image.width-2 and 2<=vv<image.height-2):continue
   colors=[image.getpixel((u+i,vv+j)) for i in [-1,0,1] for j in [-1,0,1]]
   shaded=sum(1 for rr,gg,bb in colors if 205<=rr<=230 and 220<=gg<=245 and 230<=bb<=250)>=5
   expected=truth(cs,sp.Rational(str(a)),sp.Rational(str(b)))
   assert shaded==expected,'raster shading disagrees with actual geometric region'
   tested+=1
 assert tested>=8,'insufficient visual domain samples'


def check_source_geometry(record):
 data=json.loads((Path(__file__).parent/'plot-source-domains.json').read_text())['domains'];sid=record['generation']['source_id']
 if sid not in data:return 0
 assert len(record['generation']['geometry'])==5
 for i,(g,text) in enumerate(zip(record['generation']['geometry'],data[sid])):
  expected=[sp.sympify(text,locals={'x':X,'y':Y})];got=graph_cs(g);pts=test_points([expected,got]);assert equivalent(got,expected,pts),'source raster transcription mismatch '+sid+' choice '+str(i)
 return 5
