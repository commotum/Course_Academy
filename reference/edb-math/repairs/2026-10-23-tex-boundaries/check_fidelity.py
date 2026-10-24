"""Confirm unchanged non-formatting tokens, with source-backed layout exceptions."""
import difflib,hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent

def tokens(text):
 text=re.sub(r'\\\[/?math\]',lambda _:r'\$',text)
 text=re.sub(r'\[/?(?:math|latex|tex|displaymath)\]','',text)
 text=text.replace('<br>',r'\\')
 text=re.sub(r'\\(?:begin|end)\{[^{}]+\}','',text)
 text=re.sub(r'\\(?:eqalign|matrix|cr)\b','',text)
 text=re.sub(r'\\rule\{0pt\}\{[^{}]+\}','',text)
 text=re.sub(r'\[[+-]?[\d.]+(?:pt|em|ex|cm|mm)\]','',text)
 text=re.sub(r'\\[\[\]()]','',text)
 text=re.sub(r'\\([$%#{}])',r'\1',text)
 text=text.replace('\\\\','').replace('\\ ','').replace('$','').replace('&','').replace('{','').replace('}','')
 text=re.sub(r'\\(?![A-Za-z])','',text)
 return re.sub(r'\s+','',text)

def main():
 fs=json.loads((H/'fields.json').read_text());bad=[];exceptions=[]
 for f in fs:
  if any(x in f['reasons'] for x in ['recover-original-column-multiplication-layout','restore-visible-unknown-and-close-equivalence-group']):exceptions.append([f['entity'],f['attribute'],f['reasons']]);continue
  a,b=tokens(f['before']),tokens(f['after'])
  if a!=b:
   d=list(difflib.ndiff(a,b));bad.append({'entity':f['entity'],'attribute':f['attribute'],'diff':''.join(x for x in d if not x.startswith(' '))[:500]})
 report={'fields':len(fs),'unchanged_non_formatting_tokens':len(fs)-len(exceptions)-len(bad),'source_backed_layout_exceptions':exceptions,'unexpected_changes':bad};(H/'fidelity-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Fields',len(fs),'source-backed exceptions',len(exceptions),'unexpected token changes',len(bad));print(json.dumps(bad[:8],indent=2));assert not bad
if __name__=='__main__':main()
