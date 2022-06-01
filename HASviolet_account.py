#!/usr/bin/python3
#
#   HASviolet Account
#
#     USAGE: HASviolet-account.py -s -c -u USER -p PASSWORD
#
#           -s,  --store a new user and password
#           -c,  --check (authenticate) yuser and password
#           -u,  --user
#           -p,  --password
#
#     REVISION: 20220601-0200
#
#


#
# IMPORT LIBRARIES
#

import argparse 
import hashlib
import binascii
import os
import sys
import time

print (" ")

#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HASviolet Hashgen')
parser.add_argument('-s','--store', help='Store Password', action='store_true')
parser.add_argument('-c','--check', help='Check Password', action='store_true')
parser.add_argument('-d','--delete', help='Delete User', action='store_true')
parser.add_argument('-u','--user', help='Username', required=True)
parser.add_argument('-p','--password', help='Password')

args = vars(parser.parse_args())

actionStore = args['store']
actionCheck = args['check']
actionDelete = args['delete']
user = args['user']
entered_password = args['password']


#
# STATICS
#

HASviolet_RXLOCK = False                                               # True = RX is running
HASviolet_TXLOCK = False                                               # True = TX is running
HASviolet_CFGDIR = "~/.config/HASviolet/"                              # Config file is in JSON format
HASviolet_SRVDIR = HASviolet_CFGDIR + "server/"                        # Path to files. Change when Pi
HASviolet_ETC = HASviolet_CFGDIR + "etc/"                              # Config file is in JSON format
HASviolet_CONFIG = HASviolet_CFGDIR + "HASviolet.json"                 # Config file is in JSON format
HASviolet_PWF = HASviolet_ETC + "HASviolet.pwf"                        # Password file  user:hashedpasswd
HASviolet_MSGS = HASviolet_SRVDIR + "msgs/HASviolet.msgs"              # radio writes msgs received here   
HASviolet_LOGIN = HASviolet_SRVDIR + "static/HASviolet_LOGIN.html"
HASviolet_LOGINCSS = HASviolet_SRVDIR + "static/HASviolet_LOGIN.css"
HASviolet_INDEX = HASviolet_SRVDIR + "static/HASviolet_INDEX.html"
HASviolet_INDEXCSS = HASviolet_SRVDIR + "static/HASviolet.css"
HASvioletjs = HASviolet_SRVDIR + "static/HASviolet.js"
HVDN_LOGO = HASviolet_ETC + "HVDN_logo.xbm"


#
# VARIABLES
#


#
# FUNCTIONS
#

def hash_password(entered_password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', entered_password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def save_password(user, stored_password):
    pwfLine = user + ":" + stored_password + "\n"
    f = open(HASviolet_pwf, "a")
    f.write(pwfLine)
    f.close()
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def find_user(user):
    userfound=""
    f = open(HASviolet_PWF, "r")
    flines = f.readlines()
    for fl in flines:
        fluser = fl.split(":")
        if user == fluser[0]:
            userfound = fluser[0]
    f.close()
    return (userfound)

def delete_user(user):
    with open(HASviolet_PWF, "r") as f:
        lines = f.readlines()
    with open(HASviolet_PWF, "w") as f:
        for line in lines:
            fluser = line.split(":")
            if user != fluser[0]:
                f.write(line)
    return

def find_password(user):
    userpassword = ""
    f = open(HASviolet_PWF, "r")
    flines = f.readlines()
    for fl in flines:
        fluser = fl.split(":")
        if user == fluser[0]:
            userpassword = (fluser[1]).rstrip()
    f.close()
    return (userpassword)

#
# MAIN
#

if ((actionCheck == True) and (actionStore == True)):
    sys.exit("Usage error: Choose Store or Check")

if actionCheck == True:
    if find_user(user) == "":
        sys.exit("User not found")
    stored_password = find_password(user)
    verdict = verify_password(stored_password, entered_password)
    if verdict == True:
        print ("True")
    else:
        print ("False")

if actionStore == True:
    provided_hashed = hash_password(entered_password)
    save_password(user, provided_hashed)
    print("Stored in " + HASviolet_PWF)

if actionDelete == True:
    if find_user(user) == "":
        sys.exit("User not found")
    else:
        delete_user(user)
        print (user + " deleted")


