import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
const el=(tag,cls)=>{let n=document.createElement(tag);n.className=cls;return n};
const inlinePrompt=value=>value, fieldLabel=key=>key, assetURL=value=>value.startsWith('/')?'file://'+value:'file:///media/jake/SSD/EDB/math/'+value;
const escapeHTML=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
function markdown(value, className = 'prose', fields = []) {
  const container = el('div', className);
  // Protect TeX from Markdown's underscore, backslash, and table processing.
  const math = [];
  const prefix = 'CAMATH' + crypto.randomUUID().replaceAll('-', '') + 'TOKEN';
  const fieldKeys = new Set(fields.map(field => field.key));
  const placeholder = /\{\{(?:answer-field:)?([^}]+)\}\}/g;
  let source = inlinePrompt(value, fields).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g, match => {
    math.push(match.replace(placeholder, (whole, key) => fieldKeys.has(key)
      ? `\\underbrace{\\qquad}_{\\text{answer ${fields.findIndex(field => field.key === key) + 1}}}` : whole));
    return prefix + (math.length - 1) + 'END';
  });
  source = source.replace(placeholder, (whole, key) => fieldKeys.has(key) ? `<span class="field-location">${escapeHTML(fieldLabel(key))}</span>` : whole);
  let html = marked.parse(romanLists(source), { async: false, gfm: true, breaks: false });
  html = html.replace(new RegExp(prefix + '(\\d+)END', 'g'), (_, i) => escapeHTML(math[Number(i)]));
  const fragment = DOMPurify.sanitize(html, {
    RETURN_DOM_FRAGMENT: true,
    USE_PROFILES: { html: true },
    FORBID_TAGS: ['style', 'form', 'input', 'button', 'textarea', 'select', 'iframe', 'object', 'embed'],
    FORBID_ATTR: ['style', 'srcset'],
  });
  for (const image of fragment.querySelectorAll('img')) {
    image.src = assetURL(image.getAttribute('src'));
    image.referrerPolicy = 'no-referrer';
    image.loading = 'lazy';
    image.addEventListener('error', () => {
      const note = el('span', 'math-error', `Image unavailable${image.alt ? ': ' + image.alt : '.'}`);
      image.replaceWith(note);
    }, { once: true });
  }
  for (const link of fragment.querySelectorAll('a')) {
    const href = link.getAttribute('href') || '';
    if (!/^https?:\/\//i.test(href) && !href.startsWith('#')) link.removeAttribute('href');
    else { link.target = '_blank'; link.rel = 'noopener noreferrer'; }
  }
  container.append(fragment);
  return container;
}
try {
await MathJax.startup.promise;const rows=JSON.parse(document.querySelector('#data').textContent);let reports=[];
for(let {label,record} of rows){let q=record.question,a=document.createElement('article');a.dataset.label=label;let h=document.createElement('h2');h.textContent=label;a.append(h);
const inputs=[q[':question/problem'],...q[':question/answer-fields'][0][':answer-field/choices'].map(x=>'$'+x[':answer/value']+'$'),q[':question/worked-solution']||'No solution captured.'];
let expected=0;for(let text of inputs){expected+=(text.match(/\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g)||[]).length;a.append(markdown(text));}
document.querySelector('main').append(a);for(let im of a.querySelectorAll('img'))im.loading='eager';let before=[...MathJax.startup.document.math].length;await MathJax.typesetPromise([a]);let items=[...MathJax.startup.document.math].slice(before);
let errors=[...a.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error')].map(n=>n.textContent),svgs=[...a.querySelectorAll('mjx-container svg')];
reports.push({label,expected_math:expected,rendered_math:svgs.length,items:items.map(i=>({tex:i.math,tree:i.root.toString()})),errors,literal_dollars:a.innerText.includes('$'),empty_svg:svgs.filter(n=>!n.querySelector('path,use,text,rect,line,polygon')).length,horizontal_overflow:a.scrollWidth>a.clientWidth,images:[...a.querySelectorAll('img')].map(im=>({src:im.src,width:im.naturalWidth,height:im.naturalHeight}))});
}
await new Promise(resolve=>setTimeout(resolve,5000));for(let report of reports){let article=[...document.querySelectorAll('article')].find(a=>a.dataset.label===report.label);report.images=[...article.querySelectorAll('img')].map(im=>({src:im.src,width:im.naturalWidth,height:im.naturalHeight}));report.horizontal_overflow=article.scrollWidth>article.clientWidth;}let passed=reports.every(r=>r.expected_math===r.rendered_math&&!r.errors.length&&!r.literal_dollars&&!r.empty_svg&&!r.horizontal_overflow&&r.images.every(im=>im.width>0));document.querySelector('#summary').textContent=JSON.stringify({passed,records:reports});document.title=passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});document.title='FAIL';}
