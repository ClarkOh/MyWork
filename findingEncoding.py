# -*- coding: utf-8 -*-

#from cxFile import cxFile
from sets import Set
from encodings.aliases import aliases

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

#resultFile = cxFile()
encodingCodecSet = Set()
#for encodingName in aliases.keys() :
for encodingName in aliases.items() :
    encodingCodecSet.add(encodingName[1].replace('_','-'))
    #string = encodingName[0] + encodingName[1] + '\n'
    #string = encodingName[0] + '\t:\t' + encodingName[1].replace('_','-') + '\n'
    #resultFile.write(string)

#for encodingCodec in encodingCodecSet :
#    string = encodingCodec + '\n'
#    resultFile.write(string)
#resultFile.close()

testString = '¿ÀÁø¿ø'

print testString

import sys
print sys.stdout.encoding

for encodingCodec in encodingCodecSet :
    try :
        uniStr = testString.decode(encodingCodec).encode(sys.stdout.encoding)
#        uniStr = unicode(testString, encodingCodec).encode('utf')
    except :
#        print 'encoding error : %s'%(encodingCodec)
        continue
    print encodingCodec, uniStr

