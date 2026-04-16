#!/usr/bin/env python3
"""Пометить дополнительные 3 модели для удаления"""

import json
import shutil
from pathlib import Path

def main():
    data_dir = Path("../data")
    index_file = data_dir / "index.json"
    
    # Читаем index.json
    with open(index_file, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    print("\n=== ПОМЕЧАЕМ ДОПОЛНИТЕЛЬНЫЕ 3 МОДЕЛИ ===\n")
    
    # Модели для удаления
    models_to_delete = [
        "msa-qwen3coder_next_full_v6_medium",
        "msa-giga38b_full_agent_v5_zero",
        "msa-glm_air_v0.3_t2_zero_t_06"
    ]
    
    renamed_count = 0
    
    for model_name in models_to_delete:
        old_path = data_dir / model_name
        new_path = data_dir / f"del-{model_name}"
        
        if old_path.exists():
            print(f"Переименовываем: {model_name} → del-{model_name}")
            shutil.move(str(old_path), str(new_path))
            renamed_count += 1
        else:
            print(f"⚠️  Папка не найдена: {model_name}")
    
    # Обновляем index.json
    print("\nОбновляем index.json...")
    updated_models = []
    
    for model in index_data["models"]:
        if model["name"] in models_to_delete:
            model["name"] = f"del-{model['name']}"
        updated_models.append(model)
    
    index_data["models"] = updated_models
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    # Подсчет
    keep_count = sum(1 for m in updated_models if not m["name"].startswith("del-"))
    del_count = sum(1 for m in updated_models if m["name"].startswith("del-"))
    
    print(f"\n✅ Готово!")
    print(f"   Переименовано папок: {renamed_count}")
    print(f"   Всего моделей: {len(updated_models)}")
    print(f"   Остается: {keep_count}")
    print(f"   К удалению (del-*): {del_count}")

if __name__ == "__main__":
    main()
