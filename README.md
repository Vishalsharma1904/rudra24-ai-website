# Rudra24 AI product website

Eight standalone HTML pages with local fonts, the actual app logo and the supplied launch film. No app/backend APIs, credentials, third-party player or provider calls are needed at runtime. Publish this folder, not the repository root.

## Local preview

From the repository root:

`py -3.12 marketing/website/tools/serve_site.py --port 4178`

Open `http://127.0.0.1:4178/index.html`. This optional localhost-only static server supports byte ranges for native MP4 seeking. Plain Python `http.server` lacks the needed range behaviour. Production static hosting should return `Accept-Ranges: bytes` and support `206 Partial Content` for MP4 files.

## Edit

- `site.css`: baseline responsive layout, local fonts and animation.
- `refinement.css`: warm-white palette, flat rounded cards, prominent capitalised brand and film treatment.
- `site.js`: sample interactions, menus, reveal animation and local enquiry preparation.
- `experience.js`: expandable feature cards, validated local searches, sample CRM/candidate data, editable drafts and CSV exports.
- `media.js`: muted autoplay, hover sound with policy fallback, pause control and one shared feature-hover preview.
- `tools/build_site.py`: shared markup and all eight page bodies. Run `py -3.12 marketing/website/tools/build_site.py` after editing; it rewrites the generated HTML pages.

Font licences are in `assets/fonts`. Figtree and EB Garamond match the app's Flow pairing. Preview surfaces use its Flow green preset: sidebar #034F46, canvas #FFFFEB. The original square app PNG is proportionally resized to 128px, preserving the mark. Essential descriptions and native navigation remain available without JavaScript.

## Included film

The supplied film is 211.7 seconds, 1920x1080 at 60fps, H.264 with stereo AAC audio. `assets/video/launch-film.mp4` is a lossless container remux with front-loaded metadata. Video/audio were not re-encoded and the original desktop file was not edited. `launch-poster.jpg` is a frame from the film.

The film sits directly on the page, with only its own corners rounded. It loops muted in its original 16:9 ratio. Pointer hover attempts sound; pointer leave or scroll mutes it without stopping playback. No separate sound-enabling control is shown. A trusted click/tap on the video (or Enter/Space) toggles sound when the browser requires a gesture. Hover alone cannot bypass browser autoplay rules. Expand film moves the same player into an accessible full-size dialog; Escape restores it without a second audio stream. An outside pause button remains available to keyboard and pointer users. Reduced-motion mode starts with a still poster; visitors can choose playback. Static HTML retains native controls without JavaScript. The film contains English on-screen captions; the feature overview is a readable product summary.

Five silent ten-second excerpts retain 1920x1080 at 60fps with CRF 18 encoding. Full-resolution posters replace smaller stills. The clips cover leads, calling, WhatsApp, CRM and the assistant. Feature cards share one pointer-following video preview, loaded on hover and paused on leave, scroll, resize, Escape or page hiding. Corresponding feature pages have native players and simple instructions, available to touch and keyboard users. The main film continues during ordinary scrolling and pauses in a hidden browser tab. Failed loads expose a direct MP4 link.

To replace the film, replace the media at the same paths or update `film_player()` and regenerate. Update posters, excerpts and readable descriptions to match. `tools/revise_media.py` prepares the current excerpts with ffmpeg, without modifying the source film.

## Contact and demo behaviour

Primary contact: +91 99998 81949 (Vishal Sharma). WhatsApp links open an enquiry for visitor review and sending. The Contact form prepares a link locally and requires a separate open action. Nothing is stored or submitted to this website. Fields are disabled by default to prevent accidental submission without JavaScript.

Twenty expandable product cards cover the app tabs. Native details provide descriptions without JavaScript; forms default to disabled. Lead and candidate forms validate role/industry, city, locality and count (1–20), stream deterministic fictional records, allow Stop with partial retention, and export safe CSV. The Data Hub and report totals reflect searches, saved CRM samples and planned follow-ups during this page visit. Drafts are editable. Assistant, voice and provider setup use prepared demonstrations. No live AI, real lead sourcing or new backend is connected; the user accepted a simulated experience, so the site remains standalone. Reloading clears demo state.

Lead, CRM, outreach and candidate previews use fictional records. Export produces a labelled fictional CSV. The website makes no calls, sends no messages and adds no analytics/cookies.

## Checks

`py -3.12 marketing/website/tools/check_site.py`

`py -3.12 marketing/website/tools/test_preview_server.py`

`node --check marketing/website/site.js`

`node --check marketing/website/media.js`

`node marketing/website/tools/check_experience.js`

Current evidence: `qa/verification-interactive.md`; desktop/mobile captures are in `qa/`. Earlier verification documents describe earlier designs. Static checks do not prove live app/provider behaviour.


## Maps retained after rollback — 9 October 2026

The original website design and behavior are restored. The map additions remain in `maps.css` and `maps.js`: the Lead map workspace tab, feature maps on Home/Product/Lead generation, and the office address map on all pages. Feature maps use the bundled MapLibre runtime and public map layers; sample business pins are fictional and A–B distance is straight-line. The office map uses the existing Sunita Vihar, Loni, Ghaziabad address.

## Maps, chapters and calmer scale — 9 October 2026 (evening)

- Home is organised into seven numbered chapters (Features, Live app preview, Lead map, AI assistant, How it works, Use cases, Questions) with a chapter bar under the hero. Each chapter has a label, a centred tagline, one plain line and Claude-style numbered explanations (`head()` and `points()` in `tools/build_site.py`).
- `map.js` is the single map script. It uses the app's MapLibre engine from `assets/vendor/maplibre` (loaded only when a map nears the screen), the OpenFreeMap "liberty" street style and Esri satellite imagery, with Map / Satellite / 3D views, industry filters, pin cards, Google Maps links and a visit-route planner. Head-office maps sit in the footer and on Contact. Ctrl + scroll zooms; the page keeps scrolling.
- `maps.js` and `maps.css` from the earlier map pass are no longer linked from any page and can be deleted. Leaflet is no longer used.

## Footer, email and feature films — 9 October 2026 (late)

- Every email link opens a Gmail compose window in the browser (not Outlook or another desktop mail app). Source pages may keep `mailto:`; `gmail_links()` in `tools/build_site.py` rewrites them when the pages are written.
- Footer: brand and our companies on the left, Explore and Stay in touch in the middle, head office with a larger map on the right.
- Feature films on Product, Lead generation, CRM and Outreach play silently by themselves when on screen, without a browser control bar. The text on the left explains the clip in three moments; click one to jump there. The video files were not changed; start offsets in `CLIPS` (build_site.py) and `CLIP_START` (media.js) skip the opening scene that belongs to another feature.
- Feature card labels are bold; headings use one calmer scale across all pages.

## Assistant orb, Visit us map and calmer menus — 9 October 2026 (night)

- The AI assistant window uses the app's own orb (`orb.js`, copied from the app's `clavis-orb.js` with a palette that suits the beige site) and plays a short, fictional chat by itself: the question is typed, sent, the orb thinks, and the reply appears word by word. The chat text lives in `ASSISTANT_CHAT` in `tools/build_site.py`.
- Every page ends with a "Visit us" section above the footer: the app's map with our head-office pin. Click the pin for the address, phone, email, directions and WhatsApp. The footer keeps the address as text.
- Header menus now close exactly the way they open; the header logo stays still; scrolling is slower and heavier on desktop.

