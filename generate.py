import text
import os
import text
import audio
import images
import video
import util
import shutil

def createPaths(styleOf, topic):
	path = util.path(styleOf, topic)
	os.mkdir(path)
	os.mkdir(f"{path}/text")
	os.mkdir(f"{path}/images")
	os.mkdir(f"{path}/audio")
	os.mkdir(f"{path}/subtitles")
	os.mkdir(f"{path}/video")
	shutil.copyfile("assets/list.txt", f"{path}/video/list.txt")

def gen(styleOf, topic):
	createPaths(styleOf, topic)
	text.gen(styleOf, topic)
	for i in range(1, 4):
		audio.gen(styleOf, topic, i)
		images.gen(styleOf, topic, i)
	video.genAll(styleOf, topic)