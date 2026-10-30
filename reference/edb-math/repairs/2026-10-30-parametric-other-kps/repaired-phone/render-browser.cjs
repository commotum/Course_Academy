
const fs = require('fs');
const config = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const { chromium } = require(config.playwright);
const audit = () => {
        const root = document.querySelector('.lesson-content');
        const visible = element => {
          // The native select stores TeX values for the rich UI; learners see
          // its rendered trigger/menu instead. aria-hidden alone is not a
          // visibility test, so keep this exception specific to that control.
          if (element.closest('select.answer-select-native[aria-hidden="true"]')) return false;
          const style = getComputedStyle(element);
          return style.visibility !== 'hidden' && style.visibility !== 'collapse'
            && style.display !== 'none' && element.getClientRects().length > 0;
        };
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
        const rawTex = [], codeMath = [];
        let node;
        while ((node = walker.nextNode())) {
          if (!visible(node.parentElement) || node.parentElement.closest('mjx-container,math,script,style,textarea,math-field')) continue;
          if (/\\(?:begin|end)\{|\\(?:eqalign|dfrac|frac|sqrt)\b|\$\$|\[\/?math\]/.test(node.textContent)) rawTex.push(node.textContent.slice(0,200));
          if (node.parentElement.closest('pre,code') && /\$|\\(?:begin|dfrac|frac)/.test(node.textContent)) codeMath.push(node.textContent.slice(0,200));
        }
        return {
        rawTex, codeMath,
        internalFieldLabels:[...root.querySelectorAll('.answer-field legend,.response-summary')]
          .filter(visible).map(node=>node.textContent.trim()).filter(text=>/^Answer:\s*(answer|selection)(?:\s|[·:]|$)/i.test(text)),
        mathContainers:document.querySelectorAll('mjx-container').length,
        // noUndefined renders unknown commands as mtext, not merror. SVG
        // mtext contains glyph references, so textContent alone misses them.
        mathErrors:[
          ...[...document.querySelectorAll('[data-mml-node="merror"],mjx-merror,.math-error')].filter(visible).map(node=>node.textContent),
          ...[...document.querySelectorAll('mjx-container [data-mml-node="mtext"],mjx-container mjx-mtext')]
            .filter(visible).map(node=>node.textContent || [...node.querySelectorAll('use[data-c]')]
              .map(glyph=>String.fromCodePoint(parseInt(glyph.getAttribute('data-c'),16))).join(''))
            .filter(text=>/\\[A-Za-z]+/.test(text))
        ],
        brokenImages:[...document.images].filter(image=>!image.complete || !image.naturalWidth).map(image=>image.src),
        danglingGlyphs:[...document.querySelectorAll('mjx-container use')].map(node=>node.getAttribute('href') || node.getAttribute('xlink:href'))
          .filter(href=>href?.startsWith('#') && !document.getElementById(href.slice(1))),
        text:document.querySelector('.lesson-content').innerText,
        fonts:document.fonts.status
      }};
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:config.browser,
    args:['--disable-dev-shm-usage']});
  const reports = [];
  try {
    for (let index = 0; index < config.count; index++) {
      const context = await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1});
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(String(error)));
      await page.route('**/*', route => new URL(route.request().url()).origin === config.origin
        ? route.continue() : route.abort());
      await page.goto(config.origin + '/learn?activityId=' + index, {waitUntil:'networkidle'});
      await page.locator('.lesson-content').waitFor();
      // Lazy images in the worked solution also need to load before a full-page capture.
      await page.evaluate(async () => {
        for (const image of document.images) image.loading = 'eager';
        if (window.MathJax?.startup?.promise) await MathJax.startup.promise;
        await document.fonts.ready;
      });
      await page.waitForLoadState('networkidle');
      await page.evaluate(async () => {
        if (window.MathJax?.typesetPromise) await MathJax.typesetPromise();
        await document.fonts.ready;
        await Promise.all([...document.images].map(image => image.decode().catch(() => {})));
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      });
      const state = await page.evaluate(audit);
      const stem = config.output + '/question-' + String(index + 1).padStart(3,'0');
      await page.screenshot({path:stem+'.png',fullPage:true,animations:'disabled'});
      fs.writeFileSync(stem+'.html',await page.content());
      state.dropdowns = [];
      // The completed preview intentionally disables inputs. Load an active
      // presentation through the same unmodified UI to exercise real menus.
      if (await page.locator('.answer-select-trigger').count()) {
        await page.goto(config.origin + '/learn?activityId=' + index + '-active', {waitUntil:'networkidle'});
        await page.locator('.lesson-content').waitFor();
        await page.evaluate(async () => {
          for (const image of document.images) image.loading = 'eager';
          if (window.MathJax?.startup?.promise) await MathJax.startup.promise;
          if (window.MathJax?.typesetPromise) await MathJax.typesetPromise();
          await document.fonts.ready;
          await Promise.all([...document.images].map(image => image.decode().catch(() => {})));
        });
        const triggers = page.locator('.answer-select-trigger');
        for (let optionIndex = 0; optionIndex < await triggers.count(); optionIndex++) {
          const trigger = triggers.nth(optionIndex);
          if (await trigger.isDisabled()) throw new Error('Active preview dropdown is disabled');
          await trigger.click();
          await page.evaluate(async () => {
            if (window.MathJax?.typesetPromise) await MathJax.typesetPromise();
            await document.fonts.ready;
            await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
          });
          const menu = await page.evaluate(audit);
          menu.screenshot = stem + '-dropdown-' + (optionIndex + 1) + '.png';
          menu.open = await trigger.getAttribute('aria-expanded') === 'true';
          await page.screenshot({path:menu.screenshot,fullPage:true,animations:'disabled'});
          state.dropdowns.push(menu);
          await page.keyboard.press('Escape');
        }
      }
      state.tableWidths=await page.locator('.lesson-content table').evaluateAll(nodes=>nodes.map(n=>({width:n.getBoundingClientRect().width,scrollWidth:n.scrollWidth,clientWidth:n.clientWidth})));state.index=index; state.screenshot=stem+'.png'; state.javascriptErrors=errors;
      state.passed=!errors.length && !state.mathErrors.length && !state.brokenImages.length
        && !state.danglingGlyphs.length && !state.rawTex.length && !state.codeMath.length
        && !state.internalFieldLabels.length && state.fonts==='loaded'
        && (!config.expectedMath[index] || state.mathContainers>0)
        && state.dropdowns.every(menu => menu.open && !menu.rawTex.length && !menu.codeMath.length
          && !menu.mathErrors.length && !menu.brokenImages.length && !menu.danglingGlyphs.length
          && !menu.internalFieldLabels.length && menu.fonts === 'loaded');
      reports.push(state);
      await context.close();
    }
  } finally { await browser.close(); }
  const report={renderer:'unmodified ui/Learning.html and learning.js',database_writes:0,
    passed:reports.every(item=>item.passed),cases:reports};
  fs.writeFileSync(config.output+'/rendering.json',JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({passed:report.passed,count:reports.length,report:config.output+'/rendering.json'}));
  if (!report.passed) process.exitCode=1;
})().catch(error=>{console.error(error);process.exitCode=1});
