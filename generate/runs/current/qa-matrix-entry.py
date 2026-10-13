"""Parent exact source banks and lookup from the actual displayed matrix/index."""
import importlib.util,json,re,hashlib,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','matrixentryparser')
def value(v):return v if v=='No such entry' else p.scalar(v)
def matrices(text):
 return [[[value(c.strip()) for c in row.split('&')] for row in m[1].split(r'\\')] for m in re.finditer(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',text,re.S)]
def task(q):
 text=q[':question/problem'];M=matrices(text);assert len(M)==1;M=M[0];m,n=len(M),len(M[0]);assert all(len(row)==n for row in M);a=re.search(r'\$\{?([a-z])\}?_\{(\d)(\d)\}',text);assert a;textname=a[1].upper();i,j=int(a[2]),int(a[3]);name=re.search(r'\$([A-Z])\$',text)[1];assert name==textname;return M,i,j,name,(M[i-1][j-1] if i<=m and j<=n else 'No such entry')
def raw(g,k):
 qs=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];C=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,unrated=0)
 for c in json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text()):
  old=next(q for q in qs if str(c['source_id']) in map(str,(q[':db/id'],q[':question/id'],q[':question/math-academy-id'])));q=g.generate(c.get('level','easy'),template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')))['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in old)
   if key in q and key!=':question/answer-fields':assert q[key]==(old[key][':db/ident'] if isinstance(old[key],dict) else old[key]),(k,c,key)
  C['prompts']+=1;C['solutions']+=(':question/worked-solution' in old);C['unrated']+=(':question/difficulty' not in old);assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],old[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);C['fields']+=1;C['values']+=len(f[':answer-field/choices'])
   if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];C['keys']+=1
 return C
def bank(k,r,M,i,j):
 m,n=len(M),len(M[0]);v=lambda pos:'No such entry' if pos is None else M[pos[0]-1][pos[1]-1];profile=r['generation'].get('profile',r['generation'].get('bank_profile'))
 if k==17592186100989:
  pos={'target':(i,j),'left':(i,j-1),'right':(i,j+1),'up':(i-1,j),'down':(i+1,j),'transpose':(j,i),'transposed_first':(j,1),'last_diagonal':(n,n),'previous_diagonal':(n-1,n-1),'cell11':(1,1),'cell12':(1,2),'cell21':(2,1),'cell22':(2,2),'cell23':(2,3),'missing':None}
  recipes={'transpose_neighbors':['target','left','transpose','transposed_first','missing'],'right_up_left':['target','right','up','left','missing'],'local_neighbors':['target','left','up','down','missing'],'all_four':['missing','cell11','cell12','cell21','cell22'],'inline_diagonal':['target','last_diagonal','previous_diagonal','cell23','missing'],'blank':['target']}[profile];return list(map(lambda name:v(pos[name]),recipes))
 a=i+1 if i<m else i-1;b=j+1 if j<n else j-1
 if profile=='overflow_locations':
  assert (i==m+1 and j<=n) or (j==n+1 and i<=m)
  if i==m+1:col=j+1 if j<n else j-1;positions=[None,(m,j),(1,j),(m,col),(1,col)]
  else:row=i+1 if i<m else i-1;positions=[None,(i,n),(i,1),(row,n),(row,1)]
  return list(map(v,positions))
 if profile=='blank':return [v((i,j))]
 if profile=='location_no_entry':positions=[(i,j),(a,j),(i,b),(a,b),None]
 elif profile=='four_locations':c=j-1 if j>1 and j-1!=b else j+2 if j+2<=n else j-2;positions=[(i,j),(a,j),(i,b),(a,b),(i,c)]
 elif profile=='swap_no_entry':positions=[(i,j),(j,i),(a,j),(i,b),None]
 else:raise AssertionError(('unreviewed bank',profile))
 return list(map(v,positions))
def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','matrixentrygenerator'+str(k));src=raw(g,k);rs=json.loads((R/f'qa/{k}-sampled.json').read_text());C=dict(records=0,choices=0,whole_banks=0,matched_repeated_matrices=0,prose_index_checks=0,missing_entries=0);seen=set()
 for r in rs:
  q=r['question'];M,i,j,name,correct=task(q);sol=q[':question/worked-solution'];m,n=len(M),len(M[0]);seen.add(r['generation'].get('profile',r['generation'].get('bank_profile')));C['missing_entries']+=correct=='No such entry';level=q[':question/difficulty'].split('/')[-1]
  assert (m==n)==(k==17592186100989)
  if level=='moderate':assert (m,n) in (((5,5),) if k==17592186100989 else ((5,6),(6,5))) and max(i,j)>=4
  if level=='hard':assert (m,n) in (((6,6),) if k==17592186100989 else ((6,7),(7,6))) and max(i,j)>=5
  prose=re.search(r'intersection of the \$(\d)\$\w+ row and \$(\d)\$\w+ column',sol);assert prose and tuple(map(int,prose.groups()))==(i,j);C['prose_index_checks']+=1
  for S in matrices(sol):assert S==M;C['matched_repeated_matrices']+=1
  if correct!='No such entry':
   result=re.search(r'\{?([a-z])\}?_\{(\d)(\d)\}=(.*?)\$',sol);assert result and result[1].upper()==name and (int(result[2]),int(result[3]))==(i,j) and value(result[4].rstrip('.'))==correct
  else:assert 'does not have' in sol or 'no such entry' in sol
  for a,I,J in re.findall(r'\{?([a-z])\}?_\{(\d)(\d)\}',sol):assert a.upper()==name and (int(I),int(J))==(i,j)
  for f in q[':question/answer-fields']:
   vals=[]
   for a in f[':answer-field/choices']:
    v=value(a[':answer/value']);assert (v==correct)==(a[':answer/id']==f[':answer-field/correct'][1]);assert a[':answer/type']==(':answer.type/text' if isinstance(v,str) else ':answer.type/math');assert v not in vals;vals.append(v);C['choices']+=1
   expected=bank(k,r,M,i,j);assert len(vals)==len(expected) and set(vals)==set(expected);C['whole_banks']+=1
  C['records']+=1
 out=dict(status='passed',kp_id=k,source=src,readback=C,profiles=sorted(seen),script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
