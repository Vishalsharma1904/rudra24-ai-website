/* Native playback; no live app requests. One decoder for all pointer previews. */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const film = document.querySelector('#launch-film');
  if (film) {
    const phoneLayout = matchMedia('(max-width: 760px)');
    const connection = navigator.connection;
    const constrained = Boolean(connection?.saveData || /^(slow-)?2g$/.test(connection?.effectiveType || ''));
    const toggle = document.querySelector('[data-film-toggle]');
    const expand = document.querySelector('[data-film-expand]');
    const status = document.querySelector('[data-film-status]');
    const dialog = document.querySelector('.film-dialog');
    const bounds = film.getBoundingClientRect();
    let inView = bounds.top < innerHeight && bounds.bottom > 0;
    let playRequested = false;
    let pausedByUser = false, hovering = false, audioBlocked = false, failed = false, lastScroll = 0;
    const mute = () => { film.muted = true; };
    const label = () => {
      toggle.textContent = film.paused ? (phoneLayout.matches ? 'Play' : 'Play video') : (phoneLayout.matches ? 'Pause' : 'Pause video');
      toggle.setAttribute('aria-label', film.paused ? 'Play product walkthrough' : 'Pause product walkthrough');
      toggle.setAttribute('aria-pressed', String(!film.paused));
      expand.textContent = phoneLayout.matches ? 'Full view' : 'Expand film';
    };
    const fail = () => {
      failed = true;
      status.hidden = false;
      status.textContent = 'The film could not load. Open the video directly, or read the feature overview below.';
      document.querySelector('[data-film-fallback]').hidden = false;
      toggle.disabled = expand.disabled = true;
    };
    const quietPlay = () => {
      mute();
      if (failed || pausedByUser || document.hidden || (!inView && !dialog.open) || (constrained && !playRequested)) return;
      film.play().catch(error => {
        if (error.name === 'NotSupportedError') fail();
        else if (error.name !== 'AbortError') label();
      });
    };
    const audiblePlay = () => {
      playRequested = true;
      film.muted = false;
      film.play().catch(error => {
        if (error.name === 'NotSupportedError') { fail(); return; }
        audioBlocked = true;
        quietPlay();
      });
    };
    // Serve the film pre-scaled (Lanczos) to the size it is actually drawn at, so the browser
    // never has to shrink 1920px footage itself — its quick downscale is what blurs small UI text.
    const sizes = [640, 960, 1280, 1920];
    let filmSize = 0;
    const sizeFor = width => phoneLayout.matches && !dialog.open ? 640 : sizes.find(size => size >= width * (window.devicePixelRatio || 1)) || 1920;
    const useSize = size => {
      const mobile = phoneLayout.matches && !dialog.open;
      const source = mobile ? 'assets/video/launch-mobile.mp4' : 'assets/video/launch-film' + (size === 1920 ? '' : '-' + size) + '.mp4';
      if (source === film.getAttribute('src')) return;
      if (!mobile && size <= filmSize && !film.getAttribute('src')?.includes('launch-mobile')) return;
      const time = film.currentTime, playing = !film.paused;
      filmSize = size;
      film.src = source;
      film.addEventListener('loadedmetadata', () => { if (time) film.currentTime = time; if (playing) quietPlay(); }, { once: true });
    };
    if (phoneLayout.matches) film.poster = 'assets/video/launch-mobile-poster.jpg';
    useSize(sizeFor(film.clientWidth || 640));
    window.addEventListener('resize', () => {
      film.poster = phoneLayout.matches ? 'assets/video/launch-mobile-poster.jpg' : 'assets/video/launch-poster.jpg';
      useSize(sizeFor(film.clientWidth)); label();
    });
    const DEMO_START = 19.5; // the logo/title intro is already on the page; open on the product
    film.loop = false;
    const toDemo = () => { if (film.currentTime < DEMO_START - 0.5) film.currentTime = DEMO_START; };
    film.addEventListener('loadedmetadata', toDemo);
    film.addEventListener('ended', () => { film.currentTime = DEMO_START; if (!pausedByUser) film.play().catch(() => {}); });
    if (film.readyState >= 1) toDemo();
    film.controls = false;
    film.muted = true;
    document.querySelector('#film-hint').textContent = fine.matches
      ? 'The workspace in action · Hover for sound'
      : 'Tap video for sound';
    film.autoplay = !reduced.matches && !constrained;
    if (reduced.matches || constrained) {
      film.autoplay = false; film.pause(); label();
      document.querySelector('#film-hint').textContent = 'Play when you’re ready';
    }
    else quietPlay();
    label();
    // Pause playback when the walkthrough leaves the viewport.
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => {
        inView = entries[0].isIntersecting;
        if (!inView && !dialog.open) { mute(); film.pause(); }
        else if (!reduced.matches || playRequested) quietPlay();
      }, { threshold: 0.03, rootMargin: '60px 0px' }).observe(film.closest('.launch-media'));
    }
    // Sound follows the cursor: on while the pointer rests on the film, off when it leaves; the film keeps playing.
    // Browsers only allow sound after the visitor has clicked or pressed a key somewhere on the page once.
    let pointerX = -1, pointerY = -1;
    const overFilm = () => pointerX >= 0 && document.elementFromPoint(pointerX, pointerY) === film;
    const trySound = () => {
      if (fine.matches && hovering && film.muted && !audioBlocked && !film.paused && !pausedByUser) audiblePlay();
    };
    film.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse') return;
      hovering = true;
      if (Date.now() - lastScroll > 250) trySound();
    });
    film.addEventListener('pointermove', () => { if (Date.now() - lastScroll > 250) trySound(); });
    film.addEventListener('pointerleave', () => { hovering = false; if (fine.matches) mute(); });
    document.addEventListener('pointermove', event => { pointerX = event.clientX; pointerY = event.clientY; }, { passive: true });
    document.addEventListener('scroll', () => {
      lastScroll = Date.now();
      // Only silence the film once it has scrolled out from under the cursor.
      if (!overFilm()) { hovering = false; mute(); }
    }, { passive: true, capture: true });
    const unlock = event => {
      if (!event.isTrusted) return;
      audioBlocked = false;
      if (event.target !== film) trySound();
    };
    document.addEventListener('pointerdown', unlock, true);
    document.addEventListener('keydown', unlock, true);
    const gestureSound = () => {
      if (!film.muted) { mute(); return; }
      pausedByUser = false;
      playRequested = true;
      audioBlocked = false;
      audiblePlay();
    };
    film.addEventListener('click', gestureSound);
    film.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); gestureSound(); }
    });
    // Move the same original-resolution player; never run two copies with audio.
    const home = document.createComment('launch film position');
    film.before(home);
    expand.addEventListener('click', () => {
      mute(); dialog.showModal(); window.lenis?.stop(); dialog.querySelector('[data-film-slot]').append(film); useSize(sizeFor(film.clientWidth));
      film.controls = phoneLayout.matches;
      if (!pausedByUser && !reduced.matches) quietPlay();
      dialog.querySelector('[data-film-close]').focus();
    });
    document.querySelector('[data-film-close]').addEventListener('click', () => dialog.close());
    dialog.addEventListener('close', () => {
      window.lenis?.start();
      mute(); home.after(film); film.controls = false; useSize(sizeFor(film.clientWidth)); if (!pausedByUser && (!reduced.matches || playRequested)) quietPlay(); expand.focus();
    });
    dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
    toggle.addEventListener('click', () => {
      pausedByUser = !film.paused;
      if (pausedByUser) { mute(); film.pause(); }
      else { playRequested = true; quietPlay(); }
      label();
    });
    film.addEventListener('play', label);
    film.addEventListener('pause', () => {
      label();
      // Safari can pause an autoplaying film when hover attempts to unmute it.
      if (!film.muted && !pausedByUser && !document.hidden) {
        audioBlocked = true; quietPlay();
      }
    });
    film.addEventListener('error', fail);
    document.addEventListener('visibilitychange', () => {
      mute();
      if (document.hidden) film.pause();
      else if (!reduced.matches) quietPlay();
    });
    reduced.addEventListener('change', () => {
      mute();
      if (reduced.matches) film.pause(); else quietPlay();
    });
  }

  // Where each short clip's own scene begins (a few clips open on the tail of the previous scene).
  const CLIP_START = { crm: 2, assistant: 4 };

  // Feature-page clips: no player bar; they play silently while on screen, pause when scrolled away,
  // loop from the right scene, and light up the "what happens" steps beside them as they go.
  document.querySelectorAll('[data-clip-player]').forEach(figure => {
    const video = figure.querySelector('video');
    const key = figure.dataset.clip;
    const start = Number(figure.dataset.start) || 0;
    const toggle = figure.querySelector('[data-clip-toggle]');
    const bar = figure.querySelector('.film-progress i');
    const section = figure.closest('.feature-film');
    const steps = [...section.querySelectorAll('.film-moments li')];
    let pausedByUser = false, inView = false;
    video.controls = false;
    video.loop = false;
    video.removeAttribute('autoplay');
    // The 960px Lanczos copy is sharper than the browser shrinking the 1920px file when that is all the screen shows.
    const source = video.querySelector('source')?.getAttribute('src');
    if (source && figure.clientWidth * (window.devicePixelRatio || 1) <= 980) video.src = source.replace('.mp4', '-preview.mp4');
    const play = () => { if (!pausedByUser && inView && !reduced.matches && !document.hidden) video.play().catch(() => {}); };
    const label = () => { toggle.textContent = video.paused ? 'Play' : 'Pause'; figure.classList.toggle('is-playing', !video.paused); };
    const toStart = () => { if (video.currentTime < start - 0.3) video.currentTime = start; };
    video.addEventListener('loadedmetadata', toStart);
    if (video.readyState >= 1) toStart();
    video.addEventListener('ended', () => { video.currentTime = start; play(); });
    video.addEventListener('play', label);
    video.addEventListener('pause', label);
    video.addEventListener('timeupdate', () => {
      const span = Math.max(0.1, (video.duration || 10) - start);
      bar.style.transform = 'scaleX(' + Math.min(1, Math.max(0, (video.currentTime - start) / span)) + ')';
      let current = 0;
      steps.forEach((step, i) => { if (video.currentTime >= Number(step.dataset.at) - 0.05) current = i; });
      steps.forEach((step, i) => step.classList.toggle('is-current', i === current));
    });
    toggle.addEventListener('click', () => {
      pausedByUser = !video.paused;
      if (pausedByUser) video.pause(); else { inView = true; play(); }
    });
    video.addEventListener('click', () => toggle.click());
    // Click a step to jump to that moment.
    section.querySelectorAll('[data-clip-seek]').forEach(button => button.addEventListener('click', () => {
      video.currentTime = Number(button.dataset.clipSeek);
      pausedByUser = false; inView = true; play();
    }));
    new IntersectionObserver(entries => entries.forEach(entry => {
      inView = entry.isIntersecting;
      if (inView) play(); else video.pause();
    }), { threshold: 0.35 }).observe(figure);
    document.addEventListener('visibilitychange', () => { if (document.hidden) video.pause(); else play(); });
    reduced.addEventListener('change', () => { if (reduced.matches) video.pause(); else play(); });
    label();
  });

  const cards = [...document.querySelectorAll('[data-feature-clip]')];
  if (!cards.length) return;
  // One floating preview with a stacked, preloaded clip per feature: hover shows instantly and
  // moving between cards crossfades instead of reloading. Files are pre-scaled to the exact
  // pixel size the preview needs (480 CSS px × screen density) so text is not smeared by the browser.
  const preview = document.createElement('div');
  preview.className = 'feature-hover';
  preview.setAttribute('aria-hidden', 'true');
  preview.innerHTML = '<div class="feature-hover-stack"></div><p></p>';
  document.body.append(preview);
  const stack = preview.querySelector('.feature-hover-stack');
  const caption = preview.querySelector('p');
  const clips = new Map();
  const clipFor = key => {
    if (clips.has(key)) return clips.get(key);
    const video = document.createElement('video');
    video.muted = true; video.loop = false; video.playsInline = true; video.preload = 'auto';
    video.poster = 'assets/video/' + key + '-poster.jpg';
    // Pick the file by the pixels the preview really needs (its CSS width × screen density).
    const need = (preview.offsetWidth || 560) * (window.devicePixelRatio || 1);
    video.src = 'assets/video/' + key + (need > 500 ? '-preview.mp4' : '-preview-480.mp4');
    const start = CLIP_START[key] || 0;
    video.addEventListener('ended', () => { video.currentTime = start; if (video === shown && active) video.play().catch(() => {}); });
    video.addEventListener('error', () => video.classList.add('failed'));
    stack.append(video); clips.set(key, video);
    return video;
  };
  let active = null, shown = null, frame = 0, x = 0, y = 0, targetX = 0, targetY = 0, lastTime = 0;
  let pointerX = -1, pointerY = -1, hideTimer = 0;
  const dpr = () => window.devicePixelRatio || 1;
  const move = time => {
    const blend = 1 - Math.exp(-Math.min(time - (lastTime || time - 16), 40) / 110);
    lastTime = time;
    x += (targetX - x) * blend; y += (targetY - y) * blend;
    // Snap to whole device pixels: a video drawn at a fractional offset is resampled and looks soft.
    preview.style.setProperty('--preview-x', Math.round(x * dpr()) / dpr() + 'px');
    preview.style.setProperty('--preview-y', Math.round(y * dpr()) / dpr() + 'px');
    frame = active && Math.abs(targetX - x) + Math.abs(targetY - y) > .3 ? requestAnimationFrame(move) : 0;
    if (!frame) lastTime = 0;
  };
  const aim = () => {
    const width = preview.offsetWidth || 480, height = preview.offsetHeight || 300;
    targetX = Math.max(16, Math.min(pointerX + 24, innerWidth - width - 16));
    targetY = Math.max(16, Math.min(pointerY - height - 24, innerHeight - height - 16));
    if (!frame) frame = requestAnimationFrame(move);
  };
  const show = card => {
    clearTimeout(hideTimer); hideTimer = 0;
    if (card === active) return;
    const wasVisible = !!active;
    active = card;
    const video = clipFor(card.dataset.featureClip);
    if (shown !== video) {
      if (shown) shown.classList.remove('current');
      const previous = shown; shown = video;
      if (previous) setTimeout(() => { if (previous !== shown) previous.pause(); }, 420);
      video.currentTime = CLIP_START[card.dataset.featureClip] || 0;
      video.play().catch(() => {}); // the poster stays visible if playback is unavailable
      video.classList.add('current');
    }
    caption.textContent = card.querySelector('.card-category').textContent + ' · Inside the app';
    aim();
    if (!wasVisible) { x = targetX; y = targetY; move(performance.now()); }
    preview.classList.add('active');
  };
  const hide = () => {
    clearTimeout(hideTimer); hideTimer = 0;
    active = null; preview.classList.remove('active');
    if (shown) { const last = shown; setTimeout(() => { if (!active) last.pause(); }, 320); }
    cancelAnimationFrame(frame); frame = 0; lastTime = 0;
  };
  // Short grace period so moving between neighbouring cards crossfades; repeated calls never extend it.
  const softHide = () => { if (!hideTimer) hideTimer = setTimeout(hide, 110); };
  const eligible = card => card && fine.matches && !reduced.matches && !card.closest('details')?.open;
  // Re-check what is under the pointer: works while the page scrolls under a still mouse.
  const sync = () => {
    if (pointerX < 0) return;
    const card = document.elementFromPoint(pointerX, pointerY)?.closest('[data-feature-clip]');
    if (eligible(card)) show(card); else if (active) softHide();
  };
  document.addEventListener('pointermove', event => {
    if (event.pointerType !== 'mouse') return;
    pointerX = event.clientX; pointerY = event.clientY;
    if (!active) return;
    if (event.target.closest?.('[data-feature-clip]')) aim(); else softHide();
  }, { passive: true });
  cards.forEach(card => {
    card.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse') return;
      pointerX = event.clientX; pointerY = event.clientY;
      if (eligible(card)) show(card);
    });
    card.addEventListener('pointerleave', softHide);
    card.addEventListener('click', hide);
  });
  let scrollFrame = 0;
  window.addEventListener('scroll', () => {
    if (scrollFrame) return;
    scrollFrame = requestAnimationFrame(() => { scrollFrame = 0; sync(); if (active) aim(); });
  }, { passive: true });
  document.documentElement.addEventListener('mouseleave', hide);
  window.addEventListener('resize', hide);
  document.addEventListener('keydown', event => { if (event.key === 'Escape') hide(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) hide(); });
  reduced.addEventListener('change', hide);
  fine.addEventListener('change', hide);
  // Warm the clips once the page is idle so the first hover is instant.
  const warm = () => { if (fine.matches && !reduced.matches) cards.forEach(card => clipFor(card.dataset.featureClip)); };
  if (document.readyState === 'complete') setTimeout(warm, 600); else window.addEventListener('load', () => setTimeout(warm, 600));
})();
