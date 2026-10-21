"""Independent source-MathML versus actual MathJax-tree fidelity checks.

Does not import the restoration converter. Whitespace/font spelling are ignored;
visible symbols and matrix cells, rules, fraction bars, colors and strikes are not.
"""
import collections, json, re, unicodedata
from bs4 import BeautifulSoup, Tag
SOURCE_TEX_TREES={}

def normalize(s):
    return re.sub(r'\s+|[\u2061-\u2064\u200b]', '', unicodedata.normalize('NFKC', s)).replace('−','-').replace('⋅','·')

def from_mml(node):
    if node.name=='mtext' and '[math]' in node.get_text() and '[/math]' in node.get_text():
        parts=[];value=node.get_text();end=0
        for match in re.finditer(r'\[math\]([\s\S]*?)\[/math\]',value):
            if match.start()>end:parts.append({'kind':'text','text':value[end:match.start()],'attributes':{},'children':[]})
            if match[1] not in SOURCE_TEX_TREES:raise ValueError('Missing independently rendered source TeX '+match[1])
            parts.append(SOURCE_TEX_TREES[match[1]]);end=match.end()
        if end<len(value):parts.append({'kind':'text','text':value[end:],'attributes':{},'children':[]})
        return {'kind':'mrow','attributes':dict(node.attrs),'children':parts}
    return {'kind':node.name,'attributes':dict(node.attrs),'children':[
        from_mml(c) if isinstance(c,Tag) else {'kind':'text','text':str(c),'attributes':{},'children':[]}
        for c in node.children]}

def text(node):
    if node['kind'] in ('annotation','annotation-xml','mphantom','mspace'): return ''
    if node['kind']=='text': return normalize(node.get('text',''))
    children=node.get('children',[])
    if node['kind']=='semantics':children=children[:1]
    return ''.join(text(c) for c in children)

def nodes(node):
    yield node
    if node['kind'] in ('annotation','annotation-xml'):return
    children=node.get('children',[])
    if node['kind']=='semantics':children=children[:1]
    for c in children:yield from nodes(c)

def zero(value):return bool(re.fullmatch(r'\+?0(?:\.0+)?(?:px|pt|em|ex|%)?',str(value)))

def features(root):
    tables=[];fractions=[];strikes=[];phantoms=0;colored=collections.Counter()
    for n in nodes(root):
        kind=n['kind'];attrs=n.get('attributes',{});children=n.get('children',[])
        if kind=='mtable':
            rows=[[text(c) for c in row.get('children',[]) if c['kind']=='mtd'] for row in children if row['kind'] in ('mtr','mlabeledtr')]
            width=max(map(len,rows),default=0)
            rows=[row+['']*(width-len(row)) for row in rows]
            lines=str(attrs.get('columnlines','none')).split()
            rules=[lines[min(i,len(lines)-1)] for i in range(max(0,width-1))]
            # MathJax normalizes an empty one-cell array to zero rows.
            if rows not in ([],[['']]) or any(x!='none' for x in rules):tables.append({'cells':rows,'columnlines':rules})
        if kind=='mfrac' and len(children)==2:fractions.append([zero(attrs.get('linethickness','')),text(children[0]),text(children[1])])
        if kind=='menclose' and 'strike' in str(attrs.get('notation','')):strikes.append([sorted(str(attrs['notation']).split()),text(n)])
        if kind=='mphantom':phantoms+=1
    def paint(n,color=None,hidden=False):
        hidden=hidden or n['kind'] in ('mphantom','annotation','annotation-xml')
        color=n.get('attributes',{}).get('mathcolor',color)
        if n['kind']=='text' and color and not hidden:
            for c in normalize(n.get('text','')):colored[(str(color).lower(),c)]+=1
        for c in n.get('children',[]):paint(c,color,hidden)
    paint(root)
    return {'text':text(root),'tables':tables,'fractions':fractions,'strikes':strikes,'phantoms':phantoms,'colored':dict((json.dumps(k),v) for k,v in sorted(colored.items()))}

def source_roots(source):
    soup=BeautifulSoup(source,'html.parser')
    # A captured MathJax container can include duplicate visible/assistive MathML.
    roots=[]
    for container in soup.find_all('mjx-container'):
        parent=container.find_parent('mjx-container')
        if parent:continue
        maths=container.find_all('math')
        if maths:roots.append(from_mml(maths[0]))
    for math in soup.find_all('math'):
        if not math.find_parent('mjx-container'):roots.append(from_mml(math))
    return roots

def compare(source,rendered):
    expected=[features(n) for n in source_roots(source)]
    actual=features(rendered)
    issues=[]
    # For direct MathML the entire visible expression must match in order.
    if source.lstrip().startswith('<math') and len(expected)==1 and expected[0]['text']!=actual['text']:
        issues.append({'feature':'visible-symbol-sequence','expected':expected[0]['text'],'actual':actual['text']})
    for key in ('tables','fractions','strikes'):
        want=collections.Counter(json.dumps(x,sort_keys=True) for e in expected for x in e[key])
        have=collections.Counter(json.dumps(x,sort_keys=True) for x in actual[key])
        missing=want-have
        if missing:issues.append({'feature':key,'missing':dict(missing),'actual':actual[key]})
    want=collections.Counter()
    for e in expected:want.update(e['colored'])
    missing=want-collections.Counter(actual['colored'])
    if missing:issues.append({'feature':'colored-symbols','missing':dict(missing),'actual':actual['colored']})
    needed=sum(e['phantoms'] for e in expected)
    if needed>actual['phantoms']:issues.append({'feature':'phantom-geometry','expected':needed,'actual':actual['phantoms']})
    return issues

if __name__=='__main__':
    import argparse,pathlib
    p=argparse.ArgumentParser();p.add_argument('conversions');p.add_argument('report');p.add_argument('output');p.add_argument('--source-tex-report');a=p.parse_args()
    if a.source_tex_report:
        for batch in json.load(open(a.source_tex_report))['measurements']:
            for item in batch['items']:
                if len(item['math'])==1:SOURCE_TEX_TREES[item['math'][0]['tex'].strip()]=item['math'][0]['tree']
    source=pathlib.Path(__file__).resolve().parents[2]/'2026-10-16-import-root-cause/source/occurrences.jsonl'
    raw={r['id']:r for r in map(json.loads,source.open())}
    conversion={r['id']:r for r in map(json.loads,open(a.conversions)) if not r['errors']}
    report=json.load(open(a.report));checked=[];missing=[]
    for batch in report['measurements']:
        for item in batch['items']:
            rid=item['id']
            if rid not in conversion:continue
            if len(item['math'])!=1:missing.append({'id':rid,'count':len(item['math']),'errors':item['errors']});continue
            issues=compare(raw[rid]['source_html'],item['math'][0]['tree'])
            checked.append({'id':rid,'issues':issues})
    result={'checked':len(checked),'missing':missing,'issues':[r for r in checked if r['issues']]}
    pathlib.Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'checked':len(checked),'missing':len(missing),'mismatches':len(result['issues'])}))
