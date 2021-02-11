# ros_google_speech

Google音声認識・合成ノード

## 準備
```
pip install websocket-server
cd ~/catkin_ws/src
git clone https://github.com/naka-lab/ros_google_speech.git
```

## 実行
1. 認識結果の受信プログラムを起動：`rosrun ros_google_speech google_speech.py`
2. Google Chromeで[https://hp.naka-lab.org/ros_google_speech/](https://hp.naka-lab.org/ros_google_speech/)を開く
3. 「音声認識・合成開始」ボタンを押して，マイクの使用を許可する
4. pythonプログラムと接続できてないときは，ウェブページを更新して3.をもう一度実行
