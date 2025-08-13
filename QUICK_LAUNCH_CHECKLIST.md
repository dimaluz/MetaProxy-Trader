# ✅ Быстрый чеклист запуска MetaProxy-Trader

## 🚀 Экспресс-запуск (для опытных пользователей)

### Предварительные требования:
- [ ] Python 3.7+ установлен
- [ ] Node.js 14.0+ установлен  
- [ ] Samsung A50 подключен через USB
- [ ] USB отладка включена на устройстве
- [ ] MetaTrader 4 установлен на устройстве

---

## 📋 Быстрая настройка

### 1. Установка зависимостей (5 минут)
```bash
cd /path/to/MetaProxy-Trader
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
npm install -g appium
appium driver install uiautomator2
```

### 2. Настройка устройства (5 минут)
```bash
# Проверьте подключение
adb devices

# Скопируйте deviceName из вывода
# Пример: RF8R91KXXXX
```

### 3. Обновление скрипта (2 минуты)
```python
# В файле Automation_MT4.py замените:
"appium:deviceName": "Samsung_A50"  # ← ИЗМЕНИТЬ
# На:
"appium:deviceName": "RF8R91KXXXX"  # Ваш реальный deviceName
```

---

## 🚀 Быстрый запуск

### Подготовка терминалов:
**Терминал 1:** `cd /path/to/MetaProxy-Trader && source venv/bin/activate`  
**Терминал 2:** `cd /path/to/MetaProxy-Trader`  
**Терминал 3:** `cd /path/to/MetaProxy-Trader && source venv/bin/activate`

### Последовательность запуска:

**1. MITM Proxy (Терминал 1):**
```bash
mitmproxy -s Global_JSON_Response_Extractor.py
```

**2. Appium Server (Терминал 2):**
```bash
appium --port 4723
```

**3. Автоматизация (Терминал 3):**
```bash
python Automation_MT4.py
```

---

## 📊 Ожидаемые результаты

### Успешный запуск:
```
🚀 Запуск автоматизации для физического устройства Samsung A50
📱 Device Name: RF8R91KXXXX
✅ Успешно подключились к устройству!
🔍 Ожидаем элемент для: Кнопка accept (попытка 1)
✅ Кликаем: Кнопка accept (попытка 1)
🚀 Начинаем поиск с 100 уникальными комбинациями...
📝 Поиск 1/100: 'a1z'
✅ Успешно ввели 'a1z'
```

### MITM Proxy логи:
```
✅ Сохранен ответ #1: response_1_20240813_120523.json (2,435 байт)
🏢 Найдено брокеров: 15
```

---

## 🛠️ Быстрое устранение проблем

### Устройство не определяется:
```bash
adb kill-server && adb start-server
adb devices
```

### Элементы не находятся:
- Увеличьте `WAIT_TIMEOUT = 60` в скрипте
- Проверьте через Appium Inspector

### MITM не работает:
- Проверьте настройки прокси на устройстве
- Установите сертификат с `http://mitm.it`

---

## ⏱️ Временные рамки

| Этап | Время |
|------|-------|
| Установка зависимостей | 5-10 минут |
| Настройка устройства | 5 минут |
| Обновление скрипта | 2 минуты |
| Запуск компонентов | 2 минуты |
| Выполнение автоматизации | 30-120 минут |

**Общее время настройки:** ~15 минут  
**Общее время выполнения:** 30-120 минут

---

## 🎯 Критические моменты

### Обязательно проверить:
- [ ] `adb devices` показывает устройство
- [ ] deviceName обновлен в скрипте
- [ ] MetaTrader 4 установлен и запускается
- [ ] 3 терминала готовы к запуску

### Критические ошибки:
- ❌ "device not found" → Проверьте USB подключение
- ❌ "Activity not found" → Переустановите MetaTrader 4
- ❌ "TimeoutException" → Увеличьте WAIT_TIMEOUT

---

## 📁 Результаты

После успешного выполнения:
- Файлы сохраняются в `MetaTrader_Brokers_Data/`
- Формат: `response_X_YYYYMMDD_HHMMSS.json`
- Статистика выводится в конце

### Проверка результатов:
```bash
ls -la MetaTrader_Brokers_Data/
echo "Файлов: $(ls MetaTrader_Brokers_Data/ | wc -l)"
echo "Размер: $(du -sh MetaTrader_Brokers_Data/)"
```

---

## 🚨 Экстренная остановка

**Если что-то пошло не так:**
1. `Ctrl+C` во всех терминалах
2. `adb kill-server`
3. Перезапустите устройство
4. Начните заново

**Готово! 🚀**
