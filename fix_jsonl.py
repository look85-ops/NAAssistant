import json
import os

def parse_json_objects(text):
    """Разбить текст на отдельные JSON-объекты, учитывая вложенность скобок."""
    objects = []
    current = []
    depth = 0
    in_string = False
    i = 0
    
    while i < len(text):
        char = text[i]
        
        # Обработка экранированных символов в строке
        if in_string:
            if char == '\\' and i + 1 < len(text):
                current.append(char)
                current.append(text[i + 1])
                i += 2
                continue
            elif char == '"':
                in_string = False
        else:
            if char == '"':
                in_string = True
        
        # Счётчик глубины скобок (только вне строк)
        if not in_string:
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
        
        current.append(char)
        
        # Если достигли глубины 0 и есть данные — это граница объекта
        if depth == 0 and len(''.join(current).strip()) > 0:
            obj_text = ''.join(current).strip()
            if obj_text:
                objects.append(obj_text)
            current = []
        
        i += 1
    
    return objects

def main():
    print("=" * 50)
    print("Исправление слипшегося JSONL-файла")
    print("=" * 50)
    
    # Путь к файлу
    default_path = r"C:\Users\marcenuk\Desktop\Новый проект\data\training\qwen_train.jsonl"
    path = input(f"Введите путь к файлу (или Enter для {default_path}): ").strip()
    
    if not path:
        path = default_path
    
    if not os.path.exists(path):
        print(f"Ошибка: файл не найден — {path}")
        return
    
    print(f"\nЧитаю файл: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Размер файла: {len(content)} символов")
    
    # Разбиваем на объекты
    raw_objects = parse_json_objects(content)
    print(f"Найдено объектов (сырых): {len(raw_objects)}")
    
    # Валидируем каждый объект
    valid_objects = []
    errors = []
    
    for i, obj_text in enumerate(raw_objects):
        try:
            obj = json.loads(obj_text)
            valid_objects.append(obj)
        except json.JSONDecodeError as e:
            errors.append((i + 1, str(e)[:50]))
            print(f"  Предупреждение: объект {i + 1} невалиден — {e.msg}")
    
    print(f"Валидных объектов: {len(valid_objects)}")
    
    if errors:
        print(f"Ошибок валидации: {len(errors)}")
    
    # Сохраняем в новый файл
    base, ext = os.path.splitext(path)
    output_path = f"{base}_fixed.jsonl"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for obj in valid_objects:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')
    
    print(f"\nСохранено в: {output_path}")
    print(f"Итого: {len(valid_objects)} объектов записано")

if __name__ == "__main__":
    main()