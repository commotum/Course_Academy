"""Normalize capture-only span wrappers and TeX comments before title conversion."""
import importlib.util,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];RAW=ROOT/'.local/edb/math-image-import-audit-2026-10-22'
spec=importlib.util.spec_from_file_location('converter',ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/secondary/convert_source.py');conv=importlib.util.module_from_spec(spec);spec.loader.exec_module(conv)
def normalized_title(title):
 protected={}
 def hide(m):
  key='CAPTUREHTMLFRAGMENT'+str(len(protected))+'END';protected[key]=m[0];return key
 title=conv.CONTAINER.sub(hide,title)
 title=re.sub(r'(?<!\\)%[^\n]*','',title)
 for key,value in protected.items():title=title.replace(key,value)
 # The source editor wrapped the second slash of a TeX line break in a span.
 title=title.replace('<span>\\</span>','\\\\')
 return title.replace('frame=""','frame="none"')
def main():
 source=json.loads((RAW/'repair-source-svgs.json').read_text());out={};errors=[]
 for e in json.loads((HERE/'conversion-errors.json').read_text()):
  if e['evidence']['kind']!='asset-title':continue
  path=e['evidence']['path'];original=re.search(r'<title\b[^>]*>[\s\S]*?</title>',source[path])[0]
  title=normalized_title(original)
  r=conv.convert_source({'id':path,'source_html':title})
  if r['errors']:errors.append({'path':path,'errors':r['errors']});continue
  assert not re.search(r'<[A-Za-z][^>]*>',r['tex']),r
  out[path]={'tex':r['tex'],'method':'normalized-source-title','normalizations':['capture span linebreak wrappers','omit TeX comments after protecting nested HTML','empty frame means none']}
 (HERE/'normalized-title-recoveries.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');(HERE/'remaining-title-errors.json').write_text(json.dumps(errors,indent=2)+'\n')
 print('recovered',len(out),'errors',errors)
if __name__=='__main__':main()
