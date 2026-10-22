import importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('actual_renderer','/home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.BROWSER_SCRIPT=m.BROWSER_SCRIPT.replace("const stem = config.output", """state.horizontalScroll=await page.evaluate(() => [...document.querySelectorAll('mjx-container[display=\"true\"]')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>{const before=e.scrollLeft;e.scrollLeft=e.scrollWidth;return {scrollWidth:e.scrollWidth,clientWidth:e.clientWidth,before,after:e.scrollLeft,overflowX:getComputedStyle(e).overflowX,text:e.textContent};}));
      const stem = config.output""")
m.render([json.load(open(R/'render-additional-records.json'))[-1]],R/'render-scroll',[])
