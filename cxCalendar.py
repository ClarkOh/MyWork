################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : cxCalendar.py
# date        : 2012-10-13 23:57:10
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7 Stackless 3.1b3 060516 (release27-maint, Jul 22 2010, 18:58:18) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

import sys
import calendar

class cxCalendar() :
    def dump(self, year, month) :
        weekName = ['MON','TUE','WED','THU','FRI','SAT','SUN']
        matrix = calendar.monthcalendar(year,month)

        """
        print year, month
        for week in matrix :
            for day in week :
                print '%02s'%(day),
            print
        """
        print

        print '%s (%s) %d\n'%(calendar.month_name[month],month,year)

        for day in weekName :
            print day,
        print
        
        for week in matrix :
            for day in week :
                if day == 0 :
                    print '%03s'%(' '),
                else :
                    print '%03s'%(day),
            print
        print

        print calendar.isleap(year)
        calendar.prmonth(year,month)

def test() :
    myCalendar = cxCalendar()
    myCalendar.dump(2012, 9)
    myCalendar.dump(2012,10)
    myCalendar.dump(2012,11)
    myCalendar.dump(2012,12)
    myCalendar.dump(2012, 2)


def collect_and_show_garbage() :
	"Show what garbage is present."
	print "Collecting..."
	n = gc.collect()
	print "Unreachable objects:", n
	if n > 0 : print "Garbage:"
	for i in range(n):
		print "[%d] %s" % (i, gc.garbage[i])

if __name__ == "__main__" :
	import gc

	gc.set_debug(gc.DEBUG_LEAK)

	print "before"
	collect_and_show_garbage()
	print "testing..."
	print "-"*79

	test()

	print "-"*79
	print "after"
	collect_and_show_garbage()

	raw_input("Hit any key to close this window...")
