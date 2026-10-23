"""Prepare guarded formatting-only repairs from a fresh immutable EDB export."""
import collections,hashlib,importlib.util,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SNAPSHOT=ROOT/'.local/edb/inline-display-repair-current.jsonl'
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from math_format import MATH,cells,environment;from edn import kw,dumps
spec=importlib.util.spec_from_file_location('display_audit',ROOT/'reference/edb-math/audits/2026-10-23-inline-display/scan.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
ATTRS=audit.PROSE-{'answer/value'}
TAG=re.compile(r'<(/?)([A-Za-z][\w-]*)(\s[^<>]*?)?\s*(/?)>')
MARKER=re.compile(r'\{\{(?:answer-field:)?([^}]+)\}\}')
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def save(name,v):(HERE/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def tokens(value):
 masked=re.sub(r'```[\s\S]*?```|`[^`\n]*`',lambda m:' '*len(m[0]),value)
 return list(MATH.finditer(masked))
def body(m):
 s=m[0];return s[2:-2] if s.startswith(('$$',r'\[',r'\(')) else s[1:-1]
def html_context(value,pos):
 stack=[]
 for m in TAG.finditer(value,0,pos):
  tag=m[2].lower()
  if m[1]:
   for i in range(len(stack)-1,-1,-1):
    if stack[i][0]==tag:stack=stack[:i];break
  elif not m[4] and tag not in ('img','br','hr','input','meta','link','source','wbr'):stack.append((tag,m[0]))
 return stack

def integral_reference(tex):
 s=re.sub(r'\\(?:displaystyle|textstyle|limits|nolimits|quad|qquad)(?![A-Za-z])|\\[,;!]','',tex).strip()
 # An operator/domain reference has no integrand or equation.
 return bool(re.fullmatch(r'\{?\\(?:int|iint|iiint|oint)\s*\}?(?:\s*[_^]\s*(?:\{[^{}]*\}|[A-Za-z0-9]))*\s*[.,;:]?',s)) or s in ('∫','∬','∭','∮')

def balanced_source(tex):
 depth=0;env=[];i=0
 while i<len(tex):
  if tex[i]=='%':
   newline=tex.find('\n',i);i=len(tex) if newline<0 else newline+1;continue
  if tex[i]=='\\':
   token=re.match(r'\\(begin|end)\{([^{}]+)\}',tex[i:])
   if token:
    if token[1]=='begin':env.append(token[2])
    elif not env or env.pop()!=token[2]:return False
    i+=len(token[0]);continue
   i+=2;continue
  if tex[i]=='{':depth+=1
  elif tex[i]=='}':depth-=1
  if depth<0:return False
  i+=1
 return depth==0 and not env

def decision(value,m,attr):
 lineleft=value[value.rfind('\n',0,m.start())+1:m.start()];lineend=value.find('\n',m.end());lineright=value[m.end():lineend if lineend>=0 else len(value)];line_alone=not lineleft.strip() and not lineright.strip(' \t.,;:')
 tex=body(m);integral=bool(audit.INTEGRAL.search(tex));big=bool(audit.BIG.search(tex));env=bool(audit.ENV.search(tex));fracs=tex.count(r'\frac')+tex.count(r'\dfrac');longfrac=(fracs>=2 and len(tex)>=40) or fracs and len(tex)>=70;longroot=r'\sqrt' in tex and len(tex)>=90;chain=(line_alone and tex.count('=')>=2) or (tex.count('=')>=3 and len(tex)>=70) or ('=' in tex and len(tex)>=180 and not env)
 if not any((integral,big,env,longfrac,longroot,chain)):return None,None
 if not balanced_source(tex):return 'retain','preexisting-unbalanced-source-math'
 left=value[value.rfind('\n',0,m.start())+1:m.start()];end=value.find('\n',m.end());right=value[m.end():end if end>=0 else len(value)];standalone=not left.strip() and not right.strip(' \t.,;:')
 context=html_context(value,m.start());layout=any(tag in ('table','td','th','select','option','a','code','pre') or re.search(r'class=[\'"][^\'"]*(?:matrix-operands|matrix-answer|matrix-response|question-equation)',raw) for tag,raw in context)
 explicit=bool(re.match(r'\s*(?:\{\s*)?\\displaystyle\b',tex))
 if integral:
  if integral_reference(tex):return ('retain','operator-or-domain-reference')
  paragraph=value[max(value.rfind('\n\n',0,m.start()),0):value.find('\n\n',m.end()) if value.find('\n\n',m.end())>=0 else len(value)]
  comparative=attr!='question/problem' and not standalone and bool(re.search(r'\b(?:express|rewrit\w*|written|writing)\b[\s\S]*\bas\b',paragraph,re.I)) and sum(1 for x in tokens(paragraph) if audit.INTEGRAL.search(body(x)))>=2
  if layout or comparative:return ('retain' if explicit else 'style','structured-layout' if layout else 'comparative-prose-reference')
  return 'display','substantive-integral'
 if layout:return 'retain','authored-structured-layout'
 if standalone:return 'display','standalone-large-expression'
 if env:
  if re.search(r'\\begin\{(?:aligned|align\*?|cases|gathered)\}',tex):return 'display','embedded-multiline-calculation'
  # Preserve compact vectors and small matrices used as in-sentence objects.
  if tex.count(r'\\')>=2 and len(tex)>=100:return 'display','embedded-large-matrix'
  return 'retain','compact-matrix-or-vector-reference'
 if longfrac or longroot or chain:return 'display','embedded-long-calculation'
 if big and len(tex)>=25 and ('=' in tex or re.search(r'\b(?:evaluate|calculate|compute|find|determine)\b',left,re.I)):return 'display','main-large-operator-calculation'
 return 'retain','compact-operator-reference'

def transform(row,overrides):
 value=row['v'];edits=[];review=[];parts=[];cursor=0
 for m in tokens(value):
  if m[0].startswith(('$$',r'\[')):continue
  action,reason=decision(value,m,row['a'])
  if not action:continue
  key=f"{row['e']}:{row['a']}:{m.start()}"
  if key in overrides:action='retain';reason=overrides[key]
  if action=='retain':review.append({'offset':m.start(),'math':m[0],'reason':reason});continue
  tex=body(m);prefix='' if re.match(r'\s*\\displaystyle\b',tex) else r'\displaystyle '
  end=m.end();punct='';start=m.start();deindented=False;line_prefix='';deindented_math_count=0
  line_start=value.rfind('\n',0,m.start())+1;leading=re.match(r'[ \t]*',value[line_start:m.start()])[0];previous_start=value.rfind('\n',0,max(0,line_start-1))+1;previous=value[previous_start:max(0,line_start-1)]
  if action=='display' and row['a']=='question/problem' and '{{field-' in value and not previous.strip() and (len(leading)>=4 or '\t' in leading) and line_start>=cursor:
   start=line_start;deindented=True;line_prefix=value[line_start+len(leading):m.start()];line_end=value.find('\n',m.end());line_end=len(value) if line_end<0 else line_end;deindented_math_count=max(1,len(tokens(value[line_start:line_end])))
  if action=='display' and end<len(value) and value[end] in '.,;:' and not tex.rstrip().endswith(tuple('.,;:')):punct=value[end];end+=1
  replacement='$$\n'+prefix+tex+punct+'\n$$' if action=='display' else '$'+prefix+tex+'$'
  replacement=line_prefix+replacement
  parts.extend([value[cursor:start],replacement]);cursor=end
  edits.append({'key':key,'start':start,'math_start':m.start(),'end':end,'deindented_source_equation':deindented,'deindented_math_count':deindented_math_count,'original':value[start:end],'original_math':m[0],'tex':tex,'replacement':replacement,'action':action,'reason':reason,'added_prefix':prefix,'moved_punctuation':punct})
 parts.append(value[cursor:]);after=''.join(parts)
 if edits:
  before_math=[body(m) for m in tokens(value)];after_math=[body(m) for m in tokens(after)];assert len(before_math)==len(after_math),(row['e'],row['a'],'math-count')
  planned=iter(edits);nextedit=next(planned,None)
  for a,b in zip(tokens(value),tokens(after)):
   if nextedit and a.start()==nextedit['math_start']:
    assert body(b).strip()==(nextedit['added_prefix']+body(a)+nextedit['moved_punctuation']).strip();nextedit=next(planned,None)
   else:assert body(a)==body(b)
  assert not nextedit
  assert MARKER.findall(value)==MARKER.findall(after)
  assert re.findall(r'images/[^\s)"<>]+',value)==re.findall(r'images/[^\s)"<>]+',after)
 return after,edits,review

def main():
 assert not list(HERE.glob('batch-*/commit-intent.json')),'Persisted requests must not be regenerated'
 overrides=json.loads((HERE/'overrides.json').read_text()) if (HERE/'overrides.json').exists() else {}
 rows=[];question_fields=collections.defaultdict(list);components=collections.defaultdict(dict);idents={};answer_types={};meta={};sources={}
 for r in map(json.loads,SNAPSHOT.open()):
  e,a,v=r['e'],r['a'],r['v']
  if a in ATTRS and isinstance(v,str) and ('$' in v or r'\(' in v):rows.append(r)
  if a=='question/answer-fields':question_fields[e].append(v)
  if a in ('answer-field/key','answer-field/type','answer-field/id','answer-field/correct'):components[e][a]=v
  if a=='answer/type':answer_types[e]=v
  if a=='db/ident':idents[e]=v
  if a in ('question/math-academy-id','tutorial/math-academy-id','tutorial/title'):meta.setdefault(e,{})[a]=v
 fields=[];retained=[]
 for row in rows:
  after,edits,review=transform(row,overrides)
  if review:retained.append({'entity':row['e'],'attribute':row['a'],'occurrences':review})
  if not edits:continue
  controls=[]
  for aid in sorted(question_fields[row['e']]):
   af=components[aid];typ=af.get('answer-field/type');kind=idents.get(typ,typ);ans=answer_types.get(af.get('answer-field/correct'));controls.append({'id':str(aid),'key':af['answer-field/key'],'type':kind,'answerType':idents.get(ans,ans)})
  fields.append({'entity':row['e'],'attribute':row['a'],'before':row['v'],'after':after,'before_sha256':sha(row['v']),'after_sha256':sha(after),'current_t':row['t'],'original_source':row['source'],'edits':edits,'fields':controls,'metadata':meta.get(row['e'],{})})
 fields.sort(key=lambda f:(f['entity'],f['attribute']));save('fields.json',fields);save('retained-inline.json',retained)
 batches=[];group=[];size=0
 def write_batch():
  nonlocal group,size
  if not group:return
  name=f'batch-{len(batches)+1:03d}';folder=HERE/name;folder.mkdir(exist_ok=True)
  tx=dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']] for f in group])+'\n';(folder/'transaction.edn').write_text(tx);(folder/'read-query.edn').write_text('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]\n');(folder/'read-inputs.edn').write_text(dumps([[[f['entity'],kw(f['attribute'])] for f in group]])+'\n');batches.append({'name':name,'fields':len(group),'entities':len({f['entity'] for f in group}),'sha256':sha(tx),'field_keys':[[f['entity'],f['attribute']] for f in group]});group=[];size=0
 for f in fields:
  length=len(dumps([kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]).encode())
  if size+length>3_500_000 or len(group)>=400:write_batch()
  group.append(f);size+=length
 write_batch();save('batches.json',batches)
 actions=collections.Counter(e['action'] for f in fields for e in f['edits']);reasons=collections.Counter(e['reason'] for f in fields for e in f['edits']);required=json.loads((ROOT/'reference/edb-math/audits/2026-10-23-inline-display/example-ids.json').read_text());assert set(required)<=set(f['entity'] for f in fields)
 report={'database':'math','basis':json.loads(SNAPSHOT.with_suffix('.manifest.json').read_text())['basis_t'],'fields':len(fields),'entities':len({f['entity'] for f in fields}),'edits':sum(actions.values()),'actions':dict(actions),'reasons':dict(reasons),'attributes':dict(collections.Counter(f['attribute'] for f in fields)),'batches':len(batches),'retained_reasons':dict(collections.Counter(o['reason'] for f in retained for o in f['occurrences'])),'equation_bodies_preserved':True,'answer_markers_and_image_references_preserved':True,'source':':agent/codex'};save('preparation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
