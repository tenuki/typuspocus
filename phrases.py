# -*- coding: utf-8 -*-
#
# A simple phrase generator using a modifiable grammar

import random
import string
from string import Template

grammar = {
'intro' : ["hocus pocus", "abracadabra"],
'preposition' : ["aboard","about","above","absent","across","after","against","along","alongside","amid","amidst","among","amongst","around","as","at","atop","before","behind","below","beneath","beside","besides","between","beyond","by","despite","down","during","except","following","for","from","in","inside","into","like","mid","minus","near","nearest","notwithstanding","of","off","on","onto","opposite","out","outside","over","past","re","round","since","through","throughout","till","to","toward","towards","under","underneath","unlike","until","up","upon","via","with","within","without"],
'verb' : ["expeleriamus", "habemus", "engorgio", "reducio", "crucio", "levitatio", "disparatum", "cogito","sunt","enlargio"],
'adjetive': ["bizarre", "horribilis","perfectis"],
'animal': ["alligator","alpaca","ant","anteater","antelope","ape","armadillo","ass","baboon","badger","bat","bear","bee","beetle","bird","bison","bittern","boar","buffalo","butterfly","buzzard","camel","cat","cattle","cheetah","chicken","chimpanzee","cockroach","cod","coot","coyote","crane","crocodile","deer","dog","dolphin","donkey","dove","duck","eagle","eel","elephant","elk","falcon","ferret","finch","flamingo","fly","fox","frog","gerbil","giraffe","gnat","gnu","goat","goldfinch","goose","gorilla","greyhound","grouse","guinea pig","gull","hamster","hare","hawk","hedgehog","heron","hippopotamus","hog","horse","hummingbird","hyena","impala","kangaroo","koala","lark","lemur","leopard","lion","llama","lobster","locust","magpie","mallard","manatee","mink","mole","monkey","moose","mosquito","mouse","mule","nighthawk","nightingale","opossum","ostrich","otter","ox","panda","parrot","partridge","pelican","penguin","pig","pheasant","pigeon","polar bear","polecat","porcupine","porpoise","possum","prairie dog","python","quail","rabbit","raccoon","rat","raven","reindeer","rhinoceros","rook","salmon","seal","sea lion","shark","sheep","skunk","snake","snipe","sparrow","spider","squirrel","starling","stork","swallow","swan","termite","tiger","toad","trout","turkey","turtle","turtle dove","viper","wallaby","walrus","wasp","weasel","whale","widgeon","wild boar","wolf","wombat","woodchuck","woodcock","woodpecker","wren","yak","zebra"],
'noun': ["$animal"],
'funny_phrase' : ["bizarre fragances expeleriamus","horribilis fungus habemus","pythonus idolotrus"],
'phrase' :  ["$intro, $verb $preposition $noun","$funny_phrase"]
}


class Phrase:
    def __init__(self):
        self.__phrase = ''
        self.setPhrase( random.choice( grammar["phrase"] ) )

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

    def setPhrase( self, phrase ):
        """sets a phrase to be replaced"""
        self.__phrase = phrase

    def getPhrase(self):
        """ returns the generated and replaced phrase """
        ret = self.replace( self.__phrase ) 
        return string.join(ret)

if __name__ == "__main__":

    for i in range(0,10):
        print '---------------------'
        print Phrase().getPhrase()
