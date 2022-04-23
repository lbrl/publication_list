#!/usr/bin/env python3

################################################
# NOTE: This has to be done through institution network (or through a proxy)
# Otherwise, full scopus data will not be available
################################################

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# https://www.browserstack.com/guide/selenium-wait-for-page-to-load
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By

# For saving CSV file
import tempfile

# urls = open('config.txt', 'r').readlines()

scopus_id = 57219793453
url = f'https://www.scopus.com/authid/detail.uri?authorId={scopus_id}'

################################################
# WEBDRIVER OPTIONS
################################################

# https://www.selenium.dev/documentation/webdriver/capabilities/
options = Options()

options.set_preference('network.proxy.type', 1)
options.set_preference("network.proxy.socks", "localhost");     
options.set_preference("network.proxy.socks_port", 9200);

# options.add_argument('-headless')

# tmp_dir = tempfile.TemporaryDirectory()
# options.set_preference('browser.download.folderList', 2) # custom location
# options.set_preference('browser.download.manager.showWhenStarting', False)
# options.set_preference('browser.download.dir', tmp_dir.name)
# options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')

s = Service('./geckodriver')
driver = Firefox(service=s, options=options)
wait = WebDriverWait(driver, timeout=15)

################################################
# LOADING PAGE
################################################

driver.get(url)

# TODO: There is a direct link "Export all", it probably can be used in our case

selector = (By.XPATH, '//a[@title="View list in search results format ' +\
    'for more sorting options and/or to view a full list of documents"]')
wait.until(expected.element_to_be_clickable(selector)).click()
print('Opened publications list')

# TODO: Can just extract HTML parameters from URL and go to this link:
# https://www.scopus.com/onclick/export.uri?oneClickExport=%7b%22Format%22%3a%22TEXT%22%2c%22View%22%3a%22CiteOnly%22%7d&sid=abd6d446a0ec7d3806f1404848fe4c20&sort=plf-f&origin=resultslist&src=s&zone=resultsListHeader&dataCheckoutTest=false&txGid=69af84b4550131066c8103da6f75fd10

selector = (By.ID, 'selectAllCheck')
wait.until(expected.element_to_be_clickable(selector)).click()
print('Selected all publications')

selector = (By.ID, 'export_results')
driver.find_element(*selector).click()
print('Opened save dialog')

selector = (By.XPATH, '//label[@for="TEXT"]')
wait.until(expected.element_to_be_clickable(selector)).click()
print('Selected plain text as an export format')

selector = (By.ID, 'exportTrigger')
wait.until(expected.element_to_be_clickable(selector)).click()
print('Started the export')

import time; time.sleep(2)
driver.switch_to.window(driver.window_handles[1])
selector = (By.XPATH, '//body')
text = wait.until(expected.visibility_of_element_located(selector)).text
# text = driver.find_element(By.XPATH, '//body').text

if len(text) > 1:
    open('scopus.txt', 'w').write(text)
else:
    raise RuntimeError('Empty result from the export page. Maybe sleep time was too short?')

# driver.quit()

