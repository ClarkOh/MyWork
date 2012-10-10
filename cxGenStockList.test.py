################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : cxGenStockList.py
# date        : 2012-09-01 18:31:47
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

from cxCybosPlus    import cxCpStockCode
from cxCybosPlus    import cxCpCodeMgr
from cxCybosPlus    import cxStockChart
from cxCybosPlus    import constants
import codecs

def genStockList() :
    stockList = []
    cpStockCode = cxCpStockCode()
    cpCodeMgr   = cxCpCodeMgr()
    stockChart  = cxStockChart()

    stockListNum = cpStockCode.GetCount()

    for i in range(0, stockListNum ) :
        stockInfo = []
        stockInfo.append(cpStockCode.GetData(0, i ))      # stock code 
        stockInfo.append(cpStockCode.GetData(1, i ))      # stock name
        stockInfo.append(cpStockCode.GetData(2, i ))      # full code name
        
        if cpCodeMgr.GetStockKospi200Kind( stockInfo[0] ) > 0 : # KOSPI 200
            if cpCodeMgr.GetStockStatusKind( stockInfo[0] ) == 0 : # 주식 상태 : 정상
                if cpCodeMgr.GetStockSupervisionKind( stockInfo[0] ) == 0 : # 관리 종목 여부 : 일반 종목
                    if cpCodeMgr.GetStockControlKind( stockInfo[0] ) == 0 :
                        stockInfo.append(cpCodeMgr.GetStockListedDate( stockInfo[0] ) )
                        stockList.append(stockInfo)
#        del stockInfo
    
#    for i in range(0, len(stockList) ) :
#        print 'code : ', stockList[i][0], 'name : ', stockList[i][1],  #, 'full : ', stockList[i][2]
#        print 'stocked date : ', stockList[i][3]
    print 'total num : ', len(stockList)

    print 'market start time : ', cpCodeMgr.GetMarketStartTime()
    print 'market end time   : ', cpCodeMgr.GetMarketEndTime()

    print stockList[0][1], int(stockList[0][3]) # 19560303
    
    stockChart.SetInputValue( 0, stockList[0][0] )
#    stockChart.SetInputValue( 1, ord('1') )      # 기간 요청
    stockChart.SetInputValue( 1, ord('2') )     # 개수 요청
    stockChart.SetInputValue( 4, 2800 )
    # Week Max : 1027
    # Day Max : 2800
    # Month Max : 357
    # minute Max : 265
    # tick Max : 1000

#    stockChart.SetInputValue( 2, 20120903 )
#    stockChart.SetInputValue( 2, 20120831 )
#    stockChart.SetInputValue( 2, 20120900 )
#    stockChart.SetInputValue( 3, 19920900 )
#    stockChart.SetInputValue( 3, 19560303 )
#    stockChart.SetInputValue( 3, int(stockList[0][3]) )
#    stockChart.SetInputValue( 3, 19560300 )
#    stockChart.SetInputValue( 2, 20120901 )
#    stockChart.SetInputValue( 3, 20120801 )
#    stockChart.SetInputValue( 3, 20120820 )
#    stockChart.SetInputValue( 4, 1000 )
    fieldList = [ 0, 1, 2, 3, 4, 5, 8 ]
#    fieldList = [ 1, 1, 1, 0, 1, 0, 0 ]
    stockChart.SetInputValue( 5, fieldList )
    stockChart.SetInputValue(10, ord('3') )     # 거래 시간 외 정보 제외
    chartType = 'D' #'D','W','M','m','T'
#    stockChart.SetInputValue( 6, ord('D') )
    stockChart.SetInputValue( 6, ord(chartType) )
    # 'D' : 일, 'W' : 주, 'M' : 월 'm' : 분 'T' : 틱 
    printAll = False

    fileName = stockList[0][0] + '_' + stockList[0][1] + '_' + chartType

#    hFile = open(fileName, 'w')
    hFile = codecs.open(fileName, 'w', 'utf-8')

    print hFile.name

    while stockChart.BlockRequest() == 0 :
        beContinue = stockChart.Continue() 
    
        print 'ChartType : ', chartType
        print 'DibStatus : ', stockChart.GetDibStatus()
        print 'DibMsg1   : ', stockChart.GetDibMsg1()
        print 'Continue  : ', beContinue

        stockCode = stockChart.GetHeaderValue( 0 )
        fieldNum =  stockChart.GetHeaderValue( 1 )
        rowNum = stockChart.GetHeaderValue( 3 )
        fieldNameList = stockChart.GetHeaderValue( 2 ) 

        writeLine = ''
        hFile.write(unicode(stockChart.GetDataValue( 0, 0 )) +
                    unicode(stockChart.GetDataValue( 1, 0 )) + u'\n')
        hFile.write(unicode(stockChart.GetDataValue( 0, (rowNum-1))) +
                    unicode(stockChart.GetDataValue( 1, (rowNum-1))) + u'\n')
        hFile.write(unicode(fieldNum) + u'\n')
        hFile.write(unicode(rowNum) + u'\n')

        for i in range( 0, fieldNum ) :
            hFile.write(fieldNameList[i] + u'\t')       #unicode
        hFile.write(u'\n')
        for i in range( 0, rowNum ) :
            for j in range( 0, fieldNum ) :
                writeLine += unicode(stockChart.GetDataValue( j, i )) + '\t'
            writeLine += '\n'
        writeLine += '\n'

        hFile.write(writeLine)

        if printAll == True :
            for i in range( 0, fieldNum ) :
                print fieldNameList[i],'\t'
            print
            for i in range( 0, rowNum ) :
                for j in range( 0, fieldNum ) :
                    print stockChart.GetDataValue( j, i ),' ',
                print
            print
            print 'code :', stockCode, 
            print ' field : ', fieldNum,
            print ' rowNum : ', rowNum

        else :
            print 'code :', stockCode, 
            print ' field : ', fieldNum,
            print ' rowNum : ', rowNum
            if rowNum == 0 : break
            for i in range( 0, fieldNum ) :
                print fieldNameList[i],'\t'
            print
            for j in range( 0, fieldNum ) :
                print stockChart.GetDataValue( j, 0 ), ' ' ,
            print

            for j in range( 0, fieldNum ) :
                print stockChart.GetDataValue( j, rowNum-1 ), ' ' ,
            print

        if beContinue == 0 : break

    hFile.close()
   
    print type(stockList[0][1]), stockList[0][1]
    """
    readFile = open(fileName, 'r')
    for line in readFile.readlines() :
        print line,
    readFile.close()
    """

    del cpStockCode
    del cpCodeMgr
    del stockChart


def test() :
    genStockList()


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
