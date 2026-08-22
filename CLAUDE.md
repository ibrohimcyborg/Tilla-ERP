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

---

## 0.1. UZLUKSIZLIK — kontekst to'lsa ish TO'XTAMASIN

Ibrohim ko'pincha **telefondan** ishlaydi: mockupni telefonda ko'radi,
`"o'zgartir"` yoki `"yoz, push qil"` deydi. Kod PC dagi seansda yoziladi.
Seans uzilishi, kontekst to'lishi yoki `/clear` bo'lishi mumkin — shunda
**yangi seans hech narsa so'ramasdan davom eta olishi shart**.

Buning yagona kafolati — `DAVOM.md`. Shuning uchun:

1. **`DAVOM.md` HAR versiyadan keyin DARHOL yangilanadi** — seans oxirini
   kutmaydi. Kod yozildi → commit → `DAVOM.md`. Uchtasi bitta ish.
2. **Yarim qolgan ish** `DAVOM.md` ga shunday yoziladi:
   ```
   ⏳ YARIM QOLDI — <nima>
   Qilingan:  <aniq nima tushdi> — <fayl>:<qator>
   Qolgan:    <aniq nima qolgan>
   Keyingi qadam: <bitta jumla>
   Javobsiz savol: <bor bo'lsa>
   ```
   Hech qachon `"davom etyapman"` deb qoldirma — keyingi seans o'qiydi.
3. **Mockup DOIM Artifact qilib chiqariladi** — Ibrohim telefonda ochadi.
   Faqat `mockups/` ga yozib qo'yish yetmaydi, telefonda ochilmaydi.
   Havolani javobda ber.
4. Yangi seans birinchi xabari doim shu bo'ladi:
   > `CLAUDE.md` va `DAVOM.md` ni o'qi. `POS <oxirgi>` dan davom etamiz.

   Boshqa hech narsa kerak bo'lmasligi kerak. Kerak bo'lsa — `DAVOM.md`
   kam yozilgan, tuzat.
5. Kontekst to'layotganini sezsang — **avval `DAVOM.md` ni yangila**, keyin
   ishni davom ettir.

### `/clear` tartibi (Ibrohim, 2026-08-22)

Kontekst to'lib qolganda **Claude o'zi so'raydi**, Ibrohim eslatib turmaydi:

1. Claude: `"Kontekst to'lib qolyapti. DAVOM.md ni yangiladim — /clear
   qilaylikmi?"`
2. Ibrohim: `"xop"`
3. Ibrohim `/clear` yozadi (buni Claude o'zi bajara olmaydi — bu foydalanuvchi
   buyrug'i), keyin bitta qator:
   > `CLAUDE.md` va `DAVOM.md` ni o'qi. `POS <oxirgi>` dan davom etamiz.
4. Yangi seans shu fayllardan holatni oladi va **hech narsa so'ramasdan**
   davom etadi.

⚠ **So'rashdan OLDIN `DAVOM.md` yozilgan bo'lishi shart.** So'ragandan keyin
yozaman deb qoldirma — Ibrohim `"xop"` deb darhol tozalashi mumkin.

⚠ Claude aniq foizni ko'ra olmaydi. Shuning uchun: **har versiya tugagach**
va suhbat uzayganini sezganda — `DAVOM.md` ni yangilab, `/clear` ni taklif qil.
Foizni Ibrohim o'z ekranida ko'radi.

⚠ Ibrohim **hech qachon loyihani qaytadan tushuntirmaydi.** Agar yangi seans
"qaysi ish?" deb so'rashga majbur bo'lsa — `DAVOM.md` kam yozilgan, ayb Claude'da.

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

### So'ralganidan ortiq ish qilma

So'ralgan narsani **aynan** qil — ortig'ini emas.

So'ralmasa **qilinmaydi**:
- rename, refactor, `"shu yerdaman, buniyam tuzatay"`
- so'ralmagan error handling, validatsiya, himoya tekshiruvlari
- `"tabiiy juftlik"` ko'ringan qo'shimcha funksiya
- tegishsiz qatorlarni qayta formatlash yoki tartiblash

**Bir turda bitta o'zgarish.** Kichik ko'rinsa ham ikkinchisini qo'shib
yuborma.

**Diff budjeti.** Boshlashdan oldin taxminan necha qator o'zgarishini ayt.
Haqiqiy diff shu taxmindan ~2 barobar oshsa — **to'xta va xabar ber**,
davom etma. Shishgan diff = qamrov siljigan.

**Nega bu bor:** so'ralmagan o'zgarishlar diffga qo'shilgani uchun ish
chigallashadi va keyingi xato qaysi so'rovdan kelganini topib bo'lmaydi.

---

## 2. HAR KOD O'ZGARISHIDAN OLDIN — TAXMIN BLOKI

So'ralmasa ham, avtomatik, kodga o'tishdan oldin uch qism.
**Mockup bor-yo'qligidan qat'i nazar** — kichik, mockupsiz o'zgarishda ham
shu blok chiqadi.

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

### ⚠️ HOZIR POS DAVRI — faqat `POS_VER` o'sadi

Ibrohim (2026-08-22): *"pos sistemada v o'zgarsin chunki biza hozi POS
sistemada ishlavommiz, Tilla ERP da tursin v oxirida."*

Hozir ish **POS ichida** ketyapti, shuning uchun:

| | |
|---|---|
| `POS_VER` | **HAR POS o'zgarishida o'sadi** — 1.09 → 1.10 → 1.11 … |
| `APP_VER` | **QOTIB TURADI: `v177.9`** — POS ishida TEGILMAYDI |
| `index.html` 1-qatori | **QOTIB TURADI: `<!-- v177.9 -->`** |

- Commit sarlavhasi POS versiyasi bilan: `POS 1.10 — <qisqa mazmun>`
- `CHANGELOG.md` yozuvi ham `POS 1.10` deb boshlanadi
- **Istisno:** o'zgarish POS dan TASHQARIDA bo'lsa (admin ekranlari, kassa,
  hisobot, chek dvigateli) — o'shanda `APP_VER` va 1-qator o'sadi, `POS_VER`
  tegilmaydi. Ikkalasiga ham tegadigan o'zgarish bo'lsa — **Ibrohimdan so'ra**.

### Umumiy

- `index.html` ning **ENG BIRINCHI qatori**: `<!-- v177.9 -->` —
  `<!DOCTYPE html>` dan **oldin**. Faqat raqam, boshqa hech narsa.
- `APP_VER` o'zgaruvchisi shu 1-qator bilan **doim bir xil** bo'lishi shart.
- O'zgarishlar **tafsiloti** `index.html` ichiga **YOZILMAYDI** —
  adashtiradi. Faqat `CHANGELOG.md` ga.

---

## 6. NIMAGA TEGILMAYDI

**Abdulhamid rejimi.** `hamid-x` CSS klassi va `getRol()==='hamid'`
shartlari — o'zgartirma, qo'shma.

`hamid-x` klassi: 271, 342, 345, 377, 394, 1340
`getRol()==='hamid'` sharti: 7927, 7992, 8002, 9493, 9555, 17055
`rol-hamid` CSS bloki: 261–271

(v172.4 holati. Qator raqamlari har versiyada siljiydi — ishonchsiz bo'lsa
`grep -n "hamid"` bilan qayta top.)

Istisno tarixi: v172.3 da Ibrohim ruxsati bilan kassa kun-sikliga hamid-tarmoq
qo'shilgan edi, v172.4 da Ibrohim "kerak emas ekan" deb BEKOR qildi — kod
v172.2 holatiga qaytarildi. Qoida to'liq kuchda.

---

## 7. SINOV

- **Node sintaksis-sinov MAJBURIY** har o'zgarishdan keyin.
- Firebase'ni faqat **TEST rejimida** sina — `TEST_tilla_<uid>` kolleksiyasi.
  Asosiy kolleksiyaga tegmaydi.
- Lokalda ochish: `python3 -m http.server 8000` → `http://localhost:8000`
  **`file://` bilan ochma** — Firebase auth ishlamaydi.

---

## 7.1. TEKSHIRUV — `"tayyor"` deyishdan oldin

O'zgarish **yozilgani uchun** bajarilgan bo'lmaydi. **Tushganini
isbotlaganingda** bajarilgan bo'ladi.

`git commit` dan oldin shu blokni chiqar:

```
TEKSHIRUV
So'ralgan: <bir qatorli: nima → nimaga>
Qilingan:  <haqiqatda nima o'zgardi>
Dalil:     <fayl>:<qator>   eski → yangi
Grep:      <maydon/funksiya> o'qiladigan joylar: <ro'yxat>
           — hammasi yangilandi / <qaysilari emas va nega>
```

`Dalil` qatorini **haqiqiy qator raqami** va **haqiqiy eski → yangi** bilan
to'ldira olmasang — o'zgarish tushmagan. `"Tayyor"` dema, shuni ochiq ayt.

Mockup **oldin** ko'rsatadi — HOZIRGI vs TAKLIF, bu **taklif**.
TEKSHIRUV **keyin** ko'rsatadi — eski → yangi, bu **dalil**.
Ikkalasi ham kerak, biri ikkinchisining o'rnini bosmaydi.

Bajarilmagan ish `"bajarildi"` bo'lib ketishining odatiy yo'llari — har birini
tekshir:
- edit noto'g'ri faylga yoki fayl nusxasiga tushgan
- ikkinchi kod yo'li hali eski qiymatni o'qiydi — grep o'tkazib yuborgan
- o'zgarish hech qachon ishlamaydigan shart ichida qolgan
- matnda tasvirlangan, lekin edit haqiqatda qo'llanmagan
- fayl yozilgan, lekin Node sintaksis-sinov ishga tushirilmagan

### `"Ishlamadi"` deyilganda

Ibrohim `"o'zgarmadi"` yoki `"men so'ramagan narsa paydo bo'ldi"` desa:

- avvalgi natijani **himoya qilma**
- ustiga darhol ikkinchi fix **yozma**
- nima **so'ralganini** qayta o'qi, nima **yozilganini** qayta o'qi,
  ikkisining **farqini ayt**
- keyin bitta aniq tuzatish taklif qil va **to'xta**

Tekshirilmagan fix ustiga tekshirilmagan fix qo'yish — kod izlanmaydigan
bo'lib qolishining yo'li.

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
mockups/          joriy ish uchun mockuplar (eskilari saqlanmaydi —
                  bajarilgach o'chiriladi, chunki qator raqamlari eskiradi
                  va adashtiradi)
api/pdf.py        PDF generator (Vercel funksiyasi)
print_server.py   termal chek printer (localhost:5000)
vercel.json       deploy sozlamalari
```
