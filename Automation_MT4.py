import os
import shutil
import time
import csv

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Конфигурация поиска
KEYWORDS_CSV_FILE = "keywords.csv"  # Путь к файлу с ключевыми словами
SEARCH_DELAY = 2  # Задержка после ввода поиска (секунды)
CLEAR_DELAY = 1   # Задержка после очистки поля (секунды)

# Конфигурация ожидания элементов
WAIT_TIMEOUT = 30  # Максимальное время ожидания элемента (секунды)
POLL_FREQUENCY = 0.5  # Частота проверки элемента (секунды)


def load_keywords_from_csv(csv_file_path):
    """
    Загружает ключевые слова из CSV файла
    Каждая строка в файле представляет собой отдельную поисковую комбинацию
    """
    keywords = []
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row and row[0].strip():  # Проверяем, что строка не пустая
                    keywords.append(row[0].strip())
        print(f"✅ Загружено {len(keywords)} ключевых слов из {csv_file_path}")
        return keywords
    except FileNotFoundError:
        print(f"❌ Файл не найден: {csv_file_path}")
        return []
    except Exception as e:
        print(f"❌ Ошибка при чтении файла {csv_file_path}: {str(e)}")
        return []


def safe_click_element(driver, wait, locator, locator_value, action_description):
    """Безопасный клик по элементу с ожиданием и обработкой ошибок"""
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
    """Безопасный ввод текста с ожиданием и обработкой ошибок"""
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
    """Безопасная очистка поля с ожиданием и обработкой ошибок"""
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


def preflight_checks():
    """Печатает полезные проверки окружения перед стартом сессии Appium."""
    print("🔎 Preflight checks:")
    sdk_root = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME")
    if not sdk_root:
        print("⚠️  ANDROID_SDK_ROOT / ANDROID_HOME не установлены. Рекомендуется прописать:")
        print("   ANDROID_SDK_ROOT=%LOCALAPPDATA%\\Android\\Sdk")
    else:
        print(f"✅ ANDROID_SDK_ROOT/ANDROID_HOME: {sdk_root}")

    adb_path = shutil.which("adb")
    if not adb_path:
        print("⚠️  adb не найден в PATH. Добавь '%LOCALAPPDATA%\\Android\\Sdk\\platform-tools' в PATH.")
    else:
        print(f"✅ adb найден: {adb_path}")
    print("—" * 60)


# ============================================================================
# НАСТРОЙКА ДЛЯ ФИЗИЧЕСКОГО УСТРОЙСТВА SAMSUNG A50
# ============================================================================

CAPS = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    # ВАЖНО: udid отдельно, deviceName — человеко-читаемое имя
    "appium:udid": "ca68f122",
    "appium:deviceName": "14",

    "appium:appPackage": "net.metaquotes.metatrader4",
    "appium:appActivity": "net.metaquotes.metatrader4.ui.MainActivity",
    "appium:appWaitActivity": "*",

    "appium:noReset": True,
    "appium:newCommandTimeout": 300,
    "appium:autoGrantPermissions": True
}

print("🚀 Запуск автоматизации для физического устройства Samsung A50")
print("📱 UDID:", CAPS["appium:udid"])
print("📦 App Package:", CAPS["appium:appPackage"])
print("🔍 Проверьте правильность настроек выше!")
preflight_checks()

# ============================================================================
# ИНИЦИАЛИЗАЦИЯ И ПРОВЕРКА ПОДКЛЮЧЕНИЯ
# ============================================================================

try:
    print("🔌 Подключение к Appium Server...")
    # Appium 2: базовый путь — "/", НЕ /wd/hub
    options = UiAutomator2Options().load_capabilities(CAPS)
    driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=options)

    wait = WebDriverWait(driver, WAIT_TIMEOUT, poll_frequency=POLL_FREQUENCY)
    print("✅ Успешно подключились к устройству!")

except WebDriverException as e:
    print(f"❌ Ошибка подключения к Appium Server: {str(e)}")
    print("💡 Убедитесь, что:")
    print("   - Appium Server запущен на порту 4723 (без /wd/hub)")
    print("   - Устройство подключено и доступно через `adb devices` (статус device)")
    print("   - ANDROID_SDK_ROOT/ANDROID_HOME заданы, а adb есть в PATH")
    raise

# ============================================================================
# ОЖИДАНИЕ ЗАГРУЗКИ ПРИЛОЖЕНИЯ
# ============================================================================

print("⏳ Ожидаем загрузки приложения MetaTrader 4...")
time.sleep(5)

# ============================================================================
# ОБРАБОТКА ДИАЛОГОВ ПРИЛОЖЕНИЯ
# ============================================================================

accept_button_id = "net.metaquotes.metatrader4:id/accept_button"
max_accept_attempts = 3

for attempt in range(max_accept_attempts):
    if safe_click_element(driver, wait, AppiumBy.ID, accept_button_id, f"Кнопка accept (попытка {attempt + 1})"):
        print(f"✅ Приняли условия (попытка {attempt + 1})")
        time.sleep(2)
    else:
        print(f"ℹ️ Кнопка accept не найдена (попытка {attempt + 1}) - продолжаем")
        break

# ============================================================================
# НАВИГАЦИЯ ПО ПРИЛОЖЕНИЮ
# ============================================================================

#if not safe_click_element(driver, wait, AppiumBy.ID, "net.metaquotes.metatrader4:id/actionbar_app_icon", "Иконка приложения в action bar"):
#    print("⚠️ Не удалось найти иконку приложения - продолжаем...")

#if not safe_click_element(driver, wait, AppiumBy.ID, "net.metaquotes.metatrader4:id/account_mark", "Метка аккаунта"):
#    print("⚠️ Не удалось найти метку аккаунта - продолжаем...")

#xpath_image = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.ImageView"

#if not safe_click_element(driver, wait, AppiumBy.XPATH, xpath_image, "Изображение в меню"):
#    print("⚠️ Не удалось найти изображение в меню - продолжаем...")
#    print("💡 Проверьте XPath через Appium Inspector для вашего устройства")

#xpath_text = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.TextView[1]"

#if not safe_click_element(driver, wait, AppiumBy.XPATH, xpath_text, "Первый текстовый элемент"):
#    print("⚠️ Не удалось найти текстовый элемент - продолжаем...")
#    print("💡 Проверьте XPath через Appium Inspector для вашего устройства")

# ============================================================================
# ПОИСК И ФИЛЬТРАЦИЯ БРОКЕРОВ
# ============================================================================

try:
    print("🔍 Ищем поле фильтра...")
    filter_element = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "net.metaquotes.metatrader4:id/filter")))
    print("✅ Поле фильтра найдено")
    filter_element.click()
    print("✅ Кликнули по полю фильтра")

    search_combinations = load_keywords_from_csv(KEYWORDS_CSV_FILE)
    if not search_combinations:
        print("❌ Не удалось загрузить ключевые слова из файла. Завершение работы.")
        driver.quit()
        exit()
    
    print(f"🚀 Начинаем поиск с {len(search_combinations)} ключевыми словами из файла...")

    successful_searches = 0
    failed_searches = 0

    for idx, combination in enumerate(search_combinations, 1):
        try:
            print(f"\n📝 Поиск {idx}/{len(search_combinations)}: '{combination}'")
            if safe_send_keys(driver, wait, AppiumBy.ID, "net.metaquotes.metatrader4:id/filter", combination, f"Ввод '{combination}'"):
                successful_searches += 1
                print(f"✅ Успешно ввели '{combination}'")
                time.sleep(SEARCH_DELAY)
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