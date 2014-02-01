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
import markdown as md
from markdown.util import etree
from markdown.treeprocessors import Treeprocessor


class SectionWrapperTreeprocessor(Treeprocessor):
    def run(self, doc):
        first = True
        body = etree.Element("div")
        sec = etree.SubElement(body, "section")
        for elem in doc:
            if elem.tag in ['h1', 'h2', 'hr'] and not first:
                sec = etree.SubElement(body, "section")

            if first:
                first = False

            if elem.tag not in ['hr']:
                sec.append(elem)

        return body


class Slideshow(md.Extension):
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
