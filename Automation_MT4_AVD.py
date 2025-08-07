import time
import random
import string
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains
from selenium.webdriver.common import actions
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

# Конфигурация поиска
SEARCH_COMBINATIONS_COUNT = 100  # Количество уникальных комбинаций для поиска
SEARCH_DELAY = 2  # Задержка после ввода поиска (секунды)
CLEAR_DELAY = 1   # Задержка после очистки поля (секунды)

def generate_search_combinations(num_combinations=100):
    """
    Генерирует список уникальных случайных комбинаций из букв и цифр длиной 3 символа
    
    Args:
        num_combinations (int): Количество комбинаций для генерации
    
    Returns:
        list: Список уникальных строк длиной 3 символа
    """
    # Создаем набор символов: буквы (a-z) + цифры (0-9)
    characters = string.ascii_lowercase + string.digits
    combinations = set()
    
    # Генерируем уникальные комбинации
    while len(combinations) < num_combinations:
        # Генерируем случайную комбинацию из 3 символов
        combination = ''.join(random.choices(characters, k=3))
        combinations.add(combination)
    
    # Возвращаем в виде списка для удобства итерации
    return list(combinations)

# ============================================================================
# НАСТРОЙКА ДЛЯ ANDROID STUDIO AVD
# ============================================================================
# 1. Запустите AVD в Android Studio
# 2. Выполните команду: adb devices
# 3. Скопируйте deviceName из вывода команды
# 4. Укажите правильный путь к APK файлу

desired_cap = {
    "platformName": "Android",
    "appium:appPackage": "net.metaquotes.metatrader4",
    "appium:appActivity": "net.metaquotes.metatrader4.ui.MainActivity",
    # ИЗМЕНИТЬ: Укажите правильный путь к APK файлу
    "appium:app": "/path/to/MetaTrader4.apk",  # ← ИЗМЕНИТЬ
    # ИЗМЕНИТЬ: Укажите deviceName вашего AVD (получить через adb devices)
    "appium:deviceName": "emulator-5554"        # ← ИЗМЕНИТЬ
}

# ============================================================================
# ПРОВЕРКА ПОДКЛЮЧЕНИЯ
# ============================================================================
print("🚀 Запуск автоматизации для Android Studio AVD")
print("📱 Device Name:", desired_cap["appium:deviceName"])
print("📦 APK Path:", desired_cap["appium:app"])
print("🔍 Проверьте правильность настроек выше!")

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
el1 = driver.find_element(by=AppiumBy.XPATH, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.TextView[1]")
el1.click()
time.sleep(2)

try:
    el2 = driver.find_element(by=AppiumBy.ID, value="net.metaquotes.metatrader4:id/filter")
    el2.click()

    # Генерируем случайные комбинации для поиска
    search_combinations = generate_search_combinations(num_combinations=SEARCH_COMBINATIONS_COUNT)
    
    print(f"Начинаем поиск с {len(search_combinations)} уникальными комбинациями...")
    
    # Проходим по всем сгенерированным комбинациям
    for idx, combination in enumerate(search_combinations, 1):
        try:
            print(f"Поиск {idx}/{len(search_combinations)}: '{combination}'")
            
            # Вводим комбинацию в поле поиска
            el2.send_keys(combination)
            time.sleep(SEARCH_DELAY)  # Ждем загрузки результатов
            
            # Очищаем поле для следующего поиска
            el2.clear()
            time.sleep(CLEAR_DELAY)  # Небольшая пауза между поисками
            
        except Exception as search_error:
            print(f"Ошибка при поиске '{combination}': {search_error}")
            continue

except Exception as e:
    print("Произошла ошибка при инициализации поиска:", e)
time.sleep(3)

driver.quit() 