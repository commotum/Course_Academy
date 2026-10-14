"""Root all printed Green area segments, primitive derivatives and endpoints."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186133897;D=R.parents[2]/f'generate/scratch/{K}'
def load(p,n):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_areval');t,u=p.t,p.u
fidelity=load(R/'root-source-fidelity.py','root_areval_fidelity');g=load(D.with_suffix('.py'),'root_areval_g');originals,S=fidelity.check(g,K,D)
def eq(a,b):return s.simplify(s.trigsimp(a-b))==0
def math(z):
 z=z.strip().rstrip('.,').replace(r'\text{d}','').replace(r'\text{ }','').replace(r'\:','').replace(r'\mathrm{d}','').replace(r'\textrm d','').replace(r'\limits','')
 if z in ('','+','-'):return s.Integer(-1 if z=='-' else 1)
 return p.scalar(z)
def group(text,pos,opening='{',closing='}'):
 assert text[pos]==opening;start=pos+1;depth=1;pos+=1
 while depth:depth+=(text[pos]==opening)-(text[pos]==closing);pos+=1
 return text[start:pos-1],pos
def bounds(text,pos):
 out=[]
 for op in ('_','^'):
  assert text[pos]==op;pos+=1
  if text[pos]=='{':body,pos=group(text,pos)
  else:body=text[pos];pos+=1
  out.append(math(body))
 return out,pos
def scalarrow(z):
 z=z.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\text{d}','d').replace(r'\mathrm{d}','d').replace(r'\textrm d','d').replace(r'{\int }',r'\int').replace(r'{\int}',r'\int').replace('_0','_{0}')
 while r'\int' in z:
  pos=z.index(r'\int');bs,start=bounds(z,pos+len(r'\int'));end=re.search(r'd([tu])',z[start:]);assert end,(z,start);axis={'t':t,'u':u}[end[1]];value=s.integrate(math(z[start:start+end.start()]),(axis,*bs));z=z[:pos]+'('+s.latex(value)+')'+z[start+end.end():]
 while '[' in z:
  pos=z.index('[');body,end=group(z,pos,'[',']');bs,end=bounds(z,end);primitive=math(body);axis=t if primitive.has(t) else u;value=primitive.subs(axis,bs[1])-primitive.subs(axis,bs[0]);z=z[:pos]+'('+s.latex(value)+')'+z[end:]
 if '|' in z:
  # The source cubic convention coefficient*u^3|_-1^1.
  m=re.search(r'\{*u\}*\^\{?3\}?\}*\{?\|\}*',z);assert m,z;bs,end=bounds(z,m.end());z=z[:m.start()]+'('+s.latex(bs[1]**3-bs[0]**3)+')'+z[end:]
 return math(z)
def vector(z):
 z=z.replace(r'\langle','⟨').replace(r'\rangle','⟩')
 if '⟨' in z:return s.Matrix([math(v) for v in re.search('⟨(.*?)⟩',z)[1].split(',')])
 v=s.expand(math(z));assert v.subs({p.i:0,p.j:0})==0;return s.Matrix([v.coeff(p.i),v.coeff(p.j)])
C=dict(records=0,actual_coordinate_components=0,actual_coordinate_derivatives=0,segment_closure_components=0,separate_integrands=0,calculation_rows=0,primitive_derivatives=0,individual_endpoints=0,choices=0,whole_method_banks=0,source_stage_masks=0,source_shared_prose=0,plot_segment_components=0)
records=json.load(open(R/f'qa/{K}-sampled.json'))
for family,level in g.FAMILY_LEVEL.items():records.extend(g.generate(level,template=family,seed=n) for n in (631,917))
for rec in records:
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];chunks=re.findall(r'(?:r(?:_\{?[12]\}?)?\(t\)|\{r\}_\{[12]\}\(t\))\s*=([^$]+)\$',prompt);bs=re.findall(r't(?:\\in| ∈)\s*\[([^\]]+)\]',prompt);assert len(chunks)==len(bs) in (1,2);segments=[]
 for body,bound in zip(chunks,bs):
  v=vector(body);lo,hi=map(math,bound.split(','));segments.append((v[0],v[1],lo,hi));C['actual_coordinate_components']+=2
 signed=s.simplify(sum(s.integrate(X*s.diff(Y,t)-Y*s.diff(X,t),(t,lo,hi))/2 for X,Y,lo,hi in segments));orientation=s.sign(signed);area=abs(signed);assert orientation!=0
 for (X,Y,lo,hi),(nx,ny,nlo,nhi) in zip(segments,segments[1:]+segments[:1]):assert eq(X.subs(t,hi),nx.subs(t,nlo)) and eq(Y.subs(t,hi),ny.subs(t,nlo));C['segment_closure_components']+=2
 assert ('positively oriented' in sol)==(orientation==1);useX='$P(x,y)=0$' in sol
 integrands=[s.simplify(orientation*(X*s.diff(Y,t) if useX else -Y*s.diff(X,t))) for X,Y,lo,hi in segments];C['separate_integrands']+=len(segments)
 derivative_block=sol.split('The derivative',1)[1].split('Finally,',1)[0].split('Therefore,',1)[0];derivatives=re.findall(r'(?:\(t\)\s*(?:&\s*)?=)(.*?)(?=\\\\|\\end\{aligned\}|\.\$\$|\.\n)',derivative_block,re.S)
 assert len(derivatives)==len(segments),(family,derivatives)
 for body,(X,Y,lo,hi) in zip(derivatives,segments):assert eq(vector(body)[0],s.diff(X,t)) and eq(vector(body)[1],s.diff(Y,t));C['actual_coordinate_derivatives']+=2
 chain=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[-1];rows=[part.split('&',1)[1].strip().lstrip('=').strip() for part in chain.split(chr(92)*2) if '&' in part]
 for row in rows:
  if '∮' in row or r'\oint' in row:continue
  assert eq(scalarrow(row),area),(family,row,scalarrow(row),area);C['calculation_rows']+=1
 if family=='ellipse':
  primitive_row=next(row for row in rows if '[' in row);normalized=primitive_row.replace(r'\left','').replace(r'\right','');pos=normalized.index('[');body,end=group(normalized,pos,'[',']');primitive=math(body);assert eq(s.diff(primitive,t),integrands[0]);C['primitive_derivatives']+=1
  endpoint=rows[rows.index(primitive_row)+1].replace(r'\left','').replace(r'\right','');m=re.fullmatch(r'\((.*?)-(.*?)\)-\((.*?)-(.*?)\)',endpoint);assert m;coefs=[math(v) for v in m.groups()];parts=s.Add.make_args(primitive);linear=next(z for z in parts if z.has(t) and not z.has(s.sin));trig=primitive-linear;lo,hi=segments[0][2:];want=[linear.subs(t,hi),-trig.subs(t,hi),linear.subs(t,lo),-trig.subs(t,lo)];assert all(eq(a,b) for a,b in zip(coefs,want));C['individual_endpoints']+=4
 elif rec['question'][':question/difficulty'].endswith('/moderate'):
  # Actual trig substitution is displayed in prose; independently validate du,
  # reversed u endpoints, cubic primitive and both signed endpoint values.
  sub=re.search(r'substitution \$u=(.*?),',sol)[1];sub=math(sub);assert sub in (s.sin(t),s.cos(t))
  primrow=next(row for row in rows if '|' in row);m=re.search(r'\{*u\}*\^\{?3\}?',primrow);assert m;coefficient=math(primrow[:m.start()]);primitive=coefficient*u**3;assert eq(s.diff(primitive,u),s.Rational(3,2)*area*u*u);C['primitive_derivatives']+=1
  endpoint_row=rows[-3];m=re.fullmatch(r'(.*?)\\cdot 1-(.*?)\\cdot \(-1\)',endpoint_row);assert m;assert eq(math(m[1]),primitive.subs(u,1)) and eq(-math(m[2]),primitive.subs(u,-1));C['individual_endpoints']+=2
 else:
  primrow=next(row for row in rows if '[' in row);pos=primrow.index('[');body,end=group(primrow,pos,'[',']');primitive=math(primrow[:pos])*math(body);assert eq(s.diff(primitive,t),integrands[0]);C['primitive_derivatives']+=1
  endpoint=rows[rows.index(primrow)+2];m=re.fullmatch(r'(.*?)\\left\(\\frac\{1\}\{(\d+)\}-\\left\(-\\frac\{1\}\{(\d+)\}\\right\)\\right\)',endpoint);assert m,(family,endpoint);c=math(m[1]);assert eq(c/s.Integer(m[2]),primitive.subs(t,1)) and eq(-c/s.Integer(m[3]),primitive.subs(t,-1));C['individual_endpoints']+=2
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];values=[math(a[':answer/value']) for a in choices];assert len(values)==5 and all(not eq(a,b) for a,b in itertools.combinations(values,2));assert [a[':answer/id'] for a,v in zip(choices,values) if eq(v,area)]==[f[':answer-field/correct'][1]];C['choices']+=5
 # Verify complete operation banks from actual coordinate integrals.
 a=s.factor(segments[0][0]).as_coeff_Mul()[0];b=s.factor(segments[0][1]).as_coeff_Mul()[0];a,b=abs(a),abs(b)
 if family=='ellipse':wanted=[area,-area,2*area,a*s.pi,b*s.pi]
 elif q[':question/difficulty'].endswith('/moderate'):
  wanted=[area,2*a*b/3,4*a*b,-area,0]
  assert r'\operatorname{sin}⁡2t' in rows[0] and r'2\operatorname{sin}⁡t\operatorname{cos}⁡t' in rows[2]
  assert r'{u}^{2}' in rows[4] and r'_{1}^{-1}' in rows[4] and r'_{-1}^{1}' in rows[5]
  assert r'cos}^{2}' in rows[3] or r'sin}^{2}' in rows[3]
 else:
  n=2 if family in ('left_polynomial','right_polynomial') else 4;den=2*n+1
  wanted=[area,2*a*b/den,n*a*b,-area,2*n*a*b]
  assert '∪' in rows[0] or r'\cup' in rows[0]
  assert rows[2].count(r'{\int }')==2 and r'\cdot 0' in rows[2]
  assert rows[3].endswith(('-0','+0')) and '{t}^{'+str(2*n)+'}' in rows[3],(family,rows[3])
  assert str(den) in rows[4] and '[' in rows[4]
 assert all(sum(eq(v,w) for w in wanted)==1 for v in values),(family,values,wanted)
 C['whole_method_banks']+=1
 data=json.load(open(rec['generation']['plot'].replace('.png','.json')));assert data['orientation']==int(orientation) and len(data['segments'])==len(segments)
 for rendered,actual in zip(data['segments'],segments):
  for raw,value in zip(rendered,actual):assert eq(s.sympify(raw,locals={'t':t,'pi':s.pi}),value);C['plot_segment_components']+=1
 sid=rec['generation']['source_id'];o=next((q for q in originals.values() if str(q[':db/id'])==str(sid)),None)
 if o and ':question/worked-solution' in o:
  source=o[':question/worked-solution'];clean=lambda z:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',z,flags=re.S)).strip();source=source.replace('simple, smooth, closed','simple, piecewise-smooth, closed') if family in ('sin_sin2','sin2_minus_sin','sin2_cos','minus_cos_sin2') else source;assert clean(sol)==clean(source);C['source_shared_prose']+=1
  original_chain=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',source,re.S)[-1];assert len(chain.split(chr(92)*2))>=len(original_chain.split(chr(92)*2));C['source_stage_masks']+=1
 C['records']+=1
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
