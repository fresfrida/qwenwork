import math, os, json, wave, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]/'public'/'demos'
ROOT.mkdir(parents=True,exist_ok=True)
W,H,FPS,SR=540,960,24,44100
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(n):return ImageFont.truetype(FONT,n)
def text(draw,xy,t,size=20,fill='#dce5fb',anchor='mm'):draw.text(xy,t,font=font(size),fill=fill,anchor=anchor)
def audio_write(p,a):
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(a,-.98,.98)*32767).astype('<i2').tobytes())
def tone(a,start,dur,freq,volume):
 i=int(start*SR);n=min(int(dur*SR),len(a)-i)
 if n<=0:return
 t=np.arange(n)/SR;env=np.minimum(t/.018,1)*np.exp(-t*4/dur);a[i:i+n]+=volume*np.sin(2*np.pi*freq*t)*env
lines=[(.6,5.3,'One little light was far from home.'),(6.3,11.4,'Then a reflection showed a different way.'),(12.3,17.3,'It found a harbour, and helped another light.')]
def story_audio(tmp,alt):
 a=np.zeros(SR*18)
 for i,(start,end,line) in enumerate(lines):
  p=tmp/f'voice{i}.wav';subprocess.run(['espeak-ng','-v','en-us','-s','135','-w',str(p),line],check=True,stdout=subprocess.DEVNULL)
  q=tmp/f'voice{i}-44.wav';subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-ar',str(SR),'-ac','1',str(q)],check=True)
  with wave.open(str(q),'rb') as w:v=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
  if len(v)>(end-start)*SR:raise RuntimeError('Narration exceeds its caption window')
  pos=int(start*SR);a[pos:pos+len(v)]+=v*.85
 tone(a,5.85,.65,440,.12)
 if alt:
  for x,f in zip([16.0,16.25,16.5],[440,554.37,659.25]):tone(a,x,.8,f,.19)
 else:tone(a,16,.8,440,.12)
 return a
stars=[(42+(i*67)%450,180+(i*83)%310) for i in range(18)]
def story_frame(t,alt):
 im=Image.new('RGB',(W,H),'#101724');d=ImageDraw.Draw(im)
 text(d,(W/2,72),'THE LITTLE SIGNAL',26);text(d,(W/2,113),'ORIGINAL LOCAL ANIMATION · PRERECORDED',11,fill='#8c9bb5')
 for x,y in stars:d.ellipse((x,y,x+2,y+2),fill='#6a7f9a')
 sea=590
 for y in range(sea,750,24):
  pts=[(x,y+math.sin(x/47+t*.8)*4) for x in range(24,W-24,4)];d.line(pts,fill='#263b56',width=2)
 d.polygon([(76,600),(98,403),(118,403),(142,600)],fill='#445a78');d.rectangle((82,394,134,420),fill='#7893ba');d.polygon([(77,394),(108,371),(139,394)],fill='#7893ba');d.rectangle((95,423,121,470),fill='#1b273a')
 d.line((110,410,430,340),fill='#2b4264',width=2)
 if t<6:x=155+45*math.sin(t*.5);y=450-26*math.sin(t*.65)
 elif t<12:p=(t-6)/6;x=185+200*p;y=450+85*math.sin(p*math.pi)
 else:p=min((t-12)/3,1);x=385+15*p;y=450+85*(1-p)
 d.rectangle((375,517,440,597),fill='#314560');d.polygon([(363,517),(408,482),(453,517)],fill='#486485')
 if 6<t<12:d.ellipse((x-7,650-y/10,x+7,650-y/10+10),fill='#769ccd');d.line((x,550,x,580),fill='#769ccd',width=2)
 colour='#ffc97b' if alt and t>=12 else '#b4d7ff'
 for r in [28,18,9]:d.ellipse((x-r,y-r,x+r,y+r),outline=colour if r==9 else '#385475',width=2)
 d.ellipse((x-5,y-5,x+5,y+5),fill=colour)
 if t>=15:
  d.rectangle((395,536,420,570),fill=colour);d.ellipse((270,485,282,497),fill=colour)
 act='A LIGHT, LOST' if t<6 else 'A DIFFERENT WAY' if t<12 else 'A HARBOUR, FOUND'
 text(d,(270,785),act,14,fill='#a1b8d9')
 for start,end,line in lines:
  if start<=t<=end:
   words=line.split();parts=[];cur=''
   for word in words:
    candidate=(cur+' '+word).strip()
    if d.textlength(candidate,font=font(22))>440:parts.append(cur);cur=word
    else:cur=candidate
   if cur:parts.append(cur)
   d.rounded_rectangle((25,817,515,903),radius=12,fill='#0a101b')
   for i,s in enumerate(parts):text(d,(270,843+i*29),s,22)
 text(d,(270,929),'CUT 2 · WARM ENDING / THREE NOTES' if alt else 'CUT 1 · COOL ENDING / ONE NOTE',10,fill='#8c9bb5')
 return im

def loop_frame(t):
 im=Image.new('RGB',(W,H),'#101724');d=ImageDraw.Draw(im);text(d,(270,75),'ONE PERFECT ORBIT',25);text(d,(270,113),'ORIGINAL LOCAL ANIMATION · PRERECORDED',11,fill='#8c9bb5')
 cx,cy,r=270,490,165
 d.ellipse((cx-r-26,cy-r-26,cx+r+26,cy+r+26),fill='#19273b',outline='#425a7d',width=2)
 d.ellipse((cx-r+26,cy-r+26,cx+r-26,cy+r-26),fill='#111c2b',outline='#425a7d',width=2)
 for i in range(4):
  a=i*math.pi/2;xx=cx+r*math.cos(a);yy=cy+r*math.sin(a);phase=(t-i*2)%8
  d.ellipse((xx-6,yy-6,xx+6,yy+6),fill='#b4d7ff' if phase<.25 else '#4d6790')
 a=t/8*2*math.pi;x=cx+r*math.cos(a);y=cy+r*math.sin(a)
 d.ellipse((x-27,y-22,x+24,y+28),fill='#0c111a');d.ellipse((x-21,y-21,x+21,y+21),fill='#779cff',outline='#cbdfff',width=2);d.ellipse((x-10,y-13,x-1,y-4),fill='#edf4ff')
 text(d,(270,766),'A SOFT CLICK AT EACH MARKER',15,fill='#a1b8d9');text(d,(270,809),'The bead returns to its starting point.',18);text(d,(270,844),'Sound is original, local and synchronized.',16,fill='#8c9bb5');text(d,(270,930),'8-SECOND ACTION LOOP · NO TALKING',11,fill='#8c9bb5')
 return im

def render(name,dur,a,frame,tmp):
 audio=tmp/(name+'.wav');audio_write(audio,a)
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(audio),'-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(dur),str(ROOT/(name+'.mp4'))]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for n in range(dur*FPS):p.stdin.write(frame(n/FPS).tobytes())
 p.stdin.close()
 if p.wait()!=0:raise RuntimeError('Video export failed')
 frame(2).save(ROOT/(name+'.png'))
 print('Rendered',name,dur,'seconds',flush=True)
with tempfile.TemporaryDirectory(prefix='studio-original-demos-') as directory:
 tmp=Path(directory)
 render('story',18,story_audio(tmp,False),lambda t:story_frame(t,False),tmp)
 render('story-v2',18,story_audio(tmp,True),lambda t:story_frame(t,True),tmp)
 a=np.zeros(SR*8);t=np.arange(len(a))/SR;a+=.015*np.sin(2*np.pi*90*t)*(1+.3*np.sin(2*np.pi*t/8))
 for i in range(4):tone(a,i*2,.14,880,.3)
 render('loop',8,a,loop_frame,tmp)
ROOT.joinpath('story.vtt').write_text('WEBVTT\n\n00:00.600 --> 00:05.300\nOne little light was far from home.\n\n00:06.300 --> 00:11.400\nThen a reflection showed a different way.\n\n00:12.300 --> 00:17.300\nIt found a harbour, and helped another light.\n')
ROOT.joinpath('story.srt').write_text('1\n00:00:00,600 --> 00:00:05,300\nOne little light was far from home.\n\n2\n00:00:06,300 --> 00:00:11,400\nThen a reflection showed a different way.\n\n3\n00:00:12,300 --> 00:00:17,300\nIt found a harbour, and helped another light.\n')
manifest=[{'id':'story-v1','title':'The little signal','duration':18,'url':'/demos/story.mp4','poster':'/demos/story.png','captions':'/demos/story.vtt','burned':True,'public':True,'notice':'Notice the beginning, reflected turn and resolved ending. Audible synthetic narration, timed readable captions and one closing note. Prerecorded, not generated from a later brief.'},{'id':'loop','title':'One perfect orbit','duration':8,'url':'/demos/loop.mp4','poster':'/demos/loop.png','public':True,'notice':'Listen for the original soft click as the bead crosses each marker. The movement returns to its starting point. Prerecorded local animation, no speech.'},{'id':'story-v2','title':'The little signal — prepared cut 2','duration':18,'url':'/demos/story-v2.mp4','poster':'/demos/story-v2.png','captions':'/demos/story.vtt','burned':True,'public':False,'notice':'Prepared revision: warm amber ending instead of cool blue, and a louder three-note ending instead of one note. Not a feedback-generated edit.'}]
ROOT.joinpath('manifest.json').write_text(json.dumps(manifest,indent=2))
