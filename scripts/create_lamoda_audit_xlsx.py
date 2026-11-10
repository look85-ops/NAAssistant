from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from pathlib import Path

out=Path('wardrobe/2026-11-04_audit-lamoda-wishlist.xlsx')
rows=[
('Inni','Рубашка прямого силуэта из хлопка','рубашка','18 648','В наличии','хлопок 100%; вельвет; чёрный; прямой','заказать сейчас','https://www.lamoda.ru/p/mp002xw1m07e/clothes-inni-rubashka/'),
('Inni','Водолазка','водолазка','9 302','В наличии','шерсть 100%; трикотаж; зелёный; прямой','заказать сейчас','https://www.lamoda.ru/p/mp002xw1nwhz/clothes-inni-vodolazka/'),
('12 STOREEZ','Водолазка Uomo','водолазка','13 000','В наличии','мериносовая шерсть 100%; цвет/плотность уточнить','заказать сейчас','https://www.lamoda.ru/p/mp002xw1onrp/clothes-12storeez-vodolazka/'),
('Red September','Брюки широкие из хлопка','брюки','9 450','В наличии','хлопок 100%; широкие; размер 44/46 есть','заказать сейчас','https://www.lamoda.ru/p/mp002xw1k9o7/clothes-redseptember-bryuki/'),
('Dr. Martens','3 Eye Shoe','дерби','17 615','В наличии','чёрные; круглый нос; шнуровка','заказать сейчас','https://www.lamoda.ru/p/rtlaem555502/shoes-drmartens-botinki/'),
('Vittoria Vicci','Свитер','свитер','6 872','В наличии','шерсть 100%; трикотаж; бежевый','примерка','https://www.lamoda.ru/p/mp002xw0u9k0/clothes-vittoriavicci-sviter/'),
('Lusio','Джемпер Online Exclusive','джемпер','15 990','В наличии','шерсть енота 50%, нейлон 30%, шерсть 20%; красный','примерка','https://www.lamoda.ru/p/mp002xw1opid/clothes-lusio-dzhemper/'),
('Lusio','Джемпер','джемпер','10 633','В наличии','шерсть енота 50%, нейлон 30%, шерсть 20%','примерка','https://www.lamoda.ru/p/mp002xw0v0w8/clothes-lusio-dzhemper/'),
('Colmar','Худи','худи','8 160','В наличии','хлопок 52%, полиэстер 48%; толстовочный трикотаж','примерка','https://www.lamoda.ru/p/rtlaer014301/clothes-colmar-khudi/'),
('Charuel','Рубашка из хлопка','рубашка','7 495','В наличии','хлопок 100%; текстиль; плотность уточнить','примерка','https://www.lamoda.ru/p/mp002xw0v7zw/clothes-charuel-rubashka/'),
('Salamander','Ботильоны Полнота D (4)','ботильоны','11 279','В наличии','чёрные; острый нос; каблук стандартный','примерка','https://www.lamoda.ru/p/mp002xw1nq75/shoes-salamander-botilony/'),
('Carhartt WIP','Лонгслив Cardona Pocket T-Shirt','лонгслив','9 350','В наличии','хлопок 100%; трикотаж; цвет/плотность уточнить','примерка','https://www.lamoda.ru/p/rtlafs274801/clothes-carharttwip-longsliv/'),
('Lusio','Рубашка Online Exclusive','рубашка','10 000','В наличии','вискоза 35%, эластан 5%, полиэстер 60%','примерка','https://www.lamoda.ru/p/mp002xw1p2qf/clothes-lusio-rubashka/'),
('Pinko','Джемпер','джемпер','16 560','Нет в наличии','шерсть 100%','не брать','https://www.lamoda.ru/p/rtlafl983601/clothes-pinko-dzhemper/'),
('Annemore','Футболка из хлопка','футболка','2 280','В наличии','хлопок 93%, эластан 7%; молочный','не приоритет','https://www.lamoda.ru/p/mp002xw1mtd8/clothes-annemore-futbolka/'),
('Zolla','Футболка из хлопка','футболка','839','В наличии','хлопок 92%, эластан 8%; цвет/плотность уточнить','не приоритет','https://www.lamoda.ru/p/mp002xw1mvco/clothes-zolla-futbolka/'),
('Lime','Футболка из хлопка','футболка','999','В наличии','хлопок 100%; розовый','не приоритет','https://www.lamoda.ru/p/mp002xw1pbwe/clothes-lime-futbolka/'),]
wb=Workbook(); wb.remove(wb.active); blue='4472C4'; thin=Side(style='thin',color='B7C3D0')
def sheet(name,data):
 ws=wb.create_sheet(name); heads=['Бренд','Название','Категория','Цена, ₽','Наличие','Факты карточки','Решение','Ссылка']; ws.append(heads)
 for r in data: ws.append(r)
 for cell in ws[1]: cell.fill=PatternFill('solid',fgColor=blue); cell.font=Font(color='FFFFFF',bold=True); cell.alignment=Alignment(wrap_text=True)
 for row in ws.iter_rows():
  for c in row: c.border=Border(left=thin,right=thin,top=thin,bottom=thin); c.alignment=Alignment(wrap_text=True,vertical='top')
 for i in range(1,9): ws.column_dimensions[get_column_letter(i)].width=[18,34,18,12,16,55,18,65][i-1]
 ws.freeze_panes='A2'; return ws
sheet('Все избранное',rows); sheet('Основной вариант',[r for r in rows if r[6]=='заказать сейчас']); sheet('Альтернативный вариант',[r for r in rows if r[6]=='примерка']); sheet('На потом',[r for r in rows if r[6] in ('не брать','не приоритет')]); wb.save(out)
print(out)
