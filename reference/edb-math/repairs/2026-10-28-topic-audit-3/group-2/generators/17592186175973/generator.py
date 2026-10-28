#!/usr/bin/env python3
"""Seeded, relocatable hyperbolic-cylinder generator. No writes or publication.
Raw profiles preserve original incomplete captures for evidence only.
Normal profiles preserve complete source banks with documented capture repairs.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, random, re, sys, uuid
import sympy as sp
from math_format import normalize_prose,normalize_tex,checked_math_content
DIR=pathlib.Path(__file__).resolve().parent
CAPTURE=json.loads((DIR/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
SOURCES['e-8889']=CAPTURE['record'][':knowledge-point/canonical-example']
KP_ID=17592186175973
TITLE='Parametrizing a Hyperbolic Cylinder'
VERSION='hyperbolic-cylinder-3'
T=sp.Symbol('t',real=True)
AXES='xyz';ORD=['first','second','third']
# a is the sec scale, b2 is the squared tan scale. Coordinate letters are roles.
SPECS={
 'equal_tan':dict(source='q-103998',level='moderate',a=3,b2=9,sec='x',tan='y',target='y',numbers={'3':'a','9':'a2'}),
 'radical_tan':dict(source='q-164439',level='moderate',a=3,b2=2,sec='x',tan='y',target='y',numbers={'3':'a','2':'b2','9':'a2','18':'product'}),
 'unrated_tan':dict(source='q-164387',level='moderate',a=2,b2=3,sec='z',tan='y',target='y',numbers={'2':'a','3':'b2','4':'a2','12':'product'}),
 'equal_sec':dict(source='q-164457',level='hard',a=7,b2=49,sec='y',tan='z',target='y',numbers={'7':'a','49':'a2'}),
 'unit_sec':dict(source='q-164519',level='hard',a=1,b2=16,sec='x',tan='z',target='x',numbers={'4':'b','16':'b2','5':'sum'}),
 'offplane_tan':dict(source='q-164521',level='hard',a=2,b2=4,sec='z',tan='x',target='x',numbers={'2':'a','4':'a2'}),
 'unequal_sec':dict(source='e-8889',level='moderate',a=2,b2=16,sec='z',tan='x',target='z',numbers={'2':'a','4':'a2','16':'b2'}),
}
PROFILES={**{'raw_'+s['source']:name for name,s in SPECS.items()},
 **{'normal_'+name:name for name in SPECS}}


def tex(x):return sp.latex(sp.sympify(x))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def normalize(s,prose=False):
 # Decoded answer captures really contain doubled backslashes; solution row
 # separators are distinct and are never subjected to this answer-only repair.
 if not prose:s=s.replace('\\\\','\\')
 s=re.sub(r'\\operatorname\{(sec|tan|sin|cos|csc)\}',r'\\\1 ',s)
 s=s.replace(r'\u2061',' ').replace('\u2061',' ')
 s=re.sub(r'\{(sec|tan|sin|cos|csc)\}',r'\\\1',s)
 return normalize_prose(s) if prose else normalize_tex(s)


def slots(text,s,p):
 """Mask complete intervals and exponent nodes BEFORE coefficient replacement.

 Replacing source integer tokens applies only to arithmetic coefficients. Powers
 and the parameter interval are fixed backbone; a radical's full node is masked
 before its radicand to retain source square-root workload and notation.
 """
 stash=[]
 def protect(m):stash.append(m.group());return f'@@PROTECT{chr(65+len(stash)-1)}@@'
 text=re.sub(r'\^\{2\}|\^2|\\frac\{(?:\\pi\s*|π)\}\{2\}',protect,text)
 a,b2=p['a'],p['b2'];b=sp.sqrt(b2)
 vals={'a':tex(a),'a2':tex(a*a),'b':tex(b),'b2':tex(b2),'product':tex(a*a*b2),'sum':tex(a+b)}
 text=re.sub(r'(?<!\d)\d+(?!\d)',lambda m:vals[s['numbers'][m.group()]] if m.group() in s['numbers'] else m.group(),text)
 for i,v in enumerate(stash):text=text.replace(f'@@PROTECT{chr(65+i)}@@',v)
 return text


def permute(text,s,p):
 """Reorder complete Cartesian vector components, preserving f's argument order."""
 mapping=dict(zip(AXES,p['axes']))
 oldtarget=s['target'];newtarget=mapping[oldtarget]
 def tuple_change(m):
  parts=m.group(1).replace(r'\,','').split(',')
  oldroles=list(AXES) if len(parts)==3 else sorted([s['sec'],s['tan']])
  if len(parts)!=len(oldroles):raise ValueError('Unsupported coordinate tuple')
  rows=sorted(zip(oldroles,parts),key=lambda row:AXES.index(mapping[row[0]]))
  return '⟨'+',\\,'.join(swap(part) for _,part in rows)+'⟩'
 def swap(part):
  part=re.sub(r'(?<![A-Za-z\\])[xyz](?![A-Za-z])',lambda m:mapping[m.group()],part)
  return re.sub(r'\b(?:xy|xz|yz)\b',lambda m:''.join(sorted(mapping[c] for c in m.group())),part)
 if p['axes']=='xyz':return text
 tuples=[]
 def mask(m):tuples.append(tuple_change(m));return '@@TUPLE'+str(len(tuples)-1)+'@@'
 text=re.sub(r'⟨([^⟨⟩]+)⟩',mask,text)
 text=swap(text)
 # Points in prose always have the conventional Cartesian order.
 text=re.sub(r'\$\([xyz],[xyz],[xyz]\)\$', '$(x,y,z)$',text)
 text=text.replace(ORD[AXES.index(oldtarget)]+' component',ORD[AXES.index(newtarget)]+' component')
 for i,v in enumerate(tuples):text=text.replace('@@TUPLE'+str(i)+'@@',v)
 return text


def canonical_slots(text,s,p):
 """Keep canonical prose/steps; distinguish its coincident 4=b=a² tokens."""
 text=text.replace(r'\dfrac\pi2',r'\frac{\pi}{2}').replace(r'\dfrac',r'\frac')
 text=re.sub(r'4(?=\\(?:tan|operatorname\{tan\}))','@@TANSCALE@@',text)
 text=slots(text,s,p).replace('@@TANSCALE@@',tex(sp.sqrt(p['b2'])))
 # Normalize vector delimiters before the existing coordinate permutation.
 text=re.sub(r'\\big\s*','',text).replace(r'\langle','⟨').replace(r'\rangle','⟩')
 text=text.replace(r'\mathbf{f}','f').replace(r'\geq',r'\ge')
 text=re.sub(r'\{\\color\{blue\}([^{}]*(?:\{t\})?)\}',r'\1',text)
 return text


def validate_parameters(name,p,raw=False):
 if set(p)!={'a','b2','axes'}:raise ValueError('Use a, b2, axes parameters')
 if type(p['a']) is not int or type(p['b2']) is not int:raise ValueError('Exact integer scale/radicand required')
 if p['axes'] not in ['xyz','xzy','yxz','yzx','zxy','zyx']:raise ValueError('axes must permute xyz')
 a,b2=p['a'],p['b2']
 if not 1<=a<=9 or not 1<=b2<=81:raise ValueError('Arithmetic workload bound')
 if name in ['equal_tan','equal_sec','offplane_tan'] and b2!=a*a:raise ValueError('This family has equal scales')
 if name=='unit_sec' and (a!=1 or b2 not in [4,9,16,25,36,49,64,81]):raise ValueError('Unit sec/nonunit integral tan scale')
 if name in ['radical_tan','unrated_tan'] and (a<2 or b2 not in [2,3,5,6,7]):raise ValueError('Familiar non-square radicands')
 if name=='offplane_tan' and a<2:raise ValueError('Unit scale collides in the observed bank')
 if name=='unequal_sec' and (b2 not in [b*b for b in range(1,10)] or b2==a*a):raise ValueError('Independent unequal integer scales 1..9')
 if raw and name=='unequal_sec' and (a,b2)!=(2,16):raise ValueError('Raw canonical replay uses original scales')
 if raw and p['axes']!='xyz':raise ValueError('Raw source replay preserves source coordinates')


def sample(name,rng):
 a=rng.randint(1 if name in ['equal_tan','equal_sec'] else 2,9);b2=a*a
 if name in ['radical_tan','unrated_tan']:b2=rng.choice([2,3,5,6,7])
 if name=='unit_sec':a=1;b2=rng.choice([4,9,16,25,36,49,64,81])
 if name=='unequal_sec':
  a=rng.randint(1,9);b2=rng.choice([b*b for b in range(1,10) if b!=a])
 return dict(a=a,b2=b2,axes=rng.choice(['xyz','xzy','yxz','yzx','zxy','zyx']))


def normal_bank(name,p):
 a=sp.Integer(p['a']);b2=sp.Integer(p['b2']);b=sp.sqrt(b2)
 # Preserve each complete observed bank, including domain-error distractors.
 if name=='unit_sec':return [(a+b)*sp.sec(T),sp.sec(T),(a+b)*sp.cos(T),sp.cos(T),T*T]
 if name=='offplane_tan':return [a*sp.tan(T),a*sp.cos(T),a*T*T,sp.tan(T),sp.cos(T)]
 if name=='equal_sec':return [a*sp.csc(T),a*sp.sec(T),a*sp.sin(T),a*T,a*sp.cos(T)]
 if name=='unequal_sec':return [a*sp.csc(T),a*sp.sec(T),a*sp.sin(T),a*T,a*sp.cos(T)]
 if name=='equal_tan':return [a*sp.csc(T),a*T*T,sp.sin(T),a*sp.cos(T),a*sp.tan(T)]
 if name=='radical_tan':return [b2*sp.tan(T),b*sp.csc(T),b*sp.tan(T),b*sp.cos(T),b2*sp.cos(T)]
 if name=='unrated_tan':return [b2*sp.tan(T),b*sp.cos(T),b2*sp.csc(T),b*sp.csc(T),b*sp.tan(T)]
 raise ValueError('Unknown bank')


def authored_unrated_solution(s,p):
 # Authored completion mirrors the canonical normalized substitution chain.
 a,b2=p['a'],p['b2'];b=tex(sp.sqrt(b2))
 eq=r'\frac{z^2}{'+str(a*a)+r'}-\frac{y^2}{'+str(b2)+'}=1'
 pair='⟨y,z⟩=⟨'+b+r'\tan t,\,'+str(a)+r'\sec t⟩'
 sol='Recall that the hyperbola $'+eq+'$ for $z\\ge '+str(a)+'$ in $yz$-plane has the parametrization\n\n$$\n'+pair+r',\quad t\in(-\frac{\pi}{2},\frac{\pi}{2})'+'\n$$\n\nsince \n\n$$\n'+r'\begin{aligned}'+eq.split('=')[0]+r'&=\frac{('+str(a)+r'\sec t)^2}{'+str(a*a)+r'}-\frac{('+b+r'\tan t)^2}{'+str(b2)+r'}\\&=\frac{'+str(a*a)+r'\sec^2 t}{'+str(a*a)+r'}-\frac{'+str(b2)+r'\tan^2 t}{'+str(b2)+r'}\\&=\sec^2 t-\tan^2 t\\&=1.\end{aligned}'+'\n$$\n\nNow, for any point $(x,y,z)$ on our surface, we obtain the following:\n\n$$\n'+r'\begin{aligned}f(x,t)&=⟨x,y,z⟩\\&=⟨x,\,'+b+r'\tan t,\,'+str(a)+r'\sec t⟩\end{aligned}'+'\n$$\n\nwhere $t\\in(-\\frac{\\pi}{2},\\frac{\\pi}{2})$ and $x\\in(-\\infty,\\infty).$\n\nTherefore, the second component of $f$ is $'+b+r'\tan t.$'
 return sol


@checked_math_content
def _checked(record):return record


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if not (profile and profile.startswith('raw_')):
  from authored import generate_component
  return generate_component(level,seed,template,field_type,parameters,profile)
 if level not in ['moderate','hard']:raise ValueError('Raw replay has only moderate/hard captures')
 if field_type not in [None,'radio']:raise ValueError('Observed field contract is radio')
 if profile:
  if profile not in PROFILES:raise ValueError('Unknown profile')
  if template and template!=PROFILES[profile]:raise ValueError('Profile/template mismatch')
  template=PROFILES[profile]
 eligible=[k for k,s in SPECS.items() if s['level']==level]
 rng=random.Random(seed);name=template or rng.choice(eligible)
 if name not in eligible:raise ValueError('Unsupported level/template combination')
 s=SPECS[name];raw=bool(profile and profile.startswith('raw_'));profile=profile or 'normal_'+name
 p=dict(parameters) if parameters is not None else ({'a':s['a'],'b2':s['b2'],'axes':'xyz'} if raw else sample(name,rng))
 p.setdefault('axes','xyz')
 if raw and parameters is None:p['axes']='xyz'
 validate_parameters(name,p,raw)
 src=SOURCES[s['source']]
 render_slots=(lambda text,s,p:text) if raw and name=='unequal_sec' else canonical_slots if name=='unequal_sec' else slots
 problem=render_slots(src[':question/problem'],s,p)
 sol=render_slots(src.get(':question/worked-solution',''),s,p)
 if raw:
  fielddata=[]
  for f in src.get(':question/answer-fields',[]):
   vals=[slots(a[':answer/value'],s,p) for a in f[':answer-field/choices']]
   ci=next((i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')),None)
   fielddata.append((f[':answer-field/key'],vals,ci))
 else:
  if name=='unrated_tan':
   problem=problem.replace('_____',r'\text{_____}')
   first,rest=problem.split('\n\n',1)
   problem='$$\n'+first.strip('$')+'\n$$\n\n'+rest
  problem=normalize(permute(problem,s,p),True)
  sol=normalize(permute(sol or authored_unrated_solution(s,p),s,p),True)
  vals=normal_bank(name,p)
  correct=sp.Integer(p['a'])*sp.sec(T) if s['target']==s['sec'] else sp.sqrt(p['b2'])*sp.tan(T)
  ci=next(i for i,v in enumerate(vals) if sp.simplify(v-correct)==0)
  fielddata=[('selection',[normalize(tex(v)) for v in vals],ci)]
 q={':question/problem':problem}
 if raw:
  for attr in [':db/id',':question/math-academy-id']:
   if attr in src:q[attr]=src[attr]
 if ':question/worked-solution' in src or not raw:q[':question/worked-solution']=sol
 if ':question/difficulty' in src or not raw:q[':question/difficulty']=':question.difficulty/'+level
 fields=[]
 for idx,(key,vals,ci) in enumerate(fielddata):
  fields.append({':answer-field/key':key,':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':v} for v in vals],**({':answer-field/correct-index':ci} if ci is not None else {})})
 if raw:
  for f,of in zip(fields,src.get(':question/answer-fields',[]),strict=True):
   if ':db/id' in of:f[':db/id']=of[':db/id']
   for a,oa in zip(f[':answer-field/choices'],of[':answer-field/choices'],strict=True):
    if ':db/id' in oa:a[':db/id']=oa[':db/id']
 content=digest([VERSION,level if ':question/difficulty' in q else None,q,fielddata])
 q[':question/id']=uid(content)
 for idx,f in enumerate(fields):
  f[':answer-field/id']=uid(content+'/field/'+str(idx))
  for a in f[':answer-field/choices']:a[':answer/id']=uid(f[':answer-field/id']+'/'+a[':answer/value'])
  ci=f.pop(':answer-field/correct-index',None)
  if ci is not None:f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][ci][':answer/id']]
  random.Random(seed+idx).shuffle(f[':answer-field/choices'])
 if not raw or ':question/answer-fields' in src:q[':question/answer-fields']=fields
 roles=dict(zip(AXES,p['axes']))
 task=digest({'sec_axis':roles[s['sec']],'tan_axis':roles[s['tan']],'target':roles[s['target']],'a':p['a'] if s['target']==s['sec'] else None,'b2':p['b2'] if s['target']==s['tan'] else None,'information':'recover-base','equation_form':'weighted' if name in ['radical_tan','unrated_tan'] else 'simple'})
 rec={'knowledge_point':{'db_id':KP_ID,'id':CAPTURE['record'][':knowledge-point/id'],'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'parameter_fingerprint':task,'content_fingerprint':content,'source_analysis':{k:CAPTURE[k] for k in ['database','basis','lineage']},'source_ids':[s['source']],'evidence_only':raw,'eligible_for_learning':not raw,'authored_extension':not raw and (name=='unrated_tan' or p['a']!=s['a'] or p['b2']!=s['b2'] or p['axes']!='xyz'),'bank_origin':'raw observed' if raw else ('complete observed bank; inferred a+b scale recipe' if name=='unit_sec' else 'observed valid-domain' if name=='offplane_tan' else 'complete observed bank with parameterized recipes'),'source_difficulty':src.get(':question/difficulty',{}).get(':db/ident'),'difficulty_policy':'observed label' if name!='unrated_tan' else 'authored uncertain policy','plot_rating':'none','plot_assets':{},'domain':'-pi/2<t<pi/2; free coordinate real','roles':{'sec':roles[s['sec']],'tan':roles[s['tan']],'target':roles[s['target']]}}}
 if name=='unequal_sec':
  rec['generation'].update(bank_origin='absent in source' if raw else 'authored adaptation of q-164457 complete function-confusion bank',authored_extension=not raw,difficulty_policy='source label absent; authored moderate classification')
 return rec if raw else _checked(rec)


# MODERATE — observed tan recovery, familiar exact radical/normalization workload.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — observed sec recovery or off-plane requested tan coordinate; no new math.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)


def markdown(rec):
 q=rec['question'];lines=[q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  lines.append('Field '+f[':answer-field/key'])
  for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$'+(' (key)' if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1] else ''))
 lines+=['',q.get(':question/worked-solution','Worked solution absent in raw source.'),'']
 return '\n'.join(lines)


def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='moderate');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='json');parser.add_argument('--template');parser.add_argument('--profile');parser.add_argument('--parameters',type=json.loads,help='Exact a, b2, axes JSON object for replay')
 args=parser.parse_args()
 if args.count<1:parser.error('Positive count required')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[]
 for level in levels:
  group=[generate(level,args.seed+i,args.template,parameters=args.parameters,profile=args.profile) for i in range(args.count)]
  if not (args.profile and args.profile.startswith('raw_')):
   # Batch-level position permutation prevents repeated keyed positions even
   # when a short batch crosses a single-record sampler block boundary.
   positions=list(range(6));random.Random(args.seed^0x7af319).shuffle(positions)
   for i,rec in enumerate(group):
    f=rec['question'][':question/answer-fields'][0];bank=f[':answer-field/choices']
    current=next(k for k,v in enumerate(bank) if v[':answer/id']==f[':answer-field/correct'][1])
    target=positions[i%6];bank[current],bank[target]=bank[target],bank[current]
  records.extend(group)
 print(json.dumps(_apply_source_notation(records),indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

from source_notation import install as _install_source_notation, apply as _apply_source_notation
_install_source_notation(globals())

if __name__=='__main__':main()
