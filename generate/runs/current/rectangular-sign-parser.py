"""Root proves translated-separable slope signs from printed open regions."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_rect_scalar',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p);x,y=p.x,p.y
math=p.scalar
REGIONS=((1,1),(-1,1),(-1,-1),(1,-1))
def read(text):
 raw=re.search(r'\$([^$]*?=[^$]*?)\$',text)[1];expr=math(raw.split('=',1)[1]);px=s.Poly(expr,x);py=s.Poly(expr,y);rx=s.solve(expr,x);ry=s.solve(expr,y);assert len(rx)==len(ry)==1
 h,k=rx[0],ry[0];assert not h.free_symbols and not k.free_symbols
 a,b=px.degree(),py.degree();assert a in (1,2) and b in (1,2) and not(a==b==2)
 c=s.simplify(expr/((x-h)**a*(y-k)**b));assert not c.free_symbols and c!=0
 signs=tuple(int(s.sign(c))*sx**a*sy**b for sx,sy in REGIONS)
 claims=re.findall(r'At every point[^\n]*?where\s*(.*?)the slope of the slope field is (positive|negative)',text);assert len(claims)==3,text
 boundaries=[];truth=[]
 for pair,wanted in claims:
  parts=re.findall(r'([xy])\s*([<>])\s*(.*?)(?=\s*and\s*|\Z)',pair.replace('$','').strip().rstrip(','));assert len(parts)==2,parts
  values={var:(op,math(num)) for var,op,num in parts};assert set(values)=={'x','y'} and values['x'][1]==h and values['y'][1]==k
  signsxy=tuple(1 if values[v][0]=='>' else -1 for v in ('x','y'));region=REGIONS.index(signsxy);boundaries.append((region,wanted));truth.append(signs[region]==(1 if wanted=='positive' else -1))
 return expr,(h,k,a,b,c),signs,boundaries,tuple(truth)
def subset(value):
 if value in ('None','None of those listed'):return frozenset()
 parts=value.removesuffix(' only').replace(',','').replace(' and ',' ').split();assert parts and all(z in ('I','II','III') for z in parts)
 return frozenset(('I','II','III').index(v) for v in parts)
def stages(text,values):
 expr,(h,k,a,b,c),signs,claims,truth=values
 definition=re.search(r'\$f\(x,y\)=([^$]+)\$',text);assert definition and s.expand(math(definition[1])-expr)==0
 zeros=re.search(r'when\s*\$x=([^$]+)\$\s*or\s*\$y=([^$]+)\$',text);assert zeros and math(zeros[1])==h and math(zeros[2])==k
 blocks=re.findall(r'Statement (I|II|III) is (true|false)\.(.*?)(?=Statement (?:I|II|III) is|Therefore|\Z)',text,re.S);assert len(blocks)==3
 for roman,outcome,body in blocks:
  i=('I','II','III').index(roman);region,wanted=claims[i];assert (outcome=='true')==truth[i]
  ifmatch=re.search(r'If\s*(.*?)then according',body);assert ifmatch
  coords=re.findall(r'([xy])([<>])(.*?)(?=\s*and\s*|\Z)',ifmatch[1].replace('$','').strip().rstrip(','));assert len(coords)==2
  vv={var:(op,math(num)) for var,op,num in coords};assert vv['x'][1]==h and vv['y'][1]==k and tuple(1 if vv[v][0]=='>' else -1 for v in ('x','y'))==REGIONS[region]
  inequalities=re.findall(r'=f\(x,y\)([<>])0',body);assert len(inequalities)==1 and (1 if inequalities[0]=='>' else -1)==signs[region]
  words=re.findall(r'slope of the slope field is (positive|negative)',body);assert len(words)==1 and (1 if words[0]=='positive' else -1)==signs[region]
 return dict(statement_steps=3,sign_inequalities=3,definitions=1,zero_line_pairs=1)
