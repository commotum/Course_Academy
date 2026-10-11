"""Freeze reviewed choices and fresh source evidence. No DB writes."""
import copy,hashlib,json,re
from pathlib import Path
from bs4 import BeautifulSoup
from decisions import RADIO,SELECT
ROOT=Path(__file__).resolve().parent;OLD=ROOT.parent/'2026-10-10-held-next'
def read(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def value(c):return {k:c[k] for k in ('type','value')}
rows=read(OLD/'remaining-analysis/questions.json');raw=read(OLD/'recovery-input.json');held={q['math_academy_id'] for q in read(ROOT.parent/'held-questions.json')['questions']}
# These additional fields were manually read in the same full solutions, not adopted from an old agent label.
TEMPLATES={
(343289,'field-1'):('4','Coefficient multiplying W in the explicit W-prime=4W equality.'),
(343289,'field-2'):('C{e}^{4x}','General W before imposing W(0), explicitly W=C e^(4x) in the solution chain.'),
(343293,'field-1'):('-2x','Coefficient multiplying W in W-prime=-2xW.'),
(343293,'field-2'):('C{e}^{-{x}^{2}}','General W before imposing W(2), explicitly C e^(-x^2) in the solution chain.'),
(343295,'field-1'):('-3','Coefficient multiplying W in W-prime=-3W.'),
(343295,'field-2'):('C{e}^{-3x}','General W before imposing W(0), explicitly C e^(-3x) in the source chain.'),
(338907,'field-1'):(r'\frac{n}{3}','The source explicitly gives lambda_n=n/3 for n in N; this slot asks for the parameter, not its square.'),
(339145,'field-1'):('{e}^{{x}^{2}/12}','The source explicitly computes I(x)=e^(x^2/12) before solving the IVP.'),
(342960,'field-1'):(r'\frac{4-s}{(s+2)({s}^{2}+16)}','The source first solves for the complete Y(s) before partial fractions.'),
(342960,'field-3'):(r'\frac{3}{10}{e}^{-2t}-\frac{3}{10}\operatorname{cos}⁡4t-\frac{1}{10}\operatorname{sin}⁡4t','The final source y(t) expression has all three terms with signs +,-,-.'),
(343891,'field-2'):(r'\frac{x}{108\pi }\operatorname{sin}⁡(6\pi x)','Final resonant component y_p3 includes x/(108pi), sin, and argument 6pi x.'),
(343899,'field-2'):(r'\frac{x}{8\pi }\operatorname{sin}⁡(\pi x)','Final resonant component y_p2 includes x/(8pi) sin(pi x).'),
(343910,'field-2'):(r'-\frac{x}{27\pi }\operatorname{cos}⁡(3\pi x)','Final resonant component y_p3 includes negative x/(27pi) cos(3pi x).'),
}
review={};used={};grade_count=0
for n in sorted(set(RADIO)|set(SELECT)):
 mid=f'q-{n}';assert mid in held
 row=rows[mid];path=Path(row['directory']);rec=read(path/'state.json')['questions'][mid];before=rec['before']
 o=next(o for o in raw[mid]['occurrences'] if o['directory']==str(path));used[mid]={'occurrences':[o]}
 solstage=o['source_solution_stage'];sol=rec.get(solstage) or read(path/(('history-'+mid if solstage=='history' else mid+'-after')+'.json'))
 assert sol['worked_solution']==row['worked_solution']==o['worked_solution']
 assert (before.get('source_problem') or before['problem'])==row['source_problem']==o['source_problem']
 assert [(f['key'],f['type'],[value(c) for c in f['choices']]) for f in before['fields']]==[(f['key'],f['type'],[value(c) for c in f['choices']]) for f in o['before_fields']]
 loc={'file':str(path/'state.json'),'json_pointer':f'/questions/{mid}/{solstage}/worked_solution'}
 r={'directory':str(path),'category':'select_questions' if n in SELECT else row['category'],'fields':[],'source':':org/Math-Academy','review_method':'agent interpretation of saved MA solution; original field grading rechecked for other fields','source_problem':o['source_problem'],'source_quote':o['worked_solution'],'solution_location':loc,'source_hashes':{str(p):sha(p) for p in [path/'state.json',path/'content.json']},'before_layout_sha256':hashlib.sha256(json.dumps(before,sort_keys=True,ensure_ascii=False).encode()).hexdigest()}
 for f in before['fields']:
  key=f['key'];location=loc;quote=r['source_quote'];method='saved_worked_solution_with_manual_field_binding'
  if n in RADIO:
   assert len(before['fields'])==1;ix,note=RADIO[n]
  elif key in row['unconfirmed_fields']:
   assert len(row['unconfirmed_fields'])==1;ix,note=SELECT[n]
  elif (n,key) in TEMPLATES:
   val,note=TEMPLATES[n,key];matches=[i for i,c in enumerate(f['choices']) if c['value']==val];assert len(matches)==1,(mid,key,val);ix=matches[0]
   assert val in r['source_quote'],(mid,key,'reviewed full expression absent')
  else:
   # Require the fresh capture itself to explicitly identify the correct answer,
   # with the same DOM field and exact choice collection. Old audit labels grant no authority.
   sources=[]
   for stage in ['after','history']:
    for j,g in enumerate(rec.get(stage,{}).get('fields',[])):
     if g['key']!=key or not g.get('source_correct'):continue
     assert g['dom_id']==f['dom_id'] and [value(c) for c in g['choices']]==[value(c) for c in f['choices']],(mid,key,'version/field mismatch')
     sources.append((stage,j,g))
   assert sources,(mid,key,'no fresh direct grade or manual binding')
   answers={json.dumps(g['source_correct'],sort_keys=True) for _,_,g in sources};assert len(answers)==1
   stage,j,g=sources[0];answer=g['source_correct'];indices=[i for i,c in enumerate(f['choices']) if value(c)==answer];assert len(indices)==1
   ix=indices[0];location={'file':str(path/'state.json'),'json_pointer':f'/questions/{mid}/{stage}/fields/{j}/source_correct'}
   quote=json.dumps({'key':key,'dom_id':g['dom_id'],'source_correct':answer,'source_selected':g.get('source_selected'),'source_result':g.get('source_result')},ensure_ascii=False)
   note=f'The same captured DOM field {g["dom_id"]} explicitly displays source_correct; its full original choice list is identical to before-answer. This field binds to the unique {{{{{key}}}}} prompt slot.'
   method='fresh_captured_source_correct';grade_count+=1
  answer=value(f['choices'][ix]);assert answer['value'].strip(' $\n')
  if f['type']=='select':assert r['source_problem'].count('{{'+key+'}}')==1
  r['fields'].append({'key':key,'choice_index':ix,'answer':answer,'binding':note,'source_location':location,'source_quote':quote,'method':method})
 # Capture uses Roman ordered lists; Markdown extraction lost their labels.
 if n in {103178,122932,22428,66724}:
  soup=BeautifulSoup(before['html'],'html.parser');widget=soup.select_one('.questionWidget-text');lists=widget.select('ol');assert len(lists)==1 and len(lists[0].find_all('li',recursive=False))==3
  lines=r['source_problem'].splitlines();j=0
  for i,line in enumerate(lines):
   if line.startswith('- '):lines[i]=['I. ','II. ','III. '][j]+line[2:];j+=1
  assert j==3;r['restored_problem']='\n'.join(lines);r['layout_note']='Restore I/II/III labels from the original ordered list, preserving source statement order and all original choices.'
 review[mid]=r
save(ROOT/'answer-review.json',review);save(ROOT/'recovery-input.json',used)
save(ROOT/'radio-analysis-input.json',{'questions':{k:rows[k] for k in held if rows[k]['category']!='select_field_binding'}})
save(ROOT/'review-counts.json',{'questions':len(review),'radio':len(RADIO),'select':len(SELECT),'fields':sum(len(r['fields']) for r in review.values()),'fresh_direct_field_keys':grade_count})
save(ROOT/'disagreements.json',[
 {'question':'q-103178','issue':'Original option says ÍII only, solution says III only.','resolution':'Retain exact original option; unique third-statement binding supported by the source assessment of all three statements.','material_answer_conflict':False},
 {'question':'q-342410','issue':'In the x=-1 discussion the saved solution writes (x+1)^2 Q(x)=(x-1)^2 ln(x)/(x-3).','resolution':'Retain source solution verbatim; its explicit irregular-singular conclusion is unambiguous.','material_answer_conflict':False},
 {'question':'q-340883','issue':'Zero-valued initial segment is written with integration bounds 2 to 5 in an intermediate line.','resolution':'Retain source solution verbatim; both the final full transform and domain are explicit.','material_answer_conflict':False}
])
print(read(ROOT/'review-counts.json'))
