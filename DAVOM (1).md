# Tilla ERP — davom (v170 dan keyin)

Men Ibrohim, Tilla ERP (tilla-erp.vercel.app) egasiman. Single-file `index.html`,
vanilla JS, localStorage `tilla-v2`, Firebase Firestore. **APP_VER hozir v170.**

## ISH QOIDALARI (qat'iy)

1. **Hech qachon index.html ga to'g'ridan kod yozma.** LOGIKA / MAYDON / HISOB
   o'zgarsa avval MOCKUP (alohida vizual HTML) → men "ha" / "to'g'ri" / "boshla"
   deb tasdiqlagach → kod. Sof vizual o'zgarish uchun ham avval so'ra.
2. **ESKI VERSIYALARGA QAYTIB TAHLIL QILMA.** CHANGELOG faqat arxiv — yozasan,
   lekin eski yozuvlarni tahlil qilmaysan. Eski kod DALIL emas.
   **Faqat ikki manba:** (1) men hozir aytgan spetsifikatsiya, (2) index.html ning
   HOZIRGI kodi. Mavjud funksiyani CHAQIRISH yaxshi, eski QARORNI ko'chirish yomon.
3. **Yangi funksiya yozishdan oldin grep bilan tekshir.** id/maydon naqshlarini
   taxmin qilma, kodda tekshir.
4. Har mockup oxirida taxmin bloki: (1) aniq bilmayotgan joylarim, (2) taxminlarim
   (mendanmi yoki sendanmi — belgilab), (3) ta'sir qiladigan joylar (grep natijasi).
5. Versiya izohi CHANGELOG.md ga. Node sintaksis-sinov majburiy, keyin
   `present_files`.
6. **index.html ning ENG BIRINCHI qatoriga** `<!-- v171 -->` ko'rinishida versiya.
   Faqat raqam.
7. O'zgarishlar faqat TEST va asosiy rejimga — **Abdulhamid rejimiga qo'shma**
   (`hamid-x` klassi, `getRol()==='hamid'`).

## FAYLLAR
Ish nusxasi `/home/claude/w/index.html`, CHANGELOG `/home/claude/CHANGELOG.md`.

---

# 1. DARROV BOSHLANADIGAN ISH — Haftalik daftar

**Men tasdiqladim, savol yo'q, yozilsa bo'ladi.**

Mavjud **Haftalik ostatka** ekraniga (davr strelkalari, ikki karta, ochiladigan tur
qatorlari, PDF/Excel) **ikkinchi modal** qo'shiladi: **Umumiy oldi-berdi**.

Birinchi modal (klient oldi-berdisi) allaqachon bor — TEGILMAYDI.

## Ko'rinishi
Hozirgi Haftalik ostatka bilan bir xil uslub. Tur qatori bosilsa daftari ochiladi:

```
Butterfly                                        840.00
  Hafta boshi                                  1 000.00
  27.07  Zavod · kirim          +250.00        1 250.00
  28.07  Zavod · vozvrat         −60.00        1 190.00
         Klientga berildi  5 klient  −300.00     890.00
         Sotildi                 −80.00          810.00
         Klientdan vozvrat       +30.00          840.00
  = Qo'limizda                                   840.00
```

## Qat'iy qarorlar
* **FARQ YO'Q.** Sanoq bilan solishtirish qatori ham yo'q. Faqat harakat va qoldiq.
  Uning o'rniga **Qo'limizda** ko'rsatiladi.
* **Klient amallari YIG'ILADI** — bittalab chiqmaydi (spiska uzayib ketadi).
  Uch qator: Klientga berildi / Sotildi / Klientdan vozvrat. Yoniga nechta klient.
* **Zavod amallari sanasi bilan qoladi** — ular haftada bir-ikki marta.
* **Hafta boshidagi qoldiq = o'tgan hafta oxiri.** Saqlangan haftalik qoldiq yo'q,
  shuning uchun amalda: bugungi `t.ostatka` dan shu haftadagi harakatlar orqaga
  ayiriladi. Zanjir shunday quriladi.
* **Faqat GRAMM.** Dona ustuni yo'q — men "dona hozircha shart emas" dedim.

## Ochiq qolgan mayda savollar
* Yuqoridagi ikki karta nima ko'rsatsin — Claude `Qo'limizda` va `Farq` qilgan edi,
  farq olib tashlanadi. Ikkinchi karta nima bo'lishi aytilmagan.
* Sotuv "berildi" dan alohida yozilishi kodda tasdiqlanmagan — tekshirilsin.
* "5 klient" belgisi bosilganda ro'yxat ochilsinmi — ikkinchi qadam, hozir shart emas.

## Ma'lumot manbalari — koddan tasdiqlangan
```
Zavoddan kirim      t.tarix  tip:'mol'       sana + gramm
Zavodga vozvrat     t.tarix  tip:'vozvrat'   sana + gramm
Klientga berilgan   k.tarix  tip:'berish'    sana + gramm + zavod/tur
Klientdan vozvrat   k.tarix  tip:'vozvrat'   sana + gramm + zavod/tur
```
Klient harakatlari HAMMA klientdan yig'iladi.

**TUZOQ:** ostatka tekshiruv tuzatishi ham `tip:'mol'` bo'lib yoziladi
(`inventar` belgisi bilan). Ajratilmasa "Zavoddan kirim" ga qo'shilib ketadi va
daftar yolg'on chiqadi. Alohida qator qilinsin.

---

# 2. KEYINGI ISH — F (Ostatka ikki rejim)

**Men javob berganman, savol yo'q.**

Ostatka ekranida **Tekshiruv** rejimida Saqlash bosilganda ikki tugma chiqsin
(Dona baza ekranida allaqachon bor — `donaBazaTekshirSaqla`, o'sha mantiq
`ostFormSaqla` ga keltiriladi):

* **Shakllantirish** — skan = haqiqat. Eski ombor o'chadi. Hozirgi yagona yo'l.
* **Qo'shish** — bazaga TEGILMAYDI, faqat yangi topilganlar qo'shiladi.

**Nega kerak:** faqat yangi mol skan qilinganda hozirgi kod butun omborni o'chirib
yuboradi (10 dona 125 g → 3 dona 40 g, 85 g yo'qoladi).

**Ochiq:** ikki tugma faqat Tekshiruv rejimida chiqsinmi yoki Boshlang'ich
ostatkada ham (Claude: faqat Tekshiruvda, boshlang'ichda baza baribir bo'sh).

**Sana masalasi:** shakllantirish `donaBazaOmborOchir` bilan hamma ombor yozuvini
o'chirib, skanni bugungi sana bilan qayta yozadi. Dona baza ekrani sana bo'yicha
guruhlaydi, ya'ni zavod kirimlarining sanasi yo'qoladi. Uchinchi yo'l taklif
qilingan (mos kelgan donalar eski sanasi bilan qolsin) — men javob bermaganman.

---

# 3. QO'LDA BERISH — hal qilingan, kod o'zgarmaydi

Qo'lda gramm yozilganda kod `[gramm]` ni bitta soxta dona deb qidiradi, topmaydi,
hech narsa belgilamaydi. Dona registri buziladi.

**Bu muammo emas** chunki:
* Gramm hisobi dona bazasidan mustaqil — `t.ostatka` ayrim yuritiladi.
* Nomuvofiqlik faqat `ozConfirmOch` ogohlantirishi chiqaradi, "ha" desang amal
  odatdagidek yoziladi. Hech narsa to'smaydi, grammda ortiqcha paydo bo'lmaydi.
* Men: dona hozircha shart emas, haftalik shakllantirish tekislab boradi.

**Qaysi dona ketganini taxmin qilish MUMKIN EMAS** — 10 g / 4 dona uchun
2.3+2.7+3.1+1.9 va 4.1+3.1+1.9+0.9 va boshqalar bir xil natija beradi.
Bu yo'l butunlay yopildi.

---

# 4. BU SEANSDA QILINGANI (v168 → v170)

* **v168** — Panel yagona kirish joyi bo'ldi, 4 oyna bir qatorda
  (Naqt·Perech·Karta·Lom), tur qatori yorliqsiz 2 qator (`$` · summa · $/g ·
  gramm · ✓), Kerakli summa bloki 1 qator. **500$ naqd xatosi yopildi** — 300 naqd
  + 200 karta endi to'g'ri bo'linib saqlanadi.
* **v168.1** — `$` ustiga qo'shmaydi, klientda qolgan pulni yozadi. Lom oynasi
  bosiladigan bo'ldi (`Lom +`).
* **v168.2** — panel klient almashganda tozalanadi, avto-to'ldirish, sdacha.
* **v168.3** — **yashirin eski qatorlar**: `openKlientTolov` tur ro'yxatini
  yashirardi lekin tozalamasdi, yashirin `kt-s-*` lar "Taqsimlandi" ga qo'shilib
  ketardi. Eski xato, v168 ochib qo'ydi.
* **v169** — panel FAQAT HISOBLAGICHGA aylandi, hech qayerga yozmaydi
  ("hisoblagich · saqlanmaydi"). To'lov yana pastdagi Kerakli summa blokidan
  kiritiladi, `_tolovAvto` qayta taqsimlaydi.
* **v170** — panel pastga, Kerakli summa ustiga ko'chdi. **Ptichka pastdagi Naqt
  ga yozmaydi** — blok ochiladi, maydonlar bo'sh turadi. **`$` ketma-ket
  taqsimlaydi**: 2 tur 1154.42+845.58=2000$, klientda 1800$ → 1-turga `$` 1154.42,
  2-turga `$` 645.58, qolgan 200$ = 2.36g ostatka. `$/g` ga TEGILMAYDI.

---

# 5. KEYINGI LOYIHADAN KEYIN

* **D** — ortiqcha formulasi: ekran jami sotuv narxidan, chek kiritilgan to'lovdan
  hisoblaydi. Javob bermaganman.
* **E** — dona bazada "sotilgan" holati. Claude C ni (kiritilmasin) tavsiya qilgan.
* Ostatka tekshiruvida "yo'q" donalar: tegilmaydi / "yo'qolgan" / o'chirish.
* O'lik kod: `klientSotuvChekPrint` (141 qator), `chekQur` — o'chirilmagan.
* `print_server.py` v163 da tuzatilgan, sinalganmi bilmayman.
* **G — Ostatka delta hisoblagichga.** 34 ta yozish joyi. Avval bir hafta faqat
  kuzatish (`ostatka 935 · delta 935 ✓` yonma-yon), farq chiqmasa delta asosiy.
  Shundan keyin cloud bloki yechiladi. Bu yo'l ma'qulmi — javob bermaganman.
* **H — Kassa amallarga.** 6 maydon, 56 joy. G bir hafta sinalmasdan tegilmaydi.

---

# 6. BIRINCHI XABARDA NIMA QILISH KERAK

1. `index.html` va `CHANGELOG.md` ni ish papkasiga ko'chir, APP_VER ni tasdiqla.
   **CHANGELOG ni O'QIMA.**
2. **1-bo'limdagi Haftalik daftarni yoz** — savol yo'q, spetsifikatsiya to'liq.
   Mavjud Haftalik ostatka kodini (klient yig'ish, PDF, Excel) qayta ishlat.
3. Keyin **2-bo'limdagi F**.
4. Keyin o'lik kod tozalash.
