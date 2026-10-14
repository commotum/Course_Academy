"""Root actual supplied/computed cross then dot, every minor and whole bank."""
import json,re,sys,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186105735;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);sys.modules[name]=m;z.loader.exec_module(m);return m
base=load(R/'qa-parametric-scalar-line.py','root_triple_base');p=load(R/'triangle-readback.py','root_triple_read');v=p.p
C={k:0 for k in ('records','actual_cross_components','cross_input_arrays','cofactor_minors','cross_stages','dot_stages','signed_dot_operands','choices','whole_method_banks','hard_workloads')}
ARRAY=re.compile(r'\|\\begin\{aligned\}((?:(?!\\begin\{).)*?)\\end\{aligned\}\|',re.S)
def vec(raw):return v.vector(raw.strip().rstrip('.,')).reshape(3,1)
def scalar(raw):return v.scalar(raw.strip().rstrip('.,'))
def expression(raw,known):
 raw=raw.strip().rstrip('.,');m=re.fullmatch(r'(⟨.*?⟩)\\cdot (⟨.*?⟩)',raw)
 if m:return vec(m[1]).dot(vec(m[2]))
 if r'\cdot' in raw and not ('⟨' in raw):return scalar(raw)
 if raw in ('b'+r'\times c',):return p.basis(known['d'])
 if raw=='a'+r'\cdot (b'+r'\times c)':return known['answer']
 return p.expression(raw,dict(kind='vectors',vals={},arrows={},scalars={}))
def actual(q):
 text=q[':question/problem'];data={n:vec('⟨'+body+'⟩') for n,body in re.findall(r'([abc])\s*=\s*⟨(.*?)⟩',text)}
 assert 'a' in data
 if 'b' in data and 'c' in data:data['d']=data['b'].cross(data['c'])
 else:
  raw=re.search(r'b\\times c\s*=\s*(⟨.*?⟩)',text);assert raw;data['d']=vec(raw[1])
 assert r'a\cdot (b\times c)' in text or r'a \cdot (b \times c)' in text
 data['answer']=data['a'].dot(data['d']);return data

def check(rec):
 q=rec['question'];known=actual(q);A,d=known['a'],known['d'];sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);crossing='b' in known;assert len(blocks)==(2 if crossing else 1)
 for bi,block in enumerate(blocks):
  saved=[]
  def save(m):saved.append(m[0]);return 'MATRIX'+str(len(saved)-1)
  block=ARRAY.sub(save,block)
  if crossing and bi==0:
   assert len(saved)==4;matrices=[]
   for raw in saved:
    rows=[[scalar(cell.strip()) for cell in row.split('&')] for row in ARRAY.fullmatch(raw)[1].split(chr(92)*2)];matrices.append(s.Matrix(rows))
   assert list(matrices[0][0,:])==[v.i,v.j,v.k] and list(matrices[0][1,:])==list(known['b']) and list(matrices[0][2,:])==list(known['c']);C['cross_input_arrays']+=1
   B,E=known['b'],known['c'];expected=[s.Matrix([[B[i],B[j]],[E[i],E[j]]]) for i,j in ((1,2),(0,2),(0,1))];assert matrices[1:]==expected;C['cofactor_minors']+=3;C['actual_cross_components']+=3
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');previous=None
  for row in block.split(chr(92)*2):
   row=re.sub(r'MATRIX(\d+)',lambda m:saved[int(m[1])],row).strip().rstrip('.,')
   if '=' not in row:continue
   lhs,rhs=row.split('=',1)
   actualvalue=expression(rhs,known);expected=p.basis(d) if crossing and bi==0 else known['answer'];assert s.simplify(actualvalue-expected)==0,(row,actualvalue,expected)
   if not(crossing and bi==0):
    # Each numeric dot operand must remain individually displayed.
    if '⟨' not in rhs and (r'\cdot' in rhs or re.search(r'\)\(',rhs)):
     pieces=[];depth=0;at=0
     for j,ch in enumerate(rhs):
      depth+=(ch in '({')-(ch in ')}')
      if ch=='+' and depth==0:pieces.append(rhs[at:j]);at=j+1
     pieces.append(rhs[at:]);assert len(pieces)==3
     for piece,a0,d0 in zip(pieces,A,d):
      if r'\cdot' in piece:aa,dd=piece.split(r'\cdot',1)
      else:
       match=re.fullmatch(r'\((.*?)\)\((.*?)\)',piece);assert match;aa,dd=match.groups()
      assert scalar(aa)==a0 and scalar(dd)==d0,(piece,a0,d0)
     C['signed_dot_operands']+=3
   C['cross_stages' if crossing and bi==0 else 'dot_stages']+=1
  if crossing and bi==0:assert 'First, we find the cross product:' in sol and 'Now, we can compute the scalar triple product:' in sol
 f=q[':question/answer-fields'][0];values=[scalar(z[':answer/value']) for z in f[':answer-field/choices']];ref=f[':answer-field/correct'][1];assert next(z[':answer/id'] for z in f[':answer-field/choices'] if scalar(z[':answer/value'])==known['answer'])==ref;assert len(values)==len(set(values))
 if f[':answer-field/type'].endswith('/radio'):
  assert len(values)==5
  if crossing:
   B,E=known['b'],known['c'];wrongj=s.Matrix([d[0],-d[1],d[2]]);omit=s.Matrix([B[1]*E[2],-B[0]*E[2],B[0]*E[1]]);expected=[known['answer'],A.dot(wrongj),A.dot(omit),known['answer']-A[0]*d[0],known['answer']-A[2]*d[2]]
  else:expected=[known['answer'],sum(a+b for a,b in zip(A,d)),A.dot(A),d.dot(d),A.dot(s.Matrix(list(reversed(d))))]
  assert sorted(values)==sorted(expected);C['whole_method_banks']+=1
 else:assert values==[known['answer']] and '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 if q[':question/difficulty'].endswith('/hard'):
  inputs=list(A)+list(known['b'])+list(known['c']);assert all(z!=0 and abs(z)<=5 for z in inputs) and any(abs(z)==5 for z in inputs) and all(z!=0 for z in d) and abs(known['answer'])<=375;C['hard_workloads']+=1
 C['choices']+=len(values);C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'triple_definition_gen');source=base.raw(g,K,D);records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for level,templates in g.TEMPLATES.items():
  for template in templates:
   if template!='cross_legacy_radio':records.append(g.generate(level,template=template,seed=744))
 for z in records:check(z)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
