#!/usr/bin/env python
#coding: utf-8
from __future__ import unicode_literals
import codecs
import yaml
import rospy
from std_msgs.msg import String
import grammar
import os

os.chdir( os.path.dirname(__file__) )


def to_slist( list_ ): return [ str(l) for l in list_ ]

class GrammarBasedLU():
    def __init__(self):
        rospy.init_node("grammar_lu")

        self.pub_results = rospy.Publisher('grammar_lu/results', String , queue_size=10)
        rospy.Subscriber("google_speech/recres_nbest", String, self.recog_callback)
        rospy.Subscriber("grammar_lu/grammar", String, self.set_gram)
        self.gram = grammar.Grammar()
        self.gram.load( "grammar_sample.txt" )

        rospy.spin()


    def recog_callback(self, msg ):
        results = yaml.safe_load(msg.data)

        sentences = [ r["text"] for r in results ]

        m = self.gram.match( sentences )
        if m:
            text, gram_id, slot_str, slot_id = m
            lu_res = {}
            lu_res["text"] = text 
            lu_res["gram_id"] = gram_id
            lu_res["slot_str"] = to_slist(slot_str)
            lu_res["slot_id"] = to_slist(slot_id)
            print("文法マッチ", gram_id, slot_str, slot_id)
            print(yaml.dump(lu_res))
            self.pub_results.publish( yaml.dump(lu_res) )
            print( "---------------------------" )
            return
        else:
            print( "文法マッチなし" )

    def set_gram( self, data ):
        print( "--- set grammar ---" )
        codecs.open( "tmp_gram.txt" , "w" , "utf8" ).write( data.data )
        print( data.data )
        self.gram.load( "tmp_gram.txt" )
        print( "------------------" )

def main():
    GrammarBasedLU()

if __name__ == '__main__':
    main()