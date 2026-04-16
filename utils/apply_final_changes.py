#!/usr/bin/env python3
"""Применить финальные правки к моделям"""

import os
import json
import shutil
from pathlib import Path

def main():
    data_dir = Path("../data")
    index_file = data_dir / "index.json"
    
    # Читаем index.json
    with open(index_file, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    print("\n=== ПРИМЕНЕНИЕ ФИНАЛЬНЫХ ПРАВОК ===\n")
    
    # 1. Помечаем дополнительные модели для удаления
    models_to_delete = [
        "msa-out_qwen3_coder_LITE",
        "msa-giga38b_agent_v0.3_t2_zero",
        "msa-giga38b_v0_medium"
    ]
    
    print("1. Помечаем дополнительные модели для удаления:")
    for model_name in models_to_delete:
        old_path = data_dir / model_name
        new_path = data_dir / f"del-{model_name}"
        
        if old_path.exists():
            print(f"   {model_name} → del-{model_name}")
            shutil.move(str(old_path), str(new_path))
        else:
            print(f"   ⚠️ Папка не найдена: {model_name}")
    
    # 2. Переименовываем модели
    renames = {
        "msa-glm_v5_full": "msa-glm-4.7-flash",
        "msa-stepun_2250": "msa_gigacode"
    }
    
    print("\n2. Переименовываем модели:")
    for old_name, new_name in renames.items():
        old_path = data_dir / old_name
        new_path = data_dir / new_name
        
        if old_path.exists():
            print(f"   {old_name} → {new_name}")
            shutil.move(str(old_path), str(new_path))
        else:
            print(f"   ⚠️ Папка не найдена: {old_name}")
    
    # 3. Обновляем index.json
    print("\n3. Обновляем index.json...")
    updated_models = []
    
    for model in index_data["models"]:
        name = model["name"]
        
        # Помечаем для удаления
        if name in models_to_delete:
            model["name"] = f"del-{name}"
            updated_models.append(model)
        # Переименовываем
        elif name in renames:
            model["name"] = renames[name]
            updated_models.append(model)
        else:
            updated_models.append(model)
    
    # Сохраняем
    index_data["models"] = updated_models
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    # Подсчет
    keep_count = sum(1 for m in updated_models if not m["name"].startswith("del-"))
    del_count = sum(1 for m in updated_models if m["name"].startswith("del-"))
    
    print(f"\n✅ Готово!")
    print(f"   Всего моделей: {len(updated_models)}")
    print(f"   Остается: {keep_count}")
    print(f"   К удалению (del-*): {del_count}")
    print(f"\n⚠️ ПРОВЕРЬ ЛИДЕРБОРД перед финальным удалением!")

if __name__ == "__main__":
    main()
