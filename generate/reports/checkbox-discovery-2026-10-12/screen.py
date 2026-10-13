"""Conservative structural screen; candidate status requires semantic review."""
import collections,json,re
from pathlib import Path
OUT=Path(__file__).resolve().parent
LABEL=r'(?:X|IX|VIII|VII|VI|V|IV|III|II|I|[A-Z])'
def subset(text):
 text=re.sub(r'\$|\*\*','',text).strip().rstrip('.')
 if re.fullmatch(r'(?:None|Neither|All)(?: (?:of )?(?:the |these )?(?:above|statements|listed|given statements|following|options))?',text,re.I):return text.lower()
 tokens=re.findall(r'\b'+LABEL+r'\b',text)
 rest=re.sub(r'\b'+LABEL+r'\b|\b(?:and|or|only|both|Neither|neither|Statements?|statements?)\b|[,\s&]', '',text)
 return tokens if tokens and not rest else None

def main():
 records=[]
 for path in sorted((OUT/'sources').glob('*.json')):
  try:records.append(json.loads(path.read_text()))
  except json.JSONDecodeError:continue
 questions={};members=collections.defaultdict(list)
 for kp in records:
  for q in kp.get(':knowledge-point/questions',[]):
   questions[q[':db/id']]=q;members[q[':db/id']].append(kp)
 groups=collections.defaultdict(list);types=collections.Counter()
 for eid,q in sorted(questions.items()):
  fs=q.get(':question/answer-fields',[]);fts={f.get(':answer-field/type',{}).get(':db/ident')for f in fs}
  types[','.join(sorted(fts))or'fieldless']+=1
  if fts and fts <= {':answer-field.type/checkbox'}:continue
  radios=[f for f in fs if f.get(':answer-field/type',{}).get(':db/ident')in (':answer-field.type/radio',':answer-field.type/select')]
  values=[a.get(':answer/value','')for f in radios for a in f.get(':answer-field/choices',[])]
  problem=q.get(':question/problem','');listed=re.findall(r'(?m)^\s*(?:-\s+)?(?:\*\*)?('+LABEL+r')[.)]',problem)
  bullets=re.findall(r'(?m)^\s*[-•]\s+',problem)
  parsed=[subset(v)for v in values]
  composite=any(isinstance(s,list)and len(s)>1 for s in parsed)
  reasons=[];bucket=None
  if radios and values and all(s is not None for s in parsed) and (composite or len(listed)>1):
   bucket='subset_banks';reasons.append('Label combination response bank')
  elif radios and any(re.search(r'\b(?:all|both|neither|none) of (?:the |these )?(?:above|following|statements)|\bboth [A-D] and [A-D]|\b(?:I|II|III) and (?:I|II|III)\b',v,re.I)for v in values):
   bucket='combined_prose';reasons.append('Combination/none/all prose option')
  elif radios and any(re.search(r'\b(?:and|or)\b',v)for v in values) and not all(v.startswith('Any ')for v in values):
   bucket='set_values';reasons.append('Multiple values or objects in a radio option')
  elif (not fs or radios) and (len(listed)>1 or len(bullets)>1 or re.search(r'\bselect all|\bwhich of (?:the |these )?(?:following|given).*(?:true|false|satisf|is|are)',problem,re.I|re.S)):
   bucket='listed_or_selection';reasons.append('Listed cases or selection instruction')
  if bucket:
   groups[bucket].append({'id':eid,'ma_id':q.get(':question/math-academy-id'),'kps':[{'id':k[':db/id'],'title':k[':knowledge-point/title'],'topics':k.get(':topic/_knowledge-points',[])}for k in members[eid]],'problem':problem,'fields':fs,'values':values,'parsed_subsets':parsed,'listed_labels':listed,'reasons':reasons,'image':bool(re.search(r'!\[',problem))})
 r={'captured_kps':len(records),'practice_questions_screened':len(questions),'field_shapes':dict(types),'bucket_counts':{k:len(v)for k,v in groups.items()},'buckets':groups}
 (OUT/'screening.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='buckets'},indent=2))
if __name__=='__main__':main()
