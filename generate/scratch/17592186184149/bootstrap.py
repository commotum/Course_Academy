import json,re,pathlib
P=pathlib.Path(__file__).parent
s=json.load(open(P/'source.json'))['record'];qs=s[':knowledge-point/questions']
Bs=['1/2','2','3','1/4','2','1/3','2','1/2','3','4','2/5','2/3','3/5','3']
Cs=['1/8','-1/3','-1/7','1/8','1/6','-1/12','-1/3','1/4','1/4','-2/5','-1/5','1/6','-1/5','1/4']
configs={};cases=[]
for q,b,c in zip(qs,Bs,Cs):
 sid=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1];fn='cot' if 'cot' in q[':question/problem'] else 'tan'
 config={'source_id':sid,'level':level,'B':b,'c':c,'fn':fn,'math_components':[], 'banks':[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']], 'correct':q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']}
 for role in ['problem','worked-solution']:
  text=q[':question/'+role];im=re.findall(r'!\[\]\((.*?)\)',text)[0];config[role+'_asset']='/media/jake/SSD/EDB/math/'+im
  text=text.replace('![]('+im+')','![]({{'+('prompt_plot' if role=='problem' else 'solution_plot')+'}})')
  def component(m):
   full=m.group();display=full.startswith('$$');body=full[2:-2] if display else full[1:-1];trim=body.strip();tag=None
   if 'begin{aligned}' in trim:tag='factor_block'
   elif '⟹' in trim:tag='calculation'
   elif trim.startswith('y='):
    if '+C)' in trim:tag='formula'
    elif '+\\frac{C' in trim or '+2C' in trim or '+3C' in trim or '+4C' in trim or '+\\frac{5C' in trim or '+\\frac{3C' in trim:tag='factored'
    else:tag='baseline'
   elif trim.startswith('x+'):tag='factor'
   elif '<C<' in trim:tag='bound'
   elif trim in ['C','C?']:tag='constant'
   elif 'units to' in text[m.end():m.end()+20]:tag='distance'
   else:tag='answer'
   idx=len(config['math_components']);config['math_components'].append({'tag':tag,'original':body,'display':display,'bare_baseline':trim.startswith('y=tan\\,') or trim.startswith('y=cot\\,'),'subtraction':'=' in trim and tag=='distance'})
   return ('$$' if display else '$')+'{{math_'+str(idx)+'}}'+('$$' if display else '$')
  text=re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)',component,text,flags=re.S)
  text=text.replace('units to the left','units to the {{direction}}').replace('units to the right','units to the {{direction}}')
  config[role+'_mask']=text
 configs[sid]=config;cases.append({'source_id':sid,'template':fn+'_shift','parameters':{'B':b,'c':c,'fn':fn},'bank_profile':'observed:'+sid,'level':level})
(P/'recipes.json').write_text(json.dumps(configs,indent=2,ensure_ascii=False)+'\n');(P/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
