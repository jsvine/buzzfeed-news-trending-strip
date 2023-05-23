#!/usr/bin/env python
"""
Note: This script no longer works, since buzzfeednews.com is no
longer being updated and no longer features the "Trending" strip.

When it was running, it required the following Python libraries:
- lxml
- cssselect
- requests
"""

import datetime
import os

import lxml.html
import requests

DEST = "bfn-trending-strip.tsv"

if not os.path.exists(DEST):
    with open(DEST, "w") as f:
        f.write("\t".join(["timestamp", "position", "text", "url"]))
        f.write("\n")

now = datetime.datetime.utcnow().replace(microsecond=0).isoformat()

html = requests.get("https://www.buzzfeednews.com/").content
dom = lxml.html.fromstring(html)

links = dom.cssselect(".newsblock-trending-tags-bar li a")

data = [
    (now, i, a.text_content().strip(), a.attrib["href"]) for i, a in enumerate(links)
]

with open(DEST, "a") as f:
    f.write("\n".join("\t".join(map(str, item)) for item in data))
    f.write("\n")
