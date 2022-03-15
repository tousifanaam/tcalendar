from os import system, name
from tcalendar_old import Tcalendar

if name != "posix":
    raise RuntimeError("This OS is not supported.")
foo = Tcalendar.today().split(' ')[0].split('-')[1]
with open("tcal__test.txt", 'w') as f_obj:
    f_obj.write(Tcalendar.calendar())

with open("tcal__test.txt") as f_obj:
    f = [i.rstrip("\n") for i in f_obj.readlines()]

system("echo '' > tcal__test.txt")
for i in f:
    if foo in i.split(' '):
        res = ""
        for x in i.split(' '):
            if x == foo:
                res += "\e[93m{0}\e[0m ".format(x)
            else:
                res += x + " "
        system('echo "{0}" >> tcal__test.txt'.format(res))
    else:
        system('echo "{0}" >> tcal__test.txt'.format(i))

system("cat tcal__test.txt")
system("rm -rf tcal__test.txt")
