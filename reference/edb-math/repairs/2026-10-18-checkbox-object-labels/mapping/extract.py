"""Read-only extraction of complete selectable objects from current checkbox prompts.

Only exact source spans are moved. This tool never transacts. Each case records the
spans and field identities; rejected structures remain in an explicit review queue.
"""
import collections,copy,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
RUN=HERE.parent
HISTORY={q['id']:q for q in json.loads((HERE/'historical-plans.json').read_text())}
ROMANS=('I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII')
LABEL_LINE=re.compile(r'(?m)^[ \t]*(?:[-*+]\s+)?(?:\*\*)?([A-Z]+)[.)](?:\*\*)?[ \t]+([^\n]+)$')
BULLET_LINE=re.compile(r'(?m)^[ \t]*[-*+][ \t]+([^\n]+)$')
MATH=re.compile(r'(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$])*?(?<!\\)\$')

def fields(q):return [f for f in q.get(':question/answer-fields',[]) if f.get(':answer-field/type',{}).get(':db/ident')==':answer-field.type/checkbox']
def norm(s):return re.sub(r'\s+',' ',s).strip()
def math_balanced(s):
    return len(re.findall(r'(?<!\\)\$\$',s))%2==0 and len(re.findall(r'(?<!\\)\$',re.sub(r'(?<!\\)\$\$','',s)))%2==0 and collections.Counter(re.findall(r'\\begin\{([^}]+)\}',s))==collections.Counter(re.findall(r'\\end\{([^}]+)\}',s))
def clean_prompt(s):
    return re.sub(r'\n(?:[ \t]*\n){2,}','\n\n',s).strip()
def move_spans(prompt,spans):
    for start,end in sorted(spans,reverse=True):prompt=prompt[:start]+prompt[end:]
    return clean_prompt(prompt)
def inline_object(content):
    # A single display block remains a complete mathematical object beside a box,
    # while inline delimiters avoid an unnecessarily huge click target.
    if content.startswith('$$') and content.endswith('$$'):return '$'+content[2:-2].strip()+'$'
    return content

def extract_lists(q,history):
    prompt=q[':question/problem'];fs=fields(q);labels=[f[':answer-field/key'].strip() for f in fs]
    matches=[m for m in LABEL_LINE.finditer(prompt) if m[1] in labels]
    positional=False
    if len(matches)!=len(labels) or set(m[1] for m in matches)!=set(labels):
        matches=list(BULLET_LINE.finditer(prompt))
        if not(history and len(matches)==len(labels) and set(labels)==set(history['labels'])):return None
        labels=history['labels']; positional=True
    objects=[];spans=[]
    bylabel={f[':answer-field/key'].strip():f for f in fs}
    for i,m in enumerate(matches):
        label=labels[i] if positional else m[1]
        content=m[1] if positional else m[2]
        format_repair=None
        if not math_balanced(content) and content.rstrip().endswith('$$') and math_balanced(content.rstrip()[:-2]):
            format_repair={'before':content,'after':content.rstrip()[:-2].rstrip(),'reason':'Remove an extraneous trailing display-math opener after an already complete option; mathematical content is unchanged.'}
            content=format_repair['after']
        if not math_balanced(content):return None
        if positional and re.match(r'(?:\*\*)?[A-Z]+[.)]',content):return None
        objects.append({'source_label':label,'field_id':bylabel[label][':db/id'],'content':inline_object(content.strip()),'source_fragment':m[0],'source_span':[m.start(),m.end()]})
        if format_repair:objects[-1]['format_repair']=format_repair
        spans.append((m.start(),m.end()))
    after=move_spans(prompt,spans)
    return {'objects':objects,'problem_after':after,'extraction':'historical_order_bullet_list' if positional else 'explicit_label_list'}

def extract_matrices(q,history):
    prompt=q[':question/problem'];fs=fields(q);bylabel={f[':answer-field/key'].strip():f for f in fs}
    labels=list(bylabel)
    if not all(re.fullmatch('[A-Z]',x) for x in labels):return None
    # The expression must be a complete math block composed solely of the named
    # matrix assignments, with separators outside each environment.
    blocks=list(MATH.finditer(prompt));results=[]
    for block in blocks:
        raw=block[0];width=2 if raw.startswith('$$') else 1;body=raw[width:-width].strip()
        starts=list(re.finditer(r'(?<![A-Za-z])([A-Z])\s*=\s*',body))
        if len(starts)!=len(labels) or {m[1]for m in starts}!=set(labels):continue
        if body[:starts[0].start()].strip():continue
        objects=[];valid=True
        for i,m in enumerate(starts):
            end=starts[i+1].start()if i+1<len(starts)else len(body)
            expression=body[m.start():end].strip()
            expression=re.sub(r'(?:\s|,|;|\.|\\,|\\;|\\quad|\\qquad)+$','',expression)
            if not re.search(r'\\begin\{(?:aligned|[bp]?matrix|array)\}',expression) or not math_balanced(expression):valid=False;break
            # No unnamed algebra is allowed after the complete matrix enclosure.
            tail=re.split(r'\\end\{(?:aligned|[bp]?matrix|array)\}',expression)[-1]
            if re.sub(r'\\(?:right|big|Big|bigg|Bigg)|[\s\[\](){}|.]','',tail):valid=False;break
            objects.append({'source_label':m[1],'field_id':bylabel[m[1]][':db/id'],'content':'$'+expression+'$','source_fragment':expression,'source_span':[block.start(),block.end()]})
        if valid:results.append({'objects':objects,'problem_after':move_spans(prompt,[(block.start(),block.end())]),'extraction':'named_matrix_assignments'})
    return results[0] if len(results)==1 else None

def extract_separate_matrices(q,history):
    prompt=q[':question/problem'];fs=fields(q);bylabel={f[':answer-field/key'].strip():f for f in fs}
    if not all(re.fullmatch('[A-Z]',x) for x in bylabel):return None
    objects=[];spans=[];seen=set()
    for block in MATH.finditer(prompt):
        raw=block[0];width=2 if raw.startswith('$$')else 1;body=raw[width:-width].strip()
        m=re.match(r'^([A-Z])\s*=\s*',body)
        if not m or m[1]not in bylabel:continue
        if not re.search(r'\\begin\{(?:aligned|[bp]?matrix|array)\}',body):continue
        expression=re.sub(r'(?:\s|,|;|\.|\\,|\\;|\\quad|\\qquad)+$','',body)
        tail=re.split(r'\\end\{(?:aligned|[bp]?matrix|array)\}',expression)[-1]
        if re.sub(r'\\(?:right|big|Big|bigg|Bigg)|[\s\[\](){}|.]','',tail):return None
        if not math_balanced(expression)or m[1]in seen:return None
        seen.add(m[1]);start,end=block.span()
        # Move an exact div child with its mathematical object; this avoids
        # retaining layout-only empty wrappers after recent stacked-matrix fixes.
        before,after=prompt[:start],prompt[end:]
        if before.endswith('<div>') and after.startswith('</div>'):start-=5;end+=6
        spans.append((start,end))
        objects.append({'source_label':m[1],'field_id':bylabel[m[1]][':db/id'],'content':'$'+expression+'$','source_fragment':prompt[start:end],'source_span':[start,end]})
    if seen!=set(bylabel):return None
    after=move_spans(prompt,spans)
    after=re.sub(r'<div class="matrix-operands matrix-operands-stacked">\s*</div>','',after)
    return {'objects':objects,'problem_after':clean_prompt(after),'extraction':'separate_named_matrices'}

def clarify_short_objects(q,objects):
    prompt=q[':question/problem']
    sets={'N':'natural numbers','Z':'integers','Q':'rational numbers','R':'real numbers','C':'complex numbers'}
    for obj in objects:
        before=obj['content'];after=before;reason=None
        if re.search(r'Which of the following is a variable\?',prompt):
            after='The expression '+before;reason='Identify each complete expression without using the answer-revealing word variable as a caption.'
        elif re.fullmatch(r'\$[NZQRC]\$',before) and re.search(r'\bsets?\b',prompt,re.I):
            after=before+' ('+sets[before[1]]+')';reason='Spell out the standard number-set symbol, distinguishing the mathematical object from a source choice label.'
        elif re.fullmatch(r'\$-?\d+(?:\.\d+)?\$',before):
            noun='digit'if re.search(r'\bWhich digits\b',prompt)else'number'
            after='The '+noun+' '+before;reason='Identify the complete numeric object directly beside its checkbox.'
        elif re.search(r'\b(?:vertices|vertex)\b',prompt) and re.fullmatch(r'\$\([^$]+,[^$]+\)\$',before):
            after='The point '+before;reason='Identify the point as a selectable object; any identical coordinate in the shared geometric givens remains there.'
        if after!=before:
            obj['source_content']=before;obj['content']=after;obj['caption_reason']=reason

def ref_text(s):
    s=inline_object(s).strip()
    return s if re.fullmatch(r'\$(?:\\.|[^$])*\$',s) else '“'+s.rstrip('.').replace('“','‘').replace('”','’')+'”'

def solution_references(solution,objects):
    lookup={o['source_label']:ref_text(o['content']) for o in objects if o['source_label'] in ROMANS}
    if not lookup:return solution,[]
    roman='(?:'+'|'.join(sorted(lookup,key=len,reverse=True))+')'
    edits=[];protected={}
    def mask(m):
        key=f'\ue000{len(protected)}\ue001';protected[key]=m[0];return key
    masked=MATH.sub(mask,solution)
    domain_roman=re.compile(r'\b(?:types?|classes?|categories|category|quadrants?|World War)\s+(?:VIII|VII|VI|IV|III|II|I)(?:\s*(?:,\s*(?:and\s+)?|and\s+|or\s+|[-–])(?:VIII|VII|VI|IV|III|II|I))*\b',re.I)
    masked=domain_roman.sub(mask,masked)
    # Whole quoted answers are rendered as explicit selected content. Preserve
    # the rest of the conclusion and its mathematical reasoning byte-for-byte.
    quote=re.compile(r'["“]('+roman+r'(?:\s*(?:,\s*(?:and\s+)?|and\s+)'+roman+r')*(?:\s+only)?)[.]?["”]')
    def quoted(m):
        labels=re.findall(r'\b'+roman+r'\b',m[1]);value='; '.join(lookup[x]for x in labels)
        if m[1].endswith('only'):value+=' only'
        if m[0][-2:-1]=='.':value+='.'
        edits.append({'before':m[0],'after':value,'kind':'quoted_choice_combination'})
        # Protect inserted content from matching Roman words it may contain.
        return mask(type('M',(),{'__getitem__':lambda _,n:value})())
    masked=quote.sub(quoted,masked)
    # A source range I–III denotes every case, including II; substituting only
    # the endpoints would lose that meaning.
    ranges=re.compile(r'\b('+roman+r')\s*[-–—]\s*('+roman+r')\b')
    def ranged(m):
        start,end=ROMANS.index(m[1]),ROMANS.index(m[2])
        if end<start or any(label not in lookup for label in ROMANS[start:end+1]):return m[0]
        value='; '.join(lookup[label]for label in ROMANS[start:end+1])
        edits.append({'before':m[0],'after':value,'kind':'inclusive_choice_range'})
        return mask(type('M',(),{'__getitem__':lambda _,n:value})())
    masked=ranges.sub(ranged,masked)
    token=re.compile(r'\b'+roman+r'\b')
    def reference(m):
        prefix=masked[max(0,m.start()-35):m.start()]
        # Type I/II regions and errors, World War II, or proposition names are
        # domain terminology, not removed list labels.
        if re.search(r'\b(?:type|Type|TYPE|Class|class|Category|category|War)\s+(?:(?:I|II)\s+(?:and|or)\s+)?$',prefix):return m[0]
        if m[0]=='I' and re.search(r'\b(?:that|if|as|when)\s+$',prefix,re.I):return m[0]
        replacement=lookup[m[0]]
        edits.append({'before':m[0],'after':replacement,'kind':'roman_reference','context':masked[max(0,m.start()-45):m.end()+70]})
        return mask(type('M',(),{'__getitem__':lambda _,n:replacement})())
    masked=token.sub(reference,masked)
    # Restore placeholders recursively because inserted references may contain
    # protected math spans from a prior replacement.
    for _ in range(3):
        restored=re.sub(r'\ue000\d+\ue001',lambda m:protected[m[0]],masked)
        if restored==masked:break
        masked=restored
    return masked,edits

def main():
    questions=json.loads((RUN/'questions.json').read_text());cases=[];pending=[];complete=[]
    for q in questions:
        fs=fields(q);keys=[f.get(':answer-field/key','')for f in fs]
        if not all(re.fullmatch(r'[A-Z]+',x.strip())for x in keys):
            complete.append(q[':db/id']);continue
        history=HISTORY.get(q[':db/id'])
        if q[':db/id']==17592186563954:
            history={'labels':['I','II','III'],'historical_plan':None,'mapping_evidence':'The current solution explicitly identifies I as the first negative-integral claim, II as the zero-integral claim, and III as the reversed-path negative-integral claim; existing Boolean key is false/true/false.'}
        result=extract_lists(q,history)or extract_matrices(q,history)or extract_separate_matrices(q,history)
        if result is None:
            pending.append({'id':q[':db/id'],'ma_id':q.get(':question/math-academy-id'),'keys':keys,'classification':history.get('classification')if history else None,'historical_plan':history.get('historical_plan')if history else None,'problem':q[':question/problem']});continue
        clarify_short_objects(q,result['objects'])
        for obj in result['objects']:
            fix=json.loads((HERE/'layout_overrides.json').read_text()).get(str(q[':db/id']),{}).get(obj['source_label'])
            if fix:
                assert obj['content']==fix['before']
                obj['layout_repair']=fix;obj['content']=fix['after']
        result.update({'question_eid':q[':db/id'],'math_academy_id':q.get(':question/math-academy-id'),'problem_before':q[':question/problem'],'solution_before':q.get(':question/worked-solution',''),'historical_plan':history.get('historical_plan')if history else None})
        solution=result['solution_before'];format_repairs=[]
        if q[':db/id']==17592186055072:
            fixes=[('{u,v}',r'\{u,v\}'),('{-1,1}',r'\{-1,1\}'),('A={ &',r'A=\{ &'),('(v,v,1)}.',r'(v,v,1)\}.')]
            for before,after in fixes:
                assert before in solution
                solution=solution.replace(before,after);format_repairs.append({'before':before,'after':after,'reason':'Escape literal set braces; unescaped grouping across aligned columns caused pre-existing MathJax Misplaced & errors.'})
        if q[':db/id']in (17592186338801,17592186400003):
            def drop_stray(match):
                before=match[0];after=before.rstrip()[:-2].rstrip()
                assert math_balanced(after)
                format_repairs.append({'before':before,'after':after,'reason':'Remove the same extraneous trailing display-math opener in the worked solution.'});return after
            solution=re.sub(r'(?m)^.*\S[ \t]*\$\$[ \t]*$',drop_stray,solution)
        result['solution_after'],result['solution_reference_edits']=solution_references(solution,result['objects'])
        result['solution_format_repairs']=format_repairs
        if history and history.get('mapping_evidence'):result['mapping_evidence']=history['mapping_evidence']
        cases.append(result)
    for name,data in [('cases.json',cases),('pending.json',pending),('already-descriptive-ids.json',complete)]: (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    summary={'mapped_questions':len(cases),'mapped_fields':sum(len(c['objects'])for c in cases),'pending':len(pending),'already_descriptive_questions':len(complete),'extractions':dict(collections.Counter(c['extraction']for c in cases)),'solution_reference_edits':sum(len(c['solution_reference_edits'])for c in cases)}
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
