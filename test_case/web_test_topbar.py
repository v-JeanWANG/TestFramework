# coding=utf-8

import sys
import os
sys.path.append(os.path.dirname(os.getcwd())+os.path.sep+".")
sys.path.append(os.getcwd())

import time
import unittest
from businessview.web.common.login_business import simple_login
from businessview.web.common.stream_topbar_business import *
from utilstest.base_runner import BaseWebTestCase
from utilstest.base_yaml import Yaml
from common.browser_engine import Logger


class web_test(BaseWebTestCase):
    def __init__(self, *args, **kwargs):
        BaseWebTestCase.__init__(self, *args, **kwargs)
        self.data = Yaml(Yaml.web_config_path).read()
        self.env = self.data['env']
        self.homeUrl = self.data['portal'][self.env].rstrip("/")

    def test_mainpage(self):
        self.driver = simple_login()
        stream_topbar_business = Stream_topbar_business(self.driver)

        #scenario 1, verify topbar button
        # home button
        stream_topbar_business.click_topbar_button_home()
        self.assertTrue(self.driver.current_url.rstrip("/") == self.homeUrl, '正在浏览主页')

        # discover button
        button, menu = stream_topbar_business.click_topbar_button_discover()
        self.assertTrue(button.get_attribute("aria-expanded") == 'true', '展开discover菜单')
        self.assertTrue(menu.get_attribute("aria-hidden") == 'false', '显示discover菜单')
        button, menu = stream_topbar_business.click_topbar_button_discover()
        self.assertTrue(button.get_attribute("aria-expanded") == 'false', '收起discover菜单')
        self.assertTrue(menu.get_attribute("aria-hidden") == 'true', '隐藏discover菜单')
        button, menu = stream_topbar_business.click_topbar_button_discover()
        self.assertTrue(button.get_attribute("aria-expanded") == 'true', '展开discover菜单')
        self.assertTrue(menu.get_attribute("aria-hidden") == 'false', '显示discover菜单')
        stream_topbar_business.click_topbar_button_home()
        self.assertTrue(self.driver.current_url.rstrip("/") == self.homeUrl, '正在浏览主页')
        self.assertTrue(button.get_attribute("aria-expanded") == 'false', '收起discover菜单')
        self.assertTrue(menu.get_attribute("aria-hidden") == 'true', '隐藏discover菜单')

        #scenario 2 verify topbar menu
        # discover menu
        stream_topbar_business.click_topbar_button_home()
        self.assertTrue(self.driver.current_url.rstrip("/") == self.homeUrl, '正在浏览主页')
        for it in stream_topbar_business._page.discover_dropdown_menu_tuple:
            button, menu = stream_topbar_business.click_topbar_button_discover()
            self.assertTrue(button.get_attribute("aria-expanded") == 'true', '展开discover菜单')
            self.assertTrue(menu.get_attribute("aria-hidden") == 'false', '显示discover菜单')
            link_element = stream_topbar_business.find_element(*it)
            expect_url = link_element.get_attribute("href")
            stream_topbar_business.click_topbar_link(it)
            self.assertTrue(self.driver.current_url.rstrip("/") == expect_url, '正在浏览 ' + expect_url)
            stream_topbar_business.click_topbar_button_home()
            self.assertTrue(self.driver.current_url.rstrip("/") == self.homeUrl, '正在浏览主页')

if __name__ == '__main__':
    unittest.main()