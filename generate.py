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

def gen(styleOf, topic, length):
	createPaths(styleOf, topic, length)
	text.gen(styleOf, topic, length)
	for i in range(1, length + 1):
		audio.gen(styleOf, topic, i)
		images.gen(styleOf, topic, i)
	video.genAll(styleOf, topic, length)