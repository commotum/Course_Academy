#!/usr/bin/env python3
"""Draft outer-product generator; never accesses EDB or registered generators.

Easy: observed 2x2, 3x2 and 4x3 masks with <=4 nonunit products.
Moderate: authored 3x2, six nonunit integer products, max15, total60.
Hard: authored 4x3, >=8 nonunit integer products, max50, total240.
Historical profiles are public evidence-only recipes, retaining omitted attributes.
"""
import sys
sys.dont_write_bytecode=True
import argparse,copy,hashlib,json,pathlib,random,re,uuid,platform
ROOT=pathlib.Path(__file__).resolve().parents[2]
D=pathlib.Path(__file__).with_suffix('')
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import matrix_tex,normalize_prose,normalize_tex,validate_prose,validate_tex
KP={'db_id':17592186100913,'id':'3d7d67c6-d54f-5ee1-af59-fd63d6687cfd','title':'Multiplying a Column-Vector By a Row-Vector'}
VERSION='outer-product-draft-v1'
PROFILES=json.loads((D/'templates.json').read_text())
SOURCES={'outer-2x2':['q-129961','q-275545','q-318484'],'outer-3x2':['q-13635','q-275548','q-318588'],'outer-4x3':['q-1038','q-130136']}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+str(x)))
def matrix(rows):return matrix_tex(rows,augmented=False) # Ordinary coefficient matrices, no RHS column.
def outer(a,b):return [[x*y for y in b]for x in a]
def grouped(x):return '('+str(x)+')' if x<0 else str(x)
def validate_parameters(level,template,params,evidence=False):
 if level not in ['easy','moderate','hard']:raise ValueError('unknown level')
 if set(params)!= {'a','b'}:raise ValueError('exactly a and b required')
 a,b=params['a'],params['b']
 if not all(type(x)is int for x in a+b):raise ValueError('integer entries required')
 if (len(a),len(b))not in [(2,2),(3,2),(4,3)]:raise ValueError('unsupported outer-product dimensions')
 if template!='undefined-evidence' and template!='outer-'+str(len(a))+'x'+str(len(b)):raise ValueError('template/shape mismatch')
 p=outer(a,b);ap=[abs(v)for row in p for v in row];nonunit=sum(abs(x)>1 and abs(y)>1 for x in a for y in b)
 if max(map(abs,a+b))>10 or max(ap)>50 or sum(ap)>240:raise ValueError('source-grounded whole-product ceiling exceeded')
 if evidence:return
 if not any(a)or not any(b):raise ValueError('zero whole factor makes trivial instance')
 if level=='easy':
  if nonunit>4 or sum(ap)>150:raise ValueError('easy arithmetic workload')
 elif level=='moderate':
  if(len(a),len(b))!=(3,2)or nonunit!=6 or max(map(abs,a+b))>5 or max(ap)>15 or sum(ap)>60:raise ValueError('moderate workload')
 elif(len(a),len(b))!=(4,3)or nonunit<8 or sum(ap)>240:raise ValueError('hard workload')
def sample(level,template,rng):
 n,k=map(int,template.removeprefix('outer-').split('x'))
 for _ in range(10000):
  if level=='easy':
   a=[rng.randint(-10,10)for _ in range(n)];b=[rng.choice([-1,0,1])for _ in range(k)]
   if rng.randrange(2):a=[rng.choice([-1,0,1])for _ in range(n)];b=[rng.randint(-5,5)for _ in range(k)]
  else:
   domain=[-5,-4,-3,-2,2,3,4,5]if level=='moderate'else [-10,-8,-6,-5,-4,-3,-2,2,3,4,5,6,8,10]
   a=[rng.choice(domain)for _ in range(n)];b=[rng.choice(domain)for _ in range(k)]
  params={'a':a,'b':b}
  try:validate_parameters(level,template,params);return params
  except ValueError:pass
 raise ValueError('no complete eligible instance')
def fill(mask,a,b,spec,historical=False):
 p=outer(a,b);first=matrix([b])if spec['reverse']else matrix([[x]for x in a]);second=matrix([[x]for x in a])if spec['reverse']else matrix([[x]for x in b])if spec['undefined']else matrix([b])
 def factor(x,style):return '('+str(x)+')'if style else str(x)
 def product(i,j,styles):
  st=styles[i*len(b)+j]if historical and len(styles)==len(a)*len(b)else [a[i]<0,b[j]<0]
  return factor(a[i],st[0])+r'\cdot '+factor(b[j],st[1])
 products=matrix([[product(i,j,spec.get('product_styles',[]))for j in range(len(b))]for i in range(len(a))])
 subs={'@FIRST@':first,'@SECOND@':second,'@PRODUCTS@':products,'@RESULT@':matrix(p)}
 for count in range(1,5):subs['@PARTIAL'+str(count)+'@']=matrix([[p[i][j]if i*len(b)+j<count else '∗'for j in range(len(b))]for i in range(len(a))])
 for i in range(4):
  x,y=divmod(i,len(b));subs['@CELL'+str(i)+'@']=r'\,'+str(p[x][y])+'='+product(x,y,spec.get('cell_styles',[]))
 for old,new in subs.items():mask=mask.replace(old,new)
 if '@'in mask:raise ValueError('unfilled structural slot')
 return normalize_prose(mask)
def render_fields(spec,a,b,normal_profile=None,field_type=None):
 p=outer(a,b);out=[]
 if normal_profile:
  if field_type==':answer-field.type/blank':
   for i,row in enumerate(p):
    for j,value in enumerate(row):out.append({'key':'field-'+str(i*len(b)+j+1),'type':field_type,'choices':[(str(value),':answer.type/math')],'correct':0})
   return out
  # Whole method-derived bank is selected before parameters: correct, transpose,
  # add instead of multiply, reverse every sign, undefined. No pool replacement.
  values=[matrix(p),matrix(list(map(list,zip(*p)))),matrix([[x+y for y in b]for x in a]),matrix([[-v for v in row]for row in p]),'Undefined']
  return [{'key':'selection','type':':answer-field.type/radio','choices':[(v,':answer.type/text'if v=='Undefined'else ':answer.type/math')for v in values],'correct':0}]
 for f in spec['fields']:
  choices=[]
  for c in f['choices']:
   value='Undefined'if c['recipe']=='undefined'else eval(c['recipe'],{'__builtins__':{},'matrix':matrix,'a':a,'b':b,'p':p,'str':str,'len':len,'min':min,'range':range,'sum':sum,'abs':abs},{})
   if c['type']==':answer.type/text'and c['raw'].startswith('$$'):value='$$\n'+value+'\n$$'
   choices.append((normalize_tex(value)if c['type']==':answer.type/math'else normalize_prose(value),c['type']))
  out.append({'key':f[':answer-field/key'],'type':f['type'],'choices':choices,'correct':f.get('correct_index')})
 return out
def eligible_bank(fields):
 for f in fields:
  vals=[x[0]for x in f['choices']]
  if len(vals)!=len(set(vals)):return False
  # Method-derived 2x2 transpose and other mathematical collisions are exact
  # integer matrices; their canonical printed strings coincide iff equal.
  nums=[int(v)for value,_ in f['choices']for v in re.findall(r'(?<![A-Za-z])(?<!\d)-?\d+',value)]
  if nums and(max(map(abs,nums))>50 or sum(map(abs,nums))>600):return False
 return True

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 rng=random.Random(seed);historical=profile in PROFILES
 authored_family=profile.split('/',1)[1]if profile and profile.startswith('authored-method/')else None
 if profile and not historical and profile!='authored-method'and authored_family not in sum(SOURCES.values(),[]):raise ValueError('unknown profile')
 if field_type in ['radio','blank']:field_type=':answer-field.type/'+field_type
 if field_type and field_type not in [':answer-field.type/radio',':answer-field.type/blank']:raise ValueError('unsupported field type')
 if historical:
  spec=copy.deepcopy(PROFILES[profile]);template=template or spec['template']
  if template!=spec['template']:raise ValueError('source profile/template mismatch')
  expected=spec['difficulty'].split('/')[-1]if spec['difficulty']else 'easy'
  if level!=expected:raise ValueError('source profile label/routing mismatch')
  if field_type and any(f['type']!=field_type for f in spec['fields']):raise ValueError('source field contract mismatch')
  params=copy.deepcopy(parameters if parameters is not None else spec['parameters']);validate_parameters(level,template,params,True)
  fields=render_fields(spec,params['a'],params['b'])
  if not eligible_bank(fields):raise ValueError('historical complete-bank ambiguity or arithmetic ceiling')
 else:
  options=['outer-2x2','outer-3x2','outer-4x3']if level=='easy'else ['outer-3x2']if level=='moderate'else ['outer-4x3']if level=='hard'else []
  if template and template not in options:raise ValueError('level/template incompatible')
  if not options:raise ValueError('unknown level')
  if authored_family:
   expected_template=PROFILES[authored_family]['template']
   if template and template!=expected_template:raise ValueError('profile/template mismatch')
   template=expected_template
   if template not in options:raise ValueError('profile/level mismatch')
  template=template or rng.choice(options);field_type=field_type or (':answer-field.type/radio'if parameters is not None else rng.choice([':answer-field.type/radio',':answer-field.type/blank']))
  # Family and entire bank chosen before numerical parameters.
  family=authored_family or (SOURCES[template][int(digest(parameters),16)%len(SOURCES[template])]if parameters is not None else rng.choice(SOURCES[template]));spec=copy.deepcopy(PROFILES[family]);spec['reverse']=False;spec['undefined']=False
  if field_type==':answer-field.type/blank':
   spec=copy.deepcopy(PROFILES['q-275545'if template=='outer-2x2'else 'q-275548'if template=='outer-3x2'else family])
   if template=='outer-4x3':spec['prompt_mask']+='\n\n'+ '\n'.join('| '+' | '.join('{{field-'+str(i*3+j+1)+'}}'for j in range(3))+' |'for i in range(4))
  else:spec['prompt_mask']=spec['prompt_mask'].split('\n\n|')[0]
  for _ in range(10000):
   params=copy.deepcopy(parameters)if parameters is not None else sample(level,template,rng)
   validate_parameters(level,template,params)
   fields=render_fields(spec,params['a'],params['b'],'authored-method',field_type)
   if eligible_bank(fields):break
   if parameters is not None:raise ValueError('complete bank collision or workload ceiling')
  else:raise ValueError('no eligible complete bank')
  profile='authored-method/'+family
 a,b=params['a'],params['b'];prompt=fill(spec['prompt_mask'],a,b,spec,historical);solution=fill(spec['solution_mask'],a,b,spec,historical)
 # Correct the captured2x2 staggered blank table in normal output only;
 # retain every key, scalar fragment and row-major answer role.
 if not historical and field_type==':answer-field.type/blank'and template=='outer-2x2':
  prompt=prompt.split('\n\n|')[0]+'\n\n| {{field-1}} | {{field-2}} |\n| --- | --- |\n| {{field-3}} | {{field-4}} |'
 # Authored4x3 blanks use a real Markdown table with one header/separator.
 if not historical and field_type==':answer-field.type/blank'and template=='outer-4x3':
  prompt=prompt.split('\n\n|')[0]+'\n\n| '+' | '.join('{{field-'+str(j+1)+'}}'for j in range(3))+' |\n| --- | --- | --- |\n'+'\n'.join('| '+' | '.join('{{field-'+str(i*3+j+1)+'}}'for j in range(3))+' |'for i in range(1,4))
 for text in [prompt,solution]:
  validate_prose(text)
  if any(ord(c)<32 and c not in '\n\t\r'for c in text):raise ValueError('control character')
 content={'version':VERSION,'level':level if not historical or spec['difficulty']else None,'prompt':prompt,'solution':solution if spec['solution_present']or not historical else None,'fields':fields}
 content_hash=digest(content);question={':question/id':uid(content_hash),':question/problem':prompt}
 if not historical or spec['difficulty']:question[':question/difficulty']=':question.difficulty/'+level
 if not historical or spec['solution_present']:question[':question/worked-solution']=solution
 owned=[]
 for i,f in enumerate(fields):
  fid=uid(content_hash+'field'+str(i));choices=[]
  for j,(value,atype)in enumerate(f['choices']):
   if atype==':answer.type/math':validate_tex(value)
   choices.append({':answer/id':uid(fid+str(j)+value),':answer/type':atype,':answer/value':value})
  entry={':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':f['type'],':answer-field/choices':choices}
  if f['correct']is not None:entry[':answer-field/correct']=[':answer/id',choices[f['correct']][':answer/id']]
  if f['type']==':answer-field.type/radio':rng.shuffle(choices)
  owned.append(entry)
 if not historical or spec['fields_present']:question[':question/answer-fields']=owned
 return {'knowledge_point':KP.copy(),'question':question,'generation':{'version':VERSION,'seed':seed,'level':level,'template':template,'profile':profile,'family':family if not historical else profile,'parameters':params,'mathematical_fingerprint':digest({'a':a,'b':b,'undefined':spec['undefined'],'reverse':spec['reverse']}),'content_sha256':content_hash,'evidence_only':historical,'eligible_for_learning':not historical,'source_basis':2275,'python':platform.python_version(),'matrix_role':'ordinary coefficient matrix','bank_interpretation':'opaque historical recipes; inferred intentions unresolved'if historical and spec['opaque_bank']else 'complete method-derived bank'if not historical else 'observed bank'}}

# Easy: same observed family masks, small nonunit workload; no added skill.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: authored six signed nonunit products in the same outer-product stages.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: authored4x3, eight to twelve nonunit products; no dot-product reversal.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(record):
 q=record['question'];g=record['generation'];parts=[f"### {g['level']} / {g['template']} / {g['profile']}",q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1];parts.append(f"Field {f[':answer-field/key']}: {f[':answer-field/type']}")
  if correct is None:parts.append('Raw source missing correct designation.')
  for a in f[':answer-field/choices']:parts.append(('* correct: 'if a[':answer/id']==correct else '* ')+a[':answer/value'])
 parts.extend(['Worked solution:',q.get(':question/worked-solution','Raw source missing worked solution.')]);return '\n\n'.join(parts)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args();levels=['easy','moderate','hard']if args.difficulty=='all'else [args.difficulty]
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile)for level in levels for i in range(args.count)];print(json.dumps(records,indent=2)if args.format=='json'else '\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
