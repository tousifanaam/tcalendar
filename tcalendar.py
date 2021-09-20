#!/usr/bin/env python3
# Module on date representation
# Only for Gregorian Calendars
from datetime import datetime


__author__ = 'Tousif Anaam'
__version__ = '$Revision: 0.0 $'
__date__ = '$Date: 2020-12-05 $'
__source__ = "https://github.com/tousifanaam/tcalendar.git"

class Tcalendar:

    MONTHSLIST = [
        'january', 'february', 'march',
        'april', 'may', 'june',
        'july', 'august', 'september',
        'october', 'november', 'december']

    MONTHSDICT = {
        'january': 31, 'february': 28, 'march': 31, 
        'april': 30, 'may': 31, 'june': 30, 'july': 31, 
        'august': 31, 'september': 30, 'october': 31, 
        'november': 30, 'december': 31,}

    def __init__(self, year, month, date=None):
        self.year = year
        self.month = month
        self.date = date

    def leapyear(self):
        leap_year = False
        if self.year % 4 == 0:
            leap_year = True
            if self.year % 100 == 0:
                leap_year = False
                if self.year % 400 == 0:
                    leap_year = True
        return leap_year

    @property
    def day(self):
        if self.date != None:
            return self.cal(self.year, self.month, self.date)

    @property
    def cald(self):
        return self.calendar(self.year, self.month)

    @staticmethod
    def maximum_days(year, month):
        months_list = Tcalendar.MONTHSLIST
        months_dict = Tcalendar.MONTHSDICT
        if month >= 1 or month <=12:
            selected_month = months_list[month-1]
            max_d_in_m = months_dict[selected_month]
        # for leap year:
        if month == 2:
            checkleapyear = Tcalendar(year, month, 2)
            if checkleapyear.leapyear():
                max_d_in_m = 29
        return max_d_in_m

    @staticmethod
    def cal(year, month, date):
        """
        Returns the day of the week
        for any properly given date
        """

        months_list = Tcalendar.MONTHSLIST
        months_dict = Tcalendar.MONTHSDICT

        str_base_10_numbers = [
            '0', '1', '2', '3', '4', 
            '5', '6', '7', '8', '9',]

        days_list = [
            'saturday', 'sunday', 'monday', 
            'tuesday', 'wednesday', 'thursday', 
            'friday',]

        # input variable type(s) all string or all int
        # too lazy to itterate each condition
        # check variable condition
        if type(date) == str and type(month) == str and type(year) == str:
            ok = 0
            c_date = list(date)
            for i in c_date:
                if i not in str_base_10_numbers:
                    print("--- ERR. Invalid variable type(s). [date]")
            else:
                ok += 1
            c_month = list(month)
            for i in c_month:
                if i not in str_base_10_numbers:
                    print("--- ERR. Invalid variable type(s). [month]")
            else:
                ok += 1
            c_year = list(year)
            for i in c_year:
                if i not in str_base_10_numbers:
                    print("--- ERR. Invalid variable type(s). [year]")
            else:
                ok += 1
            if ok != 3:
                return "failed! [1]"

        # check values
        date = int(date)
        month = int(month)
        year = int(year)
        input_error = 0
        if month < 0 or month > 12:
            print("--- ERR. Invalid value. [month]")
            input_error = 1
        selected_month = months_list[month-1]
        max_d_in_m = months_dict[selected_month]

        # for leap year:
        if month == 2:
            checkleapyear = Tcalendar(year, month, 2)
            if checkleapyear.leapyear():
                max_d_in_m = 29

        if date < 0 or date > max_d_in_m:
            print("--- ERR. Invalid value. [date]")
            input_error = 1
        if input_error != 0:
            return "failed! [2]"

        # If the variables passed the checks
        # good sign

        # to find the day of any date
        # formula: D = d + 2m + [3(m+1)/5] + y + [y/4] - [y/100] + [y/400] + 2
        # the values in [] means to drop the remainder and use only the int part
        # then divide D by 7
        # m - month, y - year, d - day

        # for january and february m is 13 and 14 respectively
        if month == 1:
            month = 13
        elif month == 2:
            month = 14

        if month == 13 or month == 14:
            year = year - 1

        y = year
        m = month
        d = date
        operation_1 = int(3*(m+1)/5)
        operation_2 = int(y/4)
        operation_3 = int(y/100)
        operation_4 = int(y/400)
        operation_5 = d + 2 * m + operation_1 + y + operation_2 - operation_3 + operation_4 + 2
        operation_6 = operation_5 % 7 
            
        week_day = days_list[operation_6]
        return week_day.title()

    @classmethod
    def calendar(cls, year, month):
        """
        returns the calendar page of any valid month and year pair
        """
        months_list = cls.MONTHSLIST
        months_dict = cls.MONTHSDICT

        if type(month) == str:
            try:
                if month.lower() in months_list:
                    month = months_list.index(month.lower()) + 1
            except IndexError:
                pass

        months_list_abr = [
            'jan', 'feb', 'mar',
            'apr', 'may', 'jun',
            'jul', 'aug', 'sept',
            'oct', 'nov', 'dec']

        if type(month) == str:
            try:
                if month.lower() in months_list_abr:
                    month = months_list_abr.index(month.lower()) + 1
            except IndexError:
                pass

        days_pos = {
            'sunday': 1, 'monday': 2, 'tuesday': 3,
            'wednesday': 4, 'thursday': 5, 'friday': 6, 
            'saturday': 7,}

        full_calendar = ""

        # max day in a month
        selected_month = months_list[month-1]
        max_d_in_m = months_dict[selected_month]

        # for leap year:
        if month == 2:
            checkleapyear = cls(year, month, 2)
            if checkleapyear.leapyear():
                max_d_in_m = 29

        day_1 = cls.cal(year, month, 1).lower()
        start_position = days_pos[day_1]

        # 1st line of dates
        current_value = 1
        for i in range(1,8):
            if i == 1 and i < start_position:
                full_calendar += "     "
            elif i < start_position:
                full_calendar += "    "
            elif i == 1 and i == start_position:
                full_calendar += " "
                full_calendar += "0" + str(current_value)
                full_calendar += "  "
                current_value += 1
            elif i >= start_position:
                full_calendar += "0" + str(current_value)
                full_calendar += "  "
                current_value += 1

        # further lines
        full_calendar += "\n"
        while current_value <= max_d_in_m:
            for i in range(1,8):
                if current_value > max_d_in_m:
                    break
                if i == 1:
                    full_calendar += " "
                if current_value < 10:
                    full_calendar += "0" + str(current_value)
                    full_calendar += "  "
                    current_value += 1  
                else:
                    full_calendar += str(current_value)
                    full_calendar += "  "
                    current_value += 1
            full_calendar += "\n"

        month_name = months_list[month-1].title()

        top_part = ""
        top_part += "\t" + str(month_name) + " " + str(year)
        top_part += "\n" + "\nSUN" + " MON" + " TUE" + " WED" + " THU" + " FRI" + " SAT"
        top_part += "\n" + " --  --  --  --  --  --  --\n"
        return top_part + full_calendar

    @classmethod
    def now(cls):
        r = str(datetime.today()).split(' ')
        _date = r[0]
        _day = cls.cal(_date.split('-')[0], _date.split('-')[1], _date.split('-')[2])
        _time = r[1].split('.')[0]
        return "{0} {1} {2}".format(_date, _day, _time)

    @classmethod
    def today(cls):
        r = str(datetime.today()).split(' ')
        _date = r[0]
        _day = cls.cal(_date.split('-')[0], _date.split('-')[1], _date.split('-')[2])
        return "{0} {1}".format(_date, _day)