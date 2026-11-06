// Retro-desktop bumper: generic late-90s desktop drawn from scratch (no real logos or screenshots).
// Usage: node bumper.mjs STILL OUT_DIR [--text "..."]
import {spawn} from 'node:child_process';
import {mkdirSync, writeFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import {join} from 'node:path';

const sharp = createRequire('/Users/carolyndorantes/AI/tdm155ai-week-6/package.json')('sharp');
const [still, outDir] = process.argv.slice(2);
const ti = process.argv.indexOf('--text');
const TEXT = ti > 0 ? process.argv[ti + 1] : 'joanna podcast :)';
mkdirSync(outDir, {recursive: true});

const W = 1920, H = 1080, FPS = 24, DUR = 8, N = FPS * DUR;
const FONT = `font-family="Tahoma, Verdana, Arial, sans-serif"`;
const svg = (w, h, body) => Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">${body}</svg>`);
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const ease = t => t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t);
const lerp = (a, b, t) => a + (b - a) * t;

// ---------- primitives ----------
const bevel = (x, y, w, h, inset = false) => {
  const [lt, rb, lt2, rb2] = inset ? ['#808080', '#fff', '#000', '#dfdfdf'] : ['#fff', '#000', '#dfdfdf', '#808080'];
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#c0c0c0"/>
  <path d="M${x} ${y + h}V${y}H${x + w}" stroke="${lt}" stroke-width="2" fill="none"/>
  <path d="M${x} ${y + h}H${x + w}V${y}" stroke="${rb}" stroke-width="2" fill="none"/>
  <path d="M${x + 2} ${y + h - 2}V${y + 2}H${x + w - 2}" stroke="${lt2}" stroke-width="2" fill="none"/>
  <path d="M${x + 2} ${y + h - 2}H${x + w - 2}V${y + 2}" stroke="${rb2}" stroke-width="2" fill="none"/>`;
};
const btn = (x, y, w, h, label = '', pressed = false, size = 15) =>
  bevel(x, y, w, h, pressed) + (label ? `<text x="${x + w / 2}" y="${y + h / 2 + size * 0.36}" text-anchor="middle" font-size="${size}" ${FONT}>${esc(label)}</text>` : '');
const win = (w, h, title, active = true, menu = []) => {
  let s = bevel(0, 0, w, h);
  s += `<defs><linearGradient id="tb${active}" x1="0" x2="1"><stop offset="0" stop-color="${active ? '#000080' : '#808080'}"/><stop offset="1" stop-color="${active ? '#1084d0' : '#b5b5b5'}"/></linearGradient></defs>`;
  s += `<rect x="5" y="5" width="${w - 10}" height="28" fill="url(#tb${active})"/>`;
  s += `<rect x="11" y="11" width="16" height="16" fill="#fff" stroke="#000"/><rect x="13" y="13" width="12" height="4" fill="#000080"/>`;
  s += `<text x="34" y="25" font-size="16" font-weight="bold" fill="#fff" ${FONT}>${esc(title)}</text>`;
  const bx = w - 9;
  s += btn(bx - 24, 9, 22, 20) + `<text x="${bx - 13}" y="25" text-anchor="middle" font-size="15" font-weight="bold" ${FONT}>×</text>`;
  s += btn(bx - 50, 9, 22, 20) + `<rect x="${bx - 45}" y="13" width="12" height="10" fill="none" stroke="#000" stroke-width="2"/>`;
  s += btn(bx - 74, 9, 22, 20) + `<rect x="${bx - 69}" y="22" width="10" height="3" fill="#000"/>`;
  let mx = 12;
  for (const m of menu) { s += `<text x="${mx}" y="54" font-size="15" ${FONT}>${m}</text>`; mx += m.length * 9 + 20; }
  return s;
};

// ---------- wallpaper + icons ----------
async function desktop() {
  let s = `<defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d5fd6"/><stop offset=".55" stop-color="#6fa7ee"/><stop offset="1" stop-color="#cfe4fb"/></linearGradient>
    <linearGradient id="hill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7cc843"/><stop offset=".5" stop-color="#3f9a1f"/><stop offset="1" stop-color="#22660f"/></linearGradient>
    <linearGradient id="hill2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fb23a"/><stop offset="1" stop-color="#1f5a10"/></linearGradient>
    <filter id="soft"><feGaussianBlur stdDeviation="22"/></filter></defs>
  <rect width="${W}" height="${H}" fill="url(#sky)"/>`;
  for (const [cx, cy, rx, ry, o] of [[300, 210, 260, 60, .8], [520, 170, 200, 50, .7], [1250, 140, 320, 70, .75], [1600, 260, 240, 55, .6], [900, 330, 280, 45, .5]])
    s += `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="#fff" opacity="${o}" filter="url(#soft)"/>`;
  s += `<path d="M0 760 C 400 620, 900 600, 1300 700 S 1800 820, 1920 760 V1080 H0Z" fill="url(#hill2)"/>`;
  s += `<path d="M0 820 C 500 640, 1100 600, 1920 860 V1080 H0Z" fill="url(#hill)"/>`;
  const icons = [
    ['Docs', 'folder'], ['Trash', 'trash'], ['Smiley', 'smile'], ['Star', 'star'], ['Globe', 'globe'], ['Heart', 'heart'],
    ['Music', 'note'], ['Camera', 'cam'], ['Paint', 'brush'], ['Notes', 'notes'], ['Games', 'dice'], ['Mail', 'mail'],
  ];
  icons.forEach(([label, kind], i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 30 + col * 100, y = 30 + row * 150;
    s += `<g transform="translate(${x + 18},${y})">${iconArt(kind)}</g>`;
    s += `<text x="${x + 42}" y="${y + 82}" text-anchor="middle" font-size="15" fill="#fff" ${FONT} style="paint-order:stroke" stroke="#003" stroke-width="3">${label}</text>`;
  });
  return sharp(svg(W, H, s)).png().toBuffer();
}
function iconArt(k) {
  switch (k) {
    case 'folder': return `<path d="M2 14h18l6 6h22v34H2z" fill="#f4d35e" stroke="#7a5a00" stroke-width="2"/>`;
    case 'trash': return `<path d="M10 14h28l-4 42H14z" fill="#d8d8d8" stroke="#333" stroke-width="2"/><rect x="6" y="8" width="36" height="6" fill="#aaa" stroke="#333" stroke-width="2"/><path d="M18 22v28M24 22v28M30 22v28" stroke="#555" stroke-width="2"/>`;
    case 'smile': return `<circle cx="24" cy="30" r="22" fill="#ffe600" stroke="#7a6a00" stroke-width="2"/><circle cx="17" cy="24" r="3"/><circle cx="31" cy="24" r="3"/><path d="M13 35 Q24 46 35 35" stroke="#000" stroke-width="3" fill="none"/>`;
    case 'star': return `<path d="M24 4l6 16h17l-14 10 5 17-14-10-14 10 5-17L1 20h17z" fill="#ff4fa3" stroke="#7a0040" stroke-width="2"/>`;
    case 'globe': return `<circle cx="24" cy="30" r="22" fill="#2d7de0" stroke="#002a66" stroke-width="2"/><path d="M10 22c8 2 10 10 6 16s4 10 10 6M30 10c-4 6 4 8 8 10s4 10 0 14" fill="#4cc23a"/>`;
    case 'heart': return `<path d="M24 52C6 38 2 28 8 18s16-8 16 2c0-10 10-12 16-2s2 20-16 34z" fill="#ff3355" stroke="#700" stroke-width="2"/>`;
    case 'note': return `<path d="M16 46V12l26-6v34" stroke="#222" stroke-width="4" fill="none"/><ellipse cx="11" cy="46" rx="8" ry="6" fill="#9a4dff"/><ellipse cx="37" cy="40" rx="8" ry="6" fill="#9a4dff"/>`;
    case 'cam': return `<rect x="2" y="16" width="44" height="32" rx="4" fill="#444" stroke="#000" stroke-width="2"/><rect x="14" y="10" width="16" height="8" fill="#444"/><circle cx="24" cy="32" r="11" fill="#7fd1ff" stroke="#fff" stroke-width="3"/>`;
    case 'brush': return `<rect x="4" y="34" width="40" height="18" fill="#fff" stroke="#333" stroke-width="2"/><circle cx="14" cy="43" r="4" fill="#f33"/><circle cx="24" cy="43" r="4" fill="#3c3"/><circle cx="34" cy="43" r="4" fill="#36f"/><path d="M30 4l8 4-14 24-6-2z" fill="#c96" stroke="#333" stroke-width="2"/>`;
    case 'notes': return `<rect x="8" y="6" width="32" height="46" fill="#fff" stroke="#333" stroke-width="2"/><path d="M14 18h20M14 26h20M14 34h20M14 42h12" stroke="#36c" stroke-width="2"/>`;
    case 'dice': return `<rect x="6" y="12" width="36" height="36" rx="6" fill="#fff" stroke="#333" stroke-width="2"/><circle cx="16" cy="22" r="3.5"/><circle cx="24" cy="30" r="3.5"/><circle cx="32" cy="38" r="3.5"/>`;
    case 'mail': return `<rect x="2" y="14" width="44" height="32" fill="#fff" stroke="#333" stroke-width="2"/><path d="M2 14l22 18 22-18" stroke="#333" stroke-width="2" fill="none"/>`;
  }
}

// ---------- windows ----------
const CALC = {x: 250, y: 60, w: 400, h: 430};
const PAINT = {x: 610, y: 24, w: 1100, h: 680};
const PICK = {x: 470, y: 470, w: 520, h: 440};
const NOTE = {x: 1120, y: 560, w: 640, h: 440};
const DOC = {x: 200, y: 50, w: 1360, h: 960};
const TASK_H = 46;

async function calcWin() {
  const {w, h} = CALC;
  let s = win(w, h, 'Calc', false, ['Edit', 'View', 'Help']);
  s += `<rect x="16" y="68" width="${w - 32}" height="36" fill="#fff" stroke="#808080" stroke-width="2"/><text x="${w - 26}" y="94" text-anchor="end" font-size="20" ${FONT}>0.</text>`;
  s += btn(110, 118, 84, 34, 'Back') + btn(204, 118, 84, 34, 'CE') + btn(298, 118, 84, 34, 'C');
  const keys = [['7', '8', '9', '/', 'sqrt'], ['4', '5', '6', '*', '%'], ['1', '2', '3', '-', '1/x'], ['0', '+/-', '.', '+', '=']];
  ['MC', 'MR', 'MS', 'M+'].forEach((m, r) => { s += btn(16, 166 + r * 60, 70, 46, '') + `<text x="51" y="${195 + r * 60}" text-anchor="middle" font-size="15" fill="#c00" ${FONT}>${m}</text>`; });
  keys.forEach((row, r) => row.forEach((k, c) => {
    s += btn(110 + c * 56, 166 + r * 60, 50, 46, '') + `<text x="${135 + c * 56}" y="${195 + r * 60}" text-anchor="middle" font-size="16" fill="${'/*-+='.includes(k) ? '#c00' : '#00c'}" ${FONT}>${k}</text>`;
  }));
  return sharp(svg(w, h, s)).png().toBuffer();
}
async function paintWin() {
  const {w, h} = PAINT;
  let s = win(w, h, 'untitled - Sketch', false, ['File', 'Edit', 'View', 'Image', 'Colors', 'Help']);
  // toolbox
  s += bevel(8, 66, 64, 380, false);
  const tools = ['M8 8h20v20H8z', 'M6 26L26 6', 'M16 4v24M4 16h24', 'M8 24c6-12 10-12 16-16', 'M6 6h20v20', 'M16 16m-10 0a10 10 0 1 0 20 0a10 10 0 1 0-20 0'];
  for (let i = 0; i < 16; i++) {
    const x = 12 + (i % 2) * 28, y = 72 + Math.floor(i / 2) * 32;
    s += btn(x, y, 26, 28, '', i === 7) + `<g transform="translate(${x + 1},${y + 2}) scale(.75)"><path d="${tools[i % tools.length]}" stroke="#000" stroke-width="2.5" fill="none"/></g>`;
  }
  // canvas well
  s += `<rect x="80" y="64" width="${w - 92}" height="${h - 150}" fill="#808080"/>`;
  // palette
  const pal = ['#000', '#808080', '#800000', '#808000', '#008000', '#008080', '#000080', '#800080', '#808040', '#004040', '#0080ff', '#004080', '#8000ff', '#804000',
    '#fff', '#c0c0c0', '#f00', '#ff0', '#0f0', '#0ff', '#00f', '#f0f', '#ffff80', '#00ff80', '#80ffff', '#8080ff', '#ff0080', '#ff8040'];
  s += `<rect x="12" y="${h - 76}" width="44" height="44" fill="#fff" stroke="#808080" stroke-width="2"/><rect x="18" y="${h - 70}" width="22" height="22" fill="#000"/>`;
  pal.forEach((c, i) => { const x = 66 + (i % 14) * 26, y = h - 76 + Math.floor(i / 14) * 24; s += `<rect x="${x}" y="${y}" width="22" height="20" fill="${c}" stroke="#808080" stroke-width="2"/>`; });
  s += `<text x="${66 + 14 * 26 + 16}" y="${h - 50}" font-size="14" ${FONT}>For Help, click Help Topics on the Help Menu.</text>`;
  // photo
  const cw = w - 112, ch = Math.round(cw * 9 / 16);
  const photo = await sharp(still).resize(cw, ch, {fit: 'cover'}).png().toBuffer();
  return sharp(svg(w, h, s)).composite([{input: photo, left: 90, top: 74}]).png().toBuffer();
}
async function pickWin() {
  const {w, h} = PICK;
  let s = win(w, h, 'Change Icon', false);
  s += `<text x="16" y="62" font-size="14" ${FONT}>Select an icon from the list below:</text>`;
  s += `<rect x="16" y="72" width="${w - 32}" height="${h - 140}" fill="#fff" stroke="#808080" stroke-width="2"/>`;
  const kinds = ['folder', 'trash', 'smile', 'star', 'globe', 'heart', 'note', 'cam', 'brush', 'notes', 'dice', 'mail'];
  for (let i = 0; i < 24; i++) {
    const x = 30 + (i % 8) * 58, y = 84 + Math.floor(i / 8) * 76;
    s += `<g transform="translate(${x},${y}) scale(.9)">${iconArt(kinds[(i * 5) % kinds.length])}</g>`;
  }
  s += `<rect x="30" y="84" width="48" height="60" fill="#000080" opacity=".25"/>`;
  s += btn(w - 220, h - 52, 96, 34, 'OK') + btn(w - 114, h - 52, 96, 34, 'Cancel');
  return sharp(svg(w, h, s)).png().toBuffer();
}
const noteWin = (active) => {
  const {w, h} = NOTE;
  let s = win(w, h, 'Untitled - Notes', active, ['File', 'Edit', 'Format', 'View', 'Help']);
  s += `<rect x="10" y="66" width="${w - 20}" height="${h - 76}" fill="#fff" stroke="#808080" stroke-width="2"/>`;
  s += bevel(w - 34, 68, 22, h - 80, false);
  return sharp(svg(w, h, s)).png().toBuffer();
};
const docWin = () => {
  const {w, h} = DOC;
  let s = win(w, h, 'Document - Writer', true, ['File', 'Edit', 'View', 'Insert', 'Format', 'Help']);
  s += `<path d="M8 66H${w - 8}" stroke="#808080"/>`;
  for (let i = 0; i < 12; i++) s += btn(12 + i * 36, 72, 32, 30, '');
  s += `<rect x="12" y="110" width="${w - 24}" height="${h - 152}" fill="#fff" stroke="#808080" stroke-width="2"/>`;
  s += `<rect x="12" y="${h - 36}" width="${w - 24}" height="26" fill="#c0c0c0" stroke="#808080"/><text x="20" y="${h - 17}" font-size="14" ${FONT}>For Help, press F1</text>`;
  return sharp(svg(w, h, s)).png().toBuffer();
};

// ---------- taskbar ----------
function taskbar(buttons, activeIdx) {
  const y = H - TASK_H;
  let s = `<rect x="0" y="${y}" width="${W}" height="${TASK_H}" fill="#c0c0c0"/><path d="M0 ${y + 1}H${W}" stroke="#fff" stroke-width="2"/>`;
  s += btn(4, y + 6, 104, 36, '') + `<g transform="translate(14,${y + 12}) scale(.48)">${iconArt('smile')}</g><text x="44" y="${y + 30}" font-size="17" font-weight="bold" ${FONT}>Start</text>`;
  buttons.forEach((b, i) => {
    const x = 120 + i * 230;
    s += btn(x, y + 6, 222, 36, '', i === activeIdx) + `<text x="${x + 12}" y="${y + 30}" font-size="15" ${FONT} ${i === activeIdx ? 'font-weight="bold"' : ''}>${esc(b)}</text>`;
  });
  s += bevel(W - 140, y + 6, 134, 36, true) + `<text x="${W - 73}" y="${y + 30}" text-anchor="middle" font-size="15" ${FONT}>5:58 PM</text>`;
  return s;
}
const taskBtnRect = i => ({x: 120 + i * 230, y: H - TASK_H + 6, w: 222, h: 36});

// ---------- cursor ----------
const cursorSvg = `<path d="M2 2 L2 34 L10 26 L16 40 L22 37 L16 24 L27 24 Z" fill="#fff" stroke="#000" stroke-width="2" stroke-linejoin="round"/>`;

// ---------- timeline ----------
const T = {calc: 0.15, paint: 0.4, pick: 0.65, note: 0.9, docBtn: 3.9, click: 4.7, zoom0: 4.75, zoom1: 5.25, typeStart: 1.7, typeEnd: 3.6};
const docBtnIdx = 4;
const dbr = taskBtnRect(docBtnIdx);
const path = [ // [time, x, y]
  [0, 1500, 300], [0.9, 1300, 420], [1.4, NOTE.x + 60, NOTE.y + 100], [3.5, NOTE.x + 300, NOTE.y + 180],
  [4.0, dbr.x + 140, dbr.y + 80], [4.55, dbr.x + 100, dbr.y + 18], [4.9, dbr.x + 100, dbr.y + 18],
  [5.6, 700, 800], [8, 720, 790],
];
function cursorAt(t) {
  for (let i = 0; i < path.length - 1; i++) {
    const [t0, x0, y0] = path[i], [t1, x1, y1] = path[i + 1];
    if (t <= t1) { const k = ease((t - t0) / (t1 - t0)); return [lerp(x0, x1, k), lerp(y0, y1, k)]; }
  }
  return path.at(-1).slice(1);
}

// ---------- render ----------
const bg = await desktop();
const [calcB, paintB, pickB, noteI, noteA, docB] = await Promise.all([calcWin(), paintWin(), pickWin(), noteWin(false), noteWin(true), docWin()]);
const shadow = (r) => ({input: svg(r.w, r.h, `<rect width="${r.w}" height="${r.h}" fill="#000" opacity=".35"/>`), left: r.x + 6, top: r.y + 6});

async function frame(t) {
  const L = [];
  const add = (start, r, buf) => { if (t >= start) L.push(shadow(r), {input: buf, left: r.x, top: r.y}); };
  add(T.calc, CALC, calcB); add(T.paint, PAINT, paintB); add(T.pick, PICK, pickB);
  const noteActive = t >= T.note && t < T.click;
  add(T.note, NOTE, noteActive ? noteA : noteI);
  if (t >= T.note) {
    const n = Math.round(TEXT.length * Math.max(0, Math.min(1, (t - T.typeStart) / (T.typeEnd - T.typeStart))));
    const typed = TEXT.slice(0, n);
    const caret = noteActive && Math.floor(t * 2.5) % 2 === 0;
    const tw = typed.length * 10.2;
    L.push({input: svg(NOTE.w, NOTE.h, `<text x="20" y="96" font-size="18" font-family="Courier New, monospace">${esc(typed)}</text>${caret ? `<rect x="${21 + tw}" y="80" width="2" height="21" fill="#000"/>` : ''}`), left: NOTE.x, top: NOTE.y});
  }
  // zoom animation + doc window
  let tb = '';
  if (t >= T.zoom0 && t < T.zoom1) {
    for (const lag of [0, 0.08, 0.16]) {
      const k = ease((t - T.zoom0 - lag) / (T.zoom1 - T.zoom0 - 0.16));
      if (t - T.zoom0 < lag) continue;
      const x = lerp(dbr.x, DOC.x, k), y = lerp(dbr.y, DOC.y, k), w = lerp(dbr.w, DOC.w, k), h = lerp(dbr.h, DOC.h, k);
      tb += `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="none" stroke="#000080" stroke-width="3" stroke-dasharray="6 4"/>`;
    }
  }
  if (t >= T.zoom1) {
    L.push({input: svg(DOC.w, DOC.h, `<rect width="${DOC.w}" height="${DOC.h}" fill="#000" opacity=".35"/>`), left: DOC.x + 6, top: DOC.y + 6});
    L.push({input: docB, left: DOC.x, top: DOC.y});
    if (Math.floor(t * 2.5) % 2 === 0) L.push({input: svg(4, 24, `<rect width="2" height="24" fill="#000"/>`), left: DOC.x + 30, top: DOC.y + 128});
  }
  const buttons = [];
  if (t >= T.calc) buttons.push('Calc');
  if (t >= T.paint) buttons.push('untitled - Sketch');
  if (t >= T.pick) buttons.push('Change Icon');
  if (t >= T.note) buttons.push('Untitled - Notes');
  if (t >= T.docBtn) buttons.push('Document - Writer');
  let active = noteActive ? 3 : -1;
  if (t >= T.click - 0.1) active = docBtnIdx;
  tb += taskbar(buttons, active);
  L.push({input: svg(W, H, tb), left: 0, top: 0});
  const [cx, cy] = cursorAt(t);
  L.push({input: svg(30, 44, cursorSvg), left: Math.round(cx), top: Math.round(cy)});
  return sharp(bg).composite(L).removeAlpha().raw().toBuffer();
}

const out = join(outDir, 'bumper.mp4');
const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-framerate', String(FPS), '-i', 'pipe:0',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], {stdio: ['pipe', 'inherit', 'inherit']});
for (let i = 0; i < N; i++) {
  const buf = await frame(i / FPS);
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
writeFileSync(join(outDir, 'timeline.json'), JSON.stringify({W, H, FPS, DUR, TEXT, T}, null, 2));
console.log(out);
