# kronos.py - Grok time class and other helpful date and time functions that should be made into a a class.
# -*- coding: utf-8 -*-
__version__ = '0.1'
# __all__ = ['']

import os
import calendar
import datetime
from datetime import date
from datetime import timedelta
import difflib
import re
import time
from time import strptime
from types import SimpleNamespace


# @TEST: include passing 0 in unit tests
class Grok():
    """ Class for understanding a datetime from natural speech. """
    def __init__(self):
        #time = when['Time'].lower()
        pass

    ordinals = ('1st', '2md', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th' '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd') # Bug waiting to happen.

    def get_month_abbr_from_num(month_num):
        return calendar.month_abbr(month_num)

    def get_month_name_from_num(month_num):
        month_name = calendar.month_name(month_num)
        return month_name


    def match_month(self, month):
        """ Return None if we can't match the month """
        months = {'jan', 'january', 'feb', 'february', 'mar', 'march', 'apr', 'april', 'may', 'jun', 'june', 'jul', 'july', 'aug' 'august', 'sept', 'september', 'oct', 'october', 'nov', 'november', 'dec', 'december'}
        m = difflib.get_close_matches(month.lower(), months, 1) or None
        return f'{m[0].capitalize()}' if m else None

    def clean_date_str(self, date):
        """ Regex of doom follows. Assumes user doesn't include year when saying date. Because, who talks like that? """
        date_parts = date.split(' ')
        if len(date_parts) == 2:
            # handle cases with a clean month
            try_month = self.match_month(date_parts[0])
            month_try = self.match_month(date_parts[1])
            if try_month:
                date_parts[0] = try_month
                if date_parts[1].isnumeric() and int(date_parts[1]) in range(1,32):
                    return date_parts
                #elif month_parts[1] in self.ordinals:
                elif [ord for ord in ['st', 'nd', 'rd', 'th'] if(ord in date_parts[1])]:
                    date_parts[1] = date_parts[1][:-2]
                    return date_parts # wtf is this
            #elif self.match_month(date_parts[1]): # try euro. Also, this doesn't syntactically match prev if
            elif month_try:
                 if date_parts[0].isnumeric() and int(date_parts[0]) in range(1,32):
                     date_parts[1] = date_parts[0]
                     date_parts[0] = month_try
                     return date_parts
                 elif [ord for ord in ['st', 'nd', 'rd', 'th'] if(ord in date_parts[0])]: # why doesn't Pyton have "orif" ?
                    rev = ''
                    date_parts[0] = date_parts[0][:-2]
                    rev = date_parts[0]
                    date_parts[0] = date_parts[1]
                    date_parts[1] = rev
                    return date_parts # @TOD: FIXME!!!!! #DRY
                # @TODO: handle weird cases with numberic representaions (not month name) but with spaces, not slash or dash
        elif len(date_parts) == 1: # JTN, not implementing case where date format incudes year. Come on, man!
            if '/' in date_parts[0]:
                date_split = date_parts[0].split('/')
                if len(date_split) == 2:
                    if int(date_split[0]) in range(1,13) and int(date_split[1]) in range(1,32):
                        clean_date = get_month_abbr_from_num(date_split[0]) + ' ' + date_split[1]
                        return date_split
                    """ Have no idea why anyone would type a date backwards. """
                    #elif int(date_split[1]) in range(1,13) and int(date_split[0]) in range(1,32):
                    #    clean_date = get_month_abbr_from_num(date_split[1]) + ' ' + date_split[0]
                    #    return
            elif '-' in date_parts[0]:
                date_parts[0] = date_parts[0].replace(' ', '')
                date_split = date_parts[0].split('-')
                if len(date_split) == 2:
                    if int(date_split[0]) in range(1,13) and int(date_split[1]) in range(1,32):
                        clean_date = get_month_abbr_from_num(date_split[0]) + ' ' + date_split[1]
                        return date_split
        elif len(date_parts) > 2:
            """ Workaround for CRF inserting spaces into tokens matching the pattern xx-xx """
            date_parts = ''.join(date_parts)
            date_split = date_parts.split('-')
            if len(date_split) == 2:
                if int(date_split[0]) in range(1,13) and int(date_split[1]) in range(1,32):
                    clean_date = get_month_abbr_from_num(date_split[0]) + ' ' + date_split[1]
                    return date_split
            pass  # Tell user to chill out.


    def clean_time_str(self, time):
        """ Given string representing a time, returns hour and minutes """
        if time == 'noon':
            return '12', '00', 'pm' # special case!
        ampm = ''
        # if str contsins amor pm set when['ampm']  @TODO: upper/lower case
        if 'm' in time:
            time = time.replace('m', '')
        if 'a' in time:
            ampm = 'am'
            time = time.replace('a', '')
        elif 'p' in time:
            ampm = 'pm'
            time = time.replace('p', '')
        # assume somewhat conventional business hours
        elif int(time[:1]) in range(1, 6):
            ampm = 'pm'
        else:
            ampm = 'am'

        # get leftmost part
        t1 = re.findall(r"^\w+",time)
        # all this just to remove ':'  :-p
        seq_type = type(t1[0])
        t1 = seq_type().join(filter(seq_type.isdigit, t1[0]))
        #t2 = time.replace(t1, '', 1) or '00'
        time = time.replace(' ','') # Sadly, entity tokens often come with extra spaces.
        if len(t1) == 1 or len(t1) == 2:
            t2 = time.replace(t1, '', 1) or '00'
            #if t2 == '':
            #    t2 = '00'
            return t1, t2.replace(':',''), ampm
        elif len(t1) == 3:

            return t1[:1], t1[-2:], ampm

        elif len(t1) == 4:
            return t1[:2], t1[2:], ampm

        # if len() == 3 we have our minutes

        # remove all non-numeric characters
        #seq_type= type(t1[0])
        #t1 = seq_type().join(filter(seq_type.isdigit, t1[0]))
        # get remaining minutes

        # CASE: 3p, 3pm
        # if t1 == t2: # they didn't specifiy minutes, so assume o'clock
        if t1 == '': # @TODO: Test me please!
            t2 = '00'
            return t1, t2, ampm

        # CASE: 300p 300p

        # strip double-naught, but no single-naught.
        if t1[-2:] == '00':
            t1 = t1[:-2]

        if len(t1) > 2:
            t2 = t1[-2:]
            t1 = t1.replace(t2, '')

        #elif len(t1) <= 2:
        #    t2 = '00'

        t2 = t2.replace(':','') # kill this please.

        return t1, t2, ampm

        if ampm is None:
            if int(t1) in range (8,12):
                ampm = 'am'
            elif int(t1) in range (1,7):
                ampm = 'pm'

        # no return ? 

def euro_time_to_us(euro_time):
    pass


def cat_date_and_time(date):
    """ Given date and time strings, combines them. """
    try:
        return(datetime.datetime.combine(datetime.date(date), datetime.time(time)))

    except Exception as e:
        print('oops')


def get_todays_date():
    return date.today()


def get_date_from_weekday(weekday: str):
    """ Given a weekday, returns date for the next occurance (date, not datetime)"""
    # @ TODO
    today = date.today()
    today_int = get_int_from_date(date.today().strftime('%Y-%m-%d').split('-')) # Just sayin.

    # Since we're not using a lookup for our weekDay entity, we nned to validate it.
    try:
        day_int = get_int_from_day_name(weekday)
    except Exception as e:
        print("Check spelling of day?")
        return None

    # @TODO: Use Modulo instead of If/Else
    if(day_int > today_int):
        next = today + timedelta(days=(day_int-today_int))
        return next
    elif(day_int < today_int):
        next = today + timedelta(days=(day_int-today_int)+7)
        return next
    elif(day_int == today_int):
        next = today + timedelta(days=7)
        return next


def get_int_from_date(date: list) ->int:
    """ Returns weekday (as int) when given a date as year, month, date """

    return(calendar.weekday(int(date[0]), int(date[1]), int(date[2])))


## Get int functions

def get_int_from_month_name(month: str) ->int:
    """ Returns month as int when given a month as name """
    return int(strptime(month,'%b').tm_mon)


def get_int_from_month_name_full(month: str) ->int:
    """ Returns month as int when given a month as name """
    return int(strptime(month,'%B').tm_mon)

def get_int_from_day_abbr(day: str) ->int:
    """ Expects a 3 letter day abbreviations (%a) and returns the corresponding weekday integer """
    if len(day) == 3:
        try:
            day_int = time.strptime(day).tm_wday
        except Exception as e:
            print("oh noes- ", e)

        return(day_int)
    else:
        print("Not a valid 3 letter day abbreviation")

def get_int_from_day_name(day: str) ->int:
    """ Expects a 3 letter day abbreviations (%a) and returns the corresponding weekday integer. """
    try:
        day_int = time.strptime(day, '%A').tm_wday
    except Exception as e:
        print("oh noes- ", e)

    return day_int if day_int else 0 # Do you see what I see?


def get_day_from_day_number(day_int: int)->str:
    """ Given an integer 0-7, returns the corresponding weekday name abbreviation (%a). """

    try:
        weekday = calendar.day_name[day_int]
        return(weekday)
    except Exception as e:
        print("oh noes- ", e)


def get_month_abbr_from_num(month_num): # not used?
    return calendar.month_abbr[int(month_num)]

def get_month_name_from_num(month_num):
    return calendar.month_name[int(month_num)]


## Days of the month

def get_day_of_month(date):
    """ Assumes date is Little Endian """
    date = str(date).split('-')
    return date[2]

def ordinal_from_int(day):
    """ Given a integer, returns the corresponding ordinal """
    ord = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    return(ord(int(day)))


## Strings - spelling and abbreviations

def get_day_abbr_from_day_name(day):
    pass

def get_day_name_from_day_abbr(day):
    days = {'mon': 'monday', 'tue': 'tuesday', 'wed': 'wednesday', 'thu': 'thursday', 'fri': 'friday', 'sat': 'saturday', 'sun': 'sunday'}
    try:
        len(day) == 3
        return days[day]
    except Exception as e:
        pass


def ord_FULL_from_date(date: str) ->str:
    ymd = str(date).split('-')
    m = get_month_abbr_from_num(int(ymd[1]))
    o = ordinal_from_int(int(ymd[2]))
    return (m + ' the ' + o)

def ord_day_from_date(date: str) ->str:
    ymd = str(date).split('-')
    o = ordinal_from_int(int(ymd[2]))
    return (o)


def get_day_from_alternate_spelling(day):
    """ Given a day that is not the correct 3 letter (%a) abbreviation, fix it with regex. """
    pass


def clean_day_str(day):
    if day is not None: # Well check you out.
        day = day.lower()
        relative_days = ('today', 'tomorrow')
        days = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
        if day == 'today': # @TODO: fuzzy match spelling, or use Duckling.
            today = date.today()
            weekday = today.strftime('%a')
            return(weekday)
        elif day == 'tomorrow':
            tomorrow = datetime.datetime.now()+timedelta(1)
            weekday = tomorrow.strftime('%a')
            return(weekday)
        elif day in days:
            return day
        elif len(day) == 3:
            return get_day_name_from_day_abbr(day)
        else:
            day = difflib.get_close_matches(day.lower(), days, 2) or [day]
            return f'{day[0]}'


def month_abbr_to_full(month_abbr: str) ->str:
    months = {'jan': 'january', 'feb': 'february', 'mar': 'march', 'apr': 'april', 'may': 'may', 'jun': 'june', 'jul': 'july', 'aug': 'august', 'sep': 'september', 'oct': 'october', 'nov': 'november', 'dec': 'december'}
    if month_abbr.lower() in months:
        return months[month_abbr.lower()].capitalize()
    else:
        return month_abbr


def day_abbr_to_full(day: str) ->str:
    days = {'mon': 'monday', 'tue': 'tuesday', 'wed': 'wednesday', 'thu': 'thursday', 'fri': 'friday', 'sat': 'saturday', 'sun': 'sunday'}
    if day.lower() in days:
        return days[day.lower()].capitalize()
    else:
        return day


def get_date_str(date):
    """ Assumes Bigendian dates """
    months = {'jan', 'january', 'feb', 'february', 'mar', 'march', 'apr', 'april', 'may', 'jun', 'june', 'jul', 'july', 'aug' 'august', 'sept', 'september', 'oct', 'october', 'nov', 'november', 'dec', 'december'}
    d, m, y = date.split()
    m = difflib.get_close_matches(m.lower(), months, 1) or [m]
    if len(y) == 2:
        y = '20' + y
    return f'{d} {m[0]} {y}'


# @TODO: These are class methods.
def get_date_parts(when):
    """ Given a dict containing a date, populate it with date parts. Or memoize. """
    when['dom'] = get_day_of_month(when['date'])
    when['ord'] = ordinal_from_int(when['dom'])
    when['date_parts'] = str(when['date']).split('-')
    when['date_y'] = when['date_parts'][0]
    when['date_m'] = when['date_parts'][1]
    when['date_d'] = when['date_parts'][2]

    return when


def biz_hrs(when):
    """ Blithe method assuming local business hours """


def get_date_from_month_and_day(md: list):
    """ Assumes month is a number """
    ymd = '2020-'+md[0]+'-'+md[1]
    return datetime.datetime.strptime(ymd, '%Y-%m-%d')
def get_date_from_month_abbr_and_day(md: list):
    ymd = '2020-'+md[0]+'-'+md[1]
    return datetime.datetime.strptime(ymd, '%Y-%b-%d')
def get_date_from_month_name_and_day(md: list):
    ymd = '2020-'+md[0]+'-'+md[1]
    return datetime.datetime.strptime(ymd, '%Y-%B-%d')


def get_weekday_from_date(dtobj) ->str:
    return datetime.datetime.strftime(dtobj, '%A')


def month_name_and_num(month):
    if month.isnumeric() is True:
        if int(month) in range(1,13): # make this a try/except.
            month_num = month
            month_name = get_month_name_from_num(month)
    #elif len(month) > 3:
    #    month_name = month
    #    month_num = get_int_from_month_name_full(month)
    elif len(month) > 2:
        month_name = month
        month_num = get_int_from_month_name(month[:3])
    else:
        print('add test here')
    return month_num, month_name




if __name__ == '__main__':
    #grok = Grok()
    pass
