"""Prepare small excerpts from the supplied film; original media stays untouched."""
from pathlib import Path
import shutil
import subprocess
import sys

SITE = Path(__file__).resolve().parents[1]
FFMPEG = Path(shutil.which('ffmpeg') or Path.home() / 'AppData/Local/Temp/rudra24-website-media-tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe')
CLIPS = [('leads',40),('calling',90),('outreach',112),('crm',146),('assistant',164)]
SOURCE = SITE / 'assets/video/launch-film.mp4'

def run(*args):
    subprocess.run([str(FFMPEG), '-hide_banner', '-loglevel', 'error', '-y', *map(str,args)], check=True)

LANCZOS = 'flags=lanczos+accurate_rnd+full_chroma_int,format=yuv420p'

def previews():
    # Hover previews show at 480 CSS px: 960x540 for high-density screens, 480x270 for 1x screens.
    # Pre-scaling with Lanczos means the browser never shrinks 1920px footage itself (its quick
    # bilinear downscale is what smears small UI text).
    for key, second in CLIPS:
        for w, h, out in [(960, 540, f'{key}-preview.mp4'), (480, 270, f'{key}-preview-480.mp4')]:
            run('-ss',second,'-i',SOURCE,'-t',10,'-an','-vf',f'scale={w}:{h}:{LANCZOS}','-c:v','libx264','-preset','veryslow',
                '-tune','animation','-crf',16,'-profile:v','high','-movflags','+faststart',SITE/f'assets/video/{out}')
        print(f'Prepared {key} previews', flush=True)

def film_sizes():
    # The hero film is drawn at roughly 560-760 CSS px; media.js picks the smallest copy that covers
    # (drawn width x screen density). Audio is copied untouched.
    for w in (1280, 960, 640):
        run('-i',SOURCE,'-vf',f'scale={w}:{w*9//16}:{LANCZOS}','-c:v','libx264','-preset','slow','-tune','animation',
            '-crf',18,'-profile:v','high','-c:a','copy','-movflags','+faststart',SITE/f'assets/video/launch-film-{w}.mp4')
        print(f'Prepared launch film {w}', flush=True)

if __name__ == '__main__':
    if not FFMPEG.exists():
        sys.exit('Set FFMPEG to your installed ffmpeg binary before regenerating media.')
    if sys.argv[1:] == ['--previews']:
        previews(); sys.exit()
    if sys.argv[1:] == ['--film-sizes']:
        film_sizes(); sys.exit()
    run('-i', SITE.parents[1]/'assets/rudra24-icon.png', '-vf', 'scale=128:128', '-frames:v', 1, SITE/'assets/rudra24-icon.png')
    for key, second in CLIPS:
        run('-ss',second,'-i',SOURCE,'-t',10,'-an','-c:v','libx264','-preset','fast','-crf',18,'-movflags','+faststart',SITE/f'assets/video/{key}.mp4')
        run('-ss',second+3,'-i',SOURCE,'-frames:v',1,'-q:v',2,SITE/f'assets/video/{key}-poster.jpg')
        print(f'Prepared {key}', flush=True)
    run('-ss',43,'-i',SOURCE,'-frames:v',1,'-q:v',2,SITE/'assets/video/launch-poster.jpg')
    previews()
    film_sizes()
