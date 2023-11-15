#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
from config.conf import settings


def get_logger():
    logger = logging.getLogger('main')
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # 创建一个handle写入文件
        fh = logging.FileHandler(settings.log_file, encoding='utf-8')
        fh.setLevel(logging.INFO)

        # 创建一个handle输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义输出的格式
        formatter = logging.Formatter(settings.LOGGER_FORMAT)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 添加到handle
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger


logger = get_logger()


if __name__ == '__main__':
    logger.info('hello world')
    logger.debug('hello world')
    logger.error('hello world')
