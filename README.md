# AWS Pipeline CodeBuild

AWS PipelineとAWS CodeBuildの紐づけを一覧にする。  
都合のいいように修正して使う。

## 実行

``` sh
# venv構築
python3 -m venv venv
# アクティベート
source venv/bin/activate

# 依存関係ライブラリインストール
pip3 install -r app/requirements/requirements.txt

# 実行
cd app
sh start.sh
```

## aws-cli

```sh
aws codebuild list-projects
```
