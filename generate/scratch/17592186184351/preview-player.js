import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
const el=(tag,cls)=>{let n=document.createElement(tag);n.className=cls;return n};
const inlinePrompt=value=>value;
const fieldLabel=key=>key;
const assetURL=value=>value;
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
const rows=JSON.parse(document.querySelector('#data').textContent);let expected=0;
for(const r of rows){let article=document.createElement('article');article.id=r.question[':question/id'];let h=document.createElement('h2');h.textContent=r.generation.template+' '+JSON.stringify(r.generation.parameters);article.append(h);
let values=[r.question[':question/problem'],...r.question[':question/answer-fields'][0][':answer-field/choices'].map(a=>'$'+a[':answer/value']+'$'),r.question[':question/worked-solution']];
for(let text of values){expected+=(text.match(/\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g)||[]).length;article.append(markdown(text));}document.querySelector('main').append(article);}
await MathJax.startup.promise;await MathJax.typesetPromise();
const svgs=[...document.querySelectorAll('mjx-container svg')];
const errors=[...document.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error')].map(n=>n.textContent);
const empty=svgs.filter(n=>!n.querySelector('path,use,text,rect,line,polygon')).length;
const overflow=[...document.querySelectorAll('mjx-container')].filter(n=>n.getBoundingClientRect().right>document.documentElement.clientWidth+2).length;
const result={records:rows.length,expected_math:expected,rendered_math:svgs.length,errors,empty_svg:empty,horizontal_overflow:overflow,renderer:'player Markdown protection + marked + DOMPurify + MathJax3.2.2 frozen assets'};
result.passed=errors.length===0&&empty===0&&svgs.length===expected&&overflow===0;
document.querySelector('#summary').textContent=JSON.stringify(result);document.title=result.passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});document.title='FAIL';}
