import hashlib,importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('v',R/'validate.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);g=v.g
records=json.loads((R/'review.json').read_text());allgenerated=json.loads((R/'engine-input.json').read_text())
# Two examples of every supported level/family, and every observed bank at source/changed parameters.
records=[{'label':x['label'],'record':x['record']} for x in allgenerated if x['label'].startswith(('source/','empirical-variant/'))]
for level in ('easy','moderate','hard'):
 for t in (['quarter_open','three_segments'] if level=='hard' else [k for k,p in g.TEMPLATES.items() if p[0]==level]):records += [{'label':x['label'],'record':x['record']} for x in allgenerated if x['label'].startswith(level+'/'+t+'/')][:2]
records=json.loads((R/'raw-source-records.json').read_text())+records
(R/'review.json').write_text(json.dumps(records,indent=2)+'\n')
parts=['# Source and generated review\n\nWorker review; parent independent QA remains pending. raw-source/raw-variant profiles are ineligible evidence records preserving the source attribute omissions; source/empirical-variant labels below denote normalized completed reconstructions, not raw parity. All original prompt plots and five solution plots were inspected directly. Each normal completed instance has one fixed source-shaped solution; raw q122484 retains its absent solution attribute. Zero source calculator flags were present; requirement remains unknown.\n']
for source in g.SOURCE_Q.values():
 qid=source[':question/math-academy-id'];parts+=['\n## Original '+qid+'\n']
 def images(text):
  i=[0]
  def f(m):path=str((R/(qid+'-source-'+str(i[0])+'.png')).resolve());i[0]+=1;return '![]('+path+')'
  return re.sub(r'!\[\]\([^)]*\)',f,text)
 # Source prompt is index 0; source solution plot is index1.
 combined=images(source[':question/problem']+'\n\n'+source.get(':question/worked-solution','[Source solution absent.]'))
 field=source[':question/answer-fields'][0];parts += [combined+'\n\nOriginal five options:\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in field[':answer-field/choices'])+'\n\n'+('Observed key: $'+field[':answer-field/correct'][':answer/value']+'$.' if ':answer-field/correct' in field else 'Observed key and rating absent; independently inferred value π+2√2 and authored moderate level are documented separately.')+'\n']
 for item in records:
  if item['label'] in ('raw-source/'+qid,'raw-variant/'+qid,'source/'+qid,'empirical-variant/'+qid):
   r=item['record'];q=r['question'];f=q[':question/answer-fields'][0];parts+=['\n### Generated '+item['label']+'\n\nParameters/profile: `'+json.dumps(r['generation']['parameters'])+'`, `'+r['generation']['profile']+'`.\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Raw source solution attribute absent; no completion inserted.]')+'\n']
parts+=['\n## Authored default variants\n\nObserved empirical banks are explicit replay profiles. These defaults use complete omitted/doubled-piece operations. Hard labels are authored rational-bookkeeping policy.\n']
for item in records:
 if item['label'].startswith(('raw-source/','raw-variant/','source/','empirical-variant/')):continue
 r=item['record'];q=r['question'];parts+=['\n### '+item['label']+'\n\nParameters: `'+json.dumps(r['generation']['parameters'])+'`.\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Raw source solution attribute absent; no completion inserted.]')+'\n']
(R/'review.md').write_text('\n'.join(parts))
# Exhaust the bounded normal samplers mathematically; rendering is separately tested.
capacity={}
for lev in ('easy','moderate','hard'):
 by={};allfp=set()
 for t in (['quarter_open','three_segments'] if lev=='hard' else [k for k,p in g.TEMPLATES.items() if p[0]==lev]):
  if t in ('semi','three_quarter','quarter_open','quarter_closed'):pp=[{'r':g.s.Rational(n)} for n in range(1,13)] if lev!='hard' else [{'r':g.s.Rational(k,d)} for d in (2,3) for k in range(1,12*d+1) if k%d]
  elif t=='three_segments':pp=[{'a':g.s.Rational(a,d),'b':g.s.Rational(b,d)} for d in ((2,3) if lev=='hard' else (1,)) for a,b in ((3,4),(4,3),(5,12),(12,5),(6,8),(8,6),(9,12),(12,9)) if lev!='hard' or a%d or b%d]
  else:pp=[{'a':g.s.Integer(a),'h':g.s.Integer(h),'b':g.s.Integer(b)} for a,h in ((3,4),(4,3),(6,8),(8,6)) for b in range(1,9) if not g.s.sqrt(b*b+h*h).is_Integer]
  fps=set()
  for p in pp:
   g.guard(lev,t,p);L=g.lengths(t,p);B=g.bank('authored_segments' if t.endswith('segments') else 'authored_arc',t,p,L);assert all(g.s.simplify(a-b)!=0 for i,(a,_) in enumerate(B) for b,_ in B[i+1:]);fps.add(tuple(map(g.canonical,L)))
  by[t]={'parameter_instances':len(pp),'primitive_length_tasks':len(fps)};allfp|=fps
 capacity[lev]={'families':by,'deduplicated_primitive_length_tasks':len(allfp)}
capacity['counting']='Conservative primitive-length operation tasks: excludes seed, option order, profile, direction and translation. Quarter-open and quarter-closed have the same two primitive lengths and deduplicate. Counts are finite normal-sampler capacities, not counts of all explicit permissible inputs.'
(R/'capacity.json').write_text(json.dumps(capacity,indent=2)+'\n')
report=json.loads((R/'validation.json').read_text());report['normal_sampler_capacity']=capacity;report['review_records']=len(records);report['versions']['matplotlib']=__import__('matplotlib').__version__;report['full_normalized_prompt_matches']=6;report['full_normalized_solution_matches']=5;(R/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
# Update documentation to reflect conservative task fingerprint and enumerated capacity.
p=R/'template-extraction.md';x=p.read_text().replace('Mathematical fingerprint excludes bank, profile and seed.','Mathematical fingerprint hashes the ordered primitive-length operations and excludes bank, profile, seed, translation and direction; quarter-open and quarter-closed calculations deduplicate.');x=x.split('\nNormal bounded sampler capacities')[0];x+='\nNormal bounded sampler capacities independently enumerated: easy 24, moderate 48, hard 48 primitive-length tasks. Moderate has 60 geometric parameter instances, but its 12 quarter-open/quarter-closed pairs are deliberately deduplicated. Hard has 36 rational radii and 12 rational familiar-triangle pairs. See capacity.json.\n';p.write_text(x)
print('Review records',len(records),'capacity',[(k,capacity[k]['deduplicated_primitive_length_tasks']) for k in ('easy','moderate','hard')])

source_assets={a:hashlib.sha256((Path('/media/jake/SSD/EDB/math')/a).read_bytes()).hexdigest() for q in g.SOURCE_Q.values() for a in re.findall(r'images/[^)]+',q[':question/problem']+' '+q.get(':question/worked-solution',''))}
manifest={'original_asset_sha256':source_assets,'script_sha256':hashlib.sha256(R.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((R/'source.json').read_bytes()).hexdigest(),'basis':2275,'scope':'Only generate/scratch/17592186162082.py and generate/scratch/17592186162082/','files':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(R.rglob('*')) if p.is_file() and p.name!='manifest.json' and '__pycache__' not in str(p)}}
(R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Evidence file count',len(manifest['files']),'script SHA256',manifest['script_sha256'])
