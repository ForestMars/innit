# handle_invitation.py - Class for handling calendar invitations
# -*- coding: utf-8 -*-
__version__ = '0.1'
# __all__ = ['']

import os
import calendar
import datetime
from datetime import date
from datetime import timedelta
import json
import re
import time
from time import strftime
from types import SimpleNamespace

from common import utils
from lib.calendar_event import CalendarInvite

try:
    from lib.c import kronos as kr
except ImportError:
    from build.src import kronos as kr


CRLF = "\r\n"


def check_day_avail(when) ->str:
    # This message should really be set in app, not api.
    month = kr.get_month_abbr_from_num(when['month'])
    msg = when['Day'] +", "+ month + " "+ when['ord'] +" looks doable."
    return 'yes', msg


def check_date_avail(when) ->str:
    # This message should really be set in app, not api.
    #month = kr.get_month_abbr_from_num(kr.get_int_from_month_name(when['month']))
    #msg = when['weekday'] +", "+ when['month'] +" "+ when['day'] + when['ord'] + " looks doable."
    msg = when['weekday'] +", "+ when['month_name'] +" "+ when['day'] + " looks doable."
    return 'yes', msg


def check_time_avail(when) ->str:
    # This message should really be set in app, not api.
    msg = 'we can schedule a call for ' + when['time_hour'] +":"+ when['time_minutes'] +' '+ when['am_pm'] + ' on ' + when['Day'] +' '+ when['month_name'] +' '+ when['day']
    return 'yes', msg


def send_invite(call) ->None:
    call['login'] = "themarsgroup@googlemail.com"
    invitee = call['email']
    call['attendees'] = ["forest@fractalgradient.com", "themarsgroup@gmail.com", invitee]
    call['organizer'] = "ORGANIZER;CN=organiser:mailto:themarsgroup"+CRLF+" @gmail.com"
    call['fro'] = "Forest Mars <themarsgroup@gmail.com>"
    call['from'] = "Forest Mars <themarsgroup@gmail.com>"
    call['description'] = "Call with Forest Mars"+CRLF


    if call['mins'] == '0':
        call['mins'] == '00' # @FIXME: No longer needed.
    call['time'] = str(call['hour']) + ' ' + str(call['mins'])

    call['Subject'] = 'Calendar Invite from Forest for ' + call['weekday'] +' '+ str(call['month']) + ' ' + str(call['day']) +' at '+ str(call['hour'])+':'+ str(call['mins'])
    cal_date = datetime.date(2020, call['month_no'], call['day'])
    call_time = datetime.time(call['hour'], int(call['mins']))
    call['datetime'] = datetime.datetime.combine(cal_date, call_time)

    invite = CalendarInvite()
    invite.send_invite(call)


def email_tld(email):
    providers = ['aol', 'gmail', 'hotmail', 'yahoo', 'protonmail']
    if any(provider in email for provider in providers):
        if email[-3:] =='aol' or email[-5:]=='gmail' or email[-7:]=='hotmail' or email[-5:]=='yahoo' or email[-10:]=='protonmail':
            return(email + '.com')
    return email

def is_valid_email(email):
    if len(email) > 7:
        #if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
        if re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email, re.I) is not None:
            if re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email, re.I).group() is not None:
                return True
    return False

def check_invite(call):
    """ before sending meeting invite we check to see we have all the info we need """
    req_info = ['who', 'weekday', 'month_name', 'day', 'hour', 'mins']
    missing = [k for k in req_info if k not in call]
    return missing

def update_contacts(name, number):
    log_dir = 'logs/'
    filename = 'call_log.txt'
    filepath = log_dir + filename
    #outfile = open(filename,'wb')
    contacts_dict = {}
    contacts_dict[number] = name
    right_now = strftime("%A, %d %b %Y", time.localtime())
    call_log = right_now + ', ' + number + ', ' + name + "\n"
    #pickle.dump(contacts_dict, outfile)
    utils.append_file(call_log, filepath)
    #outfile.close()


def update_file():
    filename = 'abc/call_log.txt'
    right_now = strftime("%A, %d %b %Y", time.localtime())
    call_log = right_now + ", you got it! \n"    #pickle.dump(contacts_dict, outfile)
    utils.append_file(call_log, filename)

"""
def set_attendees(call_deets) ->None:
    att_name = call_deets['name']
    att_email = call_deets['email']
    call_date_time = call_deets['datetime']
    attendee =  '"' + att_email + '"'
"""



if __name__ == '__main__':
    call = dict(
    	month = 11,
    	day = 1,
    	weekday = 'Sunday',
    	hour = 1,
    	mins = 0,
    	who = 'test',
    	email = 'lostjournals@gmail.com',
        time = '1:00 PM (EST)'
    	)
    send_invite(call)
