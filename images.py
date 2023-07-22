import openai
import urllib.request
import os
import yake
from util import path
from PIL import Image

openai.api_key_path = "assets/open-ai-key"

def processText(txt):
	stopwords = ["Trump", "text", "writing", "words", "paragraph", "letters", "shackles", "slave", "slavery"]
	e = yake.KeywordExtractor(top=10, n=3)
	kwss = e.extract_keywords(txt)
	kws = map(lambda x: x[0], kwss)
	filtered = filter(lambda x: len(set(x.split(" ")).intersection(set(stopwords)))==0,kws)
	finals = list(filtered)[0:5]
	prompt = " ".join(finals)
	return prompt

def gen(styleOf, topic, x):
	with open(f'{path(styleOf, topic)}/text/{x}.txt', 'r') as f:
		txt = f.readlines()[0]
		prompt = processText(txt)
		response = openai.Image.create(
		  prompt=prompt,
		  n=1,
		  size="1024x1024"
		)
		image_url = response['data'][0]['url']
		
		# image_url = "https://picsum.photos/1024/1024"
		urllib.request.urlretrieve(image_url, f"{path(styleOf, topic)}/images/{x}.png")
		img = Image.open(f"{path(styleOf, topic)}/images/{x}.png")
		res = img.crop((224,0,800,1024))

		res.save(f"{path(styleOf, topic)}/images/{x}.png")

#return "https://picsum.photos/576/1024"

# import replicate
# with open(f'text/{x}.txt', 'r') as f:
# 	prompt = f.readlines()[0]
# 	url = replicate.run(
# 	  "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
# 	  input={
# 		  "prompt": prompt,
# 		  "height": 1024,
# 		  "width": 576,
# 		  "num_inference_steps": 10
# 		}
# 	)
# 	return url[0]


