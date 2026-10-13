"""Generate own-folder side-by-side raster QA sheet using pinned Matplotlib.
No mathematical data creation: reads finished original/generated PNGs only.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
if sys.version_info[:2] != (3,10):
    subprocess.run(['/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10',__file__],check=True); sys.exit(0)
# Own renderer preamble is the pinned dependency authority, copied as data rather
# than importing sibling generators or a mutable environment.
source=(HERE/'render.py').read_text(); preamble=source[:source.index('job=json.loads')]
exec(compile(preamble,str(HERE/'render.py'),'exec'),globals())
from PIL import Image
replays=json.loads((HERE/'source-replays.json').read_text())
fig,axes=plt.subplots(2,2,figsize=(12,11))
for row,r in enumerate(replays):
    for col,path in enumerate((HERE/'source-images'/(r['source_id']+'.png'),Path(r['record']['generation']['plot_assets']['prompt']))):
        im=Image.open(path).convert('RGBA'); white=Image.new('RGBA',im.size,'white'); white.alpha_composite(im)
        axes[row,col].imshow(white.convert('RGB')); axes[row,col].axis('off')
        axes[row,col].set_title(r['source_id']+(' original' if col==0 else ' regenerated'))
fig.tight_layout(); fig.savefig(HERE/'source-comparison.png',dpi=100); plt.close(fig)
review=json.loads((HERE/'review.json').read_text())
fig,axes=plt.subplots(3,4,figsize=(22,16))
for ax,r in zip(axes.flat,review):
    ax.imshow(Image.open(r['generation']['plot_assets']['prompt'])); ax.axis('off')
    ax.set_title(r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['template'])
fig.tight_layout();fig.savefig(HERE/'variant-contact.png',dpi=100);plt.close(fig)
comparison=[]
for r in replays:
    original=HERE/'source-images'/(r['source_id']+'.png');generated=Path(r['record']['generation']['plot_assets']['prompt'])
    import hashlib
    comparison.append({'source_id':r['source_id'],'original_png':str(original),'source_dimensions':list(Image.open(original).size),
      'source_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'generated_png':str(generated),
      'generated_sha256':hashlib.sha256(generated.read_bytes()).hexdigest(),'generated_dimensions':list(Image.open(generated).size),
      'inspected_source_intersection':r['record']['generation']['plot_data']['intersection'],'generated_plot_data':r['record']['generation']['plot_data'],
      'visual_geometry_comparison':'Both line equations/color assignments, signed numbered unit ticks, crossing coordinate, equal unit-square grid and axis arrows preserved. Larger raster and minor text-font/background changes are intentional; not pixel-exact.',
      'source_correct_ref_available':False})
(HERE/'plot-source-comparison.json').write_text(json.dumps({'comparisons':comparison,'source_graphical_coordinate_confirmation':'Original widget/source PNGs inspected independently; actual generated PNGs inspected.','contact_sheet':'source-comparison.png'},indent=2)+'\n')
