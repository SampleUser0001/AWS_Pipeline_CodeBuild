# AWS Pipeline CodeBuild

AWS PipelineとAWS CodeBuildの紐づけを一覧にする。  
都合のいいように修正して使う。

## aws-cli

```sh
aws codepipeline list-pipelines
aws codepipeline get-pipeline --name ${CodePipeline名}
aws codebuild batch-get-projects --name ${CodeBuild名}
```
