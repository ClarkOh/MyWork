################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : cxStock.py
# date        : 2012-10-06 18:40:05
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

import sys
from cxError import UNI

class cxStock :
    def __init__(self, code = u'', name = u'', fullcode = u'') :
        #print name, type(name)
        self.code = UNI(code)
        self.name = UNI(name)
        self.fullcode = UNI(fullcode)

    def __del__(self) :
        pass

    def dump(self) :
        dumpStr = u'%s %s %s'%(self.code, self.fullcode, self.name)
        return dumpStr


def test() :
    from cxFile import cxFile
    resultFile = cxFile()
    stock = cxStock('A153360','오진원','KR71521304506')
   
    resultFile.write(stock.dump())
    resultFile.write(u'\n')
    resultFile.close()
    del stock

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
