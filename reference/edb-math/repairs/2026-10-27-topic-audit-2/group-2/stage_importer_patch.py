from pathlib import Path
import difflib,json
H=Path(__file__).resolve().parent;R=H.parents[4];p=R/'scripts/import_historical_question_content.py';s=p.read_text();original=s
s=s.replace('self.topic=topic;self.errors=[];self.assets=[];self.fields=[];self.formulas=[]','self.topic=topic;self.errors=[];self.assets=[];self.fields=[];self.formulas=[]\n        self.control_fields={};self.control_indices={};self.extracting_controls=False')
s=s.replace("        t=n.name.lower()\n        if t=='mrow':",'''        t=n.name.lower()
        if self.extracting_controls and t=='msub':
            children=n.find_all(recursive=False)
            marker=re.fullmatch(r'\\(S(\\d+)\\)',children[1].get_text('',strip=True)) if len(children)==2 else None
            if marker:
                index=int(marker[1])
                assert index in self.control_indices, 'Unmapped source control S'+str(index)
                return '{{'+self.control_indices[index]+'}}'
        if self.extracting_controls and t=='mrow':
            children=n.find_all(recursive=False)
            if len(children)==3 and self.brace_glyph(children[0],'{') and self.brace_glyph(children[2],'}') and children[1].name=='msub':
                inner=children[1].find_all(recursive=False)
                if len(inner)==2 and re.fullmatch(r'\\(S\\d+\\)',inner[1].get_text('',strip=True)):return self.m(children[1])
        if t=='mrow':''')
s=s.replace("        if extract_fields and 'selectList' in classes:\n            selected", "        if extract_fields and 'selectList' in classes:\n            if id(n) in self.control_fields:return '{{'+self.control_fields[id(n)]+'}}'\n            selected")
s=s.replace("            selected=n.find(class_='selectListFrame')\n            assert selected is not None and 'correctSelection' in selected.get('class',[]), 'Unverified historical dropdown'","            selected=n.find(class_=lambda c: c and ('selectListFrame' in c))\n            assert selected is not None and any(c in ('correctSelection','correctSelectionMultipleAttempts') for c in selected.get('class',[])), 'Unverified historical dropdown'")
s=s.replace("            value=value[1:-1] if value.startswith('$') and value.endswith('$') else value\n            choices=[]", "            value=value[1:-1] if re.fullmatch(r'\\$[^$]+\\$',value,re.S) else value\n            choices=[]")
s=s.replace("                text=text[1:-1] if text.startswith('$') and text.endswith('$') else text\n                if text not in [c['value'] for c in choices]:choices.append({'type':'math','value':text})", "                kind='math' if re.fullmatch(r'\\$[^$]+\\$',text,re.S) else 'text'\n                text=text[1:-1] if kind=='math' else text\n                if text not in [c['value'] for c in choices]:choices.append({'type':kind,'value':text})")
s=s.replace("            self.fields.append({'key':key,'type':'select'", "            self.control_fields[id(n)]=key\n            marker=re.search(r'-(\\d+)$',n.get('id',''))\n            assert marker, 'Source dropdown has no observed control index'\n            index=int(marker[1])\n            assert index not in self.control_indices, 'Duplicate source control index'\n            self.control_indices[index]=key\n            self.fields.append({'key':key,'type':'select'")
s=s.replace("            math=n if t=='math' else n.find('math')", "            if t=='math':math=n\n            else:\n                # Option CHTML can contain MathML before the enclosing formula.\n                # Select only MathML owned by this container, outside dropdowns.\n                roots=n.find_all('mjx-assistive-mml',recursive=False)\n                candidates=[m for root in roots for m in root.find_all('math') if m.find_parent(class_='selectList') is n.find_parent(class_='selectList')]\n                assert len(candidates)==1, 'Ambiguous or absent owned MathML'\n                math=candidates[0]")
s=s.replace("    def text(self,n,extract_fields=False):return normalize_math_boundaries(re.sub('\\n{3,}','\\n\\n',self.render(n,extract_fields)).strip())", "    def text(self,n,extract_fields=False):\n        previous=self.extracting_controls\n        if extract_fields:\n            # Register observed DOM indices before visiting outer assistive MML.\n            # render(select,True) requires historical correctSelection evidence.\n            for control in n.find_all(class_='selectList'):self.render(control,True)\n        self.extracting_controls=extract_fields\n        try:return normalize_math_boundaries(re.sub('\\n{3,}','\\n\\n',self.render(n,extract_fields)).strip())\n        finally:self.extracting_controls=previous")
assert s!=original
(H/'import_historical_question_content.py').write_text(s)
(H/'historical-controls.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='a/scripts/import_historical_question_content.py',tofile='b/scripts/import_historical_question_content.py')))
