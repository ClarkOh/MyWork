################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : commonFunction.py
# date        : 2012-08-10 04:50:24
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

name = u'오진원'

def UNI(param) :
    if isinstance(param,str) is True :
        return unicode(param)
    elif isinstance(param,unicode) is True :
        return param 
    else :
        return unicode(param)

def ASC(param) :
    if isinstance(param,unicode) is True :
        return str(param)
#        return param.encode('ascii')
    elif isinstance(param,str) is True :
        return str
    else :
        return str(param)

def test() :
    testStr1 = u'abs'
    testStr2 = 'abs'
    testStr3 = 1
    testStr4 = u'주문종류코드'
    testStr6 = '계좌번호'

    print 'testStr1 : ',type(testStr1), type(ASC(testStr1)), ASC(testStr1)
    print 'testStr2 : ',type(testStr2), type(UNI(testStr2)), UNI(testStr2)
    print 'testStr3 : ',type(testStr3), type(UNI(testStr3)), UNI(testStr3), type(ASC(testStr3)), ASC(testStr3)
    print testStr4, type(testStr4)
    testStr5 = UNI(testStr4)
    print testStr5, type(testStr5)
    print testStr6

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
