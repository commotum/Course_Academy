"""Check every intended TeX span and alignment row against actual UI MathML, and UI option order."""
from review_lib import *
import xml.etree.ElementTree as ET
from probe_lib import predictions
records=load(E/'render-records.json');report=load(E/'render/rendering.json');assert len(report['cases'])==len(records)==27;assert report['passed']
def signature(t):
 t=t.replace('−','-').replace('⟹','⇒').replace('⟶','⇒').replace('⟺','⇔')
 t=re.sub(r'\\(?:begin|end)\{aligned\}','',t).replace(r'\Longrightarrow','⇒').replace(r'\dfrac',r'\frac')
 t=t.replace(r'\quad','').replace('&','');return re.sub(r'\s+','',t)
def flatten(n):
 tag=n.tag.split('}')[-1]
 if tag=='mfrac':return r'\frac{'+flatten(n[0])+'}{'+flatten(n[1])+'}'
 if tag=='mtable':return '\\\\'.join(flatten(c) for c in n)
 if tag=='mspace':return ''
 return (n.text or '')+''.join(flatten(c)+(c.tail or '') for c in n)
checks=[];ui_records=[];probes=[]
for i,r in enumerate(records):
 q=r['question'];html=(E/'render'/f'question-{i+1:03d}.html').read_text();blocks=re.findall(r'<mjx-assistive-mml[^>]*>(.*?)</mjx-assistive-mml>',html,re.S);observed=[signature(flatten(ET.fromstring(s))) for s in blocks]
 field=q[':question/answer-fields'][0];cs=field[':answer-field/choices'];key=observe(r)['key'];intended=[signature(m.group(1) or m.group(2)) for text in (q[':question/problem'],q[':question/worked-solution']) for m in re.finditer(r'\$\$(.*?)\$\$|\$([^$]+)\$',text,re.S)]+[signature(c[':answer/value']) for c in cs]+[signature(key)]
 assert Counter(observed)==Counter(intended),(i,Counter(intended)-Counter(observed),Counter(observed)-Counter(intended))
 expected_rows=sum(1+block.count('\\\\') for text in (q[':question/problem'],q[':question/worked-solution']) for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S));actual_rows=html.count('data-mml-node="mtr"');assert expected_rows==actual_rows,(i,expected_rows,actual_rows)
 ids=re.findall(r'<input type="radio"[^>]*value="([^"]+)"',html);assert len(ids)==5 and set(ids)=={c[':answer/id'] for c in cs};ui=copy.deepcopy(r);ui['question'][':question/answer-fields'][0][':answer-field/choices']=sorted(cs,key=lambda c:ids.index(c[':answer/id']));ui_records.append(ui)
 checks.append({'index':i,'id':q[':question/id'],'intended_math_spans_including_controls':len(intended),'observed_math_containers':len(observed),'expected_rows':expected_rows,'rendered_rows':actual_rows,'every_formula_and_row_matched':True,'ui_key_position':observe(ui)['target'],'screenshot':f'render/question-{i+1:03d}.png'})
for k,band in enumerate(('easy','moderate','hard')):
 group=ui_records[5*k:5*k+5];scores=Counter()
 for r in group:
  for name,idx in predictions(r).items():scores[name]+=idx==observe(r)['target']
 for name,correct in scores.items():
  probes.append({'cue':name,'subgroup':band+'/final/actual-UI','scope':'within_template','strategy':'Bank-only '+name+' with first-visible tie rule, after actual ui/learning.js choiceOrder. No given or keyed answer may be consulted.','correct':correct,'total':5,'baseline':0.2,'disposition':'not_predictive','conclusion':'Uniform five-option guessing baseline is 0.2. No tested UI ordering/bank cue answers all five final questions.','sample_refs':['render-records.json','ui-ordered-final-records.json','render-math-boundary.json']})
perfect=[p for p in probes if p['correct']==p['total']];save('ui-shortcut-probes.json',probes);assert not perfect,perfect
save('ui-ordered-final-records.json',ui_records[:15]);save('render-math-boundary.json',{'passed':True,'method':'Independent multiset equality between every authored TeX math span/control and actual MathJax assistive MathML; exact row counts from source aligned environments versus rendered mtr. Actual visible DOM audit also rejects raw TeX/code math.','cases':checks,'choice_order_source':'ui/learning.js:696-708; FNV hash of item ID, field ID and choice ID','limits':'Actual fixture item IDs are used; other learner task IDs may reorder choices. Bank/target dependencies are separately tested before shuffle.'})
print(json.dumps({'formula_checks':len(checks),'math_spans':sum(c['observed_math_containers'] for c in checks),'rows':sum(c['rendered_rows'] for c in checks),'ui_key_positions':{b:[observe(r)['target'] for r in ui_records[k*5:k*5+5]] for k,b in enumerate(('easy','moderate','hard'))},'ui_perfect_probes':len(perfect)}))
