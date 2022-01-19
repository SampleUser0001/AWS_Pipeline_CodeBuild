# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os

import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum
import importenv as setting

import boto3
from boto3.session import Session
from factory import Boto3ClientFactory as Factory

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(PYTHON_APP_HOME + '/config/log_config.json')
config.dictConfig(log_conf)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

OUTPUT_FILE_PATH = os.path.join(PYTHON_APP_HOME, *['output', 'result.tsv'])

if __name__ == '__main__':
    # CodeBuild取得。
    codebuild_client = Factory.create('codebuild')
    codebuild_list = codebuild_client.batch_get_projects(
        names = codebuild_client.list_projects(
            sortBy='CREATED_TIME',
            sortOrder='ASCENDING'
        )['projects']
    )
        
    # CodeCommitとbuildspec.ymlファイルのパスを取得する
    with open(OUTPUT_FILE_PATH, mode='w', newline='') as f:
        f.write('{}\t{}\t{}\t{}'.format(
                'CodeBuild',
                'type',
                'Repository',
                'buildspec'
            )
        )
        for codebuild_info in codebuild_list['projects']:
            f.write('{}\t{}\t{}\t{}\r\n'.format(
                codebuild_info['name'],
                codebuild_info['source']['type'],
                codebuild_info['source']['location'] if 'location' in codebuild_info['source'] else '-',
                codebuild_info['source']['buildspec'] if 'buildspec' in codebuild_info['source'] else '-')
            )
