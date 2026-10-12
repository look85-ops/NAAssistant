import re, json, time, requests
from datetime import datetime
from math import radians, cos, sin, sqrt, asin
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# === CONFIG ===
MAX_PRICE = 520000
EXCLUDE_ADDR = ["белинского", "беломорская"]
EXCLUDE_MICRO = ["минск-мир", "минск мир"]

METRO = [
    ("м.Восток", 53.9345, 27.5885),
    ("м.Октябрьская", 53.9010, 27.5580),
    ("м.Акад.наук", 53.9200, 27.5980),
    ("м.Я.Коласа", 53.9150, 27.5810),
]

HEADERS_KUFAR = {
    "User-Agent": "Mozilla/5.0",
    "x-segmentation": "routing=web_re;platform=web;application=ad_listing",
    "Referer": "https://re.kufar.by/",
}

REALT_URL = ("https://realt.by/sale/flats/?"
    "addressV2=%5B%7B%22metroStationUuid%22%3A%22481ca613-7b00-11eb-8943-0cc47adabd66%22%7D"
    "%2C%7B%22metroStationUuid%22%3A%22481caca1-7b00-11eb-8943-0cc47adabd66%22%7D"
    "%2C%7B%22metroStationUuid%22%3A%22481ca9de-7b00-11eb-8943-0cc47adabd66%22%7D"
    "%2C%7B%22metroStationUuid%22%3A%22481caba5-7b00-11eb-8943-0cc47adabd66%22%7D"
    "%2C%7B%22metroStationUuid%22%3A%22481cada1-7b00-11eb-8943-0cc47adabd66%22%7D"
    "%2C%7B%22metroStationUuid%22%3A%22481ca729-7b00-11eb-8943-0cc47adabd66%22%7D"
    "%2C%7B%22metroStationUuid%22%3A%22481ca889-7b00-11eb-8943-0cc47adabd66%22%7D%5D"
    "&balconyType=27&balconyType=2&isFirstStorey=false"
    "&priceMeterType=all&priceTo=160000&priceType=840&rooms=3&rooms=4")


def h(lat1, lng1, lat2, lng2):
    r = 6371
    dlat, dlng = radians(lat2-lat1), radians(lng2-lng1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlng/2)**2
    return 2*r*asin(sqrt(a))


def score(r, dist):
    s = 5.0
    if dist < 0.3: s += 2.5
    elif dist < 0.5: s += 2.0
    elif dist < 0.8: s += 1.5
    elif dist < 1.2: s += 1.0
    elif dist < 2.0: s += 0.5
    elif dist >= 3.0: s -= 1.0
    try: area = float(r.get("area", "60"))
    except: area = 60
    ppm = r["price"] / max(area, 1)
    if ppm < 4500: s += 1.5
    elif ppm < 5000: s += 1.0
    elif ppm < 5500: s += 0.5
    elif ppm >= 6500: s -= 0.5
    fl = r.get("floor", "?/?").split("/")
    try:
        f = int(fl[0]); tf = int(fl[1])
        if tf > 1:
            if 0.25 <= f/tf <= 0.75: s += 0.5
            if f == tf: s -= 0.3
    except: pass
    mat = r.get("material", "").lower()
    if "кирпич" in mat: s += 0.8
    elif "монолит" in mat: s += 0.5
    elif "каркас" in mat: s += 0.3
    elif "панел" in mat: s -= 0.2
    balc = r.get("balcony", "").lower()
    if "два" in balc: s += 0.5
    elif "лоджи" in balc: s += 0.2
    if area >= 80: s += 1.0
    elif area >= 70: s += 0.7
    elif area >= 60: s += 0.3
    try: y = int(str(r.get("year", "1980")))
    except: y = 1980
    if y >= 2010: s += 0.5
    elif y >= 2000: s += 0.3
    elif y < 1970: s -= 0.2
    if r.get("rooms") == "4": s += 0.3
    return round(min(10, max(0, s)), 1)


def fetch_kufar():
    print("[Kufar] searching...")
    p = {"cat":1010,"cur":"USD","gtsy":"country-belarus~province-minsk~locality-minsk",
         "rms":"v.or:3,4","mee":"v.or:7,16,23,3,17,14,5","nff":1,
         "prc":"r:0,160000","size":100,"sort":"lst.d","typ":"sell"}
    resp = requests.get("https://api.kufar.by/search-api/v2/search/map/over",
                       params=p, headers=HEADERS_KUFAR, timeout=30)
    ads = [a for a in resp.json()["ads"] if a.get("r") and a.get("p",0)>0]
    print(f"  {resp.json()['total']} total, {len(ads)} to fetch")
    
    results = []
    for a in ads:
        time.sleep(0.4)
        try:
            r = requests.get(f"https://re.kufar.by/vi/{a['i']}", headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
            if r.status_code != 200: continue
            m = re.search(r'"application/ld\+json"[^>]*>(.*?)</script>', r.text, re.DOTALL)
            if not m: continue
            ld = json.loads(m.group(1))
            for item in ld.get("@graph",[ld]):
                item_type = item.get("@type","")
                if isinstance(item_type, list):
                    if "Product" not in item_type: continue
                elif item_type != "Product": continue
                props = {p2["name"]:p2["value"] for p2 in item.get("additionalProperty",[])}
                price = float(item.get("offers",{}).get("price",0))
                if price <= 0 or price > MAX_PRICE: break
                floor = props.get("Этаж","?"); tf = props.get("Количество этажей","?")
                f = int(floor) if str(floor).isdigit() else 0
                ft = int(tf) if str(tf).isdigit() else 0
                if f == 1: break
                if ft in (4, 5): break  # exclude 4-5 storey buildings
                if props.get("Балкон","") == "Нет": break
                addr_lower = item.get("address",{}).get("streetAddress","").lower()
                if any(ex in addr_lower for ex in EXCLUDE_ADDR): break
                micro = props.get("Микрорайон","").lower()
                if any(ex in micro for ex in EXCLUDE_MICRO): break
                addr = item.get("address",{}).get("streetAddress","?")
                lat = a["c"][1] if len(a["c"])>1 else None
                lng = a["c"][0] if len(a["c"])>0 else None
                best = min(METRO, key=lambda m: h(lat,lng,m[1],m[2])) if lat else ("?",0,0)
                dist = round(h(lat,lng,best[1],best[2]),1) if lat else 99
                results.append({
                    "price": price, "rooms": props.get("Количество комнат","?"),
                    "area": props.get("Общая площадь, м²","?"),
                    "area_l": props.get("Жилая площадь, м²","?"),
                    "floor": f"{floor}/{tf}", "balcony": props.get("Балкон","—"),
                    "material": props.get("Материал стен","—"),
                    "year": props.get("Год постройки","—"),
                    "addr": addr, "district": props.get("Город / Район","?"),
                    "metro": best[0], "dist": dist, "source": "Kufar",
                    "url": f"https://re.kufar.by/vi/{a['i']}",
                })
                results[-1]["score"] = score(results[-1], dist)
                break
        except: pass
    print(f"  {len(results)} passed")
    return results


def fetch_realt():
    print("[Realt] fetching SSR...")
    try:
        r = requests.get(REALT_URL, headers={"User-Agent":"Mozilla/5.0"}, timeout=30)
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.DOTALL)
        if not m: return []
        nd = json.loads(m.group(1))
        raw = nd["props"]["pageProps"]["objects"]
        print(f"  {len(raw)} raw")
        results = []
        for apt in raw:
            price = float(apt.get("price",0) or 0)
            if price <= 0: continue
            if apt.get("priceCurrency",933) == 840: price = price * 3.1
            if price > MAX_PRICE: continue
            fv = apt.get("storey") or 0; tfv = apt.get("storeys") or 0
            f = int(fv) if fv else 0; tf = int(tfv) if tfv else 0
            if tf in (4, 5): continue  # exclude 4-5 storey buildings
            if not apt.get("balconyType"): continue
            addr = apt.get("address","?")
            lat = lng = None
            loc = apt.get("location")
            if isinstance(loc, list) and len(loc)==2:
                lng, lat = loc[0], loc[1]
            best = min(METRO, key=lambda m: h(lat,lng,m[1],m[2])) if lat else ("?",0,0)
            dist = round(h(lat,lng,best[1],best[2]),1) if lat else 99
            results.append({
                "price": price, "rooms": str(apt.get("rooms","?")),
                "area": str(apt.get("areaTotal","?")),
                "area_l": str(apt.get("areaLiving","?")),
                "floor": f"{f}/{tf}" if tf else str(f),
                "balcony": "Есть", "material": str(apt.get("wallMaterial") or "—"),
                "year": str(apt.get("buildingYear") or "—"),
                "addr": addr, "district": str(apt.get("stateDistrictName") or "?"),
                "metro": best[0], "dist": dist, "source": "Realt",
                "url": f"https://realt.by/sale/flats/object/{apt.get('code','')}/",
            })
            results[-1]["score"] = score(results[-1], dist)
        print(f"  {len(results)} after filters")
        return results
    except Exception as e:
        print(f"  Realt error: {e}")
        return []


def dedupe(all_results):
    """Merge duplicates: same street + similar price = keep best score."""
    seen = {}
    for r in all_results:
        price = r["price"]
        addr = r["addr"].lower().strip().replace("минск ", "").replace("  ", " ")
        key = addr[:30]
        if key in seen:
            existing = seen[key]
            if abs(existing["price"] - price) < price * 0.05:
                if r["score"] > existing["score"]:
                    seen[key] = r
                continue
        seen[key] = r
    return list(seen.values())


# === MAIN ===
kufar = fetch_kufar()
realt = fetch_realt()
all_results = dedupe(kufar + realt)
all_results.sort(key=lambda x: x["score"], reverse=True)

print(f"\n=== {len(all_results)} unique (was {len(kufar)+len(realt)} raw) ===\n")

# === EXCEL ===
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Minsk Apartments"

headers = ["Рейтинг","Цена,BYN","к","м²","жил","Этаж","Балкон","Материал","Год","Метро","Район","Адрес","Источник","Ссылка"]
hfont = Font(bold=True, size=11)
hfill = PatternFill(start_color="D9EAD3", end_color="D9EAD3", fill_type="solid")
border = Border(left=Side(style="thin"),right=Side(style="thin"),top=Side(style="thin"),bottom=Side(style="thin"))

for col, name in enumerate(headers, 1):
    c = ws.cell(row=1, column=col, value=name)
    c.font = hfont; c.fill = hfill; c.border = border
    c.alignment = Alignment(horizontal="center", wrap_text=True)

green_fill = PatternFill(start_color="D9EAD3", end_color="D9EAD3", fill_type="solid")
gold_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

for row_idx, r in enumerate(all_results, 2):
    vals = [r["score"], r["price"], r["rooms"], r["area"], r["area_l"],
            r["floor"], r["balcony"], r["material"], r["year"],
            f'{r["metro"]} {r["dist"]}км', r["district"], r["addr"],
            r["source"], r["url"]]
    for col_idx, val in enumerate(vals, 1):
        c = ws.cell(row=row_idx, column=col_idx, value=val)
        c.border = border
        if col_idx == 2:
            c.number_format = '# ##0'
            c.alignment = Alignment(horizontal="right")
        if col_idx == 14:
            c.font = Font(color="0000FF", underline="single")
    sc = r["score"]
    if sc >= 6.5:
        for col_idx in range(1, 15):
            ws.cell(row=row_idx, column=col_idx).fill = green_fill
    elif sc >= 5.0:
        ws.cell(row=row_idx, column=1).fill = gold_fill

widths = [8, 14, 6, 8, 8, 10, 11, 16, 8, 22, 16, 35, 9, 55]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:N{len(all_results)+1}"

now = datetime.now()
filepath = rf"C:\Users\marcenuk\Desktop\Квартиры_Минск_{now:%Y%m%d_%H%M}.xlsx"
wb.save(filepath)
print(f"Excel: {filepath}")
print(f"Rows: {len(all_results)}")

# Quick summary
for r in all_results[:10]:
    print(f"  [{r['score']}] {r['price']:,.0f} BYN {r['rooms']}к {r['area']}м² {r['floor']}эт {r['balcony']} {r['material']} {r['year']}г | {r['metro']} {r['dist']}км | {r['addr']} | {r['source']}")