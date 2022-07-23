#!/usr/bin/env python
from websocket_server import WebsocketServer
import rospy
from std_msgs.msg import String
import yaml
import threading

def message_received(client, server, message):
    # 日本語の文字コードがおかしいので修正
    try:
        message = bytes(message, "iso-8859-1").decode("utf8")
    except UnicodeEncodeError:
        message = bytes(message, "utf8").decode("utf8")

    print("認識結果：")
    results = []
    for r in message.split("\n"):
        print(r)
        r = r.split(":")
        if len(r)!=2:
            continue
        text, conf = r 
        results.append( {"text":text, "conf":float(conf)} )
    print("-------")

    pub_recres.publish( results[0]["text"] )
    pub_recres_nbest.publish( yaml.dump(results) )

def new_client(client, server):
    print("クライアント接続")

def client_left(client, server):
    print("クライアント切断")

def say( data ):
    print("発話：", data.data )
    server.send_message_to_all( data.data )

def server_stop_thread():

    while 1:
        c = input()

        if c=="q":
            print("サーバーを終了します")
            server.shutdown()
            break

def main():
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received) 

    print("*********************************")
    print("GoogleChromeで ")
    print("   https://hp.naka-lab.org/ros_google_speech/")
    print("を開いて、音声認識・合成開始ボタンを押す．")
    print("q+[ENTER]で終了．")
    print("*********************************")
    
    t = threading.Thread(target=server_stop_thread)
    t.setDaemon(True)
    t.start()

    server.run_forever()

if __name__=="__main__":
    rospy.init_node('google_speech' )
    rospy.Subscriber("google_speech/utterance", String, say )
    pub_recres = rospy.Publisher('google_speech/recres', String, queue_size=10)
    pub_recres_nbest = rospy.Publisher('google_speech/recres_nbest', String, queue_size=10)

    server = WebsocketServer(port=60000, host="127.0.0.1")

    main()
