# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os

import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum
import importenv as setting

import boto3

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(PYTHON_APP_HOME + '/config/log_config.json')
config.dictConfig(log_conf)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

if __name__ == '__main__':
  codepieline_client = boto3.client('codepipeline',
    aws_access_key_id = setting.ENV_DIC[ImportEnvKeyEnum.AWS_ACCESS_KEY_ID.value],
    aws_secret_access_key = setting.ENV_DIC[ImportEnvKeyEnum.AWS_SECRET_ACCESS_KEY.value],
    region_name = setting.ENV_DIC[ImportEnvKeyEnum.REGION_NAME.value]
  )
  
  result_dict_list = []
  pipeline_response = codepieline_client.list_pipelines()
  codebuild_name_list = []
  for pipeline in pipeline_response['pipelines']:
    # Pipeline名取得
    pipeline_name = pipeline['name']

    # 最終結果用のdict
    pipeline_result_dict = {}
    pipeline_result_dict['pipeline_name'] = pipeline_name

    # CodeBuild名の取得
    for stage in codepieline_client.get_pipeline(name=pipeline_name)['pipeline']['stages']:
      if stage['name'] == 'Build':
        codebuild_name = stage['actions'][0]['configuration']['ProjectName']
        pipeline_result_dict['codebuild_name'] = codebuild_name
        codebuild_name_list.append(codebuild_name)

    result_dict_list.append(pipeline_result_dict)
        

  codebuild_client = boto3.client('codebuild',
    aws_access_key_id = setting.ENV_DIC[ImportEnvKeyEnum.AWS_ACCESS_KEY_ID.value],
    aws_secret_access_key = setting.ENV_DIC[ImportEnvKeyEnum.AWS_SECRET_ACCESS_KEY.value],
    region_name = setting.ENV_DIC[ImportEnvKeyEnum.REGION_NAME.value]
  )

  # CodeBuild取得。
  for codebuild_name in codebuild_name_list:
    # CodeBuild名は揃っているので、まとめて渡すこともできるが、buildspecと1対１にするのが容易なので、１件ずつ取得。
    # まとめたほうが早いかもしれないが、大した件数ではないはず。
    for codebuild in codebuild_client.batch_get_projects(names=[codebuild_name])['projects']:
      if len(codebuild) != 0:
        for result_dict in result_dict_list:
          if 'codebuild_name' in result_dict and result_dict['codebuild_name'] == codebuild_name:
            result_dict['buildspec'] = codebuild['source']['buildspec']

  print(result_dict_list)