# ✅ Чеклист быстрого запуска MetaProxy-Trader

## 🔧 Предварительная подготовка (один раз)

- [ ] Python 3.7+ установлен
- [ ] Node.js 14.0+ установлен
- [ ] Java JDK 8+ установлен
- [ ] Genymotion Desktop установлен
- [ ] Виртуальное Android устройство создано в Genymotion
- [ ] MetaTrader 4 APK установлен в эмулятор
- [ ] Прокси настроен в эмуляторе (IP:8080)
- [ ] MITM сертификат установлен в эмулятор

## 📦 Установка зависимостей (один раз)

```bash
# Создание окружения
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# Установка зависимостей
pip install -r requirements.txt
npm install -g appium
appium driver install uiautomator2
```

## ⚙️ Настройка конфигурации

- [ ] В `Automation_MT4.py` указан правильный путь к APK файлу
- [ ] В `Automation_MT4.py` указан правильный deviceName (`adb devices`)
- [ ] В `Global_JSON_Response_Extractor.py` настроены параметры CONFIG (опционально)

## 🚀 Последовательность запуска

### 1. Подготовка (каждый раз)
- [ ] Эмулятор Genymotion запущен и полностью загружен
- [ ] Виртуальное окружение активировано: `source venv/bin/activate`

### 2. Терминал 1 - MITM Proxy
```bash
mitmproxy -s Global_JSON_Response_Extractor.py
```
- [ ] Увидели сообщение: "🚀 Инициализация Global_JSON_Response_Extractor"
- [ ] Proxy server listening at http://*:8080

### 3. Терминал 2 - Appium Server  
```bash
appium --port 4723
```
- [ ] Увидели: "Appium REST http interface listener started on 0.0.0.0:4723"

### 4. Терминал 3 - Автоматизация
```bash
python Automation_MT4.py
```
- [ ] Приложение MT4 открылось в эмуляторе
- [ ] Началось выполнение поисковых запросов: "Поиск 1/100: 'a1z'"

## 📊 Проверка работы

### MITM Proxy логи:
- [ ] "✅ Сохранен ответ #1: response_1_YYYYMMDD_HHMMSS.json"
- [ ] "🏢 Найдено брокеров: X"
- [ ] Папка `MetaTrader_Brokers_Data/` создана автоматически

### Эмулятор:
- [ ] MetaTrader 4 приложение открыто
- [ ] Автоматически вводятся поисковые запросы
- [ ] Результаты поиска обновляются

### Файловая система:
- [ ] Файлы `response_X_YYYYMMDD_HHMMSS.json` создаются в папке

## 🛑 Остановка проекта

Остановите в правильном порядке:
1. [ ] Automation_MT4.py (Ctrl+C)
2. [ ] Appium Server (Ctrl+C)  
3. [ ] MITM Proxy (Ctrl+C)
4. [ ] Деактивируйте окружение: `deactivate`

## 🚨 Если что-то не работает

### Быстрая диагностика:
```bash
# Проверить устройства
adb devices

# Проверить порты
netstat -an | grep 4723
netstat -an | grep 8080

# Проверить файлы
ls -la MetaTrader_Brokers_Data/
```

### Частые решения:
- [ ] Перезапустить эмулятор
- [ ] Перезапустить Appium Server
- [ ] Проверить настройки прокси в эмуляторе
- [ ] Убедиться, что все пути в коде правильные

---

## 🎯 Быстрые команды

### Полная перезагрузка:
```bash
# Остановить все процессы
pkill -f appium
pkill -f mitmproxy

# Перезапустить эмулятор в Genymotion
# Затем повторить шаги 2-4 из "Последовательность запуска"
```

### Проверка результатов:
```bash
# Количество файлов
ls MetaTrader_Brokers_Data/ | wc -l

# Последний файл
ls -t MetaTrader_Brokers_Data/ | head -1

# Размер данных
du -sh MetaTrader_Brokers_Data/
```

**Время выполнения:** ~30-60 минут в зависимости от количества поисковых комбинаций

**Готово! 🎉**