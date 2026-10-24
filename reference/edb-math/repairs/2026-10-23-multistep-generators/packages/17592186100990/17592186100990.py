#!/usr/bin/env python3
"""Highlighted position -> matrix index, frozen math basis1356; no DB writes.

Every practice source is public via raw:q-* profiles using parameterized complete
matrix/prose/bank masks. Raw missing highlight/rating/correct refs/solution remain
missing; evidence-only. completed:q-* restores the highlight and authors only
missing refs/prose. Normal defaults use all supported observed families and all complete banks.
Symbolic-index blanks use native formal indexed-symbol grading.
Missing moderate/hard are authored longer visual scans, not observed MA labels.
Entries are incidental to the assessed positional operation; task counts exclude
all entry values, matrix-letter aliases, bank and field-layout aliases.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186100990-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186100990
KP_UUID='1cc70bda-40cf-5860-9a47-25f290c71041'
TITLE='Describing an Entry of a Matrix in Index Notation'
VERSION='highlight-to-index-v4'
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
LEVELS=('easy','moderate','hard')
TEMPLATES=('inline_radio','display_radio','two_indices','notation_blank')
SUPPORTED_TEMPLATES=TEMPLATES
STYLE={'q-139629':'two_indices','q-13498':'inline_radio','q-13503':'inline_radio','q-139426':'two_indices','q-13489':'display_radio','q-279553':'notation_blank','q-279556':'notation_blank','q-125611':'display_radio','q-13499':'display_radio'}
POSITIONS={'q-139629':(3,1),'q-13498':(1,2),'q-13503':(3,3),'q-139426':(3,2),'q-13489':(1,1),'q-279553':(1,1),'q-279556':(2,3),'q-125611':(4,2),'q-13499':(3,4)}
# Complete observed banks, in captured order. Coordinates explicitly identify
# their operations; intent for remote compound offsets is underdetermined.
# These are coordinate-offset generalizations, not arbitrary scalar fits.
BANKS={
 'q-13498':((1,-1),(0,1),(0,0),(1,0),(0,-1)),
 'q-13503':((-2,0),(0,0),(-1,-2),(-1,0),(1,0)),
 'q-13489':((0,0),(1,2),(1,1),(1,0),(0,1)),
 'q-125611':((-1,-1),(0,-1),(-1,0),(0,0),(0,1)),
 'q-13499':((-1,-3),(-2,-1),(1,-1),(-1,-2),(0,0)),
}
DIMS={'easy':((2,2),(2,3),(3,3),(3,4),(4,2),(4,4)), 'moderate':((5,6),(6,5)), 'hard':((6,7),(7,6))}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def ordinal(x):return str(x)+('th' if 10<=x%100<=20 else {1:'st',2:'nd',3:'rd'}.get(x%10,'th'))
def index(p,i=None,j=None,braced=True):
 return ('{'+p['letter'].lower()+'}' if braced else p['letter'].lower())+'_{'+str(i or p['i'])+str(j or p['j'])+'}'
def parse_matrix(text):
 m=re.search(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',text,re.S)
 if not m:raise ValueError('No matrix')
 return [[int(v.strip()) for v in r.split('&')] for r in m[1].split(r'\\')]
def source_parameters(sid):
 q=SOURCES[sid];a=parse_matrix(q[':question/problem']);l=re.search(r'\$([A-Z])\$',q[':question/problem'])[1]
 i,j=POSITIONS[sid];return {'matrix':a,'i':i,'j':j,'letter':l}
def matrix_body(p,highlight=False):
 return r' \\ '.join(' & '.join((r'\boxed{'+str(v)+'}') if highlight and (r,c)==(p['i'],p['j']) else str(v) for c,v in enumerate(row,1)) for r,row in enumerate(p['matrix'],1))
def validate_parameters(level,p,evidence=False):
 if set(p)!={'matrix','i','j','letter'}:raise ValueError('Exactly matrix,i,j,letter required')
 a=p['matrix'];i,j=p['i'],p['j']
 if not isinstance(a,list) or not a or not all(isinstance(r,list) and r and len(r)==len(a[0]) for r in a):raise ValueError('Rectangular nonempty matrix required')
 if not all(type(v)is int and -34<=v<=34 for r in a for v in r):raise ValueError('Entry integers -34..34 required')
 if type(i)is not int or type(j)is not int or not (1<=i<=len(a) and 1<=j<=len(a[0])):raise ValueError('Existing integer position required')
 if not isinstance(p['letter'],str) or not re.fullmatch('[A-Z]',p['letter']):raise ValueError('Single uppercase matrix letter required')
 if len(a)>7 or len(a[0])>7:raise ValueError('At most seven rows/columns')
 if not evidence:
  if (len(a),len(a[0])) not in DIMS[level]:raise ValueError('Level-specific dimensions violated')
  if level=='moderate' and max(i,j)<4 or level=='hard' and max(i,j)<5:raise ValueError('Level-specific scan distance violated')
  if not all(-9<=v<=9 for r in a for v in r):raise ValueError('Normal scan entries are single-digit integers -9..9')
def eligible_positions(level,bank=None):
 return [(m,n,i,j) for m,n in DIMS[level] for i in range(1,m+1) for j in range(1,n+1)
  if not (level=='moderate' and max(i,j)<4 or level=='hard' and max(i,j)<5)]

def bank_placements(level,sid,parameters=None):
 """Place a whole observed shape independently of which slot is correct."""
 offsets=BANKS[sid];lo_i=min(i for i,j in offsets);lo_j=min(j for i,j in offsets)
 shape=[(i-lo_i,j-lo_j) for i,j in offsets]
 dims=[(len(parameters['matrix']),len(parameters['matrix'][0]))] if parameters else DIMS[level]
 out=[]
 for m,n in dims:
  for top in range(1,m+1):
   for left in range(1,n+1):
    cells=[(top+i,left+j) for i,j in shape]
    if any(i>9 or j>9 for i,j in cells):continue
    targets=[(i,j) for i,j in cells if i<=m and j<=n and
      not (level=='moderate' and max(i,j)<4 or level=='hard' and max(i,j)<5)]
    if len(targets)<2:continue
    if parameters and (parameters['i'],parameters['j']) not in targets:continue
    out.append((m,n,cells,targets))
 return out

def bank(p,sid,cells=None):
 braced=sid not in ('q-13498','q-13503')
 if cells is None:cells=[(p['i']+di,p['j']+dj) for di,dj in BANKS[sid]]
 values=[index(p,i,j,braced) for i,j in cells]
 if len(set(values))!=5 or not all(1<=i<=9 and 1<=j<=9 for i,j in cells):raise ValueError('Whole observed bank invalid')
 if (p['i'],p['j']) not in cells:raise ValueError('Bank must contain highlighted coordinate')
 return values

def source_render(p,sid,highlight=False):
 """Whole-component slots; never short-expression global substitution."""
 old=SOURCES[sid];op=source_parameters(sid);prompt=old[':question/problem']
 # Complete matrix interior, all matrix letter tokens and complete generic symbol.
 pattern=r'(\\begin\{(?:aligned|bmatrix)\})(.*?)(\\end\{(?:aligned|bmatrix)\})'
 prompt=re.sub(pattern,lambda m:m[1]+matrix_body(p,highlight)+m[3],prompt,flags=re.S)
 prompt=prompt.replace('$'+op['letter']+'$', '$'+p['letter']+'$')
 prompt=prompt.replace(op['letter']+' = ',p['letter']+' = ').replace(op['letter']+'=[',p['letter']+'=[')
 prompt=prompt.replace(op['letter']+'=',p['letter']+'=')
 prompt=prompt.replace('{'+op['letter'].lower()+'}_{ij}','{'+p['letter'].lower()+'}_{ij}').replace(op['letter'].lower()+'_{ij}',p['letter'].lower()+'_{ij}')
 solution=None
 if ':question/worked-solution' in old:
  solution=old[':question/worked-solution'];i,j=p['i'],p['j'];oi,oj=op['i'],op['j']
  # All source solutions share one ordered position sentence and one conclusion.
  solution=re.sub(r'at the intersection of the \$\d+\$(?:st|nd|rd|th) row and \$\d+\$(?:st|nd|rd|th) column',lambda _: 'at the intersection of the $'+str(i)+'$'+ordinal(i)[len(str(i)):]+' row and $'+str(j)+'$'+ordinal(j)[len(str(j)):]+' column',solution)
  if STYLE[sid]=='two_indices':
   solution=solution.replace('{'+op['letter'].lower()+'}_{ij}','{'+p['letter'].lower()+'}_{ij}')
   solution=re.sub(r'i=\d+',lambda _: 'i='+str(i),solution)
   solution=re.sub(r'j=\d+',lambda _: 'j='+str(j),solution)
  else:
   old_entry=index(op);new_entry=index(p);oldvalue=op['matrix'][oi-1][oj-1];newvalue=p['matrix'][i-1][j-1]
   conclusion=old_entry+'='+str(oldvalue) if STYLE[sid]=='display_radio' else str(oldvalue)+'='+old_entry
   newconclusion=new_entry+'='+str(newvalue) if STYLE[sid]=='display_radio' else str(newvalue)+'='+new_entry
   if conclusion not in solution:raise AssertionError('Complete conclusion mask missing')
   solution=solution.replace(conclusion,newconclusion)
 return prompt,solution

def normal_render(p,template):
 """Original source prose/stage masks retained; restore explicit highlight.

 Two-indices source capture whitespace alone is normalized to make slots visible.
 Each solution remains one positional statement then the original conclusion.
 """
 sid={'inline_radio':'q-13498','display_radio':'q-13489','two_indices':'q-139426','notation_blank':'q-279553'}[template]
 prompt,solution=source_render(p,sid,True)
 if template=='two_indices':prompt='\n'.join(x.strip() for x in prompt.splitlines());prompt=re.sub(r'\n{3,}','\n\n',prompt)
 if solution is None:
  solution='The entry lies at the intersection of the $'+str(p['i'])+'$'+ordinal(p['i'])[len(str(p['i'])):]+' row and $'+str(p['j'])+'$'+ordinal(p['j'])[len(str(p['j'])):]+' column. Hence, we have $'+index(p,braced=False)+'='+str(p['matrix'][p['i']-1][p['j']-1])+'.$'
 return prompt,solution

def assemble(level,seed,template,p,profile,sid=None,raw=False,cells=None):
 if sid:
  prompt,sol=source_render(p,sid,not raw)
  if not raw and sol is None:_,sol=normal_render(p,template)
  if not raw and template=='two_indices':prompt=re.sub(r'\n{3,}','\n\n','\n'.join(x.strip() for x in prompt.splitlines()))
 else:prompt,sol=normal_render(p,template)
 q={':question/problem':prompt}
 old=SOURCES[sid] if sid else None
 if not raw or ':question/difficulty' in old:q[':question/difficulty']=':question.difficulty/'+level
 if sol is not None:q[':question/worked-solution']=sol
 # Preserve raw source replay, while all completed and normal variants render
 # matrix columns and brackets correctly and retain their highlighted cell.
 if not raw:
  for attr in (':question/problem', ':question/worked-solution'):
   if attr in q:q[attr]=q[attr].replace(r'[\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}')
  q[':question/problem']=q[':question/problem'].replace('where$', 'where $')
 # Preserve source field order (two_indices is column first, then row).
 if template=='two_indices':specs=[('field-2','blank',[str(p['j'])],str(p['j'])),('field-1','blank',[str(p['i'])],str(p['i']))]
 elif template=='notation_blank':v=index(p);specs=[('field-1','blank',[v],v)]
 else:
  bank_source=sid or profile
  values=bank(p,bank_source,cells)
  correct=index(p,braced=bank_source not in ('q-13498','q-13503'))
  specs=[('selection','radio',values,correct)]
 if sid:
  source_order={f[':answer-field/key']:i for i,f in enumerate(old[':question/answer-fields'])}
  specs.sort(key=lambda f:source_order[f[0]])
 refs=not raw or all(':answer-field/correct' in f for f in old[':question/answer-fields'])
 identity={'version':VERSION,'question':q,'fields':[{'key':k,'type':t,'bank':sorted(v),'correct':c if refs else None,'correct_present':refs} for k,t,v,c in specs]}
 cid=digest(identity);qid=uid('question:'+cid);fields=[]
 for key,typ,values,correct in specs:
  fid=uid(qid+':'+key);choices=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
  if typ=='radio':random.Random(seed).shuffle(choices)
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+typ,':answer-field/choices':choices}
  if refs:f[':answer-field/correct']=[':answer/id',uid(fid+':'+correct)]
  fields.append(f)
 q[':question/id']=qid;q[':question/answer-fields']=fields
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
  'version':VERSION,'seed':seed,'template':template,'profile':profile,'source':sid,
  'origin':'observed-parameterized' if raw else 'authored-source-completion' if sid else 'source-shaped-authored',
  'parameters':p,'mathematical_fingerprint':digest(['position-to-index',len(p['matrix']),len(p['matrix'][0]),p['i'],p['j']]),
  'content_identity':cid,'eligible_for_learning':not raw,'evidence_only':raw,
  'native_limitation':None,
  'source_provenance':CAPTURE.get('additional_source_provenance',{}).get(sid,{k:CAPTURE[k] for k in ('database','basis','lineage')}),
  'authored_level':level!='easy' or bool(sid and ':question/difficulty' not in old),
  'presentation_repair':not raw,'plot_rating':'none','plot_assets':{},
  'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},
  'bank_coordinates':cells if cells is not None else [[p['i']+di,p['j']+dj] for di,dj in BANKS[sid or profile]] if template.endswith('radio') else []}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio','blank'):raise ValueError('Unknown field type')
 rng=random.Random(seed);sid=None;raw=False;cells=None
 if profile and ':' in profile:
  mode,sid=profile.split(':',1)
  if mode not in ('raw','completed') or sid not in SOURCES:raise ValueError('Unknown evidence profile')
  if level!='easy':raise ValueError('Source replay API workload easy; original raw difficulty presence is preserved')
  raw=mode=='raw';selected=STYLE[sid]
  if template and template!=selected:raise ValueError('Source/template mismatch')
  template=selected
 elif profile and profile not in (*BANKS,'blank'):raise ValueError('Unknown bank profile')
 eligible=[t for t in (TEMPLATES if template is not None else SUPPORTED_TEMPLATES) if field_type is None or (t.endswith('radio'))==(field_type=='radio')]
 if template and template not in eligible:raise ValueError('Template/field mismatch')
 if profile in BANKS and template and not template.endswith('radio'):raise ValueError('Radio bank requires radio template')
 if profile=='blank' and template and template.endswith('radio'):raise ValueError('Blank profile requires blank template')
 if template is None:
  if profile in BANKS:eligible=[t for t in eligible if t.endswith('radio')]
  if profile=='blank':eligible=[t for t in eligible if not t.endswith('radio')]
  if not eligible:raise ValueError('Profile and field type conflict')
  template=rng.choice(eligible)
 if not sid:
  if template.endswith('radio'):
   # Select complete bank BEFORE parameters, never first-valid candidate recipes.
   profile=profile or (list(BANKS)[int(digest(parameters),16)%len(BANKS)] if parameters is not None else rng.choice(tuple(BANKS)))
  else:profile=profile or 'blank'
 if not sid and template.endswith('radio'):
  placements=bank_placements(level,profile,parameters)
  if not placements:raise ValueError('No whole-bank placement contains this target with another eligible target')
  m,n,cells,targets=rng.choice(placements)
  i,j=rng.choice(targets)
 elif not sid and parameters is None:
  m,n,i,j=rng.choice(eligible_positions(level))
 if parameters is None:
  if sid:p=source_parameters(sid)
  else:p={'matrix':[[rng.randint(-9,9) for _ in range(n)] for _ in range(m)],'i':i,'j':j,'letter':rng.choice('ABCPXYZ')}
 else:p=json.loads(json.dumps(parameters))
 validate_parameters(level,p,evidence=bool(sid))
 return assemble(level,seed,template,p,profile,sid,raw,cells)

def generate_batch(level,seed,count,template=None,field_type=None,profile=None):
 """Finite practice pools include contrasting targets for each radio bank.

 A replay is literal. A single radio request cannot exhibit between-item
 variation. Larger radio groups reuse their bank, not their answer role.
 """
 if profile and ':' in profile:
  return [generate(level,seed+i,template,field_type,profile=profile) for i in range(count)]
 rng=random.Random(seed);out=[]
 while len(out)<count:
  remaining=count-len(out);item_seed=seed+len(out)
  selected=template
  if remaining==1 and selected is None and field_type!='radio' and profile not in BANKS:
   selected=rng.choice(('two_indices','notation_blank'))
  record=generate(level,item_seed,selected,field_type,profile=profile)
  out.append(record)
  if record['generation']['template'].endswith('radio') and remaining>1:
   g=record['generation'];p=g['parameters'];m,n=len(p['matrix']),len(p['matrix'][0])
   alternatives=[(i,j) for i,j in g['bank_coordinates'] if i<=m and j<=n and (i,j)!=(p['i'],p['j']) and
     not (level=='moderate' and max(i,j)<4 or level=='hard' and max(i,j)<5)]
   i,j=rng.choice(alternatives)
   other=dict(p,i=i,j=j)
   out.append(assemble(level,item_seed+1,g['template'],other,g['profile'],cells=g['bank_coordinates']))
   if remaining==3 and (template and template.endswith('radio') or field_type=='radio' or profile in BANKS):
    # Keep an explicitly radio-only odd tail in this same contrasting group.
    # If only two cells fit, repeat a role with new incidental data, not a
    # duplicate record that delivery deduplication would discard.
    targets=[(p['i'],p['j'])]+alternatives
    i,j=rng.choice(targets)
    matrix=[[rng.randint(-9,9) for _ in row] for row in p['matrix']]
    third=dict(p,matrix=matrix,i=i,j=j)
    out.append(assemble(level,item_seed+2,g['template'],third,g['profile'],cells=g['bank_coordinates']))
 # Output order must not signal which bank role was selected first.
 rng.shuffle(out)
 return out

# EASY: observed 2x2 through 4x2/3x4 scan shapes, all four source field families.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: authored 30-cell rectangular scan, 5x6 or 6x5, max(i,j)>=4.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored 42-cell rectangular scan, 6x7 or 7x6, max(i,j)>=5.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];out=[q.get(':question/difficulty','Unrated original evidence'),q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  out+=['Field '+f[':answer-field/key']+' ('+f[':answer-field/type']+')']
  for a in f[':answer-field/choices']:out+=['- $'+a[':answer/value']+'$']
  if ':answer-field/correct' in f:out+=['Correct: $'+next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])+'$']
 if ':question/worked-solution' in q:out+=['Worked solution:',q[':question/worked-solution']]
 return '\n\n'.join(out)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--field-type',choices=('radio','blank'));ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('Positive count required')
 levels=LEVELS if args.difficulty=='all' else [args.difficulty]
 try:records=[r for l in levels for r in generate_batch(l,args.seed,args.count,args.template,args.field_type,args.profile)]
 except ValueError as ex:ap.error(str(ex))
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186100990-source-policy.json'))

if __name__=='__main__':main()
