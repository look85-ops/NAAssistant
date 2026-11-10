import json, time, sys
import requests

NOM = "https://nominatim.openstreetmap.org/search"
HDR = {"User-Agent": "NMAssistant-local-context/1.0 (personal, low rate)"}

def geo(address):
    try:
        r = requests.get(NOM, params={"format":"json","q":address,"limit":1}, headers=HDR, timeout=20)
        r.raise_for_status()
        d = r.json()
        if d:
            return float(d[0]["lat"]), float(d[0]["lon"]), d[0]["display_name"]
    except Exception as e:
        print("geo err:", e, file=sys.stderr)
    return None

home = geo("Дубнинская 6 корпус 2, Москва")
if home is None:
    home = geo("Дубнинская улица, Москва")
print("HOME:", home, file=sys.stderr)
if home is None:
    sys.exit("no home")
lat, lon, label = home
RADIUS = 2400

# Поиск поблизости: Nominatim support "around" per category.
# Используем параметр viewbox/around через специальный синтаксис: correlated query
# Проще: поиск с "q=кафе" и "viewbox" — надёжнее с viewbox + bounded.
def nearby(q, limit=8):
    try:
        params = {
            "format":"json","q":q,"limit":limit,
            "viewbox": f"{lon-0.05},{lat+0.05},{lon+0.05},{lat-0.05}",
            "bounded":1,
            "addressdetails":1,
        }
        r = requests.get(NOM, params=params, headers=HDR, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("nearby err:", q, e, file=sys.stderr)
        return []

CATS = {
    "Еда и кофе": ["кафе","кофейня","ресторан","пекарня","кондитерская","пиццерия","столовая"],
    "Продукты": ["супермаркет","продуктовый магазин","пекарня-магазин","магазин продуктов","рынок"],
    "Парки и прогулки": ["парк","сквер","бульвар","детская площадка","пруд","стадион"],
    "Третьи места": ["библиотека","культурный центр","дом культуры","книжный магазин","кинотеатр","музей","анти-кафе"],
    "Здоровье и медицина": ["клиника","поликлиника","аптека","Медси","стоматология"],
    "Покупки и быт": ["торговый центр","магазин одежды","парикмахерская","банк","отделение почты","салон красоты"],
    "Транспорт": ["станция метро","железнодорожная станция","остановка автобуса"],
    "Необычное и красивое": ["храм","церковь","памятник","скульптура","арт-объект","фреска","усадьба"],
}

OUT = "projects/moscow-local/poi-data.json"

def load_partial():
    try:
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"home": {"lat": lat, "lon": lon, "label": label, "radius": RADIUS}, "spots": {}}

def save_partial(spots):
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"home": {"lat": lat, "lon": lon, "label": label, "radius": RADIUS}, "spots": spots}, f, ensure_ascii=False, indent=2)

data = load_partial()
spots = data.get("spots", {})

for cat, queries in CATS.items():
    if cat in spots:
        continue  # уже собрано ранее
    found = {}
    for q in queries:
        for d in nearby(q):
            name = d.get("display_name","").split(",")[0]
            ll = [float(d["lat"]), float(d["lon"])]
            key = name.lower()
            if key not in found:
                found[key] = {"name": name, "ll": ll, "why": q}
        time.sleep(0.5)
    spots[cat] = list(found.values())
    save_partial(spots)  # чекпоинт после каждой категории

for cat, lst in spots.items():
    print(f"=== {cat} ({len(lst)}) ===", file=sys.stderr)
    for s in lst:
        print(" -", s["name"], s["why"], s["ll"], file=sys.stderr)