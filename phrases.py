# -*- coding: utf-8 -*-
#
# A simple phrase generator using a modifiable grammar

import random
import string
from string import Template

grammar = {
'preposition' : ["aboard","about","above","absent","across","after","against","along","alongside","amid","amidst","among","amongst","around","as","at","atop","before","behind","below","beneath","beside","besides","between","beyond","by","despite","down","during","except","following","for","from","in","inside","into","like","mid","minus","near","nearest","notwithstanding","of","off","on","onto","opposite","out","outside","over","past","re","round","since","through","throughout","till","to","toward","towards","under","underneath","unlike","until","up","upon","via","with","within","without"],

'verb' : ["expeleriamus", "habemus", "levitatio", "disparatum", "cogitum", "summus"],

'execellent' : ['huge','execellent','nice','awesome','wonderful','incredible'],

'adjective': [ "$execellent", "insolent", "bizarre", "horribilis","perfectis","bad","jittery","purple","tan","better","jolly","quaint","tender","beautiful","kind","quiet","testy","big","long","quick","tricky","black","lazy","quickest","tough","blue","bright","magnificent","magenta","rainy","rare","ugly","ugliest","clumsy","many","ratty","vast","crazy","mighty","red","watery","dizzy","mushy","roasted","wasteful","dull","nasty","robust","wide-eyed","fat","new","round","wonderful","frail","nice","sad","yellow","friendly","nosy","scary","yummy","funny","nutty","scrawny","zany","great","nutritious","short","green","odd","silly","gigantic","orange","stingy","gorgeous","ordinary","strange","grumpy","pretty","striped","handsome","precious","spotty","happy","prickly","tart","horrible","tall","itchy","tame"],

'animal': ["alligator","alpaca","ant","ape","armadillo","ass","baboon","badger","bat","bear","bee","beetle","bird","bison","bittern","boar","buffalo","butterfly","buzzard","camel","cat","cattle","cheetah","chicken","chimpanzee","cockroach","cod","coot","coyote","crane","crocodile","deer","dog","dolphin","donkey","dove","duck","eagle","eel","elephant","elk","falcon","ferret","finch","flamingo","fly","fox","frog","gerbil","giraffe","gnat","gnu","goat","goldfinch","goose","gorilla","greyhound","grouse","guinea pig","gull","hamster","hare","hawk","hedgehog","heron","hippopotamus","hog","horse","hummingbird","hyena","impala","kangaroo","koala","lark","lemur","leopard","lion","llama","lobster","locust","magpie","mallard","manatee","mink","mole","monkey","moose","mosquito","mouse","mule","nighthawk","nightingale","opossum","ostrich","otter","ox","panda","parrot","partridge","pelican","penguin","pig","pheasant","pigeon","polar bear","polecat","porcupine","porpoise","possum","prairie dog","python","quail","rabbit","raccoon","rat","raven","reindeer","rhinoceros","rook","salmon","seal","sea lion","shark","sheep","skunk","snake","snipe","sparrow","spider","squirrel","starling","stork","swallow","swan","termite","tiger","toad","trout","turkey","turtle","turtle dove","viper","wallaby","walrus","wasp","weasel","whale","widgeon","wild boar","wolf","wombat","woodchuck","woodcock","woodpecker","wren","yak","zebra"],

'noun': ["$animal"],

'direct_object' : ['$animal','I','you','she','he','we','they'],

'phrase1' : ["python","god"],

'phrase2' : ["holy python", "odius perl", "greatest guido", "marilyn monroe","import this","pythonus idolotrus"],

'phrase3' : ["$verb $preposition $noun", "guido van rossum","oh my god", "bizarre fragances expeleriamus","horribilis fungus habemus"],

'phrase4' : ["$verb $preposition $adjective $noun", "your boobs are $execellent"],

'phrase5' : ["$direct_object $verb $preposition $adjective $noun"],

'phrase6' : ["the $animal $verb $preposition $adjective $noun", "the $adjective $animal $verb $preposition $noun"],

'phrase7' : ["the $adjective $animal $verb $preposition $adjective $noun"],

'phrase8' : ["the $adjective $preposition $animal $verb $preposition $adjective $noun"],

'spell_begin' : ["hocus pocus", "abracadabra"],

'now' : ["right now","now","", "at this moment", "immediately", "without delay"],

'spell_end' : ["evaporatum $now", "disappearum $now", "go away $now"],

'funny_phrase' : ["bizarre fragances expeleriamus","horribilis fungus habemus","pythonus idolotrus"],
}

MAXPHRASE = 8

class Phrase:
    def __init__(self):
        self.__phrase = ''
        self.setGrammar( random.choice( grammar["phrase8"] ) )

    def replace(self, aString ):
        """parses a string, and replaces all the variables with another string,
        which might contain new variables, but will be replaced as well."""

        ret = []
        words = string.split(aString)
        for word in words:
            # variables start with $
            if word[0] == '$':
            # little optimization
                try:
                    # make it fail
                    Template( word ).substitute()
                except KeyError, key:
                    keystr = str(key)[1:-1]
                    varstr = random.choice( grammar[ keystr ] )
                    ret.extend( self.replace( Template( word ).substitute( { keystr :  varstr} ) ) )
            else:
                ret.append( word )
        return ret

    def setGrammar( self, phrase ):
        """sets a grammar to be replaced"""
        self.__phrase = phrase

    def getGrammar( self ):
        """returns the grammar."""
        return self.__phrase
         

    def getPhrase(self):
        """ returns the generated and replaced phrase """
        ret = self.replace( self.__phrase ) 
        return string.join(ret)


class PhraseLen( Phrase ):
    """returns a phrase of a fixed len of words."""
    def __init__( self, l ):
        Phrase.__init__(self)
        self.__len = l
        self.findPhrase()

    def findPhrase( self ):
        i = self.__len

        comma = ""
        phrase = ""
        while i > 0:
            # hardcoded, if you want to support more, just add to grammar
            if i > MAXPHRASE:
                d = int( random.random() * MAXPHRASE + 1 )
            else:
                d = i

            name = "$phrase%d" % d
            phrase += comma + name
            comma = ", "
            i -= d

        self.setGrammar( phrase )

class Spell( PhraseLen ):
    def __init__( self, l ):

        begin = self.replace( random.choice( grammar['spell_begin'] ) )
        end = self.replace( random.choice( grammar['spell_end'] ) )
        PhraseLen.__init__(self,l-( len(begin) + len(end) ) )

        self.setGrammar( string.join(begin)
                           + ', '
                           + self.getGrammar()
                           + ', '
                           + string.join(end) )

class FunnyPhrase( Phrase ):
    """returns a phrase that should be funny."""
    def init( self ):
        self.Phrase.__init__(self)
        self.setGrammar( random.choice( grammar["funny_phrase"] ) )

if __name__ == "__main__":
    for i in range(1,100):
        print '---------------------'
#        print Phrase().getPhrase()
        print "Len(%d): %s" % (i, Spell(i).getPhrase() )
