#
# A simple http server for saving hi scores
# pyweek - PyAr2 - Typos Pocus
#

import urllib2
import xml.dom.minidom

HISCORE_SERVER = 'localhost'
HISCORE_PORT = 8000


class HiScoreClient:

    def __init__(self):
        self.__dom = None

    def addHiScore( self, score, name ):
        try:
            urllib2.urlopen('http://%s:%s/addHiScore/%d/%s' % (HISCORE_SERVER,HISCORE_PORT,score,name) )
        except Exception, e:
            print str(e)
            raise Exception("local hiscore not yet implemented")

    def listHiScores( self ):
        try:
            f = urllib2.urlopen('http://%s:%s/listHiScoresInXML'% (HISCORE_SERVER,HISCORE_PORT) )
            document = f.read()
            self.__dom = xml.dom.minidom.parseString(document)

        except Exception, e:
            print str(e)
            raise Exception("local hiscore not yet implemented")

    def handleHiScores(self):
        handleSlideshowTitle(self.__dom.getElementsByTagName("title")[0])
        slides = slideshow.getElementsByTagName("slide")
        handleToc(slides)
        handleSlides(slides)
        print "</html>"

if __name__ == '__main__':
    a = HiScoreClient()
    print a.listHiScores()
#    for i in range(1,100):
#    a.addHiScore(i,'usuario_test_%s' % i )
#    print a.getHiScores()
