import os
import subprocess
from util import path
from util import getLength

#image to video
def imageToVideo(styleOf, topic, x):
	vlen = getLength(styleOf, topic, x) + 0.25
	cmd = f'ffmpeg -y -loop 1 -i {path(styleOf, topic)}/images/{x}.png -y -filter_complex "[0]scale=1080:-2,setsar=1:1[out];[out]crop=1080:1920[out];[out]scale=8000:-1,zoompan=z=\'zoom+0.002\':x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=500:s=1080x1920:fps=25[out]" -acodec aac -vcodec libx264 -map "[out]" -map "0:a?" -pix_fmt yuv420p -r 25 -t {vlen} {path(styleOf, topic)}/video/{x}.mp4'
	return os.system(cmd)

#add audio
def addAudio(styleOf, topic, x):
	cmd = f"ffmpeg -y -i {path(styleOf, topic)}/video/{x}.mp4 -i {path(styleOf, topic)}/audio/{x}.mp3 -c:v copy -c:a aac {path(styleOf, topic)}/video/{x}a.mp4"
	return os.system(cmd)

#add caption
def addCaption(styleOf, topic, x):
	cmd = f'ffmpeg -y -i {path(styleOf,topic)}/video/{x}a.mp4 -lavfi "subtitles={path(styleOf, topic)}/subtitles/{x}.srt:force_style=\'Alignment=10,Fontsize=30\'" {path(styleOf, topic)}/video/{x}b.mp4'
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
		next = addCaption(styleOf, topic, x)
	print("Done")

	#add background audio
	#upload
def genAll(styleOf, topic):
	for i in range(1, 3):
		gen(styleOf, topic, i)
	concat(styleOf, topic)
	addMusic(styleOf, topic)

#TODO upload