from PIL import Image, ImageChops
from selenium import webdriver
import time
import yagmail
from yagmail.sender import SMTP

"""
    With yagmail, you can register your username and password once in one line of code, from any file.
    yagmail.register('your username', 'your password')
    
    So that you don't have to write password directly into code.
    Aditionally, you can set up envrion variables on your computer to store username and password, so you don't have to add either.
"""

yag = yagmail.SMTP("PASTE SENDER USERNAME HERE)

url = "PASTE URL HERE"

driver = webdriver.Safari()
driver.get(url)
driver.fullscreen_window()

time.sleep(5)

driver.save_screenshot('im1.png')


while True:
    driver.refresh()
    time.sleep(5)

    driver.save_screenshot('im2.png')

    im1 = Image.open('im1.png')
    im2 = Image.open('im2.png')

    imdifference = ImageChops.difference(im1, im2)

    if imdifference.getbbox():
        print("Change.")
        yag.send('RECIPIENT FULL EMAIL', 'New change', 'Please check website or update notifier')
    else:
        print("No change")
        
