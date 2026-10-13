#!/usr/bin/env python3
"""Triangle vertices -> two ordered differences -> determinant -> norm / 2.

Exact source arithmetic/prose masks, explicit empirical observed banks, separately
labelled operation-derived defaults. Source at math basis 1356. No DB access.
Easy and hard are authored workload policies, not recovered MA labels.
All plots: none. CLI previews are local records, never transaction payloads.
"""
import argparse,hashlib,itertools,json,random,re,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text()); RAW=CAPTURE['record']
KP_ID=17592186105733; VERSION='triangle-vertices-v1'
SOURCES={q[':question/math-academy-id']:q for q in RAW[':knowledge-point/questions']}

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def ident(obj):return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(obj)))
def tex(x):return sp.latex(sp.simplify(x)).replace(' ','')
def vector(v,zeros=False):
 out=''
 for n,b in zip(v,'ijk'):
  if not n and not zeros:continue
  sign='-' if n<0 else ('+' if out else '')
  out+=sign+('' if abs(n)==1 else str(abs(n)))+b
 return out or '0'
def coords(v):return '⟨'+','.join(map(str,v))+'⟩'
def grouped(n):return '('+str(n)+')' if n<0 else str(n)
def numeric(s):
 s=s.replace(r'\cdot','*').replace('{','(').replace('}',')').replace('^','**')
 return sp.sympify(s)
def scalar(s):
 # Source area banks contain only integer/radical/fraction values.
 if s.startswith(r'\frac'):
  m=re.fullmatch(r'\\frac\{(.*)\}\{(\d+)\}',s);return scalar(m[1])/int(m[2])
 m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',s)
 return sp.Integer(m[1] or 1)*sp.sqrt(int(m[2])) if m else sp.Rational(s)
def vertices(q):return [[int(x.strip()) for x in m[1].split(',')] for m in re.findall(r'([A-Z])\(([^()]*)\)',q[':question/problem'])]
def calculation(p):
 a,b,c=[sp.Matrix(v) for v in p['vertices']];u=b-a;v=c-a;w=u.cross(v);n=w.dot(w)
 return [list(x) for x in (u,v,w)]+[n,sp.sqrt(n)/2]
def outer_blocks(sol):return re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)

def extract(q):
 p={'vertices':vertices(q)};u,v,w,n,area=calculation(p)
 labels=''.join(m[0] for m in re.findall(r'([A-Z])\(([^()]*)\)',q[':question/problem']))
 prompt=q[':question/problem']
 for i,match in reversed(list(enumerate(re.finditer(r'([A-Z])\(([^()]*)\)',prompt)))):
  # Slot the whole coordinate tuple, never the short numbers.
  prompt=prompt[:match.start(2)]+'{V'+str(i)+'}'+prompt[match.end(2):]
 sol=q.get(':question/worked-solution')
 if not sol:return {'prompt':prompt,'labels':labels,'authored_solution':True,'coordinate_spaces':', ' in q[':question/problem']}
 blocks=outer_blocks(sol);assert len(blocks)==4
 # Construct vector rows by replacing complete RHSs; grouping is source style.
 b0=blocks[0];expressions=re.findall(r' & =(.*?)(?= \\\\ |\\end\{aligned\})',b0)
 assert len(expressions)==8,(q[':question/math-academy-id'],expressions)
 masks=[]
 for i,e in enumerate(expressions):
  if i in (0,4):masks.append(e)
  elif i in (1,5):
   end=1 if i==1 else 2
   # Original parentheses around each full position vector are retained.
   lhs=vector(p['vertices'][end]);rhs=vector(p['vertices'][0])
   assert e in ('('+lhs+')-('+rhs+')','('+lhs+')-'+rhs)
   masks.append('{POS'+str(end)+'}-'+('{POS0}' if e.endswith(')') else '{BARE0}'))
  elif i in (2,6):masks.append('{EDGE'+str(i//4)+'}')
  else:masks.append('{TUP'+str(i//4)+'}')
 for old,new in zip(expressions,masks):b0=b0.replace(' & ='+old,' & ='+new,1)
 # Replace complete determinant and component stages in top-level row RHSs.
 b1=blocks[1];rs=re.split(r' \\\\  & =',b1)
 assert len(rs)==5
 first=rs[0];det_start=first.index(' & =')+5
 def num_mask(s,slots):
  numbers=list(re.finditer(r'(?<![A-Za-z])-?\d+',s));assert len(numbers)==len(slots),(s,slots)
  for m,slot in reversed(list(zip(numbers,slots))):s=s[:m.start()]+'{'+slot+'}'+s[m.end():]
  return s
 first=first[:det_start]+num_mask(first[det_start:],['u0','u1','u2','v0','v1','v2'])
 minor=num_mask(rs[1],['u1','u2','v1','v2','u0','u2','v0','v2','u0','u1','v0','v1'])
 # Each scalar product has two ordered factors; preserve original commutations.
 arithmetic=rs[2];products=re.findall(r'(\(-?\d+\)|\d+)\\cdot (\(-?\d+\)|\d+)',arithmetic)
 assert len(products)==6,products
 pairs=[('u1','v2'),('u2','v1'),('u0','v2'),('u2','v0'),('u0','v1'),('u1','v0')]
 data={f'{k}{i}':int(z) for k,vs in [('u',u),('v',v)] for i,z in enumerate(vs)}
 for (a,b),(s,t) in zip(products,pairs):
  av,bv=int(a.strip('()')),int(b.strip('()'))
  if (av,bv)!=(data[s],data[t]):assert (av,bv)==(data[t],data[s]),(q[':question/math-academy-id'],a,b,s,t,data);s,t=t,s
  arithmetic=arithmetic.replace(a+r'\cdot '+b,'{G'+s+'}'+r'\cdot '+'{G'+t+'}',1)
 b1=' \\\\  & ='.join([first,minor,arithmetic,'{CROSS}',rs[4].replace(coords(w),'{WTUP}')])
 # Source norm row count/style remain fixed. Braces and sign conventions preserved.
 b2=blocks[2];parts=re.split(r' \\\\  & =',b2);squares=parts[1]
 square_matches=list(re.finditer(r'(\(-?\d+\)|\{\d+\})\^\{2\}',squares));assert len(square_matches)==3
 for i,m in reversed(list(enumerate(square_matches))):
  val=int(m[1].strip('{}()'));mode='ABS' if val>=0 and w[i]<0 else ''
  squares=squares[:m.start(1)]+'{SQ'+mode+str(i)+'}'+squares[m.end(1):]
 newparts=[parts[0],squares]
 for j,part in enumerate(parts[2:]):
  end=j==len(parts)-3
  if end:newparts.append(re.sub(r'\\sqrt\{.*?\}|\d+\\sqrt\{.*?\}|\d+',lambda m:'{NORM}',part,count=1))
  else:
   body=re.search(r'\\sqrt\{(.*?)\}',part)[1]
   val='{SUMSQ}' if '+' in body else '{N}'
   newparts.append(part.replace(body,val,1))
 b2=' \\\\  & ='.join(newparts)
 # Replace full final numerical chain, retaining source half/norm/final stages.
 b3=blocks[3];tail=b3.split(r'\frac{1}{2}A=')[1].rstrip('.')
 if '=' in tail:
  before,after=tail.split('=');newtail=r'\frac{{NORM}}{2}'+'={AREA}'
 elif tail==r'\frac{1}{2}':newtail='{AREA}'
 elif tail=='1':newtail='{AREA}'
 else:newtail=r'\frac{{NORM}}{2}'
 at=b3.index(r'\frac{1}{2}A=')+len(r'\frac{1}{2}A=');b3=b3[:at]+newtail+b3[at+len(tail):]
 mask=sol
 for old,new in zip(blocks,[b0,b1,b2,b3]):mask=mask.replace(old,new,1)
 return {'prompt':prompt,'solution':mask,'labels':labels,'authored_solution':False,
  'edge_zeros':[bool(re.search(r'0[ijk]',expressions[j])) for j in (2,6)],
  'cross_zeros':bool(re.search(r'0[ijk]',rs[3])),
  'unreduced_norm':bool(re.fullmatch(r'\\sqrt\{'+str(n)+r'\}\.',parts[-1].split(r'\end{aligned}')[0]))}

SPECS={sid:extract(q) for sid,q in SOURCES.items()}
TEMPLATES={sid:('moderate',q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]) for sid,q in SOURCES.items()}
TEMPLATES.update({f'authored_{lv}_{ft}':(lv,ft) for lv in ('easy','moderate','hard') for ft in ('blank','radio')})

def apply(mask,slots):
 # Slots are complete component masks with unique names; existing TeX braces survive.
 return re.sub(r'\{([A-Z][A-Za-z0-9]*|[uv][012])\}',lambda m:str(slots[m[1]]) if m[1] in slots else m[0],mask)

def solution(spec,p):
 u,v,w,n,area=calculation(p);a,b,c=p['vertices'];l=spec['labels']
 vals={f'V{i}':(', ' if spec.get('coordinate_spaces') else ',').join(map(str,pt)) for i,pt in enumerate((a,b,c))}
 for i,pt in enumerate((a,b,c)):vals['POS'+str(i)]='('+vector(pt)+')'
 base_expr=vector(a);vals['BARE0']=base_expr if re.fullmatch(r'\d*[ijk]',base_expr) else '('+base_expr+')'
 for key,vec in [('u',u),('v',v)]:
  for i,x in enumerate(vec):vals[key+str(i)]=str(x);vals['G'+key+str(i)]=grouped(x)
 for i,e in enumerate((u,v)):vals['EDGE'+str(i)]=vector(e,spec.get('edge_zeros',[False,False])[i]);vals['TUP'+str(i)]=coords(e)
 vals.update(CROSS=vector(w,spec.get('cross_zeros',False)),WTUP=coords(w),N=str(n),NORM=(r'\sqrt{'+str(n)+'}' if spec.get('unreduced_norm') else tex(sp.sqrt(n))),AREA=tex(area),SUMSQ='+'.join(str(int(x*x)) for x in w if x))
 for i,x in enumerate(w):
  vals['SQ'+str(i)]=grouped(x) if x<0 else '{'+str(x)+'}'
  vals['SQABS'+str(i)]='{'+str(abs(x))+'}'
 if not spec.get('authored_solution'):
  return apply(spec['solution'],vals),apply(spec['prompt'],vals)
 uv=r'\overset{\to }{'+l[:2]+'}';vv=r'\overset{\to }{'+l[0]+l[2]+'}'
 det=lambda rows:'|'+r'\begin{aligned}'+' \\\\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{aligned}'+'|'
 expr='('+grouped(u[1])+r'\cdot '+grouped(v[2])+'-'+grouped(u[2])+r'\cdot '+grouped(v[1])+')i-('+grouped(u[0])+r'\cdot '+grouped(v[2])+'-'+grouped(u[2])+r'\cdot '+grouped(v[0])+')j+('+grouped(u[0])+r'\cdot '+grouped(v[1])+'-'+grouped(u[1])+r'\cdot '+grouped(v[0])+')k'
 align=lambda rows:r'\begin{aligned}'+' \\\\ '.join(rows)+r'\end{aligned}'
 block=lambda x:'$$\n'+x+'\n$$'
 construction=[]
 for end,e,name in [(1,u,uv),(2,v,vv)]:construction.extend([name+' & ='+l[end].lower()+'-'+l[0].lower(),' & =('+vector(p['vertices'][end])+')-('+vector(a)+')',' & ='+vector(e),' & ='+coords(e)])
 cross=[uv+r'\times '+vv+' & ='+det([['i','j','k'],u,v]),' & ='+det([[u[1],u[2]],[v[1],v[2]]])+'i-'+det([[u[0],u[2]],[v[0],v[2]]])+'j+'+det([[u[0],u[1]],[v[0],v[1]]])+'k',' & ='+expr,' & ='+vector(w),' & ='+coords(w)+'.']
 norm=['A & =|'+uv+r'\times '+vv+'|',' & ='+r'\sqrt{'+ '+'.join(vals['SQ'+str(i)]+'^{2}' for i in range(3))+'}']
 if tex(sp.sqrt(n))!=r'\sqrt{'+str(n)+'}':norm.append(' & ='+r'\sqrt{'+str(n)+'}')
 norm.append(' & ='+tex(sp.sqrt(n))+'.')
 half=r'\frac{'+tex(sp.sqrt(n))+'}{2}';area_chain=half+('='+tex(area) if half!=tex(area) else '')
 text='First, we find the vectors $'+uv+'$ and $'+vv+':$\n\n'+block(align(construction))+'\n\nNow, using the formula to compute the cross product, we get\n\n'+block(align(cross))+'\n\nTherefore, the area of the parallelogram spanned by $'+uv+'$ and $'+vv+'$ is\n\n'+block(align(norm))+'\n\nFinally, the area of the triangle is half of the area of the respective parallelogram. So, the area of $△\\,'+l+'$ is\n\n'+block(r'{A}_{△}=\frac{1}{2}A='+area_chain+'.')
 return text,apply(spec['prompt'],vals)

def guard(p,level,observed=False):
 if set(p)!={'vertices'}:raise ValueError('parameters must contain only vertices')
 pts=p['vertices']
 if len(pts)!=3 or not all(len(v)==3 for v in pts):raise ValueError('exactly three 3D vertices required')
 if any(type(x)!=int for v in pts for x in v):raise ValueError('integer coordinates required')
 u,v,w,n,area=calculation(p)
 if n==0:raise ValueError('collinear vertices')
 bound={'easy':2,'moderate':5,'hard':7}[level]
 if max(abs(x) for e in (u,v) for x in e)>bound:raise ValueError('reduced edge workload exceeds level')
 if max(abs(x) for pt in pts for x in pt)>15:raise ValueError('coordinate subtraction workload bound')
 if not observed and level=='easy':
  if any(sum(x!=0 for x in e)>2 for e in (u,v)) or max(abs(x) for x in w)>5:raise ValueError('easy sparse edges/cross bound')
 if not observed and level=='hard':
  if any(0 in e for e in (u,v)) or max(abs(x) for e in (u,v) for x in e)<6 or not any(x<0 for e in (u,v) for x in e) or sum(x!=0 for x in w)!=3 or max(abs(x) for x in w)>65:raise ValueError('hard six nonzero signed differences, substantive product bound')
 return u,v,w,n,area

def empirical(value,n,n0):
 # Explicit observed expression profile: radial homogeneous scaling, not claimed error intent.
 if r'\sqrt{' in value:
  m=re.search(r'\\sqrt\{(\d+)\}',value);return value[:m.start(1)]+tex(sp.Rational(m[1])*n/n0)+value[m.end(1):]
 return tex(scalar(value)*sp.sqrt(n/n0))

def bank(profile,spec,p):
 u,v,w,n,a=calculation(p)
 if profile.startswith('observed/') or profile.startswith('raw/'):
  sid=profile.split('/')[1];q=SOURCES[sid];n0=calculation({'vertices':vertices(q)})[3]
  values=[empirical(x[':answer/value'],n,n0) for x in q[':question/answer-fields'][0][':answer-field/choices']]
  # Single minimal repair for observed duplicate sqrt17 alternatives.
  if sid=='q-127908' and not profile.startswith('raw/'):values[1]=tex(n/2)
  return values
 # Whole authored profile, selected before evaluating the instance. All positive.
 # Norm, squared norm, dot product used as area, and product of edge magnitudes.
 return [tex(a),tex(sp.sqrt(n)),tex(n/2),tex(abs(sp.Matrix(u).dot(sp.Matrix(v)))/2),tex(sp.sqrt(sp.Matrix(u).dot(sp.Matrix(u))*sp.Matrix(v).dot(sp.Matrix(v)))/2)]

def task_key(p):
 # Incidental common translation and vertex permutation don't inflate task counts.
 # Preserve Cartesian component differences (no rotation or coordinate-axis aliasing).
 pts=p['vertices'];variants=[]
 for ordering in itertools.permutations(pts):
  origin=ordering[0];variants.append(tuple(tuple(b-a for a,b in zip(origin,v)) for v in ordering[1:]))
 return digest(min(variants))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown level')
 rng=random.Random(seed)
 if template is None and profile and '/' in profile:template=profile.split('/')[1]
 template=template or 'authored_'+level+'_'+(field_type or 'radio')
 if template not in TEMPLATES or TEMPLATES[template][0]!=level:raise ValueError('template/level mismatch')
 kind=TEMPLATES[template][1]
 if field_type and kind!=field_type:raise ValueError('field type mismatch')
 observed=template in SPECS
 spec=SPECS[template] if observed else {'labels':'ABC','authored_solution':True,'prompt':r'Calculate the area of the $△\,ABC$, if $A({V0})$, $B({V1})$, $C({V2}).$'+ ('\n\n${A}_{△}=${{field-1}}' if kind=='blank' else '')}
 profile=profile or ('blank' if kind=='blank' else 'authored_operations')
 if kind=='blank' and profile!='blank':raise ValueError('blank fields have no choice-bank profile')
 if profile in ('blank','authored_operations'):
  if (profile=='blank')!=(kind=='blank'):raise ValueError('profile field mismatch')
 elif profile not in ('observed/'+template,'raw/'+template) or not observed:raise ValueError('profile belongs to template')
 explicit=parameters is not None
 for _ in range(10000):
  if explicit:p=json.loads(json.dumps(parameters))
  else:
   bound={'easy':2,'moderate':5,'hard':7}[level];base=[rng.randint(-4,4) for _ in range(3)]
   edges=[[rng.randint(-bound,bound) for _ in range(3)] for j in range(2)]
   p={'vertices':[base]+[[a+b for a,b in zip(base,e)] for e in edges]}
  try:
   u,v,w,n,a=guard(p,level,observed)
   sol,prompt=solution(spec,p)
   vals=[tex(a)] if kind=='blank' else bank(profile,spec,p)
   numeric_values=[scalar_general(x) for x in vals]
   if any(x<=0 for x in numeric_values):raise ValueError('nonpositive area choice')
   if len(set(numeric_values))!=len(vals) and not profile.startswith('raw/'):raise ValueError('complete bank collision')
   matches=[i for i,x in enumerate(numeric_values) if sp.simplify(x-a)==0]
   if len(matches)!=1:raise ValueError('unique correct value required')
   break
  except (ValueError,AssertionError) as exc:
   if explicit:raise ValueError(str(exc)) from exc
 else:raise ValueError('no valid whole-bank instance')
 content={'version':VERSION,'prompt':prompt,'solution':sol,'field':kind,'bank':sorted(vals),'correct':tex(a)}
 qid=ident(content);fid=ident([qid,'field',kind]);answers=[{':answer/id':ident([fid,i,value]),':answer/type':':answer.type/math',':answer/value':value} for i,value in enumerate(vals)]
 correct=answers[matches[0]][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'field-1' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 return {'knowledge_point':{'db_id':KP_ID,'id':RAW[':knowledge-point/id'],'title':RAW[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[field]},'generation':{'version':VERSION,'dependencies':{'sympy':sp.__version__},'template':template,'seed':seed,'parameters':p,'bank_profile':profile,'parameter_fingerprint':task_key(p),'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'authored_level':level!='moderate','observed_template':observed,'plots':'none','raw_bank_anomaly':profile=='raw/q-127908'}}

def scalar_general(s):
 # Restricted exact scalar parser covers parameterized rational radical arguments.
 if s.startswith(r'\frac'):
  def take(at):
   depth=1;j=at+1
   while depth:depth+=(s[j]=='{')-(s[j]=='}');j+=1
   return s[at+1:j-1],j
  numerator,end=take(5);denominator,end=take(end);assert end==len(s)
  return sp.simplify(scalar_general(numerator)/scalar_general(denominator))
 m=re.fullmatch(r'(\d*)\\sqrt\{(.*)\}',s)
 return sp.simplify(sp.Integer(m[1] or 1)*sp.sqrt(scalar_general(m[2]))) if m else sp.Rational(s)
# Easy: authored sparse small integer differences, same full vertex method.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: observed complete determinant/subtraction workload and authored defaults.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: authored signed six-component edges of magnitude at most 7; no new method.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 if args.format=='json':print(json.dumps(records,indent=2,ensure_ascii=False))
 else:
  for r in records:
   print(r['question'][':question/problem']);print('\n'.join(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']));print(r['question'][':question/worked-solution'])
