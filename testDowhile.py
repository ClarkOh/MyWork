################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : dowhile.py
# date        : 2012-09-03 21:50:04
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

condition = 1

def setCondition(value) :
    global condition
    condition = value

def testCondition() :
    print 'testing'
    return condition

def doSomeThing() :
    print 'Hi'
    return 1

def doSomeThing2() :
    print 'Bye'

def test() :
    
    while doSomeThing() :
        doSomeThing2()
        setCondition(0)
        testCondition == 0 :
            break

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
