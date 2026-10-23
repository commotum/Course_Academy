import importlib.util,sys
from pathlib import Path
sys.dont_write_bytecode=True
p=Path('/home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py')
s=importlib.util.spec_from_file_location('actual_renderer',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
needle="fs.writeFileSync(stem+'.html',await page.content());"
extra=r'''
      state.scrollGeometry = await page.evaluate(() => [...document.querySelectorAll('mjx-container[display="true"]')].map(e=>({clientWidth:e.clientWidth,scrollWidth:e.scrollWidth,overflow:getComputedStyle(e).overflowX})));
      for (const fraction of [0.5,1]) {
        await page.evaluate(f => { for (const e of document.querySelectorAll('mjx-container[display="true"]')) e.scrollLeft=(e.scrollWidth-e.clientWidth)*f; }, fraction);
        await page.screenshot({path:stem+'-scroll-'+fraction+'.png',fullPage:true,animations:'disabled'});
      }
'''
assert needle in m.BROWSER_SCRIPT
m.BROWSER_SCRIPT=m.BROWSER_SCRIPT.replace(needle,needle+extra)
m.main()
