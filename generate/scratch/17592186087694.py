#!/usr/bin/env python3
"""Ordered dimensions of row, column and singleton matrices; local review only.

Easy assesses the observed one-step count. Moderate/hard are unsupported;
the prior authored-peer labels were not justified difficulty bands. Source profiles preserve complete historical
banks (including ordered \\cdot labels) and prompt/prose grammar. No DB writes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import sympy as sp

KP_ID = 17592186087694
KP_UUID = '34fd903a-fa34-57b0-a098-08fa1cbd4f95'
TITLE = 'Determining the Dimensions of a Matrix with One Row or Column'
VERSION = '1.1.0'
SUPPORTED_LEVELS = ('easy',)
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
EVIDENCE = Path(__file__).with_suffix('')
TEMPLATES = ('aligned_radio', 'double_blank', 'legacy_column', 'legacy_singleton')
# Each complete observed profile is retained. The numerical origin of the final
# options in legacy_column and row_observed is underdetermined; these explicit
# affine-count replay recipes are NOT used as recovered default error intent.
PROFILES = {
 'authored': ('aligned_radio', None),
 'row_observed': ('aligned_radio', 'q-7809'),
 'singleton_root_observed': ('aligned_radio', 'q-125543'),
 'singleton_zero_observed': ('aligned_radio', 'q-7813'),
 'legacy_column_observed': ('legacy_column', 'q-7810'),
 'legacy_singleton_observed': ('legacy_singleton', 'q-7812'),
 'blank_observed': ('double_blank', 'q-319329'),
 'blank_plural_observed': ('double_blank', 'q-319338'),
}
ENTRY_POOL = tuple(map(str,range(-9,10))) + (r'\frac{2}{3}',r'-\frac{1}{2}',r'\sqrt{2}',r'-\sqrt{3}',r'-\sqrt{7}')
SHAPES = ((1,1),)+tuple((1,n) for n in range(2,6))+tuple((n,1) for n in range(2,6))

def stable(v):
 return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(v):
 return hashlib.sha256(stable(v).encode()).hexdigest()
def uid(parent,text):
 return str(uuid.uuid5(uuid.UUID(parent),text))
def entry_value(s):
 """Bounded exact scalar grammar; never treat signs/roots/fractions as columns."""
 if re.fullmatch(r'-?\d+',s): return sp.Integer(s)
 m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',s)
 if m and int(m[3]): return (-1 if m[1] else 1)*sp.Rational(int(m[2]),int(m[3]))
 m=re.fullmatch(r'(-?)\\sqrt\{(\d+)\}',s)
 if m: return (-1 if m[1] else 1)*sp.sqrt(int(m[2]))
 raise ValueError('Entry must be an integer, exact fraction or numeric square root')
def dimensions(p):
 return len(p['entries']),len(p['entries'][0])
def guard(p,template,profile):
 if set(p) != {'name','entries'}: raise ValueError('Expected name and entries only')
 if not re.fullmatch('[A-Z]',p['name']): raise ValueError('Matrix name must be one uppercase letter')
 a=p['entries']
 if not isinstance(a,list) or not a or not all(isinstance(row,list) and row for row in a): raise ValueError('Nonempty rectangular array required')
 if len({len(row) for row in a})!=1: raise ValueError('Ragged array')
 r,c=dimensions(p)
 if (r,c) not in SHAPES: raise ValueError('Only one row/column; length 1..5')
 for row in a:
  for x in row:
   if not isinstance(x,str): raise ValueError('Entries must be TeX strings')
   v=entry_value(x)
   if not v.is_real or abs(v)>9: raise ValueError('Entry magnitude must be at most nine')
 if template=='legacy_column' and not (c==1 and r>=2): raise ValueError('Legacy column template requires a non-singleton column')
 if template=='legacy_singleton' and (r,c)!=(1,1): raise ValueError('Legacy singleton template requires 1×1')
 if profile=='row_observed' and not (r==1 and c>=2): raise ValueError('Observed row profile requires row length >=2')
 if 'singleton' in profile and (r,c)!=(1,1): raise ValueError('Singleton profile requires 1×1')
 if profile=='legacy_singleton_observed':
  v=entry_value(a[0][0])
  if not v.is_Integer or not 2<=v<=9: raise ValueError('Legacy singleton bank requires positive integer entry 2..9')

def sample(rng,template,profile):
 if 'singleton' in profile or template=='legacy_singleton': r,c=1,1
 elif template=='legacy_column': r,c=rng.randint(2,5),1
 elif profile=='row_observed': r,c=1,rng.randint(2,5)
 else: r,c=rng.choice(SHAPES)
 entries=[[rng.choice(ENTRY_POOL) for _ in range(c)] for _ in range(r)]
 if profile=='legacy_singleton_observed': entries=[[str(rng.randint(2,9))]]
 return {'name':rng.choice('ABCDEFGHJKLMNPQRSTUVWXYZ'),'entries':entries}

def render_array(p,template):
 body=r' \\ '.join(' & '.join(row) for row in p['entries'])
 if template=='legacy_column': return r'\begin{bmatrix}'+body+r'\end{bmatrix}'
 if template=='legacy_singleton': return '['+body+']'
 return r'[\begin{aligned}'+body+r'\end{aligned}]'
def prompt(p,template):
 name=p['name']; array=render_array(p,template)
 if template=='legacy_column': return f'What are the dimensions of the matrix ${name}$, where ${name} = {array}$?'
 if template=='legacy_singleton': return f'What are the dimensions of the matrix ${name}$ where ${name} = {array}$?'
 if template=='double_blank': return f'Let ${name}={array}.$ \nThe dimensions of the matrix ${name}$ are'+ '{{field-1}}\n$\\times $\n{{field-2}}.'
 return f'What are the dimensions of the matrix ${name}$, where ${name}={array}?$'

def solution(p,template,profile):
 r,c=dimensions(p); name=p['name']
 rows='row' if r==1 else 'rows'; columns='column' if c==1 else 'columns'
 if profile=='blank_plural_observed': columns='columns' # captured grammatical typo; no mathematical error
 if template=='double_blank': return f'The matrix ${name}$ has ${r}$ {rows} and ${c}$ {columns}. Therefore, its dimensions are ${r}\\times {c}.$'
 if profile in ('singleton_root_observed','singleton_zero_observed'): return f'The matrix ${name}$ has ${r}$ {rows}  and ${c}$ {columns}.  So,  its dimensions are  ${r}\\times {c}.$'
 if profile=='row_observed': return f'The matrix ${name}$ has ${r}$ {rows} and ${c}$ {columns}.  Hence,  its dimensions are  ${r}\\times {c}.$'
 return f'The matrix ${name}$ has ${r}$ {rows} and ${c}$ {columns}. So, its dimensions are ${r}\\times {c}.$'

def bank(p,profile):
 r,c=dimensions(p); n=max(r,c)
 if profile=='row_observed': pairs=[(0,n),(n,0),(n,1),(1,n),(n-1,2*n-1)]
 elif profile=='singleton_root_observed': pairs=[(2,0),(0,2),(1,2),(1,0),(1,1)]
 elif profile=='singleton_zero_observed': pairs=[(0,1),(0,0),(1,0),(1,1),(2,1)]
 elif profile=='legacy_column_observed': pairs=[(1,n),(n,1),(1,1),(n,n),(n+2,n-1)]
 elif profile=='legacy_singleton_observed':
  v=int(entry_value(p['entries'][0][0])); pairs=[(v,v),(0,1),(1,1),(1,0),(0,0)]
 elif (r,c)==(1,1): pairs=[(1,1),(0,1),(1,0),(0,0),(2,2)]
 else:
  pairs=[(r,c),(c,r),(n,n),(0,c),(r,0)]
 if len(set(pairs))!=5 or pairs.count((r,c))!=1: raise ValueError('Reject entire ambiguous bank')
 op=' \\cdot ' if profile.startswith('legacy_') else r'\times '
 return [(str(a)+op+str(b),(a,b)==(r,c)) for a,b in pairs]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: only easy is validated; see capabilities.json')
 if field_type not in (None,'blank','radio'): raise ValueError('Invalid field type')
 if profile is not None and profile not in PROFILES: raise ValueError('Unknown complete profile')
 rng=random.Random(seed)
 if profile and profile!='authored':
  prescribed=PROFILES[profile][0]
  if template and template!=prescribed: raise ValueError('Profile/template conflict')
  template=prescribed
 template=template or ('double_blank' if field_type=='blank' else rng.choice(('aligned_radio','double_blank')))
 if template not in TEMPLATES: raise ValueError('Unknown template')
 kind='blank' if template=='double_blank' else 'radio'
 if field_type and kind!=field_type: raise ValueError('Template/field conflict')
 if profile is None: profile='blank_observed' if kind=='blank' else 'legacy_column_observed' if template=='legacy_column' else 'legacy_singleton_observed' if template=='legacy_singleton' else 'authored'
 if kind=='blank' and profile=='authored': profile='blank_observed'
 p=json.loads(json.dumps(parameters)) if parameters is not None else sample(rng,template,profile)
 guard(p,template,profile)
 r,c=dimensions(p); text=prompt(p,template); worked=solution(p,template,profile)
 values=bank(p,profile) if kind=='radio' else []
 # Source field collection order is field-2 then field-1; their placeholders
 # still correctly request row count first and column count second.
 specs=[('selection',values)] if kind=='radio' else [('field-2',[(str(c),True)]),('field-1',[(str(r),True)])]
 content=digest({'version':VERSION,'problem':text,'solution':worked,'fields':[(k,kind,sorted(v)) for k,v in specs]})
 qid=uid(KP_UUID,content); fields=[]
 for key,vals in specs:
  fid=uid(qid,key); answers=[{':answer/id':uid(fid,'math:'+value),':answer/type':':answer.type/math',':answer/value':value} for value,correct in vals]
  correct_id=next(a[':answer/id'] for a,(_,correct) in zip(answers,vals) if correct)
  if kind=='radio': rng.shuffle(answers)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':text,':question/worked-solution':worked,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'parameter_fingerprint':digest({'ordered_dimensions':[r,c]}),'content_fingerprint':content,'basis':1356,'database':'math','lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','source_id':PROFILES[profile][1],'level_origin':'observed-or-supported-easy' if level=='easy' else 'authored-peer-level','meaningful_shape_count':9,'scope':'Count rows, then columns; entries are incidental','dependencies':{'sympy':sp.__version__}}}

# EASY: observed row/column/singleton reading, radios and two separate blanks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: explicitly unsupported; no harder counting move is validated.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: explicitly unsupported; no harder counting move is validated.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def batch(level,count,seed=0,template=None,field_type=None,profile=None):
 """Distinct ordered dimension tasks; incidental entry/choice changes never refill."""
 if level not in SUPPORTED_LEVELS: raise ValueError('Unsupported difficulty: '+level)
 if count<1: raise ValueError('Positive count required')
 used=set(); records=[]
 for offset in range(1000):
  record=generate(level,seed+offset,template,field_type,profile=profile)
  fp=record['generation']['parameter_fingerprint']
  if fp not in used:
   used.add(fp); records.append(record)
   if len(records)==count:return records
 raise ValueError(f'Finite variant limit: requested {count}, found {len(records)} distinct shapes in this profile')

def markdown(record):
 q=record['question']; lines=[q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  for a in f[':answer-field/choices']:
   correct=a[':answer/id']==f[':answer-field/correct'][1]
   lines.append(f"- {f[':answer-field/key']}: ${a[':answer/value']}$"+(' (correct)' if correct else ''))
 return '\n'.join(lines+['','Worked solution: '+q[':question/worked-solution']])
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--difficulty',choices=('all','easy','moderate','hard'),default='all'); ap.add_argument('--seed',type=int,default=0); ap.add_argument('--count',type=int,default=1); ap.add_argument('--format',choices=('markdown','json'),default='markdown'); ap.add_argument('--template',choices=TEMPLATES); ap.add_argument('--profile',choices=tuple(PROFILES)); ap.add_argument('--field-type',choices=('blank','radio'))
 args=ap.parse_args()
 if args.count<1: ap.error('Positive count required')
 levels=SUPPORTED_LEVELS if args.difficulty=='all' else (args.difficulty,)
 records=[record for level in levels for record in batch(level,args.count,args.seed,args.template,args.field_type,args.profile)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(x) for x in records))
if __name__=='__main__': main()
