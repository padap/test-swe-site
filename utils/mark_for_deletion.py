#!/usr/bin/env python3
"""Скрипт для пометки моделей префиксом del- перед удалением"""

import os
import json
import shutil
from pathlib import Path

# Модели которые НЕ трогаем (оставляем как есть)
KEEP_MODELS = {
    # Aider модели - все оставляем
    "aider-Codestral-v0.1",
    "aider-DeepSeek-R1-DQ32B",
    "aider-Devstral-24B",
    "aider-Llama-3.3-70B",
    "aider-QwQ-32B",
    "aider-Qwen2.5-Coder-14B",
    "aider-Qwen2.5-Coder-32B",
    "aider-Qwen2.5-Coder-7B",
    "aider-Qwen3-32B",
    "aider-deepseek-r1",
    
    # MSA модели - лучшие из каждой группы
    "msa-qwen3_coder_next",  # 38.64% - топ
    "msa-minimax_2_5",  # 24.69%
    "msa-stepun_2250",  # 20.21%
    "msa-out_qwen3_coder_LITE",  # 15.74%
    "msa-giga38b_agent_v0.3_t2_zero",  # 14.49%
    "msa-giga38b_full_agent_v5_zero",  # 13.60%
    "msa-qwen3_235b_a22b_instruct",  # 11.99%
    "msa-qwen3coder_next_full_v6_medium",  # 12.88%
    "msa-glm_v5_full",  # 10.38%
    "msa-qwen3_coder_30b",  # 8.41%
    "msa-giga38b_v0_medium",  # 7.33%
    "msa-gpt-oss-120b",  # 7.51%
    "msa-glm_air_v0.3_t2_zero_t_06",  # 6.26%
}

def main():
    data_dir = Path("../data")
    index_file = data_dir / "index.json"
    
    # Читаем index.json
    with open(index_file, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    models_to_rename = []
    models_to_keep = []
    
    # Собираем модели для переименования
    for model in index_data["models"]:
        name = model["name"]
        if name.startswith("del-"):
            # Уже помечена
            continue
        if name in KEEP_MODELS:
            models_to_keep.append(name)
        else:
            models_to_rename.append(name)
    
    print(f"\n✅ Оставляем: {len(models_to_keep)} моделей")
    print(f"🗑️  Помечаем для удаления: {len(models_to_rename)} моделей\n")
    
    # Переименовываем папки
    renamed_count = 0
    for model_name in models_to_rename:
        old_path = data_dir / model_name
        new_path = data_dir / f"del-{model_name}"
        
        if old_path.exists():
            print(f"  Переименовываем: {model_name} → del-{model_name}")
            shutil.move(str(old_path), str(new_path))
            renamed_count += 1
        else:
            print(f"  ⚠️  Папка не найдена: {model_name}")
    
    print(f"\n✅ Переименовано папок: {renamed_count}")
    
    # Обновляем index.json
    updated_models = []
    for model in index_data["models"]:
        name = model["name"]
        if name in KEEP_MODELS:
            updated_models.append(model)
        elif not name.startswith("del-"):
            # Добавляем префикс del-
            model["name"] = f"del-{name}"
            updated_models.append(model)
        else:
            # Уже с префиксом
            updated_models.append(model)
    
    # Сохраняем обновленный index.json
    index_data["models"] = updated_models
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Обновлен index.json")
    print(f"\nВсего в индексе: {len(updated_models)} моделей")
    print(f"  - Оставлено: {len(models_to_keep)}")
    print(f"  - Помечено для удаления: {len(models_to_rename)}")
    print(f"\n⚠️  ПРОВЕРЬ ЛИДЕРБОРД! Если всё ОК, запусти скрипт удаления.")

if __name__ == "__main__":
    main()
