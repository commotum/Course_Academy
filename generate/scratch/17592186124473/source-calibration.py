"""Read-only source raster calibration (transparent pixels composited in memory)."""
import json,sys,re
from pathlib import Path
cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
for package in ('numpy','pillow'):
 candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name)]
 sys.path.insert(0,str(sorted(candidates)[-1]))
import numpy as np
from PIL import Image
here=Path(__file__).resolve().parent;records=[]
units={'q-36039':(43,43),'q-36941':(40,40),'q-108667':(40,40),'q-108673':(37.5,37.5),'q-108791':(35,35),'q-108795':(40,40),'q-36002':(49.5,49.5),'q-36004':(17.5,17.5),'q-36008':(48.25,48.25),'q-36011':(39.2,39.2),'q-36061':(34,40),'q-36066':(37.5,37.5),'q-36934':(40,40),'e-3962':(37.5,37.5)}
for p in sorted(here.glob('*-0-0.png')):
 im=Image.open(p).convert('RGBA');canvas=Image.new('RGBA',im.size,'white');canvas.alpha_composite(im);rgb=np.asarray(canvas)[:,:,:3]/255
 black=np.max(rgb,axis=2)<.7;ox=int(np.argmax(black.sum(axis=0)));oy=int(np.argmax(black.sum(axis=1)))
 grey=(np.max(rgb,axis=2)-np.min(rgb,axis=2)<.025)&(rgb[:,:,0]>.55)&(rgb[:,:,0]<.95)
 def groups(mask,axis):
  score=mask.sum(axis=axis);threshold=mask.shape[axis]*.4;positions=np.where(score>threshold)[0];runs=[]
  for k in positions:
   if not runs or k>runs[-1][-1]+1:runs.append([k])
   else:runs[-1].append(k)
  return [round(sum(g)/len(g),2) for g in runs]
 x=groups(grey,0);y=groups(grey,1)
 records.append({'file':p.name,'origin_pixels':[ox,oy],'vertical_grid_columns':x,'horizontal_grid_rows':y,'median_grid_spacing_pixels':[float(np.median(np.diff(x))) if len(x)>1 else None,float(np.median(np.diff(y))) if len(y)>1 else None],'inspection':'Axes and each endpoint/tail/grid/label checked against full-resolution raster. Exact formulas and unlabelled fractional values not inferred.'})
for r in records:
 sid=r['file'].split('-0-0')[0];r['label_calibrated_pixels_per_unit']=units[sid];r['pixel_measurement_tolerance']=1;r['grid_coordinate_increment']=2 if sid in ('q-36941','q-36004') else 1 if sid!='q-36061' else None;r['axis_measurement_notes']='Origin detection uses axis stroke intensity; grid spacing is measured independently per raster. q-36061 uses labeled coordinate points instead of grid and unequal pixel scales.'
(here/'source-calibration.json').write_text(json.dumps({'renderer':'Read-only Pillow/numpy pixel analysis','python':sys.version.split()[0],'records':records},indent=2));print(json.dumps(records,indent=2))
