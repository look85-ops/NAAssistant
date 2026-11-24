import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MINSK = ROOT / "projects/minsk-map"


def extract_array(text: str, varname: str):
    m = re.search(rf"const\s+{re.escape(varname)}\s*=\s*", text)
    if not m:
        raise ValueError(f"{varname} not found")
    i = text.index("[", m.end())
    depth = 0
    j = i
    quote = None
    esc = False
    while j < len(text):
        ch = text[j]
        if quote:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                quote = None
        else:
            if ch in "'\"`":
                quote = ch
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    break
        j += 1
    return ast.literal_eval(text[i:j + 1])


def load(path: Path):
    return path.read_text(encoding="utf-8")


teplo_items = extract_array(load(MINSK / "teplo-vnutri.html"), "cards")
minsk_items = extract_array(load(MINSK / "cards-enhanced-cover-route.html"), "cards")
povody_src = extract_array(load(MINSK / "cards-moscow.html"), "sourceCards")
povody_order = extract_array(load(MINSK / "cards-moscow.html"), "cards")
povody_items = [povody_src[i] for i in povody_order]

OUT = ROOT / "projects/naoborot/print"
OUT.mkdir(parents=True, exist_ok=True)

DECKS = {
    "teplo": {
        "items": teplo_items, "kind": "state", "label": "Тепло внутри",
        "tw": 148, "th": 105, "sw": 138, "sh": 95, "pw": 164, "ph": 121,
    },
    "minsk": {
        "items": minsk_items, "kind": "route", "label": "Минск, который станет нашим",
        "tw": 105, "th": 148, "sw": 95, "sh": 138, "pw": 121, "ph": 164,
    },
    "povody": {
        "items": povody_items, "kind": "route", "label": "Приятные поводы",
        "tw": 105, "th": 148, "sw": 95, "sh": 138, "pw": 121, "ph": 164,
    },
}

HTML = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><title>__LABEL__ — A6</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Manrope:wght@400;500;600&display=swap');
:root{--wine:#641f2c;--deep:#42131d;--acid:#d9e85c;--paper:#f4f0e8;--white:#fffdf8;--ink:#211b18;--muted:#6f655c;--display:"DM Sans",Arial,sans-serif;--sans:Manrope,Arial,sans-serif;
--pw:__PW__mm;--ph:__PH__mm;--tw:__TW__mm;--th:__TH__mm;--sw:__SW__mm;--sh:__SH__mm}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{margin:0;background:#ddd;font-family:var(--sans);color:var(--ink)}
.page{position:relative;width:var(--pw);height:var(--ph);background:#fff;page-break-after:always;overflow:hidden;margin:0 auto}
.page:last-child{page-break-after:auto}
.trim{position:absolute;left:8mm;top:8mm;width:var(--tw);height:var(--th);overflow:hidden}
.front .trim{background:var(--wine);color:var(--paper)}
.back .trim{background:var(--white);color:var(--ink);box-shadow:inset 0 0 0 0.2mm rgba(33,27,24,.12)}
.safe{position:absolute;left:13mm;top:13mm;width:var(--sw);height:var(--sh);display:flex;flex-direction:column}
.front .safe{justify-content:flex-end}
.cat{font-size:6.5pt;letter-spacing:.14em;text-transform:uppercase;opacity:.7;margin-bottom:auto}
h1{margin:0 0 2mm;font:600 17pt/.98 var(--display);letter-spacing:-.03em;text-wrap:balance;max-width:100%}
.mood{font-size:7.5pt;line-height:1.35;margin:0;opacity:.82;max-width:100%}
h2{margin:0 0 2mm;font:600 12pt/1.05 var(--display);letter-spacing:-.02em;text-wrap:balance}
.body{font-size:7.4pt;line-height:1.38;color:#3b332b;text-wrap:pretty}
.body p{margin:0 0 1.6mm}
.sparkle{color:var(--wine);font-size:11pt;margin-bottom:3mm}
.meta{margin:2.5mm 0 0;font-size:7pt;line-height:1.35;color:var(--muted)}
.meta dt{font-size:5.8pt;letter-spacing:.1em;text-transform:uppercase;color:var(--wine);margin-top:1.6mm}
.meta dd{margin:0.4mm 0 0;color:var(--ink)}
.rec{margin-top:auto;padding-top:2.5mm;border-top:0.2mm solid rgba(33,27,24,.18);font-size:7pt;line-height:1.35;color:var(--wine)}
.rec b{display:block;font-size:5.8pt;letter-spacing:.1em;text-transform:uppercase;margin-bottom:0.6mm}
.mark{position:absolute;background:var(--ink)}
@page{size:var(--pw) var(--ph);margin:0}
@media print{html,body{background:#fff}.page{margin:0}}
</style></head><body><main id="pages"></main>
<script>
const DATA = __DATA__;
const KIND = "__KIND__";
const TW = __TW__, TH = __TH__;
const re = /\\s+(в|во|и|а|но|к|ко|с|со|у|о|об|от|до|из|на|по|за|для|без|над|под|при|про|не|что|как|же)\\s+/gi;
const t = s => String(s == null ? '' : s).replace(re, ' $1\\u00A0');
const el = (tag, cls, html) => { const n=document.createElement(tag); if(cls)n.className=cls; if(html!=null)n.innerHTML=html; return n; };
const pages = document.getElementById('pages');
function marks(){
  const m = el('div','marks');
  const pos = [[8,8,'h'],[8,8,'v'],[8+TW,8,'h'],[8+TW,8,'v'],[8,8+TH,'h'],[8,8+TH,'v'],[8+TW,8+TH,'h'],[8+TW,8+TH,'v']];
  pos.forEach(([x,y,dir])=>{
    const line = el('div','mark');
    if(dir==='h'){ line.style.cssText += `left:${x-4}mm;top:${y}mm;width:4mm;height:0.2mm`; }
    else { line.style.cssText += `left:${x}mm;top:${y-4}mm;width:0.2mm;height:4mm`; }
    m.appendChild(line);
  });
  return m;
}
DATA.forEach((c) => {
  const front = el('section','page front');
  const trimF = el('div','trim');
  const safeF = el('div','safe');
  if (KIND === 'state') {
    safeF.appendChild(el('div','cat','зима · открытка'));
    safeF.appendChild(el('h1', null, t(c[0])));
    safeF.appendChild(el('p','mood', ''));
  } else {
    safeF.appendChild(el('div','cat', t(c[1])));
    safeF.appendChild(el('h1', null, t(c[0])));
    safeF.appendChild(el('p','mood', t(c[7])));
  }
  trimF.appendChild(safeF); front.appendChild(trimF); front.appendChild(marks()); pages.appendChild(front);

  const back = el('section','page back');
  const trimB = el('div','trim');
  const safeB = el('div','safe');
  safeB.appendChild(el('div','sparkle','✦'));
  safeB.appendChild(el('h2', null, t(c[0])));
  if (KIND === 'state') {
    const body = el('div','body');
    String(c[1]).split(/\\n+/).filter(Boolean).forEach(p => body.appendChild(el('p', null, t(p))));
    safeB.appendChild(body);
    safeB.appendChild(el('div','rec', `<b>Рекомендация</b>${t(c[2])}`));
  } else {
    const meta = el('dl','meta');
    const rows = [['Куда', c[2]], ['Остановки', c[5]], ['Ритм', c[3]]];
    rows.forEach(([k,v]) => { if(v){ meta.appendChild(el('dt', null, k)); meta.appendChild(el('dd', null, t(v))); } });
    safeB.appendChild(meta);
    safeB.appendChild(el('div','rec', `<b>Саундтрек</b>${t(c[6])}`));
  }
  trimB.appendChild(safeB); back.appendChild(trimB); back.appendChild(marks()); pages.appendChild(back);
});
</script></body></html>"""

for key, deck in DECKS.items():
    html = (HTML
            .replace("__LABEL__", deck["label"])
            .replace("__DATA__", json.dumps(deck["items"], ensure_ascii=False))
            .replace("__KIND__", deck["kind"])
            .replace("__PW__", str(deck["pw"])).replace("__PH__", str(deck["ph"]))
            .replace("__TW__", str(deck["tw"])).replace("__TH__", str(deck["th"]))
            .replace("__SW__", str(deck["sw"])).replace("__SH__", str(deck["sh"])))
    out = OUT / f"a6-{key}.html"
    out.write_text(html, encoding="utf-8")
    print(f"{out.name}: {len(deck['items'])} cards -> {len(deck['items'])*2} pages ({deck['tw']}x{deck['th']} trim)")
