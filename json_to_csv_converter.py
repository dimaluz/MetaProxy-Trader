#!/usr/bin/env python3
"""
Конвертер JSON файлов в CSV формат для MetaProxy-Trader
Преобразует собранные JSON данные о брокерах в CSV формат для импорта в Google Sheets
"""

import json
import csv
import os
from pathlib import Path
from datetime import datetime

def load_json_files(json_dir):
    """Загружает все JSON файлы из указанной директории"""
    json_files = []
    json_path = Path(json_dir)
    
    if not json_path.exists():
        print(f"❌ Директория {json_dir} не существует")
        return []
    
    # Ищем все JSON файлы
    for file_path in json_path.glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                json_files.append({
                    'filename': file_path.name,
                    'data': data,
                    'timestamp': file_path.stem.split('_')[2:4] if '_' in file_path.stem else ['unknown', 'unknown']
                })
            print(f"✅ Загружен файл: {file_path.name}")
        except Exception as e:
            print(f"❌ Ошибка при загрузке {file_path.name}: {e}")
    
    return json_files

def extract_broker_data(json_data):
    """Извлекает данные о брокерах из JSON структуры"""
    brokers = []
    
    def extract_from_dict(data, path=""):
        """Рекурсивно извлекает данные из словаря"""
        if isinstance(data, dict):
            # Проверяем, содержит ли объект данные о брокере
            broker_keys = ['name', 'title', 'company', 'broker', 'server', 'description']
            if any(key in data for key in broker_keys):
                broker_info = {
                    'name': data.get('name', data.get('title', data.get('company', ''))),
                    'server': data.get('server', data.get('server_name', '')),
                    'description': data.get('description', data.get('comment', '')),
                    'type': data.get('type', ''),
                    'country': data.get('country', ''),
                    'url': data.get('url', data.get('website', '')),
                    'path': path
                }
                brokers.append(broker_info)
            
            # Рекурсивно обрабатываем все значения
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                extract_from_dict(value, new_path)
        
        elif isinstance(data, list):
            # Обрабатываем массивы
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                extract_from_dict(item, new_path)
    
    extract_from_dict(json_data)
    return brokers

def create_csv_output(brokers, output_file):
    """Создает CSV файл с данными о брокерах"""
    if not brokers:
        print("⚠️ Нет данных о брокерах для сохранения")
        return False
    
    # Определяем все возможные поля
    all_fields = set()
    for broker in brokers:
        all_fields.update(broker.keys())
    
    # Сортируем поля для стабильного порядка
    fieldnames = sorted(list(all_fields))
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for broker in brokers:
                # Заполняем отсутствующие поля пустыми значениями
                row = {field: broker.get(field, '') for field in fieldnames}
                writer.writerow(row)
        
        print(f"✅ CSV файл создан: {output_file}")
        print(f"📊 Сохранено {len(brokers)} записей о брокерах")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании CSV файла: {e}")
        return False

def main():
    """Основная функция конвертера"""
    print("🔄 Конвертер JSON в CSV для MetaProxy-Trader")
    print("=" * 50)
    
    # Настройки
    json_directory = "Captured_JSON"
    output_csv = f"brokers_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Загружаем JSON файлы
    print(f"📁 Загружаем JSON файлы из {json_directory}...")
    json_files = load_json_files(json_directory)
    
    if not json_files:
        print("❌ Не найдено JSON файлов для обработки")
        return
    
    print(f"✅ Загружено {len(json_files)} JSON файлов")
    
    # Извлекаем данные о брокерах
    print("🔍 Извлекаем данные о брокерах...")
    all_brokers = []
    
    for file_info in json_files:
        brokers = extract_broker_data(file_info['data'])
        all_brokers.extend(brokers)
        print(f"📊 Извлечено {len(brokers)} брокеров из {file_info['filename']}")
    
    # Удаляем дубликаты по имени и серверу
    unique_brokers = []
    seen = set()
    
    for broker in all_brokers:
        key = (broker['name'], broker['server'])
        if key not in seen:
            seen.add(key)
            unique_brokers.append(broker)
    
    print(f"🔄 Удалено {len(all_brokers) - len(unique_brokers)} дубликатов")
    
    # Создаем CSV файл
    print(f"💾 Создаем CSV файл: {output_csv}")
    if create_csv_output(unique_brokers, output_csv):
        print("\n🎉 Конвертация завершена успешно!")
        print(f"📄 Файл готов для импорта в Google Sheets: {output_csv}")
        print("\n📋 Инструкция по импорту в Google Sheets:")
        print("1. Откройте Google Sheets")
        print("2. File → Import")
        print("3. Upload → выберите файл " + output_csv)
        print("4. Import location: Create new spreadsheet")
        print("5. Separator type: Comma")
        print("6. Нажмите Import data")
    else:
        print("❌ Ошибка при создании CSV файла")

if __name__ == "__main__":
    main()
