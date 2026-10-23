"""Independent visible-record parsers/checks retained from prior review; batch driver replaced by check_repair.py."""
import json,re,sys,importlib.util,collections,hashlib,pathlib,copy,platform,subprocess,shutil
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent; PKG=ROOT.parent; JOB=PKG.parent; REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(p,x): (ROOT/p).write_text(json.dumps(x,indent=2,default=str))
def load(p):return json.load(open(p))
def module(p):
 s=importlib.util.spec_from_file_location('review_gen',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=module(PKG/'17592186161968.py')
def mats(s):return [[[int(v.strip()) for v in row.split('&')] for row in raw.split(r'\\')] for raw in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)]
def ops(s):
 s=re.sub(r'\s+','',s).replace('{C}','C').replace('{','').replace('}','').replace(':&=',':=')
 out=[]
 for i,j,sign,n,p in re.findall(r'C_(\d):=C_(\d)([+-])(\d*)C_(\d)',s):
  assert i==j
  out.append((int(i)-1,int(p)-1,int(sign+(n or '1'))))
 return out

def apply(A,os):
 B=copy.deepcopy(A)
 for i,p,k in os:
  for r in range(3): B[r][i]+=k*B[r][p]
 return B

def field(rec):return rec['question'][':question/answer-fields'][0]
def choices(rec):return field(rec)[':answer-field/choices']
def correctid(rec):
 k=field(rec)[':answer-field/correct'];return k[1] if isinstance(k,list) else k[':answer/id']
def optionpairs(rec):return [tuple(x[2] for x in ops(c[':answer/value'])) for c in choices(rec)]
def check(rec):
 q=rec['question']; A,B=mats(q[':question/problem']); cs=choices(rec)
 truth=[apply(A,ops(c[':answer/value']))==B and len(ops(c[':answer/value']))==2 for c in cs]
 assert sum(truth)==1 and cs[truth.index(True)][':answer/id']==correctid(rec)
 sm=mats(q[':question/worked-solution']);co=ops(cs[truth.index(True)][':answer/value'])
 assert sm==[A,apply(A,co[:1]),B]
 assert ops(q[':question/worked-solution'])==co+co
 return {'id':q[':question/id'],'correct_index':truth.index(True),'coefficients':optionpairs(rec)[truth.index(True)],'matrix_check':True,'solution_check':True}

def modal(rec):
 pairs=optionpairs(rec);freq=[collections.Counter(t[i] for t in pairs) for i in range(2)]
 modes=[[k for k,v in f.items() if v==max(f.values())] for f in freq]
 indices=[i for i,t in enumerate(pairs) if all(t[j] in modes[j] for j in range(2))]
 unique=len(modes[0])==len(modes[1])==len(indices)==1
 chosen=indices[0] if unique else None
 return {'unique_component_modes':unique,'selected_index':chosen,'correct':chosen is not None and choices(rec)[chosen][':answer/id']==correctid(rec),'pairs':pairs,'frequencies':[dict(x) for x in freq]}

def summarize(records):
 groups={}
 for r in records:
  p=r['generation']['bank_profile'];g=groups.setdefault(p,{'count':0,'mode_attempts':0,'mode_correct':0,'correct_positions':collections.Counter(),'row_pivot':set(),'signs':set()});g['count']+=1
  c=check(r);pr=modal(r);g['mode_attempts']+=pr['unique_component_modes'];g['mode_correct']+=pr['correct'];g['correct_positions'][c['correct_index']]+=1
  pa=r['generation']['parameters'];g['row_pivot'].add((pa['row'],pa['pivot']));g['signs'].add(tuple(1 if k>0 else -1 for k in c['coefficients']))
 for g in groups.values():g['row_pivot']=sorted(g['row_pivot']);g['signs']=sorted(g['signs'])
 return groups
