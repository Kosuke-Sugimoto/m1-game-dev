# Chapter7

## フリップブックを作成
- FlipbookというSpriteを連番でアニメーションさせる機能の、形式データを用意する  
- 複数のスプライトを同時に選択することで、 連番アニメーションとして扱うことが 可能な機能になる

1. キャラクターのSpriteを右クリック ->  Create Flipbook


## PaperCharacterを作成
以下のディレクトリ構造を作る
```
All
└─Content
    ├─2DAction
    │  ├─Assets
    │  │  └─Textures
    │  ├─Blueprints
    │  └─Maps
    └─Tools
```
1. 「Blueprints」フォルダで右クリック -> Blueprint Class
2. ALL CLASSES をクリック
3. 検索欄で「paper」と検索 -> PaperCharacter(一番下)をクリック -> 選択ボタン(ファイル名 : BP_Player_2D)
4. BP_Player_2Dをダブルクリックで開き、Sprite(左のメニュー)を選択
5. Source Flipbook(右の詳細欄)に、用意したキャラクターをセット
## カメラ設定
キャラクターの中にカメラを用意する
1. BP_Player_2D Self(一番上)を選択した状態で、+Add(左上)を選択 
2. 検索欄で「arm」と検索 -> SpringArmを追加
3. SpringArmを選択した状態で、+Add(左上)を選択
4. 検索欄で「camera」と検索 ->Cameraを追加
5. SpringArmを選択した状態で、Transform(右の詳細欄)のRotationのz軸 を-90に変更
6. Rotationとなっている項目をWorldに変更(Absolute Rotationになる)
    - Absolute Rotationは、親階層の回転の影響を受けないという設定になる
7. Camera CollisionのDo Collision Testのチェックを外す
    - チェックがあると、SpringArmに障害物が当たった際に、障害物より手前に来ようとする設定になる
8. Cameraを選択 -> Camera Settings
9. Projection ModeをPerspectiveからOrthographicsに変更
    - レトロゲームの場合はOrthographics。Perspectiveは立体的にな表示でOrthographicsは図面的な表示
10. Ortho Widthの値を1000に変更
11. コンパイル -> 保存