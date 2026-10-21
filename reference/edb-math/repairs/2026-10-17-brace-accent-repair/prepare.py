"""Compose source-proved brace repairs into CAS forms; never submits."""
import collections,difflib,hashlib,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from capture.scripts.database.edn import dumps,loads,kw
from scripts.question_capture.math_format import validate_prose
HERE=Path(__file__).resolve().parent;E=HERE/'evidence'
def save(n,v): (HERE/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str)+'\n')
def prepare():
 status=json.loads((E/'status.json').read_text())
 qs=loads((E/'questions.edn').read_text());ts=loads((E/'tutorials.edn').read_text());entities={v[':db/id']:v for v in qs+ts}
 census={}
 attrmap={1064:':tutorial/content',1071:':question/problem',1074:':question/worked-solution',1080:':answer/value',1081:':answer/feedback',1085:':multistep/context'}
 for p in E.glob('current-*.edn'):
  for e,a,v,tx,s,added in loads(p.read_text()):
   assert added and a in [1064,1071,1074]
   census[e,attrmap[a]]=v
 changes=[];seen=set();validation=[]
 for name,kind in [('structured','structured'),('flattened','source-recovered')]:
  for c in json.loads((HERE/name/'changes.json').read_text()):
   e,a,b,n=c['entity'],c['attribute'],c['before'],c['after'];key=e,a
   assert key not in seen;seen.add(key)
   assert census[key]==b==entities[e][a]
   assert b!=n and not re.search('[⏟⏞︷︸]',n)
   assert a in [':question/problem',':question/worked-solution',':tutorial/content']
   # Answer placeholders and image references remain byte-identical.
   for f in entities[e].get(':question/answer-fields',[]):
    token='{{'+f[':answer-field/key']+'}}';assert b.count(token)==n.count(token),(e,token)
   assert re.findall(r'!\[[^\]]*\]\([^)]+\)',b)==re.findall(r'!\[[^\]]*\]\([^)]+\)',n)
   errors={}
   for stage,value in [('before',b),('after',n)]:
    try:validate_prose(value)
    except ValueError as err:errors[stage]=str(err)
   assert not errors.get('after') or errors.get('before')==errors['after'],(key,errors)
   if errors:validation.append({'entity':e,'attribute':a,**errors})
   if kind=='source-recovered':
    assert hashlib.sha256(Path(c['sourcepath']).read_bytes()).hexdigest()==c['source_sha256']
   changes.append({'entity':e,'attribute':a,'before':b,'after':n,'repair_kind':kind,'evidence_file':name+'/changes.json','repaired_brace_occurrences':b.count('⏟')+b.count('⏞')})
 assert seen==set(census),(set(census)-seen,seen-set(census))
 changes.sort(key=lambda c:(c['entity'],c['attribute']))
 ids=sorted({c['entity'] for c in changes});forms=[[kw('db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']]for c in changes]
 for e in ids:forms.append([kw('db/ensure'),e,kw('tutorial/validate' if ':tutorial/id' in entities[e] else 'question/validate')])
 text='[\n'+'\n'.join(' '+dumps(f)for f in forms)+'\n]\n';assert loads(text)==forms
 (HERE/'transaction.edn').write_text(text);save('changes.json',changes)
 (HERE/'changes.diff').write_text(''.join(''.join(difflib.unified_diff(c['before'].splitlines(True),c['after'].splitlines(True),fromfile=str(c['entity'])+' '+c['attribute']+' before',tofile=str(c['entity'])+' '+c['attribute']+' after'))+'\n'for c in changes))
 sha=hashlib.sha256(text.encode()).hexdigest()
 source=loads((E/'source.edn').read_text());assert len(source)==1 and source[0][':db/ident']==':agent/codex'
 save('plan.json',{'database':status['database'],'lineage':status['lineage'],'snapshot_basis':status['basis'],'source':':agent/codex','source_eid':source[0][':db/id'],'changed_attributes':len(changes),'changed_entities':len(ids),'attributes':dict(collections.Counter(c['attribute']for c in changes)),'repair_kinds':dict(collections.Counter(c['repair_kind']for c in changes)),'repaired_brace_occurrences':sum(c['repaired_brace_occurrences']for c in changes),'transaction_sha256':sha,'transaction_bytes':len(text.encode()),'cas_forms':len(changes),'ensure_forms':len(ids),'preexisting_structural_findings':len(validation),'database_writes':0})
 save('structural-validation.json',{'no_new_structural_errors':True,'preexisting_findings':validation,'placeholder_keys_preserved':True,'image_references_preserved':True,'all_current_defects_covered':True,'no_raw_brace_glyphs_after':True})
 print((HERE/'plan.json').read_text())
if __name__=='__main__':prepare()
