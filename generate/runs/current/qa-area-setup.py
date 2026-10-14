"""Root actual coordinate derivatives, two separate substitution factors and banks."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186133896;D=R.parents[2]/f'generate/scratch/{K}'
def load(p,n):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','area_setup_root');t=p.t
fidelity=load(R/'root-source-fidelity.py','area_setup_fidelity');g=load(D.with_suffix('.py'),'area_setup_g');originals,S=fidelity.check(g,K,D)
def math(z):return p.scalar(z.strip().rstrip('.,'))
def eq(a,b):
 a,b=[s.powsimp(s.expand(z),combine='exp',force=True) for z in (a,b)]
 return s.trigsimp(s.expand(a-b))==0
def braces(text,pos):
 assert text[pos]=='{';start=pos+1;depth=1;pos+=1
 while depth:depth+=(text[pos]=='{')-(text[pos]=='}');pos+=1
 return text[start:pos-1],pos
def integral(text,start):
 pos=start;bounds=[]
 for symbol in ('_','^'):
  assert text[pos]==symbol;pos+=1
  if text[pos]=='{':body,pos=braces(text,pos)
  else:body=text[pos];pos+=1
  bounds.append(math(body))
 ends=[q for suffix in (r'\,dt',r'\,\mathrm{d}t') if (q:=text.find(suffix,pos))>=0];assert ends
 return bounds,text[pos:min(ends)]
def evaluate(expr,lo,hi):
 if expr.has(s.exp):
  val=s.integrate(expr,(t,lo,hi));return val
 return s.simplify(s.integrate(s.expand_trig(expr),(t,lo,hi)))
C=dict(records=0,actual_coordinates=0,actual_coordinate_derivatives=0,closure_checks=0,orientation_checks=0,integral_bounds=0,substitution_factors=0,collected_integrands=0,choices=0,bank_pointwise_pairs=0,bank_integral_pairs=0,method_banks=0,source_prose_masks=0,actual_plot_samples=0,actual_arrow_tangents=0,easy_domain_instances=0)
records=json.load(open(R/f'qa/{K}-sampled.json'))
for family,(level,sid,_) in g.TEMPLATES.items():records.extend(g.generate(level,template=family,seed=n) for n in (631,917))
records.append(g.generate_easy(parameters={'a':20,'b':20}))
for index,rec in enumerate(records):
 if index%10==0:print('readback',index,rec['generation']['template'],flush=True)
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];coords=[math(z) for z in re.search('⟨(.*?)⟩',prompt)[1].replace(r'\,','').split(',')];X,Y=coords;dx,dy=s.diff(X,t),s.diff(Y,t);bounds=[math(z) for z in re.search(r'for \$t.*?\[(.*?)\]',prompt)[1].split(',')];lo,hi=bounds;P=-Y if '$P(x,y)=-y$' in prompt else 0;Q=X if '$Q(x,y)=x' in prompt else 0;orientation=-1 if 'negatively oriented' in sol else 1;expected=s.trigsimp(orientation*(P*dx+Q*dy));C['actual_coordinates']+=2
 derivative=[math(z) for z in re.search('⟨(.*?)⟩',sol)[1].replace(r'\,','').split(',')];assert eq(derivative[0],dx) and eq(derivative[1],dy);C['actual_coordinate_derivatives']+=2
 for coordinate in coords:assert eq(coordinate.subs(t,lo),coordinate.subs(t,hi));C['closure_checks']+=1
 import mpmath as mp
 with mp.workdps(35):signed=mp.quad(s.lambdify(t,X*dy,'mpmath'),[mp.mpf(str(s.N(lo,35))),mp.mpf(str(s.N(hi/2,35))),mp.mpf(str(s.N(hi,35)))])
 assert signed*orientation>mp.mpf('1e-20');C['orientation_checks']+=1
 chain=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[-1];assert len(chain.split(chr(92)*2))==2
 items=[]
 for m in re.finditer(r'\{\\int \}|\\int(?=_)',chain):
  bs,body=integral(chain,m.end());assert all(eq(a,b) for a,b in zip(bs,bounds));C['integral_bounds']+=2;items.append(body)
 assert len(items)==2
 factors=items[0].split(r'\cdot');assert len(factors)==2
 want=[orientation*(P if P!=0 else Q),dx if P!=0 else dy]
 for factor,value in zip(factors,want):assert eq(math(factor),value);C['substitution_factors']+=1
 assert eq(math(items[1]),expected);C['collected_integrands']+=1
 f=q[':question/answer-fields'][0];values=[math(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5
 assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if eq(v,expected)]==[f[':answer-field/correct'][1]]
 coordinate=Y if P!=0 else X;first=orientation*(P if P!=0 else Q);scale=coordinate.subs(t,s.pi/2 if P==0 and family not in ('ellipse_ccw','exp_ccw','exp_cw','double_cos') else 0)
 # Coefficient scale is recovered from the actual coordinate's normalized shape,
 # never from generation metadata.
 scale=abs(s.factor(coordinate).as_coeff_Mul()[0])
 if family.startswith('exp'):scale=s.expand(coordinate).as_coeff_Mul()[0]
 want=[expected,-expected,expected/scale,2*expected,first*(X if P!=0 else Y)]
 assert all(sum(eq(v,w) for w in want)==1 for v in values),(family,coords,scale,values,want);C['choices']+=5;C['method_banks']+=1
 for a,b in itertools.combinations(values,2):assert not eq(a,b);C['bank_pointwise_pairs']+=1
 # Quadrature is independent of the worker's Bessel identity shortcut; verify
 # every pair of complete integrals to bounded high precision on actual curves.
 import mpmath as mp
 with mp.workdps(35):
  vals=[mp.quad(s.lambdify(t,v,'mpmath'),[mp.mpf(str(s.N(lo,35))),mp.mpf(str(s.N(hi/2,35))),mp.mpf(str(s.N(hi,35)))]) for v in values]
  for a,b in itertools.combinations(vals,2):assert abs(a-b)>mp.mpf('1e-20');C['bank_integral_pairs']+=1
 data=json.load(open(rec['generation']['plots']['data']));assert data['orientation']==orientation
 import numpy as np
 tv=np.array(data['samples']['t']);assert np.allclose(s.lambdify(t,X,'numpy')(tv),data['samples']['x'],atol=1e-8) and np.allclose(s.lambdify(t,Y,'numpy')(tv),data['samples']['y'],atol=1e-8);C['actual_plot_samples']+=2*len(tv)
 for arrow in data['arrows']:
  assert arrow['t_end']>arrow['t_start']
  for tag,point in [('t_start','start'),('t_end','end')]:
   assert abs(float(X.subs(t,arrow[tag]))-arrow[point][0])<1e-8 and abs(float(Y.subs(t,arrow[tag]))-arrow[point][1])<1e-8
  C['actual_arrow_tangents']+=1
 old=originals.get(rec['generation']['source_id'])
 if old and ':question/worked-solution' in old and family!='circle_cw':
  clean=lambda z:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',z,flags=re.S)).strip();assert clean(sol)==clean(old[':question/worked-solution']);C['source_prose_masks']+=1
 for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S):assert len(block.split(chr(92)*2))>1
 C['records']+=1
fingerprints=set()
for radius in range(2,21):
 r=g.generate_easy(parameters={'a':radius,'b':radius});fingerprints.add(r['generation']['mathematical_fingerprint']);C['easy_domain_instances']+=1
assert len(fingerprints)==19
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
