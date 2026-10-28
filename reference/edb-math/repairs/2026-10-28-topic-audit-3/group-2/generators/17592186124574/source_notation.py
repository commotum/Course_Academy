"""Explicit per-KP source roles, applied before assigning final content UUIDs.
No source-family selection, mathematical value, bank, or truth-mask changes.
"""
import copy,functools,hashlib,json,re,uuid
from pathlib import Path
from math_format import MATH,normalize_prose,normalize_tex,validate_generated_record
VERSION='source-vector-fonts-2026-10-28-v1'
ROLES=['F', 'i', 'j', 'k'] # Filled per reviewed package; not inferred from arbitrary variable names.
def styled_math(value):
 def walk(s):
  out='';i=0
  while i<len(s):
   if s[i]=='\\':
    m=re.match(r'\\[A-Za-z]+|\\.',s[i:]);token=m[0]if m else'\\';out+=token;i+=len(token)
    if token in ('\\mathbf','\\boldsymbol','\\mathbb','\\mathcal','\\text','\\textrm','\\mathrm','\\operatorname'):
     while i<len(s)and s[i].isspace():out+=s[i];i+=1
     if i<len(s)and s[i]=='{':
      j=i+1;depth=1
      while j<len(s)and depth:
       if s[j]=='{':depth+=1
       if s[j]=='}':depth-=1
       j+=1
      out+=s[i:j];i=j
     elif i<len(s):out+=s[i];i+=1
    continue
   c=s[i]
   # Subscripted components are scalar coordinates. Plain vector/function
   # symbols in this explicit mathematical role receive the source font.
   before=s[i-1]if i else'';after=s[i+1]if i+1<len(s)else''
   if c in ROLES and not before.isalpha()and not after.isalpha()and after!='_':out+='\\mathbf{'+c+'}'
   else:out+=c
   i+=1
  return out
 return walk(value)
def prose(value):
 def one(m):
  n=2 if m[0].startswith('$$')else 1
  return m[0][:n]+styled_math(m[0][n:-n])+m[0][-n:]
 return normalize_prose(MATH.sub(one,value))
def raw_replay(record):
 g=record.get('generation',{})
 return any(g.get(k)for k in ('source_replay','replay_source','replay_only','evidence_only','raw_observed','observed_replay'))or g.get('profile')in ('observed','raw')
def asset_identity(value):
 def one(path):
  p=Path(path)
  return 'asset-sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()if p.is_file()else path
 if value.endswith(('.png','.svg'))and Path(value).is_file():return one(value)
 return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',lambda m:'!['+m[1]+']('+one(m[2])+')',value)
def apply(record):
 if isinstance(record,list):return[apply(x)for x in record]
 if not isinstance(record,dict)or not isinstance(record.get('question'),dict)or raw_replay(record):return record
 r=copy.deepcopy(record);q=r['question'];old=copy.deepcopy(q)
 for a in (':question/problem',':question/worked-solution'):
  if a in q:q[a]=prose(q[a])
 for f in q.get(':question/answer-fields',[]):
  if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for aa in f.get(':answer-field/choices',[]):
   if isinstance(aa[':answer/type'],dict):aa[':answer/type']=aa[':answer/type'][':db/ident']
  if f[':answer-field/type']==':answer-field.type/checkbox':f[':answer-field/key']=prose(f[':answer-field/key'])
  for a in f.get(':answer-field/choices',[]):
   if a[':answer/type']==':answer.type/math':a[':answer/value']=normalize_tex(styled_math(a[':answer/value']))
   elif a[':answer/type']==':answer.type/text':a[':answer/value']=prose(a[':answer/value'])
   if ':answer/feedback'in a:a[':answer/feedback']=prose(a[':answer/feedback'])
 # Identity includes final normalized authored values, not provisional IDs,
 # option order, seed, caller paths, or original source IDs.
 content={k:asset_identity(v)if isinstance(v,str)else v for k,v in q.items()if k not in (':question/id',':question/answer-fields',':db/id')}
 content['fields']=[];right_by_field=[]
 for f in q.get(':question/answer-fields',[]):
  right=f[':answer-field/correct'];right=right[1]if isinstance(right,list)else right[':answer/id']
  right_value=next(a for a in f[':answer-field/choices']if a[':answer/id']==right)
  av=lambda a:{k:asset_identity(v)if isinstance(v,str)else v for k,v in a.items()if k not in (':answer/id',':db/id')}
  content['fields'].append({'key':f[':answer-field/key'],'type':f[':answer-field/type'],'choices':sorted([av(a)for a in f[':answer-field/choices']],key=lambda x:json.dumps(x,sort_keys=True)),'correct':av(right_value)})
  right_by_field.append(right)
 content['fields'].sort(key=lambda f:f['key']);canonical=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
 id_mapping={}
 qid=str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+canonical(content)));id_mapping[q.get(':question/id')]=qid;q[':question/id']=qid
 for f,right in zip(q[':question/answer-fields'],right_by_field):
  fid=str(uuid.uuid5(uuid.UUID(qid),f[':answer-field/key']));id_mapping[f.get(':answer-field/id')]=fid;f[':answer-field/id']=fid
  for a in f[':answer-field/choices']:
   old_id=a[':answer/id'];a[':answer/id']=str(uuid.uuid5(uuid.UUID(fid),a[':answer/type']+asset_identity(a[':answer/value'])))
   id_mapping[old_id]=a[':answer/id']
   if old_id==right:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
 def remap(v):
  if isinstance(v,dict):return {id_mapping.get(k,k):remap(x)for k,x in v.items()}
  if isinstance(v,list):return[remap(x)for x in v]
  return id_mapping.get(v,v)if isinstance(v,str)else v
 r['generation']=remap(r.get('generation',{}));r['generation']['source_notation_version']=VERSION
 return validate_generated_record(r)
_depth=0
def wrap(function,is_main=False):
 @functools.wraps(function)
 def checked(*args,**kwargs):
  global _depth
  outer=_depth==0;_depth+=1
  try:result=function(*args,**kwargs)
  finally:_depth-=1
  return apply(result)if outer and not is_main and not kwargs.get('replay') else result
 return checked
def install(namespace):
 for key in ('generate','generate_records','generate_normal','make_record','generate_batch','sample','practice'):
  if callable(namespace.get(key)):namespace[key]=wrap(namespace[key])
 if callable(namespace.get('main')):namespace['main']=wrap(namespace['main'],is_main=True)

