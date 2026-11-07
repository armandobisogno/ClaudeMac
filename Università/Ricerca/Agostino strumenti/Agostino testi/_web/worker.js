/* Scrinium Augustini — motore di ricerca (Web Worker).
   Tiene in memoria i testi, esegue le interrogazioni, calcola concordanze,
   distribuzioni, forme e collocazioni. Parla con la pagina via postMessage. */
'use strict';

const CORPORA = ['O', 'S', 'E'];
const S = {
  catalog: null, built: '', docs: [], byId: new Map(), K: {},
  pending: new Map(), slots: {}, freq: new Map(),
};

// ---------- cache (IndexedDB) ----------
let dbp = null;
function idb() {
  if (dbp) return dbp;
  dbp = new Promise((res) => {
    try {
      const r = indexedDB.open('scrinium', 1);
      r.onupgradeneeded = () => r.result.createObjectStore('files');
      r.onsuccess = () => res(r.result);
      r.onerror = () => res(null);
    } catch (e) { res(null); }
  });
  return dbp;
}
async function cacheGet(key) {
  const db = await idb(); if (!db) return null;
  return new Promise((res) => {
    try {
      const q = db.transaction('files').objectStore('files').get(key);
      q.onsuccess = () => res(q.result || null); q.onerror = () => res(null);
    } catch (e) { res(null); }
  });
}
async function cachePut(key, val) {
  const db = await idb(); if (!db) return;
  try { db.transaction('files', 'readwrite').objectStore('files').put(val, key); } catch (e) {}
}
async function cachePrune(prefix) {
  const db = await idb(); if (!db) return;
  try {
    const st = db.transaction('files', 'readwrite').objectStore('files');
    const q = st.getAllKeys();
    q.onsuccess = () => q.result.forEach((k) => { if (!String(k).startsWith(prefix)) st.delete(k); });
  } catch (e) {}
}

// ---------- caricamento ----------
async function fetchBytes(name, label) {
  const key = S.built + ':' + name;
  const hit = await cacheGet(key);
  if (hit) return hit;
  const r = await fetch('data/' + name);
  if (!r.ok) throw new Error('Impossibile scaricare ' + name + ' (' + r.status + ')');
  const total = +r.headers.get('content-length') || 0;
  const reader = r.body.getReader();
  const chunks = []; let got = 0, lastTick = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value); got += value.length;
    const now = Date.now();
    if (now - lastTick > 150) { lastTick = now; post({ t: 'progress', label, got, total }); }
  }
  let buf = new Uint8Array(got); let o = 0;
  for (const c of chunks) { buf.set(c, o); o += c.length; }
  if (name.endsWith('.txt')) {
    // pacchetti gzip codificati in base64 (gli artifact non servono .gz)
    const bin = atob(new TextDecoder().decode(buf).replace(/\s+/g, ''));
    buf = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
  }
  cachePut(key, buf.buffer);
  return buf.buffer;
}
async function gunzipJSON(buf) {
  const u = new Uint8Array(buf);
  let text;
  if (u[0] === 0x1f && u[1] === 0x8b) {
    const ds = new Blob([u]).stream().pipeThrough(new DecompressionStream('gzip'));
    text = await new Response(ds).text();
  } else {
    text = new TextDecoder().decode(u);
  }
  return JSON.parse(text);
}
const LABELS = { O: 'Opere', S: 'Sermoni', E: 'Lettere', la: 'latino', it: 'italiano', notes: 'note', refs: 'indici' };
function ensure(k, part) {
  const key = k + '-' + part;
  const K = S.K[k];
  if (K[part]) return Promise.resolve(K[part]);
  if (S.pending.has(key)) return S.pending.get(key);
  const p = (async () => {
    const label = LABELS[k] + ' · ' + LABELS[part];
    post({ t: 'progress', label, got: 0, total: 0 });
    const data = await gunzipJSON(await fetchBytes(key + '.gz.txt', label));
    K[part] = data;
    if (part === 'la' || part === 'it') buildLayer(k, part);
    if (part === 'notes') buildNotes(k);
    post({ t: 'loaded', key });
    return data;
  })();
  S.pending.set(key, p);
  p.catch(() => S.pending.delete(key));
  return p;
}

function buildLayer(k, lang) {
  const K = S.K[k];
  const parts = [];
  const starts = new Int32Array(K.total + 1);
  let g = 0, off = 0;
  for (const doc of K[lang]) {
    for (const t of doc) { starts[g++] = off; parts.push(t); off += t.length + 1; }
  }
  starts[g] = off;
  K.layers[lang] = { str: parts.join('\n'), starts };
}
function buildNotes(k) {
  const K = S.K[k];
  const parts = [], starts = [], ng = [], nn = [];
  let off = 0;
  K.notes.forEach((list, di) => {
    for (const [pi, n, t] of list) {
      starts.push(off); parts.push(t); off += t.length + 1;
      ng.push(K.base[di] + Math.max(0, pi)); nn.push(n);
    }
  });
  starts.push(off);
  K.layers.nt = { str: parts.join('\n'), starts: Int32Array.from(starts), ng: Int32Array.from(ng), nn: Int32Array.from(nn) };
}

async function init() {
  const r = await fetch('data/catalog.json');
  S.catalog = await r.json();
  S.built = S.catalog.built;
  cachePrune(S.built + ':');
  S.docs = S.catalog.docs;
  for (const k of CORPORA) S.K[k] = { docs: [], layers: {} };
  S.docs.forEach((d, idx) => { d.x = idx; S.byId.set(d.id, d); S.K[d.c].docs[d.i] = d; });
  for (const k of CORPORA) {
    const K = S.K[k];
    K.base = new Int32Array(K.docs.length + 1);
    let t = 0;
    K.docs.forEach((d, i) => { K.base[i] = t; t += d.np; });
    K.base[K.docs.length] = t; K.total = t;
    K.gDoc = new Int32Array(t); K.gPar = new Int32Array(t);
    K.docs.forEach((d, i) => { for (let p = 0; p < d.np; p++) { K.gDoc[K.base[i] + p] = i; K.gPar[K.base[i] + p] = p; } });
  }
  return S.catalog;
}

// ---------- citazioni ----------
function refOf(k, g) { const K = S.K[k]; return K.refs ? K.refs[K.gDoc[g]][0][K.gPar[g]] : ''; }
function citeOf(d, ref) {
  const r = String(ref).split('.').filter((x) => x !== '').join(', ');
  return d.s + (r ? (d.c === 'O' ? ' ' : ', ') + r : '');
}
function ymid(d) { return d.y0 == null ? null : (d.y0 + d.y1) / 2; }

// ---------- linguaggio di interrogazione ----------
const L = '\\p{L}\\p{M}';
const GAP = '(?:\\[n\\d+\\]|[^' + L + '\\n])+';
const WORD = '[' + L + ']+';
function esc(c) { return c.replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&'); }

function charClass(c, lang, flex) {
  const lc = c.toLowerCase();
  if (!flex) return esc(c);
  if (lang === 'la') {
    if (lc === 'a') return '[aàáâä]';
    if (lc === 'e') return '[eèéêë]';
    if (lc === 'i' || lc === 'j') return '[iìíîïj]';
    if (lc === 'o') return '[oòóôö]';
    if (lc === 'u' || lc === 'v') return '[uùúûüv]';
    if (lc === 'y') return '[yi]';
    return esc(c);
  }
  if (lc === 'a') return '[aàáâ]';
  if (lc === 'e') return '[eèéê]';
  if (lc === 'i') return '[iìíî]';
  if (lc === 'o') return '[oòóô]';
  if (lc === 'u') return '[uùúû]';
  if (c === "'" || c === '’') return "['’]";
  return esc(c);
}
function termSrc(word, lang, o) {
  let w = word;
  const aeFlex = o.flex && lang === 'la';
  if (aeFlex) w = w.replace(/æ|œ/gi, 'e').replace(/ae|oe/gi, 'e');
  let s = '';
  for (const ch of w) {
    if (ch === '*') s += '[' + L + ']*';
    else if (ch === '?') s += '[' + L + ']';
    else if (aeFlex && (ch === 'e' || ch === 'E')) s += '(?:ae|oe|æ|œ|[eèéêë])';
    else s += charClass(ch, lang, o.flex);
  }
  return '(?<![' + L + '])' + s + '(?![' + L + '])';
}
function phraseSrc(words, slop, lang, o) {
  const gap = slop > 0 ? '(?:' + GAP + WORD + '){0,' + slop + '}' + GAP : GAP;
  return words.map((w) => termSrc(w, lang, o)).join(gap);
}

function tokenize(q) {
  const toks = []; let i = 0;
  while (i < q.length) {
    const c = q[i];
    if (/\s/.test(c)) { i++; continue; }
    if (c === '(' || c === ')') { toks.push({ t: c }); i++; continue; }
    if (c === '|') { toks.push({ t: 'OR' }); i++; continue; }
    if (c === '-' && (i === 0 || /[\s(]/.test(q[i - 1]))) { toks.push({ t: 'NOT' }); i++; continue; }
    let layer = null;
    const lm = /^(la|lat|it|ita|nota|note|nt):/i.exec(q.slice(i));
    if (lm) {
      const x = lm[1].toLowerCase();
      layer = x.startsWith('la') ? 'la' : x.startsWith('it') ? 'it' : 'nt';
      i += lm[0].length;
    }
    if (q[i] === '"') {
      const j = q.indexOf('"', i + 1);
      if (j < 0) throw new Error('Virgolette non chiuse.');
      const words = q.slice(i + 1, j).trim().split(/\s+/).filter(Boolean);
      i = j + 1;
      let slop = 0;
      const sm = /^~(\d+)/.exec(q.slice(i));
      if (sm) { slop = +sm[1]; i += sm[0].length; }
      if (!words.length) throw new Error('Frase vuota.');
      toks.push({ t: 'ATOM', kind: 'phrase', words, slop, layer });
      continue;
    }
    if (q[i] === '/') {
      let j = i + 1;
      while (j < q.length && !(q[j] === '/' && q[j - 1] !== '\\')) j++;
      if (j >= q.length) throw new Error('Espressione regolare non chiusa: manca la / finale.');
      toks.push({ t: 'ATOM', kind: 'regex', src: q.slice(i + 1, j), layer });
      i = j + 1; continue;
    }
    let j = i;
    while (j < q.length && !/[\s()|"]/.test(q[j])) j++;
    const w = q.slice(i, j); i = j;
    if (!w) continue;
    const up = w === w.toUpperCase() ? w : '';
    if (!layer && (up === 'OR' || up === 'O')) { toks.push({ t: 'OR' }); continue; }
    if (!layer && (up === 'AND' || up === 'E')) { toks.push({ t: 'AND' }); continue; }
    if (!layer && (up === 'NOT' || up === 'NON')) { toks.push({ t: 'NOT' }); continue; }
    const nm = /^(NEAR|VICINO|PRIMA|BEFORE)\/(\d+)$/.exec(up);
    if (!layer && nm) { toks.push({ t: 'NEAR', n: +nm[2], ordered: nm[1] === 'PRIMA' || nm[1] === 'BEFORE' }); continue; }
    toks.push({ t: 'ATOM', kind: 'term', words: [w], layer });
  }
  return toks;
}
function parse(q) {
  const toks = tokenize(q); let p = 0;
  const peek = () => toks[p];
  function orE() {
    const kids = [andE()];
    while (peek() && peek().t === 'OR') { p++; kids.push(andE()); }
    return kids.length > 1 ? { op: 'or', kids } : kids[0];
  }
  function andE() {
    const kids = [];
    for (;;) {
      const t = peek();
      if (!t || t.t === 'OR' || t.t === ')') break;
      if (t.t === 'AND') { p++; continue; }
      kids.push(unary());
    }
    if (!kids.length) throw new Error('Manca un termine da cercare.');
    return kids.length > 1 ? { op: 'and', kids } : kids[0];
  }
  function unary() {
    if (peek() && peek().t === 'NOT') { p++; return { op: 'not', kid: unary() }; }
    return near();
  }
  function near() {
    let a = prim();
    while (peek() && peek().t === 'NEAR') {
      const nt = toks[p++];
      const b = prim();
      const A = toAtom(a), B = toAtom(b);
      a = { op: 'atom', a: { kind: 'near', left: A, right: B, n: nt.n, ordered: nt.ordered, layer: A.layer || B.layer } };
    }
    return a;
  }
  function prim() {
    const t = toks[p++];
    if (!t) throw new Error('Interrogazione incompleta.');
    if (t.t === '(') {
      const e = orE();
      if (!peek() || peek().t !== ')') throw new Error('Parentesi non chiusa.');
      p++; return e;
    }
    if (t.t === 'ATOM') return { op: 'atom', a: t };
    throw new Error('Operatore fuori posto: ' + (t.t === 'NEAR' ? 'NEAR' : t.t));
  }
  const e = orE();
  if (p < toks.length) throw new Error('Parentesi chiusa in più.');
  return e;
}
// un gruppo di sole alternative (a | b | "c d") può fare da operando di NEAR
function toAtom(node) {
  if (node.op === 'atom') return node.a;
  if (node.op === 'or') {
    const items = node.kids.map(toAtom);
    const layers = new Set(items.map((x) => x.layer || ''));
    if (layers.size > 1) throw new Error('Dentro un gruppo usato con NEAR i termini devono stare nella stessa lingua.');
    return { kind: 'alt', items, layer: items[0].layer };
  }
  throw new Error('NEAR/PRIMA collega termini, frasi o gruppi di alternative (a | b), non gruppi con AND o esclusioni.');
}
function atomSrc(a, lang, o) {
  if (a.kind === 'alt') return '(?:' + a.items.map((x) => atomSrc(x, lang, o)).join('|') + ')';
  if (a.kind === 'term') return termSrc(a.words[0], lang, o);
  if (a.kind === 'phrase') return phraseSrc(a.words, a.slop, lang, o);
  if (a.kind === 'regex') return '(?:' + a.src + ')';
  if (a.kind === 'near') {
    const A = atomSrc(a.left, lang, o), B = atomSrc(a.right, lang, o);
    const gap = '(?:' + GAP + WORD + '){0,' + a.n + '}' + GAP;
    return a.ordered ? A + gap + B : '(?:' + A + gap + B + '|' + B + gap + A + ')';
  }
}
function compileAtom(a, o) {
  const layer = a.layer || o.scope;
  const langs = layer === 'both' ? ['la', 'it'] : [layer];
  const res = {};
  for (const lang of langs) {
    try { res[lang] = new RegExp(atomSrc(a, lang, o), 'gu' + (o.cs ? '' : 'i')); }
    catch (e) { throw new Error('Espressione non valida: ' + e.message); }
  }
  return res;
}
function collectLayers(node, o, set = new Set()) {
  if (node.op === 'atom') { const l = node.a.layer || o.scope; (l === 'both' ? ['la', 'it'] : [l]).forEach((x) => set.add(x)); }
  else if (node.kids) node.kids.forEach((k) => collectLayers(k, o, set));
  else if (node.kid) collectLayers(node.kid, o, set);
  return set;
}

// ---------- valutazione ----------
const MAX_MATCH = 300000;
function scanAtom(res, k, allowed, stat) {
  const K = S.K[k];
  const out = new Map();
  for (const lang in res) {
    const Ly = K.layers[lang]; if (!Ly) continue;
    const re = res[lang]; re.lastIndex = 0;
    const st = Ly.starts; let g = 0, m;
    const isNt = lang === 'nt';
    const n = isNt ? Ly.ng.length : K.total;
    while ((m = re.exec(Ly.str))) {
      if (!m[0].length) { re.lastIndex++; continue; }
      if (++stat.n > MAX_MATCH) { stat.capped = true; break; }
      while (g < n && st[g + 1] <= m.index) g++;
      const gg = isNt ? Ly.ng[g] : g;
      if (!allowed[K.gDoc[gg]]) continue;
      let h = out.get(gg);
      if (!h) { h = {}; out.set(gg, h); }
      const rel = m.index - st[g];
      (h[lang] || (h[lang] = [])).push(isNt ? [rel, rel + m[0].length, g] : [rel, rel + m[0].length]);
    }
  }
  return out;
}
function mergeHits(a, b) {
  for (const l in b) a[l] = (a[l] || []).concat(b[l]);
  return a;
}
function evalNode(node, k, o, allowed, stat) {
  if (node.op === 'atom') return { pos: scanAtom(compileAtom(node.a, o), k, allowed, stat) };
  if (node.op === 'not') {
    const r = evalNode(node.kid, k, o, allowed, stat);
    if (r.neg) throw new Error('Doppia negazione non ammessa.');
    return { neg: new Set(r.pos.keys()) };
  }
  if (node.op === 'or') {
    const pos = new Map();
    for (const kid of node.kids) {
      const r = evalNode(kid, k, o, allowed, stat);
      if (r.neg) throw new Error('Una negazione (-) non può stare da sola in un OR.');
      for (const [g, h] of r.pos) { const e = pos.get(g); if (e) mergeHits(e, h); else pos.set(g, { ...h }); }
    }
    return { pos };
  }
  if (node.op === 'and') {
    let pos = null; const negs = [];
    for (const kid of node.kids) {
      const r = evalNode(kid, k, o, allowed, stat);
      if (r.neg) { negs.push(r.neg); continue; }
      if (!pos) { pos = new Map(); for (const [g, h] of r.pos) pos.set(g, { ...h }); continue; }
      const nx = new Map();
      for (const [g, h] of pos) { const h2 = r.pos.get(g); if (h2) nx.set(g, mergeHits(h, h2)); }
      pos = nx;
    }
    if (!pos) throw new Error('Serve almeno un termine positivo oltre alle esclusioni.');
    for (const ng of negs) for (const g of ng) pos.delete(g);
    return { pos };
  }
}

function allowedDocs(k, f) {
  const K = S.K[k];
  const a = new Uint8Array(K.docs.length);
  const ids = f.docs && f.docs.length ? new Set(f.docs) : null;
  K.docs.forEach((d, i) => {
    if (ids && !ids.has(d.id)) return;
    if (!ids) {
      if (d.y0 == null) { if (!f.undated) return; }
      else if (d.y1 < f.y0 || d.y0 > f.y1) return;
      if (f.tag && d.c === 'O' && !(d.tag || '').includes(f.tag)) return;
      if (f.tag && d.c !== 'O') return;
      if (f.augOnly && d.c === 'E' && !d.aug) return;
    }
    a[i] = 1;
  });
  return a;
}

async function search(req) {
  const t0 = performance.now();
  const o = { scope: req.scope, flex: req.flex, cs: req.cs };
  const tree = parse(req.q);
  const layers = collectLayers(tree, o);
  const corpora = req.corpora.filter((k) => CORPORA.includes(k));
  if (!corpora.length) throw new Error('Scegli almeno un corpus (Opere, Sermoni, Lettere).');
  const loads = [];
  for (const k of corpora) {
    loads.push(ensure(k, 'refs'));
    for (const l of layers) loads.push(ensure(k, l === 'nt' ? 'notes' : l));
  }
  await Promise.all(loads);
  const stat = { n: 0, capped: false };
  const hits = [];
  for (const k of corpora) {
    const allowed = allowedDocs(k, req.filters);
    const r = evalNode(tree, k, o, allowed, stat);
    if (r.neg) throw new Error('Serve almeno un termine positivo oltre alle esclusioni.');
    for (const [g, h] of r.pos) hits.push({ k, g, h });
  }
  let occ = 0;
  for (const x of hits) { let c = 0; for (const l in x.h) c += x.h[l].length; x.c = c; occ += c; }
  const primary = req.scope === 'it' ? 'it' : req.scope === 'nt' ? 'nt' : 'la';
  const slot = req.slot || 'ui';
  S.slots[slot] = { req, hits, primary, layers: [...layers] };
  sortHits(req.sort || 'chrono', slot);
  // distribuzione per documento
  const perDoc = {};
  for (const x of hits) {
    const d = S.K[x.k].docs[S.K[x.k].gDoc[x.g]];
    const e = perDoc[d.id] || (perDoc[d.id] = [0, 0, {}]);
    e[0]++; e[1] += x.c;
    for (const l in x.h) e[2][l] = (e[2][l] || 0) + x.h[l].length;
  }
  return {
    paras: hits.length, occ, perDoc, capped: stat.capped, layers: [...layers],
    ms: Math.round(performance.now() - t0),
  };
}
function sortHits(mode, slot) {
  const L = S.slots[slot || 'ui']; if (!L) return;
  const key = (x) => { const d = S.K[x.k].docs[S.K[x.k].gDoc[x.g]]; return d; };
  const co = { O: 0, S: 1, E: 2 };
  L.hits.sort((a, b) => {
    if (mode === 'dense') return b.c - a.c || a.g - b.g;
    const da = key(a), db = key(b);
    if (mode === 'chrono') {
      const ya = ymid(da) ?? 9999, yb = ymid(db) ?? 9999;
      if (ya !== yb) return ya - yb;
    }
    return co[a.k] - co[b.k] || a.g - b.g;
  });
  L.sort = mode;
}

function paraOut(k, g, h) {
  const K = S.K[k];
  const di = K.gDoc[g], pi = K.gPar[g];
  const d = K.docs[di];
  const ref = K.refs ? K.refs[di][0][pi] : '';
  const o = {
    id: d.id, k, g, pi, ref, cite: citeOf(d, ref),
    la: K.la ? K.la[di][pi] : null, it: K.it ? K.it[di][pi] : null,
    hl: { la: h && h.la ? h.la.map((x) => [x[0], x[1]]) : [], it: h && h.it ? h.it.map((x) => [x[0], x[1]]) : [] },
  };
  if (h && h.nt) {
    const Ly = K.layers.nt; const byNote = new Map();
    for (const [s, e, ni] of h.nt) {
      if (!byNote.has(ni)) byNote.set(ni, { n: Ly.nn[ni], text: Ly.str.slice(Ly.starts[ni], Ly.starts[ni + 1] - 1), hl: [] });
      byNote.get(ni).hl.push([s, e]);
    }
    o.notes = [...byNote.values()];
  }
  if (K.notes) o.pn = K.notes[di].filter((n) => n[0] === pi).map((n) => [n[1], n[2]]);
  return o;
}
async function page(start, count, slot) {
  const L = S.slots[slot || 'ui']; if (!L) return { items: [] };
  const sl = L.hits.slice(start, start + count);
  await Promise.all([...new Set(sl.map((x) => x.k))].flatMap((k) => ['la', 'it', 'notes'].map((p) => ensure(k, p))));
  return { items: L.hits.slice(start, start + count).map((x) => paraOut(x.k, x.g, x.h)), total: L.hits.length };
}

// ---------- concordanza (KWIC) ----------
function kwic(req) {
  const L = S.slots[req.slot || 'ui']; if (!L) return { rows: [] };
  const lang = req.lang || L.primary;
  const W = req.width || 70, max = req.max || 5000;
  const rows = []; let total = 0;
  for (const x of L.hits) {
    const arr = x.h[lang]; if (!arr) continue;
    const K = S.K[x.k];
    const di = K.gDoc[x.g], pi = K.gPar[x.g];
    let text;
    if (lang === 'nt') text = null; else text = K[lang][di][pi];
    const d = K.docs[di];
    for (const hit of arr) {
      total++;
      if (rows.length >= max) continue;
      let t = text;
      if (lang === 'nt') { const Ly = K.layers.nt; t = Ly.str.slice(Ly.starts[hit[2]], Ly.starts[hit[2] + 1] - 1); }
      const s = hit[0], e = hit[1];
      rows.push({
        id: d.id, g: x.g, k: x.k, pi, ref: K.refs[di][0][pi], cite: citeOf(d, K.refs[di][0][pi]),
        l: t.slice(Math.max(0, s - W), s).replace(/\s+/g, ' '), m: t.slice(s, e), r: t.slice(e, e + W).replace(/\s+/g, ' '),
      });
    }
  }
  return { rows, total, lang };
}

// ---------- forme trovate ----------
function forms(req) {
  const L = S.slots[req.slot || 'ui']; if (!L) return {};
  const out = {};
  for (const x of L.hits) for (const lang in x.h) {
    const K = S.K[x.k];
    const di = K.gDoc[x.g], pi = K.gPar[x.g];
    const m = out[lang] || (out[lang] = new Map());
    for (const hit of x.h[lang]) {
      let t;
      if (lang === 'nt') { const Ly = K.layers.nt; t = Ly.str.slice(Ly.starts[hit[2]] + hit[0], Ly.starts[hit[2]] + hit[1]); }
      else t = K[lang][di][pi].slice(hit[0], hit[1]);
      t = t.replace(/\[n\d+\]/g, '').replace(/\s+/g, ' ').toLowerCase();
      m.set(t, (m.get(t) || 0) + 1);
    }
  }
  const res = {};
  for (const l in out) res[l] = [...out[l]].sort((a, b) => b[1] - a[1]).slice(0, 400);
  return res;
}

// ---------- lessico e collocazioni ----------
const WRE = /[\p{L}\p{M}]+/gu;
function freqFor(lang, corpora) {
  const key = lang + ':' + corpora.join('');
  if (S.freq.has(key)) return S.freq.get(key);
  const f = new Map(); let N = 0;
  for (const k of corpora) {
    const Ly = S.K[k].layers[lang]; if (!Ly) continue;
    const str = lang === 'it' ? Ly.str.replace(/\[n\d+\]/g, ' ') : Ly.str;
    for (const m of str.matchAll(WRE)) { const w = m[0].toLowerCase(); f.set(w, (f.get(w) || 0) + 1); N++; }
  }
  const r = { f, N };
  S.freq.set(key, r);
  return r;
}
async function lexicon(req) {
  const lang = req.lang, corpora = req.corpora;
  await Promise.all(corpora.map((k) => ensure(k, lang)));
  const per = {};
  for (const k of corpora) per[k] = freqFor(lang, [k]).f;
  let re;
  const p = (req.pattern || '').trim();
  if (!p) throw new Error('Scrivi l’inizio di una parola, o un modello con * e ?.');
  if (p.startsWith('/') && p.endsWith('/') && p.length > 2) re = new RegExp('^(?:' + p.slice(1, -1) + ')$', 'iu');
  else {
    const o = { flex: req.flex };
    let body = termSrc(p.includes('*') || p.includes('?') ? p : p + '*', lang, o);
    body = body.replace(/^\(\?<!\[[^\]]+\]\)/, '').replace(/\(\?!\[[^\]]+\]\)$/, '');
    re = new RegExp('^' + body + '$', 'iu');
  }
  const all = new Map();
  for (const k of corpora) for (const [w, c] of per[k]) {
    if (!re.test(w)) continue;
    const e = all.get(w) || { w, n: 0, by: {} };
    e.n += c; e.by[k] = c; all.set(w, e);
  }
  const list = [...all.values()].sort((a, b) => b.n - a.n);
  return { forms: list.slice(0, 1500), total: list.length, tokens: list.reduce((s, x) => s + x.n, 0) };
}

const STOP = {
  la: 'a ab ac ad an ante apud at atque aut autem cum de dum e ego eius enim ea eam eas eis eo eos eorum erat ergo es esse esset est et etiam ex fuit haec hic hoc huius iam id igitur illa ille illud in inter ipsa ipse ipsum is ita me mihi nam ne nec neque nisi non nos nobis nunc o per post pro propter quae quam quando quia quibus quid quidem quis quo quod quoniam quos qui se sed si sibi sic sine sit sub sunt super tamen te tibi tu tunc uel ubi uero ut uos vel vero vos quem cuius hanc hunc his illi illis nihil ipso omnia omnibus quasi sicut tam',
  it: 'a ad al alla alle ai agli all anche anzi c che chi ci ciò coi col come con cosa così cui d da dai dal dall dalla dalle degli dei del dell della delle di dove e è ed egli era essa essere esso fra gli già ha hanno i il in io l la le lei li lo loro lui ma me mi ne né nei nel nell nella nelle noi non o per perché però più poi quale quali quando quel quella quelle quelli quello questa queste questi questo se si sia siamo sono su sua sue sul sull sulla suo suoi te ti tra tu tutti tutto un una uno voi quindi cioè dunque nostro nostra loro essi sé stesso fu può',
};
const STOPS = { la: new Set(STOP.la.split(' ')), it: new Set(STOP.it.split(' ')) };
function collocates(req) {
  const L = S.slots[req.slot || 'ui']; if (!L) return { rows: [] };
  const lang = req.lang || (L.primary === 'nt' ? 'la' : L.primary);
  const win = req.win || 5;
  const corpora = [...new Set(L.hits.map((x) => x.k))];
  if (!corpora.every((k) => S.K[k].layers[lang])) return { rows: [], missing: true, lang };
  const { f, N } = freqFor(lang, corpora);
  const co = new Map(); let nodes = 0;
  for (const x of L.hits) {
    const arr = x.h[lang]; if (!arr) continue;
    const K = S.K[x.k];
    const text = K[lang][K.gDoc[x.g]][K.gPar[x.g]];
    const toks = [...text.replace(/\[n\d+\]/g, (m) => ' '.repeat(m.length)).matchAll(WRE)].map((m) => [m.index, m.index + m[0].length, m[0].toLowerCase()]);
    for (const [s, e] of arr) {
      nodes++;
      let first = toks.findIndex((t) => t[1] > s);
      if (first < 0) continue;
      let last = first; while (last + 1 < toks.length && toks[last + 1][0] < e) last++;
      const seen = new Set();
      for (let i = Math.max(0, first - win); i <= Math.min(toks.length - 1, last + win); i++) {
        if (i >= first && i <= last) continue;
        if (arr.some(([hs, he]) => toks[i][0] < he && toks[i][1] > hs)) continue;
        const w = toks[i][2];
        if (req.stop && STOPS[lang] && STOPS[lang].has(w)) continue;
        if (w.length < 2 || seen.has(w)) continue;
        seen.add(w);
        co.set(w, (co.get(w) || 0) + 1);
      }
    }
  }
  const rows = [];
  for (const [w, c] of co) {
    if (c < (req.min || 2)) continue;
    const fw = f.get(w) || c;
    const dice = 14 + Math.log2((2 * c) / (nodes + fw));
    rows.push({ w, c, f: fw, dice: Math.round(dice * 100) / 100 });
  }
  rows.sort(req.by === 'count' ? (a, b) => b.c - a.c : (a, b) => b.dice - a.dice || b.c - a.c);
  return { rows: rows.slice(0, 200), nodes, N, lang };
}

// ---------- lettura ----------
async function getDoc(id) {
  const d = S.byId.get(id); if (!d) throw new Error('Documento non trovato: ' + id);
  await Promise.all(['refs', 'la', 'it', 'notes'].map((p) => ensure(d.c, p)));
  const K = S.K[d.c];
  return { id, refs: K.refs[d.i][0], heads: K.refs[d.i][1], la: K.la[d.i], it: K.it[d.i], notes: K.notes[d.i] };
}
async function findRef(id, ref) {
  const d = S.byId.get(id); if (!d) throw new Error('Documento non trovato: ' + id);
  await ensure(d.c, 'refs');
  const refs = S.K[d.c].refs[d.i][0];
  let pi = refs.indexOf(ref);
  if (pi < 0) pi = refs.findIndex((r) => r.startsWith(ref + '.') || ref.startsWith(r + '.'));
  return pi;
}
async function passage(id, ref, ctx) {
  const d = S.byId.get(id); if (!d) throw new Error('Documento non trovato: ' + id);
  await Promise.all(['refs', 'la', 'it'].map((p) => ensure(d.c, p)));
  const pi = await findRef(id, ref);
  if (pi < 0) throw new Error('Riferimento ' + ref + ' non trovato in ' + d.s);
  const K = S.K[d.c];
  const out = [];
  for (let p = Math.max(0, pi - ctx); p <= Math.min(d.np - 1, pi + ctx); p++) {
    const r = K.refs[d.i][0][p];
    out.push({ id: d.id + ':' + r, cite: citeOf(d, r), la: K.la[d.i][p].slice(0, 4000), it: K.it[d.i][p].replace(/\[n\d+\]/g, '').slice(0, 4000) });
  }
  return { opera: d.t, data: d.d, passi: out };
}

// ---------- RPC ----------
function post(m, tr) { self.postMessage(m, tr || []); }
const H = {
  init, search,
  sort: (r) => { sortHits(r.mode, r.slot); return true; },
  page: (r) => page(r.start, r.count, r.slot),
  kwic, forms, collocates, lexicon, getDoc, passage,
  findRef: (r) => findRef(r.id, r.ref),
  preload: async (r) => { await Promise.all(r.parts.map(([k, p]) => ensure(k, p))); return true; },
};
self.onmessage = async (ev) => {
  const { id, type, payload } = ev.data;
  try {
    const f = H[type]; if (!f) throw new Error('Richiesta sconosciuta: ' + type);
    const result = await f(payload || {});
    post({ t: 'reply', id, ok: true, result });
  } catch (e) {
    post({ t: 'reply', id, ok: false, error: String(e && e.message || e) });
  }
};
