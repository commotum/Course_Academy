"""Explicit non-serving diagnostics: native interval argument bound, not math errors."""
import copy,hashlib,importlib.util,json,subprocess,uuid
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sp=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
items=[]
for m,p,wrong in [('q-310179',{'a':24,'b':20},r'95x^{3}\sec^{2}(24x^{4}+20)'),('q-310179',{'a':24,'b':20},'314159'),('q-31241',{'b':2,'c':-20},'0')]:
 valid={'a':24,'b':-8} if m=='q-310179' else {'b':2,'c':-16};r=g.generate(g.LEVELS[m],template=m,parameters=valid);r['generation'].update(parameters=p,eligible_for_learning=False,evidence_only=True,profile='unsupported-native-diagnostic')
 q=r['question'];src=g.SOURCES[m];q[':question/problem']=g.normalized_prose(g.transform(src[':question/problem'],m,p));q[':question/worked-solution']=g.normalized_prose(g.transform(src[':question/worked-solution'],m,p)).replace('{sec}',r'\sec')
 if m=='q-310179':value=r'96x^{3}\sec^{2}(24x^{4}+20)'
 else:value=r'2\cos(20)';q[':question/problem']+='\n\n{{field-1}}'
 qid=str(uuid.uuid5(uuid.UUID(g.KP_UUID),json.dumps([m,p,wrong])));q[':question/id']=qid;f=q[':question/answer-fields'][0];fid=str(uuid.uuid5(uuid.UUID(qid),f[':answer-field/key']));aid=str(uuid.uuid5(uuid.UUID(fid),value));f[':answer-field/id']=fid;f[':answer-field/choices']=[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value}];f[':answer-field/correct']=[':answer/id',aid]
 items.append({'label':f'unsupported-{m}-{wrong}','record':r,'checks':[{'submitted':wrong,'expected':'unresolved','purpose':'Document the excluded native argument-bound limitation'}]})
(D/'native-limits-input.json').write_text(json.dumps(items,indent=2)+'\n');p=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'native-limits-input.json'),str(D/'native-limits-report.json')],capture_output=True,text=True);(D/'native-limits.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr;print(p.stdout)
