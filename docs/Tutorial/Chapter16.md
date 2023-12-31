# Chapter16

## 整頓
カメラが寄りすぎな気がする
1. キャラクターのブループリントを開く -> 「Camera」を選択
2. 「Ortho With」の値を「2000」に変更
## リダイレクタの修正
「Textures」フォルダの中で1枚画像のサンプル用で使った素材を削除をする際に「Some of the assets being deleted are still referenced in memory.」と表示される場合
1. Sceneの中から使用されているものを削除
2. 「File」 -> 「Save All」 -> 環境を更新
3. 「Content Browser」 -> 「Content」フォルダを右クリック -> 「 Fix Up Redirectors」
4. 「T_White16_Sprite」を「S_White16」に名前を変更
5. 「Sprites」フォルダに移動
## バックアップ
1. 「File」-> 「Zip Project」を選択
2. フォルダを選択 -> 名前に「_Template_5_1_1」追加 -> 「Save」