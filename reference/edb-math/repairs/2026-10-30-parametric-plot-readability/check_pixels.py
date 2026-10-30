"""Read actual PNG pixels to verify the promised one-unit grid is present."""
import json,math
from pathlib import Path
import numpy as np
from PIL import Image
H=Path(__file__).resolve().parent
def check(path):
    path=Path(path);side=json.loads(path.with_suffix('.json').read_text());im=np.array(Image.open(path).convert('RGB'));height,width=im.shape[:2]
    x,y,w,h=side['axes_pixel_bounds'];xl,yl=side['bounds']
    r0=math.ceil(height-y-h+4);r1=math.floor(height-y-4);c0=math.ceil(x+4);c1=math.floor(x+w-4)
    grey=(np.max(im,axis=2)-np.min(im,axis=2)<4)&(im[:,:,0]<250)
    scores=[]
    for k in range(math.ceil(xl[0])+1,math.floor(xl[1])):
        column=round(x+(k-xl[0])/(xl[1]-xl[0])*w)
        scores.append(float(grey[r0:r1,column-1:column+2].any(axis=1).mean()))
    for k in range(math.ceil(yl[0])+1,math.floor(yl[1])):
        row=round(height-(y+(k-yl[0])/(yl[1]-yl[0])*h))
        scores.append(float(grey[row-1:row+2,c0:c1].any(axis=0).mean()))
    assert scores and min(scores)>.65,(path,min(scores))
    return min(scores)

if __name__=='__main__':
    rows=json.loads((H/'candidate-pool.json').read_text())+json.loads((H/'representative-sources.json').read_text());scores=[]
    for r in rows:
        for path in [*r['generation']['paths'],r['generation']['solution_path']]:scores.append(check(path))
    result={'passed':True,'actual_png_grids_checked':len(scores),'minimum_grid_line_coverage':min(scores)}
    (H/'pixel-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
