#!/usr/bin/env python3

"""

This script generates a .flashrc in `/tmp` (by default) and then opens the Flash Projector and makes it use this new .flashrc
by setting $HOME to `/tmp. If you then check your flash projector bookmarks, you will see the list of SWFs on 4chan.org/f/

"""

settings = {
	"json": "http://a.4cdn.org/f/catalog.json",
	"baseurl": "http://i.4cdn.org/f/",
	"directory": "/tmp",
	"flashplayer-path": "flashplayer" #my player is on my $PATH
}

import urllib.request, json, os, urllib.parse, html, subprocess

f = open("%s/.flashrc" % (settings["directory"]), "w")

with urllib.request.urlopen(settings["json"]) as response:
	for x in json.loads(response.read())[0]["threads"]:
		filename = html.unescape(x["filename"])
		try:
			subject = ": " + html.unescape(x["sub"])
		except KeyError:
			subject = ""

		f.write("<A HREF=\"%s%s.swf\">%s</A>\n" % (
			settings["baseurl"],
			urllib.parse.quote(x["filename"], safe=" "),
			"{0:<30} [{1}] {2}".format(
				"[" + ((filename[:25] + '(…)') if len(filename) > 25 else filename) + "]",
				("?" if x["tag"] == "Other" else x["tag"][0]),
				((subject[:25] + '(…)') if len(subject) > 25 else subject)
			)
		))

f.close()


if not os.path.exists("%s/.gtkrc-2.0" %settings["directory"]):
	print("Generating .gtkrc...")
	f = open("%s/.gtkrc-2.0" %settings["directory"], "w")
	f.write( # !WRITE GTK SETTINGS HERE
"""
gtk-font-name = "DejaVu Sans Mono 9"
""")
	f.close()

os.environ["HOME"] = settings["directory"] # set .flashrc to tmp

with open(os.devnull, "wb") as f:
	subprocess.Popen(settings["flashplayer-path"], stdout=f, stderr=subprocess.STDOUT)
