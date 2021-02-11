#!/usr/bin/env python
from websocket_server import WebsocketServer
import rospy
from std_msgs.msg import String

def message_received(client, server, message):
    # 日本語の文字コードがおかしいので修正
    message = bytes(message, "iso-8859-1").decode("utf8")
    print( "認識結果：", message )
    pub_recres.publish( message )

def new_client(client, server):
    print("クライアント接続")

def client_left(client, server):
    print("クライアント切断")

def say( data ):
    print("発話：", data.data )
    server.send_message_to_all( data.data )

def main():
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received) 


    server.run_forever()

if __name__=="__main__":
    rospy.init_node('google_speech' )
    rospy.Subscriber("google_speech/utterance", String, say )
    pub_recres = rospy.Publisher('google_speech/recres', String, queue_size=10)

    server = WebsocketServer(60000, host="127.0.0.1")

    main()
