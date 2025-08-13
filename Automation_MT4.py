import time
import random
import string
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Конфигурация поиска
SEARCH_COMBINATIONS_COUNT = 100  # Количество уникальных комбинаций для поиска
SEARCH_DELAY = 2  # Задержка после ввода поиска (секунды)
CLEAR_DELAY = 1   # Задержка после очистки поля (секунды)

# Конфигурация ожидания элементов
WAIT_TIMEOUT = 30  # Максимальное время ожидания элемента (секунды)
POLL_FREQUENCY = 0.5  # Частота проверки элемента (секунды)

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

def safe_click_element(driver, wait, locator, locator_value, action_description):
    """
    Безопасный клик по элементу с ожиданием и обработкой ошибок
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        locator: Тип локатора (AppiumBy.ID, AppiumBy.XPATH, etc.)
        locator_value: Значение локатора
        action_description: Описание действия для логирования
    
    Returns:
        bool: True если клик успешен, False если произошла ошибка
    """
    try:
        print(f"🔍 Ожидаем элемент для: {action_description}")
        element = wait.until(EC.element_to_be_clickable((locator, locator_value)))
        print(f"✅ Кликаем: {action_description}")
        element.click()
        return True
    except TimeoutException:
        print(f"❌ Таймаут ожидания элемента: {action_description}")
        print(f"   Локатор: {locator} = '{locator_value}'")
        return False
    except Exception as e:
        print(f"❌ Ошибка при клике: {action_description}")
        print(f"   Ошибка: {str(e)}")
        return False

def safe_send_keys(driver, wait, locator, locator_value, text, action_description):
    """
    Безопасный ввод текста с ожиданием и обработкой ошибок
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        locator: Тип локатора
        locator_value: Значение локатора
        text: Текст для ввода
        action_description: Описание действия для логирования
    
    Returns:
        bool: True если ввод успешен, False если произошла ошибка
    """
    try:
        print(f"🔍 Ожидаем поле ввода для: {action_description}")
        element = wait.until(EC.element_to_be_clickable((locator, locator_value)))
        print(f"📝 Вводим текст: '{text}' - {action_description}")
        element.clear()
        element.send_keys(text)
        return True
    except TimeoutException:
        print(f"❌ Таймаут ожидания поля ввода: {action_description}")
        print(f"   Локатор: {locator} = '{locator_value}'")
        return False
    except Exception as e:
        print(f"❌ Ошибка при вводе текста: {action_description}")
        print(f"   Ошибка: {str(e)}")
        return False

def safe_clear_field(driver, wait, locator, locator_value, action_description):
    """
    Безопасная очистка поля с ожиданием и обработкой ошибок
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        locator: Тип локатора
        locator_value: Значение локатора
        action_description: Описание действия для логирования
    
    Returns:
        bool: True если очистка успешна, False если произошла ошибка
    """
    try:
        print(f"🧹 Очищаем поле: {action_description}")
        element = wait.until(EC.element_to_be_clickable((locator, locator_value)))
        element.clear()
        return True
    except TimeoutException:
        print(f"❌ Таймаут ожидания поля для очистки: {action_description}")
        return False
    except Exception as e:
        print(f"❌ Ошибка при очистке поля: {action_description}")
        print(f"   Ошибка: {str(e)}")
        return False

# ============================================================================
# НАСТРОЙКА ДЛЯ ФИЗИЧЕСКОГО УСТРОЙСТВА SAMSUNG A50
# ============================================================================
# 1. Подключите Samsung A50 через USB
# 2. Включите режим разработчика и USB отладку
# 3. Выполните команду: adb devices
# 4. Скопируйте deviceName из вывода команды
# 5. Убедитесь, что MetaTrader 4 установлен на устройстве

desired_cap = {
    "platformName": "Android",
    "appium:appPackage": "net.metaquotes.metatrader4",
    "appium:appActivity": "net.metaquotes.metatrader4.ui.MainActivity",
    # ИЗМЕНИТЬ: Укажите deviceName вашего Samsung A50 (получить через adb devices)
    "appium:deviceName": "Samsung_A50",  # ← ИЗМЕНИТЬ на реальное имя устройства
    # Убираем appium:app так как приложение уже установлено на устройстве
    "appium:automationName": "UiAutomator2",
    "appium:noReset": True,  # Не сбрасывать данные приложения
    "appium:newCommandTimeout": 300,  # Таймаут команд (5 минут)
    "appium:autoGrantPermissions": True  # Автоматически давать разрешения
}

# ============================================================================
# ИНИЦИАЛИЗАЦИЯ И ПРОВЕРКА ПОДКЛЮЧЕНИЯ
# ============================================================================
print("🚀 Запуск автоматизации для физического устройства Samsung A50")
print("📱 Device Name:", desired_cap["appium:deviceName"])
print("📦 App Package:", desired_cap["appium:appPackage"])
print("🔍 Проверьте правильность настроек выше!")

try:
    # Инициализация WebDriver
    print("🔌 Подключение к Appium Server...")
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    
    # Инициализация WebDriverWait
    wait = WebDriverWait(driver, WAIT_TIMEOUT, poll_frequency=POLL_FREQUENCY)
    
    print("✅ Успешно подключились к устройству!")
    
except WebDriverException as e:
    print(f"❌ Ошибка подключения к Appium Server: {str(e)}")
    print("💡 Убедитесь, что:")
    print("   - Appium Server запущен на порту 4723")
    print("   - Устройство подключено и доступно через adb devices")
    print("   - Device Name указан правильно")
    exit(1)

# ============================================================================
# ОЖИДАНИЕ ЗАГРУЗКИ ПРИЛОЖЕНИЯ
# ============================================================================
print("⏳ Ожидаем загрузки приложения MetaTrader 4...")
time.sleep(5)  # Базовое ожидание загрузки приложения

# ============================================================================
# ОБРАБОТКА ДИАЛОГОВ ПРИЛОЖЕНИЯ
# ============================================================================

# Обработка кнопки "accept" (может появиться несколько раз)
accept_button_id = "net.metaquotes.metatrader4:id/accept_button"
max_accept_attempts = 3

for attempt in range(max_accept_attempts):
    if safe_click_element(driver, wait, AppiumBy.ID, accept_button_id, f"Кнопка accept (попытка {attempt + 1})"):
        print(f"✅ Приняли условия (попытка {attempt + 1})")
        time.sleep(2)  # Небольшая пауза между попытками
    else:
        print(f"ℹ️ Кнопка accept не найдена (попытка {attempt + 1}) - продолжаем")
        break

# ============================================================================
# НАВИГАЦИЯ ПО ПРИЛОЖЕНИЮ
# ============================================================================

# Клик по иконке приложения в action bar
if not safe_click_element(driver, wait, AppiumBy.ID, "net.metaquotes.metatrader4:id/actionbar_app_icon", "Иконка приложения в action bar"):
    print("⚠️ Не удалось найти иконку приложения - продолжаем...")

# Клик по метке аккаунта
if not safe_click_element(driver, wait, AppiumBy.ID, "net.metaquotes.metatrader4:id/account_mark", "Метка аккаунта"):
    print("⚠️ Не удалось найти метку аккаунта - продолжаем...")

# Клик по изображению (возможно, для открытия меню)
# ВАЖНО: Этот XPath может отличаться на реальном устройстве!
# Проверьте через Appium Inspector и обновите при необходимости
xpath_image = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.ImageView"

if not safe_click_element(driver, wait, AppiumBy.XPATH, xpath_image, "Изображение в меню"):
    print("⚠️ Не удалось найти изображение в меню - продолжаем...")
    print("💡 Проверьте XPath через Appium Inspector для вашего устройства")

# Клик по первому текстовому элементу (возможно, для открытия списка брокеров)
# ВАЖНО: Этот XPath может отличаться на реальном устройстве!
# Проверьте через Appium Inspector и обновите при необходимости
xpath_text = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.TextView[1]"

if not safe_click_element(driver, wait, AppiumBy.XPATH, xpath_text, "Первый текстовый элемент"):
    print("⚠️ Не удалось найти текстовый элемент - продолжаем...")
    print("💡 Проверьте XPath через Appium Inspector для вашего устройства")

# ============================================================================
# ПОИСК И ФИЛЬТРАЦИЯ БРОКЕРОВ
# ============================================================================

try:
    print("🔍 Ищем поле фильтра...")
    
    # Ожидаем появления поля фильтра
    filter_element = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "net.metaquotes.metatrader4:id/filter")))
    print("✅ Поле фильтра найдено")
    
    # Кликаем по полю фильтра
    filter_element.click()
    print("✅ Кликнули по полю фильтра")

    # Генерируем случайные комбинации для поиска
    search_combinations = generate_search_combinations(num_combinations=SEARCH_COMBINATIONS_COUNT)
    
    print(f"🚀 Начинаем поиск с {len(search_combinations)} уникальными комбинациями...")
    
    # Проходим по всем сгенерированным комбинациям
    successful_searches = 0
    failed_searches = 0
    
    for idx, combination in enumerate(search_combinations, 1):
        try:
            print(f"\n📝 Поиск {idx}/{len(search_combinations)}: '{combination}'")
            
            # Вводим комбинацию в поле поиска
            if safe_send_keys(driver, wait, AppiumBy.ID, "net.metaquotes.metatrader4:id/filter", combination, f"Ввод '{combination}'"):
                successful_searches += 1
                print(f"✅ Успешно ввели '{combination}'")
                
                # Ждем загрузки результатов
                time.sleep(SEARCH_DELAY)
                
                # Очищаем поле для следующего поиска
                if safe_clear_field(driver, wait, AppiumBy.ID, "net.metaquotes.metatrader4:id/filter", f"Очистка после '{combination}'"):
                    print(f"✅ Успешно очистили поле после '{combination}'")
                    time.sleep(CLEAR_DELAY)
                else:
                    print(f"⚠️ Не удалось очистить поле после '{combination}'")
                    failed_searches += 1
            else:
                print(f"❌ Не удалось ввести '{combination}'")
                failed_searches += 1
                
        except Exception as search_error:
            print(f"❌ Ошибка при поиске '{combination}': {search_error}")
            failed_searches += 1
            continue

    # Выводим итоговую статистику
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"✅ Успешных поисков: {successful_searches}")
    print(f"❌ Неудачных поисков: {failed_searches}")
    print(f"📈 Процент успеха: {(successful_searches / len(search_combinations) * 100):.1f}%")

except TimeoutException:
    print("❌ Не удалось найти поле фильтра")
    print("💡 Возможные причины:")
    print("   - Приложение не загрузилось полностью")
    print("   - Изменился интерфейс приложения")
    print("   - Элемент имеет другой ID на вашем устройстве")
    print("   - Проверьте через Appium Inspector актуальный ID элемента")
except Exception as e:
    print(f"❌ Произошла ошибка при инициализации поиска: {e}")

# ============================================================================
# ЗАВЕРШЕНИЕ РАБОТЫ
# ============================================================================
print("\n🏁 Завершение работы...")
time.sleep(3)

try:
    driver.quit()
    print("✅ Драйвер успешно закрыт")
except Exception as e:
    print(f"⚠️ Ошибка при закрытии драйвера: {e}")

print("🎉 Автоматизация завершена!")
