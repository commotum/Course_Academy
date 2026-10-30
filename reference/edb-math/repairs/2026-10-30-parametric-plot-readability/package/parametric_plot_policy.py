"""Bank-wide readable scales for parametric graph recognition."""
from pathlib import Path
import hashlib,json,math,struct

KP = 17592186087721
VERSION = 'parametric-readable-grid-1'
IMAGE_PIXELS = 624
NARROW_IMAGE_PIXELS = 240
AXES_RECT = [.10,.09,.85,.85]
LABEL_POINTS = 14
MIN_GRID_PIXELS = 5.5
MIN_DIFFERENCE_PIXELS = 8

class UnreadableBank(ValueError):
    pass

def coordinates(shape, times):
    import numpy as np
    env={'t':times,'sqrt':np.sqrt,'cos':np.cos,'sin':np.sin,'pi':np.pi}
    return np.column_stack([np.broadcast_to(eval(shape[axis],{'__builtins__':{}},env),times.shape) for axis in ('x','y')])

def scalar(value):
    return float(eval(str(value),{'__builtins__':{}},{'pi':math.pi,'oo':math.inf}))

def plot_plan(bank, ts):
    """Uses the complete candidate bank, never the selected correct role."""
    import numpy as np
    if len(bank)!=5:raise ValueError('Expected five parametric candidates')
    times=np.array([scalar(v) for v in ts]);curves=[];points=[]
    for shape in bank:
        t=np.geomspace(.002,2000,3000) if shape['kind']=='rational' else np.linspace(scalar(shape['lo']),scalar(shape['hi']),1601)
        curve=coordinates(shape,t);sample=coordinates(shape,times)
        if not np.isfinite(curve).all() or not np.isfinite(sample).all():raise UnreadableBank('Nonfinite plotted coordinates')
        curves.append(curve);points.append(sample)
    # Unbounded reciprocal curves use the source table's useful viewing region.
    extent=np.concatenate(points if any(s['kind']=='rational' for s in bank) else curves)
    low=np.floor(np.minimum(0,extent.min(axis=0)))-1
    high=np.ceil(np.maximum(0,extent.max(axis=0)))+1
    spans=high-low;longest=float(max(spans))
    grid_pixels=NARROW_IMAGE_PIXELS*AXES_RECT[2]/longest
    if grid_pixels < MIN_GRID_PIXELS:raise UnreadableBank('One-unit grid is too small at the narrow display size')
    # Different loci are insufficient if their differences disappear on screen.
    pair_differences=[]
    for a in range(5):
        for b in range(a):
            distance=max(float(np.linalg.norm(points[a][:,None,:]-curves[b][None,:,:],axis=2).min(axis=1).max()),float(np.linalg.norm(points[b][:,None,:]-curves[a][None,:,:],axis=2).min(axis=1).max()))
            pixels=distance*grid_pixels
            if pixels < MIN_DIFFERENCE_PIXELS:raise UnreadableBank('Candidates cannot be distinguished clearly from their table checkpoints')
            pair_differences.append({'pair':[b,a],'pixels':pixels})
    for sample in points:
        if not ((sample>=low).all() and (sample<=high).all()):raise UnreadableBank('A table checkpoint is clipped')
    return {'version':VERSION,'bounds':[[float(low[0]),float(high[0])],[float(low[1]),float(high[1])]],'minor_step':1,'major_step':2 if longest<=24 else 5,'image_pixels':IMAGE_PIXELS,'axes_rect':AXES_RECT,'label_points':LABEL_POINTS,'narrow_image_pixels':NARROW_IMAGE_PIXELS,'narrow_unit_pixels':grid_pixels,'pair_differences':pair_differences,'checkpoints':[p.tolist() for p in points],'choice_point_markers':False,'choice_coordinate_labels':False}

def validate_delivery_batch(records,kp_id,math_root=None,assets_directory=None):
    if int(kp_id)!=KP:return
    for record in records:
        g=record.get('generation',{})
        if g.get('version')!='parametric-graphs-3':raise ValueError('Parametric delivery requires the repaired readable plotter')
        expected=plot_plan(g['bank'],g['ts'])
        if g.get('plot_plan')!=expected:raise ValueError('Parametric bank readability metadata disagrees with the formulas')
        q=record['question'];field=q[':question/answer-fields'][0]
        def resolve(value):
            path=Path(value)
            if path.is_absolute():return path
            for root in (math_root,assets_directory):
                if root and (Path(root)/path).is_file():return Path(root)/path
            raise ValueError('Cannot inspect the delivered parametric plot')
        expected_hashes=[]
        for path in g['paths']:
            source=Path(path);side=json.loads(source.with_suffix('.json').read_text())
            image_hash=hashlib.sha256(source.read_bytes()).hexdigest()
            if side.get('plot_plan')!=expected or side.get('image_sha256')!=image_hash or side.get('solution_points') or side.get('endpoints') or side.get('coordinate_labels'):
                raise ValueError('Parametric choice plot uses stale scales or answer-revealing annotations')
            data=source.read_bytes()
            if data[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',data[16:24])!=(IMAGE_PIXELS,IMAGE_PIXELS):raise ValueError('Unexpected parametric plot dimensions')
            expected_hashes.append(image_hash)
        delivered=[hashlib.sha256(resolve(a[':answer/value']).read_bytes()).hexdigest() for a in field[':answer-field/choices']]
        if sorted(delivered)!=sorted(expected_hashes):raise ValueError('Delivered graph bank differs from the inspected plots')
        correct=field[':answer-field/correct'];correct_id=str(correct.get(':answer/id')) if isinstance(correct,dict) else str(correct[1])
        correct_choice=next(a for a in field[':answer-field/choices'] if str(a[':answer/id'])==correct_id)
        if hashlib.sha256(resolve(correct_choice[':answer/value']).read_bytes()).hexdigest()!=expected_hashes[g['role']]:raise ValueError('Parametric plot key disagrees with the target role')
        source=Path(g['solution_path']);side=json.loads(source.with_suffix('.json').read_text())
        if side.get('plot_plan')!=expected or side.get('solution_points')!=g['ts'] or side.get('shape')!=g['bank'][g['role']] or side.get('image_sha256')!=hashlib.sha256(source.read_bytes()).hexdigest():
            raise ValueError('Parametric solution does not plot the calculated checkpoints')
