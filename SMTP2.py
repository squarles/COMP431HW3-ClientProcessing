#Jess Quarles (Onyen squarles)
#I pledge the UNC Honor Pledge

import sys
import re

def parse(x):
    global in_body
    if in_body:
        if re.compile('^From: <.*>$').match(x):
            print(".")
            response = input()
            sys.stderr.write(response + '\n')
            address = x.split("<")[1].split(">")[0]
            print("MAIL FROM: <" + address + ">")
            response = input()
            sys.stderr.write(response + '\n')
            if not re.compile('^250 .*$').match(response):
                raise UserWarning("")
            in_body = 0
        else:
            print(x, end="")
    elif re.compile('^From: <.*>$').match(x):
        address = x.split("<")[1].split(">")[0]
        print("MAIL FROM: <" + address + ">")
        response = input()
        sys.stderr.write(response + '\n')
        if not re.compile('^250 .*$').match(response):
            raise UserWarning("")
    elif re.compile('^To: <.*>$').match(x):
        address = x.split("<")[1].split(">")[0]
        print("RCPT TO: <" + address + ">")
        response = input()
        sys.stderr.write(response + '\n')
        if not re.compile('^250 .*$').match(response):
            raise UserWarning("")
    else:
        print("DATA")
        response = input()
        sys.stderr.write(response + '\n')
        if not re.compile('^354 .*$').match(response):
            raise UserWarning("")
        print(x, end = "")
        in_body = 1

f = open(sys.argv[1], "r")
lines = f.readlines()
in_body = 0
for line in lines:
    try: parse(line)
    except UserWarning as w:
        print("QUIT")
        break
if in_body:
    print(".")
    response = input()
    sys.stderr.write(response + '\n')
    print("QUIT")
