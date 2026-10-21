import json,pathlib,itertools,math,copy,shutil,os,importlib.util,hashlib
from audit import g,fields,answer,independently_check,save
from pixel_probe import geometry
ROOT=pathlib.Path.cwd();JOB=ROOT.parent;PKG=JOB/'workspace'
source=json.load(open(JOB/'source/source.json'));cases={v['id']:v for v in json.load(open('source-analysis.json'))['source_cases']};records=json.load(open('source-replay-records.json'))
def distance(a,b):
 d=abs(a-b);return min(d,180-d)
replay=[]
for r,q in zip(records,source['material']['kp'][':knowledge-point/questions']):
 p=cases[q[':question/math-academy-id']]['points'];src=[]
 for a in q[':question/answer-fields'][0][':answer-field/choices']:
  d=geometry(pathlib.Path('/media/jake/SSD/EDB/math')/a[':answer/value'],p,'source');src.append({'asset':a[':answer/value'],'angles':[v['angle_degrees'] for v in d]})
 target=[]
 for a in fields(r)[':answer-field/choices']:
  d=json.load(open(pathlib.Path(a[':answer/value']).with_suffix('.json')));mp={tuple(pt):v for pt,v in zip(d['exact_points'],d['slopes'])};target.append({'asset':a[':answer/value'],'angles':[90 if mp[tuple(pt)]=='inf' else math.degrees(math.atan(float(__import__('fractions').Fraction(mp[tuple(pt)])))) for pt in p]})
 errors=[[max(distance(a,b) for a,b in zip(s['angles'],t['angles'])) for t in target] for s in src]
 perm=min(itertools.permutations(range(5)),key=lambda z:sum(errors[i][j] for i,j in enumerate(z)))
 row={'source_id':q[':question/math-academy-id'],'question_id':q[':question/id'],'prompt_exact':r['question'][':question/problem']==q[':question/problem'],'full_bank':[{'original':src[i],'generated':target[j],'max_angle_error_degrees':errors[i][j]} for i,j in enumerate(perm)],'max_angle_error_degrees':max(errors[i][j] for i,j in enumerate(perm))}
 assert row['max_angle_error_degrees']<3 and row['prompt_exact']
 # Compare instructional prose outside normalized substitution block and image URL.
 import re
 def prose(s):return re.sub(r'!\[\]\([^)]*\)','IMAGE',re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}','SUBSTITUTIONS',s,flags=re.S))
 if ':question/worked-solution' in q:
  row['solution_prose_preserved']=prose(q[':question/worked-solution'])==prose(r['question'][':question/worked-solution']);assert row['solution_prose_preserved']
 else:row['solution_prose']='Absent source key/solution; generated solution treated as inference.'
 replay.append(row)
save('source-bank-comparison.json',replay);print('source banks',[(r['source_id'],round(r['max_angle_error_degrees'],2)) for r in replay],flush=True)
manifest=json.load(open(PKG/'package.json'));rel=[]
for stem in ['relocation-a','nested/relocation-b']:
 dest=ROOT/stem;dest.mkdir(parents=True,exist_ok=True)
 for name in manifest['files']:
  p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PKG/name,p)
 out=ROOT/(stem.replace('/','-')+'-assets');os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(out)
 spec=importlib.util.spec_from_file_location('relocated_'+str(len(rel)),dest/manifest['entrypoint']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 r=m.generate('easy',seed=863981,template='affine_fraction');rel.append({'root':str(dest),'output':str(out),'record':r})
for rr in rel:
 assert all(pathlib.Path(a[':answer/value']).is_file() and pathlib.Path(a[':answer/value']).is_relative_to(rr['output']) for a in fields(rr['record'])[':answer-field/choices'])
normalized=[json.dumps(rr['record'],sort_keys=True).replace(rr['output'],'OUTPUT') for rr in rel];assert normalized[0]==normalized[1]
save('relocation-results.json',{'manifest':manifest,'normalized_identical':True,'records':rel,'command':'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python source_and_package.py'})
print('manifest-only relocation deterministic; all asset references resolve',flush=True)
