(() => {
  'use strict';
  const comparison = document.querySelector('[data-plan-comparison]');
  if (!comparison) return;
  // Leave features readable if matching pricing styles fail to load.
  if (getComputedStyle(comparison).getPropertyValue('--plans-layout-version').trim() !== '3') return;
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

  const grid = comparison.querySelector('.plan-grid');
  const cards = [...grid.querySelectorAll('.plan-card')];
  const picker = comparison.querySelector('[data-plan-picker]');
  const choices = [...picker.querySelectorAll('[data-plan-choice]')];
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const select = index => choices.forEach((choice, i) => choice.setAttribute('aria-pressed', String(i === index)));
  const showPlan = index => {
    select(index);
    const left = grid.scrollLeft + cards[index].getBoundingClientRect().left - grid.getBoundingClientRect().left;
    grid.scrollTo({ left, behavior: motion.matches ? 'auto' : 'smooth' });
  };
  choices.forEach((choice, index) => {
    choice.addEventListener('click', () => showPlan(index));
    choice.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? choices.length - 1
        : (index + (event.key === 'ArrowRight' ? 1 : -1) + choices.length) % choices.length;
      choices[next].focus();
      showPlan(next);
    });
  });
  let scrollTimer;
  const syncChoice = () => {
    const left = grid.getBoundingClientRect().left;
    let nearest = 0;
    cards.forEach((card, index) => {
      if (Math.abs(card.getBoundingClientRect().left - left) < Math.abs(cards[nearest].getBoundingClientRect().left - left)) nearest = index;
    });
    select(nearest);
  };
  grid.addEventListener('scroll', () => { clearTimeout(scrollTimer); scrollTimer = setTimeout(syncChoice, 120); }, { passive: true });
  grid.addEventListener('scrollend', syncChoice);
  picker.hidden = false;
  comparison.querySelector('.plans-swipe-hint').firstChild.textContent = 'Choose a plan or swipe to compare ';

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
