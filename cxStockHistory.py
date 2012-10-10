################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : cxStockHistory.py
# date        : 2012-10-03 18:21:27
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

from cxCybosPlus    import cxCpStockMst
from cxCybosPlus    import cxCpStockMstM
from cxCybosPlus    import cxCpStockMst2
from cxCybosPlus    import getCybosPlusClassDic

from cxStockMgr     import cxStockMgr
from cxError        import cxError
from cxLog          import cxLog
import sys
import codecs

def templateBlockRequest( obj, paramList, errLog ) :
    """
    for param in paramList :
        try :
            obj.SetInputValue( param[0], param[1] )
        except cxError as e :
            errLog.write(u'%s.SetInputValue:%s'%(obj.__class__.__name__,e.desc))
            return []
    """

    result = templateSetInputValue( obj, paramList, errLog ) 
    print 'result:',result

    bContinue = 1
    resultList = []

    while bContinue == 1 :
        try :
            obj.BlockRequest()
        except cxError as e :
            errLog.write(u'%s.BlockRequest : %s'%(obj.__class__.__name__, e.desc))
            return []

        result = obj.getResult()
        resultList.append(result)

        #print getValueString(result[6])

        nDibStatus = result[0]
        if ( nDibStatus == -1 ) or ( nDibStatus == 1 ): #-1 : error, 1 : waiting
            errLog.write(result[1])
            return resultList

        bContinue = result[2]

    return resultList

"""
def templateDumpResult( resultList, outputFile, errLog ) :

    for result in resultList :
"""


log = codecs.open('result__.txt','w','utf-8')

class cxStockHistory :
    cpStockMst = cxCpStockMst()
    cpStockMstM = cxCpStockMstM()
    cpStockMst2 = cxCpStockMst2()

    def __init__(self) :
        pass

    def __del__(self) :
        pass

    def getResultString(self, resultList) :
        if resultList is None : return u'' 
        if isinstance(resultList, list) :
            resultString = u'\tGetDibStatus : %d'%(resultList[0]) + u'\n' #GetDibStatus
            resultString +=u'\tGetDibMsg1   : %s'%(resultList[1]) + u'\n' #GetDibMsg1
            resultString +=u'\tContinue     : %d'%(resultList[2]) + u'\n' #Continue
            resultString +=u'\tTime         : %s'%(resultList[3]) + u'\n' #time
            resultString +=u'\tClass Name   : %s'%(resultList[4]) + u'\n' #class name
            if len(resultList[5]) :
                for headerDic in resultList[5] :
                    for key in headerDic.keys() :
                        resultString += u'\t%s : %s'%(headerDic[key][1], headerDic[key][2]) + u'\n'
            if len(resultList[6]) :
                dataList = resultList[6]
                for dataDic in dataList :
                    for key in dataDic.keys() :
                        resultString += u'\t\t%s : %s'%(dataDic[key][1], dataDic[key][2]) + u'\n'

            return resultString
        else : return u''

    def requestStockMst(self, stockCode ) :
        self.cpStockMst.SetInputValue( 0 , stockCode )
        self.cpStockMst.BlockRequest()
        print self.getResultString(self.cpStockMst.getResult())

    def requestStockMstM(self, stockCodeList ) :
        reqStr = u''
        if len(stockCodeList) > 110 :
            print u'StockMstM.Request : MAX(110) : failed\n'
            return False
        for stockCode in stockCodeList :
            reqStr += stockCode

        self.cpStockMstM.SetInputValue( 0, reqStr )
        bContinue = 1
        while bContinue == 1 :
            self.cpStockMstM.BlockRequest()
            resultList = self.cpStockMstM.getResult()
            log.write(self.getResultString(resultList))
            bContinue = resultList[2]
        return True

    def requestStockMst2(self, stockCodeList ) :
        global log

        reqStr = u''
        if len(stockCodeList) > 110 :
            print u'StockMst2.Request : MAX(110) : failed\n'
            return False
        for stockCode in stockCodeList :
            reqStr += stockCode + u','

#        print reqStr
        
        try :self.cpStockMst2.SetInputValue( 0, reqStr )
        except : 
            print 'error'
            return False
        bContinue = 1
        while bContinue == 1 :
            self.cpStockMst2.BlockRequest()
            resultList = self.cpStockMst2.getResult()
            dataList = resultList[6]
            logStr = u''
            for dic in dataList :
                for key in dic.keys() :
                    logStr += u'%s\t'%(dic[key][2])
                logStr += u'\n'
            log.write(logStr)
            bContinue = resultList[2]
        return True

def getTitleString( dic ) :
    if len(dic) :
        title = u''
        for key in dic :
            title += dic[key][1] + u'\t'
        title += u'\n'
        return title
    else : return u''

def getValueString( resultList ) :
    if len( resultList ) :
        string = u''
        for dic in resultList :
            for key in dic.keys() :
                string += u'%s\t'%(dic[key][2])
            string += u'\n'
        string += u'\n'
        return string
    else : return u''

def test_BlockRequest( obj, prm ) :
    obj.SetInputValue(prm[0], prm[1] )

    bContinue = 1
    while bContinue == 1 :
        obj.BlockRequest()
        resultList = obj.getResult()
        if resultList[0] != 0 :
            print resultList[1]
            return
        bContinue = resultList[2]
        print getTitleString(obj.headerIndexDic)
        print getValueString(resultList[5])
        print getTitleString(obj.dataIndexDic)
        print getValueString(resultList[6])

def dumpDic( dic ) :
    for key in dic.keys() :
        print '\t%s = {'%(key)
        print '\t\t',dic[key] 
        print '\t}'

"""
param = [ [ 0, 'A000660' ] , 
          [ 1, '1'], 
          [ 2, 20121010 ], 
          [ 3, 20120901 ],
          [ 4, 
"""
def templateSetInputValue( obj, paramList, errLog ) :

    returnValue = 0

    for param in paramList :
        if len(param) >= 3 :
            try :
                print param[0],'{',param[1:],'}'
                returnValue = obj.SetInputValue( param[0], param[1:] )
            except cxError as e :
                print (u'%s.SetInputValue:%s'%(obj.__class__.__name__, e.desc))
                if errLog != None : 
                    errLog.write(u'%s.SetInputValue:%s'%(obj.__class__.__name__, e.desc))
                                                    
                return returnValue
            except :
                return returnValue
        else :
            try :
                print param[0],':',param[1]
                returnValue = obj.SetInputValue( param[0], param[1] )
            except cxError as e :
                print (u'%s.SetInputValue:%s'%(obj.__class__.__name__, e.desc))
                if errLog != None : 
                    errLog.write(u'%s.SetInputValue:%s'%(obj.__class__.__name__, e.desc))
                                                    
                return returnValue
            except :
                return returnValue

    return returnValue

def test_cpStockChart() :
    cpClsDic = getCybosPlusClassDic()
    clsName = 'cxStockChart'
    try :
        cpClsDic[clsName].SetInputValue(0,'A000660')
    except KeyError :
        print "\'%s\' is not key in CybosPlus Class Dic."%(clsName)
        print 'Please, check the class name in cxCybosPlus.py again.'

    try :
        cpClsDic[clsName].SetInputValue(1,'1')
    except KeyError :
        print "\'%s\' is not key in CybosPlus Class Dic."%(clsName)
        print 'Please, check the class name in cxCybosPlus.py again.'

    


    del cpClsDic

def test_cpStockMsts() :
    errLog = cxLog()
    stockHistory = cxStockHistory()
    stockMgr = cxStockMgr()

    stockMgr.update()

    stockCodeList = u''
    listLen = len(stockMgr.stockList)

    for i in range( 0, listLen ) :
        if ( ( ( i + 1 ) % 110 ) == 0 ) or ( ( i + 1 ) == listLen ) :
            param = []
            param.append( [ 0, stockCodeList ] )
            #print stockCodeList
            #test_BlockRequest( stockHistory.cpStockMst2, param )
            resultList = templateBlockRequest( stockHistory.cpStockMst2, param, errLog )
            stockCodeList = u''
        else :
            stockCodeList += stockMgr.stockList[i][0] + u','

    errLog.close()
    del stockMgr
    del stockHistory


def test_cpStockMst2() :
    global log

    stockHistory = cxStockHistory()
    stockMgr     = cxStockMgr()

#    stockHistory.requestStockMst('A000660')
    reqList = []
    cnt = 0
    stockMgr.update()
#    for stockInfo in stockMgr.stockList :
#        if cnt >= 110 : break
#        else : cnt += 1
#        reqList.append( stockInfo[0] )
    dic = stockHistory.cpStockMst2.dataIndexDic
    title = u''
    for key in dic :
        title += dic[key][1] + u'\t'
    title += u'\n'
    log.write(title)
   
    for stockInfo in stockMgr.stockList :
        if cnt >= 110 :
            #print reqList
            #print len(reqList)
            stockHistory.requestStockMst2(reqList)
            reqList = []
            cnt = 0
#            raw_input('continue?')
        else :
            reqList.append( stockInfo[0] )
            cnt += 1


    if len(reqList) > 0 :
        stockHistory.requestStockMst2(reqList)
        reqList = []
    
#    print len(reqList)

#    stockHistory.requestStockMst2(reqList)

    log.close()
    del stockHistory
    del stockMgr

def test() :
#    test_cpStockMst2()
    test_cpStockMsts()
#    test_cpStockChart()

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
