# Tilla ERP

Ibrohim Mirikromov loyihasi — tilla ulgurji savdo ERP tizimi.
Single-file `index.html`, vanilla JS, localStorage kaliti `tilla-v2`,
Firebase Firestore (har foydalanuvchi uchun `tilla_<uid>`).
Prod: tilla-erp.vercel.app

---

## 0. SEANS BOSHIDA — birinchi ish

1. `DAVOM.md` ni o'qi. Hozirgi holat, tugallangan ish, keyingi vazifa —
   hammasi shu yerda.
2. `index.html` ning 1-qatoridagi versiyani va `APP_VER` o'zgaruvchisini
   solishtir. Mos kelmasa Ibrohimga ayt, o'zing tuzatma.
3. **`CHANGELOG.md` ni O'QIMA.** U faqat arxiv — yozasan, o'qimaysan.

### ⚠️ `index.html` NI TO'LIQ O'QIMA

Fayl ~17 385 qator, ~1 MB, **~311k token** — kontekst oynasi 200k.
To'liq o'qishga urinish oynani to'ldiradi va ish to'xtaydi.

Doim shunday ishla:
1. `grep -n` bilan kerakli joyni **top**
2. Faqat o'sha atrofdagi 20–50 qatorni o'qi
3. Aniq blokni almashtir

Bu qoida `CHANGELOG.md` ga ham tegishli (224 KB).

---

## 1. KOD YOZISH TARTIBI (eng muhim qoida)

### LOGIKA / MAYDON / HISOB-KITOB o'zgarsa

Foyda hisobi, kassa oqimi, yangi maydon, funksiya mantiqi, ma'lumot
o'qish yo'li — bunday o'zgarishlarda **`index.html` ga TEGMA**.

Ketma-ketlik:

1. `mockups/vNNN-<nom>.html` yarat — alohida vizual HTML fayl:
   - HOZIRGI holat vs TAKLIF
   - tashxis (nima buzuq, qayerda, nechanchi qator)
   - qaror nuqtalari — Ibrohim tanlashi kerak bo'lgan joylar
2. Faylni ko'rsat va **TO'XTA**. Kod yozma.
3. Ibrohim `"ha"` / `"to'g'ri"` / `"shunaqa qil"` / `"boshla"` degach —
   endi kod.

Bu qoida `"tekshir"`, `"to'g'irla"`, `"muammo bor"` deyilganda **ham**
amal qiladi. Muammoni topganingda ham avval mockup.

### SOF VIZUAL o'zgarish

Rang, matn, joylashuv, typo — mantiqqa tegmasa mockupsiz mumkin,
**LEKIN oldin so'ra**:

> "Bu vizual o'zgarish, mockupsiz yozaman, rozimisan?"

`"ha"` degach yoz.

### Ikkilanish

Ikkilangan holat = **LOGIKA** deb hisobla, mockup qil.
`"Bu oddiy-ku"` degan qarorni **O'ZING qabul qilmaysan** — qaror doim
Ibrohimdan chiqadi. Avvalgi seanslarda aynan shu joyda xato bo'lgan:
oddiy deb o'ylangan narsa oddiy emas edi.

---

## 2. HAR MOCKUP OXIRIDA — TAXMIN BLOKI

So'ralmasa ham, avtomatik, kodga o'tishdan oldin uch qism:

**1. ANIQ BILMAYOTGAN JOYLARIM**
Spetsifikatsiyadagi bo'shliqlar, aniq aytilmagan qarorlar.
Jim to'ldirma — sana.

**2. TAXMINLARIM**
Agar shu bo'shliqlarni to'ldirsam, qanday to'ldiraman. Va har taxmin
yoniga: bu qaror **Ibrohimdanmi yoki mendanmi** chiqqan.

**3. TA'SIR QILADIGAN JOYLAR**
Bu o'zgarish yana qaysi funksiya / maydon / ekranga tegadi.
Grep natijasi bilan — faqat o'zgaruvchi nomi emas, **maydonni o'qiydigan
HAMMA joy**.

Qisqa signal: Ibrohim `"taxmin?"` yoki `"3 savol"` deb yozsa — darhol
shu uch qismni chiqar.

**Nega bu bor:** Ibrohim har safar "muammo nima" deb so'raydi, lekin
3-4 savoldan keyin bu esdan chiqadi va taxmin jim kodga singib ketadi.
Loyiha cho'zilishining asosiy sababi shu.

---

## 3. ESKI VERSIYALAR — DALIL EMAS

Faqat **ikki manba** bor:
1. Ibrohim hozir aytgan spetsifikatsiya
2. `index.html` ning **HOZIRGI** kodi

`v120` / `v113` kabi eski versiyalardan **QAROR ko'chirma**. "O'xshash-ku"
deb takrorlama. Ibrohim aytgan spetsifikatsiyani AYNAN bajar.

- Mavjud funksiyani **chaqirish** — yaxshi
- Eski **qaror va taxminni** meros olish — yomon

Haqiqiy misol: Ibrohim "kassa paneli 3x2 qil" dedi, v120 dagi `_kartaBor`
dinamik yashirish qarori perechga ham ko'chirildi → qiymat 0 bo'lgani
uchun panel 1 ustunga tushdi. Xato.

---

## 4. GREP BIRINCHI, KOD KEYIN

Yangi funksiya yozishdan oldin `grep` bilan tekshir. id yoki maydon
naqshlarini **taxmin qilma** — kodda ko'r.

Yangi maydon qo'shganda: aniq o'zgaruvchi nomlarini emas, o'sha
**maydonni o'qiydigan HAMMA joyni** grep qil.

Haqiqiy misol: v136 da perech `sdachaTaqsimSaqla` da va chek yorlig'ida
qolib ketdi. Ibrohim topdi, Claude emas.

---

## 5. VERSIYA VA CHANGELOG

- `index.html` ning **ENG BIRINCHI qatori**: `<!-- v171.7 -->` —
  `<!DOCTYPE html>` dan **oldin**. Faqat raqam, boshqa hech narsa.
- `APP_VER` o'zgaruvchisi ham shu versiyaga o'zgartiriladi.
- O'zgarishlar **tafsiloti** `index.html` ichiga **YOZILMAYDI** —
  adashtiradi. Faqat `CHANGELOG.md` ga.

---

## 6. NIMAGA TEGILMAYDI

**Abdulhamid rejimi.** `hamid-x` CSS klassi va `getRol()==='hamid'`
shartlari — o'zgartirma, qo'shma.

`hamid-x` klassi: 271, 342, 345, 377, 394, 1340
`getRol()==='hamid'` sharti: 7858, 7923, 7933, 9416, 9478, 16976
`rol-hamid` CSS bloki: 261–271

(v171.7 holati. Qator raqamlari har versiyada siljiydi — ishonchsiz bo'lsa
`grep -n "hamid"` bilan qayta top.)

---

## 7. SINOV

- **Node sintaksis-sinov MAJBURIY** har o'zgarishdan keyin.
- Firebase'ni faqat **TEST rejimida** sina — `TEST_tilla_<uid>` kolleksiyasi.
  Asosiy kolleksiyaga tegmaydi.
- Lokalda ochish: `python3 -m http.server 8000` → `http://localhost:8000`
  **`file://` bilan ochma** — Firebase auth ishlamaydi.

---

## 8. GIT

**Hech qachon `git push` qilma.**

Kod yozgandan keyin faqat:
```bash
git add -A && git commit -m "v171.8 — <qisqa mazmun>"
```

Push qilishni faqat Ibrohim aytganda bajar. Prodga chiqarish qarori
**faqat Ibrohimda** — push bo'lsa Vercel darhol deploy qiladi.

Har versiya o'z commit'iga tushsin — shunda `git diff v170 v171` bilan
o'zgargan hamma qator ko'rinadi, yashirin qolmaydi.

---

## 9. SEANS OXIRIDA

1. `CHANGELOG.md` ga yangi versiya yozuvini qo'sh.
2. **`DAVOM.md` ni yangila** — nima qilindi, nima qoldi, qaysi savol
   javobsiz. Keyingi seans shu fayldan boshlanadi.
3. `git commit`.

---

## 10. KODDAGI TASDIQLANGAN FAKTLAR (v171.7)

Bularni qayta aniqlashga urinma — tekshirilgan.

### Ma'lumot yozuvlari

| Amal | Joy | Yozuv |
|---|---|---|
| Zavoddan kirim | `t.tarix` | `tip:'mol'` + sana + gramm |
| Zavodga vozvrat | `t.tarix` | `tip:'vozvrat'` + sana + gramm |
| Klientga berish | `k.tarix` | `tip:'berish'` + sana + gramm + zavod/tur |
| Klientdan vozvrat | `k.tarix` | `tip:'vozvrat'` + sana + gramm + zavod/tur |

### ⚠️ SOTUV BELGILANMAYDI — ochiq muammo

`_sotuvDavomEt` (14938) sotuvni **belgisiz** `tip:'berish'` qilib yozadi.
Butun faylda `manba:'sotuv'` va `_sotuv:true` **bir marta ham
yozilmaydi**.

Ammo `haftaOstData` (6239, 6246) o'sha belgini o'qiydi:
```js
sotuv:(op.manba==='sotuv' || op._sotuv===true)
```
→ qiymat **doim `false`**. 6739 / 6797 / 6842 dagi
`(r.sotuv?'sotuv':...)` hech qachon `'sotuv'` chiqarmaydi.
Dona bazadagi `holat:'sotilgan'` ham **0 marta** qo'yiladi.

**Natija:** `k.tarix` da sotuv va berish farqlanmaydi. Sotuvni alohida
qator qiladigan har qanday ekran avval bu muammoni hal qilishni talab
qiladi. Qaror Ibrohimdan.

### `inventar` belgisi — tuzoq va yechimi

Ostatka amallari ham `tip:'mol'` / `tip:'berish'` bo'lib yoziladi.
Ajratish belgisi bor:
- `inventar:'boshlangich'` — shakllantirish (6189)
- `inventar:'tekshiruv'` — tekshiruv tuzatish

Ajratmasa "Zavoddan kirim" ga qo'shilib ketadi va hisobot yolg'on
chiqadi. `haftaOstData` `'boshlangich'` ni tashlaydi (6218 izohiga qara), lekin
`'tekshiruv'` ni **emas**.

### `haftaOstData` (6221) chegarasi

Faqat `data.klientlar` → `k.tarix` o'qiydi. **`t.tarix` ga tegmaydi.**
Zavod kirim/vozvratini ko'rsatadigan hisobot uchun yangi o'quvchi kerak
— bu funksiya yordam bermaydi.

### O'lik kod (hech qayerdan chaqirilmaydi)

- `chekQur` — 9814
- `klientSotuvChekPrint` — 15384

### Muhim funksiyalar

| Funksiya | Qator |
|---|---|
| `haftaOstData` | 6221 |
| `haftaOstRender` | 6654 |
| `haftaOstPDF` / `haftaOstExcel` | 6780 / 6826 |
| `donaBazaTekshirSaqla` | 6543 |
| `donaBazaOmborOchir` | 7922 |
| `ostFormSaqla` | 7990 |
| `_sotuvDavomEt` | 14938 |
| `_skanChipHTML` (umumiy skan chizuvchi) | 12016 |
| `_qarzTarkib` | 15413 atrofida |
| `klientQarzSplit` | grep bilan top |

---

## 11. FAYLLAR

```
index.html        ~17 385 qator (~1 MB, ~311k token) — butun ilova
CHANGELOG.md      versiya arxivi (YOZASAN, O'QIMAYSAN)
DAVOM.md          hozirgi holat + keyingi vazifa
mockups/          tasdiq kutayotgan va tasdiqlangan mockuplar
api/pdf.py        PDF generator (Vercel funksiyasi)
print_server.py   termal chek printer (localhost:5000)
vercel.json       deploy sozlamalari
```
