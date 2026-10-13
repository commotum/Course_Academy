"""Independent parent: supplied partial, complete line relation, normals and direction."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','section_parser');axes=(p.x,p.y,p.z)
def scalar(t):
 t=t.strip().rstrip('.,:').replace(r'\dfrac',r'\frac').replace(r'\!', '').replace(r'\;', '')
 t=re.sub(r'\|([^|]+)\|',r'Abs(\1)',t)
 return p.scalar(t)
def eq(a,b):return s.simplify(a-b)==0
def vec(t):
 t=t.strip().rstrip('.,')
 if t.startswith('⟨'):return s.Matrix([scalar(v) for v in t[1:-1].split(',')])
 e=s.expand(scalar(t));v=s.Matrix([e.coeff(b) for b in (p.i,p.j,p.k)]);assert eq(e,sum(a*b for a,b in zip(v,(p.i,p.j,p.k))));return v
def parallel(a,b):return a!=s.zeros(3,1) and b!=s.zeros(3,1) and all(eq(v,0) for v in a.cross(b))
def spans(t):return re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',t,re.S)
def task(q):
 text=q[':question/problem'];m=re.search(r'plane\s*\$([xy])\s*=\s*(.*?)\$',text);assert m,text;hold=m[1];H=scalar(m[2]);m=re.search(r'and that\s*\$(.*?)\$',text);assert m;text=m[1];lhs,rhs=text.split('=',1);var=re.search(r'_\{?([xy])',lhs)[1];assert var!=hold;F=scalar(rhs)
 m=re.search(r'\$P\((.*?)\)\$',q[':question/problem'])
 if m:point=tuple(scalar(v) for v in m[1].split(','));assert len(point)==3
 else:
  m=re.search(r'with\s*\$([xy])\$-coordinate\s*\$(.*?)\$',q[':question/problem']);assert m and m[1]==var;V=scalar(m[2]);point=(V,H,0) if var=='x' else (H,V,0)
 assert eq(point['xy'.index(hold)],H);M=s.simplify(F.subs(dict(zip(axes,point)),simultaneous=True));assert M.is_real and not M.has(s.zoo,s.nan,s.oo);u=axes['xy'.index(var)];line=s.expand(M*(u-point['xy'.index(var)])+point[2]);direction=s.Matrix((1,0,M) if var=='x' else (0,1,M));return F,var,hold,point,M,line,direction
def equations(text):
 # Actual legacy doubled command bytes are decoded for mathematics only;
 # literal byte preservation is checked separately on original replay.
 text=text.replace(r'\\begin',r'\begin').replace(r'\\end',r'\end')
 text=re.sub(r'\\(?:begin|end)\{aligned\}','',text).replace(r'\{','').lstrip('{').replace('&','')
 rows=text.split(r'\\');out=[]
 for row in rows:
  if '=' not in row:continue
  lhs,rhs=row.split('=',1);out.append(scalar(lhs)-scalar(rhs))
 assert len(out)==2,(text,out);return out
def line_key(es):
 A,b=s.linear_eq_to_matrix(es,axes);assert A.rank()==2;return tuple(s.simplify(v) for v in A.row_join(b).rref()[0])
def line_of(value):return line_key(equations(value))
def raw(g,k):
 originals=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());counts=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,unrated=0)
 for c in cases:
  q0=next(q for q in originals if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));level=q0.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/'+c.get('difficulty',c.get('level','easy'))).split('/')[-1];q=g.generate(level,template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')))['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in q0),(k,c,key)
   if key in q and key!=':question/answer-fields':assert q[key]==(q0[key][':db/ident'] if isinstance(q0[key],dict) else q0[key]),(k,c,key)
  counts['prompts']+=1;counts['solutions']+=(':question/worked-solution' in q0);counts['unrated']+=(':question/difficulty' not in q0);assert len(q[':question/answer-fields'])==len(q0[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];vals=[a[':answer/value'] for a in f[':answer-field/choices']];assert sorted(vals)==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);counts['fields']+=1;counts['values']+=len(vals)
   if ':answer-field/correct' in f:
    value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);old=f0[':answer-field/correct'][':answer/value'];assert eq(scalar(value),scalar(old)) if k==17592186124437 else line_of(value)==line_of(old) if k==17592186124438 else parallel(vec(value),vec(old));counts['keys']+=1
 return counts
def replace_formal(text,F,var,point,M):
 def partial(m):
  assert m[1]==var;args=tuple(scalar(v) for v in m[2].split(','));assert len(args)==2;return '('+s.latex(F.subs(dict(zip(axes,args)),simultaneous=True),ln_notation=True)+')'
 text=re.sub(r'\{?f\}?_\{?([xy])\}?\(([^()]*)\)',partial,text)
 text=re.sub(r'f\(([^()]*)\)',lambda m:'('+s.latex(point[2])+')' if all(eq(a,b) for a,b in zip(tuple(scalar(v) for v in m[1].split(',')),point[:2])) else (_ for _ in ()).throw(AssertionError(m[0])),text)
 text=re.sub(r'z\{?\|\}?_\{\((.*?)\)\}',lambda m:'('+s.latex(point[2])+')',text)
 text=re.sub(r'\\frac\{∂z\}\{∂([xy])\}\{?\|\}?_\{\((.*?)\)\}',lambda m:'('+s.latex(M)+')' if m[1]==var and all(eq(a,b) for a,b in zip(tuple(scalar(v) for v in m[2].split(',')),point[:2])) else (_ for _ in ()).throw(AssertionError(m[0])),text)
 return text
def scalar_bank(t,F,X,Y,M):
 x,y=axes[:2];A=s.expand(F).coeff(x,2).coeff(y) if t in ('polynomial','monomial') else s.expand(F).coeff(x) if t=='linear' else s.simplify(s.expand(F).coeff(x)*y) if t.startswith('canonical_') else None;B=-s.expand(F).coeff(x).coeff(y,2) if t=='polynomial' else s.expand(F).coeff(s.cos(s.pi*y)) if t=='canonical_trig' else None
 if t=='linear':W=[A*X+Y,A*X,-Y,A*Y-X]
 elif t=='cos_sum':W=[Y*s.sin(X)+s.cos(Y),-s.cos(Y),Y,Y*s.sin(X)-s.cos(Y)]
 elif t=='sin_product':W=[-s.sin(X)+X*Y,s.sin(X),X*Y,s.sin(X)+X]
 elif t=='rational_radical':u=(X*X+1)/(X*X*Y*Y);v=Y*s.sqrt(X);W=[(X*X+1)/(X*X*Y)+v,u,v,u-v]
 elif t=='cos_shift':W=[s.sqrt(2)*X*s.cos(X*Y),X*s.cos(X*Y+s.pi/4),s.sqrt(2)*X,-s.sqrt(2)*X*s.cos(X*Y+s.pi/4)]
 elif t=='polynomial':W=[A*X*X*Y+B*X*Y*Y,A*X*X*Y,-B*X*Y*Y,A*Y*Y*X-B*Y*X*X]
 elif t=='monomial':W=[A*X*Y,A*Y*Y*X,A*X*X,A*(X*X+Y)]
 elif t=='log_exp':W=[Y*s.log(X)-s.exp(Y),2*Y*s.log(X),-s.exp(Y)/X,2*Y*s.log(X)+s.exp(Y)/X]
 elif t=='exp_cos':W=[Y,(X+Y)*s.exp(-s.cos(X*Y)),X+s.exp(s.cos(X*Y))*Y,(X+Y)*s.cos(X*Y)]
 elif t=='radical_ratio':u=s.sqrt(X*X-2*Y*Y);W=[u/(X-Y),u/Y,-u/Y,s.sqrt(X*X-Y*Y)/(Y-X)]
 elif t=='base_exp':
  powterm=next(v for v in F.atoms(s.Pow) if v.exp==x+y);A=powterm.base;u=A**(X+Y)*Y*(X*s.log(A)+1);W=[A**X*Y*(X*s.log(A)+1),-u,A**(X+Y)*Y*X*s.log(A),A**(X+Y)*Y*(X*s.log(A)+Y+1)]
 else:
  u=A*X/Y;v=-A*X*X*Y;w=B*s.cos(s.pi*Y) if t=='canonical_trig' else 0;W=[u-v+w,v+w,u+w,A*X+v+w]
 return [M]+W
def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','sectiong'+str(k));source=raw(g,k);records=json.loads((R/f'qa/{k}-sampled.json').read_text());seen={r['generation']['template'] for r in records}
 for c in json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text()):
  if c['template'] not in seen:
   records.append(g.generate(c.get('difficulty',c.get('level','moderate' if k==17592186124438 else 'hard')),seed=91,template=c['template']));seen.add(c['template'])
 stats=dict(records=0,scalar_stages=0,point_slope_stages=0,line_relations=0,normal_vectors=0,cross_product_stages=0,prose_vectors=0,choices=0,complete_banks=0)
 for r in records:
  q=r['question'];F,var,hold,point,M,line,direction=task(q);sol=q[':question/worked-solution'];u=axes['xy'.index(var)];u0=point['xy'.index(var)];H=point['xy'.index(hold)];wanted=line_key([axes['xy'.index(hold)]-H,p.z-line]);bs=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
  for span in spans(sol):
   for args in re.findall(r'P\((.*?)\)',span):assert len(args.split(','))==3 and all(eq(scalar(v),w) for v,w in zip(args.split(','),point)),(k,span,point)
   if re.fullmatch(r'[xy]\s*=.*',span):assert eq(scalar(span.split('=',1)[1]),point['xy'.index(span[0])]),(k,span,point)
   for axis,args in re.findall(r'\{?f\}?_\{?([xy])\}?\((.*?)\)',span):
    assert axis==var
    if args.replace(' ','')!='x,y':assert all(eq(scalar(v),w) for v,w in zip(args.split(','),point[:2])),(k,span,point)
  for row in bs[0].split(r'\\'):
   sides=row.replace('&','').split('=');assert len(sides)>=2
   for side in sides[1:]:assert eq(scalar(side),M),(k,r['generation']['template'],side,M);stats['scalar_stages']+=1
  if k!=17592186124437:
   for row in bs[1].split(r'\\'):
    row=replace_formal(row.replace('&',''),F,var,point,M);a,b=row.split('=',1);assert eq((scalar(a)-scalar(b)).subs(p.z,line),0),(k,r['generation']['template'],row,line);stats['point_slope_stages']+=1
   assert line_key(equations(bs[2]))==wanted;stats['line_relations']+=1
  if k==17592186124439:
   normals=[]
   for index,span in enumerate(spans(sol)):
    n=re.search(r'\{?n\}?_\{?([12])\}?=(.*)',span)
    if n:
     V=vec(n[2]);assert V!=s.zeros(3,1) and eq(V.dot(direction),0)
     expected=s.Matrix((0,1,0) if hold=='y' else (1,0,0)) if n[1]=='1' else s.Matrix((M,0,-1) if var=='x' else (0,M,-1))
     assert parallel(V,expected);normals.append(V);stats['normal_vectors']+=1
    m=re.fullmatch(r'(.*?)=0[.,]?',span)
    if m and not n and 'or ' not in span:
     try:E=scalar(m[1]);assert eq(E.subs(p.z,line).subs(axes['xy'.index(hold)],H),0)
     except (ValueError,AssertionError):raise AssertionError(('implicit plane prose',span))
   assert len(normals)==2 and parallel(normals[0].cross(normals[1]),direction);cross=normals[0].cross(normals[1]);crossblock=bs[-1]
   first=crossblock.split(r'\\')[0].split('=',1)[1];operands=first.split(r'\times');assert len(operands)==2 and [vec(t) for t in operands]==normals
   det=re.search(r'\\left\|\\begin\{aligned\}(.*?)\\end\{aligned\}\\right\|',sol,re.S);assert det;rows=det[1].split(r'\\');assert len(rows)==3;assert rows[0].replace(' ','')=='i&j&k';mat=[s.Matrix([scalar(v) for v in row.split('&')]) for row in rows[1:]];assert mat==normals
   # The determinant is nested in the cross-product aligned block, so read
   # its suffix separately instead of treating its matrix rows as equations.
   after=sol[det.end():].split(r'\end{aligned}',1)[0]
   for row in after.split(r'\\'):
    if '=' in row:assert vec(row.split('=',1)[1])==cross,(k,row,cross);stats['cross_product_stages']+=1
   for span in spans(sol):
    if '⟨' in span and not re.search(r'n.*_.*=',span):
     for v in re.findall(r'⟨[^⟩]+⟩',span):assert parallel(vec(v),direction),(k,span,direction);stats['prose_vectors']+=1
    if span.strip().startswith(('- i','- j','i ','j ','k ')):assert parallel(vec(span),direction);stats['prose_vectors']+=1
  for f in q[':question/answer-fields']:
   vals=[]
   for a in f[':answer-field/choices']:
    V=scalar(a[':answer/value']) if k==17592186124437 else line_of(a[':answer/value']) if k==17592186124438 else vec(a[':answer/value']);good=eq(V,M) if k==17592186124437 else V==wanted if k==17592186124438 else parallel(V,direction);assert good==(a[':answer/id']==f[':answer-field/correct'][1]),(k,r['generation']['template'],a,M,line,direction);vals.append(V);stats['choices']+=1
   if k==17592186124437:bank=scalar_bank(r['generation']['template'],F,*point[:2],M);matches=lambda a,b:eq(a,b)
   elif k==17592186124438:
    other=axes['xy'.index(hold)];actual=[line,-M*(u-u0)+point[2],M*(u+u0)+point[2] if u0!=0 else M*u-point[2],M*(u-u0),M*(other-H)+point[2]];bank=[line_key([other-H,p.z-e]) for e in actual[:-1]]+[line_key([u-u0,p.z-actual[-1]])];matches=lambda a,b:a==b
   else:bank=[direction,s.Matrix((1,0,-M) if var=='x' else (0,1,-M)),s.Matrix((M,0,1) if var=='x' else (0,M,1)),s.Matrix((0,1,0) if hold=='y' else (1,0,0)),s.Matrix((M,0,-1) if var=='x' else (0,M,-1))];matches=parallel
   assert len(vals)==5 and all(sum(matches(v,w) for v in vals)==1 for w in bank),(k,r['generation']['template'],vals,bank);stats['complete_banks']+=1
  stats['records']+=1
 out=dict(status='passed',kp_id=k,source=source,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
