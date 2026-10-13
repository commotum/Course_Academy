"""Parent positional readback, actual boxed cell and all whole indexed-symbol banks."""
import importlib.util,json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186100990
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
def index(value):
 m=re.fullmatch(r'\{?([a-z])\}?_\{(\d)(\d)\}',value.strip());assert m,value;return m[1],int(m[2]),int(m[3])
def task(q):
 text=q[':question/problem'];body=re.search(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',text,re.S);assert body;rows=[row.split('&') for row in body[1].split(r'\\')];n=len(rows[0]);assert all(len(row)==n for row in rows);boxes=[(i,j,re.fullmatch(r'\s*\\boxed\{(-?\d+)\}\s*',v)) for i,row in enumerate(rows,1) for j,v in enumerate(row,1) if r'\boxed' in v];assert len(boxes)==1 and boxes[0][2];i,j,box=boxes[0];V=int(box[1]);matrix=[[int(re.sub(r'\\boxed\{(-?\d+)\}',r'\1',v).strip()) for v in row] for row in rows];name=re.search(r'\$([A-Z])\$',text)[1];return matrix,i,j,V,name
def raw(g):
 qs=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];C=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,unrated=0)
 for c in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  old=next(q for q in qs if str(c['source_id']) in map(str,(q[':db/id'],q[':question/id'],q[':question/math-academy-id'])));q=g.generate(c.get('level','easy'),template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')))['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in old)
   if key in q and key!=':question/answer-fields':assert q[key]==(old[key][':db/ident'] if isinstance(old[key],dict) else old[key])
  C['prompts']+=1;C['solutions']+=(':question/worked-solution' in old);C['unrated']+=(':question/difficulty' not in old);assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],old[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);C['fields']+=1;C['values']+=len(f[':answer-field/choices'])
   if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];C['keys']+=1
 return C
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','matrixindexgenerator');source=raw(g);rs=json.loads((R/f'qa/{K}-sampled.json').read_text());seen={r['generation']['profile'] for r in rs};profiles={'q-13498':((1,-1),(0,1),(0,0),(1,0),(0,-1)),'q-13503':((-2,0),(0,0),(-1,-2),(-1,0),(1,0)),'q-13489':((0,0),(1,2),(1,1),(1,0),(0,1)),'q-125611':((-1,-1),(0,-1),(-1,0),(0,0),(0,1)),'q-13499':((-1,-3),(-2,-1),(1,-1),(-1,-2),(0,0))}
 for profile in profiles:
  if profile not in seen:rs.append(g.generate('hard',seed=123,profile=profile,template='display_radio'))
 C=dict(records=0,marked_cells=0,prose_position_checks=0,conclusions=0,choices=0,whole_banks=0)
 for r in rs:
  q=r['question'];M,i,j,V,name=task(q);m,n=len(M),len(M[0]);sol=q[':question/worked-solution'];C['marked_cells']+=1;assert not r['generation']['evidence_only'] and r['generation']['eligible_for_learning'];level=q[':question/difficulty'].split('/')[-1]
  if level=='moderate':assert (m,n) in ((5,6),(6,5)) and max(i,j)>=4
  if level=='hard':assert (m,n) in ((6,7),(7,6)) and max(i,j)>=5
  a=re.search(r'intersection of the \$(\d)\$\w+ row and \$(\d)\$\w+ column',sol);assert a and tuple(map(int,a.groups()))==(i,j);C['prose_position_checks']+=1
  if r['generation']['template']=='two_indices':assert re.search(r'\$i='+str(i)+r'\$',sol) and re.search(r'\$j='+str(j)+r'[.]?\$',sol);C['conclusions']+=2
  else:
   a=re.search(r'\{?([a-z])\}?_\{(\d)(\d)\}=(-?\d+)',sol);assert a and a[1].upper()==name and (int(a[2]),int(a[3]),int(a[4]))==(i,j,V);C['conclusions']+=1
  for f in q[':question/answer-fields']:
   vals=[]
   for a in f[':answer-field/choices']:
    v=(int(a[':answer/value']),) if f[':answer-field/type'].endswith('/blank') else index(a[':answer/value']);want=((i,) if f[':answer-field/key']=='field-1' else (j,)) if f[':answer-field/type'].endswith('/blank') else (name.lower(),i,j);assert (v==want)==(a[':answer/id']==f[':answer-field/correct'][1]);assert v not in vals;vals.append(v);C['choices']+=1
   if f[':answer-field/type'].endswith('/radio'):
    expected={(name.lower(),i+di,j+dj) for di,dj in profiles[r['generation']['profile']]};assert len(vals)==5 and set(vals)==expected;C['whole_banks']+=1
  C['records']+=1
 out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
