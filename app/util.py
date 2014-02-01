from __future__ import print_function

from datetime import datetime
from dateutil import tz
import smtplib
from email.mime.text import MIMEText


tz_utc = tz.tzutc()
tz_local = tz.tzutc()
dateform = '%Y-%m-%d %H:%M:%S'
__log__ = print

def set_log(func):
    __log__ = func

def set_timezone(timezone):
    tz_local = tz.gettz(timezone)

def set_dateform(form):
    dateform = form

def date_str(date, form):
    date = date.replace(tzinfo=tz_utc)
    date = date.astimezone(tz_local)
    d_str = date.strftime(form)
    return d_str

def totimestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6 


def now_str(form):
    now = datetime.utcnow()
    n_str = date_str(now, form)
    return n_str

def log(*args):
    try:
        msg = u' '.join([unicode(x) for x in args])
        msg = msg.encode('utf-8')
    except Exception as e:
        __log__(e)
        msg =  'invalid msg'
    __log__(now_str(dateform) + ' ' +  msg)


def sendmail(sender, receiver, subject, content, cc=None, bcc=None):
    if type(receiver) == str:
        receiver = [receiver]
    if type(cc) == str:
        cc = [cc]
    if type(bcc) == str:
        bcc = [bcc]

    msg = MIMEText(content, 'html')
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receiver)
    msg['CC'] = COMMASPACE.join(cc)
    msg['BCC'] = COMMASPACE.join(bcc)
    msg['Subject'] = subject

    smtp = conf['smtp']
    s = smtplib.SMTP(smtp['server'], smtp['port'])
    s.starttls()
    s.login(smtp['id'], smtp['pw'])
    s.sendmail(sender, [receivers] + cc + bcc, msg.as_string())
