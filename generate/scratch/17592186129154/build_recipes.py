import json,re,pathlib
D=pathlib.Path(__file__).parent
s=json.load(open(D/'source.json'))['record']
# All exact exponents below are defensible plotting representatives of visible categories,
# not recovered source formulas. Only q-38779's displayed intercept fixes amplitude.
anchors={
'q-38762':([-1,1,2],[1,1,2],1,[('even',2),('odd_pair',0,1),('value',2)]),
'q-38768':([-1,0,2],[2,1,2],1,[('even',1),('even_pair',0,2),('limit',1,1)]),
'q-112591':([-2,0,2],[1,3,2],1,[('simple',0),('odd',1),('even',2)]),
'q-112585':([-2,0,2],[1,3,1],-1,[('positive',),('limit',1,-1),('odd',1)]),
'q-112587':([-2,0,1],[1,2,1],-1,[('limit',-1,1),('value',0),('even',2)]),
'q-38680':([-3,-1,2],[1,3,1],-1,[('limit',1,-1),('simple',1),('even',2)]),
'q-38770':([-2,-1,2],[1,2,1],1,[('simple',2),('even',1),('limit',1,-1)]),
'q-38779':([-4,1,3],[2,1,2],'-1/48',[('odd',0),('value',3),('odd',1)]),
'q-80302':([-3,-1,2],[1,1,3],1,[('simple',1),('odd',2),('simple',2)]),
'q-80303':([-2,1,4],[1,3,1],1,[('even',0),('not_simple',1),('even',1)]),
}
recipes={}
for q in s[':knowledge-point/questions']:
 name=q[':question/math-academy-id']; roots,mult,c,claims=anchors[name]
 problem=q[':question/problem'];asset=re.search(r'!\[\]\((.*?)\)',problem).group(1)
 problem=problem.replace(asset,'{asset}')
 # Only complete root operands, never broad numeric or character replacement.
 def mask(text):
  if text is None:return None
  def rep(m):
   value=int(m.group(2));return m.group(1)+'{r'+str(roots.index(value))+'}'
  text=re.sub(r'(x\s*=\s*)(-?\d+)',rep,text)
  if name=='q-38762':text=text.replace('± 1','± {symmetric_root}')
  if name=='q-38779':
   text=re.sub(r'(p\(0\)\s*=\s*)3',r'\g<1>{y0}',text)
   text=text.replace('y=3','y={y0}')
  return text
 fields=q.get(':question/answer-fields',[])
 recipes[name]={'level':q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').rsplit('/',1)[-1],
  'unrated':':question/difficulty' not in q,'roots':roots,'multiplicities':mult,'coefficient':str(c),'claims':claims,
  'prompt_mask':mask(problem),'solution_mask':mask(q.get(':question/worked-solution')),'asset':asset,
  'source_id':q[':db/id'],'source_uuid':q[':question/id'],
  'field_present':':question/answer-fields' in q,'correct_present':bool(fields and ':answer-field/correct' in fields[0]),
  'bank':[a[':answer/value'] for a in fields[0][':answer-field/choices']] if fields else None,
  'key':fields[0][':answer-field/key'] if fields else None,'field_type':fields[0][':answer-field/type'][':db/ident'] if fields else None}
(D/'recipes.json').write_text(json.dumps(recipes,indent=2)+'\n')
