# Import modules
import time
import os
from PIL import Image
from selenium import webdriver
import yagmail 

# Create driver instance of webdriver
driver = webdriver.Safari()

# Create yag instance of yagmail to send from teencourtnotifier
'''
    Note! Before you create yag, you must register your username and password using the module. 
    Run this line of code ONLY once from ANYWHERE:
    
        yagmail.register(username, password)
    
    This eliminates the need for setting environment variables as you are only doing it once, not writing it directly into your code. 
    Afterwards, all you have to do is create a yag object that takes only your username. If you'd like, you can set that up as an env var.
'''
yag = yagmail.SMTP('SenderEmailUsername')

# Function to conver ta screenshot to a list of pixels
def pixelconverter(screenshotfile):
    # Using image module to open file and convert to a list of pixels
    unconvertedimage = Image.open(screenshotfile)
    image_pix_list = list(unconvertedimage.getdata())
    return(image_pix_list)

# Procedure to remove and create a new screenshot
def makess(screenshotfile):
    # Check if screenshot exists already and delete if it does
    if os.path.isfile(screenshotfile) == True:
        os.remove(screenshotfile)
    else:
        pass
    # Save a screenshot (asumming pre-initialized webdriver session)
    time.sleep(10) # Delay is needed! To make a reliable screenshot.
    driver.save_screenshot(screenshotfile)

# Function to return the difference between two lists
def lists_diff(list1, list2):
    return (list(set(list1)-set(list2)))

# Remove and replace original --> called only once
url = ''
driver.get(url)
driver.fullscreen_window()

driver.refresh()

makess('ogss.png')

# Calling pixelconverter function to return ogss as a list of pixels
originalpixels = pixelconverter('ogss.png')

try: # The try/except allows for the user to keyboard stop the program (cntrl + C) and pass on from the infinite loop to the driver.quit method
    while True:

        driver.refresh()
        time.sleep(10)

        makess('newss.png')
        newpixels = pixelconverter('newss.png')
        
        # Comparing new to old and seeing if there has been a change
        wad = lists_diff(newpixels, originalpixels)

        if len(wad) > 5000:
            print('There has been a SIGNIFICANT change of {0} pixels.'.format(len(wad)))
            yag.send('recipient@email.com', subject = 'Something has changed', contents = 'Check webpage or update driver.')
        else:
            print('There has been a change of {0} pixels.'.format(len(wad)))
        
        originalpixels = newpixels
     
except:
    pass

driver.quit()
