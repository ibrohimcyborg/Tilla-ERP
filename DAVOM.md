# DAVOM.md — qayerdan davom etamiz

> Bu fayl **har seans boshida o'qiladi**. Ish qoidalari CLAUDE.md da.
> Har versiyadan keyin bu fayl **yangilanadi** — aks holda keyingi seans
> nimadan davom etishini bilmaydi.

**Oxirgi yangilanish:** v172.31 · 2026-08-11

---

## Hozirgi holat

| | |
|---|---|
| Versiya | **v172.31** (`index.html` birinchi qatorida `<!-- v172.31 -->`, `APP_VER` da ham) |
| Hajm | ~17,400 qator · ~1 MB · **~311k token** |
| Deploy | tilla-erp.vercel.app (GitHub: ibrohimcyborg) |
| Saqlash | localStorage `tilla-v2` + Firebase Firestore `tilla_<uid>` |
| Sinov | **TEST rejimi** — `TEST_tilla_<uid>`. v172.15 dan yana **ADMIN xonasi**: login admin/admin123, `ADMIN-` prefiks + `ADMIN_tilla_<uid>` cloud — bo'sh, Qo'limizdagi ostatkani boshidan tekshirish uchun. |
| Git | **v172.31 gacha push qilingan** (2026-08-11, Ibrohim ruxsati bilan) — prod v172.31. |
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

## Ochiq masalalar

Quyidagilar **hal qilinmagan**. Tartib — muhimligi bo'yicha.

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

⚠ **Ochiq xavf (v172.29 da yopilmagan):** 3–4 qurilmada ilova ochiq.
`chekBuQurilmadan()` sukut bo'yicha `!printerYoq()` — ya'ni **har qurilma
navbatni tinglayveradi**. `tilla-chek-chiqdi` ro'yxati faqat **bitta qurilma
ichida** ishlaydi. Ikki qurilmada printer bo'lsa chek ikki joydan chiqadi.
Yopish uchun alohida qaror kerak (masalan «chiqaruvchi qurilma» bulutda bitta
bo'lib belgilansin).

### 0k. CLOUD 1:1 — 3-QADAM QOLDI (ASOSIY qurilma rejimi)

2026-08-10 da Ibrohim: "cloudga boshqa qurilmala tupurib qo'ygan", "PC asosiy
bo'gani bilan **teldigi malumotlayam ishlatilvotganida** tori bo'ladi".

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

### 0g. MAVJUD takror yozuvlarni tozalash — SANASH KUTILMOQDA

v172.27 da takror **paydo bo'lishi** to'xtatildi, lekin allaqachon yozilganlari
ma'lumotda turibdi. Ular klient qarzi, hisobot, foyda va kassani buzadi
(Asror Aka 23, 09.08 14:55 — berish 41.56 o'rniga 83.12, to'lov $7,428 o'rniga
~$3,714, skidka 1.56 o'rniga ~0.78).

Tozalash qoidasi tayyor: bir massivda `_ostImzo` si bir xil, **bittasida `_id`
bor / ikkinchisida yo'q** juftlikdan `_id` siz nusxa o'chiriladi. Ikkalasida ham
o'z `_id` si bor yozuvlarga TEGILMAYDI (haqiqiy ikki amal bo'lishi mumkin).
Tartib: ro'yxat ko'rsatish → backup → o'chirish.

Ibrohimga sanash uchun konsol buyrug'i berilgan, natija hali kelmagan.

### 0h. ~~Sinxron: "yuborildi" belgisi tasdiqdan OLDIN~~ — BAJARILDI (v172.30)

`amalSyncPush` / `amalDeletePush` / `amalMovePush` da `.set()` chaqirilgach
darhol `set[id]=vaqt` qilinardi, `.catch` faqat konsolga yozardi.

**BAJARILDI v172.30 da.** Belgi endi faqat `.then()` da (`_amalPushTasdiq`).
Yuborish uchun **alohida** ro'yxat `tilla-amal-push` = `{id: imzo}` — `set[]`
formati tegilmadi (qabul yo'nalishi buzilmasin). O'chirish uchun navbat
`tilla-amal-ochir-navbat`, har `save()` da qayta urinadi, 7 kunda tashlanadi.
⚠ **SINOVDAN O'TMAGAN** — 0k dagi sinov rejasiga qarang.

### 0f. Eski (soatsiz) offset yozuvlarini o'z to'loviga qaytarish — MOCKUP KERAK

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

```
cd Tilla-ERP
claude
```

Keyin:
> CLAUDE.md va DAVOM.md ni o'qi. v171.7 dan davom etamiz.

Keyingi safar shu ishni davom ettirish uchun — `claude -c`.

**Har versiyadan keyin:** `/clear` qiling va yangi seans boshlang.
Uzun seans tokenni ko'p yeydi (har so'rovda butun suhbat qayta yuboriladi).
