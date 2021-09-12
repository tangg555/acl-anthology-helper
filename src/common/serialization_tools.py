"""
@Reference:
https://blog.csdn.net/dou_being/article/details/82290588
https://blog.csdn.net/zywvvd/article/details/106131555
"""

import json


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception:
            return obj.__str__()
