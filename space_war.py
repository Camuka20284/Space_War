#pgzero

# Oyunun temel ayarları
import random

WIDTH = 700  # Oyun penceresinin genişliği
HEIGHT = 450  # Oyun penceresinin yüksekliği

TITLE = "Uzay Yolculuğu"  # Oyun başlığı
FPS = 30  # Oyunun saniyedeki çerçeve sayısı

# Oyundaki değişkenler ve nesnelerin tanımlanması
gemi = Actor("gemi", (300, 400))  # Oyuncu gemisi
gemi1 = Actor("gemi1", (150, 200))  # Oyuncu gemisi seçenekleri
gemi2 = Actor("gemi2", (350, 200))
gemi3 = Actor("gemi3", (550, 200))
uzay = Actor("uzy")  # Uzay arka planı
dusmanlar = []  # Düşman gemileri listesi
gezegenler = [Actor("gezegen1", (random.randint(0, 600), -100)),
              Actor("gezegen2", (random.randint(0, 600), -100)),
              Actor("gezegen3", (random.randint(0, 600), -100))]  # Gezegenler
meteorlar = []  # Meteorlar
fuzeler = []  # Oyuncu tarafından ateşlenen füzeler
puan = 0  # Oyuncu puanı
mod = 'menü'  # Oyun modu ('menü', 'oyun', 'son')

# Düşman gemilerinin listesini oluştur
for i in range(7):
    x = random.randint(0, 600)
    y = random.randint(-450, -50)
    dusman = Actor("düşman", (x, y))
    dusman.speed = random.randint(2, 6)
    dusmanlar.append(dusman)

# Meteorların listesini oluştur
for i in range(5):
    x = random.randint(0, 600)
    y = random.randint(-450, -50)
    meteor = Actor("meteor", (x, y))
    meteor.speed = random.randint(2, 10)
    meteorlar.append(meteor)

# Oyun ekranının çizimi
def draw():
    # Oyun Modu
    if mod == 'oyun':
        uzay.draw()
        gezegenler[0].draw()
        # Meteorların çizimi
        for i in range(len(meteorlar)):
            meteorlar[i].draw()
        gemi.draw()
        # Düşman gemilerinin çizimi
        for i in range(len(dusmanlar)):
            dusmanlar[i].draw()
        for i in range(len(fuzeler)):
            fuzeler[i].draw()
        screen.draw.text(puan, center=(18, 24), color="white", fontsize=25)

    # Oyun Sonu ekranı
    elif mod == 'son':
        uzay.draw()
        screen.draw.text("OYUN BİTTİ!", center=(350, 200), color="white", fontsize=36)
        screen.draw.text(puan, center=(350, 260), color="white", fontsize=60)

    # Ana Menü ekranı
    elif mod == "menü":
        uzay.draw()
        gemi1.draw()
        gemi2.draw()
        gemi3.draw()
        screen.draw.text('GEMİNİZİ SEÇİNİZ', center=(350, 100), color="white", fontsize=36)

# Fare kontrolleri
def on_mouse_move(pos):
    gemi.pos = pos

# Yeni düşman gemilerinin eklenmesi
def yeni_dusman():
    x = random.randint(0, 400)
    y = -50
    dusman = Actor("düşman", (x, y))
    dusman.speed = random.randint(2, 8)
    dusmanlar.append(dusman)

# Düşman gemilerinin hareketi
def dusman_gemisi():
    for i in range(len(dusmanlar)):
        if dusmanlar[i].y < 650:
            dusmanlar[i].y = dusmanlar[i].y + dusmanlar[i].speed
        else:
            dusmanlar.pop(i)
            yeni_dusman()

# Gezegenlerin hareketi
def gezegen():
    if gezegenler[0].y < 550:
        gezegenler[0].y = gezegenler[0].y + 1
    else:
        gezegenler[0].y = -100
        gezegenler[0].x = random.randint(0, 600)
        birinci = gezegenler.pop(0)
        gezegenler.append(birinci)

# Meteorların hareketi
def meteorlar_hareket():
    for i in range(len(meteorlar)):
        if meteorlar[i].y < 450:
            meteorlar[i].y = meteorlar[i].y + meteorlar[i].speed
        else:
            meteorlar[i].x = random.randint(0, 600)
            meteorlar[i].y = -20
            meteorlar[i].speed = random.randint(2, 10)

# Çarpışma kontrolü
def carpismalar():
    global mod
    global puan
    for i in range(len(dusmanlar)):
        if gemi.colliderect(dusmanlar[i]):
            mod = 'son'
        for j in range(len(fuzeler)):
            if dusmanlar[i].colliderect(fuzeler[j]):
                dusmanlar.pop(i)
                fuzeler.pop(j)
                yeni_dusman()
                puan = puan + 1
                break

# Oyun güncelleme döngüsü
def update(dt):
    global mod
    if mod == 'oyun':
        dusman_gemisi()
        carpismalar()
        gezegen()
        meteorlar_hareket()

        for i in range(len(fuzeler)):
            if fuzeler[i].y < 0:
                fuzeler.pop(i)
                break
            else:
                fuzeler[i].y = fuzeler[i].y - 10

        if mod == "son" and keyboard.space:
            mod = "oyun"
            puan = 0
            for i in range(len(dusmanlar)):
                dusmanlar.pop(i)
            for j in range(len(meteorlar)):
                meteorlar.pop(j)
            for a in range(len(gezegenler)):
                gezegenler.pop(a)

# Fare tıklamaları
def on_mouse_down(button, pos):
    global mod
    if mod == "menü" and gemi1.collidepoint(pos):
        gemi.image = "gemi1"
        mod = "oyun"
    elif mod == "menü" and gemi2.collidepoint(pos):
        gemi.image = "gemi2"
        mod = "oyun"
    elif mod == "menü" and gemi3.collidepoint(pos):
        gemi.image = "gemi3"
        mod = "oyun"

    if mod == "oyun" and button == mouse.LEFT:
        fuze = Actor("füzeler")
        fuze.pos = gemi.pos
        fuzeler.append(fuze)
