/* Progressive enhancement only. All demo data is fictional and stays in this page. */
(() => {
  'use strict';
  const all = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.documentElement.classList.add('enhanced');

  const menus = all('.site-header details');
  const closeMenus = (restoreFocus = false) => menus.forEach(menu => {
    if (!menu.open) return;
    menu.open = false;
    if (restoreFocus) menu.querySelector('summary').focus();
  });
  document.addEventListener('click', event => {
    menus.forEach(menu => { if (menu.open && !menu.contains(event.target)) menu.open = false; });
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenus(true);
  });
  menus.forEach(menu => menu.addEventListener('toggle', () => {
    if (menu.open) menus.forEach(other => { if (other !== menu) other.open = false; });
  }));
  const root = document.documentElement;
  const header = document.querySelector('.site-header');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const mobileLayout = window.matchMedia('(max-width: 760px)');
  mobileLayout.addEventListener('change', () => closeMenus());

  // Weighted wheel/trackpad scrolling on desktop only. Touch, keyboard and reduced motion stay native.
  if (window.Lenis && finePointer.matches && !motion.matches) {
    window.lenis = new window.Lenis({
      autoRaf: true, lerp: 0.042, wheelMultiplier: 0.7, smoothWheel: true, syncTouch: false, // heavier, slower glide
      stopInertiaOnNavigate: true,
      anchors: { duration: 1.7 }, // in-page links glide to their section (respects scroll-margin-top)
      prevent: node => node.matches('textarea, select, dialog, .experience-records, .mobile-menu nav, .menu-panel')
    });
  }
  // In-page links also move keyboard focus to the section they point at (scrolling alone leaves it behind).
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    const id = link && link.getAttribute('href').slice(1);
    const target = id && document.getElementById(id);
    if (!target) return;
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  });

  // Compact header: shrinks after a little scroll, slides away going down, returns on any upward scroll.
  let lastY = window.scrollY;
  const updateHeader = () => {
    const y = window.scrollY, delta = y - lastY;
    root.classList.toggle('scrolled', y > 24);
    if (y < 160) root.classList.remove('header-hidden');
    else if (Math.abs(delta) > 8) {
      const busy = motion.matches || header.matches(':focus-within') || menus.some(menu => menu.open);
      root.classList.toggle('header-hidden', delta > 0 && !busy);
    } else return;
    lastY = y;
  };
  window.addEventListener('scroll', updateHeader, { passive: true });
  header.addEventListener('focusin', () => root.classList.remove('header-hidden'));
  updateHeader();

  // Header menus (Product, Contact) open on hover right under their label and fade out on leave.
  all('.desktop-nav .nav-menu').forEach(menu => {
    let openTimer = 0, closeTimer = 0, openedByHover = false;
    const shut = () => {
      if (!menu.open) return;
      menu.classList.add('is-closing');
      setTimeout(() => { menu.open = false; menu.classList.remove('is-closing'); }, motion.matches ? 0 : 280);
    };
    menu.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse' || !finePointer.matches) return;
      clearTimeout(closeTimer);
      menu.classList.remove('is-closing');
      if (!menu.open) openTimer = setTimeout(() => { menu.open = true; openedByHover = true; }, 60);
    });
    menu.addEventListener('pointerleave', event => {
      if (event.pointerType !== 'mouse') return;
      clearTimeout(openTimer);
      closeTimer = setTimeout(shut, 220);
    });
    menu.querySelector('summary').addEventListener('click', event => {
      // A click right after hover-opening should not snap the menu shut again.
      if (openedByHover && menu.open) { event.preventDefault(); openedByHover = false; }
    });
    menu.addEventListener('toggle', () => { if (!menu.open) openedByHover = false; });
  });

  // Sliding pill behind the desktop nav links.
  const nav = document.querySelector('.desktop-nav');
  if (nav) {
    const pill = document.createElement('span');
    pill.className = 'nav-pill'; pill.setAttribute('aria-hidden', 'true');
    nav.prepend(pill);
    const targets = all(':scope > a:not(.button), .nav-menu > summary', nav);
    const current = targets.find(item => item.getAttribute('aria-current') === 'page' || item.classList.contains('is-current'));
    const moveTo = item => {
      if (!item) { pill.classList.remove('on'); return; }
      const a = item.getBoundingClientRect(), b = nav.getBoundingClientRect();
      pill.style.setProperty('--x', (a.left - b.left) + 'px');
      pill.style.setProperty('--w', a.width + 'px');
      pill.classList.add('on');
    };
    targets.forEach(item => {
      item.addEventListener('pointerenter', () => moveTo(item));
      item.addEventListener('focus', () => moveTo(item));
    });
    nav.addEventListener('pointerleave', () => moveTo(current));
    nav.addEventListener('focusout', event => { if (!nav.contains(event.relatedTarget)) moveTo(current); });
    window.addEventListener('resize', () => moveTo(current));
    moveTo(current);
  }

  // Gentle magnetic pull on the main call-to-action buttons (fine pointers only).
  all('.site-header .button, .launch-copy .button, .closing .button').forEach(button => {
    button.addEventListener('pointermove', event => {
      if (!finePointer.matches || motion.matches) return;
      const r = button.getBoundingClientRect();
      const clamp = value => Math.max(-8, Math.min(8, value));
      button.style.setProperty('--mx', clamp((event.clientX - r.left - r.width / 2) * 0.3) + 'px');
      button.style.setProperty('--my', clamp((event.clientY - r.top - r.height / 2) * 0.3) + 'px');
    });
    button.addEventListener('pointerleave', () => { button.style.removeProperty('--mx'); button.style.removeProperty('--my'); });
  });

  // AI assistant window: the app's orb (orb.js, loaded when the window comes near) and a short,
  // fictional chat that plays itself — the question is typed into the composer, sent, then Rudra
  // thinks and answers word by word. Plays only while on screen; reduced motion keeps the still chat.
  const loadOrb = () => window.StrandsOrb ? Promise.resolve() : (loadOrb.promise ||= new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = 'orb.js'; script.onload = resolve; script.onerror = reject;
    document.head.append(script);
  }));
  // Sound for the assistant window, made in the browser (no audio files): a soft ambient pad for the orb that
  // breathes and shifts with its state, quiet key clicks while the question is typed, a tiny "send", a two-note
  // chime when Rudra answers and soft ticks as the words appear. It fades in only while the window is on screen
  // and fades out (then sleeps) as soon as you scroll away. Browsers allow sound only after one click or key press.
  const assistantSound = () => {
    const AC = window.AudioContext || window.webkitAudioContext;
    let ctx = null, master = null, pad = null, tone = null, noise = null, live = false, sleepTimer = 0;
    let enabled = true;
    try { enabled = localStorage.getItem('rudra-sound') !== 'off'; } catch (error) { /* private mode: default on */ }
    const build = () => {
      if (ctx || !AC) return ctx;
      ctx = new AC();
      master = ctx.createGain(); master.gain.value = 0; master.connect(ctx.destination);
      tone = ctx.createBiquadFilter(); tone.type = 'lowpass'; tone.frequency.value = 520; tone.Q.value = 0.5;
      pad = ctx.createGain(); pad.gain.value = 0.05; tone.connect(pad); pad.connect(master);
      // A warm, open chord (A · E · A · E) with slight detune so it slowly shimmers.
      [[110, 0, 0.5], [164.81, -5, 0.3], [220, 4, 0.2], [329.63, -3, 0.07]].forEach(([freq, detune, level]) => {
        const osc = ctx.createOscillator(), gain = ctx.createGain();
        osc.type = 'sine'; osc.frequency.value = freq; osc.detune.value = detune; gain.gain.value = level;
        osc.connect(gain); gain.connect(tone); osc.start();
      });
      const breathe = (rate, depth, target) => { // slow LFOs: the pad "breathes" like the orb
        const lfo = ctx.createOscillator(), amount = ctx.createGain();
        lfo.frequency.value = rate; amount.gain.value = depth; lfo.connect(amount); amount.connect(target); lfo.start();
      };
      breathe(0.07, 140, tone.frequency); breathe(0.19, 0.012, pad.gain);
      noise = ctx.createBuffer(1, Math.round(ctx.sampleRate * 0.04), ctx.sampleRate);
      const data = noise.getChannelData(0);
      for (let i = 0; i < data.length; i++) data[i] = (Math.random() * 2 - 1) * (1 - i / data.length);
      return ctx;
    };
    const level = () => (live && enabled ? 1 : 0);
    const fade = () => {
      if (!ctx) return;
      const now = ctx.currentTime, on = level();
      clearTimeout(sleepTimer);
      if (on && ctx.state !== 'running') ctx.resume();
      master.gain.cancelScheduledValues(now);
      master.gain.setTargetAtTime(on, now, on ? 0.45 : 0.25); // slow swell in, quicker fade out
      if (!on) sleepTimer = setTimeout(() => { if (!level() && ctx.state === 'running') ctx.suspend(); }, 1600);
    };
    const blip = make => { if (ctx && level() && ctx.state === 'running') make(ctx.currentTime); };
    const click = (freq, gainValue, length) => blip(now => {
      const src = ctx.createBufferSource(), band = ctx.createBiquadFilter(), gain = ctx.createGain();
      src.buffer = noise; band.type = 'bandpass'; band.frequency.value = freq; band.Q.value = 1.4;
      gain.gain.setValueAtTime(0, now); gain.gain.linearRampToValueAtTime(gainValue, now + 0.002); gain.gain.exponentialRampToValueAtTime(0.0001, now + length);
      src.connect(band); band.connect(gain); gain.connect(master); src.start(now); src.stop(now + length + 0.02);
    });
    const note = (freq, at, gainValue, length, endFreq) => blip(now => {
      const osc = ctx.createOscillator(), gain = ctx.createGain(), t = now + at;
      osc.type = 'sine'; osc.frequency.setValueAtTime(freq, t);
      if (endFreq) osc.frequency.exponentialRampToValueAtTime(endFreq, t + length * 0.6);
      gain.gain.setValueAtTime(0, t); gain.gain.linearRampToValueAtTime(gainValue, t + 0.012); gain.gain.exponentialRampToValueAtTime(0.0001, t + length);
      osc.connect(gain); gain.connect(master); osc.start(t); osc.stop(t + length + 0.05);
    });
    const MOODS = { idle: [520, 0.05], listening: [620, 0.055], thinking: [820, 0.06], speaking: [700, 0.068] };
    return {
      get enabled() { return enabled; },
      unlock() { if (build()) fade(); },
      toggle() {
        enabled = !enabled;
        try { localStorage.setItem('rudra-sound', enabled ? 'on' : 'off'); } catch (error) { /* ignore */ }
        if (enabled) build();
        fade();
      },
      active(on) { live = on; fade(); },
      mood(state) {
        if (!ctx) return;
        const [freq, gainValue] = MOODS[state] || MOODS.idle, now = ctx.currentTime;
        tone.frequency.setTargetAtTime(freq, now, 0.8); pad.gain.setTargetAtTime(gainValue, now, 0.8);
      },
      key: () => click(2400 + Math.random() * 1400, 0.07, 0.035),            // a soft keyboard click
      tick: () => click(1150 + Math.random() * 350, 0.035, 0.03),            // a quieter tick per word
      send: () => note(520, 0, 0.05, 0.22, 900),                             // a small rising "send"
      chime: () => { note(659.25, 0, 0.035, 0.9); note(987.77, 0.11, 0.025, 1.1); } // Rudra answers
    };
  };

  all('[data-assistant-demo]').forEach(win => {
    const thread = win.querySelector('[data-assistant-thread]');
    const typed = win.querySelector('[data-assistant-typing]');
    const status = win.querySelector('[data-assistant-state]');
    const send = win.querySelector('.composer-send');
    const chat = all('.chat-msg', thread).map(msg => ({ you: msg.classList.contains('you'), html: msg.innerHTML, text: msg.querySelector('p').textContent }));
    const transcript = thread.cloneNode(true); // screen readers get the whole chat once; the moving copy is decorative
    transcript.className = 'sr-only'; transcript.removeAttribute('data-assistant-thread');
    win.append(transcript); thread.setAttribute('aria-hidden', 'true');
    let orb = null, inView = false, playing = false, waiting = [];
    const sound = assistantSound();
    const soundButton = win.querySelector('[data-assistant-sound]');
    const soundLabel = win.querySelector('[data-assistant-sound-label]');
    let unlocked = false, unlockedAt = 0;
    const showSound = () => {
      soundButton.setAttribute('aria-pressed', String(sound.enabled));
      win.classList.toggle('sound-off', !sound.enabled);
      soundLabel.textContent = !sound.enabled ? 'Sound off' : unlocked ? 'Sound on' : 'Tap for sound';
    };
    const unlock = () => { if (unlocked) return; unlocked = true; unlockedAt = performance.now(); sound.unlock(); showSound(); };
    ['pointerdown', 'keydown'].forEach(type => document.addEventListener(type, unlock, { once: true, capture: true }));
    soundButton.addEventListener('click', () => {
      // The first press anywhere only switches sound on (it is also the browser's permission click).
      if (!unlocked || performance.now() - unlockedAt < 800) { unlock(); if (!sound.enabled) sound.toggle(); } else sound.toggle();
      showSound();
    });
    showSound();
    const visible = () => inView && !document.hidden;
    const resume = () => { if (visible()) waiting.splice(0).forEach(go => go()); };
    const wait = async ms => {
      if (!visible()) await new Promise(go => waiting.push(go));
      await new Promise(go => setTimeout(go, ms));
      if (!visible()) await new Promise(go => waiting.push(go));
    };
    const LABELS = { idle: 'Ready when you are', listening: 'Listening…', thinking: 'Thinking…', speaking: 'Replying…' };
    const setState = state => { win.dataset.state = state; status.textContent = LABELS[state]; orb && orb.setState(state); sound.mood(state); };
    const EASE = 'cubic-bezier(.22,1,.36,1)';
    const add = msg => { // the whole conversation glides up together, the new message rising in from below (FLIP)
      const kids = [...thread.children], before = kids.map(kid => kid.getBoundingClientRect().top);
      thread.append(msg);
      const after = kids.map(kid => kid.getBoundingClientRect().top);
      const top = thread.getBoundingClientRect().top + 30;
      const lift = msg.offsetHeight + parseFloat(getComputedStyle(thread).rowGap || 0);
      const timing = { duration: 720, easing: EASE };
      kids.forEach((kid, i) => {
        if (before[i] !== after[i]) kid.animate([{ transform: `translateY(${before[i] - after[i]}px)` }, { transform: 'none' }], timing);
        if (after[i] < top && !kid.dataset.gone) { // pushed past the top: fade away softly
          kid.dataset.gone = '1';
          kid.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 560, easing: 'ease', fill: 'forwards' });
        }
      });
      msg.animate([{ transform: `translateY(${lift}px)`, opacity: 0 }, { transform: 'none', opacity: 1 }], timing);
      while (thread.children.length > 5) thread.firstElementChild.remove();
    };
    const bubble = (item, words) => {
      const msg = document.createElement('div');
      msg.className = 'chat-msg ' + (item.you ? 'you' : 'rudra');
      msg.innerHTML = item.html;
      if (words) { // reserve the final size now; the words fade in one by one
        const p = msg.querySelector('p');
        p.textContent = '';
        item.text.split(/(\s+)/).forEach(part => {
          if (/^\s+$/.test(part) || !part) { p.append(part); return; }
          const word = document.createElement('span'); word.className = 'w'; word.textContent = part; p.append(word);
        });
      }
      return msg;
    };
    const play = async () => {
      if (playing) return; playing = true;
      await loadOrb().then(() => { orb = orb || window.StrandsOrb.create(win.querySelector('[data-assistant-orb]')); }).catch(() => {});
      thread.replaceChildren(); setState('idle');
      for (;;) {
        await wait(900);
        for (let i = 0; i < chat.length; i++) {
          const item = chat[i];
          if (item.you) {
            setState('listening');
            win.classList.add('is-typing');
            for (const ch of item.text) { typed.textContent += ch; if (ch !== ' ') sound.key(); await wait(34 + Math.random() * 46); }
            await wait(420);
            send.classList.add('is-sent'); orb && orb.pulse(); sound.send();
            add(bubble(item, false));
            typed.textContent = ''; win.classList.remove('is-typing');
            await wait(240); send.classList.remove('is-sent');
            setState('thinking'); await wait(1300);
          } else {
            const msg = bubble(item, true); add(msg); setState('speaking'); sound.chime();
            for (const word of msg.querySelectorAll('.w')) {
              word.classList.add('on'); sound.tick();
              orb && orb.setProps({ amplitude: 1.4 + Math.random() * 0.8, intensity: 0.4 + Math.random() * 0.22, speed: 0.2 + Math.random() * 0.05 });
              await wait(95 + Math.random() * 70);
            }
            await wait(500); setState('idle'); await wait(2400);
          }
        }
        await wait(2600);
        await thread.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 700, easing: 'ease', fill: 'forwards' }).finished.catch(() => {});
        thread.replaceChildren(); thread.getAnimations().forEach(animation => animation.cancel());
      }
    };
    new IntersectionObserver(entries => {
      inView = entries[entries.length - 1].isIntersecting;
      if (inView && !motion.matches) play();
      else if (inView && !orb) loadOrb().then(() => { orb = window.StrandsOrb.create(win.querySelector('[data-assistant-orb]')); }).catch(() => {});
      sound.active(visible());
      resume();
    }, { threshold: 0.3 }).observe(win);
    document.addEventListener('visibilitychange', () => { sound.active(visible()); resume(); });
  });

  // Smoothly grow or shrink a container from its previous height to its new one.
  const easeHeight = (element, before) => {
    const after = element.offsetHeight;
    if (Math.abs(after - before) < 3) return;
    element.getAnimations().forEach(animation => { if (animation.id === 'ease-height') animation.cancel(); });
    element.style.overflow = 'clip';
    const animation = element.animate([{ height: before + 'px' }, { height: after + 'px' }], { duration: 560, easing: 'cubic-bezier(.22,1,.36,1)' });
    animation.id = 'ease-height';
    animation.finished.then(() => { element.style.overflow = ''; }, () => {});
  };

  // Tabs have immediate state changes; their new content animates without blocking input.
  all('[data-tabs]').forEach(group => {
    const tabs = all('[data-tab]', group);
    const panels = all('[data-panel]', group);
    const list = group.querySelector('[data-tablist]');
    if (!tabs.length || !panels.length || !list) return;
    list.setAttribute('role', 'tablist');
    // A single pill slides between tabs; the panel area eases to its new height instead of jumping.
    const indicator = document.createElement('span');
    indicator.className = 'tab-indicator';
    indicator.setAttribute('aria-hidden', 'true');
    list.prepend(indicator);
    let current = null, firstRun = true;
    const placeIndicator = () => {
      if (!current) return;
      indicator.style.setProperty('--x', current.offsetLeft + 'px');
      indicator.style.setProperty('--y', current.offsetTop + 'px');
      indicator.style.setProperty('--w', current.offsetWidth + 'px');
      indicator.style.setProperty('--h', current.offsetHeight + 'px');
    };
    if ('ResizeObserver' in window) new ResizeObserver(placeIndicator).observe(list);
    const activate = (selected, focus = false) => {
      const before = group.offsetHeight;
      current = selected;
      tabs.forEach(tab => {
        const active = tab === selected;
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
      });
      panels.forEach(panel => {
        const active = panel.dataset.panel === selected.dataset.tab;
        panel.hidden = !active;
        panel.classList.remove('is-entering');
        if (active && !motion.matches) {
          // Restart the CSS animation without timers or obsolete pending panel changes.
          panel.getAnimations().forEach(animation => animation.cancel());
          panel.classList.add('is-entering');
        }
      });
      const status = group.querySelector('[data-tab-status]');
      if (status) status.textContent = selected.dataset.status || selected.textContent.trim();
      if (focus) selected.focus();
      placeIndicator();
      if (!firstRun && !motion.matches) easeHeight(group, before);
      firstRun = false;
    };
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      const panel = panels.find(item => item.dataset.panel === tab.dataset.tab);
      if (panel) {
        tab.setAttribute('aria-controls', panel.id);
        panel.setAttribute('role', 'tabpanel');
        panel.setAttribute('aria-labelledby', tab.id);
        panel.tabIndex = 0;
      }
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); activate(tabs[next], true); }
      });
    });
    activate(tabs.find(tab => tab.getAttribute('aria-selected') === 'true') || tabs[0]);
  });

  // App preview: a working copy of the app's sidebar. Some screens are live demos, others are preview-only.
  all('[data-app-shell]').forEach(shell => {
    const crumb = shell.querySelector('[data-app-crumb]');
    const main = shell.querySelector('.app-main');
    const views = all('.app-view', shell);
    const navItems = all('.app-nav-item', shell);
    const collapse = shell.querySelector('[data-app-collapse]');
    const sidebar = shell.querySelector('.app-sidebar');
    const setCollapsed = collapsed => {
      shell.classList.toggle('is-collapsed', collapsed);
      collapse.setAttribute('aria-expanded', String(!collapsed));
      collapse.setAttribute('aria-label', collapsed ? 'Expand sidebar' : 'Collapse sidebar');
      sidebar.inert = mobileLayout.matches && collapsed;
      main.inert = mobileLayout.matches && !collapsed;
    };
    setCollapsed(mobileLayout.matches);
    mobileLayout.addEventListener('change', () => setCollapsed(mobileLayout.matches));
    shell.addEventListener('keydown', event => {
      if (event.key === 'Escape' && mobileLayout.matches && !shell.classList.contains('is-collapsed')) {
        setCollapsed(true); collapse.focus();
      }
    });
    document.addEventListener('click', event => {
      if (mobileLayout.matches && !sidebar.contains(event.target) && !collapse.contains(event.target)) setCollapsed(true);
    });
    let fromNav = false;
    const show = name => {
      const before = main.offsetHeight;
      views.forEach(view => {
        const on = view.dataset.view === name;
        if (view.hidden !== on) return; // already in the right state
        view.hidden = !on;
        if (on && !motion.matches) {
          view.classList.remove('is-entering');
          void view.offsetWidth; // restart the entrance animation
          view.classList.add('is-entering');
        }
      });
      if (!motion.matches) easeHeight(main, before);
    };
    const select = item => {
      navItems.forEach(other => { if (other === item) other.setAttribute('aria-current', 'true'); else other.removeAttribute('aria-current'); });
      if (item) crumb.textContent = item.querySelector('span').textContent;
    };
    navItems.forEach(item => item.addEventListener('click', () => {
      select(item);
      if (mobileLayout.matches) { setCollapsed(true); collapse.focus({ preventScroll: true }); }
      if (item.dataset.appView) { show(item.dataset.appView); return; }
      show('workflow');
      fromNav = true;
      shell.querySelector('[data-tab="' + item.dataset.tabTarget + '"]')?.click();
      fromNav = false;
    }));
    // Using the tabs directly keeps the sidebar highlight in step.
    all('[data-tab]', shell).forEach(tab => tab.addEventListener('click', () => {
      if (!fromNav) select(navItems.find(item => item.dataset.tabTarget === tab.dataset.tab));
    }));
    shell.querySelector('.app-run')?.addEventListener('click', () => {
      navItems.find(item => item.textContent.trim() === 'Run Agent')?.click();
    });
    collapse?.addEventListener('click', () => {
      setCollapsed(!shell.classList.contains('is-collapsed'));
    });
  });

  all('[data-lead-open]').forEach(button => button.addEventListener('click', () => {
    const group = button.closest('[data-lead-demo]');
    group.querySelector('[data-lead-detail]').textContent = button.dataset.leadOpen;
    all('[data-lead-open]', group).forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  }));
  const samples = {
    email: { meta: 'Email draft · Review before sending', copy: 'Subject: Housekeeping support for Oakfield Suites\n\nHello,\n\nWe provide housekeeping support for hospitality teams. I would like to understand whether Oakfield Suites is reviewing its staffing needs.\n\nWould a short conversation next week be useful?\n\nThank you,\nYour team' },
    whatsapp: { meta: 'WhatsApp draft · Review before sending', copy: 'Hello, this is your service team. We help hotels with housekeeping staffing. Is there a suitable person at Oakfield Suites we could speak with about your current needs?\n\nWe can share a short company introduction if it would be helpful.' },
    call: { meta: 'Call script · Preparation only', copy: 'Introduction\nHello, I am calling from your service team. Is this a convenient time for a short conversation?\n\nAsk\nAre you reviewing housekeeping or staffing support for your property?\n\nNext step\nIf there is a fit, ask permission to share a company introduction and agree on a follow-up time.' }
  };
  all('[data-channel]').forEach(button => button.addEventListener('click', () => {
    const group = button.closest('[data-draft-demo]');
    const selected = samples[button.dataset.channel];
    group.querySelector('[data-draft-meta]').textContent = selected.meta;
    group.querySelector('[data-draft-copy]').textContent = selected.copy;
    all('[data-channel]', group).forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  }));
  all('[data-crm-demo]').forEach(group => {
    const card = group.querySelector('[data-deal]');
    const columns = all('[data-stage]', group);
    const button = group.querySelector('[data-move-deal]');
    const status = group.querySelector('[data-crm-status]');
    let stage = 0;
    button.addEventListener('click', () => {
      stage = (stage + 1) % columns.length;
      columns[stage].append(card);
      columns.forEach((column, index) => column.querySelector('[data-count]').textContent = index === stage ? '1' : '0');
      card.querySelector('.tag').textContent = ['Ready to review', 'Contact attempted', 'Follow-up needed'][stage];
      button.textContent = ['Move to Contacted', 'Move to Follow-up', 'Reset sample'][stage];
      status.textContent = 'Sample moved to ' + columns[stage].dataset.stage + '.';
    });
  });
  all('[data-export-sample]').forEach(button => button.addEventListener('click', () => {
    const data = 'Company,Category,Area,Data type\r\nOakfield Suites,Hotel,Delhi,Fictional demo\r\nWillow Care Centre,Healthcare,Noida,Fictional demo\r\nCedar Business Park,Offices,Gurugram,Fictional demo\r\n';
    const url = URL.createObjectURL(new Blob([data], { type: 'text/csv;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url; link.download = 'rudra24-fictional-sample.csv';
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }));
  all('[data-candidate-filter]').forEach(button => button.addEventListener('click', () => {
    const group = button.closest('[data-candidate-demo]');
    const role = button.dataset.candidateFilter;
    all('[data-candidate-role]', group).forEach(card => card.hidden = role !== 'all' && card.dataset.candidateRole !== role);
    all('[data-candidate-filter]', group).forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    group.querySelector('[data-candidate-status]').textContent = role === 'all' ? '3 fictional candidates shown.' : '1 fictional ' + role + ' candidate shown.';
  }));

  const form = document.querySelector('[data-contact-form]');
  if (form) {
    form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const values = new FormData(form);
    const name = String(values.get('name') || '').trim();
    const business = String(values.get('business') || '').trim();
    const interest = String(values.get('interest') || 'a product walkthrough');
    const message = String(values.get('message') || '').trim();
    const text = 'Hi, I would like to know more about Rudra24 AI.' + (name ? '\nMy name is ' + name + '.' : '') + (business ? '\nBusiness: ' + business : '') + '\nI am interested in ' + interest + '.' + (message ? '\n\n' + message : '');
    const draftLink = form.querySelector('[data-prepared-enquiry]');
    draftLink.href = 'https://wa.me/919999881949?text=' + encodeURIComponent(text);
    draftLink.hidden = false;
    form.querySelector('[data-enquiry-status]').textContent = 'Your enquiry is ready. Open WhatsApp, review it, then send when you are ready.';
    draftLink.focus();
    });
    // Disabled HTML defaults prevent native implicit submission without JS.
    form.querySelector('[data-contact-fields]').disabled = false;
  }

  // Media interactions are isolated in media.js.

  // Scroll reveals: blocks on the left glide in from the left, on the right from the right,
  // full-width blocks rise. Cards sharing a row arrive one after another (left → right).
  // Scroll-linked where supported (Chrome, Edge, Safari 26); a one-time spring glide elsewhere.
  // Once a block has fully arrived its animation is removed, so text renders as plain, crisp page text.
  const reveals = all('.reveal');
  const scrollLinked = window.CSS && CSS.supports('animation-timeline: view()');
  const motionClass = scrollLinked ? 'scroll-reveal' : 'motion-ready';
  const measure = () => {
    const vw = window.innerWidth, vh = window.innerHeight, rows = new Map();
    const travel = Math.round(Math.max(72, Math.min(vw * 0.11, 160)));
    reveals.forEach(element => {
      // Resting position = drawn position minus whatever slide is currently applied.
      const box = element.getBoundingClientRect();
      const [tx = 0, ty = 0] = (getComputedStyle(element).translate || '').split(' ').map(parseFloat).map(n => n || 0);
      const r = { left: box.left - tx, top: box.top - ty, width: box.width, height: box.height };
      const center = r.left + r.width / 2;
      const side = vw < 760 || r.width > vw * 0.62 ? 'center' : center < vw * 0.47 ? 'left' : center > vw * 0.53 ? 'right' : 'center';
      element.dataset.side = side;
      element.style.setProperty('--travel', travel + 'px');
      element.classList.toggle('reveal-tall', r.height > vh * 0.6);
      const key = element.parentElement && Math.round(r.top + window.scrollY);
      if (!rows.has(key)) rows.set(key, []);
      rows.get(key).push([r.left, element]);
    });
    rows.forEach(row => row.sort((a, b) => a[0] - b[0]).forEach(([, element], index) => {
      element.style.setProperty('--stagger', Math.min(index, 3));
    }));
  };
  if (reveals.length && 'IntersectionObserver' in window) {
    measure();
    if (!motion.matches) root.classList.add(motionClass);
    let measureFrame = 0;
    const remeasure = () => { cancelAnimationFrame(measureFrame); measureFrame = requestAnimationFrame(measure); };
    window.addEventListener('resize', remeasure);
    window.addEventListener('load', remeasure); // fonts and posters can shift layout after first paint
    document.addEventListener('toggle', remeasure, true); // opening a card reflows the grid
    if ('ResizeObserver' in window) { const sizes = new ResizeObserver(remeasure); reveals.forEach(element => sizes.observe(element)); }
    if (scrollLinked) {
      let settleFrame = 0;
      const settle = () => {
        settleFrame = 0;
        reveals.forEach(element => {
          if (element.classList.contains('settled')) return;
          const animations = element.getAnimations();
          if (animations.length && animations.every(animation => (animation.effect.getComputedTiming().progress ?? 0) >= 1)) element.classList.add('settled');
        });
      };
      window.addEventListener('scroll', () => { if (!settleFrame) settleFrame = requestAnimationFrame(settle); }, { passive: true });
    } else {
      const observer = new IntersectionObserver(entries => entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
      }), { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
      reveals.forEach(element => observer.observe(element));
    }
    motion.addEventListener('change', () => {
      root.classList.toggle(motionClass, !motion.matches);
      if (motion.matches) reveals.forEach(element => element.classList.add('visible'));
    });
  }
})();
