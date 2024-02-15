#Jess Quarles (Onyen squarles)
#I pledge the UNC Honor Pledge

import sys
import re

def parse(x):
    print(x, end = "")
    if in_body:
        body(x)
    else:
        if re.compile('^MAIL[ \t]+FROM:.*').match(x):
            if not last_command == "DATA":
                raise UserWarning(503)
            else: mail_from(x)
        elif re.compile('^RCPT[ \t]+TO:.*').match(x):
            if last_command == "DATA":
                raise UserWarning(503)
            else: rcpt_to(x)
        elif re.compile('^DATA[ \t]*$').match(x):
            if not last_command == "TO":
                raise UserWarning(503)
            else: data(x)
        else: raise UserWarning(500)

def mail_from(x):
    y = x
    y = re.split(r'^MAIL[ \t]+FROM:',y)[1]
    y = nullspace(y)
    y = path(y)
    y = CRLF(y)
    global last_command
    last_command = "FROM"
    output = "From: <" + x.split("<")[1].split(">")[0] + ">\n"
    global content
    content += output
    print("250 OK")

def rcpt_to(x):
    y = x
    y = re.split(r'^RCPT[ \t]+TO:',y)[1]
    y = nullspace(y)
    y = path(y)
    y = CRLF(y)
    address = x.split("<")[1].split(">")[0]
    global last_command
    last_command = "TO"
    output = "To: <" + address + ">\n"
    global content
    content += output
    global recipients
    recipients += address
    recipients += "\n"
    print("250 OK")

def data(x):
    y = x
    if not re.compile('^DATA[ \t]*$').match(y):
        raise UserWarning(500)
    global last_command
    last_command = "DATA"
    global in_body
    in_body = 1
    print("354 Start mail input; end with <CRLF>.<CRLF>")

def body(x):
    global in_body
    global content
    global recipients
    if re.compile('^\.$').match(x):
        in_body = 0
        paths = recipients.split("\n")
        for path in paths:
            if path:
                file_path = "forward/" + path
                file = open(file_path, 'a')
                file.write(content)
                file.close()
        content = ""
        recipients = ""
        print("250 OK")
    else:
        in_body = 1
        output = x
        content += output
        return

def whitespace(x):
    if not re.compile('^[ \t]+').match(x):
        raise UserWarning(500)
    return re.split(r'^[ \t]+', x)[1]

def nullspace(x):
    if not re.compile('^[ \t]+').match(x):
        return x
    return re.split(r'^[ \t]+', x)[1]

def path(x):
    y = x
    if not re.compile('^<').match(y):
        raise UserWarning(501)
    y = re.split(r'^<', y)[1]
    y = mailbox(y)
    if not re.compile('^>').match(y):
        raise UserWarning(501)
    y = re.split(r'^>', y)[1]
    return y

def mailbox(x):
    y = x
    y = local_part(y)
    if not re.compile('^@').match(y):
        raise UserWarning(501)
    y = re.split(r'^@', y)[1]
    y = domain(y)
    return y

def local_part(x):
    if not re.compile('^[^ \t<>()\[\]\\.,;:@\"]+').match(x):
        raise UserWarning(501)
    return re.split(r'^[^ \t<>()\[\]\\.,;:@\"]+', x)[1]

def domain(x):
    y = x
    y = element(y)
    while re.compile('^\.').match(y):
        y = re.split(r'^\.', y)[1]
        y = element(y)
    return y

def element(x):
    if not re.compile('^[a-zA-Z][a-zA-Z0-9]*').match(x):
        raise UserWarning(501)
    return re.split(r'^[a-zA-Z][a-zA-Z0-9]*', x)[1]

def CRLF(x):
    if not re.compile('^[ \t]*$').match(x):
        raise UserWarning(501)
    return x

last_command = "DATA"
content = ""
recipients = ""
in_body = 0
for line in sys.stdin:
    try: parse(line)
    except UserWarning as w:
        last_command = "DATA"
        content = ""
        errorMsg = "Oops! This error message shouldn't be possible!"
        if w.args[0] == 500:
            errorMsg = "500 Syntax error: command unrecognized"
        elif w.args[0] == 501:
            errorMsg = "501 Syntax error in parameters or arguments"
        elif w.args[0] == 503:
            errorMsg = "503 Bad sequence of commands"
        print(errorMsg)
if in_body:
    print("501 Syntax error in parameters or arguments")
