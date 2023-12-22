# Chapter10<Enhanced Input 設定>

## 足場の調整
- スプライトの複製 : Alt + 矢印をDrag
    - 矢印がない場合 -> 「十字の矢印」(ビューポート中央上)を選択 or Wキー
- スプライトの大きさ、色をoutlinerタブで調整して地面(足場)、ブロックを作成
## 初めてのブループリント
1. 「BP_Player_2D」をダブルクリック
2. 「Event Graph」のタブであることを確認
    - ブループリント(イベントグラフ)の基本操作  
        - ノードの作成 : 右クリック   
        - ノードの選択 : 三角(っぽい)アイコンをDrag  
        - 関連するノードだけ表示 : 丸いピンをDrag

## 簡易インプット
1. 右クリック -> 検索欄で「@」キーボードイベントを選択 
2. 「@」を選択した状態でDetailの「キーボードマーク」をクリック
3. スペースバーを押す(スペースバーのキー入力が設定される)
4. 「Space Bar」の「Pressed」から右にドラッグ
5. 検索欄で「jump」と検索
6. 「Jump」ノードを繋ぐ

- 直接入力処理をブループリント上に置く行為は、行儀が悪い処理!
## インプット確認
1. Edit -> プラグイン
2. 「enhanced」と検索 ->「Enhanced Input」にチェックがあるのを確認
## 入力アクション/マッピングコンテキスト作成
1. 以下のディレクトリ構造を作る
```
All
└─Content
    ├─2DAction
    │  ├─Assets
    │  │  └─Textures
    │  ├─Blueprints
    │  ├─Input
    |  |  └─Actions
    │  └─Maps
    └─Tools
```
2. Actionsフォルダ内で右クリック ->「Input」->「Input Action」
3. 名前を「IA_Jump」に変更
4. Inputフォルダ内で右クリック ->「Input」->「Input Mapping Context」
5. 名前を「IMC_2DAction」に変更
6. 「IMC_2DAction」をダブルクリック -> 「Mappings」-> 「Plus」
7. 「IA_Jump」を指定 -> 「キーボードアイコン」をクリック
8. キーボードのスペースバーを押す(スペースバーのキー入力が設定される)
## Enhanced Input 宣言
1. 「Blueprints」フォルダー -> 「BP_Player_2D」をダブルクリック -> 「Event Graph」
2. 「EventBeginPlay」以外Deleteキーで削除
    - Event BeginPlay : このキャラクターがレベル上に発生した時に一度呼ばれるイベント  
    ここに「Enhanced Input」を使用する宣言をする
3.  イベントグラフ内で右クリック -> 「get controller」と検索 ->「Get Controller」を選択
4. 「Get Controller」の青ピンからDrag -> 「cast player」と検索 ->「Cast To PlayerController」を選択
5. 「Cast To PlayerController」 の青ピンからドラッグ -> 「enh」と検索 -> 「Enhanced Input Local Player Subsystem」を選択
6.  「Enhanced Input Local Player Subsystem」の青ピンから右にドラッグ -> 「isvalid」と検索 -> 「?isvalid」を選択
7. 「Cast」の上のピンから「Is Valid」に繋げる
8. 「Subsystem」ノードの青ピンからドラッグ ->「addm」と検索 -> 「Add Mapping Context」を選択
9. 「Add Mapping Context」ノード -> 「Mapping Context」->「IMC_2DAction」をセット
10. 「Add Mapping Context」と「Is Valid」を繋げる
11. 「Event BeginPlay」と「Cast To PlayerController」を繋げる
## Enhanced Input ジャンプ
1. イベントグラフ内で右クリック -> 「ia_」と検索 -> 「IA_Jump」を選択
2. 「IA_Jump」の「Started」のピンからドラッグ -> 「jump」と検索 -> 「Jump」ノードを繋げる(繋がる)
    - 「Triggered」の方に繋げると、押している間イベントが発生し続ける
    - 線のつなぎ替え : Ctrl + Drag
    - 線の消去 : Alt + Click
3. 「IA_Jump」の「Completed」->「jump」と検索 -> 「Stop Jumping」を追加
## 入力アクション　左右移動
1. 「Actions」ファイル内で右クリック -> 「Input」->「Input Action」を選択
2. 名前を「IA_MoveRight」とする
3. 「IA_MoveRight」をダブルクリック -> 「Value Type」を「Axis1D(Float)」に変更
    - 「Value Type」について
        - 「Digital(bool)」 : キーを押すだけ
        - 「Axis1D(float)」 : ゲームパッドのスティックの横軸や 縦軸の値が必要なもの
        - 「Axis2D(Vector2D)」: 3Dのゲームなどで、360度移動するような場合
        - 「Axis3D(Vecter)」: VRなどの3D空間上のコントローラー用
4. 「Input」フォルダ内の「IMC_2DAction」をダブルクリック -> 「Mappings」->Plusアイコンをクリック -> 「IA_MoveRight」をセット
5.  「IA_MoveRight」のPlusアイコンをクリック -> キーを2つ用意 -> 上にA、下にDをセット
6.  (Aの方は、押したらマイナスという設定にする)「Modifires」のPlusアイコンをクリック -> 「Index 0」に「Negate」を当てる
## Enhanced Input 左右移動
1. 「Blueprints」フォルダ内の「BP_Player_2D」をダブルクリック
2. イベントグラフで右クリックから -> 「ia_」と検索 -> 「IA_MoveRight」を選択
3. 「IA_MoveRight」の「Action Value」からドラッグ -> 「addm」と検索 -> 「Add Movement Input」を選択
4. 「World Direction」のxの値を1.0 にする
5. 「Triggered」と「Add Movement Input」を繋ぐ