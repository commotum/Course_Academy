"""Root reads actual linked graph data and contextual response independently."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186138429;D=R.parents[2]/f'generate/scratch/{K}'
spec=importlib.util.spec_from_file_location('root_contextual_graph_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Read directly from original captured PNGs, independently of generator metadata.
original={'cars':(80,s.Rational(-3,4),40,s.Rational(-1,4)), 'trucks':(0,50,750,-75),'pools':(150,50,775,-75)}
counts=dict(printed_instances=0,linked_plot_specs=0,source_banks=0,source_values=0,source_correct_refs_matched=0,source_missing_correct_derived=0,source_available_practice_solutions=0,complete_choices=0)
def check(r):
 q=r['question'];assets=r['generation']['plot_assets'];name=r['generation']['template'];expected_units={'cars':('Distance (m)','Speed (km/h)','meters'), 'trucks':('Hours','Miles','hours'),'pools':('Days','Liters','days')}[name]
 specs=[]
 for role,text in (('prompt',q[':question/problem']),('solution',q[':question/worked-solution'])):
  refs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text);assert len(refs)==1
  png=D/refs[0];assert png.is_file() and png==Path(assets[role]['path'])
  if assets[role]['renderer']=='captured PNG':
   v=assets[role]['geometry'];par=v['parameters'];assert tuple(s.Rational(par[k]) for k in ('a0','a1','b0','b1'))==original[name]
   captured=Path('/media/jake/SSD/EDB/math/images')/Path(refs[0]).relative_to('images');assert captured.is_file() and hashlib.sha256(captured.read_bytes()).digest()==hashlib.sha256(png.read_bytes()).digest()
  else:
   assert png.with_suffix('.json').is_file();v=json.loads(png.with_suffix('.json').read_text());par=v['parameters'];assert v['renderer']['matplotlib'] and v['renderer_revision']=='wordgraphs4'
   assert v['annotated']==(role=='solution')
   for key in ('a','b'):
    endpoints=v['plotted_line_endpoints'][key];assert endpoints[0]==[0,str(s.Rational(par[key+'0']))]
    assert s.Rational(endpoints[1][0])==s.Rational(par['xmax']) and s.Rational(endpoints[1][1])==s.Rational(par[key+'0'])+s.Rational(par[key+'1'])*s.Rational(par['xmax'])
   ticks=list(range(0,int(par['xmax'])+1,int(par['dx'])));assert v['grid_x_ticks']==ticks and v['numbered_x_ticks']==[x for x in ticks if x and x%int(par['xlabel_step'])==0]
  assert (v['labels']['x_label'],v['labels']['y_label'])==expected_units[:2];assert len(v['labels']['labels'])==2
  a,b,c,d=(s.Rational(par[k]) for k in ('a0','a1','b0','b1'));assert b!=d
  t=(c-a)/(b-d);y=a+b*t;assert (t,y)==tuple(map(s.Rational,v['intersection']))
  assert t.q==y.q==1 and 0<t<s.Rational(par['xmax']) and 0<y<s.Rational(par['ymax'])
  assert all(0<=v<s.Rational(par['ymax']) for v in (a,c,a+b*s.Rational(par['xmax']),c+d*s.Rational(par['xmax'])))
  if role=='solution':assert tuple(map(s.Rational,v['annotation_point']))==(t,y)
  specs.append((a,b,c,d,t,y));counts['linked_plot_specs']+=1
 assert specs[0]==specs[1];t,y=specs[0][-2:]
 points=re.findall(r'\$\((-?\d+),(-?\d+)\)\$',q[':question/worked-solution']);assert len(points)==1 and tuple(map(s.Integer,points[0]))==(t,y)
 assert expected_units[2] in q[':question/problem'] and expected_units[2] in q[':question/worked-solution']
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio'
 choices=f[':answer-field/choices'];assert len(choices)==5
 def value(raw):
  if name=='trucks':assert raw.endswith('h');raw=raw[:-1]
  return s.Rational(raw)
 vals=[value(a[':answer/value']) for a in choices];assert len(set(vals))==5 and all(v.q==1 and 0<v<=par['xmax'] for v in vals)
 selected=[i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1]];assert len(selected)==1 and vals[selected[0]]==t
 if r['generation']['bank_profile']=='adjacent_grid':
  dx=s.Rational(par['dx']);assert set(vals)=={t+k*dx for k in (-2,-1,0,1,2)}
 counts['printed_instances']+=1;counts['complete_choices']+=5;return vals
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'],q[':question/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case.get('source_ma_id',case['source_id'])];r=g.generate(case.get('level',case.get('difficulty')),template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile')));vals=check(r)
 assert old[':question/problem']==r['question'][':question/problem'];f=old[':question/answer-fields'][0]
 ov=[s.Rational(a[':answer/value'].removesuffix('h')) for a in f[':answer-field/choices']];assert sorted(ov)==sorted(vals)
 assert not f.get(':answer-field/correct') and not old.get(':question/worked-solution');counts['source_banks']+=1;counts['source_values']+=len(ov);counts['source_missing_correct_derived']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
