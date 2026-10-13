#!/usr/bin/env python3
"""Identify y=b^x+c from five graph choices; basis 1356. No database writes.
API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), plus generate_easy/moderate/hard. CLI below.
Observed complete banks are evidence profiles: exact labelled geometry is known,
but unlabelled horizontal scaling does not establish the original exponential
base. Default authored banks use the source recognition method. Whole bank is
selected before parameters and rejected as a unit on collision.
"""
from __future__ import annotations
import argparse,hashlib,json,random,uuid,sys,subprocess,tempfile,os
from pathlib import Path
import sympy as sp
KP_ID=17592186087821
KP_UUID='dd63cb30-a236-546e-82ac-08bce09c88f7'
TITLE='Identifying a Vertically Shifted Exponential Growth Curve'
VERSION='vertical-growth-7'
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
RUNTIME='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
# Every original option, in capture order: amplitude, asymptote, exponent direction.
# These are labelled geometric observations; historical error intent is unknown.
OBS={
 'q-25154':('8','1/2',[(sp.Rational(1,2),1,1),(2,-sp.Rational(1,2),1),(1,sp.Rational(3,2),1),(1,sp.Rational(1,2),1),(1,-sp.Rational(3,2),1)]),
 'q-25292':('5','-2',[(1,1,1),(1,-1,1),(-3,2,1),(1,-2,1),(-1,0,1)]),
 'q-170588':('3/2','3/2',[(sp.Rational(1,2),1,1),(sp.Rational(3,2),0,1),(sp.Rational(3,2),1,1),(1,sp.Rational(3,2),1),(sp.Rational(3,2),sp.Rational(3,2),1)]),
 'q-170590':('5/3','1',[(sp.Rational(5,3),0,1),(sp.Rational(8,3),0,1),(sp.Rational(5,3),1,1),(1,1,1),(sp.Rational(2,3),1,1)]),
 'q-26810':('3','7/2',[(1,sp.Rational(7,2),-1),(8,-sp.Rational(7,2),1),(1,1,1),(1,-sp.Rational(7,2),1),(1,sp.Rational(7,2),1)]),
 'q-26811':('7','4',[(1,-4,1),(5,0,1),(2,-4,1),(1,4,-1),(1,4,1)]),
 'q-26815':('6','-3/4',[(1,sp.Rational(3,4),1),(1,-sp.Rational(3,4),-1),(1,-sp.Rational(3,4),1),(1,sp.Rational(1,2),1),(sp.Rational(3,4),-sp.Rational(1,2),1)])}
AUTHORED=('authored_transformations','authored_offsets')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,v))
def tex(v,decimal=False):
 v=sp.Rational(v)
 if decimal and v.q!=1:return str(float(v)).rstrip('0').rstrip('.')
 return sp.latex(v)
def expression(b,c,style='integer'):
 base=tex(b)
 power=('{('+base+')}^{x}' if b.q!=1 else '{'+base+'}^{x}')
 if style=='legacy':power=base+'^{x}'
 return power+('+' if c>=0 else '-')+tex(abs(c),style in ('decimal','legacy'))
def values(level):
 bases=[sp.Rational(k) for k in range(2,10)] if level=='easy' else sorted({sp.Rational(p,q) for q in (2,3,4) for p in range(q+1,10) if sp.Rational(p,q).q!=1})
 shifts=([sp.Rational(k,4) for k in range(-16,17) if k] if level=='easy' else [sp.Rational(k,2) for k in range(-8,9) if k] if level=='moderate' else sorted({sp.Rational(k,d) for d in (3,4) for k in range(-3*d,3*d+1) if sp.Rational(k,d).q in (3,4)}))
 return bases,shifts

def validate_parameters(level,p,observed=False):
 if set(p)!={'b','c'}:raise ValueError('Parameters must contain exactly b and c')
 b,c=sp.Rational(p['b']),sp.Rational(p['c'])
 if not observed and (b not in values(level)[0] or c not in values(level)[1]):raise ValueError('Parameters outside documented level workload bounds')
 if observed and not (1<b<=9 and b.q<=4 and abs(c)<=4 and c.q<=4 and c!=0):raise ValueError('Observed extension workload bounds')
 return b,c

def render_plots(specs):
 (HERE/'plots').mkdir(exist_ok=True)
 pending=[]
 for item in specs:
  path=Path(item['path']);side=path.with_suffix('.json')
  try:
   cache=json.loads(side.read_text())
   valid=cache['version']=='shift-plots-7' and cache['spec']==item and cache['png_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
  except (OSError,ValueError,KeyError):valid=False
  if not valid:pending.append(item)
 if not pending:return
 fd,tmp=tempfile.mkstemp(dir=HERE,suffix='.render-input.json');os.close(fd)
 try:
  Path(tmp).write_text(json.dumps(pending));subprocess.run([RUNTIME,str(HERE/'render.py'),tmp],check=True)
 finally:Path(tmp).unlink(missing_ok=True)

def plot(b,A,c,direction,cue,grid,ylim,decimal=False):
 data={'b':str(b),'A':str(A),'c':str(c),'direction':direction,'cue':cue,'grid':str(grid),'ylim':ylim,'intercept_tex':'(0,'+tex(A+c,decimal)+')','shift_tex':tex(c,decimal),'renderer_version':'shift-plots-7'}
 path=HERE/'plots'/('plot-'+digest(data)+'.png');return {**data,'path':str(path)}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio field supported')
 if template not in (None,'identify_shifted_growth'):raise ValueError('Unknown template')
 rng=random.Random(seed);profile=profile or rng.choice(AUTHORED) # Complete bank first.
 observed=profile.startswith('observed:');sid=profile.split(':',1)[1] if observed else None
 if observed and sid not in OBS:raise ValueError('Unknown observed bank')
 if not observed and profile not in AUTHORED:raise ValueError('Unknown bank')
 src=QUESTIONS[sid] if observed else None
 rawlevel=src.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] if src else ''
 if rawlevel and rawlevel!=level:raise ValueError('Observed label mismatch')
 explicit=parameters is not None
 if parameters is None:parameters={'b':OBS[sid][0],'c':OBS[sid][1]} if observed else {'b':str(rng.choice(values(level)[0])),'c':str(rng.choice(values(level)[1]))}
 if not observed and not explicit:
  # Reject a whole candidate parameter set, retaining the chosen bank.
  while profile=='authored_offsets' and sp.Rational(parameters['c']) in (sp.Rational(1,2),-sp.Rational(1,2),1,-1):
   parameters={'b':str(rng.choice(values(level)[0])),'c':str(rng.choice(values(level)[1]))}
 b,c=validate_parameters(level,parameters,observed)
 baseline=observed and (b,c)==tuple(map(sp.Rational,OBS[sid][:2]))
 if observed:
  # Parameterized labelled-feature continuation: amplitude ratios and asymptote
  # offsets are anchored to each source's labelled geometry. Not inferred intent.
  oldb,oldc=map(sp.Rational,OBS[sid][:2]);bank=[(sp.Rational(A),c+(sp.Rational(C)-oldc),D) for A,C,D in OBS[sid][2]]
 else:
  bank=([(1,c,1),(1,-c,1),(1,c,-1),(1,0,1),(b,c,1)] if profile=='authored_transformations' else [(1,c,1),(1,-c,1),(1,c+1,1),(1,c-1,1),(1,0,1)])
 # All complete required members must be distinct. No option replacement.
 if len(set(bank))!=5 or sum(t==(1,c,1) for t in bank)!=1:
  if parameters is not None:raise ValueError('Whole bank rejected: equivalent options')
 cue='grid' if level=='hard' and not observed else 'labels';grid=sp.Rational(1,c.q) if cue=='grid' else sp.Integer(1)
 ymin=float(min([0]+[C for A,C,D in bank]+[A+C for A,C,D in bank]))-1.5
 ymax=float(max([0]+[C for A,C,D in bank]+[A+C for A,C,D in bank]))+3
 ylim=[ymin,ymax];specs=[plot(b,A,C,D,cue,grid,ylim,decimal=level=='easy') for A,C,D in bank]
 paths=[s['path'] for s in specs]
 if baseline:paths=[a[':answer/value'] for a in src[':question/answer-fields'][0][':answer-field/choices']]
 else:render_plots(specs)
 style=('legacy' if sid in ('q-25154','q-25292') else 'decimal' if sid in ('q-26810','q-26815') else 'decimal' if level=='easy' and not observed else 'integer')
 eq=expression(b,c,style);base=eq.split('^{x}')[0]+'^{x}'
 prompt='Which of the following is the graph of $y='+eq+'?$'
 if style=='legacy':prompt='Which of the following is the graph of $y = '+tex(b)+'^{x} '+('+' if c>0 else '-')+' '+tex(abs(c),True)+'$?'
 unshift=plot(b,1,0,1,'labels',1,[-1.5,4.5]);unshift['role']='original';unshift['marker_color']='#ffae18'
 shifted=plot(b,1,c,1,'labels',1,ylim,decimal=level=='easy');shifted['role']='translation';shifted['arrow_x']=-3.5
 for item in (unshift,shifted):item['path']=str(HERE/'plots'/('plot-'+digest({k:v for k,v in item.items() if k!='path'})+'.png'))
 solpaths=[unshift['path'],shifted['path']]
 if baseline and ':question/worked-solution' in src:
  import re
  solpaths=re.findall(r'!\[\]\((.*?)\)',src[':question/worked-solution'])
 elif not observed or ':question/worked-solution' in src:render_plots([unshift,shifted])
 amount=tex(abs(c),style=='decimal');units='unit' if abs(c)==1 else 'units'
 solution=f'First, we plot the graph of $y={base}:$\n\n![]({solpaths[0]})\n\nTo sketch the graph of $y={eq},$ we take the graph of $y={base}$ and shift it ${amount}$ {units} '+('up' if c>0 else 'down')+f'. The $y$-intercept moves from $(0,1)$ to $(0,{tex(1+c,style=="decimal")}),$ and the horizontal asymptote moves from $y=0$ to $y={tex(c,style=="decimal")}.$\n\n![]({solpaths[1]})'
 # All five choices share the growth base; its magnitude changes appearance,
 # not the discriminating translation/orientation operation. Do not inflate
 # finite task counts by that presentation parameter.
 mathematical={'c':str(c),'cue':cue,'grid':str(grid) if cue=='grid' else None}
 q={':question/problem':prompt}
 if not observed or ':question/difficulty' in src:q[':question/difficulty']=':question.difficulty/'+level
 if not observed or ':question/worked-solution' in src:q[':question/worked-solution']=solution
 content=digest({'version':VERSION,'level':level,'prompt':prompt,'solution':q.get(':question/worked-solution'),'bank':sorted(paths),'mathematics':mathematical,'raw_presence':sorted(q)})
 qid=ident(content);fid=ident(content+'/selection');choices=[]
 for i,path in enumerate(paths):choices.append({':answer/id':ident(content+'/selection/'+path),':answer/type':':answer.type/image',':answer/value':path})
 correct=choices[bank.index((1,c,1))][':answer/id'];rng.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if not observed or ':answer-field/correct' in src[':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',correct]
 q.update({':question/id':qid,':question/answer-fields':[field]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'difficulty':level,'template':'identify_shifted_growth','bank_profile':profile,'parameters':{'b':str(b),'c':str(c)},'mathematical_fingerprint':digest(mathematical),'content_identity':content,'source_id':sid,'source_provenance':{k:SOURCE[k] for k in ('database','basis','lineage')},'evidence_only':observed,'eligible_for_learning':not observed,'inferred_correct_answer_id':correct if observed and ':answer-field/correct' not in field else None,'geometry':[dict(s,path=p) for s,p in zip(specs,paths)],'domain':'x in R; b>1; unscaled target b^x+c','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# EASY — observed integer growth bases and signed quarter-unit shifts; labelled
# asymptote/intercept reading, one vertical translation. No stretched target.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE — observed proper rational growth base >1, signed half-unit shifts;
# same translation plus rational-number recognition, no extra mathematical branch.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)

# HARD (authored missing level) — same unscaled growth curve, fractional third or
# quarter shift read from subdivided numbered axes without coordinate labels.
# No solving unknown c/k; this KP only selects the graph of the supplied equation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];meta=r['generation'];field=q[':question/answer-fields'][0]
 cid=field.get(':answer-field/correct',[None,meta.get('inferred_correct_answer_id')])[1]
 kind='ORIGINAL REPLAY' if meta['evidence_only'] and meta['parameters']==dict(zip(('b','c'),OBS[meta['source_id']][:2])) else 'GENERATED VARIANT'
 actual=q.get(':question/difficulty','unrated original; authored '+meta['difficulty']+' routing').split('/')[-1]
 out='### '+kind+' — '+actual+' — '+meta['bank_profile']+'\n\n'+q[':question/problem']+'\n\n'
 for i,a in enumerate(field[':answer-field/choices']):
  marker=' **CORRECT**' if a[':answer/id']==cid and ':answer-field/correct' in field else ' **INFERRED CORRECT; original designation absent**' if a[':answer/id']==cid else ''
  out+=f'{i+1}.{marker} ![]({a[":answer/value"]})\n\n'
 return out+q.get(':question/worked-solution','[Original source has no worked solution.]')
def review_manifest():
 runtime_path=HERE/'renderer-runtime.json'
 return {'version':VERSION,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256((HERE/'render.py').read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':sp.__version__,'renderer_runtime':json.loads(runtime_path.read_text()) if runtime_path.exists() else {'status':'not invoked in this review; original assets reused'}}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 rows=[]
 for level in ('easy','moderate','hard') if args.difficulty=='all' else [args.difficulty]:
  for i in range(args.count):
   # Deterministic whole-instance retries after complete bank selection.
   for attempt in range(100):
    try:r=generate(level,args.seed+i+attempt*1009,args.template,profile=args.profile);break
    except ValueError:
     if args.profile and args.profile.startswith('observed:'):raise
   else:raise ValueError('No eligible whole instance')
   rows.append(r)
 manifest=review_manifest()
 for r in rows:r['generation']['review_manifest']=manifest
 print(json.dumps(rows,indent=2) if args.format=='json' else '## Generator review manifest\n\n'+json.dumps(manifest,indent=2)+'\n\n'+'\n\n'.join(markdown(r) for r in rows))
if __name__=='__main__':main()
