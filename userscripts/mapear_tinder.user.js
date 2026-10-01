// ==UserScript==
// @name         Mapa de telas - Tinder (pesquisa)
// @namespace    tinder-pesquisa
// @version      0.1
// @description  Lista a estrutura dos elementos da tela atual, sem copiar textos de conversas e sem enviar nada.
// @match        https://tinder.com/*
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function () {
  'use strict';

  const ATTRS = ['data-testid', 'role', 'aria-label', 'type', 'placeholder', 'contenteditable', 'name'];
  const TARGETS = 'button, a[href], input, textarea, [contenteditable], [role], [data-testid], [aria-label]';
  const Z = '2147483647';

  const btn = document.createElement('button');
  btn.textContent = 'Mapear tela';
  Object.assign(btn.style, {
    position: 'fixed', bottom: '90px', right: '12px', zIndex: Z,
    padding: '10px 14px', background: '#111', color: '#fff',
    border: 'none', borderRadius: '8px', fontSize: '14px',
  });
  document.body.appendChild(btn);

  function describe(el) {
    const parts = [el.tagName.toLowerCase()];
    for (const a of ATTRS) {
      const v = el.getAttribute(a);
      if (v !== null) parts.push(`${a}="${v.slice(0, 40)}"`);
    }
    const cls = (el.getAttribute('class') || '').split(/\s+/).filter(Boolean).slice(0, 3).join('.');
    if (cls) parts.push(`class=".${cls}"`);
    return parts.join(' ');
  }

  function path(el) {
    const out = [];
    while (el && el !== document.body && out.length < 6) {
      const tid = el.getAttribute('data-testid');
      out.unshift(tid ? `[data-testid="${tid}"]` : el.tagName.toLowerCase());
      el = el.parentElement;
    }
    return out.join(' > ');
  }

  function buildReport() {
    // Match ids in the URL are replaced so the report does not identify anyone.
    const lines = [`URL: ${location.pathname.replace(/[a-f0-9]{16,}/gi, '<id>')}`];
    const seen = new Set();
    document.querySelectorAll(TARGETS).forEach((el) => {
      if (el === btn || el.closest('#mapa-overlay')) return;
      const line = `${describe(el)}  @ ${path(el)}`;
      if (!seen.has(line)) {
        seen.add(line);
        lines.push(line);
      }
    });
    return lines.slice(0, 300).join('\n');
  }

  function showReport(text) {
    const overlay = document.createElement('div');
    overlay.id = 'mapa-overlay';
    Object.assign(overlay.style, {
      position: 'fixed', inset: '0', zIndex: Z, background: '#fff', color: '#111',
      display: 'flex', flexDirection: 'column', gap: '8px', padding: '12px',
    });

    const note = document.createElement('p');
    note.textContent = 'Confira e apague nomes de pessoas que aparecerem em aria-label antes de enviar.';
    note.style.margin = '0';
    note.style.fontSize = '13px';

    const area = document.createElement('textarea');
    area.value = text;
    area.readOnly = true;
    Object.assign(area.style, { flex: '1', fontSize: '11px', fontFamily: 'monospace' });

    const row = document.createElement('div');
    row.style.display = 'flex';
    row.style.gap = '8px';

    const copy = document.createElement('button');
    copy.textContent = 'Copiar';
    copy.addEventListener('click', () => {
      navigator.clipboard.writeText(area.value)
        .then(() => { copy.textContent = 'Copiado'; })
        .catch(() => { area.select(); copy.textContent = 'Selecionado: copie manualmente'; });
    });

    const close = document.createElement('button');
    close.textContent = 'Fechar';
    close.addEventListener('click', () => overlay.remove());

    for (const b of [copy, close]) Object.assign(b.style, { flex: '1', padding: '10px', fontSize: '14px' });
    row.append(copy, close);
    overlay.append(note, area, row);
    document.body.appendChild(overlay);
  }

  btn.addEventListener('click', () => showReport(buildReport()));
})();
