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
import markdown as md
from markdown.util import etree
from markdown.treeprocessors import Treeprocessor

cleanTags = list(bl.ALLOWED_TAGS)
cleanTags.extend(['p', 'img', 'small', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6','br', 'hr', 'article', 'section', 'div'])
cleanAttr = dict(bl.ALLOWED_ATTRIBUTES)
cleanAttr["img"] = ["src", "width", "height"]
cleanAttr["i"] = ["class"]


class SectionWrapperTreeprocessor(Treeprocessor):
    def run(self, doc):
        first = True
        body = etree.Element("div")
        sec = etree.SubElement(body, "section")
        for elem in doc:
            if elem.tag in ['h1'] and not first:
                sec = etree.SubElement(body, "section")

            if first:
                first = False

            sec.append(elem)

        return body


class CustomMarkdownExtension(md.Extension):
    def __init__(self, configs={}):
        self.config = {}
        for key, value in configs:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        self.processor = SectionWrapperTreeprocessor()
        self.processor.md = md
        self.processor.config = self.getConfigs()
        md.treeprocessors.add('sectionwrap', self.processor, '>prettify')


def sanitize(pre_clean):
    """
    Sanitize the input into safe HTML through bleach

    :param pre_clean: a `str` of (probably) html to sanitize
    """
    return bl.clean(pre_clean, tags=cleanTags, attributes=cleanAttr)


def markdown_raw(text):
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
    extras = [
        "headerid",
        "footnotes",
        "fenced_code",
        "nl2br",
        "wikilinks",
        CustomMarkdownExtension()
    ]

    return md.markdown(text, extensions=extras)


def markdown(text):
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
    text = markdown_raw(text)
    return sanitize(text)
