#!/usr/bin/env python
"""
helper utils for mainly the redis db models

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com

"""
from fuzzywuzzy import fuzz

def toBoolean(str):
    if str == 'True':
        return True
    elif str == 'False':
        return False
    else:
        raise Exception("Not a boolean")

def phot_filter(filt):
    orig = ""
    if filt == "all":
        orig = "$"
    if filt in ["gif", "png", "tiff"]:
        orig = filt+"$"
    if filt == "jpg":
        orig = "jp(eg|g)$"

    return orig

def search_tags(tags, query, min_score=85):
    tag_scores = {}
    for tag in tags:
        tag = tag.replace("_", " ")
        score = fuzz.partial_ratio(query, tag)
        if score >= min_score:
            tag_scores[tag] = score

    final_tags = []
    final_tags.extend(tag_scores.copy().keys())

    if final_tags:
        if query in final_tags:
            final_tags.pop(final_tags.index(query))
            return final_tags, query
        else:
            top_match = max(tag_scores, key=tag_scores.get)
            final_tags.pop(final_tags.index(top_match))
            return final_tags, top_match
    else:
        raise Exception("Could not find any matching tags")
