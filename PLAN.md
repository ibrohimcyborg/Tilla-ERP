# PLAN.md — Dona bazaga to'liq o'tish rejasi

> Bu fayl — **kelajak ish ro'yxati**. Ertaga ochib o'qiganda nima qilish
> kerakligi shu yerdan ko'rinadi. Joriy holat esa DAVOM.md da.

**Yozilgan:** v172.13 · 2026-08-05

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

## Eslatmalar

- X1–X7 tafsiloti bilan: `mockups/v172.13-dona-baza-tushuntirish.html`
  (mockup o'chirilgan bo'lsa — shu fayldagi ro'yxat yetarli)
- Chernovik rejimi kiritilgan mockup: `mockups/v172.13-dona-baza-chiqarish.html`
- Bayroqni yoqishdan oldin BU FAYLNING 1-qadami to'liq yashil bo'lishi shart
