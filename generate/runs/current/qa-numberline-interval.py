"""Root independent PNG endpoint readback and full set/bank/solution checks."""
import importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186059828;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_numberline_set',P/'interval-readback.py');g=module('root_numberline_gen',D.with_suffix('.py'));C=dict(records=0,raster_files=0,choices=0,whole_banks=0,actual_solution_sets=0,raw_evidence_records=0,source_prompts=0,source_values=0,source_banks=0,normal_scope_repairs=0)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']};records=[]
for case in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=r['question'];old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];assert sorted(z[':answer/value'] for z in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(z[':answer/value'] for z in old[':question/answer-fields'][0][':answer-field/choices']);C['source_prompts']+=1;C['source_values']+=5;C['source_banks']+=1;records.append(r)
 normal=g.generate('easy',parameters=case['normal_parameters'],profile=case['normal_profile']);records.append(normal);C['normal_scope_repairs']+=int(case['source_id']=='q-31762')
review=json.loads((D/'review.json').read_text());records +=[r for rows in review.values() for r in rows];records+=json.loads((P/'qa'/f'{K}-sampled.json').read_text())
# Re-detect circles/fill/ticks from actual PNGs, independently of cached detections.
fits={};cfg=[]
for r in records:
 path=re.search(r'!\[\]\((.*?)\)',r['question'][':question/problem'])[1]
 if path.startswith('images/'):
  path=str(Path('/media/jake/SSD/EDB/math')/path);anchors=([1,6],[25,271]) if 'a2e3d' in path else ([-3,3],[25,320]);fit=dict(anchor_values=anchors[0],anchor_pixels=anchors[1],tick_pixels=[25,74,123,172,221,271]+([] if 'a2e3d' in path else [320]))
 else:
  side=json.loads(Path(r['generation']['plots']['sidecar']).read_text());axis=side['axis_pixel_fit'];fit=dict(anchor_values=[0,1],anchor_pixels=[axis['origin_pixel'],axis['origin_pixel']+axis['pixels_per_unit']],tick_pixels=[])
 if path not in fits:fits[path]=fit;cfg.append(dict(path=path,fit=fit))
input_path=P/'qa'/f'{K}-raster-input.json';output_path=P/'qa'/f'{K}-raster-output.json';input_path.write_text(json.dumps(dict(output=str(output_path),cases=cfg)));subprocess.run([str(P.parents[2]/'.venv/bin/python'),str(D/'renderer.py'),'--readback',str(input_path)],check=True)
measurements={item['path']:item['measurement'] for item in json.loads(output_path.read_text())};C['raster_files']=len(measurements)
for r in records:
 q=r['question'];path=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1];path=str(Path('/media/jake/SSD/EDB/math')/path) if path.startswith('images/') else path
 m=measurements[path];a,b=[s.Rational(str(round(z*2)/2)) for z in m['endpoint_values']];assert all(abs(float(v)-z)<.025 for v,z in zip((a,b),m['endpoint_values']));lc,rc=m['closed'];target=s.Interval(a,b,left_open=not lc,right_open=not rc)
 f=q[':question/answer-fields'][0];vals=[p.meaning(z[':answer/value']) for z in f[':answer-field/choices']];assert len(set(vals))==len(vals)==5;good=[z[':answer/id'] for z,v in zip(f[':answer-field/choices'],vals) if v==target];assert len(good)==1
 raw=r['generation']['evidence_only'];profile=r['generation']['bank_profile'];base={s.Interval(a,b,left_open=L,right_open=R) for L in (False,True) for R in (False,True)}
 tick=s.Rational(r['generation']['parameters']['tick_step']);label=s.Rational(r['generation']['parameters']['label_step'])
 extra=s.Interval(-s.oo,b,right_open=False) if profile in ('raw_q28850','repair_q28850','observed_left_ray') else s.Interval(-a,b,left_open=True,right_open=True) if profile in ('raw_q31762','repair_q31762','observed_negate_left') else s.Interval(a-tick,b,left_open=not lc,right_open=not rc)
 assert set(vals)==base|{extra};C['whole_banks']+=1
 if raw:assert ':question/difficulty' not in q and ':question/worked-solution' not in q and ':answer-field/correct' not in f;C['raw_evidence_records']+=1
 else:
  assert lc!=rc and good==[f[':answer-field/correct'][1]];level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert a.is_Integer and b.is_Integer and -4<=a<b<=4 and b-a<=4 and tick==label==1
  elif level=='moderate':assert a.is_Integer and b.is_Integer and -6<=a<0 and b<=6 and 2<=b-a<=6 and (a%2 or b%2) and tick==1 and label==2
  else:assert -4<=a<0 and b<=4 and 1<=b-a<=4 and (a.q==2 or b.q==2) and tick==s.Rational(1,2) and label==1
  blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==2
  for z in blocks:assert p.meaning(z.replace(r"\lt", "<"))==target;C['actual_solution_sets']+=1
 C['records']+=1;C['choices']+=5
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
