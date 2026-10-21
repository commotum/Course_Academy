"""Data-only reflow of the reviewed non-scrollable checkbox math spans."""
import copy,importlib.util,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;RUN=HERE.parent
spec=importlib.util.spec_from_file_location('extract',HERE/'extract.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
owned=json.loads((RUN/'exceptions/further-review/overflow-owned.json').read_text())
print('owned shape',type(owned))
if isinstance(owned,dict):owned=owned.get('cases',owned.get('fields',owned.get('owned',owned)))
owned_ids={x['field_id']for x in owned}
cs={c['after'][':db/id']:c for c in json.loads((RUN/'mapped-cases.json').read_text())['cases']}
issues=json.loads((HERE/'overflow-review.json').read_text())

def cuts(s,chars):
    braces=parens=brackets=angles=0;result=[];i=0
    while i<len(s):
        ch=s[i]
        if ch=='\\':
            match=re.match(r'\\[A-Za-z]+|\\.',s[i:]);i+=len(match[0])if match else 1;continue
        if ch=='{':braces+=1
        elif ch=='}':braces-=1
        elif not braces:
            if ch=='(':parens+=1
            elif ch==')':parens-=1
            elif ch=='[':brackets+=1
            elif ch==']':brackets-=1
            elif ch=='⟨':angles+=1
            elif ch=='⟩':angles-=1
        if ch in chars and braces==parens==brackets==angles==0:result.append(i)
        i+=1
    return result

def chunks(s,positions,after=True):
    start=0;parts=[]
    for p in positions:
        end=p+1 if after else p
        if end>start:parts.append(s[start:end].strip());start=end
    parts.append(s[start:].strip());return [p for p in parts if p]

def group_math(s):
    # A leading bracket is otherwise read as gathered's optional alignment
    # argument, silently swallowing the vector. A spacing token prevents that.
    if s.lstrip().startswith('['):s=r'\,'+s
    return r'\begin{gathered}'+s+r'\end{gathered}'
def set_group(s):
    # A complete outer set/collection group can contain a nested table while
    # preserving its original delimiter tokens and all enclosed mathematics.
    escaped=re.match(r'^(.*?)(\\\{)(.*)(\\\})([.,]?)$',s,re.S)
    if escaped and not any(ch in escaped[1]for ch in'+-'):
        inside=escaped[3];positions=cuts(inside,',:')
        if positions:return group_math(escaped[1]+r'\left\{'+group_math(r'\\'.join(chunks(inside,positions)))+r'\right\}'+escaped[5])
    candidates=([0]if s.startswith('{')else[])+[m.end()-1 for m in re.finditer(r'=\s*\{',s)]
    if not candidates:return None
    start=candidates[0]
    depth=0;end=None
    for i in range(start,len(s)):
        if s[i]=='\\':continue
        if s[i]=='{':depth+=1
        elif s[i]=='}':
            depth-=1
            if depth==0:end=i;break
    if end is None or s[end+1:].strip()not in('',',','.'):return None
    inside=s[start+1:end];positions=cuts(inside,',:')
    if not positions:return None
    return group_math(s[:start]+r'\left\{'+group_math(r'\\'.join(chunks(inside,positions)))+r'\right\}'+s[end+1:])

def reflow(raw):
    width=2 if raw.startswith('$$')else 1;body=raw[width:-width].strip()
    nested=set_group(body)
    if nested:return '$'+nested+'$','nested_set_rows'
    positions=cuts(body,',:')
    parts=chunks(body,positions)if positions else[body]
    segments=[]
    for p in parts:
        eq=cuts(p,'=')
        if not eq:
            # A top-level inequality is also a natural break. In particular,
            # keep both operands of the associativity statement readable.
            for m in re.finditer(r'\\(?:ne|neq)(?![A-Za-z])',p):
                probe=p[:m.start()]+'='+p[m.end():]
                if m.start() in cuts(probe,'='):eq.append(m.start())
        pp=chunks(p,eq,False)if eq else[p]
        for piece in pp:
            # Break long sums at existing top-level operators; factor groups,
            # functions, subscripts and exponents remain intact.
            if len(piece)>55:
                ops=cuts(piece,'+-');pieces=chunks(piece,[i for i in ops if i>0],False)
            else:pieces=[piece]
            segments.extend(pieces)
    if len(segments)>1:return ' '.join('$'+p+'$'for p in segments),'inline_natural_breaks'
    return '$'+group_math(body)+'$','responsive_indivisible_math'

fixes=[];metric_only=[]
for issue in issues:
    qid=issue['question_eid'];c=cs[qid];f=sorted(c['after'][':question/answer-fields'],key=lambda f:f[':db/id'])[issue['choice_index']]
    fid=f[':db/id']
    if fid in owned_ids:continue
    before=f[':answer-field/key'];matches=list(mod.MATH.finditer(before));rights=issue['choice']['svgRights'];assert len(matches)==len(rights),(qid,len(matches),len(rights))
    edits=[];after=before;styles=[]
    for m,right in reversed(list(zip(matches,rights))):
        if right<=issue['choice']['right']+1:continue
        value,style=reflow(m[0]);edits.append({'before':m[0],'after':value,'style':style,'literal_set_delimiters_restored':style=='nested_set_rows'});styles.append(style);after=after[:m.start()]+value+after[m.end():]
    if after==before:
        metric_only.append({'question_eid':qid,'field_id':fid,'reason':'SVG content already fits within the choice; overflow metric includes internal table layout width. Review screenshot before accepting.','measurement':issue});continue
    fixes.append({'question_eid':qid,'field_id':fid,'before':before,'after':after,'reason':'Reflow a complete selectable object at existing mathematical boundaries so it remains visible beside its checkbox at375px. No mathematical tokens or Boolean answers change.','math_spans':list(reversed(edits)),'styles':styles})
# This held question's B choice needed multiline set notation. Restore the same
# visible outer delimiters for its A/C objects so all three complete sets agree.
qid=17592186420586
for f in cs[qid]['after'][':question/answer-fields']:
    if f[':db/id'] not in (17592186475201,17592186475203):continue
    before=f[':answer-field/key'];after,style=reflow(before)
    fixes.append({'question_eid':qid,'field_id':f[':db/id'],'before':before,'after':after,'reason':'Restore the visible outer set delimiters consistently across the three selectable sets in this held question.','math_spans':[{'before':before,'after':after,'style':style,'literal_set_delimiters_restored':True}],'styles':[style]})
(HERE/'metric-only-overflow.json').write_text(json.dumps(metric_only,ensure_ascii=False,indent=2)+'\n')
(HERE/'overflow-own-overrides.json').write_text(json.dumps(fixes,ensure_ascii=False,indent=2)+'\n')
print('fixes',len(fixes),'questions',len({f['question_eid']for f in fixes}))
