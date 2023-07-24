import text
import os
import text
import audio
import images
import video
import util
import shutil

def createPaths(styleOf, topic, length):
	path = util.path(styleOf, topic)
	os.mkdir(path)
	os.mkdir(f"{path}/text")
	os.mkdir(f"{path}/images")
	os.mkdir(f"{path}/audio")
	os.mkdir(f"{path}/subtitles")
	os.mkdir(f"{path}/video")
	cmd = f"head -n {length} assets/list.txt > {path}/video/list.txt"
	os.system(cmd)

def genVideo(styleOf, topic, length):
	video.genAll(styleOf, topic, length)

def genAudio(styleOf, topic, length):
	for i in range(1, length + 1):
		audio.gen(styleOf, topic, i)

def genImages(styleOf, topic, length):
	for i in range(1, length + 1):
		images.gen(styleOf, topic, i)

def genText(styleOf, topic, length):
	text.gen(styleOf, topic, length)

def gen(styleOf, topic, length):
	createPaths(styleOf, topic, length)
	genText(styleOf, topic, length)
	genAudio(styleOf, topic, length)
	genImages(styleOf, topic, length)
	genVideo(styleOf, topic, length)
