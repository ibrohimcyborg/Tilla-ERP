# DAVOM.md — qayerdan davom etamiz

> Bu fayl **har seans boshida o'qiladi**. Ish qoidalari CLAUDE.md da.
> Har versiyadan keyin bu fayl **yangilanadi** — aks holda keyingi seans
> nimadan davom etishini bilmaydi.

**Oxirgi yangilanish:** v179.11 · POS 1.33 · 2026-09-05

---

## ✅ v179.6 — klient PDF hisoboti 500 berardi

**Ibrohim:** «klientga kirsam pdf hisobotini olmoqchi bosam» — `/api/pdf.py 500`.

**Sabab:** klient tarixida bitta yozuvda `gramm` yo'q → `runBal += undefined`
→ NaN → o'sha klientning hamma qatoridagi ostatka NaN → JSON da `null`
→ `pdf.py` da `None < -0.001` → TypeError → 500.
`.get('ostatka', 0)` yordam bermaydi: Python'da standart qiymat faqat kalit
**yo'q** bo'lganda ishlaydi, `null` bo'lganda emas.

**Qilindi:** `index.html:18306` — gramm o'qilmasa 0 olinadi, `runBal` NaN
bo'lmaydi. `api/pdf.py` — `_num()` yordamchisi, faqat `build_klient_tarix`
ichida (8 joyda).

**Abdulhamid:** tegilmadi — uning oltita sharti va `hamid-x` dan tashqarida.
⌘ PDF tugmasida (811) `hamid-x` yo'q, ya'ni u ham shu 500 ni olardi; endi ochadi.

**Hisob-kitobga ta'sir yo'q:** `klientPDFYukor` hech narsa yozmaydi — na
`save()`, na cloud, na `localStorage`, na `data.klientlar`. Chizilgan 44 ta
matn eski kod bilan solishtirildi — hammasi bir xil.

### ⚠ Aytildi, tegilmadi — Ibrohim so'ramadi

1. «Hamma klientlar» hisobotida (18658 `bal += op.gramm`) **aynan shu xato bor**.
2. `pdf.py` dagi qolgan 4 hisobot turi ham `.get(k, 0)` bilan himoyasiz.
3. index.html 11154 `tip:'tolov_hisobot'` — `pdf.py` da bu tip uchun **shox yo'q**.
4. Buzuq yozuvni PDF da **belgilash** (qizil «?») — Ibrohim aytgan edi,
   alohida qadam sifatida qoldirildi.
5. Qaysi yozuv buzuq ekani **hali topilmagan**.

---

## 🟢 POS NI AJRATISH — QAROR QABUL QILINDI (2026-09-05)

**Ibrohim:** *«shunaqa qilsak manimcha to'g'riroq bo'ladi — Tilla ERP dan chiqaradi,
cloud bilan ulanadigan bo'ladi, alohida loginli qilamiz, test qilib testda
hammasini hal qilvoganimizdan keyin adminga ulaymiz»*.

Avvalgi qaror (2026-08-23: «2 ni qilaqolilik» — keyinga qoldirish) BEKOR QILINDI.

### O'lchangan holat (2026-09-05, v179.6)

| | |
|---|---|
| POS kodi jami | 66 funksiya, **~837 qator** |
| Kassir tomoni → `pos.html` | ~50 funksiya, **~560 qator** |
| Admin tomoni → `index.html` da QOLADI | ~18 funksiya, ~277 qator (qo'ng'iroqcha, chernovik, `posChQabul`) |
| **`hisob.js`** — yangi, ikkalasi yuklaydi | **15 funksiya, ~158 qator** |

### `hisob.js` tarkibi — O'LCHANGAN, yopiq

Tranzitiv bog'liqlik hisoblandi: 13 urug'dan faqat `_ostDelta` va `turOstMap`
ergashdi. **Cloud qatlami ergashmadi.**

| Guruh | Funksiyalar |
|---|---|
| Mayda | `parseNum` (2464) `fmtG` (2465) `fmtD` (2466) `today` (2468) `roundG` (2469) |
| Ombor | `_ostDelta` (7452) `turOstMap` (7470) `turOst` (7493) |
| Qarz | `klientJamiQarz` (9803) `klientJamiSavdo` (9841) `_qarzJamiRows` (17993) `_qarzTarkibRows` (18006) `_qarzTarkib` (18068) |
| Narx | `getKatNarx` (15791) `getZavodNarx` (15812) |

⚠ **NUSXALANMAYDI — KO'CHIRILADI.** Qarz funksiyalari nusxalansa raqamlar
ajraladi: v177.4 da aynan shu bo'lgan (POS `+557.46`, ilova `559.58`).

✅ **Dona baza va cloud `hisob.js` ga KERAK EMAS** — o'lchandi: `donaBazaOlish`,
`donaRegQosh`, `donaRegOlish`, `saqlashKlientVozvrat`, `davomEt`, `turDona`
faqat `posChQabul` dan chaqiriladi, u esa admin tomonida qoladi.

### ⚠ VERCEL XAVFI — 1-qadamda hal qilinadi

`vercel.json` da:
```
{ "source": "/((?!api).*)", "destination": "/index.html" }
```
Bu `api` dan boshqa HAMMA yo'lni `index.html` ga buradi. Vercel odatda avval
haqiqiy faylni qidiradi (ya'ni ishlashi kerak), lekin kafolat yo'q — `pos.html`
ochilmay, o'rniga Tilla ERP chiqib qolishi mumkin. Yechim: naqshga `pos.html`
va `hisob.js` istisnosi qo'shiladi.

### Qadamlar

| | Qadam | Xavf | Holat |
|---|---|---|---|
| 1 | `hisob.js` ajratish + `vercel.json` istisnosi | ⚠ eng xavfli — ERP buzilmasin | **BOSHLANMAGAN** |
| 2 | `pos.html` qobig'i: alohida login, Firebase, cloud o'qish | past | — |
| 3 | Kassir ekranlarini ko'chirish (~560 qator) | past | — |
| 4 | `index.html` dan kassir kodini o'chirish | o'rta | — |
| 5 | Sinov: `kassatest` → `pos.html` → chernovik → `test` da qabul | — | — |

**1-qadamdan keyin TO'XTALADI** — Ibrohim ERP ni ochib tekshiradi.
Sinov TEST bazasida; hammasi hal bo'lgach admin (haqiqiy) bazaga ulanadi.

---

## 🔴 UCHTA YANGI VAZIFA (Ibrohim, 2026-09-05)

### 1. Yakunlangan chekni tahrirlashda TURNI ham almashtirish

Hozir tahrirlash oynasida faqat GRAMM o'zgartiriladi. Ammo xato ko'pincha
grammda emas, **TURDA** bo'ladi.

Haqiqiy holat: «Diamond · Polimer» da 8.49 g vozvrat qilingan, dasturga
«Diamond · Oddiy» bo'lib yozilgan. Grammni tuzatish yordam bermaydi.

**Ibrohim qarorlari:**
- Tur ro'yxatdan tanlanadi, gramm avvalgidek o'zgartiriladi
- Qatorni o'chirish qolsin (hozir gramm bo'shatilsa o'chadi)
- Bir xil tur chiqib qolsa — **QO'SHILIB ketsin**
- Tahrirlangani **BILINIB TURSIN** — masalan «Oddiy -> Polimer, 05.09 14:20»
- **Butun chekni o'chirish KERAK EMAS**, faqat ichidagi qatorlar. Chek allaqachon
  chiqib ketgan bo'ladi, keyin mijoz bilan tuzatib yangi chek chiqariladi

### 2. Sinxronizatsiya — o'zgarish boshqa qurilmaga o'tmaydi

Bir qurilmada tahrirlangandan keyin, ikkinchi qurilmada **eski holida qoladi**.
Faqat asosiy qurilmadan cloud yuborilib, qolgani qabul qilgandagina o'zgaradi —
ya'ni **avtomatik emas**. (Bog'liq: «0k. CLOUD 1:1 — 3-QADAM» va «0j. Kassa
qurilmalar orasida SINXRON EMAS».)

### ✅ 3. PDF 500 — SANA TANLANGANDA — BAJARILDI (v179.7)

`/api/pdf.py` 500 beradi — hisobot **sana tanlab** chiqarilganda.
v179.6 da «grammi yo'q yozuv» tuzatilgan, demak sana tanlanganda **boshqa yo'l**
ochilyapti. Shubha: `_pdfTip` dispecheri (9821 atrofida) va «hamma klientlar»
hisoboti (18658 `bal += op.gramm` — himoyasiz, v179.6 da TEGILMAGAN).

**Topildi:** «hamma klientlar» hisoboti (18610 `bal += op.gramm`) — v179.6 da
TEGILMAGAN edi, ildizi klient detalidagi bilan aynan bir xil.

**Qilindi (v179.7):** `index.html:18610–18620` himoyalandi; `api/pdf.py` da `_num()`
**oltita hisobot quruvchisining hammasiga** qo'llandi. Sinov `build_pdf` da yana
to'rtta yashirin yiqilish yo'lini topdi — ular ham yopildi.

Endi oltita hisobot turi ham `null` bilan chaqirilganda yiqilmaydi (o'lchandi).
To'g'ri ma'lumotli hisobotlar o'zgarmadi — chizilgan matnlar eski kod bilan
solishtirildi, hammasi bir xil.

ℹ Alohida narsa, xato emas: `localhost:5000/print ERR_CONNECTION_REFUSED` —
printer serveri o'chiq edi.

### ✅ PDF 500 — TO'LIQ YOPILDI (Ibrohim tasdiqladi, 2026-09-05)

Uch bosqichda hal bo'ldi, har biri BOSHQA sabab edi:

| Versiya | Sabab | Holat |
|---|---|---|
| v179.6 | klient detalida grammi yo'q yozuv → NaN → null | tuzatildi |
| v179.7 | o'sha xato «hamma klientlar» hisobotida ham + `pdf.py` da 6 ta quruvchi himoyasiz | tuzatildi |
| v179.8 | ⚠ v179.6 da O'ZIM kiritgan rang xatosi (qarz tarkibi hammasi qizil) | tuzatildi |
| v179.9 | `SPAN` kvadratik → katta klientda 10 s dan oshardi | jadval bo'laklarga bo'lindi + `maxDuration` 60 s |
| v179.10 | xato matni ko'rinmasdi — `'Server xatosi'` deb almashtirilardi | `_pdfJavob()` haqiqiy sababni ko'rsatadi |
| v179.11 | **haqiqiy sabab**: baland ostatka bloki sahifaga sig'masdi | blok kunlar bo'yicha bo'linadi |

**Ibrohim tasdiqladi:** «hozircha ishlavotti, 33,1 kb pdf».

⚠ DARS: v179.10 gacha xato matni ko'rinmagani uchun uch marta noto'g'ri
yo'ldan borildi. Xato ko'rinadigan bo'lgach sabab bir urinishda topildi.

⚠ DARS 2: v179.6/v179.7 regressiya sinovi faqat MATNNI solishtirardi va
o'zim kiritgan rang xatosini o'tkazib yubordi. Endi sinov matn bilan birga
RANGNI ham solishtiradi (`rang.py` naqshi).

### Qolgan ikkitasi — BOSHLANMAGAN

1-vazifa (chekni tahrirlashda TURNI almashtirish) va 2-vazifa (sinxronizatsiya)
hali qo'lga olinmadi.

---

## Hozirgi holat

| | |
|---|---|
| Versiya | **`APP_VER v179.11`** · **`POS_VER 1.33`**. POS ishida faqat `POS_VER` o'sadi; v179 — POS dan TASHQARIDAGI o'zgarish (cloud sozlamalari), shuning uchun `APP_VER` o'sdi. Qoida: CLAUDE.md §5 |
| Hajm | ~19,418 qator · ~1 MB · **~311k token** |
| Deploy | tilla-erp.vercel.app (GitHub: ibrohimcyborg) |
| Saqlash | localStorage `tilla-v2` + Firebase Firestore `tilla_<uid>` |
| Sinov | **TEST rejimi** — `TEST_tilla_<uid>`. v172.15 dan yana **ADMIN xonasi**: login admin/admin123, `ADMIN-` prefiks + `ADMIN_tilla_<uid>` cloud — bo'sh, Qo'limizdagi ostatkani boshidan tekshirish uchun. |
| Git | **v179.5 gacha push qilingan** (prodda). **v179.6 va v179.7** commit qilindi, ⚠ **push qilinmagan** — Ibrohim ko'rib, sinab, o'zi yuboradi. |
| ⚠ Git auth | Credential Manager dagi GitHub token **eskirgan** — push «Invalid username or token» berdi. Tuzatildi: shu repoda git `gh` CLI orqali autentifikatsiya qiladi (`git config --local credential.https://github.com.helper "!gh auth git-credential"`). `gh auth status` — `ibrohimcyborg`, `repo` huquqi bor. Push yana ishlamasa avval `gh auth status` ni tekshir. |
| **Ombor (BIZDA)** | **v172.26 dan TARIXDAN hisoblanadi** — `turOstMap()` / `turOst(zNom,tNom)`, yagona qoida `_ostDelta(op, klientTomon)` da. `t.ostatka` endi hech qayerda KO'RSATILMAYDI (18 joy o'tkazildi: bosh ekran, zavod, tur paneli, berish/vozvrat/sotuv modallari, tekshiruv, chiqim, zapros, birlashtirish, kassa snapshot). 🔧 «Ostatkani qayta tiklash» + `ostatkaQaytaTiklaOch` + `ostatkaHisobla` O'CHIRILDI. Kesh `_ostKesh`, tozalanadi: `save()`, amal-sinxron listener, `cloudYuklab`. `qoldData` ham `_ostDelta` ni chaqiradi → 1:1 konstruksiyadan. |
| **Qo'limizdagi ostatka** | **B usuli (v172.14)** — hafta boshi TARIXDAN hisoblanadi, `t.ostatka` o'qilmaydi. Qator tartibi: bosh → +kirimlar → +klient vozvrat (umumiy) → JAMI → −berish (umumiy) → −zavod vozvrat → qolgan. C bosqich (dushanba skan langari) PLAN.md da. |
| **Dona baza** | **CHERNOVIK** — `DONA_BAZA_UI=false` (1966). Ko'rinmaydi, yozmaydi, muzlatilgan. To'liq o'tish rejasi: **PLAN.md** |

### 2026-08-05 seansida bo'lgan voqea (muhim kontekst)

Ibrohim BIZDA raqami noto'g'riligini ko'rdi (BIZDA 230.66 bo'lishi kerak ~0).
Tahlil: klientga berilganlar va sotuvlar ombordan ayirilmagan — `t.ostatka`
41 joydan yoziladi, xato yig'ilib qolgan. 🔧 «Ostatkani qayta tiklash»
bosilgan, natija yomonlashgan → Ibrohim backupdan tikladi. Qaysi yo'l bilan
tiklagani (Backup Import / Vaqt mashinasi) ANIQLANMAGAN — Vaqt mashinasi
bo'lsa dona bazasi eski holatda qolgan bo'lishi mumkin (endi bu muhim emas,
dona baza muzlatildi). Shu voqea dona bazani chernovikka chiqarish qaroriga
olib keldi.

> **DIQQAT — faylni to'liq o'qib bo'lmaydi.** 311k token, kontekst oynasi 200k.
> Har doim `grep` bilan qidiring, keyin kerakli 20–50 qatorni o'qing.
> `CHANGELOG.md` (221 KB) — **hech qachon o'qilmaydi**, faqat yoziladi.

---

## ⚠ 2026-08-12 SEANSIDA QOIDA BUZILGAN — keyingi seans bilsin

**CLAUDE.md §9 (hujjat).** v172.32–v172.42 (11 versiya) yozilgandan keyin
CHANGELOG va DAVOM.md **yangilanmadi**. Ibrohim so'raganda, seans oxirida
birdan yozildi. Sabab: har versiyada kod → commit → push qilinib, hujjat
qadami tashlab ketildi.

**CLAUDE.md §2 (TAXMIN BLOKI).** Uch versiyada berilmadi:
* **v172.36** — logo sababi topilgach darhol tahrirga o'tildi
* **v172.38** — blob muddati to'g'ridan-to'g'ri o'zgartirildi
* **v172.39** — **eng kattasi** (109 qator, `index.html` + `api/pdf.py`).
  Taxminlar (davr chegarasi, `lom` kirmasligi, soat tartibi) kodga **jim
  singdi**, faqat yozilgandan KEYIN sanab berildi.

**CLAUDE.md §1 (mockup → tasdiq → kod).** O'n versiyadan faqat **uchtasi**
(v172.32, v172.33, v172.35) to'liq siklni bosib o'tdi. Qolganlari
to'g'ridan-to'g'ri kodga ketdi. **v172.41 esa qoidaning teskarisi** — kod
yozilib bo'lgandan keyin, Ibrohim «mockupda ko'rsat» deb **ikki marta**
aytganida mockup chizildi.

Naqsh: «yangi funksiya» bo'lsa qoidaga amal qilinadi, «tuzatish» yoki «kichik
o'zgarish» deb his qilinsa tashlab ketiladi. CLAUDE.md §1 aynan shuni
taqiqlaydi — «Bu oddiy-ku» degan qarorni Claude o'zi qabul qilmaydi.

Ibrohim (2026-08-12): «mani bulani yozmaganinga aybdor qimagin, bu sani
vazifangdi». To'g'ri — tezlik so'ralgani bahona emas.

**v172.43 dan boshlab tuzatildi:** TAXMIN BLOKI berildi, «mockup kerakmi yoki
to'g'ridan yozayinmi?» deb SO'RALDI (Ibrohim: «mockupda before after qil»),
before/after mockup chizildi, tasdiqlangandan keyin kod, keyin darhol
CHANGELOG + DAVOM. Shu tartib davom etsin.

---

## ⚠ TUZOQ — chek chiqmay qolsa BIRINCHI shuni tekshir

**2026-08-19, Ibrohim:** PC da chek chiqmadi, «Yuborilmoqda...» da qotib qoldi.
Print-server ishlab turardi, internet ham bor edi.

**Sabab:** `printXato()` (2171) chek chiqmasa shu oynani chiqaradi — «Bu qurilmada
printer YO'Qmi? OK bossangiz...». Bir marta **OK** bosilgan va
`localStorage['tilla-printer-yoq']='1'` **doimiy** yozilgan.

Zanjir: `printerYoq()`→true (2014) → `chekBuQurilmadan()`→false (2031) →
`chekYubor()` chekni **cloud navbatiga** yozadi (2096) → o'sha kuni Firestore ham
ishlamadi (DNS: `ERR_NAME_NOT_RESOLVED`) → hech narsa chiqmadi.

**Yechim (5 soniya):** Sozlamalar → 🖨 «Chek shu qurilmadan chiqsin» YOQ.
`tilla-chek-bu-qurilma='1'` bayrog'i `printerYoq()` dan USTUN turadi (2029).
Yoki konsolda:
```
localStorage.removeItem('tilla-printer-yoq'); localStorage.setItem('tilla-chek-bu-qurilma','1'); location.reload()
```

Ibrohim tasdiqladi: «ishlab ketti shuni qiganimdan kegin».

**Tuzatilmagan kamchilik:** bitta tasodifiy «OK» mahalliy bosishni abadiy o'chiradi
va oynadagi matn chalg'ituvchi (print-server o'sha payt ishlamayotgan bo'lishi ham
mumkin). Yumshatish taklif qilingan, Ibrohim hali qaror bermagan.

---

## 🟢 HOZIRGI ISH — POS (planshet kassa)

**Login:** `kassatest` / `kassatest` — `CREDS`, `rol:'pos'`, `sandbox:'TEST'`

⚠ **POS 1.17 dan (Ibrohim, 2026-08-23):** `test` loginida POS tabi **YO'Q**.
Ish taqsimoti: **telefon → `kassatest`** (POS), **PC → `test`** (Tilla ERP,
qo'ng'iroqchani tekshirish uchun). POS tabi endi faqat `rol==='pos'` da.

### Baza qayerdan

```
kolleksiya = SANDBOX_ + 'tilla_' + uid
             ↑ kassatest       ↑ Firebase logini (admin@tilla.com)
```
Hozir `TEST_tilla_<uid>` — haqiqiy pulga tegmaydi.
**Haqiqiyga o'tish:** `CREDS` dagi qatordan `sandbox:'TEST'` OLIB TASHLANADI. Boshqa
hech narsa o'zgarmaydi.

### Yozilgan (POS 1.00–1.07)

| | |
|---|---|
| Klient bazasi | qidiruv, A–Z rels, qarz ustuni — `renderPOS` / `_posRoyxat` |
| Klient modali | `openKlientDetail` (11780) nusxasi — qarz tarkibi bilan |
| Kurs paneli | faqat ko'rish: kurs, lom, B ustama, zavod/A/B narxlar |
| Versiya belgisi | POS rolida `POS 1.33` — FAQAT tepada (pastdagi belgi POS da yashirin) — o'ng pastda **va** berish oynasi tepa satrida |
| **BERISH** | **POS 1.09** — zavodga kirish + ichida chap/o'ng. `posBerishOch` / `_pbDraw` / `posBSaqla` (14952–15304) |
| **VOZVRAT** | **POS 1.09** — berish bilan BITTA kod, `_pbMode` bilan ajraladi. `posVozvratOch` |

**Qarz hisobi qayta yozilmagan** — `klientJamiQarz` (9733), `_qarzTarkib` (17057),
`_qarzJamiRows` (16980), `klientJamiSavdo` (9779) CHAQIRILADI. Bu shart: boshqa yo'l
bilan hisoblansa raqamlar klient ekranidagidan farq qiladi (v177.4 da aynan shu
xato tuzatilgan).

### Yozilmagan — mockup tayyor

**1. ~~Berish~~ + ~~Vozvrat~~ — BAJARILDI (v177.9 / POS 1.09, 2026-08-22)**

Ekran (Ibrohim aytgani; planshet **gorizontal** turadi):
zavod kartasi → ichiga kirish → tepada tur chiplari · **o'ngda** gramm+klaviatura ·
**chapda** katakchalar (qatorda 5 ta, tor ekranda 4 ta) + JAMI →
«Savatga qo'shib chiqish» → boshqa zavod. O'zgartirish — **savat qatorini bosib**.
Minus — zavod ichida `±`.

* **NARX YO'Q.** Ibrohim: «klient to'lagani kelganda tilla narxi oshib ketsa
  berishda aytilgan narxga to'g'ri kelmaydi». Faqat gramm va dona.
  Shu sababli **A/B/C ham chiqarildi** (u faqat narx uchun edi).
  `posKursOch` kurs paneliga TEGILMADI.
* **Ombor ostatkasi — OGOHLANTIRADI, to'xtatmaydi** (admin'dagi blok ko'chirilmadi).
* **Vozvrat** — berish bilan **bitta kod**, `_pbMode` ajratadi. Yozuvlar
  `saqlashKlientVozvrat` (13099) bilan **1:1**, `_kdVoz` to'lov yozuvi ham.
  Musbat bo'lmagan tur saqlanmaydi — ochiq aytiladi.
  Qarz ko'rsatkichi `_qarzTarkibRows` (17468) dan.
* Chek nusxasi **1 ta**, sana **bugungi**.
### ✅ SKAN MAYDONI FOKUSNI SAQLAYDI (POS 1.33)

Ibrohim: «1 ta skan qilsam chiqib ketvotti, sichqonchada yana inputga bosib
ishlatvomman».

Sabab: `posBellOch()` panelni butunlay qayta quradi (`posBellYop()` +
`appendChild`) — eski `<input>` DOM dan o'chadi, fokus yo'qoladi.

Yechim: `_posChFokus` (14963) qaysi qatorga qaytishni eslaydi;
`posBellOch()` oxirida (15224) `#pch-in-<qator>` ga `focus()` beriladi.
`posChOch` panel ochilishida 0-qatorga qo'yadi.

⚠ Panelni qayta chizadigan YANGI amal qo'shsang — `_posChFokus=ri` ni ham
qo'y, aks holda o'sha amaldan keyin fokus yana yo'qoladi.

### ✅ CHERNOVIK REJIMI — POS HISOBGA TEGMAYDI (POS 1.27)

Ibrohim (2026-08-23): *«buni faqat chernovik bo'lib keladigan qilgin, man testda
tekshiraman, qo'ng'iroqcha keladi, yozib yoki skan qilib kirgizsam, qabul qilsam
o'tadi»*.

**POS tomoni** (`posBSaqla`) — `k.tarix`, `t.ostatka`, `t.donaOst` ga **umuman
tegmaydi**, `save()` ham chaqirilmaydi. Faqat cloudga chernovik yozadi:
`collection(cloudKol()).doc('_poschernovik').collection('items')` — chek navbati
(`_cheknavbat`) bilan bir xil naqsh, har chernovik alohida hujjat (massiv emas —
ikki qurilma bir-birini o'chirmasin). ⚠ **Chek POS 1.28 da OLIB TASHLANDI** (Ibrohim: «chek chiqarish digan narsani unut») — chernovik hisobga tegmagani uchun chek qabuldan keyin ma'noga ega.
Chernovikda **`donalar:[...]`** ham bor — `k.tarix` ularni saqlamaydi, skan
solishtiruvi uchun shart.

⚠ **POS 1.28 tuzatish:** `posChListen()` avval FAQAT Firebase auth chaqirig'ida
bir marta ishga tushardi — o'sha paytda rol hali `admin` bo'lmasa yoki cloud
tayyor bo'lmasa jimgina qaytardi va **boshqa hech qachon urinmasdi**, natijada
chernovik admin ekraniga **yetib kelmasdi** (Ibrohim: «0 ta kutmoqda»). Endi
`applyRol` dan ham chaqiriladi va cloud tayyor bo'lmasa 2 soniyada qayta urinadi.

**Tilla ERP tomoni** (`test` logini) — `posChListen()` tinglaydi, qo'ng'iroqcha
sanaydi. Ochilganda har tur uchun POS donalari ko'rinadi, admin **yozib yoki
skan qilib** kiritadi, `_posChRecon` (skReconcile mantig'i) mos/kam/ortiq
ko'rsatadi. **Hamma tur tekshirilmaguncha qabul tugmasi yopiq.** Farq bo'lsa
tugma «⚠ O'zgarish bilan qabul» ga aylanadi.

**Yozuvlar FAQAT `posChQabul` da tug'iladi** — `saqlashKlientBerish` /
`saqlashKlientVozvrat` bilan aynan bir xil (`_kdVoz` ham). **Admin skani
haqiqiy** hisoblanadi. Sana/soat chernovikdan olinadi (kassir qilgan payt).
Zavod/tur/klient **nom bo'yicha** qayta topiladi — indeksga ishonilmaydi.

Sinov: POS yubordi → k.tarix 0, qarz/ostatka/donaOst o'zgarmadi, save() yo'q.
Admin 3D ni 1.50 o'rniga 1.80 kiritdi → qabuldan keyin k.tarix da **1.8**,
ostatka 307.98→300.68, donaOst 20→18, chernovik holati `qabul`.
* **YANGI USLUB (POS 1.16 → 1.29):** POS **YORUG'** palitrada (POS 1.29,
  Ibrohim: «fon oq bo'lsin, faqat POS da») — `#EEF1F7` fon, `#FFFFFF` karta,
  `#3B6FE0` urg'u, `#D14A2E` qarz, `#0F1B33` matn.
  ⚠ Ranglar to'q ko'kdagidan **ataylab farq qiladi**: `#5183FF`/`#FF8B6B` oq
  ustida xiralashardi (qarz kontrasti 2.1 → 4.4 ga ko'tarildi).
  **Shakl (POS 1.29):** tugma va maydonlar **to'liq pill** (`999px`, iOS uslubi —
  Ibrohim: «rangiga emas formasiga»), avatar **oq va dumaloq** (50%), kartalar
  14–24px. Pill uchun `!important` shart — POS kodi inline style bilan chiziladi.
  **Sticky (POS 1.29):** `_posBoy()` `#main-pos` balandligini **o'lchab** qo'yadi
  (piksel taxmin qilinmaydi) — aks holda butun sahifa siljib, klient qatori tepa
  panel va soat ustida ko'rinib qolardi. Endi faqat `#pos-list` siljiydi.
  ~~POS ko'k palitrada — `#030F2C` fon, `#5183FF` urg'u.~~ Tokenlar `body.rol-pos, #main-pos, #pos-ovl, #pb-ovl`
  selektorida qayta e'lon qilingan ([index.html:265](index.html)) — `topbar`,
  `main-tabs`, `logo` ham tokenlar bilan ishlagani uchun **butun POS logini**
  ko'k. Inline `var(--...)` lar qayta yozilmadi.
  ⚠ **Admin/zavod/hamid tegilmagan** — ular hamon `--gold:#c9a84c` (sinovda
  har safar tekshiriladi).
  Amallar klient oynasining **sarlavhasida**, uchta ko'k pill (`_posAmalPill`);
  tor ekranda (`max-width:700px`) o'z qatoriga tushadi (`.pos-hd`/`.pos-pills`).
  Klient oynasi ham berish oynasi ham **orqani to'liq yopadi** (fon `var(--bg)`),
  qo'shimcha: berish ochiqda `_pbOrqa('none')` topbar/tablar/`#main-pos` ni
  **yashiradi** (POS 1.22 — telefonda fixed qatlam tepani qoplamas ekan).
  ⚠ `body.rol-pos #main-pos` da `display:flex !important` bor — yashirish uchun
  `setProperty('display','none','important')` shart.
  Amal ikonlari **inline SVG** (POS 1.23) — `↩` iOS da emoji bo'lib ketardi.
  Chapdagi ro'yxat **faqat tanlangan turni** ko'rsatadi (POS 1.24) — boshqa
  turlar yo'qolmaydi, chipida grammi turadi va savatga tushadi.

### ✅ «Orqasi yurvotti» — HAL BO'LINDI (POS 1.25)

Uch urinishdan keyin. Avvalgi ikkitasi **noto'g'ri mexanizmni** tuzatgan:
* POS 1.14 — fonni qattiq qildi → muammo shaffoflikda emas edi
* POS 1.22 — orqadagi elementlarni yashirdi → `mainTab('pos')`
  ([index.html:12456](index.html)) `#main-pos` ga `display:block !important`
  qo'yib qayta ochib yuborardi (u `applyRol` dan chaqiriladi)

**Asl sabab:** oyna `position:fixed` bo'lsa ham **orqadagi sahifa scroll
bo'laverardi** — iOS da surilganda tepasi qatlam ustida ko'rinardi.

**Yechim:** `_posScrollLock(on)` — `body` ga `position:fixed` + `top:-scrollY`,
yopilganda qaytariladi. **Sanagich shart:** berish oynasi klient oynasi ustida
ochiladi, ikkalasi ham qulflaydi, faqat oxirgisi bo'shatadi. `posBYop` /
`posModalYop` oyna yo'q bo'lsa qulfga tegmaydi.

---

## ⚠️ ARXITEKTURA QARORI KUTILMOQDA — POS ni AJRATISH

Ibrohim (2026-08-23): *«POS sistemani shunaqa qigansanki u Tilla ERP ning orqa
fonida ishlayapti — bu umuman noto'g'ri yo'nalish, eng katta xato».*

**U haq.** POS `index.html` ichida, ERP ning `#main-pos` div'i sifatida yashaydi:
bitta `body`, bitta `:root`, bitta scroll, bitta tab tizimi. Bugungi muammolarning
deyarli **hammasi** shuning ko'rinishi edi:

| Muammo | Ildizi |
|---|---|
| Tepada klient qidirish ko'rinardi | POS ERP div'i ichida |
| `mainTab('pos')` yashirishni bekor qilardi | ERP tab tizimiga bo'ysunadi |
| Palitrani `body.rol-pos` ga o'rash | bitta CSS, bitta tema |
| Orqa fon suzardi | bitta `body`, bitta scroll |
| **Surib ERP ga kirib ketish** | umumiy swipe ishlovchisi (POS 1.30 da yopildi) |

**Taklif:** POS alohida fayl — `pos.html`. O'z DOM'i, CSS'i, qobig'i. ERP bilan
faqat Firestore orqali uchrashadi (o'qish + `_poschernovik` ga yozish).
Chernovik g'oyasiga to'g'ri keladi — POS `data` ga baribir yozmaydi.

⚠ **Yagona jiddiy xavf:** qarz funksiyalari (`klientJamiQarz`, `_qarzTarkibRows`)
nusxalanmasin — aks holda raqamlar ajraladi (v177.4 xatosi). Yechim: ularni
`hisob.js` ga chiqarib, `index.html` va `pos.html` **ikkalasi** yuklasin.

**Narxi:** yangi `pos.html` qobig'i; `hisob.js` ko'chiriladi; bugungi POS
ekranlari deyarli o'zgarishsiz ko'chadi; `index.html` dan ~700 qator o'chadi;
qo'ng'iroqcha va qabul `index.html` da qoladi. `viewport-fit`, sticky o'lchash,
`!important`, `body.rol-pos` — hammasi keraksiz bo'ladi.

**Ibrohim qarori (2026-08-23):** *«2 ni qilaqolilik»* — avval hozirgi POS sinaladi,
ishonch hosil qilingach ajratiladi. Ajratish **hozir boshlanmaydi**.

### 🔒 KAFOLAT — boshqa loginlarga TEGILMAYDI

Ibrohim: *«bu o'zgarishla Abdulhamid loginiga, admin tilla loginiga umuman
ta'sir qilmasin»*.

**O'lchandi (2026-08-23, POS 1.30):**

| Login | Palitra | Topbar | Qo'ng'iroqcha | Tugma radiusi | POS tabi | `hamid-x` |
|---|---|---|---|---|---|---|
| `tilla` | `#0f0f0f` / `#c9a84c` | qorong'i | yashirin | 50% | yashirin | flex |
| `abdulhamid_7777` | `#0f0f0f` / `#c9a84c` | qorong'i | yashirin | 50% | yashirin | **none** ✔ |
| `zavod` | `#0f0f0f` / `#c9a84c` | qorong'i | yashirin | 50% | yashirin | flex |
| `admin/admin123` | `#0f0f0f` / `#c9a84c` | qorong'i | yashirin | 50% | yashirin | flex |
| `test` | `#0f0f0f` / `#c9a84c` | qorong'i | **ko'rinadi** (ataylab) | 50% | yashirin | flex |
| `kassatest` | `#EEF1F7` / `#3B6FE0` | oq | yashirin | **999px** | ko'rinadi | flex |

Kod jihatdan ham tekshirildi: `hamid` so'zi uchraydigan 36 qatordan **faqat bitta
IZOH** o'chgan (POS 1.17 da olib tashlangan blokning izohi). CSS va shartlar
o'zgarmagan. `rol-zavod` qatorlari aynan bir xil.

⚠ **Ikkita o'zgarish GLOBAL** (Ibrohim ruxsati bilan, v178):
1. `viewport-fit=cover` — notchli telefonda **hamma login** endi safe-area'ni
   hisobga oladi (avval `env(safe-area-inset-*)` 0 edi, himoyalar o'lik turgan)
2. `#app-ver` pastki chekkasi `calc(6px + var(--safe-bot))`

Bular mantiqqa, hisobga, ma'lumotga tegmaydi — faqat bo'shliq.

## ☁️ CLOUD AUDITI — 2026-08-23 (kod O'ZGARMADI, faqat tahlil)

Ibrohim POS da kursni uch qurilmada uch xil ko'rdi (planshet 77.7 · telefon 74.4
· PC 84) va cloud qanday qurilganini so'radi. Uch audit o'tkazildi.
Hujjat (Artifact, telefonda ochiladi):
https://claude.ai/code/artifact/c5df1f9e-fa33-4ea0-815a-2928002b52b6

### ILDIZ — bitta, alomati ikkita

Blobdan oplogga o'tish **boshlangan, lekin oxirigacha yetkazilmagan**.
`data.kassa` va kurs/narx sozlamalari o'sha o'tishda qolib ketgan — ikkalasi
ham FAQAT blob bilan sayohat qiladi, blob esa ma'lumoti bor qurilmaga
hech qachon tushmaydi (`cloudListen` 19645: `bosh && lokalVaqt===0`).

| Alomat | Sabab | Joy |
|---|---|---|
| ~~Kurs har qurilmada boshqa~~ **✅ v179 da YOPILDI** | `tilla-kurs-bugun` localStorage da; cloudga faqat `data._narxSync` bilan chiqardi | endi `sozlamalar` jonli hujjati — `sozListen`/`sozQollash`/`sozKuzat` |
| Kassa sinxronlanmaydi | `amalWalk` kassani ATAYLAB tashlab ketadi — «obyekt, blob orqali sinxron bo'ladi» | izoh 8279 |

⚠ POS kursni 14873 va 14801 da localStorage dan o'qiydi.

### To'g'ri ishlayotgan joylar — TEGILMASIN

- **Oplog** (`_amallar/items`, 8389/8392) — har yozuv o'z `_id` si bilan.
- **Ostatka tarixdan** — `turOst` 7484. Increment-hisob v99 da ATAYLAB
  o'chirilgan (`hisobListen` 8530). ⚠ Uni qaytarish TAKLIF QILINSA — RAD ET,
  Ibrohim bu qarorni allaqachon qilgan.
- **Sinov xonasi** — `tk()` prefikslash 2007, `cloudKol()` 19447.
- **`arrayUnion` + `zaImportIds`** — Zavod ko'prigi to'qnashuvsiz.

### Boshqa tasdiqlangan kamchiliklar

- **Yashil chiroq aldaydi** — cloudda yangiroq nusxa borligini ko'rib, uni
  YUKLAMAYDI, lekin «sinxron» deb ko'rsatadi (19649).
- **POS chernovigini faqat TEST xonasi tinglaydi** — `posChListen` 14974:
  `getRol()==='admin' && SANDBOX==='TEST'`. ⚠ Haqiqiy bazaga o'tishda SHU
  SHART o'zgarishi kerak, aks holda chernovik hech kimga bormaydi.
- **`_poschernovik` hujjatlari hech qachon o'chirilmaydi** (chekda tozalash bor — 2197).
- **Zavod ERP ga kassa hisobi KO'CHIRILGAN** — Zavod 623–631, to'rt funksiya.
  Tillada hisob o'zgarsa, Zavodda qo'lda o'zgartirilmasa ikki xil raqam chiqadi.
- **Zavod ERP `tillaKolTop`** (Zavod 498) eng oxirgi yozilgan omborni tanlaydi —
  TEST da ko'p ishlangan bo'lsa SINOV bazasiga ulanib qoladi.
- **Zavod ERP o'z bazasiga hisobsiz ulanadi** (Zavod 559–560) va uni har
  saqlashda to'liq ustiga yozadi (1338/1341).
- **Bo'lak BELGI bilan kesiladi** (19843), Firestore esa BAYT bilan cheklaydi.
- **`enablePersistence` ikkala faylda ham YO'Q** — internetsiz navbat yoqilmagan.
- **`YOZUV_LIMIT` 25000** (19412) — bu Firestore limiti EMAS, o'z tormozimiz;
  va `cloudSaqlaNow` hisoblagichni umuman chaqirmaydi.
- **`kassa_snapshot`** har saqlashda yoziladi, lekin Zavod uni O'QIMAYDI.

### ✅ 1-QADAM BAJARILDI — SOZLAMALAR JONLI HUJJATDA (v179)

Ibrohim: «cloud bir xil turmasligi charchatti, zavod erpda bu muammo yoqde» →
Zavod ERP usuli olindi: bitta hujjat, hamma tinglaydi.

`cloudKol()/sozlamalar` — kurs, lom, lom-farq, B ustama, zavod foizlari.

| Funksiya | Nima qiladi |
|---|---|
| `sozRef()` | hujjat manzili |
| `sozListen()` | **hamma rol** tinglaydi (pos, zavod, hamid ham) |
| `sozQollash(d)` | localStorage ga yozadi + ekranni qayta chizadi. ⚠ narx maydoniga yozayotgan bo'lsa TEGMAYDI |
| `sozYubor(h)` | **faqat `getRol()==='admin'`** yozadi (Ibrohim qarori) |
| `sozKuzat()` | 3 soniyalik barmoq izi kuzatuvchisi — ~20 yozuv joyiga chaqiruv qo'shmaslik uchun |
| `_kursTarixBirlashtir` | tarix BIRLASHTIRILADI, hech narsa o'chmaydi |
| `sozManbaSaqla` / `sozManba` | **v179.1** — kursni kim va qachon qo'ygani. `tilla-soz-manba` kalitida |

**v179.1 — manba ko'rsatildi.** Admin bosh ekranidagi «Kunlik kurs» blokida
«23.08 · 14:30 · Qurilma-1», POS kurs oynasida «Kursni qo'ygan: Qurilma-1 · 14:32».
POS kurs TUGMASIGA (pill) tegilmadi — joy tor, Ibrohim so'rasa qo'shiladi.

⚠ **«ASOSIY» qurilma HECH NIMA QILMAYDI.** `qurilmaAsosiy()` (19470) butun faylda
faqat 19591 da yorliq chizishda ishlatiladi — imtiyoz yo'q. Ibrohim uni qidirib
vaqt sarflagan. Kodga tegilmadi. Kelajakda «asosiy qurilma» bilan bir narsa
qilmoqchi bo'lsang — u avval haqiqiy xulqqa ega bo'lishi kerak.

⚠ **Kursni o'qiydigan 20 joyga TEGILMADI** — ular localStorage dan o'qiyveradi.
Yangi kurs o'qish joyi qo'shsang ham shu yo'ldan o'qi, alohida kanal ochma.

⚠ Eski `data._narxSync` ko'prigi (2313/2325/2338) **o'chirilmadi** — u faqat
sahifa yuklanganda ishlaydi, yangi tinglovchi undan keyin ustun keladi.
Sahifa ochilganda bir lahza eski kurs ko'rinib, keyin to'g'rilanishi mumkin.

**Qolgan tartib:**

| | Ish | Xavf |
|---|---|---|
| ~~1~~ | ~~`settings/global_config` — kurs~~ **✅ v179** | — |
| 0 | `enablePersistence` + yashil chiroq yolg'oni | juda kichik |
| 2 | `zavod_amallar` → subkolleksiya (massiv emas) | kichik |
| 3 | **Kassa** tarixdan + hisob ikki ilovada UMUMIY — Ibrohim «avval kurs» dedi, navbat shunda | katta |
| 4 | Faqat shundan keyin blobni nafaqaga chiqarish | katta |

---

### Tavsiya qilingan tartib (eski yozuv)

| | Ish | Xavf |
|---|---|---|
| 0 | `enablePersistence` + yashil chiroq yolg'oni | juda kichik |
| 1 | `settings/global_config` — kurs bitta manbadan | kichik |
| 2 | `zavod_amallar` → subkolleksiya (massiv emas) | kichik |
| 3 | Kassa tarixdan + hisob ikki ilovada UMUMIY | katta |
| 4 | Faqat shundan keyin blobni nafaqaga chiqarish | katta |

⚠ Gemini «arxitekturani tubdan o'zgartir, increment/transaction ishlat» dedi —
tahlil qilindi, RAD ETILDI: increment allaqachon sinalib o'chirilgan (8530),
`runTransaction` yozuvni ko'paytiradi, `arrayUnion` esa xavfsiz qism.
To'liq tahlil suhbatda, 2026-08-23.

---

## Ochiq masalalar

Quyidagilar **hal qilinmagan**. Tartib — muhimligi bo'yicha.

### ✅ 0r. SDACHA — offset ortig'ini naqt qaytarish — BAJARILDI (v176.3)

**2026-08-18 — v176.3 da yozildi.** Ibrohim spetsifikatsiyasi: «$ tongle bosaman,
ortiqcha pul shunaqa ko'rsatadi, bo'ldi. Biz sdacha — naqt qaytardim qilamiz,
kassadan chiqim qilib ko'rsatadi — kimga, nimadan chiqim bo'lganini.»

Ildiz: offsetning ortig'i **ataylab** tashlanardi (13763 / 15275 dagi izohning
o'zi shuni yozgan). Sdacha esa uch manbadan yig'ilardi (13778) — offset ularda
yo'q edi, shuning uchun panel ochilmasdi.

Yechim: yangi panel **yozilmadi**. Ortiqcha `ktSdacha` / `ortiqcha` yig'indisiga
qo'shildi → mavjud panel o'zi ochildi (13867 dagi shart allaqachon bor edi).
«Sdacha — naqt qaytardim» tanlansa `sdachaTaqsimSaqla` (13486) kassaga
`kategoriya:'Offset sdacha'` chiqimini yozadi: klient nomi + manba zavod·tur +
gramm × narx. Manba turining qarzi ham yopiladi — offset qatori endi TO'LIQ
yoziladi (14173 kt, 16039 ks).

Tanlovlar: **A1** ikkala modal · **B1** qarz yopiladi · **C1** chiqim faqat offset
ulushiga · **D1** bekor qilish qatori yo'q · **E2** naqd tekshirilmaydi.

⚠ **Tekshirilmagan** — Ibrohim hali ilovada sinamagan.
⚠ `_ktOffsetPulUsed` (14151) yetim qoldi, o'chirilmadi.

<details><summary>Eski yozuv (v176.2 gacha bo'lgan tahlil)</summary>

2026-08-16: Ibrohim sotuv modalida offsetni **sdacha qilib pul bilan qaytarish**
imkonini so'radi. Mockupdagi to'rt variantdan **B — pul qaytarish** ni tanladi
(`mockups/v176.2-uzun-son-va-sdacha.html`).

**2026-08-16 TOPILMA — noldan yozilmaydi.** Ilovada **pul sdachasi mexanizmi
TO'LIQ mavjud**, faqat u hozir **ortiqcha to'lov** uchun ishlaydi:

| Nima | Qator |
|---|---|
| `sdachaTaqsimRender` — tanlash oynasi | **13528** |
| `sdachaTaqsimSaqla` — saqlash + kassaga yozish | **13431** |
| `window._ktSdachaTanlov = {tip:'sdacha'}` | **13629** |
| `_ktSdachaPul` — chekka ketadigan summa | **13972–13977** |
| `kt-sdacha-val` — ekrandagi ko'rsatkich | 1694 |

Ya'ni Ibrohim so'ragani — **offset summasini xuddi ortiqcha to'lovdek** shu
mexanizmga uzatish. Bu «noldan dizayn» emas, **mavjud yo'lga ulash**.

✅ **UCHALA SAVOLGA HAM JAVOB BOR** (2026-08-16). Kod yozish uchun spetsifikatsiya
to'liq — faqat mexanizmni o'qib chiqish qoldi.

⚠ **Yozilmadi** — bu **kassadan pul chiqadigan** amal. Avval
`sdachaTaqsimSaqla` (13431) ning kassaga NIMA yozishini o'qib chiqish shart,
aks holda pul hisobida xato bo'ladi. Uch qaror kerak:
1. **Qaysi ekrandan?** Sotuv modalidagi `$ ✓` tugmasi yonidami, yoki alohida
   «sdacha bilan qaytarish» tugmasimi? (To'lov modalida sdacha allaqachon bor —
   sotuvga ham o'shani ulash kerakmi?)
2. ~~**Kassaga qanday yoziladi?**~~ ✅ **IBROHIM JAVOB BERDI (2026-08-16):**
   «chiqim qivorasan sdachani shunda» — ya'ni kassaga **CHIQIM** sifatida
   yoziladi. Qolgan aniqlik: **qaysi chiqim tipi** (mavjud tiplardan birimi
   yoki yangi «Sdacha» tipimi) — buni `sdachaTaqsimSaqla` (13431) va mavjud
   chiqim mexanizmini o'qib aniqlash kerak.
3. ✅ **IBROHIM JAVOB BERDI (2026-08-16):** «offsettan klient nomini yozib
   shu klientga sdacha bervorildi offset qilib summasnin nimadanligin yozasan»

   Ya'ni **chiqim yozuvida** shular bo'lishi kerak:
   * **klient nomi** (offset qaysi klientniki bo'lsa)
   * izoh: «sdacha berildi — offset qilib»
   * **summa qaysi zavod·turdan** kelgani (offset manbai)
   * summaning o'zi

   ⚠ Chekda qanday ko'rinishi — hali aytilmagan (alohida qatormi yoki mavjud
   «Sdacha» blokigami).

Eslatma: ilovada **gramm sdacha** (`tip:'klientda'`) allaqachon bor — u klient
tarixida `↩ Butterfly · Oddiy` bo'lib chiqadi. Ibrohim so'ragani esa **pul**.

</details>

### ⚠ 0s. UZUN SON — ILDIZ TUZATILMAGAN (v176.2)

`_qarzTarkibRows` da qarz **besh joyda** yaxlitlanmasdan yig'iladi:
**16735, 16739, 16744, 16751, 16762**. Natijada `qarz` maydoni
`5.209999999999999` kabi bo'lib yuradi.

v176.2 da **A darajasi** qilindi — maydonga yozishda `roundG` (4 joy). Ibrohim:
«ildizzi kegin qilamiz».

⚠ Ildizni tuzatish `_qarzTarkibRows` ni o'zgartiradi, u esa v175.2 dan beri
**hamma joyda** yagona manba (klient ekrani, ro'yxat, qidiruv, berish modali,
sotuv, PDF, chek). Raqamlar 0.01 g darajasida siljishi mumkin — alohida versiya
va diqqatli tekshiruv kerak.

### ⭐ 0q. OFFSET — YOPILDI (v174.4–v175)

2026-08-14: Ibrohim rasm bilan ko'rsatdi — offset **ikki marta** hisoblanardi.
Sabab: offset BITTA pul, IKKI tomondan yozilgan yozuv (manba `_kdYopish:true`,
manzil belgisiz). Ba'zi ekranlar ikkala tomonni qo'shib yuborardi.

**Tuzatildi:** klient tarixi sarlavhasidagi pul (11594) · PDF kunlik bloki (16939)
· **2-chi chek jadvali (14410, v174.6)**.
**Ko'rinish qo'shildi (v174.5):** manba qatori + `→ / ←` o'qlari, PDF da binafsha.

**Xato C ham yopildi (v174.7).** `_tolovTurAniq` da offset IKKI yo'l bilan
topilardi va ikkalasi ham ishlardi: manba yozuvidagi `_kdYopish` belgisidan +
manzil yozuvlarida `summa − naqd` ayirmasidan. Natija qo'shilardi
(Dilfuza: 4,572.17 + 4,572.17 = 9,144.34). Faqat **ARALASH** to'lovda ko'rinardi.

Endi alohida yig'iladi (`offManba` / `offAyirma`), oxirida
`Math.max(offManba, offAyirma)`. **3-variant** tanlandi — qaror **Claude'dan**:
1 va 2 variant har biri bir tomonni butunlay o'chirar edi va belgisiz eski
yozuvlarda (v172.24 holati) yoki pul maydonsiz eski formatda offset **ko'rinmay
qolardi**. `max()` ikkalasini saqlaydi.

Ayirma hisobi `_opOffUlush` (11594) ga o'tkazildi — u naqtni `_opNaqtPul` orqali
o'qiydi. Xom `op.naqtPul` bilan eski `naqtPul:0` xatosi (v174.1) yolg'on katta
offset berib, `max()` da to'g'ri manbani bosib ketardi.

`ofNom` endi **manbadan** olinadi (`ofNomManba || ofNomAyirma`) — «Offset — X dan»
pul QAYERDAN kelganini bildiradi. Avval qaysi yozuv birinchi kelsa o'shanikini
olardi, ya'ni manba bor bo'lsa ham manzil nomini yozib qo'yishi mumkin edi.

**Sinov holati:** v174.4–v174.7 **haqiqiy kod bilan** sinaldi (`index.html` dan
blok ajratib olinib ma'lumot o'tkazildi). v174.7 uchun **6 holat**: sof offset ·
aralash · manba yo'q · eski format · `naqtPul:0`+lom · sof naqt — 6/6 to'g'ri,
`jami` o'zgarmadi. PDF chizuvchisi ham tekshirildi (binafsha rang + Symbol
shrifti).

✅ **2026-08-16: IBROHIM PRODDA TASDIQLADI** — «pdf tori ishladi». v174.4–v174.9
ning hammasi haqiqiy PDF da ko'rildi: offset qatori, `→ / ←` o'qlar, Ostatka
ustuni. Offset masalasi **yopildi**.

**v174.8 — PDF tepa jadvali.** Ibrohim rasm yubordi: Ostatka ustuni 85.15 dan
**−18.23g** ga tushgan. Sabab yana o'sha — manba qatori oddiy to'lovdek
ayirilardi. `klientPDFYukor` ning boshlanish qismida (16896–16950) `_kdYopish`
**0 marta** uchraydi. `runBal` (16922) tuzatildi:
`if(op.tip==='berish' || op._kdYopish) runBal+=g;`
Sinov: `berish 100 → tolov 30 → OFFSET 20 → vozvrat 10 → tolov 5`,
eski `100·70·50·40·35` → yangi `100·70·90·80·75`, farq 40 = 2×offset.
✅ **Prodda tasdiqlandi (2026-08-16).**

✅ **PDF DAGI OXIRGI IKKI JOY HAM YOPILDI (v175):**

1. ~~**`qarz_bd`**~~ — **BAJARILDI.** PDF o'zining alohida hisobini yuritardi va u
   `_qarzTarkib` (16666) dan **uch joyda** farq qilardi: offset qoidasi yo'q,
   `klientda` (sdacha) o'qilmaydi, zavod/tursiz to'lovlar taqsimlanmaydi. Faqat
   offsetni tuzatish yetmasdi. `qarz_bd` **butunlay olib tashlandi** — PDF endi
   `_qarzTarkib(curKlientIdx)` ni chaqiradi. Yagona manba.
   Sinov: eski `-46.29g` → yangi `+45.49g`, farq **91.78g**.
2. ~~**JAMI qatoridagi `qolgan`**~~ — **BAJARILDI.** `jami_qolgan` payloadda
   keladi (`qarz_tarkib` qatorlarining yig'indisi). Berilmasa eski formula
   zaxira bo'lib qoladi (orqaga moslik). Ko'rinish xatosi ham tuzatildi:
   manfiy qiymatda **«--87.56g»** chiqardi, endi **«+87.56g» yashil**.
   ⏳ **Ibrohim hali PDF da ko'rmagan.**
3. ~~**Ko'rinish belgisi**~~ — **BAJARILDI (v174.9).** Sarlavha «Offset»
   (binafsha, belgisiz — `⇄` Helvetica da qora kvadrat bo'lishi mumkin),
   Tur ustunida `→ 3D, 3DS` / `← Oddiy`. Guruh **butunlay** offsetdan
   yopilgandagina «Offset», aralashda «$ Tolov» qoladi. PDF chindan
   chizib tekshirildi — o'qlar haqiqiy glif (`\256` / `\254`), notdef yo'q.

`bal` (16904) — grep bilan tekshirildi, **hech qayerda ishlatilmaydi**
(o'lik o'zgaruvchi), tegilmadi.

Tashxis mockupi: `mockups/v174.8-pdf-tepa-jadval-offset.html`

⚠ **TEGILMAGAN, o'sha joyda turibdi:** `_ostJadvalUstunlar` (14408) da
`nom='berildi'` bor, `inventar==='boshlangich'` tekshiruvi YO'Q — shuning uchun
2-chi chekda shakllantirish hali «berildi» deb chiqadi (0m masalasi).
v174.5 dagi `→ / ←` o'qlari ham 2-chi chekka kengaytirilmagan.

⚠ **v174.7 da TOPILDI, tekshirilmagan:** `TOLOV_TURLARI` butun faylda **ikki
marta** e'lon qilingan — **11583** va **15389**. v171.8 dagi `kh*` global
to'qnashuviga o'xshash naqsh. Ikkalasi bir xilmi, qaysi biri qaysi joyda
ishlatiladi — **qaralmagan**. Offsetga aloqasi yo'q, shuning uchun tegilmadi.

### 0i. ~~Telefondan chek bosilsa PC dan chiqishi~~ — BAJARILDI (v172.28)

Ibrohim so'radi (2026-08-09): telefondan chek bossa, PC ga ulangan termal
printerdan chiqsin.

**To'g'ridan-to'g'ri bo'lmaydi.** Kodda 5 joyda `fetch('http://localhost:5000/print')`
(2913, 3096, 8514, 10190, 10193). `localhost` — har qurilmaning o'zi, telefonda
printer yo'q. PC ning LAN IP siga yozish ham ishlamaydi: ilova HTTPS da (Vercel),
brauzer HTTPS sahifadan `http://192.168.x.x` ga so'rovni mixed-content deb bloklaydi
(`http://localhost` uchun maxsus istisno bor, LAN IP uchun yo'q).

**Ishlaydigan yechim — chek navbati Firestore orqali:**
telefon `_chekNavbat` ga topshiriq yozadi → PC (ilova ochiq) tinglaydi →
o'z `localhost:5000` iga yuboradi → chek chiqadi. PC o'z localhost'iga murojaat
qilgani uchun blok yo'q. Mavjud Firestore-listener qolipiga to'liq mos.

Hal qilinadigan nuqtalar:
- **Qaysi qurilma chiqaradi** — bitta qurilma "printer" deb belgilanishi kerak,
  aks holda ikki PC ochiq bo'lsa chek ikki marta chiqadi
- **Muddat** — PC keyinroq ochilsa eski chek chiqmasligi uchun (masalan 2 daqiqa)
- **Telefonda javob** — "yuborildi / chiqarildi" ko'rinishi

**BAJARILDI v172.28 da.** `chekYubor()` yagona kirish nuqtasi (11 chaqiruv o'tdi),
Firestore `_cheknavbat/items`, Sozlamalar > Printer kaliti. Sukut bo'yicha
`!printerYoq()` — PC da avvalgidek lokal, telefonda navbat. Muddat 10 daqiqa,
1 soatdan keyin o'chiriladi, `bajarildi` belgisi chiqarishdan OLDIN qo'yiladi.
Kalitni PC da YOQ, telefonda O'CHIQ qilish shart (faqat bitta qurilmada yoqilsin).

**2026-08-10: sinovda 1 marta bosilgan, 7 marta chiqqan** → v172.29 da tuzatildi
(pastga qarang). ⚠ v172.29 dan keyin QAYTA SINALMAGAN.

⚠ **2026-08-14 — Ibrohim yangi yechim so'radi:** «ba'zida 2 ta 3 ta qurilma
bo'lib qolishi mumkin, bunga boshqa yechim qilish kerak — qaysi qurilmadan
kelsa ham 1 ta chiqarishi kerak».

Taklif (mockup: `mockups/v174.4-offset-ikki-marta-va-javoblar.html`):
chiqaruvchi qurilma **bulutda bitta** bo'lib belgilansin — `_chekprinter`
hujjati, qurilma o'z nomini yozadi, boshqalar ko'rib o'z kalitini avtomat
o'chiradi. ~25–35 qator. **Uch savolga javob kutilmoqda:**
1. Chiqaruvchi hech kim bo'lmasa — navbatda kutsinmi yoki bosgan qurilma chiqarsinmi?
2. Chiqaruvchi ilovani yopgan bo'lsa — hozirgi 10 daqiqa muddat qolsinmi?
3. ⚠ Abdulhamid bu ro'yxatga kirsinmi? (taxminim: **tegilmasin**)

⚠ **Ochiq xavf (v172.29 da yopilmagan):** 3–4 qurilmada ilova ochiq.
`chekBuQurilmadan()` sukut bo'yicha `!printerYoq()` — ya'ni **har qurilma
navbatni tinglayveradi**. `tilla-chek-chiqdi` ro'yxati faqat **bitta qurilma
ichida** ishlaydi. Ikki qurilmada printer bo'lsa chek ikki joydan chiqadi.
Yopish uchun alohida qaror kerak (masalan «chiqaruvchi qurilma» bulutda bitta
bo'lib belgilansin).

### 0p. ~~BOSH EKRAN HISOBOTI~~ — BAJARILDI (v174.2)

`renderHisobot` (5117) kun bo'yicha guruhlanadi, Kirim/Vozvrat/Chiqim filtri
qo'shildi, qatorda zavod nomi qoldi. ⚠ SINALMAGAN — Ibrohim ko'rishi kerak.

Eslatma: v172.44 da noto'g'ri ekran (`renderZavodHisobot`) o'zgartirilgan edi,
v173.1 da bekor qilindi. Zavod ICHIDAGI hisobot ataylab eski holatida
(Ibrohim: "kam ishlatiladi").

### 0o. ESKI YOZUVLARDA naqtPul:0 — yopqich YETARLI (Ibrohim, 2026-08-14)

Ibrohim so'radi: «eski versiyalarda bo'lmaganini hisobiga ko'rinmaydi
demoqchimisan?» — **qisman ha, lekin ikki xil holat bor:**
1. **Maydon umuman yo'q edi** (juda eski format) — `_opNaqtPul` 3307 yopadi
2. **Maydon bor, ichiga 0 yozilgan** (aralash sotuvdagi YOZUV XATOSI, Dilobar
   Opa $6,850 / Dilorom Opa $1,765) — 3310–3314 qoldiqdan hisoblaydi

Ya'ni asosiy sabab versiya emas, **yozuv xatosi**. Migratsiya **qilinmaydi**.

⚠ Yopqich `_opOffUlush` (v174.5) da ham ishlatiladi — eski `naqtPul:0` yolg'on
offset ko'rsatmasin uchun.

<details><summary>Eski yozuv (arxiv)</summary>

v174.1 muammoni **o'qishda** hal qildi (`_opNaqtPul`) — kassa endi to'g'ri
ko'rsatadi. Lekin `k.tarix` dagi yozuvlarda `naqtPul:0` **hali turibdi**.

Ibrohim ataylab shu yo'lni tanladi (xavfsiz: ma'lumot va cloud tegilmaydi,
orqaga qaytarish oson). Migratsiya — alohida ish, hali qilinmagan.

⚠ Diqqat: `_opNaqtPul` qo'riqchisi — faqat **lom bor** va naqt 0 bo'lganda
ishlaydi. Agar kelajakda **karta bilan** ham shunday holat chiqsa (naqt 0,
karta bor, lom yo'q) — u tuzalmaydi, chunki sof karta sotuvda naqt haqiqatan 0.
</details>

### 0n. CLOUD AXLATI TOZALANMAGAN — faqat «chiqmasligi» to'xtatildi (v172.32)

2026-08-11: eski, allaqachon o'chirilgan vozvratlar qaytib keldi va zavodni
qarzdor qilib ko'rsatdi. Sabab uchta narsaning birlashuvi (to'liq tashxis:
`mockups/v172.32-tashxis-eski-vozvrat-tiriladi.html`):

1. Oplogda **o'lik hujjatlar** qolgan — `deleted:true` belgisi hech qachon
   qo'yilmagan (v172.30 gacha o'chirish belgisi tasdiqsiz edi).
2. `syncFullFill` ichida `deleted` so'zi **0 marta** — ⬆ tugmasi cloudga faqat
   QO'SHADI, ortiqchasini **hech qachon olib tashlamaydi**.
3. v172.30 da `vaqt: Date.now()` qilingani uchun o'lik hujjatlar «yangi» bo'lib
   hamma qurilmaga tarqaldi.

**v172.32 da faqat 3-band qaytarildi** (Ibrohim: «manga chiqmasin boldi»).
Ya'ni **axlat cloudda TURIBDI**, shunchaki qayta e'lon qilinmayapti.

⚠ Xavf: **yangi/bo'sh qurilma** birinchi marta ulansa oplogni noldan o'qiydi
va o'sha axlatni oladi. Bu v172.28 gacha ham shunday edi, yangi emas.

Tozalash yo'li (yozilmagan): ⬆ ni **ko'zgu** qilish — `ref.get()` bilan
oplogdagi hujjatlarni o'qib, mahalliyda YO'Q bo'lganlariga `deleted:true`
qo'yish (~12–16 qator, faqat `syncFullFill` ichida). Ibrohim hozircha
tanlamadi. ⚠ Kuchli amal: ⬆ bosilgan qurilmada bo'lmagan yozuv HAMMA joydan
o'chadi — faqat to'g'ri ma'lumotli qurilmada bosish mumkin, tasdiq oynasi
bilan qilish tavsiya etilgan.

### 0m. 2-CHI CHEK (ostatka jadvali) — FAQAT SOTUVDA (v172.35)

Rasm (raster) yo'li bilan bosiladi: `print_server.py` `/print-table` →
PIL 576 px rasm → `GS v 0`. Sotuv modalida chap tarafda `ostatka` toggle,
sukut bo'yicha **o'chiq**.

⚠ **2026-08-14 — Ibrohim: «ishimiz ko'p, hali men aytgandek holatga kelmadi,
uniyam qayerga kelganini ko'rsatishi kerak».** Bu jumla **TUSHUNILMADI** —
taxmin qilib kod yozilmadi. Uch variant so'raldi, javob kutilmoqda:
**A** har qator qaysi turdan kelganini · **B** grammning sababi (berildi/vozvrat/
to'lov/ostatka) · **C** ostatka qayerga ketgani (klientda/zavodga/sotildi).

⚠ Shuningdek `_ostJadvalUstunlar` (14397) da **0q dagi offset xatosi bor** —
0q bo'limiga qara.

**Qolgan 3 modal QILINMAGAN:** berish (`kb`), vozvrat (`kv`), to'lov (`kt`).
Ularda ham `chekYubor` yonida `chekJadvalYubor` chaqirilishi va toggle
qo'shilishi kerak — har biri ~12–15 qator.

⚠ **print-server QAYTA ISHGA TUSHIRILISHI SHART.** Eski server yo'lni
tekshirmaydi va jadval so'rovini matnli chek deb oladi → yolg'iz **logo**
chiqadi. Bu belgini ko'rsangiz — server eski. Tekshirish:
`POST /print-table` bo'sh `ustunlar` bilan → yangi server
`{"status":"ERROR: ustunlar bosh"}` qaytaradi.

⚠ Shakllantirish yorlig'i 2-chi chekda **tuzatilmagan** — `_ostJadvalUstunlar`
da hali `berildi` deb chiqadi (PDF va ilovada v172.41/42 da tuzatilgan).

### 0l. ~~PDF DOWNLOAD~~ — ISHLAYAPTI (Ibrohim tasdiqladi 2026-08-14)

Ibrohim: «pdf yuklavotti... hozir yuklavotti, ishlavotti bu funksiya».
Qolgan 6 joy hali eski yo'lda (`window.open(blobUrl)`) — **2934** kurs tarixi ·
**9640** zavod/tur · **10961** kassa · **11017** to'lov hisoboti ·
**16720** qarz cheki · **17174** klientlar ro'yxati. Muammo ko'rinmagani uchun
**tegilmadi**. Kerak bo'lsa har biri 1 qator (`pdfOch(blob,'<nom>')`).

Ibrohim aytgan «pdf offset nimaligini tushunmayapti» — bu 0l EMAS,
**0q dagi Xato B** edi, v174.4 da tuzatildi.

<details><summary>Eski yozuv (arxiv)</summary>

Sabab: `window.open(blobUrl)` `fetch().then()` ichida — brauzer popup deb
bloklaydi; ustiga `revokeObjectURL` 10 s da chaqirilib, Chrome PDF
ko'ruvchisidagi «Download» tugmasi «internetga ulanmagan» berardi.
Yechim: `pdfOch(blob, nom)` — `<a download>`, blob 10 daqiqa tirik.

**Qolgan 5 joy TEGILMAGAN** (Ibrohim so'ramadi), hammasida xuddi shu muammo:
`9560` zavod/tur hisoboti · `10879` kassa PDF · `10935` to'lov hisoboti ·
`16617` klient qarz cheki · `17010` klientlar ro'yxati.
Har biri **1 qator** — `pdfOch(blob, '<nom>')` ga o'tkazish.
</details>

### 0k. CLOUD 1:1 — 3-QADAM QOLDI (ASOSIY qurilma rejimi)

2026-08-10 da Ibrohim: "cloudga boshqa qurilmala tupurib qo'ygan", "PC asosiy
bo'gani bilan **teldigi malumotlayam ishlatilvotganida** tori bo'ladi".

**2026-08-14 tasdiq:** «asosiy qurilma haliyam PC, lekin cloudda hammada bir xil
bo'lishi kerak, mobile qurilmalar ham asosiy qurilmadek ishlashi kerak minus
plyuslar qilinganda. Abdulhamid logiga umuman ta'sir qilishi kerak emas.»

✅ **Bu talab bajarilishi mumkin** — chunki ikki xil sinxron bor:
- **Yozuvlar (oplog)** — har berish/to'lov/vozvrat bittalab, HAR qurilmadan.
  ASOSIY rejimi bunga **TEGMAYDI**. Telefondagi +/− avvalgidek hamma joyga yetadi.
- **Blob (butun nusxa)** — kim oxirgi yozsa o'shaniki. ASOSIY rejimi **FAQAT shunga**.

Ochiq savol qoldi: ASOSIY = 1-raqamli qurilma avtomatmi yoki Sozlamalarda
qo'lda belgilanadimi (qo'lda ishonchliroq — raqam almashib qolishi mumkin);
ergashuvchi jim olsinmi yoki xabar chiqsinmi.

Uch qadamli reja tuzildi:
- **1-qadam — BAJARILDI (v172.30 + v172.31).** Oplog teshiklari yopildi:
  tahrirlangan yozuv ham ketadi, belgi tasdiqdan keyin qo'yiladi, o'chirish
  navbati bor, `syncFullFill` yangi vaqt bilan yozadi.
  ⚠ **v172.30 da xato bor edi** — Ibrohim topdi (2026-08-11: «klient tarixiga
  kirib grammi tahrirlasam telda almashmayapti»). `_amalPushInit` urug'lash
  `amalSyncPush` ichida, ya'ni `save()` dan KEYIN ishlar edi va endigina
  tahrirlangan yozuvni «yuborilgan» deb muhrlab qo'yardi. `tilla-amal-push-init`
  bayrog'i ⬇ bosilganda o'chgani uchun har yuklanishdan keyin takrorlanardi.
  **v172.31 da tuzatildi:** urug'lash skript oxirida (sahifa yuklanganda,
  tahrirdan OLDIN) + `amalInit()` ichida. ⚠ **QAYTA SINALMAGAN.**
- **2-qadam — BAJARILDI (qo'lda).** PC da ⬆, qolganlarida ⬇. Ibrohim
  2026-08-10 da tasdiqladi: "hozircha bir xil" — qurilmalarda ma'lumot mos.
- **3-qadam — QOLDI.** ASOSIY qurilma rejimi, mockup tayyor:
  `mockups/v172.30-asosiy-qurilma.html`. Ikki kichik o'zgarish:
  - `cloudSaqlaNow` (~18009): `if(!qurilmaAsosiy()) return;` — faqat ASOSIY
    blob yozadi. **1 qator.**
  - `cloudListen` (~17830): ergashuvchi blobni AVTOMAT oladi. **1–3 qator.**

  Hozirgi holat: `qurilmaAsosiy()` (17655) butun faylda **bitta joyda** —
  Cloud holati oynasidagi ko'k «ASOSIY» yorlig'ini chizishda (17776).
  Sinxronga ta'siri **nol**.

  ⚠ 3-qadamni 1-qadam **sinovdan o'tmasdan** yoqmang — telefondagi yozuv PC ga
  yetmasa, avtomat kelgan blob uni o'chirib yuboradi.

  ⚠⚠ **ABDULHAMID — CLAUDE.md §6.** Ibrohim (2026-08-11): «bu narsala abdulhamid
  logiga tasir qimasin umuman». `qurilmaRoyxatgaQosh` (17776) hamid qurilmasini
  ro'yxatga QO'SHMAYDI → `qurilmaRaqam()`=0 → `qurilmaAsosiy()`=**false**.
  Demak oddiy `if(!qurilmaAsosiy()) return;` hamid qurilmasini cloudga
  yozishdan BUTUNLAY to'xtatadi. Shart majburan shunday bo'lsin:
  `if(!_qurilmaHamid() && !qurilmaAsosiy()) return;`
  Xuddi shu `cloudListen` dagi avtomat yuklashga ham tegishli — u yerda
  17825 (`cloudQurilma`) qolipidagidek hamid ESKI YO'LDA qolishi kerak.

  Tekshirilgan (2026-08-11): v172.29/30/31 hamid kodiga **tegmagan** —
  `git diff 9ddd144..HEAD -- index.html | grep -i hamid` bo'sh.

  Ochiq savollar (mockupda): ASOSIY = `qurilmaRaqam()===1` qoladimi yoki
  Sozlamalarda qo'lda belgilanadimi; ergashuvchi jim olsinmi yoki xabar
  chiqsinmi; ergashuvchida kassa tahriri bloklansinmi.

### 0j. Kassa qurilmalar orasida SINXRON EMAS — hal qilinmagan

`amalWalk` (7959-7962) izohi: «data.kassa — OBYEKT, oplogga kirmaydi, blob
orqali sinxron bo'ladi». Lekin blob **yuklab olinmaydi** (`cloudListen` 17829:
faqat bo'sh qurilma oladi). Demak kassa amalda **umuman sinxron bo'lmaydi**.

Ikki yo'l bor, ikkalasi ham katta qaror:
- **K1.** Blobni davriy yuklash — xavfi yuqori, ikki qurilma bir vaqtda
  ishlasa biri ikkinchisini bosib ketadi (v93 da aynan shuning uchun o'chirilgan).
- **K2.** Kassani oplogga chiqarish — ko'p kod, alohida versiya.

Hozircha ⬆/⬇ qo'lda. 3-qadam (0k) bajarilsa K1 ning xavfsiz shakli chiqadi.

**2026-08-14 — Ibrohim: «asosiy qurilma baribir PC».** Demak **K1** tanlandi.
⚠ Buning narxi ochiq aytilgan: kassa oplogdan o'tmaydi (8144 — obyekt, massiv
emas), shuning uchun **telefonda kiritilgan kassa tuzatishi PC ga yetmaydi va
PC dan nusxa kelganda yo'qoladi**. Ya'ni kassa tuzatishlari / zakazlar /
chiqimlar **faqat PC dan** kiritilishi kerak bo'ladi. Ibrohim buni tasdiqlashi
kerak — agar telefondan ham kerak bo'lsa, K2 (kassani oplogga chiqarish) zarur.

### 0g. ~~MAVJUD takror yozuvlarni tozalash~~ — YOPILDI (Ibrohim qo'lda tuzatdi)

**2026-08-14, Ibrohim:** «takror yozuvlarni men to'g'irlab qo'ydim, grammlarni
tekshirib. Bundan keyin bo'lmasa bo'ldi.»

Tozalash kodi va sanash buyrug'i **kerak emas**. Paydo bo'lishi v172.27 da
to'xtatilgan (`_id` saqlashdan oldin beriladi, cloud nusxasi `_ostImzo` (8290)
bo'yicha egizakni topib unga id yopishtiradi).

⚠ Kuzatilsin: yana takror ko'rinsa — sabab boshqa joyda, qaytadan qidirish kerak.

<details><summary>Eski yozuv (arxiv)</summary>

v172.27 da takror **paydo bo'lishi** to'xtatildi, lekin allaqachon yozilganlari
ma'lumotda turibdi. Ular klient qarzi, hisobot, foyda va kassani buzadi
(Asror Aka 23, 09.08 14:55 — berish 41.56 o'rniga 83.12, to'lov $7,428 o'rniga
~$3,714, skidka 1.56 o'rniga ~0.78).

Tozalash qoidasi tayyor: bir massivda `_ostImzo` si bir xil, **bittasida `_id`
bor / ikkinchisida yo'q** juftlikdan `_id` siz nusxa o'chiriladi. Ikkalasida ham
o'z `_id` si bor yozuvlarga TEGILMAYDI (haqiqiy ikki amal bo'lishi mumkin).
Tartib: ro'yxat ko'rsatish → backup → o'chirish.

Ibrohimga sanash uchun konsol buyrug'i berilgan, natija hali kelmagan.
</details>

### 0h. ~~Sinxron: "yuborildi" belgisi tasdiqdan OLDIN~~ — BAJARILDI (v172.30)

`amalSyncPush` / `amalDeletePush` / `amalMovePush` da `.set()` chaqirilgach
darhol `set[id]=vaqt` qilinardi, `.catch` faqat konsolga yozardi.

**BAJARILDI v172.30 da.** Belgi endi faqat `.then()` da (`_amalPushTasdiq`).
Yuborish uchun **alohida** ro'yxat `tilla-amal-push` = `{id: imzo}` — `set[]`
formati tegilmadi (qabul yo'nalishi buzilmasin). O'chirish uchun navbat
`tilla-amal-ochir-navbat`, har `save()` da qayta urinadi, 7 kunda tashlanadi.
⚠ **SINOVDAN O'TMAGAN** — 0k dagi sinov rejasiga qarang.

### 0f. Eski (soatsiz) offset yozuvlari — KICHRAYDI, lekin qoldi

⚠ **2026-08-14 aniqlik:** Ibrohim «offsetda muammo bor» deganda **bu emas**,
**0q** (ikki marta hisoblanishi) nazarda tutilgan edi — u v174.4 da tuzatildi.

Soat masalasi **hali turibdi** va endi yana bir joyda chiqadi: v174.5 dagi PDF
o'qlari `sana|soat` bo'yicha bog'lanadi. Soati yo'q yozuvda o'sha kunda bir
nechta to'lov bo'lsa — bog'lash ishonchsiz, shuning uchun **o'q chizilmaydi**
(`_ofOq`, 16965). Raqamlarga ta'siri YO'Q, faqat yorliq ko'rinmaydi.

v172.25 da offset yozuviga `soat` qo'shildi, lekin faqat **yangi** yozuvlarga.
Undan oldin saqlangan `_kdYopish` yozuvlarida soat **umuman yo'q** — sessiya
kaliti (`ki|sana|soat`, 9711) bo'yicha ular o'sha kundagi bitta guruhga
yopishib qoladi va boshqa to'lovga qo'shilib ko'rinadi (Marhabo Opa TJK,
06.08 · 15:20 vs 15:22 misoli).

Yechim yo'nalishi: o'qish paytida soati yo'q offsetni o'sha sana + o'sha
zavod·tur bo'yicha to'lov qatoriga bog'lash (offset yozuvida `zavod`/`tur`
saqlangan). Nozik joyi — bir kunda bir xil turga ikki to'lov bo'lsa qaysi
biriga bog'lash. Ibrohim: "alohida mockup bilan qil".

### 0e. Dona bazaga to'liq o'tish — PLAN.md da (yangi, v172.13)

Dona baza chernovikda. Qachondir to'liq o'tiladi — qilinadigan ishlar
ro'yxati (X1–X7 xatolar, qaytadan shakllantirish, bayroq yoqish) **PLAN.md** da.
Bayroq: `DONA_BAZA_UI` (1966). Yoqishdan oldin PLAN.md 1-qadami shart.

### 0d. ~~QARZ TARKIBI paneli «Jami» mos emas~~ — BAJARILGAN BO'LIB CHIQDI

2026-08-05 da tekshirildi: mockupdagi taklif **v172.12 da allaqachon
bajarilgan** (`_qarzJamiRows` 15980 atrofi, panel 11157, PDF 16062, tepadagi
blok 11129). Bu yozuv eskirgan edi. Prodda ko'rinmasligining sababi —
v172.12 push qilinmagan, prod v172.11 da. Mockup
`mockups/tashxis-qarz-cheki-jami.html` endi arxiv — o'chirsa bo'ladi.

### 0b. Vozvrat donasi keyin "berilgan" bo'la olmaydi — QAROR KUTILMOQDA

Ibrohim v172.11 da aytdi: "vozvrat bo'gan zavodga qaytgan bo'sa ko'rsatsin
toki berilgan bo'magunicha" — ya'ni vozvrat donasi keyin berilgan bo'lishi
kerak. Hozir `donaBazaHolat` (8049) faqat `holat==='ombor'` bo'lgan donani
o'zgartiradi, shuning uchun vozvrat donasi o'sha holatda qotib qoladi.

Ochilsa yana bir savol: `donaBazaOmbor` / `donaBazaMosEmas` (7976, 7978) ham
vozvratni omborda deb hisoblasinmi? Zavodga vozvrat qilingan dona jismonan
bizda emas — shuning uchun bu oddiy shart o'zgarishi emas.

### 0c. v172.10 — bajarilmagan (raqam bo'sh qoldi)

Sotuv chekida BIZNING qarzimiz ko'rinmasligi (eskiOstMap `>0.001` filtri,
15035 va 15357) + berish chekiga Ostatka jadvali qo'shish. Mockup tayyor
edi va Ibrohim tasdiqlagan (ishora: `+2 / −5 = −3`, qoldiq 0 bo'lsa ham
ko'rsatilsin), lekin kod yozilmadi — dona baza ishi oldinga o'tdi.
Mockup fayli o'chirilgan, kerak bo'lsa qaytadan qilinadi.

### 0a. Klient ostatka shakllantirish — "ustiga/boshqattan" dialogi YO'Q

v172 da zavod tomoniga qo'shildi, klient tomoni (ostKlSaqla, "✓
shakllantirilgan" belgisi 6111 atrofida) Ibrohim qarori bilan keyinga
qoldirildi. Klient tomonida qayta shakllantirish hozir ham eski usulda
ishlaydi — dialog yo'q.

### 0. O'lik kod — tashxis tayyor, o'chirish KEYINROQ (Ibrohim qarori)

47 funksiya hech qayerdan chaqirilmaydi — to'liq ro'yxat guruhlari bilan:
`mockups/v171.7-tashxis-olik-kod.html`. Ibrohim: "hozir o'chirmaymiz —
keyinroq". Tashxisdagi takroriy e'lonlardan `kh*` to'qnashuvi v171.8 da
tuzatildi; `lblOf`/`balansOf`/`sanaToDt` lokal chiqdi (xavfsiz, tegilmadi).
Diqqat: o'chirish paytida qator raqamlari siljiydi → CLAUDE.md §6/§10
raqamlarini yangilash kerak bo'ladi.

### 1. Lom narxi chekda 73.1, saqlanganda 73 — SABAB TOPILMAGAN

Zulfiya Opa Andijon, 31.07.2026. Chekda `108.93 g × 73.1 = 7,962.78 $`,
tarixga `108.93 × 73 = 7,951.89 $` tushgan. Farq **10.89 $** — bu sdachani
12.77 g dan 12.63 g ga tushirgan.

Tekshirilgani: chek chizuvchi ham, saqlovchi ham **aynan bir xil maydondan**
(`kt-lk-<i>`) **aynan bir xil usul bilan** (`parseNum`) o'qiydi. `parseNum`
da vergul himoyasi bor — `73,1` to'g'ri o'qiladi.

Demak qiymat **chek chizilgandan keyin, Saqlash bosilgunicha** o'zgargan.
Taxmin bilan kod o'zgartirilmadi.

**Ibrohimdan kutilmoqda:** takrorlash. Lom narxini **nuqta bilan** kiritib,
keyin boshqa maydonga tegmasdan saqlash. Farq chiqadimi-yo'qmi.

### 2. Eski ikkilangan sdacha yozuvlari tozalanmagan

v171.3 da sabab tuzatildi (ikki joydan yozilardi), lekin **allaqachon
yozilganlari turibdi**. Zulfiya Opada ortiqcha **+12.63 g**. Boshqa
klientlarda ham bo'lishi mumkin — sdacha qaytarilgan har to'lovda.

Avtomatik tozalash **qilinmadi, ataylab** — ikkita bir xil yozuv haqiqatan
ham ikki alohida amal bo'lishi mumkin. Qaror Ibrohimdan: topib ko'rsatish
kerakmi, yoki qo'lda o'zi o'chiradimi.

### 3. `klientQarzSplit` da sdacha turga ajratilmaydi

v171.3 da `_qarzTarkib` tuzatildi — Qarz tarkibi panelida sdacha endi o'z
turi ostida ko'rinadi. Lekin `klientQarzSplit` da hali ham:

```js
else if(op.tip==='klientda') bizQarzi += op.gramm;   // umumiy qopga
```

Ya'ni tur bo'yicha emas, to'g'ridan-to'g'ri umumiy "bizning qarz" ga.
Ibrohim panel haqida aytgan edi, faqat o'sha tuzatildi. Bu tegilmadi.

### 4. Sotuv va berish yozuvlari farqlanmaydi

`saqlashKlientBerish` va `saqlashKlientSotuv` ikkalasi ham bir xil
`tip:'berish'` yozadi — maydon-maydon farqsiz.

Koddan tasdiqlangan holat:
* `manba:'sotuv'` — butun faylda **0 marta yoziladi**
* `_sotuv:true` — **hech qachon yozilmaydi**
* Lekin `haftaOstData` (6239, 6246-qatorlar) ikkalasini ham **o'qiydi**
  → natija **doim `false`**
* Dona bazadagi `holat:'sotilgan'` — **0 marta qo'yiladi**

To'lov cheki sharti `if(s>0 && n>0)` — qarzga sotuv (Ibrohim tasdiqlagan
odatiy holat) belgisiz qoladi.

Bu masala bo'yicha eski mockuplar bor edi, lekin ular **saqlanmadi va
kerak emas** — v170 holatiga tayangan, qator raqamlari eskirgan.
Ish boshlanganda tahlil **qaytadan**, hozirgi koddan qilinadi.
Qaror qabul qilinmagan.

---

## Oxirgi versiyalar (qisqacha)

| Versiya | Nima qilindi |
|---|---|
| v176.5 | **Chekda offset sdachasi** — manba turi qarzi yopiladi + «Naqt qaytarildi → tur» qatori (ikkala chek) |
| v176.4 | **Sdacha ro'yxatida faqat klientda turgan turlar** — qarzi yo'q va biz qarzdor turlar chiqmaydi (`sdachaTaqsimRender` 13584) |
| v176.3 | **Offset ortig'i sdacha panelidan o'tadi** → «naqt qaytardim» kassaga `Offset sdacha` chiqimi (kim + nimadan) |
| v176.2 | **Uzun son yaxlitlandi** (4 joy) + **to'lov chekida naqt ko'rinadi** (13950) |
| v176.1 | **Sotuvda offset tugmasi o'zi yonadi** (A varianti, `kSotuvRenderTolov` 14687) |
| v176 | **Skan oynasi bir vaqtda bitta** — vozvrat/sotuvda ham (`_skanUniYop` 12745) |
| v175.5 | **Nol farqda tarixga yozuv yozilmaydi** (`ostFormSaqla` 8712) |
| v175.4 | **Ostatka tekshiruvi hisobotda ko'rinmaydi** (`renderHisobot` 5134, `renderZavodHisobot` 6066) |
| v175.3 | **Klient PDF tepa katagi: KLIENT OSTATKASI + BIZNING QARZ alohida** (A varianti) |
| v175.2 | **Klient qarzi hamma joyda bir xil** — `klientJamiQarz` endi `_qarzTarkibRows` dan (Madina Opa: 0.66 → 0.00) |
| v175.1 | **Qarz chekida zavod ostidagi «Jami:» qatori olib tashlandi** (`pdf.py` 333) |
| v175 | **PDF «Qarz tarkibi» va JAMI qatori ilovadagi bilan bir xil** — `qarz_bd` olib tashlandi, `_qarzTarkib` chaqiriladi |
| v174.9 | **PDF tepa jadvalida offset ko'rinadi** — «Offset» sarlavhasi (binafsha) + Tur ustunida `→ / ←` o'qlar |
| v174.8 | **PDF tepa jadvali Ostatka ustuni** — offset ayirilardi, endi qo'shiladi (`runBal` 16922) |
| v174.7 | **Xato C** — `v.offset` ikki yo'ldan qo'shilardi, endi `max(manba, ayirma)`; ayirma `_opOffUlush` ga o'tdi; `ofNom` manbadan |
| v174.6 | **2-chi chek jadvalida ham offset xatosi** tuzatildi (`_ostJadvalUstunlar` 14410) |
| v174.5 | **Offsetning ikki tomoni bir-birini ko'rsatadi** — klient tarixida manba qatori (avval `false &&` bilan o'chirilgan edi) + manzilga `←`; PDF da `offset → 3D, 3DS` va `tolov ← Oddiy`; `pdf.py` da binafsha rang |
| v174.4 | **OFFSET IKKI MARTA hisoblanardi** — klient tarixida pul $9,144.34 (to'g'risi $4,572.17), PDF kunlik blokida QOLDI +105.96g (to'g'risi 0.00g) |
| v171 | "Qo'limizdagi ostatka" ekrani — zavod→tur→gramm, hafta bo'yicha |
| v171.1 | Hafta zanjiri tuzatildi (hafta oxiri = bugungi ostatka − keyingi harakatlar) |
| v171.2 | Sdacha `soat` ga Date obyekti yozilardi → tuzatildi + bir martalik migratsiya (`data._soatFix1`) |
| v171.3 | Sdacha **ikki marta** yozilardi → takror blok o'chirildi; `_qarzTarkib` ga `klientda` qo'shildi |
| v171.4 | Klient hisoboti va kassa — kunlar yig'ilgan, bugun ochiq; hisobotga filtr (Berildi/Vozvrat/Tolov) |
| v171.5 | Zavod skanida fokus — × va rejim almashishda kiritish maydonida qoladi |
| v171.6 | Vozvrat/sotuv skani berish darajasiga ko'tarildi (1/2-skan, ro'yxat, ×) |
| v171.7 | Chip ro'yxati + 2-skan chek-ro'yxat — uchala modalda bir xil |
| v171.8 | `kh*` global to'qnashuvi (v171.4 dan): klient hisoboti `khr*` ga ko'chdi, kassa kh-filtr paneli tuzaldi |
| v171.9 | Vaqt mashinasi / nollash parol maydonlari: type="text" + CSS maska — Chrome parol-ro'yxati chiqmaydi |
| v172 | Qayta shakllantirishda "USTIGA / BOSHQATTAN" modal; ustiga-yo'lning registr/dona-baza bug'i tuzatildi; boshqattan faqat orada harakat bo'lmaganda (aks holda Tekshiruvga yo'naltiradi) |
| v172.1 | Ostatka formi dizayni skan-kirim uslubiga o'tkazildi (2 karta, kirim tugma/maydon uslublari) — sof vizual |
| v172.2 | Ostatka skanida × bosilganda fokus maydonda qoladi (ostSkFokus — kirimdagi v171.5 skFokus nusxasi) |
| v172.3 | Abdulhamid loginida kassa v171.3 oddiy ketma-ketligiga qaytarilgan edi (§6 istisno) |
| v172.4 | v172.3 BEKOR (Ibrohim: "kerak emas ekan") — kod v172.2 bilan bayt-ma-bayt bir xil, hamid o'zgarishsiz |
| v172.5 | Sotuv chekida offset (O) va karta/perech (K/P) alohida ko'rsatiladi — avval hammasi N bo'lib chiqardi |
| v172.6 | Offset umumiy summadan ayirilib ko'rsatiladi: `Umumiy Summa → Skidka → Offset → Kerakli summa`. Ikkala chek (sotuv + to'lov) bir xil qolipga keldi |
| v172.7 | `Qoldi 0` chiqmaydi; to'liq yopilganlar tepada, qoldig'i borlar pastda — ikkala chekda bir xil |
| v172.8 | «KLIENTDA BOR» paneli: offset endi RESURS (Jami ga kiradi), tarqatma emas → `Oshdi 100.04$`. Yangi OFFSET katakchasi, ikkala modalda |
| v172.9 | Sotuv chekida boshqa turning eski qarziga to'langan pul ko'rinadi (avval chek 160$ kam summa yozardi — pul xatosi) |
| v172.11 | Dona bazasi kataklik: bir xil gramm+holat `×N` bo'lib birlashadi, sana sarlavhasida sanoq, sanalar yopiq ochiladi |
| v172.12 | Sotuvda offset avtomat yeyilgani chekda ko'rinadi (Berildi minussiz, «Qoldi» o'rniga izoh, Ostatka manfiyni oladi) + «Qolgan qarz» 52.78 → 47.36 |
| v172.13 | Dona baza CHERNOVIK rejimiga chiqarildi (`DONA_BAZA_UI=false`, 11 qo'riqchi), PLAN.md yaratildi |
| v172.14 | «Qo'limizdagi ostatka» B usuli: hafta boshi tarixdan, `t.ostatka` o'qilmaydi; yangi qator tartibi JAMI bilan |
| v172.15 | admin/admin123 — ADMIN sandbox xonasi (TEST mexanizmi nomlangan sandboxga umumlashdi, cloud `ADMIN_tilla_<uid>`) |
| v172.16 | Shakllantirishga 📅 Sana maydoni (zavod + klient) — orqaga sana bilan shakllantirsa bo'ladi, klientdan klientga saqlanadi |
| v172.17 | Zavodlar tartibi qo'lda: ⇅ Tartib rejimi, ↑↓ tugmalar; gramm bo'yicha avto-saralash o'chirildi |
| v172.18 | JAMI dan BIZNING QARZIMIZ ayiriladi (tur + zavod + bosh ekran) — 1376.10 → 1300.12 |
| v172.19 | KLIENTDA ning o'zi ham sof: 615.08 − 75.98 = 539.10; jami yana oddiy qo'shuv (ikki marta ayirmaslik uchun) |
| v172.20 | Sandbox belgisi (🧪 ADMIN/TEST XONASI) pastdan tepa markazga — adashib sinov xonasida ishlamaslik uchun |
| v172.21 | Tahrirda sana qo'shni to'lovga ham yozilardi — ✏ tugmaga va filtrga soat sharti qo'shildi |
| v172.22 | Sana keyin o'zgartirilsa chek yangilanmasdi — berish/vozvrat/to'lov sana maydonlariga onchange qo'shildi |
| v172.23 | Kurs avto-saqlanadi (Saqlash tugmasi o'rnida «Kunlik kurs» ko'rinadi) + kategoriya har amalda A dan boshlanadi, klientga yozilmaydi |
| v172.24 | Offsetdan yopilgan to'lov tarixda va hisobotda «⇄ Offset» bo'lib ko'rinadi (ayirma bilan aniqlanadi, eski yozuvlarga ham ishlaydi) |
| v172.25 | Lom hisobotda o'z to'lovida ko'rinadi (kalitga soat) + offset yozuviga soat qo'shildi |
| v172.30 | **Oplog teshiklari yopildi** — tahrirlangan yozuv ham ketadi (imzo bo'yicha), belgi tasdiqdan keyin, o'chirish navbati, `syncFullFill` yangi vaqt bilan. Telefondagi yozuv PC ga ishonchli yetadi |
| v172.29 | **Chek 1 bosilib 7 chiqardi** — sabab: belgi faqat bulutda edi, token rad etilib lokal kesh orqaga qaytardi (halqa). Lokal `tilla-chek-chiqdi` ro'yxati + muddat 90s + telefonda haqiqiy javob |
| v174.3 | Zavod ichidagi hisobotda **vozvrat tafsiloti «−NaN g»** chiqardi — eski xato, `op.jami` o'rniga `op.gramm` |
| v174.2 | **Bosh ekran Hisoboti kun bo'yicha** guruhlanadi + Kirim/Vozvrat/Chiqim filtr chiplari |
| v174.1 | **Aralash sotuvda naqt yo'qolishi tuzatildi** — eski yozuvlar o'qishda qoldiqdan (`_opNaqtPul`), yangi sotuvda maydon bo'sh bo'lsa o'zi to'ldiriladi |
| v173.2 | Kassa panelida «Naqt» qatori ko'rinmasdi (v174.1 da yagona joyga ko'chirildi) |
| v173.1 | **v172.44 BEKOR** — zavod ichidagi hisobot v172.43 holatiga qaytarildi (noto'g'ri ekran o'zgartirilgan edi) |
| v173 | **BOSQICH BELGISI** — kod v172.44 bilan bir xil, faqat raqam ko'tarildi |
| v172.44 | **Zavod hisoboti kun bo'yicha** guruhlanadi + Kirim/Vozvrat/Chiqim filtr chiplari (klient hisoboti qolipi) |
| v172.43 | Blokda **«boshi 0.00g» qatori chizilmaydi** (0 dan boshqa bo'lsa qoladi) + PDF **tepadagi jadvalda** shakllantirish «Ostatka» (oltin) |
| v172.42 | Ilovada ham shakllantirish «Berildi» emas **«Ostatka»** — 4 joy (hisobot ekrani, klient tarixi, kun-sessiya, kun tahriri), rangi kulrang |
| v172.41 | PDF blokida shakllantirish «berildi» emas **«ostatka»** (oltin), `inventar:'boshlangich'` bo'yicha ajratiladi |
| v172.40 | PDF blokida oxirgi qoldiq rangi — klient qarzdor **qizil**, biz qarzdor **`+` yashil**, nol qora |
| v172.39 | **Klient PDF ga «Zavod·tur bo'yicha kunlik ostatka» bo'limi** — har tur alohida blok, kunlik amallar va kun oxiridagi qoldiq (v172.34 raqami bo'sh qoldi) |
| v172.38 | `pdfOch` — blob 10 daqiqa tirik qoladi, aks holda Chrome «Download» tugmasi «internetga ulanmagan» berardi |
| v172.37 | Klient PDF yuklab olinmasdi — `window.open(blob)` popup deb bloklanardi, `<a download>` ga o'tkazildi |
| v172.36 | Jadval payloadiga `logo:false` himoyasi — eski print-server yo'lni tekshirmay yolg'iz logo chiqarardi |
| v172.35 | **2-CHI CHEK — ostatka jadvali RASM (raster)** qilib bosiladi, sotuv modalida `ostatka` toggle (sukut bo'yicha o'chiq) |
| v172.33 | Sotuv chekida to'langan ostatka ko'rinadi — «jami» to'lovni ayiradi, ostiga «ostatka ham to'landi ✓» |
| v172.32 | `syncFullFill` eski vaqtga qaytarildi — cloudda qolgan **belgisiz axlat** qayta e'lon qilinmaydi |
| v172.31 | **v172.30 xatosi tuzatildi** — urug'lash `save()` dan keyin ishlab tahrirni «yuborilgan» deb muhrlardi; endi sahifa yuklanganda |
| v172.30 | **Oplog teshiklari yopildi** — yuborish ro'yxati imzo bo'yicha (tahrir ham ketadi), belgi tasdiqdan keyin, o'chirish navbati, `syncFullFill` yangi vaqt bilan |
| v172.29 | **Chek takrori tuzatildi** — lokal «chiqarildi» ro'yxati (bulutga bog'liq emas), muddat 90s, telefonda haqiqiy javob |
| v172.28 | **Telefondan chek → PC dan chiqadi** — Firestore chek navbati, Sozlamalarda printer kaliti |
| v172.27 | **Takror yozuv tuzatildi** — `_id` saqlashdan oldin beriladi + cloud nusxasi `_id` siz egizakni topib unga id yopishtiradi; sinxrondan keyin `renderHome` chaqiriladi (Update bosish kerak emas) |
| v172.26 | **BIZDA tarixdan** — «Jami qo'limizda» bilan 1:1, 18 joy o'tkazildi, 🔧 tugma o'chirildi. Qurilmalar orasidagi 199.49 g farq shu bilan yopiladi |

To'liq tafsilot — `CHANGELOG.md` (o'qimang, kerak bo'lsa Ibrohimdan so'rang).

---

## Muhim texnik joylar

**Skan tizimi (v171.7 dan keyin):**
* `_skanChipHTML(pass1, pass2, mode, oc)` — **umumiy chizuvchi**, uchala
  modal ham shundan foydalanadi. Ko'rinish o'zgarsa faqat shu yerda.
* Berish: `kbSkan*` (`_kbSkanState`, kalit `zi_ti`)
* Vozvrat/sotuv: `uniSkan*` (`_uniSkan`, kalit maydon id si)
* **`uniSkanDona` / `uniSkanArr` DOIM `pass1` dan** — 2-skan saqlashga
  ta'sir qilmaydi. Dona registri shunga bog'liq, buzmang.
* `uniSkan*` **5 joyda** chaqiriladi: klient vozvrat, to'lovdagi vozvrat,
  sotuv grammi, sotuvdagi vozvrat, ostatka vozvrati. API o'zgartirilmasin.

**Ataylab farqli qoldirilgan:** berishda `−` tugmasi **manfiy gramm
qo'shadi** (tuzatish uchun), vozvrat/sotuvda **oxirgisini o'chiradi**.
Sabab: manfiy gramm dona registriga tushib uni buzishi mumkin.

**Tegilmaydigan joylar — `hamid-x`** (snabjenets rolidan yashiriladi):
qatorlar **271, 342, 345, 377, 394, 1340**. Bularga tegmang.

**Yordamchilar:** `roundG`, `parseNum`, `fdSanaTs(sana,soat)`, `fmtG`,
`fmtD`, `esc`, `today()` (ru-RU DD.MM.YYYY), `skParseGram`, `skSum`,
`skMultiset`, `_skanSvg`, `_touchQurilma`.

---

## Rejalashtirilgan, hali kod yozilmagan

* **Yangi foyda modeli** — narx qatlamlari (Zavod%, A%, B=A+2$), foyda tur
  bo'yicha, chiqimda qulflanadi, LOM foydasi 100% kompaniyaniki
* **Haqiqiy Kassa** — uch cho'ntak, nol nuqta, lom ombori, zakaz muzlatish,
  999 arbitraji, ulush havzasi (pro-rata)
* **Abdulhamid diler tizimi** — alohida Firebase, ikki tomonlama sinx

Bularning hammasi **mockup/tahlil bosqichida**. Kod yozilmagan.

---

## Seans boshlash

### ⚠ BOSHQA KOMPYUTERGA O'TGANDA — avval `git pull`

Ibrohim ikki joyda ishlaydi: **uy PC** va **ishxona PC**. Loyiha GitHub'da
(`ibrohimcyborg/Tilla-ERP`), hamma narsa shu yerda sinxronlanadi —
`index.html`, `CLAUDE.md`, `DAVOM.md`, `CHANGELOG.md`, `mockups/`.

Yangi kompyuterda ish boshlashdan oldin:

```
cd "<loyiha papkasi>"
git pull
```

⚠ `git pull` xato bersa (lokal o'zgarish bor deb) — **o'zing hal qilma**,
Ibrohimga ayt. Eski kompyuterda saqlanmagan ish qolgan bo'lishi mumkin.

Papka umuman yo'q bo'lsa:
```
git clone https://github.com/ibrohimcyborg/Tilla-ERP.git
```

```
cd Tilla-ERP
claude
```

Birinchi xabar — doim shu:
> CLAUDE.md va DAVOM.md ni o'qi. POS 1.26 dan davom etamiz.

Boshqa hech narsa tushuntirilmasligi kerak. Kerak bo'lsa — bu fayl kam
yozilgan, tuzatilsin (CLAUDE.md §0.1).

**Har versiyadan keyin:** `/clear` qiling va yangi seans boshlang.
Uzun seans tokenni ko'p yeydi (har so'rovda butun suhbat qayta yuboriladi).

---

## Ish tartibi — Ibrohim telefonda, Claude PC da

Ibrohim ko'chada bo'lganda PC yoniq qoladi va ish shunday ketadi:

| Kim | Nima qiladi |
|---|---|
| **Claude (PC)** | mockup yozadi → **Artifact qilib chiqaradi** → havolani beradi |
| **Ibrohim (telefon)** | havolani ochadi, ko'radi — `"o'zgartir"` yoki `"yoz, push qil"` |
| **Claude (PC)** | kodni yozadi, sinaydi, commit + **push** qiladi |
| **Ibrohim (telefon)** | `tilla-erp.vercel.app` → `kassatest`/`kassatest` da sinaydi |

⚠ **Mockupni faqat `mockups/` ga yozib qo'yish YETMAYDI** — telefonda
ochilmaydi. Har mockup **Artifact** qilib chiqarilsin va havolasi berilsin.

⚠ **Chek** sinovi uchun PC da `print_server.py` ishlab turishi kerak —
chek planshetdan cloud navbatga ketadi, uni PC printerga beradi.

⚠ Telefondan **PC dagi seansga to'g'ridan yozib bo'lmaydi** (masofaviy
ulanish yoqilmagan). Seans uzilsa — yangi seans shu faylni o'qib davom etadi.
