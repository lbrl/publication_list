#!/usr/bin/env python3

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

wos_id = 5891442
url = f'https://www.webofscience.com/wos/author/record/{wos_id}'

################################################
# WEBDRIVER OPTIONS
################################################

# https://www.selenium.dev/documentation/webdriver/capabilities/
options = Options()

tmp_dir = tempfile.TemporaryDirectory()

# options.set_preference('network.proxy.type', 1)

options.add_argument('-headless')
options.set_preference('browser.download.folderList', 2) # custom location
options.set_preference('browser.download.manager.showWhenStarting', False)
options.set_preference('browser.download.dir', tmp_dir.name)
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain')

s = Service('./geckodriver')
driver = Firefox(service=s, options=options)
wait = WebDriverWait(driver, timeout=20)

################################################
# LOADING PAGE
################################################

driver.get(url)

selector = (By.ID, 'onetrust-accept-btn-handler')
wait.until(expected.element_to_be_clickable(selector)).click()
selector = (By.ID, 'onetrust-policy')
wait.until(expected.invisibility_of_element_located(selector))
print('Accepted cookies')

selector = (By.CLASS_NAME, '_pendo-button')
wait.until(expected.element_to_be_clickable(selector)).click()
wait.until(expected.invisibility_of_element_located(selector))
print('Closed welcome window')

selector = (By.CLASS_NAME, 'view-results-button')
wait.until(expected.element_to_be_clickable(selector)).click()
print('Opened publications list')

selector = (By.ID, 'mat-checkbox-1')
wait.until(expected.element_to_be_clickable(selector)).click()
print('Selected all publications')

selector = (By.XPATH, '//app-export-menu/div')
driver.find_element(*selector).click()
print('Opened save dialog')

selector = (By.ID, 'exportToFieldTaggedButton')
wait.until(expected.element_to_be_clickable(selector)).click()
print('Selected plain text as an export format')

selector = (By.ID, 'exportTrigger')
selector = (By.XPATH, '//div/button')
selector = (By.XPATH, '//span[text() = "Export"]')
wait.until(expected.element_to_be_clickable(selector)).click()
print('Started the export')

content = open(f'{tmp_dir.name}/savedrecs.txt').read()

open('wos.txt', 'w').write(content)

driver.quit()

# for url in urls:

# if __name__ == '__main__':
#     main()

