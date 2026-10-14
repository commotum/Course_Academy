import importlib.util,json,hashlib,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
rows=[];plots=[]
for mid,spec in g.SPECS.items():
 q=g.ORIGINALS[mid]
 ref=__import__('re').search(r'!\[\]\(([^)]+)\)',q[':question/problem']).group(1)
 original=Path('/media/jake/SSD/EDB/math')/ref;copy=HERE/'source-plots'/original.name;shutil.copyfile(original,copy)
 plots.append({'source_id':mid,'reference':ref,'original_path':str(original),'copied_path':str(copy),'sha256':hashlib.sha256(copy.read_bytes()).hexdigest(),'dimensions':[360,304]})
 rows.append({'source_id':mid,'source_db_id':q[':db/id'],'template':spec['family'],'level':'moderate','parameters':{'scale':1} if mid in ['q-18051','q-18052'] else {'points':spec['points']},'bank_profile':'evidence:'+mid,'observed_level':q.get(':question/difficulty'),'attribute_presence':{k:k in q for k in [':question/answer-fields',':question/difficulty',':question/worked-solution',':question/requires-calculator']},'authored_replay_level':':question/difficulty' not in q})
(HERE/'source-cases.json').write_text(json.dumps(rows,indent=2)+'\n')
(HERE/'source-plot-manifest.json').write_text(json.dumps(plots,indent=2)+'\n')
ind=[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Authored homogeneous scaling of q-18051 or q-18052, five-choice radio, supplied correct key/solution/moderate rating. Useful current inventory; not original MA difficulty or distractor-intent evidence.'} for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
(HERE/'independent-inventory.json').write_text(json.dumps({'database':g.SOURCE['database'],'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'questions':ind},indent=2)+'\n')
for row in rows:
 r=g.generate(row['level'],template=row['template'],profile=row['bank_profile'],parameters=row['parameters'])
 q=g.ORIGINALS[row['source_id']]
 assert r['question'][':question/problem']==q[':question/problem'],row['source_id']
 assert r['question'].get(':question/worked-solution')==q.get(':question/worked-solution'),row['source_id']
 print(row['source_id'],r['question'].keys())
for level in ['easy','moderate','hard']:
 r=g.generate(level,1);print(level,r['generation']['template'],r['generation']['parameters'])
