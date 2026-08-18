# PLAN.md — kelajak ishlar rejasi

> Bu fayl — **kelajak ish ro'yxati**. Ertaga ochib o'qiganda nima qilish
> kerakligi shu yerdan ko'rinadi. Joriy holat esa DAVOM.md da.

**Yozilgan:** v172.13 · 2026-08-05
**Oxirgi qo'shimcha:** v176 Telegram rejasi · 2026-08-16

Ichida uchta mustaqil reja bor:
1. **Dona bazaga to'liq o'tish** — X1–X7, qaytadan shakllantirish, bayroq
2. **«Qo'limizdagi ostatka» C bosqichi** — dushanba skan langari
3. **Telegram qarz eslatmasi** — v176, ikki bosqich

---

## Hozirgi holat (v172.13 dan)

Dona baza **CHERNOVIK rejimida** — Ibrohim qarori:
qopcha (gramm) hisobi asosiy, dona baza to'liq shakllanmaguncha ishga aralashmaydi.

- Bayroq: `index.html` da `var DONA_BAZA_UI = false;` (APP_VER yonida)
- Ko'rinmaydi: «N dona» yozuvi (BIZDA ostida), DONA BAZASI paneli,
  🗄 Dona baza tugmasi, «dona ro'yxatda yo'q» ogohlantirishlari
- Muzlatilgan: bazaga yozish, holat o'zgartirish, ombor o'chirish,
  cloud'dan quyish — hammasi bayroq bilan to'xtatilgan
- Ma'lumot **joyida**: `localStorage['tilla-dona-baza']` + Firestore `_donabaza/items`
- Gramm hisobi, qarz, kassa, chek — bunga umuman bog'lanmagan, ishlayveradi

---

## TO'LIQ O'TISHDA QILINADIGAN ISHLAR — tartib bilan

### 1-qadam. Kod xatolarini tuzatish (bayroq yoqishdan OLDIN)

Bular tuzatilmasa baza yana yolg'on ko'rsatadi. Har biri alohida versiya bo'lishi mumkin.

- [ ] **X1 — Klientdan vozvratda dona bazasi omborga qaytmaydi** (3 joy:
      12431, 13617, 15394 atrofi — qator raqamlari eskiradi, `donaRegQosh` bilan qayta top).
      Vozvrat saqlanganda `donaBazaHolat(..., 'ombor')` ga o'xshash qaytarish kerak —
      LEKIN `donaBazaHolat` faqat `ombor→boshqa` yo'nalishda ishlaydi, teskari yo'l yozilishi kerak.
- [ ] **X2 — Ostatka TEKSHIRUV dona bazasini yangilamaydi** (shakl rejimi yangilaydi,
      tekshiruv rejimi yo'q — 8196 atrofi `else c.t.donalar = p1.slice()`).
- [ ] **X3 — 🔧 «Ostatkani qayta tiklash» uch sanoqni uzadi** (`ostatkaHisobla` faqat
      ostatka+donaOst ni yozadi, `t.donalar` va dona bazaga tegmaydi — 8727 atrofi).
- [ ] **X4 — `ostatkaHisobla` da vozvrat donasi `d += op.dona`** (8685 atrofi) —
      ehtimol `-=` bo'lishi kerak. ATAYLABMI-XATOMI ANIQLANMAGAN — Ibrohim bilan ko'rib chiqiladi.
- [ ] **X5 — 🕐 Vaqt mashinasi dona bazasini tiklamaydi** (`snapSaqla` faqat `data` ni oladi,
      `tilla-dona-baza` ni olmaydi — 8812 atrofi). Snapshot'ga dona bazani ham qo'shish kerak.
- [ ] **X6 — Qo'lda gramm yozilganda baza jimgina orqada qoladi** — to'liq o'tishda
      qoida kerak: yo hamma berish/sotuv skan bilan, yo qo'lda yozish uchun alohida yechim.
- [ ] **X7 — `sotilgan` va `yoqolgan` holatlar hech qachon qo'yilmaydi** — sotuv ham
      `berilgan` deb yozadi (CLAUDE.md §10 dagi «sotuv belgilanmaydi» muammosi bilan bog'liq).
- [ ] **Nom bilan bog'lanish tuzog'i** — baza zavod/turga NOM MATNI bilan bog'lanadi.
      Eski nom bilan yangi zavod/tur ochilsa eski yozuvlar yopishadi. To'liq o'tishdan
      oldin eski `berilgan`/`vozvrat` chernovik yozuvlarini tozalash yo'li kerak
      (hozir ularni hech narsa o'chira olmaydi).

### 2-qadam. Bazani qaytadan shakllantirish

- [ ] Chernovikdagi eski yozuvlarni tozalash (1-qadamdagi tozalash yo'li bilan)
- [ ] Har zavod·turni **skan bilan** qaytadan shakllantirish — chernovik davrida
      baza yangilanmagani uchun eski yozuvlarga ishonib bo'lmaydi
- [ ] Klientlardagi donalarni qanday kiritish — hal qilinmagan, Ibrohim bilan

### 3-qadam. Yoqish

- [ ] `DONA_BAZA_UI = true`
- [ ] 1340-qatordagi 🗄 tugmadan `display:none;` ni olish (hamid-x qator — §6, ruxsat bilan)
- [ ] TEST rejimida sinov: skan kirim → berish → vozvrat → tekshiruv zanjiri
- [ ] Sinov davri: ogohlantirishlar haqiqiy ishda to'g'ri chiqayaptimi kuzatiladi

---

## «Qo'limizdagi ostatka» — C bosqich: dushanba skan langari (KELAJAK)

> Ibrohim qarori (2026-08-05): avval B qilinadi (hafta boshi TARIXDAN
> hisoblanadi, saqlangan `t.ostatka` ga qaralmaydi — v172.14).
> Keyin C ga o'tiladi.

C nima: har dushanba jismoniy skan natijasi «haftaning rasmiy boshi»
sifatida SAQLANADI va hisob shu langar-nuqtadan yuradi. Shunda hisob
tarixga ham emas, haqiqiy sanoqqa bog'lanadi.

C uchun qilinadigan ishlar:
- [ ] Langar yozuvi qayerda saqlanishi (yangi struktura: zavod·tur·hafta → gramm)
- [ ] Dushanba skan oqimi bilan bog'lash — skan yakunida «hafta langari
      sifatida saqlansinmi?» qadami
- [ ] `qoldData` da langar bor haftalar langar­dan, yo'q haftalar B usulida
      (tarixdan) hisoblanishi
- [ ] Langar bilan tarix orasida farq chiqsa — farqni ko'rsatish
      (qayerda yozuv yetishmasligini topish vositasi)
- [ ] Cloud sinxron: langar yozuvlari boshqa qurilmalarga ham borishi

---

## TELEGRAM — qarz eslatmasi (v176, KELAJAK)

**Yozilgan:** 2026-08-16 · mockup: `mockups/v176-telegram-C-avtomat.html`
(uch variant solishtiruvi: `mockups/v176-telegram-ogohlantirish.html`)

Ibrohim: klient telefonini qo'shib, **muddati 10 kun** bo'lgan klientga
Telegramdan chiroyli ogohlantirish yuborilsin.

### Tanlangan yo'l: **C — o'z hisobidan avtomat (botsiz)**

Ibrohim **A** (qo'lda) va **B** (bot) ni rad etdi, **C** ni tanladi.
Sababi: bot uchun klient bir marta «Start» bosishi kerak, u kerak emas.

⚠ **Xavf ochiq aytilgan va Ibrohim qabul qilgan:** Telegram o'z hisobidan
avtomat xabar yuborishni taqiqlaydi, hisob bloklanishi mumkin. Ibrohim:
«Block bo'maydi chunki profil Premium keyin klient bilan gaplashib turamiz».
Premium himoya EMAS (limitni oshiradi, avtomatga ruxsat bermaydi) — bu
aytilgan. Haqiqiy himoya — **mavjud suhbat**, u 1-qoidaga aylantirildi.

### Kodda ALLAQACHON bor (noldan boshlanmaydi)

| Nima | Qayerda |
|---|---|
| Klient telefoni `k.tel` | 11969 («+ Tel qo'shish») |
| «Necha kun» `klientQarzHolat` | 9656 — oxirgi to'lov/vozvratdan beri |
| Qarz raqami `klientJamiQarz` | 9670 (v175.2 dan yagona manba) |
| Qarz tarkibi `_qarzTarkibRows` | 16676 |
| **Navbat qolipi** | `_cheknavbat` (2036, 2136) — AYNAN shu nusxalanadi |
| **PC dasturi qolipi** | `print_server.py` (stdlib `http.server`) |

Shart: `klientQarzHolat(k).kun >= 10 && klientJamiQarz(k) > 0`

### Arxitektura — chek printeri bilan bir xil

```
Ilova  ->  bulut navbati  ->  PC dasturi  ->  Telegram
         (_tgnavbat)        (tg_server.py)
```

Bulut orqali bo'lgani uchun **telefondan ham** ishga tushiriladi.

### Yangi fayllar

- `tg_server.py` — PC da, `print_server.py` yonida. Telethon (MTProto).
- `tg_session.dat` — Telegram kaliti. ⚠ **`.gitignore` ga SHART** — repo OCHIQ.

### 1-BOSQICH — ilova tomoni (~120 qator)

- [ ] Yangi ekran: «Qarz eslatmalari» — 10+ kun, qarzi bor klientlar ro'yxati
- [ ] Har qatorda: nom, kun, qarz, telefon, «suhbat bor/yo'q» belgisi
- [ ] Telefoni yo'q / suhbati yo'q / yaqinda eslatilgan — kulrang, yuborilmaydi
- [ ] ~~Belgilash + tugma~~ — Ibrohim **avtomat** yuborishni tanladi (javob 2).
      Ro'yxat ekrani baribir kerak: **ko'rish va nazorat** uchun, lekin yuborish
      uchun tugma bosilmaydi.
- [ ] Nomzodlar ro'yxatini bulutga yozish (ilova har ochilganda) — arxitektura
      savoli javobidan keyin («IBROHIM JAVOBLARI» 2-bandiga qara)
- [ ] Xabar matni sozlamada tahrirlanadigan qolip bo'lsin

### 2-BOSQICH — PC dasturi (~180 qator)

- [ ] `tg_server.py`: Firestore `_tgnavbat` ni tinglaydi
- [ ] Telethon bilan yuboradi, natijani navbatga qaytaradi (bajarildi/xato)
- [ ] Bir martalik login oqimi (telefon + kod -> `tg_session.dat`)

### XAVFSIZLIK QOIDALARI — kodga yoziladi, beshtasi ham

1. [ ] **Faqat suhbati bor klientga** — eng muhimi, `get_dialogs` bilan tekshiriladi
2. [ ] **40–60 soniyada bitta** — ketma-ket tez yuborish robotni bildiradi
3. [ ] **Kuniga 20 ta** chegara — oshsa ertaga davom etadi
4. [ ] **Bir klientga 7 kunda bir marta** — takror yo'q
5. [ ] **Faqat 09:00–19:00** — kechasi yuborilgan xabar shubha uyg'otadi

### IBROHIM JAVOBLARI (2026-08-16)

**1. «10 kun» — OXIRGI JARAYONDAN.** Ibrohim: «10kun oxirgi jarayondan kegin
pul berishi ostatkaga yoki mol ogandan kegin ostatkaga». Ya'ni sanoq
**har qanday amaldan** qayta boshlanadi: **to'lov** ham, **mol olish (berish)**
ham hisoblanadi.

⚠ **Bu mavjud kodni O'ZGARTIRADI.** `klientQarzHolat` (9656) hozir faqat
`vozvrat`/`tolov` ni qaraydi, `berish` esa **faqat zaxira** sifatida ishlatiladi
(agar umuman to'lov bo'lmagan bo'lsa):

```
hozir:  if(op.tip==='vozvrat' || op.tip==='tolov')     <- berish HISOBLANMAYDI
kerak:  if(op.tip==='vozvrat' || op.tip==='tolov' || op.tip==='berish')
```

⚠⚠ **Bu Telegramdan tashqari joylarga ham tegadi.** `klientQarzHolat` uch
joyda ishlatiladi va hammasida «N kun» yorlig'i va rangi (yashil/sariq/qizil)
o'zgaradi:
* **11471** — klientlar ro'yxatidagi yorliq
* **11486** — «qizil» (qarzdorlar) ro'yxati va uning tartibi
* **11722** — klient kartasi

Kod yozishdan oldin Ibrohimga **ko'rsatib tasdiqlatish** kerak: mol olgan kun
sanoqni qayta boshlagani uchun ko'p klient birdan «yashil» bo'lib qolishi mumkin.

**2. O'ZI YUBORADI.** Ibrohim tugma bosmaydi — belgilangan soatda avtomat.

⚠ **Bu arxitekturaga ta'sir qiladi — HAL QILINMAGAN.** Kim «kim 10 kun
o'tgan» ro'yxatini hisoblaydi?
* Ilova hisoblasa — ilova **yopiq** bo'lsa ro'yxat eskirib qoladi
* PC dasturi hisoblasa — butun qarz mantiqini **Pythonda qaytadan yozish**
  kerak bo'ladi. Bu v175 da endigina yopgan «yagona manba» qoidasini buzadi
  (bir hisob ikki tilda → ikki xil raqam).

Taklif (tasdiqlanmagan): **ilova har ochilganda/saqlanganda** nomzodlar
ro'yxatini `_tgnavbat` yoniga yozib qo'yadi, PC dasturi esa faqat **yuboradi**
va hisoblamaydi. Ibrohim ilovani har kuni ochgani uchun ro'yxat yangi qoladi.
⚠ Ilova bir necha kun ochilmasa eslatma ham yuborilmaydi — bu qabul qilinadimi?

**3. Xabar matni** — Ibrohim: «matnni ko'ramiz». Keyinroq hal qilinadi,
mockupdagi namuna boshlang'ich nuqta.

### Sozlash — Ibrohim bir marta qiladi (~10 daqiqa)

1. `my.telegram.org` dan API kaliti (bepul)
2. `pip install telethon`
3. Skriptni ishga tushirib telefon + Telegram kodi bilan kirish
4. `tg_server.py` ni `print_server.py` kabi yoqib qo'yish

⚠ PC yoqiq bo'lmasa ishlamaydi — chek printeri bilan bir xil cheklov.

---

## Eslatmalar

- X1–X7 tafsiloti bilan: `mockups/v172.13-dona-baza-tushuntirish.html`
  (mockup o'chirilgan bo'lsa — shu fayldagi ro'yxat yetarli)
- Chernovik rejimi kiritilgan mockup: `mockups/v172.13-dona-baza-chiqarish.html`
- Bayroqni yoqishdan oldin BU FAYLNING 1-qadami to'liq yashil bo'lishi shart
