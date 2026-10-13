#!/usr/bin/env python3
"""Relate an instantaneous derivative to supplied rates; no calculus evaluation.

math basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
Nine fully slotted source prose/layout templates and five complete bank profiles
are extracted in 17592186064272/templates.json. Three missing fields are authored
supported radio repairs, not recovered fields. The missing hard level is an
explicitly authored signed-net-rate extension. Different contexts, units, letters
and choice order do not constitute different mathematical tasks. The meaningful
finite structures are growth, positive loss, positive entry-minus-exit and signed
entry-plus-exit. No source or new task substitutes into a rate function.

API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None); generate_easy/moderate/hard. Complete operation banks are selected
before construction and rejected as a whole if ambiguous. Explicit inputs fail
instead of being replaced. UUID identities hash the actual prompt, fixed solution
and complete bank; task fingerprints exclude bank and incidental notation.
Source playback uses the same slotted recipes as ordinary generation. Captured
physical-unit errors receive documented repairs; original
records remain in source.json. No EDB writes, renderer or network dependencies.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064272
KP_UUID='fa38f112-466c-50e9-ac08-be72b6f53782'
TITLE='Relating a Derivative to a Rate of Change'
VERSION='derivative-rate-1'
EVIDENCE=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES=json.loads((EVIDENCE/'templates.json').read_text())
TEMPLATES.update({
 'single_growth':{'kind':'single','level':'easy','profile':'single_sign','source_id':None},
 'single_loss':{'kind':'loss','level':'easy','profile':'single_loss','source_id':None},
 'net_magnitudes':{'kind':'net','level':'moderate','profile':'net_standard','source_id':None},
 'signed_net':{'kind':'signed','level':'hard','profile':'signed_net','source_id':None},
})
# Five observed bank profiles (museum_net differs only in notation), and two
# authored sign-aware profiles. Each tuple contains ALL five displayed operations.
PROFILES={
 'single_sign':('single',('stock_rate','stock_rate_derivative','correct','stock_negative_rate_derivative','negative_derivative_rate')),
 'single_reciprocal':('single',('reciprocal','square_rate','correct','stock_rate_derivative','one_minus_rate')),
 'museum_net':('net',('stock_sum','correct','product','sum','stock_difference')),
 'net_standard':('net',('sum','correct','stock_sum','stock_difference','product')),
 'net_accounts':('net',('stock_negative_sum','stock_sum','sum','correct','stock_difference')),
 'single_loss':('loss',('stock_rate','stock_rate_derivative','correct','positive_derivative_rate','stock_negative_rate')),
 'signed_net':('signed',('difference','correct','negative_sum','stock_sum','product')),
}
CONTEXTS={
 'water':('volume of water in a tank','liters','minutes'),
 'grain':('mass of grain in a silo','kilograms','hours'),
 'fuel':('volume of fuel in a reservoir','liters','seconds'),
 'inventory':('number of items in a store','items','days'),
}
LETTERS=tuple('ABCEFGHILMNOPQRSUVWZ')
TIMES=('t','u','s')
CLARIFIER='The change ratio denotes an instantaneous rate: the limit of change ratios as the time interval tends to zero.'

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,x))
def slot(mask,p):
 for k,v in p.items():mask=mask.replace('@'+k+'@',str(v))
 if re.search(r'@[A-Z]+@',mask):raise ValueError('unfilled template slot')
 return mask

def check_parameters(spec,p):
 kind=spec['kind']; keys={'Q','T','unit','R'} if kind in ('single','loss') else {'Q','T','unit','I','L'}
 if not spec.get('source_id'):keys|={'context'}
 if set(p)!=keys:raise ValueError('parameters must contain exactly '+str(sorted(keys)))
 functions=[p[k] for k in ('Q','R') if k in p] if kind in ('single','loss') else [p[k] for k in ('Q','I','L')]
 if any(not re.fullmatch(r'[A-Za-z]',v) for v in functions):raise ValueError('function names must be single letters')
 if len(set(functions))!=len(functions) or p['T'] in functions or p['T'] not in TIMES:raise ValueError('function/time names must be distinct; time is t/u/s')
 if spec.get('source_id'):
  if p['unit']!=spec['parameters']['unit']:raise ValueError('source context has a fixed time unit')
 else:
  if p['context'] not in CONTEXTS or p['unit']!=CONTEXTS[p['context']][2]:raise ValueError('context and physical time unit disagree')


def sample(spec,rng):
 names=rng.sample(LETTERS,3);kind=spec['kind']; p={'Q':names[0],'T':rng.choice(TIMES)}
 if kind in ('single','loss'):p['R']=names[1].lower()
 else:p.update(I=names[1],L=names[2])
 # Retry if a lower-case rate name happens to equal the independent variable.
 if p.get('R')==p['T']:p['R']='v' if p['T']!='v' else 'r'
 if spec.get('source_id'):p['unit']=spec['parameters']['unit']
 else:
  p['context']=rng.choice(tuple(CONTEXTS));p['unit']=CONTEXTS[p['context']][2]
 return p


def relation_bank(kind,p,profile):
 """Derive exact full equations and source spelling from complete error operations."""
 Q=p['Q'];T=p['T'];qt=f'{Q}({T})';dt=f'{{{Q}}}^{{′}}({T})'
 if profile=='museum_net':dt=f'{Q}^{{′}}({T})'
 rt=f"{p.get('R','r')}({T})";rd=f"{{{p.get('R','r')}}}^{{′}}({T})"
 it=f"{p.get('I','I')}({T})";lt=f"{p.get('L','L')}({T})"
 formulas={
 'stock_rate':(qt,rt),'stock_rate_derivative':(qt,rd),
 'stock_negative_rate_derivative':(qt,'-'+rd),'negative_derivative_rate':(dt,'-'+rt),
 'positive_derivative_rate':(dt,rt),'stock_negative_rate':(qt,'-'+rt),
 'reciprocal':(dt,r'\frac{1}{'+rt+'}'),'square_rate':(qt,f"{{{p.get('R','r')}}}^{{2}}({T})"),
 'one_minus_rate':(dt,'1-'+rt),
 'stock_sum':(qt,it+'+'+lt),'stock_difference':(qt,it+'-'+lt),
 'stock_negative_sum':(qt,'-'+it+'-'+lt),
 'sum':(dt,it+'+'+lt),'difference':(dt,it+'-'+lt),
 'negative_sum':(dt,'-'+it+'-'+lt),'product':(dt,it+r'\cdot '+lt),
 'correct':(dt,rt if kind=='single' else '-'+rt if kind=='loss' else it+'-'+lt if kind=='net' else it+'+'+lt),
 }
 # Exact universal-identity eligibility: arbitrary supplied functions need not
 # obey any extra equation. Wrong relations may coincide at particular times;
 # they cannot be identical under the supplied relationship for all times.
 qv,dq,rv,dr,iv,lv=sp.symbols('q dq r dr i l')
 exact={
 'stock_rate':qv-rv,'stock_rate_derivative':qv-dr,
 'stock_negative_rate_derivative':qv+dr,'negative_derivative_rate':dq+rv,
 'positive_derivative_rate':dq-rv,'stock_negative_rate':qv+rv,
 'reciprocal':dq-1/rv,'square_rate':qv-rv**2,'one_minus_rate':dq-1+rv,
 'stock_sum':qv-iv-lv,'stock_difference':qv-iv+lv,
 'stock_negative_sum':qv+iv+lv,'sum':dq-iv-lv,'difference':dq-iv+lv,
 'negative_sum':dq+iv+lv,'product':dq-iv*lv,
 }
 expected=rv if kind=='single' else -rv if kind=='loss' else iv-lv if kind=='net' else iv+lv
 exact['correct']=dq-expected
 residuals=[exact[k] for k in PROFILES[profile][1]]
 if sum(sp.simplify(v.subs(dq,expected))==0 for v in residuals)!=1:
  raise ValueError('ambiguous whole operation bank')
 for j,a in enumerate(residuals):
  for b in residuals[j+1:]:
   ratio=sp.cancel(a/b)
   if ratio!=0 and not ratio.free_symbols:raise ValueError('equivalent complete options')
 result=[]
 for recipe in PROFILES[profile][1]:
  lhs,rhs=formulas[recipe]
  if profile=='museum_net':
   rhs=rhs.replace('+',' + ').replace('-',' - ').replace(r'\cdot',r' \cdot')
   text=lhs+' = '+rhs
  else:text=lhs+'='+rhs
  result.append((recipe,text))
 return result


def authored_text(kind,p):
 Q,T=p['Q'],p['T']; desc,amount,unit=CONTEXTS[p['context']];q=f'{Q}({T})';d=f"{Q}'({T})"
 intro=f'A model records the {desc} at time ${T}$, measured in {unit} after observations begin.\n\n- ${q}$ - the {desc}, in {amount}.\n\n'
 if kind in ('single','loss'):
  r=f"{p['R']}({T})";word='increasing' if kind=='single' else 'decreasing'
  prompt=intro+f'- ${r}$ - the positive rate at which that amount is {word}, in {amount} per {unit[:-1]}.\n\nWhat is the relationship between ${q}$ and ${r}$?'
  final=d+'='+('' if kind=='single' else '-')+r
  conclusion=f'Thus, ${d}$ gives the instantaneous rate of change of that amount. '+(f'This is the same as ${r}$.' if kind=='single' else f'The amount is decreasing, so the derivative is the negative of the positive loss rate ${r}$.')+f' Therefore, the relationship is ${final}$.'
  solution=f'The function ${q}$ gives the {desc} after ${T}$ {unit}. Then,\n\n$$\n{d}=\\frac{{\\text{{d}}{q}}}{{\\text{{d}}{T}}}=\\frac{{\\text{{Change in }}{Q}}}{{\\text{{Change in }}{T}}}.\n$$\n\n'+conclusion
 else:
  i,l=f"{p['I']}({T})",f"{p['L']}({T})"
  rateunit=f'{amount} per {unit[:-1]}'
  prompt=intro+f'- ${i}$ - the positive rate at which the amount is added, in {rateunit}.\n\n'
  if kind=='net':prompt+=f'- ${l}$ - the positive rate at which the amount is removed, in {rateunit}.'
  else:prompt+=f'- ${l}$ - the signed contribution of removal to the rate of change, in {rateunit}; ${l}<0$ when removal occurs.'
  prompt+='\n\nWhat is the relationship between the three functions above?'
  final=d+'='+i+('-' if kind=='net' else '+')+l
  solution=f'The function ${q}$ gives the {desc} after ${T}$ {unit}. Then,\n\n$$\n{d}=\\frac{{\\text{{d}}{q}}}{{\\text{{d}}{T}}}=\\frac{{\\text{{Change in }}{Q}}}{{\\text{{Change in }}{T}}}.\n$$\n\nThus, ${d}$ gives the instantaneous rate at which the amount changes at time ${T}$.\n\n'
  if kind=='net':solution+=f'In addition, we can compute this rate by finding the difference between the addition and removal rates at time ${T}$. That is,'
  else:solution+=f'In addition, ${l}$ already includes the negative sign of removal. We add the two signed contributions at time ${T}$. That is,'
  solution+='\n\n$$\n'+final+'.\n$$'
 return prompt,solution


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('invalid difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only radio is supported')
 if profile is not None and profile not in PROFILES:raise ValueError('unknown profile')
 rng=random.Random(seed)
 if template is None:
  defaults={'easy':['single_growth','single_loss'],'moderate':['net_magnitudes'],'hard':['signed_net']}
  eligible=defaults[level]
  if profile:eligible=[k for k,v in TEMPLATES.items() if v['level']==level and v['kind']==PROFILES[profile][0]]
  if not eligible:raise ValueError('profile unavailable at difficulty')
  template=rng.choice(eligible)
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level:raise ValueError('template/difficulty mismatch')
 spec=TEMPLATES[template];kind=spec['kind'];profile=profile or spec['profile']
 if PROFILES[profile][0]!=kind:raise ValueError('profile does not assess template relationship')
 p=dict(parameters) if parameters is not None else sample(spec,rng);check_parameters(spec,p)
 bank=relation_bank(kind,p,profile)
 if spec.get('source_id'):
  prompt=slot(spec['prompt_mask'],p);solution=slot(spec['solution_mask'],p)
 else:prompt,solution=authored_text(kind,p)
 # The observed derivative ratio is informal; preserve its ordered stage and
 # explicitly identify its limiting, instantaneous meaning in normal output.
 fixed_solution=solution+'\n\n'+CLARIFIER
 payload={'version':VERSION,'prompt':prompt,'solution':fixed_solution,'bank':sorted(v for _,v in bank),'level':level}
 identity=digest(payload);question_id=uid(identity);field_id=uid(identity+'/selection')
 answers=[];correct=None
 for recipe,value in bank:
  aid=uid(field_id+'/'+value);answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
  if recipe=='correct':correct=aid
 if correct is None or len({a[':answer/value'] for a in answers})!=5:raise ValueError('invalid whole bank')
 rng.shuffle(answers)
 field={':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 fingerprint=digest({'skill':'derivative-supplied-rate-relationship','semantic_structure':kind})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':question_id,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':fixed_solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'source':SOURCE,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'source_ids':[spec['source_id']] if spec.get('source_id') else [],'origin':'source template with documented repairs' if spec.get('source_id') else 'authored same-skill extension','repairs':spec.get('repairs',[]),'field_origin':spec.get('field_origin','authored'),'content_fingerprint':identity,'mathematical_fingerprint':fingerprint,'domain':{'time':'nonnegative observation time','quantity':'nonnegative modeled amount','rate': 'positive growth/loss magnitude' if kind in ('single','loss') else 'positive entry and exit magnitudes' if kind=='net' else 'positive inflow and negative signed outflow'},'recipes':list(PROFILES[profile][1]),'dependencies':{'sympy':sp.__version__},'plots':[]}}

# EASY: direct positive growth or positive loss; the observed easy net-rate
# sources remain explicitly available with their recorded easy labels.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE: two positive flow magnitudes; identify derivative and subtract exit.
# The same workload is observed under easy too; no new numerical evaluation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)

# HARD (authored missing level): two contributions, one already signed negative.
# Extra demand is recognizing that subtraction would negate a sign twice.
# The structure is finite; contexts/units/letters provide peer presentations.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q,g=r['question'],r['generation'];f=q[':question/answer-fields'][0]
 return '\n\n'.join([f"## {q[':question/difficulty'].split('/')[-1]} — {g['template']} ({g['bank_profile']})",q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']),'**Worked solution**',q[':question/worked-solution']])

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(PROFILES));ap.add_argument('--format',choices=['markdown','json'],default='markdown');args=ap.parse_args()
 if args.count<1 or (args.template or args.profile) and args.difficulty=='all':ap.error('positive count and specific level are required for template/profile')
 try:records=[generate(lev,args.seed+n,args.template,profile=args.profile) for lev in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for n in range(args.count)]
 except ValueError as ex:ap.error(str(ex))
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
