import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const read = name => readFile(new URL('../ui/' + name, import.meta.url), 'utf8');
const profile = await read('profile.js');
const themeSource = profile.slice(profile.indexOf('const themeKey'), profile.indexOf('const trigger')).replaceAll('export ', '');
const graph = await read('Math-Academy-Graph-Explorer.html');
const competencySource = graph.slice(graph.indexOf('  function competencyFor('), graph.indexOf('  function updateCompetencyReadout('));
const paletteSource = graph.match(/const PALETTE = .*;/)[0];
const styles = await read('navigation.css');
const colors = { dark: {}, light: {} };
for (const match of styles.matchAll(/:root(\[data-theme="light"\])?\s*\{([^}]+)\}/g)) {
  for (const declaration of match[2].matchAll(/(--[\w-]+):\s*([^;]+);/g)) {
    colors[match[1] ? 'light' : 'dark'][declaration[1]] = declaration[2].trim();
  }
}

function fixture(theme) {
  const window = new EventTarget();
  const document = { documentElement: { dataset: { theme } } };
  const context = vm.createContext({ window, document, CustomEvent, localStorage: { setItem() {} }, repetitions: {} });
  vm.runInContext(`${themeSource}\n${paletteSource}\n${competencySource}`, context);
  return context;
}

test('each page restores light mode before its styles load, with a safe dark fallback', async () => {
  for (const name of ['Learning.html', 'Assignments.html', 'Course.html', 'Topic.html', 'Math-Academy-Graph-Explorer.html']) {
    const html = await read(name);
    const script = html.match(/<script>([\s\S]*?)<\/script>/);
    assert.ok(script.index < html.indexOf('<link'), name);
    for (const stored of ['light', 'dark', null, 'invalid']) {
      const document = { documentElement: { dataset: {} } };
      vm.runInNewContext(script[1], { document, localStorage: { getItem: () => stored } });
      assert.equal(document.documentElement.dataset.theme, stored === 'light' ? 'light' : 'dark', name);
    }
    const document = { documentElement: { dataset: {} } };
    vm.runInNewContext(script[1], { document, localStorage: { getItem() { throw new Error('Storage blocked'); } } });
    assert.equal(document.documentElement.dataset.theme, 'dark', name);
  }
});

test('shared neutral colors invert while preserving alpha and error text stays red', () => {
  for (const [name, dark] of Object.entries(colors.dark)) {
    if (!name.startsWith('--tone-')) continue;
    const light = colors.light[name];
    assert.ok(light, name);
    assert.equal(parseInt(dark.slice(1, 3), 16) + parseInt(light.slice(1, 3), 16), 255, name);
    assert.equal(light.slice(7), dark.slice(7), name);
  }
  assert.equal(colors.dark['--theme-scheme'], 'dark');
  assert.equal(colors.light['--theme-scheme'], 'light');
  assert.equal(colors.light['--error-text'], '#a12424');
});

test('graph nodes and progress swatches share reversed mastery bands without changing scores', () => {
  const dark = fixture('dark'), light = fixture('light');
  const luminance = hex => {
    const v = parseInt(hex.slice(1, 3), 16) / 255;
    return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
  };
  for (let level = 0; level <= 6; level++) {
    for (const [theme, context] of [['dark', dark], ['light', light]]) {
      const repetitions = level + 0.25;
      context.repetitions[1] = repetitions;
      const node = context.competencyFor(1);
      assert.equal(node.level, level);
      assert.equal(node.repetitions, repetitions);
      assert.equal(node.fill.toLowerCase(), colors[theme][`--mastery-${level}`]);
      assert.equal(node.text.toLowerCase(), colors[theme][`--mastery-text-${level}`]);
      const fill = luminance(node.fill), text = luminance(node.text);
      assert.ok((Math.max(fill, text) + 0.05) / (Math.min(fill, text) + 0.05) >= 4.5);
    }
    assert.equal(colors.light[`--mastery-${level}`], colors.dark[`--mastery-${6 - level}`]);
  }
  const unknown = light.competencyFor(999);
  assert.equal(unknown.known, false);
  assert.equal(unknown.repetitions, null);
  assert.equal(unknown.fill, '#ffffff');
  assert.equal(unknown.dash, '4 3');
});

test('canvas colors invert RGB but preserve transparency', () => {
  const c = fixture('light');
  assert.equal(c.themeColor('#050505'), '#fafafa');
  assert.equal(c.themeColor('#fff'), '#000000');
  assert.equal(c.themeColor('#090909ee'), '#f6f6f6ee');
  assert.equal(c.themeColor('rgba(255,255,255,.18)'), 'rgba(0,0,0,.18)');
  c.setColorTheme('dark', false);
  assert.equal(c.themeColor('#050505'), '#050505');
});
