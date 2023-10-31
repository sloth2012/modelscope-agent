import json
import os

import requests
from requests.exceptions import RequestException, Timeout

from .pipeline_tool import ModelscopePipelineTool


DEFAULT_TARGET = "glucose"


class GraphSearchTool(ModelscopePipelineTool):
    default_model = ''
    description = '根据起始与终止顶点，从图数据库中查询合成生物路径。'
    name = 'kongfoo_graph-search'
    parameters: list = [
        {
            'name': 'target',
            'description': '开始节点，英文形式。',
            'required': True
        },
        {
            "name": "source",
            'description': f"结束节点，英文形式，默认值：{DEFAULT_TARGET}",
            "default": DEFAULT_TARGET
        }
    ]
    task = ''

    def _parse_output(self, origin_result, *args, **kwargs):
        return {'result': origin_result}

    # TODO测试下推理，不用远程api
    def _remote_call(self, *args, **kwargs):
        return {"result": {"paths": """CHEBI:62047:(S)-carnitine <=RHEA:30543=> CHEBI:20047:(S)-carnitinyl-CoA"""}}
