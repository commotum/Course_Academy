import { marked } from './vendor/marked/marked.esm.js';

const roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX'];

// Call after protecting TeX, then sanitize the final Markdown output as usual.
// Legacy captures label statement lists with Roman numerals, which Markdown
// otherwise treats as one paragraph with soft line breaks.
export function romanLists(source) {
  const lines = source.split('\n'), result = [];
  let fence = null;
  for (let i = 0; i < lines.length; i++) {
    const delimiter = /^ {0,3}(`{3,}|~{3,})/.exec(lines[i]);
    if (delimiter) {
      if (!fence) fence = delimiter[1];
      else if (delimiter[1][0] === fence[0] && delimiter[1].length >= fence.length) fence = null;
      result.push(lines[i]); continue;
    }
    if (fence) { result.push(lines[i]); continue; }
    const items = [];
    let next = i;
    while (next < lines.length && items.length < roman.length) {
      let candidate = next;
      if (items.length) while (candidate < lines.length && !lines[candidate].trim()) candidate++;
      const match = /^ {0,3}([IVX]+)\.[ \t]+(.+)$/.exec(lines[candidate] || '');
      if (!match || match[1] !== roman[items.length]) break;
      items.push(match[2]); next = candidate + 1;
    }
    if (items.length < 2) { result.push(lines[i]); continue; }
    // The leading bullet is a known nested-list artifact in Roman captures.
    const nestedBullet = items.every(item => item.startsWith('- '));
    result.push('', '<ol type="I" class="statement-list">', ...items.map(item =>
      `<li>${marked.parseInline(nestedBullet ? item.slice(2) : item, { async: false, gfm: true })}</li>`), '</ol>', '');
    i = next - 1;
  }
  return result.join('\n');
}
