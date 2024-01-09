# Chapter11<振り向き処理・関数>

## 関数
1. 「Blueprints」フォルダ内の「BP_Player_2D」を開く
2. 「My Blueprint」の中の「Function」の右の「+」をクリック
3. 名前を「FlipTurn」に変更
    - 関数のタブが開いていなかったら、「FlipTurn」をダブルクリック


白い線がつながる実行ピンがついている関数 : 青いアイコン。 
実行ピンが付いていない関数(純粋関数) : 緑のアイコン

## 振り向き

1. 「FlipTurn」の関数内で右クリック -> 「comparef」と検索 -> 「Compare Float」のノードを選択
2. 「Input」の値を関数の実行ピンの下側にドラッグ ->  「Input」の実行ピンも繋げる
    - 入力値を、関数の外から受け取るようにする
    - 入力値が0より大きい場合 : 上のイベントが実行
    - 入力値が0より小さい場合 : 下のイベントが実行
3. 「FlipTurn」Window内で右クリック -> 「getcontroller」と検索  -> 「Get Controller」ノードを選択
4. 「Get Controller」の「Return Value」から右にドラッグ -> 「Set Rotation」と検索 -> 「Set Control Rotation」ノード を出す
5. 「Set Control Rotation」の「New Rotation」を右クリック -> 「Split Struct Pin」を選択
6. 「Set Control Rotation」をコピペ
7.  X軸y軸は0のまま、z軸の値を180にする
8.  「Get Controller」の「Return Value」と2つの「Set Control Rotation」をつなげる
9. 「Compare Float」の上のイベントをz軸値が0の「Set Control Rotation」、「Compare Float」の下のイベントをz軸値が180の「Set Control Rotation」と繋げる
10. 「Event Graph」のタブに戻る -> 「FlipTurn」の関数をドラッグ
11. 「Add Movement Input」の後ろに繋げる
12. 「FlipTurn」の「Input」に「Action Value」の値を繋げる