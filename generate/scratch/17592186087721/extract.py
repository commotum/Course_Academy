"""One-time read-only capture extraction; masks are complete math components."""
import json,re
from pathlib import Path
P=Path(__file__).parent
s=json.loads((P/'source.json').read_text())['record']
forms=[('t**2-2','3-t','-3','3','poly'),('t**2','(2-t)*(t+3)','-5','5','poly'),('t+1','1-t','-3','3','poly'),('t-1','t**2-5','-3','3','poly'),('2-t**2','t+1','-1','3','poly'),('2*sqrt(t)','t','0','4','root'),('2*t','5/t','0','oo','rational'),('t**2','t*(5-t)','0','5','poly'),('3*sqrt(t)','t**3-2*t','0','2','root'),('7*cos(t)','5*sin(t)','0','2*pi','ellipse'),('1-2*t','t','-3','3','poly'),('5-t**2','t**2-3','0','3','poly'),('t-2','t**2+1','-4','4','poly'),('t**2','t**3/5','-4','4','poly'),('2*cos(t)','2*sin(t)','0','2*pi','ellipse'),('2*t-1','2-t**2','-3','3','poly')]
ts_ellipse=['0','pi/6','pi/3','2*pi/3','pi','4*pi/3','5*pi/3']
out={};cases=[]
for q,(x,y,lo,hi,kind) in zip(s[':knowledge-point/questions'],forms):
 sol=q[':question/worked-solution'];tables=re.findall(r'(?:\|.*\|\n){3}\|.*\|',sol)
 xt=re.search(r'formula \$x=(.*?)\.\$',sol).group(1);yt=re.search(r'using \$y=(.*?)\.\$',sol).group(1)
 mask=sol.replace(tables[0],'{TABLE1}').replace(tables[1],'{TABLE2}')
 mask=mask.replace('formula $x='+xt+'.$','formula $x={X}.$').replace('using $y='+yt+'.$','using $y={Y}.$')
 asset=re.search(r'!\[\]\((.*?)\)',sol).group(1);mask=mask.replace(asset,'{ASSET}')
 prompt=q[':question/problem'];start=prompt.index('x=')+2;end=start+len(xt);assert prompt[start:end]==xt
 prompt=prompt[:start]+'{X}'+prompt[end:];start=prompt.index('y=')+2;end=start+len(yt);assert prompt[start:end]==yt;prompt=prompt[:start]+'{Y}'+prompt[end:]
 cells=[z.strip() for z in tables[0].splitlines()[0].split('|')[1:-1]];label=cells[0][3:-3];tts=[z[1:-1] for z in cells[1:]]
 ts=ts_ellipse if kind=='ellipse' else tts
 af=q[':question/answer-fields'][0];assets=[a[':answer/value'] for a in af[':answer-field/choices']];ci=assets.index(af[':answer-field/correct'][':answer/value'])
 ident=q[':question/math-academy-id'];out[ident]={'source_id':q[':question/id'],'source_db_id':q[':db/id'],'x':x,'y':y,'lo':lo,'hi':hi,'kind':kind,'x_tex':xt,'y_tex':yt,'label':label,'ts':ts,'ts_tex':tts,'decimal':kind in ('root','rational') or ident=='q-16195','prompt_mask':prompt,'solution_mask':mask,'choice_assets':assets,'correct_index':ci,'solution_asset':asset}
 if kind=='ellipse':out[ident].update(a='7' if ident=='q-16198' else '2',b='5' if ident=='q-16198' else '2')
 cases.append({'source_id':q[':question/id'],'math_academy_id':ident,'template':ident,'parameters':{'m':1,'n':1,'h':0,'k':0},'bank_profile':'observed:'+ident})
(P/'templates.json').write_text(json.dumps(out,indent=2)+'\n');(P/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
