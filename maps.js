/* Same MapLibre runtime and public layers as the app; only fictional demonstration records. */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const samples = [
    {name:'Oakfield Suites',category:'Hotel',area:'Central Delhi',point:[77.216,28.635]},
    {name:'Willow Care Centre',category:'Healthcare',area:'Noida',point:[77.322,28.584]},
    {name:'Cedar Business Park',category:'Offices',area:'Gurugram',point:[77.081,28.459]}
  ];
  let engine = null;
  function loadEngine() {
    if (window.maplibregl) return Promise.resolve(window.maplibregl);
    if (engine) return engine;
    engine = new Promise((resolve,reject) => {
      if (!document.querySelector('[data-map-css]')) {
        const css=document.createElement('link');css.rel='stylesheet';css.href='assets/vendor/maplibre/maplibre-gl.css';css.dataset.mapCss='';document.head.append(css);
      }
      const script=document.createElement('script');script.src='assets/vendor/maplibre/maplibre-gl.js';script.async=true;
      script.onload=()=>window.maplibregl?resolve(window.maplibregl):reject(new Error('Map engine unavailable'));
      script.onerror=()=>{script.remove();reject(new Error('Map engine unavailable'));};
      document.head.append(script);
    }).catch(error=>{engine=null;throw error;});
    return engine;
  }
  const satellite = {
    version:8,
    sources:{imagery:{type:'raster',tiles:['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],tileSize:256,maxzoom:19,attribution:'Imagery © Esri, Maxar, Earthstar Geographics'}},
    layers:[{id:'satellite',type:'raster',source:'imagery',paint:{'raster-fade-duration':180}}]
  };
  const duration = () => reduced.matches?0:420;
  function distance(a,b) {
    const rad=v=>v*Math.PI/180;
    const dlat=rad(b[1]-a[1]),dlng=rad(b[0]-a[0]);
    const h=Math.sin(dlat/2)**2+Math.cos(rad(a[1]))*Math.cos(rad(b[1]))*Math.sin(dlng/2)**2;
    return 6371*2*Math.asin(Math.sqrt(Math.min(1,h)));
  }
  document.querySelectorAll('[data-map-demo]').forEach(root=>{
    const canvas=root.querySelector('.map-canvas'), loading=root.querySelector('[data-map-loading]');
    const loadButton=root.querySelector('[data-map-load]'), status=root.querySelector('[data-map-status]');
    const recordButtons=[...root.querySelectorAll('[data-map-record]')];
    const styleButtons=[...root.querySelectorAll('[data-map-style]')];
    const routeButton=root.querySelector('[data-map-route]');
    let map=null, initializing=false, selected=0, currentStyle='map', markers=[], popup=null, points=[], picking=false, deadline=0;
    let failureShown=false;
    const setStatus=message=>{status.textContent=message;};
    const updateRoute=()=>{
      if (!map?.isStyleLoaded()) return;
      const geo={type:'FeatureCollection',features:points.length===2?[{type:'Feature',properties:{},geometry:{type:'LineString',coordinates:points}}]:[]};
      if (map.getSource('demo-distance')) map.getSource('demo-distance').setData(geo);
      else {
        map.addSource('demo-distance',{type:'geojson',data:geo});
        map.addLayer({id:'demo-distance',type:'line',source:'demo-distance',paint:{'line-color':currentStyle==='satellite'?'#FFFFEB':'#034F46','line-width':3,'line-dasharray':[2,2]}});
      }
    };
    const selectRecord=(index,fly=true)=>{
      selected=index;
      const record=samples[index];
      recordButtons.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
      markers.forEach((marker,i)=>marker.getElement().setAttribute('aria-pressed',String(i===index)));
      const detail=root.querySelector('[data-map-detail]');
      detail.querySelector('b').textContent=record.name;
      detail.querySelector('span').textContent=record.category+' · '+record.area+'. Fictional business at a sample map location. Contact details are not real.';
      if (!map) return;
      popup?.remove();
      const box=document.createElement('div'), name=document.createElement('b'), body=document.createElement('span');
      name.textContent=record.name;body.textContent=record.category+' · '+record.area+' · Fictional demo';box.append(name,body);
      popup=new window.maplibregl.Popup({offset:24,closeButton:true,maxWidth:'260px'}).setLngLat(record.point).setDOMContent(box).addTo(map);
      if(fly)map.easeTo({center:record.point,zoom:12,pitch:currentStyle==='3d'?50:0,duration:duration()});
      setStatus('Selected '+record.name+' in '+record.area+'. Fictional sample record.');
    };
    const choosePoint=point=>{
      if(!picking)return;
      if(points.length===2)points=[];
      points.push(point);
      if(points.length===1)setStatus('A selected. Choose a second point on the map or a sample company for B.');
      else {
        picking=false;routeButton.setAttribute('aria-pressed','false');routeButton.textContent='Choose A → B';
        setStatus('A → B: '+distance(points[0],points[1]).toFixed(2)+' km straight-line distance. Road routes and journey time can differ.');
        updateRoute();
      }
    };
    const fail=()=>{
      if(!map)return;
      clearTimeout(deadline);failureShown=true;loading.hidden=false;
      loading.querySelector('span').textContent='Map tiles are unavailable right now.';
      loadButton.disabled=false;loadButton.textContent='Retry map';
      setStatus('Check your connection and retry. The sample company list remains available.');
    };
    const ready=()=>{
      if(!map || failureShown)return;
      clearTimeout(deadline);loading.hidden=true;loadButton.disabled=false;
      updateRoute();
      if(currentStyle==='3d')addBuildings();
      setStatus('Map ready. Select a company, drag to explore, or choose A → B. Use Ctrl + scroll to zoom.');
    };
    const addBuildings=()=>{
      if(!map?.isStyleLoaded() || map.getLayer('demo-buildings'))return;
      const style=map.getStyle();
      const source=Object.entries(style.sources).find(([,value])=>value.type==='vector');
      if(!source)return;
      try {
        map.addLayer({id:'demo-buildings',type:'fill-extrusion',source:source[0],'source-layer':'building',minzoom:14,paint:{'fill-extrusion-color':'#CBD3BA','fill-extrusion-height':['coalesce',['get','render_height'],8],'fill-extrusion-base':['coalesce',['get','render_min_height'],0],'fill-extrusion-opacity':.75}});
      } catch (_) {/* The tilted view is still usable if a layer omits building heights. */}
    };
    async function initialize() {
      if(initializing)return;
      if(map && !failureShown){map.resize();return;}
      initializing=true;failureShown=false;loadButton.disabled=true;
      loading.hidden=false;loading.querySelector('span').textContent='Opening your map…';
      loadButton.textContent='Loading…';
      try {
        const lib=await loadEngine();
        map?.remove();popup=null;markers=[];canvas.replaceChildren();
        map=new lib.Map({container:canvas,style:currentStyle==='satellite'?satellite:'https://tiles.openfreemap.org/styles/liberty',center:[77.207,28.576],zoom:9.6,pitch:currentStyle==='3d'?50:0,attributionControl:{compact:true},cooperativeGestures:true,pixelRatio:Math.min(2,devicePixelRatio||1),fadeDuration:180,maxPitch:65});
        map.addControl(new lib.NavigationControl({visualizePitch:true}),'bottom-right');
        samples.forEach((record,index)=>{
          const pin=document.createElement('button');pin.type='button';pin.className='map-pin';pin.textContent=String(index+1);pin.setAttribute('aria-label',record.name+' · '+record.area+' · Fictional sample');pin.setAttribute('aria-pressed',String(index===selected));
          pin.addEventListener('click',event=>{event.stopPropagation();if(picking)choosePoint(record.point);else selectRecord(index);});
          markers.push(new lib.Marker({element:pin,anchor:'center'}).setLngLat(record.point).addTo(map));
        });
        map.on('click',event=>{if(picking)choosePoint([event.lngLat.lng,event.lngLat.lat]);});
        map.on('style.load',()=>{failureShown=false;updateRoute();if(currentStyle==='3d')addBuildings();});
        map.on('load',ready);
        // A concrete timeout exposes a retry instead of claiming that an unloaded map is ready.
        deadline=setTimeout(fail,18000);
        map.on('error',event=>{if(event.error?.message?.includes('WebGL'))fail();});
      } catch (_) {
        loading.hidden=false;loading.querySelector('span').textContent='The interactive map could not open.';
        loadButton.disabled=false;loadButton.textContent='Retry map';failureShown=true;
        setStatus('The map needs network access and a WebGL-capable browser. Sample company details still work.');
      } finally {initializing=false;}
    }
    loadButton.addEventListener('click',initialize);
    recordButtons.forEach((button,index)=>button.addEventListener('click',()=>{
      if(picking)choosePoint(samples[index].point);else selectRecord(index);
      if(!map)initialize();
    }));
    styleButtons.forEach(button=>button.addEventListener('click',async()=>{
      currentStyle=button.dataset.mapStyle;
      styleButtons.forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
      if(!map){await initialize();return;}
      popup?.remove();
      if(currentStyle==='satellite')map.setStyle(satellite);
      else if(map.getStyle()?.sources?.imagery)map.setStyle('https://tiles.openfreemap.org/styles/liberty');
      else if(currentStyle==='3d')addBuildings();
      else if(map.getLayer('demo-buildings'))map.removeLayer('demo-buildings');
      map.easeTo({pitch:currentStyle==='3d'?50:0,bearing:currentStyle==='3d'?-18:0,duration:duration(),...(currentStyle==='3d'?{center:samples[selected].point,zoom:14.5}:{})});
      setStatus(currentStyle==='3d'?'Tilted 3D view. Drag to explore; building detail depends on available map data.':currentStyle==='satellite'?'Satellite imagery view. Sample company pins remain clickable.':'Street map view. Sample company pins remain clickable.');
    }));
    routeButton.addEventListener('click',()=>{
      if(!map)initialize();
      picking=!picking;points=[];updateRoute();
      routeButton.setAttribute('aria-pressed',String(picking));routeButton.textContent=picking?'Cancel A → B':'Choose A → B';
      setStatus(picking?'Choose A, then B on the map or from the company list. We show straight-line distance.':'Distance selection cancelled.');
    });
    root.querySelector('[data-map-reset]').addEventListener('click',()=>{
      picking=false;points=[];routeButton.setAttribute('aria-pressed','false');routeButton.textContent='Choose A → B';popup?.remove();updateRoute();
      map?.easeTo({center:[77.207,28.576],zoom:9.6,pitch:currentStyle==='3d'?50:0,bearing:0,duration:duration()});
      setStatus('View reset. Select any company to explore its sample location.');
    });
    const observer=new IntersectionObserver(entries=>{
      if(entries.some(entry=>entry.isIntersecting)){initialize();observer.unobserve(canvas);}
    },{rootMargin:'80px',threshold:.05});observer.observe(canvas);
    const resize=()=>{if(map && canvas.getClientRects().length)map.resize();};
    let resizeFrame=0;
    const queueResize=()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(resize);};
    new ResizeObserver(queueResize).observe(canvas);
    document.addEventListener('rudra:tab',queueResize);
    document.addEventListener('rudra:resize',queueResize);
    let placeholder=null,returnFocus=null;
    const dialog=document.createElement('dialog');dialog.className='map-dialog';dialog.setAttribute('aria-label','Expanded interactive lead map');
    const close=document.createElement('button');close.type='button';close.className='button secondary';close.textContent='Close expanded map';dialog.append(close);document.body.append(dialog);
    close.addEventListener('click',()=>dialog.close());
    const expandButton=root.querySelector('[data-map-fullscreen]');
    expandButton.addEventListener('click',()=>{
      returnFocus=document.activeElement;placeholder=document.createElement('div');placeholder.style.height=root.offsetHeight+'px';root.before(placeholder);
      expandButton.disabled=true;
      dialog.append(root);dialog.showModal();initialize();queueResize();close.focus();
    });
    dialog.addEventListener('close',()=>{placeholder?.replaceWith(root);placeholder=null;expandButton.disabled=false;queueResize();returnFocus?.focus();});
    dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
  });
})();
