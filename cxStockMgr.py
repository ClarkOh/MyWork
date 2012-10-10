################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : cxStockMgr.py
# date        : 2012-10-01 19:07:23
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

from cxCybosPlus    import cxCpStockCode
import codecs
import time

class cxStockMgr :

    def __init__(self) :
        self.stockList = []

    def __del__(self) :
        pass

    def update(self) :
        del self.stockList
        self.stockList = []
        try :
            cpStockCode = cxCpStockCode()
        except : return -1
        stockNum = cpStockCode.GetCount() + 1 
        for i in range( 0, stockNum ) :
            stockItem = []
            stockItem.append( cpStockCode.GetData( 0, i ) )     # stockCode
            stockItem.append( cpStockCode.GetData( 1, i ) )     # stockName
            stockItem.append( cpStockCode.GetData( 2, i ) )     # stockFullCode
            self.stockList.append( stockItem )

        del cpStockCode
        return len( self.stockList)

    def dump(self) :
        dumpString = u''
        for i in range( 0, len( self.stockList ) ) :
            dumpString += self.stockList[i][0] + u'\t' 
            dumpString += self.stockList[i][2] + u'\t'
            dumpString += self.stockList[i][1] + u'\n'
        return dumpString

    def searchStockCode(self, stockName ) :
        stockNum = len( self.stockList )
        if stockNum <= 0 : return []
        resultList = []
        for i in range( 0, stockNum ) :
            if self.stockList[i][1].find( stockName ) >= 0 :
                resultList.append( [ self.stockList[i][0], self.stockList[i][1] ] )
        return resultList


def test() :
    stockMgr = cxStockMgr()

    if stockMgr.update() > 0 :
        print stockMgr.dump()
        for result in stockMgr.searchStockCode( u'삼성' )   :
            print result[0], result[1] 

    del stockMgr


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
