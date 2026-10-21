"""Prepare exact source-occurrence repairs; no EDB reads or writes."""
from pathlib import Path
import collections,hashlib,importlib.util,json,re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));import position_map as positions
s=importlib.util.spec_from_file_location('bulk_source_convert',HERE.parent/'secondary/convert_source.py');convert=importlib.util.module_from_spec(s);s.loader.exec_module(convert)

def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def controls(s):return re.findall(r'\{\{[^{}]+\}\}',s)
def images(s):return re.findall(r'!\[[^\]]*\]\([^\n]*?\)',s)
def wrap(old,tex):
 # Preserve math mode and punctuation without corrupting invisible right fences.
 stripped=old.strip()
 if stripped.startswith('$$'):
  end=stripped.rfind('$$');tail=stripped[end+2:]
  return '$$\n'+tex+'\n$$'+tail
 assert stripped.startswith('$') and stripped.count('$')>=2,('Unknown oldmathspan',old)
 end=stripped.rfind('$');tail=stripped[end+1:]
 if tail:
  visible_tail=re.sub(r'(?:\\right\.|\\end\{(?:array|aligned|cases)\}|[}\s])+$','',tex)
  if visible_tail.endswith(tail):tail=''
  elif tex.rstrip().endswith(tail) and not tex.rstrip().endswith(r'\right.'):
   tex=tex.rstrip()[:-len(tail)].rstrip()
 return '$'+tex+'$'+tail

def main():
 manual={r['source_occurrence_id']:r for r in json.loads((HERE/'manual-conversions.json').read_text())}
 rows=[json.loads(l) for l in (positions.AUDIT/'database/source-backed-candidates.jsonl').read_text().splitlines()]
 bound={(r['entity'],r['attribute']):r for r in json.loads((HERE/'bound.json').read_text())}
 exceptions={(r['entity'],r['attribute']):r for r in json.loads((HERE/'position-exceptions.json').read_text())}
 changes=[];decisions=[];conversions={}
 for row in rows:
  key=row['entity'],row['attribute'];decision={'entity':row['entity'],'attribute':row['attribute'],'source_occurrences':[s['id'] for s in row['source_occurrences']]}
  if key not in bound:
   decisions.append({**decision,'status':'needs-source-position-review','errors':[exceptions[key]['error']]});continue
  replacements=[];errors=[];unchanged=[]
  for span in bound[key]['spans']:
   record=positions.sources[span['source_occurrence_id']];converted=conversions.setdefault(record['id'],convert.convert_source(record))
   if record['id'] in manual and (converted['errors'] or record['id']=='3428:step-182411:340346'):
    converted={**converted,'tex':manual[record['id']]['tex'],'errors':[],'manual_source_review':manual[record['id']]['reason']}
    conversions[record['id']]=converted
   if converted['errors']:errors.append({'source_occurrence_id':record['id'],'errors':converted['errors']});continue
   new=wrap(span['old_markdown'],converted['tex'])
   if new==span['old_markdown']:unchanged.append(record['id']);continue
   replacements.append({**span,'before':span['old_markdown'],'after':new,'conversion':converted,
    'source_offset':record['source_offset'],'source_line':record['source_line'],'source_owner':record['dom_id'],
    'source_file_sha256':digest(positions.read_source(record['source_file'])[0]),
    'source_html_sha256_verified':digest(record['source_html'])==record['source_sha256']})
  after=row['current_value']
  for replacement in sorted(replacements,key=lambda r:r['start'],reverse=True):
   assert after[replacement['start']:replacement['end']]==replacement['before']
   after=after[:replacement['start']]+replacement['after']+after[replacement['end']:]
  assert controls(after)==controls(row['current_value']),(key,'answer control changed')
  assert images(after)==images(row['current_value']),(key,'image changed')
  if replacements:
   changes.append({'entity':row['entity'],'attribute':row['attribute'],'before':row['current_value'],'after':after,
    'before_sha256':digest(row['current_value']),'after_sha256':digest(after),'replacements':replacements,
    'preserved_answer_controls':controls(after),'preserved_images':images(after),'context':row['context']})
  decisions.append({**decision,'status':'partially-prepared' if replacements and errors else 'prepared' if replacements else 'needs-source-conversion-review' if errors else 'unchanged',
    'replacements':len(replacements),'errors':errors,'unchanged_occurrences':unchanged})
 (HERE/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
 (HERE/'decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n')
 (HERE/'conversions.json').write_text(json.dumps(list(conversions.values()),ensure_ascii=False,indent=2)+'\n')
 result={'candidate_fields':len(rows),'prepared_fields':len(changes),'replacement_occurrences':sum(len(r['replacements']) for r in changes),
  'decisions':dict(collections.Counter(r['status'] for r in decisions)), 'source_conversion_errors':dict(collections.Counter(e for r in conversions.values() for e in r['errors'])),
  'all_answer_control_tokens_preserved':True,'all_existing_image_tokens_preserved':True,'no_database_access':True,
  'files_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'position_map.py',HERE/'build.py',HERE.parent/'secondary/convert_source.py']}}
 (HERE/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
