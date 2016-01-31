#!/bin/env python
# Hide your Facebook posts by changing their privacy settings to "Only Me"
# Requires selenium with python bindings
# Tested with Firefox driver
# 31 Jan 2016
# @singe

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, re
from IPython import embed

class FbLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.facebook.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_fb_login(self):
        driver = self.driver

        #Login
        driver.get("https://login.facebook.com/login.php")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("PUT YOUR USERNAME HERE")
        driver.find_element_by_id("pass").clear()
        driver.find_element_by_id("pass").send_keys("PUT YOUR PASSWORD HERE")
        driver.find_element_by_id("u_0_2").click()
        time.sleep(3)

        #Save browser warning
        #driver.find_element_by_id("u_0_2").click()
        #driver.find_element_by_id("checkpointSubmitButton").click()

        driver.get(self.base_url + "PUT YOUR FB USERNAME HERE (NOT YOUR EMAIL ADDRESS)/allactivity")
        posts = []
        index = -1 
        while True:
            count = 0
            for divs in driver.find_elements_by_xpath("//div[@class='uiSelector inlineBlock audienceSelector audienceSelectorNoTruncate dynamicIconSelector uiSelectorRight uiSelectorNormal uiSelectorDynamicTooltip']"):
                if count <= index:
                    print('continue '+str(count)+' index '+str(index))
                    count = count + 1
                    continue
                #embed()
                try:
                    actions = ActionChains(driver)
                    actions.move_to_element(divs)
                    actions.perform()
                    print('move to div '+str(count)+' index '+str(index))
                    foo=divs.find_element_by_xpath(".//a[@class='uiSelectorButton uiButton uiButtonSuppressed uiButtonNoText']")
                except NoSuchElementException:
                    driver.find_element_by_tag_name('body').click()
                    actions = ActionChains(driver)
                    actions.move_to_element(divs)
                    actions.perform()
                    foo=divs.find_element_by_xpath(".//a[@class='uiSelectorButton uiButton uiButtonSuppressed uiButtonNoText']")
                try:
                    posts.index(foo)
                except ValueError:
                    posts.append(foo) 
                    index = posts.index(foo)
                    print('add to index '+str(count)+' index '+str(index))
                    actions = ActionChains(driver)
                    actions.move_to_element(foo)
                    actions.perform()
                    #foo.send_keys(Keys.ENTER)
                    if foo.get_attribute('aria-label') != 'Only Me':
                        foo.send_keys(Keys.ENTER)
                        time.sleep(0.5)
                        divs.find_element_by_xpath(".//li[@data-label='Only Me']/a").send_keys(Keys.ENTER)
                        #foo.send_keys(Keys.SPACE)
                        #time.sleep(0.5)
                        #divs.find_element_by_xpath(".//li[@data-label='Only Me']/a").click()
                count = count + 1

            baz=driver.find_element_by_xpath("//a[@title='Make your next career move to our brilliant company.']")
            actions = ActionChains(driver)
            actions.move_to_element(baz)
            actions.perform()
            baz.send_keys(Keys.SPACE)
            baz=driver.find_element_by_xpath("//span[@class='uiMorePagerLoader pam uiBoxLightblue']")
            baz.send_keys(Keys.SPACE)
            time.sleep(2)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
