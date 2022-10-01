import os
import base64
import io
import sys
import uuid
import time as clock
from time import sleep
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytesseract import image_to_string
from PIL import Image

start = clock.time()

headless = True
max_try = 10

if headless == True:
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--log-level=3')
  driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
else:
  driver = webdriver.Chrome(executable_path='./chromedriver')

vehicle_number = sys.argv[1]

url = 'https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml'
get_data_url_script = ("window.getDataUrl = function (img) {"
                       "var canvas = document.createElement('canvas');"
                       "var ctx = canvas.getContext('2d');"
                       "canvas.width = img.width;"
                       "canvas.height = img.height;"
                       "ctx.drawImage(img, 0, 0);"
                       "return canvas.toDataURL();"
                       "}")

rc_details_panel = ''

for i in range(1, max_try):
  # hit the URL
  driver.get(url)

  # vehicle number textbox
  vehicle_textbox = driver.find_element_by_id("regn_no1_exact")
  vehicle_textbox.clear()
  vehicle_textbox.send_keys(vehicle_number)

  # get the captcha image
  driver.execute_script(get_data_url_script)
  imgstring = driver.execute_script("return window.getDataUrl($('img')[1])")
  # get the base64 string
  imgstring = imgstring.split('base64,')[-1].strip()
  image = base64.b64decode(imgstring)
  # get the image object
  img = Image.open(io.BytesIO(image))

  # get the captcha value from image
  captcha_value = image_to_string(
      img, lang='eng', config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

  # captcha textbox
  captcha_textbox = driver.find_element_by_id("txt_ALPHA_NUMERIC")
  captcha_textbox.clear()
  captcha_textbox.send_keys(captcha_value)  # captcha value

  #submit button
  submit_button = driver.find_element_by_xpath('//button[@type="submit"]')
  submit_button.click()

  try:
    # wait for spinner to get hidden for 20 seconds
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'ui-blockui')]")))
    # main panel which has the result data
    rc_details_panel = driver.find_element_by_id('rcDetailsPanel').text
    break
  except exceptions.NoSuchElementException as e:
    # if captcha value is wrong; run the loop again until it doesn't provide the info
    pass

if rc_details_panel == '':
  print('No details found.')
else:
  print(rc_details_panel)

end = clock.time()
print(end - start)
