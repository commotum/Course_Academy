import json,re,collections,importlib.util
from pathlib import Path
p=Path('generate/reports/checkbox-discovery-2026-10-12');r=json.loads((p/'report.json').read_text());m={q[':db/id']:q for q in json.loads((p/'readiness-metadata.json').read_text())}
spec=importlib.util.spec_from_file_location('screen',p/'screen.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
LABEL=r'(?:III|II|I|IV|V|VI|VII|VIII|IX|X|[A-Z])'
def atoms(problem):
 explicit=list(re.finditer(r'(?m)^\s*(?:-\s+)?(?:\*\*)?('+LABEL+r')[.)](?:\*\*)?\s+',problem))
 bullets=list(re.finditer(r'(?m)^\s*[-•]\s+',problem))
 matches=explicit if explicit else bullets
 if not 2<=len(matches)<=5:return None
 labels=[x.group(1)for x in explicit] if explicit else ['I','II','III','IV','V'][:len(matches)]
 if len(set(labels))!=len(labels):return None
 bodies=[problem[x.end():matches[i+1].start() if i+1<len(matches) else len(problem)].strip() for i,x in enumerate(matches)]
 if any(not b or re.search(r'\b(?:select all|which of|determine which|choose|answer)\b',b,re.I)for b in bodies):return None
 if len(set(bodies))!=len(bodies):return None
 return [{'label':l,'text':b}for l,b in zip(labels,bodies)]
accepted=[];counts=collections.Counter()
for q in r['strong_candidates']:
 if q['review_flags']:counts['existing review flag']+=1;continue
 if not m[q['id']].get(':question/difficulty'):counts['unrated']+=1;continue
 if not re.search(r'\bwhich\b[\s\S]{0,120}\bstatements\b[\s\S]{0,60}\b(?:true|false)\b',q['problem'],re.I):counts['not explicit statements true/false']+=1;continue
 a=atoms(q['problem'])
 if a is None:counts['case extraction requires review']+=1;continue
 labels={x['label']for x in a};f=q['fields'][0]
 parsed=[s.subset(x[':answer/value'])for x in f[':answer-field/choices']]
 if any(not isinstance(x,list)or not set(x)<=labels for x in parsed):counts['option labels not explicit finite subsets']+=1;continue
 key=s.subset(f[':answer-field/correct'][':answer/value'])
 if not isinstance(key,list)or not set(key)<=labels:counts['key requires review']+=1;continue
 accepted.append({**q,'atomic_options':a,'correct_labels':key,'difficulty':m[q['id']][':question/difficulty'][':db/ident']})
(p/'direct-format-provisional.json').write_text(json.dumps(accepted,indent=2)+'\n')
print('accepted',len(accepted),'excluded',dict(counts))
print('\n'.join(f'{n} | {id} | {title}'for (id,title),n in collections.Counter((k['id'],k['title'])for q in accepted for k in q['kps']).most_common()))
for q in accepted[:6]:print(json.dumps({k:q[k]for k in ('id','problem','atomic_options','correct_labels')},ensure_ascii=False))
