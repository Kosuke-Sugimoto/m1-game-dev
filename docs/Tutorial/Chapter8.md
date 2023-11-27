# Chapter8

## ゲームモードを作成
1. Blueprintsフォルダの中で右クリック -> Blueprint Class -> Game Mode Base(ファイル名 : BP_Gamemode_2D)
2. BP_Gamemode_2Dをダブルクリック -> Default Pawn ClassをBP_Player_2Dに設定
    - 主人公が誰なのかを指定する
3. コンパイル -> 保存
## ゲームモードの指定 
### 方法1
レベルごとに別のGamemodeになる
1. Window(左上のメニュー) -> World Setting
2. World Setting タブ(右下)のGameMode OVerrideにBP_Gamemode_2Dをセット
### 方法2
全てのレベルで、指定したGamemodeになる
1. Edit(左上のメニュー) -> Project Setting
2. Maps & Modes -> Default GameModeにBP_Gamemode_2Dをセット

- Default GameModeとWorld Settings」の指定はworld Settingsが優先される 
- タイトル画面や エンディングロール、ステージセレクトのようなキャラクターを操作しない場面では、別の「Gamemode」を用意してレベルの「World Settings」に指定することで、キャラクター以外の操作や、カメラが扱いやすくなる
## Player Start
何も用意していない場合、「x0 y0 z0」の座標からプレイヤーが発生する。指定の場所から発生させる場合はPlayerStartを用意する
1. コンテンツの追加アイコン -> Basic -> PlayerStart
2. transform(右) -> 座標(0,0,0)にする(リターンアイコンをクリック)
3. 少し右にずらす(ずれた位置にスポーンする)
4. Esc -> 保存