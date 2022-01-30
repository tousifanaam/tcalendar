from datetime import datetime


class UnderDevError(Exception):
    """Under development error"""
    pass


class NotGregorianError(Exception):
    """
    'The Gregorian calendar is the calendar used in most of the world. 
    It was introduced in October 1582 by Pope Gregory XIII as a modification of, 
    and replacement for, the Julian calendar.' - source Wikipedia
    """
    pass


class Tcalendar:

    MONTHSLIST = [
        'january', 'february', 'march',
        'april', 'may', 'june',
        'july', 'august', 'september',
        'october', 'november', 'december']

    class _ArgCheck:

        null = object()

        def __init__(self, year, month, day, monthslist: list) -> None:

            self.MONTHSLIST = monthslist

            if len([i for i in [year, month, day] if not isinstance(i, str) and not isinstance(i, int)]) != 0:
                raise TypeError("ERR. invalid argument type(s).")

            # year
            try:
                year = int(year)
            except ValueError:
                raise ValueError(
                    "ERR. '{0}' - invalid year!".format(year)) from None
            if year < 0:
                raise ValueError(
                    "ERR. '{0}' - invalid year selected!".format(year))
            self.year = year

            # month
            try:
                month = int(month)
            except ValueError:
                if month.lower() in self.MONTHSLIST:
                    month = self.MONTHSLIST.index(month.lower()) + 1
                elif month.lower()[:3] in (foo := [i.lower()[:3] for i in self.MONTHSLIST]):
                    month = foo.index(month.lower()[:3]) + 1
                else:
                    raise ValueError(
                        "ERR. '{0}' - invalid month selected!".format(month)) from None
            if month < 0 or month > 12:
                raise ValueError(
                    "ERR. '{0}' - invalid month selected!".format(month))
            self.month = month

            # day
            try:
                day = int(day)
            except ValueError:
                raise ValueError(
                    "ERR. '{0}' - invalid date!".format(day)) from None
            if day < 0:
                raise ValueError(
                    "ERR. '{0}' - invalid date selected!".format(day))
            self.day = day

            if (self.year == 1582 and self.month < 10) or self.year < 1582:
                raise NotGregorianError(
                    "The given date does not exist on the Gregorian calender. [year: {}, month: {}]".format(self.year, self.month))

    def __init__(self, year, month, date, escape_values=(0, 0, 0), escape=False):
        """
        initializing the attributes
        """
        if type(escape) != bool:
            raise TypeError("ERR. '{0}' - invalid arg type for escape given!".format(escape))
        else:
            self.escape = escape
        if isinstance(escape_values, tuple) and len(escape_values) == 3 and len(set([type(i) for i in escape_values])) == 1 and len([i for i in escape_values if type(i) == int]) == 3:
            self._escape_values= escape_values
        else:
            raise ValueError(
                "ERR. '{0}' - invalid escape_values selected!".format(escape_values))
        if (year, month, date) == self._escape_values and self.escape:
            self.year, self.month, self.date = self._escape_values
        else:
            foo = self._ArgCheck(year, month, date, self.MONTHSLIST)
            self.year = foo.year
            self.month = foo.month
            self.date = foo.day if foo.day <= self.max_days() else ValueError(
                "ERR. '{0}' - invalid date selected!".format(foo.day))
            if isinstance(self.date, Exception):
                raise self.date

    def __str__(self) -> str:
        def foo(n): return str(n) if n >= 10 else "0" + str(n)
        return "{0}-{1}-{2} {3}".format(foo(self.year), foo(self.month), foo(self.date), self.day())

    def __repr__(self) -> str:
        return "Tcalendar({0}, {1}, {2})".format(self.year, self.month, self.date)

    def leapyear(self) -> bool:
        """
        find a year is leapyear or not
        """
        if self.escape: return
        if self.year % 4 == 0 and self.year % 100 != 0:
            return True
        return self.year % 4 == 0 and self.year % 100 == 0 and self.year % 400 == 0

    def max_days(self) -> int:
        """
        find max days in a month
        """
        if self.escape: return
        if self.leapyear() and self.month == 2:
            return 29
        return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][self.month - 1]

    def day(self, return_int: bool = False) -> str or int:
        """
        find week day of a particular date
        """
        if self.escape: return
        # to find the day of any date
        # formula: D = d + 2m + [3(m+1)/5] + y + [y/4] - [y/100] + [y/400] + 2
        # the values in [] means to drop the remainder and use only the int part
        # then mod 7
        # m - month, y - year, d - day
        # for january and february year = year - 1
        y = self.year - 1 if self.month == 1 or self.month == 2 else self.year
        # for january and february m is 13 and 14 respectively
        m = (12 + self.month) if self.month == 1 or self.month == 2 else self.month
        d = self.date
        day_index = (d + (2 * m) + ((3 * (m + 1)) // 5) + y +
                     (y // 4) - (y // 100) + (y // 400) + 2) % 7
        if return_int:
            return day_index
        return ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', ][day_index].title()

    def cald(self) -> str:
        """
        returns the calendar page of any valid month and year pair
        """
        if self.escape: return
        n = Tcalendar(self.year, self.month, 1).day(return_int=True)
        n = n - 1 if n != 0 else 6
        foo = ["  " for _ in range(
            n)] + ["0{0}".format(i + 1)[-2:] for i in range(self.max_days())]
        bar = [foo[i: i+7] for i in range(0, len(foo), 7)]
        top_part = "\t" + self.MONTHSLIST[self.month - 1].title() + " " + str(self.year) + \
            "\n\nSUN MON TUE WED THU FRI SAT\n --  --  --  --  --  --  --\n "
        res = "\n ".join(["  ".join(i) for i in bar])
        return top_part + res

    def nextday(self) -> object:
        """
        returns a Tcalender object with one day incremented
        """
        if self.escape: return
        y, m, d = self.year, self.month, self.date
        if self.date == self.max_days() and self.month == 12:
            y += 1
            m, d = 1, 1
        elif self.date == self.max_days():
            m += 1
            d = 1
        else:
            d += 1
        return Tcalendar(y, m, d)

    def prevday(self) -> object:
        """
        returns a Tcalender object with one day decremented
        """
        if self.escape: return
        y, m, d = self.year, self.month, self.date
        if d > 1:
            d -= 1
        elif d == 1:
            m = m - 1 if m - 1 > 0 else 12
            d = Tcalendar(y, m, 1).max_days()
            if self.month == 1 and m == 12:
                y -= 1
        return Tcalendar(y, m, d)

    @classmethod
    def today(cls):
        i = str(datetime.today()).split(' ')[0].split('-')
        return cls(i[0], i[1], i[2])

    @classmethod
    def yesterday(cls):
        return cls.today() - 1

    @classmethod
    def tomorrow(cls):
        return cls.today() + 1

    def __add__(self, other):
        if isinstance(other, int):
            if other < 0:
                return self - (-1 * other)
            foo = self
            for _ in range(other):
                foo = foo.nextday()
            return foo
        if isinstance(other, Tcalendar):
            raise UnderDevError("Still working ...")

    def __sub__(self, other):
        if isinstance(other, int):
            if other < 0:
                return self + (-1 * other)
            foo = self
            for _ in range(other):
                foo = foo.prevday()
            return foo
        if isinstance(other, Tcalendar):
            raise UnderDevError("Still working ...")

    def __eq__(self, _o: object):
        return (self.year, self.month, self.date) == (_o.year, _o.month, _o.date)

    def __gt__(self, _o: object):
        if self.year != _o.year:
            return self.year > _o.year
        elif self.month != _o.month:
            return self.month > _o.month
        elif self.date != _o.date:
            return self.date > _o.date
        else:
            return False

    def __lt__(self, _o: object):
        if self.year != _o.year:
            return self.year < _o.year
        elif self.month != _o.month:
            return self.month < _o.month
        elif self.date != _o.date:
            return self.date < _o.date
        else:
            return False

    @staticmethod
    def gen(a, b):
        if a < b:
            while True:
                yield a
                if (a := a.nextday()) == b:
                    break
        elif b < a:
            while True:
                yield a
                if (a := a.prevday()) == b:
                    break

    @classmethod
    def range(cls, t1, t2) -> list:
        return [i for i in cls.gen(t1, t2)]
