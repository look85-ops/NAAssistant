import json, html

SRC = "projects/moscow-local/poi-data.json"
DST = "projects/moscow-local/index.html"

d = json.load(open(SRC, encoding="utf-8"))
home = d["home"]
spots = d["spots"]

def esc(s):
    return html.escape(str(s), quote=False)

# собрать JS-группы
groups_js = []
for cat, lst in spots.items():
    items = ", ".join(
        '{"name":%s,"why":%s,"ll":[%r,%r],"dist":%d}' % (
            json.dumps(s["name"], ensure_ascii=False),
            json.dumps(s["why"], ensure_ascii=False),
            s["ll"][0], s["ll"][1], s["dist"])
        for s in lst
    )
    groups_js.append('{"cat":%s,"items":[%s]}' % (json.dumps(cat, ensure_ascii=False), items))

HOME_JS = '[%r, %r]' % (home["lat"], home["lon"])

html_doc = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Мои места — полчаса от дома</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  :root{--paper:#f6f2ea;--card:#fbf9f4;--ink:#191613;--muted:#7a746c;--line:#26221c;--hl:#2d5568;--hl-bg:#e7edf0}
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{background:var(--paper);color:var(--ink);font-family:"Helvetica Neue",-apple-system,"Segoe UI",Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.5}
  .wrap{max-width:1080px;margin:0 auto;padding:0 24px}
  .serif{font-family:Georgia,"Times New Roman",serif}
  header{padding:32px 0 0}
  .masthead{display:flex;justify-content:space-between;align-items:baseline;border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);padding:8px 2px;font-size:12px;letter-spacing:.22em;text-transform:uppercase;flex-wrap:wrap;gap:6px}
  .hero{position:relative;padding:56px 0 40px;overflow:hidden}
  .hero #map{position:absolute;inset:0;z-index:0;opacity:.22;filter:grayscale(1);pointer-events:none}
  .hero h1,.hero .sub{position:relative;z-index:1}
  h1{font-family:Georgia,"Times New Roman",serif;font-size:clamp(40px,7.5vw,78px);font-weight:700;line-height:.98;letter-spacing:-.01em;max-width:26ch}
  .sub{margin-top:22px;font-size:15px;color:var(--muted);max-width:74ch;font-style:italic}
  .ticker{margin-top:36px;border:1.5px solid var(--ink);padding:14px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;background:var(--card)}
  .ticker .big{font-family:Georgia,"Times New Roman",serif;font-size:30px;font-weight:700;letter-spacing:.02em}
  .ticker .lbl{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
  .legend{margin-top:20px;font-size:13px;color:var(--muted);font-style:italic}
  main{padding:12px 0 80px}
  section{padding:36px 0 8px}
  .cat-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;border-bottom:2px solid var(--ink);padding-bottom:10px;margin-bottom:22px}
  .cat-head h2{font-family:Georgia,"Times New Roman",serif;font-size:26px;font-weight:700}
  .cat-head span{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
  .card{background:var(--card);border:1px solid var(--line);padding:18px;cursor:pointer;position:relative;display:flex;flex-direction:column;min-height:140px;transition:border-color .15s ease}
  .card:hover{border-color:var(--hl)}
  .card.visited{background:var(--hl-bg);border-color:var(--hl)}
  .card .name{font-family:Georgia,"Times New Roman",serif;font-size:19px;font-weight:700;line-height:1.1}
  .card .why{margin-top:8px;font-size:13px;color:var(--muted);line-height:1.45}
  .card .walk{margin-top:10px;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--hl)}
  .card .maplink{margin-top:12px;font-size:12px;letter-spacing:.1em;text-transform:uppercase;text-decoration:underline;text-underline-offset:3px;align-self:flex-start}
  .card .check{position:absolute;top:14px;right:14px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--hl);opacity:0;transition:opacity .2s ease}
  .card.visited .check{opacity:1}
  .card.visited .check::before{content:"✓ "}
  footer{padding:30px 0 70px;border-top:1px solid var(--ink);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
</style>
</head>
<body>
<header class="wrap">
  <div class="masthead">
    <span>Дубнинская 6к2</span>
    <span>Москва · до отъезда</span>
  </div>
  <div class="hero">
    <div id="map"></div>
    <h1>Мои места<br>в получасе<br>от дома</h1>
    <p class="sub">52 точки в радиусе 2.4 км (~30 мин пешком), собранные из OpenStreetMap. Что значимо именно здесь — тебе виднее меня: кликни по карточке, чтобы отметить «была». Карта живёт в браузере, никуда не уходит.</p>
  </div>
  <div class="ticker">
    <span class="lbl">Рядом с домом</span>
    <span class="big serif" id="count">0</span>
  </div>
  <div class="legend">Отсортировано по расстоянию от дома. «Почему это я» — категория объекта из карты, при желании перепишешь на своё.</div>
</header>

<main class="wrap">
  <div id="sections"></div>
</main>

<footer class="wrap">Локальный контекст · карта © OpenStreetMap (Nominatim) · данные собраны вручную, возможны неточности</footer>

<script>
const HOME = HOMEPLACEHOLDER;
const GROUPS = [GROUPSPLACEHOLDER];
const KEY = "moscow-local-done-v1";
let done = new Set();
try { done = new Set(JSON.parse(localStorage.getItem(KEY) || "[]")); } catch(e) { done = new Set(); }

function fmtMin(m){
  if(m === 0) return "у дома";
  if(m < 1) return "меньше минуты";
  const n = Math.round(m);
  const m10=n%10, m100=n%100;
  let w = "минут";
  if(m10===1 && m100!==11) w="минута";
  else if(m10>=2&&m10<=4&&(m100<12||m100>14)) w="минуты";
  return n+" "+w;
}
function mapLink(ll){
  return "https://yandex.ru/maps/?pt=" + ll.join(",") + "&z=16";
}

const sections = document.getElementById("sections");
let total = 0;

GROUPS.forEach((g,gi)=>{
  const sec = document.createElement("section");
  const head = document.createElement("div");
  head.className = "cat-head";
  head.innerHTML = "<h2>" + g.cat + "</h2><span>" + g.items.length + "</span>";
  sec.appendChild(head);
  const grid = document.createElement("div");
  grid.className = "grid";
  g.items.forEach(it=>{
    total++;
    const id = gi + ":" + it.name;
    const el = document.createElement("div");
    el.className = "card" + (done.has(id) ? " visited" : "");
    el.innerHTML = '<span class="check">была</span>' +
      '<div class="name">' + it.name + '</div>' +
      '<div class="why">' + it.why + '</div>' +
      '<div class="walk">' + fmtMin(it.dist/80) + ' пешком · ' + it.dist + ' м</div>' +
      '<a class="maplink" target="_blank" rel="noopener" href="' + mapLink(it.ll) + '">на карте</a>';
    el.addEventListener("click", e=>{
      if(e.target.closest("a")) return;
      done.has(id) ? done.delete(id) : done.add(id);
      localStorage.setItem(KEY, JSON.stringify([...done]));
      el.classList.toggle("visited");
      renderCount();
    });
    grid.appendChild(el);
  });
  sec.appendChild(grid);
  sections.appendChild(sec);
});

function renderCount(){
  document.getElementById("count").textContent = done.size + " из " + total + " мест отмечено";
}
renderCount();

const map = L.map("map", {
  center: HOME, zoom: 14, zoomControl:false, attributionControl:false,
  dragging:false, scrollWheelZoom:false, touchZoom:false,
  doubleClickZoom:false, boxZoom:false, keyboard:false
});
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom:18 }).addTo(map);
L.circle(HOME, { radius:2400, color:"#2d5568", weight:1, dashArray:"6 5", fillColor:"#2d5568", fillOpacity:.05 }).addTo(map);
L.marker(HOME).addTo(map).bindPopup("<b>Дом</b> — Дубнинская 6к2");
GROUPS.forEach(g=>g.items.forEach(it=>{
  L.marker(it.ll).addTo(map).bindPopup("<b>" + it.name + "</b><br>" + it.why + "<br>" + fmtMin(it.dist/80) + " пешком");
}));
</script>
</body>
</html>
"""

html_doc = html_doc.replace("HOMEPLACEHOLDER", HOME_JS)
html_doc = html_doc.replace("GROUPSPLACEHOLDER", ", ".join(groups_js))

open(DST, "w", encoding="utf-8").write(html_doc)
print("written", DST, "with", sum(len(g) for g in spots.values()), "points")