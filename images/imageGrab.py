import os
import random
import numpy as np
import pyautogui
from PIL import Image
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Location of all folders
folders = "D:\\CNN\\images\\"

'''
These few lines set options to open your normal Chrome browser
To find the below argument go to chrome://version/ on Chrome and copy the Profile Path and remove "\Default"
'''
options = Options()
options.add_argument("user-data-dir=C:\\Users\\Russ\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(executable_path="D:\\CNN\\images\\chromedriver.exe", options=options)
driver.get("https://www.google.co.in")
driver.close()


# Method that will take a screenshot and crop the image to 512px x 512px
def take_screenshot(country, dir):
    if dir == "train":
        folder = "train\\"
    if dir == "valid":
        folder = "valid\\"
    if dir == "test":
        folder = "test\\"
    myScreenshot = pyautogui.screenshot()
    filePath = folders + folder + country
    path, dirs, files = next(os.walk(filePath))

    # If the folder is empty, start numbering at 10,000
    if len(os.listdir(filePath)) == 0:
        k = 10000

    # Otherwise, add one to the highest number
    else:
        k = int(files[-1].replace(country, "").replace(".jpg", "")) + 1

    imageFilePath = filePath + "\\" + country + str(k) + ".jpg"
    myScreenshot.save(imageFilePath)

    # Make images 512px x 512px
    img = Image.open(imageFilePath)
    cropped_img = img.crop((625, 230, 1137, 742))
    cropped_img.save(imageFilePath)


# Method that will take the screenshots in Geoguessr
def compile_screenshots(country, options, dir):
    countryNoSpaces = country.replace(" ", "")

    # Open browser
    driver = webdriver.Chrome(executable_path="D:\\CNN\\images\\chromedriver.exe", options=options)
    driver.maximize_window()

    # Open Geoguessr Explorer mode and select the country
    # implicitly.wait() will wait on the webpage to fully load
    driver.get("https://www.geoguessr.com/explorer")
    driver.implicitly_wait(3)

    # Select the explorer mode that matches the country you specify
    driver.find_element_by_xpath("//a[.='" + country + "']").click()
    driver.implicitly_wait(3)

    # Loop until you want to end the screenshots, then close browser
    while True:
        # Click "PLAY" and "START GAME"
        # I recommend you select "No move" beforehand to remove the white arrows
        driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div[1]/div[4]/button').click()
        driver.implicitly_wait(3)
        driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[4]/button').click()

        # Loop through 5 rounds
        for i in range(5):
            # Take screenshot of starting screen
            # sleep() gives the program enough time to take a screenshot, save it, and crop it
            sleep(2)
            take_screenshot(countryNoSpaces, dir)
            sleep(2)

            # A series of actions to click on the map and deviate a little
            # I added this feature to avoid bot-detection
            action = webdriver.ActionChains(driver)
            element = driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div[3]/div/div[3]/div/div/div/div/div[2]/div[3]')
            action.move_to_element(element)
            action.move_by_offset(-475+np.random.normal(0, 15, 1), -250+np.random.normal(0, 25, 1))     # 10px to the right 20px to bottom
            action.click()
            action.perform()
            sleep(round(random.uniform(1, 2), 2))

            # Click "GUESS"
            driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div[3]/div/div[4]/button').click()
            driver.implicitly_wait(3)

            if i == 4:
                # Click "VIEW SUMMARY" and "PLAY THE SAME MAP AGAIN"
                driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div/div/div/div[1]/div/div/section/section[3]/button').click()
                driver.implicitly_wait(3)
                driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[1]/div/div/div[1]/div/div/div[3]/div/a[2]').click()
                driver.implicitly_wait(3)

            else:
                # Click "PLAY NEXT ROUND"
                driver.find_element_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div/div/div/div[1]/div/div/section/section[3]/button').click()
                driver.implicitly_wait(3)


# Taking the screenshots, select country below
country = "United Kingdom"                                         # Spell with spaces, case sensitive
compile_screenshots(country, options, "valid")                # run this until desired number of photos
