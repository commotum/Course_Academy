"""Canonical, source-backed HTML tables without arbitrary source styles."""
import html,re
from bs4 import NavigableString,Comment
try:
    from .math_format import MATH
except ImportError:
    from math_format import MATH

STRUCTURAL={'table','thead','tbody','tfoot','tr','td','th','caption','colgroup','col'}
INLINE={'strong','em','sup','sub','p','ul','ol','li'}

def source_matrix_layout(table,render_leaf):
    """Recognize explicit source bracket/brace decoration before sanitizing it.

    Check the complete structure before visiting controls: speculative rendering
    would register the same field twice when falling back to an ordinary table.
    """
    try:
        from .math_format import matrix_equation,system_answer
    except ImportError:
        from math_format import matrix_equation,system_answer
    def rows(t):return[r for r in t.find_all('tr')if r.find_parent('table')is t]
    def cells(row):return row.find_all(['td','th'],recursive=False)
    def empty(c):return not c.get_text(strip=True)and not c.select('input,select,textarea,.freeResponseTextbox,.matheditor-wrapper-answer,[contenteditable="true"]')
    def edge(c,side):
        p=properties(c);value=p.get('border-'+side,p.get('border',''))
        return bool(value)and not re.match(r'^(?:hidden|none|0(?:px)?)(?:\s|$)',value)
    def grid(t,has_label=False):
        rr=rows(t);out=[];labels=[]
        spanning=bool(rr and cells(rr[0])and cells(rr[0])[0].get('rowspan')==str(len(rr)))
        for i,row in enumerate(rr):
            cc=cells(row)
            if has_label and(not spanning or i==0):labels.append(cc.pop(0))
            if len(cc)<3 or not empty(cc[0])or not empty(cc[-1])or not edge(cc[0],'left')or not edge(cc[-1],'right'):return None
            entries=cc[1:-1]
            if not all(empty(c)for c in entries):out.append(entries)
        if not out or len({len(r)for r in out})!=1 or any(empty(c)for r in out for c in r):return None
        return out,labels
    def entry(c):
        text=render_leaf(c).strip()
        return MATH.sub(lambda m:m[0][2:-2]if m[0].startswith(('$$',r'\(',r'\['))else m[0][1:-1],text).strip()
    nested=[t for t in table.find_all('table')if t.find_parent('table')is table]
    outer=rows(table)
    if len(nested)==3 and len(outer)==1:
        parsed=[grid(t)for t in nested]
        if any(p is None for p in parsed):return None
        outside=[c for c in cells(outer[0])if c.find('table')is None and not empty(c)]
        if len(outside)!=1 or outside[0].get_text(strip=True)!='=':return None
        gs=[[[entry(c)for c in r]for r in p[0]]for p in parsed]
        return '\n\n'+matrix_equation([gs[0],gs[1],'=',gs[2]])+'\n\n'
    if nested:return None
    if len(outer)>=2:
        first=cells(outer[0]);system=bool(first and first[0].get('rowspan')==str(len(outer))and first[0].get_text(strip=True)=='{')
        if system:
            rr=[cells(r)[1:]if i==0 else cells(r)for i,r in enumerate(outer)]
            if all(len(r)==3 and r[1].get_text(strip=True)=='='for r in rr):
                return '\n\n'+system_answer([[entry(c)for c in r]for r in rr])+'\n\n'
    parsed=grid(table,has_label=True)
    if parsed is not None:
        rr,labels=parsed;nonempty=[c for c in labels if not empty(c)]
        if len(nonempty)==1 and '='in nonempty[0].get_text():
            label=entry(nonempty[0]);gs=[[entry(c)for c in r]for r in rr]
            return '\n\n'+matrix_equation([label,gs])+'\n\n'
    return None
def escaped_text(value):
    """Keep protected TeX exact; escape only ordinary HTML text."""
    value=str(value);parts=[];end=0
    for m in MATH.finditer(value):
        parts.extend([re.sub(r'(?<!\\)\$',lambda m:r'\$',html.escape(value[end:m.start()],quote=False)),m[0]]);end=m.end()
    return ''.join(parts)+re.sub(r'(?<!\\)\$',lambda m:r'\$',html.escape(value[end:],quote=False))

def properties(node):
    return {k.strip().lower():v.strip() for k,v in
            (part.split(':',1)for part in node.get('style','').split(';')if ':'in part)}

def color(value):
    value=str(value or '').strip()
    if re.fullmatch(r'[\da-f]{6}',value,re.I):value='#'+value
    if re.fullmatch(r'#[\da-f\s]+',value,re.I):value=re.sub(r'\s','',value)
    if re.fullmatch(r'#[\da-f]{3}(?:[\da-f]{3})?|[a-z]+|rgba?\([\d.,%\s]+\)',value,re.I) and value.lower()not in {'transparent','inherit','initial','unset','currentcolor'}:return value
    return None

def alignment(value):return value if value in {'left','right','center','justify'}else None

def attrs(node,last_rows):
    tag=node.name.lower();s=properties(node);a=[]
    if s.get('display')in {'grid','inline-grid','flex','inline-flex'}or s.get('position')in {'absolute','fixed'}:raise ValueError('Unsupported table layout style')
    def put(k,v):a.append(' '+k+'="'+html.escape(str(v),quote=True)+'"')
    if tag=='table':
        put('class','source-table');put('data-rules',node.get('rules')if node.get('rules')in {'all','rows','cols'}else'none')
        location=alignment(node.get('align'))or('center'if s.get('margin')=='auto'or s.get('margin-left')=='auto'and s.get('margin-right')=='auto'else None)
        if location:put('data-table-align',location)
        border=s.get('border','')
        if str(node.get('border','0'))not in {'','0'}or border and not re.match(r'^(?:none|hidden|0(?:px)?)(?:\s|$)',border):put('data-frame','true')
    elif tag=='tr'and id(node)not in last_rows:put('data-next-row','true')
    for key in ['rowspan','colspan','span']:
        value=node.get(key)
        if value is None:continue
        if not re.fullmatch(r'\d{1,3}',str(value))or int(value)==0 and key!='rowspan':raise ValueError('Unsupported table span: '+str(value))
        put(key,value)
    if tag=='th'and node.get('scope')in {'row','col','rowgroup','colgroup'}:put('scope',node['scope'])
    ancestors=[node]
    if tag in {'td','th'}:
        for parent in node.parents:
            ancestors.append(parent)
            if parent.name=='table':break
    for parent in ancestors:
        p=properties(parent);align=(alignment(parent.get('align'))if parent.name!='table'else None)or alignment(p.get('text-align'))
        if align:put('data-cell-align',align);break
    fill=color(node.get('bgcolor')or s.get('background-color')or s.get('background'))
    if fill:put('data-fill',fill)
    if re.fullmatch(r'bold|[6-9]00',s.get('font-weight','')):put('data-cell-weight','bold')
    valign=s.get('vertical-align')or node.get('valign')
    if valign in {'top','middle','bottom'}:put('data-cell-valign',valign)
    if tag in {'td','th'}:
        for side in ['top','right','bottom','left']:
            value=s.get('border-'+side,s.get('border'))
            if value is not None:put('data-border-'+side,'hidden'if re.search(r'\bhidden\b',value)else'none'if re.match(r'^(?:none|0(?:px)?)(?:\s|$)',value)else'solid')
    return ''.join(a)

def source_table_html(table,render_leaf,skip=lambda node:False):
    """Reuse the caller's math/widget/asset renderer, retaining actual cell roles."""
    layout=source_matrix_layout(table,render_leaf)
    if layout is not None:return layout
    last_rows={id(rows[-1])for t in [table]+table.find_all('table')if(rows:=[r for r in t.find_all('tr')if r.find_parent('table')is t])}
    def walk(node):
        if isinstance(node,Comment):return ''
        if isinstance(node,NavigableString):return escaped_text(re.sub(r'[\t\r\n ]+',' ',str(node)))
        tag=getattr(node,'name','')
        if not tag or skip(node):return ''
        if tag in {'script','style','mjx-assistive-mml'}:return ''
        classes=node.get('class',[])
        if tag in {'math','mjx-container','svg','input','select','img'}or any(c in classes for c in ['freeResponseTextbox','selectList','mjpage','MathJax']):
            value=render_leaf(node)
            image=re.fullmatch(r'!\[([^]]*)\]\(([^)]+)\)',value.strip())
            if image:return '<img src="'+html.escape(image[2],quote=True)+'" alt="'+html.escape(image[1],quote=True)+'">'
            return escaped_text(value)
        if tag in STRUCTURAL:
            body=''.join(walk(c)for c in node.children);result='<'+tag+attrs(node,last_rows)+'>'+body+(''if tag=='col'else'</'+tag+'>')
            return '<div class="source-table-scroll">'+result+'</div>'if tag=='table'else result
        if tag=='br':return '<br>'
        normalized={'b':'strong','i':'em'}.get(tag,tag);body=''.join(walk(c)for c in node.children)
        if normalized in INLINE:
            extra=''.join(' '+k+'="'+html.escape(str(node[k]),quote=True)+'"'for k in ['type','start','reversed','value']if node.has_attr(k))
            return '<'+normalized+extra+'>'+body+'</'+normalized+'>'
        if tag=='a'and node.get('href'):return '<a href="'+html.escape(node['href'],quote=True)+'">'+body+'</a>'
        return body
    return '\n\n'+walk(table)+'\n\n'
