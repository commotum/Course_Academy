import importlib.util,json,concurrent.futures,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def render(args):
 p,out=args;s=importlib.util.spec_from_file_location('kp',ROOT.with_suffix('.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m.render_plot(p,output_dir=out)
if __name__=='__main__':
 s=importlib.util.spec_from_file_location('kp',ROOT.with_suffix('.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 private=ROOT/'concurrency-plots'/uuid.uuid4().hex
 inputs=[{'radius':2,'region':'q4'},{'radius':2,'region':'q4'},{'radius':3,'region':'left'}]
 with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:outputs=list(pool.map(render,[(p,str(private)) for p in inputs]))
 assert outputs[0]==outputs[1] and outputs[0]!=outputs[2]
 for inp,out in zip(inputs,outputs):
  p=Path(out);meta=json.loads(p.with_suffix('.json').read_text());assert meta['radius']==inp['radius'];assert meta['angles']==[str(v) for v in m.REGIONS[inp['region']]];assert meta['renderer_version']=='region-render-5';assert meta['pixel_qa']['interior_fill_coverage']>.995
  import hashlib
  assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['png_sha256']
  assert all(b['axis_clearance_px']>=4 and b['blue_ink_clearance_px']>=4 and b['other_label_clearance_px']>=4 for b in meta['text_boxes'])
 assert not list(private.glob('*.*.png')) and not list(private.glob('*.*.json'))
 (ROOT/'concurrency.json').write_text(json.dumps({'fresh_inputs':inputs,'outputs':outputs,'identical_and_different_processes':True,'temporary_files_remaining':0},indent=2));print('PASS fresh concurrent identical/different renders')
