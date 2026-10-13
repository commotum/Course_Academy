#!/usr/bin/env python3
"""Projecting onto a perpendicular vector, math basis 1356; scratch only.

Observed moderate: one unknown coordinate -> three dot-product contributions ->
linear equation. Twenty-two extracted masks retain layouts and every teaching row.
Opaque historical radio banks are public evidence profiles, never normal sampling.
Easy is authored recognition (two finite supplied-information forms); hard is an
authored same-method two-linear-contribution instance, never a quadratic problem.
No database access or writes. See the adjacent extraction and validation evidence.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186105918
KP_UUID='a51e317c-f6b3-5704-afb4-bdfc79f1176f'
TITLE='Projecting a Vector Onto a Perpendicular Vector'
VERSION='perpendicular-projection-v1'
DIR=Path(__file__).with_suffix('')
RECIPES={r['template']:r for r in json.loads((DIR/'recipes.json').read_text())}
X=sp.Symbol('x')
TEMPLATES={**{k:{'level':'moderate','type':r['field_type']} for k,r in RECIPES.items()},'perpendicular':{'level':'easy','type':'blank'},'right-angle':{'level':'easy','type':'blank'},'two-linear-terms':{'level':'hard','type':'blank'},'two-linear-terms-radio':{'level':'hard','type':'radio'}}
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}

def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(obj):return hashlib.sha256(canonical(obj).encode()).hexdigest()
def uid(*parts):return str(uuid.uuid5(uuid.UUID(KP_UUID),canonical(parts)))
def exact(v):
 e=sp.sympify(v,locals={'x':X})
 if not isinstance(e,sp.Expr) or e.free_symbols-{X}:raise ValueError('Unknown parameter symbols or non-expression')
 return e

def tex(e):
 e=exact(e)
 return sp.latex(e).replace(' ','')
def term(c):
 c=exact(c)
 return 'x' if c==1 else '-x' if c==-1 else tex(c)+'x'
def joined(parts):
 out=''
 for p in parts:
  if not p:continue
  out+=('+' if out and not p.startswith('-') else '')+p
 return out or '0'
def linear(A,B,const_first=False):
 parts=([tex(B) if B else '',term(A) if A else ''] if const_first else [term(A) if A else '',tex(B) if B else ''])
 return joined(parts)
def grouped(e):
 t=tex(e)
 return '('+t+')' if exact(e).is_negative else t

def vector(v,layout):
 if layout=='angle':return '⟨'+','.join(tex(c) for c in v)+'⟩'
 if layout=='column':return r'[\begin{aligned}'+' \\\\ '.join(tex(c) for c in v)+r'\end{aligned}]'
 if layout!='basis':raise ValueError('Unknown layout')
 terms=[]
 for c,b in zip(v,'ijk'):
  if c==0:continue
  terms.append((('' if c==1 else '-' if c==-1 else tex(c))+b))
 return joined(terms)

def dot_data(p,q):
 products=[sp.expand(a*b) for a,b in zip(p,q)]
 dot=sp.expand(sum(products));A=dot.coeff(X);B=dot.subs(X,0)
 if A==0 or sp.degree(dot,X)!=1:raise ValueError('Need one nondegenerate linear equation')
 r=sp.cancel(-B/A)
 if any(sum(c.subs(X,r)**2 for c in v)==0 for v in (p,q)):raise ValueError('Projection requires nonzero vectors')
 return products,A,B,r

def substitution(p,q,evaluated=False):
 if evaluated:
  return joined([linear(sp.expand(a*b).coeff(X),sp.expand(a*b).subs(X,0)) for a,b in zip(p,q)])
 return '+'.join(grouped(a)+r'\cdot '+grouped(b) for a,b in zip(p,q))

def formal(n1,n2,multiplication=True):
 return n1+r'\cdot '+n2+' & ='+ '+'.join('{'+n1+'}_{'+c+'}'+(r'\cdot ' if multiplication else '')+'{'+n2+'}_{'+c+'}' for c in 'xyz')

def solution_blocks(p,q,names,cfg,raw=False):
 products,A,B,r=dot_data(p,q);n1,n2=names
 dotblock=cfg.get('formal_row',formal(n1,n2))+' \\\\  & ='+substitution(p,q,cfg.get('evaluated_products',False))+' \\\\  & ='+linear(A,B,cfg.get('constant_first',False))+'.'
 if not raw and cfg.get('solution_alias_error'):
  dotblock=dotblock.replace('{p}','{a}').replace('{q}','{b}').replace(r'p\cdot q',r'a\cdot b')
 rows=[]
 if cfg.get('has_dot',True):rows.append((('p'+r'\cdot q') if raw and cfg.get('solution_alias_error') else n1+r'\cdot '+n2)+' & =0')
 rows.append(linear(A,B,cfg.get('constant_first',False))+' & =0')
 intermediate=cfg.get('intermediate',abs(A)!=1 and B!=0)
 if intermediate:
  c=abs(A);rhs=-B if A>0 else B
  rows.append(term(c)+' & ='+tex(rhs))
 rows.append('x & ='+tex(r)+'.')
 return dotblock,' \\\\ '.join(rows)

def method_profile(p,q):
 products,A,B,r=dot_data(p,q)
 known=[(a,b) for a,b in zip(p,q) if not (a*b).has(X) and a*b!=0]
 return 'method:'+('two-products' if len(known)==2 else 'one-product')+('-unit' if abs(A)==1 else '')

def bank(p,q,profile,cfg):
 products,A,B,r=dot_data(p,q)
 if profile.startswith('observed:'):
  if cfg['field_type']=='blank':return [r],['correct']
  # Scalar historical options do not determine author intent. Preserve their
  # complete proportional pattern as an explicitly opaque evidence profile.
  vals=[r*exact(t) for t in cfg['historical_ratios']]
  return vals,['historical-ratio:'+t for t in cfg['historical_ratios']]
 if profile=='blank':return [r],['correct']
 known=[(a,b) for a,b in zip(p,q) if not (a*b).has(X) and a*b!=0]
 if profile=='method:hard':
  coeff=[t.coeff(X) for t in products if t.has(X)]
  vals=[r,-r,-B/coeff[0],-B/coeff[1],-B]
  labels=['correct','wrong-sign','omit-second-linear-contribution','omit-first-linear-contribution','omit-division']
 elif profile=='method:two-products':
  t1,t2=[a*b for a,b in known];vals=[r,-r,-t1/A,-t2/A,-B]
  labels=['correct','wrong-sign','omit-second-known-product','omit-first-known-product','omit-division']
 elif profile=='method:two-products-unit':
  t1,t2=[a*b for a,b in known];vals=[r,-r,-t1/A,-t2/A,(t1-t2)/A]
  labels=['correct','wrong-sign','omit-second-known-product','omit-first-known-product','reverse-first-product-sign']
 elif profile=='method:one-product':
  a,b=known[0];vals=[r,-r,-B,a,b];labels=['correct','wrong-sign','omit-division','use-first-known-component','use-second-known-component']
 elif profile=='method:one-product-unit':
  a,b=known[0];vals=[r,-r,a,b,-(a+b)/A];labels=['correct','wrong-sign','use-first-known-component','use-second-known-component','add-known-components-instead-of-multiply']
 else:raise ValueError('Unknown profile')
 if profile!='blank' and not profile.startswith('observed:') and profile!=(method_profile(p,q) if profile!='method:hard' else 'method:hard'):raise ValueError('Ineligible complete bank')
 return list(map(sp.cancel,vals)),labels

def check_bank(vals,answer):
 if len(set(map(str,map(sp.simplify,vals))))!=len(vals):raise ValueError('Whole bank rejected: equivalent options')
 if sum(sp.simplify(v-answer)==0 for v in vals)!=1:raise ValueError('Whole bank rejected: correct count')

def moderate_parameters(cfg,rng,profile):
 orig=[[exact(c) for c in cfg['parameters'][k]] for k in ('p','q')]
 # The coefficient-one and zero-constant source row structures remain invariant.
 for _ in range(2000):
  p,q=[[c if c==X or c==0 or c.has(sp.sqrt(2)) or c.has(sp.sqrt(3)) else sp.Integer(rng.choice([i for i in range(-6,7) if i])) for c in v] for v in orig]
  oi=next((i,j) for i,v in enumerate(orig) for j,c in enumerate(v) if c==X)
  oldA=dot_data(*orig)[1]
  (q if oi[0]==0 else p)[oi[1]]=sp.Integer((1 if rng.randrange(2) else -1) if abs(oldA)==1 else rng.choice([-6,-5,-4,-3,-2,2,3,4,5,6]))
  if dot_data(*orig)[2]==0:
   # Source cancellation family has two unit known q coordinates. Solve its
   # second known p entry to preserve the zero-constant teaching structure.
   indices=[j for j in range(3) if not (p[j]*q[j]).has(X) and p[j]*q[j]!=0]
   i,j=indices;q[i]=q[j]=sp.Integer(1);p[j]=-p[i]
  try:
   products,A,B,r=validate_parameters('moderate',p,q,cfg,bool(profile and profile.startswith('observed:')))
   chosen=profile or ('blank' if cfg['field_type']=='blank' else method_profile(*orig))
   vals,_=bank(p,q,chosen,cfg);check_bank(vals,r)
   return {'p':list(map(str,p)),'q':list(map(str,q))}
  except ValueError:pass
 raise ValueError('No eligible whole instance')

def validate_parameters(level,p,q,cfg,observed):
 if len(p)!=3 or len(q)!=3:raise ValueError('Three coordinates required')
 unknown=[(i,j) for i,v in enumerate((p,q)) for j,c in enumerate(v) if c.has(X)]
 if any(c not in (X,) and c.has(X) for v in (p,q) for c in v):raise ValueError('Unknown entries must be x alone')
 products,A,B,r=dot_data(p,q)
 bound=15 if observed else 6
 for v in (p,q):
  for c in v:
   if c==X:continue
   if not (c.is_Integer or level=='moderate' and c in [sp.sqrt(2),sp.sqrt(3)]) or abs(c)>bound:raise ValueError('Coordinate number form or magnitude outside scope')
 if level=='moderate':
  orig=[[exact(c) for c in cfg['parameters'][k]] for k in ('p','q')]
  old_unknown=[(i,j) for i,v in enumerate(orig) for j,c in enumerate(v) if c==X]
  if unknown!=old_unknown:raise ValueError('Source family unknown coordinate changed')
  for vi,(v,ov) in enumerate(zip((p,q),orig)):
   for j,(c,oc) in enumerate(zip(v,ov)):
    if c!=X and not c.is_Integer and (oc.is_Integer or (q if vi==0 else p)[j]!=0):raise ValueError('Radical entries only in original zero-product slots')
    if oc==0 and c!=0 or oc!=0 and oc!=X and c==0:raise ValueError('Source zero/nonzero coordinate structure changed')
  oldA,oldB=dot_data(*orig)[1:3]
  if (abs(oldA)==1)!=(abs(A)==1) or (oldB==0)!=(B==0):raise ValueError('Source teaching row workload changed')
 elif level=='hard':
  if unknown!=[(0,0),(1,1)] or any(c==0 for v in (p,q) for c in v):raise ValueError('Hard requires two distinct nonzero linear contributions')
  coeff=[t.coeff(X) for t in products if t.has(X)]
  if len(coeff)!=2 or any(c==0 for c in coeff) or abs(A)<2 or abs(A)>12 or coeff[0]==coeff[1]:raise ValueError('Hard collection demand outside bounds')
 return products,A,B,r

def build_record(level,seed,template,profile,params,prompt,solution,vals,labels,key,kind,raw=False,source_id=None,task=None):
 ordered=sorted([tex(v) for v in vals])
 content={'version':VERSION,'difficulty':level,'prompt':prompt,'solution':solution,'bank':ordered,'kind':kind,'key':key}
 h=digest(content);qid=uid('question',h);fid=uid('field',h,key)
 answers=[{':answer/id':uid('answer',fid,tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in vals]
 correct_value=tex(vals[0]);correct_id=next(a[':answer/id'] for a in answers if a[':answer/value']==correct_value)
 random.Random(str(seed)+':option-order').shuffle(answers)
 q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':params,'source':SOURCE,'source_ids':[source_id] if source_id else [],'source_replay':bool(raw and source_id and params==RECIPES[template]['parameters']),'authored_level':level!='moderate','evidence_only':raw and kind=='radio' or raw and source_id==17592186292830,'eligible_for_learning':not(raw and kind=='radio' or raw and source_id==17592186292830),'recipe_labels':labels,'content_hash':h,'mathematical_fingerprint':digest(task),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none','domains':{'nonzero_vectors':True,'coordinates_max_abs':15 if raw else 6}}}

# EASY: authored finite recognition, no component algebra or non-right angles.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: source one-unknown-coordinate linear solve; all 22 masks are sampled.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored exactly two nonzero linear dot terms, never x*x or extra branches.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 kind=field_type.split('/')[-1] if field_type else None
 rng=random.Random(seed)
 if profile and profile.startswith('observed:'):
  pt=profile.split(':',1)[1]
  if template and pt!=template:raise ValueError('Profile/template mismatch')
  template=pt
 if template is None:
  eligible=[k for k,v in TEMPLATES.items() if v['level']==level and (not kind or kind==v['type'])]
  if not eligible:raise ValueError('No field type at this level')
  template=rng.choice(eligible)
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level or kind and TEMPLATES[template]['type']!=kind:raise ValueError('Template/level/type mismatch')
 kind=TEMPLATES[template]['type'];raw=bool(profile and profile.startswith('observed:'))
 if level=='easy':
  if profile not in (None,'blank'):raise ValueError('Easy has only the observed-style blank shape')
  params=parameters or {}
  if params:raise ValueError('Easy has no numeric or notation diversity parameters')
  condition='the nonzero vectors $a$ and $b$ are perpendicular' if template=='perpendicular' else 'the angle between the nonzero vectors $a$ and $b$ is $90^\\circ$'
  prompt='Given that '+condition+', find the scalar projection of $a$ onto $b.$\n\n{{field-1}}'
  solution='Since $a$ and $b$ are perpendicular, the scalar projection of $a$ onto $b$ is $0.$' if template=='perpendicular' else 'Using the formula for the scalar projection, we obtain\n\n$$\n'+r'\begin{aligned}\text{comp}_{b}\,a & =|a|\cos\theta \\ & =|a|\cos(90^\circ) \\ & =|a|\cdot 0 \\ & =0.\end{aligned}'+'\n$$'
  return build_record(level,seed,template,'blank',{},prompt,solution,[sp.S(0)],['correct'],'field-1',kind,task={'criterion':'perpendicular-scalar-projection-zero'})
 cfg=RECIPES.get(template,{})
 if level=='moderate':
  chosen=profile or ('blank' if kind=='blank' else method_profile(*[[exact(c) for c in cfg['parameters'][k]] for k in ('p','q')]))
  if kind=='blank' and chosen not in ('blank','observed:'+template) or kind=='radio' and chosen=='blank':raise ValueError('Profile/field type mismatch')
  params=parameters if parameters is not None else moderate_parameters(cfg,rng,chosen)
 else:
  chosen=profile or ('blank' if kind=='blank' else 'method:hard')
  if chosen not in ('blank','method:hard') or kind=='blank' and chosen!='blank' or kind=='radio' and chosen!='method:hard':raise ValueError('Hard profile/type mismatch')
  if parameters is None:
   for _ in range(1000):
    a,b,c,d=[sp.Integer(rng.choice([i for i in range(-6,7) if i])) for _ in range(4)]
    params={'p':['x',str(a),str(b)],'q':[str(c),'x',str(d)]}
    try:
     p,q=[[exact(t) for t in params[k]] for k in ('p','q')];validate_parameters(level,p,q,cfg,False)
     vs,_=bank(p,q,chosen,cfg);check_bank(vs,dot_data(p,q)[3]);break
    except ValueError:pass
   else:raise ValueError('No eligible whole hard instance')
  else:params=parameters
 if set(params)!= {'p','q'}:raise ValueError('Require exactly p/q vector parameters')
 p,q=[[exact(t) for t in params[k]] for k in ('p','q')]
 products,A,B,r=validate_parameters(level,p,q,cfg,raw)
 vals,labels=bank(p,q,chosen,cfg);check_bank(vals,r)
 # First option is always mathematically correct before deterministic shuffling.
 if vals[0]!=r:
  idx=next(i for i,v in enumerate(vals) if v==r);vals[0],vals[idx]=vals[idx],vals[0];labels[0],labels[idx]=labels[idx],labels[0]
 if level=='moderate':
  n1,n2=cfg['names'];prompt=cfg['prompt_mask'].replace('@V1@',vector(p,cfg['layout'])).replace('@V2@',vector(q,cfg['layout']))
  dotblock,solveblock=solution_blocks(p,q,(n1,n2),cfg,raw)
  solution=cfg['solution_mask'].replace('@DOTBLOCK@',dotblock).replace('@SOLVEBLOCK@',solveblock)
  if not raw and cfg.get('solution_alias_error'):
   solution=solution.replace('$p$','$a$').replace('$q$','$b$').replace('p⊥q','a⊥b').replace(r'p\cdot q',r'a\cdot b')
  key=cfg['field_key']
 else:
  n1,n2='p','q';key='field-1' if kind=='blank' else 'selection'
  prompt='Let $p='+vector(p,'angle')+'$ and $q='+vector(q,'angle')+'.$ Given that the scalar projection of $p$ onto $q$ is zero, find the value of $x.$'+ ('\n\n$x=$\n{{field-1}}' if kind=='blank' else '')
  dotblock,solveblock=solution_blocks(p,q,('p','q'),{})
  solution='Since $p$ is a nonzero vector, its scalar projection onto another nonzero vector $q$ equals zero only when the vectors are perpendicular. \n\nSo, we must have\n\n$$\np⊥q\\,⟹\\,p\\cdot q=0.\n$$\n\nComputing the dot product, we obtain\n\n$$\n\\begin{aligned}'+dotblock+'\\end{aligned}\n$$\n\nSetting the dot product equal to $0,$ we get\n\n$$\n\\begin{aligned}'+solveblock+'\\end{aligned}\n$$'
 if kind=='blank' and '{{'+key+'}}' not in prompt:raise ValueError('Blank placeholder missing')
 # Canonical assessed task excludes notation, profile, incidental zero products,
 # and common scaling of the complete linear equation.
 normalized=[str(sp.cancel(t/A)) for t in products]
 task={'criterion':'zero-projection-unknown-component','linear_contributions':sorted(normalized),'unknown_contributions':sum(t.has(X) for t in products)}
 return build_record(level,seed,template,chosen,{k:list(map(str,v)) for k,v in zip(('p','q'),(p,q))},prompt,solution,vals,labels,key,kind,raw,cfg.get('source_id'),task)

def markdown(r):
 q=r['question'];g=r['generation']
 label=('Observed original replay' if g.get('source_replay') else 'Generated evidence-only variant') if g['profile'].startswith('observed:') else 'Generated variant'
 text=f"### {label}: {q[':question/difficulty'].split('/')[-1]} / {g['template']} / {g['profile']}\n\n"+q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  correct=f[':answer-field/correct'][1]
  text+='\n'.join(('- [x] ' if a[':answer/id']==correct else '- [ ] ')+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'
 return text+'Worked solution:\n\n'+q[':question/worked-solution']+'\n'

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type');args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
 records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
