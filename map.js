/* Live maps — the same MapLibre engine, street style (OpenFreeMap "liberty") and satellite layer as the app.
   The engine (~1 MB) loads only when a map is about to scroll into view. Businesses on the lead map are fictional. */
(() => {
  'use strict';
  const roots = [...document.querySelectorAll('[data-lead-map], [data-visit-map]')];
  if (!roots.length) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const STREETS = 'https://tiles.openfreemap.org/styles/liberty';
  const SATELLITE = {
    version: 8,
    sources: { imagery: { type: 'raster', tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'], tileSize: 256, maxzoom: 19, attribution: 'Imagery © Esri, Maxar, Earthstar Geographics' } },
    layers: [{ id: 'satellite', type: 'raster', source: 'imagery', paint: { 'raster-fade-duration': 180 } }]
  };
  const escapeHtml = text => String(text).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
  const mapsLink = (lat, lng) => 'https://www.google.com/maps/search/?api=1&query=' + lat + ',' + lng;
  const ms = value => (reduced.matches ? 0 : value);

  let engine = null;
  const loadEngine = () => {
    if (window.maplibregl) return Promise.resolve(window.maplibregl);
    if (engine) return engine;
    engine = new Promise((resolve, reject) => {
      const css = document.createElement('link');
      css.rel = 'stylesheet'; css.href = 'assets/vendor/maplibre/maplibre-gl.css';
      document.head.append(css);
      const script = document.createElement('script');
      script.src = 'assets/vendor/maplibre/maplibre-gl.js'; script.async = true;
      script.onload = () => (window.maplibregl ? resolve(window.maplibregl) : reject(new Error('engine')));
      script.onerror = () => { script.remove(); reject(new Error('engine')); };
      document.head.append(script);
    }).catch(error => { engine = null; throw error; });
    return engine;
  };

  const pinElement = kind => {
    const pin = document.createElement('button');
    pin.type = 'button';
    pin.className = 'map-pin kind-' + kind;
    pin.innerHTML = '<span></span>';
    return pin;
  };
  const newMap = (lib, container, options) => new lib.Map({
    container, style: STREETS, attributionControl: { compact: true },
    cooperativeGestures: true, // Ctrl/⌘ + scroll (or two fingers) to zoom, so the page keeps scrolling
    pixelRatio: Math.min(2, window.devicePixelRatio || 1), fadeDuration: 180, maxPitch: 65, ...options
  });
  const watchFailure = (map, el) => {
    // A plain timeout keeps the honest fallback visible if tiles never arrive.
    const deadline = setTimeout(() => el.classList.add('map-failed'), 15000);
    map.on('load', () => { clearTimeout(deadline); el.classList.add('map-ready'); el.classList.remove('map-failed'); });
    // Keep the credits as the small "i" button instead of a strip across the map (it opens on click).
    const collapse = () => el.querySelector('.maplibregl-ctrl-attrib')?.classList.remove('maplibregl-compact-show');
    map.once('load', collapse);
    map.once('idle', collapse);
  };

  // Map / Satellite / 3D — the same three views as the app, shared by both maps.
  const addBuildings = map => {
    if (!map.isStyleLoaded() || map.getLayer('buildings-3d')) return;
    const source = Object.entries(map.getStyle().sources).find(([, value]) => value.type === 'vector');
    if (!source) return;
    try {
      map.addLayer({ id: 'buildings-3d', type: 'fill-extrusion', source: source[0], 'source-layer': 'building', minzoom: 13.5,
        paint: { 'fill-extrusion-color': '#CBD3BA', 'fill-extrusion-height': ['coalesce', ['get', 'render_height'], 8], 'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], 0], 'fill-extrusion-opacity': 0.78 } });
    } catch (error) { /* tilted view still works without building heights */ }
  };
  const useViews = (root, map, focus, onStyle) => {
    let view = 'map';
    map.on('style.load', () => { if (onStyle) onStyle(view); if (view === '3d') addBuildings(map); });
    root.querySelectorAll('[data-map-view]').forEach(button => button.addEventListener('click', () => {
      const next = button.dataset.mapView;
      if (next === view) return;
      root.querySelectorAll('[data-map-view]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
      const wasSatellite = view === 'satellite';
      view = next;
      if (view === 'satellite') map.setStyle(SATELLITE);
      else if (wasSatellite) map.setStyle(STREETS);
      else if (view === '3d') addBuildings(map);
      else if (map.getLayer('buildings-3d')) map.removeLayer('buildings-3d');
      map.easeTo(view === '3d'
        ? { center: focus(), zoom: Math.max(map.getZoom(), 15), pitch: 55, bearing: -18, duration: ms(1100) }
        : { pitch: 0, bearing: 0, duration: ms(800) });
    }));
    return () => view;
  };

  // Visit us: our head-office pin. Clicking it raises a card with address, phone and email above the pin.
  const startVisit = async root => {
    const lib = await loadEngine();
    const point = [parseFloat(root.dataset.lng), parseFloat(root.dataset.lat)];
    const host = root.querySelector('[data-visit-canvas]');
    const card = root.querySelector('[data-visit-card]');
    const pin = root.querySelector('[data-visit-pin]');
    const map = newMap(lib, host, { center: point, zoom: 14.2 });
    map.addControl(new lib.NavigationControl({ visualizePitch: true }), 'bottom-right');
    watchFailure(map, root);
    const marker = document.createElement('div');
    marker.className = 'visit-marker';
    map.once('load', () => {
      marker.append(card, pin);
      new lib.Marker({ element: marker, anchor: 'bottom' }).setLngLat(point).addTo(map);
      map.easeTo({ center: point, offset: [0, 90], duration: 0 }); // pin sits low, leaving room for the card above it
    });
    const isOpen = () => marker.classList.contains('is-open');
    const toggle = open => {
      marker.classList.toggle('is-open', open);
      pin.setAttribute('aria-expanded', String(open));
      if (!open) return;
      // Glide the pin low enough that the whole card fits above it.
      const half = host.clientHeight / 2;
      const offset = Math.max(0, Math.min(half - 16, card.offsetHeight + pin.offsetHeight + 14 + 16 - half));
      map.easeTo({ center: point, offset: [0, offset], duration: ms(900) });
    };
    pin.addEventListener('click', event => { event.stopPropagation(); toggle(!isOpen()); });
    card.addEventListener('click', event => event.stopPropagation());
    card.querySelector('[data-visit-close]').addEventListener('click', () => { toggle(false); pin.focus(); });
    map.on('click', () => toggle(false));
    document.addEventListener('keydown', event => { if (event.key === 'Escape' && isOpen()) { toggle(false); if (marker.contains(document.activeElement)) pin.focus(); } });
    useViews(root, map, () => point);
  };

  const startLeadMap = async root => {
    const lib = await loadEngine();
    const leads = JSON.parse(root.dataset.leads);
    const el = root.querySelector('[data-map-canvas]');
    const status = root.querySelector('[data-map-status]');
    const items = [...root.querySelectorAll('[data-map-item]')];
    const routeText = root.querySelector('[data-map-route-text]');
    const canvas = document.createElement('div');
    canvas.className = 'map-gl';
    el.append(canvas);
    let filter = 'All', stops = [], view = () => 'map', popup = null;
    const map = newMap(lib, canvas, { center: [77.21, 28.6], zoom: 9.4 });
    map.addControl(new lib.NavigationControl({ visualizePitch: true }), 'bottom-right');
    watchFailure(map, el);

    const visible = i => filter === 'All' || leads[i].kind === filter;
    const card = (lead, i) => `<div class="map-card"><span class="map-card-kind">${escapeHtml(lead.kind)}</span><b>${escapeHtml(lead.name)}</b><small>${escapeHtml(lead.area)}</small><div class="map-card-actions"><button type="button" data-route-add="${i}"${stops.includes(i) ? ' disabled' : ''}>${stops.includes(i) ? 'Added to visit' : 'Add to visit'}</button><a href="${mapsLink(lead.lat, lead.lng)}" target="_blank" rel="noopener noreferrer">Open in Google Maps</a></div><em>Fictional sample business</em></div>`;
    const open = i => {
      popup?.remove();
      const lead = leads[i];
      popup = new lib.Popup({ offset: 18, closeButton: false, maxWidth: '260px', className: 'map-popup' })
        .setLngLat([lead.lng, lead.lat]).setHTML(card(lead, i)).addTo(map);
      items.forEach((item, n) => item.classList.toggle('is-active', n === i));
      popup.on('close', () => items[i].classList.remove('is-active'));
    };

    const markers = leads.map((lead, i) => {
      const pin = pinElement(lead.kind.toLowerCase());
      pin.setAttribute('aria-label', lead.name + ', ' + lead.area + ' (fictional sample)');
      pin.style.setProperty('--delay', (i * 70) + 'ms');
      pin.addEventListener('click', event => { event.stopPropagation(); open(i); });
      return new lib.Marker({ element: pin, anchor: 'center' }).setLngLat([lead.lng, lead.lat]).addTo(map);
    });

    const fit = animate => {
      const shown = leads.filter((_, i) => visible(i));
      if (!shown.length) return;
      const bounds = new lib.LngLatBounds();
      shown.forEach(lead => bounds.extend([lead.lng, lead.lat]));
      map.fitBounds(bounds, { padding: 64, maxZoom: 12.5, duration: animate ? ms(900) : 0 });
    };
    root.querySelectorAll('[data-map-filter]').forEach(button => button.addEventListener('click', () => {
      filter = button.dataset.mapFilter;
      root.querySelectorAll('[data-map-filter]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
      popup?.remove();
      markers.forEach((marker, i) => marker.getElement().classList.toggle('is-hidden', !visible(i)));
      items.forEach((item, i) => { item.parentElement.hidden = !visible(i); });
      const count = leads.filter((_, i) => visible(i)).length;
      status.textContent = count + (filter === 'All' ? ' sample businesses in Delhi NCR' : ' sample ' + filter.toLowerCase() + (count === 1 ? '' : 's') + ' shown');
      fit(true);
    }));
    items.forEach((item, i) => {
      item.addEventListener('click', () => {
        map.flyTo({ center: [leads[i].lng, leads[i].lat], zoom: view() === '3d' ? 15 : 13, duration: ms(1000), essential: true });
        open(i);
      });
      item.addEventListener('pointerenter', () => markers[i].getElement().classList.add('is-hot'));
      item.addEventListener('pointerleave', () => markers[i].getElement().classList.remove('is-hot'));
    });

    // Visit plan: straight-line distance between stops, in the order they were added.
    const km = (a, b) => {
      const rad = d => d * Math.PI / 180;
      const dLat = rad(b.lat - a.lat), dLng = rad(b.lng - a.lng);
      const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dLng / 2) ** 2;
      return 12742 * Math.asin(Math.sqrt(Math.min(1, h)));
    };
    const routeData = () => ({ type: 'FeatureCollection', features: stops.length > 1 ? [{ type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: stops.map(i => [leads[i].lng, leads[i].lat]) } }] : [] });
    const drawRoute = () => {
      if (!map.isStyleLoaded()) return;
      if (map.getSource('visit-route')) map.getSource('visit-route').setData(routeData());
      else {
        map.addSource('visit-route', { type: 'geojson', data: routeData() });
        map.addLayer({ id: 'visit-route', type: 'line', source: 'visit-route', layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': view() === 'satellite' ? '#FFFFEB' : '#034F46', 'line-width': 3, 'line-dasharray': [1.5, 2] } });
      }
    };
    const describeRoute = () => {
      root.classList.toggle('has-route', stops.length > 0);
      if (!stops.length) { routeText.textContent = 'Open a pin and choose “Add to visit” to plan a route.'; return; }
      let total = 0;
      for (let n = 1; n < stops.length; n++) total += km(leads[stops[n - 1]], leads[stops[n]]);
      routeText.textContent = stops.map(i => leads[i].name).join(' → ') + (stops.length > 1 ? ' · about ' + total.toFixed(1) + ' km in a straight line' : ' · add one more stop');
    };
    canvas.addEventListener('click', event => {
      const add = event.target.closest('[data-route-add]');
      if (!add) return;
      const i = Number(add.dataset.routeAdd);
      if (!stops.includes(i)) stops.push(i);
      add.textContent = 'Added to visit'; add.disabled = true;
      drawRoute(); describeRoute();
    });
    root.querySelector('[data-map-route-clear]').addEventListener('click', () => { stops = []; popup?.remove(); drawRoute(); describeRoute(); });

    view = useViews(root, map, () => (popup ? popup.getLngLat() : map.getCenter()), drawRoute);

    map.once('load', () => fit(false));
  };

  // Start each map only when it is about to scroll into view (no map traffic for visitors who never get there).
  const start = el => {
    el.classList.add('map-live');
    (el.matches('[data-lead-map]') ? startLeadMap(el) : startVisit(el)).catch(() => el.classList.add('map-failed'));
  };
  if (!('IntersectionObserver' in window)) { roots.forEach(start); return; }
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    observer.unobserve(entry.target);
    start(entry.target);
  }), { rootMargin: '500px 0px' });
  roots.forEach(el => observer.observe(el));
})();
