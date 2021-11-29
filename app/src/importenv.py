# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv
from enum import Enum

class ImportEnvKeyEnum(Enum):
  """ .envファイルのキーを書く """
  USE_PROFILE="use_profile"
  PROFILE="profile"
  AWS_ACCESS_KEY_ID = "aws_access_key_id"
  AWS_SECRET_ACCESS_KEY = "aws_secret_access_key"
  REGION_NAME = "region_name"

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ENV_DIC = {}
# ImportEnvKeyEnumの値を書く
ENV_KEYS = []

for e in ImportEnvKeyEnum:
  ENV_DIC[e.value] = os.environ.get(e.value)