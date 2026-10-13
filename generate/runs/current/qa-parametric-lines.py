"""Parent actual-curve derivatives, complete line/intercept banks and every numeric stage."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
p=load(R/'ode-scalar-parser.py','paramlineparser');t,x,y=p.t,p.x,p.y
def scalar(raw):
 raw=raw.strip().rstrip('.,:').replace(r'\dfrac',r'\frac').replace(r'\!', '').replace(r'\;', '').replace('[','(').replace(']',')')
 return p.scalar(raw)
def eq(a,b):return s.simplify(s.trigsimp(a-b))==0
def blocks(text):return [m[1] or m[2] for m in re.finditer(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$(?!\$)',text,re.S)]
def relation(raw):
 a,b=raw.replace('&','').strip().rstrip('.,').split('=',1);return s.expand(scalar(a)-scalar(b))
def lk(e):
 poly=s.Poly(s.expand(e),x,y,domain='EX');assert poly.total_degree()==1,e;cs=[poly.coeff_monomial(x),poly.coeff_monomial(y),poly.coeff_monomial(1)];d=next(v for v in cs if v!=0);return tuple(s.simplify(v/d) for v in cs)
def point(raw):return tuple(scalar(v) for v in raw.strip().rstrip('.,')[1:-1].replace(r'\,','').split(','))
def task(q,normal):
 bs=blocks(q[':question/problem']);raw=next(b for b in bs if re.match(r'\s*x\s*=',b));raw=raw.replace(r'\qquad','').replace(r'\quad','').replace(r'\,','');m=re.match(r'\s*x\s*=(.*?),\s*y\s*=(.*?),',raw,re.S);assert m,raw;F,G=map(scalar,m.groups());us=[scalar(b.split('=',1)[1]) for b in bs if re.match(r't\s*=',b)];assert len(us)==1;u=us[0];dx,dy=s.diff(F,t),s.diff(G,t);X,Y=s.simplify(F.subs(t,u)),s.simplify(G.subs(t,u));ratio=s.simplify(dy/dx);DX,DY=s.simplify(dx.subs(t,u)),s.simplify(dy.subs(t,u))
 if DX==0 and DY==0:
  assert normal
  L=s.limit(ratio,t,u,dir='-');R0=s.limit(ratio,t,u,dir='+');assert eq(L,R0);M=L
  # Independently identify the actual regular geometric branch after shifts,
  # and check its derivative at this endpoint, not canceled 0/0 alone.
  K=s.simplify(F-s.log(s.sin(t)));H=s.simplify(G-1/s.sin(t));assert not K.has(t) and not H.has(t);assert eq(G-H,s.exp(-(F-K)));assert eq(M,s.diff(s.exp(-(x-K))+H,x).subs(x,X))
 else:assert DX!=0 and DY!=0;M=s.simplify(DY/DX)
 N=s.simplify(-1/M) if normal else M;line=y-Y-N*(x-X);xi=s.simplify(X-Y/N);yi=s.simplify(Y-N*X);axis='x' if re.search(r'crosses the \$x\$-axis',q[':question/problem']) else 'y' if re.search(r'crosses the \$y\$-axis',q[':question/problem']) else None
 return dict(F=F,G=G,u=u,dx=dx,dy=dy,X=X,Y=Y,M=M,N=N,ratio=ratio,line=line,xi=xi,yi=yi,axis=axis,DX=DX,DY=DY)
def raw(g,k):
 qs=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];counts=dict(prompts=0,solutions=0,fields=0,values=0,literal_values=0,keys=0,unrated=0)
 for c in json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text()):
  q0=next(q for q in qs if str(c['source_id']) in map(str,(q[':db/id'],q[':question/id'],q[':question/math-academy-id'])));r=g.generate(c.get('level',c.get('difficulty')),template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')));q=r['question'];counts['prompts']+=1;counts['solutions']+=(':question/worked-solution' in q0);counts['unrated']+=(':question/difficulty' not in q0)
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in q0)
   if key in q and key!=':question/answer-fields':assert q[key]==(q0[key][':db/ident'] if isinstance(q0[key],dict) else q0[key]),(k,c,key)
  assert len(q[':question/answer-fields'])==len(q0[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   vals=[a[':answer/value'] for a in f[':answer-field/choices']];old=[a[':answer/value'] for a in f0[':answer-field/choices']];counts['literal_values']+=sum(v in old for v in vals)
   obj=lambda v:point(v) if v.strip().startswith('(') else lk(relation(v)) if '=' in v else (scalar(v),)
   remaining=list(map(obj,old))
   for v in vals:
    V=obj(v);i=next((i for i,W in enumerate(remaining) if len(V)==len(W) and all(eq(a,b) for a,b in zip(V,W))),None);assert i is not None;(remaining.pop(i))
   assert not remaining;assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);counts['fields']+=1;counts['values']+=len(vals)
   if ':answer-field/correct' in f:
    v=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert all(eq(a,b) for a,b in zip(obj(v),obj(f0[':answer-field/correct'][':answer/value'])));counts['keys']+=1
 return counts
def bank(r,z,normal):
 X,Y,M,N=z['X'],z['Y'],z['M'],z['N'];name=r['generation']['template']
 if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank'):return None
 if z['axis']: 
  if normal:return None
  if name=='exponential_y_intercept':vals=[z['yi'],-z['DY']*X,M*X,Y,M];return [(0,v) for v in vals]
  if name=='trig_x_intercept':
   F,G=z['F'],z['G'];a=F.coeff(s.sin(t));b=F.coeff(s.cos(t));c=G.coeff(s.cos(t));return [(v,0) for v in [z['xi'],X-Y*(a+b)/c,X+Y/M,X,-Y/M]]
  return None
 if not normal:return [lk(y-YY-MM*(x-XX)) for MM,(XX,YY) in zip([M,1/M,-M,M,M],[(X,Y),(X,Y),(X,Y),(-X,Y),(X,-Y)])]
 if name=='log_sine':lines=[y-Y-N*(x-X),y-Y-M*(x-X),y-N*x,y+Y-N*(x-X),y-M*x]
 else:lines=[y-Y-N*(x-X),y-Y-M*(x-X),y-Y-(1/M)*(x-X),y-Y-N*x,y+Y-N*(x-X)]
 return [lk(v) for v in lines]
def check(k):
 normal=k==17592186083245;g=load(ROOT/f'generate/scratch/{k}.py','paramlineg'+str(k));src=raw(g,k);rs=json.loads((R/f'qa/{k}-sampled.json').read_text());seen={r['generation']['template'] for r in rs}
 for c in json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text()):
  if c['template'] not in seen:rs.append(g.generate(c.get('level',c.get('difficulty')),seed=92,template=c['template']));seen.add(c['template'])
 counts=dict(records=0,derivatives=0,coordinate_stages=0,slope_stages=0,symbolic_ratio_stages=0,negative_reciprocal_stages=0,line_intercept_stages=0,prose_points=0,choices=0,complete_method_banks=0,limiting_endpoint_cases=0)
 for r in rs:
  q=r['question'];z=task(q,normal);bs=blocks(q[':question/worked-solution']);ratio=z['ratio'];linekey=lk(z['line']);coord=False
  if z['DX']==z['DY']==0:counts['limiting_endpoint_cases']+=1
  for b in bs:
   if (re.search(r"x(?:'|\\prime)\(t\)=",b) or '{x}^{′}(t)=' in b):
    parts=re.split(r',\\(?:,|quad|qquad)\s*',b);assert len(parts)==2,b
    for part,d in zip(parts,(z['dx'],z['dy'])):assert eq(scalar(part.split('=',1)[1]),d),(k,part,d);counts['derivatives']+=1
    continue
   if not coord and r'\begin{aligned}' in b:
    body=b.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0];rows=body.split(r'\\');assert len(rows)==2
    for row,v in zip(rows,(z['X'],z['Y'])):
     for side in row.replace('&','').split('=')[1:]:assert eq(scalar(side),v),(k,r['generation']['template'],side,v);counts['coordinate_stages']+=1
    coord=True;continue
   if 'frac{dy}{dx}' in b or r'\frac{\mathrm{d}y}{\mathrm{d}x}' in b:
    if b.strip().startswith('m') or r'\begin{aligned}m' in b:
     rows=b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
     for row in rows:
      sides=(row.split('&',1)[1] if '&' in row else row).split('=')[1:]
      for side in sides:
       if '|' not in side:assert eq(scalar(side),z['M']),(k,side,z['M']);counts['slope_stages']+=1
    else:
     rows=b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
     for row in rows:
      for side in row.replace('&','').split('=')[1:]:
       if "′" in side or "'" in side or r'\prime' in side:continue
       assert eq(scalar(side),ratio),(k,side,ratio);counts['symbolic_ratio_stages']+=1
    continue
   if re.match(r'\s*m\s*=',b) or r'\begin{aligned}m &' in b:
    for side in b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').split('=')[1:]:assert eq(scalar(side),z['M']);counts['slope_stages']+=1
    continue
   if ('{m}_{n}' in b or 'm_n' in b) and '=' in b:
    for side in b.split('=')[1:]:assert eq(scalar(side.replace('m', '('+s.latex(z['M'])+')')),z['N']),(k,side,z['N']);counts['negative_reciprocal_stages']+=1
    continue
   if r'\begin{aligned}' in b:
    rows=b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
    for row in rows:
     E=relation(row);expected=lk((x-z['xi']) if z['axis']=='x' else (y-z['yi'])) if z['axis'] and not E.has(x,y) or z['axis'] and not E.has(y if z['axis']=='x' else x) else linekey
     # Final axis-isolation rows retain only the unknown intercept coordinate.
     assert lk(E)==expected,(k,r['generation']['template'],row,expected,linekey);counts['line_intercept_stages']+=1
    continue
   if re.fullmatch(r'[xy]=0[.,]?',b.strip()):assert z['axis'] and b.strip()[0]!=z['axis'];continue
   if re.match(r'\s*y(?:[+\-=]|\s)',b) and '=' in b:assert lk(relation(b))==linekey,(k,b,linekey);counts['line_intercept_stages']+=1
   if b.strip().startswith('m='):assert eq(scalar(b.split('=',1)[1]),z['M'])
   if '{m}_{n}=' in b:assert eq(scalar(b.split('=',1)[1]),z['N'])
   if '=' in b and ('x_1' in b or '{x}_{1}' in b):b=b.split('=',1)[1]
   if b.strip().startswith('(') and b.strip().rstrip('.,').endswith(')') and ',' in b:
    P=point(b);want=(z['X'],z['Y']);axiswant=(z['xi'],0) if z['axis']=='x' else (0,z['yi']);assert len(P)==2 and (all(eq(a,c) for a,c in zip(P,want)) or z['axis'] and all(eq(a,c) for a,c in zip(P,axiswant))),(k,b,z);counts['prose_points']+=1
  vals=[];placeholderkeys=re.findall(r'\{\{(field-\d)\}\}',q[':question/problem'])
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    v=a[':answer/value']
    if f[':answer-field/type'].endswith('/radio'):
     V=point(v) if v.startswith('(') else lk(relation(v));want=((z['xi'],0) if z['axis']=='x' else (0,z['yi'])) if z['axis'] else linekey;good=len(V)==len(want) and all(eq(c,d) for c,d in zip(V,want));vals.append(V)
    else:
     V=scalar(v);want=((z['xi'],0) if z['axis']=='x' else (0,z['yi']))[placeholderkeys.index(f[':answer-field/key'])] if z['axis'] else s.expand(z['Y']+z['N']*(x-z['X']));good=eq(V,want)
    assert good==(a[':answer/id']==f[':answer-field/correct'][1]),(k,f[':answer-field/key'],v,want);counts['choices']+=1
  expected=bank(r,z,normal)
  if expected is not None:assert len(vals)==5 and all(sum(len(v)==len(w) and all(eq(a,b) for a,b in zip(v,w)) for v in vals)==1 for w in expected),(k,vals,expected);counts['complete_method_banks']+=1
  counts['records']+=1
 out=dict(status='passed',kp_id=k,source=src,readback=counts,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
