from PIL import Image, ImageChops
from selenium import webdriver
import time
import yagmail
from yagmail.sender import SMTP

yag = yagmail.SMTP('teencourtnotifier')

url = 'https://www.collincountytx.gov/teencourt/Pages/TCCalendar.aspx?visibleDate=9%2f1%2f2021'

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
        yag.send('amritg7709@gmail.com', 'New listing', 'Please check or update notifier')
    else:
        print("No change")
        