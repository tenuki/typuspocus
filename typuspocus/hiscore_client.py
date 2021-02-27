"""A simple http server for saving hi scores."""

import os
import xml.dom.minidom
import traceback
from urllib import request

import hiscore_server

HISCORE_SERVER = 'typospocus.servegame.org'
HISCORE_PORT = 8080

hiscore_server.HiScoreData.HISCORE_FILENAME = os.path.expanduser(
    "~/.local/share/typuspocus/hiscores")


class HiScoreClient:

    def __init__(self):
        self.__dom = None
        self.__hiscores = []
        self.__internet = False

    def addLocalHiScore(self, score, name):
        """Add local Hi Scores."""
        data = hiscore_server.Handle(hiscore_server.HiScoreData)
        data.addHiScore(score, name, 'localhost')

    def addHiScore(self, score, name):
        """Add Hi Scores."""
        if self.__internet:
            try:
                request.urlopen(
                    'http://%s:%s/addHiScore/%d/%s' % (HISCORE_SERVER, HISCORE_PORT, score, name))
            except Exception:
                traceback.print_exc()
                print('Internet connection failed... using local hiscores')
                self.__internet = False
                self.addLocalHiScore(score, name)
        else:
            self.addLocalHiScore(score, name)

    def listLocalHiScores(self):
        """List local Hi Scores."""
        data = hiscore_server.Handle(hiscore_server.HiScoreData)
        self.__hiscores = data.listHiScores()

    def listHiScores(self):
        """List Hi Scores."""
        if self.__internet:
            try:
                f = request.urlopen(
                    'http://%s:%s/listHiScoresInXML' % (HISCORE_SERVER, HISCORE_PORT))
                document = f.read()
                self.__dom = xml.dom.minidom.parseString(document)
                self.handleXMLScores()

            except Exception:
                import traceback
                traceback.print_exc()
                print('Internet connection failed... using local hiscores')
                self.__internet = False
                self.listLocalHiScores()
        else:
            self.listLocalHiScores()

        return self.__hiscores

    def handleXMLScores(self):
        self.__hiscores = []
        entries = self.__dom.getElementsByTagName("entry")
        for entry in entries:
            score = entry.getElementsByTagName("score")[0]
            scoreStr = self.getText(score.childNodes)
            name = entry.getElementsByTagName("name")[0]
            nameStr = self.getText(name.childNodes)
            ipaddr = entry.getElementsByTagName("ipaddress")[0]
            ipaddrStr = self.getText(ipaddr.childNodes)
            theTime = entry.getElementsByTagName("when")[0]
            theTimeStr = self.getText(theTime.childNodes)
            self.__hiscores.append((int(scoreStr), nameStr, ipaddrStr, theTimeStr))

    def getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc


if __name__ == '__main__':
    a = HiScoreClient()
    print(a.listHiScores())
    for i in range(1, 100):
        a.addHiScore(i, 'usu,<>,ario_test_%s' % i)
    print(a.listHiScores())
