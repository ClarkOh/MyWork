################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : commonTemplate.py
# date        : 2012-10-11 17:57:20
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

import sys
from cxError import cxError


reload(sys)
sys.setdefaultencoding('utf-8')



def getHeaderResultString( headerList , titleOption = 0 ) :

    resultString = u''
    if headerList == None : return resultString
    if isinstance(headerList, list) :
        for headerDic in headerList :
            for key in headerDic.keys() :
                if titleOption != 0 :
                    if type(headerDic[key][2]) == tuple :
                        resultString += u'\t%s : (\n'%(headerDic[key][1])
                        for value in headerDic[key][2] :
                            resultString += u'\t\t%s\n'%(value)
                        resultString += u'\t)\n'
                    else :
                        resultString += u'\t%s : %s\n'%(headerDic[key][1], headerDic[key][2])
                else :
                    if type(headerDic[key][2]) == tuple :
                        resultString += u'(\t'
                        for value in headerDic[key][2] :
                            resultString += u'%s\t'%(value)
                        resultString += u')\t'
                    else :
                        resultString += u'%s\t'%(headerDic[key][2])
            if titleOption == 0 :
                resultString += u'\n'

    return resultString

def getDataResultString( dataList , titleOption = 0 ) :

    resultString = u''
    if dataList == None : return resultString
    if isinstance(dataList, list) :
        for dataDic in dataList :
            for key in dataDic.keys() :
                if titleOption != 0 :
                    if type(dataDic[key][2]) == tuple :
                        resultString += u'\t%s : (\n'%(dataDic[key][1])
                        for value in dataDic[key][2] :
                            resultString += u'\t\t%s\n'%(value)
                        resultString += u'\t)\n'
                    else :
                        resultString += u'\t%s : %s\n'%(dataDic[key][1], dataDic[key][2])
                else :
                    if type(dataDic[key][2]) == tuple :
                        resultString += u'(\t'
                        for value in dataDic[key][2] :
                            resultString += u'%s\t'%(value)
                        resultString += u')\t'
                    else :
                        resultString += u'%s\t'%(dataDic[key][2])
            if titleOption == 0 :
                resultString += u'\n'

    return resultString


def dumpResult( resultList ) :

    for dataDic in resultList :
        print u'    {'
        for key in dataDic.keys() :
            print u'        %s = {'%(key)
            for item in dataDic[key] :
                if type(item) == tuple :
                    print u'            ('
                    for value in item :
                        print u'                %s'%(value)
                    print u'            )'
                else :
                    print u'            %s'%(item)
            print u'        }'
        print u'    }'

def getTitleString( dic ) :
    title = u''
    for key in dic :
        title += dic[key][1] + u'\t'
    title += u'\n'
    return title

def getValueString( resultList ) :
    string = u''
    if resultList == None : return string
    for dic in resultList :
        for key in dic.keys() :
            string += u'%s\t'%(dic[key][2])
        string += u'\n'
    string += u'\n'
    return string

def templateSetInputValue( obj, paramList, errLog = sys.stderr ) :

    eCodeDic = { 'OK' : 0, 'cxError' : -1, 'UnknownError' : -2 }

    for param in paramList :
        try :
            if len(param) >= 3 :
                obj.SetInputValue( param[0], param[1:] )
            else :
                obj.SetInputValue( param[0], param[1] )
        except cxError as e :
            if errLog != None :
                errLog.write(u'%s.SetInputValue : %s'%(obj.__class__.__name__, e.desc))
            return eCodeDic['cxError']
        except :
                return eCodeDic['UnknownError']

    return eCodeDic['OK']


def templateBlockRequest( obj, paramList, resultFile = None, errLog = sys.stderr ) :

    if templateSetInputValue( obj, paramList, errLog ) != 0 :
        return []

    bContinue = 1
    resultList = []

    while bContinue == 1 :
        try :
            obj.BlockRequest()
        except cxError as e :
            if errLog != None :
                errLog.write(u'%s.BlockRequest : %s'%(obj.__class__.__name__, e.desc))
            return []

        result = obj.getResult()
        resultList.append(result)

        if resultFile != None :
            resultFile.write(getValueString(result[6]))

        nDibStatus = result[0]
        if ( nDibStatus == -1 ) or ( nDibStatus == 1 ) : # 1 -> waiting, -1 -> error
            if errLog != None :
                errLog.write(result[1])
                return resultList

        bContinue = result[2]
    # end of 'while bContinue == 1'

    return resultList


def test_cxStockChart() :

    from cxCybosPlus import getCybosPlusClassDic        
    from cxLog import cxLog
   
    log = cxLog()
    cpClsDic = getCybosPlusClassDic()
    className = 'cxStockChart'

    fieldList = [ 0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, \
                  14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, \
                  25, 26, 37 ]

    paramList = [ 
        [ 0, u'A000660' ], # 하이닉스
        [ 1, ord('1') ],
        [ 2, 20121010 ],
        [ 3, 20120901 ],
        [ 4, len(fieldList) ],
        [ 5 ] + fieldList,
        [ 6, ord('D') ],
        [ 10, ord('3') ]
    ]

    resultList = templateBlockRequest( cpClsDic[className], paramList )

    for results in resultList :
        log.write( getHeaderResultString(results[5],1 ) )
        log.write( getDataResultString(results[6],1 ) )

    log.close()

    del cpClsDic


def test() :
    test_cxStockChart()

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
