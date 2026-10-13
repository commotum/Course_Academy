"""Read-only source SVG rasterization via installed librsvg/cairo, no generated SVG."""
import ctypes as c, ctypes.util,json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent
r=c.CDLL(ctypes.util.find_library('rsvg-2')); ca=c.CDLL(ctypes.util.find_library('cairo'))
r.rsvg_handle_new_from_file.argtypes=[c.c_char_p,c.c_void_p];r.rsvg_handle_new_from_file.restype=c.c_void_p
r.rsvg_handle_render_cairo.argtypes=[c.c_void_p,c.c_void_p];r.rsvg_handle_render_cairo.restype=c.c_int
class Dimensions(c.Structure):_fields_=[('width',c.c_int),('height',c.c_int),('em',c.c_double),('ex',c.c_double)]
r.rsvg_handle_get_dimensions.argtypes=[c.c_void_p,c.POINTER(Dimensions)]
ca.cairo_image_surface_create.argtypes=[c.c_int,c.c_int,c.c_int];ca.cairo_image_surface_create.restype=c.c_void_p
ca.cairo_create.argtypes=[c.c_void_p];ca.cairo_create.restype=c.c_void_p
ca.cairo_scale.argtypes=[c.c_void_p,c.c_double,c.c_double]
ca.cairo_set_source_rgb.argtypes=[c.c_void_p,c.c_double,c.c_double,c.c_double];ca.cairo_paint.argtypes=[c.c_void_p]
ca.cairo_surface_write_to_png.argtypes=[c.c_void_p,c.c_char_p]
assets=['f8/f82cf760dee34626c290e29420fbaddb4ef254180087d05bb6fb883f2dc32e75.svg','1c/1c2567cd1c2cf28ed17b6dc445025cb60061dc7d7d6c78c960be77f8866ef4a7.svg']
report=[]
for i,a in enumerate(assets):
 p=Path('/media/jake/SSD/EDB/math/images')/a;h=r.rsvg_handle_new_from_file(str(p).encode(),None);dim=Dimensions();r.rsvg_handle_get_dimensions(h,c.byref(dim))
 surface=ca.cairo_image_surface_create(0,dim.width*4,dim.height*4);ctx=ca.cairo_create(surface);ca.cairo_set_source_rgb(ctx,1,1,1);ca.cairo_paint(ctx);ca.cairo_scale(ctx,4,4)
 assert r.rsvg_handle_render_cairo(h,ctx)
 output=D/('canonical-asset-'+str(i)+'.png');assert ca.cairo_surface_write_to_png(surface,str(output).encode())==0
 report.append({'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rendered':output.name,'original_size':[dim.width,dim.height],'scale':4,'renderer':'installed librsvg-2/libcairo','role':'canonical inverse-map math typesetting' if i==0 else 'canonical formal transformation math typesetting'})
(D/'asset-inspection.json').write_text(json.dumps(report,indent=2)+'\n')
