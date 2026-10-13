"""Parent readback for one scalar: displayed combination, path and actual plots."""
import importlib.util,json,re
from pathlib import Path
sp=importlib.util.spec_from_file_location('single_vector_parent_scalar',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p);s=p.s
def same(a,b):return s.expand(a-b)==0
def scalar(raw,basis):
 raw=raw.strip().strip('$').rstrip('.,');pieces=re.split(r'(\\[A-Za-z]+)',raw)
 raw=''.join(z if z.startswith('\\') else re.sub('[a-z]',lambda m:'('+str(basis[m[0]])+')' if m[0] in basis else m[0],z) for z in pieces)
 return p.scalar(raw.replace(r'\lambda','x'))
def check(record,source_geometry=None):
 q=record['question'];stem=q[':question/problem'];worked=q[':question/worked-solution'];m=re.search(r'c=([^$]+)',stem);assert m
 bs={'a':p.i,'b':p.j};given=s.expand(scalar(m[1],bs));direction=s.diff(given,p.x);assert direction in (p.i,p.j);unknown='a' if direction==p.i else 'b';known='b' if unknown=='a' else 'a';knownexpr=given.subs(p.x,0);knowncoef=knownexpr.coeff(bs[known]);assert given==knowncoef*bs[known]+p.x*bs[unknown]
 refs=re.findall(r'!\[\]\((.*?)\)',stem+worked);assert len(refs)==2
 side=[]
 for z in refs:
  path=Path(z)
  if not path.is_file():path=Path('/media/jake/SSD/EDB/math')/z
  assert path.is_file(),z
  if path.with_suffix('.json').is_file():side.append(json.loads(path.with_suffix('.json').read_text()))
 if side:
  geom=side[0].get('plot_data',side[0]);G=s.Matrix.hstack(s.Matrix(geom['a']),s.Matrix(geom['b']))
  if 'c' in geom:C=s.Matrix([s.Rational(str(z)) for z in geom['c']]);P=s.Matrix([s.Rational(str(z)) for z in geom['p']])
  else:
   C=G*s.Matrix([s.Rational(geom['ca_exact']),s.Rational(geom['cb_exact'])]);P=s.Matrix(geom[known])*knowncoef
  coefficients=G.inv()*C;factor=coefficients[0 if unknown=='a' else 1];assert same(coefficients[0 if known=='a' else 1],knowncoef)
  assert all(same(z,0) for z in P-s.Matrix(geom[known])*knowncoef)
  other=side[1].get('plot_data',side[1]);assert geom['a']==other['a'] and geom['b']==other['b']
  if 'c' in geom:assert geom['c']==other['c'] and geom['p']==other['p']
  else:assert geom['ca_exact']==other['ca_exact'] and geom['cb_exact']==other['cb_exact']
 else:
  assert source_geometry is not None
  geom=source_geometry;G=s.Matrix.hstack(s.Matrix(geom['a']),s.Matrix(geom['b']));factor=s.Rational(geom.get('scalar', '-'+str(geom.get('r'))));C=G*s.Matrix([factor,knowncoef] if unknown=='a' else [knowncoef,factor]);P=s.Matrix(geom[known])*knowncoef
 assert G.det()!=0
 combo=given.subs(p.x,factor);bs['c']=combo;points={'O':0,'A':p.i,'B':p.j,'C':combo,'P':knowncoef*bs[known]}
 paths=re.findall(r'c\s*(?:&\s*)?=\s*\\overset\{\\to\s*\}\{O([A-Z])\}\+\\overset\{\\to\s*\}\{([A-Z])C\}',worked)
 assert paths,worked
 for first,second in paths:assert first==second;points[first]=knownexpr
 def vector(raw):
  saved=[]
  def hold(m):saved.append(points[m[1][1]]-points[m[1][0]]);return 'ZZ'+str(len(saved)-1)+'ZZ'
  raw=re.sub(r'\\overset\{\\to\s*\}\{([A-Z]{2})\}',hold,raw)
  pieces=re.split(r'(\\[A-Za-z]+)',raw);raw=''.join(z if z.startswith('\\') else re.sub('[a-z]',lambda m:'('+str(bs[m[0]])+')' if m[0] in bs else m[0],z) for z in pieces)
  raw=raw.replace(r'\lambda','('+str(factor)+')')
  for n,v in enumerate(saved):raw=raw.replace('ZZ'+str(n)+'ZZ','('+str(v)+')')
  return p.scalar(raw)
 lengths=re.findall(r'\$([A-Z]{2})=([^$]*?)\|([ab])\|\$',worked);assert lengths
 for seg,c,name in lengths:
  magnitude=p.scalar(c) if c.strip() else 1;expected=vector(r'\overset{\to }{'+seg+'}');unit=bs[name];assert same(expected,magnitude*unit) or same(expected,-magnitude*unit)
  if seg=='PC':assert same(magnitude,abs(factor)) and ('opposite directions' in worked)==(factor<0)
 identities=0;coordinates=0
 for raw in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',worked,re.S):
  raw=next(z for z in raw if z);raw=re.sub(r'\\(?:begin|end)\{aligned\}','',raw);carry=None
  for row in raw.split(r'\\'):
   parts=row.replace('&','').strip().rstrip('.,').split('=')
   if len(parts)<2 or '|' in row:continue
   if parts[0].strip()=='P' and len(parts)==2:
    coords=parts[1].strip().strip('()').split(',');assert len(coords)==2 and all(same(p.scalar(z),v) for z,v in zip(coords,P));coordinates+=1;continue
   if not parts[0].strip():assert carry is not None;parts[0]=carry
   else:carry=parts[0]
   vals=[vector(z) for z in parts];assert all(same(vals[0],z) for z in vals[1:]),(row,vals);identities+=len(vals)-1
 assert identities>=7
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1;values=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];good=[same(v,factor) for v in values]
 if f[':answer-field/type'].endswith('/radio'):assert sum(good)==1 and len(set(values))==len(values)
 else:assert all(good) and '{{'+f[':answer-field/key']+'}}' in stem
 assert good[next(n for n,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
 return {'values':len(values),'path_identities':identities,'length_rows':len(lengths),'plot_pair':int(bool(side)),'coordinate_rows':coordinates},factor,knowncoef
