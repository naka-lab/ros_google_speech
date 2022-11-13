#!/usr/bin/env python
#coding: utf-8
from __future__ import unicode_literals
import codecs
import yaml
import rospy
from std_msgs.msg import String
import grammar
import os
import codecs

# windowsの場合
if os.name=="nt":
    import winsound

os.chdir( os.path.dirname(__file__) )


def to_slist( list_ ): return [ str(l) for l in list_ ]

def play_sound( filename ):
    if os.name!="nt":
        os.system( "aplay " + filename )
    else:
        winsound.PlaySound( filename, winsound.SND_FILENAME )

class GrammarBasedLU():
    def __init__(self):
        rospy.init_node("grammar_lu")

        with codecs.open( "prohibited_words.txt", "r", "utf8" ) as f:
            self.probibited_words = [ line.strip() for line in f.readlines()]

        self.pub_results = rospy.Publisher('grammar_lu/results', String , queue_size=10)
        rospy.Subscriber("google_speech/recres_nbest", String, self.recog_callback)
        rospy.Subscriber("grammar_lu/grammar", String, self.set_gram)
        self.gram = grammar.Grammar()
        self.gram.load( "grammar_sample.txt" )

        rospy.spin()


    def recog_callback(self, msg ):
        results = yaml.safe_load(msg.data)

        sentences = [ r["text"] for r in results ]

        # 禁止用語が含まれているものを除外する
        for s in sentences:
            for pw in self.probibited_words:
                if pw in s:
                    print( "禁止用語発見", s )
                    play_sound( "beep_failed.wav" )
                    return

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
            play_sound( "beep_success.wav" )
            return
        else:
            print( "文法マッチなし" )
            play_sound( "beep_failed.wav" )

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