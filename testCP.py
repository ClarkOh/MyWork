################################################################################
# -*- coding: utf-8 -*-


# author      : Jinwon Oh
# file name   : testCP.py
# date        : 2012-09-28 17:23:26
# ver         : 
# desc.       : 
# tab size    : set sw=4, ts=4
# python ver. : 2.7.1 Stackless 3.1b3 060516 (release27-maint, Jan  1 2011, 13:04:37) [MSC v.1500 32 bit (Intel)]

# ADD CODES FROM HERE

from cxCybosPlus import cxCpSvrNew7216

def testCpSvrNew7216() :
    cpSvrNew7216 = cxCpSvrNew7216()

    stockCode = 'A005180'
   
    cpSvrNew7216.SetInputValue( '0', stockCode )

    cpSvrNew7216.BlockRequest()

    result = cpSvrNew7216.getResult()

    print 'GetDibStatus', result[0]
    print 'GetDibMsg1', result[1]
    print 'Continue?', result[2]
    if result[2] == 1 : print 'Continue'
    elif result[2] == 0 : print 'End'
    print 'time', result[3]
    print 'class', result[4]

    headerList = result[5]
    dataList = result[6]

    for headerDic in headerList :
        key = headerDic.keys()[0]
        print headerDic[key][1], headerDic[key][2]

    for data in dataList :
        for dataDic in data :
            key = dataDic.keys()[0]
            print dataDic[key][1], dataDic[key][2]

        if raw_input() == 'n' : break

    """
    stockCode = cpSvrNew7216.GetHeaderValue(0)
    count = cpSvrNew7216.GetHeaderValue(1)
    dateTime = cpSvrNew7216.GetHeaderValue(2)

    print u'종목코드\t:', stockCode
    print u'카운트\t\t:', count
    print u'조회일자\t:', dateTime

    raw_input()

    for i in range( 0, count ) :
        print u'일자\t\t:', cpSvrNew7216.GetDataValue( 0, i )
        print u'종가\t\t:', cpSvrNew7216.GetDataValue( 1, i )
        flag = cpSvrNew7216.GetDataValue( 2, i )
        print u'전일대비 Flag\t:',
        if   flag == ord(u'1') : print u'상한'
        elif flag == ord(u'2') : print u'상승'
        elif flag == ord(u'3') : print u'보합'
        elif flag == ord(u'4') : print u'하한'
        elif flag == ord(u'5') : print u'하락'
        elif flag == ord(u'6') : print u'기세상한'
        elif flag == ord(u'7') : print u'기세상승'
        elif flag == ord(u'8') : print u'기세하한'
        elif flag == ord(u'9') : print u'기세하락'
        print u'전일대비\t:', cpSvrNew7216.GetDataValue( 3, i )
        print u'전일대비율\t:', cpSvrNew7216.GetDataValue( 4, i )
        print u'거래량\t\t:', cpSvrNew7216.GetDataValue( 5, i )
        print u'기관매매\t:', cpSvrNew7216.GetDataValue( 6, i )
        print u'기관매매 누적\t:', cpSvrNew7216.GetDataValue( 7, i )
        print u'외국인 순매매\t:', cpSvrNew7216.GetDataValue( 8, i )
        print u'외국인 지분율\t:', cpSvrNew7216.GetDataValue( 9, i )

        if raw_input() == 'n' : break
    """

    del cpSvrNew7216


def test() :
    testCpSvrNew7216()

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
