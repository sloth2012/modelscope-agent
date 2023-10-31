from modelscope.utils.constant import Tasks
from .pipeline_tool import ModelscopePipelineTool
from .tool import MAX_RETRY_TIMES
import requests
import json
from requests.exceptions import RequestException, Timeout

DEFAULT_TARGET = "glucose"
PATH_MAX_LENGTH = 3

# TODO 先不做这个了
class SearchReactionTool(ModelscopePipelineTool):
    default_model = ''
    description = '从reaction数据库中搜索合成反应式'
    name = 'kongfoo_graph-search-path'
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

    def _build_query_url(self, obj: str):
        return f"{self.url.rstrip('/')}/{obj}"

    def _single_remote_call(self, source):
        """单轮查询，从reaction数据库进行检索"""
        origin_result = None
        retry_times = MAX_RETRY_TIMES
        url = self._build_query_url(source)
        while retry_times:
            retry_times -= 1
            try:
                response = requests.request(
                    'GET',
                    url,
                )
                if response.status_code != requests.codes.ok:
                    response.raise_for_status()

                origin_result = response.content.decode('utf-8')
                candidates = []
                for line in origin_result.strip().split("\n"):
                    line = line.strip("\n")
                    if not line or source not in line:
                        continue
                    candidates.append(line)
                return '\n'.join(candidates)
            except Timeout:
                continue
            except RequestException as e:
                raise ValueError(
                    f'Remote call failed with error code: {e.response.status_code},\
                    error message: {e.response.content.decode("utf-8")}')

        raise ValueError(
            'Remote call max retry times exceeded! Please try to use local call.'
        )

    def _remote_call(self, *args, **kwargs):
        if self.url == '':
            raise ValueError(
                f"Could not use remote call for {self.name} since this tool doesn't have a remote endpoint"
            )
        path_counter = 0
        while path_counter <= PATH_MAX_LENGTH:
            pass





