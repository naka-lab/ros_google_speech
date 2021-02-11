#!/usr/bin/env python
import rospy
from std_msgs.msg import String


def main():
	rospy.init_node('gspeech_example')
	synthesisPub = rospy.Publisher( "google_speech/utterance", String, queue_size=10 )	

	while not rospy.is_shutdown():
		msg = rospy.wait_for_message( 'google_speech/recres',  String )

		print( msg.data )

		if msg.data=="こんにちは":
			synthesisPub.publish( "こんにちは" )
		elif msg.data=="おはよう":
			synthesisPub.publish( "おはよう" )
		elif msg.data.find("元気")!=-1:
			synthesisPub.publish( "元気です。" )
			

if __name__ == '__main__':
	main()
