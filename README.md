# ros_google_speech

Google音声認識・合成ノード

## 準備
```
pip install websocket-server
cd ~/catkin_ws/src
git clone https://github.com/naka-lab/ros_google_speech.git
```
[Google Chrome](https://www.google.co.jp/chrome/)がインストールされていなければインストールする

## 音声認識・合成
### 実行
1. 認識結果の受信プログラムを起動：`rosrun ros_google_speech google_speech.py`
2. Google Chromeで[https://hp.naka-lab.org/ros_google_speech/](https://hp.naka-lab.org/ros_google_speech/)を開く
3. 「音声認識・合成開始」ボタンを押して，マイクの使用を許可する
4. pythonプログラムと接続できてないときは，ウェブページを更新して3.をもう一度実行

### Topic
- Publish
  - `google_speech/recres`:音声認識結果の文字列
  - `google_speech/recres_nbest`:複数の音声認識候補文字列とそのスコア（yaml形式の文字列）
- Subscribe
  - `google_speech/utterance`:発話文字列

## 文法ベースの言語理解
### 実行
1. 音声認識・合成ノードを実行
2. 言語理解ノードを実行：`rosrun ros_google_speech grammar_lang_understanding.py`
3. 認識文法を送信（[sample](scripts/example_grammar.py)参照）

### Topic
- Subscribe
  - `grammar_lu/grammar`：認識文法
  - `google_speech/recres_nbest`：音声認識ノードから送られてくる認識結果
- Publish
  - `grammar_lu/results`:言語理解結果．yaml形式のテキストで，認識文・文法ID・スロットに入った単語・スロットに入った単語のIDを送信．

### 文法書式
```
[GRAMMAR]
greeding : ロボット $slot_greeding
bring : $slot_drink * $slot_person * <持って行って|届けて|取って>


[SLOT]
$slot_greeding
hello : こんにちは|ハロー
bye : さようなら|バイ
morning : おはよう

$slot_drink
drink1 : ジュース
drink2 : コーラ|コーク
drink3 : お茶|緑茶

$slot_person
person1 : 中村|中村さん
person2 : 田中
person3 : 太郎
```
`[GRAMMAR]`に音声認識文法を記述します．`greeding : ロボット $slot_greeding`の`greeding`は認識文のIDを，右側の文字列が認識される文章になります．
`$slot_greeding`は単語が入るスロットを表しており，`[SLOT]`以下がスロットに入る単語を定義しています．
`hello : こんにちは|ハロー`の`hello`が単語のIDを，`こんにちは|ハロー`が認識される文字列を表しています．
`|`はorを表しており，`こんにちは`または`ハロー`が認識されます．文法では`<a|b|c>`という書式でorを記述できます．
`*`はいずれの文字列にもマッチします．

`|`や`*`を使うことでユーザ発話のゆらぎを吸収して，発話内容を認識できます．
