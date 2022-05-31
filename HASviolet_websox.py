#!/usr/bin/python3
#
# HASviolet WebSocket Server
#
#   USAGE: HASviolet_websox.py 
#
#   REVISION: 20210327-0700
#
#


#
# IMPORT LIBRARIES
#

import asyncio
import argparse 
import binascii
import gc
import hashlib
import json
import os
import ssl
import sys
import threading
import time
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
import uuid
from HASvioletRF import HASrf
from HASvioletHID import HAShid


#
# VARIABLES
#

define("port", default=8000, help="run on the given port", type=int)
wsxCLIENTS = []                                                          # Client Connection Tracking for Tornado
HASviolet_RXLOCK = False                                                  # True = RX is running
HASviolet_TXLOCK = False                                                  # True = TX is running
HASviolet_SERVERPATH = "/home/pi/HASviolet/server/"                       # Path to files. Change when Pi
HASviolet_CFG_JSON = "/home/pi/HASviolet/cfg/HASviolet.json"                   # Config file is in JSON format
HASviolet_MSGS = HASviolet_SERVERPATH + "msgs/HASviolet.msgs"              # radio writes msgs received here   
HASviolet_PWF = "/home/pi/HASviolet/cfg/HASviolet.pwf"                    # Password file  user:hashedpasswd
HASviolet_LOGIN = HASviolet_SERVERPATH + "static/HASviolet_LOGIN.html"
HASviolet_LOGINCSS = HASviolet_SERVERPATH + "static/HASviolet_LOGIN.css"
HASviolet_INDEX = HASviolet_SERVERPATH + "static/HASviolet_INDEX.html"
HASviolet_INDEXCSS = HASviolet_SERVERPATH + "static/HASviolet.css"
HASvioletjs = HASviolet_SERVERPATH + "static/HASviolet.js"

stored_password = ""                                                     # hashedpassword stored in Password file
currmsg_ts = ""
lastmsg_ts = ""

#
# CLASSES
#

class HASsession:
    def __init__(self):
        self.MsgFile = HASvioletmsgs
        self.currMsg = ""
        self.currMsgTs = time.time()
        self.lastMsg = ""
        self.lastMsgTs = time.time()
        self.wsMsg = "NULL:NULL"                # Websocket Message Received from Client "CMD:OPR"
        self.wsCmd = "NULL"                     # Command (CMD) parsed
        self.wsOpr = "NULL"                     # Operator (OPR) aka message parsed  

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("HASvioletuser")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('server/static/HASviolet_INDEX.html')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('server/static/HASviolet_LOGIN.html')

    def post(self):
        fusername = self.get_argument("fusername")
        fpassword = self.get_argument("fpassword")
        if find_user(fusername) == "":
            self.redirect("/login")
        stored_password = find_password(fusername)
        verdict = verify_password(stored_password, fpassword)
        if verdict == True:
            self.set_secure_cookie("HASvioletuser", str(uuid.uuid4()), secure=True, expires_days=1)
            self.redirect("/")

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    @classmethod
    def on_rxradio(self, message):
        print ("WS:RXRADIO:" + message)
        for client in wsxCLIENTS:
            client.write_message(message)

    def cl_multicast(self, message):
        print ("WS:MULTICAST:" + message)
        for client in wsxCLIENTS:
            client.write_message("WS:CLIENTS:", wsxCLIENTS)

    def open(self):
        if self not in wsxCLIENTS:
            wsxCLIENTS.append(self)
        print ('WS:CLIENT:NEW')
        self.write_message("WS:CLIENT:CONNECTED")

    def on_message(self, message):
        print ('WS:CLIENT: %s' % message)
        # Message received on the handler
        messageParse = message.split (':', 1)
        
        ## RX
        if message.startswith("RX:"):
            ## Send received to all clients
            self.cl_multicast(message)

        ## RADIO
        if message =="SET:RADIO:RESET":
            ## Reset Radio - LoRa task
            self.write_message("ACK:RADIO:RESET")
            ## Trigger while LoRaRX condition
        
        ## DUMP LORA
        if message =="GET:LORA":
            ## Dump LoRa config
            self.write_message("ACK:GET:LORA")

        ## BEACON
        if message =="SET:BEACON:ON":
            ## Turn me on
            self.write_message("ACK:BEACON:ON")
            ## Add a beacon coroutine
        elif message =="SET:BEACON:OFF":
            ## Turn me off
            self.write_message("ACK:BEACON:OFF")
            ## Add a beacon coroutine
        
        ## TXPWR
        if message =="SET:TXPWR:LOW":
            ## Turn me on
            self.write_message("ACK:TXPWR:LOW")
            ## Add a beacon coroutine
        elif message =="SET:TXPWR:MEDIUM":
            ## Turn me off
            self.write_message("ACK:TXPWR:MEDIUM")
            ## Add a beacon coroutine
        elif message =="SET:TXPWR:HIGH":
            ## Turn me off
            self.write_message("ACK:TXPWR:HIGH")
            ## Add a beacon coroutine
        
        ## CHANNELS
        if message.startswith("SET:TUNER:"):
            self.write_message("ACK:SET:TUNER")
            messageParse = message.split (':')
            localjunk = messageParse[0]
            localjunk = messageParse[1]
            modemconfig = messageParse[2]
            frequency = int(messageParse[3])
            ## Trigger while LoRaRX condition
        
        ## TX
        if message.startswith("TX:"):
            ## read channel info then set
            self.write_message("ACK:" + message)
            message = message.lstrip("TX:")
            HASit.transmit(message)
    
    def on_close(self):
        wsxCLIENTS.remove(self)
        print ('WS:CLIENT:CLOSED')
        gc.collect()


class HASviolet(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            while not HASit.rfm.available():
                pass
            HASit.receive = HASit.rfm.recv()
            HASit.receive_rssi = str(int(HASit.rfm.last_rssi))
            HASit.receive_string = str(HASit.receive)
            HASit.receive_ascii=""
            for i in HASit.receive:
                HASit.receive_ascii=HASit.receive_ascii+chr(i)
            rx_oled_scroll()
            WebSocketHandler.on_rxradio("RX:" + HASit.receive_ascii)


#
# GLOBAL FUNCTIONS
#

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by username"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def find_user(user):
    userfound=""
    f = open(HASvioletpwf, "r")
    flines = f.readlines()
    for fl in flines:
        fluser = fl.split(":")
        if user == fluser[0]:
            userfound = fluser[0]
    f.close()
    return (userfound)

def find_password(user):
    userpassword = ""
    f = open(HASvioletpwf, "r")
    flines = f.readlines()
    for fl in flines:
        fluser = fl.split(":")
        if user == fluser[0]:
            userpassword = (fluser[1]).rstrip()
    f.close()
    return (userpassword)

def rx_oled_scroll():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text("RSSI: " + HASit.receive_rssi, 0, 0, 1)
    HAShat.OLED.text(HASit.receive_ascii[0:20], 0, 8, 1)
    HAShat.OLED.text(HASit.receive_ascii[20:40], 0, 16, 1)
    HAShat.OLED.text(HASit.receive_ascii[40:60], 0, 24, 1)
    HAShat.OLED.text(HASit.receive_ascii[60:73], 0, 32, 1)
    HAShat.OLED.show()

def main():
    tornado.options.parse_command_line()

    settings = {
        "cookie_secret":"gWsdN18jkIWNmksfh2poINsJxZZ83Vo=",
        "login_url": "/login",
    }

    app = tornado.web.Application(
        handlers=[
            ('/wss', WebSocketHandler),
            ('/', MainHandler),
            ('/login', LoginHandler),
            ('/css/(.*)', tornado.web.StaticFileHandler, {'path': 'server/static/'}),
            ('/js/(.*)', tornado.web.StaticFileHandler, {'path': 'server/static/'}),
            ('/cfg/(.*)', tornado.web.StaticFileHandler, {'path': 'cfg/'}),
            ('/msgs/(.*)', tornado.web.StaticFileHandler, {'path': 'server/msgs/'}),
            ('/(.*)', tornado.web.StaticFileHandler, {'path': 'server/static/'})
        ], **settings
    )
    
    httpServer = tornado.httpserver.HTTPServer(app,
        ssl_options = {
            "certfile": os.path.join("cfg/HASviolet.crt"),
            "keyfile": os.path.join("cfg/HASviolet.key"),
        }
    )

    httpServer.listen(options.port)
    print (" ")
    print ("HASviolet Websox Server started: listening on port:", options.port)
    print (" ")
    
    ##threadRX = threading.Thread(target=HASviolet, name=HASvRX)
    ##threadRX.start()
    threadRX = HASviolet()
    threadRX.start()

    tornado.ioloop.IOLoop.instance().start()


#
# MAIN
#

HASit = HASrf()
HAShat = HAShid()
HASsess = HASsession()
HASit.startradio()
main()
