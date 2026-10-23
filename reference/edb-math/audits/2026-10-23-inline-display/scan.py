"""Read-only formatting inventory at one EDB basis. Flags are review candidates."""
import collections,csv,hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from audit_math_image_imports import META,PARENTS
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import MATH
SNAPSHOT=ROOT/'.local/edb/math-image-import-audit-2026-10-23-inline-display-facts.jsonl'
INTEGRAL=re.compile(r'\\(?:int(?:op)?|iint|iiint|iiiint|idotsint|oint|oiint|oiiint)(?![A-Za-z])|[∫∬∭∮∯∰]')
BIG=re.compile(r'\\(?:sum|prod|coprod|lim|limsup|liminf|bigcup|bigcap)(?![A-Za-z])|[∑∏⋃⋂]')
ENV=re.compile(r'\\begin\{(?:[pbBvV]?matrix|array|aligned|align\*?|cases|gathered)\}')
PROSE={'question/problem','question/worked-solution','tutorial/content','answer/feedback','answer-field/feedback','multistep/context','answer/value','assigned-problem/instructions'}
def save(name,v):(HERE/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 records=collections.defaultdict(dict);parents=collections.defaultdict(set);qroles=collections.defaultdict(set);fields=[];facts=strings=mathcount=0;mathattrs=collections.Counter();all_integrals=collections.Counter()
 for row in map(json.loads,SNAPSHOT.open()):
  facts+=1;e,a,v=row['e'],row['a'],row['v']
  if a in META or a in ('answer/type','db/ident'):records[e][a]=v
  if a in PARENTS or a in ('question-generator/_knowledge-point',):parents[v].add(e)
  if a in ('knowledge-point/questions','knowledge-point/canonical-example'):qroles[v].add(a)
  if not isinstance(v,str):continue
  strings+=1
  if not INTEGRAL.search(v) and not BIG.search(v) and not ENV.search(v) and '\\frac' not in v and '\\sqrt' not in v:continue
  matches=[]
  # Skip code examples; their delimiters are documentation, not learner prose.
  masked=re.sub(r'```[\s\S]*?```|`[^`\n]*`',lambda m:' '*len(m[0]),v)
  for m in MATH.finditer(masked):
   whole=v[m.start():m.end()];display=whole.startswith(('$$',r'\['));body=whole[2:-2] if whole.startswith(('$$',r'\[',r'\(')) else whole[1:-1]
   mathcount+=1;mathattrs[a]+=1
   if INTEGRAL.search(body):all_integrals['display' if display else 'inline']+=1
   if display:continue
   lineleft=v[v.rfind('\n',0,m.start())+1:m.start()];n=v.find('\n',m.end());lineright=v[m.end():n if n>=0 else len(v)]
   standalone=not lineleft.strip() and not lineright.strip()
   integral=bool(INTEGRAL.search(body));explicit=bool(re.search(r'\\displaystyle\b',body));reasons=[]
   if integral:reasons.append('inline-integral-with-displaystyle' if explicit else 'inline-integral-without-displaystyle')
   if BIG.search(body):reasons.append('inline-large-operator')
   if ENV.search(body):reasons.append('inline-multiline-or-matrix')
   if body.count('\\frac')+body.count('\\dfrac')>=2 and len(body)>=40 or ('\\frac' in body or '\\dfrac' in body) and len(body)>=70:reasons.append('long-inline-fraction-expression')
   if '\\sqrt' in body and len(body)>=90:reasons.append('long-inline-radical-expression')
   if not reasons:continue
   matches.append({'start':m.start(),'end':m.end(),'math':whole,'tex':body,'standalone_line':standalone,'contains_displaystyle':explicit,'integral':integral,'reasons':reasons,'context':v[max(0,m.start()-100):min(len(v),m.end()+100)]})
  if matches:fields.append({**row,'value_sha256':hashlib.sha256(v.encode()).hexdigest(),'occurrences':matches,'prose_attribute':a in PROSE})
 def context(e):
  seen=set();todo=[e]
  while todo:
   n=todo.pop()
   if n in seen:continue
   seen.add(n);todo.extend(parents[n]);scope=records.get(n,{}).get('activity/scope')
   if scope:todo.append(scope)
  return [{'entity':n,**records[n]} for n in sorted(seen) if n in records]
 for f in fields:
  f['context']=context(f['e']);r=records.get(f['e'],{});f['role']='tutorial' if 'tutorial/id' in r else 'canonical-example' if 'knowledge-point/canonical-example' in qroles[f['e']] else 'practice-question' if 'question/id' in r else 'choice-or-feedback' if f['a'].startswith('answer') else 'other'
 integrals=[f for f in fields if f['prose_attribute'] and any(o['integral'] for o in f['occurrences'])];others=[f for f in fields if f['prose_attribute'] and any(not o['integral'] for o in f['occurrences'])];primary=[f for f in integrals if f['a']!='answer/value']
 occurrences=[(f,o) for f in primary for o in f['occurrences'] if o['integral']];without=[(f,o) for f,o in occurrences if not o['contains_displaystyle']];standalone=[(f,o) for f,o in occurrences if o['standalone_line']];topics={c['topic/math-academy-id'] for f in primary for c in f['context'] if 'topic/math-academy-id' in c}
 save('inline-integrals.json',integrals);save('other-display-candidates.json',others);save('non-prose-candidates.json',[f for f in fields if not f['prose_attribute']]);save('metadata.json',{str(e):r for e,r in records.items() if any(k.startswith(('topic/','knowledge-point/')) for k in r)})
 with (HERE/'inline-integrals.csv').open('w') as stream:
  w=csv.writer(stream);w.writerow(['entity','attribute','role','ma_id','topic_ids','topic_titles','inline_integrals','without_displaystyle','standalone_inline_integrals','current_t','source'])
  for f in primary:
   ints=[o for o in f['occurrences'] if o['integral']];own=records.get(f['e'],{});tc=[c for c in f['context'] if 'topic/math-academy-id' in c];w.writerow([f['e'],f['a'],f['role'],own.get('question/math-academy-id',own.get('tutorial/math-academy-id','')),';'.join(str(c['topic/math-academy-id']) for c in tc),';'.join(c.get('topic/title','') for c in tc),len(ints),sum(not o['contains_displaystyle'] for o in ints),sum(o['standalone_line'] for o in ints),f['t'],f['source']])
 summary={'database':'math','basis':json.loads(SNAPSHOT.with_suffix('.manifest.json').read_text())['basis_t'],'exported_facts_scanned':facts,'textual_values_scanned':strings,'primary_prose_inline_integral_entities':len({f['e'] for f in primary}),'primary_prose_inline_integral_fields':len(primary),'primary_prose_inline_integral_occurrences':len(occurrences),'inline_integrals_without_displaystyle':len(without),'entities_without_displaystyle':len({f['e'] for f,o in without}),'fields_without_displaystyle':len({(f['e'],f['a']) for f,o in without}),'inline_integrals_with_displaystyle':len(occurrences)-len(without),'standalone_line_inline_integrals':len(standalone),'standalone_without_displaystyle':sum(not o['contains_displaystyle'] for f,o in standalone),'topics_with_inline_integrals':len(topics),'primary_fields_by_attribute':dict(collections.Counter(f['a'] for f in primary)),'primary_fields_by_role':dict(collections.Counter(f['role'] for f in primary)),'primary_occurrences_by_tx':dict(collections.Counter(f['t'] for f,o in occurrences)),'other_candidate_fields':len(others),'other_candidate_entities':len({f['e'] for f in others}),'other_candidate_reasons':dict(collections.Counter(reason for f in others for o in f['occurrences'] if not o['integral'] for reason in o['reasons'])),'note':'Formatting candidates, not approved replacements. Explicit displaystyle is a lexical flag, not a proof of effective scope. Bare math answer values require a separate rendering policy.'}
 save('summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
