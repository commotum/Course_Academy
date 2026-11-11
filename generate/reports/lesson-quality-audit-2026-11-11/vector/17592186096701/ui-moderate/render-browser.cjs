
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
    for (const index of config.selectedIndices) {
    for (const presentation of config.states) {
    for (const viewport of config.viewports) {
      const context = await browser.newContext({viewport,deviceScaleFactor:1});
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(String(error)));
      await page.route('**/*', route => new URL(route.request().url()).origin === config.origin
        ? route.continue() : route.abort());
      await page.goto(config.origin + '/learn?activityId=' + index + (presentation === 'active' ? '-active' : ''), {waitUntil:'networkidle'});
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
      const filename = 'question-' + String(index + 1).padStart(3,'0') + '-' + presentation + '-' + viewport.width + 'x' + viewport.height;
      const stem = config.output + '/' + filename;
      await page.screenshot({path:stem+'.png',fullPage:true,animations:'disabled'});
      fs.writeFileSync(stem+'.html',await page.content());
      // Wide prose math and option labels may scroll in outer prose containers.
      // Retain the left-edge screenshot above, then inspect the hidden right edge.
      state.horizontalMath = await page.evaluate(() =>
        [...document.querySelectorAll('.lesson-content mjx-container, .lesson-content .choice .prose, .lesson-content .worked-solution > .prose')]
          .filter(node => node.getClientRects().length && node.clientWidth > 0
            && !node.closest('details:not([open])')
            && node.scrollWidth > node.clientWidth + 3
            // SVG intrinsic scrollWidth may exceed its responsive drawn width.
            // Audit only formulas whose drawn SVG actually exceeds the viewport.
            && [...node.querySelectorAll('svg')].some(svg => svg.getBoundingClientRect().width > node.clientWidth + 3))
          .map(node => {
            node.scrollLeft = node.scrollWidth;
            return {tagName:node.tagName, className:node.className, clientWidth:node.clientWidth, scrollWidth:node.scrollWidth,
              overflowX:getComputedStyle(node).overflowX, scrollLeft:node.scrollLeft};
          }));
      if (state.horizontalMath.length) {
        state.horizontalMathScreenshot = filename + '-math-scroll-right.png';
        await page.screenshot({path:config.output + '/' + state.horizontalMathScreenshot,
          fullPage:true,animations:'disabled'});
        await page.evaluate(() => {
          for (const node of document.querySelectorAll('.lesson-content mjx-container, .lesson-content .choice .prose, .lesson-content .worked-solution > .prose')) node.scrollLeft = 0;
        });
      }
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
          menu.screenshot = filename + '-dropdown-' + (optionIndex + 1) + '.png';
          menu.state = 'active';
          menu.open = await trigger.getAttribute('aria-expanded') === 'true';
          await page.screenshot({path:config.output + '/' + menu.screenshot,fullPage:true,animations:'disabled'});
          state.dropdowns.push(menu);
          await page.keyboard.press('Escape');
        }
      }
      state.index=index; state.screenshot=filename+'.png'; state.javascriptErrors=errors;
      state.state=presentation; state.viewport=viewport; state.record_sha256=config.recordSha256[index];
      state.passed=!errors.length && !state.mathErrors.length && !state.brokenImages.length
        && !state.danglingGlyphs.length && !state.rawTex.length && !state.codeMath.length
        && !state.internalFieldLabels.length && state.fonts==='loaded'
        && state.horizontalMath.every(math => ['auto','scroll'].includes(math.overflowX)
          && math.scrollLeft > 0)
        && (!config.expectedMath[presentation][index] || state.mathContainers>0)
        && state.dropdowns.every(menu => menu.open && !menu.rawTex.length && !menu.codeMath.length
          && !menu.mathErrors.length && !menu.brokenImages.length && !menu.danglingGlyphs.length
          && !menu.internalFieldLabels.length && menu.fonts === 'loaded');
      reports.push(state);
      await context.close();
    }
    }
    }
  } finally { await browser.close(); }
  const report={renderer:'unmodified ui/Learning.html and learning.js',database_writes:0,
    passed:reports.every(item=>item.passed),cases:reports};
  fs.writeFileSync(config.output+'/rendering.json',JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({passed:report.passed,count:reports.length,report:config.output+'/rendering.json'}));
  if (!report.passed) process.exitCode=1;
})().catch(error=>{console.error(error);process.exitCode=1});
