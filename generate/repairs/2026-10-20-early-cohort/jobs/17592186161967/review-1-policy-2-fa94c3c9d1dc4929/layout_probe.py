import sys,json,importlib.util,pathlib
sys.dont_write_bytecode=True
p='/home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py'
s=importlib.util.spec_from_file_location('actual_renderer',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.BROWSER_SCRIPT=m.BROWSER_SCRIPT.replace('const stem = config.output', '''state.overflow = await page.evaluate(() => [...document.querySelectorAll('mjx-container')].filter(n=>n.scrollWidth>n.clientWidth+2).map(n=>{const before=n.scrollLeft;n.scrollLeft=n.scrollWidth;const after=n.scrollLeft;n.scrollLeft=before;return {width:n.clientWidth,scrollWidth:n.scrollWidth,overflowX:getComputedStyle(n).overflowX,scrollable:after>0,text:n.parentElement.textContent.slice(0,200)}}));
      const stem = config.output''')
m.render(json.load(open('render-records.json'))[:1],pathlib.Path('layout-render'),[])
print(json.load(open('layout-render/rendering.json'))['cases'][0]['overflow'])
