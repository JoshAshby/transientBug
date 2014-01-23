#!/usr/bin/env python
"""
helper utils for searching random shit

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com

"""
from fuzzywuzzy import fuzz


def photo_filter(filt):
    orig = ""
    if filt == "all":
        orig = "$"
    if filt in ["gif", "png", "tiff"]:
        orig = filt+"$"
    if filt == "jpg":
        orig = "jp(eg|g)$"

    return orig


def search_tags(tags, query, min_score=75):
    q = query.replace("_", " ").lower()

    match = ""

    tag_scores = {}
    for tag in tags:
        tag_search = tag.replace("_", " ").lower()

        if tag_search == q:
            match = query
        else:
            score = fuzz.partial_ratio(query, tag_search)
            if score >= min_score:
                tag_scores[tag] = score

    final_tags = []
    final_tags.extend(tag_scores.copy().keys())

    if match:
        return final_tags, match
    elif final_tags:
        top_match = max(tag_scores, key=tag_scores.get)
        final_tags.pop(final_tags.index(top_match))
        return final_tags, top_match
    else:
        return [], ""
