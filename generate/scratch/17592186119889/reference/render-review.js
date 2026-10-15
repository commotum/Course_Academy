import {marked} from '/ui/vendor/marked/marked.esm.js';
import {romanLists} from '/ui/prose-lists.js';
function el(tag,cls){const n=document.createElement(tag);if(cls)n.className=cls;return n;}
function fieldLabel(key){return key;}
function escapeHTML(text) { return String(text).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]); }
function assetURL(value) {
  if (!value) return '';
  if (String(value).startsWith('/api/asset?')) return value;
  return '/api/asset?path=' + encodeURIComponent(String(value).replace(/^file:\/\//, ''));
}
function markdown(value, className = 'prose', fields = []) {
  const container = el('div', className);
  // Protect TeX from Markdown's underscore, backslash, and table processing.
  const math = [];
  const prefix = 'CAMATH' + crypto.randomUUID().replaceAll('-', '') + 'TOKEN';
  const fieldKeys = new Set(fields.map(field => field.key));
  const placeholder = /\{\{(?:answer-field:)?([^}]+)\}\}/g;
  let source = String(value).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g, match => {
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

const rows=await (await fetch('validation/side-by-side.json')).json();
const candidates=await (await fetch('replenishment/candidates.json')).json();
const main=document.querySelector('main');
const sections=[];
for(const candidate of candidates){
 const sid=candidate.generation.template,source=rows.find(x=>x.source_id===sid).original;
 const section=el('section');section.style='display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start';
 for(const [label,q] of [['Source '+sid,source],['New '+JSON.stringify(candidate.generation.parameters),candidate.question]]){
  const card=el('article');card.style='padding:24px;background:white;border:1px solid #ddd;min-width:0';
  const title=el('h2');title.textContent=label;card.append(title,markdown(q[':question/problem']));
  if(q[':question/answer-fields'])for(const f of q[':question/answer-fields'])for(const a of f[':answer-field/choices'])card.append(markdown('$'+a[':answer/value']+'$'));
  card.append(markdown(q[':question/worked-solution']));section.append(card);
 }
 main.append(section);sections.push(section);
}
// Exercise every family through the same Markdown/sanitization/MathJax path.
for(const row of rows){const card=el('article');card.append(markdown(row.variant.question[':question/problem']),markdown(row.variant.question[':question/worked-solution']));main.append(card);}
await MathJax.startup.promise;await MathJax.typesetPromise([main]);
const errors=[...document.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.textContent);
const status=el('pre');status.id='render-status';status.textContent=JSON.stringify({done:true,errors,svg:document.querySelectorAll('mjx-container').length,columns:sections.length*2});document.body.prepend(status);
