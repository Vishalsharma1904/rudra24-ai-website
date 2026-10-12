(() => {
  'use strict';
  const comparison = document.querySelector('[data-plan-comparison]');
  if (!comparison) return;
  // Leave features readable if matching pricing styles fail to load.
  if (getComputedStyle(comparison).getPropertyValue('--plans-layout-version').trim() !== '2') return;
  const buttons = [...comparison.querySelectorAll('[data-plan-expand]')];
  const panels = [...comparison.querySelectorAll('.plan-feature-wrap')];
  let expanded = false;

  function setExpanded(next) {
    expanded = next;
    comparison.classList.toggle('features-expanded', next);
    for (const button of buttons) {
      button.setAttribute('aria-expanded', String(next));
      button.querySelector('[data-expand-label]').textContent = next
        ? 'Hide all features' : 'Show all features';
    }
    for (const panel of panels) {
      panel.inert = !next;
      panel.setAttribute('aria-hidden', String(!next));
    }
  }

  setExpanded(false);
  comparison.classList.add('features-ready');
  requestAnimationFrame(() => requestAnimationFrame(() => {
    comparison.classList.add('features-animated');
  }));
  for (const button of buttons) {
    button.hidden = false;
    button.addEventListener('click', () => setExpanded(!expanded));
  }
})();
