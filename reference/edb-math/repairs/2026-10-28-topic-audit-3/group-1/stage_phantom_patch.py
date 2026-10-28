from pathlib import Path
import difflib
H=Path(__file__).resolve().parent;R=H.parents[4];P=H/'phantom-patch';P.mkdir(exist_ok=True)
dom=(R/'scripts/question_capture/dom.js').read_text();extract=(R/'capture/scripts/browser/extract.js').read_text()
helper=extract[extract.index('  const mathColor ='):extract.index('  // MathJax emits a brace')]
helper=helper.replace("fail('Unsupported decorated MathML phantom: ' + reason)","errors.push('Unsupported decorated MathML phantom: ' + reason)")
helper=helper.replace('m(child, true)','m(child)')
helper+='''  function visiblePhantomOwner(n) {
    for (let p = n.parentElement; p && p.localName !== 'math'; p = p.parentElement) {
      if (p.localName === 'menclose' && ['box','longdiv',null].includes(p.getAttribute('notation'))) return true;
      if (p.localName === 'mstyle' && (p.hasAttribute('mathbackground') || p.hasAttribute('style'))) return true;
    }
    return false;
  }
'''
dom=dom.replace('  function m(n, environment=null) {',helper+'  function m(n, environment=null) {')
dom=dom.replace("if (n.nodeType !== 1 || !value) return value;","if (n.nodeType !== 1 || !value || (n.localName === 'mstyle' && n.querySelector('mphantom') && (n.hasAttribute('mathbackground') || n.hasAttribute('style')))) return value;")
dom=dom.replace("    // Phantom content only reserves space; none of its descendants are visible.\n    if (t === 'mphantom') return '';", "    const decorated = decoratedPhantom(n);\n    if (decorated !== null) return decorated;\n    // Bare phantoms remain invisible; an explicit box depends on their width.\n    if (t === 'mphantom') return visiblePhantomOwner(n) ? '\\\\phantom{' + [...n.childNodes].map(child => m(child)).join('') + '}' : '';")
(P/'dom.js').write_text(dom)
hist=(R/'scripts/import_historical_question_content.py').read_text()
method=r'''    def decorated_phantom(self,n):
        if n.name!='mstyle' or not n.find('mphantom') or not any(n.has_attr(a) for a in ('style','mathbackground')):return None
        def reject(reason):
            self.errors.append('Unsupported decorated MathML phantom: '+reason);return ''
        if any(a not in ('style','mathbackground') and not a.startswith('data-mjx-') for a in n.attrs):return reject('container attributes')
        background=n.get('mathbackground');style=n.get('style');options=[]
        if background is not None and not re.fullmatch(r'[A-Za-z]+|#[\da-fA-F]{3}(?:[\da-fA-F]{3})?',background):return reject('background')
        children=n.find_all(recursive=False)
        if len(children)!=1:return reject('padding container')
        padded=children[0]
        if background is not None and style is None and padded.name=='mrow' and all(a.startswith('data-mjx-') for a in padded.attrs):return '\\bbox['+background+']{'+''.join(self.m(c) for c in padded.children)+'}'
        if padded.name!='mpadded' or any(a not in ('height','depth','lspace','width') and not a.startswith('data-mjx-') for a in padded.attrs):return reject('padding container')
        pad=re.fullmatch(r'(\d+)(pt|px|em|ex|in|cm|mm)',padded.get('lspace',''))
        if not pad or int(pad[1])<=0 or padded.get('height')!='+'+pad[0] or padded.get('depth')!='+'+pad[0] or padded.get('width')!='+'+str(2*int(pad[1]))+pad[2]:return reject('asymmetric or unsupported padding')
        options.append(pad[0])
        if background is not None:options.append(background)
        if style is not None:
            match=re.fullmatch(r'\s*border:\s*([^:;]+);?\s*',style);tokens=match[1].split() if match else []
            widths=[x for x in tokens if re.fullmatch(r'\d+(?:pt|px|em|ex|in|cm|mm)',x)]
            colors=[x for x in tokens if x!='solid' and re.fullmatch(r'[A-Za-z]+|#[\da-fA-F]{3}(?:[\da-fA-F]{3})?',x)]
            if len(tokens) not in (2,3) or len(widths)!=1 or len(colors)!=len(tokens)-2 or tokens.count('solid')!=1:return reject('border style')
            options.append('border:'+widths[0]+' solid'+(' '+colors[0] if colors else ''))
        return '\\bbox['+','.join(options)+']{'+''.join(self.m(c) for c in padded.children)+'}'
    @staticmethod
    def visible_phantom_owner(n):
        for p in n.parents:
            if not isinstance(p,Tag) or p.name=='math':return False
            if p.name=='menclose' and p.get('notation') in (None,'box','longdiv'):return True
            if p.name=='mstyle' and any(p.has_attr(a) for a in ('style','mathbackground')):return True
        return False
'''
# Raw text above intentionally contains Python TeX string escapes; regular source uses doubled slashes.
method=method.replace("'\\\\bbox[","'\\bbox[") if False else method
hist=hist.replace('    def m(self,n):',method+'    def m(self,n):')
hist=hist.replace("if not isinstance(n,Tag) or not value:return value","if not isinstance(n,Tag) or not value or (n.name=='mstyle' and n.find('mphantom') and any(n.has_attr(a) for a in ('style','mathbackground'))):return value")
hist=hist.replace("        if t in ('mphantom','annotation','annotation-xml'):return ''", "        decorated=self.decorated_phantom(n)\n        if decorated is not None:return decorated\n        if t=='mphantom':return '\\\\phantom{'+''.join(self.m(c) for c in n.children)+'}' if self.visible_phantom_owner(n) else ''\n        if t in ('annotation','annotation-xml'):return ''")
(P/'import_historical_question_content.py').write_text(hist)
patch=''
for original,staged in [('scripts/question_capture/dom.js','dom.js'),('scripts/import_historical_question_content.py','import_historical_question_content.py')]:patch+=''.join(difflib.unified_diff((R/original).read_text().splitlines(True),(P/staged).read_text().splitlines(True),fromfile='a/'+original,tofile='b/'+original))
(H/'decorated-phantom-parity.patch').write_text(patch)
print('staged',len(patch),'bytes')
