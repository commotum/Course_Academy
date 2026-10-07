import assert from 'node:assert/strict';
import test from 'node:test';
import { romanLists } from '../ui/prose-lists.js';
import { marked } from '../ui/vendor/marked/marked.esm.js';

test('captured statements render as separate Roman list items without nested bullet artifacts', () => {
  const html = marked.parse(romanLists('Which equations?\n\nI. - CAMATH0END\nII. - CAMATH1END\nIII. - CAMATH2END'));
  assert.match(html, /<ol type="I" class="statement-list">/);
  assert.equal((html.match(/<li>/g) || []).length, 3);
  assert.ok(!html.includes('<ul>'));
  assert.match(html, /<li>CAMATH0END<\/li>/);
});

test('Roman list bodies preserve rich inline content and explicit math minus signs', () => {
  const html = romanLists('I. **First** CAMATH0END\nII. CAMATH1END');
  assert.match(html, /<strong>First<\/strong> CAMATH0END/);
  assert.equal(romanLists('I. CAMATH0END\nII. CAMATH1END').includes('CAMATH0END'), true);
});

test('ordinary prose, unordered lists, isolated labels and code examples are left intact', () => {
  for (const source of ['A sentence\nwrapped over lines.', '- First\n- Second', 'I. One statement.', 'I. First\nIII. Third', '```text\nI. First\nII. Second\n```', '    I. First\n    II. Second']) {
    assert.equal(romanLists(source), source);
  }
});


test('Roman statement lists preserve separate paragraphs between authored equations', () => {
  const html = marked.parse(romanLists('Which systems?\n\nI. CAMATH0END\n\nII. CAMATH1END\n\nIII. CAMATH2END\n\nExplanation.'));
  assert.equal((html.match(/<li>/g) || []).length, 3);
  assert.match(html, /<\/ol>\s*<p>Explanation\.<\/p>/);
});
