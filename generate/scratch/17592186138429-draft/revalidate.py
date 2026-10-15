"""Read-only original-source/full-bank and actual-output revalidation of owned draft."""
import os,sys,json,pathlib,hashlib,importlib.util,subprocess,re,copy
sys.dont_write_bytecode=True
import sympy as sp
H=pathlib.Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('draft_word',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((H/'source.json').read_text())
(H/'independent-inventory.json').write_text(json.dumps({'database':source['database'],'basis':source['basis'],'lineage':source['lineage'],'questions':[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Captured existing non-MA graph-intersection question in the same KP; motion or volume context and intersection reading match the source method. Excluded from MA template counts.'}for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'not in q]},indent=2)+'\n')
cases=json.loads((H/'source-cases.json').read_text());records=[];fidelity=[];engine=[];slots={}
def check(r):
 q=r['question'];m=r['generation'];p=m['parameters'];name=m['template'];a0,a1,b0,b1=[sp.Rational(p[k]) for k in ('a0','a1','b0','b1')]
 # Independently read exact plotted-line endpoints from the linked assets.
 for role,body in [('prompt',q[':question/problem']),('solution',q[':question/worked-solution'])]:
  refs=re.findall(r'!\[\]\((.*?)\)',body);assert len(refs)==1
  path=H/refs[0];assert path.read_bytes().startswith(b'\x89PNG')
  if path.with_suffix('.json').exists():
   side=json.loads(path.with_suffix('.json').read_text());lines=[]
   for key in ('a','b'):
    (x1,y1),(x2,y2)=[[sp.Rational(v) for v in row] for row in side['plotted_line_endpoints'][key]];slope=(y2-y1)/(x2-x1);lines.append((y1-slope*x1,slope))
   (aa,ab),(ba,bb)=lines;assert [aa,ab,ba,bb]==[a0,a1,b0,b1]
   tt=(ba-aa)/(ab-bb);yy=aa+ab*tt
   if role=='solution':assert list(map(sp.Rational,side['annotation_point']))==[tt,yy]
   assert side['numbered_x_ticks']==[x for x in side['grid_x_ticks'] if x and x%p['xlabel_step']==0]
 t=(b0-a0)/(a1-b1);y=a0+a1*t;assert t>0 and y>0
 assert re.search(r'point \$\('+str(t)+','+str(y)+r'\)\.?\$',q[':question/worked-solution'])
 body=q[':question/worked-solution'];assert body.index('intersect')<body.index('![]')<body.index('In this case')<body.index('So,')
 for text in [q[':question/problem'],body]:assert text.count('$')%2==0 and text.count('{')==text.count('}')
 fields=q[':question/answer-fields'];expected={'field-1':t,'field-2':y} if name=='walkers' else {fields[0][':answer-field/key']:t}
 checks=[]
 for i,f in enumerate(fields):
  vals=[a[':answer/value'] for a in f[':answer-field/choices']];key=f[':answer-field/key'];correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);cv=correct[':answer/value'];v=sp.Rational(cv[:-1] if name=='trucks' else cv);assert v==expected[key]
  assert len(vals)==len(set(vals));assert not any('$' in s for s in vals)
  if f[':answer-field/type']==':answer-field.type/radio':
   assert len(vals)==5
   for a in f[':answer-field/choices']:
    av=sp.Rational(a[':answer/value'][:-1] if name=='trucks' else a[':answer/value']);assert 0<av<=p['xmax'];assert (av==v)==(a==correct)
    checks.append(dict(field_index=i,submitted_answer_id=a[':answer/id'],expected='accepted' if a==correct else 'rejected',purpose='Complete displayed bank independently read against intersection'))
  else:
   assert len(vals)==1 and '{{'+key+'}}' in q[':question/problem']
   for text,exp in [(str(v),'accepted'),(str(v)+'.0','accepted'),(str(v*2)+'/2','accepted'),(str(v+1),'rejected'),(str(-v),'rejected'),(str(y if key=='field-1' else t),'rejected')]:
    checks.append(dict(field_index=i,submitted=text,expected=exp,purpose='Exact numeric fragment; equivalent integer/decimal/quotient and wrong/sign/coordinate controls'))
 unit={'planes':'ft','tanks':'L','walkers':'m','trucks':'miles','cars':'km/h','pools':'L'}[name]
 assert '\\text{'+unit+'}' in body or '\\textrm{'+unit+'}' in body
 if name=='planes':assert f'{int(y)*1000:,}' in body and f'${t}$ minutes' in body
 if name=='tanks':assert f'$t={t}$ minutes' in body and f'${y}\\,' in body
 if name=='walkers':assert 'Mary and Sam met' in body and f'${t}$ minutes' in body and f'${y}\\,' in body
 assert g.generate(q[':question/difficulty'].split('/')[-1],seed=991,template=name,parameters=p,profile=m['bank_profile'])['question'][':question/id']==q[':question/id']
 engine.append({'label':str(len(records))+'-'+name,'record':r,'checks':checks})
 slots.setdefault(name,[]).append({'t':str(t),'y':str(y),'a1':str(a1),'b1':str(b1),'a0':str(a0),'b0':str(b0),'task':m['parameter_fingerprint']})
 return t,y
for c in cases:
 r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);t,y=check(r);records.append(r)
 sq=next(q for q in source['record'][':knowledge-point/questions'] if q.get(':question/math-academy-id')==c['source_id']);q=r['question'];assert q[':question/problem']==sq[':question/problem']
 sf={f[':answer-field/key']:f for f in sq[':question/answer-fields']};matches=0
 for f in q[':question/answer-fields']:
  s=sf[f[':answer-field/key']];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in s[':answer-field/choices']);matches+=len(s[':answer-field/choices'])
  if ':answer-field/correct' in s:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==s[':answer-field/correct'][':answer/value']
 normalize=lambda text:re.sub(r'!\[\]\(.*?\)','<PLOT>',text)
 sol='unavailable; authored canonical-method solution'
 if ':question/worked-solution' in sq:
  raw=normalize(sq[':question/worked-solution']);got=normalize(q[':question/worked-solution'])
  if c['template']=='walkers':raw=raw.replace('Mary and her brother','Mary and Sam');sol='supported identity repair; remaining normalized prose exact'
  else:sol='normalized prose exact'
  assert raw==got
 fidelity.append(dict(source_id=c['source_id'],prompt_exact=True,matched_values=matches,full_bank=True,solution=sol))
for name,level in [('trucks','easy'),('pools','moderate'),('cars','hard'),('planes','easy'),('tanks','easy'),('walkers','easy')]:
 for seed in range(8):
  r=g.generate(level,seed=seed,template=name);check(r);records.append(r)
# Canonical task fingerprint excludes seed, bank and profile; preserve normal original geometry.
for c in cases[:2]:
 pp=c['parameters'].copy();pp.update({'xmax':9} if c['template']=='trucks' else {});a=g.generate(c['level'],parameters=pp,template=c['template'],profile=c['bank_profile']);b=g.generate(c['level'],parameters=pp,template=c['template']);assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']
# Negative controls target independent printed stage/field/plot checks.
negative_controls=0
for original in [records[0],records[3],records[4]]:
 for mutation in ['wrong_key','wrong_point','wrong_unit']:
  bad=copy.deepcopy(original)
  if mutation=='wrong_key':bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='99999'
  elif mutation=='wrong_point':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('point $(','point $(99999,')
  else:bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('\\text{','\\text{WRONG').replace('\\textrm{','\\textrm{WRONG')
  try:check(bad)
  except (AssertionError,ValueError):negative_controls+=1
  else:raise AssertionError('Negative control accepted '+mutation)
# Public CLI defaults/count contract through real JSON and markdown paths.
cli=[]
for fmt in ['json','markdown']:
 for count in [1,3]:
  cmd=[str(ROOT/'.venv/bin/python'),str(H.with_suffix('.py')),'--difficulty','all','--seed','314','--count',str(count),'--format',fmt]
  text=subprocess.check_output(cmd,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
  if fmt=='json':assert len(json.loads(text))==3*count
  else:assert text.count('**Worked solution**')==3*count
  cli.append(dict(format=fmt,count=count,output_records=3*count))
(H/'revalidation-engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
subprocess.run([str(H/'check-engine-frozen'),str(H/'revalidation-engine-input.json'),str(H/'revalidation-engine-report.json')],check=True)
(H/'revalidation-sampled.json').write_text(json.dumps(records,indent=2)+'\n')
(H/'revalidation-review.md').write_text('\n\n---\n\n'.join('## '+r['generation']['template']+' / '+str(i)+'\n\n'+g.markdown(r) for i,r in enumerate(records))+'\n')
report=dict(status='awaiting independent root review',basis=2275,source_raw_ma=5,captured_nonma_inventory=13,canonical_examples=1,source_banks=5,source_values=18,source_distractors=12,source_fields=6,source_fidelity=fidelity,actual_output_records=len(records),linked_plots=2*len(records),native_grading=json.loads((H/'revalidation-engine-report.json').read_text()),slots={name:{key:sorted({x[key] for x in rows}) for key in rows[0]} for name,rows in slots.items()},public_cli=cli,negative_controls_rejected=negative_controls,prior_qa_preserved='registered baseline and historical1356 validation retained; original two radio sources unchanged',database_writes=0)
(H/'revalidation.json').write_text(json.dumps(report,indent=2)+'\n');print('Revalidation records',len(records))
