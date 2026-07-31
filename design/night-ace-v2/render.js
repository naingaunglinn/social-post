const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, 'out');
const SHOTS = path.join(__dirname, 'shots');
fs.mkdirSync(SHOTS, { recursive: true });

const sizes = { 'hero-fb': [1200, 630], 'hero-x': [1920, 1080] };

(async () => {
  const browser = await chromium.launch();
  const metrics = {};
  for (const f of fs.readdirSync(OUT).filter(f => f.endsWith('.html')).sort()) {
    const name = f.replace('.html', '');
    const [w, h] = sizes[name] || [1080, 1350];
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await page.goto('file://' + path.join(OUT, f));
    await page.evaluate(() => document.fonts.ready);
    metrics[name] = await page.evaluate(() => {
      const px = v => parseFloat(v) || 0;
      const hex = (rgb) => {
        const m = (rgb || '').match(/\d+/g);
        return m ? '#' + m.slice(0, 3).map(n => (+n).toString(16).padStart(2, '0')).join('') : '#000000';
      };
      const texts = [];
      document.querySelectorAll('.slide *').forEach(el => {
        if (el.closest('.bar')) return;
        if (el.tagName === 'SPAN' || el.tagName === 'BR') return;
        const kids = [...el.children];
        if (!kids.every(c => c.tagName === 'SPAN' || c.tagName === 'BR')) return;
        if (!el.textContent.trim()) return;
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        const runs = [];
        el.childNodes.forEach(n => {
          if (n.nodeType === 3 && n.textContent) runs.push({ t: n.textContent, c: hex(cs.color) });
          else if (n.tagName === 'SPAN' && n.textContent) runs.push({ t: n.textContent, c: hex(getComputedStyle(n).color) });
          else if (n.tagName === 'BR') runs.push({ br: true });
        });
        texts.push({
          x: r.x, y: r.y, w: r.width, h: r.height,
          fs: px(cs.fontSize), lh: px(cs.lineHeight) || px(cs.fontSize) * 1.2,
          ls: cs.letterSpacing === 'normal' ? 0 : px(cs.letterSpacing),
          weight: +cs.fontWeight, family: cs.fontFamily,
          align: cs.textAlign, runs
        });
      });
      const shapes = [];
      document.querySelectorAll('.bar, .bar i').forEach(el => {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        shapes.push({ x: r.x, y: r.y, w: r.width, h: r.height,
                      color: hex(cs.backgroundColor), radius: px(cs.borderRadius) });
      });
      document.querySelectorAll('.slide [style*="border-left"]').forEach(el => {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        shapes.push({ x: r.x - px(cs.borderLeftWidth), y: r.y, w: px(cs.borderLeftWidth) || 1,
                      h: r.height, color: hex(cs.borderLeftColor), radius: 0 });
      });
      return { bg: hex(getComputedStyle(document.querySelector('.slide')).backgroundColor), texts, shapes };
    });
    await page.screenshot({ path: path.join(SHOTS, name + '.png') });
    await page.close();
    console.log('rendered', name, w + 'x' + h);
  }
  fs.writeFileSync(path.join(__dirname, 'metrics.json'), JSON.stringify(metrics, null, 1));
  await browser.close();
})();
