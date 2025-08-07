# 📱 Адаптация MetaProxy-Trader для Android Studio AVD

## ✅ Совместимость

**Хорошие новости:** Проект **полностью совместим** с Android Studio AVD! 

### Что работает без изменений:
- ✅ **MITM Proxy** (Global_JSON_Response_Extractor.py)
- ✅ **Appium автоматизация** (основная логика)
- ✅ **Логика поиска** (генерация комбинаций)
- ✅ **Все зависимости** (requirements.txt)

### Что нужно изменить:
- ⚙️ **Device Name** в скрипте автоматизации
- ⚙️ **Путь к APK** файлу
- ⚙️ **Настройка прокси** в AVD

---

## 🔧 Пошаговая адаптация

### Шаг 1: Подготовка AVD

1. **Установите Android Studio**
2. **Создайте AVD:**
   - Tools → AVD Manager
   - Create Virtual Device
   - Выберите: **Pixel 3** + **Android 9.0 (API 28)**
   - Рекомендуемые параметры:
     - RAM: 4GB
     - Storage: 32GB
     - Graphics: Hardware

3. **Установите MetaTrader 4:**
   - Скачайте APK файл
   - Перетащите в AVD или установите через Google Play

### Шаг 2: Получение Device Name

```bash
# Запустите AVD в Android Studio
# Затем выполните команду:
adb devices

# Пример вывода:
# List of devices attached
# emulator-5554    device
```

### Шаг 3: Настройка прокси в AVD

1. **Откройте AVD**
2. **Settings → Network & Internet → Wi-Fi**
3. **Длинный тап на сеть → Modify Network**
4. **Advanced Options → Manual Proxy**
5. **Введите настройки:**
   ```
   Proxy hostname: [IP_ВАШЕГО_КОМПЬЮТЕРА]
   Proxy port: 8080
   ```
6. **Сохраните настройки**

### Шаг 4: Адаптация скрипта

Используйте файл `Automation_MT4_AVD.py` или измените `Automation_MT4.py`:

```python
desired_cap = {
    "platformName": "Android",
    "appium:appPackage": "net.metaquotes.metatrader4",
    "appium:appActivity": "net.metaquotes.metatrader4.ui.MainActivity",
    # ИЗМЕНИТЬ: Укажите правильный путь к APK файлу
    "appium:app": "/path/to/MetaTrader4.apk",  # ← ИЗМЕНИТЬ
    # ИЗМЕНИТЬ: Укажите deviceName вашего AVD
    "appium:deviceName": "emulator-5554"        # ← ИЗМЕНИТЬ
}
```

---

## 🚀 Запуск с AVD

### Последовательность запуска (такая же):

**Терминал 1 - MITM Proxy:**
```bash
mitmproxy -s Global_JSON_Response_Extractor.py
```

**Терминал 2 - Appium Server:**
```bash
appium --port 4723
```

**Терминал 3 - Автоматизация:**
```bash
# Для AVD используйте:
python Automation_MT4_AVD.py
# Или измените оригинальный:
python Automation_MT4.py
```

---

## 🔍 Диагностика AVD

### Проверка подключения:
```bash
# Проверка устройств
adb devices

# Проверка установленных пакетов
adb shell pm list packages | grep metaquotes

# Проверка сетевых настроек
adb shell settings get global http_proxy
```

### Частые проблемы AVD:

**❌ AVD не запускается:**
- Увеличьте RAM в настройках AVD
- Включите Hardware Acceleration в BIOS
- Обновите Android Studio

**❌ Прокси не работает:**
- Перезапустите AVD после настройки прокси
- Проверьте IP адрес компьютера
- Убедитесь, что порт 8080 не занят

**❌ Appium не подключается:**
- Проверьте deviceName через `adb devices`
- Убедитесь, что AVD полностью загружен
- Перезапустите Appium Server

---

## 📊 Сравнение: Genymotion vs AVD

| Аспект | Genymotion | Android Studio AVD |
|--------|------------|-------------------|
| **Производительность** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Простота настройки** | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Совместимость** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Бесплатность** | ❌ (платный) | ✅ (бесплатный) |
| **Интеграция с Android Studio** | ❌ | ✅ |

---

## 🎯 Рекомендации

### Для разработчиков:
- ✅ **AVD лучше** для разработки и тестирования
- ✅ **Бесплатный** и интегрирован с Android Studio
- ✅ **Полная совместимость** с проектом

### Для продакшена:
- ⚠️ **Genymotion может быть быстрее** для больших объемов
- ⚠️ **AVD потребляет больше ресурсов**

---

## ✅ Заключение

**Проект MetaProxy-Trader полностью совместим с Android Studio AVD!**

**Преимущества использования AVD:**
- 🆓 Бесплатный
- 🔧 Интегрирован с Android Studio
- 📱 Официальный эмулятор Google
- 🚀 Полная совместимость с проектом

**Минимальные изменения:**
- Изменить deviceName в скрипте
- Настроить прокси в AVD
- Указать правильный путь к APK

**Готово к использованию! 🎉** 