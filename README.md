# MetaProxy-Trader

**Автоматизация сбора данных брокеров MetaTrader 4 через Android устройство и MITM прокси**

## 🎯 Описание проекта

MetaProxy-Trader - это система автоматизации для сбора данных о брокерах MetaTrader 4. Проект использует Android устройство (физическое или эмулятор) для автоматизации взаимодействия с приложением MetaTrader 4, а MITM (Man-in-the-Middle) прокси для перехвата и сохранения сетевого трафика в формате JSON.


## 🔧 Принцип работы

### 1. Основной скрипт автоматизации (Automation_MT4.py)

**Назначение:** Автоматизация взаимодействия с приложением MetaTrader 4 на Android устройстве.

**Принцип работы:**
1. **Инициализация:** Подключение к Android устройству через Appium сервер
2. **Загрузка ключевых слов:** Чтение уникального ключевого слова из файла `keywords.csv`
3. **Навигация:** Открытие приложения MetaTrader 4 и переход к полю поиска
4. **Автоматический поиск:** Для каждого ключевого слова:
   - Ввод в поле поиска
   - Ожидание результатов (2 секунды)
   - Очистка поля
   - Переход к следующему ключевому слову
5. **Обработка ошибок:** Безопасные функции взаимодействия с UI элементами
6. **Логирование:** Подробные логи процесса выполнения

**Ключевые функции:**
```python
# Безопасные функции взаимодействия
def safe_click_element(driver, wait, locator, locator_value, action_description)
def safe_send_keys(driver, wait, locator, locator_value, text, action_description)
def safe_clear_field(driver, wait, locator, locator_value, action_description)

# Загрузка ключевых слов
def load_keywords_from_csv(csv_file_path)
```

### 2. MITM прокси (mt_json_sniffer.py)

**Назначение:** Перехват и сохранение JSON ответов от серверов MetaTrader.

**Принцип работы:**
1. **Фильтрация трафика:** Перехват только HTTP/HTTPS запросов к серверам MetaQuotes
2. **Анализ ответов:** Проверка, является ли ответ JSON-данными
3. **Дедупликация:** Избежание сохранения одинаковых ответов через MD5 хэши
4. **Сохранение:** Запись JSON данных в файлы с временными метками
5. **Логирование:** Запись всех URL и статистики в лог-файл

**Конфигурация:**
```python
CONFIG = {
    "out_dir": "Captured_JSON",           # Папка для результатов
    "host_substrings": ["metaquotes", "mt5", "mt4"],  # Фильтр хостов
    "write_urls_log": True,               # Логировать URL
    "save_duplicates": False,             # Сохранять дубликаты
}
```

### 3. Ключевые слова (keywords.csv)

**Назначение:** Список из 331 уникального ключевого слова для поиска брокеров.

**Формат:** Каждая строка содержит одно 3-символьное ключевое слово
```csv
0cm
0ex
0fx
0tr
1cm
1ex
# ... 331 строка
```

**Принцип генерации:** Комбинации букв (a-z) и цифр (0-9) длиной 3 символа

### 4. Конвертер JSON в CSV (json_to_csv_converter.py)

**Назначение:** Преобразование собранных JSON данных в CSV формат для импорта в Google Sheets.

**Принцип работы:**
1. **Загрузка JSON файлов:** Чтение всех JSON файлов из папки `Captured_JSON/`
2. **Извлечение данных:** Рекурсивный поиск информации о брокерах в JSON структуре
3. **Дедупликация:** Удаление дублирующихся записей по имени и серверу
4. **Создание CSV:** Формирование таблицы с данными о брокерах
5. **Экспорт:** Сохранение в CSV файл с временной меткой

**Ключевые функции:**
```python
def load_json_files(json_dir)           # Загрузка JSON файлов
def extract_broker_data(json_data)      # Извлечение данных о брокерах
def create_csv_output(brokers, output_file)  # Создание CSV файла
```

**Структура данных:**
- name - Название брокера
- server - Сервер брокера
- description - Описание брокера
- type - Тип брокера
- country - Страна брокера
- url - Веб-сайт брокера
- path - Путь в JSON структуре

## 🛠️ Системные требования

### Обязательные требования:
- **Python 3.7+**
- **Node.js 14.0+**
- **Android SDK** (для ADB)
- **Физическое Android устройство** или эмулятор
- **MetaTrader 4** установлен на устройстве

### Рекомендуемые требования:
- **macOS 10.15+** / **Windows 10+** / **Ubuntu 18.04+**
- **8 GB RAM**
- **2 GB свободного места**
- **USB подключение** для физического устройства

## 📋 Пошаговая установка

### Шаг 1: Подготовка системы (5 минут)

#### 1.1 Установка Python
```bash
# Проверьте версию Python
python --version
# Должно быть 3.7 или выше

# Если Python не установлен:
# macOS: brew install python3
# Ubuntu: sudo apt install python3 python3-pip
# Windows: скачайте с python.org
```

#### 1.2 Установка Node.js
```bash
# Проверьте версию Node.js
node --version
# Должно быть 14.0 или выше

# Если Node.js не установлен:
# macOS: brew install node
# Ubuntu: curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
# Windows: скачайте с nodejs.org
```

#### 1.3 Установка Android SDK
```bash
# macOS
brew install android-sdk

# Ubuntu
sudo apt install android-sdk

# Windows
# Скачайте Android Studio и установите SDK
```

### Шаг 2: Клонирование проекта (2 минуты)

```bash
# Клонируйте репозиторий
git clone https://github.com/your-repo/MetaProxy-Trader.git
cd MetaProxy-Trader

# Или скачайте ZIP и распакуйте
```

### Шаг 3: Настройка виртуального окружения (3 минуты)

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Шаг 4: Установка зависимостей (5 минут)

```bash
# Обновите pip
pip install --upgrade pip

# Установите зависимости
pip install -r requirements.txt
```

### Шаг 5: Установка Appium (3 минуты)

```bash
# Установите Appium глобально
npm install -g appium

# Установите драйвер для Android
appium driver install uiautomator2

# Проверьте установку
appium --version
```

### Шаг 6: Настройка Android SDK (2 минуты)

```bash
# Добавьте Android SDK в PATH
# macOS/Linux:
export ANDROID_SDK_ROOT=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools

# Windows:
# Добавьте в переменные среды:
# ANDROID_SDK_ROOT=C:\Users\YourUser\AppData\Local\Android\Sdk
# PATH=%PATH%;%ANDROID_SDK_ROOT%\platform-tools

# Проверьте ADB
adb version
```

## 📱 Настройка Android устройства

### Вариант A: Физическое устройство

#### 1. Включение режима разработчика
1. Откройте **Settings** → **About phone**
2. Нажмите **Build number** 7 раз
3. Вернитесь в **Settings** → **Developer options**
4. Включите **USB debugging**

#### 2. Подключение устройства
```bash
# Подключите устройство через USB
adb devices

# Ожидаемый вывод:
# List of devices attached
# [SERIAL_NUMBER]    device
```

#### 3. Установка MetaTrader 4
```bash
# Скачайте APK с официального сайта MetaQuotes
# Или установите через Google Play Store

# Проверьте установку
adb shell pm list packages | grep metaquotes
```

### Вариант B: Эмулятор

#### 1. Установка Android Studio
```bash
# Скачайте Android Studio с developer.android.com
# Установите и настройте эмулятор
```

#### 2. Создание эмулятора
1. Откройте **AVD Manager**
2. Создайте новый виртуальный девайс
3. Рекомендуемые настройки:
   - API Level: 30 (Android 11)
   - RAM: 2 GB
   - Internal Storage: 4 GB

#### 3. Запуск эмулятора
```bash
# Запустите эмулятор
emulator -avd [AVD_NAME]

# Проверьте подключение
adb devices
```

## ⚙️ Конфигурация проекта

### Шаг 1: Настройка Automation_MT4.py

Откройте файл `Automation_MT4.py` и настройте параметры:

```python
# Настройки для физического устройства
CAPS = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:udid": "ca68f122",  # ← ИЗМЕНИТЬ на ваш UDID
    "appium:deviceName": "14",   # ← ИЗМЕНИТЬ на имя вашего устройства
    "appium:appPackage": "net.metaquotes.metatrader4",
    "appium:appActivity": "net.metaquotes.metatrader4.ui.MainActivity",
    "appium:noReset": True,
    "appium:newCommandTimeout": 300,
    "appium:autoGrantPermissions": True
}

# Настройки поиска
SEARCH_DELAY = 2    # Задержка после поиска (секунды)
CLEAR_DELAY = 1     # Задержка после очистки (секунды)
WAIT_TIMEOUT = 30   # Таймаут ожидания элементов (секунды)
```

#### Получение UDID устройства:
```bash
# Для физического устройства
adb devices

# Для эмулятора
adb -s emulator-5554 shell getprop ro.serialno
```

### Шаг 2: Настройка keywords.csv

Файл `keywords.csv` содержит ключевые слова для поиска. Каждая строка - одно ключевое слово:

```csv
0cm
0ex
0fx
0tr
1cm
1ex
# ... и так далее
```

Вы можете:
- Добавить свои ключевые слова
- Изменить существующие
- Увеличить/уменьшить количество

### Шаг 3: Настройка MITM прокси

Откройте файл `mt_json_sniffer.py` и настройте параметры:

```python
CONFIG = {
    "out_dir": "Captured_JSON",           # Папка для результатов
    "host_substrings": ["metaquotes", "mt5", "mt4"],  # Фильтр хостов
    "write_urls_log": True,               # Логировать URL
    "save_duplicates": False,             # Сохранять дубликаты
}
```

## 🚀 Запуск проекта

### Шаг 1: Подготовка терминалов

Вам понадобится **3 открытых терминала**:

**Терминал 1** - MITM прокси:
```bash
cd /path/to/MetaProxy-Trader
source venv/bin/activate  # Активируйте виртуальное окружение
```

**Терминал 2** - Appium сервер:
```bash
cd /path/to/MetaProxy-Trader
```

**Терминал 3** - Автоматизация:
```bash
cd /path/to/MetaProxy-Trader
source venv/bin/activate  # Активируйте виртуальное окружение
```

### Шаг 2: Последовательность запуска

#### 1. Запустите MITM прокси (Терминал 1)
```bash
mitmproxy -s mt_json_sniffer.py
```

**Ожидаемый вывод:**
```
🚀 JSON sniffer запущен. Папка: /path/to/Captured_JSON
Proxy server listening at http://*:8080
```

#### 2. Запустите Appium сервер (Терминал 2)
```bash
appium --port 4723
```

**Ожидаемый вывод:**
```
[Appium] Welcome to Appium v2.x.x
[Appium] Non-default server args:
[Appium] { port: 4723 }
[Appium] Attempting to load driver uiautomator2...
[Appium] Appium REST http interface listener started on 0.0.0.0:4723
```

#### 3. Запустите автоматизацию (Терминал 3)
```bash
python Automation_MT4.py
```

**Ожидаемый вывод:**
```
🚀 Запуск автоматизации для физического устройства Samsung A50
📱 UDID: ca68f122
📦 App Package: net.metaquotes.metatrader4
🔍 Проверьте правильность настроек выше!
🔌 Подключение к Appium Server...
✅ Успешно подключились к устройству!
```

### Шаг 3: Настройка прокси на устройстве

#### Для физического устройства:
1. Откройте **Settings** → **Connections** → **Wi-Fi**
2. Нажмите долго на подключенную сеть
3. Выберите **Modify Network**
4. Включите **Advanced Options**
5. Настройте **Manual Proxy**:
   - **Hostname:** `192.168.1.XXX` (IP вашего компьютера)
   - **Port:** `8080`

#### Для эмулятора:
```bash
# Установите прокси через ADB
adb shell settings put global http_proxy 192.168.1.XXX:8080

# Проверьте настройки
adb shell settings get global http_proxy
```

### Шаг 4: Установка сертификата MITM

1. Откройте браузер на устройстве
2. Перейдите на `http://mitm.it`
3. Выберите **Android** и скачайте сертификат
4. Установите сертификат:
   - **Settings** → **Security** → **Install from storage**
   - Найдите скачанный файл и установите

## 📊 Мониторинг выполнения

### Логи автоматизации:
```
🔍 Ожидаем элемент для: Кнопка accept (попытка 1)
✅ Кликаем: Кнопка accept (попытка 1)
✅ Приняли условия (попытка 1)

🔍 Ищем поле фильтра...
✅ Поле фильтра найдено
✅ Кликнули по полю фильтра

🚀 Начинаем поиск с 331 ключевыми словами из файла...

📝 Поиск 1/331: '0cm'
🔍 Ожидаем поле ввода для: Ввод '0cm'
📝 Вводим текст: '0cm' - Ввод '0cm'
✅ Успешно ввели '0cm'
🧹 Очищаем поле: Очистка после '0cm'
✅ Успешно очистили поле после '0cm'
```

### Логи MITM прокси:
```
2024-01-15 10:30:15 200 application/json GET https://updates.metaquotes.net/public/mt5/network/mobile
✅ JSON сохранён: resp_0001_20240115_103015_updates.metaquotes.net_public_mt5_network_mobile.json (2435 байт)
```

### Созданные файлы:
```
Captured_JSON/
├── resp_0001_20240115_103015_updates.metaquotes.net_public_mt5_network_mobile.json
├── resp_0002_20240115_103020_updates.metaquotes.net_public_mt5_network_mobile.json
├── resp_0003_20240115_103025_updates.metaquotes.net_public_mt5_network_mobile.json
└── urls.log
```

## 📊 Обработка результатов

### Конвертация JSON в CSV

После завершения автоматизации и сбора JSON файлов, необходимо конвертировать данные в CSV формат для удобного анализа в Google Sheets:

```bash
# Запустите конвертер JSON в CSV
python json_to_csv_converter.py
```

**Ожидаемый вывод:**
```
🔄 Конвертер JSON в CSV для MetaProxy-Trader
==================================================
📁 Загружаем JSON файлы из Captured_JSON...
✅ Загружен файл: resp_0001_20240115_103015_*.json
✅ Загружен файл: resp_0002_20240115_103020_*.json
✅ Загружен файл: resp_0003_20240115_103025_*.json
✅ Загружено 3 JSON файлов
🔍 Извлекаем данные о брокерах...
📊 Извлечено 15 брокеров из resp_0001_20240115_103015_*.json
📊 Извлечено 12 брокеров из resp_0002_20240115_103020_*.json
📊 Извлечено 8 брокеров из resp_0003_20240115_103025_*.json
🔄 Удалено 5 дубликатов
💾 Создаем CSV файл: brokers_data_20240115_103045.csv
✅ CSV файл создан: brokers_data_20240115_103045.csv
📊 Сохранено 30 записей о брокерах

🎉 Конвертация завершена успешно!
📄 Файл готов для импорта в Google Sheets: brokers_data_20240115_103045.csv

📋 Инструкция по импорту в Google Sheets:
1. Откройте Google Sheets
2. File → Import
3. Upload → выберите файл brokers_data_20240115_103045.csv
4. Import location: Create new spreadsheet
5. Separator type: Comma
6. Нажмите Import data
```

### Структура CSV файла

Созданный CSV файл содержит следующие колонки:
- **name** - Название брокера
- **server** - Сервер брокера
- **description** - Описание брокера
- **type** - Тип брокера
- **country** - Страна брокера
- **url** - Веб-сайт брокера
- **path** - Путь в JSON структуре

### Преимущества CSV формата

✅ **Удобный анализ** - данные структурированы в табличном формате  
✅ **Импорт в Google Sheets** - готов для работы в облачных таблицах  
✅ **Фильтрация и сортировка** - легко найти нужных брокеров  
✅ **Удаление дубликатов** - автоматическое исключение повторяющихся записей  
✅ **Временные метки** - каждый файл имеет уникальное имя с датой и временем

## 🛠️ Устранение проблем

### Проблема 1: Ошибка подключения к Appium
```
❌ Ошибка подключения к Appium Server
```

**Решение:**
1. Убедитесь, что Appium сервер запущен
2. Проверьте порт 4723
3. Проверьте подключение устройства: `adb devices`

### Проблема 2: Элементы не находятся
```
❌ Таймаут ожидания элемента: Кнопка accept
```

**Решение:**
1. Увеличьте `WAIT_TIMEOUT` в скрипте
2. Проверьте через Appium Inspector
3. Убедитесь, что приложение загрузилось

### Проблема 3: MITM прокси не перехватывает трафик
```
# Нет логов о сохранении JSON файлов
```

**Решение:**
1. Проверьте настройки прокси на устройстве
2. Убедитесь, что сертификат установлен
3. Перезапустите устройство

### Проблема 4: Приложение не открывается
```
Activity not found or app not installed
```

**Решение:**
```bash
# Проверьте установленные пакеты
adb shell pm list packages | grep metaquotes

# Переустановите приложение
adb uninstall net.metaquotes.metatrader4
adb install MetaTrader4.apk
```

## 🔧 Дополнительные инструменты

### Appium Inspector
```bash
# Установите Appium Inspector
npm install -g appium-inspector

# Запустите Inspector
appium-inspector
```

### Диагностические команды
```bash
# Проверка системы
python --version
node --version
adb version
appium --version

# Проверка зависимостей
pip list | grep -E "(appium|selenium|mitmproxy)"

# Проверка устройства
adb devices
adb shell getprop ro.product.model
```

## 📝 Конфигурация для разных устройств

### Samsung A50 (текущая конфигурация)
```python
CAPS = {
    "appium:udid": "ca68f122",
    "appium:deviceName": "14",
    "appium:appPackage": "net.metaquotes.metatrader4",
}
```

### Другие устройства
```python
# Для эмулятора
CAPS = {
    "appium:udid": "emulator-5554",
    "appium:deviceName": "Android Emulator",
}

# Для другого физического устройства
CAPS = {
    "appium:udid": "YOUR_DEVICE_UDID",
    "appium:deviceName": "YOUR_DEVICE_NAME",
}
```

## 🎯 Оптимизация производительности

### Настройки для быстрого поиска:
```python
SEARCH_DELAY = 1      # Уменьшите задержку
CLEAR_DELAY = 0.5     # Уменьшите задержку
WAIT_TIMEOUT = 15     # Уменьшите таймаут
```

### Настройки для стабильности:
```python
SEARCH_DELAY = 3      # Увеличьте задержку
CLEAR_DELAY = 2       # Увеличьте задержку
WAIT_TIMEOUT = 60     # Увеличьте таймаут
```

## 📚 Полезные ссылки

- [Appium Documentation](http://appium.io/docs/en/about-appium/intro/)
- [Android Developer Tools](https://developer.android.com/studio)
- [MetaTrader 4](https://www.metatrader4.com/)
- [MITM Proxy](https://mitmproxy.org/)

## 🎯 Заключение

После выполнения всех шагов у вас будет:

1. ✅ Установленная система автоматизации
2. ✅ Настроенное Android устройство
3. ✅ Работающий MITM прокси
4. ✅ Автоматический сбор данных брокеров
5. ✅ Конвертация JSON в CSV для анализа в Google Sheets

### 📋 Полный рабочий процесс:

1. **Установка и настройка** (20 минут)
2. **Запуск автоматизации** (время зависит от количества ключевых слов)
3. **Сбор JSON данных** (автоматически в папке `Captured_JSON/`)
4. **Конвертация в CSV** (`python json_to_csv_converter.py`)
5. **Импорт в Google Sheets** для анализа и работы с данными


