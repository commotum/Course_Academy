"""Interval injectivity from formulas; frozen math basis 1356, local review only.

Easy: observed nonzero lines (four prose/bank layouts), plus explicitly authored
constant-line contrast. Moderate: all eight observed folded-function layouts.
Hard: authored rational vertex/finite interval bookkeeping, same branch test.
Raw q-66785 replay preserves its absent answer-fields and is ineligible.
No derivatives, inverse calculation, graph-reading prompt, or database writes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix(''); ROOT=Path(__file__).resolve().parents[2]
KP=17592186124474; VERSION='1.0.0'; TITLE='Identifying the Intervals on Which a Function is Invertible Given a Description'
SNAPSHOT=json.loads((HERE/'source.json').read_text()); REC=SNAPSHOT['record']; KP_UUID=REC[':knowledge-point/id']
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
# Complete observed profiles are selected BEFORE the function parameters.
SPECS={
'q-66482':('moderate','quadratic',1,0,2,[[1],[2,3]]),
'q-66723':('easy','linear',1,0,1,[]),
'q-66785':('moderate','absolute',1,4,2,[]),
'q-36010':('moderate','absolute',1,2,1,[[1,3],[2]]),
'q-66483':('easy','linear',-1,0,1,[]),
'q-66669':('moderate','quadratic',1,2,0,[[2],[1,3]]),
'q-66679':('moderate','quadratic',1,1,-2,[[1,2],[3]]),
'q-66687':('moderate','quadratic',-1,0,1,[[1],[2]]),
'q-66725':('easy','linear',-1,0,3,[]),
'q-66729':('moderate','absolute',1,1,-2,[[1,2],[3]]),
'q-66778':('moderate','absolute',1,-1,-3,[[3,2],[1]]),
'q-66724':('easy','linear',2,0,4,[])}
NS=uuid.UUID(KP_UUID)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(NS,v))
def task_fingerprint(level,kind,a,h,ivs):
 # Endpoint relation/closure and finite/unbounded domains are substantive;
 # common translations/scales and vertical changes are incidental.
 return digest([level,'nonzero_line' if a else 'constant']) if kind=='linear' else digest([level,'folded',[[str(sp.sign(lo-h)),str(sp.sign(hi-h)),lo==-sp.oo,hi==sp.oo,l,r] for lo,hi,l,r in ivs]])
def tex(v):return sp.latex(sp.sympify(v)).replace('\\log','\\ln')
def signed(v):return ('+' if v>0 else '-')+tex(abs(v)) if v else ''
def endpoint(s):
 s=s.strip()
 if s==r'-\infty':return -sp.oo
 if s==r'\infty':return sp.oo
 s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
 s=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',s)
 return sp.sympify(s,rational=True)
def parse_interval(s):
 m=re.search(r'([\[(])\s*(.*?)\s*,\s*(.*?)\s*([\])])',s)
 if not m:raise ValueError('Invalid interval '+s)
 return (endpoint(m[2]),endpoint(m[3]),m[1]=='[',m[4]==']')
def interval_tex(iv):
 a,b,l,r=iv;return ('[' if l else '(')+tex(a)+','+tex(b)+(']' if r else ')')
def valid_interval(iv):
 a,b,l,r=iv
 if not a<b or (a==-sp.oo and l) or (b==sp.oo and r):raise ValueError('Invalid interval domain')
def injective(kind,h,iv,a=1):
 valid_interval(iv)
 if kind=='linear':return a!=0
 return iv[1]<=h or iv[0]>=h

def choice_subset(v):
 # Roman labels are conceptual finite subsets; punctuation aliases collide.
 return frozenset(re.findall(r'\bIII\b|\bII\b|\bI\b',v))
def subset_text(indices):
 labels=['I','II','III'];items=[labels[i-1] for i in indices]
 return 'None of these intervals' if not items else ', '.join(items[:-1])+', and '+items[-1] if len(items)==3 else ' and '.join(items)+' only'
def make_field(key,values,correct,content):
 if len(values)!=5 or len({choice_subset(v) for v in values})!=5:raise ValueError('Whole bank has equivalent subsets')
 if sum(choice_subset(v)==correct for v in values)!=1:raise ValueError('Whole bank misses or duplicates correct subset')
 fid=uid(content+':field:'+key);answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/text',':answer/value':v} for v in values]
 cid=next(a[':answer/id'] for a in answers if choice_subset(a[':answer/value'])==correct)
 return {':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}
def equation(kind,a,h,k,style=''):
 if kind=='linear':
  if style=='q-66483':return tex(k)+'-'+('' if a==-1 else tex(abs(a)))+'x'
  return ('' if a==1 else '-' if a==-1 else tex(a))+'x'+signed(k) if a else tex(k)
 inner='x'+signed(-h)
 base='|'+inner+'|' if kind=='absolute' else ('('+inner+')^{2}' if h else '{x}^{2}')
 return ('-' if a==-1 else '')+base+signed(k)
def replace_components(text,mapping):
 # Mask complete components before substitution; never numeric global replace.
 tokens={};counter=0
 for old,new in sorted(mapping.items(),key=lambda x:-len(x[0])):
  if old in text:
   mark='@@COMPONENT'+str(counter)+'@@';counter+=1;tokens[mark]=new;text=text.replace(old,mark)
 for mark,new in tokens.items():text=text.replace(mark,new)
 return text

def render_plots(name,p,kind,ivs,roles,original):
 q=SOURCES[name];paths=re.findall(r'!\[\]\((images/[^)]+)\)',q[':question/worked-solution'])
 if original:return dict(zip(paths,paths)),[]
 key=digest([name,p]);folder=HERE/'plots';folder.mkdir(exist_ok=True)
 outs=[folder/(key+'-'+str(i)+'.png') for i in range(len(paths))]
 if not all(x.exists() and x.with_suffix('.json').exists() for x in outs):
  import tempfile
  data={'kind':kind,'parameters':p,'intervals':[[str(a),str(b),l,r] for a,b,l,r in ivs],'roles':[[]]+roles,'outputs':[str(x) for x in outs]}
  with tempfile.NamedTemporaryFile('w',suffix='.json',dir=folder,delete=False) as f:json.dump(data,f);inp=Path(f.name)
  try:subprocess.run([str(Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')),str(HERE/'render.py'),str(inp)],check=True,capture_output=True,text=True)
  finally:inp.unlink(missing_ok=True)
 return dict(zip(paths,[str(x) for x in outs])),[str(x.with_suffix('.json')) for x in outs]

def observed(name,p,profile,seed):
 q=SOURCES[name];level,kind,a0,h0,k0,roles=SPECS[name]
 expected={'a','h','k','offset'}
 if set(p)!=expected:raise ValueError('Exact parameter keys required: '+str(expected))
 a,h,k,t=[sp.sympify(p[x]) for x in ('a','h','k','offset')]
 if any(x.is_Integer is not True for x in [a,h,k,t]):raise ValueError('Observed-template parameters must be integers')
 if kind=='linear':
  if not 1<=abs(a)<=4 or sp.sign(a)!=sp.sign(a0) or h!=0 or not 1<=k<=6 or not -4<=t<=4:raise ValueError('Easy bounds/sign/layout violated')
 else:
  if a!=a0 or t!=0 or not -6<=h<=6 or not -6<=k<=6:raise ValueError('Moderate bounds/layout violated')
  if (h0==0 and h!=0) or (h0!=0 and (h==0 or sp.sign(h)!=sp.sign(h0))) or (k0==0 and k!=0) or (k0!=0 and (k==0 or sp.sign(k)!=sp.sign(k0))):raise ValueError('Parameters must preserve observed translation steps')
 p={key:int(sp.sympify(p[key])) for key in ('a','h','k','offset')}
 interval_strings=re.findall(r'\$([^$]*\\in[^$]*)\$',q[':question/problem']);old_ivs=[parse_interval(x) for x in interval_strings]
 dh=h-h0 if kind!='linear' else t
 ivs=[(lo+dh if lo!=-sp.oo else lo,hi+dh if hi!=sp.oo else hi,l,r) for lo,hi,l,r in old_ivs]
 original=(a,h,k,t)==(a0,h0,k0,0)
 mapping={}
 # Source expression forms are kept exactly at original parameters via recipes.
 old_eq=re.search(r'f\(x\)=(.*?),\$',q[':question/problem'])[1]
 new_eq=equation(kind,a,h,k,name)
 mapping[old_eq]=new_eq
 if kind!='linear':
  old_inner='x'+signed(-h0);new_inner='x'+signed(-h)
  old_base='|'+old_inner+'|' if kind=='absolute' else ('('+old_inner+')^{2}' if h0 else '{x}^{2}')
  new_base='|'+new_inner+'|' if kind=='absolute' else ('('+new_inner+')^{2}' if h else '{x}^{2}')
  mapping[old_base]=new_base
 for old,iv in zip(interval_strings,ivs):
  # Keep exact source spacing/endpoint spelling at the source parameter values.
  m=re.search(r'([\[(].*[\])])',old)
  replacement=interval_tex(iv)
  if '0.5' in m[0]:replacement=replacement.replace(tex(iv[0]),str(float(iv[0])),1)
  mapping[m[0]]=m[0] if original else replacement
 prompt=replace_components(q[':question/problem'],mapping)
 solution=replace_components(q[':question/worked-solution'],mapping)
 if kind=='linear':
  solution=re.sub(r'slope \$[^$]+\$',lambda _: 'slope $'+tex(a)+'$',solution)
  solution=re.sub(r'intercept \$[^$]+,\$',lambda _: 'intercept $'+tex(k)+',$',solution)
 else:
  def translation_prose(m):
   direction=m[5].split()[-1];value=abs(h) if direction in ('right','left') else abs(k)
   # Original spellings/grammar remain exact in source replay.
   unit=m[3] if value==sp.Integer(m[1]) else ('unit' if value==1 else 'units')
   return 'by $'+str(value)+'$'+m[2]+unit+m[4]+m[5]
  solution=re.sub(r'by \$(\d+)\$( +)(units?)( +)(to +the +right|to +the +left|up|down)',translation_prose,solution)
 assets,sidecars=render_plots(name,p,kind,ivs,roles,original)
 solution=replace_components(solution,assets)
 correct=frozenset(['I','II','III'][i] for i,iv in enumerate(ivs) if injective(kind,h,iv,a))
 fields=q.get(':question/answer-fields')
 if fields:
  bank=[v[':answer/value'] for v in fields[0][':answer-field/choices']]
 else:bank=['I only','II only','III only','I and II only','II and III only']
 if profile=='repaired' and fields is not None:raise ValueError('No repair applies to this source')
 raw_missing=fields is None and profile=='raw'
 content=digest([VERSION,level,prompt,solution,None if raw_missing else bank, None if raw_missing else sorted(correct)])
 result={':question/id':uid(content),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution}
 if not raw_missing:result[':question/answer-fields']=[make_field('selection',bank,correct,content)]
 # Source correctness refs are derivable but missing fields are never silently repaired.
 gen={'version':VERSION,'seed':seed,'template':name,'bank_profile':profile,'parameters':p,'family':kind,'source_id':name,'source_replay':original,'origin':'observed' if fields else 'authored repair' if profile=='repaired' else 'raw source evidence','eligible_for_learning':not raw_missing,'evidence_only':raw_missing,'missing_keys':[':question/answer-fields'] if raw_missing else [],'plot_rating':'moderate' if kind!='linear' else 'light','plot_sidecars':sidecars,'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},'content_fingerprint':content,'parameter_fingerprint':task_fingerprint(level,kind,a,h,ivs)}
 return result,gen

# EASY: source nonzero-line layouts and a source-grounded constant-line contrast.
# MODERATE: source quadratic/absolute-value translations and whole observed banks.
# HARD: all finite intervals, rational vertex comparisons, no additional method.
MODERATE_TYPES={'LI':(-sp.oo,0,False,True),'RI':(0,sp.oo,False,False)}
HARD_TYPES={'L':(-3,-1,True,False),'LO':(-2,0,True,False),'LC':(-2,0,False,True),'R':(1,3,False,True),'RO':(0,2,False,True),'RC':(0,2,True,False),'X':(-1,1,False,True)}

def authored(level,template,p,seed):
 if level=='easy':
  if template!='constant' or set(p)!={'k','offset'} or type(p['k']) is not int or not -6<=p['k']<=6 or type(p['offset']) is not int or not -4<=p['offset']<=4:raise ValueError('Constant-line easy bounds')
  kind='linear';h=0;a=0;k=p['k'];t=p['offset'];ivs=[(-sp.oo,sp.oo,False,False),(t,sp.oo,True,False),(t-2,t+2,False,True)]
  eq=tex(k)
  solution='A function is invertible on a particular interval if and only if it is one-to-one on that interval.\n\nThe function is constant: distinct inputs in each listed interval have the same output $'+tex(k)+'$. Thus it is not one-to-one on any of the three intervals.\n\nTherefore, the correct answer is "None of these intervals".'
 else:
  allowed=('rational_quadratic','rational_absolute') if level=='hard' else ('integer_quadratic','integer_absolute')
  if template not in allowed or set(p)!={'h','k','types'}:raise ValueError('Authored folded template/keys')
  h=sp.Rational(p['h']);k=sp.Rational(p['k']);a=1
  if level=='hard' and (h.q not in (2,3,4) or abs(h)>4 or k.q!=1 or abs(k)>4):raise ValueError('Hard reduced rational-vertex bounds')
  if level=='moderate' and (h.q!=1 or abs(h)>6 or k.q!=1 or abs(k)>6):raise ValueError('Authored moderate integer bounds')
  p={'h':str(h) if level=='hard' else int(h),'k':int(k),'types':list(p['types']) if isinstance(p['types'],list) else p['types']}
  types=p['types']
  catalog=HARD_TYPES if level=='hard' else {**HARD_TYPES,**MODERATE_TYPES}
  if not isinstance(types,list) or len(types)!=3 or len(set(types))!=3 or any(t not in catalog for t in types) or 'X' not in types:raise ValueError('Requires two distinct branch intervals and one crossing interval')
  if level=='moderate' and sum(t in MODERATE_TYPES for t in types)!=1:raise ValueError('Moderate requires exactly one half-infinite interval')
  kind='quadratic' if template.endswith('quadratic') else 'absolute'
  ivs=[(h+sp.sympify(catalog[t][0])/h.q,h+sp.sympify(catalog[t][1])/h.q,catalog[t][2],catalog[t][3]) for t in types]
  ivs=[(sp.sympify(lo),sp.sympify(hi),l,r) for lo,hi,l,r in ivs]
  eq=equation(kind,a,h,k)
  solution='A function is invertible on a particular interval if and only if it is one-to-one on that interval.\n\nThe vertex occurs at $x='+tex(h)+'$. On either side of this vertex, the function is strictly monotone. Including the vertex as an endpoint does not create a repeated output. An interval containing points on both sides is not one-to-one: inputs equally far from the vertex have the same output.\n\n'
  for i,iv in enumerate(ivs):
   good=injective(kind,h,iv)
   if good:
    relation=tex(iv[1])+r'\le '+tex(h) if iv[1]<=h else tex(iv[0])+r'\ge '+tex(h)
    sentence='lies on one side of the vertex, since $'+relation+'$. It is therefore invertible.'
   else:
    d=min(h-iv[0],iv[1]-h)/2;f=(d**2 if kind=='quadratic' else d)+k
    sentence='contains the distinct inputs $'+tex(h-d)+'$ and $'+tex(h+d)+'$, both with output $'+tex(f)+'$. It is therefore not invertible.'
   solution+='- Interval '+['I','II','III'][i]+', $'+interval_tex(iv)+'$, '+sentence+'\n\n'
  correct_indices=[i+1 for i,iv in enumerate(ivs) if injective(kind,h,iv)]
  solution+='Therefore, the correct answer is "'+subset_text(correct_indices)+'".'
 prompt='Given that $f(x)='+eq+',$ on which of the following intervals is $f(x)$ invertible?\n\n'+'\n\n'.join(label+'. $x\\in '+interval_tex(iv)+'$' for label,iv in zip(['I','II','III'],ivs))
 correct=frozenset(['I','II','III'][i] for i,iv in enumerate(ivs) if injective(kind,h,iv,a))
 # Choose a complete error bank: omit either true interval, or replace either
 # true interval with the crossing interval. Three paired choices prevent an
 # answer-length shortcut; no first-valid pool or arbitrary wrong value.
 if level=='easy':
  bank=['None of these intervals','I only','II only','III only','I, II, and III']
 else:
  omitted=next(i for i in (1,2,3) if i not in correct_indices)
  left,right=correct_indices
  bank=[subset_text(correct_indices),subset_text([left]),subset_text([right]),subset_text(sorted([left,omitted])),subset_text(sorted([right,omitted]))]
 content=digest([VERSION,level,prompt,solution,bank,sorted(correct)])
 q={':question/id':uid(content),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[make_field('selection',bank,correct,content)]}
 return q,{'version':VERSION,'seed':seed,'template':template,'bank_profile':'authored','parameters':p,'family':kind,'origin':'authored missing-level extension' if level=='hard' else 'authored same-level extension','eligible_for_learning':True,'evidence_only':False,'missing_keys':[],'plot_rating':'none','plot_sidecars':[],'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},'content_fingerprint':content,'parameter_fingerprint':task_fingerprint(level,kind,a,h,ivs)}

def generate_legacy(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard') or field_type not in (None,'radio'):raise ValueError('Supported difficulty and field type required')
 rng=random.Random(seed)
 eligible=[s for s,v in SPECS.items() if v[0]==level ]
 eligible+=['constant'] if level=='easy' else ['rational_quadratic','rational_absolute'] if level=='hard' else ['integer_quadratic','integer_absolute']
 if template is not None and template not in eligible:raise ValueError('Template not eligible for requested level/profile')
 name=template or rng.choice(eligible)
 if name in SPECS:
  profile=profile or ('repaired' if name=='q-66785' else 'observed')
  if profile not in ('observed','raw','repaired'):raise ValueError('Unknown observed profile')
  if name=='q-66785' and profile not in ('raw','repaired'):raise ValueError('Fieldless source needs explicit raw or repaired profile')
  if parameters is None:
   _,kind,a0,h0,k0,_=SPECS[name]
   parameters={'a':int(sp.sign(a0))*rng.randint(1,4) if kind=='linear' else a0,'h':int(sp.sign(h0))*rng.randint(1,6) if h0 else 0,'k':int(sp.sign(k0))*rng.randint(1,6) if k0 else 0,'offset':rng.randint(-4,4) if kind=='linear' else 0}
  q,g=observed(name,parameters,profile,seed)
 else:
  if profile not in (None,'authored'):raise ValueError('Authored template profile required')
  if parameters is None:
   if level=='easy':parameters={'k':rng.randint(-6,6),'offset':rng.randint(-4,4)}
   elif level=='hard':
    h=rng.choice([sp.Rational(n,d) for d in (2,3,4) for n in range(-4*d,4*d+1) if sp.Rational(n,d).q==d]);types=rng.sample([t for t in HARD_TYPES if t!='X'],2)+['X'];rng.shuffle(types)
    parameters={'h':str(h),'k':rng.randint(-4,4),'types':types}
   else:
    types=[rng.choice(list(MODERATE_TYPES)),rng.choice([t for t in HARD_TYPES if t!='X']),'X'];rng.shuffle(types)
    parameters={'h':rng.randint(-6,6),'k':rng.randint(-6,6),'types':types}
  q,g=authored(level,name,parameters,seed)
 for f in q.get(':question/answer-fields',[]):random.Random(seed).shuffle(f[':answer-field/choices'])
 g.update({'python_version':sys.version.split()[0],'sympy_version':sp.__version__})
 return {'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':q,'generation':g}

# Current database response contract: one checkbox per supplied interval.
CURRENT_SNAPSHOT=json.loads((HERE/'current-source.json').read_text())
CURRENT=CURRENT_SNAPSHOT['record']
CURRENT_SOURCES={q[':question/math-academy-id']:q for q in CURRENT[':knowledge-point/questions']}
CURRENT_VERSION='1.1.0-checkbox'
ROMANS=('I','II','III')
def mathematical_fingerprint(level,kind,a,h,ivs):
 # Unordered topology: interval/Roman permutation, folded formula family,
 # reflection, translation and numeric aliases cannot replenish inventory.
 if kind=='linear':return digest([level,'nonzero_line' if a else 'constant'])
 topology=[[str(sp.sign(lo-h)),str(sp.sign(hi-h)),lo==-sp.oo,hi==sp.oo,l,r] for lo,hi,l,r in ivs]
 return digest([level,'folded',sorted(topology,key=lambda z:json.dumps(z))])
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in (None,'checkbox'):raise ValueError('Current field type is checkbox')
 if profile and profile.startswith('current:'):
  import copy
  q=copy.deepcopy(CURRENT_SOURCES[profile.split(':',1)[1]])
  if q[':question/difficulty'][':db/ident']!=':question.difficulty/'+level:raise ValueError('Source level mismatch')
  return {'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':CURRENT_VERSION,'seed':seed,'template':profile,'bank_profile':'current boolean bank','source_replay':True,'evidence_only':True,'eligible_for_learning':False}}
 r=generate_legacy(level,seed,template,None,parameters,profile)
 q,meta=r['question'],r['generation']
 if not meta['eligible_for_learning']:return r
 selected=next(a for a in q[':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==q[':question/answer-fields'][0][':answer-field/correct'][1])
 correct=choice_subset(selected[':answer/value'])
 supplied=re.findall(r'\$([^$]*\\in[^$]*)\$',q[':question/problem'])
 assert len(supplied)==3
 prompt=q[':question/problem'].splitlines()[0]+'\n\nSelect all that apply.\n\n'+('\n\n' if meta['template'] in CURRENT_SOURCES and '\n\n- **II.**' in CURRENT_SOURCES[meta['template']][':question/problem'] else '\n').join('- **'+label+'.** $'+text+'$' for label,text in zip(ROMANS,supplied))
 content=digest([CURRENT_VERSION,level,prompt,q[':question/worked-solution'],sorted(correct)])
 q[':question/id']=uid(content);q[':question/problem']=prompt;fields=[]
 for label in ROMANS:
  fid=uid(content+':checkbox:'+label)
  answers=[{':answer/id':uid(fid+':'+value),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
  desired='true' if label in correct else 'false'
  fields.append({':answer-field/id':fid,':answer-field/key':label,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==desired)]})
 q[':question/answer-fields']=fields
 ivs=[parse_interval(t) for t in supplied]
 pars=meta['parameters'];kind=meta['family'];a=pars.get('a',0 if kind=='linear' else 1);h=sp.sympify(pars.get('h',0))
 meta.update({'version':CURRENT_VERSION,'legacy_sampling_profile':meta['bank_profile'],'bank_profile':'field-owned boolean','mathematical_fingerprint':mathematical_fingerprint(level,kind,a,h,ivs),'current_source_basis':CURRENT_SNAPSHOT['basis'],'current_source_lineage':CURRENT_SNAPSHOT['lineage'],'assets':{str(i):path for i,path in enumerate(re.findall(r'!\[\]\((/[^)]+)\)',q[':question/worked-solution']))}})
 return r

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Easy: four observed nonzero-line layouts or authored constant contrast."""
 return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Moderate: eight source masks/repair, or 72 integer-domain catalogs."""
 return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Hard authored: reduced rational vertex, finite intervals, 90 catalogs."""
 return generate('hard',seed,template,field_type,parameters,profile)
def markdown(record):
 q=record['question'];g=record['generation'];label='Original source replay' if g.get('source_replay') else 'Generated variant';lines=[f"## {label} — {g['origin']} — {q.get(':question/difficulty','unrated').split('/')[-1]}",f"Template `{g['template']}`; bank `{g['bank_profile']}`; eligible: {g['eligible_for_learning']}.",'',q[':question/problem'],'']
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:lines.append('- '+a[':answer/value']+(' **(correct)**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
 if ':question/answer-fields' not in q:lines+=['**Raw evidence: answer-fields absent. Inferred answer: I only.**']
 lines+=['','**Worked solution**','',q.get(':question/worked-solution','Absent')]
 return '\n'.join(lines).replace('![](images/','![](/media/jake/SSD/EDB/math/images/')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
 if a.count<1 or a.difficulty=='all' and (a.template or a.profile):p.error('Positive count and specific difficulty required with template/profile')
 rs=[generate(l,a.seed+i,a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_legacy', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
