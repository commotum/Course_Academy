import json,hashlib,copy,importlib.util,re,math,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path('generate/scratch/17592186096649-draft');root=D.resolve().parents[2]
s=importlib.util.spec_from_file_location('val',D/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
legacy=D.with_name('17592186096649')/'plots';assetmap={}
for p in legacy.glob('*.png'):
 if 'patch_vertices_pixels' in json.loads(p.with_suffix('.json').read_text()):assetmap[hashlib.sha256(p.read_bytes()).hexdigest()]=p
c=json.loads((D/'source.json').read_text());ind=[q for q in c['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q];rows=[{'label':'authored '+str(i),'record':r} for i,r in enumerate(json.loads((D/'review.json').read_text()))];checked=[];repairs=[]
for q in ind:
 raw=copy.deepcopy(q);f=raw[':question/answer-fields'][0];raw[':question/difficulty']=raw[':question/difficulty'][':db/ident'];level=raw[':question/difficulty'].split('/')[-1];f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
 r={'question':raw,'knowledge_point':{'db_id':17592186096649,'id':'dc49f831-8e1d-5fb4-8952-1dd4ee3bfa02','title':'Creating Parallel Vectors'},'generation':{'actual_difficulty':level,'eligible_for_learning':True,'template':'pair' if level=='hard' else 'single'}}
 rows.append({'label':'existing independent '+raw[':question/id'],'record':copy.deepcopy(r)})
 mappings={}
 for p in re.findall(r'!\[\]\((.*?)\)',raw[':question/problem']+raw[':question/worked-solution'])+[a[':answer/value'] for a in f[':answer-field/choices']]:
  file=Path('/media/jake/SSD/EDB/math')/p;sha=hashlib.sha256(file.read_bytes()).hexdigest();assert sha in assetmap,p;mappings[p]=str(assetmap[sha])
 for key in (':question/problem',':question/worked-solution'):
  for p,x in mappings.items():raw[key]=raw[key].replace(p,x)
 for a in f[':answer-field/choices']:a[':answer/value']=mappings[a[':answer/value']]
 v.mathematics(r)
 pimage=re.findall(r'!\[\]\((.*?)\)',raw[':question/problem'])[0];avec=v.from_plot(pimage)['vectors'][0]['vector'];angle=int(round(math.degrees(math.atan2(avec[1],avec[0]))))%360;length=str(int(round(math.hypot(*avec))));scales=[str(v.parse_scalar(x)) for x in re.findall(r'\$(.*?)\$',raw[':question/problem'].split('Which of the following diagrams shows ')[1])]
 repaired=v.g.generate(level,parameters={'angle':angle,'length':length,'scales':scales});assert re.sub(r'!\[\]\(.*?\)','<diagram>',raw[':question/worked-solution'])==re.sub(r'!\[\]\(.*?\)','<diagram>',repaired['question'][':question/worked-solution']);repairs.append({'original_question_id':q[':question/id'],'reason':'Legacy600px image canvas exceeded the player choice cap and displayed at a different pixel scale from the prompt; compact180px replacement preserves the task, full bank and worked prose.','record':repaired});rows.append({'label':'repaired existing '+q[':question/id'],'record':repaired})
 checked.append({'question_id':q[':question/id'],'level':level,'images_exactly_match_legacy_rendered_assets':len(mappings),'mathematics':'pass'})
rows += [{'label':'inferred source completion '+str(i),'record':r} for i,r in enumerate(json.loads((D/'source-completions.json').read_text()))]
for q in c['record'][':knowledge-point/questions'][:2]:
 q=copy.deepcopy(q)
 for f in q[':question/answer-fields']:
  f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
 rows.append({'label':'raw MA '+q[':question/math-academy-id'],'record':{'question':q}})
q=copy.deepcopy(c['record'][':knowledge-point/canonical-example']);q[':question/answer-fields']=[];rows.append({'label':'canonical exact preserved prose and stage illustrations','record':{'question':q}})
(D/'supported-presentation-repairs.json').write_text(json.dumps(repairs,indent=2)+'\n');(D/'independent-validation.json').write_text(json.dumps(checked,indent=2)+'\n');(D/'visual-records.json').write_text(json.dumps(rows,indent=2)+'\n');print(len(checked),'independent banks validated;',len(rows),'browser rows')
