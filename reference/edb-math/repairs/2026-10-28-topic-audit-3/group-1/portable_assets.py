import json,re
from pathlib import Path
H=Path(__file__).resolve().parent
for cfg in json.loads((H/'generator-stage-config.json').read_text()):
 root=Path(cfg['directory']);helper=root/'audit_presentation.py';text=helper.read_text();text=text.replace("return '![](sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()+')'", "return m[0][:m[0].rfind('](')+2]+'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()+')'")
 text+='''\n\ndef asset_output(path):
    # Immutable packages never write generated plots or caches into themselves.
    import os,tempfile
    base=Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(Path(tempfile.gettempdir())/'course-academy-generator-assets')))
    result=base / PACKAGE_KP / Path(path).name
    result.parent.mkdir(parents=True,exist_ok=True)
    return result
'''.replace('PACKAGE_KP',repr(str(cfg['kp'])))
 helper.write_text(text)
 p=root/cfg['entrypoint'];s=p.read_text();s=s.replace('identity_material as _ca_material','identity_material as _ca_material, asset_output as _ca_asset_output')
 s=re.sub(r'json\.dumps\((obj|x),',lambda m:'json.dumps(_ca_material('+m[1]+'),',s)
 k=cfg['kp']
 if k in[17592186129267,17592186129268]:s=s.replace("dest=EVIDENCE/'images'/('projection-'+key+'.png')","dest=_ca_asset_output(EVIDENCE/'images'/('projection-'+key+'.png'))")
 if k==17592186133899:s=s.replace("target=HERE/'plots'/'legacy-positive.png'","target=_ca_asset_output(HERE/'plots'/'legacy-positive.png')")
 if k==17592186133900:
  s=s.replace("dest=ROOT/'plots'","dest=_ca_asset_output(ROOT/'plots'/'plot').parent")
  s=s.replace("  for f in fields:\n   old=f.get(':answer-field/correct',[None,None])[1];correct_value=next((a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==old),None)\n   for a in f[':answer-field/choices']", "  for field in fields:\n   for a in field[':answer-field/choices']")
 if k==17592186157298:
  s=s.replace("path=HERE/'assets'/f'{key}-{role}.png'","path=_ca_asset_output(HERE/'assets'/f'{key}-{role}.png')")
  lines=s.splitlines(True);identity=[l for l in lines if "qid=uid('question:'+VERSION+':'+sid"in l or "choices=[{':answer/id':uid(fid+':recipe:'"in l];assert len(identity)==2
  s=''.join(l for l in lines if l not in identity)
  marker=" return {'knowledge_point':{'db_id':KP,"
  before=" prompt=_ca_problem(prompt);solution=_ca_prose('\\n\\n'.join(stages));rendered=_ca_values([integral(row)for row in options])\n qid=uid('question:'+digest([VERSION,sid,scale,prompt,solution,rendered]));fid=uid(qid+':selection')\n choices=[{':answer/id':uid(fid+':recipe:'+str(i)),':answer/type':':answer.type/math',':answer/value':value}for i,value in enumerate(rendered)]\n"
  assert s.count(marker)==1;s=s.replace(marker,before+marker)
  s=s.replace("':question/problem':_ca_problem(prompt),':question/worked-solution':_ca_prose('\\n\\n'.join(stages))","':question/problem':prompt,':question/worked-solution':solution")
 if k==17592186175987:s=s.replace("out=BASE/'plots'/f'{key}.png'","out=_ca_asset_output(BASE/'plots'/f'{key}.png')")
 if k==17592186176023:s=s.replace("d=BASE/'plots'","d=_ca_asset_output(BASE/'plots'/'plot').parent")
 if k==17592186176024:s=s.replace("output_dir=Path(output_dir);output_dir.mkdir", "output_dir=_ca_asset_output(Path(output_dir)/'plot').parent;output_dir.mkdir")
 # Keep Matplotlib's font cache outside the immutable package too.
 s=re.sub(r"str\((?:EVIDENCE|HERE|ROOT|BASE)/'(?:matplotlib-cache|reference/mpl-cache)'\)","str(_ca_asset_output(Path('matplotlib-cache')).parent/'matplotlib-cache')",s)
 s=s.replace("cache=HERE/'plots'/'matplotlib-cache'","cache=_ca_asset_output(HERE/'plots'/'matplotlib-cache')")
 p.write_text(s);compile(s,str(p),'exec')
 practice=root/'practice.py'
 if practice.exists():
  s=practice.read_text();s=re.sub(r"VERSION = '([^']+)'",lambda m:'VERSION = '+repr(m[1]+'-format-audit-9837-v1'),s,count=1);practice.write_text(s)
print('Portable assets and pre-identity normalization reviewed for all staged packages.')
