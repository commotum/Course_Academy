"""Remove generator-added invisible exponents and redundant answer fences."""
import copy, json, re, shutil
from fractions import Fraction
from pathlib import Path
from scripts.generator_packages import build_manifest,manifest_digest,verify_package
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
PHANTOM=re.compile(r'\^\{\\phantom\{\d+\}\}')
def clean_answer(value):
 text=PHANTOM.sub('',value)
 # All affected choices are positive products. Keep parentheses precisely
 # where a displayed exponent applies to the enclosed factor.
 stack=[];remove=[]
 for token in re.finditer(r'\\left\(|\\right\)',text):
  if token[0]==r'\left(':stack.append(token.span())
  else:
   assert stack
   opening=stack.pop()
   if not re.match(r'\s*\^',text[token.end():]):
    remove.extend([opening,token.span()])
 assert not stack
 for start,end in sorted(remove,reverse=True):text=text[:start]+text[end:]
 assert '\\phantom' not in text
 return text
class Exact:
 """Restricted exact arithmetic for these positive product/fraction banks."""
 def __init__(self,text):self.text=re.sub(r'\s+','',text.replace(r'\left','').replace(r'\right',''));self.i=0
 def take(self,token):
  if self.text.startswith(token,self.i):self.i+=len(token);return True
  return False
 def atom(self):
  if self.take(r'\frac'):
   a=self.group();b=self.group();x=a/b
  elif self.take('('):
   x=self.product();assert self.take(')')
  elif self.text[self.i]=='{':x=self.group()
  else:
   m=re.match(r'\d+',self.text[self.i:]);assert m,(self.text,self.i)
   x=Fraction(int(m[0]));self.i+=len(m[0])
  if self.take('^'):
   n=self.group();assert n.denominator==1;x=x**int(n)
  return x
 def group(self):
  assert self.take('{'),(self.text,self.i)
  x=self.product();assert self.take('}');return x
 def product(self):
  x=self.atom()
  while self.take(r'\times') or self.take(r'\cdot'):x*=self.atom()
  return x
 def value(self):
  x=self.product();assert self.i==len(self.text),(self.text,self.i);return x

def patch_generator(path):
 old=path.read_text();text=old
 if 'def practice_texts(p):' in text:
  start=text.index('def practice_texts(p):');end=text.index('@checked_math_content',start)
  text=text[:start]+text[end:]
  text=text.replace('    if source is None: texts=practice_texts(p)\n','')
  text=text.replace("VERSION = '1.1.0'","VERSION = '1.1.1'")
  path.write_text(text)
 assert r'\phantom' not in text and 'practice_texts(' not in text
 return old!=text

def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def run():
 before=json.loads((HERE/'all-questions.json').read_text());after=copy.deepcopy(before);changes=[];values=[]
 for [q] in after:
  for f in q.get(':question/answer-fields',[]):
   for a in f[':answer-field/choices']:
    old=a[':answer/value']
    if '\\phantom' not in old:continue
    new=clean_answer(old)
    old_math=Exact(PHANTOM.sub('',old)).value();new_math=Exact(new).value();assert old_math==new_math
    a[':answer/value']=new
    if f[':answer-field/correct'][':db/id']==a[':db/id']:f[':answer-field/correct'][':answer/value']=new
    changes.append({'question':q[':db/id'],'entity':a[':db/id'],'attribute':':answer/value','before':old,'after':new})
    values.append({'answer':a[':db/id'],'value_before':str(old_math),'value_after':str(new_math)})
 save('changes.json',changes);save('all-questions-after.json',after);save('exact-mathematics.json',{'passed':True,'choices':values})
 kp=next(k for k in json.loads((HERE/'topic.json').read_text())[0][0][':topic/knowledge-points'] if k[':db/id']==17592186129111)
 gen=kp[':knowledge-point/question-generator'];ref=gen[':question-generator/script'];original=Path('/media/jake/SSD/EDB/math')/Path(ref).parent
 package=verify_package(original,Path(ref).parts[2]);dest=HERE/'generator';dest.mkdir(exist_ok=True)
 for name in package.manifest['files']:shutil.copyfile(original/name,dest/name)
 patch_generator(dest/'generator.py')
 workspaces=[]
 for script in (ROOT/'.local/learning').rglob('workspace/generator.py'):
  text=script.read_text()
  if '17592186129111' in text and 'def practice_texts(p):' in text:
   workspaces.append({'script':str(script.relative_to(ROOT)),'changed':patch_generator(script)})
 manifest=build_manifest(dest,package.entrypoint,package.manifest['files'],dependencies=package.manifest['dependencies']);digest=manifest_digest(manifest)
 save('generator-manifest.json',manifest);save('generator-update.json',{'entity':gen[':db/id'],'old_reference':ref,'new_reference':f'generators/{digest[:2]}/{digest}/{package.entrypoint}','digest':digest,'workspaces':workspaces})
 affected={c['question'] for c in changes}
 render=[{'question':q} for [q] in after if q[':db/id']==17592186576428]
 render.extend({'question':q} for [q] in after if q[':db/id'] in affected and q[':db/id']!=17592186576428)
 save('render-input.json',render)
 print(json.dumps({'audited':len(before),'affected_questions':len(affected),'answers_repaired':len(changes),'generator_drafts_patched':len(workspaces)}))
if __name__=='__main__':run()
