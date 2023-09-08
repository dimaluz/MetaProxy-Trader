import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains
from selenium.webdriver.common import actions
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

desired_cap = {
    "platformName": "Android",
    "appium:appPackage": "net.metaquotes.metatrader4",
    "appium:appActivity": "net.metaquotes.metatrader4.ui.MainActivity",
    "appium:app": "C:\\Users\\T. Bannikere\\Downloads\\MetaTrader 4 Forex Trading_400.1388_Apkpure.apk",
    "appium:deviceName": "emulator-5554"
}

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)

# Wait for 10 seconds after the app opens
time.sleep(10)

# Find and click on the "accept" button
el2 = driver.find_element(by=AppiumBy.ID, value="net.metaquotes.metatrader4:id/accept_button")
el2.click()
time.sleep(5)
el2 = driver.find_element(by=AppiumBy.ID, value="net.metaquotes.metatrader4:id/accept_button")
el2.click()
time.sleep(5)
el8 = driver.find_element(by=AppiumBy.ID, value="net.metaquotes.metatrader4:id/actionbar_app_icon")
el8.click()
time.sleep(3)
el13 = driver.find_element(by=AppiumBy.ID, value="net.metaquotes.metatrader4:id/account_mark")
el13.click()
time.sleep(2)
el14 = driver.find_element(by=AppiumBy.XPATH, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.ImageView")
el14.click()
time.sleep(3)
el1 = driver.find_element(by=AppiumBy.XPATH, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.TextView[1]")
el1.click()
time.sleep(2)

try:
    el2 = driver.find_element(by=AppiumBy.ID, value="net.metaquotes.metatrader4:id/filter")
    el2.click()

    # Define the set of letters to iterate through
    letters = 'abcdefghijklmnopqrstuvwxyz'

 # Loop through all combinations of three letters from the defined set and a space
    for i in range(len(letters)):
        for j in range(len(letters)):
            for space in [' ']:
                keys = letters[i] + letters[j] + space
                el2.send_keys(keys)
                time.sleep(2)
                el2.clear()
                time.sleep(1)

except Exception as e:
    print("An error occurred:", e)
time.sleep(3)

driver.quit()
