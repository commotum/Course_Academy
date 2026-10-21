import sys
sys.dont_write_bytecode=True
import json,re,collections,hashlib,importlib.util,difflib
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path('/home/jake/Developer/Course_Academy');P=Path(__file__).resolve().parent;OUT=P.parent/'flattened'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
lj=load('hat_lj',Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py'))
md=load('hat_md',Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py'))
metadata={x[':db/id']:x for x in json.loads((P.parent/'evidence/metadata.json').read_text())}
rows=[x for x in json.loads((P.parent/'candidates.json').read_text())if x['flattened_occurrences']]
attrs={1064:':tutorial/content',1071:':question/problem',1074:':question/worked-solution',1080:':answer/value'}
census=json.loads((P/'archived-hat-mathml.json').read_text());sourcebyid=collections.defaultdict(list);cache={}
for item in census:
 jp=str(Path(item['file']).with_suffix('.json'))
 if jp not in cache:cache[jp]=json.loads(Path(jp).read_text())
 d=cache[jp];kind,number=item['selector'][1:].split('-');s=next(x for x in d['lesson']['items']if str(x.get('question_id'if kind=='question'else'step_id'))==number)
 sid='q-'+number if kind=='question' else ('tutorial-'if s.get('step_type')=='tutorial' else'e-')+str(s.get('content_id'))
 m=BeautifulSoup(item['mathml'],'html.parser').mover;cs=m.find_all(recursive=False)
 bad=md.normalize_math_tex(lj.mathml_to_text(m));base=md.normalize_math_tex(lj.mathml_to_text(cs[0]));command='hat'if cs[1].get('stretchy')=='false'else'widehat'
 sourcebyid[sid].append(item|{'source_identity':sid,'source_json':jp,'bad':bad,'base':base,'command':command,'good':'\\'+command+'{'+base+'}'})

def find_identity(obj):
 if isinstance(obj,dict):
  if ':question/math-academy-id'in obj:return obj[':question/math-academy-id']
  if ':tutorial/math-academy-id'in obj:return 'tutorial-'+str(obj[':tutorial/math-academy-id'])
  for v in obj.values():
   result=find_identity(v)
   if result:return result
 elif isinstance(obj,list):
  for v in obj:
   result=find_identity(v)
   if result:return result
 return None
orphans={metadata[x['entity']][':answer/id']:x['entity']for x in rows if not find_identity(metadata[x['entity']])}
legacy={}
for path in sorted((ROOT/'.local/edb/lesson-seed').glob('lessons-*.edn')):
 for index,line in enumerate(path.read_text().splitlines()):
  found=[uid for uid in orphans if uid in line]
  if not found:continue
  mid=re.search(r':question/math-academy-id\s+(\d+)',line)
  assert mid,(path,index)
  for uid in found:legacy[orphans[uid]]={'source_identity':'q-'+mid[1],'legacy_seed_path':str(path),'legacy_seed_line':index+1,'answer_uuid':uid,'legacy_seed_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
assert len(legacy)==len(orphans),(len(legacy),len(orphans))
changes=[];unresolved=[]
for row in rows:
 eid=row['entity'];sid=find_identity(metadata[eid])or legacy[eid]['source_identity'];sources=sourcebyid[sid]
 before=row['value'];after=before;proofs=[]
 if not sources:
  unresolved.append({'entity':eid,'source_identity':sid,'reason':'No archived source hats','value':before});continue
 targets=collections.defaultdict(list)
 for a in sources:targets[re.sub(r'\s+','',a['bad'])].append(a)
 for target,evidence in sorted(targets.items(),key=lambda kv:len(kv[0]),reverse=True):
  choices={a['good']for a in evidence}
  if len(choices)>1:
   unresolved.append({'entity':eid,'source_identity':sid,'reason':'Ambiguous source width for sameflattenedtext','target':target,'options':list(choices),'value':before});continue
  a=evidence[0]
  while True:
   indices=[i for i,c in enumerate(after)if not c.isspace()];compact=''.join(after[i]for i in indices);at=compact.find(target)
   if at<0:break
   start=indices[at];end=indices[at+len(target)-1]+1;old=after[start:end]
   after=after[:start]+a['good']+after[end:]
   proofs.append({'before':old,'after':a['good'],'command':a['command'],'base':a['base'],'source_identity':sid,'sourcepath':a['file'],'source_sha256':a['file_sha256'],'selector':a['selector'],'source_mathml':a['mathml'],'source_bad_tex':a['bad'],'source_operator_attrs':a['operator_attrs'],'match':'Exact original converter output ignoring whitespace; source MathML supplies full hat base and width.'})
 if re.search(r'\^\(\^\)',after):unresolved.append({'entity':eid,'source_identity':sid,'reason':'Remaining flattened hat','after':after,'source_forms':[(a['bad'],a['good'])for a in sources]})
 if after!=before:changes.append({'entity':eid,'attribute_id':row['attribute_id'],'attribute':attrs[row['attribute_id']],'before':before,'after':after,'proofs':proofs,'source_identity':sid,'orphan_provenance':legacy.get(eid)})
(P/'flat-unresolved.json').write_text(json.dumps(unresolved,ensure_ascii=False,indent=2)+'\n');(OUT/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
(P/'archive-index.json').write_text(json.dumps(dict(sourcebyid),ensure_ascii=False,indent=2)+'\n')
summary={'candidate_fields':len(rows),'prepared_fields':len(changes),'prepared_occurrences':sum(len(x['proofs'])for x in changes),'orphan_answers_source_mapped':len(legacy),'unresolved':len(unresolved)}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
for x in unresolved:print(x['entity'],x['source_identity'],x['reason'],x.get('target',''))
assert not unresolved,unresolved
assert len(changes)==len(rows)
assert sum(len(x['proofs'])for x in changes)==sum(x['flattened_occurrences']for x in rows)
for x in changes:
 replay=x['before']
 for proof in x['proofs']:
  assert re.sub(r'\s+','',proof['before'])==re.sub(r'\s+','',proof['source_bad_tex'])
  assert proof['after']=='\\'+proof['command']+'{'+proof['base']+'}'
  assert proof['command']==('hat'if proof['source_operator_attrs'].get('stretchy')=='false'else'widehat')
  assert proof['before']in replay
  replay=replay.replace(proof['before'],proof['after'],1)
  assert hashlib.sha256(Path(proof['sourcepath']).read_bytes()).hexdigest()==proof['source_sha256']
 assert replay==x['after']
 assert re.findall(r'\{\{[^{}]+\}\}',x['before'])==re.findall(r'\{\{[^{}]+\}\}',x['after'])
(OUT/'changes.diff').write_text(''.join(''.join(difflib.unified_diff(x['before'].splitlines(True),x['after'].splitlines(True),fromfile=str(x['entity'])+x['attribute']+' before',tofile=str(x['entity'])+x['attribute']+' after'))+'\n'for x in changes))
summary.update({'all_current_spans_match_original_converter_output':True,'all_source_hashes_rechecked':True,'all_outside_text_unchanged':True,'placeholder_keys_unchanged':True,'hat_occurrences':sum(z['command']=='hat'for x in changes for z in x['proofs']),'widehat_occurrences':sum(z['command']=='widehat'for x in changes for z in x['proofs'])})
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
