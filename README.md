# MetaProxy-Trader
Extracting MetaTrader Platform Broker List using Android Emulator and MITM Proxy

The scripting process is employed for automation, encompassing tasks such
as navigating and searching for all broker names within the Genymotion environment. The main objective is to extract a comprehensive list of brokers
along with their corresponding information. To achieve this, MITM (Man-in-the-Middle) techniques are employed. Specifically, a proxy certificate is installed
in the Genymotion environment. As the Appium automation script is executed,
the MITM proxy captures network traffic. Subsequently, the captured traffic
leads to the local storage of specific responses in the form of JSON files.

The overall system architecture of our project is depicted below in Figure. It consists
of several key components.

![System Architecture](https://github.com/3rtha/MetaProxy-Trader/assets/126825143/f88cb935-f5e2-407e-b2b7-82aa8835c853)

## 📚 Документация

**Для быстрого старта:**
- 🚀 **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Подробная пошаговая инструкция
- ✅ **[CHECKLIST.md](CHECKLIST.md)** - Быстрый чеклист для запуска
- 📱 **[AVD_SETUP_GUIDE.md](AVD_SETUP_GUIDE.md)** - Адаптация для Android Studio AVD

Follow the below steps to get started:
1. Set Up Genymotion Android Emulator: Download and install GenyMotion from their official website. Create a virtual device in Genymotion
with the desired Android version and specifications. Install the MetaTrader app on the virtual device using either the Google Play Store or an
APK file.

2. Configure MITM Proxy Settings: Install and configure MITM
Proxy on your local machine. Download the MITM CA certificate and
adjust the proxy settings on the Genymotion emulator. Ensure that the
virtual Android emulator’s IP address and port match your computer’s
IP address and port.

```
 mitmproxy -s Global_JSON_Response_Extractor.py
```
4. Initiate Appium Server: Install Appium on your machine using
npm or another method. Start the Appium server using the appium command in a terminal.

5. Use Appium Inspector to Begin Session: Open Appium Inspector, a tool that comes with Appium, in your web browser. Configure the
desired capabilities for your test session. This includes specifying the device, app package, app activity, etc. Start a session using the capabilities
you’ve configured.

Use the below Desired Capabilities and start the session:
```
For MT4 "platformName":
"Android", "appium:appPackage": "net.metaquotes.metatrader4",
"appium:appActivity": "net.metaquotes.metatrader4.ui.MainActivity",
"appium:app": "C:/Users/Downloads/MetaTrader4.apk"
```
6. Execute Automation Scripts: The automation script now uses an improved search algorithm that generates random combinations of letters and numbers (3 characters each). Run the automation script:
```bash
python Automation_MT4.py
```

### Новые возможности автоматизации:
- **Случайная генерация поиска**: Скрипт теперь генерирует 100 уникальных комбинаций из букв (a-z) и цифр (0-9) длиной 3 символа каждая
- **Избежание повторений**: Алгоритм гарантирует уникальность каждой поисковой комбинации
- **Настраиваемые параметры**: В начале файла `Automation_MT4.py` можно настроить:
  - `SEARCH_COMBINATIONS_COUNT` - количество поисковых комбинаций (по умолчанию 100)
  - `SEARCH_DELAY` - задержка после ввода поиска (по умолчанию 2 секунды)
  - `CLEAR_DELAY` - задержка после очистки поля (по умолчанию 1 секунда)
- **Подробное логирование**: Скрипт выводит прогресс и ошибки в консоль

### Примеры поисковых комбинаций:
- a1z, 9x3, k7m, 2b8, q5f, etc.

7. Monitor and Analyze Results: Monitor the output and logs of
your automation scripts to ensure they are executing as expected. The script will display progress like "Поиск 1/100: 'a1z'" for each search combination. Inspect
the app's behavior in the Genymotion emulator as the automation scripts
run. Use MITM Proxy to capture and analyze network traffic for debugging and testing purposes.

## Contributing
We welcome contributions from the community. If you have ideas for improvement or find any issues, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Полная документация по запуску

### Системные требования:
- Python 3.7+
- Appium Server
- Genymotion Android Emulator
- mitmproxy
- MetaTrader 4 APK файл

### Шаг за шагом инструкция запуска:

#### 1. Подготовка окружения:

**Вариант 1: Быстрая установка через requirements.txt**
```bash
# Клонируйте репозиторий
git clone https://github.com/3rtha/MetaProxy-Trader.git
cd MetaProxy-Trader

# Создайте виртуальное окружение (рекомендуется)
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установите все зависимости из файла
pip install -r requirements.txt

# Установка Appium (требует Node.js)
npm install -g appium
```

**Вариант 2: Установка через setup.py**
```bash
# После клонирования репозитория
pip install -e .

# Установка Appium
npm install -g appium
```

**Вариант 3: Ручная установка основных зависимостей**
```bash
pip install appium-python-client==4.1.0 selenium==4.15.2 mitmproxy==10.1.5
npm install -g appium
```

#### 2. Настройка Android эмулятора:
1. Запустите Genymotion и создайте виртуальное устройство
2. Установите MetaTrader 4 APK на эмулятор
3. Настройте прокси в эмуляторе на IP вашего компьютера, порт 8080

#### 3. Настройка MITM Proxy:
```bash
# Директория создается автоматически в папке проекта как MetaTrader_Brokers_Data/

# Запуск MITM proxy с улучшенным обработчиком
mitmproxy -s Global_JSON_Response_Extractor.py
```

**Новые возможности Global_JSON_Response_Extractor.py:**
- ✅ **Кроссплатформенность**: Работает на Windows, macOS, Linux
- ✅ **Автосоздание директорий**: Не нужно создавать папки вручную
- ✅ **Фильтрация дубликатов**: Избегает сохранения одинаковых ответов
- ✅ **Временные метки**: Добавляет дату/время в имена файлов
- ✅ **Подробное логирование**: Показывает размер файлов и количество брокеров
- ✅ **Улучшенная обработка ошибок**: Лучшая диагностика проблем
- ✅ **Настраиваемость**: Легко изменять параметры в CONFIG

#### 4. Запуск Appium Server:
```bash
# В отдельном терминале запустите Appium
appium
```

#### 5. Настройка автоматизации:
В файле `Automation_MT4.py` убедитесь, что:
- Путь к APK файлу указан корректно (строка 40)
- IP адрес Appium сервера корректен (строка 44)
- deviceName соответствует вашему эмулятору (строка 41)

#### 6. Запуск автоматизации:
```bash
python Automation_MT4.py
```

### Конфигурация поиска:
Вы можете настроить параметры поиска в начале файла `Automation_MT4.py`:
```python
SEARCH_COMBINATIONS_COUNT = 100  # Количество поисковых комбинаций
SEARCH_DELAY = 2                 # Задержка после поиска (сек)
CLEAR_DELAY = 1                  # Задержка после очистки (сек)
```

### Мониторинг результатов:
**Логи автоматизации:**
- Прогресс поиска отображается в консоли: "Поиск 1/100: 'a1z'"
- Ошибки и статус выполнения каждого поиска

**Логи MITM Proxy:**
- ✅ Сохранен ответ #1: response_1_20240804_164523.json (2,435 байт)
- 📁 Путь: /path/to/MetaTrader_Brokers_Data/response_1_20240804_164523.json
- 🏢 Найдено брокеров: 15
- 🔄 Пропускаем дубликат ответа (hash: a1b2c3d4...)

**Сохранение данных:**
- JSON ответы сохраняются в `./MetaTrader_Brokers_Data/` (создается автоматически)
- Имена файлов: `response_1_20240804_164523.json` (с временными метками)
- Дубликаты автоматически фильтруются
- Сетевой трафик можно анализировать через веб-интерфейс mitmproxy (http://mitm.it)

### Возможные проблемы и решения:
1. **Ошибка подключения к Appium**: Убедитесь, что сервер запущен на порту 4723
2. **Прокси не перехватывает трафик**: Проверьте настройки прокси в эмуляторе
3. **Элементы не найдены**: Возможно изменился интерфейс приложения, обновите селекторы

## Acknowledgments
MetaTrader for providing valuable broker information.
Our open-source community for their support and contributions.


