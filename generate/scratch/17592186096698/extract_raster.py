"""Private numerical evidence reader; raster fitting is not learner generation."""
import json,math
from pathlib import Path
from PIL import Image
H=Path(__file__).parent
spec={
'q-50195':[(141,223,56,54),(141,167,56,39),(141,128,56,39),(141,223,56,54),(169,167,67,39),(169,235,67,45)],
'q-50196':[(169,167,38,39)]*6,
'q-119132':[(169,163,20,16.5),(169,163,31,25.5),(169,163,20,16.5),(169,163,20,16.5),(169,163,20,16.5),(169,240,31,25.5)],
'q-49947':[(85,167,56,39),(85,167,56,39),(85,234,56,46),(102,204,67,39),(73,125,49,39),(73,204,49,39)],
'q-50197':[(85,234,56,46),(85,234,56,46),(85,234,56,46),(85,100,56,46),(85,234,56,46),(85,100,56,46)],
'q-50198':[(169,150,38,35),(169,150,38,35),(169,167,38,39),(169,163,38,28),(169,162,38,28),(169,150,38,35)],
'q-79565':[(169,204,67,67),(169,204,67,67),(169,163,80,80),(169,123,67,67),(169,163,67,63),(169,163,67,63)],
'q-79566':[(295,167,54,39),(295,167,54,39),(295,167,54,39),(275,167,49,39),(295,156,54,39),(295,167,54,39)],
'q-119139':[(232,163,31,31),(232,163,31,31),(232,163,31,31),(232,163,31,31),(194,188,26,25.5),(106,163,31,31)],
'q-119142':[(169,163,31,31)]*6,
'q-79563':[(169,163,67,56),(169,163,67,56),(169,163,46,40),(169,133,52.5,48),(169,192,52.5,48.5),(169,163,67,56)],
'e-530':[(169,203,67,40)]}
# Expected base functions inferred from whole plots, then calibrated against pixels.
base={
'q-50195':['(x-1)**2','x','-(x-1)**2','(x-1)**2','x**3','x**2'],
'q-50196':['-(x+1)**3','-(x+1)**3','-(x-1)**2','(x-1)**3','-(x+1)**2','-x**3'],
'q-119132':['-2*exp(-x/4)','-x**2/4','2*exp(-x/4)-2','-2*exp(x/4)+2','-2*exp(-x/4)','x**2/4'],
'q-49947':['log(x)','log(x)','1/x','x','log(x)','1/x'],
'q-50197':['1/x','x','x**2/4','-1/x','1/x','-sqrt(x)'],
'q-50198':['-2*x','-2*x','-x**3/4','x**2','-x**2','2*x'],
'q-79565':['x**2','x**2','2*x','-x**2','x**3','x**3'],
'q-79566':['(x+2)**3/2','(x+2)**3/2','(x+2)**2','(x+3)**3/2','-(x+2)**2','-(x+2)**3/2'],
'q-119139':['-2*exp(2*x)','2*exp(2*x)','-(x+2)**2/4','-2*exp(2*x)','(x+2)**2/4','-2*exp(-2*x)'],
'q-119142':['-(x-1)**3/4','(x+1)**2','-(x-1)**3/4','-(x+1)**3/4','(x-1)**3/4','-(x-1)**2'],
'q-79563':['3*x','-3*x','x**3','-x**2','x**2','3*x'],
'e-530':['x**2']}
# Colored curves fitted as A*base+B; possible horizontal translation explicitly
# handled later, because a polynomial coefficient fit cannot recover that family.
result=[]
for a in json.loads((H/'asset-index.json').read_text()):
 i=0 if a['role']=='solution' else int(a['role']);src=a['source'];ox,oy,sx,sy=spec[src][i]
 im=Image.open(a['local']).convert('RGB');points={c:[] for c in ('red','blue')}
 for px in range(12,im.width-25):
  if abs(px-ox)<8:continue
  for color in points:
   ys=[]
   for py in range(24,im.height-5):
    r,g,b=im.getpixel((px,py))
    if abs(py-oy)<5:continue
    if (color=='red' and r>170 and g<100 and b<100) or (color=='blue' and b>170 and r<100 and g<100):ys.append(py)
   if not ys:continue
   py=sum(ys)/len(ys);x=(px-ox)/sx;y=(oy-py)/sy
   try:z=eval(base[src][i],{'x':x,'exp':math.exp,'log':math.log,'sqrt':math.sqrt})
   except (ValueError,ZeroDivisionError):continue
   points[color].append((z,y))
 fits={}
 for c,pts in points.items():
  n=len(pts);sz=sum(z for z,y in pts);syy=sum(y for z,y in pts);szz=sum(z*z for z,y in pts);szy=sum(z*y for z,y in pts)
  aa=(n*szy-sz*syy)/(n*szz-sz*sz);bb=(syy-aa*sz)/n;rmse=math.sqrt(sum((aa*z+bb-y)**2 for z,y in pts)/n)
  fits[c]={'scale':round(aa,4),'offset':round(bb,4),'rmse_units':round(rmse,4),'samples':n}
 result.append(dict(a,origin=[ox,oy],pixels_per_unit=[sx,sy],proposed_base=base[src][i],fits=fits))
(H/'raster-evidence.json').write_text(json.dumps(result,indent=2))
for a in result:print(a['source'],a['role'],a['proposed_base'],a['fits'])
