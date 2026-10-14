"""Root actual components and real restrictions, full mathematical/graph banks."""
import json,re,sys,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186172086;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 q=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(q);sys.modules[name]=m;q.loader.exec_module(m);return m
base=load(R/'qa-parametric-scalar-line.py','domain_root_base');p=load(R/'domain-math-parser.py','domain_root_math');x,y=p.x,p.y;rho=x*x+y*y

def math(raw):return p.scalar(raw.replace(r'\operatorname{arctan}','atan').strip().rstrip('.,'))
def restrictions(expr):
 cs=[]
 for atom in s.preorder_traversal(expr):
  if atom.func==s.log:cs.append(s.Gt(atom.args[0],0))
  if atom.is_Pow and atom.exp.is_Rational:
   if atom.exp.q%2==0:cs.append((s.Gt if atom.exp<0 else s.Ge)(atom.base,0))
   elif atom.exp<0:cs.append(s.Ne(atom.base,0))
 return [c for c in cs if c is not s.true]

def relation(raw):
 raw=raw.replace(r'\,','').strip().rstrip('.,')
 if raw.startswith('(x,y)'+r'\ne'):return [s.Ne(rho,0)]
 if r'\pm' in raw:
  left,rhs=raw.split(r'\pm',1);op=r'\ne' if r'\ne' in left else '=';lhs=left.split(op)[0];aa,bb=math(lhs),math(rhs)
  return [s.Ne(aa,bb),s.Ne(aa,-bb)] if op!= '=' else [s.Or(s.Eq(aa,bb),s.Eq(aa,-bb))]
 parts=re.split(r'(\\ge|\\le|\\ne|>|<|=)',raw);assert len(parts)>=3,raw;ops={r'\ge':s.Ge,r'\le':s.Le,r'\ne':s.Ne,'>':s.Gt,'<':s.Lt,'=':s.Eq};return [ops[parts[i]](math(parts[i-1]),math(parts[i+1])) for i in range(1,len(parts),2)]
def domain(raw):
 if r'\text{all real }' in raw or raw.strip()==r'{R}^{2}':return []
 if '|' not in raw:raise AssertionError(('No set criterion',raw))
 raw=raw.split('|',1)[1].strip().rstrip('.')
 if raw.endswith(r'\}'):raw=raw[:-2]
 elif raw.endswith('}'):raw=raw[:-1]
 # A point-tuple exclusion has an internal comma, so keep it intact.
 pieces=raw.split(r',\,');out=[]
 for piece in pieces:out+=relation(piece)
 return out

def graph(g):
 shape=g['shape']
 if shape=='plane':return [s.Ne(rho,0)] if g.get('puncture') else [s.Ne(y,g['line']*x)] if g.get('line') else []
 if shape=='halfplane':return [s.Gt(y-g['m']*x,0)]
 if shape=='strip_x':return [s.Lt(x*x,g['a']**2)]
 if shape=='strip_y':return [s.Le(s.Abs(y),g['b'])]
 if shape=='rectangle':
  lo=-g['b'] if g.get('lower') is None else g['lower'];return [(s.Le if g['cx'] else s.Lt)(s.Abs(x),g['a']),(s.Ge if g.get('lower_closed',g['cy']) else s.Gt)(y,lo),(s.Le if g['cy'] else s.Lt)(y,g['b'])]
 assert shape=='disk';cs=[(s.Le if g['closed'] else s.Lt)(rho,g['r2'])]
 if g.get('puncture'):cs.append(s.Ne(rho,0))
 if g.get('line'):cs.append(s.Ne(y,g['line']*x))
 if g.get('side'):op,m=g['side'];cs.append({'ge':s.Ge,'gt':s.Gt,'lt':s.Lt}[op](y,m*x))
 return cs

def points(groups):
 pts=set(itertools.product([s.Rational(k,2) for k in range(-14,15)],repeat=2))
 for cs in groups:
  for c in cs:
   if c in (s.true,s.false):continue
   for rel in c.atoms(s.core.relational.Relational):
    f=rel.lhs-rel.rhs
    for axis,other in ((x,y),(y,x)):
     for v in (0,1,-1,2,-2,s.Rational(1,4),-s.Rational(1,4),s.Rational(1,2),-s.Rational(1,2)):
      for root in s.solve(f.subs(other,v),axis):
       if root.is_real and root.is_number:
        for delta in (-s.Rational(1,10),0,s.Rational(1,10)):pts.add((root+delta,v) if axis==x else (v,root+delta))
 return sorted(pts,key=str)
def truth(cs,pt):return tuple(bool(c.subs({x:pt[0],y:pt[1]})) for c in cs)
def signature(cs,pts):return tuple(all(truth(cs,pt)) for pt in pts)
def image_domain(path):
 path=Path(path);d=json.loads(path.with_suffix('.json').read_text());assert path.exists() and d['equal_aspect'] and d['png_sha256']==hashlib.sha256(path.read_bytes()).hexdigest();return graph(d['geometry'])
C={k:0 for k in ('records','actual_components','component_definitions','component_domains','solved_relations','intersection_domains','choice_domains','whole_banks','exact_boundary_probes','solution_plots','choice_plots')}
def check(rec):
 q=rec['question'];text=q[':question/problem'];sol=q[':question/worked-solution'];raw=re.search(r'\$\$\s*F\(x,y\)=(.*?)\$\$',text,re.S)[1].strip().removesuffix('.');rawP,rawQ=re.fullmatch(r'(.*?)\\,i\+(.*?)\\,j(?:\\,)?',raw,re.S).groups();P=math(rawP);cp=list(p.last_domain);Q=math(rawQ);cq=list(p.last_domain);actual=[[c for c in cs if c is not s.true] for cs in (cp,cq)];C['actual_components']+=2
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);definitions=next(v for v in blocks if v.startswith('P(x,y)='));a,b=definitions.split(r',\,Q(x,y)=');pa=math(a.split('=',1)[1]);ca=list(p.last_domain);qb=math(b);cb=list(p.last_domain);assert s.simplify(pa-P)==0 and s.simplify(qb-Q)==0;pp=points(actual+[ca,cb]);assert all(signature(a,pp)==signature(b,pp) for a,b in zip(actual,(ca,cb)));C['component_definitions']+=2
 f=q[':question/answer-fields'][0];banks=[]
 for a in f[':answer-field/choices']:
  if a[':answer/type']==':answer.type/image':banks.append(image_domain(a[':answer/value']));C['choice_plots']+=1
  else:banks.append(domain(a[':answer/value']))
 pts=points(actual+banks);target=signature(actual[0]+actual[1],pts);sigs=[signature(b,pts) for b in banks];assert len(set(sigs))==5 and sigs.count(target)==1,(rec['generation']['template'],P,Q,actual,banks,len(set(sigs)),sigs.count(target));assert f[':answer-field/choices'][sigs.index(target)][':answer/id']==f[':answer-field/correct'][1],(rec['generation']['template'],P,Q,actual,banks,sigs.index(target),[i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]]);C['choice_domains']+=5;C['whole_banks']+=1;C['exact_boundary_probes']+=len(pts)
 if any(v.startswith('{D}_{1}=') for v in blocks):
  ds=[]
  for n in (1,2):
   body=next((v.split('=',1)[1] for v in blocks if v.startswith('{D}_{'+str(n)+'}=')),None)
   if body is None:assert n==2 and r'{D}_{2}={R}^{2}' in sol;body=r'{R}^{2}'
   ds.append(domain(body))
  pp=points(actual+ds)
  for a,b in zip(actual,ds):assert signature(a,pp)==signature(b,pp);C['component_domains']+=1
  final=next(v for v in blocks if v.startswith('D='));dd=domain(final.split('=',2)[2].replace(r'\,.',''));pp=points([actual[0]+actual[1],dd]);assert signature(actual[0]+actual[1],pp)==signature(dd,pp);C['intersection_domains']+=1
 else:
  ims=re.findall(r'!\[\]\((.*?)\)',sol);assert len(ims)==3
  for path,a in zip(ims,actual+[actual[0]+actual[1]]):
   dd=image_domain(path);pp=points([a,dd]);assert signature(a,pp)==signature(dd,pp);C['solution_plots']+=1
 for block in blocks:
  if '⟹' in block:
   a,b=block.split('⟹');a,b=relation(a),relation(b);pp=points([a,b]);assert signature(a,pp)==signature(b,pp);C['solved_relations']+=1
 assert sol.startswith('The function $F$ can be expressed') and 'We first find the domain of each component function.' in sol;C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_domain_gen');source=base.raw(g,K,D);records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for fam,(lev,sid) in g.TEMPLATES.items():records.append(g.generate(lev,template=fam,seed=643))
 for rec in records:check(rec)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
