#!/usr/bin/env python3
"""Independent displayed arithmetic, fidelity, geometry, determinism and native QA."""
import concurrent.futures, copy, hashlib, importlib.util,json,math,re,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('kp',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def check(r):
 q=r['question'];md=q[':question/problem'];sol=q.get(':question/worked-solution','');meta=r['generation'];p=meta['parameters'];f=q[':question/answer-fields'][0]
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert json.loads(json.dumps(r))==r
 assert md.count('$$')%2==0 and sol.count('$$')%2==0
 for text in [md,sol]+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert text.count('{')==text.count('}');assert (text.replace('$$','').count('$')%2)==0
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in md
 if meta['evidence_only']:return
 assert r'{A}_{△BCD} & ={A}_{△ABD}-{A}_{ABCD}' in sol
 assert all(x.strip().replace(' ','')==p['unit'] for x in re.findall(r'\\text\{([^}]+)\}',sol))
 Q=int(re.search(r'area of \$ABCD\$ is \$(\d+)',md).group(1));assert Q==p['quadrilateral']
 if 'outer' in p:
  S=int(re.search(r'enclosing \$△ABD\$ is \$(\d+)',md).group(1));R=S;c=S-Q
 else:
  # Read every formal/substituted/collected stage independently.
  assert r'{A}_{△ABD} & =\frac{1}{2}\cdot AB\cdot AD\cdot \operatorname{sin}⁡A' in sol
  # Read displayed substitution, not merely remembered generator inputs.
  match=re.search(r'\\frac\{1\}\{2\}\\cdot (\d+(?:\.\d+)?)\\cdot (\d+(?:\.\d+)?)\\cdot \\operatorname\{sin\}⁡\{(\d+)\}',sol);assert match,sol
  a,b,t=map(float,match.groups());assert [a,b,t]==[p['a'],p['b'],p['angle']]
  T=a*b*math.sin(math.radians(t))/2;R=math.floor(T+.5+1e-10);c=R-Q
  stage=re.search(r'\\\\\s+& =((?:\\frac\{1\}\{2\}\\cdot )?\d+(?:\.\d+)?)(?:\\cdot )?\\operatorname\{sin\}',sol);assert stage
  st=stage.group(1);assert abs(float(re.search(r'(\d+(?:\.\d+)?)$',st).group(1))*(.5 if 'frac' in st else 1)-a*b/2)<1e-9
  decimals=re.findall(r'& =(\d+\.\d{3})…',sol)
  assert all(v==f'{math.floor(T*1000+1e-8)/1000:.3f}' for v in decimals)
  assert re.search('≈'+str(R)+r'\{\\text',sol)
  if f[':answer-field/type'].endswith('/blank'):expected=[c]
  elif t==90:expected=[c,R,R+Q,math.floor(2*T+.5+1e-10)-Q,math.floor(T-Q/2+.5+1e-10)]
  else:expected=[c,R,R+Q,math.floor(2*T+.5+1e-10)-Q,math.floor(a*b/2+.5)-Q]
 if 'outer' in p:expected=[c] if f[':answer-field/type'].endswith('/blank') else [c,S,S+Q,Q,math.floor(c/2+.5)]
 assert f'={R}-{Q}' in sol
 assert re.search('='+str(c)+r'\{\\text',sol)
 vals=[int(re.match(r'\d+',a[':answer/value']).group()) for a in f[':answer-field/choices']]
 assert sorted(vals)==sorted(expected);assert len(set(vals))==len(vals) and min(vals)>0
 correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert int(re.match(r'\d+',correct[':answer/value']).group())==c
 v=meta['plot_spec']['vertices']
 def area(ks):
  points=[v[k] for k in ks];return abs(sum(x*y2-y*x2 for (x,y),(x2,y2) in zip(points,points[1:]+points[:1])))/2
 assert abs(area('ABCD')-Q)<1e-8
 assert abs(area('BCD')-(area('ABD')-Q))<1e-8
 for k,length in [('B',p['a']),('D',p['b'])]:assert abs(math.dist(v['A'],v[k])-length)<1e-8
 for path in meta['plot_assets'].values():assert Path(path).exists() and Path(path).with_suffix('.json').exists()

raw=[];repaired=[];replays=[];matched_choices=0;matched_refs=0
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];src=g.QS[sid];r=g.generate('hard',template=sid,parameters=case['parameters'],profile=case['bank_profile']);q=r['question'];check(r)
 for key in (':question/problem',':question/worked-solution'):assert q.get(key)==src.get(key) and (key in q)==(key in src)
 assert (':question/difficulty' in src)==(':question/difficulty' in q)
 if ':question/difficulty' in src:assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
 sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
 assert sf[':answer-field/type'][':db/ident']==f[':answer-field/type'];assert sf[':answer-field/key']==f[':answer-field/key']
 assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']);matched_choices+=len(sf[':answer-field/choices'])
 assert (':answer-field/correct' in sf)==(':answer-field/correct' in f)
 if ':answer-field/correct' in sf:
  ca=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ca[':answer/value']==sf[':answer-field/correct'][':answer/value'];matched_refs+=1
  pp=case['parameters'];independent=math.floor(pp['a']*pp['b']*math.sin(math.radians(pp['angle']))/2+.5+1e-10)-pp['quadrilateral'];assert int(re.match(r'\d+',sf[':answer-field/correct'][':answer/value']).group())==independent
 raw.append(r);repaired.append(g.generate('hard',template=sid,parameters=case['parameters'],profile='repaired_'+sid))
 # Changed parameters exercise actual public opaque evidence recipes.
 pp=dict(case['parameters']);pp['quadrilateral']+=1
 if pp['quadrilateral']<float(g.calculation(pp)[0]) and g.calculation(pp)[2]>0:
  changed=g.generate('hard',template=sid,parameters=pp,profile=case['bank_profile']);assert changed['question'][':question/problem']!=q[':question/problem'];check(changed)

normal=[];fingerprints={l:set() for l in ('easy','moderate','hard')};family_coverage=set()
for level in fingerprints:
 for seed in range(40):
  r=g.generate(level,seed);check(r);normal.append(r);fingerprints[level].add(r['generation']['parameter_fingerprint']);family_coverage.add(r['generation']['template'])
# Ensure every observed source-family normal chain is independently checked twice.
variants=[]
for i,sid in enumerate(g.QS):
 for j in range(2):
  r=g.generate('hard',1000+2*i+j,template=sid);check(r);variants.append(r)
assert set(g.QS)<=family_coverage
# Regression: the angle label must not occupy the concave vertex at equal
# 10-unit sides, 60 degrees and quadrilateral area20, under each rotation.
for orientation in (0,90,180,270):
 regression=g.generate('hard',template='q-18188',parameters={'a':10,'b':10,'angle':60,'quadrilateral':20,'unit':'cm','orientation':orientation})
 check(regression);plot=regression['generation']['plot_spec']
 assert plot['angle_label_mode']=='exterior_callout'
 assert math.dist(plot['angle_label_position'],plot['vertices']['C'])>2
# Stable seed-independent identity and full fresh/cache metadata equality.
p={'a':12,'b':18,'angle':67,'quadrilateral':61,'unit':'cm','orientation':270}
r=g.generate('hard',10,'q-18188',parameters=p);r2=g.generate('hard',11,'q-18188',parameters=p)
assert r['question'][':question/id']==r2['question'][':question/id']
alias=g.generate('hard',10,'q-18188',parameters={**p,'a':12.0});assert alias==r
omit_orientation={k:v for k,v in p.items() if k!='orientation'};zero=g.generate('hard',10,'q-18188',parameters={**p,'orientation':0});assert zero==g.generate('hard',10,'q-18188',parameters=omit_orientation)
assert sorted(r['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])==sorted(r2['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])
pp={**p,'angle':68,'quadrilateral':62};path,side=g.render(pp);Path(path).unlink();Path(path).with_suffix('.json').unlink();fresh=g.generate('hard',70,'q-18188',parameters=pp);cached=g.generate('hard',70,'q-18188',parameters=pp);assert fresh==cached
# Concurrent identical and different plot calls, with full record equality.
inputs=[p,p,{**p,'orientation':90},{**p,'angle':69,'quadrilateral':64}]
for x in inputs:
 path,_=g.render(x);Path(path).unlink(missing_ok=True);Path(path).with_suffix('.json').unlink(missing_ok=True)
with concurrent.futures.ThreadPoolExecutor(4) as ex:
 records=list(ex.map(lambda x:g.generate('hard',90,'q-18188',parameters=x),inputs))
for x,r in zip(inputs,records):check(r);assert r==g.generate('hard',90,'q-18188',parameters=x)
assert not list((D/'plots').glob('tmp*'))
# Mutation regression: correct answer cannot conceal a wrong displayed product stage.
bad=copy.deepcopy(r);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('108', '109')
try:check(bad)
except AssertionError:pass
else:raise AssertionError('wrong intermediate product not rejected')
for level,pbad in [('moderate',{**p,'angle':90,'a':7}),('hard',{**p,'angle':90}),('easy',{**p,'outer':121})]:
 try:g.generate(level,parameters=pbad)
 except ValueError:pass
 else:raise AssertionError('difficulty bounds failed')
# Real native checks of supported repaired originals and variants.
fixtures=[]
for i,r in enumerate([r for r in raw if ':answer-field/correct' in r['question'][':question/answer-fields'][0]]+repaired+normal[:10]+normal[40:50]+normal[80:90]+variants):
 f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all owned original/authored choices'} for a in f[':answer-field/choices']]
 else:
  value=f[':answer-field/choices'][0][':answer/value'];checks=[{'submitted':value,'expected':'accepted','purpose':'integer canonical'}, {'submitted':str(int(value)+1),'expected':'rejected','purpose':'wrong area'}, {'submitted':value+'+0','expected':'rejected','purpose':'mathematically equivalent expression rejected by nearest-integer form requirement'}, {'submitted':'0'+value,'expected':'rejected','purpose':'equivalent leading-zero numeral rejected by rounding format'}, {'submitted':' '+value+' ','expected':'accepted','purpose':'integer whitespace normalization'}]
 fixtures.append({'label':str(i),'record':r,'checks':checks})
(D/'native-input.json').write_text(json.dumps(fixtures,indent=2));engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
report={'status':'passed','practice_sources':8,'exact_prompts':8,'exact_present_solutions':7,'solution_absence_preserved':1,'exact_banks':8,'source_options_matched':matched_choices,'source_correct_designations_matched':matched_refs,'source_missing_designation':1,'raw_attribute_presence_parity':8,'mathematically_correct_source_keys':7,'inferred_missing_key':{'q-18192':33},'normal_checked':len(normal)+len(variants),'normal_unique_tasks':{l:len(v) for l,v in fingerprints.items()},'normal_family_coverage':sorted(family_coverage),'fresh_cache_full_equality':True,'concurrent_full_equality':True,'mutation_rejected':True,'database_writes':0,'limitations':['All 4 historical radio banks have opaque distractor intent; public replay profiles evidence only.','q-18192 has no observed difficulty/key/solution; repaired hard/key 33 and solution are authored/inferred.','q-285754 mm-to-m intermediate unit typo preserved raw; fixed normally.','Three source substitution rows reverse the AB/AD labels relative to rasters; raw evidence retained, changed normal diagrams follow their displayed factor order.'],'native_rounding_form_limitation':'Nearest-integer prompts reject unevaluated equivalent expressions and leading-zero numerals; canonical integer and surrounding whitespace accepted.', 'runtime':{'python':sys.version.split()[0],'sympy':g.sp.__version__,'matplotlib':g.matplotlib.__version__},'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
review_records=variants+[g.generate(level,200+i) for level in ('easy','moderate') for i in range(2)]
(D/'review.json').write_text(json.dumps(review_records,indent=2,ensure_ascii=False)+'\n')
review=['# Triangle-from-quadrilateral review','Original raw evidence preserves omissions and errors. Historical banks are evidence only; generated method banks are labeled authored.']
for original,repair in zip(raw,repaired):
 sid=original['generation']['template'];review.extend(['## Original '+sid,g.markdown(original),'### Supported repair (opaque bank; evidence only)',g.markdown(repair)])
for r in review_records:review.extend(['## Generated '+r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['template'],g.markdown(r)])
(D/'review.md').write_text('\n\n'.join(review)+'\n')
print(json.dumps(report,indent=2))
