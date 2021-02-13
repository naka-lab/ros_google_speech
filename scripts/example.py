#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import yaml


def main():
	rospy.init_node('gspeech_example')
	synthesisPub = rospy.Publisher( "google_speech/utterance", String, queue_size=10 )	

	while not rospy.is_shutdown():
		msg = rospy.wait_for_message( 'google_speech/recres_nbest',  String )
		results = yaml.safe_load(msg.data)

		for r in results:
			text = r["text"]

			print(text)
			if text=="こんにちは":
				synthesisPub.publish( "こんにちは" )
			elif text=="おはよう":
				synthesisPub.publish( "おはよう" )
			elif text.find("元気")!=-1:
				synthesisPub.publish( "元気です。" )
			else:
				continue
			break
			

if __name__ == '__main__':
	main()
