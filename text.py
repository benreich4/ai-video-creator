import openai
import os
import re
from util import path

openai.api_key_path = "assets/open-ai-key"

def gen(styleOf, topic, length):
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": f"Generate {len} short enumerated quotes in the style of {styleOf} on the topic of {topic}."},
	])

	msg = response.choices[0].message.content
	msgs = re.split("\d[\.|\)]", msg)
	nonempty = [x for x in msgs if x.strip() != ""]
	for i in range(0,len(nonempty)):
		#remove numbering and remove quotes
		clean = nonempty[i].strip().strip('"').strip().replace("\n", " ")
		with open(f"{path(styleOf, topic)}/text/{i+1}.txt", 'w+') as f:
				f.write(clean)