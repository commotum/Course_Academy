import copy,json,subprocess,collections,sys
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import validate_generated_record
H=Path(__file__).resolve().parent;staged={x['kp']for x in json.loads((H/'generator-candidates.json').read_text())};samples=[x for x in json.loads((H/'generator-samples.json').read_text())if x['kp']not in staged]+json.loads((H/'staged-generator-samples.json').read_text())+json.loads((H/'generator-full-samples.json').read_text())+json.loads((H/'generator-api-samples.json').read_text());seen=set();unique=[]
for r in samples:
 q=r['record']['question'];key=(r['kp'],q[':question/id'],r.get('kind','fresh'))
 if key not in seen:unique.append(r);seen.add(key)
fields=[];tests=[];report=[];nofields=[];mathD=copy.deepcopy(json.loads((H/'snapshot.json').read_text()));kpTopics={k:t for t,k,q in mathD['links']};mathD['questions']=[];mathD['links']=[];idents=dict(json.loads((H/'idents.json').read_text()));byident={v:k for k,v in idents.items()}
def ident(v):return v.get(':db/ident')or idents[v[':db/id']]if isinstance(v,dict)else v
def right(f):
 c=f.get(':answer-field/correct');c=c[1]if isinstance(c,list)else c.get(':answer/id',c.get(':db/id'))if isinstance(c,dict)else c
 return next((a for a in f.get(':answer-field/choices',[])if c in[a.get(':answer/id'),a.get(':db/id')]),None)
for i,r in enumerate(unique):
 rec=copy.deepcopy(r['record']);q=rec['question'];label=str(r['kp'])+'/'+str(i);kind=r.get('kind','fresh');fresh=kind.startswith('fresh')or kind=='fresh' or kind=='staged-successor';meta={'kp':r['kp'],'label':label,'kind':kind,'template':rec.get('generation',{}).get('template'),'source':rec.get('generation',{}).get('source_ids',rec.get('generation',{}).get('source_id'))};checks=[]
 try:validate_generated_record(rec);meta['format_pass']=True
 except Exception as ex:meta['format_pass']=False;meta['format_error']=str(ex)
 for a in[':question/problem',':question/worked-solution']:
  if a in q:fields.append({'entity':label,'attribute':a,'value':q[a]})
 for j,f in enumerate(q.get(':question/answer-fields',[])):
  typ=ident(f[':answer-field/type']);f[':answer-field/type']=typ;c=right(f)
  if typ==':answer-field.type/checkbox':fields.append({'entity':label,'attribute':'answer-field/key','value':f[':answer-field/key']})
  for a in f.get(':answer-field/choices',[]):
   a[':answer/type']=ident(a[':answer/type']);fields.append({'entity':label,'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type']==':answer.type/math'})
  if c is None:meta.setdefault('missing_key_fields',[]).append(j);continue
  f[':answer-field/correct']=[':answer/id',c[':answer/id']]
  if typ==':answer-field.type/blank':checks.extend([{'field_index':j,'submitted':c[':answer/value'],'expected':'accepted'},{'field_index':j,'submitted':'987654321','expected':'rejected'}])
  else:checks.extend({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==c[':answer/id']else'rejected'}for a in f[':answer-field/choices'])
 if not meta.get('missing_key_fields')and q.get(':question/answer-fields'):tests.append({'label':label,'record':rec,'checks':checks})
 else:nofields.append(meta)
 # Synthetic IDs only in local math-check input; real identities are preserved in unique sample ledger.
 mq=copy.deepcopy(q);mq[':db/id']=990000000000+i
 for j,f in enumerate(mq.get(':question/answer-fields',[])):
  f[':db/id']=991000000000+i*10+j;f[':answer-field/type']={':db/id':byident[f[':answer-field/type']]};cid=f.get(':answer-field/correct',[None,None]);cid=cid[1]if isinstance(cid,list)else None
  for k,a in enumerate(f.get(':answer-field/choices',[])):a[':db/id']=992000000000+i*100+j*10+k;a[':answer/type']={':db/id':byident[a[':answer/type']]}
  c=next((a for a in f.get(':answer-field/choices',[])if a[':answer/id']==cid),None)
  if c:f[':answer-field/correct']=copy.deepcopy(c)
  else:f.pop(':answer-field/correct',None)
 mathD['questions'].append(mq);mathD['links'].append([kpTopics[r['kp']],r['kp'],mq[':db/id']]);meta['synthetic_math_id']=mq[':db/id'];report.append(meta)
(H/'generator-final-samples.json').write_text(json.dumps(unique,indent=2));(H/'generator-math-snapshot.json').write_text(json.dumps(mathD,indent=2));(H/'generator-final-coverage.json').write_text(json.dumps({'records':len(unique),'packages':len({r['kp']for r in unique}),'graded_records':len(tests),'checks':sum(len(x['checks'])for x in tests),'ungradable_evidence_only':nofields,'format_failures':[r for r in report if not r['format_pass']],'records_ledger':report},indent=2));(H/'generator-grading-input.json').write_text(json.dumps(tests,indent=2));(H/'generator-render-input.json').write_text(json.dumps(fields,indent=2));subprocess.run([str(H.parent/'check-engine'),str(H/'generator-grading-input.json'),str(H/'generator-grading.json')],check=True);print('generators',len(unique),'renderfields',len(fields),'gradedrecords',len(tests),'formatfailures',sum(not r['format_pass']for r in report))
