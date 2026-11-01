/* Learn course translation (TASK-193). The cards stay English; a language is a catalog i18n/<lang>.json:
   { "_player": {English: translation}, "<card slug>": {English: translation}, ... }  (English text = key).
   vptLearnTranslate(doc, map) rewrites the card's text nodes in place and keeps doing it for text the card's
   own script writes later (counters, typed text). Keys may hold {n} for a number ("Channel {n}").
   Used by the Learn player (same-origin card iframe) and by render.py --lang. */
(function () {
  function compile(map) {
    var pats = [];
    Object.keys(map).forEach(function (k) {
      if (k.indexOf('{n}') < 0) return;
      var esc = k.split('{n}').map(function (p) { return p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); });
      pats.push([new RegExp('^' + esc.join('(-?[\\d.,−]+)') + '$'), map[k]]);
    });
    var typed = Object.keys(map).filter(function (k) { return k.length >= 16; });
    return function (s) {
      var key = s.trim();
      if (!key) return null;
      if (Object.prototype.hasOwnProperty.call(map, key)) return s.replace(key, map[key]);
      for (var i = 0; i < pats.length; i++) {
        var m = key.match(pats[i][0]);
        if (m) { var j = 1, out = pats[i][1].replace(/\{n\}/g, function () { return m[j++]; }); return s.replace(key, out); }
      }
      // typed text: a prefix of a long string grows letter by letter; show the same share of the translation
      var hits = typed.filter(function (k) { return k.length > key.length && k.indexOf(key) === 0; });
      if (hits.length === 1) {
        var tr = map[hits[0]];
        return s.replace(key, tr.slice(0, Math.round(tr.length * key.length / hits[0].length)));
      }
      return null;
    };
  }

  // room(el) < 1: the text of el is wider than the space it has, either el itself (a fixed-width label) or the
  // nearest visible box around it (an ancestor with a background or a border), minus that box's padding.
  // 0.9 = it needs to be 10 % narrower. Used by the auto-fit below and by learn_i18n.py overflow.
  function room(el) {
    var view = el.ownerDocument.defaultView, r = el.ownerDocument.createRange();
    r.selectNodeContents(el);
    var t = r.getBoundingClientRect();
    if (!t.width) return NaN;   // not laid out yet (hidden, scaled to 0): measure again later
    var k = el.clientWidth > 0 && el.scrollWidth > el.clientWidth + 1 ? el.clientWidth / el.scrollWidth : 1;
    for (var a = el; a && a !== el.ownerDocument.body; a = a.parentElement) {
      var cs = view.getComputedStyle(a);
      var bg = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent';
      if (!bg && !(parseFloat(cs.borderLeftWidth) > 0 && parseFloat(cs.borderRightWidth) > 0)) continue;
      var b = a.getBoundingClientRect();
      var left = b.left + parseFloat(cs.borderLeftWidth) + Math.min(parseFloat(cs.paddingLeft), 8);
      var right = b.right - parseFloat(cs.borderRightWidth) - Math.min(parseFloat(cs.paddingRight), 8);
      if (right - left > 0) {
        var outL = t.left < left - 1, outR = t.right > right + 1;
        if (outL && outR) k = Math.min(k, (right - left) / t.width);             // centred: both sides
        else if (outR) k = Math.min(k, (right - t.left) / t.width);           // runs out on the right
        else if (outL) k = Math.min(k, (t.right - left) / t.width);
      }
      break;
    }
    return k;
  }

  function translate(doc, map) {
    if (!map || doc.__vptLearnLang) return;
    var tr = compile(map), mine = new WeakMap();   // node -> the value we wrote (not to translate it twice)
    var view = doc.defaultView, boxes = [];
    function box(p) { return view.getComputedStyle(p).display === 'inline' && p.parentElement ? p.parentElement : p; }
    function fix(node) {
      if (node.nodeType !== 3) return;
      var p = node.parentElement;
      if (!p || p.closest('script,style')) return;
      if (mine.get(node) === node.nodeValue) return;
      var out = tr(node.nodeValue);
      if (out !== null && out !== node.nodeValue) {
        var b = box(p);
        if (b.__vptOver === undefined) { var k0 = room(b); b.__vptOver = k0 < 1; boxes.push(b); }   // the English text's state
        node.nodeValue = out;
        b.__vptDone = false;
      }
      mine.set(node, node.nodeValue);
    }
    // a translated label wider than the box its English fitted in: scale that label down, never below 70 %
    function fit() {
      var later = false;
      boxes.forEach(function (b) {
        if (b.__vptOver || b.__vptDone) return;
        if (b.__vptSize === undefined) b.__vptSize = parseFloat(view.getComputedStyle(b).fontSize);
        b.style.fontSize = b.__vptSize + 'px';
        var k = room(b);
        if (isNaN(k)) { later = true; return; }
        if (k < 1) b.style.fontSize = (b.__vptSize * Math.max(0.7, k * 0.98)) + 'px';
        b.__vptDone = true;
      });
      // labels not laid out yet (they pop in later): look again on the next frames, for at most 20 s
      if (later && Date.now() - t0 < 20000) view.requestAnimationFrame(fit);
    }
    var t0 = Date.now();
    function walk(root) {
      if (root.nodeType === 3) return fix(root);
      var w = doc.createTreeWalker(root, 4), n;
      while ((n = w.nextNode())) fix(n);
    }
    // the social views (4x5, 1x1) stack headline, diagram and caption: a longer headline or caption would push the
    // caption into the diagram, so each block keeps its English height (scaled down, headline to 72 %, caption 80 %)
    var blocks = [['h1', 0.72], ['.caption', 0.8]].map(function (x) {
      var e = doc.querySelector(x[0]);
      return e && e.offsetHeight ? [e, e.offsetHeight, x[1]] : null;
    }).filter(Boolean);
    walk(doc.body);
    blocks.forEach(function (x) {
      var e = x[0], size = parseFloat(view.getComputedStyle(e).fontSize), k = 1;
      while (e.offsetHeight > x[1] + 1 && k > x[2]) { k -= 0.02; e.style.fontSize = size * k + 'px'; }
    });
    fit();
    var title = doc.querySelector('title');
    if (title && map[title.textContent]) title.textContent = map[title.textContent];
    new doc.defaultView.MutationObserver(function (recs) {
      recs.forEach(function (r) {
        if (r.type === 'characterData') fix(r.target);
        else r.addedNodes.forEach(walk);
      });
      fit();
    }).observe(doc.body, { subtree: true, childList: true, characterData: true });
    doc.__vptLearnLang = true;
  }

  var g = typeof window !== 'undefined' ? window : this;
  g.vptLearnTranslate = translate; g.vptLearnRoom = room;
})();
