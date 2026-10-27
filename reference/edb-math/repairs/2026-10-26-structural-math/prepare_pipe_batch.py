"""Prepare a source-bound table repair; never overwrite a submitted payload."""
import collections,hashlib,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/structural-math-2026-10-26';B=H/'batch-05';assert not(B/'commit-intent.json').exists()
sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import dumps,kw
from question_capture.math_format import MATH,cells,environment,normalize_limit_operators,validate_math_structure
ns={'__file__':str(H/'recover_formulas.py')};exec(compile((H/'recover_formulas.py').read_text().split('index=collections.defaultdict(list)')[0],str(H/'recover_formulas.py'),'exec'),ns)
meta=json.loads((W/'metadata.json').read_text());parents=json.loads((W/'parents.json').read_text());sourceindex=json.load(open('/tmp/structural-pipe-source-index.json'));targets={(d['e'],d['a']):d for d in json.load(open('/tmp/structural-pipe-extended.json'))};props={(d['entity'],d['attribute']):d for d in json.load(open('/tmp/structural-pipe-combined.json'))};remaining=json.load(open('/tmp/structural-pipe-unresolved-final.json'));review=[];retained=[];cache={}
def currency_layout(d,src):
 # Archived currency MathML itself contains malformed [math] wrappers. The
 # verified source grid controls layout only; preserve repaired current math.
 body=d['before'][2:-2].strip();body=re.sub(r'^\\displaystyle\s*','',body);rows=[];start=depth=i=0
 while i<len(body):
  if body[i]=='\\':i+=2;continue
  depth+=(body[i]=='{')-(body[i]=='}')
  if body[i]==';'and not depth:rows.append(body[start:i].strip());start=i+1
  i+=1
 rows.append(body[start:].strip());span=environment(src,0);source_rows=cells(src[span[0]:span[1]]);assert len(rows)==len(source_rows)
 assert '|='in rows[0]and all(r.startswith('=')for r in rows[1:])
 rows[0]=rows[0].replace('|=','&=',1);rows[1:]=['&'+r for r in rows[1:]]
 return r'\begin{aligned}'+' \\\\ '.join(rows)+r'\end{aligned}'
error_sources={(d['entity'],d['attribute'],tuple(d['span'])):d for d in json.load(open('/tmp/structural-layout-error-sources.json'))}
for d in remaining:
 key=d['entity'],d['attribute'];opts={c['source_tex']for c in d['position_candidates']if isinstance(c['source_tex'],str)and r'\begin{aligned}'in c['source_tex']};error=error_sources.get((*key,tuple(d['span'])))
 if not opts and not error:
  retained.append({**d,'review':'Retain legitimate conditional/set/absolute-value notation or terminal punctuation; no serialized equation grid.'});continue
 assert len(opts)<=1
 source=next(s for s in sourceindex if s['identity']==d['identity']and s['attribute']==d['attribute']);before=targets[key]['v'];maths=list(MATH.finditer(before));index=next(i for i,m in enumerate(maths)if m.start()==d['span'][0])
 if error and 'math]'in error['raw_source_tex']and d['entity']in {17592186179565,17592186179566,17592186179567,17592186180695}:
  tex=currency_layout(d,error['raw_source_tex']);proof='Archived row grid only: retained all current currency and expression tokens because archived currency markup is corrupt'
 else:
  if source['html']not in cache:cache[source['html']]=ns['formulas'](source['html'])
  fs=cache[source['html']];assert len(fs)==len(maths);tex=fs[index];assert isinstance(tex,str),(key,index,tex);proof='Individually reviewed source formula at the same identity, attribute, formula count and position; recovered annotations and row roles'
 assert '[math]'not in tex and '[/math]'not in tex
 after='$$\n'+tex+'\n$$'if d['before'].startswith('$$')else'$'+tex+'$';validate_math_structure(after)
 o=props.setdefault(key,{'entity':key[0],'attribute':key[1],'identity':d['identity'],'source_path':source['path'],'before':before,'changes':[]});assert all(c['span']!=d['span']for c in o['changes']);o['changes'].append({'span':d['span'],'before':d['before'],'after':after,'proof':proof,'source_path':source['path']})
proposed={};reasons=collections.defaultdict(set)
for key,o in props.items():
 after=o['before'];changes=sorted(o['changes'],key=lambda c:c['span']);last=-1
 for c in changes:
  a,b=c['span'];assert a>=last and after[a:b]==c['before'];last=b
 for c in reversed(changes):a,b=c['span'];after=after[:a]+c['after']+after[b:]
 proposed[key]={'before':o['before'],'after':after};reasons[key].add('source-formula-recovery');review.append(o)
attrs={'question/problem','question/worked-solution','tutorial/content','answer/value','answer/feedback','answer-field/feedback','multistep/context','multistep/content','assigned-problem/instructions'};seen=set();new_limits=0
for line in(W/'final.jsonl').open():
 d=json.loads(line);key=d['e'],d['a'];value=d['v']
 if key in proposed:assert value==proposed[key]['before'];seen.add(key);value=proposed[key]['after']
 if d['a']not in attrs or not isinstance(value,str)or'lim'not in value:continue
 bare=d['a']=='answer/value'and meta.get(str(d['e']),{}).get('answer/type')==17592186045498
 def replace(m):
  whole=m[0];size=2 if whole.startswith(('$$',r'\[',r'\('))else 1;body=whole[size:-size];fixed=normalize_limit_operators(body)
  if fixed!=body:reasons[key].add('limit-operator')
  result=whole[:size]+fixed+whole[-size:]
  left=value[value.rfind('\n',0,m.start())+1:m.start()];end=value.find('\n',m.end());right=value[m.end():end if end>=0 else len(value)]
  if d['a']!='answer/value'and size==1 and re.search(r'\\lim(?![A-Za-z])',result)and not left.strip()and not right.strip()and '{{'not in result:
   result='$$\n'+fixed.strip()+'\n$$';reasons[key].add('standalone-limit-display')
  return result
 after=normalize_limit_operators(value)if bare else MATH.sub(replace,value)
 if after!=value:
  if bare:reasons[key].add('limit-operator')
  new_limits+=1
  proposed.setdefault(key,{'before':d['v']})['after']=after
assert len(seen)==len(props)
fields=[];validation=[]
for(e,a),d in sorted(proposed.items()):
 before,after=d['before'],d['after'];assert before!=after
 if(e,a)==(17592186221065,'question/worked-solution'):
  old=r'\left(\dfrac{7}{9}\right'+'\n$$';new=r'\left(\dfrac{7}{9}\right.'+'\n$$'
  assert old in after;after=after.replace(old,new,1);reasons[e,a].add('source-null-delimiter')
 if(e,a)==(17592186204245,'question/problem'):
  # q-212891 source explicitly shows visible set delimiters, including across
  # the same three response slots. Escape only those delimiters.
  for old,new in [('$X = {1, 2, 3, 4}$',r'$X = \{1, 2, 3, 4\}$'),('$S∘R = {(1, 1), (1$',r'$S∘R = \{(1, 1), (1$'),('$, 2)}$',r'$, 2)\}$')]:
   assert old in after;after=after.replace(old,new,1)
  reasons[e,a].add('source-set-delimiters')
 bare=a=='answer/value'and meta.get(str(e),{}).get('answer/type')==17592186045498
 try:validate_math_structure(after,bare_math=bare)
 except ValueError as ex:
  validation.append({'entity':e,'attribute':a,'before':before,'after':after,'error':str(ex)})
 assert re.findall(r'\{\{[^{}]+\}\}',before)==re.findall(r'\{\{[^{}]+\}\}',after)
 assert re.findall(r'!\[[^\]]*\]\([^)]*\)|<img\b[^>]*>',before)==re.findall(r'!\[[^\]]*\]\([^)]*\)|<img\b[^>]*>',after)
 fields.append({'entity':e,'attribute':a,'before':before,'after':after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'math_answer':bare,'answer_fields':sorted({p for p,attr in parents.get(str(e),[])if attr in ('answer-field/choices','answer-field/correct')}),'reasons':sorted(reasons[e,a])})
(H/'pipe-validation-failures.json').write_text(json.dumps(validation,indent=2)+'\n');assert not validation,[(d['entity'],d['error'])for d in validation]
B.mkdir(exist_ok=True);(B/'fields.json').write_text(json.dumps(fields,indent=2)+'\n');(B/'source-edits.json').write_text(json.dumps(review,indent=2)+'\n');(B/'reviewed-nonrepairs.json').write_text(json.dumps(retained,indent=2)+'\n');(B/'transaction.edn').write_text(dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in fields])+'\n')
for name in ['verify_render.py','verify_db.py','apply.py','check_grading.py']:(B/name).write_text((H/name).read_text().replace('R=H.parents[3]','R=H.parents[4]'))
report={'basis_t':8653,'fields':len(fields),'source_formula_fields':len(review),'source_formula_blocks':sum(len(o['changes'])for o in review),'additional_limit_fields':new_limits,'retained_candidate_blocks':len(retained),'attributes':dict(collections.Counter(f['attribute']for f in fields))};(B/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
