"""Build parameter masks once from captured source. Does not run during generation."""
import json,re,hashlib
from pathlib import Path
R=Path(__file__).parent
src=json.loads((R/'source.json').read_text()); qs=src['record'][':knowledge-point/questions']
configs={
'q-11732':('scalar_radio','easy',{'a':5,'b':2},{5:'a',2:'b'},3),
'q-1917':('natural_sum_radio','easy',{'b':4,'c':3},{4:'b',3:'c'},0),
'q-11735':('quadratic_radio','easy',{'b':6,'q':5,'l':6,'k':19},{6:'b_or_l',5:'q',10:'q2',19:'k'},2),
'q-17388':('natural_rate_radio','moderate',{'b':3,'c':5},{3:'b',5:'c',6:'c1'},1),
'q-304038':('linear_blank','easy',{'a':3,'b':8,'l':12,'k':10},{3:'a',8:'b',12:'l',10:'k'},0),
'q-340272':('constant_first_blank','easy',{'b':8,'a':2,'k':7},{8:'b',2:'a',7:'k'},0),
'q-340280':('cubic_rate_blank','moderate',{'b':5,'q':6,'l':4,'k':1},{5:'b',6:'q',4:'l',1:'k',18:'q3'},0),
}
# Identical source base/linear constants need role-aware complete component masks.
def mask(s,mapping,sid):
 if sid=='q-11735':
  # The literal 6 has two distinct roles; separate complete base exponent/log
  # components before constant tokenization. Only math expressions contain it.
  s=s.replace('{6}^{x}','{@@b@@}^{x}').replace('ln⁡6','ln⁡@@b@@')
  mapping=dict(mapping);mapping[6]='l'
 if sid=='q-340280':
  # Unit coefficient literals in 4(1), powers/evaluation zeros stay fixed.
  s=re.sub(r'(?<![A-Za-z])-1(?![0-9])','-@@k@@',s)
  s=s.replace(r'\text{d}x}(1)',r'\text{d}x}(@@k@@)')
  mapping=dict(mapping);del mapping[1]
 return re.sub(r'(?<![0-9_@])\d+(?![0-9_@])',lambda m:'@@'+mapping[int(m[0])]+'@@' if int(m[0]) in mapping else m[0],s)
masks={};cases=[]
for q in qs:
 sid=q[':question/math-academy-id'];template,level,p,mapping,correct=configs[sid];f=q[':question/answer-fields'][0]
 bank=[a[':answer/value'] for a in f[':answer-field/choices']]
 solution=q.get(':question/worked-solution')
 if not solution:
  if sid=='q-11732':solution='Applying the formula, we get\n\n$$\n\\begin{aligned}f^{′}(x)&=\\frac{\\text{d}}{\\text{d}x}(5 \\cdot 2^{x}) \\\\ &=5\\frac{\\text{d}}{\\text{d}x}(2^{x}) \\\\ &=5\\cdot 2^{x}\\ln 2 \\\\ &=5\\ln 2\\cdot 2^{x}.\\end{aligned}\n$$'
  else:solution='Applying the formula, we get\n\n$$\n\\begin{aligned}f^{′}(x)&=\\frac{\\text{d}}{\\text{d}x}(4^{x}+3e^{x}) \\\\ &=\\frac{\\text{d}}{\\text{d}x}(4^{x})+\\frac{\\text{d}}{\\text{d}x}(3e^{x}) \\\\ &=\\frac{\\text{d}}{\\text{d}x}(4^{x})+3\\frac{\\text{d}}{\\text{d}x}(e^{x}) \\\\ &=4^{x}\\ln 4+3e^{x}.\\end{aligned}\n$$'
 masks[template]={'level':level,'parameters':p,'prompt':mask(q[':question/problem'],mapping,sid),'solution':mask(solution,mapping,sid),'bank':[mask(s,mapping,sid) for s in bank],'correct_index':correct,'field_type':f[':answer-field/type'][':db/ident'].split('/')[-1],'key':f[':answer-field/key'],'source_id':sid,'solution_observed':':question/worked-solution' in q}
 cases.append({'source_id':sid,'source_uuid':q[':question/id'],'template':template,'level':level,'parameters':p,'profile':'observed','bank_profile':sid,'observed_difficulty':q.get(':question/difficulty',{}).get(':db/ident'),'original_correct_ref_present':':answer-field/correct' in f})
(R/'masks.json').write_text(json.dumps(masks,indent=2,ensure_ascii=False)+'\n')
(R/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
# Authoritative historical capture shows no source solutions/correct refs either.
a=json.loads(Path('/home/jake/Developer/MA/DATA/Lessons/1114/Source/1114.json').read_text())
items=[x for x in a['lesson']['items'] if x.get('question_id') in ('11732','1917')]
(R/'authoritative-widget-evidence.json').write_text(json.dumps({'path':'/home/jake/Developer/MA/DATA/Lessons/1114/Source/1114.json','sha256':hashlib.sha256(Path('/home/jake/Developer/MA/DATA/Lessons/1114/Source/1114.json').read_bytes()).hexdigest(),'items':items},indent=2)+'\n')
