"""Build complete-component masks from frozen decoded source strings; no source writes."""
import json,re,pathlib
D=pathlib.Path(__file__).parent
qs=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']
names=['legacy_radian_radio','legacy_degree_radio','degree_unrepeated_radio','radian_negative_fraction_radio','radian_mixed_radio','axis_radian_radio','radian_repeated_radio','axis_zero_radio','radian_blank','degree_blank','degree_signed_blank','degree_signed_radio']
rs=['1','5','6','1/3','2','2','4','7','8','12','3','8'];angles=['5/3','330','315','5/4','7/4','3/2','4/3','0','7/4','60','240','150']
recipes={};cases=[]
for q,t,r,a in zip(qs,names,rs,angles):
 sid=q[':question/math-academy-id'];unit='radians' if 'radian' in t or t=='axis_zero_radio' else 'degrees'
 p=q[':question/problem'];m=re.search(r'origin is \$(.+?)\$',p);rt=m[1].rstrip(',');p=p[:m.start(1)]+'{{radius}}'+(',' if m[1].endswith(',') else '')+p[m.end(1):]
 m=re.search(r'angle of \$(.+?)\$',p);at=m[1];p=p[:m.start(1)]+'{{angle}}'+p[m.end(1):]
 rec={'source_id':sid,'level':'moderate','difficulty_present':':question/difficulty' in q,'prompt_mask':p,'fields':[],'original_radius_tex':rt,'original_angle_tex':at}
 for f in q[':question/answer-fields']:
  rec['fields'].append({'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'answer_type':f[':answer-field/choices'][0][':answer/type'][':db/ident'],'correct_present':':answer-field/correct' in f})
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];sol=sol.replace('r='+rt+',','r={{radius}},',1).replace(r'\theta ='+at+'.',r'\theta ={{angle}}.',1)
  blocks=list(re.finditer(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S));styles={}
  for coord,block in reversed(list(zip(('x','y'),blocks))):
   text=block[1];rows=text.split('\\\\');style={}
   for i,slot in ((1,'sub'),(2,'mul'),(3,'final')):
    row=rows[i];m=re.search(r'(&\s*=)(.*?)(\s*)$',row,re.S);rhs=m[2].strip()
    if slot=='sub':style['sub_mask']=rhs.replace(rt,'{{radius}}',1).replace(at,'{{angle}}',1)
    if slot=='mul':
     remainder=rhs[len(rt):]
     if remainder.startswith(r'\cdot '):prefix=r'\cdot ';rest=remainder[len(prefix):]
     else:prefix='';rest=remainder
     wrapped=rest.startswith('(') and rest.endswith(')');style['mul_prefix']=prefix;style['mul_wrapped']=wrapped;style['negative_numerator']=r'\frac{-' in rest
     # Preserve the source family condition: a negative unit value groups; a positive one uses cdot unless source always groups.
     style['always_wrapped']=t in ('radian_negative_fraction_radio','radian_blank','degree_blank','degree_signed_blank')
    rows[i]=row[:m.start(2)]+'{{'+coord+'_'+slot+'}}'+m[3]
   styles[coord]=style
   sol=sol[:block.start(1)]+'\\\\'.join(rows)+sol[block.end(1):]
  sol=re.sub(r'(Therefore,.*?are \$)(\([^$]*\))',lambda m:m[1]+'{{cartesian}}',sol,flags=re.S)
  rec['solution_mask']=sol;rec['styles']=styles
 recipes[t]=rec
 cases.append({'source_id':sid,'level':'moderate','template':t,'parameters':{'radius':r,'angle':a,'unit':unit},'bank_profile':'raw-'+sid,'level_origin':'observed' if rec['difficulty_present'] else 'authored evidence assignment; raw difficulty omitted'})
for t in ('legacy_radian_radio','legacy_degree_radio'):
 recipes[t]['normal_solution_mask']=recipes['degree_unrepeated_radio']['solution_mask'];recipes[t]['styles']=recipes['degree_unrepeated_radio']['styles'];recipes[t]['normal_solution_origin']='authored common source four-stage component solution; original lacks worked solution'
(D/'recipes.json').write_text(json.dumps(recipes,indent=2,ensure_ascii=False)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
