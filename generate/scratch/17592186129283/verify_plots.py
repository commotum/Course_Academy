import importlib.util,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',D/'validate_inventory.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
path=D/'reference/replenishment/basis-2604';records=json.loads((path/'generated.json').read_text());root=Path('/media/jake/SSD/EDB/math')
canvas=Image.new('RGB',(1250,len(records)*240),'white');draw=ImageDraw.Draw(canvas);points=0;assets=set()
for row,r in enumerate(records):
 v.g.validate_generated_record(r)
 f=r['question'][':question/answer-fields'][0]
 specs=[r['generation']['plot_specs'][a[':answer/id']] for a in f[':answer-field/choices']]
 locals=v.g.render_plots(specs)
 draw.text((8,row*240+2),str(row+1)+' '+r['question'][':question/difficulty'].split('/')[-1]+' '+str(r['generation']['parameters']),fill='black')
 for col,(a,geometry,local) in enumerate(zip(f[':answer-field/choices'],specs,locals)):
  local=Path(local);stored=root/a[':answer/value'];assert local.read_bytes()==stored.read_bytes()
  assets.add(str(stored));im=Image.open(stored).convert('RGB');meta=json.loads(Path(str(local)+'.json').read_text());x0,y0,x1,y1=meta['bbox'];xmin,xmax=meta['xlim'];ymin,ymax=meta['ylim']
  # Read actual PNG shading, independent of metadata's answer designation.
  for i in range(2,19):
   for j in range(2,19):
    X=xmin+(xmax-xmin)*i/20;Y=ymin+(ymax-ymin)*j/20
    if abs(X)<.25 or abs(Y)<.25 or (j>15 and i<14):continue
    U=X-float(v.F(str(geometry['h'])));V=Y-float(v.F(str(geometry['k'])));c=float(v.F(geometry['coefficient']));n=geometry['degree'];m=geometry['mode']
    if n==0:dist=abs(V) if m in ('top','bottom') else abs(U)
    elif n==-1:
     if abs(U)<.3:continue
     dist=abs(V-c/U)
    else:dist=abs(V-c*U**n)
    slope=0 if n==0 else abs(-c/U**2) if n==-1 else abs(c*n*U**(n-1))
    if dist/(1+slope*slope)**.5<.25:continue
    rgb=im.getpixel((round(x0+(x1-x0)*i/20),round(meta['height']-(y0+(y1-y0)*j/20))))
    # Skip line/text antialiasing; retain pale fill and white background pixels.
    if min(rgb)<180:continue
    actual=rgb[2]>rgb[0]+8 and rgb[0]<235
    assert actual==v.contains(geometry,v.F(str(X)),v.F(str(Y))),(row,col,X,Y,rgb,geometry)
    points+=1
  thumb=im.resize((245,214));canvas.paste(thumb,(col*250,row*240+23))
  if a[':answer/id']==f[':answer-field/correct'][1]:draw.text((col*250+190,row*240+23),'KEY',fill='black')
canvas.save(path/'plot-review.png')
(path/'plot-validation.json').write_text(json.dumps({'passed':True,'actual_png_shading_checks':points,'unique_published_images':len(assets),'plot_montage':str(path/'plot-review.png'),'all_published_bytes_verified':True,'canonical_math_format':True},indent=2)+'\n')
print(points,'actual PNG checks;',len(assets),'published images')
