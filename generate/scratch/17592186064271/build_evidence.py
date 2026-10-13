import json,shutil,pathlib
D=pathlib.Path(__file__).parent
src=pathlib.Path('generate/runs/current/sources/17592186064271.json')
shutil.copyfile(src,D/'source.json')
s=json.loads(src.read_text());qs=s['record'][':knowledge-point/questions']
names=['farmer','pail','website','reward','cupcake','milk','battery','currency','coffee']
params=[dict(u='ton',v='dollar'),dict(u='centimeter',v='second'),dict(u='visitor',v='hour'),dict(u='dollar',v='point'),dict(u='gram',v='cupcake',alt='kilogram'),dict(u='dollar',v='liter',alt='milliliter'),dict(u='hour',v='minute'),dict(u='euro',v='dollar'),dict(u='degree Fahrenheit',v='minute')]
# Each term is a complete displayed unit expression; fixed recipe exponents
# and plural/style choices reconstruct every source choice exactly.
def t(s,p=1,plural=True,style='prefix'):return [s,p,plural,style]
def frac(a,b):return [a,b]
banks=[
 [[t('v',1,False),t('u',2,False,'suffix')],frac(t('v',1,False),t('u',1,False)),[t('u')],[t('v')],frac(t('u'),t('v',1,False))],
 [[t('v')],frac(t('u'),t('v',1,False)),[t('u')],frac(t('u',3),t('v',1,False)),frac(t('v'),t('u',3,False))],
 [frac(t('u'),t('v',1,False)),[t('u')],[t('v')],frac(t('v'),t('u',1,False)),frac(t('u',2),t('v',1,False))],
 [frac(t('u'),t('v',1,False)),[t('u')],[t('v')],frac(t('v'),t('u',1,False)),frac(t('u',2),t('v',1,False))],
 [frac(t('alt',2),t('v',1,False)),frac(t('v'),t('alt',1,False)),frac(t('alt'),t('v',1,False)),frac(t('u'),t('v',1,False)),frac(t('v'),t('u',1,False))],
 [frac(t('alt'),t('u',2,False)),frac(t('u'),t('v',1,False)),frac(t('v'),t('u',1,False)),frac(t('u'),t('alt',1,False)),frac(t('u',3),t('v',2))],
 [[t('u',2)],frac(t('u'),t('v',1,False)),[t('v')],[t('u')],frac(t('v'),t('u',1,False))],
 [[t('v')],frac(t('u'),t('v',1,False)),frac(t('v'),t('u',2,False,'suffix')),frac(t('v'),t('u',1,False)),[t('u')]],
 [frac(t('u'),t('v',1,False)),[t('u')],frac(t('v'),t('u')), [t('v')],frac(t('u',2,True,'suffix'),t('v',1,False))],
]
eligible=[dict(u=['ton','kilogram'],v=['dollar','euro']),dict(u=['centimeter','meter'],v=['second','minute','hour']),dict(u=['visitor'],v=['hour','minute','second']),dict(u=['dollar','euro'],v=['point']),dict(u=['gram','kilogram'],v=['cupcake'],alt=['gram','kilogram']),dict(u=['dollar','euro'],v=['liter','milliliter'],alt=['liter','milliliter']),dict(u=['hour'],v=['minute','second']),dict(u=['euro'],v=['dollar']),dict(u=['degree Fahrenheit'],v=['minute','second','hour'])]
# Complete lexical slots only, longest expressions first. No variable-symbol
# replacement occurs, so TeX commands/function labels cannot be corrupted.
unit_lex={'gram':'grams','kilogram':'kilograms','centimeter':'centimeters','second':'seconds','visitor':'visitors','hour':'hours','dollar':'dollars','point':'points','cupcake':'cupcakes','liter':'liters','milliliter':'milliliters','minute':'minutes','euro':'euros','ton':'tons','degree Fahrenheit':'degrees Fahrenheit'}
def singular(k):return k
out={};cases=[]
for name,q,p,bank,domain in zip(names,qs,params,banks,eligible):
 prompt=q[':question/problem'];sol=q.get(':question/worked-solution','')
 if not sol:
  fn,x=('w','p') if name=='farmer' else ('V','t')
  u='tons' if name=='farmer' else 'cubic centimeters';v='dollars per ton' if name=='farmer' else 'seconds'
  d=r'\frac{\text{d}'+fn+r'}{\text{d}'+x+'}'
  ratio=(r'\frac{\text{tons}}{\text{dollars per ton}}=\frac{\text{squared tons}}{\text{dollars}}' if name=='farmer' else r'\frac{\text{cubic centimeters}}{\text{seconds}}')
  answer='squared tons per dollar' if name=='farmer' else 'cubic centimeters per second'
  sol=f'We have that ${fn}({x})$ is measured in {u} and ${x}$ is measured in {v}. \n\n$$\n'+r'\begin{aligned}'+fn+'('+x+'): & '+r'\text{'+u+r'} \\ '+x+r': & \text{'+v+r'}\end{aligned}'+'\n$$\n\n'+f'The derivative ${d}$ measures a change in ${fn}({x})$ over a change in ${x}.$ So, it represents a ratio of the units:\n\n$$\n'+r'\begin{aligned}'+d+': & '+ratio+r'\end{aligned}'+'\n$$\n\n'+f'Therefore, ${d}$ is measured in "{answer}".'
 lexical=[]
 for slot,k in p.items():
  for power in (1,2,3):
   for plural in (True,False):
    for style in ('prefix','suffix'):
     base=unit_lex[k] if plural else k
     text=base if power==1 else (('squared ' if power==2 else 'cubic ')+base if style=='prefix' else base+(' squared' if power==2 else ' cubed'))
     lexical.append((text,slot,power,plural,style))
 lexical.sort(key=lambda x:-len(x[0]));tokens=[];used=set()
 import re
 for text,slot,power,plural,style in lexical:
  if text in used:continue
  used.add(text);tok='@@'+str(len(tokens))+'@@'
  pat=r'(?<![A-Za-z])'+re.escape(text)+r'(?![A-Za-z])'
  if re.search(pat,prompt) or re.search(pat,sol):
   prompt=re.sub(pat,tok,prompt);sol=re.sub(pat,tok,sol);tokens.append([tok,slot,power,plural,style])
 out[name]={'source_id':q[':question/math-academy-id'],'parameters':p,'eligible':domain,'prompt':prompt,'solution':sol,'tokens':tokens,'bank':bank,'u_power':3 if name=='pail' else 1,'v_power':1,'bank_origin':'authored missing-field repair' if name in ('website','reward') else 'observed','capital_bank':name=='coffee'}
 cases.append({'source_id':q[':question/math-academy-id'],'template':name,'level':'hard' if name=='farmer' else 'easy','parameters':p,'bank_profile':'raw_observed' if name=='farmer' else 'observed'})
(D/'templates.json').write_text(json.dumps(out,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
# Preserve only relevant authoritative widgets with their external provenance.
ma=json.load(open('/home/jake/Developer/MA/DATA/Lessons/296/Source/296.json'))
widgets=[]
def walk(x):
 if isinstance(x,dict):
  if x.get('question_id') in ('48557','48613'):widgets.append(x)
  else:
   for y in x.values():walk(y)
 elif isinstance(x,list):
  for y in x:walk(y)
walk(ma)
(D/'authoritative-widgets.json').write_text(json.dumps({'path':'/home/jake/Developer/MA/DATA/Lessons/296/Source/296.json','widgets':widgets,'missing_widget_ids':['110040','72091']},indent=2)+'\n')
