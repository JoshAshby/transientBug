#!/usr/bin/env python
"""
utils for handling unsafe markdown
renders and cleans

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import bleach as bl
import markdown as md

cleanTags = bl.ALLOWED_TAGS
cleanTags.extend(['p', 'img', 'small', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6','br', 'hr'])
cleanAttr = bl.ALLOWED_ATTRIBUTES
cleanAttr["img"] = ["src", "width", "height"]
cleanAttr["i"] = ["class"]


def markClean(markdown, markdown_extras=[]):
    mark = md.markdown(markdown, markdown_extras)
    cleanedMark = bl.clean(mark, tags=cleanTags, attributes=cleanAttr)

    return cleanedMark

def mark(markdown):
    return md.markdown(markdown)

def cleanInput(preClean):
    return bl.clean(preClean, tags=cleanTags, attributes=cleanAttr)
