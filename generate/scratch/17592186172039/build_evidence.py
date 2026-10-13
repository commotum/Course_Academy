"""Read-only source extraction and local review preparation; no DB operations."""
import importlib.util,json,re,pathlib,sys
sys.dont_write_bytecode=True
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.parent/(HERE.name+'.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=json.loads((HERE/'source.json').read_text())['record']
config={
'q-96767':('moderate','bilinear_open_thin','bank96767'),
'q-97483':('hard','parity_numbered','bank97483'),
'q-119766':('moderate','bilinear_closed','bank119766'),
'q-119769':('moderate','bilinear_closed','bank119769'),
'q-119774':('hard','parity_closed','bank119774'),
'q-97477':('moderate','bilinear_open','bank97477'),
'q-97482':('moderate','bilinear_open','bank97482'),
'q-97487':('hard','parity_open','bank97487'),
}
def parse_expr(expr):
 cleaned=expr.replace('{','').replace('}','')
 m=re.fullmatch(r'(-?\d*)x(\^2)?(y(\^2)?)?',cleaned)
 if not m:raise ValueError(expr)
 return {'c':int(m[1]) if m[1] not in ('','-') else -1 if m[1]=='-' else 1,'a':2 if m[2] else 1,'b':0 if not m[3] else 2 if m[4] else 1}
cases=[]
for q in s[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];level,template,profile=config[sid]
 expr=q[':question/problem'].split('$')[1].split('=')[1].strip()
 p=parse_expr(expr)
 claims=re.findall(r'At every point in the (first|second|third|fourth) quadrant, the slope of the slope field is (positive|negative)',q[':question/problem'])
 p['quadrants']=[{v:k for k,v in g.WORDS.items()}[a] for a,b in claims];p['claims']=[1 if b=='positive' else -1 for a,b in claims]
 cases.append({'source_id':sid,'level':level,'template':template,'parameters':p,'bank_profile':profile,'observed_difficulty':q.get(':question/difficulty',{}).get(':db/ident'),'repair':'Derived missing correct ref and authored solution; authored hard assignment' if sid=='q-97483' else None})
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
records=[];text=['# Originals and generated variants','Every generated record has one fixed worked solution. Source q97483 has no observed worked solution or correct marker; those additions are explicitly authored. The other seven source replays match whole prompt/solution strings.']
for case,q in zip(cases,s[':knowledge-point/questions']):
 r=g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters=case['parameters']);records.append(r)
 text += ['## Original '+case['source_id'],q[':question/problem'],'Original bank: '+', '.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']),q.get(':question/worked-solution','**No source solution or correct designation.**'),'### Parameterized replay'+(' (repaired)' if case['repair'] else ''),g.markdown(r)]
 for seed in [17,31]:
  r=g.generate(case['level'],seed=seed,template=case['template'],profile=case['bank_profile']);records.append(r)
  text+=['### Generated variant: '+case['template']+' / '+case['bank_profile']+' / seed '+str(seed),g.markdown(r)]
for level in ['easy','moderate','hard']:
 for seed in [43,58]:
  r=g.generate(level,seed);records.append(r);text+=['## Authored default '+level+' / seed '+str(seed),g.markdown(r)]
(HERE/'review.json').write_text(json.dumps(records,indent=2)+'\n');(HERE/'review.md').write_text('\n\n'.join(text)+'\n')
# Snapshot widget, authoritative for layout/bank but without correct designation.
lesson=json.load(open('/home/jake/Developer/MA/DATA/Lessons/3352/Source/3352.json'))
def walk(obj):
 if isinstance(obj,dict):
  if obj.get('question_id')=='97483':return obj
  for val in obj.values():
   found=walk(val)
   if found:return found
 elif isinstance(obj,list):
  for val in obj:
   found=walk(val)
   if found:return found
widget=walk(lesson);assert widget
(HERE/'q97483-widget.json').write_text(json.dumps(widget,indent=2)+'\n')
