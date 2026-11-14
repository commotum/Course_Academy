import json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup,Tag,NavigableString
ROOT=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(ROOT/'scripts'))
from import_historical_question_content import Renderer
from question_capture.math_format import normalize_source_tex
OUT=ROOT/'reference/edb-math/repairs/2026-11-13-subspaces-source-latex'
snap=json.loads((OUT/'snapshot.json').read_text());kp=next(k for k in snap['topic'][':topic/knowledge-points'] if k[':db/id']==17592186119926)
class Faithful(Renderer):
 def math_node(self,n):
  if isinstance(n,Tag) and n.name=='mspace':
   w=n.get('width');return {'1em':'\\quad ','2em':'\\qquad '}.get(w,super().math_node(n))
  return super().math_node(n)
r=Faithful('1853')
def forms(s):
 out=[]
 def old(n):
  if isinstance(n,NavigableString):return str(n)
  if n.name=='mjx-container':return normalize_source_tex(r.m(n.find('math')))
  return ''.join(old(c) for c in n.children)
 for n in s.find_all(['svg','mjx-container']):
  if any(p.name in ('svg','mjx-container') for p in n.parents):continue
  if n.name=='svg':
   if n.title:out.append(normalize_source_tex(old(n.title)))
  else:out.append(normalize_source_tex(r.m(n.find('math'))))
 return out
formula=re.compile(r'(?<!\\)\$\$(.*?)\$\$|(?<![\\$])\$(?!\$)(.*?)(?<!\\)\$',re.S)
def current(s):return [(m.group(1) if m.group(1) is not None else m.group(2)).strip() for m in formula.finditer(s)]
paths={155956:('old',14096346),156607:('differential',14129646),156596:('differential',14246322),156624:('differential',14246322),156628:('old',14096346),156653:('old',14096346),157290:('differential',14129646),156620:('foundations',14116419),156682:('differential',14246322),156650:('differential',14246322),157293:('differential',14246322),157295:('linear',14339907)}
def read(p):return BeautifulSoup(json.loads(p.read_text())['html'] if p.suffix=='.json' else p.read_text(),'html.parser')
qs=[kp[':knowledge-point/canonical-example'],*kp[':knowledge-point/questions']];data=[];notes=[]
for q in qs:
 mid=q[':question/math-academy-id'];i=int(mid.split('-')[1]);raw={}
 if mid.startswith('e'):
  p=next((ROOT/'reference/mathacademy/capture/differential/14246322/observations').glob('lesson-step-41646-*.html'));s=read(p)
  raw={'problem':(s.select_one('.exampleQuestion'),p),'worked-solution':(s.select_one('.exampleExplanation'),p)}
 else:
  typ,task=paths[i]
  if typ=='old':
   base=ROOT/f'reference/mathacademy/question-capture/{task}';p=base/f'q-{i}-before.json';ss=base/f'history-q-{i}.json';s=read(p)
   raw={'problem':(s.select_one('.questionWidget-text'),p),'worked-solution':(read(ss),ss)}
  else:
   base=ROOT/f'reference/mathacademy/capture/{typ}/{task}/observations';p=next(base.glob(f'history-q-{i}-*.html'));ss=next(base.glob(f'history-solution-q-{i}-*.html'));s=read(p)
   raw={'problem':(s.select_one('.questionText'),p),'worked-solution':(read(ss),ss)}
 e={'id':q[':db/id'],'ma_id':mid,'question':q,'fields':{}}
 for field,(s,p) in raw.items():
  assert s is not None,(mid,field)
  e['fields'][field]={'source':str(p.relative_to(ROOT)),'source_formulas':forms(s),'current_formulas':current(q[':question/'+field])}
  notes.append('\n'+mid+' '+field+' '+str(p.relative_to(ROOT)))
  from itertools import zip_longest
  for a,b in zip_longest(e['fields'][field]['current_formulas'],e['fields'][field]['source_formulas']):notes.append(f'CURRENT: {a}\nSOURCE:  {b}')
 data.append(e)
(OUT/'lines2d-inventory.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');(OUT/'lines2d-compare.txt').write_text('\n'.join(notes));print('Saved inventory',len(data),'errors',r.errors)
def sig(s):
 s=re.sub(r'\\(?:mathbb|mathbf|mathrm|mathit|mathbfit)\{([^{}]*)\}',r'\1',s)
 s=re.sub(r'\\color(?:\[HTML\])?\{[^}]+\}', '',s)
 s=re.sub(r'\\hspace\{[^}]+\}|\\(?:qquad|quad)\b|\\[,;! ]','',s)
 s=s.replace('\\displaystyle','')
 s=s.replace('\\neq','\\ne').replace('\\checkmark','✓').replace('−','-')
 return re.sub(r'[\s{}]','',s)
proposals=[];coverage=[];unmatched=[];diffs=[]
for e in data:
 q=e['question'];sourceforms=sum((f['source_formulas'] for f in e['fields'].values()),[])
 matchmap={}
 for s in sourceforms:
  matchmap.setdefault(sig(s),[])
  if s not in matchmap[sig(s)]:matchmap[sig(s)].append(s)
 # Source checkbox labels retain original statements; only actual math is in scope.
 attrs=[(q[':db/id'],':question/problem',q[':question/problem']),(q[':db/id'],':question/worked-solution',q[':question/worked-solution'])]
 for f in q.get(':question/answer-fields',[]):
  attrs.append((f[':db/id'],':answer-field/key',f[':answer-field/key']))
  for a in f.get(':answer-field/choices',[]):attrs.append((a[':db/id'],':answer/value',a[':answer/value']))
 changes=0
 for entity,attr,before in attrs:
  if e['ma_id'].startswith('e-'):continue # canonical source styles already preserved; inspected separately
  def replace(m):
   old=(m.group(1) if m.group(1) is not None else m.group(2)).strip();new=old;opts=matchmap.get(sig(old),[])
   if not opts:
    unmatched.append({'ma_id':e['ma_id'],'attribute':attr,'formula':old});return m.group(0)
   # Ignore syntactic-only changes, such as spacing inside source grouping.
   style=lambda t: (re.findall(r'\\(?:mathbf|mathbb|mathrm|mathit|mathbfit)\{[^}]*\}',t),re.findall(r'\\color(?:\[HTML\])?\{[^}]+\}',t),re.findall(r'\\(?:qquad|quad)\b|\\hspace\{[^}]+\}',t))
   if len(opts)>1 and len({style(s) for s in opts})>1:raise Exception(('ambiguous',e['ma_id'],old,opts))
   new=opts[0]
   if old.startswith('\\displaystyle ') and not new.startswith('\\displaystyle '):new='\\displaystyle '+new
   if style(old)==style(new):return m.group(0)
   diffs.append({'ma_id':e['ma_id'],'entity':entity,'attribute':attr,'before_formula':old,'after_formula':new})
   return '$$\n'+new+'\n$$' if m.group(1) is not None else '$'+new+'$'
  after=formula.sub(replace,before)
  if after!=before:
   changes+=1;proposals.append({'entity':entity,'attribute':attr,'before':before,'after':after,'reason':'Restore original raw-HTML/MathML vector boldface, real-space blackboard bold, and original marker color/spacing where applicable; preserve migrated response structure and prose.','source':[f['source'] for f in e['fields'].values()]})
 coverage.append({'entity':q[':db/id'],'ma_id':e['ma_id'],'source_files':list(dict.fromkeys(f['source'] for f in e['fields'].values())),'prompt_formulas':len(e['fields']['problem']['current_formulas']),'solution_formulas':len(e['fields']['worked-solution']['current_formulas']),'answer_fields':len(q.get(':question/answer-fields',[])),'answer_choices':sum(len(f.get(':answer-field/choices',[])) for f in q.get(':question/answer-fields',[])),'changed_attributes':changes})
(OUT/'lines2d-proposals.json').write_text(json.dumps(proposals,ensure_ascii=False,indent=2)+'\n')
(OUT/'lines2d-formula-diffs.json').write_text(json.dumps(diffs,ensure_ascii=False,indent=2)+'\n')
(OUT/'lines2d-unmatched.json').write_text(json.dumps(unmatched,ensure_ascii=False,indent=2)+'\n')
(OUT/'lines2d-audit.json').write_text(json.dumps({'snapshot_basis':snap['basis'],'knowledge_point':kp[':db/id'],'coverage':coverage,'proposed_attributes':len(proposals),'formula_diffs':len(diffs),'unmatched_formulas':unmatched,'notes':['Canonical e-10974 already retains source boldface, blackboard bold and red failure markers with 1em spacing; alternative matrix syntax is equivalent.','All choices are statement-number text or boolean values; mathematical statement labels are audited against raw original prompt MathML.','Question checkbox migration wording is preserved.','Raw saved source HTML includes mixed SVG title TeX and MathML; both are consulted, never flattened capture text.']},ensure_ascii=False,indent=2)+'\n')
print('Proposals',len(proposals),'formula changes',len(diffs),'unmatched',len(unmatched));print(json.dumps(unmatched,ensure_ascii=False,indent=2))
missing=[];mathml=[]
for e in data:
 if e['ma_id'].startswith('e'):continue
 allcurrent=[]
 for field in ('problem','worked-solution'):allcurrent+=e['fields'][field]['current_formulas']
 for f in e['question'].get(':question/answer-fields',[]):allcurrent+=current(f[':answer-field/key']);allcurrent+=sum((current(a[':answer/value']) for a in f[':answer-field/choices']),[])
 for field,f in e['fields'].items():
  for s in f['source_formulas']:
   if sig(s) not in {sig(t) for t in allcurrent}:missing.append({'ma_id':e['ma_id'],'field':field,'source_formula':s})
  raw=read(ROOT/f['source']);mathml.append({'ma_id':e['ma_id'],'field':field,'variants':sorted(set(n.get('mathvariant') for n in raw.select('[mathvariant]'))),'colors':sorted(set(n.get('mathcolor') for n in raw.select('[mathcolor]'))),'spaces':sorted(set(n.get('width','') for n in raw.select('mspace')))})
assert not missing,missing
for p in proposals:
 assert formula.sub('<MATH>',p['before'])==formula.sub('<MATH>',p['after']),(p['entity'],'Prose change')
 assert [sig(f) for f in current(p['before'])]==[sig(f) for f in current(p['after'])],(p['entity'],'Math semantic change')
p=OUT/'lines2d-audit.json';a=json.loads(p.read_text());a['source_formula_omissions']=missing;a['raw_mathml_features']=mathml;a['validation']={'all_source_bank_formulas_accounted_for':True,'nonmath_prose_preserved':True,'all_modified_formulas_semantically_unchanged':True,'edb_mutation':False};p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
print('Reverse source coverage and prose/semantic preservation passed')
