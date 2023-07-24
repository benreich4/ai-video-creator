from types import SimpleNamespace

def get(name):
	d = info.get(name, info.get("Shakespeare"))
	return SimpleNamespace(**d)

info = {
	"Shakespeare": {
		"language_code":"en-GB", 
        "name":"en-GB-Neural2-D",
        "pitch": -3,
        "speaking_rate": 1.2
	},
	"Barbie": {
	    "language_code":"en-US", 
	    "name":"en-US-Neural2-F",
	    "pitch": 4,
        "speaking_rate": 1.2
	},
	"Taylor Swift": {
	    "language_code":"en-US", 
	    "name":"en-US-Neural2-F",
	    "pitch": 1,
        "speaking_rate": 1.2
	}
}