"""Read-only source extraction; no generator imports or database access."""
import json,re,itertools,hashlib,shutil
from pathlib import Path
D=Path(__file__).resolve().parent
S=json.loads((D/'source.json').read_text()); R=S['record']; specs={};cases=[]
M=re.compile(r'\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}')
def matrix(v):return [[int(x.strip()) for x in row.split('&')] for row in v.split('\\\\')]
def mult(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def atoms(a,b):
 out=[]
 for i in range(len(a)):
  for j in range(len(b[0])):
   out += [('dot',i,j,sum(a[i][k]*b[k][j] for k in range(len(b))))]
   for k in range(len(b)):out += [('product',i,k,j,a[i][k]*b[k][j])]
 for name,m in [('A',a),('B',b)]:
  for i,row in enumerate(m):
   for j,v in enumerate(row):out.append((name,i,j,v))
 return out

def recipe(v,a,b):
 if v==0:return []
 atom=atoms(a,b)
 for w in [1,-1]:
  for x in atom:
   if w*x[-1]==v:return [[w,list(x[:-1])]]
 for x,y in itertools.combinations(atom,2):
  for w,z in itertools.product([1,-1],repeat=2):
   if w*x[-1]+z*y[-1]==v:return [[w,list(x[:-1])],[z,list(y[:-1])]]
 raise ValueError(v)
for q in R[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];ms=list(M.finditer(q[':question/problem']));a,b=[matrix(x[1]) for x in ms[:2]];c=mult(a,b);m,n,p=len(a),len(b),len(b[0]);fields=q[':question/answer-fields'];blank=fields[0][':answer-field/type'][':db/ident'].endswith('/blank')
 roles={}
 if blank:
  rows=q[':question/problem'].split('\n\n|')[1].splitlines();r=0
  for line in rows:
   if '---' in line:continue
   entries=re.findall(r'\{\{(field-\d+)\}\}|\$(-?\d+)\$',line)
   if entries:
    assert len(entries)==p,(sid,entries)
    for j,(key,val) in enumerate(entries):
     if key:roles[key]=[r,j]
    r+=1
  targets=sorted(roles.values())
 else:targets=[[i,j] for i in range(m) for j in range(p)]
 names=re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}',q[':question/problem']);assert len(names)==2
 prompt=q[':question/problem'];index=0
 def pm(match):
  global index
  k=index;index+=1;return '{{A}}' if k==0 else '{{B}}'
 prompt=M.sub(pm,prompt)
 # Every supplied product table value becomes a derived component slot.
 if blank:
  lines=prompt.splitlines();rr=0
  for k,line in enumerate(lines):
   if line.startswith('|') and '---' not in line:
    jj=0
    def tc(match):
     global jj
     z='{{C_'+str(rr)+'_'+str(jj)+'}}' if match[2] else match[0];jj+=1;return z
    lines[k]=re.sub(r'(\{\{field-\d+\}\})|\$(-?\d+)\$',tc,line);rr+=1
  prompt='\n'.join(lines)
 sol=q.get(':question/worked-solution');solution=None;mat_masks=[];anomalies=[]
 if sol:
  mats=list(M.finditer(sol));assert len(mats)==3*len(targets)+1
  vals={}; ii=0
  def sm(match):
   global ii
   k=ii;ii+=1
   if k==len(mats)-1:typ='C'
   elif k%3==0:
    typ='A'
    if matrix(match[1])!=a:typ='A_typo';anomalies.append({'stage':k//3,'kind':'wrong printed left matrix','raw':match[0],'repair':'use actual A at every stage'})
   elif k%3==1:typ='B'
   else:
    typ='progress_'+str(k//3);mat_masks.append([[('*' if cell.strip()=='∗' else 'C') for cell in row.split('&')] for row in match[1].split('\\\\')])
   return '{{'+typ+'}}'
  solution=M.sub(sm,sol);dots=[]
  def dot(match):
   dots.append(match[0]);return '{{dot_'+str(len(dots)-1)+'}}'
  solution=re.sub(r'\\,-?\d+=.*?(?= \\\\|\\end\{aligned\})',dot,solution);assert len(dots)==len(targets),(sid,len(dots),len(targets))
 bank=[]
 for f in fields:
  row={'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'has_correct':':answer-field/correct' in f,'choices':[]}
  for v in f[':answer-field/choices']:
   value=v[':answer/value'];vm=M.fullmatch(value)
   if vm:
    cells=matrix(vm[1]);rec=[[recipe(x,a,b) for x in rr] for rr in cells]
   else:cells=[[int(value)]];rec=[[recipe(int(value),a,b)]]
   row['choices'].append({'matrix':bool(vm),'recipes':rec,'raw_value':value,'raw_answer_id':v[':answer/id']})
  if row['has_correct']:row['correct_index']=next(i for i,v in enumerate(f[':answer-field/choices']) if v[':answer/id']==f[':answer-field/correct'][':answer/id'])
  bank.append(row)
 products=[abs(a[i][k]*b[k][j]) for i in range(m) for j in range(p) for k in range(n)]; dot_abs=[sum(abs(a[i][k]*b[k][j]) for k in range(n)) for i in range(m) for j in range(p)]
 specs[sid]={'source_id':sid,'source_db_id':q[':db/id'],'level':'easy','observed_difficulty':q.get(':question/difficulty'),'names':names,'parameters':{'A':a,'B':b,'targets':targets},'roles':roles,'blank':blank,'prompt_template':prompt,'solution_template':solution,'progress_masks':mat_masks,'bank':bank,'source_anomalies':anomalies,'has_solution':sol is not None,'bounds':{'coefficient':max(abs(x) for z in [a,b] for rr in z for x in rr),'product':max(products),'dot_l1':max(dot_abs),'result':max(abs(x) for rr in c for x in rr)},'answer_presence':list(q.keys())}
 cases.append({'source_id':sid,'template':sid,'parameters':specs[sid]['parameters'],'level':'easy','profile':'observed-raw','bank_profile':sid+'-opaque-observed' if not blank else None})
(D/'replay-specifications.json').write_text(json.dumps(specs,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(D/'independent-inventory.json').write_text(json.dumps({k:S[k] for k in ['database','basis','lineage']}|{'questions':[]},indent=2)+'\n')
(D/'source-findings.json').write_text(json.dumps({'unrated_missing_solution_correct':['q-1029','q-1034'],'wrong_intermediate_operand':{'q-129495':specs['q-129495']['source_anomalies']},'plots':'none in practice; canonical images are matrix typography, visually read as C=[[1,-2,0],[2,1,1]],D=[[0,1],[2,0],[-3,2]],CD=[[-4,1],[-1,4]]','opaque_banks':'historical distractor intent underdetermined; explicit source-shaped linear recipes over actual operand entries/products/dots retained for evidence only; never default.'},indent=2)+'\n')
print('Extracted',len(specs),'sources;',sum(len(f['choices']) for s in specs.values() for f in s['bank']),'answers')
