from pathlib import Path
import json
w=Path(__file__).resolve().parent
p=w/'17592186100990.py'
s=p.read_text()
s=s.replace('Symbolic-index blanks remain public ineligible drafts because the native math\nparser rejects subscript notation; normal blanks use supported numeric indices.', 'Symbolic-index blanks use native formal indexed-symbol grading.')
s=s.replace("VERSION='highlight-to-index-v3'", "VERSION='highlight-to-index-v4'")
s=s.replace("SUPPORTED_TEMPLATES=('inline_radio','display_radio','two_indices')", "SUPPORTED_TEMPLATES=TEMPLATES")
s=s.replace("STYLE={'q-13498'", "STYLE={'q-139629':'two_indices','q-13498'")
s=s.replace("POSITIONS={'q-13498'", "POSITIONS={'q-139629':(3,1),'q-13498'")
s=s.replace("(3,4),(4,2))", "(3,4),(4,2),(4,4))")
a=s.index('def eligible_positions(');b=s.index('\ndef source_render',a)
s=s[:a]+'''def eligible_positions(level,bank=None):
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
''' +s[b:]
s=s.replace('def assemble(level,seed,template,p,profile,sid=None,raw=False):','def assemble(level,seed,template,p,profile,sid=None,raw=False,cells=None):')
s=s.replace('values=bank(p,bank_source)','values=bank(p,bank_source,cells)')
s=s.replace("'eligible_for_learning':not raw and template!='notation_blank','evidence_only':raw or template=='notation_blank',", "'eligible_for_learning':not raw,'evidence_only':raw,")
s=s.replace("'native_limitation':'Symbolic index blank parser: unconsumed mathematical notation' if template=='notation_blank' else None,", "'native_limitation':None,")
s=s.replace("'distractor_operations':[[di,dj] for di,dj in BANKS[sid or profile]] if template.endswith('radio') else []", "'bank_coordinates':cells if cells is not None else [[p['i']+di,p['j']+dj] for di,dj in BANKS[sid or profile]] if template.endswith('radio') else []")
s=s.replace("rng=random.Random(seed);sid=None;raw=False", "rng=random.Random(seed);sid=None;raw=False;cells=None")
s=s.replace("rng.choices(tuple(BANKS),weights=[len(eligible_positions(level,b)) for b in BANKS],k=1)[0]", "rng.choice(tuple(BANKS))")
a=s.index(' if parameters is None:\n  if sid:');b=s.index('\n# EASY:',a)
s=s[:a]+''' if not sid and template.endswith('radio'):
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
 # Output order must not signal which bank role was selected first.
 rng.shuffle(out)
 return out
''' +s[b:]
s=s.replace('records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]','records=[r for l in levels for r in generate_batch(l,args.seed,args.count,args.template,args.field_type,args.profile)]')
p.write_text(s)
# Keep the old eight source masks; add the missing observed case, not an older draft.
p=w/'17592186100990/source.json';d=json.loads(p.read_text())
source=json.loads((w.parent/'source/source.json').read_text())
q=next(q for q in source['material']['kp'][':knowledge-point/questions'] if q[':question/math-academy-id']=='q-139629')
d['record'][':knowledge-point/questions'].append(q)
p.write_text(json.dumps(d,indent=2)+'\n')
