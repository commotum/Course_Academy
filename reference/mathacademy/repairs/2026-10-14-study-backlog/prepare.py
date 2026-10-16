"""Prepare, never apply, image-equation and matrix-layout repairs."""
import hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'))
from edn import dumps,kw
from math_format import ENV,MATH,environment,matrix_tex,normalize_prose,normalize_tex,validate_prose,validate_tex
IMAGES=json.loads((H/'images.json').read_text());RECOVERY={x['path']:x for x in json.loads((H/'svg-recovery.json').read_text()) if 'tex' in x}
M=Path('/media/jake/SSD/EDB/math')
def blue(x):return r'{\color{blue}'+str(x)+'}'
def red(x):return r'{\color{red}'+str(x)+'}'
def pivot(x):return r'\bbox[lightgray,2pt]{'+blue(x)+'}'
def matrix(rows):return matrix_tex(rows)
def pair(a,b):return 'A='+matrix(a)+r',\qquad B='+matrix(b)
MANUAL={
 '627d12115d61ddfdedf9db08330269de2137a23abceada977d039e90e5b88675':'A='+matrix([[1,2,3],[4,2,-1],[7,12,13]]),
 '82729e1d34174d58f01547b58aa63db28ec68a4e1964ef5cd127a2167ed4a722':'A='+matrix_tex([[-1,5,4,1],[1,0,5,2],[3,7,1,9]],augmented=True),
 '56fd7e343edf6c26f36718a30f899af6c8eaf0cad5f6b07c90ffa93c19df6346':pair([[-4,-2,4],[4,1,2],[1,2,3]],[[-4,-2,4],[0,-1,6],[1,2,3]]),
 '59ee8e91d058e347238320a2bd5496630f33534564f67f901d2ddf89000f0108':'A='+matrix([[3,1,-2],[-1,5,6],[0,2,4]]),
 '1d7b89b6790ed713a8885b5124d988cda34cccff589ceaef9d556708bc21233f':pair([[-1,2,1,5],[blue(1),pivot(1),blue(2),blue(-1)],[-1,3,1,1],[0,-2,1,5]],[[-3,red(0),-3,7],[blue(1),pivot(1),blue(2),blue(-1)],[-4,red(0),-5,4],[2,red(0),5,3]]),
 '81176c8bb51128cdaf5d72842e2b2b909b1c41d63249eb3640d745bc9e0c7f9b':pair([[7,blue(-3),-1,-6],[7,blue(-2),-2,-4],[-5,pivot(1),4,2],[-8,blue(-3),-6,-4]],[[-8,blue(-3),11,0],[-3,blue(-2),6,0],[red(0),pivot(1),red(0),red(0)],[-23,blue(-3),6,2]]),
 '572d87625c3056d795203d2592c72aa063d1e125d386365ea620b4b596869085':pair([[pivot(1),blue(4),blue(-7)],[2,2,-8],[-3,-2,1]],[[pivot(1),blue(4),blue(-7)],[red(0),-6,6],[red(0),10,-20]]),
 '941de9bd4837b4b5c9f0d2bf64c4ea0fd9be657b0368d03cac169742083822d1':pair([[-6,-5,pivot(1)],[8,3,blue(-4)],[9,7,blue(-2)]],[[red(0),red(0),pivot(1)],[-16,-17,blue(-4)],[-3,-3,blue(-2)]])}
for item in IMAGES:
 digest=Path(item['path']).stem
 if digest in MANUAL:
  RECOVERY[item['path']]={**item,'tex':MANUAL[digest],'source_sha256':hashlib.sha256((M/item['path']).read_bytes()).hexdigest(),'method':'Visually transcribed from original PNG; checked against worked-solution matrices and operations'}
(H/'image-replacements.json').write_text(json.dumps(list(RECOVERY.values()),indent=2)+'\n')
def top_spans(text):
 """Only split at root level, preserving nested matrix and equation rows."""
 spans=[];stack=[];depth=0;i=0
 while i<len(text):
  env=ENV.match(text,i)
  if env:
   if env[1]=='begin':stack.append(env[2])
   else:assert stack and stack.pop()==env[2]
   i=env.end();continue
  if not stack and not depth:
   m=re.match(r'(?:,\s*(?:\\(?:quad|qquad|,|;|!|enspace|hspace\{[^}]*\})\s*)*|\\(?:quad|qquad)\s*)',text[i:])
   if m:spans.append((i,i+m.end()));i+=m.end();continue
  if text[i]=='\\':
   m=re.match(r'\\[A-Za-z]+|\\.',text[i:]);i+=len(m[0]) if m else 1;continue
  if text[i]=='{':depth+=1
  elif text[i]=='}':depth-=1
  i+=1
 return spans

def display_stack(tex):
 spans=top_spans(tex);chunks=[];start=0
 for a,b in spans:chunks.append(tex[start:a].strip());start=b
 chunks.append(tex[start:].strip())
 # Require each independent piece to contain a structured math expression;
 # scalar commas, vector coordinates and prose annotations are not a list.
 if len(chunks)>1 and all(re.search(r'\\begin\{(?:bmatrix|array|aligned)\}',c) for c in chunks):
  return '\n\n'.join('$$\n'+c+'\n$$' for c in chunks)
 # Retain the direction of a before/after matrix transformation, on two rows.
 if r'\longrightarrow' in tex and tex.count(r'\begin{bmatrix}')==2 and r'\begin{aligned}' not in tex:
  left,right=tex.split(r'\longrightarrow',1)
  left=re.sub(r'(?:\\quad\s*)+$','',left).strip();right=re.sub(r'^(?:\s*\\quad)+','',right).strip()
  return '$$\n'+r'\begin{aligned}'+left.replace('=', ' &=',1)+r' \\ &\longrightarrow '+right+r'\end{aligned}'+'\n$$'
 return '$$\n'+tex+'\n$$'

fields=json.loads((H/'fields.json').read_text());changes=[];retained=[]
for f in fields:
 old=f['before'];new=old;reasons=[]
 def replace_image(match):
  path=match[1]
  if path not in RECOVERY:
   retained.append({'entity':f['entity'],'attribute':f['attribute'],'path':path,'reason':'Intentional shaded row-echelon schematic, not a formula screenshot'})
   return match[0]
  reasons.append('recover formula image as semantic TeX')
  return '\n\n'+display_stack(validate_tex(normalize_tex(RECOVERY[path]['tex'])))+'\n\n'
 new=re.sub(r'!\[[^\]]*\]\(([^)]+)\)',replace_image,new)
 def replace_math(m):
  display=m[0].startswith('$$')
  if not display and not re.search(r'\\begin\{(?:bmatrix|array)\}',m[0]):return m[0]
  size=2 if display else 1
  result=display_stack(m[0][size:-size].strip())
  if not display:reasons.append('promote matrix from unbounded inline math to display math')
  if result.count('$$')>2 or r'\longrightarrow' in result and r'\begin{aligned}' in result and r'\begin{aligned}' not in m[0]:reasons.append('stack independent matrices or transformation vertically')
  return result
 new=MATH.sub(replace_math,new)
 if f['kind']=='prose':new=validate_prose(normalize_prose(new))
 else:new=validate_tex(normalize_tex(new))
 # HTML image replacement leaves only harmless blank-line differences.
 if new!=old:
  new=re.sub(r'\n{3,}','\n\n',new)
  f['after']=new;changes.append({**f,'reasons':sorted(set(reasons))})
 else:f['after']=old
(H/'fields.json').write_text(json.dumps(fields,indent=2)+'\n')
(H/'changes.json').write_text(json.dumps(changes,indent=2)+'\n')
(H/'retained-images.json').write_text(json.dumps(retained,indent=2)+'\n')
(H/'all-expected.edn').write_text(dumps([[f['entity'],kw(f['attribute']),f['after']] for f in fields]))
forms=[[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']] for f in changes]
transaction=H/'transaction.edn';payload=dumps(forms)
if transaction.exists() and transaction.read_text()!=payload:
 assert not (H/'receipt.edn').exists(), 'Never replace an attempted transaction'
 assert json.loads((H/'commit-intent.json').read_text())['authorized_to_apply'] is False
 previous=hashlib.sha256(transaction.read_bytes()).hexdigest()
 (H/('transaction.draft-'+previous[:12]+'.edn')).write_bytes(transaction.read_bytes())
transaction.write_text(payload);digest=hashlib.sha256(transaction.read_bytes()).hexdigest()
(H/'expected.edn').write_text(dumps([[f[1],f[2],f[4]] for f in forms]))
(H/'read-query.edn').write_text('[:find ?entity ?attr ?value :in $ [[?entity ?attr]] :where [?entity ?attr ?value]]')
(H/'read-inputs.edn').write_text(dumps([[[f[1],f[2]] for f in forms]]))
(H/'commit-intent.json').write_text(json.dumps({'status':'PREPARED ONLY — AWAITING USER', 'authorized_to_apply':False,'database':'math','source':':application/ca-engine','endpoint':'/tmp/edb-math/writer.sock','file':str(transaction),'sha256':digest,'request_key':'study-backlog-'+digest,'snapshot_basis':json.loads((H/'snapshot.json').read_text())['basis'],'fields':len(forms),'entities':len({f[1] for f in forms})},indent=2)+'\n')
print(json.dumps({'fields':len(fields),'changed_fields':len(changes),'recovered_images':len(RECOVERY),'retained_images':retained,'changes_by_reason':{r:sum(r in c['reasons'] for c in changes) for r in {r for c in changes for r in c['reasons']}}}))
