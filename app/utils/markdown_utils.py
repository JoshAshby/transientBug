#!/usr/bin/env python
"""
Utils for handling unsafe markdown
Renders and cleans

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import bleach as bl
import markdown2 as md

cleanTags = list(bl.ALLOWED_TAGS)
cleanTags.extend(['p', 'img', 'small', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6','br', 'hr'])
cleanAttr = dict(bl.ALLOWED_ATTRIBUTES)
cleanAttr["img"] = ["src", "width", "height"]
cleanAttr["i"] = ["class"]


def sanitize(pre_clean):
    """
    Sanitize the input into safe HTML through bleach

    :param pre_clean: a `str` of (probably) html to sanitize
    """
    return bl.clean(pre_clean, tags=cleanTags, attributes=cleanAttr)


def markdown(text):
    """
    Renders markdown into, well, markdown, through markdown2 and a custom
    markdown class (for custom preprocessing).

    These extras are enabled in markdown:
     * header-ids
     * footnote
     * fenced-code-blocks
     * break-on-newline
     * pyshell

    :param text: `str` or `unicode` object which is the text to render to html
    """
    extras = ["header-ids", "footnote", "fenced-code-blocks",
        "break-on-newline", "pyshell"]
    return CustomMarkdown(extras=extras).convert(text)


def markdown_clean(text):
    """
    Renders markdown into, well, markdown, through markdown2 and a custom
    markdown class (for custom preprocessing). Then runs it through bleach to
    sanitize it.

    These extras are enabled in markdown:
     * header-ids
     * footnote
     * fenced-code-blocks
     * break-on-newline
     * pyshell

    :param text: `str` or `unicode` object which is the text to render to html
    """
    text = markdown(text)
    return sanitize(text)


class CustomMarkdown(md.Markdown):
    def preprocces(self, text):
        """
        currently does nothing, however I want a more simple way to embed media
        into a post in transientbug so I'm looking into doing something like
        `[[media name]]` or something that this will then just basically parse and
        replace with the proper link or something. Maybe its more of a post
        processing thing? Idk, because the markdown2, unlike the plain markdown
        module for Python doesn't support writing your own extensions without
        subclassing the Markdown class and basically rewriting things to do:
        `if "blag" in self.extras`
        """
        print "[[media]]" in text
        return text
