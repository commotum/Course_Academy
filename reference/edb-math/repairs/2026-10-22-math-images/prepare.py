"""Build the exact CAS repair; replace formula images only and preserve other bytes."""
import collections,hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];RAW=ROOT/'.local/edb/math-image-import-audit-2026-10-22';AUDIT=ROOT/'reference/edb-math/audits/2026-10-22-math-images'
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import dumps,kw
IMAGE=re.compile(r'!\[[^\]]*\]\((images/[0-9a-f]{2}/[0-9a-f]{64}\.(?:svg|png))\)')
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def save(name,v):(HERE/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 assert not (HERE/'commit-intent.json').exists(),'A persisted request already exists; do not recompute it'
 assert json.loads((HERE/'remaining-assets.json').read_text())==[]
 findings=json.loads((AUDIT/'findings.json').read_text());replacements=json.loads((HERE/'validated-replacements.json').read_text());fields=[];forms=[];counts=collections.Counter()
 for f in findings:
  before=f['v'];assert digest(before)==f['value_sha256'];math={i['path'] for i in f['math_images']};edits=[]
  def replace(m):
   if m[1] not in math:return m[0]
   tex=replacements[m[1]]['tex'];assert tex and not re.search(r'<(?:mjx|math|span|svg|title)\b',tex)
   lineleft=before[before.rfind('\n',0,m.start())+1:m.start()];rightend=before.find('\n',m.end());lineright=before[m.end():rightend if rightend>=0 else len(before)]
   display=not lineleft.strip() and not lineright.strip()
   value='$$\n'+tex+'\n$$' if display else '$'+tex.replace('\r','')+'$'
   edits.append({'asset':m[1],'before_start':m.start(),'before_end':m.end(),'original':m[0],'replacement':value,'display':display})
   counts['display' if display else 'inline']+=1
   return value
  after=IMAGE.sub(replace,before)
  assert len(edits)==len(f['math_images']),(f['e'],f['a'],len(edits),len(f['math_images']))
  assert not math.intersection(re.findall(r'images/[0-9a-f]{2}/[0-9a-f]{64}\.(?:svg|png)',after))
  # Check preservation independently by rebuilding from the original spans.
  cursor=0;pieces=[]
  for edit in edits:pieces.extend([before[cursor:edit['before_start']],edit['replacement']]);cursor=edit['before_end']
  pieces.append(before[cursor:]);assert ''.join(pieces)==after
  remaining_before=[m[0] for m in IMAGE.finditer(before) if m[1] not in math];remaining_after=[m[0] for m in IMAGE.finditer(after)];assert remaining_before==remaining_after
  field={'entity':f['e'],'attribute':f['a'],'before':before,'after':after,'before_sha256':digest(before),'after_sha256':digest(after),'original_t':f['t'],'edits':edits}
  fields.append(field);forms.append([kw('db/cas'),f['e'],kw(f['a']),before,after]);counts['preserved_genuine_image_references']+=len(remaining_before)
 save('fields.json',fields);text=dumps(forms)+'\n';(HERE/'transaction.edn').write_text(text)
 (HERE/'read-query.edn').write_text('[:find ?entity ?attr ?value :in $ [[?entity ?attr]] :where [?entity ?attr ?value]]\n');(HERE/'read-inputs.edn').write_text(dumps([[[f['entity'],kw(f['attribute'])] for f in fields]])+'\n')
 summary={'database':'math','audited_basis':5565,'fresh_snapshot_basis':5637,'fields':len(fields),'entities':len({f['entity'] for f in fields}),'formula_image_occurrences':sum(len(f['edits']) for f in fields),'distinct_assets':len(replacements),'attributes':dict(collections.Counter(f['attribute'] for f in fields)),**dict(counts),'transaction_sha256':digest(text),'forms':'CAS for existing scalar content attributes only','outside_formula_image_spans_unchanged':True,'genuine_image_references_preserved':True}
 save('preparation.json',summary);print(json.dumps(summary))
if __name__=='__main__':main()
