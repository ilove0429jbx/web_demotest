#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import yaml
from config.conf import settings


class Element(object):
    """获取元素"""

    def __init__(self, name: str):
        self.file_name = '%s.yaml' % name
        self.element_path = os.path.join(settings.ELEMENT_PATH, self.file_name)
        if not os.path.exists(self.element_path):
            raise FileNotFoundError("%s 文件不存在！" % self.element_path)
        with open(self.element_path, encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def __getitem__(self, item: str):
        """获取属性"""
        if not item:
            raise KeyError("关键字不正确")
        data: str = self.data.get(item)
        if not data:
            raise ArithmeticError("{}中不存在关键字：{}".format(self.file_name, item))
        if '==' not in data:
            raise ValueError("{}中{}关键字数据不正确".format(self.file_name, item))
        name, value = data.split('==')
        return name, value


if __name__ == '__main__':
    search = Element('search')
    print(search['搜索框'])
