#!/usr/bin/env python3
"""
Скрипт для конвертации данных из формата sample*.json в JSONL формат
"""
import json
import os
from pathlib import Path
from collections import defaultdict

# Читаем все sample*.json файлы
data_dir = Path("src/data")
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

# Собираем все данные
all_rows = []
for json_file in sorted(data_dir.glob("sample*.json")):
    print(f"Loading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Преобразуем колоночный формат в строчный
    keys = list(data.keys())
    n_rows = len(data[keys[0]])
    
    for i in range(n_rows):
        row = {}
        for key in keys:
            row[key] = data[key].get(str(i), data[key].get(i))
        all_rows.append(row)

print(f"Total rows: {len(all_rows)}")

# Группируем по моделям
models_data = defaultdict(list)
for row in all_rows:
    model = row['model']
    models_data[model].append({
        'date': row['date'],
        'task_id': row['task_id'],
        'pass@1': row['pass@1'],
        'pass@6': row.get('pass@6', 0)
    })

print(f"Total models: {len(models_data)}")

# Создаем структуру: data/{model}/results.jsonl
index_data = {"models": []}

for model, rows in models_data.items():
    model_dir = output_dir / model
    model_dir.mkdir(exist_ok=True)
    
    # Пишем results.jsonl
    jsonl_file = model_dir / "results.jsonl"
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for row in rows:
            # Конвертируем timestamp в ISO дату
            if isinstance(row['date'], (int, float)):
                from datetime import datetime
                date_str = datetime.fromtimestamp(row['date'] / 1000).strftime('%Y-%m-%d')
            else:
                date_str = row['date']
            
            f.write(json.dumps({
                'date': date_str,
                'task_id': row['task_id'],
                'pass@1': row['pass@1'],
                'pass@6': row['pass@6']
            }) + '\n')
    
    # Добавляем в index
    index_data["models"].append({
        "name": model,
        "files": {"results": "results.jsonl"}
    })
    
    print(f"  ✓ {model}: {len(rows)} rows")

# Пишем index.json
with open(output_dir / "index.json", 'w', encoding='utf-8') as f:
    json.dump(index_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Done! Created {len(models_data)} model directories in data/")
print(f"✅ Created data/index.json")
