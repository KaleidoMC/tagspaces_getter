from pathlib import Path
import json
import datetime
import codecs

appName = "TagSpaces"
appVersion = "3.11.9"

# https://github.com/ljcucc/tagspaces-cli/blob/main/tag_selector.py
def time():
    result = "T".join(str(datetime.datetime.now()).split(" "))
    result = result.split(".")
    result[1] = result[1][:3]
    result = ".".join(result)
    return result + "Z"

class Tags:
	
	def __init__(self, path):
		self.tags = []
		if isinstance(path, str):
			path = Path(path)
		self.path = path.parent.joinpath(".ts", path.name + ".json")
		if not self.path.exists():
			return;
		jo = self.__getJO();
		if "tags" not in jo:
			return;
		for tag in jo["tags"]:
			self.tags.append(tag["title"])
	
	def add(self, tagDef):
		if not self.path.parent.exists():
			self.path.parent.mkdir(parents=True, exist_ok=True)
		tag = {}
		if self.path.exists():
			jo = self.__getJO();
			if tagDef.title in self.tags:
				for o in jo["tags"]:
					if o["title"] == tagDef.title:
						tag = o
						break
			else:
				jo["tags"].append(tag)
		else:
			jo = {}
			jo["tags"] = [ tag ]
			jo["appName"] = appName
			jo["appVersion"] = appVersion
			jo["lastUpdated"] = time()
		
		tag["title"] = tagDef.title
		tag["color"] = tagDef.color
		tag["textcolor"] = tagDef.textcolor
		tag["type"] = "sidecar"
		
		with self.path.open(mode="w") as f:
			json.dump(jo, f)
		if tagDef.title not in self.tags:
			self.tags.append(tagDef.title)
	
	def remove(self, title):
		if title not in self.tags:
			return
		jo = self.__getJO();
		tag = None
		for o in jo["tags"]:
			if o["title"] == title:
				tag = o
				break
		if tag == None:
			return
		jo["tags"].remove(tag)
		with self.path.open(mode="w") as f:
			json.dump(jo, f)
			self.tags.remove(title)
	
	def __getJO(self):
		jo = self.path.read_bytes();
		if len(jo) == 0:
			return { "tags": [] }
		if jo[:3] == codecs.BOM_UTF8:
			jo = jo[3:]
		jo = jo.decode("utf-8")
		return json.loads(jo)

class TagDef:

	def __init__(self, title, color, textcolor):
		self.title = title
		self.color = color
		self.textcolor = textcolor