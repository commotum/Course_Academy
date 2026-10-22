import json,importlib.util,pathlib,sys
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
path=pathlib.Path('/home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py')
spec=importlib.util.spec_from_file_location('real_preview',path);r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace("mathContainers:document.querySelectorAll('mjx-container').length,", """mathBoxes:[...document.querySelectorAll('mjx-container')].map(n=>{const b=n.getBoundingClientRect();const svg=n.querySelector('svg');const s=svg?.getBoundingClientRect();const p=n.parentElement.getBoundingClientRect();const overflowX=getComputedStyle(n).overflowX;const before=n.scrollLeft;n.scrollLeft=n.scrollWidth;const reachable=n.scrollLeft;n.scrollLeft=before;return {overflowX,reachableScrollLeft:reachable,tex:n.getAttribute('data-tex'),text:n.textContent,box:{left:b.left,right:b.right,width:b.width},svg:s?{left:s.left,right:s.right,width:s.width}:null,parent:{left:p.left,right:p.right,width:p.width},clientWidth:n.clientWidth,scrollWidth:n.scrollWidth};}),
        mathContainers:document.querySelectorAll('mjx-container').length,""")
records=json.loads((E/'render-records.json').read_text())[12:14]
(E/'overflow-records.json').write_text(json.dumps(records,indent=2))
r.render(records,E/'render-overflow',[E])
print('Additional actual-UI geometry captured for the two screenshot cases.')
