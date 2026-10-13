"""One-time extraction of complete source component masks; does not generate questions."""
import json, pathlib, shutil
P=pathlib.Path(__file__).parent; C=P.parents[1]/'runs/current'
for src,dst in [('sources/17592186129122.json','source.json'),('topics/17592186049872.json','topic.json'),('lessons/17592186049872.json','lesson.json')]:shutil.copyfile(C/src,P/dst)
s=json.load(open(P/'source.json'))['record']; qs=s[':knowledge-point/questions']
data=[
 ('rad_sine_fraction',1,6,5,3,-1,2,'rad','sin','fraction'),
 ('rad_cos_fraction',1,2,1,3,0,1,'rad','cos','multiplier'),
 ('rad_cos_integer',1,1,12,1,-1,6,'rad','cos','integer'),
 ('degree_sine_fraction',1,1,8,3,20,1,'degree','sin','fraction'),
 ('rad_sine_scaled_fraction',-3,1,3,4,1,3,'rad','sin','fraction'),
 ('degree_sine_scaled_fraction',-4,1,4,3,-45,1,'degree','sin','fraction'),
 ('degree_cos_integer',1,1,8,1,90,1,'degree','cos','integer'),
 ('degree_sine_integer',-2,1,9,1,-1,1,'degree','sin','integer')]
# Exact scalar-bank display masks, with all original scalar components independently supplied.
bank_values=[[(6,5),(1,2),(5,3),(1,6),(2,1)],[(1,3),(3,1),(1,1),(2,1),(6,1)],[],[],[(3,2),(4,3),(1,3),(8,3),(1,4)],[(300,1),(270,1),(480,1),(90,1),(120,1)],[(60,1),(30,1),(45,1),(15,1),(75,1)],[(90,1),(120,1),(30,1),(75,1),(40,1)]]
replacements=[
 [(r'\frac{1}{6}','@A@'),(r'\frac{5x}{3}','@BX@'),(r'-\frac{\pi }{2}','@C@')],
 [(r'\frac{1}{2}','@A@'),(r'\frac{1}{3}x','@BX@')],
 [('12x','@BX@'),(r'-\frac{\pi }{6}','@C@')],
 [(r'\frac{8x}{3}','@BX@'),('+{20}^{∘}','@C@')],
 [('-3\\operatorname','@A@\\operatorname'),(r'\frac{3x}{4}','@BX@'),(r'+\frac{\pi }{3}','@C@')],
 [('-4\\operatorname','@A@\\operatorname'),(r'\frac{4x}{3}','@BX@'),('-{45}^{∘}','@C@')],
 [('8x','@BX@'),('+{90}^{∘}','@C@')],
 [('-2\\operatorname','@A@\\operatorname'),('9x','@BX@'),('-{1}^{∘}','@C@')]]
specs={};cases=[]
for i,(q,d) in enumerate(zip(qs,data)):
 name,an,ad,bn,bd,cn,cd,unit,trig,bstyle=d; sid=q[':question/math-academy-id']
 params=dict(a_n=an,a_d=ad,b_n=bn,b_d=bd,c_n=cn,c_d=cd)
 prompt=q[':question/problem']
 for old,new in replacements[i]:assert old in prompt;prompt=prompt.replace(old,new)
 sol=q.get(':question/worked-solution')
 if sol:
  oldb=str(bn) if bd==1 else r'\frac{'+str(bn)+'}{'+str(bd)+'}'
  # Mask the whole last math expression independently, before masking B.
  last=sol.rsplit('$',2)[1];sol=sol.replace('$'+last+'$','$@PERIOD_STAGE@$',1)
  sol=sol.replace('$B='+oldb+'.$','$B=@B@.$')
 fields=q.get(':question/answer-fields');banks=[]
 for j,((on,od),a) in enumerate(zip(bank_values[i],fields[0][':answer-field/choices'] if fields else [])):
  text=a[':answer/value'];mode='degree' if unit=='degree' else 'unicode_fraction' if 'π' in text and '\\frac' in text else 'unicode_integer' if 'π' in text else 'pi_fraction' if '\\frac' in text else 'pi_integer'
  banks.append({'mode':mode,'original_value':text,'keys':list(a),'db_id':a[':db/id']});params[f'o{j}_n']=on;params[f'o{j}_d']=od
 specs[name]={'source_id':sid,'prompt_mask':prompt,'solution_mask':sol,'unit':unit,'trig':trig,'bstyle':bstyle,'a_style':'fraction' if ad>1 else 'integer' if an!=1 else 'unit','keys':list(q),'db_id':q[':db/id'],'banks':banks,'field':{'keys':list(fields[0]),'db_id':fields[0][':db/id']} if fields else None,'opaque':bool(banks),'source_parameters':params,'source_period_stage':q.get(':question/worked-solution','').rsplit('$',2)[1] if sol else None}
 cases.append({'source_id':sid,'template':name,'parameters':params,'bank_profile':'raw:'+sid,'authored_level':'easy','original_difficulty_present':':question/difficulty' in q})
(P/'template-masks.json').write_text(json.dumps(specs,indent=2,ensure_ascii=False)+'\n');(P/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False)+'\n')
# Frozen authoritative widget evidence, where present.
x=json.load(open('/home/jake/Developer/MA/DATA/Lessons/2062/Source/2062.json'));hits=[]
def walk(v):
 if isinstance(v,dict):
  if v.get('question_id') in ('53457','117580','117583'):hits.append(v)
  else:
   for w in v.values():walk(w)
 elif isinstance(v,list):
  for w in v:walk(w)
walk(x)
(P/'authoritative-widgets.json').write_text(json.dumps({'source_path':'/home/jake/Developer/MA/DATA/Lessons/2062/Source/2062.json','widgets':hits,'not_present':['117580','117583']},indent=2,ensure_ascii=False)+'\n')
slashes=[]
for q in qs:
 for k in (':question/problem',':question/worked-solution'):
  text=q.get(k,'');runs=[];run=0
  for c in text+'!':
   if ord(c)==92:run+=1
   elif run:runs.append(run);run=0
  slashes.append({'source_id':q[':question/math-academy-id'],'attribute':k,'present':k in q,'ord_backslash':92,'adjacent_backslash_runs':runs,'max_adjacent':max(runs,default=0)})
(P/'decoded-string-evidence.json').write_text(json.dumps(slashes,indent=2)+'\n')
