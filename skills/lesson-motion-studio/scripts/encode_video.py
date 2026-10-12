"""Encode numbered PNG frames with verified audio and video duration."""
import argparse,math,subprocess
from pathlib import Path
from PIL import Image

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--frames',type=Path,required=True,help='000000.png onward at 30 fps')
    p.add_argument('--audio',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(a.audio)],text=True))
    files=sorted(a.frames.glob('*.png'));n=math.ceil(duration*30)
    if len(files)!=n:raise SystemExit(f'Expected {n} frames, found {len(files)}')
    size=None
    for i,f in enumerate(files):
        if f.name!=f'{i:06d}.png':raise SystemExit('Frames must be consecutive from 000000.png')
        with Image.open(f) as im:
            if size is None:size=im.size
            if im.size!=size:raise SystemExit('Inconsistent frame dimensions')
    w,h=size
    if (w*9!=h*16 and w*16!=h*9) or w%2 or h%2:raise SystemExit('Require even 16:9 or 9:16 dimensions')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-framerate','30','-start_number','0','-i',str(a.frames/'%06d.png'),'-i',str(a.audio),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-movflags','+faststart',str(a.output)],check=True)
    actual=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(a.output)],text=True))
    if abs(actual-duration)>.15:raise SystemExit('Encoded duration differs from narration')
    print(a.output)
