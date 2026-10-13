import assert from 'node:assert/strict';
import test from 'node:test';
import { romanLists } from '../ui/prose-lists.js';
import { marked } from '../ui/vendor/marked/marked.esm.js';

test('imported bold Roman labels render aligned statements without duplicate bullets', () => {
  const html = marked.parse(romanLists('Which equations?\n\nSelect all that apply.\n\n- **I.** CAMATH0END\n- **II.** CAMATH1END\n- **III.** CAMATH2END'));
  assert.match(html, /<ol type="I" class="statement-list">/);
  assert.equal((html.match(/<li>/g) || []).length, 3);
  assert.ok(!html.includes('<ul>'));
  assert.ok(!html.includes('<strong>I.</strong>'));
  assert.match(html, /<li>CAMATH0END<\/li>/);
  assert.match(html, /<p>Select all that apply\.<\/p>/);
});

test('imported statements preserve inline formatting and leading body punctuation', () => {
  const html = marked.parse(romanLists('- **I.** - CAMATH0END **negative**\n\n- **II.** [Reference](https://example.com) CAMATH1END\n\nExplanation.'));
  assert.match(html, /<li>- CAMATH0END <strong>negative<\/strong><\/li>/);
  assert.match(html, /<li><a href="https:\/\/example.com">Reference<\/a> CAMATH1END<\/li>/);
  assert.match(html, /<\/ol>\s*<p>Explanation\.<\/p>/);
});

test('ordinary prose, unordered lists, isolated labels and code examples are left intact', () => {
  for (const source of ['A sentence\nwrapped over lines.', '- First\n- Second', 'I. One statement.', 'I. - First\nII. - Second', 'I. First\nII. Second', 'I. First\nIII. Third', '```text\nI. First\nII. Second\n```', '    I. First\n    II. Second', '- **I.** One statement.', '- **I.** First\n- **III.** Third', '- **I.** First\nII. Second', '```text\n- **I.** First\n- **II.** Second\n```', '    - **I.** First\n    - **II.** Second']) {
    assert.equal(romanLists(source), source);
  }
});


test('Roman statement lists preserve separate paragraphs between authored equations', () => {
  const html = marked.parse(romanLists('Which systems?\n\n- **I.** CAMATH0END\n\n- **II.** CAMATH1END\n\n- **III.** CAMATH2END\n\nExplanation.'));
  assert.equal((html.match(/<li>/g) || []).length, 3);
  assert.match(html, /<\/ol>\s*<p>Explanation\.<\/p>/);
});
