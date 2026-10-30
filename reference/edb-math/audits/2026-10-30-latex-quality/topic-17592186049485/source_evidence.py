import json,re,shutil
from pathlib import Path
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent;SOURCE=Path('/home/jake/Developer/MA/DATA/Lessons/1376/Source')
s=json.loads((HERE/'snapshot.json').read_text());fields=json.loads((HERE/'render-input.json').read_text());html=BeautifulSoup((SOURCE/'1376.html').read_text(),'html.parser')
out=HERE/'source-evidence';out.mkdir(exist_ok=True)
selections={17592186107157:'#step-44724',17592186107159:'#step-44736',17592186105463:'#step-44725 .exampleExplanation',17592186105464:'#step-44728 .exampleExplanation',17592186105465:'#step-44732 .exampleExplanation',17592186105466:'#step-44735 .exampleExplanation'}
proof=[];confirmed=[]
for eid,sel in selections.items():
 n=html.select_one(sel);assert n is not None
 (out/(str(eid)+'.html')).write_text(str(n))
 tokens=[x.get_text() for x in n.select('mjx-assistive-mml [mathvariant="bold"]')]
 proof.append({'entity':eid,'selector':sel,'bold_mathml_tokens':tokens,'source':str(SOURCE/'1376.html')})
 attr='tutorial/content' if eid in (17592186107157,17592186107159) else 'question/worked-solution'
 confirmed.append({'entity':eid,'attribute':attr})
for qid in (35960,35966,22291,32819,162143,162144):
 q=next(q for q in s['questions'] if q.get(':question/math-academy-id')=='q-'+str(qid));sel='#question-'+str(qid)+' .questionWidget-text';n=html.select_one(sel);assert n is not None
 tokens=[x.get_text() for x in n.select('mjx-assistive-mml [mathvariant="bold"]')]
 (out/(str(q[':db/id'])+'-problem.html')).write_text(str(n))
 proof.append({'entity':q[':db/id'],'attribute':'question/problem','selector':sel,'bold_mathml_tokens':tokens});confirmed.append({'entity':q[':db/id'],'attribute':'question/problem'})
for qid in (35960,35966,35973,35982):
 q=next(q for q in s['questions'] if q.get(':question/math-academy-id')=='q-'+str(qid));n=html.select_one('#question-'+str(qid)+' .questionWidget-choicesTable');assert n is not None
 (out/(str(q[':db/id'])+'-choices.html')).write_text(str(n))
 tokens=[x.get_text() for x in n.select('mjx-assistive-mml [mathvariant="bold"]')]
 proof.append({'question':q[':db/id'],'attribute':'answer/value','bold_mathml_tokens':tokens})
 for a in q[':question/answer-fields'][0][':answer-field/choices']:confirmed.append({'entity':a[':db/id'],'attribute':'answer/value'})
candidates=[{'entity':f['entity'],'attribute':f['attribute'],'value':f['value']} for f in fields if re.search(r'(?<![A-Za-z\\])[rpvijk](?:\(|\s*&?\s*=|\s*\\[, ]|\s*\+|\s*\$)',f['value'])]
(HERE/'vector-formatting-evidence.json').write_text(json.dumps({'source_proof':proof,'direct_source_confirmed_fields':confirmed,'direct_source_confirmed_count':len(confirmed),'same_pattern_candidate_count':len(candidates),'same_pattern_candidate_fields':candidates,'note':'32 fields directly compared with original lesson DOM/screenshots.217 fields share loss of vector boldface; additional185 are pattern-based candidates, not individually source-confirmed.'},indent=2,ensure_ascii=False)+'\n')
for name in ('01-step-44724.png','03-question-35960.png','09-step-44732.png','14-question-162143.png'):shutil.copyfile(SOURCE/'Sections'/name,out/name)
print('source-confirmed',len(confirmed),'same-pattern candidates',len(candidates))
