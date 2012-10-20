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
from common         import templateBlockRequest
from common         import getResultDibStatus
from common         import getResultDibMsg1
from common         import getResultContinue
from common         import getResultTime
from common         import getResultClassName
from common         import checkFileExist
from cxCybosPlus    import getCybosPlusClassDic
from cxFile         import cxFile

class cxEmulator :
    chartTypeDic = {
            'Day'       : 'D',
            'Week'      : 'W',
            'Month'     : 'M',
            'Minute'    : 'm',
            'Tick'      : 'T'
    }

    cpClsDic = getCybosPlusClassDic() 

    def __init__(self) :
        pass
    
    def __del__(self) :
        pass

    def testStrategy001(self, dataList ) :

        resultFile = cxFile('log\\day\\st01.txt')
        dataListLen = len(dataList)

        if dataListLen == 0 :
            print 'data가 없습니다.'
            return

        desc = u'현재가가\n20일 고가보다 높을 때 사고,\n20일 저가보다 낮을 때 판다.\n'                     
        flagBuy = False
        earningMoney = 0
        buyCount = 0
        buyedMoney = 0
        maxBuyedMoney = 0

        for i in range( 20, dataListLen ) :
            data = dataList[i]
            date = data[0]
            currentValue = int(data[4])
            avr = 0
            total = 0
            maxValue = 0
            minValue = 10000000000
            for j in range( i - 20, i ) :
                oldValue = int(dataList[j][3])
                total += oldValue
                if maxValue < oldValue :
                    maxValue = oldValue
                if minValue > oldValue :
                    minValue = oldValue
            avr = int(total/20)
            resultFile.write(u'%s:current:%d,avr:%d,20s min:%d,20s max:%d\n'%(date,
                                                                      currentValue,
                                                                      avr,
                                                                      minValue,
                                                                      maxValue))

            if (currentValue > maxValue) and (flagBuy == False ) :
                resultFile.write(u'BUY at cv:%d for mv:%d in bm:%d (em:%d, bc:%d)\n' \
                                                            %(currentValue,
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
        resultFile.write(u'%s~%s:%d~%d(%d)\n'%( dataList[0][0],
                                            dataList[dataListLen-1][0],
                                            int(dataList[0][4]),
                                            int(dataList[dataListLen-1][4]),
                                int(int(dataList[dataListLen-1][4])/int(dataList[0][4]))))
        resultFile.write(desc)
        resultFile.close()
        print

    def testStrategy002(self, dataList ) :

        resultFile = cxFile('log\\day\\st02.txt')
        dataListLen = len(dataList)

        if dataListLen == 0 :
            print 'data가 없습니다.'
            return

        desc = u'현재가가\n20일 고가보다 높을 때 사고,\n20일 평균가보다 낮을 때 판다.\n'                     
        flagBuy = False
        earningMoney = 0
        buyCount = 0
        buyedMoney = 0
        maxBuyedMoney = 0

        for i in range( 20, dataListLen ) :
            data = dataList[i]
            date = data[0]
            currentValue = int(data[3])
            avr = 0
            total = 0
            maxValue = 0
            minValue = 10000000000
            for j in range( i - 20, i ) :
                oldValue = int(dataList[j][3])
                total += oldValue
                if maxValue < oldValue :
                    maxValue = oldValue
                if minValue > oldValue :
                    minValue = oldValue
            avr = int(total/20)
            resultFile.write(u'%s:current:%d,avr:%d,20s min:%d,20s max:%d\n'%(date,
                                                                      currentValue,
                                                                      avr,
                                                                      minValue,
                                                                      maxValue))

            if (currentValue > maxValue) and (flagBuy == False ) :
                resultFile.write(u'BUY at cv:%d for mv:%d in bm:%d (em:%d, bc:%d)\n' \
                                                            %(currentValue,
                                                              maxValue,
                                                              buyedMoney,
                                                              earningMoney,
                                                              buyCount))
                flagBuy = True
                buyedMoney += currentValue
                buyCount += 1
                maxBuyedMoney = max(maxBuyedMoney, buyedMoney)
            elif flagBuy == True and currentValue < avr :
                earningMoney += (currentValue*buyCount)-buyedMoney
                resultFile.write(u'SELL at cv:%d for av:%d in bm:%d (em:%d, bc:%d)\n'%( currentValue, 
                                                                 avr, 
                                                                 buyedMoney,
                                                                 earningMoney,
                                                                 buyCount))
                flagBuy = False
                buyCount = 0
                buyedMoney = 0

        resultFile.write(u'earned Money :%d, max buyed money : %d, (%f)\n'%(earningMoney,
                                            maxBuyedMoney,
                                            float(earningMoney)/float(maxBuyedMoney)*(100.0)))
        resultFile.write(u'%s~%s:%d~%d(%d)\n'%( dataList[0][0],
                                            dataList[dataListLen-1][0],
                                            int(dataList[0][3]),
                                            int(dataList[dataListLen-1][3]),
                                int(int(dataList[dataListLen-1][3])/int(dataList[0][3]))))
        resultFile.write(desc)
        resultFile.close()
        print

    def testStrategy003(self, dataList ) :

        resultFile = cxFile('log\\day\\st03.txt')
        dataListLen = len(dataList)

        if dataListLen == 0 :
            print 'data가 없습니다.'
            return

        desc = u'현재가가\n20일 평균가보다 높을 때 사고,\n20일 평균가보다 낮을 때 판다.\n'                     
        flagBuy = False
        earningMoney = 0
        buyCount = 0
        buyedMoney = 0
        maxBuyedMoney = 0

        for i in range( 20, dataListLen ) :
            data = dataList[i]
            date = data[0]
            currentValue = int(data[3])
            avr = 0
            total = 0
            maxValue = 0
            minValue = 10000000000
            for j in range( i - 20, i ) :
                oldValue = int(dataList[j][3])
                total += oldValue
                if maxValue < oldValue :
                    maxValue = oldValue
                if minValue > oldValue :
                    minValue = oldValue
            avr = int(total/20)
            resultFile.write(u'%s:current:%d,avr:%d,20s min:%d,20s max:%d\n'%(date,
                                                                      currentValue,
                                                                      avr,
                                                                      minValue,
                                                                      maxValue))

            if (currentValue > avr) and (flagBuy == False ) :
                resultFile.write(u'BUY at cv:%d for mv:%d in bm:%d (em:%d, bc:%d)\n' \
                                                            %(currentValue,
                                                              avr,
                                                              buyedMoney,
                                                              earningMoney,
                                                              buyCount))
                flagBuy = True
                buyedMoney += currentValue
                buyCount += 1
                maxBuyedMoney = max(maxBuyedMoney, buyedMoney)
            elif flagBuy == True and currentValue < avr :
                earningMoney += (currentValue*buyCount)-buyedMoney
                resultFile.write(u'SELL at cv:%d for av:%d in bm:%d (em:%d, bc:%d)\n'%( currentValue, 
                                                                 avr, 
                                                                 buyedMoney,
                                                                 earningMoney,
                                                                 buyCount))
                flagBuy = False
                buyCount = 0
                buyedMoney = 0

        resultFile.write(u'earned Money :%d, max buyed money : %d, (%f)\n'%(earningMoney,
                                            maxBuyedMoney,
                                            float(earningMoney)/float(maxBuyedMoney)*(100.0)))
        resultFile.write(u'%s~%s:%d~%d(%d)\n'%( dataList[0][0],
                                            dataList[dataListLen-1][0],
                                            int(dataList[0][3]),
                                            int(dataList[dataListLen-1][3]),
                                int(int(dataList[dataListLen-1][3])/int(dataList[0][3]))))
        resultFile.write(desc)
        resultFile.close()
        print

    def testStrategy004(self, dataList ) :

        resultFile = cxFile('log\\day\\st04.txt')
        dataListLen = len(dataList)

        if dataListLen == 0 :
            print 'data가 없습니다.'
            return

        desc = u'현재가가\n20일 고가보다 높을 때 사고 (누적),\n20일 평균가보다 낮을 때 판다.\n'                     
        flagBuy = False
        earningMoney = 0
        buyCount = 0
        buyedMoney = 0
        maxBuyedMoney = 0

        for i in range( 20, dataListLen ) :
            data = dataList[i]
            date = data[0]
            currentValue = int(data[3])
            avr = 0
            total = 0
            maxValue = 0
            minValue = 10000000000
            for j in range( i - 20, i ) :
                oldValue = int(dataList[j][3])
                total += oldValue
                if maxValue < oldValue :
                    maxValue = oldValue
                if minValue > oldValue :
                    minValue = oldValue
            avr = int(total/20)
            resultFile.write(u'%s:current:%d,avr:%d,20s min:%d,20s max:%d\n'%(date,
                                                                      currentValue,
                                                                      avr,
                                                                      minValue,
                                                                      maxValue))

            if (currentValue > maxValue) : #and (flagBuy == False ) :
                resultFile.write(u'BUY at cv:%d for mv:%d in bm:%d (em:%d, bc:%d)\n' \
                                                            %(currentValue,
                                                              maxValue,
                                                              buyedMoney,
                                                              earningMoney,
                                                              buyCount))
                flagBuy = True
                buyedMoney += currentValue
                buyCount += 1
                maxBuyedMoney = max(maxBuyedMoney, buyedMoney)
            elif flagBuy == True and currentValue < avr :
                earningMoney += (currentValue*buyCount)-buyedMoney
                resultFile.write(u'SELL at cv:%d for av:%d in bm:%d (em:%d, bc:%d)\n'%( currentValue, 
                                                                 avr, 
                                                                 buyedMoney,
                                                                 earningMoney,
                                                                 buyCount))
                flagBuy = False
                buyCount = 0
                buyedMoney = 0

        resultFile.write(u'earned Money :%d, max buyed money : %d, (%f)\n'%(earningMoney,
                                            maxBuyedMoney,
                                            float(earningMoney)/float(maxBuyedMoney)*(100.0)))
        resultFile.write(u'%s~%s:%d~%d(%d)\n'%( dataList[0][0],
                                            dataList[dataListLen-1][0],
                                            int(dataList[0][3]),
                                            int(dataList[dataListLen-1][3]),
                                int(int(dataList[dataListLen-1][3])/int(dataList[0][3]))))
        resultFile.write(desc)
        resultFile.close()
        print

    def testStrategy005(self, dataList ) :

        resultFile = cxFile('log\\day\\st05.txt')
        dataListLen = len(dataList)

        if dataListLen == 0 :
            print 'data가 없습니다.'
            return

        desc = u'현재가가\n산 가격의 20% 이상 오를 때 이익실현하고\n산 가격의 5% 이하일 때 청산한다.'                     
        flagBuy = False
        earningMoney = 0
        buyCount = 0
        buyedMoney = 0
        maxBuyedMoney = 0

        for i in range( 20, dataListLen ) :
            data = dataList[i]
            date = data[0]
            currentValue = int(data[3])
            avr = 0
            total = 0
            maxValue = 0
            minValue = 10000000000
            for j in range( i - 20, i ) :
                oldValue = int(dataList[j][3])
                total += oldValue
                if maxValue < oldValue :
                    maxValue = oldValue
                if minValue > oldValue :
                    minValue = oldValue
            avr = int(total/20)
            resultFile.write(u'%s:current:%d,avr:%d,20s min:%d,20s max:%d\n'%(date,
                                                                      currentValue,
                                                                      avr,
                                                                      minValue,
                                                                      maxValue))

            if (currentValue > maxValue) and (flagBuy == False ) :
                resultFile.write(u'BUY at cv:%d for mv:%d in bm:%d (em:%d, bc:%d)\n' \
                                                            %(currentValue,
                                                              maxValue,
                                                              buyedMoney,
                                                              earningMoney,
                                                              buyCount))
                flagBuy = True
                buyedMoney = currentValue
                buyCount += 1
                maxBuyedMoney = max(maxBuyedMoney, buyedMoney)

            elif flagBuy == True and  \
                 ( currentValue > int(float(buyedMoney)*1.2) ) :
                earningMoney += (currentValue*buyCount)-buyedMoney
                resultFile.write(u'SELL at cv:%d for av:%d in > bm:%d (em:%d, bc:%d)\n'%
                                                               ( currentValue, 
                                                                 avr, 
                                                                 int(float(buyedMoney)*1.2),
                                                                 earningMoney,
                                                                 buyCount))
                flagBuy = False
                buyCount = 0
                buyedMoney = 0

            elif flagBuy == True and \
                 ( currentValue < int(float(buyedMoney)*0.95) ):
                earningMoney += (currentValue*buyCount)-buyedMoney
                resultFile.write(u'SELL at cv:%d for av:%d in < bm:%d (em:%d, bc:%d)\n'%
                                                               ( currentValue, 
                                                                 avr, 
                                                                 int(float(buyedMoney)*0.95),
                                                                 earningMoney,
                                                                 buyCount))
                flagBuy = False
                buyCount = 0
                buyedMoney = 0

        resultFile.write(u'earned Money :%d, max buyed money : %d, (%f)\n'%(earningMoney,
                                            maxBuyedMoney,
                                            float(earningMoney)/float(maxBuyedMoney)*(100.0)))
        resultFile.write(u'%s~%s:%d~%d(%d)\n'%( dataList[0][0],
                                            dataList[dataListLen-1][0],
                                            int(dataList[0][3]),
                                            int(dataList[dataListLen-1][3]),
                                int(int(dataList[dataListLen-1][3])/int(dataList[0][3]))))

        resultFile.write(desc)
        resultFile.close()
        print

    def testStrategy006(self, dataList ) :

        resultFile = cxFile('log\\day\\st06.txt')
        dataListLen = len(dataList)

        if dataListLen == 0 :
            print 'data가 없습니다.'
            return

        desc = u'현재가가\n20일 고가의 75%에서 사서, 20일 저가의 125%에서 판다.\n'                     
        flagBuy = False
        earningMoney = 0
        buyCount = 0
        buyedMoney = 0
        maxBuyedMoney = 0

        for i in range( 20, dataListLen ) :
            data = dataList[i]
            date = data[0]
            currentValue = int(data[3])
            avr = 0
            total = 0
            maxValue = 0
            minValue = 10000000000
            for j in range( i - 20, i ) :
                oldValue = int(dataList[j][3])
                total += oldValue
                if maxValue < oldValue :
                    maxValue = oldValue
                if minValue > oldValue :
                    minValue = oldValue
            avr = int(total/20)
            resultFile.write(u'%s:current:%d,avr:%d,20s min:%d,20s max:%d\n'%(date,
                                                                      currentValue,
                                                                      avr,
                                                                      minValue,
                                                                      maxValue))
            buyValue = int(float(maxValue)*0.75)
            sellValue = int(float(minValue)*1.25)
            if (currentValue > buyValue )and (flagBuy == False ) :
                resultFile.write(u'BUY at cv:%d > bv:%d in bm:%d (em:%d, bc:%d)\n' \
                                                            %(currentValue,
                                                              buyValue,
                                                              buyedMoney,
                                                              earningMoney,
                                                              buyCount))
                flagBuy = True
                buyedMoney = currentValue
                buyCount += 1
                maxBuyedMoney = max(maxBuyedMoney, buyedMoney)

            elif flagBuy == True and  \
                 ( currentValue > sellValue ) :
                 #(currentValue < sellValue ) :
                earningMoney += (currentValue*buyCount)-buyedMoney
                resultFile.write(u'SELL at cv:%d < sv:%d in bm:%d (em:%d, bc:%d)\n'%
                                                               ( currentValue, 
                                                                 sellValue,
                                                                 buyedMoney,
                                                                 earningMoney,
                                                                 buyCount))
                flagBuy = False
                buyCount = 0
                buyedMoney = 0



        resultFile.write(u'earned Money :%d, max buyed money : %d, (%f)\n'%(earningMoney,
                                            maxBuyedMoney,
                                            float(earningMoney)/float(maxBuyedMoney)*(100.0)))
        resultFile.write(u'%s~%s:%d~%d(%d)\n'%( dataList[0][0],
                                            dataList[dataListLen-1][0],
                                            int(dataList[0][3]),
                                            int(dataList[dataListLen-1][3]),
                                int(int(dataList[dataListLen-1][3])/int(dataList[0][3]))))

        resultFile.write(desc)
        resultFile.close()
        print

    def loadLogData(self, stockCode, chartType ) :

        try :
            ct = self.chartTypeDic[chartType]
        except KeyError :
            print 'ERROR: cxEmulator.loadLogData : param chartType : "%s" is not valid.\n'%\
                    (chartType) 
            return None

        cpStockCode = self.cpClsDic['cxCpStockCode']

        stockName = cpStockCode.CodeToName(stockCode)
        #print '"%s"'%(stockName)
        if stockName == u'' :
            print 'Can not find stock name for stock code "%s".'%(stockCode)
            return

        path = 'log\\%s\\'%(chartType.lower())

        fileName = u'%s%s_%s.log'%(path,stockCode,stockName)

        print fileName 

        if checkFileExist(fileName) == False : return None

        dataFile = cxFile(fileName)

        tmpList = []
        dataList = []
        i = 0
        for lines in dataFile.readlines() :
            if i < 5 : 
                i += 1
                continue
            tmpList = []
            for item in lines[:-1].split() :
                tmpList.append(item)
            dataList.append(tmpList)
        dataFile.close()
        del dataFile

        #print 'len of dataList', len(dataList) 
        #print dataList[0]
        #print dataList[len(dataList)-1]
        return dataList


    def makeLogData(self, stockCode, chartType ) :

        try :
            ct = self.chartTypeDic[chartType]
        except KeyError :
            print 'ERROR: cxEmulator.makeLogData : param chartType : "%s" is not valid.\n'%\
                    (chartType) 
            return False

        fieldList = [ 
            0, # 날짜
            1, # 시간
            3, # 고가
            4, # 저가
            5, # 종가
            8, # 거래량
            9, # 거래대금
            25, # 주식회전율
        ]

        #if ct == 'T' or ct == 'm' :
        #    fieldList += [1]  # 시간 - hhmm

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

        stockChart = getCybosPlusClassDic()[u'cxStockChart']

        resultList = templateBlockRequest( stockChart, paramList )

        if resultList == None :
            print 'templateBlockRequest("cxStockChart"): result is none.\n'
            return False

        if len(resultList) == 0 :
            print 'templateBlockRequest("cxStockChart") : result length is zero.\n'
            return False

        bFirst = 1
        fieldNum = 0
        storeList = []
        dataNum = 0

        for result in resultList :
            if getResultDibStatus(result) != 0 :
                break
            headerList = result[5]
            if len(headerList) == 0 :
                print 'header result is empty.'
                continue
            dataNum += headerList[0][3][2]
            print 'dataNum', dataNum, type(dataNum)
            if bFirst == 1 :
                fieldNum = headerList[0][1][2]
                fieldNameList = headerList[0][2][2]
                print 'fieldNum', fieldNum, type(fieldNum)
                print 'fieldNameList'
                for fieldName in fieldNameList :
                    print fieldName,
                print
                
                storeList.insert(3,fieldNum)
                storeList.insert(4,fieldNameList)

                bFirst = 0

            dataList = result[6]
            print 'len of dataList', len(dataList)

            tmpList = []
            for dataDic in dataList :
                tmpList = [] 
                for fieldType in range( 0, fieldNum ) :
                    key = stockChart.fieldNameDic[fieldNameList[fieldType]]
                    tmpList.append( dataDic[key][2] )
                storeList.append(tmpList)


        storeList.insert(0,dataNum)
        storeList.insert(1,storeList[len(storeList)-1][0])
        storeList.insert(2,storeList[4][0])
        print 'len of storeList',len(storeList)
        #print storeList

        """
        [0] : dataNum
        [1] : start date
        [2] : end date
        [3] : fieldNum
        [4] : field Name List
        [5] ~ : data
        """

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

        dataFile.write('%s\n'%(storeList[0]))
        dataFile.write('%s\n'%(storeList[1]))
        dataFile.write('%s\n'%(storeList[2]))
        dataFile.write('%s\n'%(storeList[3]))

        for fieldName in storeList[4] :
            dataFile.write('%s\t'%(fieldName))
        dataFile.write('\n')
        tmpList = storeList[5:]
        tmpList.reverse()
        for itemList in tmpList :
            for item in itemList :
                dataFile.write('%s\t'%(item))
            dataFile.write('\n')

        dataFile.close()
        del dataFile


def test_cxEmulator() :

    emul = cxEmulator()

    stockCode = u'A000660'
    emul.makeLogData(stockCode,u'Day')
    #dataList = emul.loadLogData(stockCode,u'Day')
    #emul.testStrategy001(dataList)
    #emul.testStrategy002(dataList)
    #emul.testStrategy003(dataList)
    #emul.testStrategy004(dataList)
    #emul.testStrategy005(dataList)
    #emul.testStrategy006(dataList)

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
