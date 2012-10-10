################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : ExampleCodeOfGeneratingObjectFunctionCallWithClassName.py
# date        : 2012-10-08 19:02:36
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

#import sys
#import inspect
#from cxCybosPlus import *

class cHello :
    def __init__(self) :
        pass

    def __del__(self) :
        pass

    def hello(self) :
        print 'hello'

def getCybosPlusClassDic( errLog = None ) :
    import sys
    import inspect
    import cxCybosPlus

    classList = inspect.getmembers(sys.modules['cxCybosPlus'], inspect.isclass)
    classDic = {}
    for classMember in classList :
        if classMember[0] == 'cxCybosBase' or classMember[0] == 'cxCybosBaseWithEvent' :
            continue
        try :
            classDic[classMember[0]] = classMember[1]()
        except TypeError as e :
            if errLog != None : errLog.write(u'%s : %s'%(classMember[0],e.message))
            continue
        except :
            continue
    return classDic

def test_1() :
#    print __name__
#    print sys.modules.keys()
    clsmembers = inspect.getmembers(sys.modules['cxCybosPlus'], inspect.isclass)
    #clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    #print clsmembers
    #tmpObj = clsmembers[0][1]()

#    for clsmember in clsmembers :
#        if clsmember[0] == 'cHello' :       # class name
#            """
            # class code starting address + __init__ call : creating class's object
#            tmpObj = clsmember[1]()         
            # call the hello()
#            tmpObj.hello()
#            del tmpObj
#            """
#            clsmember[1]().hello()

    #makeing dictionary

#    for clsmember in clsmembers :
#        print clsmember[0],

    clsdic = {}
    for clsmember in clsmembers :
        if clsmember[0] == 'cxCybosBase' or clsmember[0] == 'cxCybosBaseWithEvent' :
            continue
        try :
            clsdic[clsmember[0]] = clsmember[1]()
        except TypeError : 
            print 'Error : %s'%clsmember[0]
            continue

        #clsdic['cHello'].hello()

    print clsdic.keys()

    cpStockMst = clsdic['cxCpStockMst']
    print cpStockMst.__class__.__name__
    print cpStockMst.GetDibStatus()

    del clsdic

def test() :
    import inspect
#    print getCybosPlusClassDic()
#    print dir()
#    print type(1).__dict__.items()
    print
    print
    print inspect.getmembers(1)

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
