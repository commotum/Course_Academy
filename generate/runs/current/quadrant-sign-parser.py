"""Root proves monomial signs over open quadrants from the displayed equation."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_quad_scalar',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x,y=p.x,p.y
WORDS=['first','second','third','fourth'];Q=((1,1),(-1,1),(-1,-1),(1,-1))
def math(raw):return p.scalar(raw.strip().rstrip('.,'))
def read(text):
 raw=re.search(r'\$([^$]*?=[^$]*?)\$',text)[1];expression=math(raw.split('=',1)[1]);poly=s.Poly(expression,x,y);assert len(poly.terms())==1;((a,b),c),=poly.terms();assert a>=1 and b>=0 and c.is_real and c!=0
 signs=tuple(int(s.sign(c))*(sx**a)*(sy**b) for sx,sy in Q)
 claims=re.findall(r'At every point in the (first|second|third|fourth) quadrant, the slope of the slope field is (positive|negative)',text);assert len(claims)==3
 truth=tuple(signs[WORDS.index(word)]==(1 if desired=='positive' else -1) for word,desired in claims)
 return expression,(a,b,c),signs,claims,truth

def subset(value):
 if value in ('None','None of those listed'):return frozenset()
 value=value.removesuffix(' only').replace(',','').replace(' and ',' ')
 parts=value.split();assert parts and all(z in ('I','II','III') for z in parts);return frozenset(('I','II','III').index(z) for z in parts)

def stages(text,values):
 expression,(a,b,c),signs,claims,truth=values
 definition=re.search(r'\$f\(x,y\)=([^$]*?)\$',text);assert definition and s.expand(math(definition[1])-expression)==0
 if b==0:assert 'or $y=0' not in text and 'or y=0' not in text
 groups=re.findall(r'Statement (I|II|III) is (true|false)\.(.*?)(?=Statement (?:I|II|III) is|\Z)',text,re.S);assert len(groups)==3
 for roman,result,body in groups:
  i=('I','II','III').index(roman);assert (result=='true')==truth[i]
  words=re.findall(r'(first|second|third|fourth) quadrant',body);assert words and all(word==claims[i][0] for word in words)
  z=re.findall(r'=f\(x,y\)([<>])0',body);assert len(z)==1 and (1 if z[0]=='>' else -1)==signs[WORDS.index(claims[i][0])]
  wording=re.findall(r'slope of the slope field is (positive|negative)',body);assert len(wording)==1 and (1 if wording[0]=='positive' else -1)==signs[WORDS.index(claims[i][0])]
 return dict(statement_steps=3,sign_inequalities=3,monomial_definitions=1)
