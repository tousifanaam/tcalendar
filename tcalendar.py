from datetime import datetime
import copy


class UnderDevError(NotImplementedError):
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

    __slots__ = ("year", "month", "date", "__dict__")

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
            if year <= 0:
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
            if month <= 0 or month > 12:
                raise ValueError(
                    "ERR. '{0}' - invalid month selected!".format(month))
            self.month = month

            # day
            try:
                day = int(day)
            except ValueError:
                raise ValueError(
                    "ERR. '{0}' - invalid date!".format(day)) from None
            if day <= 0:
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
            raise TypeError(
                "ERR. '{0}' - invalid arg type for escape given!".format(escape))
        else:
            self.escape = escape
        if isinstance(escape_values, tuple) and len(escape_values) == 3 and len(set([type(i) for i in escape_values])) == 1 and len([i for i in escape_values if type(i) == int]) == 3:
            self._escape_values = escape_values
        else:
            raise ValueError(
                "ERR. '{0}' - invalid escape_values selected!".format(escape_values))
        if (year, month, date) == self._escape_values and self.escape:
            self.year, self.month, self.date = self._escape_values
        else:
            foo = self._ArgCheck(year, month, date, self.MONTHSLIST)
            self.year = foo.year
            self.month = foo.month
            self.date = foo.day if foo.day <= self.maxdays() else ValueError(
                "ERR. '{0}' - invalid date selected!".format(foo.day))
            if isinstance(self.date, Exception):
                raise self.date

    def __str__(self) -> str:
        def foo(n): return str(n) if n >= 10 else "0" + str(n)
        return "{0}-{1}-{2} {3}".format(foo(self.year), foo(self.month), foo(self.date), self.day())

    def __repr__(self) -> str:
        return "Tcalendar({0}, {1}, {2})".format(self.year, self.month, self.date)

    def __hash__(self) -> int:
        return hash((self.year, self.month, self.date))
    
    def deep_copy(self):
        return copy.deepcopy(self)

    def leapyear(self) -> bool:
        """
        find a year is leapyear or not
        """
        if self.escape:
            return
        return (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 4 == 0 and self.year % 100 == 0 and self.year % 400 == 0)

    def month_name(self) -> str:
        if self.escape:
            return
        return self.MONTHSLIST[self.month - 1].title()

    def maxdays(self) -> int:
        """
        find max days in a month
        """
        if self.escape:
            return
        return 29 if self.leapyear() and self.month == 2 else [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][self.month - 1]

    def day(self, return_int: bool = False):
        """
        find week day of a particular date
        """
        if self.escape:
            return
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
        returns the calendar page
        """
        if self.escape:
            return
        _days = [f"{i:02}" for i in range(1, self.maxdays() + 1)]
        _days[self.date - 1] = f"\033[103m\033[30m{self.date:02}\033[0m"
        if Tcalendar(self.year, self.month, 1).day(return_int=True) == 0: _days = ["  " for _ in range(6)] + _days
        else: _days = ["  " for _ in range(1, Tcalendar(self.year, self.month, 1).day(return_int=True))] + _days
        return f"{self.month_name()} {self.year}".center(28) + "\n\nSUN MON TUE WED THU FRI SAT\n--  --  --  --  --  --  --\n" + "\n".join(["  ".join(_days[i: i + 7]) for i in range(0, len(_days) + 1, 7)])

    def nextday(self) -> object:
        """
        returns a Tcalender object with one day incremented
        """
        if self.escape:
            return
        y, m, d = self.year, self.month, self.date
        if self.date == self.maxdays() and self.month == 12:
            y += 1
            m, d = 1, 1
        elif self.date == self.maxdays():
            m += 1
            d = 1
        else:
            d += 1
        return Tcalendar(y, m, d)

    def prevday(self) -> object:
        """
        returns a Tcalender object with one day decremented
        """
        if self.escape:
            return
        y, m, d = self.year, self.month, self.date
        if d > 1:
            d -= 1
        elif d == 1:
            m = m - 1 if m - 1 > 0 else 12
            d = Tcalendar(y, m, 1).maxdays()
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

    def __add__(self, _o):
        if isinstance(_o, int):
            if _o < 0:
                return self - (-1 * _o)
            foo = self
            for _ in range(_o):
                foo = foo.nextday()
            return foo
        if isinstance(_o, Tcalendar):
            raise UnderDevError("Still working ...")

    def __sub__(self, _o):
        if isinstance(_o, int):
            if _o < 0:
                return self + (-1 * _o)
            foo = self
            for _ in range(_o):
                foo = foo.prevday()
            return foo
        if isinstance(_o, Tcalendar):
            raise UnderDevError("Still working ...")

    def __eq__(self, _o: object):
        if not isinstance(_o, Tcalendar):
            raise TypeError("Can only compare Tcalendar with Tcalendar.")
        return (self.year, self.month, self.date) == (_o.year, _o.month, _o.date)

    def __gt__(self, _o: object):
        if not isinstance(_o, Tcalendar):
            raise TypeError("Can only compare Tcalendar with Tcalendar.")
        if self.year != _o.year:
            return self.year > _o.year
        elif self.month != _o.month:
            return self.month > _o.month
        elif self.date != _o.date:
            return self.date > _o.date
        else:
            return False

    def __lt__(self, _o: object):
        if not isinstance(_o, Tcalendar):
            raise TypeError("Can only compare Tcalendar with Tcalendar.")
        if self.year != _o.year:
            return self.year < _o.year
        elif self.month != _o.month:
            return self.month < _o.month
        elif self.date != _o.date:
            return self.date < _o.date
        else:
            return False
        
    def __le__(self, _o: object):
        if not isinstance(_o, Tcalendar):
            raise TypeError("Can only compare Tcalendar with Tcalendar.")
        return self == _o or self < _o
    
    def __ge__(self, _o: object):
        if not isinstance(_o, Tcalendar):
            raise TypeError("Can only compare Tcalendar with Tcalendar.")
        return self == _o or self > _o

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
    def range(cls, t1, t2, step: int = 1) -> list:
        """returns [t1: Tcalendar(y1, m1, d1), ..., t2: Tcalendar(y2, m2, d2) (+-) 1]: list"""
        return [i for i in cls.gen(t1, t2)][::step]

    @staticmethod
    def now():
        """returns Tuple(hour: int, minute: int, second: int)"""
        return tuple(map(lambda x: int(x), str(datetime.today()).split(' ')[1].split('.')[0].split(":")))

    @classmethod
    def maxdays_in_month(cls, y, m) -> int:
        return cls(y, m, 1).maxdays()

    @classmethod
    def fullmonth(cls, y, m):
        res = [(foo := cls(y, m, 1))]
        for _ in range(foo.maxdays() - 1):
            res.append((foo := foo.nextday()))
        return res

    @classmethod
    def fullyear(cls, y):
        res = [(foo := cls(y, 1, 1))]
        for _ in range((366 if foo.leapyear() else 365) - 1):
            res.append((foo := foo.nextday()))
        return res

    @classmethod
    def calendar(cls, y, m) -> str:
        return cls(y, m, 1).cald()

    @classmethod
    def sort(cls, l: list) -> list:
        """
        l: LIST[Tcalendar, ..., Tcalendar]

        returns a sorted list of Tcalendar objects
        """

        def merge(a: list, b: list) -> list:
            x, y, sol = (0, 0, [])
            while True:
                if a[x] < b[y]:
                    sol.append(a[x])
                    x += 1
                elif a[x] > b[y]:
                    sol.append(b[y])
                    y += 1
                elif a[x] == b[y]:
                    sol.append(a[x])
                    sol.append(b[y])
                    x, y = x + 1, y + 1
                if len(a) - 1 < x and len(b) - 1 < y:
                    return sol
                elif len(a) - 1 < x:
                    return sol + foo(b[y:])
                elif len(b) - 1 < y:
                    return sol + foo(a[x:])

        def foo(n: list) -> list:
            if len(n) == 0 or len(n) == 1:
                return n
            else:
                return merge(foo(n[:len(n)//2]), foo(n[len(n)//2:]))

        return foo(l)


class Ttime:

    AM = "AM"
    PM = "PM"
    TIMEDICT = {a*3600 + b*60 + c: (a, b, c) for a in range(24) for b in range(60) for c in range(60)}

    class _Argcheck:

        def __init__(self, h, m, s, me) -> None:

            # meridiem check
            self.tformat = 24
            if me != None and isinstance(me, str):
                self.tformat = 12
                if me.lower() in ['am', 'ante', 'a']:
                    self.meridiem = Ttime.AM
                elif me.lower() in ['pm', 'post', 'p']:
                    self.meridiem = Ttime.PM
            elif me != None and isinstance(me, str):
                raise ValueError(
                    "ERR. '{0}' - invalid meridiem selected! [am:('a', 'am', 'ante'), pm:('p', 'pm', 'post')].".format(me))
            elif not isinstance(me, str) and me != None:
                raise TypeError(
                    "ERR. '{0}' - invalid meridiem type! Should be str.".format(type(me)))
            else:
                self.meridiem = None

            # hour
            if isinstance(h, int):
                if self.tformat == 12:
                    if h >= 1 and h <= 12:
                        self.hour = h
                    else:
                        raise ValueError(
                            "ERR. '{0}' - invalid hour selected! [1 - 12]".format(h))
                elif self.tformat == 24:
                    if h >= 0 and h < 24:
                        self.hour = h
                    else:
                        raise ValueError(
                            "ERR. '{0}' - invalid hour selected! [0 - 23]".format(h))
            else:
                raise TypeError(
                    "ERR. '{0}' - invalid hour type! Should be int.".format(type(h)))

            # minute
            if isinstance(m, int):
                if m >= 0 and m < 60:
                    self.minute = m
                else:
                    raise ValueError(
                        "ERR. '{0}' - invalid minute selected! [0 - 59]".format(m))
            else:
                raise TypeError(
                    "ERR. '{0}' - invalid minute type! Should be int.".format(type(m)))

            # second
            if isinstance(s, int):
                if s >= 0 and s < 60:
                    self.second = s
                else:
                    raise ValueError(
                        "ERR. '{0}' - invalid second selected! [0 - 59]".format(s))
            else:
                raise TypeError(
                    "ERR. '{0}' - invalid second type! Should be int.".format(type(s)))

    def __init__(self, hour: int, minute: int, second: int, meridiem: str = None) -> None:
        foo = self._Argcheck(hour, minute, second, meridiem)
        self.hour = foo.hour
        self.minute = foo.minute
        self.second = foo.second
        self.meridiem = foo.meridiem
        self.tformat = foo.tformat

    @property
    def format(self):
        return self.tformat
    
    @format.setter
    def format(self, f):
        if f == 12 or f == 24:
            if self.format != f:
                if self.format == 12:
                    self.format24()
                elif self.format == 24:
                    self.format12()
        else:
            raise ValueError(f"Ttime format can only be integers of value 12 and 24 not {f}.")

    def __repr__(self) -> str:
        if self.meridiem is None:
            return "Ttime({0}, {1}, {2})".format(self.hour, self.minute, self.second)
        else:
            return "Ttime({0}, {1}, {2}, '{3}')".format(self.hour, self.minute, self.second, self.meridiem)

    def __str__(self) -> str:
        def foo(x): return str(x) if x > 9 else '0' + str(x)
        if self.tformat == 12:
            return "{0}:{1}:{2} {3}".format(foo(self.hour), foo(self.minute), foo(self.second), self.meridiem)
        elif self.tformat == 24:
            return "{0}:{1}:{2}".format(foo(self.hour), foo(self.minute), foo(self.second))
        
    def __hash__(self) -> int:
        return hash((self.hour, self.minute, self.second, self.format))
    
    def deep_copy(self):
        return copy.deepcopy(self)

    @classmethod
    def now(cls):
        """return a Ttime object of the current time in 24 hr format"""
        return cls(*(Tcalendar.now()))

    def format12(self) -> None:
        """set the Ttime format to 12 hr format"""
        if self.tformat == 24:
            if self.hour >= 12:
                if self.hour > 12:
                    self.hour -= 12
                self.meridiem = self.PM
            else:
                if self.hour == 0:
                    self.hour = 12
                self.meridiem = self.AM
            self.tformat = 12

    def format24(self) -> None:
        """set the Ttime format to 24 hr format"""
        if self.tformat == 12:
            if self.meridiem == self.PM and self.hour != 12:
                self.hour += 12
            if self.meridiem == self.AM and self.hour == 12:
                self.hour = 0
            self.meridiem = None
            self.tformat = 24

    def _to_sec(self) -> int:
        if self.tformat == 24:
            return (self.hour * 3600) + (self.minute * 60) + self.second
        else:
            self.format24()
            res = (self.hour * 3600) + (self.minute * 60) + self.second
            self.format12()
            return res

    def __eq__(self, _o):
        if not isinstance(_o, Ttime):
            raise TypeError("Can only compare Ttime to Ttime.")
        return self._to_sec() == _o._to_sec()

    def __gt__(self, _o):
        if not isinstance(_o, Ttime):
            raise TypeError("Can only compare Ttime to Ttime.")
        return self._to_sec() > _o._to_sec()

    def __lt__(self, _o):
        if not isinstance(_o, Ttime):
            raise TypeError("Can only compare Ttime to Ttime.")
        return self._to_sec() < _o._to_sec()
    
    def __le__(self, _o):
        if not isinstance(_o, Ttime):
            raise TypeError("Can only compare Ttime to Ttime.")
        return (a := self._to_sec()) == (b := _o._to_sec()) or a < b
    
    def __ge__(self, _o):
        if not isinstance(_o, Ttime):
            raise TypeError("Can only compare Ttime to Ttime.")
        return (a := self._to_sec()) == (b := _o._to_sec()) or a > b

    @classmethod
    def sort(cls, l: list) -> list:
        """
        l: LIST[Ttime, ..., Ttime]

        returns a sorted list of Tcalendar objects
        """

        def merge(a: list, b: list) -> list:
            x, y, sol = (0, 0, [])
            while True:
                if a[x] < b[y]:
                    sol.append(a[x])
                    x += 1
                elif a[x] > b[y]:
                    sol.append(b[y])
                    y += 1
                elif a[x] == b[y]:
                    sol.append(a[x])
                    sol.append(b[y])
                    x, y = x + 1, y + 1
                if len(a) - 1 < x and len(b) - 1 < y:
                    return sol
                elif len(a) - 1 < x:
                    return sol + foo(b[y:])
                elif len(b) - 1 < y:
                    return sol + foo(a[x:])

        def foo(n: list) -> list:
            if len(n) == 0 or len(n) == 1:
                return n
            else:
                return merge(foo(n[:len(n)//2]), foo(n[len(n)//2:]))

        return foo(l)

    @staticmethod
    def sec_to_hms(seconds: int) -> tuple:
        """returns a tuple. Seconds -> (Hour, Min, Sec)"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        sec = seconds % 60
        return (hours, minutes, sec)
    

class Tcalendar_time:


    class ArgCheck:
        
        def __init__(self, cal: Tcalendar, ti: Ttime) -> None:
            if isinstance(cal, Tcalendar):
                self.cal = cal
            else:
                raise TypeError("Argument [cal] must be a Tcalendar object.")
            if isinstance(ti, Ttime):
                self.ti = ti
            else:
                raise TypeError("Argument [cal] must be a Ttime object.")


    class Seconds:

        SECVAL = 1

        def __init__(self, n: int) -> None:
            if isinstance(n, int) and n >= 0:
                self.value = n
            else:
                raise TypeError("Argument must be an Integer object and greater than or equal to 0.")

        def __str__(self):
            return f"Seconds({self.value})"

        def __repr__(self):
            return self.__str__()

        def __hash__(self):
            return hash(self.value)


    class Minute:

        SECVAL = 60

        def __init__(self, n: int) -> None:
            if isinstance(n, int) and n >= 0:
                self.value = n
            else:
                raise TypeError("Argument must be an Integer object and greater than or equal to 0.")

        def __str__(self):
            return f"Minute({self.value})"

        def __repr__(self):
            return self.__str__()

        def __hash__(self):
            return hash(self.value)


    class Hour:

        SECVAL = 3600

        def __init__(self, n: int) -> None:
            if isinstance(n, int) and n >= 0:
                self.value = n
            else:
                raise TypeError("Argument must be an Integer object and greater than or equal to 0.")

        def __str__(self):
            return f"Hour({self.value})"

        def __repr__(self):
            return self.__str__()

        def __hash__(self):
            return hash(self.value)
        

    class Day:

        SECVAL = 86400

        def __init__(self, n: int) -> None:
            if isinstance(n, int) and n >= 0:
                self.value = n
            else:
                raise TypeError("Argument must be an Integer object and greater than or equal to 0.")

        def __str__(self):
            return f"Day({self.value})"

        def __repr__(self):
            return self.__str__()

        def __hash__(self):
            return hash(self.value)
        

    class Week:

        def __init__(self, n: int) -> None:
            if isinstance(n, int) and n >= 0:
                self.value = n
            else:
                raise TypeError("Argument (n) must be an Integer object and greater than or equal to 0.")
            self.dc = 7 # day_count

        def __str__(self):
            return f"Week({self.value})"

        def __repr__(self):
            return self.__str__()

        def __hash__(self):
            return hash(self.value)
        

    class Month:

        def __init__(self, n: int, default_day_count: int = 30) -> None:
            if isinstance(n, int) and n >= 0:
                self.value = n
            else:
                raise TypeError("Argument (n) must be an Integer object and greater than or equal to 0.")
            if isinstance(default_day_count, int) and default_day_count in (28, 29, 30, 31):
                self.dc = default_day_count # day_count
            else:
                raise TypeError("Argument (default_day_count) must be an Integer object and must be in range [28, 31].")

        def __str__(self):
            return f"Month({self.value})"

        def __repr__(self):
            return self.__str__()

        def __hash__(self):
            return hash(self.value)
        

    class Year:

        def __init__(self, n: int, default_day_count: int = 365) -> None:
            if isinstance(n, int) and n >= 0:
                self.value = n
            else:
                raise TypeError("Argument (n) must be an Integer object and greater than or equal to 0.")
            if isinstance(default_day_count, int) and default_day_count in (365, 366):
                self.dc = default_day_count # day_count
            else:
                raise TypeError("Argument (default_day_count) must be an Integer object and must be in range [365, 366].")

        def __str__(self):
            return f"Year({self.value})"

        def __repr__(self):
            return self.__str__()

        def __hash__(self):
            return hash(self.value)


    def __init__(self, the_date: Tcalendar, the_time: Ttime) -> None:
        foo = self.ArgCheck(the_date, the_time)
        self.cal = foo.cal
        self.ti = foo.ti

    def __repr__(self) -> str:
        return f"Tcalendar_time({repr(self.cal)}, {repr(self.ti)})"
    
    def __str__(self) -> str:
        return f"{self.cal} - {self.ti}"
    
    def __hash__(self) -> int:
        return hash((self.cal, self.ti))
    
    def deep_copy(self):
        return copy.deepcopy(self)
    
    def sub_sec(self, n: int):
        x = self.ti._to_sec() - (n)
        while True:
            if x < 0:
                self.cal -= 1
                x = 86400 + x
            else:
                break
        self.ti = Ttime(*(Ttime.TIMEDICT[x]))

    def add_sec(self, n: int):
        x = self.ti._to_sec() + n
        while x >= 86400:
            self.cal += 1
            x -= 86400
        self.ti = Ttime(*(Ttime.TIMEDICT[x]))

    def __eq__(self, other):
        if not isinstance(other, Tcalendar_time):
            return False
        return self.cal == other.cal and self.ti == other.ti

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, Tcalendar_time):
            return NotImplemented
        if self.cal < other.cal:
            return True
        elif self.cal == other.cal:
            return self.ti < other.ti
        else:
            return False

    def __le__(self, other):
        if not isinstance(other, Tcalendar_time):
            return NotImplemented
        return self < other or self == other

    def __gt__(self, other):
        if not isinstance(other, Tcalendar_time):
            return NotImplemented
        if self.cal > other.cal:
            return True
        elif self.cal == other.cal:
            return self.ti > other.ti
        else:
            return False

    def __ge__(self, other):
        if not isinstance(other, Tcalendar_time):
            return NotImplemented
        return self > other or self == other
    
    def add(self, time_interval):
        if isinstance(time_interval, Tcalendar_time.Seconds):
            self.add_sec(time_interval.value)
        elif isinstance(time_interval, Tcalendar_time.Minute):
            self.add_sec(time_interval.value * time_interval.SECVAL)
        elif isinstance(time_interval, Tcalendar_time.Hour):
            self.add_sec(time_interval.value * time_interval.SECVAL)
        elif isinstance(time_interval, Tcalendar_time.Day):
            self.cal += time_interval.value
        elif isinstance(time_interval, Tcalendar_time.Week):
            self.cal += (time_interval.value * time_interval.dc)
        elif isinstance(time_interval, Tcalendar_time.Month):
            self.cal += (time_interval.value * time_interval.dc)
        elif isinstance(time_interval, Tcalendar_time.Year):
            self.cal += (time_interval.value * time_interval.dc)

    def sub(self, time_interval):
        if isinstance(time_interval, Tcalendar_time.Seconds):
            self.sub_sec(time_interval.value)
        elif isinstance(time_interval, Tcalendar_time.Minute):
            self.sub_sec(time_interval.value * time_interval.SECVAL)
        elif isinstance(time_interval, Tcalendar_time.Hour):
            self.sub_sec(time_interval.value * time_interval.SECVAL)
        elif isinstance(time_interval, Tcalendar_time.Day):
            self.cal -= time_interval.value
        elif isinstance(time_interval, Tcalendar_time.Week):
            self.cal -= (time_interval.value * time_interval.dc)
        elif isinstance(time_interval, Tcalendar_time.Month):
            self.cal -= (time_interval.value * time_interval.dc)
        elif isinstance(time_interval, Tcalendar_time.Year):
            self.cal -= (time_interval.value * time_interval.dc)
