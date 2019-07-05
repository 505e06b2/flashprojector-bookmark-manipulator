#!/usr/bin/env python3

settings = {
	"git": "https://gitlab.com/api/v4/projects/505e06b2%2Fswf-archive/repository/tree?per_page=100&page=",
	"baseurl": "https://glcdn.githack.com/505e06b2/swf-archive/raw/master/"
}

import urllib.request, urllib.parse, os, json

request_json = ["not empty"]
swf_list = []
index = 1

while request_json:
	print("Getting page %d" % index)
	with urllib.request.urlopen("%s%d" % (settings["git"], index)) as response:
		request_json = json.loads(response.read())

	for i in request_json:
		swf_list.append(i["name"])
	index += 1

swf_list = sorted(swf_list, key=lambda s: s.casefold())
f = open("%s/.flashrc" % (os.environ["HOME"]), "w")
for i in swf_list:
	f.write("<A HREF=\"%s%s\">%s</A>\n" % (settings["baseurl"], urllib.parse.quote(i), i))

f.close()
