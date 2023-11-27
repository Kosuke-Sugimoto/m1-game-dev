# m1-game-dev
5号館メンツにて作成中のゲームに関するリポジトリ

## feature/#2-graffiti-dataset ブランチに関して
### 概要・注意点
***このブランチは Merge せずに置いておく***  
quickdraw-dataset を用いた落書き認識モデルの調査・調整に関するスクリプトを保存しておくためのブランチ

### 使い方
基本的に docker-container 上で動作させることを仮定している  
docker_run.sh を実行すれば、必要なパッケージが含まれた docker-container が起動

### データセットのダウンロードについて
データセットは gsutil コマンドを使ってダウンロード  
（※ gsutil コマンドは docker-container 内で初めから使えるようにしてあります）
- raw files をダウンロードしたい場合
  ```bash
  gsutil -m cp 'gs://quickdraw_dataset/full/raw/*.ndjson' .
  ```
- simplified drawings files をダウンロードしたい場合
  ```bash
  gsutil -m cp 'gs://quickdraw_dataset/full/simplified/*.ndjson' .
  ```
- binary files をダウンロードしたい場合
  ```bash
  gsutil -m cp 'gs://quickdraw_dataset/full/binary/*.bin' .
  ```
- numpy binary files をダウンロードしたい場合
  ```bash
  gsutil -m cp 'gs://quickdraw_dataset/full/numpy_bitmap/*.npy' .
  ```

各コマンドでの格納先は現在いるディレクトリの配下  
変更したい場合には . を任意のディレクトリに変更すること
