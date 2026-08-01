# DAVOM.md — qayerdan davom etamiz

> Bu fayl **har seans boshida o'qiladi**. Ish qoidalari CLAUDE.md da.
> Har versiyadan keyin bu fayl **yangilanadi** — aks holda keyingi seans
> nimadan davom etishini bilmaydi.

**Oxirgi yangilanish:** v171.8 · 2026-08-01

---

## Hozirgi holat

| | |
|---|---|
| Versiya | **v171.8** (`index.html` birinchi qatorida `<!-- v171.8 -->`, `APP_VER` da ham) |
| Hajm | 17,385 qator · ~1 MB · **~311k token** |
| Deploy | tilla-erp.vercel.app (GitHub: ibrohimcyborg) |
| Saqlash | localStorage `tilla-v2` + Firebase Firestore `tilla_<uid>` |
| Sinov | **TEST rejimi** — `TEST_tilla_<uid>`. Ishlab chiqarishda sinamaymiz. |

> **DIQQAT — faylni to'liq o'qib bo'lmaydi.** 311k token, kontekst oynasi 200k.
> Har doim `grep` bilan qidiring, keyin kerakli 20–50 qatorni o'qing.
> `CHANGELOG.md` (221 KB) — **hech qachon o'qilmaydi**, faqat yoziladi.

---

## Ochiq masalalar

Quyidagilar **hal qilinmagan**. Tartib — muhimligi bo'yicha.

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
