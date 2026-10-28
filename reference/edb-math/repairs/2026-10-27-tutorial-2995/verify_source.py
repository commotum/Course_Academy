"""Compare every source matrix and independently evaluate the product cells."""
import ast,hashlib,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment,cells,normalize_source_tex
p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';ns={'__file__':str(p)};exec(compile(p.read_text().split('parents=json.loads')[0],str(p),'exec'),ns)
soup=BeautifulSoup((H/'source.html').read_text(),'html.parser');source=[normalize_source_tex(ns['reconstruct'](n))for n in soup.find_all('title')];after=(H/'proposed.md').read_text()
def grids(text):
 out=[]
 for match in ENV.finditer(text):
  if match.groups()!=('begin','bmatrix'):continue
  span=environment(text,match.start());out.append(cells(text[span[0]:span[1]]))
 return out
original=grids('\n'.join(source));current=grids(after);assert len(current)==len(original)==6
canonical=lambda s:re.sub(r'\s+|[{}]','',s).replace(r'\times',r'\cdot')
assert [[list(map(canonical,row))for row in g]for g in current]==[[list(map(canonical,row))for row in g]for g in original]
def calculate(s):
 s=canonical(s).replace(r'\cdot','*');assert re.fullmatch(r'[\d+*()\-]+',s)
 def value(n):
  if isinstance(n,ast.Constant)and type(n.value)is int:return n.value
  if isinstance(n,ast.UnaryOp)and isinstance(n.op,ast.USub):return-value(n.operand)
  if isinstance(n,ast.BinOp)and isinstance(n.op,(ast.Add,ast.Sub,ast.Mult)):
   a,b=value(n.left),value(n.right);return a+b if isinstance(n.op,ast.Add)else a-b if isinstance(n.op,ast.Sub)else a*b
  raise ValueError('Unexpected arithmetic')
 return value(ast.parse(s,mode='eval').body)
result=[[calculate(c)for c in row]for row in current[4]];expected=[[-2,3,10],[6,-2,2],[23,4,8]];assert result==expected
report={'source_archive':'/home/jake/Developer/MA/DATA/Lessons/1171/Source/1171.html','source_tutorial':2995,'source_fragment_sha256':hashlib.sha256((H/'source.html').read_bytes()).hexdigest(),'source_formulas':len(source),'matrices_compared':len(current),'all_matrix_cells_match_source':True,'expanded_product_evaluates_to_A':result,'passed':True};(H/'source-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
