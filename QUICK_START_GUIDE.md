# 🚀 Пошаговый гайд запуска MetaProxy-Trader

Этот гайд поможет вам запустить проект MetaProxy-Trader для автоматического извлечения списка брокеров MetaTrader 4.

## 📋 Предварительные требования

### Системные требования:
- **ОС**: Windows 10+, macOS 10.14+, или Ubuntu 18.04+
- **Python**: 3.7 или выше
- **Node.js**: 14.0 или выше (для Appium)
- **Java**: JDK 8 или выше (для Android SDK)
- **RAM**: Минимум 8GB (рекомендуется 16GB)
- **Свободное место**: 5GB+

### Проверка версий:
```bash
python --version     # Должен быть 3.7+
node --version       # Должен быть 14.0+
java -version        # Должен быть JDK 8+
```

---

## 📦 ШАГ 1: Подготовка проекта

### 1.1 Клонирование и настройка окружения:
```bash
# Клонируйте репозиторий (или перейдите в папку проекта)
cd /path/to/MetaProxy-Trader

# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# На macOS/Linux:
source venv/bin/activate
# На Windows:
# venv\Scripts\activate
```

### 1.2 Установка Python зависимостей:
```bash
# Установите все зависимости
pip install -r requirements.txt

# Проверьте успешность установки
pip list | grep -E "(appium|selenium|mitmproxy)"
```

**Ожидаемый результат:**
```
appium-python-client   4.1.0
selenium              4.15.2
mitmproxy             10.1.5
```

---

## 📱 ШАГ 2: Настройка Android эмулятора

### 2.1 Установка Genymotion:
1. Скачайте Genymotion Desktop с [официального сайта](https://www.genymotion.com/download/)
2. Установите и зарегистрируйтесь
3. Установите VirtualBox (если требуется)

### 2.2 Создание виртуального устройства:
1. Откройте Genymotion Desktop
2. Нажмите "+" для создания нового устройства
3. Выберите Android 8.0+ (API 26+)
4. Рекомендуемые параметры:
   - **Устройство**: Google Pixel 3
   - **Android версия**: 9.0 (API 28)
   - **RAM**: 4GB
   - **Хранилище**: 32GB

### 2.3 Настройка прокси в эмуляторе:
1. Запустите созданное устройство
2. Зайдите в Settings → Wi-Fi
3. Длинный тап на подключенную сеть → Modify Network
4. Advanced Options → Manual Proxy
5. Настройте прокси:
   ```
   Proxy hostname: [IP_ВАШЕГО_КОМПЬЮТЕРА]
   Proxy port: 8080
   ```
6. Сохраните настройки

### 2.4 Установка MetaTrader 4:
1. Скачайте MetaTrader 4 APK
2. Перетащите APK файл в эмулятор для установки
3. Или установите через Google Play Store в эмуляторе

### 2.5 Получение Device Name:
```bash
# Запустите эмулятор и выполните команду:
adb devices

# Результат будет примерно таким:
# List of devices attached
# 192.168.56.101:5555    device
```

---

## 🔧 ШАГ 3: Установка и настройка Appium

### 3.1 Установка Appium:
```bash
# Установите Appium глобально
npm install -g appium

# Проверьте установку
appium --version
```

### 3.2 Установка драйвера для Android:
```bash
# Установите UiAutomator2 драйвер
appium driver install uiautomator2

# Проверьте установленные драйверы
appium driver list --installed
```

### 3.3 Настройка файла Automation_MT4.py:
Откройте файл `Automation_MT4.py` и настройте параметры:

```python
desired_cap = {
    "platformName": "Android",
    "appium:appPackage": "net.metaquotes.metatrader4",
    "appium:appActivity": "net.metaquotes.metatrader4.ui.MainActivity",
    "appium:app": "/ПОЛНЫЙ/ПУТЬ/К/MetaTrader4.apk",  # ← ИЗМЕНИТЬ
    "appium:deviceName": "192.168.56.101:5555"        # ← ИЗМЕНИТЬ на ваш device
}

# Опционально: настройте параметры поиска
SEARCH_COMBINATIONS_COUNT = 50  # Уменьшите для тестирования
SEARCH_DELAY = 3               # Увеличьте для медленных устройств
CLEAR_DELAY = 2
```

---

## 🕵️ ШАГ 4: Настройка MITM Proxy

### 4.1 Проверка настройки Global_JSON_Response_Extractor.py:
Файл уже настроен, но вы можете изменить параметры:

```python
CONFIG = {
    "output_directory": "MetaTrader_Brokers_Data",
    "url_filter": "updates.metaquotes.net/public/mt5/network/mobile",
    "save_duplicates": False,    # True - если хотите сохранять дубликаты
    "add_timestamp": True,       # False - для простых имен файлов
    "detailed_logging": True     # False - для минимальных логов
}
```

### 4.2 Установка сертификата в эмулятор:
1. Запустите mitmproxy:
   ```bash
   mitmproxy -s Global_JSON_Response_Extractor.py
   ```

2. В эмуляторе откройте браузер и перейдите на: `http://mitm.it`

3. Скачайте сертификат для Android

4. Установите сертификат:
   - Settings → Security → Install from storage
   - Выберите скачанный сертификат
   - Назовите его "mitmproxy"

---

## 🚀 ШАГ 5: Запуск проекта

### 5.1 Подготовка терминалов:
Вам понадобится **3 открытых терминала**:

**Терминал 1 - MITM Proxy:**
```bash
cd /path/to/MetaProxy-Trader
source venv/bin/activate  # Активируйте виртуальное окружение
mitmproxy -s Global_JSON_Response_Extractor.py
```

**Терминал 2 - Appium Server:**
```bash
cd /path/to/MetaProxy-Trader
appium --port 4723
```

**Терминал 3 - Автоматизация:**
```bash
cd /path/to/MetaProxy-Trader
source venv/bin/activate
# Пока не запускайте - дождитесь готовности других компонентов
```

### 5.2 Последовательность запуска:

**1. Запустите эмулятор Genymotion** ✅
   - Убедитесь, что устройство полностью загружено
   - Проверьте, что прокси настроен правильно

**2. Запустите MITM Proxy** (Терминал 1) ✅
   ```bash
   mitmproxy -s Global_JSON_Response_Extractor.py
   ```
   
   **Ожидаемый вывод:**
   ```
   🚀 Инициализация Global_JSON_Response_Extractor
   📁 Директория сохранения: /path/to/MetaTrader_Brokers_Data
   🎯 Фильтр URL: updates.metaquotes.net/public/mt5/network/mobile
   🔄 Дубликаты: блокированы
   Proxy server listening at http://*:8080
   ```

**3. Запустите Appium Server** (Терминал 2) ✅
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

**4. Запустите автоматизацию** (Терминал 3) ✅
   ```bash
   python Automation_MT4.py
   ```

---

## 📊 ШАГ 6: Мониторинг выполнения

### 6.1 Что вы должны увидеть:

**В терминале автоматизации:**
```
Начинаем поиск с 100 уникальными комбинациями...
Поиск 1/100: 'a1z'
Поиск 2/100: '9x3'
Поиск 3/100: 'k7m'
...
```

**В терминале MITM Proxy:**
```
✅ Сохранен ответ #1: response_1_20240804_164523.json (2,435 байт)
📁 Путь: /path/to/MetaTrader_Brokers_Data/response_1_20240804_164523.json
🏢 Найдено брокеров: 15
✅ Сохранен ответ #2: response_2_20240804_164545.json (1,892 байт)
🔄 Пропускаем дубликат ответа (hash: a1b2c3d4...)
```

**В эмуляторе:**
- Приложение MetaTrader 4 должно открыться
- Должен происходить автоматический ввод поисковых запросов
- Экран должен обновляться с результатами поиска

### 6.2 Проверка результатов:
```bash
# Проверьте созданную папку с данными
ls -la MetaTrader_Brokers_Data/

# Посмотрите содержимое одного из файлов
cat MetaTrader_Brokers_Data/response_1_*.json | head -20
```

---

## 🛠️ ШАГ 7: Устранение проблем

### 7.1 Частые проблемы и решения:

**❌ Ошибка подключения к Appium:**
```
selenium.common.exceptions.WebDriverException: Message: 
An unknown server-side error occurred while processing the command.
```
**Решение:**
- Убедитесь, что Appium Server запущен на порту 4723
- Проверьте, что device name правильный (`adb devices`)
- Перезапустите эмулятор и Appium

**❌ MITM Proxy не перехватывает трафик:**
```
# Нет логов о сохранении JSON файлов
```
**Решение:**
- Проверьте настройки прокси в эмуляторе (IP:8080)
- Убедитесь, что сертификат установлен правильно
- Перезапустите эмулятор после установки сертификата

**❌ Элементы не найдены в приложении:**
```
selenium.common.exceptions.NoSuchElementException
```
**Решение:**
- Обновите MetaTrader 4 до последней версии
- Возможно изменился интерфейс - нужно обновить селекторы
- Увеличьте задержки в коде (`time.sleep()`)

**❌ Приложение не открывается:**
```
Activity not found or app not installed
```
**Решение:**
- Проверьте правильность пути к APK файлу
- Убедитесь, что APK установлен в эмуляторе
- Попробуйте запустить приложение вручную сначала

### 7.2 Команды для диагностики:
```bash
# Проверка подключенных устройств
adb devices

# Проверка установленных пакетов
adb shell pm list packages | grep metaquotes

# Проверка сетевых подключений
netstat -an | grep 4723
netstat -an | grep 8080

# Проверка логов эмулятора
adb logcat | grep -i metatrader
```

---

## 🎯 ШАГ 8: Финализация

### 8.1 После успешного выполнения:

1. **Остановите все процессы** в правильном порядке:
   - Сначала остановите `Automation_MT4.py` (Ctrl+C)
   - Затем остановите Appium Server (Ctrl+C)
   - Наконец остановите MITM Proxy (Ctrl+C)

2. **Проверьте результаты:**
   ```bash
   # Количество файлов
   ls MetaTrader_Brokers_Data/ | wc -l
   
   # Общий размер данных
   du -sh MetaTrader_Brokers_Data/
   
   # Пример данных
   head -10 MetaTrader_Brokers_Data/response_1_*.json
   ```

3. **Деактивируйте виртуальное окружение:**
   ```bash
   deactivate
   ```

### 8.2 Следующие шаги:
- Анализируйте собранные JSON файлы
- Создайте скрипты для обработки данных
- Настройте регулярное выполнение сбора данных

---

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте [README.md](README.md) для дополнительной информации
2. Просмотрите логи всех компонентов
3. Убедитесь, что все зависимости установлены корректно
4. Создайте issue в репозитории с детальным описанием проблемы

**Удачного сбора данных! 🚀**