# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os
from logutil import LogUtil

from logutil import LogUtil
from importenv import ImportEnvKeyEnum
import importenv as setting

import boto3
from boto3.session import Session

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(PYTHON_APP_HOME + '/config/log_config.json')
config.dictConfig(log_conf)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

class Boto3ClientFactory:
    @staticmethod
    def create(service):
        if int(setting.ENV_DIC[ImportEnvKeyEnum.USE_PROFILE.value]):
            # profileを使う
            profile = setting.ENV_DIC[ImportEnvKeyEnum.PROFILE.value]
            return Session(profile_name=profile).client(service)

        else:
            # profileを使わない
            return boto3.client(service,
                aws_access_key_id = setting.ENV_DIC[ImportEnvKeyEnum.AWS_ACCESS_KEY_ID.value],
                aws_secret_access_key = setting.ENV_DIC[ImportEnvKeyEnum.AWS_SECRET_ACCESS_KEY.value],
                region_name = setting.ENV_DIC[ImportEnvKeyEnum.REGION_NAME.value]
            )

