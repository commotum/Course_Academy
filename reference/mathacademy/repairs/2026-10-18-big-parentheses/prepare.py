"""Prepare a formatting-only lesson repair and updated generator package."""
import copy, importlib.util, json, re, shutil
from pathlib import Path
from scripts.generator_packages import build_manifest,manifest_digest,verify_package
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('fraction_formatter',ROOT/'scripts/question_capture/math_format.py')
fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def strip_sizes(s): return s.replace(r'\left(', '(').replace(r'\right)', ')')

def run():
 changes=[]; questions=json.loads((HERE/'questions.json').read_text())
 after=copy.deepcopy(questions)
 def field(entity,key):
  before=entity.get(key)
  if not isinstance(before,str):return
  # Touch only math spans for prose; answers are bare TeX.
  new=fmt.MATH.sub(lambda m: fmt.scalable_fraction_parentheses(m[0]),before) if key!=':answer/value' else fmt.scalable_fraction_parentheses(before)
  assert strip_sizes(new)==strip_sizes(before)
  if new!=before:
   entity[key]=new;changes.append({'entity':entity[':db/id'],'attribute':key,'before':before,'after':new})
 for [q] in after:
  field(q,':question/problem'); field(q,':question/worked-solution')
  for f in q.get(':question/answer-fields',[]):
   for a in f.get(':answer-field/choices',[]):field(a,':answer/value');field(a,':answer/feedback')
 tutorials=[s[':step/content'] for [l] in json.loads((HERE/'lessons.json').read_text()) for s in l[':activity/steps'] if ':tutorial/content' in s[':step/content']]
 for t in tutorials:field(t,':tutorial/content')
 save('changes.json',changes);save('questions-after.json',after);save('tutorials-after.json',tutorials)
 old=json.loads((HERE/'topics.json').read_text())[0][0][':topic/knowledge-points'][0][':knowledge-point/question-generator'][':question-generator/script']
 source=ROOT/'reference/mathacademy/repairs/2026-10-18-big-parentheses/generator'
 original=Path('/media/jake/SSD/EDB/math')/Path(old).parent
 package=verify_package(original,Path(old).parts[2])
 source.mkdir(exist_ok=True)
 for name in package.manifest['files']:shutil.copyfile(original/name,source/name)
 function=(ROOT/'scripts/question_capture/math_format.py').read_text().split('def scalable_fraction_parentheses(text):')[1].split('def normalize_tex(value):')[0]
 def patch_helper(path):
  text=path.read_text()
  if 'def scalable_fraction_parentheses(text):' not in text:
   text=text.replace('def normalize_tex(value):','def scalable_fraction_parentheses(text):'+function+'def normalize_tex(value):')
   text=text.replace('text = _matrix_layouts(_legacy_commands(text))','text = scalable_fraction_parentheses(_matrix_layouts(_legacy_commands(text)))')
   path.write_text(text)
  assert 'text = scalable_fraction_parentheses(_matrix_layouts(_legacy_commands(text)))' in text
 patch_helper(source/'math_format.py')
 (source/'generator.py').write_text((source/'generator.py').read_text().replace("VERSION = '1.0.0'", "VERSION = '1.0.1'"))
 workspaces=[]
 for path in (ROOT/'.local/learning').rglob('workspace/generator.py'):
  text=path.read_text()
  if not any(k in text for k in ('17592186105742','17592186105743','17592186105744')):continue
  helper=path.with_name('math_format.py')
  if helper.is_file():
   before=helper.read_bytes();patch_helper(helper)
   workspaces.append({'script':str(path.relative_to(ROOT)),'kp':next(k for k in ('17592186105742','17592186105743','17592186105744') if k in text),'helper_changed':before!=helper.read_bytes()})
 manifest=build_manifest(source,package.entrypoint,package.manifest['files'],dependencies=package.manifest['dependencies'])
 save('generator-manifest.json',manifest)
 save('generator-update.json',{'entity':17592186576549,'old_reference':old,'new_reference':f'generators/{manifest_digest(manifest)[:2]}/{manifest_digest(manifest)}/{package.entrypoint}','digest':manifest_digest(manifest),'workspaces':workspaces})
 print(json.dumps({'questions_audited':len(questions),'questions_changed':len({c['entity'] for c in changes if c['attribute'].startswith(':question/')}),'fields_changed':len(changes),'tutorials':len(tutorials),'workspace_generators_patched':len(workspaces),'new_package':manifest_digest(manifest)},indent=2))
if __name__=='__main__':run()
