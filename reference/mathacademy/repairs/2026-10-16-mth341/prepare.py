"""Prepare the authorized format-only repair; never submit or alter a saved request."""
import collections,hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
AUDIT=ROOT/'reference/mathacademy/audits/2026-10-16-mth341'
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import dumps,kw
from math_format import normalize_tex,normalize_prose,validate_tex,validate_prose,FORMAT_VERSION

def save(n,data):(HERE/n).write_text(json.dumps(data,indent=2,default=str)+'\n')
assert not (HERE/'commit-intent.json').exists(),'Never overwrite a retained transaction request'
fields=json.loads((AUDIT/'fields.json').read_text());entities=json.loads((AUDIT/'entities.json').read_text())
manual_path=HERE/'manual-display/changes.json';image_path=HERE/'image-recovery/replacements.json'
manual=json.loads(manual_path.read_text()) if manual_path.exists() else []
if isinstance(manual,dict):manual=manual['changes']
manual={(c['entity'],c['attribute']):c for c in manual}
images=json.loads(image_path.read_text()) if image_path.exists() else {}
if isinstance(images,list):images={x['path']:x for x in images}
if 'replacements' in images:images=images['replacements']
changes=[];expected=[];issues=[];used_images=collections.Counter();applied_manual=set()
for f in fields:
 key=f['entity'],f['attribute'];before=f['value'];after=before;reasons=[]
 if key in manual:
  c=manual[key];assert c['before']==before,key
  after=c['after'];reasons.append('manual-display');applied_manual.add(key)
 def image_replace(match):
  path=match[1]
  if path not in images:return match[0]
  item=images[path];tex=item if isinstance(item,str) else item.get('tex',item.get('latex'))
  assert isinstance(tex,str) and tex,path
  used_images[path]+=1
  return '\n\n$$\n'+tex+'\n$$\n\n'
 converted=re.sub(r'!\[[^\]]*\]\(([^)]+)\)',image_replace,after)
 if converted!=after:reasons.append('formula-image');after=converted
 normalize=normalize_tex if f['kind']=='math' else normalize_prose
 validate=validate_tex if f['kind']=='math' else validate_prose
 try:
  normalized=normalize(after)
  if normalized!=after:
   # Avoid changes solely to display whitespace in otherwise correct content.
   if re.sub(r'\s+','',normalized)!=re.sub(r'\s+','',after) or reasons:
    after=normalized;reasons.append('canonical-tex')
  validate(after)
 except Exception as ex:issues.append({'entity':key[0],'attribute':key[1],'error':str(ex)})
 expected.append({**f,'value':after})
 if before!=after:changes.append({'entity':key[0],'attribute':key[1],'before':before,'after':after,'kind':f['kind'],'topics':f['topics'],'reasons':reasons})
assert applied_manual==set(manual),(set(manual)-applied_manual)
save('changes.json',changes);save('expected-fields.json',expected);save('preparation-issues.json',issues)
save('preparation-summary.json',{'basis':3078,'format':FORMAT_VERSION,'fields':len(fields),'changes':len(changes),'entities':len({c['entity'] for c in changes}),'attributes':dict(collections.Counter(c['attribute'] for c in changes)),'manual_fields':len(manual),'converted_image_assets':len(used_images),'image_occurrences':sum(used_images.values()),'issues':len(issues)})
print((HERE/'preparation-summary.json').read_text())
if '--final' not in sys.argv:sys.exit(0)
assert manual and images,'Wait for both manual and image recovery evidence'
assert not issues,issues
expected_images={x['path'] for x in json.loads((AUDIT/'images.json').read_text()) if x['classification']=='formula'}
assert set(used_images)==expected_images,(set(used_images)^expected_images)
# No field identities, answer keys, question membership, or missing solutions change.
allowed={':tutorial/content',':question/problem',':question/worked-solution',':answer/value',':answer/feedback',':multistep/context'}
assert all(c['attribute'] in allowed and isinstance(c['before'],str) for c in changes)
forms=[[kw('db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in changes]
for eid in sorted({c['entity'] for c in changes}):
 e=entities[str(eid)];kind=next(k for k in ['question','answer','tutorial','multistep'] if ':'+k+'/id' in e)
 forms.append([kw('db/ensure'),eid,kw(kind+'/validate')])
(HERE/'transaction.edn').write_text(dumps(forms)+'\n')
(HERE/'read-query.edn').write_text('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]')
(HERE/'read-inputs.edn').write_text(dumps([[[c['entity'],kw(c['attribute'])] for c in changes]]))
(HERE/'expected.edn').write_text(dumps([[c['entity'],kw(c['attribute']),c['after']] for c in changes]))
print('Prepared',len(forms),'CAS and ensure forms; no database changes')
