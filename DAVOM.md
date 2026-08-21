# DAVOM.md — qayerdan davom etamiz

> Bu fayl **har seans boshida o'qiladi**. Ish qoidalari CLAUDE.md da.
> Har versiyadan keyin bu fayl **yangilanadi** — aks holda keyingi seans
> nimadan davom etishini bilmaydi.

**Oxirgi yangilanish:** v176.5 · 2026-08-19

---

## Hozirgi holat

| | |
|---|---|
| Versiya | **v176.5** (`index.html` birinchi qatorida `<!-- v176.5 -->`, `APP_VER` da ham) |
| Hajm | ~17,470 qator · ~1 MB · **~311k token** |
| Deploy | tilla-erp.vercel.app (GitHub: ibrohimcyborg) |
| Saqlash | localStorage `tilla-v2` + Firebase Firestore `tilla_<uid>` |
| Sinov | **TEST rejimi** — `TEST_tilla_<uid>`. v172.15 dan yana **ADMIN xonasi**: login admin/admin123, `ADMIN-` prefiks + `ADMIN_tilla_<uid>` cloud — bo'sh, Qo'limizdagi ostatkani boshidan tekshirish uchun. |
| Git | **v176.5 gacha push qilingan** (2026-08-19) — prod v176.5. ⏳ Tekshiruv kutilmoqda: v175.3 PDF · v175.4 hisobot · v175.5 nol-yozuv · v176 skan oynasi · v176.1 offset ptichkasi · v176.2 yaxlitlash (✅ chekda naqt — Ibrohim tasdiqladi 2026-08-19: kerakli summaga yozilmasa ham qolgan summa N qatori bo'lib chekda chiqadi) · **v176.3 offset sdachasi** · **v176.4 sdacha ro'yxati filtri**. |
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

```
cd Tilla-ERP
claude
```

Keyin:
> CLAUDE.md va DAVOM.md ni o'qi. v171.7 dan davom etamiz.

Keyingi safar shu ishni davom ettirish uchun — `claude -c`.

**Har versiyadan keyin:** `/clear` qiling va yangi seans boshlang.
Uzun seans tokenni ko'p yeydi (har so'rovda butun suhbat qayta yuboriladi).
