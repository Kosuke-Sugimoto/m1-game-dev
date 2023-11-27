# Chapter5

## コンテンツブラウザを開く
1. Content Drower(左下) or Ctrl & Space  
  
    Dock in Layout(右側)をクリックすると常にコンテンツブラウザが表示されるようになる

### ディレクトリ構造
以下のディレクトリ構造を作る
```
All
└─Content
    └─2DAction
        ├─Assets
        │  └─Textures
        └─Maps
```

## インポートテクスチャ
### 推奨
ドット絵はpng推奨
テクスチャの解像度は2の乗数
### 方法
URLからダウンロード
URL :  https://ue5study.com/2d/2d-action-texture-import-sample/
２つのテクスチャをTextureフォルダに保存(移動)

## テクスチャ設定
### 読み込んだサンプル画像がぼやけて表示される時の対処法
1. 該当テクスチャ画像を右クリック　-> Sprite Action -> Paper 2D texture setting
2. 画像をビューポートに表示 -> Details
    - Mip fgen setting : NoMipmaps
    - texture group : 2d pixcel (unfiltered)
    - comparession setting : user interface 2d (rgba)
    - Filter : nearest
## ビットの深さ
### 確認方法
エクスプローラーから該当画像を右クリック　-> プロパティからbitdepthを確認　
- 24bit 32bit ならOK 
- 48bit~ は変換する必要がある
### 変換方法
1. エクスプローラーから該当画像を右クリック
2. プログラムを開く(Open with)
3. Snip & Sketchで画像を開く
4. 名前を付けて保存(この画像を使う)
## 一括設定ツール
URL : https://www.youtube.com/watch?v=_sgyZ2dsUV0  
を参照