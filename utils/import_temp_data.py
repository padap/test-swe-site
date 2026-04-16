#!/usr/bin/env python3
"""
Импорт данных из temp_data в формат demo-swe-mera.
Конвертирует JSONL файлы с замерами агентов в формат data/{model}/results.jsonl
"""
import json
import os
from pathlib import Path
from collections import defaultdict

def parse_temp_jsonl(filepath):
    """Парсит JSONL файл из temp_data."""
    results = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                results.append(data)
            except json.JSONDecodeError as e:
                print(f"Ошибка парсинга {filepath}: {e}")
                continue
    return results

def extract_model_name(filename):
    """Извлекает имя модели из имени файла."""
    # Удаляем расширение .jsonl и суффиксы типа _swemera
    name = filename.replace('.jsonl', '')
    name = name.replace('_swemera', '')
    name = name.replace('_out', '')
    return name

def convert_to_target_format(records):
    """Конвертирует записи в формат {task_id, date, pass@1, pass@6}."""
    converted = []
    for rec in records:
        # Базовые поля
        task_id = rec.get('instance_id', 'unknown')
        created_at = rec.get('created_at', '2025-01-01 00:00:00')
        solved = rec.get('solved', 0)
        
        # pass@1 = solved (0 или 1)
        # pass@6 = пока тоже solved (нет данных о pass@6)
        converted.append({
            'task_id': task_id,
            'date': created_at,
            'pass@1': solved,
            'pass@6': solved
        })
    
    return converted

def main():
    temp_data_dir = Path('../../temp_data')
    data_dir = Path('../data')
    
    if not temp_data_dir.exists():
        print(f"Папка {temp_data_dir} не найдена!")
        return
    
    # Группируем файлы по моделям
    model_files = defaultdict(list)
    
    for filepath in temp_data_dir.glob('*.jsonl'):
        if filepath.name.startswith('DEBUG'):
            continue  # Пропускаем DEBUG файлы
        
        model_name = extract_model_name(filepath.name)
        model_files[model_name].append(filepath)
    
    print(f"Найдено {len(model_files)} моделей")
    
    # Обрабатываем каждую модель
    all_models = []
    
    for model_name, files in sorted(model_files.items()):
        print(f"\\nОбработка модели: {model_name}")
        
        # Собираем все записи для модели
        all_records = []
        for filepath in files:
            records = parse_temp_jsonl(filepath)
            all_records.extend(records)
            print(f"  {filepath.name}: {len(records)} записей")
        
        if not all_records:
            print(f"  Пропускаем {model_name} - нет данных")
            continue
        
        # Конвертируем в целевой формат
        converted = convert_to_target_format(all_records)
        
        # Создаем папку для модели
        model_dir = data_dir / model_name
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # Записываем results.jsonl
        output_file = model_dir / 'results.jsonl'
        with open(output_file, 'w', encoding='utf-8') as f:
            for record in converted:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        print(f"  → Сохранено {len(converted)} записей в {output_file}")
        
        all_models.append({
            'name': model_name,
            'files': {'results': 'results.jsonl'}
        })
    
    # Обновляем index.json
    index_file = data_dir / 'index.json'
    
    # Читаем существующий index
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
    else:
        index_data = {'models': []}
    
    # Добавляем новые модели (не дублируем)
    existing_names = {m['name'] for m in index_data['models']}
    for model in all_models:
        if model['name'] not in existing_names:
            index_data['models'].append(model)
    
    # Сортируем по имени
    index_data['models'].sort(key=lambda x: x['name'])
    
    # Записываем index.json
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"\\n✅ Обработано {len(all_models)} моделей")
    print(f"✅ Обновлен {index_file}")
    print(f"\\nВсего моделей в индексе: {len(index_data['models'])}")

if __name__ == '__main__':
    main()
