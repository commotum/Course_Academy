"""Compare original compound formulas with one pinned EDB content projection."""
from pathlib import Path
import collections,html,json,re,sys,xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from capture.scripts.database.edn import loads,kw
from scripts.question_capture.math_format import MATH
import importlib.util
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('compound_source_audit',HERE/'audit.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
base_tex=a.tex

def tex(node):
 tag=node.tag.rsplit('}',1)[-1]
 if tag=='mtable':return r'\begin{matrix}'+r' \\ '.join(' & '.join(tex(c) for c in row) for row in node)+r'\end{matrix}'
 return base_tex(node)
a.tex=tex

def matrices(title):
 result=[];errors=[]
 for math in a.MML.findall(title):
  try:
   root=ET.fromstring(math);parent={child:node for node in root.iter() for child in node}
   for table in root.findall('.//{*}mtable'):
    surrounding=parent.get(table)
    if surrounding is None:continue
    brackets=''.join(''.join(c.itertext()) for c in surrounding if c.tag.rsplit('}',1)[-1]=='mo')
    if not (('[' in brackets and ']' in brackets) or ('(' in brackets and ')' in brackets) or '|' in brackets or surrounding.tag.rsplit('}',1)[-1]=='mfenced'):continue
    rows=[[tex(c) for c in row if c.tag.rsplit('}',1)[-1]=='mtd'] for row in table]
    if rows and rows[0] and len({len(r) for r in rows})==1:result.append({'rows':rows,'signature':a.matrix_signature(rows)})
  except (ET.ParseError,ValueError) as error:errors.append(str(error))
 return result,errors

def formula_norm(text):
 text=html.unescape(text)
 for env,left,right in [('bmatrix','[',']'),('pmatrix','(',')'),('vmatrix','|','|'),('Vmatrix','|','|')]:
  text=text.replace('\\begin{'+env+'}',left).replace('\\end{'+env+'}',right)
 text=re.sub(r'\\(?:begin|end)\{(?:matrix|aligned|gathered|align\*?)\}','',text)
 text=re.sub(r'<[^>]+>','',text)
 text=text.replace('$$','').replace('$','').replace(r'\(', '').replace(r'\)','').replace(r'\[','').replace(r'\]','').replace('\u2061','')
 return a.norm(text)

records={}
for kind in ['tutorial','question']:
 for row in loads((HERE/(kind+'-current.edn')).read_text()):
  item=row[0];records[(kind,item[kw(kind+'/math-academy-id')])]=item
rows=json.loads((HERE/'source-candidates.json').read_text());findings=[];review=[];complete=[];unimported=[]
for candidate in rows:
 c={k:v for k,v in candidate.items() if k not in ['sourceTitleHtml','matrices','conversionErrors']}
 item=records.get((c['kind'],c['sourceId']))
 if item is None:unimported.append(c);continue
 c['entity']=item[kw('db/id')]
 texts=[item.get(kw(c['attribute']), '')]
 if c['attribute']=='answer/value':texts=[ch.get(kw('answer/value'),'') for f in item.get(kw('question/answer-fields'),[]) for ch in f.get(kw('answer-field/choices'),[])]
 texts=[str(text) for text in texts if text]
 if not texts:review.append({**c,'reason':'No current content for the source section'});continue
 expected,errors=matrices(candidate['sourceTitleHtml'])
 if expected:
  signatures=[m['signature'] for m in expected]
  first=signatures[0]
  comparisons=[]
  labels=re.findall(r'(?<![A-Za-z])([A-Za-z])\s*=\s*FORMULA',c['outerTex'])
  for text in texts:
   actual=a.current_matrices(text)
   missing=[m for m in expected if m['signature'] not in actual]
   missing_labels=[label for label in labels if not re.search(r'(?<![A-Za-z])'+re.escape(label)+r'\s*(?:&\s*)?=',text)]
   comparisons.append((first in actual,missing,missing_labels,text))
  intact=next((part for part in comparisons if not part[1] and not part[2]),None)
  if intact:complete.append(c);continue
  confirmed=next((part for part in comparisons if part[0] and (part[1] or part[2])),None)
  if confirmed:
   c.update({'reason':'missing_matrices' if confirmed[1] else 'missing_matrix_labels','sourceMatrices':expected,'missingMatrices':confirmed[1],'missingLabels':confirmed[2],'currentText':confirmed[3]})
   findings.append(c)
  else:review.append({**c,'reason':'Source matrix could not be anchored to current content','conversionErrors':errors})
  continue
 try:
  first_math=a.MML.search(candidate['sourceTitleHtml'])
  if not first_math:raise ValueError('No embedded MathML')
  fragment=tex(ET.fromstring(first_math[0]))
  def expand(match):
   math=a.MML.search(match[0])
   if not math:raise ValueError('Nested math container has no MathML')
   return tex(ET.fromstring(math[0]))
  full=html.unescape(a.CONTAINER.sub(expand,candidate['sourceTitleHtml'])).strip()
  plain_first=formula_norm(fragment);plain_full=formula_norm(full)
  if not plain_first or plain_first==plain_full:complete.append(c);continue
  if any(plain_full in formula_norm(text) for text in texts):complete.append(c);continue
  anchored=next((text for text in texts if plain_first in [formula_norm(m.group()) for m in MATH.finditer(text)]),None)
  if anchored:
   findings.append({**c,'reason':'truncated_compound_formula','firstFragmentTex':fragment,'sourceCompleteTex':full,'currentText':anchored})
  else:review.append({**c,'reason':'Compound formula differs; exact first-fragment match not established'})
 except (ValueError,ET.ParseError) as error:review.append({**c,'reason':'Formula conversion requires review','error':str(error)})

# Repeated source occurrences stay in evidence, but count each affected attribute once.
unique={}
for finding in findings:
 key=(finding['entity'],finding['attribute'])
 if key not in unique:unique[key]={**finding,'sourceOccurrences':[]}
 unique[key]['sourceOccurrences'].append({'lessonId':finding['lessonId'],'sourceFile':finding['sourceFile'],'line':finding['line'],'reason':finding['reason']})
findings=list(unique.values())
by_lesson=collections.defaultdict(list)
for finding in findings:
 for lesson in {o['lessonId'] for o in finding['sourceOccurrences']}:
  by_lesson[lesson].append(finding)
lesson_titles={r['lessonId']:r['lessonTitle'] for r in rows}
summary={'databaseBasis':2832,'sourceFilesScanned':2964,'sourceCandidates':len(rows),'candidateLessons':len({r['lessonId'] for r in rows}),'currentRecordsRead':len(records),'patternMatchedAttributes':len(findings),'patternMatchedEntities':len({f['entity'] for f in findings}),'patternMatchedLessons':len(by_lesson),'reasons':dict(collections.Counter(f['reason'] for f in findings)),'candidateOccurrencesAlreadyComplete':len(complete),'candidateOccurrencesNotImported':len(unimported),'candidateOccurrencesNeedingReview':len(review)}
(HERE/'matches.json').write_text(json.dumps(findings,indent=2))
(HERE/'needs-review.json').write_text(json.dumps(review,indent=2))
(HERE/'already-complete.json').write_text(json.dumps(complete,indent=2))
(HERE/'comparison-summary.json').write_text(json.dumps(summary,indent=2))
lessons=[{'id':lesson,'title':lesson_titles[lesson],'affectedAttributes':len(items),'entities':sorted({f['entity'] for f in items}),'reasons':dict(collections.Counter(f['reason'] for f in items))} for lesson,items in sorted(by_lesson.items())]
(HERE/'affected-lessons.json').write_text(json.dumps(lessons,indent=2))
print(json.dumps(summary,indent=2))
for lesson in lessons:
 if re.search('matri|vector|determinant|eigen|linear transformation',lesson['title'],re.I):print(lesson['id'],lesson['title'],lesson['affectedAttributes'])
