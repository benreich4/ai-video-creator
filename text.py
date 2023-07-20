import openai
import os
from util import path

openai.api_key_path = "assets/open-ai-key"

def gen(styleOf, topic):
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": f"Generate 4 short sentences in the style of {styleOf} on the topic of {topic}."},
	])

	msgs = response.choices[0].message.content.split("\n")
	nonempty = [x for x in msgs if x]
	for i in range(0,len(nonempty)):
		#remove numbering
		clean = msgs[i][3:]
		with open(f"{path(styleOf, topic)}/text/{i+1}.txt", 'w+') as f:
				f.write(clean)