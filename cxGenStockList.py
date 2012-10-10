################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : cxGenStockList.py
# date        : 2012-09-16 19:35:35
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

from cxCybosPlus    import cxCpStockCode
from cxCybosPlus    import cxCpStockMst
from cxCybosPlus    import cxCpStockMstM
from cxCybosPlus    import cxCpStockMst2
from cxCybosPlus    import constants
import codecs
import time
import os

"""
cxStockCodeList
    reset(), update(), save(), load(), 
    getData(), getNum(), getCategory(), getDataString(), getUpdateTime(),
    dump()
"""
class cxStockCodeList :

    def __init__ ( self ) :
        self.data = []
        self.num = 0
        self.updateTime = ''
        self.category = ['stockCode','stockName','stockFullCode']
    
    def __del__ ( self ) :
        pass

    def getUpdateTime( self ) :
        return self.udpateTime

    def getNum( self ) :
        return self.num

    def getCategory( self ) :
        return self.category
   
    def reset( self ) :
        if self.data != [] and self.data != None :
            del self.data
        self.data = []
        self.num = 0
        
    def update( self ) :
        self.reset()
        cpStockCode = cxCpStockCode()
        self.num = cpStockCode.GetCount() + 1   # add 0'th stock item

        for i in range( 0, self.num ) :
            stockItem = []
            stockItem.append( cpStockCode.GetData( 0, i ) )     # stockCode
            stockItem.append( cpStockCode.GetData( 1, i ) )     # stockName
            stockItem.append( cpStockCode.GetData( 2, i ) )     # stockFullCode
            self.data.append( stockItem )
        
        self.updateTime = unicode(time.strftime('%Y%m%d%H%M%S'))

        del cpStockCode

    def getData( self ) :
        return self.data

    def getDataString( self ) :
        if self.num <= 0 : return None
        
        string = ''
        for i in range( 0, len(self.category) ) :
            string += self.category[i]
            if i == len(self.category) - 1 :
                string += u'\n'
            else : string += u'\t'

        for i in range( 0, self.num ) :
            for j in range( 0, 3 ) :
                string += self.data[i][j]
                if j == 2 : string += u'\n'
                else      : string += u'\t'

        return string

    def save( self, path = u'.', fileName = u'stockCodeList.txt' ) :
        directory = os.path.dirname( path + u'\\' + fileName )
        if not os.path.exists(directory) :
            os.makedirs(directory)

        try :
            saveFile = codecs.open( path + u'\\' + fileName, 'w', 'utf-8' )
        except :
            return False

        saveString = self.getDataString()
        if saveString is None : return False
        saveFile.write( self.updateTime + u'\n' )       # updateTime
        saveFile.write( unicode( self.num ) + u'\n' )   # total amount of stock code list
        saveFile.write( saveString )
        saveFile.close()
        return True

    def load( self, path = u'.', fileName = u'stockCodeList.txt' ) :
        directory = os.path.dirname( path + u'\\' + fileName )
        if not os.path.exists(directory) :
            return False

        try :
            loadFile = codecs.open( path + u'\\' + fileName, 'r', 'utf-8' )
        except :
            return False

        self.reset()

        stockItem = []

        self.updateTime = loadFile.readline()
        self.updateTime = self.updateTime[:-1]
        self.num = int(loadFile.readline())
        categories = loadFile.readline()
        for i in range( 0, self.num ) :
            line = loadFile.readline()
            line = line[:-1]
            stockItem = line.split(u'\t')
            self.data.append(stockItem)

        del stockItem
        loadFile.close()
        return True

    def backup( self, path = u'.\\backup', fileName = u'stockCodeList_' + \
                                              unicode(time.strftime('%Y%m%d%H%M%S')) + \
                                              u'.txt' ) :
        self.save( path, fileName )

    def dump( self ) :
        print 'updateTime : ', self.updateTime
        print 'num        : ', self.num

        for i in range( 0, 3 ) :
            print self.category[i],
            if i == 2 : print

        for i in range( 0, self.num ) :
            for j in range( 0, 3 ) :
                print self.data[i][j],
            print


class cxStock :
    code = ''
    name = ''
    fullCode = ''
    curPrice = 0
    netChange = 0                      #전일대비
    status = ''
    marketPrice = 0     #시가
    highPrice = 0       #고가
    offerPrice = 0      #매도호가
    bidPrice = 0        #(long) 매수호가
    volume = 0          #(unsigned long) 거래량 [주의] 단위 1주
    tradingValue = 0    #(long) 거래대금 [주의] 단위 천원
    totalSellResidualQuentity = 0                   #(long) 총매도잔량
    totalBuyResidualQuentity = 0                        #(long) 총매수잔량
    SellResidualQuentity = 0                        #(long) 매도잔량
    BuyResidualQuentity = 0                        #(long) 매수잔량
    numListedStock = 0                               #(unsigned long) 상장주식수
    ratioForeignerPossession = 0                  #(long) 외국인보유비율(%)
    prevClosingPrice = 0                    #(long) 전일종가
    prevVolume = 0                        #(unsigned long) 전일거래량
    conclusionStrength = 0                    #(long) 체결강도
    numInstantConclusion = 0                    #(unsigned long) 순간체결량
    conclusionPriceCompFlag = ''                    #(char) 체결가비교 Flag
    offerPriceCompFlag = ''                    #(char) 호가비교 Flag
    simultaneousOfferPriceFlag = ''                        #(char) 동시호가구분
    expectedConclusionPrice = 0                     #(long) 예상체결가
    netChangeOfexpectedConclusionPrice = 0                        #(long) 예상체결가 전일대비
                        #(long) 예상체결가 상태구분
                        #(unsigned long) 예상체결가 거래량

    def __init__ ( self, code = '', name = '', fullCode = '' ) :
        self.code = code
        self.name = name
        self.fullCode = fullCode

    def __del__ ( self ) :
        pass

    def dump( self ) :
        print 'code (%s)'% self.code, 
        print 'fullCode (%s)'% self.fullCode,
        print 'name (%s)'% self.name 
#        print self.code, self.name, self.fullCode


class cxStockMgr :
    
    stockCodeList = cxStockCodeList()
    stockDic = {} 

    def __init__ ( self ) :
        pass

    def __del__ ( self ) :
        pass

    def updateStockCodeList( self ) :
        self.stockCodeList.update()

    def saveStockCodeList( self, path = u'.\\', fileName = u'stockCodeList' + \
                                                            u'.txt' ) :
        self.stockCodeList.save( path, fileName )

    def loadStockCodeList( self, path = u'.\\', fileName = u'stockCodeList' + \
                                                            u'.txt' ) :
        self.stockCodeList.load( path, fileName )

    def backupStockCodeList( self ) :
        self.stockCodeList.backup( path = 'backup' )

    def dumpStockCodeList( self ) :
        self.stockCodeList.dump()

    def generateStockDic( self ) :
        if len(self.stockDic) != 0 :
            self.stockDic.clear()

        if self.stockCodeList.num > 0 :
            for i in range( 0, self.stockCodeList.num ) :
                self.stockDic[ self.stockCodeList.data[i][0] ] =    \
                                       cxStock( self.stockCodeList.data[i][0], \
                                                self.stockCodeList.data[i][1], \
                                                self.stockCodeList.data[i][2] ) 

    def dumpStockDic( self ) :
        i = 0
        for key in self.stockDic.keys() :
            print i,
            self.stockDic[key].dump()
            i += 1

        print len(self.stockDic.keys())

    def searchStockCode( self, stockName ) :
        searchedCodes = []
        if self.stockCodeList.num > 0 :
            for i in range( 0 , self.stockCodeList.num ) :
                if self.stockCodeList.data[i][1].find(stockName) >= 0 :
                    searchedCodes.append( [ self.stockCodeList.data[i][0], \
                                            self.stockCodeList.data[i][1] ] )

        return searchedCodes

    #TODO : make stock's detail information with StockMst, StockMstM, StockMst2
    def setStockDetailInfo( self ) :
        cpStockMst = cxCpStockMst()
        cpStockMst2 = cxCpStockMst2()
        cpStockMstM = cxCpStockMstM()

        


        del cpStockMst2
        del cpStockMstM
        del cpStockMst

    #TODO : make history files per stock item with each type(T,D,M,Y) at accumulated style

def test() :
    stockMgr = cxStockMgr()
    stockMgr.updateStockCodeList()
    stockMgr.generateStockDic()
    stockMgr.dumpStockDic()
    del stockMgr

def test01() :
    stockMgr = cxStockMgr()

    option = 2 

    if option == 1 :
        stockMgr.updateStockCodeList()
        stockMgr.saveStockCodeList(path = u'backup')
#        stockMgr.backupStockCodeList()
    elif option == 2 :
        stockMgr.loadStockCodeList(path = u'backup')
#        stockMgr.dumpStockCodeList()
        stockMgr.generateStockDic()
        stockMgr.dumpStockDic()
    else :
        stockMgr.updateStockCodeList()
        name = u'중공업'
        
        for result in stockMgr.searchStockCode( name ) :
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
