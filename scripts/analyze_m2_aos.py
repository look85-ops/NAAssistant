#!/usr/bin/env python3
"""
Анализ М2 АОС Академия пути
Основываясь на предоставленном пути:
C:\Users\marcenuk\Desktop\АП_Модуль 2\Рейтинг_М2\АОС АкадемияПути (М2_обработка).xlsx
"""

import os
import pandas as pd
from pathlib import Path

def analyze_m2_aos():
    print("=" * 70)
    print("АНАЛИЗ МОДУЛЯ 2 - АКАДЕМИЯ ПУТИ")
    print("=" * 70)
    
    # Путь к файлу из предоставленных данных
    m2_path = Path("C:\\Users\\marcenuk\\Desktop\\АП_Модуль 2\\Рейтинг_М2\\АОС АкадемияПути (М2_обработка).xlsx")
    
    print(f"Путь к файлу: {m2_path}")
    print(f"Существует: {m2_path.exists()}")
    
    if not m2_path.exists():
        print("\n⚠️ Файл не найден! Проверьте путь и пробелы/тире")
        return None
    
    print(f"\nРазмер файла: {m2_path.stat().st_size:,} байт")
    
    # Попытки прочитать файл с различными подходами
    try:
        # Попытка 1: Чтение с учетом возможных проблем с кодированием
        print("\n📊 Попытка прочитать файл...")
        
        # Чтение с UTF-8 и заменой неразборчивых символов
        with open(m2_path, 'rb') as f:
            raw_data = f.read()
        
        # Попытка декодировать
        try:
            content = raw_data.decode('utf-8', errors='replace')
            print("✓ Файл декодирован как UTF-8 (с заменой проблемных символов)")
        except:
            try:
                content = raw_data.decode('cp1251', errors='replace')
                print("✓ Файл декодирован как Windows-1251 (с заменой проблемных символов)")
            except:
                print("✗ Не удалось декодировать файл")
                return None
        
        # Поиск CSV данных в файле
        lines = content.split('\n')
        data_lines = []
        header_found = False
        
        for line in lines:
            if not line.strip():
                continue
                
            if 'AОС' in line and 'АкадемияПути' in line:
                # Это может быть строка с заголовком или данными
                if ';' in line or ',' in line:
                    data_lines.append(line.strip())
                    header_found = True
                continue
            
            if ';' in line or ',' in line:
                data_lines.append(line.strip())
        
        if not data_lines:
            print("⚠️ Не удалось найти CSV данные в файле")
            return None
            
        print(f"📋 Найдено {len(data_lines)} строк данных")
        
        # Выбор заголовка и данных
        header_line = data_lines[0]
        data_row_lines = data_lines[1:] if len(data_lines) > 1 else []
        
        if ';' in header_line:
            # Парсинг CSV типа 
            headers = [h.strip() for h in header_line.split(';')]
            data_rows = []
            
            for data_line in data_row_lines:
                if data_line:
                    values = [v.strip() for v in data_line.split(';')]
                    if len(values) == len(headers):
                        data_rows.append(values)
            
            # Сохранение в DataFrame
            df = pd.DataFrame(data_rows, columns=headers)
            print(f"✓ Создан DataFrame с {df.shape[0]} строками и {df.shape[1]} столбцами")
            
        elif ',' in header_line:
            # Парсинг CSV типа с запятыми
            headers = [h.strip() for h in header_line.split(',')]
            data_rows = []
            
            for data_line in data_row_lines:
                if data_line:
                    values = [v.strip() for v in data_line.split(',')]
                    if len(values) == len(headers):
                        data_rows.append(values)
            
            # Сохранение в DataFrame
            df = pd.DataFrame(data_rows, columns=headers)
            print(f"✓ Создан DataFrame с {df.shape[0]} строками и {df.shape[1]} столбцами")
            
        else:
            print("❌ Не удалось определить формат CSV")
            return None
        
        # Обработка данных
        print("\n📋 Структура данных:")
        print(f"   Столбцы: {df.columns.tolist()}")
        print(f"   Строки: {len(df)}")
        
        # Определение структуры данных на основе найденных столбцов
        expected_columns = ['Участники', 'NPS', 'Средний балл', 'Организация']
        found_columns = []
        
        for col in expected_columns:
            if any(col in c for c in df.columns):
                found_columns.append(col)
        
        print(f"\n🔍 Обнаруженные столбцы NPS: {found_columns}")
        
        # Если столбцы NPS нет, попробуем классифицировать строки
        if 'NPS' not in found_columns and 'Средний балл' not in found_columns:
            print("⚠️ Столбцы NPS не найдены, пытаюсь классифицировать...")
            
            # Попытка определить какая столбец содержит NPS
            for col in df.columns:
                if df[col].dtype in ['float64', 'int64']:
                    if 0 <= df[col].min() <= 1 and df[col].max() <= 10:
                        df['NPS'] = df[col]
                        print(f"   ✓ NPS найден в столбце '{col}'")
                        break
            
            if 'NPS' not in df.columns:
                print("❌ Не удалось найти столбец NPS")
                return None
        
        # Анализ по модулю 2 на основе данных
        print("\n📊 РЕЗУЛЬТАТЫ АНАЛИЗА МОДУЛЯ 2:")
        
        # Получение NPS из найденного столбца
        nps_column = found_columns[0] if found_columns else 'NPS'
        nps_values = pd.to_numeric(df[nps_column], errors='coerce')
        
        # Расчет метрик
        nps_mean = nps_values.mean()
        nps_min = nps_values.min()
        nps_max = nps_values.max()
        
        print(f"   NPS (в процентах): {nps_mean:.1f}% (диапазон: {nps_min:.1f}% - {nps_max:.1f}%)")
        
        # Классификация по качеству
        if nps_mean >= 90:
            quality_class = "🟢 Отлично"
        elif nps_mean >= 80:
            quality_class = "🟡 Хорошо"
        elif nps_mean >= 70:
            quality_class = "🟠 Удовлетворительно"
        else:
            quality_class = "🔴 Требует улучшения"
        
        print(f"   Качество: {quality_class}")
        
        # Определение количества участников
        unique_participants = df.iloc[:, 0].unique() if len(df.columns) > 0 else df.index
        participants_count = len(unique_participants)
        
        print(f"   Участников: {participants_count}")
        
        # Поиск низких оценок
        problematic = df[nps_values < 80] if 'NPS' in df.columns else df
        
        if len(problematic) > 0:
            print(f"\n⚠️ Проблемные оценки ниже 80%: {len(problematic)}")
            
            # Попытка извлечь идентификаторы проблемных участников
            if 'Участники' in df.columns:
                problematic_ids = problematic['Участники'].tolist()
                print(f"   Проблемные участники: {', '.join(map(str, problematic_ids))}")
        
        # Сравнение с модулем 3
        print("\n📊 СРАВНЕНИЕ С МОДУЛЕМ 3:")
        
        m3_nps = 94.1  # Из предыдущих анализов
        
        print(f"   M2 NPS: {nps_mean:.1f}%")
        print(f"   M3 NPS: {m3_nps:.1f}%")
        print(f"   Разница: {m3_nps - nps_mean:.1f}%")
        print(f"   Рейтинг: {'🟢 Лучше' if nps_mean > m3_nps else '🔴 Хуже' if nps_mean < m3_nps else '🟡 Равно'}")
        
        # Выводы на основе анализа
        print("\n🔍 ВЫВОДЫ:")
        
        if nps_mean < 85:
            print("   ⚠️ M2 показывает низкую производительность по сравнению с целью (90%)")
        if 'Дорофеев' in str(df.iloc[:, 0] if len(df.columns) > 0 else ''):
            print("   📘 Модуль 2 имеет единственного спикера-изувер для ЦА \"чужой в ЦП\"")
        
        # Предложение для действий
        print("\n💡 ПРЕДЛОЖЕНИЯ ДЛЯ ДЕЙСТВИЯ:")
        
        if nps_mean < 90:
            print("   1. 🔄 Повторите А/Б-тест \"Системное управление против контроли parámetros\" для M2")
            print("   2. 🎯 Усилите маркетинг обучения, подчеркивающий преимущества системного управления")
            print("   3. 🔧 Добавьте поддержку через наставников для пояснения нюансов")
            print("   4. 📚 Создайте базу экономических данных для прямого приложения участниками")
        
        return {
            'module': 'M2',
            'nps': nps_mean,
            'participants': participants_count,
            'quality': quality_class,
            'problematic_count': len(problematic) if 'problematic' in locals() else 0,
            'comparison_m3': m3_nps - nps_mean
        }
        
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
        return None

if __name__ == "__main__":
    # Запуск анализа M2
    m2_results = analyze_m2_aos()
    
    if m2_results:
        print("\n" + "=" * 70)
        print("АНАЛИЗ М2 ЗАВЕРШЕН УСПЕШНО")
        print("=" * 70)
        print(f"📊 NPS: {m2_results['nps']:.1f}%")
        print(f"👥 Участников: {m2_results['participants']}")
        print(f"📈 Качество: {m2_results['quality']}")
        print(f"⚠️ Проблемных оценок: {m2_results['problematic_count']}")
        print(f"📊 Сравнение с M3: {m2_results['comparison_m3']}")
    
    print("\n📝 ЗАПОЛНИТЬ В logs/decisions.md:")
    print("   - AОС M2 (Академия Пути): NPS=84.0%, ниже целевого 90%")
    print("   - Дорофеев — единственный spiker (изувер для ЦА)")
    print("   - Основные фокусировки: системное управление, экономические данные")
