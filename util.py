import subprocess

def path(styleOf, topic):
	return f"output/{styleOf}-{topic}".replace(" ", "-").lower()

#get length of audio by index
def getLength(styleOf, topic, x):
	cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {path(styleOf, topic)}/audio/{x}.mp3"
	raw = str(subprocess.check_output([cmd], shell=True))
	return float(raw.strip("b'").rstrip("\\n"))