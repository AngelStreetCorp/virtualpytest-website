/* VirtualPyTest site mockups: theme, language, Ask AI, menu and motion.
   Theme, language and Ask AI follow the live site exactly (same storage keys, same API). */
(function(){
  var root = document.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Theme: localStorage['virtualpytest:theme'] = light | dark, else the system ---------- */
  var mq = window.matchMedia('(prefers-color-scheme: dark)');
  function currentTheme(){ return root.getAttribute('data-theme') || (mq.matches ? 'dark' : 'light'); }
  // Screenshots are <picture> with a dark <source>; a forced theme rewrites its media so the image agrees.
  function syncPictures(){
    var forced = root.getAttribute('data-theme');
    document.querySelectorAll('picture source[data-dark]').forEach(function(s){
      s.media = forced === 'dark' ? 'all' : forced === 'light' ? 'not all' : '(prefers-color-scheme: dark)';
    });
  }
  function labelThemeButton(){
    var b = document.querySelector('[data-theme-toggle]'); if(!b) return;
    var label = t('Switch to ' + (currentTheme() === 'dark' ? 'light' : 'dark') + ' theme');
    b.setAttribute('aria-label', label); b.setAttribute('title', label);
  }
  document.addEventListener('click', function(e){
    if(!e.target.closest('[data-theme-toggle]')) return;
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('virtualpytest:theme', next); } catch(err) {}
    syncPictures(); labelThemeButton();
  });
  mq.addEventListener && mq.addEventListener('change', labelThemeButton);

  /* ---------- Language: same catalog shape and walker as the live site ---------- */
  var supported = ['en','fr','es','de','zh-CN','hi'];
  var names = {en:'English',fr:'Français',es:'Español',de:'Deutsch','zh-CN':'中文',hi:'हिन्दी'};
  var codes = {en:'EN',fr:'FR',es:'ES',de:'DE','zh-CN':'ZH',hi:'HI'};
  var catalogs = {}, current = 'en';
  function t(message){ var c = catalogs[current]; return (c && c[message]) || message; }
  window.vptT = t; window.vptLocale = function(){ return current; };
  window.vptLocaleHooks = window.vptLocaleHooks || [];

  function applyLocale(lang){
    current = supported.indexOf(lang) >= 0 ? lang : 'en';
    root.lang = current;
    var titleKey = document.querySelector('meta[name="vpt-title"]');
    if(titleKey) document.title = t(titleKey.content);
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), node;
    while((node = walker.nextNode())){
      if(node.parentElement.closest('script,style,code,.no-i18n')) continue;
      if(typeof node.__src === 'undefined') node.__src = node.nodeValue;
      var key = node.__src.trim(); if(!key) continue;
      node.nodeValue = node.__src.replace(key, t(key));
    }
    document.querySelectorAll('[alt],[aria-label],[title],[placeholder]').forEach(function(el){
      ['alt','aria-label','title','placeholder'].forEach(function(a){
        if(!el.hasAttribute(a) || el.hasAttribute('data-theme-toggle')) return;
        var o = el.getAttribute('data-src-' + a);
        if(o === null){ o = el.getAttribute(a); el.setAttribute('data-src-' + a, o); }
        el.setAttribute(a, t(o));
      });
    });
    var picker = document.getElementById('language-select');
    if(picker){
      picker.querySelector('[data-language-code]').textContent = codes[current];
      picker.setAttribute('aria-label', t('Language') + ': ' + names[current]);
      document.querySelectorAll('#language-menu [data-locale]').forEach(function(o){
        o.setAttribute('aria-selected', o.getAttribute('data-locale') === current ? 'true' : 'false');
      });
    }
    labelThemeButton();
    window.vptLocaleHooks.forEach(function(h){ try { h(); } catch(e) {} });
  }

  var picker = document.getElementById('language-select');
  var menu = document.getElementById('language-menu');
  function closeMenu(focus){ if(!menu) return; menu.hidden = true; picker.setAttribute('aria-expanded','false'); if(focus) picker.focus(); }
  if(picker && menu){
    picker.addEventListener('click', function(){
      var opening = menu.hidden; menu.hidden = !opening;
      picker.setAttribute('aria-expanded', opening ? 'true' : 'false');
      if(opening){ var s = menu.querySelector('[data-locale="' + current + '"]'); if(s) s.focus(); }
    });
    menu.addEventListener('click', function(e){
      var o = e.target.closest('[data-locale]'); if(!o) return;
      applyLocale(o.getAttribute('data-locale'));
      try { localStorage.setItem('virtualpytest:language', current); } catch(err) {}
      closeMenu(true);
    });
    menu.addEventListener('keydown', function(e){
      var opts = Array.prototype.slice.call(menu.querySelectorAll('[data-locale]'));
      var i = opts.indexOf(document.activeElement);
      if(e.key === 'Escape'){ e.preventDefault(); closeMenu(true); }
      else if(e.key === 'ArrowDown' || e.key === 'ArrowUp'){ e.preventDefault(); opts[(i + (e.key === 'ArrowDown' ? 1 : -1) + opts.length) % opts.length].focus(); }
    });
    document.addEventListener('click', function(e){ if(!e.target.closest('.lang')) closeMenu(false); });
  }

  // Served over http the catalog is locales.json. Opened from disk (file://) the browser blocks that fetch,
  // so the same catalog is read from locales.js, generated next to it by tools/build_locales.py.
  function loadCatalog(){
    if(location.protocol !== 'file:') return fetch('locales.json').then(function(r){ if(!r.ok) throw new Error('locales'); return r.json(); });
    return new Promise(function(resolve, reject){
      var s = document.createElement('script'); s.src = 'locales.js';
      s.onload = function(){ resolve(window.VPT_LOCALES || {}); }; s.onerror = reject; document.head.appendChild(s);
    });
  }
  loadCatalog().then(function(d){ catalogs = d; }).catch(function(){ catalogs = {}; })
    .then(function(){
      var want = '';
      try { want = localStorage.getItem('virtualpytest:language') || ''; } catch(e) {}
      if(supported.indexOf(want) < 0){
        var sys = (navigator.language || 'en').toLowerCase();
        var b = sys.indexOf('zh') === 0 ? 'zh-CN' : sys.slice(0,2);
        want = supported.indexOf(b) >= 0 ? b : 'en';
      }
      applyLocale(want);
      root.setAttribute('data-locale-ready', current);
    });

  /* ---------- Mobile drawer ---------- */
  var burger = document.querySelector('.burger'), sheet = document.querySelector('.sheet');
  if(burger && sheet){
    function setSheet(open){
      sheet.classList.toggle('open', open); burger.classList.toggle('x', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      sheet.setAttribute('aria-hidden', open ? 'false' : 'true');
      document.body.style.overflow = open ? 'hidden' : '';
    }
    burger.addEventListener('click', function(){ setSheet(!sheet.classList.contains('open')); });
    sheet.addEventListener('click', function(e){ if(e.target.closest('a')) setSheet(false); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && sheet.classList.contains('open')) setSheet(false); });
  }

  /* Nav hides while scrolling down, comes back on the way up (one rAF per frame at most). */
  var nav = document.querySelector('.navwrap'), lastY = window.scrollY, ticking = false;
  if(nav) window.addEventListener('scroll', function(){
    if(ticking) return; ticking = true;
    requestAnimationFrame(function(){
      var y = window.scrollY;
      if(y > lastY + 4 && y > 120) nav.classList.add('is-hidden');
      else if(y < lastY - 4 || y <= 120) nav.classList.remove('is-hidden');
      lastY = y; ticking = false;
    });
  }, {passive:true});

  /* ---------- Tagline: built from the translated sentence, one span per word (per glyph in Chinese) ---------- */
  var tagObserver = null;
  function buildTagline(){
    document.querySelectorAll('[data-tagline]').forEach(function(p){
      var accent = +(p.getAttribute('data-accent') || 0);
      p.innerHTML = '';
      p.getAttribute('data-tagline').split('|').forEach(function(line, li, all){
        var text = t(line), cjk = /[\u3400-\u9fff]/.test(text), parts = cjk ? Array.from(text) : text.split(' ');
        parts.forEach(function(w, i){
          var s = document.createElement('span');
          s.className = 'w' + (li === all.length - 1 && i >= parts.length - accent ? ' acc' : '');
          s.textContent = w; p.appendChild(s);
          if(!cjk && i < parts.length - 1) p.appendChild(document.createTextNode(' '));
        });
        if(li < all.length - 1) p.appendChild(document.createElement('br'));
      });
      p.querySelectorAll('.w').forEach(function(w){ if(tagObserver) tagObserver.observe(w); else w.classList.add('on'); });
    });
  }
  window.vptLocaleHooks.push(buildTagline);

  /* ---------- Tabs (mockup 3 feature groups) ---------- */
  document.querySelectorAll('[data-tabs]').forEach(function(list){
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    function select(tab, focus){
      tabs.forEach(function(x){
        var on = x === tab;
        x.setAttribute('aria-selected', on ? 'true' : 'false'); x.tabIndex = on ? 0 : -1;
        document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
      });
      if(focus) tab.focus();
    }
    tabs.forEach(function(tab, i){
      tab.addEventListener('click', function(){ select(tab); });
      tab.addEventListener('keydown', function(e){
        if(e.key === 'ArrowRight' || e.key === 'ArrowLeft'){ e.preventDefault(); select(tabs[(i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length], true); }
      });
    });
  });

  /* ---------- Screenshot carousel (best-of hero): auto plays, pauses on hover, off under reduced motion ---------- */
  document.querySelectorAll('[data-carousel]').forEach(function(c){
    var slides = Array.prototype.slice.call(c.querySelectorAll('.slide'));
    var cap = c.querySelector('.cap-text'), dotsBox = c.querySelector('.dots'), playBtn = c.querySelector('[data-play]');
    var i = 0, timer = null, playing = !reduce, hover = false, dots = [];
    slides.forEach(function(s, k){
      var b = document.createElement('button'); b.type = 'button';
      b.addEventListener('click', function(){ show(k); restart(); });
      dotsBox.appendChild(b); dots.push(b);
    });
    function label(){
      dots.forEach(function(b, k){ b.setAttribute('aria-label', t('Show screenshot {index} of {count}').replace('{index}', k + 1).replace('{count}', slides.length)); });
      var l = t(playing ? 'Pause slideshow' : 'Play slideshow'); playBtn.setAttribute('aria-label', l); playBtn.setAttribute('title', l);
      playBtn.classList.toggle('paused', !playing);
      cap.textContent = t(slides[i].getAttribute('data-caption'));
    }
    function show(n){
      i = (n + slides.length) % slides.length;
      slides.forEach(function(s, k){ s.classList.toggle('on', k === i); s.setAttribute('aria-hidden', k === i ? 'false' : 'true'); });
      dots.forEach(function(b, k){ b.setAttribute('aria-current', k === i ? 'true' : 'false'); });
      // warm the next slide so the fade never shows an empty frame
      var next = slides[(i + 1) % slides.length].querySelector('img'); if(next) next.loading = 'eager';
      label();
    }
    function restart(){ clearTimeout(timer); if(playing && !hover) timer = setTimeout(function(){ show(i + 1); restart(); }, 5000); }
    c.querySelector('[data-prev]').addEventListener('click', function(){ show(i - 1); restart(); });
    c.querySelector('[data-next]').addEventListener('click', function(){ show(i + 1); restart(); });
    playBtn.addEventListener('click', function(){ playing = !playing; label(); restart(); });
    c.addEventListener('mouseenter', function(){ hover = true; clearTimeout(timer); });
    c.addEventListener('mouseleave', function(){ hover = false; restart(); });
    c.addEventListener('focusin', function(){ hover = true; clearTimeout(timer); });
    c.addEventListener('focusout', function(){ hover = false; restart(); });
    window.vptLocaleHooks.push(label);
    show(0); restart();
  });

  /* ---------- Video facade: YouTube loads only when the visitor presses play ---------- */
  document.querySelectorAll('[data-video-src]').forEach(function(btn){
    btn.addEventListener('click', function(){
      var box = btn.parentElement, f = document.createElement('iframe');
      f.src = btn.getAttribute('data-video-src'); f.title = 'VirtualPyTest in 60 seconds';
      f.allow = 'accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.referrerPolicy = 'strict-origin-when-cross-origin'; f.allowFullscreen = true;
      box.appendChild(f); btn.remove();
    });
  });

  /* ---------- Zoom: every screenshot opens at full size in a dialog ---------- */
  var zoom = document.getElementById('zoom');
  if(zoom && zoom.showModal){
    var zImg = document.getElementById('zoom-img'), zCap = document.getElementById('zoom-cap');
    document.addEventListener('click', function(e){
      var img = e.target.closest('.shot img'); if(!img || e.target.closest('.zoom,.video')) return;
      // the 2x file is the same name without the -1040 suffix
      zImg.src = (img.currentSrc || img.src).replace('-1040.webp', '.webp');
      zImg.alt = img.alt; zCap.textContent = img.alt;
      zoom.showModal();
    });
    zoom.addEventListener('click', function(e){ if(e.target === zoom || e.target === zImg || e.target.closest('[data-zoom-close]')) zoom.close(); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Enter' && document.activeElement && document.activeElement.matches('.shot img')) document.activeElement.click(); });
    document.querySelectorAll('.shot img').forEach(function(img){ img.tabIndex = 0; img.setAttribute('role', 'button'); });
  }

  /* ---------- Motion ---------- */
  if('IntersectionObserver' in window && !reduce){
    // Card intro once, at about 30% visible.
    var rv = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); rv.unobserve(e.target); } });
    }, {threshold:0.3, rootMargin:'0px 0px -5% 0px'});
    document.querySelectorAll('[data-rv]').forEach(function(el){ rv.observe(el); });
    // Stories run only while on screen; they start after the intro has landed.
    var st = new IntersectionObserver(function(es){
      es.forEach(function(e){
        var el = e.target;
        if(e.isIntersecting){ clearTimeout(el.__t); el.__t = setTimeout(function(){ el.classList.add('playing'); }, el.__started ? 0 : 900); el.__started = true; }
        else { clearTimeout(el.__t); el.classList.remove('playing'); }
      });
    }, {threshold:0.2});
    document.querySelectorAll('[data-story]').forEach(function(el){ st.observe(el); });
    // Tagline: each word lights up as it crosses a line 40% up the viewport.
    tagObserver = new IntersectionObserver(function(es){
      es.forEach(function(e){ e.target.classList.toggle('on', e.boundingClientRect.top < window.innerHeight * 0.6); });
    }, {rootMargin:'0px 0px -40% 0px', threshold:[0,1]});
  } else {
    document.querySelectorAll('[data-rv]').forEach(function(el){ el.classList.add('in'); });
  }
  buildTagline();

  /* ---------- Ask AI: same endpoint, payload, history key and clear button as the live site ---------- */
  var panel = document.getElementById('ask-panel');
  if(panel){
    var log = document.getElementById('ask-log'), form = document.getElementById('ask-form');
    var input = document.getElementById('ask-input'), send = document.getElementById('ask-send');
    var fab = document.querySelector('.ask-fab');
    var api = panel.getAttribute('data-api').replace(/\/$/, '') + '/server/public/ask';
    var docsBase = 'https://github.com/AngelStreetCorp/virtualpytest/blob/main/docs/';
    var KEY = 'askai:history', MAX = 40, history = [], busy = false;
    function readHistory(){ try { var p = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(p) ? p : []; } catch(e){ return []; } }
    function writeHistory(){ try { localStorage.setItem(KEY, JSON.stringify(history.slice(-MAX))); } catch(e){} }
    function openPanel(){ panel.classList.add('is-open'); fab.style.display = 'none'; input.focus(); }
    function closePanel(){ panel.classList.remove('is-open'); fab.style.display = ''; }
    document.addEventListener('click', function(e){ if(e.target.closest('[data-ask-open]')){ e.preventDefault(); openPanel(); } });
    panel.querySelector('[data-ask-close]').addEventListener('click', closePanel);
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && panel.classList.contains('is-open')) closePanel(); });
    var expandBtn = panel.querySelector('[data-ask-expand]');
    function setLarge(on){
      panel.classList.toggle('is-large', on);
      var l = t(on ? 'Shrink' : 'Expand'); expandBtn.setAttribute('aria-label', l); expandBtn.setAttribute('title', l);
      try { localStorage.setItem('askai:large', on ? '1' : '0'); } catch(e) {}
    }
    expandBtn.addEventListener('click', function(){ setLarge(!panel.classList.contains('is-large')); });
    try { if(localStorage.getItem('askai:large') === '1') setLarge(true); } catch(e) {}

    function makeMsg(kind, text){ var d = document.createElement('div'); d.className = 'ask-msg ' + kind; d.textContent = text; return d; }
    function makeSources(paths){
      var d = document.createElement('div'); d.className = 'ask-src';
      d.appendChild(document.createTextNode(t('Sources: ')));
      paths.forEach(function(p, i){
        if(i) d.appendChild(document.createTextNode(' · '));
        var a = document.createElement('a'); a.href = docsBase + p; a.target = '_blank'; a.rel = 'noopener'; a.textContent = p; d.appendChild(a);
      });
      return d;
    }
    function addMsg(kind, text, persist){
      var d = makeMsg(kind, text); log.appendChild(d); log.scrollTop = log.scrollHeight;
      if(persist !== false){ history.push({role: kind === 'user' ? 'user' : (kind === 'error' ? 'error' : 'bot'), text: text}); writeHistory(); syncClear(); }
      return d;
    }
    var clearBtn = panel.querySelector('[data-ask-clear]');
    var hBox = document.getElementById('ask-history'), hBody = document.getElementById('ask-history-body');
    var hToggle = document.getElementById('ask-history-toggle'), hLabel = document.getElementById('ask-history-label');
    var restored = 0;
    function setHistoryLabel(){ hLabel.textContent = t('Previous questions') + ' (' + restored + ')'; }
    function syncClear(){ clearBtn.hidden = history.length === 0; }
    hToggle.addEventListener('click', function(){ var o = hBox.classList.toggle('is-open'); hToggle.setAttribute('aria-expanded', o ? 'true' : 'false'); });
    clearBtn.addEventListener('click', function(){
      history = []; try { localStorage.removeItem(KEY); } catch(e) {}
      log.innerHTML = ''; hBody.innerHTML = ''; hBox.hidden = true; restored = 0; input.value = ''; input.focus(); syncClear();
    });
    window.vptLocaleHooks.push(setHistoryLabel);
    history = readHistory(); syncClear();
    if(history.length){
      history.forEach(function(it){
        if(!it || !it.text) return;
        if(it.role === 'user') restored++;
        hBody.appendChild(makeMsg(it.role === 'user' ? 'user' : (it.role === 'error' ? 'error' : 'bot'), it.text));
        if(it.sources && it.sources.length) hBody.appendChild(makeSources(it.sources));
      });
      hBox.hidden = false; setHistoryLabel();
    }
    function ask(q){
      q = (q || '').trim(); if(!q || busy) return;
      busy = true; send.disabled = true; input.value = '';
      addMsg('user', q);
      var typing = addMsg('bot ask-typing', t('Checking the docs') + '…', false);
      fetch(api, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({question:q, language: current})})
        .then(function(r){ return r.json().then(function(b){ return {ok:r.ok, body:b}; }); })
        .then(function(res){
          typing.remove();
          if(res.ok && res.body && res.body.success){
            addMsg('bot', res.body.answer);
            if(res.body.sources && res.body.sources.length){ log.appendChild(makeSources(res.body.sources)); history[history.length - 1].sources = res.body.sources; writeHistory(); }
          } else addMsg('error', t((res.body && res.body.error) || 'Something went wrong. Try again in a moment.'));
        })
        .catch(function(){ typing.remove(); addMsg('error', t('Could not reach the assistant. Try again in a moment.')); })
        .then(function(){ busy = false; send.disabled = false; input.focus(); log.scrollTop = log.scrollHeight; });
    }
    form.addEventListener('submit', function(e){ e.preventDefault(); ask(input.value); });
    document.querySelectorAll('[data-ask-chip]').forEach(function(c){ c.addEventListener('click', function(){ ask(c.textContent); }); });
  }

  syncPictures();
})();
