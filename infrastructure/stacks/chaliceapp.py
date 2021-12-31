import os

from aws_cdk import (
    core as cdk
)
from chalice.cdk import Chalice


RUNTIME_SOURCE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), os.pardir, 'runtime')

class ChaliceApp(cdk.Stack):

    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        # self.dynamodb_table = self._create_ddb_table()
        self.chalice = Chalice(self, 'ChaliceApp', source_dir=RUNTIME_SOURCE_DIR)
