#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
selenium基类
本文件存放了selenium基类的封装方法
"""
from typing import Union, Callable
from selenium.webdriver import Chrome, Firefox, Edge, Ie, Opera, Safari, Remote
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config.conf import settings
from utils.times import sleep
from utils.logger import logger


class WebPage(object):
    """selenium基类"""

    def __init__(self, driver):
        self.driver: Union[Chrome, Firefox, Edge, Ie, Opera, Safari, Remote] = driver
        self.timeout: int = 20
        self.wait: WebDriverWait = WebDriverWait(self.driver, self.timeout)

    def get_url(self, url):
        """打开网址并验证"""
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            logger.info("打开网页：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    @staticmethod
    def element_locator(func: Callable, locator: tuple):
        """元素定位器"""
        logger.info("locator is:{}".format(locator))
        name, value = locator
        return func(settings.LOCATE_MODE[name], value)

    def find_element(self, locator: tuple):
        """寻找单个元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)

    def find_elements(self, locator: tuple):
        """查找多个相同的元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def elements_num(self, locator: tuple) -> int:
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        logger.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, locator: tuple, txt: str):
        """输入(输入前先清空)"""
        sleep(0.5)
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(txt)
        logger.info("输入文本：{}".format(txt))

    def click(self, locator: tuple):
        """点击"""
        self.find_element(locator).click()
        sleep()
        logger.info("点击元素：{}".format(locator))

    def is_visible(self, locator: tuple) -> bool:
        """元素是否可见"""
        try:
            ele = WebPage.element_locator(lambda *args: self.visible_obj.until(
                EC.visibility_of_element_located(args), locator))
            if ele:
                return True
            return False
        except TimeoutException:
            return False

    def element_text(self, locator: tuple):
        """获取当前的text"""
        _text = self.find_element(locator).text
        logger.info("获取文本：{}".format(_text))
        return _text

    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)


if __name__ == "__main__":
    pass
