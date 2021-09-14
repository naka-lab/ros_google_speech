# encoding: utf8
from __future__ import unicode_literals
import re
import codecs
from collections import OrderedDict

class Grammar:
    def __init__(self):
        self.slot_finder = re.compile( "\$slot[A-z0-9-]*" )
        self.grammars = OrderedDict()
        self.slot2id = {}

    def normalize( self, s ):
        s = s.strip()

        # 不要な文字を取り除く
        s = s.replace( "\n" , "" )
        s = s.replace( "\r" , "" )

        # 句読点は全て全角にしてう白いスペースを入れる
        s = s.replace( u"，" , u"、 " )
        s = s.replace( u"、" , u"、 " )
        s = s.replace( u"。" , u"。 " )
        s = s.replace( u"．" , u"。 " )
        s = s.replace( "," , u"、 " )
        s = s.replace( "." , u"。 " )
        s = s.replace( "\t" , " " )

        while "  " in s:
            s = s.replace( "  " , " " )

        s = s.lower()

        return s


    def load(self, filename):
        lines = codecs.open( filename , "r" , "utf8" ).readlines()
        lines = [ l for l in lines ]

        self.grammars = OrderedDict()
        self.slot2id = {}

        slots = {}
        slot_re = {}


        # [SLOT]を読み込み
        start = False
        for line in lines:
            if "[SLOT]" in line:
                start = True
                continue

            if start:
                # SLOTセクションの修了
                if "[" in line:
                    break
                elif "$" in line:
                    class_id = line.strip()
                    slots[class_id] = []

                if ":" in line:
                    id,slot = line.split(":")
                    id = id.strip()

                    for n in slot.split("|"):
                        n = self.normalize(n)
                        slots[class_id].append( n )
                        self.slot2id[n] = id
                        #print class_id ,id, n

        for id,n in slots.items():
            slot_re[id] = "(" + "|".join(n) + ")"

        # [GRAMMAR]を読み込み
        start = False
        for line in lines:
            # 文法セクションの開始
            if "[GRAMMAR]" in line:
                start = True
                continue

            if start:
                # 文法セクションの修了
                if "[" in line:
                    break

                if ":" in line:
                    id,gram = line.split(":")
                    id = id.strip()
                    gram = self.normalize(gram)

                    # slotを正規表現に変換
                    for class_id in self.slot_finder.findall(gram):
                        if class_id=="$slot_any":
                            # 文字列を抽出する
                            gram = gram.replace( class_id, "(\S+?)" )
                        else:
                            gram = gram.replace( class_id, slot_re[class_id] )

                    # その他を正規表現に変換
                    gram = gram.replace("<" , "(?:")
                    gram = gram.replace(">" , ")")
                    gram = gram.replace("*" , ".*?")
                    #gram = gram.replace( " " , "\s*?" )
                    # gram = ".*?" + gram + ".*?"
                    gram = gram.replace( " " , "" )
                    gram = gram.replace( "　" , "" )
                    #gram = gram.lower()

                    self.grammars[id] = re.compile(gram)
                    print( "RegEx:",id,"->",gram )

    def match(self, sentences ):
        matched_gramid = ""
        matched_slot = []
        mathced_slotid = []
        for id, g in self.grammars.items():
            for s in sentences:
                s = s.lower()
                m = g.match(s)

                if m:
                    matched_gramid = id
                    matched_slot = m.groups()
                    for n in matched_slot:
                        if n in self.slot2id:
                            mathced_slotid.append( self.slot2id[n] )
                        else:
                            mathced_slotid.append( "any" )

                    return s, matched_gramid, matched_slot, mathced_slotid

        return None


def main():
    g = Grammar()

    g.load( "grammar_sample.txt" )
    print( g.match( ["ラーメンを中村に持って行って", "コーヒーを中村に持って行って"] ) )
    print( g.match( "人を探して" ) )
    print( g.match( "こんにちは" ) )
    return

if __name__ == '__main__':
    main()