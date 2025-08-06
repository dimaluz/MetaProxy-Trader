import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from mitmproxy import ctx

# Конфигурация
CONFIG = {
    "output_directory": "MetaTrader_Brokers_Data",  # Относительный путь
    "url_filter": "updates.metaquotes.net/public/mt5/network/mobile",
    "save_duplicates": False,  # Избегать дубликатов
    "add_timestamp": True,     # Добавлять время в имя файла
    "detailed_logging": True   # Подробное логирование
}

# Инициализация
BASE_DIR = Path(__file__).parent / CONFIG["output_directory"]
response_counter = 1
processed_hashes = set()  # Для отслеживания дубликатов

def ensure_directory_exists():
    """Создает директорию для сохранения файлов если она не существует"""
    try:
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        ctx.log.error(f"Не удалось создать директорию {BASE_DIR}: {e}")
        return False

def get_content_hash(content):
    """Генерирует хэш для определения дубликатов"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def generate_filename(counter, add_timestamp=True):
    """Генерирует имя файла с опциональной временной меткой"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if add_timestamp else ""
    if timestamp:
        return f"response_{counter}_{timestamp}.json"
    return f"response_{counter}.json"

def response(flow):
    global response_counter, processed_hashes
    
    # Фильтрация запросов по URL
    if CONFIG["url_filter"] in flow.request.url:
        # Проверка типа контента
        content_type = flow.response.headers.get("content-type", "")
        if "application/json" in content_type:
            try:
                # Парсинг JSON контента
                response_content = flow.response.content.decode('utf-8')
                json_data = json.loads(response_content)
                
                # Проверка на дубликаты
                if not CONFIG["save_duplicates"]:
                    content_hash = get_content_hash(response_content)
                    if content_hash in processed_hashes:
                        if CONFIG["detailed_logging"]:
                            ctx.log.info(f"Пропускаем дубликат ответа (hash: {content_hash[:8]}...)")
                        return
                    processed_hashes.add(content_hash)
                
                # Создание директории если не существует
                if not ensure_directory_exists():
                    return
                
                # Генерация имени файла
                filename = generate_filename(response_counter, CONFIG["add_timestamp"])
                filepath = BASE_DIR / filename
                
                # Сохранение JSON с красивым форматированием
                with open(filepath, "w", encoding='utf-8') as f:
                    json.dump(json_data, f, indent=4, ensure_ascii=False)
                
                # Логирование результатов
                file_size = filepath.stat().st_size
                if CONFIG["detailed_logging"]:
                    ctx.log.info(f"✅ Сохранен ответ #{response_counter}: {filename} ({file_size} байт)")
                    ctx.log.info(f"📁 Путь: {filepath}")
                    if "brokers" in json_data:
                        broker_count = len(json_data.get("brokers", []))
                        ctx.log.info(f"🏢 Найдено брокеров: {broker_count}")
                else:
                    ctx.log.info(f"JSON ответ {response_counter} сохранен: {filename}")
                
                response_counter += 1
                
            except json.JSONDecodeError as e:
                ctx.log.error(f"❌ Ошибка декодирования JSON: {e}")
            except UnicodeDecodeError as e:
                ctx.log.error(f"❌ Ошибка кодировки: {e}")
            except IOError as e:
                ctx.log.error(f"❌ Ошибка записи файла: {e}")
            except Exception as e:
                ctx.log.error(f"❌ Неожиданная ошибка: {e}")

# Инициализация при запуске скрипта
if ensure_directory_exists():
    ctx.log.info(f"🚀 Инициализация Global_JSON_Response_Extractor")
    ctx.log.info(f"📁 Директория сохранения: {BASE_DIR.absolute()}")
    ctx.log.info(f"🎯 Фильтр URL: {CONFIG['url_filter']}")
    ctx.log.info(f"🔄 Дубликаты: {'разрешены' if CONFIG['save_duplicates'] else 'блокированы'}")
else:
    ctx.log.error("❌ Не удалось инициализировать экстрактор")

