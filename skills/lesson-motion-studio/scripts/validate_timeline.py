"""Validate a production timeline; this does not assess teaching or visuals."""
import argparse,json,math,subprocess
from pathlib import Path
from PIL import ImageFont

def validate(path):
    d=json.loads(path.read_text()); errors=[]
    def check(ok,msg):
        if not ok:errors.append(msg)
    w,h=d.get('width',0),d.get('height',0)
    check(isinstance(w,int) and isinstance(h,int) and w>0 and h>0 and (w*9==h*16 or w*16==h*9),'Require positive 16:9 or 9:16 dimensions')
    check(d.get('fps')==30,'Require 30 fps')
    duration=d.get('duration',0)
    check(isinstance(duration,(int,float)) and math.isfinite(duration) and duration>0,'Require positive duration')
    end=0;ids=set()
    for s in d.get('scenes',[]):
        check(s.get('id') not in ids,'Duplicate scene id');ids.add(s.get('id'))
        check(abs(s['start']-end)<=1/30+1e-6,'Scene gap or overlap')
        check(s['end']>s['start'],'Scene duration must be positive')
        check(all(s.get(k) for k in ['id','text','motion','purpose']),'Missing scene description')
        end=s['end']
    check(abs(end-duration)<=1/30+1e-6,'Scenes must cover entire duration')
    for key in ['font_regular','font_bold']:
        f=path.parent/d.get(key,'missing');check(f.is_file(),f'Missing {key}')
        if f.is_file():check('Cairo' in ImageFont.truetype(str(f),32).getname()[0],f'{key} is not Cairo')
    audio=path.parent/d.get('audio','missing');check(audio.is_file(),'Missing audio')
    if audio.is_file():
        actual=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(audio)],text=True))
        check(abs(actual-duration)<=.12,'Audio and planned video durations differ')
    q=d.get('question',{})
    if q:
        check(4<=q['answer_start']-q['prompt_end']<=6,'Thinking interval must be 4 to 6 seconds')
        check(q['answer_start']<q['answer_end']<=duration+.001,'Invalid answer interval')
    else:errors.append('Missing final retrieval question timing')
    return errors

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('timeline',type=Path);a=p.parse_args()
    try:errors=validate(a.timeline)
    except (KeyError,ValueError,TypeError,OSError,subprocess.CalledProcessError) as e:errors=[str(e)]
    for e in errors:print('ERROR:',e)
    if not errors:print('Timeline checks passed; inspect exported visuals and audio separately')
    raise SystemExit(bool(errors))
