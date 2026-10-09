/* Paste this function into the browser console after changing viewport or demo view. */
function checkResponsiveLayout() {
  const failures = [];
  const width = document.documentElement.clientWidth;
  if (document.documentElement.scrollWidth > width + 1) failures.push('Page overflows horizontally');
  for (const element of document.querySelectorAll('.app-main,.app-view,.experience-workspace,.experience-fields,.contact-form,.demo-tabs,.visit-details')) {
    if (element.closest('details:not([open]),[hidden]')) continue;
    if (element.clientWidth && element.scrollWidth > element.clientWidth + 2) failures.push(element.className + ' clips content');
  }
  if (window.innerWidth <= 760) {
    for (const shell of document.querySelectorAll('[data-app-shell]')) {
      const closed = shell.classList.contains('is-collapsed');
      const sidebar = shell.querySelector('.app-sidebar');
      const main = shell.querySelector('.app-main');
      const toggle = shell.querySelector('[data-app-collapse]');
      if (toggle.getAttribute('aria-expanded') !== String(!closed)) failures.push('Sidebar state disagrees with toggle');
      if (sidebar.hasAttribute('inert') !== closed || main.hasAttribute('inert') === closed) failures.push('Hidden or covered preview accepts focus');
      if (main.clientWidth < shell.clientWidth - 2) failures.push('Sidebar squeezes phone content');
      if (toggle.getBoundingClientRect().height < 43.5) failures.push('Sidebar toggle is too small for touch'); // Allow subpixel rounding.
    }
    for (const field of document.querySelectorAll('input:not([type=checkbox]),select,textarea')) {
      if (field.closest('details:not([open]),[hidden]')) continue;
      if (field.getBoundingClientRect().width && +getComputedStyle(field).fontSize.replace('px', '') < 16) failures.push('Phone input would trigger zoom');
    }
  }
  if (failures.length) throw new Error(failures.join('; '));
  return { page: location.pathname, width: window.innerWidth, height: window.innerHeight, passed: true };
}
if (typeof module !== 'undefined') module.exports = checkResponsiveLayout;
