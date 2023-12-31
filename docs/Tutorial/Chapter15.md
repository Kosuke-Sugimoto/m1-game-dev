# Chapter15< Character Movement>

## Character Movement
1. BluePrintフォルダ -> CharacterBluePrintを開く
2. 「Components」欄(左上) -> 「Character Movement」を選択
    - 右の詳細欄に、キャラクターの挙動を制御 する値がたくさん表示される
    - マウスカーソルを合わせてみると、項目の説明が確認できる
## Character Movementの設定
重要なCharacter Movementの設定
- 「Character Movement (General Settings)」の「Gravity Scale」
    - アクションゲームの場合、この重力設定が ゲームの世界観を決める大きな要素になる
- 「Character Movement Walking」の「Max Walk Speed」
    - 移動速度を変更したい場合に触る
- 「Advanced」の「Use Flat Base for Floor Checks」
    - 地面との接地面をカプセル の形状にそうかどうかという設定
    - ドット絵ゲームの場合は、チェックを入れる
- 「Character Movement Jumping / Falling」の「Jump Z Velocity」
    - ジャンプ力の値
- 「Air Control」
    - 0 : ジャンプ後、着地するまで、動きの制御ができない状態
    - 1 : ジャンプ後に、空中での移動の制御が可能な状態 
- 「Planer Movement」の「Constrain to Plane」
    - y = 1 : オブジェクト同士が衝突した際に、奥や手前などに押し出され たりする可能性がなくなる
## サンプルデータ
- 「2D Slide Scroller Character」
- 「Getting Started With Your Paper 2D Project」
- 「Unreal Stick Figure 2D」