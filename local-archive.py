#!/usr/bin/env python3

import os, subprocess

settings = {
	"path": "/media/sd/swf-archive",
	"flashrc": os.environ["HOME"] + "/.flashrc",
	"flashplayer-path": "flashplayer"
}

swf_list = sorted(
	filter(lambda f: not f.startswith("."), os.listdir(settings["path"]))
, key=lambda s: s.casefold())

write_buffer = "" #might not need it, but it saves iterating twice
largest_mtime = 0.0

for i in swf_list:
	mtime = os.path.getmtime("%s/%s" % (settings["path"], i))
	if mtime > largest_mtime: largest_mtime = mtime
	write_buffer += "<A HREF=\"file://%s/%s\">%s</A>\n" % (settings["path"], i, i)

if not os.path.exists(settings["flashrc"]) or largest_mtime > os.path.getmtime(settings["flashrc"]):
	print("Updating .flashrc...")
	with open(settings["flashrc"], "w") as f:
		f.write(write_buffer)

with open(os.devnull, "wb") as f:
	subprocess.Popen(settings["flashplayer-path"], stdout=f, stderr=subprocess.STDOUT)
