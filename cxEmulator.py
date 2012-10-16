################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : cxEmulator.py
# date        : 2012-10-15 14:19:04
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

from common         import testBlockRequest
from cxCybosPlus    import getCybosPlusClassDic
from cxFile         import cxFile

class cxEmulator :
    cpClsDic = getCybosPlusClassDic() 

    def __init__(self) :
        pass
    
    def __del__(self) :
        pass

    def makeLogData(self, stockCode, chartType ) :

        chartTypeDic = {
            'Day'       : 'D',
            'Week'      : 'W',
            'Month'     : 'M',
            'Minute'    : 'm',
            'Tick'      : 'T'
        }

        try :
            ct = chartTypeDic[chartType]
        except KeyError :
            print 'ERROR: cxEmulator.makeLogData : param chartType : "%s" is not valid.\n'%\
                    (chartType) 
            return False

        fieldList = [ 
            0, # 날짜
            3, # 고가
            4, # 저가
            5, # 종가
            8, # 거래량
            9, # 거래대금
            25, # 주식회전율
        ]

        if ct == 'T' or ct == 'm' :
            fieldList += [1]  # 시간 - hhmm

        paramList = [
            [ 0,    stockCode       ],
            [ 1,    ord(u'1')       ],  # 기간요청
            [ 3,    19500101        ],
            [ 4,    len(fieldList)  ],
            [ 5 ] + fieldList,
            [ 6,    ord(ct)         ],  # 차트종류
            [ 9,    ord(u'1')       ],  # 수정주가
            [ 10,   ord(u'3')       ]   # 시간외거래량 모두 제외
        ]

        stockChart = getCybosPlusDic[u'cxStockChart']

        resultList = templateBlockRequest( stockChart, paramList )

        for result in resultList :
            if getResultDibStatus(result) != 0 :
                break
            # TODO : BEGIN FROM HERE
            

        cpStockCode = self.cpClsDic['cxCpStockCode']

        stockName = cpStockCode.CodeToName(stockCode)
        #print '"%s"'%(stockName)
        if stockName == u'' :
            print 'Can not find stock name for stock code "%s".'%(stockCode)
            return

        path = 'log\\%s\\'%(chartType.lower())

        fileName = u'%s%s_%s.log'%(path,stockCode,stockName)

        print fileName 

        dataFile = cxFile(fileName)

        testBlockRequest(u'cxStockChart', paramList, 0, 0, 1, 1, dataFile)

        dataFile.close()


def test_cxEmulator() :

    emul = cxEmulator()

    emul.makeLogData(u'A000660',u'Day')
    #emul.makeLogData(u'001',u'Day')


def test_getStockDayData() :

    from cxCybosPlus import cxCpStockCode

    from cxFile import cxFile

    #stockCode = u'A000660'  #하이닉스
    #stockCode = u'A005930'  #삼성전자
    stockCode = u'A005380'  #현대자동차
    #stockCode = u'A004990'  #롯데제과

    cpStockCode = cxCpStockCode()

    stockName = cpStockCode.CodeToName(stockCode)

    chartType = u'D'

    fileName = u'%s_%s_%s.log'%(stockCode, stockName, chartType)

    refreshLog = 1 
    
    if refreshLog == 1 :

        resultFile = cxFile(fileName)
   
        fieldList = [ 
            0, # 날짜
            3, # 고가
            4, # 저가
            5, # 종가
            8, # 거래량
            9, # 거래대금
            25, # 주식회전율
        ]

        paramList = [
            [ 0, stockCode ],
            [ 1, ord(u'1') ],
            [ 3, 19920901 ],
            [ 4, len(fieldList) ],
            [ 5 ] + fieldList,
            [ 6, ord(chartType) ],
            [ 9, ord(u'1') ],        # 수정주가
            [ 10, ord(u'3') ]
        ]

        testBlockRequest(u'cxStockChart', paramList, 0, 0, 1, 1, resultFile )

        resultFile.close()
    
    
    resultFile = cxFile(fileName)

    lines = resultFile.readlines()

    """
    value = lines[1].split(u'\t')
    print value
    print value[0], value[3]
    """

    dataLog = []
    
    for i in range(0, len(lines)) :
        if i == 0 : continue
        value = lines[i].split(u'\t')
        #print value[0],value[3]
        dataLog.append( [ value[0], value[3] ] )
    
    resultFile.close()

    dataLogLen = len(dataLog)

    print dataLogLen
    flagBuy = False

    earningMoney = 0

    resultFile = cxFile()
    buyCount = 0
    buyedMoney = 0
    maxBuyedMoney = 0

    for i in range(dataLogLen -1 -20, -1, -1 ) :
        currentValue = int(dataLog[i][1])
        avr = 0
        total = 0
        maxValue = 0
        minValue = 10000000000
        #resultFile.write(u'%d\t'%(i))
        resultFile.write(u'%s\t'%(dataLog[i][0]))
        for j in range(i+20,i,-1) :
            oldValue = int(dataLog[j][1])
            #resultFile.write(u'%d(%s,%d),'%(j,dataLog[i][0],oldValue))
            total += oldValue
            if maxValue < oldValue :
                maxValue = oldValue
            if minValue > oldValue :
                minValue = oldValue
        resultFile.write(u' ')
        avr = int(total/20)
        resultFile.write(u'current:%d,avr:%d,20s min:%d,20s max:%d\n'%( currentValue,
                                                                      avr,
                                                                      minValue,
                                                                      maxValue))
        if (currentValue > maxValue) and (flagBuy == False) :
            resultFile.write(u'BUY at cv:%d for mv:%d in bm:%d (em:%d, bc:%d)\n'%( currentValue, 
                                                                maxValue, 
                                                                buyedMoney,
                                                                earningMoney,
                                                                buyCount))
            flagBuy = True
            buyedMoney += currentValue
            buyCount += 1
            maxBuyedMoney = max(maxBuyedMoney, buyedMoney)
        elif flagBuy == True and currentValue < minValue :
            earningMoney += (currentValue*buyCount)-buyedMoney
            resultFile.write(u'SELL at cv:%d for mv:%d in bm:%d (em:%d, bc:%d)\n'%( currentValue, 
                                                                 minValue, 
                                                                 buyedMoney,
                                                                 earningMoney,
                                                                 buyCount))
            flagBuy = False
            buyCount = 0
            buyedMoney = 0

    resultFile.write(u'earned Money :%d, max buyed money : %d, (%f)\n'%(earningMoney,
                                                                  maxBuyedMoney,
                                                                  float(earningMoney)/float(maxBuyedMoney)*(100.0)))
    resultFile.write(u'%s~%s:%d~%d(%d)\n'%( dataLog[dataLogLen-1][0],
                                            dataLog[0][0],
                                            int(dataLog[dataLogLen-1][1]),
                                            int(dataLog[0][1]),
                                            int(int(dataLog[0][1])/int(dataLog[dataLogLen-1][1]))))

    print

def test() :
    #test_getStockDayData()
    test_cxEmulator()

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
