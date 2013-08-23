#!/usr/bin/env python
"""
Base util for sending emails from within fla.gr

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pystache

import utils.markdownUtils as mdu
import models.couch.template.templateModel as tm
import config.config as c

from gevent import monkey; monkey.patch_all()
import gevent

from gevent_zeromq import zmq
context = zmq.Context()
zmqSock = context.socket(zmq.SUB)
zmqSock.connect("tcp://127.0.0.1:5000")
zmqSock.setsockopt(zmq.SUBSCRIBE, "sendEmail")

import json

import logging
logger = logging.getLogger(c.general.logName+"email.sender")

import models.redis.setting.settingModel as sm


class emailer(object):
    def __init__(self):
        """
        Sets up an emailer which can funtion as both a util and a stand alone system

        After initializing, run emailer.getMessages() to start it as a stand alone
        system which will listen on zmq for sendEmail:jsonData.

        To use as a util, call sendMessage or sendMessages with the proper data
        """
        self.setup()

    def setup(self):
        if sm.getSetting("emailServer", "notLocalhost"):
            logger.debug("Email server not localhost, attempting to login")
            self.s = smtplib.SMTP(sm.getSetting("emailServer", "host"),
                    int(sm.getSetting("emailServer", "port")))
            self.s.ehlo()
            self.s.starttls()
            self.s.ehlo()
            try:
                self.s.login(sm.getSetting("emailServer", "loginEmail"),
                        sm.getSetting("emailServer", "loginPassword"))
            except Exception as exc:
                logger.critical("Could not login to email server!")
                logger.debug(exc)
        else:
            try:
                self.s = smtplib.SMTP('localhost')
            except Exception as exc:
                logger.critical("Could not connect to localhost email server!")
                logger.debug(exc)
        logger.debug("Connected to email server...")


    def sendMessage(self, tmplid, tmplData, whoTo, subject):
        """
        Finds the given template id in the database, renders it into HTML
        via markdown, then runs mustache to fill in template data. Finally,
        the rendered and compiled template is put into an email package
        and sent via email to the person given by `whoTo`

        :param tmplid: The document id of the template for which to use for the email
        :param tmplData: The data which should be placed into the template with mustache
        :param whoTo: The email address of the person who this email should go to
        :param subject: The subject of the email
        """
        tmplObj = tm.templateORM.getByID(tmplid)
        tmpl = tmplObj.template

        msg = self.makeMessage(subject, whoTo, tmpl, tmplData)

        logger.debug("Sending message...")
        if sm.getSetting("emailServer", "sendEmail"):
            try:
                self.s.sendmail("fla.gr", [whoTo], msg.as_string())
            except:
                self.s.connect()
                self.s.sendmail("fla.gr", [whoTo], msg.as_string())


    def sendMessages(self, tmplid, tmplData, whoTo, subject):
        """
        Same as above however sends the message to multiple people
        Finds the given template id in the database, renders it into HTML
        via markdown, then runs mustache to fill in template data. Finally,
        the rendered and compiled template is put into an email package
        and sent via email to the person given by `whoTo`

        :param tmplid: The document id of the template for which to use for the email
        :param tmplData: The data which should be placed into the template with mustache
            Should be in a dict whos keys are the emails in `whoTo` and the values are the
            data
        :param whoTo: The email address of the person who this email should go to
            should be a list
        :param subject: The subject of the email
        """
        tmplObj = tm.templateORM.getByID(tmplid)
        tmpl = tmplObj.template

        for person in whoTo:
            msg = self.makeMessage(subject, person, tmpl, tmplData[person])

            logger.debug("Sending message...")
            if sm.getSetting("emailServer", "sendEmail"):
                try:
                    self.s.sendmail("fla.gr", [person], msg.as_string())
                except:
                    self.s.connect()
                    self.s.sendmail("fla.gr", [person], msg.as_string())



    def compileTmpl(self, tmpl, tmplData):
        """
        Takes in the given template, and filles it out with mustache from `tmplData`
        Then compiles it into HTML with markdown.

        :param tmpl: The mustache and markdown template to fill out and render
        :param tmplData: The dict of values to render the template with, for mustache
        :return: `part1, part2` are `MIMEText` objects with encodings of plain and HTML
            for use in `MIMEMultipart` messages.
        """
        compiledTmpl = pystache.render(tmpl, tmplData)
        tmplMarked = mdu.mark(compiledTmpl)

        part1 = MIMEText(compiledTmpl, 'plain')
        part2 = MIMEText(tmplMarked, 'html')

        return part1, part2


    def makeMessage(self, subject, person, tmpl, tmplData):
        """
        Returns a full email with both plain text and HTML parts

        :param subject: Subject for the message
        :param person: The email address of the person to address the message to
        :param tmpl: The mustache and markdown template to render and compile for the message
        :param tmplData: The mustache template data to be used to fill out the message
        :return: A full mutlipart email with plain text and HTML parts ready to be sent
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = "fla.gr"
        msg['To'] = person
        part1, part2 = self.compileTmpl(tmpl, tmplData)

        msg.attach(part1)
        msg.attach(part2)

        return msg


    def getMessages(self):
        while True:
            reply = zmqSock.recv()
            jsonBit = reply.split(":", 1)[1]
            logger.debug("Got: "+jsonBit)

            data = json.loads(jsonBit)

            if type(data["whoTo"]) != list:
                logger.debug("Sending single message...")
                self.sendMessage(data["tmplID"], data["tmplData"],
                        data["whoTo"], data["subject"])
            else:
                logger.debug("Sending same tmpl to multiple people...")
                self.sendMessages(data["tmplID"], data["tmplData"],
                        data["whoTo"], data["subject"])


def start():
    logger.debug("Starting up email sending service...")
    sender = emailer()
    ser = gevent.spawn(sender.getMessages)
    try:
        ser.join()
    except Exception as exc:
        sender.s.quit()
        logger.debug("emailSender: Got exception: " + exc)
        gevent.shutdown
    except KeyboardInterrupt:
        sender.s.quit()
        logger.debug("emailSender shutting down from keyboard interrupt...")
        gevent.shutdown
    else:
        sender.s.quit()
        logger.debug("emailSender shutting down...")
        gevent.shutdown
