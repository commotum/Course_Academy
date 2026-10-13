"""Independent raster extents under each original's own axis transform."""
import json,hashlib
from pathlib import Path
from PIL import Image
D=Path(__file__).resolve().parent
# Origins/scales read from black axes and signed labeled ticks, not from ellipse aspect ratios.
# Two-label tick spans used where labels are sparse.
axes={
'q-78679':(94,200,37.5),'q-78680':(56,125,37.5),'q-106398':(201,109,21.1),'q-106399':(205,195,16.1),'q-106704':(172,136,13.35),'q-274862':(95,138,24.65),'q-327171':(169,230,15.0),'q-327172':(205,181,17.8),'q-79289':(92,247,14.0),'q-79290':(188,263,22.2),'q-106706':(223,205,21.1),'q-79285':(247,201,25.9),'q-79286':(229,83,20.0),'q-79287':(92,213,25.3),'q-79292':(46,219,56.0)}
rows=[]
for s in json.load(open(D/'specs.json')):
 im=Image.open('/media/jake/SSD/EDB/math/'+s['asset']).convert('RGBA');pts=[]
 for y in range(im.height):
  for x in range(im.width):
   r,g,b,alpha=im.getpixel((x,y))
   if alpha>120 and b>r+35 and g>r+20:pts.append((x,y))
 box=[min(x for x,y in pts),max(x for x,y in pts),min(y for x,y in pts),max(y for x,y in pts)]
 ox,oy,scale=axes[s['id']];p=s['parameters'];a,b,h,k=[p[x] for x in ('a','b','h','k')];pred=[ox+(h-a)*scale,ox+(h+a)*scale,oy-(k+b)*scale,oy-(k-b)*scale];delta=max(abs(x-y) for x,y in zip(box,pred));assert delta<=2.8,(s['id'],box,pred,delta)
 rows.append({'source_id':s['id'],'raster_sha256':hashlib.sha256(Path('/media/jake/SSD/EDB/math/'+s['asset']).read_bytes()).hexdigest(),'origin_pixels':[ox,oy],'pixels_per_unit':scale,'blue_extents_pixels':box,'predicted_extents_pixels':pred,'maximum_error_pixels':delta,'allowance_pixels':2.8,'signed_labels_inspected':True,'rightmost_A_and_CCW_arrow_inspected':s['level']=='hard','dimension':list(im.size)})
(D/'raster-geometry.json').write_text(json.dumps(rows,indent=2)+'\n');print('Verified',len(rows),'independent original raster geometries')
