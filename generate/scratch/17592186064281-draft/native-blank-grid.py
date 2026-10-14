"""Exhaust every declared normal blank parameter configuration in memory."""
import importlib.util,json,subprocess,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sp=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
probes=[];counts={}
for m in ('q-310179','q-310180','q-310182','q-31241','q-48508','q-48636'):
 counts[m]=0
 for p in g.parameters_for(m):
  r=g.generate(g.LEVELS[m],template=m,parameters=p);v=r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
  if m=='q-310179':b=p['b'];arg=str(p['a'])+r'x^{4}'+('+'+str(b) if b>=0 else str(b));eq=str(4*p['a'])+r'x^{3}/\cos^{2}('+arg+')'
  elif m=='q-31241':eq=str(p['b'])+r'\cos('+str(p['c'])+')'
  elif m=='q-310180':eq='1-1'
  elif m in ('q-48508','q-48636'):eq='2/2'
  else:eq=v+'+0'
  probes.append({'label':m+':'+json.dumps(p,sort_keys=True),'record':r,'checks':[{'submitted':v,'expected':'accepted','purpose':'Every normal blank canonical answer'},{'submitted':eq,'expected':'accepted','purpose':'Every normal blank equivalent answer'},{'submitted':'1' if v=='0' else '0','expected':'rejected','purpose':'Every normal blank simple incorrect answer'}]});counts[m]+=1
(D/'native-blank-grid-input.json').write_text(json.dumps(probes,indent=2)+'\n');binary=ROOT/'generate/runs/current/check-engine';p=subprocess.run([str(binary),str(D/'native-blank-grid-input.json'),str(D/'native-blank-grid-report.json')],text=True,capture_output=True);(D/'native-blank-grid.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stdout+p.stderr
(D/'native-blank-grid-summary.json').write_text(json.dumps({'counts':counts,'records':len(probes),'native_binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'database_writes':0},indent=2)+'\n');print(counts,p.stdout)
