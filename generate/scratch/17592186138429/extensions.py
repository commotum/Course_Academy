"""Additional easy source templates captured by math basis 2019.

Observed plane bank uses exact scalar replay expressions, without inferring
original error intent. Normal variants use a complete adjacent-grid bank.
Tank blanks preserve field-1, numeric minutes, and the source solution sequence.
"""
from types import SimpleNamespace
import json, random, uuid
import sympy as sp
PARAMS={
 'planes':dict(a0=4,a1='4/3',b0=0,b1='5/3',xmax=24,dx=3,ymax=36,dy=4,ylabel_step=4,xlabel_step=3),
 'tanks':dict(a0=25,a1='-5/2',b0=5,b1='5/2',xmax=7,dx=1,ymax=35,dy=5,ylabel_step=5,xlabel_step=1)}
CONFIG={
 'planes':dict(x_label='Minutes',y_label='Feet (thousands)',labels=['Airplane A','Airplane B']),
 'tanks':dict(x_label='Minutes',y_label='Liters',labels=['Tank A','Tank B'])}
SOURCE_IDS={'planes':'q-102519','tanks':'q-237989'}
def generate(namespace,level,seed,name,field_type=None,parameters=None,profile=None):
 g=SimpleNamespace(**namespace)
 if level!='easy':raise ValueError('New source templates support easy only')
 expected='radio' if name=='planes' else 'blank'
 if field_type not in (None,expected,':answer-field.type/'+expected):raise ValueError('Preserve source field type')
 profile=profile or ('adjacent_grid' if name=='planes' else 'blank')
 if profile not in (('adjacent_grid','observed_plane_expressions') if name=='planes' else ('blank',)):raise ValueError('Unsupported source bank')
 rng=random.Random(seed)
 if parameters is not None:p=g.normalize(parameters)
 elif profile=='observed_plane_expressions':p=g.normalize(PARAMS[name])
 elif name=='planes':
  t=rng.choice([9,12,15,18]);b=rng.choice([sp.Rational(4,3),sp.Rational(5,3),2]);gap=rng.choice([sp.Rational(1,3),sp.Rational(2,3)])
  p=g.normalize(dict(a0=gap*t,a1=b-gap,b0=0,b1=b,xmax=t+9,dx=3,ymax=4*(int(b*(t+9)/4)+2),dy=4,ylabel_step=4,xlabel_step=3))
 else:
  t=rng.randint(2,6);rate=rng.choice([sp.Rational(5,2),5]);b0=rng.choice([0,5,10]);a0=b0+2*rate*t;xmax=t+2
  p=g.normalize(dict(a0=a0,a1=-rate,b0=b0,b1=rate,xmax=xmax,dx=1,ymax=5*(int(max(a0,b0+rate*xmax)/5)+2),dy=5,ylabel_step=5,xlabel_step=1))
 r={k:sp.Rational(v) for k,v in p.items()};t,y=g.derive(p)
 original=p==g.normalize(PARAMS[name])
 if t.q!=1 or y<=0 or not 0<t<r['xmax'] or not 0<y<r['ymax']:raise ValueError('Visible positive integer time intersection required')
 if any(r[k]<=0 or r[k].q!=1 for k in ('xmax','dx','ymax','dy','xlabel_step','ylabel_step')):raise ValueError('Positive integer grid required')
 if any(r[k]%r['dx'] for k in ('xmax','xlabel_step')) or r['ymax']%r['dy'] or r['ylabel_step']%r['dy']:raise ValueError('Integral grid required')
 if t%r['dx'] or r['xlabel_step']!=r['dx']:raise ValueError('Easy directly numbered ticks')
 if name=='planes':
  if r['a0']<=0 or r['b0']!=0 or not 0<r['a1']<r['b1'] or r['dx']!=3 or r['dy']!=4:raise ValueError('Airplane scope')
  vals=([3*t/4,5*t/3,t,5*t/4,4*t/3] if profile=='observed_plane_expressions' else [t,t-6,t-3,t+3,t+6])
  if len(set(vals))!=5 or any(v.q!=1 or not 0<v<=r['xmax'] for v in vals):raise ValueError('Invalid complete bank')
 else:
  if r['a0']<=r['b0'] or r['b0']<0 or r['a1']!=-r['b1'] or r['a1']>=0 or r['dx']!=1 or r['dy']!=5:raise ValueError('Conserved transfer scope')
  vals=[t]
 if not original and any(not 0<=r[k+'0']+r[k+'1']*r['xmax']<r['ymax'] for k in ('a','b')):raise ValueError('Nonnegative physical segments')
 source=json.loads((g.HERE/'source-current.json').read_text())
 sq=next(q for q in source['record'][':knowledge-point/questions'] if q[':question/math-academy-id']==SOURCE_IDS[name])
 # Use shared renderer without changing the generator's globally cached configs.
 local=dict(namespace);local['CONFIG']={**g.CONFIG,name:CONFIG[name]};local['SOURCE_PARAMETERS']={**g.SOURCE_PARAMETERS,name:PARAMS[name]};local['ORIGINAL_ASSETS']={**g.ORIGINAL_ASSETS,name:sq[':question/problem'].split('![](')[1].split(')')[0]}
 import types
 renderer=types.FunctionType(g.render_plots.__code__,local)
 assets=renderer(name,p)
 prompt='![]('+assets['prompt']['reference']+')'+sq[':question/problem'].split(')',1)[1]
 graph='![]('+assets['solution']['reference']+')'
 if name=='planes':worked='Here, we need to find the point of intersection of the two graphs.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y}).$ So, it takes ${t}$ minutes for both planes to get to the same altitude (of ${int(y)*1000:,}\\,\\text{{ft}}$).'
 else:worked='The tanks contain the same amount when the two graphs intersect.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y}).$ So, the tanks contain the same amount (${y}\\,\\text{{L}}$) of water after $t={t}$ minutes.'
 values=list(map(str,vals));content=g.digest(dict(version=g.VERSION,prompt=prompt,solution=worked,bank=sorted(values)))
 qid=uuid.uuid5(uuid.NAMESPACE_URL,g.KP_UUID+'/'+content);key='selection' if name=='planes' else 'field-1';fid=uuid.uuid5(qid,key)
 choices=[{':answer/id':str(uuid.uuid5(fid,'math:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values];rng.shuffle(choices)
 return {'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':'Word Problems'},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/easy',':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':key,':answer-field/type':':answer-field.type/'+expected,':answer-field/choices':choices,':answer-field/correct':[':answer/id',str(uuid.uuid5(fid,'math:'+str(t)))]}]},'generation':{'version':g.VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':'observed expressions; intent unknown' if profile=='observed_plane_expressions' else 'authored adjacent grid' if name=='planes' else 'source blank','level_origin':'observed easy','source_analysis':{'database':'math','basis':2019,'lineage':g.SOURCE['lineage']},'source_reference':SOURCE_IDS[name],'parameter_fingerprint':g.digest({'context':name,'lines':[[p['a0'],p['a1']],[p['b0'],p['b1']]],'response':'horizontal coordinate','horizontal_grid':[p['dx'],p['xlabel_step']]}),'content_fingerprint':content,'plot_rating':'moderate','plot_assets':assets,'sympy_version':sp.__version__}}
