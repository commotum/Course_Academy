"""Read-only audit of legacy SVG titles truncated to their first nested MathML."""
from pathlib import Path
import bisect, collections, hashlib, html as html_lib, json, re, sys, time, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.edn import loads,dumps,kw
from scripts.question_capture.math_format import environment,cells
HERE=Path(__file__).resolve().parent
SOURCE=Path('/home/jake/Developer/MA/DATA/Lessons')
TITLE=re.compile(r'<title\b[^>]*>([\s\S]*?)</title>')
CONTAINER=re.compile(r'<mjx-container\b[\s\S]*?</mjx-container>')
MML=re.compile(r'<math\b[^>]*>[\s\S]*?</math>')
UNICODE={'−':'-','×':r'\times','⋅':r'\cdot','π':r'\pi','θ':r'\theta','λ':r'\lambda','α':r'\alpha','β':r'\beta','∞':r'\infty','∂':r'\partial','∇':r'\nabla'}

def tex(node):
    tag=node.tag.rsplit('}',1)[-1];children=list(node)
    if tag in ('mi','mn','mo','mtext','ms'):
        text=''.join(node.itertext());return ''.join(UNICODE.get(c,c) for c in text)
    if tag in ('math','mrow','mstyle','mtd','mpadded','semantics','menclose'):
        return ''.join(tex(c) for c in children if c.tag.rsplit('}',1)[-1] not in ('annotation','annotation-xml'))
    if tag=='msqrt':return r'\sqrt{'+''.join(tex(c) for c in children)+'}'
    if tag=='mfrac' and len(children)==2:return r'\frac{'+tex(children[0])+'}{'+tex(children[1])+'}'
    if tag in ('msup','msub') and len(children)==2:return tex(children[0])+('^' if tag=='msup' else '_')+'{'+tex(children[1])+'}'
    if tag=='msubsup' and len(children)==3:return tex(children[0])+'_{'+tex(children[1])+'}^{'+tex(children[2])+'}'
    if tag=='mroot' and len(children)==2:return r'\sqrt['+tex(children[1])+']{'+tex(children[0])+'}'
    if tag in ('mspace','mphantom'):return ''
    raise ValueError(tag)

def norm(value):
    value=html_lib.unescape(value).replace('−','-')
    value=re.sub(r'\\(?:left|right|displaystyle|textstyle|,|!|;|:|quad|qquad)\b?','',value) if False else value
    value=re.sub(r'\\(?:left|right|displaystyle|textstyle)\b|\\[,!;:]|\\(?:quad|qquad)\b','',value)
    value=re.sub(r'\\(?:dfrac|tfrac)\b',r'\\frac',value)
    value=re.sub(r'\\(?:mathrm|mathbf|boldsymbol)\{([^{}]*)\}',r'\1',value)
    return re.sub(r'[\s{}]','',value)

def matrix_signature(rows):return [[norm(cell) for cell in row] for row in rows]

def source_matrices(title):
    result=[];errors=[]
    for math in MML.findall(title):
        try:
            root=ET.fromstring(math)
            for table in root.findall('.//{*}mtable'):
                # Nested matrix cells or alignment structures need manual review.
                if any(cell.find('.//{*}mtable') is not None for row in table for cell in row):continue
                rows=[[tex(cell) for cell in row if cell.tag.rsplit('}',1)[-1]=='mtd'] for row in table]
                if not rows or not rows[0] or len({len(r) for r in rows})!=1:continue
                result.append({'rows':rows,'signature':matrix_signature(rows)})
        except (ValueError,ET.ParseError) as error:errors.append(str(error))
    return result,errors

def current_matrices(text):
    result=[]
    for token in re.finditer(r'\\begin\{(?:bmatrix|pmatrix|vmatrix|Vmatrix|matrix|array)\}',text):
        bounds=environment(text,token.start())
        if not bounds:continue
        start,end,_=bounds;body=text[start:end]
        if token.group().endswith('{array}'):
            body=re.sub(r'^\{[^}]*\}','',body)
        rows=cells(body)
        if rows:result.append(matrix_signature(rows))
    return result

def scan():
    found=[];lessons=[];errors=[];started=time.monotonic()
    paths=sorted(SOURCE.glob('*/Source/*.html'))
    for index,path in enumerate(paths):
        if path.stem!=path.parent.parent.name:continue
        text=path.read_text(errors='replace')
        if '<mjx-container' not in text:continue
        try:data=json.loads(path.with_suffix('.json').read_text())
        except (FileNotFoundError,json.JSONDecodeError) as error:errors.append({'file':str(path),'error':str(error)});continue
        items=data.get('lesson',{}).get('items',[]);owners=[]
        for item in items:
            dom=item.get('dom_id')
            if not dom:continue
            position=text.find('id="'+dom+'"')
            if position>=0:owners.append((position,item))
        owners.sort(key=lambda x:x[0]);positions=[p for p,_ in owners]
        for match in TITLE.finditer(text):
            title=match[1]
            if '<mjx-container' not in title:continue
            outer=CONTAINER.sub('FORMULA',title)
            significant=re.sub(r'FORMULA|[\s,.;]','',outer)
            if not significant and len(MML.findall(title))<=1:continue
            which=bisect.bisect_right(positions,match.start())-1
            if which<0:continue
            position,item=owners[which];prefix=text[position:match.start()]
            if item.get('step_type')=='tutorial':kind='tutorial';source_id=int(item['content_id']);attribute='tutorial/content'
            elif item.get('step_type')=='example':
                kind='question';source_id='e-'+str(item['content_id']);attribute='question/worked-solution' if re.search(r'class="[^"]*\bexampleExplanation\b',prefix) else 'question/problem'
            elif item.get('item_type')=='question':
                kind='question';source_id='q-'+str(item['question_id'])
                attribute='question/worked-solution' if re.search(r'class="[^"]*(?:explanation|Explanation|solution|Solution)[^"]*"',prefix) else 'answer/value' if 'questionWidget-choiceLetterCircle' in prefix else 'question/problem'
            else:continue
            matrices,conversion_errors=source_matrices(title)
            entry={'lessonId':int(data.get('topic_id',path.stem)),'lessonTitle':data.get('topic_title',path.stem),'kind':kind,'sourceId':source_id,'attribute':attribute,'ownerTitle':item.get('title'),'domId':item['dom_id'],'sourceFile':str(path),'line':text[:match.start()].count('\n')+1,'outerTex':outer.strip(),'mathmlFragments':len(MML.findall(title)),'matrices':matrices,'conversionErrors':conversion_errors,'sourceTitleHtml':title}
            found.append(entry)
        lessons.append(path.stem)
        if index%100==0:
            progress={'filesScanned':index+1,'filesTotal':len(paths),'candidates':len(found),'elapsedSeconds':round(time.monotonic()-started,1)}
            (HERE/'progress.json').write_text(json.dumps(progress));print(json.dumps(progress),flush=True)
    (HERE/'source-candidates.json').write_text(json.dumps(found,indent=2))
    (HERE/'scan-summary.json').write_text(json.dumps({'filesScanned':len(paths),'lessonsWithMathJax':len(lessons),'candidates':len(found),'candidateLessons':len({e['lessonId'] for e in found}),'errors':errors,'elapsedSeconds':round(time.monotonic()-started,1)},indent=2))
    for kind in ['tutorial','question']:
        ids=sorted({e['sourceId'] for e in found if e['kind']==kind})
        (HERE/(kind+'-inputs.edn')).write_text(dumps([ids]))
        id_attr='tutorial/math-academy-id' if kind=='tutorial' else 'question/math-academy-id'
        pattern='[:db/id :tutorial/math-academy-id :tutorial/title :tutorial/content]' if kind=='tutorial' else '[:db/id :question/math-academy-id :question/problem :question/worked-solution {:question/answer-fields [:db/id :answer-field/key {:answer-field/choices [:db/id :answer/value {:answer/type [:db/ident]}]}]}]'
        (HERE/(kind+'-query.edn')).write_text('[:find (pull ?e '+pattern+') :in $ [?id ...] :where [?e :'+id_attr+' ?id]]')
    print((HERE/'scan-summary.json').read_text(),flush=True)

if __name__=='__main__':scan()
