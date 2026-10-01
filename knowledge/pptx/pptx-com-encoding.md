# COM + кириллица: TextPlaceholder vs TextBox (урок из М3Д1, 2026-08-06)

Проблема: win32com возвращает битый текст (кракозябры) для TextBox (type 17),
но корректный для TextPlaceholder (type 14) при чтении русских символов.

**Решение:** идентифицировать шаблоны по SlideID (уникальный ID слайда в COM),
а не по тексту. `pres.Slides.Item(N).SlideID` не меняется при перестановках.

**Детали:**
- `shp.TextFrame.TextRange.Text` для TextBox (type 17) — возвращает нечитаемые
  символы (cp1251 → Latin-1), сравнение с русскими строками не работает.
- `shp.TextFrame.TextRange.Text` для Text Placeholder (type 14) — возвращает
  корректные русские строки.
- SlideID стабилен после клонирования и MoveTo.

**Использование:**
```python
tpl_id = pres.Slides.Item(4).SlideID  # запомнить ID шаблона
# позже найти:
for i in range(1, count+1):
    if pres.Slides.Item(i).SlideID == tpl_id: return i
```

**Применимо:** все модули с программой «Профессионал+. Путь» и подобными
презентациями, где шаблоны содержат русский текст в TextBox.
