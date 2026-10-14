"""Root constant curl, actual rendered regions, every separate area component."""
import importlib.util,json,re,hashlib,itertools,sys
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186133886;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_greens_holes');x,y=p.x,p.y
def math(t):return p.scalar(t.strip().rstrip('.,'))
def eq(a,b):return s.expand(a-b)==0
def fields(body):
 body=body.replace('{∮}_{∂D}','').replace('∮_(∂D)','').replace(r'\,','').rstrip(',');terms=re.findall(r'([+-]?[^+-]*?)(dx|dy)',body);assert len(terms)==2;d={v:math(raw.strip() or '1') for raw,v in terms};return d['dx'],d['dy']
def polygon_area(vertices):return abs(s.Rational(1,2)*sum(s.Rational(str(a[0]))*s.Rational(str(b[1]))-s.Rational(str(b[0]))*s.Rational(str(a[1])) for a,b in zip(vertices,vertices[1:]+vertices[:1])))
C={n:0 for n in ('records','actual_P_Q','held_function_definitions','held_partial_values','displayed_curls','actual_region_components','individual_area_components','complete_arithmetic_rows','choices','whole_method_banks','source_sequences','raster_boundary_probes','orientation_arrows','hole_permutation_checks')}
def geometry(prompt):
 asset=Path(re.search(r'!\[\]\((.*?)\)',prompt)[1]);data=json.loads(asset.with_suffix('.json').read_text());assert data['png_sha256']==hashlib.sha256(asset.read_bytes()).hexdigest();boundaries=data['boundaries'];assert boundaries[0]['role']=='outer' and len(boundaries) in (2,3);areas=[]
 for b in boundaries:
  d=b['points'];areas.append(polygon_area(d['vertices']) if 'vertices' in d else s.pi*d['radius']**2/(2 if 'angle' in d else 1));assert b['orientation']==('counterclockwise' if b['role']=='outer' else 'clockwise')
  if 'angle' in d:assert d['angle']==[0,180] and d['diameter']==[[-d['radius'],0],[d['radius'],0]] and 'annular region' not in prompt
 O,holes=areas[0],areas[1:];assert O>sum(holes);C['actual_region_components']+=len(areas)
 pixels=np.array(Image.open(asset).convert('RGB'));height=pixels.shape[0];origin,ux,uy=np.array(data['axes_transform']);sx=ux[0]-origin[0];sy=uy[1]-origin[1];assert abs(sx-sy)<1e-8;orange=(pixels[:,:,0]>160)&(pixels[:,:,1]>80)&(pixels[:,:,1]<200)&(pixels[:,:,2]<70)
 def hit(pt):
  px,py=int(round(origin[0]+pt[0]*sx)),int(round(height-origin[1]-pt[1]*sy));assert orange[max(0,py-4):py+5,max(0,px-4):px+5].any();C['raster_boundary_probes']+=1
 for b in boundaries:
  d=b['points']
  if 'vertices' in d:
   for a,c in zip(d['vertices'],d['vertices'][1:]+d['vertices'][:1]):
    for f in (.2,.5,.8):hit(np.array(a)+f*(np.array(c)-a))
  else:
   center=np.array(d['center']);radius=d['radius'];angles=(20,50,110,160) if 'angle' in d else (20,70,140,210,300)
   for a in angles:hit(center+radius*np.array([np.cos(np.deg2rad(a)),np.sin(np.deg2rad(a))]))
   if 'diameter' in d:
    for f in (-.8,.3,.8):hit(center+np.array([f*radius,0]))
 for a in data['arrows']:
  tail,tip=np.array(a['tail']),np.array(a['tip']);role=a['role'];shape=data['shape']
  if shape in ('annulus','semicircle','two_circles'):
   centers=[b['points']['center'] for b in boundaries if b['role']==role];c=min(centers,key=lambda c:np.linalg.norm(tail-c));v=tail-c;delta=tip-tail;cross=v[0]*delta[1]-v[1]*delta[0];assert cross>0 if role=='outer' else cross<0
  elif role=='hole':assert tip[0]>tail[0] and tip[1]==tail[1]
  elif shape=='diamond':assert all(tip>tail)
  else:assert tip[0]>tail[0] and tip[1]==tail[1]
  C['orientation_arrows']+=1
 return O,holes
def check(rec,old):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];P,Q=fields(re.search(r'Calculate \$(.*?)\$',prompt,re.S)[1]);a,b=s.diff(P,y),s.diff(Q,x);curl=b-a;O,holes=geometry(prompt);A=O-sum(holes);answer=curl*A;C['actual_P_Q']+=2
 defs=re.search(r'P\(x,y\)=(.*?)\$ and \$Q\(x,y\)=(.*?)\.\$',sol);assert defs and eq(math(defs[1]),P) and eq(math(defs[2]),Q);C['held_function_definitions']+=2
 derivatives=re.search(r'\\frac\{∂P\}\{∂y\}=(.*?),\\,\\frac\{∂Q\}\{∂x\}=(.*?)\.',sol);assert derivatives and eq(math(derivatives[1]),a) and eq(math(derivatives[2]),b);C['held_partial_values']+=2
 chain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1];lhs,*rr=chain.split(' & =');rr=[t.split(chr(92)*2)[0].strip() for t in rr];lhs=lhs.strip();assert fields(lhs)==(P,Q);assert rr[0]==r'{∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A'
 difference=rr[1].removeprefix(r'{∬}_{D}').removesuffix(r'\,\text{d}A');assert eq(math(difference),curl);C['displayed_curls']+=1
 for row in rr[2:]:
  if r'{∬}_{D}' in row:
   before,after=row.split(r'{∬}_{D}');after=after.removesuffix(r'\,\text{d}A');coef=math(before) if before not in ('','-') else -1 if before=='-' else 1;body=math(after) if after else 1;value=coef*body*A
  else:value=math(row.replace(r'\text{Area}(D)','('+s.latex(A)+')'))
  assert eq(value,answer);C['complete_arithmetic_rows']+=1
 geometric=next(t for t in rr[2:] if '^{2}' in t or r'\frac{' in t and r'\cdot' in t);inside=re.findall(r'\(([^()]*)\)',geometric);inside=inside[-1] if inside else geometric;components=inside.split('-');assert len(components)==1+len(holes)
 for t,val in zip(components,[O,*holes]):assert eq(math(t),val);C['individual_area_components']+=1
 if family not in ('annulus_positive','circle_semicircle'):
  collected=rr[rr.index(geometric)+1];inside=re.findall(r'\(([^()]*)\)',collected);inside=inside[-1] if inside else collected;components=inside.split('-');assert len(components)==1+len(holes)
  for t,val in zip(components,[O,*holes]):assert eq(math(t),val);C['individual_area_components']+=1
 choices=q[':question/answer-fields'][0][':answer-field/choices'];values=[math(a[':answer/value']) for a in choices];assert len(values)==5 and len(set(values))==5;assert [a[':answer/id'] for a,v in zip(choices,values) if eq(v,answer)]==[q[':question/answer-fields'][0][':answer-field/correct'][1]]
 if rec['generation']['profile']=='constant_operations':want=[answer,-answer,curl*O,curl*sum(holes),curl*(O+sum(holes))]
 elif rec['generation']['profile']=='semicircle_operations':want=[answer,-answer,curl*O,curl*(O-2*holes[0]),curl*(O+holes[0])]
 elif rec['generation']['profile']=='two_hole_operations':want=[answer,-answer,curl*(O-holes[0]),curl*(O-holes[1]),curl*(O+sum(holes))]
 else:want=[answer,-answer,curl*O,curl*(O+sum(holes)),b*A]
 assert all(sum(eq(v,w) for w in want)==1 for v in values);C['choices']+=5;C['whole_method_banks']+=1
 if old and ':question/worked-solution' in old:
  original=old[':question/worked-solution'];oldchain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',original,re.S)[1];assert chain.count(' & =')==oldchain.count(' & =');prose=lambda t:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',t,flags=re.S)).strip();assert prose(sol)==prose(original);C['source_sequences']+=1
 C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'parent_greens_generator');frozen=json.load(open(R/f'sources/{K}.json'));assert json.load(open(D/'source.json'))==frozen;originals={q[':question/math-academy-id']:q for q in frozen['record'][':knowledge-point/questions']};S=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,unrated=0)
 for case in json.load(open(D/'source-cases.json')):
  o=originals[case['source_id']];q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];assert q[':question/problem']==o[':question/problem'];assert (':question/worked-solution' in q)==(':question/worked-solution' in o) and (':question/difficulty' in q)==(':question/difficulty' in o);S['prompts']+=1;S['unrated']+=(':question/difficulty' not in o)
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];S['solutions']+=1
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);S['fields']+=1;S['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];S['refs']+=1
   else:S['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for family,c in g.SPECS.items():records.extend(g.generate(c['level'],seed=seed,template=family) for seed in (631,917))
 for rec in records:check(rec,originals.get(g.SPECS[rec['generation']['template']].get('source')))
 for family,names in [('circle_two_holes',('r','t')),('rectangle_two_holes',('s','t'))]:
  params=g.parameters_for(family);swapped=params|dict(zip(names,reversed([params[n] for n in names])));a=g.generate_hard(template=family,parameters=params);b=g.generate_hard(template=family,parameters=swapped);assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id'];C['hole_permutation_checks']+=1
 out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
