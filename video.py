import os
import subprocess
from util import path

#get length of audio by index
def getLength(styleOf, topic, x):
	cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {path(styleOf, topic)}/audio/{x}.mp3"
	raw = str(subprocess.check_output([cmd], shell=True))
	return float(raw.strip("b'").rstrip("\\n"))

#image to video
def imageToVideo(styleOf, topic, x):
	vlen = getLength(styleOf, topic, x) + 0.5
	cmd = f'ffmpeg -y -loop 1 -i {path(styleOf, topic)}/images/{x}.png -y -filter_complex "[0]scale=1080:-2,setsar=1:1[out];[out]crop=1080:1920[out];[out]scale=8000:-1,zoompan=z=\'zoom+0.002\':x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=500:s=1080x1920:fps=25[out]" -acodec aac -vcodec libx264 -map "[out]" -map "0:a?" -pix_fmt yuv420p -r 25 -t {vlen} {path(styleOf, topic)}/video/{x}.mp4'
	return os.system(cmd)

#add audio
def addAudio(styleOf, topic, x):
	cmd = f"ffmpeg -y -i {path(styleOf, topic)}/video/{x}.mp4 -i {path(styleOf, topic)}/audio/{x}.mp3 -c:v copy -c:a aac {path(styleOf, topic)}/video/{x}a.mp4"
	return os.system(cmd)

def srtTime(rt):
	rts = str(int(rt // 1)).rjust(2,"0")
	rtms = str((rt % 1) + 0.0001)[2:5]
	return f"00:00:{rts},{rtms}"

#generate srt
#TODO use timepoints from API
def genSubs(styleOf, topic, x):
	vlen = getLength(styleOf, topic, x)
	f = open(f'{path(styleOf, topic)}/text/{x}.txt','r').readlines()[0]
	ws = f.split(" ")
	spw = vlen / len(ws)
	wss = [ws[i:i + 5] for i in range(0, len(ws), 5)] 
	lt = 0
	f2 = open(f'{path(styleOf, topic)}/subtitles/{x}.srt', 'w+')
	for k in range(0, len(wss)):
		f2.write(str(k+1))
		f2.write("\n")
		rt = min((k+1)*5*spw,vlen)
		f2.write(srtTime(lt) + " --> " + srtTime(rt))
		lt = rt
		f2.write("\n")
		f2.write(" ".join(wss[k]))
		f2.write("\n\n")
	f2.close()

#add caption
def addCaption(styleOf, topic, x):
	cmd = f'ffmpeg -y -i {path(styleOf,topic)}/video/{x}a.mp4 -lavfi "subtitles={path(styleOf, topic)}/subtitles/{x}.srt:force_style=\'Alignment=10,MarginV=Fontsize=24\'" {path(styleOf, topic)}/video/{x}b.mp4'
	return os.system(cmd)

#concat all videos
def concat(styleOf, topic):
	#TODO generate list.text
	cmd = f'ffmpeg -y -f concat -safe 0 -i {path(styleOf,topic)}/video/list.txt -c copy {path(styleOf, topic)}/video/output.mp4'
	print(cmd)
	return os.system(cmd)

#add background audio
def addMusic(styleOf, topic):
	#TODO cut audio
	#Merge audio
	cmd = f"ffmpeg -y -i {path(styleOf, topic)}/video/output.mp4 -i assets/back.mp3 -filter_complex '[0:a]aresample=async=1[0a];[1:a]volume=0.3[1a];[0a][1a]amix=inputs=2:duration=first:dropout_transition=3,loudnorm' {path(styleOf, topic)}/video/output_final.mp4"
	# cmd = f"ffmpeg -y -i {path(styleOf, topic)}/video/output.mp4 -i assets/back.mp3 -c:v copy -shortest -filter_complex \"[0:a]aformat=fltp:44100:stereo,apad[0a];[1]aformat=fltp:44100:stereo,volume=0.2[1a];[0a][1a]amerge[a]\" \
       # -map 0:v -map \"[a]\" {path(styleOf, topic)}/video/output_final.mp4"
	return os.system(cmd)

def gen(styleOf, topic, x):
	print("Image to video")
	next = imageToVideo(styleOf, topic, x)
	print(next)
	if (next==0):
		print("Adding audio")
		next = addAudio(styleOf, topic, x)
	if (next==0):
		print("Generating subs")
		genSubs(styleOf, topic, x)
		next = addCaption(styleOf, topic, x)
	print("Done")

	#add background audio
	#upload
def genAll(styleOf, topic):
	for i in range(1, 4):
		gen(styleOf, topic, i)
	concat(styleOf, topic)
	addMusic(styleOf, topic)

#TODO upload