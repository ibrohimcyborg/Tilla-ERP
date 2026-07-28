# Tilla ERP — versiya tarixi

> index.html dan ajratildi (v137.1 dan keyin). Ibrohim: "v digi o'zgarishlani o'chirib tasha indexdan, bu adashtirvotti sani".
> Bu fayl faqat ARXIV. Yangi kod yozganda bu yerdagi qarorlarni MEROS QILIB OLMA — Ibrohimning aytgan spetsifikatsiyasi asosiy manba.

## v168.3: yashirin eski qatorlar (Taqsimlandi qopketishi)

**Ibrohim:** "bundan oldin summa yozasanu nimadur summala keyingi safar to'lovga
kirsen qopketib qovotti" — panelda hamma oyna bo'sh, Jami 0$, lekin
Taqsimlandi 236.5$ va qizil "Oshdi 236.5$".

**Sabab (eski, v168 ochib qo'ydi):** `openKlientTolov()` modal ochilganda tur
ro'yxatini faqat YASHIRARDI (`kt-turlar-cont.style.display='none'`), lekin
`kt-turlar-list.innerHTML` ni TOZALAMASDI. Oldingi seansdagi qatorlar summasi
bilan DOM da qolib ketardi. v168 gacha buni hech kim o'qimasdi — `kTolovCalc`
o'zining `jamiSummaKt` sini joriy klient breakdown i bo'yicha sanaydi.
Yangi `pulPanelTaqsim` esa `[id^="kt-s-"]` bilan DOM dagi HAMMA summa maydonini
sanaydi, shu jumladan yashirin eskilarini.

Natijada: Taqsimlandi = eski qatorlar (236.5), kerakli = joriy klient (0) ->
`pulPanelAvto('kt', 0)` panelni tozalab qo'yardi.

**Tuzatildi:**
* `openKlientTolov()` — `kt-turlar-list` va `kt-vozvrat-list` tozalanadi,
  `window._kTolovBD=null` qilinadi.
* `kTolovKlientChange()` — klient almashganda ham `kt-turlar-list` tozalanadi.
* Sotuv modalida bu muammo yo'q edi (`ks-tolov-list` allaqachon tozalanardi).

**Takrorlash sinovi** (`t49.js`, haqiqiy `kTolovCalc` soxta DOM da):
tozalashdan oldin `Taqsimlandi 236.5$ · Oshdi 236.5$`, keyin `Taqsimlandi 0$ ·
Qoldi 0$`.

## v168.2: uch xato tuzatildi (Ibrohim sinovi)

**1. Panel oldingi klientdan qolib ketardi.** Bir klientga pul yozib, keyingisiga
kirilganda paneldagi "Jami 1,000$" qolib turardi (oynalar bo'sh, lekin ko'rsatkich
eski). Sabab: `pulPanelReset` faqat qiymatlarni tozalardi, ko'rinishni yangilamasdi,
va klient almashganda umuman chaqirilmasdi.
* `pulPanelReset` oxirida `pulPanelUpd(pfx)` chaqiriladi.
* `pulPanelReset` panel oynalaridagi `userEdited` belgilarini ham tozalaydi.
* `kTolovKlientChange()` va `ksSotuvPickK()` boshida `pulPanelReset` chaqiriladi.

**2. Panelda avto-to'ldirish yo'q edi.** Ibrohim: "kerakli summa 4053.12 edi,
kartaga 2000$ yozsam naqtda 2053.12 bo'lishi keregidi, u o'zgarmayapti".
* Yangi `pulPanelAvto(pfx, kerakli)` — TEGILMAGAN birinchi oyna (naqt -> perech ->
  karta) kerakli summaning qolganini oladi. Tegilganlari qotadi.
* Yangi `pulPanelKirit(pfx, el)` — oynaga yozilganda `userEdited='1'` qo'yadi,
  bo'shatilsa olib tashlaydi (avto qaytadi). Panel oynalarining `oninput` i shunga
  ulandi.
* `pulPanelAvto` `kTolovCalc` va `kSotuvCalc` ichida, kerakli summa hisoblangandan
  keyin chaqiriladi.

**3. Sdacha.** Ibrohim: "klient puli ko'p bo'sa sdacha chiqsin". Avto-to'ldirish
`Math.max(0, kerakli - tegilganlar)` ishlatgani uchun, tegilgan summa kerakliddan
oshsa avto oyna 0 ga tushadi va jami kerakliddan katta bo'lib qoladi — mavjud
sdacha hisobi (`max(0, ktBerdi - ktKerakli)`) o'z-o'zidan ishlaydi. Panelda
"Oshdi N$" qizil chiqadi.

**Ochiq qolgan:** panel oynalari tartibi hozir Naqt · Perech · Karta (Ibrohim
shunday yozgan edi). Sinov rasmida u "kartaga yozdim" degan, lekin 2000 PERECH da
turgan — tartib chalkashtirayotgan bo'lishi mumkin.

## v168.1: $ tugmasi ustiga qo'shmaydi · Lom oynasi bosiladi

* `turDolTog` — qatorga qo'lda summa yozilgan bo'lsa, `$` bosilganda ustiga
  QO'SHILMAYDI. Klientda QOLGAN pul yoziladi (qolgan = jami − boshqa qatorlar).
  Ibrohim: "qo'lda yozib qo'yib $ bossa ustigamas klientda qogan pulli yozishi kere".
* Paneldagi **Lom** oynasi bosiladigan bo'ldi — `pulPanelLomQosh(pfx)` yangi lom
  qatorini qo'shadi, ekranni o'sha qatorga suradi va gramm maydoniga fokus beradi.
  Yorlig'i "Lom +", ramkasi oltin. To'lov modalida klient tanlanmagan bo'lsa
  ishlamaydi (`kt-lom-btn` yashirin bo'lsa chiqib ketadi).

## v168: Panel yagona kirish joyi · 1 qatorli oynalar · tur qatorida $ tugmasi

**Muammo (v167 da topilgan):** panel pastdagi "Kerakli summa" maydonlari bilan
bitta pulni talashardi. Panelga turlardan OLDIN yozilsa, yozilgan raqam
`kTolovCalc` ning nol-holat shoxida darrov o'chib ketardi; keyin avto-to'ldirish
kerakli summani NAQT ga yozardi. Natija: 300 naqd + 200 karta olingan to'lov
**500$ naqd** bo'lib saqlanardi. Jami to'g'ri, tur bo'linishi xato — kassa naqd
qoldig'i, klient tarixidagi to'lov turi belgisi, kunlik naqd hisobi buzilardi.

**Panel (ikkala modalda):**
* 4 oyna bir qatorda: **Naqt · Perech · Karta · Lom**. Nom tepasida, summa tagida.
* Qiymati 0 bo'lgan oyna YASHIRILMAYDI — 4 ustun doim 4 ustun.
* Panel turlar ro'yxatidan TEPAGA ko'chdi (avval lom bo'limidan keyin edi).
* Panel doim ochiq (avval faqat pul yozilganda chiqardi).
* Lom oynasi lom qatorlaridan avtomat to'ladi.

**Kerakli summa bloki:** u ham 4 oynali bir qator (Naqt/Perech/Karta/Lom),
`readonly`, faqat ko'rsatadi. Eski ✓ katakchalari (`*-cb-*`) olib tashlandi —
`_tolovToggle` cbEl topolmay chiqib ketadi, qolgan chaqiruvlar `if()` bilan
himoyalangan.

**Tur qatori — 3-variant (yorliqsiz, 2 qator):**
* Tepada: tur nomi + qarz gramm. ✓ tepadan pastga tushdi.
* Pastda bitta qatorda: `$` · SUMMA · $/g · gramm · ✓. SUMMA/$/g/gramm
  yorliqlari olib tashlandi, birlik belgisi maydon ichida qoldi.
* Biz qarzdor qatorlarda `$` va ✓ o'rniga `$ offset` turadi.
* Sotuv modalida ham shunday (u yerda yorliqlar allaqachon yo'q edi).

**Yangi funksiyalar:** `pulPanelBor` (klientda bor pul), `pulPanelSync`
(panel → pastki maydonlar, hodisasiz — rekursiya bo'lmasin), `turDolTog`
($ tugmasi), `ktQarzD`/`ksQarzD` (qatorning dollardagi qarzi).
`pulPanelUpd` endi FAQAT KO'RSATADI, hech qayerga yozmaydi.

**Jonli hisob:** `pulPanelUpd` `kTolovCalc` va `kSotuvCalc` oxiriga ulandi —
tur summasi, lom, skidka o'zgarganda Jami/Taqsimlandi/Qoldi darrov yangilanadi.
Avval faqat panelning o'z maydoniga tegilganda yangilanardi.

**Nol-holat tuzatildi:** `jamiSummaKt===0` shoxi endi panelda pul bo'lsa
pastdagi maydonlarni TOZALAMAYDI — `pulPanelSync` bilan qayta yozadi.

**Claude qarori (Ibrohimdan chiqmagan):** panel BO'SH bo'lsa eski avto-to'ldirish
ishlayveradi. Sababi: butunlay o'chirilsa, ✓ bosib qarz yopilganda-yu panelga pul
yozilmasa **0$ to'lov** saqlanardi. Panelga pul yozilishi bilan panel g'olib
bo'ladi (`userEdited='1'`).

**Tegilmadi:** skidka, saqlash, chek, kassa, klient tarixi, sdacha, qarz hisobi,
$/g va gramm qiymatlari, dona baza, ostatka, cloud, Abdulhamid rejimi.

## v167: "Klientda bor" pul paneli — kalkulyator

Ibrohim: "klientda nechpul borligini yozadigan joy yo'q ozi, manga shunaqa joy
kere bo'vottide. Klient qo'lida puli bor, man hisoblab plus minus qb yurman.
Pulini yozib uni qarziga chochvoradigan qiladigan qilsak bo'lmaydimi?"

Aniqlashtirildi: bu SAQLANADIGAN HISOB EMAS. Klient keladi, mol oladi,
qo'lidagi pulni beradi — o'sha pul turlarga taqsimlanadi va oxirida 0 bo'ladi.
"Bu odatda olgan molidan beradigan puli kam bo'lganda ko'proq asqotadi."

### PANEL

Joyi: "Kerakli summa" blokining USTIDA, to'lov va sotuv modalida bir xil
(Ibrohim: "kerakli summani tepasida tursa bo'ldi").

Tarkibi:
* Naqd / Karta / Perech — qo'lda yoziladi
* Lom — pastdagi lom qatorlaridan AVTOMAT yig'iladi
* Jami = naqd + karta + perech + lom
* Progress chizig'i
* Taqsimlandi / Qoldi

Jami 0 bo'lsa panel KO'RINMAYDI.

### YANGI FUNKSIYALAR

`pulPanelLom(pfx)` — lom qatorlaridan gramm, kurs, pul. Id naqshlari:
`<pfx>-lg-{i}` gramm, `<pfx>-lk-{i}` kurs. Gramm yoki kurs yo'q bo'lsa
o'sha qator hisobga KIRMAYDI.

`pulPanelTaqsim(pfx)` — turlarga yozilgan summalar yig'indisi.
To'lov modali `kt-s-{zi}-{ti}`, sotuv modali `kst-s-{zi}-{ti}`.
DIQQAT: naqshlar boshqa-boshqa, shuning uchun to'lov va sotuv ARALASHMAYDI.

`pulPanelUpd(pfx, tushir)` — qayta hisoblaydi. Qoldi manfiy bo'lsa
"Oshdi N$" deb QIZIL bo'ladi, lekin saqlashga xalaqit bermaydi.

`pulPanelReset(pfx)` — modal ochilganda tozalanadi.

### PASTGA TUSHIRISH

Ibrohim: "ha tushursin, biratola yozib o'tirmiman kerakli summaga".

Panelga yozilgan naqd/karta/perech pastdagi `<pfx>-naqt-berildi`,
`-karta-berildi`, `-perech-berildi` maydonlariga tushadi va ularning
`oninput` i chaqiriladi — ya'ni mavjud hisob o'zi ishlaydi.

Foydalanuvchi o'sha maydonni TAHRIRLAYOTGAN bo'lsa (`document.activeElement`)
tegilmaydi — yozayotganini buzmasin.

### SAQLANMAYDI

Panel hech narsani saqlamaydi, yangi maydon qo'shmaydi. Modal yopilganda
yo'qoladi. Ishlatmasangiz ko'rinmaydi ham.

### SINOV (t35.js)

1. Bitta lom: 10.70g × 72.7 = 777.89$
2. Ikki lom qo'shiladi: 15.7g = 1,127.89$
3. Kurssiz lom hisobga kirmaydi
4. To'lov taqsimoti 10,403.76$, sotuv 3,000$
5. To'lov va sotuv ARALASHMAYDI
6. Jami 13,627.89$, qoldi 3,224.13$
7. Panel ikkala modalda, reset ulangan, tushirish bor

### HALI YOZILMAGAN — keyingi qadam

Ibrohim so'ragan OLTIN "$" TUGMASI har tur qatorida (grammning yashil ✓
yonida, chap tomonda). Bosilganda klientda QOLGAN pulni o'sha turga qo'yadi.
Qarzdan ko'p bo'lsa faqat qarzicha qo'yadi.

Va har tur tagida "qolgan N$ → M g" ko'rsatkichi.

Bular tur qatorlarini render qiladigan funksiyalarga tegishni talab qiladi —
alohida qadam sifatida qoldirildi.

## v166: ochirTur narx kalitlari + chekda "aylantirildi"

Ibrohim: "A va B ni qilib qo'ysin".

### A — `ochirTur` narx kalitlarini tekislamasdi

Narx TUR INDEKSI bo'yicha saqlanadi: `tilla-foiz-{zi} = {ti: qiymat}`.
Tur o'chirilganda `z.turlar.splice(ti,1)` keyingilarining indeksini siljitardi,
lekin narx kalitlari joyida qolardi. Natijada foizi 13.5 bo'lgan tur 3.7 bo'lib
qolardi — sezilmaydigan, lekin PULGA TA'SIR QILADIGAN xato.

`turNarxKalitOchir` v165 da yozilgan edi (birlashtirish uchun), lekin `ochirTur`
ga ulanmagan edi. Endi `splice` dan OLDIN chaqiriladi.

To'rt prefiks ham tekislanadi: `tilla-foiz-`, `tilla-manual-`,
`tilla-a-foiz-`, `tilla-a-manual-`.

`save()` ga izoh ham qo'shildi: "Tur ochirildi: Zavod | Tur".

### B — chekda "aylantirildi"

Offset qatori chekda faqat `O` harfi bilan chiqardi, klient nima bo'lganini
bilmasdi. Endi:

```
 O  Rasul Oddiy aylantirildi              684.70#
```

YO'LDA TOPILGAN: bu qatorda hali `\u00b7` (o'rta nuqta) qolgan ekan —
`r.zavod+' \u00b7 '+r.tur+' dan'`. v160 da to'lov chekining TUR nomidagi
nuqta tuzatilgan, lekin OFFSET qatoridagi qolib ketgan. UTF-8 da ikki bayt,
printerda xitoy ieroglifi bo'lardi. Olib tashlandi.

KENGLIK TEKSHIRILDI: dastlab "dan aylantirildi" yozilgan edi, lekin
"Butterfly Polimer" bilan qator 49 belgi bo'lib 48 dan OSHIB KETDI.
"dan" olib tashlandi — endi eng uzun haqiqiy nom bilan ham aynan 48 ga sig'adi.

### SINOV (t34.js)

* `turNarxKalitOchir` `splice` dan OLDIN chaqiriladi
* Chekda "aylantirildi" bor, `\u00b7` yo'q
* Haqiqiy zavod-tur nomlari bilan qator kengligi 48 dan oshmaydi

### IBROHIM JAVOBLARI (keyingi ishlar uchun)

* **C** — kurs/foizni PC ga bog'lash KERAK EMAS. Aksincha: PC da o'zgarsa
  hammada o'zgarsin, lekin PC da svet ketsa telefondan ham o'zgartirib bo'lsin.
  Ya'ni vazifa "cheklash" emas, "SINXRONLASH" ga aylandi.
* **F** — IKKALASI ham kerak: shakllantirish (baza shu bo'yicha qayta quriladi)
  VA qo'shish (bazaga tegmay qo'shiladi). "Odatda shakllantiraman, lekin nimadur
  qolib ketsa qo'shvorish uchun tegmaydigan joyi ham kerak."
* **D, E, G** — Ibrohim tushuntirish so'radi, mockup kutmoqda

## v165: Tur nomi hamma joyda ko'chadi + turni birlashtirish

Ibrohim topgan JIDDIY bug: "zavod turining otini o'zgartiruvdim, sistema eski
otida deb o'ylayapti, narxini chiqarberolmayapti... 3DS qilib berilgan
klientlarga ostatka ko'rsatib, S bo'lib kirgan klientlarniki o'chib ketgan,
keyin S deb tur qo'shsam S digi ostatkalar ko'rindi".

### SABAB — bitta qator

```
function turNomTahrir(ti) {
  t.nom = yangiNom;   // FAQAT shu. Boshqa hech narsa.
  save();
}
```

Tur nomi HAMMA JOYDA KALIT: klient tarixida `op.tur`, dona bazada `r.tur`,
oplogda `loc.tur`. Nom o'zgarsa eski yozuvlar bog'lanmay qoladi.

DIQQAT: `zavodNomTahrir` (zavod nomi) klient tarixini YANGILAYDI. Ya'ni to'g'ri
yo'l kodda bor edi — tur uchun yozilmagan.

Ibrohimda nima bo'ldi:
1. "S" turi bor edi — omborda oltin, 14 klientda 144.53 g qarz
2. Nomi "3DS" qilindi — faqat tur obyektining nomi o'zgardi
3. Klient yozuvlari hali ham `tur:'S'` — hech qaysi turga bog'lanmadi, ko'rinmay qoldi
4. Yangi "S" turi qo'shildi — eski yozuvlar darrov unga yopishdi
5. Natija: bitta tur IKKIGA BO'LINDI (oltin 3DS da, qarzlar S da)

### `_turKochir(zavodNom, eskiNom, yangiNom)`

Umumiy funksiya, nom o'zgarganda ham birlashtirishda ham ishlatiladi:

* Klient tarixi — `op.zavod` VA `op.tur` ikkalasi mos kelsa ko'chadi
  (boshqa zavoddagi bir xil nomli tur TEGILMAYDI)
* Dona baza — lokal + `donaBazaCloudYoz` bilan cloudga
* Hisob snapshot keshi tozalanadi (kalit eskirdi)

### eskiTur — FAQAT KO'RSATISH UCHUN

Ibrohim B variantini tanladi: eski yozuvlarda eski nom eslatilsin
(qog'ozdagi chek bilan chalkashmasin). Lekin "sistema chalkashib ketmasa bo'ldi"
dedi — shuning uchun:

```
{ tip:'berish', tur:'3DS', eskiTur:'S', gramm:20.79 }
                ^ sistema shuni    ^ faqat ekranga
                  ishlatadi
```

Hisob-kitob, guruhlash, narx, ostatka — HAMMASI `tur` ni o'qiydi, u bitta qiymat.
`eskiTur` ni HECH QANDAY HISOB o'qimaydi. Grep bilan tekshirildi (t33.js, 9-sinov):
u faqat `_eskiTurBelgi` (ko'rsatish), `_turKochir` (yozish) va uchta render
joyida uchraydi.

Bir marta yoziladi: `if(op.eskiTur===undefined)`. Ikkinchi ko'chirishda BIRINCHI
nom saqlanadi (S -> 3DS -> XYZ bo'lsa ham `eskiTur` "S" bo'lib qoladi).

KO'RINADI: klient tarixi breakdown qatorlari (10040, 10058, 10097).
KO'RINMAYDI: klient ostatkasi, zavod ekrani, chek, dona baza — ular YIG'INDI,
ichida eski ham yangi ham bor, "avval S" yozish yolg'on bo'lardi.

### TURNI BIRLASHTIRISH

Tur ochilganda, dona baza panelidan keyin "Turni birlashtirish" tugmasi.
Faqat zavodda 2+ tur bo'lsa ko'rinadi.

Ochilgan tur BOSHQASIGA qo'shiladi va o'chadi. Raqam bilan tanlanadi, keyin
oldindan hisob ko'rsatiladi (ostatka, klient yozuvlari, dona, zavod tarixi soni),
ikki marta tasdiq so'raladi.

Ko'chadi: klient tarixi, dona baza, zavod tarixi, donalar ro'yxati.
Qo'shiladi: ostatka, donaOst.

### `turNarxKalitOchir(zi, delTi, turSoni)` — YANGI

Narx TUR INDEKSI bo'yicha saqlanadi: `tilla-foiz-{zi} = {ti: qiymat}`.
Tur o'chirilsa keyingilarining indeksi siljiydi va NARXI ARALASHIB KETARDI.

Bu funksiya to'rt prefiksni ham (`tilla-foiz-`, `tilla-manual-`,
`tilla-a-foiz-`, `tilla-a-manual-`) tekislaydi: o'chirilgan indeks tashlanadi,
undan keyingilari bir pog'ona pastga suriladi.

MUHIM: mavjud `ochirTur` (turni o'chirish) bu funksiyani CHAQIRMAYDI — ya'ni
qo'lda tur o'chirilsa narxlar hali ham siljiydi. Bu ALOHIDA bug, Ibrohim
aytmagani uchun tegilmadi.

### `turNomTahrir` YANGILANDI

* Bir xil nomli tur bo'lsa OGOHLANTIRADI va birlashtirishga yo'naltiradi
* `_turKochir` chaqiriladi
* `obyektPush('tur',...)` — yangi nom cloudga ham chiqadi (v164)
* Oxirida nechta yozuv ko'chgani aytiladi

### SINOV (t33.js)

1. 2 klient yozuvi + 2 dona ko'chdi
2. BOSHQA zavoddagi "S" tegilmadi
3. Boshqa tur ("3D") tegilmadi
4. `eskiTur` yozildi
5. Cloudga yozildi (d1, d2)
6. Ikkinchi ko'chirishda birinchi nom saqlandi
7. Belgi matni; `eskiTur` yo'q yoki `tur` ga teng bo'lsa bo'sh
8. Narx kalitlari to'g'ri siljidi (foiz va manual)
9. `eskiTur` grep — hisobda ishlatilmaydi

### CLOUD HAQIDA OGOHLANTIRISH

Oplogdagi ESKI yozuvlarda `loc.tur` hali eski nomda. Nom o'zgartirilgandan
keyin boshqa qurilma oplogdan eski nomli yozuv olishi mumkin.

Shuning uchun: nom o'zgartirgandan yoki birlashtirgandan keyin PC dan
"Bu qurilmanikini cloudga yuborish", boshqa qurilmalarda "Cloud'dan yuklab
olish" bosilsin. Blobda nomlar to'g'ri.

Bu to'liq hal qilinmadi — oplogga qayta yuborish keyingi ish.

## v164: Yangi klient / zavod / tur endi OQADI

Ibrohim: "3 ta klient keldi, 3 ta qurilma ishlayapti... nimalar to'qnashayapti,
manga cloud sekundiga ishlasa zo'r edi, live daka ishlaydigan, nimadur qo'shilsa
olinsa ketsa to'g'ri silliq xatosiz".

Ibrohim shuni ham aytdi: "san tarixni o'qima, shunchaki hozirgi holatdan tuzatib
ket, sani tarixlar chalg'itadi". Shuning uchun v99/v104 sabablariga qaralmadi —
faqat hozirgi kod bo'yicha ishlandi.

### TASNIF (Ibrohimga tushuntirilgan)

Uch xil amal bor:

* **QO'SHISH** — yangi narsa qo'shiladi, eskisiga tegilmaydi. TO'QNASHMAYDI.
* **DELTA** — "shuncha kamaydi" deb yoziladi, cloud o'zi qo'shadi. TO'QNASHMAYDI.
* **ALMASHTIRISH** — eski qiymat yangisiga almashadi. TO'QNASHADI.

Hozir HAMMASI to'qnashadi, chunki `cloudSaqla` butun ma'lumotni bitta hujjatga
yozadi. Blok — kasallik emas, BINT. Kasallik butun holatni yozishda.

Ibrohim qaror qildi: kurs va foizni faqat PC (Qurilma-1) o'zgartiradi.
Shu bilan ALMASHTIRISH kategoriyasi butunlay yo'qoladi.

### BU VERSIYADA — 1-QADAM

Yangi klient / zavod / tur oplogga chiqadi.

TOPILGAN: `amalRecAdd` (7112) allaqachon yetishmagan zavod/tur/klientni O'ZI
yaratadi — lekin faqat TARIX yozuvi kelganda. Amali yo'q yangi klient hech qachon
o'tmasdi, va blob yozilganda YO'QOLIB KETARDI.

Yangi kod:

* `obyektRef()` — cloudda `_obyektlar/items` kolleksiyasi
* `obyektPush(tip, obj)` — 'klient' | 'zavod' | 'tur'. Hujjat id si:
  `klient|Nom`, `zavod|Nom`, `tur|Zavod|Nom`. `{merge:true}` bilan yoziladi.
* `obyektQabul(d)` — MAVJUDIGA TEGMAYDI. Faqat yo'q bo'lsa qo'shadi.
  Tur kelsa va zavodi yo'q bo'lsa — zavod ham yaratiladi.
* `obyektListen()` — onSnapshot, LIVE. Ko'rilganini `tilla-obyekt-synced`
  bo'yicha o'tkazib yuboradi.
* `obyektUnsub()` — chiqishda to'xtatiladi

Chaqiruv joylari: `saqlashKlient` (10709), klient sotuv modalidagi qo'shish
(12744), `saqlashZavod` (7806), `saqlashTur` (7807).

Listener `donaBazaCloudListen()` yonida yoqiladi/o'chiriladi.

### NEGA XAVFSIZ

Bu QO'SHISH amali. Ikki qurilma ikki klient qo'shsa ikkalasi ham qoladi.
Mavjud yozuv hech qachon ustidan yozilmaydi — nom, telefon, tarix tegilmaydi.

### SINOV (t32.js)

1. Yangi klient qabul qilindi
2. MAVJUD klient ustidan yozilmadi (tel 999 kelsa ham eskisi qoldi)
3. Yangi zavod
4. Yangi tur mavjud zavodga
5. Noma'lum zavodga tur kelsa — zavod ham yaratildi
6. Takror tur qo'shilmadi
7. Tur id si zavod bilan, `{merge:true}`
8. Listener ko'rilganini o'tkazadi
9. To'rt chaqiruv joyi ham ulangan

### KEYINGI QADAMLAR (hali qilinmagan)

* **2-qadam:** kurs va foizni PC ga bog'lash (kichik, xavfsiz)
* **3-qadam:** ostatka delta hisoblagichga (o'rta) — SHUNDAN KEYIN blok yechiladi
* **4-qadam:** kassa amallarga (katta, eng xavfli)

Blok faqat 3-qadamdan keyin yechiladi: blok yechilsa blob avtomat yuklanadi,
ostatka hali blobda bo'lsa u yo'qoladi.

### OCHIQ SAVOL

Ibrohim "C kategoriyada narxini o'zgartirsa bo'ladi" dedi — tushunilmadi.
Tur narxini (foizni) telefondan ham o'zgartirish kerakmi, yoki u ham faqat PC damikan?

## v163: Clouddan yuklash QAT'IY — ustiga qo'shilmaydi

Ibrohim telefonidan cloudni yukladi, lekin grammlar mos kelmadi:

```
PC (Qurilma-1)   12769.21 g   bizda 8339.56   klientda 4429.65
iPhone           12963.79 g   bizda 8339.56   klientda 4624.23
                                              farq +194.58 g
```

### SABAB — BIZDA mos, KLIENTDA mos emas

Bu tasodif emas. Ikkalasi butunlay boshqacha hisoblanadi (5047-5052):

```
bizda    = sum(t.ostatka)            // SAQLANGAN raqam, blobdan keladi
klientda = sum(klientQarzSplit(...)) // TARIXDAN qayta hisoblanadi
```

Blob to'g'ri yuklangan (bizda aynan mos). Lekin telefonda ORTIQCHA TARIX
YOZUVLARI paydo bo'lgan va ular klient qarzini 194.58 g ga oshirgan.
Ma'lumot yo'qolmagan — USTIGA QO'SHILGAN.

### IKKI XATO TOPILDI

**1. `cloudYuklab` synced ro'yxatini tozalardi**

```
localStorage.removeItem('tilla-amal-synced');   // "ko'rilgan yozuvlar"
```

Tozalangach `amalListen` oplogdagi HAMMA yozuvni `known===undefined` deb
ko'radi va `amalRecAdd` bilan blobning USTIGA qayta qo'shadi.

**2. `amalInit` versiyani 1 ga tushirardi**

```
set[r._id]=1;      // har doim 1
```

Oplogdagi haqiqiy `vaqt` (Date.now, ~1.7e12) 1 dan katta. Shuning uchun
`amalListen` dagi `dv<=known` sharti HECH QACHON rost bo'lmaydi va har yozuv
"yangilangan" deb `remove+add` qilinadi. Agar `amalRecRemoveById` yozuvni
topa olmasa (masalan blobdagi `_id` boshqacha) — remove ishlamaydi, add
ishlaydi -> IKKILANISH.

### TUZATISH

**1. `amalInit`** — mavjud versiyani tushirmaydi:

```
if(set[r._id]===undefined) set[r._id]=1;
```

**2. `cloudYuklab`** — blob YAGONA HAQIQAT. Yuklangandan keyin oplog to'liq
o'qiladi va HAMMA yozuv HAQIQIY vaqti bilan "ko'rilgan" deb belgilanadi:

```
_aRef.get().then(function(snap){
  var base = {};
  snap.forEach(function(doc){ base[doc.id] = (doc.data()||{}).vaqt || Date.now(); });
  localStorage.setItem('tilla-amal-synced', JSON.stringify(base));
  location.reload();
})
```

Shundan keyin oplogdagi eski yozuvlar ustiga QO'SHILMAYDI — faqat
yuklashdan KEYIN kelgan yangi yozuvlar qabul qilinadi.

XATO HOLATI: oplog o'qilmasa, eski `tilla-amal-synced` TOZALANMAYDI
(bo'sh baseline xavfli — hammasi qayta qo'shilardi) va ogohlantirish chiqadi.

### SINOV (t31.js)

Mantiq simulyatsiya qilindi, 3 ta oplog yozuvi bilan:

```
ESKI (synced bo'sh)   -> 3 ta qo'shildi   <- ikkilanish
ESKI (versiya=1)      -> 3 ta qo'shildi   <- bu ham ikkilaydi
YANGI (baseline)      -> 0 ta qo'shildi   OK
keyingi yangi yozuv   -> 1 ta qabul qilindi  OK
```

### IBROHIMGA AYTILGAN

* PC dagi 12769.21 g TO'G'RI — u hech qachon blob yuklamagan
* Telefondan hech narsa kiritmasin (ikkilangan yozuv cloudga chiqib PC ga o'tardi)
* Backup olsin

Tuzatilgach telefon PC dan qayta yuklab oladi va farq o'z-o'zidan yo'qoladi.

### VERSIYA IZOHI

Ibrohim so'ragan: index.html ning ENG BIRINCHI qatoriga `<!-- v163 -->`.
Shu versiyadan boshlab yozib boriladi.

## v162: Qurilma raqamlash — cloud navbat bo'yicha raqam beradi

Ibrohim: "Qurilma-1 asosiy qilamiz, mani pcim Qurilma-1 bo'lgan. Yana bitta muhim
joyi: Qurilma-1 bo'lgandan keyin luboy boshqa qurilma qo'shilsa, ketma-ketligida
cloudga kirsa 'Qurilma-1 mi' deb so'radi, u 'ha' deb yozsa u ham Qurilma-1
bo'p qolishi mumkin. Shuning uchun kim ulansa qurilmalar ketma-ketligida nomer
berib ketishi kerak."

### XATO

```
q = prompt('Bu qurilmaga nom bering...', 'Qurilma-1') || 'Qurilma-1';
```

Standart qiymat 'Qurilma-1'. Kim OK bossa — u ham Qurilma-1. BEKOR bossa ham
Qurilma-1 (`|| 'Qurilma-1'`).

Bu sinxronni BUTUNLAY o'ldiradi, chunki `cloudListen` qurilma nomiga tayanadi:

```
if (m.vaqt > lokalVaqt && m.qurilma !== mening) { ... }
```

Ikkala qurilma ham 'Qurilma-1' bo'lsa bu shart HECH QACHON rost bo'lmaydi.
Ular bir-birining o'zgarishini umuman ko'rmaydi, har biri o'zicha ishlaydi.
Ibrohim sezgan "o'zicha bo'p qolyapti" ning sabablaridan biri shu.

### YANGI

`qurilmaId()` — qurilmaning O'ZGARMAS ID si (`tilla-qurilma-id`), bir marta
beriladi. Tasodifiy, noyob, hech qachon o'zgarmaydi.

`_qurilmalar` — cloudda ro'yxat hujjati:

```
{ q7f3a9c2e: {raqam:1, nom:'Qurilma-1', birinchi:..., oxirgi:...},
  qb21d8f04: {raqam:2, nom:'Qurilma-2', ...} }
```

`qurilmaRoyxatgaQosh()` — TRANSACTION bilan ishlaydi. ID ro'yxatda bo'lsa o'z
raqamini oladi; bo'lmasa eng katta raqam + 1. Transaction shart: ikki qurilma
bir vaqtda ulansa bir xil raqam olmasin.

`qurilmaRaqam()`, `qurilmaAsosiy()` — raqam 1 bo'lsa ASOSIY.

### NOM O'ZGARTIRISH — QURILMA-1 HIMOYALANGAN

Ibrohim: "mumkin bo'vursin lekin Qurilma-1 qilolmasin ulanbo'lgandan keyin".

`_nomNormal()` harf va raqamdan boshqasini olib tashlaydi, kichik harfga
o'giradi. Shuning uchun `Qurilma-1`, `qurilma1`, `QURILMA 1`, `Qurilma - 1`,
`qUrIlMa1` — hammasi bir xil deb tanilib to'siladi.

`qurilmaNomBand(nom, royxat, ozId)` uchta narsani tekshiradi:
1. Bo'sh nom
2. `qurilma1` — faqat raqami 1 bo'lgan qurilmaning O'ZI ishlata oladi
3. Boshqa qurilmaning nomi band bo'lsa

RAQAM O'ZGARMAYDI — faqat ko'rinadigan nom almashadi.

### ABDULHAMID ROLIGA TEGMAYDI

Ibrohim aniq aytdi: "faqat bu Abdulhamid logiga ta'sir qilmasin, u alohida
har doim, unga ta'sir qilsa uni hisob-kitoblari ochib muammo bo'lishi mumkin".

`_qurilmaHamid()` qo'riqchisi UCH joyda:
* `qurilmaRoyxatgaQosh()` — darrov qaytadi, cloud ro'yxatiga umuman tegmaydi
* `qurilmaNomOzgartir()` — ishlamaydi
* `cloudQurilma()` — hamid rejimida ESKI prompt yo'li saqlanadi

Ya'ni hamid rejimida `_qurilmalar` hujjati yaratilmaydi ham, o'qilmaydi ham.

### VAQTINCHALIK NOM

Ro'yxatdan raqam kelguncha (transaction async) nom sifatida qurilma ID si
ishlatiladi. U ham NOYOB, shuning uchun `cloudListen` dagi qurilma solishtiruvi
shu paytda ham TO'G'RI ishlaydi. Raqam kelgach nom `Qurilma-N` ga almashadi.

Eski `tilla-qurilma` kaliti saqlanib qoldi — u 7 joyda o'qiladi (7094, 7140,
7145, 7234, 16164, 16210, 16382), ularga tegilmadi.

### CLOUD HOLATI OYNASI

Qurilma qatoriga qo'shildi: `ASOSIY` belgisi (raqam 1 bo'lsa), raqam, va
"nomni o'zgartirish" tugmasi. Hamid rejimida bularning hech biri ko'rinmaydi.

### SINOV (t30.js)

1. ID barqaror — ikki chaqiriqda bir xil
2. Boshqa qurilma boshqa ID oladi
3. `Qurilma-1` besh xil yozilishda ham to'sildi
4. Qurilma-1 ning O'ZI o'z nomini saqlay oladi
5. Band nom to'sildi
6. Bo'sh nom to'sildi
7. Oddiy nom ("Kassa PC") o'tdi
8. Hamid rejimi uch joyda ham to'xtatadi, `cloudQurilma` eski yo'lda qoladi
9. Raqam 1 -> asosiy, raqam 2 -> asosiy emas

### ISHLATISHDAN OLDIN

Ibrohim PC dan BIRINCHI kirishi kerak — shunda PC raqam 1 ni oladi va ASOSIY
bo'ladi. Boshqa qurilma oldin kirsa, u 1 bo'lib qoladi.

### KEYINGISI — HALI QILINMAGAN

"Jo'natish / qabul qilish" modeli. Ibrohim alohida qilishni tanladi.
Tashxis tayyor (`cloudListen` 16210 da blob qabul qilinmaydi, faqat vaqt
belgilanadi va yashil "sinxron" yoziladi — yolg'on). Hal qilinmagan savollar:
asosiyni ko'chirish, qurilmalar ro'yxatini ko'rish, eski qurilmani o'chirish.

## v161: Klient tarixi — to'lov turi belgilari, pul, filtr menyusi

Ibrohim: "Tarixda to'lov naqt yoki karta yoki aralash bo'lgan bo'lsa ko'rsatishi kerak
grammi oldida, keyin puliniyam ko'rsatishi kerak". Va: "Klient offset qilsa tarixida
to'lov bo'p turipti, o'shani offset qilinganini aytish kerak".

### TASDIQLANGAN QARORLAR

* Sof offset ham, aralash ham -> `$ Tolov` + `OFFSET` belgisi (alohida sarlavha EMAS)
* V1: aralashda HAMMA belgi ko'rinadi (`NAQT` `KARTA` `LOM`), bitta "ARALASH" emas
* Pul ajratiladi: har tur alohida qatorda
* Lom: gramm, kurs va pul UCHALASI ko'rsatiladi
* Belgi FAQAT ikki ekranda: klient tarixi va Hisobot/Tahrirlash.
  Klient hisoboti (9792) va kun tahrirlash (9881) TEGILMADI
* Filtr menyusi qoladi
* Bo'sh tur menyuda KO'RSATILMAYDI
* Jami pul SKIDKA AYIRILGAN

### MA'LUMOT ALLAQACHON BOR EDI

Tekshirildi: har to'lov yozuvida `naqtPul`, `kartaPul`, `perechPul`, `lomPul`,
`lomGramm`, `lomKurs` saqlanadi (12376). Offset esa `_kdYopish` bayrog'i bilan.
Ya'ni ESKI yozuvlarda ham hammasi ko'rinadi, qayta hisoblash kerak emas.

MUHIM: `summa` maydoni SKIDKA AYIRILGAN qiymat (12343: `sNet = s - sSk`).
Shuning uchun jami pulga qo'shimcha ayirish KERAK EMAS — bu tekshirildi,
aks holda skidka ikki marta ayirilardi.

### YANGI KOD

`TOLOV_TURLARI` — tur, harf, belgi nomi va rang bitta manbadan (dona baza
`DONA_HOLATLAR` bilan bir xil naqsh).

`_tolovTurAniq(ops)` -> `{bor:[...], lomG, lomK, ofNom, jami}`.
Guruhdagi hamma operatsiyani yig'ib, qaysi tur ishlatilganini aniqlaydi.
0.009 dan kichik summalar hisobga olinmaydi.

`_tolovPillHTML(bor)` — sarlavha yonidagi belgilar.

`_tolovPulQator(d)` — pul ajratmasi. Bitta tur bo'lsa BO'SH qaytaradi
(jami allaqachon yuqorida turibdi, takrorlash shart emas).
Lom qatori: `Lom 10.70g × 72.7$/g` -> `$778.05`.
Offset qatori: `Offset — Rasul · Oddiy dan` -> `$684.70`.

### FILTR MENYUSI

`_ktTarixFiltr` ('' = hammasi), `_ktTarixMenyu` (ochiq/yopiq), `_ktTarixKi`
(qayta render uchun klient indeksi — `openKlientDetail` boshida yoziladi).

Tugma bosilganda menyu ochiladi: Hammasi · Berildi · To'lov · Vozvrat ·
Bizda qolsin. Bo'sh turlar ro'yxatga KIRMAYDI. Bitta turdan boshqa hech narsa
bo'lmasa menyu umuman chiqmaydi (`_fBor.length>1` sharti).

Tanlangan tur keyin yo'qolsa (masalan yozuv o'chirilsa) filtr avtomatik
'Hammasi' ga qaytadi.

### ESKI OFFSET QUTISI OLIB TASHLANDI

Avval aralash holatda pastda yashil quti chiqardi:
"↳ pul offsetdan berildi — ... (Ng ishlatildi)". Endi bu ma'lumot yuqoridagi
`OFFSET` belgisi va pul qatorida ko'rinadi, quti takror bo'lib qolgandi.
Kodi o'chirilmadi, sharti `false &&` bilan o'chirildi — kerak bo'lsa qaytarish oson.

### SINOV (t29.js)

1. Faqat naqt -> `[N:500]`, jami $500
2. Naqt + karta -> `[N:1500 K:406.65]`, jami $1906.65
3. Lom -> `[L:778.05]`, gramm 10.7, kurs 72.7
4. Offset + naqt -> `[N:2000 O:684.7]`, manba "Rasul · Oddiy"
5. Skidkali -> jami $1978.84 (ikki marta ayirilmadi)
6. Bitta tur -> pul qatori chiqmadi
7. Ikki tur -> pul qatori chiqdi, lom matni to'liq

### TEGILMAGANI

* `renderKlientHisobot` (9792) va `klientGunTahrir` (9881) — Ibrohim aytdi,
  ularda belgi kerak emas
* Chekda "Aylantirildi" so'zi hali YOZILMADI — Ibrohim tasdiqlagan, lekin bu
  alohida ish (chek generatorlariga tegish kerak)

## v160: Chekda skidka SDACHA bo'lib chiqishi tuzatildi

Ibrohim: "Skidka qilingan summani oxirida sdacha db yozib qo'yvotti chekda".
Keyin aniqlashtirdi: "Sistemada to'g'ri, chekda noto'g'ri ko'rsatvotti, formula
to'g'ri lekin".

### SABAB — chek generatoridagi else tarmog'i

v156 da sotuv chekiga ortiqcha bloki yozilganda default XATO qo'yilgan edi:

```
if(tn && tn.tip==='tur')        -> Qolgan summa -> zavod tur
else if(tn && tn.tip==='bizda') -> Qolgan summa
else                            -> SDACHA          <- XATO
```

`tanlov` NULL bo'lganda (foydalanuvchi taqsimotni tanlamagan — 12506, 13475)
`else` tarmog'iga tushib "SDACHA" yozilardi.

Sistemada bu holatda hech narsa saqlanmaydi (kodda izoh bor: "Sdacha bo'lsa —
hech narsa saqlanmaydi, faqat chekda ko'rinadi"). Ya'ni kassa to'g'ri edi, faqat
qog'oz "klientga N$ qaytarildi" degan yolg'onni yozardi.

Skidka bo'lganda bu ayniqsa ko'rinardi, chunki `_lomOrtiqchaSave` (14200) skidkani
qo'shadi va to'lov to'liq bo'lmasa skidkaning o'zi ortiqcha bo'lib qolardi.

### TUZATISH

SDACHA endi FAQAT `tip==='sdacha'` aniq tanlanganda yoziladi. Tanlov yo'q bo'lsa
chekka hech narsa chiqmaydi:

```
if(ort>0.01 && tn){
  if(tn.tip==='tur' && tn.narx>0)  -> Qolgan summa -> zavod tur
  else if(tn.tip==='bizda')        -> Qolgan summa
  else if(tn.tip==='sdacha')       -> SDACHA
}
```

HISOB FORMULASIGA TEGILMADI. Ibrohim aniq aytdi: "formula to'g'ri". `_lomOrtiqchaSave`
(14200), `lomOrtiqchaPul` (13412) va boshqa hisob joylari o'z holicha qoldi.

To'lov chekida (`kTolovChekGen`) bir xil xato YO'Q edi — u `_ktSdachaPul` ni ishlatadi,
u esa faqat `tanlov.tip==='sdacha'` bo'lganda to'ldiriladi (12090). Faqat izoh qo'shildi.

### SINOV (t28.js)

1. Tanlov yo'q + ortiqcha 100 -> chekka hech narsa yozilmadi
2. `tip='sdacha'` -> SDACHA chiqdi
3. `tip='tur'` -> "Qolgan summa -> Simay 3D", SDACHA yo'q
4. `tip='bizda'` -> "Qolgan summa", SDACHA yo'q
5. Ortiqcha 0 -> hech narsa

### TAHLILDA TOPILGAN, LEKIN TUZATILMAGAN

Preview va chek ORTIQCHANI ikki xil formula bilan hisoblaydi:

```
preview 13412: lomPulJami - kerakliNarxi + skidka          // JAMI narx
chek    14200: _lomPulJamiSave - _jamiSotuvPulReal + _skidka2  // TO'LANGAN
```

Ya'ni ekranda ortiqcha chiqmasligi, chekda chiqishi mumkin. v154 da chek MATNI bir
funksiyaga birlashtirilgan edi, lekin ortiqcha HISOBI ikki joyda alohida qolgan.
Ibrohim "formula to'g'ri" degani uchun tegilmadi — lekin bu ochiq masala.

## v159: Ostatka shakllantirish endi QO'YADI (qo'shmaydi)

Ibrohim: "Ostatka dona baza shakllantirish bosgan bazaga boriga qo'shilishi keremas,
prosta shakllantirgan vesi i donasini qo'yishi kere".
Keyin aniqlashtirdi: "Umuman 0 bo'lib shakllansin boshqattan, uje u tema yopiladi".

### XATO

Ostatka ekranidagi shakllantirish USTIGA QO'SHARDI:

```
7452: if(_ostMode==='shakl') donaRegQosh(c.t, p1);      // registrga QO'SHADI
7453: if(_ostMode==='shakl') donaBazaQosh(...);          // bazaga QO'SHADI
```

Bazada 5 dona bo'lsa, yangi 5 tani skanlaganda 10 dona bo'lib qolardi.
Ostatka grammi to'g'ri qolardi (u farq bilan hisoblanadi), lekin baza va registr
shishardi. Keyingi berishda dona soni mos kelmasdi.

Dona baza ekranida bu allaqachon to'g'ri ishlardi (`donaBazaTekshirSaqla` 6273,
`rejim==='shakl'`) — eski ombor o'chirilib, keyin skan qo'shilardi. Ikki ekran
bir xil ishni ikki xil qilardi.

### TUZATISH

**Yangi funksiya `donaBazaOmborOchir(zavod, tur)`** — zavod-turning OMBOR
yozuvlarini bazadan butunlay o'chiradi, cloud'dan ham (`donaBazaCloudOchir`).
Hamma sanadan o'chadi, faqat bugungidan emas.

**`ostFormSaqla` shakl tarmog'i qayta yozildi:**

```
if(_ostMode==='shakl'){
  donaBazaOmborOchir(c.z.nom, c.t.nom);   // eski ombor butunlay o'chadi
  c.t.donalar = p1.slice();               // registr ALMASHTIRILADI
  donaBazaQosh(c.z.nom, c.t.nom, p1, sana);
}
```

Registr endi `donaRegQosh` bilan qo'shilmaydi, `=` bilan almashtiriladi.
Aks holda baza tuzatilsa ham registr shishib qolaverardi.

### NIMA O'CHADI, NIMA QOLADI

Faqat `holat==='ombor'`. Berilgan, sotilgan, vozvrat TEGILMAYDI — klientda turgan
dona shakllantirish bilan yo'qolmasligi kerak. Boshqa zavod-turlar ham tegilmaydi.

Ibrohim tanladi: eski ombor yozuvlari CHIZIB QOLDIRILMAYDI, butunlay o'chadi.
Sabab (uning so'zi bilan): "uje u tema yopiladi" — har hafta shakllantirish qilinadi,
qatlam yig'ilishi kerak emas.

### YON FOYDA — donaSlack 0 ga tushadi

`donaSlack(t) = turDona(t) - turDonalar(t).length`. Registr endi skan bilan aynan
teng bo'lgani uchun slack 0 bo'ladi. Bu MUHIM: hozir gramm bilan berilganda kod
`[roundG(g)]` soxta bitta dona yasab, registrdan topa olmay, slack tufayli JIMGINA
o'tib ketardi. Slack 0 bo'lgach `donaRegOlish` mos kelmaganini `yoq` ro'yxatiga
qo'shadi va `ozConfirmOch` ogohlantirish chiqaradi (10989, 14257).

Ya'ni Ibrohimning "endi umumiy gramm qilmayman" degani kod tomonidan eslatiladi.
DIQQAT: ogohlantirish SO'RAYDI, lekin TO'XTATMAYDI — "OK" bosilsa baribir o'tadi.

### SINOV (t27.js)

1. Ombor yozuvlari o'chdi (2 ta), berilgan/vozvrat/boshqa tur qoldi
2. Cloud'dan ham o'chirildi (`a`, `b`)
3. Hamid rolida umuman tegilmadi (0 qaytdi, baza o'zgarmadi)
4. Registr qo'shilmadi, qo'yildi (3 dona)

### TASDIQLANMAGANI

* Tasdiqlash oynasi QO'SHILMADI. Dona baza ekranida bor ("Baza to'liq
  almashtirilsinmi?"), Ostatkada yo'q. Ibrohim bu savolga javob bermadi.
* Tekshiruv rejimi (`_ostMode==='tekshir'`) TEGILMADI, hozirgidek qoladi —
  bazaga yozmaydi. Ibrohim uni keyinga qoldirdi.

## v158: Dona baza holatlari + skan kirim/vozvrat bazaga bog'landi

Ibrohim: "Dona baza nega faqat 13chida shakllangani bo'yicha qopketgan, man qolgan
kunlayam skanda donaga kirim qilganman, umuman qo'shilmayapti".

### TASHXIS

Ikkita alohida ro'yxat bor edi va ular boshqa-boshqa to'ldirilardi:

* `t.donalar` REGISTR — `donaRegQosh()` bilan, 9 joyda
* `tilla-dona-baza` BAZA — `donaBazaQosh()` bilan, atigi 4 joyda

Dona baza ekrani faqat ikkinchisini ko'rsatadi. Farq 5 joy edi.

Asosiy sabab 7473 (hozir 7506), SKAN KIRIM:

```
t.ostatka = roundG((t.ostatka||0) + total);
t.donaOst = turDona(t) + skState.pass1.length;
donaRegQosh(t, skState.pass1);      // registrga qo'shilardi
// donaBazaQosh YO'Q               <- shu yerda yetishmasdi
```

Ostatka oshgan, registr to'lgan, tarixga yozilgan — bazaga hech narsa tushmagan.
13.07 turgani: o'sha kuni shakllantirish qilingan, u yagona yo'l bo'lib bazaga yozardi
(7388, faqat `_ostMode==='shakl'` bo'lganda).

### QILINGANI

**1. `donaBazaHolat(zavod, tur, arr, holat, izoh)`** — yangi funksiya.
Yozuvni O'CHIRMAYDI, faqat holatini o'zgartiradi. Mavjud `donaBazaOlish()` ga
o'xshaydi, lekin holat parametrdan keladi (`donaBazaOlish` faqat 'berilgan' yozardi).
Faqat `holat==='ombor'` yozuvlarga tegadi.

**2. `DONA_HOLATLAR`** — holat, nom va rang bitta manbadan:

```
ombor     yashil   bizda
berilgan  ko'k     klientda
sotilgan  oltin    klient to'ladi
vozvrat   qizil    zavodga qaytdi
yoqolgan  kulrang  tekshiruvda topilmadi
```

`donaHolatMeta(h)` — holat bo'yicha rang/nom qaytaradi.

**3. Skan kirim (7506)** — `donaBazaQosh(z.nom, t.nom, skState.pass1, sana)`.
Sana `sana` o'zgaruvchisidan, tarixga yozilayotgani bilan bir xil.

**4. Skan vozvrat (7496)** — `donaBazaHolat(..., 'vozvrat')`.
Yozuv o'z kunida qoladi, faqat holati o'zgaradi.

**5. Dona baza ekrani (3-daraja)** — filtr chiplari qo'shildi. Ochilganda `Ombor`
tanlangan. Bo'sh holat chipi ko'rsatilmaydi. Kataklar holat rangida, ketganlar
chizilgan. Tagida har holat alohida qator bo'lib yakunlanadi.

**6. Zavod·tur ro'yxati (2-daraja)** — avval jami dona ko'rsatardi, endi
`N ombor · Ng` va yonida `(M ketgan)`. Sabab: jami raqam "bizda nima bor" degan
savolga javob bermaydi.

### ABDULHAMID ROLIGA TEGMAYDI

Ibrohim aniq aytdi. Skan kirim tugmasi (343, 371) `hamid-x` EMAS — ya'ni Abdulhamid
ham skan kirim qila oladi. Shuning uchun qo'riqchi funksiya ICHIGA qo'yildi:

```
if(typeof getRol==='function' && getRol()==='hamid') return;
```

`donaBazaQosh` va `donaBazaHolat` ikkalasida ham bor. Hamid rolida baza yozuvlariga
umuman tegilmaydi.

### SINOV (t26.js)

1. Vozvrat -> yozuv soni o'zgarmadi (4 ta qoldi), 2 tasining holati 'vozvrat' bo'ldi
2. `DONA_TOL = 0` -> 4.53 skanlansa bazadagi 4.52 TOPILMAYDI (aniq mos kerak)
3. 'berilgan' yozuvga tegmaydi — faqat 'ombor' o'zgaradi
4. Hamid rolida funksiya darrov qaytadi, baza o'zgarmaydi

### HAL QILINMAGANI — 'sotilgan' HOLATI

Ibrohim "sotilganini sotilgan qilib" dedi, LEKIN mexanizm aniq emas, shuning uchun
YOZILMADI. Sabab: hozir berish (10908) va sotuv (13902) IKKALASI ham 'berilgan'
yozadi. Sotuv modalida `ksg-` skan qilingan donalar — bu BERILDI qismi, sotilgan emas.
v154 da aniqlangan: sotildi = to'langan summa / narx, berildi = oldilar.gramm.
Ya'ni klient 30g olib 20g pulini to'lasa, qaysi ANIQ dona sotilganini kod bilmaydi.

Uch yo'l bor, Ibrohim tanlashi kerak:
A) sotuv modalida skan qilinganlar 'sotilgan' (lekin bu noto'g'ri — berildi != sotildi)
B) to'lov to'liq bo'lganda o'sha klientning hamma 'berilgan' donasi 'sotilgan' ga o'tadi
C) 'sotilgan' umuman kiritilmaydi, uch holat qoladi

`yoqolgan` holati ham ta'rifda bor, lekin hali hech kim yozmaydi — ostatka
tekshiruvi bilan bog'lanmagan (Ibrohim uni keyinga qoldirdi).

### TEGILMAGANI

* `ostFormSaqla` 7389 — ostatka tekshiruvi hali bazaga tegmaydi
* `donaBazaTekshirSaqla` 6239 — baza ekranidagi tekshiruv, eski ikki rejimda qoldi
* Klient vozvrati (11197, 12380, 14135) — registrga qo'shiladi, bazada 'berilgan'
  bo'lib qolaveradi
* `donaBazaRender` 7331 (zavod ekranidagi ro'yxat) — hali `r.holat!=='ombor'` deb
  ikkiga bo'ladi, besh holatga moslanmagan

## v157: CHEK tugmasi doim yoqiq ochiladi

Ibrohim: "chek chiqarishni bosadigan o'chib qolgan, kerakmas paytida o'chirardim,
umuman o'chib turipti, shuni yoqib tursin".

### Sabab

Tugma holati emas, `localStorage` dagi bayroq. Modal ochilganda holat har safar
qaytadan hisoblanardi:

```
_kbChekOn = !printerYoq();      // 10704, 10938, 11248, 12458
printerYoq() -> localStorage['tilla-printer-yoq'] === '1'
```

Ya'ni tugmani qo'lda yoqsa ham, modal yopilib qayta ochilganda yana o'chardi.

Bayroq `printXato` ichida yoqiladi: chek chiqmaganda chiqadigan oynada "OK"
bosilsa `setItem('tilla-printer-yoq','1')` yoziladi. Bir vaqt print server
o'chiq bo'lganda shu bosilgan.

### ASOSIY XATO

`tilla-printer-yoq` kodda faqat IKKI joyda uchrardi: 2023 o'qish, 2030 yoqish.
O'chiradigan joy YO'Q. Sozlamalarda ham yo'q. Bir marta bosilgan, o'sha
qurilmada cheklar abadiy o'chgan holda qolgan.

### Tuzatish

To'rt joyda `!printerYoq()` -> `true`. Chek tugmasi endi DOIM yoqiq ochiladi,
kerak bo'lmasa Ibrohim qo'lda o'chiradi (avval ham shunday ishlatardi).

`printerYoq()` funksiyasi o'chirilmadi, `printXato` ichida qoldi: printeri yo'q
qurilmada xato oynasi chiqavermasin. Bayroq endi chek tugmasiga TA'SIR QILMAYDI,
faqat xato oynasini jimlatadi.

### OCHIQ QOLGANI

Sozlamalarga "bu qurilmada printer bor / yo'q" almashtirgichi qo'shilmadi
(mockupdagi C varianti). Ibrohim faqat "yoqib tursin" dedi, C ni tasdiqlamadi.
Bayroqni o'chirish hali ham faqat konsol orqali:
`localStorage.removeItem('tilla-printer-yoq')`

## v156: Cheklar to'liq qayta ishlandi (2 chek, yangi to'lov formati, ieroglif sababi)

Ibrohim butun sistemadagi cheklarni nomerlab ko'rib chiqdi va har biriga alohida ko'rsatma berdi.
Mockup tasdiqlangandan keyin yozildi.

### 1, 2 — Berish va Vozvrat: ikkita chek

Avval bitta chek chiqardi va `kb-chek-body` / `kv-chek-body` matnini o'qib printerga yuborardi.
Endi sotuvdagidek ikkita: chek 1 klientga (logo, tagida `Rahmat`), chek 2 o'zimizga
(LOGOSIZ, tagida 2x kattalikda `[  ] Tekshirildi`).

Yangi umumiy yordamchilar (chekQur dan keyin qo'shildi):

* `chekYakun(body, W)` -> `{chek1, chek2, ekran}`. Ptichka ESC/POS bilan kattalashtiriladi:
  `ESC a 1` markazga, `GS ! 0x11` eni va bo'yi 2x, keyin normal holatga qaytariladi.
* `chekIkkiChop(cheklar, cnt)` -> chek1 (logo) yuboriladi, 2500ms dan keyin chek2 (logosiz).
  Nusxa bo'lsa har juftlik orasida 5000ms, aralashib ketmasin.

Preview endi `chekYakun(...).ekran` ni ko'rsatadi, chop esa yakunsiz tanani globalga
saqlangan holidan (`_kbChekBody`, `_kvChekBody`) qayta yig'adi. Ya'ni ekrandagi matn
printerga ketmaydi, ikkalasi ham bitta manbadan chiqadi.

Eski `RAHMAT!` (katta harf, undov bilan) hamma chekdan olib tashlandi, o'rniga `Rahmat`.

### 3 — To'lov cheki: sotuv qolipiga o'tdi

`chekQur` o'rniga yangi `kTolovChekGen(d)`. Ibrohimning ko'rsatmasi: 4-chek (sotuv)
qolipini olib, `Berildi` blokini olib tashlash (to'lovda berish yo'q).

Yangi tuzilish:

* To'lov qatoridan keyin nuqtali chiziq, tagida `Qoldi` o'ng chetda (`g` qo'shimchasisiz)
* Yakuniy blok: YORLIQSIZ yalang'och summa, `Skidka`, nuqtali chiziq,
  `Umumiy Summa` (skidkadan keyingi qiymat), `Umumiy g`
* Ostatka jadvali uch ustun: `Ostatka` / `to'landi` / `qoldi` (birinchi ustun nomi
  `eski` emas, Ibrohim shunday dedi)
* Chek 2 ham chiqadi

Pul formati: generator O'Z `fmtD` sini yozdi (`minimumFractionDigits:2`). Global `fmtD`
`.00` ni tashlab yuboradi va `1,508#` bo'lib chiqardi, sotuv cheki esa `1,508.00#` beradi.
Global funksiyaga tegilmadi, 264 joyda ishlatiladi.

`chekQur` (9137) endi hech qayerdan chaqirilmaydi. O'chirilmadi, ruxsat berilmagan.

### 3b, 3c — Ortiqcha pulning ikki holati

Ibrohim ajratdi:

* Pul zavod turidan yopilsa -> `Qolgan summa -> Zavod Tur   +Ng`
* Faqat naqd qaytarilsa -> `SDACHA   N#`

Naqd holat avval `tolovlar` ro'yxatiga manfiy qator bo'lib qo'shilardi
(`SDACHA qaytarildi`), ya'ni "Jami to'landi" ichida ko'rinardi. Endi alohida
`_ktSdachaPul` maydoni orqali yakuniy blokda chiqadi.

Uchinchi holat `tip:'bizda'` uchun `Qolgan summa` yozildi. BU MENING TAXMINIM,
Ibrohim bu holatni aytmagan.

### 4 — Sotuv chekiga skidka va ortiqcha qo'shildi

Modalda `ks-skidka` va sdacha taqsimoti allaqachon bor edi, lekin chekka chiqmasdi.
Endi `klientSotuvChekYangiGen` `skidka`, `ortiqcha`, `tanlov` ni ham qabul qiladi.

`window._ksSotuvOrtiqcha` qo'shildi (`kSotuvCalc` ichida yoziladi) — preview va chop
bir xil qiymatni ko'rsin uchun. Avval ortiqcha faqat saqlash paytidagi lokal
o'zgaruvchida bor edi, preview uni ko'ra olmasdi.

Qoldi qatori sotuvda ham nuqtali chiziq + `Qoldi` formatiga o'tdi.
Ostatka birinchi ustuni `eski` -> `Ostatka`.
Chek 2 ptichkasi kattalashtirildi.

### 6 — Ostatka hisoboti

Zavod alohida sarlavha qator bo'lib chiqardi, tur tagida turardi. Endi Ibrohim
ko'rsatgandek zavod va tur KETMA KET bitta qatorda:

```
 Simay Butterfly                          30.00g
 Simay 3D                                 12.00g
 Rasul Oddiy (biz qarz)                   +5.00g
```

Gramm `g` bilan, klient qarzi belgisiz (avval `-` bilan edi), biz qarzdor bo'lsak
`(biz qarz)` va `+`. Oxirida `JAMI` qatori qo'shildi, biz qarzdor qism MINUS bo'lib
qo'shiladi: 30 + 12 - 5 = 37.00g.

JAMI manfiy chiqsa `+` bilan yoziladi (qator konvensiyasiga mos). BU MENING QARORIM,
Ibrohim bu holatni aytmagan.

### 10 — Skan vozvrat 32 -> 48

`W = 32` -> `W = 48`. Boshqa cheklar bilan bir xil kenglikda bosiladi.

### XITOYCHA IEROGLIF: sabab topildi

Ibrohim chekda xitoycha yozuv chiqishini aytgan edi. Ikki sabab:

1. **To'lov chekida (index.html).** Tur nomi `r.zavod+' \u00b7 '+r.tur` shaklida
   yig'ilardi. `\u00b7` bu O'RTA NUQTA belgisi, UTF-8 da IKKI bayt (`C2 B7`).
   Termal printer buni bitta xitoy ierogilifi deb o'qiydi. Oddiy bo'sh joyga almashtirildi.
2. **print_server.py da.** Alohida yozilgan (pastga qarang).

Chop etiladigan hamma chek matni belgima belgi tekshirildi, boshqa non ASCII belgi yo'q.

### print_server.py TUZATILDI

Sabab 448-qatorda edi: `text.encode('utf-8', errors='replace')`. Printerga UTF-8
baytlari yuborilardi, lekin termal printer UTF-8 tushunmaydi, bir baytli codepage
kutadi. `Gʻayrat` dagi `ʻ` UTF-8 da `CA BB` ikki bayt, printer uni bitta ieroglif
deb bosadi. Ustiga faylda codepage tanlash komandasi umuman yo'q edi.

Uch o'zgarish:

1. `CANCEL_KANJI = b"\x1c\x2e"` (FS .) qo'shildi, `ESC @` dan keyin yuboriladi.
   Xitoy rejimini bekor qiladi.
2. `CODEPAGE_437 = b"\x1b\x74\x00"` (ESC t 0) qo'shildi, bir baytli CP437 tanlaydi.
3. `to_ascii(text)` funksiyasi yozildi. Chop etishdan oldin hamma non ASCII belgini
   ASCII ga o'giradi: `ʻ ʼ ' '` -> `'`, `– —` -> `-`, `·` -> bo'sh joy, `─` -> `-`,
   kirill harflar lotinga (`ў` -> `o'`, `қ` -> `q`, `ғ` -> `g'`, `ҳ` -> `h`).
   Noma'lum belgi `?` bo'ladi, ieroglif emas. Kodlash `cp437`.

`to_ascii` faqat 0x80 dan katta belgilarga tegadi, ESC/POS boshqaruv baytlari
(`\x1b`, `\x1d`, `\x1c`) 0x80 dan kichik, ular buzilmaydi. Sinovda tekshirildi:
2x ptichka baytlari o'zgarishsiz o'tdi.

### SINOVLAR

* `t23.js` — `kTolovChekGen` + `chekYakun`, kenglik va ptichka baytlari
* `t24.js` — `klientSotuvChekYangiGen` skidka va Qolgan summa bilan
* `t25.js` — Ostatka hisoboti formati va JAMI hisobi

Uchalasi ham tasdiqlangan mockup natijasiga aynan mos chiqdi.

### TEGILMAGANI

* `klientSotuvChekPrint` (14223) hali o'lik kod, o'chirilmadi
* 5a klient dublikat cheki (berish) tegilmadi
* 5b (to'lov dublikatiga skidka) hali yozilmadi
* 7, 8, 9 cheklar to'g'ri deb tasdiqlangan, tegilmadi

## v155: Sotuv modali eski to'lov qiymatini saqlab qolishi tuzatildi

Ibrohim: sotuv modali bundan oldingi klient nimaga to'lov qilgan bo'lsa o'shani saqlab qolyapti (boshqa klientga o'tganda oldingi to'lov inputlari qolib ketardi).

SABAB: kSotuvRenderTolov "Mavjud inputlar qiymatlarini saqlab qo'yamiz" (savedS/savedG/savedUst) — DOM dagi eski qiymatlarni o'qib, render'dan keyin qaytaradi (bir klient ichida foydali). LEKIN modal ochilganda / boshqa klient tanlanganda ks-zavod-list va ks-tolov-list tozalanmasdi -> eski klientning kst-s/kst-n/ksg qiymatlari DOM da qolib, savedS/savedG orqali yangi klientga ko'chardi.

TUZATISH (2 joy):
- openKlientSotuv: ks-zavod-list + ks-tolov-list innerHTML='' (modal ochilganda).
- ksSotuvPickK: render oldidan ks-zavod-list + ks-tolov-list innerHTML='' (klient tanlanganda).
Endi har klient uchun toza inputlar.

Ostatka (Ibrohim tekshirdi): hamma tur (tegilgan+tegilmagan eski qarz) allaqachon to'g'ri ko'rinadi (eskiOstMap=_klientTurQarzMap butun qarz, snapshot berish push dan OLDIN). Rasm 2 dagi Diamond eski 55.95+yangi 52.23 to'g'ri (Diamond berilgan lekin sotilmagan).

Sinov: eski 267 o'tdi. APP_VER v154.4 -> v155.

---
## v154.4: Chekka g + # qaytarildi

Ibrohim fikrini o'zgartirdi: chekka g (gramm) va # (summa) qaytsin. g -> hamma gramm joyga, # -> summa qatorlariga.

klientSotuvChekYangiGen:
- g qo'shildi: Berildi (-10.00g), JAMI berildi, sotildi gramm (10.00g x narx), qoldi (5.00g), L gramm (3.00g x kurs), Ostatka jadval har katak (0.00g/5.00g/10.00g), JAMI qatori. Umumiy g allaqachon g'li edi.
- # qo'shildi: sotildi summa (836.00#), L summa, N, Umumiy Summa.
Sinov t21/t22 g/# bilan yangilandi. Eski 267 o'tdi. APP_VER v154.3 -> v154.4.

---
## v154.3: 2 chek kesish tuzatildi (Rahmat/Tekshirildi o'rtasidan kesmasin)

Ibrohim: printer 2 chekni "Rahmat" va "Tekshirildi" o'rtasidan kesib qo'yyapti. Sabab: chek1/chek2 juda tez (1200ms) ketma-ket yuborilardi -> printer chek1'ni to'liq chiqarib kesib ulgurmasdan chek2 kelardi, o'rtadan noto'g'ri kesardi. Yana chek oxirida feed (bo'sh joy) yetarli emasdi -> kesish chizig'i oxirgi qatorni kesardi.

TUZATISH:
- chek1/chek2 oxiriga feed qo'shildi: LINE+center(...)+'\n\n\n\n' (avval bitta \n edi). Kesish chizig'i oxirgi matndan pastroqda bo'ladi.
- chek1 -> chek2 kechikishi 1200ms -> 2500ms. Printer chek1'ni to'liq chiqarib kesib ulguradi, keyin chek2 keladi.
- body (ekran preview) feed'siz qoladi (faqat print chek1/chek2 da feed).

Sinov: qisman to'lov (t22, 13/13) + eski 267 o'tdi. APP_VER v154.2 -> v154.3. Vercel deploy kerak.

---
## v154.2: Sotuv chek — qisman to'lov (sotildi != berildi) + ekran preview ham yangi format

Ibrohim TEST rejimida sinadi (rasm): berildi to'g'ri, LEKIN chek qisman to'lovni ko'rsatmadi. Oddiy 836 to'liq, 3D faqat 5g (431.5), S umuman to'lov yo'q -> lekin chekda hammasi 10g to'liq sotilgan kabi chiqdi, qoldi/ostatka yo'q. Ayni paytda ekran preview (kSotuvUpdateChek, eski TOLOVLAR format) va print (yangi format) IKKI XIL edi.

SABAB: chek funksiyasiga oldilar.gramm (=BERILDI, ksg input, 10) sotildi deb uzatilgan edi. Haqiqiy sotildi = kst-s (to'langan summa) / kst-n (narx) [3D: 431.5/86.3=5, S: 0].

TUZATISH:
- Print chaqiruvi (saqlashKlientSotuv): _sotOldilar yasaldi — gramm = HAQIQIY sotildi (kst-s/kst-n), to'lov 0 bo'lsa chekda ko'rinmaydi. berildiMap = oldilar.gramm (berildi). oldilar:_sotOldilar uzatiladi (chek gramm=sotildi, berildiMap=berildi -> qoldi to'g'ri).
- Ekran preview (kSotuvUpdateChek oxiri): eski TOLOVLAR/RAHMAT bloki o'rniga klientSotuvChekYangiGen chaqiriladi (print bilan BIR XIL mantiq: sotildi=kst-s/kst-n, berildi=oldilar.gramm, lom=ks-lg/ks-lk, eski ostatka=_klientTurQarzMap). ks-chek-body ga _cPrev.body yoziladi. Xato bo'lsa eski lines2 fallback.

Natija (Ibrohim misoli): berildi 10/10/10, sotildi 10/5/0, To'lov Oddiy 836 + 3D 431.5 (qoldi 5), S umuman yo'q, Ostatka 3D 5 + S 10 = 15. Ekran va print endi BIR XIL.

DIQQAT: str_replace paytida saqlashKlientSotuv funksiya deklaratsiyasi tasodifan o'chib ketdi -> qayta tiklandi (sintaksis tekshiruvda topildi).

Sinov: chek logika (berildi!=sotildi -> qoldi). Eski 267 sinov o'tdi. APP_VER v154.1 -> v154.2.

ESLATMA: # allaqachon v154.1 da olib tashlangan edi, lekin Ibrohim ko'rgan chek eski deploy (# bor). Yangi versiyani Vercel'ga deploy qilish kerak. Berildi=sotildi endi AJRATILDI (kst-s/kst-n orqali qisman).

---
## v154.1: Sotuv chekidan # belgisi olib tashlandi

Ibrohim: chekdan # ni hammasidan ol. klientSotuvChekYangiGen ichida 4 joyda # bor edi (To'lov summa, L, N, Umumiy Summa) -> hammasi olib tashlandi, faqat raqam qoladi. Faqat vizual (mantiq tegmagan). Node sinov o'tdi. APP_VER v154 -> v154.1.

---
## v154: Sotuv cheki YANGI FORMAT (2 chek: klient logo + o'zimizga ptichka)

Ibrohim eski murakkab sotuv chekini (offset, biz qarzdor, lom bloki, kerakli/ortiqcha) qadam-baqadam qayta dizayn qildi (ko'p mockup aylanishi). Yangi sodda format tasdiqlandi.

YANGI CHEK (48 belgi, klientSotuvChekYangiGen):
- Sarlavha: klient nom + sana (HISOB/Klientga berildi yozuvi YO'Q)
- BERILDI: har zavod-tur -gramm (g harfsiz), JAMI berildi. Hamma tur (sotilgan+sotilmagan).
- TO'LOV: sotilgan har zavod ' Nom  gramm x narx   summa #'. Qisman bo'lsa tegida '  qoldi Ng'.
- JAMI TO'LANDI: L (lom: gramm x kurs, probasiz) + N (naqd). Lom yo'q bo'lsa L qatori yo'q.
- Umumiy Summa + Umumiy g.
- OSTATKA jadval: eski | yangi | jami ustunlar (zavod bo'yicha), + JAMI qatori. Ostatka yo'q bo'lsa jadval yo'q.
- 2 CHEK bir bosishda: chek1 = klient (logo:true, "Rahmat"), chek2 = o'zimizga (logo:false, "[ ] Tekshirildi" ptichka). setTimeout 1200ms bilan ketma-ket.

INTEGRATSIYA (saqlashKlientSotuv):
- _klientTurQarzMap(k) helper qo'shildi — tur bo'yicha klient qarzi (berish-vozvrat-tolov-klientda).
- saqlashKlientSotuv boshida (oldilar dan oldin) _eskiQarzMap snapshot (sotuvdan OLDINGI ostatka).
- Chek chaqiruvida berildiMap (oldilar.gramm) + eskiOstMap (_eskiQarzMap musbat) uzatiladi.
- Eski klientSotuvChekPrint chaqiruvi olib tashlandi (funksiya ta'rifi qoldi, zararsiz).

ESLATMA (hozircha): berildi = sotildi (oldilar.gramm) — modalda alohida "sotildi" (qisman yopish) inputi hali YO'Q. Qisman yopish (berildi 100 / sotildi 80 / qoldi 20) keyingi qadam — modal input qo'shilganda ishlaydi. Chek logikasi qismanni ALLAQACHON qo'llab-quvvatlaydi (berildiMap != sotildi bo'lsa qoldi chiqadi).

Sinov (t21.js, Node, 8/8): _klientTurQarzMap (Diamond 15.50), chek1 berildi/sotildi/L/Umumiy/Rahmat, chek2 Tekshirildi, ostatka eski. Chek logika sinovi (25 test t_chek). Eski 259 sinov o'tdi. APP_VER v153 -> v154.

KEYINGI: modalga "sotildi" gramm input (qisman yopish) + eski klientSotuvChekPrint tozalash. TEST rejimida 2 chek chiqishini print_server bilan sinash.

---
## v153: Multi-qurilma o'chirish — tombstone known'dan qat'i nazar o'chiradi

Ibrohim (root cause topdi): 3-4 qurilma bir hisobda; biri yozuv o'chirsa boshqalarda DARROV o'zgarmaydi -> o'chmagan qurilma qayta sync'da o'chirilganni QAYTARADI. v152 (klient o'chirishni cloud'ga push) yetarli emas edi — chuqurroq muammo amalListen da.

SABAB: amalListen o'chirish sharti `if(known!==undefined && amalRecRemoveById(id))` — ya'ni "faqat AVVAL KO'RGAN (oplogda) bo'lsang o'chir". Lekin qurilma yozuvni oplogdan ko'rmay, to'liq cloud blob orqali olishi mumkin (known===undefined). Unda tombstone kelsa ham o'chirmasdi -> yozuv qolib, keyingi sync'da qaytardi.

RISK TAHLILI (Ibrohimga ko'rsatildi): shart izohи "ostatka hisob-increment orqali keladi" degan — lekin hisobListen (increment) v99'da O'CHIRILGAN, ostatka endi tarixdan hisoblanadi. Ya'ni shart himoya qilayotgan narsa endi yo'q. amalRecRemoveById faqat tarix massividan o'chiradi (ostatka RAQAMIga tegmaydi), topilmasa false (xavfsiz), ikki marta o'chirish xavfsiz. Risk juda past.

TUZATISH: `if(known!==undefined && amalRecRemoveById(id))` -> `if(amalRecRemoveById(id))`. Endi tombstone kelsa localda bor bo'lsa HAR DOIM o'chadi (ko'rgan-ko'rmaganidan qat'i nazar). set[id]=dv saqlanadi.

Sinov (t20.js, Node, 8/8): known bor+bor->o'chadi; known YO'Q+bor->ENDI o'chadi (bug tuzatildi); known yo'q+yo'q->xavfsiz; ikki marta->xavfsiz; zavod tarixidan ham. Eski 251 sinov o'tdi. APP_VER v152 -> v153.

NATIJA: v152+v153 birga to'liq hal qiladi — qaysi qurilma o'chirsa tombstone hammaga boradi, har biri o'z localidan o'chiradi, qaytmaydi. Avval TEST rejimida sinash tavsiya.

---
## v152: Klient tarix o'chirish — cloud'ga amalDeletePush (qaytib chiqmaydi)

Ibrohim (taxmin bilan): klient hisobotidan yozuvni o'chiraman, lekin azgina keyin QAYTIB chiqadi. Umumiy hisobotdan o'chsa chiqmaydi (taxmin).

SABAB TOPILDI: klientTarixOchir k.tarix.splice() bilan LOKALDA o'chiradi + save(), lekin cloud amal kolleksiyasidan o'chirmaydi. save->amalSyncPush faqat YANGI yozuvlarni qo'shadi (o'chirishni bilmaydi). Natijada amalListen (boshqa qurilma yoki qayta ulanish) o'sha _id ni ko'rib QAYTARADI. Mavjud amalDeletePush(op) funksiyasi bor (cloud'ga deleted:true tombstone yozadi, listener amalRecRemoveById bilan o'chiradi) — u zavod ostatka o'chirishida (6691) to'g'ri chaqirilgan, lekin klientTarixOchir da UNUTILGAN.

TUZATISH: klientTarixOchir ichida, har o'chirilgan op uchun splice'dan keyin try{ amalDeletePush(op); }catch(e){} qo'shildi (6691 namunasi bilan bir xil). Endi o'chirish cloud'ga tombstone bo'lib boradi, listener boshqa qurilmalarda ham o'chiradi, qaytmaydi.

Sinov (t19.js, Node, 5/5): berildi (19:48) 2 yozuv o'chirish -> local 1 qoldi (tolov), qolgan to'g'ri op, amalDeletePush op1+op2 (2 ta) chaqirildi. Eski 246 sinov o'tdi. APP_VER v151 -> v152.

ESLATMA (kelajakda tekshirish kerak): klientTarixTahrir gramm o'zgartirsa _id saqlanadi lekin amalSyncPush set[_id] bor deb qayta yozmaydi -> cloud'da eski qiymat qolishi mumkin (tahrir sync bug, alohida). Sotuv modali "kerakli summa" + _qarzTarkib/klientQarzSplit farqi (ekran breakdown) + katta 3D jadval hali ochiq.

---
## v151: Klient chek — FAQAT bosgan operatsiya (ostatka/tarkib olib tashlandi)

Ibrohim asl muammoni topdi (rasm bilan): berildi chekini bosdi, chek noto'g'ri Ostatka (404.85) + QARZ TARKIBI bilan chiqdi. Ekranda klient qarzi to'g'ri (412.27), lekin chekdagi Ostatka (joriyQarz = berish-vozvrat-tolov, soddalashtirilgan) klientda/manfiy berish/biz qarzni hisobga olmagani uchun noto'g'ri (404.85). Ibrohim: "berilganini print qsa bo'ldi, boshqa narsalarni chiqarmasin".

QAROR (Ibrohim tanladi): chek FAQAT bosgan operatsiyani ko'rsatsin — qarz tarkibi + ostatka YO'Q.

TUZATISH — klientChekBasit(ki,sana,soat,isBerish) to'liq qayta yozildi (127 -> 70 qator):
- ops filtri endi SANA + SOAT + tip bo'yicha (avval faqat sana -> bir kunda bir necha operatsiya bo'lsa aralashardi). soat bo'sh bo'lsa butun kun (orqaga moslik).
- isBerish -> "Klientga berildi" ro'yxati (guruh zavod||tur, kiritilish tartibida) + JAMI berildi.
- tolov/vozvrat -> shu operatsiya qatorlari (tolov: gxkurs=summa#, jami to'landi; vozvrat: +g, jami vozvrat).
- OLIB TASHLANDI: joriyQarz/Ostatka qatori, QARZ TARKIBI bo'limi, bd/bd_before/ops_grouped/qbd murakkab hisoblar (ular butun-klient hisobi edi va chekda noto'g'ri chiqardi). logo:true saqlandi, printXato.

Sinov (t18.js, Node, 20/20): berildi cheki faqat o'sha berish (boshqa kun/tolov/vozvrat YO'Q, Ostatka YO'Q, QARZ TARKIBI YO'Q); tolov cheki faqat tolov; vozvrat cheki faqat vozvrat; soat filtri (soatsiz butun kun). Eski 226 sinov o'tdi. APP_VER v150 -> v151.

ESLATMA: _qarzTarkib va klientQarzSplit farqi (klientda/manfiy berish) hali bor, lekin chekdan olingani uchun endi ta'sir qilmaydi. Ekran breakdown (10057) hali _qarzTarkib ishlatadi — agar u ham noto'g'ri ko'rsatsa alohida tuzatiladi. Sotuv modali "kerakli summa" muammosi (oldingi savol) hali ochiq. rasmdagi katta 3D jadval ochiq.

---
## v150: DONA BAZA — shakllantirish + tekshirish (skan bilan, 2 tanlov)

Ibrohim: dona baza ekraniga ikki tugma — ostatka shakllantirish (skan bilan bazaga) + keyingi hafta tekshirish (qolganini skan). Muhim: ostatka olganda ustiga qo'r-ko'rona qo'shilmaydi — tekshirilib, IKKI TANLOV so'raladi.

MOCKUP AYLANISHI: dona-baza-shakl-tekshir -> (Ibrohim: ostatka olganda shunchaki tekshiriladi) -> dona-baza-tekshir-tanlov (2 tanlov: ustiga qo'shish vs shakllantirish) -> ostatka-moslash (3-savol: ostatka moslashadimi -> A: oshadi). Yakuniy: A variant (ostatka har amalda moslanadi), ortiqcha sana bo'lsa o'sha kunga.

QO'SHILDI (dona baza 1-daraja sanalar tepasiga 2 tugma):
1. 📥 SHAKLLANTIRISH — zavod/tur select -> gramm skan (dbsk-inp, +/- Enter) -> 5xN grid -> "Bazaga qo'shish". donaBazaShaklSaqla: donaBazaQosh (ombor, bugungi sana) + ostatka +jami + donaOst +N + donaRegQosh (A variant).
2. 🔍 TEKSHIRISH — zavod/tur -> qolganini skan -> "Solishtirish". donaBazaTekshirYakun: skan vs donaBazaOmbor -> mos (ikkovida) / yoq (bazada bor skanda yo'q) / ortiqcha (skanda bor bazada yo'q). Natija jadval + 2 TANLOV:
   - ➕ USTIGA QO'SHISH (donaBazaTekshirSaqla 'qosh'): ortiqcha bazaga qo'shiladi (bugungi sana), yoqlar omborda QOLADI (tegilmaydi), ostatka +ortiqcha gramm, donaRegQosh. Ibrohim: "shakllantirdik qo'limizni, lekin 8 ta qopketgan bo'sa ustiga qo'shamiz".
   - 🔄 SHAKLLANTIRISH ('shakl'): o'sha zavod-tur ombor rekordlari o'chadi (donaBazaCloudOchir har biriga), skan = yangi haqiqat. Ostatka = eski ombor gramm olib skan gramm qo'yiladi, registr almashadi. Boshqa tur tegilmaydi.

Holat: _dbSk {rejim,zi,ti,skan[]}, _dbTekNatija. donaBazaSkanBoshla/Render/Add/Del/Bekor. donaBazaEkranYop skan ochiq bo'lsa avval uni yopadi.

Sinov (t16.js, Node, 31/31): shakl (baza 3, ostatka 50->62.11, donaOst, registr); tekshir-qosh (mos 2/yoq 1/ortiqcha 1, baza 4, yoq qoldi, ostatka +5.60); tekshir-shakl (baza=skan, boshqa tur tegilmadi, ostatka 100-9.02+12.11=103.09). Eski 197+18 qayta o'tdi. APP_VER v149.1 -> v150.

---
## v150: DONA BAZA — ostatka olish (shakl) + tekshirish (2 tanlov) skan bilan

Ibrohim: dona bazaga ostatka olish (skan bilan tekshirish) + keyingi hafta tekshirish (skan bilan qolganini solishtirish) qo'sh. Mockup aylanishi: dona-baza-shakl-tekshir -> dona-baza-tekshir-tanlov -> ostatka-moslash. QARORLAR: (1) "ostatka olganda ustiga qo'shilmaydi, shunchaki qo'limizdagi tekshiriladi". (2) tekshirishda 2 tanlov: ➕ ustiga qo'shish (baza saqlanadi, ortiqcha qo'shiladi, yo'qlar omborda qoladi) yoki 🔄 shu bo'yicha shakllantirish (baza tozalanib skan=yagona haqiqat). (3) ortiqcha qo'shilganda bugungi sanaga. (4) ostatka MOSLASHADI (A variant): qo'shilsa +ortiqcha, shakllantirsa =skan yig'indisi.

DIQQAT — DUBLIKAT TOZALANDI: avvalgi sessiyada bu funksionallik ALLAQACHON yozilgan ekan (_dbSk, donaBazaSkanBoshla/Render/Add/Del, donaBazaTekshirYakun/NatijaModal/Saqla, _dbTekQator — modal UI bilan, to'liqroq). Claude buni ko'rmay ikkinchi to'plam (_odbSk, odbSkanBoshla...) qo'shib dublikat yaratdi. Xato tuzatildi: mening dublikat blok (11239 belgi) va keraksiz HTML (odb-tugma/odb-skan konteynerlari) o'chirildi, donaBazaEkranOch/Yop avvalgi _dbSk holatiga qaytarildi. Mavjud kod ishlatiladi.

MAVJUD KOD (v150 da tasdiqlangan/test qilingan): donaBazaEkranRender 1-daraja (sanalar) da 2 tugma o'zi chizadi (📥 Ostatka olish=shakl, 🔍 Tekshirish=tekshir), odb-body ichiga. donaBazaSkanBoshla(rejim) -> _dbSk={rejim,zi,ti,skan[]}. donaBazaSkanRender: zavod/tur select + gramm input (Enter qo'shadi) + 5xN grid + yakun tugma, odb-body da. donaBazaSkanAdd/Del. donaBazaTekshirYakun: skanni ombor bilan solishtiradi -> {mos,yoq,ortiqcha} -> _dbTekNatija -> donaBazaTekshirNatijaModal (2 tanlov modal). donaBazaTekshirSaqla('qosh'|'shakl'): qosh -> donaBazaQosh(ortiqcha,bugun)+ostatka+=og+donaOst+donaRegQosh, yoqlar tegilmaydi; shakl -> eski ombor rekordlar o'chadi (donaBazaCloudOchir)+donaBazaQosh(skan)+ostatka=eskiOmbGolib+skanG+registr almashadi.

Sinov (t17.js, Node, 11/11): solishtir (18 mos/2 ortiqcha/2 yoq); qosh (ostatka +11.15, donaOst 20->22, baza 22, ombor 22, registr); shakllantirish (baza=4 skan, ostatka=skan yig'indisi 18.02, donaOst 4). Eski 215 sinov o'tdi. APP_VER v149.1 -> v150.

TUZATISH (v150 ichida): dublikat blokni o'chirganda _odbSanaTs helper (sanalarni yangi->eski sortlash) ham kesilib ketdi -> qayta qo'shildi (donaBazaEkranRender 6075 da ishlatiladi). Endi sintaksis + 226 sinov toza.

ESLATMA: bu sessiyada dublikat yaratish xatosi — kelajakda yangi funksiya yozishdan oldin grep bilan tekshirish kerak (funksionallik allaqachon bormi). rasmdagi katta 3D jadval hali ochiq.

---
## v149.1: PC modeда KASSA paneli yashirildi (mobil qoladi)

Ibrohim rasm bilan: PC modeда kassa panelini olib tashlash kerak. Faqat PC (mobilда qolsin).

TUZATISH: @media (min-width:1024px) ga `#kassa-card-pc{display:none !important;}` qo'shildi. Desktop zavod panelidan KASSA mini karta (Naqd/Lom583/999) yo'qoladi. Mobil (kassa-card-mob) tegilmadi — o'sha joyда qoladi. Faqat CSS, mantiqqa tegilmadi. APP_VER v149 -> v149.1.

---
## v149: DONA BAZA EKRANI — sana -> zavod·tur -> 5xN gramm jadval + kimga ketgani

Ibrohim: dona bazani alohida ko'rish/boshqarish ekrani. Ko'p mockup aylanishi (dona-baza-ekran -> dona-ochir-tahrir -> dona-baza-asos -> hafta-snapshot -> zavod-ostatka-hafta -> zavod-tur-kirim -> dona-baza-sana -> uzun-ism). YAKUNIY QAROR: dona baza ekrani 3 bosqichli — SANA -> zavod·turlar (nechta·gramm) -> 5 ustunli gramm jadval. Ketgan dona xira + birinchi so'z (ism, B variant), ombordagi tiniq. Katakni bossa: to'liq ma'lumot + o'chirish/tahrirlash.

QO'SHILDI: (1) Ostatka ekraniga "🗄 Dona baza" tugma (hamid-x — Abdulhamiddan yashirin). (2) Panel #ost-dona-baza + donaBazaEkranOch/Yop/Render — 3 daraja: sanalar (yangi->eski, _odbSanaTs), zavod·turlar (nechta ta + jami gramm), 5xN grid (aspect 2/1 past katak, tartib raqami + gramm, ketgan opacity .5 + qizil tasmada _odbIsm(klient)=birinchi so'z). Legenda: omborda N·Xg, ketgan N. Orqaga navigatsiya (× tugma darajama-daraja). (3) donaBazaKatakOch(id) — prompt: yangi gramm=tahrir, "ochir"=o'chirish. (4) donaBazaKatakOchir: OMBORDAGI o'chsa ostatka+registr kamayadi (donaRegOlish), BERILGAN o'chsa faqat baza. (5) donaBazaKatakTahrir: OMBORDAGI gramm o'zgarsa ostatka farqga moslanadi (donaRegOlish eski + donaRegQosh yangi), BERILGAN faqat baza. (6) donaBazaOlish ga klient parametri qo'shildi -> rekordga r.klient (kimga ketgani). Sotuv 2 joyda k.nom uzatadi (saqlashKlientBerish 10432, sotuv 13397). (7) Cloud: payloadga klient qo'shildi, donaBazaCloudOchir (delete), listen klient maydonini o'qiydi. (8) initOstatka da panel reset.

Sinov (t16.js, Node, 18/18): _odbIsm birinchi so'z (Abdulhamid Aka Andijon->Abdulhamid); sana tartibi; donaBazaOlish klient saqlaydi; o'chirish ombordagi (ostatka 100->95.89, registr, baza) vs berilgan (faqat baza, ostatka tegilmaydi); tahrir ombordagi (ostatka +0.09, registr almashadi). Eski 197 sinov qayta o'tdi. APP_VER v148.2 -> v149.

ESLATMA: "kimga ketgani" faqat BUNDAN KEYINGI sotuvlarda saqlanadi (eski berilgan donalarda klient yo'q — xira, nomsiz). 5 ustunli grid pastga cheksiz davom etadi (25 dan ko'p bo'lsa 5x6, 5x7...). rasmdagi katta 3D jadval hali ochiq.

---
## v148.2: Light theme mobil fon tuzatish (html background)

Ibrohim: light theme'да mobilда butun sahifa foni qora bo'lib qolgan (safe-area va scroll chetlarida). Sabab: html elementiga fon berilmagan edi -> body min-height:100vh bo'lsa ham, iOS PWA'да html foni tizim (qora) rangida qolib, safe-area/overscroll chetlarida ko'rinardi.

TUZATISH: html{background:var(--bg);} bitta qator qo'shildi. Endi html foni ham theme bilan o'zgaradi (light'да #f5f4f0, dark'да #0f0f0f). Boshqa hech narsaga tegilmadi. APP_VER v148.1 -> v148.2.

---
## v148.1: Skan vozvrat tugmasi rang tuzatish (light + dark)

Ibrohim rasm bilan: Skan vozvrat tugmasi light theme'да matni qora/xira, foni ochib qolgan. Sabab: tugmaga inline background:var(--red-bg) berilgan-u, LABEL rangi berilmagan (Skan kirim esa 'kirim' klassidan foydalanadi -> yashil to'g'ri). Chiqim tugmasi 'chiqim' klassini ishlatadi (fon+matn ikkalasi, ikki theme'да to'g'ri).

TUZATISH: ikkala Skan vozvrat tugmasi (mobil big-btn + desktop pc-zbtn) inline rang o'rniga 'chiqim' klassiga o'tkazildi (chiqim hamid-x). Endi Chiqim tugmasi bilan aynan bir xil: matn+ikonка qizil, fon dark'да to'q light'да och qizil. hamid-x saqlandi (Abdulhamiddan yashirin). Faqat CSS klass o'zgardi, mantiqqa tegilmadi.

Sinov: eski t15 (23) + tugmalar chiqim klassida ekani. APP_VER v148 -> v148.1.

---
## v148: SKAN VOZVRAT — zavodga qaytarish (skan kirim teskarisi) + chek

Ibrohim: "skan kirimga skan vozvrat kere, chiqim(zavodga vozvrat)ga skan, 1x2 qilib qo'shish". Ko'p mockup aylanishi (skan-vozvrat-mockup) -> Ibrohim tanlovlari -> "yoz". TANLOVLAR: (1) chekda zavod nomi KATTA 2x (double); (2) ekranda 1-skan/2-skan solishtiruv BO'LSIN (skan kirimdagi kabi); (3) chekda sana/soat YO'Q, logo YO'Q, donalab EMAS (faqat jami dona + jami gramm); (4) faqat zavod nomi (tur shart emas). Abdulhamiddan YASHIRIN.

YONDASHUV: s-skan ekrani rejim bilan qayta ishlatiladi (skState.rejim='kirim'|'vozvrat', _skRejim goTo dan oldin). Butun UI/skan mantiq (zavod/tur select, 1-skan/2-skan, ves solishtiruv, skReconcile) BIR XIL — faqat sarlavha/tugma matni, saqlash yo'nalishi va chek farq qiladi.

QO'SHILDI: (1) skRejimBoshla(r) — rejim o'rnatib s-skan ochadi. (2) initSkan rejimga qarab sarlavha (Skan kirim/vozvrat), saqlash tugmasi (✓ Kirim/Vozvrat qilish, gold/red), chek tugmasi (faqat vozvratda), ves label ni moslaydi. (3) skSaqlash BRANCHED: kirim -> ostatka+total, donaOst+dona, donaRegQosh, tip:'mol' (avvalgidek); vozvrat -> ostatka-total, donaOst-dona, donaRegOlish (topilmagan jimgina o'tadi), tip:'vozvrat'; vozvratda ostatka yetmasa ogohlantirish. (4) skVozvratChek() — 32 belgi, center('VOZVRAT SKAN'), zavod nomi ESC/POS double (GS ! 0x11) + markazlangan (ESC a 1), jami dona + jami gramm, logo:false. (5) Tugmalar 1x2: desktop (zavod panel, Skan kirim yashil + Skan vozvrat qizil hamid-x) va mobil bosh ekran (big-btn 1x2, vozvrat hamid-x). Sarlavha/ves-label/tugmalarga id (sk-title, sk-ves-label, sk-chek-btn, sk-saqla-btn).

Sinov (t15.js, Node, 23/23): kirim ostatka oshadi (100->115.74, donaOst 20->23, tip:mol); vozvrat ostatka kamayadi (100->84.26, donaOst 20->17, registrdan 3 dona olindi 5->2, tip:vozvrat); topilmagan dona jimgina o'tadi (gramm baribir ayirildi); chek logo:false, VOZVRAT SKAN, double BUTTERFLY, JAMI DONA 7 / GRAMM 38.04, sana/soat YO'Q, donalab EMAS; tugmalar 1x2 + hamid-x. Eski 174 sinov qayta o'tdi. APP_VER v147 -> v148.

ESLATMA: kirim oqimiga TEGILMADI (avvalgidek ishlaydi). Chek double shrift print_server (localhost:5000) ESC/POS GS ! 0x11 ni qo'llashini talab qiladi — qo'llamasa oddiy o'lchamda chiqadi (matn baribir to'g'ri). rasmdagi katta 3D jadval hali ochiq.

---
## v147: HAFTALIK OSTATKA — TUR SARLAVHASI OLDIGA (CHETGA) PTICHKA

Ibrohim rasm bilan: "zavoddi turini oldigayam ptichka kere tekshirib bo'l[ish uchun]" -> keyin "chetki[ga] index qil". Tur sarlavhasida ham ptichka kerak — butun turni "tekshirib bo'ldim" deb belgilash uchun, ptichka eng CHETGA (o'ng tomonga). Mockup (hafta-tur-ptichka-mockup) -> "chetki index qil".

QO'SHILDI: tur sarlavhasi qatoriga o'ng chetda mustaqil ptichka (18x18 kvadrat, klient ptichkalari bilan bir xil ko'rinish). Tur qatori endi ikki qismli: chap qism (nom + jami, bosilsa OCHILADI/yopiladi) va o'ng chetdagi ptichka (bosilsa BELGILANADI). Belgilanganda tur nomi+jami xiralashadi (opacity .5). Belgi kaliti _hoBelgi['t|zavod|tur'] — MUSTAQIL (klient ptichkalariga tegmaydi, faqat "bu turni ko'rib chiqdim" belgisi). Sessiyada, bazaga yozilmaydi.

PDF: tur qatorining birinchi ✓ ustuniga bo'sh □ qo'shildi (qo'lda belgilash uchun). Excel: mavjud Tekshir_B ustuni tur JAMI qatorida bo'sh qoladi (o'zgarmadi).

Sinov (Node, 42/42): tur ptichkasi render'da bor (haftaOstBelgi t|Butterfly|Oddiy), belgilanganda yashil ✓. Eski 132 sinov qayta o'tdi. APP_VER v146 -> v147.

ESLATMA: endi ptichka 4 joyda — tur oldida (chetda), har klient berish oldida, vozvrat oldida, (zavod darajasida yo'q). rasmdagi katta 3D jadval + Skan vozvrat modali hali ochiq.

---
## v146: HAFTALIK OSTATKA — ZAVOD->TUR->KUN->KLIENT + PTICHKA TUZATILDI

Ibrohim rasm bilan 2 shikoyat: (1) "notori qivossan — zavod Butterfly, tur Oddiy, endi chislo bo'yicha haftani qaysi kuni nimadan kimga ketgani kere" -> ierarxiya SANA->ZAVOD emas, ZAVOD->TUR->KUN->KLIENT bo'lishi kerak edi. (2) "ptichka kateginiyam kottaro qil ko'rinmayapti, tekismas bug'i bor" -> checkbox juda kichik (13px, --border rang -> ko'rinmasdi), ustunlar tekislanmagan. Mockup (hafta-zavod-tur-mockup + hafta-tuzatish-mockup) -> "boldi yoz xatosiz indexga".

O'ZGARISH: v145 da SANA->ZAVOD->KLIENT edi. Endi ZAVOD -> TUR -> KUN -> KLIENT: zavod ochsang turlari, tur ochsang o'sha turdan hafta ichida qaysi KUN kimga ketgani/qaytgani, har kun ostida o'sha kungi klientlar. Har daraja alohida yopib-ochiladi (_hoOchiq: z|zavod, t|zavod|tur; kunlar tur ichida ochiq).

PTICHKA TUZATILDI: endi 18x18px kvadrat, 1.5px --muted ramka (ko'rinadi), belgilangач yashil to'ldirilgan ✓ (#0a1a0f), raqam xiralashadi (opacity .4). Gramm yo'q katakda so'nik punktir (1px dashed, opacity .2 — bosilmaydi). Grid ustunlar bir xil: 1fr / 34px / 62px / 34px / 62px, hammasi flex align — sarlavha bilan tekis. Qatorlar 6-7px padding (barmoq uchun).

QO'SHILDI: (1) haftaOstRender to'liq qayta yozildi — D.qatorlar dan Z2 piramida quradi (zavod->tur->kun->rows), ck()/gnum() yordamchilari, gid = zavod|tur|kun|index|b yoki |v. (2) haftaOstPiramida(D) — umumiy helper (render/PDF/Excel uchun): Z2 + tartiblangan zsr/tsr/ksr qaytaradi. (3) PDF: zavod(qora)->tur(sariq)->kun(kulrang)->klient, Berish/Vozvrat oldida bo'sh checkbox. (4) Excel: Zavod;Tur;Sana;Klient;Berish;Tekshir_B;Vozvrat;Tekshir_V + tur JAMI qatorlari.

Sinov (Node, 40/40): piramida — 2 zavod, Butterfly 97.31, 2 tur (3D+Oddiy sort), Oddiy 49.27/10, 3 kun (14/15/17 vozvrat alohida kun), kunlar eskidan, 14.07 Elshod 31.17; render HTML — zavod/tur/kun, 18px ptichka box, dashed punktir, jami 130.57. Eski 132 sinov qayta o'tdi. APP_VER v145 -> v146.

ESLATMA: rasmdagi katta 3D jadval, Skan vozvrat modali (1x2 + chek, Abdulhamiddan yashirin) — hali ochiq.

---
## v145: HAFTALIK OSTATKA — SANA -> ZAVOD -> KLIENT + PTICHKA HAR GRAMM OLDIDA

Ibrohim: "zavodlar bo'yicha bo'lsin" (mockup -> ruxsat) + "ptichkani vozvrat grammi berilgan grammi oldiga qo'yish kere" (mockup -> "koddi xatosiz yoz").

O'ZGARISH: v144 da kun -> tekis klient qatorlari edi. Endi kun ochilganda ZAVOD bo'yicha guruhlanadi (har zavod o'z jami berish·vozvrat bilan, default ochiq, yopib-ochsa bo'ladi), ostida o'sha zavoddan olgan klientlar. PTICHKA endi bitta emas — HAR GRAMM oldida alohida: berilgan gramm oldida chap checkbox (ck...|b), vozvrat gramm oldida o'ng checkbox (ck...|v). Grid 5 ustun: Klient · [✓] · Berish · [✓] · Vozvrat. Belgilangan gramm xiralashadi (opacity .45). Gramm yo'q (—) katakda ptichka o'rniga kichik nuqta.

QO'SHILDI/O'ZGARDI: (1) haftaOstRender qayta yozildi — kun ichida qatorlarni zavod bo'yicha guruhlaydi (qatorlar allaqachon zavod+tur+klient sort), zavod sarlavhasi + jami, _hoOchiq[dk|zavod] bilan zavod ochiq/yopiq (default ochiq — ===false tekshiruvi), ckCell/gCell yordamchilari. (2) _hoBelgi kaliti endi dk|zavod|qatorIndex|b yoki |v. (3) PDF: sana(qora) -> zavod(sariq) -> klient, Berish/Vozvrat oldida bo'sh checkbox ustunlari (qo'lda belgilash uchun). (4) Excel: Sana;Zavod;Klient;Tur;Berish;Tekshir_B;Vozvrat;Tekshir_V.

Sinov (Node, soxta DOM, 34/34): render HTML — kun sarlavhasi, Butterfly+Jilva zavod guruhlari, zavod jami 79.21, ptichka katagi □, 5-ustun grid, jami statlar 112.47/10.00, belgilangach ✓ chiqishi. Eski 132 sinov qayta o'tdi. APP_VER v144 -> v145.

ESLATMA: rasmdagi katta 3D jadval va Skan vozvrat modali (1x2 + chek, Abdulhamiddan yashirin) — hali ochiq.

---
## v144: HAFTALIK OSTATKA — SANA BO'YICHA + PTICHKA (TEKSHIRISH)

Ibrohim rasm bilan: "klient bo'yicha emas, SANA bo'yicha — klient berganlari kere". Keyin: "faqat sana bo'sin, tagidan klientla ketma-ketligida, yoniga ptichka qo'yadigan qil tekshirish uchunam". Mockup (hafta-sana-boyicha, sodda — hafta kuni nomisiz) -> tasdiq -> kod.

O'ZGARISH: v142/v143 da tuzilish zavod->tur->klient->kun edi. Endi SANA asosiy: kun -> o'sha kuni bergan/qaytargan klientlar (zavod·tur klient yonida kichik yozuv).

QO'SHILDI: (1) haftaOstData endi {Z, D} qaytaradi — Z eski struktura (ichki, saqlanadi), D yangi: sana(kun) -> {sana, ts, b, v, qatorlar[{knom, zavod, tur, tip, sotuv, g, ts}]}; qatorlar zavod+tur+klient bo'yicha tartiblangan. (2) Render sana bo'yicha: har kun sarlavhasi (sana + kungi jami berish·vozvrat, Roboto shrift, oltin), bosilsa ochiladi; kunlar ENG ESKIDAN (ts sort). (3) PTICHKA ustuni: har qatorda checkbox (□/✓), bosilsa _hoBelgi da belgilanadi, belgilangan qator opacity:.5 bo'ladi — bloknot bilan solishtirganda "tekshirildi" belgisi. Sessiyada saqlanadi, bazaga YOZILMAYDI, hafta almashsa/panel qayta ochilsa tozalanadi. (4) PDF sana bo'yicha qayta yozildi: kun qatori qora, klient qatorlari, oxirida bo'sh ✓ ustuni (qo'lda belgilash uchun bosma). (5) Excel: Sana;Klient;Zavod;Tur;Berish;Vozvrat;Tekshirildi ustunlari, kun JAMI qatorlari bilan. (6) haftaOstNav hafta almashganda _hoBelgi+_hoOchiq tozalaydi.

Sinov (Node, 26/26): D 3 kun, eng eskidan tartib (14->15->17), kun jami (14.07=79.21), kun ichida 2 qator, qatorda knom+zavod+tur, vozvrat kuni, OBSHIY 97.31/20.00. Eski 132 sinov (t14 .Z ga moslandi) qayta o'tdi. APP_VER v143 -> v144.

ESLATMA: rasmdagi katta 3D jadval (klient bo'yicha) — Ibrohim "keyin qo'shamiz" dedi. Skan vozvrat modali (1x2 + chek, Abdulhamiddan yashirin) hali kutilmoqda. Bu ikkalasi ochiq.

---
## v143: HAFTALIK OSTATKA — SANA (KUN-KUN) QO'SHILDI

Ibrohim: "haftalik ostatkani qaysi sanada bo'lganini qo'shib ber ... sanasini ketma-ketligida, oldin eskisidan qilib". Mockup (hafta-sana-mockup, A=sana ustunda / B=kun-kun) -> B tanlandi (bloknot bilan aynan solishtirish).

QO'SHILDI: haftaOstData har klientda endi `ops[]` massivi saqlaydi — har amal {ts, sana, tip, sotuv, g}, ts bo'yicha ESKISIDAN yangisiga sort. Render: klient qatoridan keyin kun-kun qatorlar (padding-left:24px, kichik) — "14.07 Se · berish 31.17" ko'rinishida (sana, hafta kuni Ya/Du/Se/Cho/Pa/Ju/Sha, turi berish/sotuv/vozvrat, o'sha kungi gramm). PDF ga ham (padding-left:40px, kulrang qatorlar), Excel ga ham (klient ↳ sana kun turi + "(jami)" qatori). Berish/vozvrat mos ustunga, ikkinchisi "—".

Sinov (Node, 19/19): ops massivi 2 amal; ESKISIdan tartiblangan ([0]=14.07 berish, [1]=18.07 vozvrat); gramm saqlangan. Eski 147 sinov qayta o'tdi. APP_VER v142 -> v143.

ESLATMA: rasmda ko'rsatilgan 3D jadval (klientlar bo'yicha katta ro'yxat) — Ibrohim "keyin qo'shamiz" dedi, tegilmadi. sotuv belgisi (o.sotuv) op.manba==='sotuv' yoki op._sotuv bilan aniqlanadi — agar sotuvdan yozilgan berishda bu bayroq bo'lmasa "berish" deb ko'rsatiladi (gramm/jami baribir to'g'ri).

---
## v142: HAFTALIK OSTATKA — OSTATKA EKRANIDA YANGI BO'LIM

Ibrohim: "har hafta qaysi zavoddan nima chiqib ketgani haqida hisobot — kimga nechi gramm, qancha vozvrat; qo'lda bloknotimiz bor, shuni solishtiramiz". Tartib to'liq: 5 mockup aylanishi (hafta-mockup -> hafta-hisobot -> hafta-final -> hafta-jadval, 2 marta qayta ishlangan; tuzatish tushunchasi minus-nima-mockup bilan tushuntirildi) -> Ibrohim qarorlari -> "bo'ldi huddi shunaqa qo'sh, Ostatkaga, haftalik ostatka qilib" -> kod.

IBROHIM QARORLARI: (1) sotuvdan berilgani ham, Berish modalidan ham — HAMMASI kiradi ("sotilganam ostatkaga berilganam hammasi qo'limizdan chiqqani ko'rinishi kere"). (2) Har yozuv turi ALOHIDA USTUNDA: Berish ustuni · Vozvrat ustuni ("vozvrat alohida ustunda berish alohida ustunda"). (3) SOF USTUNI YO'Q ("sof keremas"). (4) Har turda jami qatori + zavodda obshiy + tepada umumiy obshiy ("har 1ta turri kegin obshiysiyam kere"). (5) Tuzatish (manfiy berish) qatori KERAK EMAS ("unaqa narsa bo'lmaydi") — manfiy uchrasa jimgina Berish ustuniga qo'shiladi. (6) Joy: OSTATKA EKRANI ("qo'sh ostatkaga haftalik ostatka qilib") — avval Hisobot tabi ko'rilgandi, oxirgi qaror Ostatka. (7) PDF + Excel ikkalasi.

QO'SHILDI: (1) Ostatka ekrani (ost-choice) ga 4-tugma "📅 Haftalik ostatka". (2) Yangi panel #ost-hafta: hafta navigatsiyasi (‹ ›, dushanba–yakshanba, faqat orqaga — _hoOffset<=0), ikki obshiy stat (BERILGAN/VOZVRAT), zavod kartalari (bosilsa ochiladi — _hoOchiq), ochilganda 3 ustunli jadval: Tur—jami (oltin fon) -> klientlar -> Zavod—obshiy (surf2 fon); qiymat 0 bo'lsa "—". (3) haftaOstData(): klient tarixidan tip berish/vozvrat, hafta ts oralig'ida; inventar:'boshlangich' KIRMAYDI (shakllantirish — zavoddan chiqmagan); tolov oplari kirmaydi; zavod->tur->klient uch daraja, roundG. (4) haftaOstPDF: oltin-sarlavha uslubi (ostHisobotPDF naqshi), zavod qora qator / tur sariq / obshiy kulrang / OBSHIY qora. (5) haftaOstExcel: CSV (;) BOM bilan, kasr vergul, Zavod;Tur;Klient;Berish;Vozvrat + JAMI/OBSHIY qatorlari. (6) initOstatka da panel reset (ekranga qaytganda yopiq).

Sinov (Node, 15/15): hafta chegarasi (18.07.2026 Sha -> Du 13.07..Ya 19.07; offset -1 -> 06.07..12.07); mockup stsenariysi — Butterfly obshiy 99.86/48.04, Oddiy jami 51.82/20.00, klient qatorlari; hafta tashqarisi KIRMADI; boshlang'ich KIRMADI; tolov KIRMADI; manfiy berish jimgina qo'shildi (41.17-10=31.17). Eski 132 sinov qayta o'tdi. APP_VER v141 -> v142.

ESLATMA: Abdulhamid roli bu tugmani ko'radi (hamid-x klassi qo'yilmadi — Ibrohim so'ramadi). Kerak bo'lsa aytilsin.

---
## v141: QULF TAQSIMOTI — FIFO QOLDI, ENDI KO'RINADI

Ibrohim rasm bilan: "kassadagi pullar qulflanmayapti, lekin chiqimlar foydani qulflashi kerak edi". Tartib: tashxis (qulf-tashxis.html, Node isboti) -> Ibrohim "fifo qolishi kere" (B variant) -> kod.

TASHXIS (Node bilan isbotlangan): FIFO navbat pulni ENG ESKI sovdalardan boshlab sarflaydi — ochiq/yopiqligini TEKSHIRMASDAN. Ibrohim holatida $95,948 chiqim navbatga tushgan, lekin eski (zavodga allaqachon topshirilgan, foydasi yopiq) sovdalar uni to'liq yutib yuborgan — bugungi ochiq Shoazim ($58) va Guli ($2,853) ga yetmagan -> "qulflanmagan — foyda suzadi". Ekranda yopiq sovdalar ko'rinmagani uchun bu sarf umuman sezilmasdi. Ildiz: v136 da navbat sessiyalariga HAMMA naqtli sovda kiritilgan, ekran (kassaSuzuvchiXaritasi) esa faqat OCHIQ qismga suzuvchi hisoblaydi — ikki ro'yxat mos emas edi.

IBROHIM QARORI: FIFO mantiq O'ZGARMAYDI (A variant — faqat ochiq sovdalarga yo'naltirish — rad etildi). B: ko'rsatish qo'shildi.

QO'SHILDI: (1) kassaQulfTaqsimot() — kassaPulAmallar (jami navbat puli, kurs>0) va kassaSuzuvchiXaritasi (har op: qopPul + ochiqEkv) dan uch raqam: YOPIQQA (ochiqEkv=0 oplarga ketgan qulf), OCHIQQA (haqiqiy ta'sir), QOLDI (sarflanmadi — sovda yetmadi). Karta/perech quli navbat puli emasligi hisobga olingan (sarflangan = min(navbat, yopiq+ochiq)). (2) CHIQIMLAR panelida uch stat ostida yangi blok "QULF TAQSIMOTI (FIFO — eng eski sovdadan)": Yopiq sovdalarga ketdi $X (kulrang) / Ochiq sovdalarni qulfladi $Y (yashil) / Sarflanmadi $Z (oltin, faqat >0 bo'lsa) + izoh. Navbat bo'sh bo'lsa blok chiqmaydi.

Sinov (Node, 6/6): eski $10,000 yopiq (zavodga 125g topshirilgan) + bugungi Guli $2,853 ochiq + chiqim $11,000 -> navbat $11,000, yopiqqa $10,000, ochiqqa $1,000, qoldi $0; FIFO TEGILMAGANI: Guli qisman 35.1% (1000/2853), eski sovdalar ulush 100% — mantiq aynan avvalgidek. Eski 126 sinov qayta o'tdi. APP_VER v140.3 -> v141.

ESLATMA: sotuv chekini yangi qolipga o'tkazish (rejalashtirilgan v141) endi KEYINGI versiyada.

---
## v140.3: SDACHA RADIOSI BOSILMASDI — AVTO-TANLOV USTIDAN YOZARDI

Ibrohim rasm bilan: "bosib almashtirib bo'mayapti". Bu safar QAT'IY TARTIB bilan: avval mockup (radio-tashxis.html, jonli buzuq/tuzatilgan rejim namoyishi), Ibrohim "bo'ldi to'g'irla" degach index.

SABAB (v137 da Claude kiritgan xato): sdachaRadioTanla tanlovni yozib kTolovCalc()/kSotuvCalc() ni chaqiradi; calc ichidagi avto-tanlov bloki SHARTSIZ ishlab foydalanuvchi bosgan `_sdachaRadio_kt/ks` ni birinchi qarzli turga QAYTA yozardi -> belgi eski joyiga sakrab qaytardi. Avto "jim xulq saqlanadi" uchun qo'yilgan edi, "faqat tanlov hali YO'Q bo'lsa" sharti unutilgan.

YECHIM: kt da avto blok `if (!window['_sdachaRadio_kt'])` ichiga olindi (guard tashqi if ICHIDA — else semantikasi o'zgarmadi, sdacha yo'qolganda tozalash joyida). ks da shart `ortiqcha > 0.01 && !window['_sdachaRadio_ks']` bo'ldi VA else `else if (ortiqcha <= 0.01)` ga o'zgartirildi — aks holda "ortiqcha bor + tanlov bor" holati else ga tushib tanlovni O'CHIRIB yuborardi (yozish jarayonida topilgan nozik joy). Modal ochilishida ikkala radio null ga tozalanadi (10378 kt / openKlientSotuv ks — allaqachon bor edi) -> birinchi renderda avto ishlaydi, jim xulq saqlanadi.

Sinov (Node, bloklarni fayldan ajratib, 7/7): kt — birinchi render avto Butterfly||Oddiy; Simay bosilgach USTIDAN YOZILMAYDI; sdacha yo'qolsa tozalanadi. ks — bir xil + tanlov obyekti else tuzatilgani uchun saqlanadi. Eski 119 sinov qayta o'tdi. APP_VER v140.2 -> v140.3.

---
## v140.2: SOTUV MODALI TO'LOV QISMI — MAYDON O'CHIRILGANDA JUFTI QOLIB KETARDI

Ibrohim 3 rasm bilan: "gramm yozib o'chirsang pul qolib ketvotti (2-rasm), pulni 0 qilsang g 0.01 qolib ketvotti (3-rasm)".

SABAB (eski xato, kSotuvTolovUpd 11969): sinxron FAQAT `> 0` da ishlardi — `if (changed==='s' && s>0 && n>0) g=s/n; else if (changed==='g' && g>0 && n>0) s=g*n;`. Maydon O'CHIRILSA yoki 0 YOZILSA shart yolg'on bo'lib, jufti ESKI qiymatida osilib qolardi: gramm o'chirildi -> pul 243.6 qoldi, hisob pul bo'yicha 3.00g deb davom etdi ("qoldi: 0.17g"); pul 0 qilindi -> gramm 0.01 qoldi (81.2 dan yaxlitlash qoldig'i), hisob "qoldi: 3.16g" ko'rsatdi.

YECHIM: `changed==='s'` va `s<=0` -> gramm ham '' ; `changed==='g'` va `g<=0` -> pul ham ''. Narx yo'q holatda (n=0) gramm yozilsa jufti TEGILMAYDI (hisoblab bo'lmaydi — avvalgidek). Hisob/saqlash/chek tarafi allaqachon `s>0`/`g>0` bo'yicha ishlaydi — endi ikkalasi birga tozalangani uchun qator butunlay hisobdan chiqadi, qo'shimcha o'zgarish kerak emas.

Sinov (Node, soxta DOM, 7/7): 2-rasm stsenariysi (257.4/3.17 -> g o'chirildi -> s ham ''); 3-rasm (s=0 -> g ham ''); oddiy oqim buzilmadi (3.17->257.40, 257.4->3.17, narx kiritilsa qayta hisob); n=0 da g yozilsa pul tegilmaydi; backspace ('') holati. Eski 112 sinov qayta o'tdi. APP_VER v140.1 -> v140.2.

---
## v140.1: OLDINGI CHEK PREVIEW'DA QOLIB KETARDI

Ibrohim: "muammo — oldingi qilingan chek preview'da qolib ketvotti, shuni tekshir". ESKI xato (v135 da ham bor edi), lekin ko'rinishdan jiddiyroq.

IKKI QAVAT:
(1) `openKlientTolov` chek preview'ga UMUMAN tegmasdi — boshqa uch modal (Berish/Vozvrat/Sotuv) hech bo'lmasa yashirardi, To'lov esa yashirmasdi ham. Natija: modalni ochsang OLDINGI klientning cheki ko'rinib turardi.
(2) BUTUN faylda `chek-body`.textContent HECH QACHON tozalanmasdi (0 ta joy) — faqat preview yashirilardi. Chop etish esa `if (_ktChekOn && chekEl && chekEl.textContent.trim())` ni tekshiradi, ya'ni YASHIRIN body dagi ESKI matn ham printerga ketishi mumkin edi (masalan yangi sovda qator bermasa: `!bor` -> preview yashirinadi, body eski matn bilan qoladi).

YECHIM: yangi `chekTozala(pre)` — preview'ni yashiradi VA body matnini o'chiradi. 8 joyga ulandi: 4 modal ochilishi (openKlientBerish/Vozvrat/Tolov/Sotuv) + early-return'lar (kTolovChekUpd `!bor`, kSotuvUpdateChek bo'sh sovda, ks ning 2 ta reset nuqtasi). Mavjud bo'lmagan elementda yiqilmaydi.

Sinov (Node, 11/11): body'da eski matn turgan holatdan chekTozala -> preview 'none', body '', chop sharti false (eski chek endi chiqmaydi); to'rt prefiks (kt/ks/kb/kv) ham; noto'g'ri prefiksda yiqilmaydi; to'rt modalning hammasida chaqiruv bor. Eski 101 sinov qayta o'tdi. APP_VER v140 -> v140.1.

---
## v140: YAGONA CHEK QOLIPI + TO'LOV CHEKI QAYTA QURILDI

Ibrohim rasm bilan: "qara chekki tartibsiz tushunarsizligini san tushuntir manga", keyin "huddi shu tartib 2ta modalda qilinsin". Mockup 5 marta aylanib tasdiqlandi.

TASHXIS (rasmdagi sotuv chekidan): hisob TO'G'RI edi (2,574.64 = naqt 1,707.04 + lom 867.60; ostatka 87.84 = 38.04+39.59+10.21), muammo KO'RINISHDA: (1) `N` IKKI marta chiqardi — TOLOVLAR bloki ham, LOM bloki ham mustaqil N/K/P yozardi; (2) "Jami to'landi 2,574.64" — u to'langan emas, sovda summasi; (3) `(31.17)` YORLIQSIZ (`rjust('', '(...)')`); (4) Ostatka sarlavhasiz boshlanardi; (5) tur o'rtada osilgan (kodda 16 ta bo'sh joy qattiq yozilgan); (6) gramm birligi yo'q; (7) klient "31.17 qayerdan?" deb tushunmasdi — 41.17 bor edi, 10 qaytardi, 31.17 to'ladi, 0 qoldi (chekda bu zanjir ko'rinmasdi); (8) sotuv cheki klient nima OLGANINI umuman ko'rsatmaydi (`oldilar` uzatiladi-yu chekka chiqmaydi).
2/3/4 — bir xil kasallik: to'lov chekida tuzatilgan, sotuv chekida qolib ketgan (v134 izohi "ikki chekda ham" degan, aslida bittasida).

ILDIZ: chek UCH joyda mustaqil qurilardi — kTolovChekUpd (to'lov), kSotuvUpdateChek (sotuv preview), klientSotuvChekPrint (sotuv chop). Biri tuzatilsa boshqasi eskiligicha qolardi.

YANGI YAGONA QOLIP (chekQur + chekTurBloki + chekRoyxat + chekG/chekR/chekC/chekPad): format BITTA joyda. Ma'lumot YIG'ISH har chaqiruvchida o'z joyida qoladi — preview sovdadan OLDINGI holatni bashorat qiladi, chop esa save() dan KEYINGI haqiqatni o'qiydi (kt: 11487 chekEl.textContent; ks: klientSotuvChekPrint alohida) — timing xavfiga tegilmadi, faqat KO'RINISH umumiy.

TUZILISH (Ibrohim tasdiqlagan): SOTUV/TO'LOV bo'limi -> har zavod-tur uchun ZANJIR (Ostatka -> +Oldi -> -Vozvrat -> -To'lov -> Qoldi; har qator faqat qiymati bo'lsa) -> JAMI SUMMA / SKIDKA / JAMI GRAMM -> to'lov turlari FAQAT HARF (L lom · O offset · N naqt · K karta · P perech) -> JAMI TO'LANDI -> SDACHA -> QOLGAN OSTATKA + JAMI OSTATKA.

IBROHIM QARORLARI (aynan): "bor edi"->"Ostatka" · "qolgan qarz"->"QOLGAN OSTATKA", "jami qarz"->"JAMI OSTATKA" · "qanday to'ladi" sarlavhasi KERAKMAS · "LOM NAQT so'zlari hammasi L N P bo'lib yozilsin" · "hamma g lani ob tasha, gramm kerakmas yozilishi" (pul '#', gramm belgisiz — ilovaning o'z konvensiyasi) · "biz qarzdor" bloki YO'Q, `+` bilan QOLGAN OSTATKA ichida · offset RAMKASIZ, lekin QAYSI zavod-turning `+` idan olingani ko'rsatilsin -> offset manbai ham o'z ZANJIRI bilan chiqadi (Ostatka +13.42 -> Offsetga ketdi -5.00 -> Qoldi +8.42) va to'lov blokida `O  Simay · Oddiy dan  400.00 #` · JAMI OSTATKA manfiylarni AYIRADI (87.84 − 8.42 = 79.42) · uzunlik ahamiyatsiz.

TO'LOV CHEKI ULANDI (kTolovChekUpd 188 -> 118 qator): 6 qadam — qatorlarni yig'ish -> lom/skidka/offsetning ISHLATILGAN ulushi (offIsh = min(offJami, kerak); avvalgi rowFrac mantiqi saqlandi) -> tur bloklari (offsetda tolG MANFIY, balans nolga qarab siljiydi; ko'rsatishda abs) -> to'lov harflari -> sdacha -> QOLGAN OSTATKA (sovdadan keyingi bashorat). `N` endi BIR joyda — takror imkonsiz.

SINOV (Node, soxta DOM, 19/19 + qolip 13/13): oddiy to'lov (41.17 -> vozvrat 10 -> to'lov 31.17 x 82.6 -> Qoldi 0.00, L+N, N bir marta, Butterfly yopilgani uchun QOLGAN OSTATKAda yo'q, Jilva 39.59 qoldi); offset (Simay +13.42 -> Offsetga ketdi -5.00 -> Qoldi +8.42, O qatori "Simay · Oddiy dan", ro'yxatda +8.42, BIZ QARZDOR bloki yo'q); ' g' birligi hech qayerda yo'q; 48 belgi buzilmadi. Eski 101 sinov qayta o'tkazildi. APP_VER v139 -> v140.

QOLDI: SOTUV cheki (kSotuvUpdateChek + klientSotuvChekPrint) hali ESKI ko'rinishda — v141 da. Ular IKKITA builder, har xil paytdagi ma'lumot bilan; birdan qayta yozilsa biror shoxobcha (offset/skidka/sdacha/oldilar) e'tibordan qolib butun sotuv oqimi to'xtashi mumkin. kassaChek (kassadan qayta chop) ham eski qolipda — Ibrohim aytmagan, tegilmadi.

---
## v139: VOZVRAT CHEKIGA "JAMI GRAMM" QO'SHILDI

Ibrohim (rasm bilan): "vozvrat jami gramm yo'q, ko'rsat" — Elshod Aka cheki: Butterfly-Oddiy +1.17g, Butterfly-3D +38.04g, jami yo'q.

kVozvratUpdateChek (10143) da qatorlardan keyin darhol LINE va RAHMAT chiqardi. Endi: LINE -> `Jami gramm  +39.21g` -> LINE -> RAHMAT.

QAROR — DOIM ko'rsatiladi, 1 qator bo'lsa ham. Sabab: TO'LOV chekining `Jami gramm` qatori (11120) shartsiz chiqadi — ilovaning o'z konvensiyasi shu. Berish chekidagi `JAMI` esa faqat 2+ qator bo'lsa chiqadi (v82 qarori) — u KO'CHIRILMADI, chunki Ibrohim shuni so'ramagan va eski qarorni meros qilib olish taqiqlangan.

Yorliq `Jami gramm` (chek konvensiyasi; `JAMI GRAMM` — bu kassa UI statining yorlig'i, chekniki emas). Format `+39.21g` — qatorlar bilan bir xil. Yig'indi roundG bilan yaxlitlanadi (0.1+0.2 -> 0.30, float qoldig'i yo'q).

CHOP ETISH: alohida tuzatish kerak emas — `saqlashKlientVozvrat` (10237) `kv-chek-body.textContent` ni o'qiydi, ya'ni AYNAN shu matn printerga ketadi. Butun faylda `Vozvrat qilindi` bitta joyda (10143) — boshqa nusxa yo'q, tekshirildi.

Sinov (Node, rasmdagi aniq raqamlar): 2 qator -> `Jami gramm  +39.21g`, o'ng chetga tekis (48 belgi); 1 qator -> +38.04g chiqadi; 0.1+0.2 -> +0.30g — 6/6. APP_VER v138 -> v139.

---
## v138: CHANGELOG index.html DAN AJRATILDI

Ibrohim: "v digi o'zgarishlani o'chirib tasha indexdan, bu adashtirvotti sani" — haqli. Claude v136 da aynan shundan xato qildi: v120 ning izohini o'qib, uning `_kartaBor` dinamik yashirish QARORINI so'ralmagan joyga ko'chirdi -> kassa paneli 3x2 bo'lmadi.

O'CHIRILDI (index.html dan):
- `</html>` dan keyingi 92 ta changelog izohi (v55 ... v137.1) — 113 KB, faylning 11.3%
- body ichida qolib ketgan 1 ta changelog izohi (v44, cloudKol/TEST_MODE)
- struktura yorliqlaridan versiya raqami: `<!-- v136: TO'LOV HISOBOTI MODALI ... -->` -> `<!-- TO'LOV HISOBOTI MODALI -->`, `<!-- Perech (v136) -->` -> `<!-- Perech -->`

QOLDI: 60 ta qisqa struktura yorlig'i (`<!-- HOME -->`, `<!-- Kurs kiritish -->` kabi) — bular navigatsiya uchun, changelog emas.
TEGILMADI: JS ichidagi `// v136: ...` izohlari — ular tegishli kodning YONIDA turadi va NEGA shunday qilinganini tushuntiradi (arxeologiyaga chaqirmaydi). Kerak bo'lsa aytilsin.

KOD O'ZGARMADI — faqat izohlar. Sinov: sintaksis toza, 481 noyob id joyida, funksiyalar joyida, 63 sinov qayta o'tdi, fayl `</html>` bilan tugaydi. APP_VER v137.1 -> v138.

QOIDA: bundan keyin versiya izohi SHU FAYLGA yoziladi, index.html ga emas. Bu fayl ARXIV — yangi kod yozganda bu yerdagi qarorlar MEROS QILIB OLINMAYDI.

---
## v55: Mobil 4 tugma ikonlari (Berish/Vozvrat/To'lov/Sotuv) izchil SVGga almashtirildi — Vozvrat=refresh uslubi, To'lov=toza matn $, hech biri emoji sifatida renderlanmaydi. Rangli fon (v54) saqlanib qoldi.

## v57: Zavod-tur detali paneliga 4-chi blok qo'shildi — 'BIZNING QARZIMIZ' (klient ro'yxatidagi barcha musbat/yashil balanslar yig'indisi, ya'ni bizga qaytgan fizik ortiqcha + pul-asosli ortiqcha to'lov). Faqat shu qiymat 0 dan katta bo'lsa ko'rinadi (3 ustundan 4 ustunga o'tadi). BIZDA/KLIENTDA/JAMI hisobi o'zgarmadi — bu faqat qo'shimcha ko'rsatkich.

## v58: Chiqim ekraniga "Kurs" kartasi qo'shildi — bitta kurs kiritiladi (583 yoki 999, ikkalasi ×1.7/÷1.7 avto sinxron), "Kunlik kurs" tugmasi tilla-kurs-bugun dan to'ldiradi, har foizli turning KURS maydoni getZavodNarx formulasi (kurs×(1+pct/100), 0.1 yaxlitlash) bilan avto to'ladi — 999 arbitraji uchun: 999 narxi 131.5 yozilsa → 583=77.4 → Butterfly 7% kirim 82.8. Foizsiz turlar tegilmaydi (qo'lda). cCalc natijasiga "bugungi narx bilan farq" qatori qo'shildi (arzon=yashil/qimmat=qizil). chiqimSaqlash, FIFO, kassaFifoModel mantiqiga TEGILMADI.

## v59: SKANER XATOSI TUZATILDI — klient modallarida (Berish/Vozvrat/To'lov/Sotuv) QR/shtrix skan qilinganda skaner yakunlovchi Enter yuborishi global Enter-saqlash tinglovchisiga (4818) oqib borib, modal darhol saqlanib chek printerga ketardi. Ikki qavat himoya: (1) kbskan-inp maydonida Enter/+/- endi stopPropagation bilan to'xtatiladi — ves ro'yxatga qo'shiladi, modal ochiq qoladi; (2) skaner-detektor: Enter oldidan 3+ belgi <35ms oraliqda kelgan bo'lsa (odam bunday tera olmaydi) — 4 klient modalida Enter-saqlash bosilmaydi, qiymat maydonda qoladi. Odam Enter bosishi (oddiy tezlikda) avvalgidek tez-saqlash qiladi. Boshqa hech narsa o'zgarmadi.

## v60: (1) SOTIB OLISH modaliga DAVR qo'shildi — sana+soat maydonlari, Hozir/Kecha tez tugmalar; kechasi olib ertasiga kiritish uchun. Yozuvga tanlangan sana/soat/sana_ts yoziladi; lomKunlik endi DAVR kunining lom kursidan (tilla-kurs-tarix dan topiladi, topilmasa qo'lda — LOM foyda to'g'ri kun kursi bilan qulflanadi); tanlangan kunga Z bo'lsa yoki orqa sana bo'lsa sariq ogohlantirish; confirm da ORQA SANA belgisi. (2) koPreview endi KASSA TA'SIRI ko'rsatadi: Naqd hozirgi→yangi (−summa), 999 yoki Lom583(ekv) cho'ntagi hozirgi→yangi (+gramm), erkin qoladi. (3) YOPILMAGAN KUN ESLATMASI — kassa qoldiq panelida: oxirgi Z dan keyingi eng eski yopilmagan kun (bugungacha) sariq banner, 'Kunni yopish' tugmasi Z modalini o'sha sana bilan ochadi, × shu sessiyada yashiradi; hali umuman Z qilinmagan bo'lsa chiqmaydi. Z YOPISH AVTOMAT EMAS — qo'lda sanash bilan qoladi.

## v61: XATO TUZATILDI — 'lomNeytral is not defined' (renderLomInto, LOM tab JAMI FOYDA kartasi). Asl faylda ham bor edi: o'zgaruvchi ishlatilgan lekin e'lon qilinmagan (eski tahrir qoldig'i), LOM tab ochilganda yoki to'lov saqlangach renderLomAnywhere orqali yiqilardi. Endi lomNeytral = olishda QULFLANGAN kurs-neytral foyda: sum((lomKunlik − narx) × gramm) barcha kirimlar bo'yicha, kassaFoyda() LOM oqimi bilan bir xil formula; lomKunlik yozilmagan eski yozuvlar hisobga kirmaydi. Kartada 'neytral: X$' — qulflangan, 'taxminiy' — faqat baholash.

## v62: SOTIB OLISH modali to'liq yangilandi (mockuplar bo'yicha): (1) Proba 999 tanlansa narx JUFTLIK bo'ladi — '583/kurs' va '999 narxi' maydonlari ×1.7/÷1.7 avto sinxron (0.1 yaxlitlash), boshqa probalarda oddiy bitta narx. (2) Kunlik asos maydoni DAVR KUNIdan avto: 999 uchun kurs×1.7 (tilla-kurs-tarix .kurs), lom uchun lom kursi (.lom); topilmasa qo'lda. (3) Preview endi: 'Pul → oltinga' NEYTRAL (qizil minus olib tashlandi — bu zarar emas, ayirboshlash), cho'ntak o'tishi, QULFLANGAN FOYDA=(kunlik−narx)×g yashil/qizil + izoh (999 da samarali kurs=narx÷1.7), erkin qoladi. (4) Tasdiqlash oynasida: Kassa qatori (naqd −$ → +g) va Qulflangan foyda (arzon/QIMMAT belgisi). (5) A-QOIDA: 999/lom spread OLISHDA qotadi (LOM oqimi, 100% kompaniya, lomNeytral/lomF shu yozuvdan hisoblanadi) — shu arzon 999 keyin zavodga topshirilganda Chiqimda KUNLIK kurs yoziladi, aks holda foyda ikki marta hisoblanadi. Sotib olish sotuvlar FIFO navbatiga TEGMAYDI — sotuvlar faqat zavod chiqimida yopiladi.

## v63: FOYDA MODELI TUZATILDI (Ibrohim 3 nuqtasi): (1) 999 SOTIB OLISHDA FOYDA QOTMAYDI — yozuvga lomKunlik=0 yoziladi, lomF/lomNeytral ga kirmaydi; preview/confirm 'TAXMINIY — chiqimda qotadi' + samarali kurs (narx÷1.7). Haqiqiy foyda zavod CHIQIMIDA tur foizi orqali FIFO bilan qotadi (chiqim kurs kartasiga samarali kursni yozish kerak) — asos har doim SOVDA muhri, bugungi zavod narxi emas; kurs oshganda arzon 999 zararni kamaytiradi, mutlaq foyda faqat 999 sovda kursidan arzon bo'lsa. Ikki marta hisoblash yo'q. (2) LOM ASOSI = ASL BAHO = davr kunining KURSI−1.5 (tilla-kurs-tarix .kurs dan; zaxira: tilla-kurs-bugun−1.5). tilla-lom-bugun (kurs−2, klient olish narxi) asos sifatida ISHLATILMAYDI — standart 76 da olishning o'zida +0.5/g bor. Yorliq: 'Asl lom baho (kurs−1.5)'. (3) Lom foydasi olishda qotishicha qoladi (gramm operatsiyasi).

## v64: XATO TUZATILDI — Klientlar > Hisobot tabida ✏ tahrir modalidagi '🗑 Ochir' tugmasi HECH QACHON ishlamasdi: klientGunTahrir kun-guruh rejimida _kopOi=-1 qo'yadi, kopEditOchir esa tarix[-1]=undefined olib indamay chiqib ketardi (confirm ham chiqmasdi). Endi kopEditOchir ikkala rejimni biladi: bitta-op (_kopOi>=0) va kun-guruh (kop-oi-list dan). Guruhda: kunning barcha operatsiyalari katta indeksdan boshlab (splice siljitmasligi uchun) o'chiriladi, har berish/vozvrat uchun zavod ostatkasi qaytariladi, o'chirilgan tolovlarning lom yozuvlari (klient tarixida ham, data.lomlar da ham) tozalanadi, confirm 'N ta operatsiya o'chirilsinmi?' deb so'raydi. Saqlash (kopEditSaqla) tekshirildi — u avvaldan to'g'ri ishlagan (gramm/kurs/summa/sana o'zgartirish, ostatka korreksiyasi, tahrir-log).

## v65: SOZLAMALARGA 'GRAMMLARNI NOLLASH (yangi davr)' qo'shildi — parol blokidan keyin, sariq tugma. NOLLANADI: barcha zavod-tur ostatkalari va tarixi, klient tarixi (balanslar avtomatik 0), data.lomlar (lom ombori + sotib olishlar), data.kassa (Z-hisoblar, tuzatishlar, zakazlar — ochiq zakazlar ham, oldindan sariq ogohlantirish bilan). QOLADI: zavodlar+sheriklar, turlar (nomlari, tilla-foiz/manual/a-b narx sozlamalari), klientlar (nom, kategoriya), kurs tarixi, mavzu/parol/printer. Himoya: parol (mavjud) + 'NOL' so'zini yozish (tugma shunda ochiladi) + nollashdan OLDIN avto backupExport (muvaffaqiyatsiz bo'lsa confirm so'raydi). KESH QOLDIG'I QOLMAYDI: barcha qoldiqlar (kassa cho'ntaklari, suzuvchi, FIFO, LOM, hisobotlar) yozuvlardan jonli hisoblanadi — yozuvlar bo'shagach o'z-o'zidan 0; nollashdan keyin barcha renderlar chaqiriladi va save() cloud bilan sinxronlaydi (TEST rejimi o'z izolyatsiyasida).

## v66: Sozlamalar (reset-parol) va Vaqt mashinasi (snap-parol) ichki parol maydonlarida Chrome parol menejeri popup'i chiqib 'parolni saqlash' taklif qilardi (bular sayt logini emas, ilova ichki paroli). Yechim: autocomplete='new-password' + noyob name + data-lpignore + readonly-onfocus trigi — brauzer endi saqlangan loginlar ro'yxatini ochmaydi va saqlashni taklif qilmaydi. Firebase login modali (login-pass, cl-parol) ATAYIN tegilmadi — u haqiqiy login, u yerda eslab qolish foydali.

## v66: MOBIL KLAVIATURA XATOSI TUZATILDI — Berish/Vozvrat/To'lov/Sotuv modallarida klient qidiruv maydoni bosilganda klaviatura chiqmasdi. Sabab: modal ochilganda setTimeout(.focus(),200) dasturiy fokus berardi; iOS Safari foydalanuvchi imo-ishorasisiz fokusda klaviaturani OCHMAYDI, maydon esa 'band' bo'lib qoladi — keyin bosilganda yangi focus hodisasi bo'lmay klaviatura umuman chiqmaydi (pastdagi ^v✓ panel ko'rinib turadi, klaviatura yo'q). Yechim: _touchQurilma aniqlash (ontouchstart/maxTouchPoints) + fokusDesktop() yordamchisi — sensorli qurilmalarda avto-fokus O'CHIRILDI (birinchi fokus foydalanuvchi bosishidan → klaviatura ochiladi), desktopda avto-fokus qulayligi saqlanadi. 5 joy almashtirildi: kb-q, kv-q, kt-q, ks-q ochilishlari va _klientResetSel(prefix).

## v67: Chrome avtoto'ldirishi klient qidiruv maydoniga saqlangan loginni ('tilla') yozib qo'yib, ro'yxat filtrланиб 'topilmadi' bo'lib qolardi — klientlar o'chgandek ko'rinardi (aslida joyida). Yechim: maydon type='search' + noyob name + yuklanishda 600ms dan keyin qiymat bo'lsa avto-tozalash va renderKlientlar.

## v68: KURS TAKROR SAQLASH TUZATILDI — hkSaqla har 'Saqlash' bosilishida tarixga yangi yozuv qo'shardi, kurs o'zgarmagan bo'lsa ham (kurs tarixi bir xil qiymatlar bilan to'lib ketardi). Endi: oxirgi yozuv SHU KUNDA va AYNAN SHU KURS bo'lsa (farq<0.001) — tarixga yozilmaydi; kurs o'zgargan bo'lsa (kun ichida ham) yangi yozuv qo'shiladi. tilla-kurs-bugun, lom, narxlar va renderlar avvalgidek yangilanadi.

## v69: DAVR KETMA-KETLIGI TUZATILDI — kurs tarixi sanalarni MATN sifatida solishtirardi ('29.06.2026'>'11.07.2026' chiqardi), roykhat/grafik/PDF/oxirgi-yozuv tartibsiz edi. Yangi yagona manba: kursTarixTs (fdSanaTs orqali haqiqiy timestamp), kursTarixSort, kursTarixOl (oqish+saralash). 8 nuqta shu manbaga otkazildi: hkSaqla (dedupe xronologik oxirgi bilan, saqlashda sort), renderKursGrafik (roykhat+grafik chizigi), renderHomeKurs (bugungi kurs paneli), kursTarixEditSave/Delete (tahrirdan keyin sort, tilla-kurs-bugun xronologik oxirgidan), hkPDFDavr (PDF xronologik), koDavrUpd (davr kunining ENG SONGGI kursi). Endi hamma joyda tartib sana+soatdan kelib chiqadi.

## v70: CLOUD ZIDDIYAT DIALOGI 3 ANIQ TUGMAGA ALMASHTIRILDI — eski oqim (confirm 'Yuklab olinsinmi?' -> yoq desa keyingi saqlashda yana confirm 'ustidan yozilsinmi?') chalkash edi, 'eski malumotni saqlash' uchun ikki bosqich kerak bolardi. Yangi modal-cloud-tanlov: (1) '☁ Shu boyicha ozgarsin' — cloudYuklab(meta), boshqa qurilma holatini oladi; (2) 'Bu qurilmaniki saqlansin' — _cloudRemoteNewer=false qoyib cloudSaqlaNow() birdan chaqiradi (eski ikkinchi confirm shart bolmay qoladi), bu qurilma holati DARHOL cloudga yoziladi; (3) 'Keyinroq hal qilaman' — hech narsa ozgarmaydi, _cloudRemoteNewer=true (avvalgi Отмена bilan bir xil xulq). cloudListen dagi eski confirm() shoxobchasi cloudTanlovOch(m) bilan almashtirildi. cloudSaqlaNow dagi eski himoya-confirm oddiy avtosaqlash paytida (foydalanuvchi 'keyinroq' tanlagandan keyin) hali ishlaydi — xavfsizlik zaxirasi sifatida qoldirildi.

## v71: DONA OSTATKA TIZIMI. (1) Har zavod-turga donaOst sanogi (grammga parallel): skan kirimda +dona, klientga berishda skan paneli ishlatilgan bolsa −dona (op.dona ham yoziladi; qolda gramm yozilsa dona nomalum — donaOst tegilmaydi, haftalik tekshiruv moslaydi). SON boyicha sanaladi, qiymat boyicha EMAS — bir xil grammli buyumlar har biri alohida dona. (2) BIZDA kartasida dona soni korinadi (>0 bolsa). (3) OSTATKA modali (zavod tarafda Skan kirim oldida, klient tarafda PDF/+Klient qatorida, mobil versiyalarda ham): Tekshirish rejimi — har turga qolda sanalgan dona+gramm kiritiladi, tizim bilan farq jonli koriladi, saqlashda confirm bilan TUZATILADI (tip:mol, inventar:'tekshiruv', ± farq; ostatka va donaOst haqiqiy sanoqqa tenglashadi, tarixda log qoladi); Shakllantirish (1-martalik) rejimi — nollashdan keyin boshlangich dona+gramm kirim yozuvi (inventar:'boshlangich') sifatida kiritiladi, bosh qoldirilgan turlar tegilmaydi. (4) SKAN KIRIM HISOBOTI — Skan kirim ekranida Excel (CSV, \ufeff BOM, ; ajratgich, vergulli kasr) va PDF (print oynasi) tugmalari: sana/zavod/tur/dona/gramm + JAMI, yangi tepada; inventar yozuvlari hisobotga KIRMAYDI.

## v72: OSTATKA MODALIGA SKAN qoshildi — har tur qatorida ⚖ tugma skan panelini ochadi: barcode har skanida +1 dona, gramm yigiladi (skParseGram — 2,59=2.59), dona/gramm maydonlari avto toladi (qolda tahrir ham mumkin), '−' oxirgisini ochiradi. Bir xil grammli buyumlar ALOHIDA dona bolib sanaladi (sinovda 3x3.55g = 3 dona). Enter/+/− stopPropagation bilan — skaner Enter'i saqlashga oqib ketmaydi. Print YOQ — faqat skan. Ikkala rejimda (Shakllantirish ham Tekshirish ham) ishlaydi; rejim almashganda skan holati tozalanadi. Sensorli qurilmada avto-fokus yoq (v66 qoidasi).

## v72.1: ⚖ ikoni ikkala skan-toggle tugmasida (ost-sb va kbskan-btn) barcode SVG ikoni bilan almashtirildi (yumaloq ramka + har xil uzunlikdagi vertikal chiziqlar, currentColor — tugma holatiga qarab rang oladi).

## v73: UNIVERSAL SKAN (uniSkan) — 4 yangi nuqtaga skan qoshildi, Berish (v71) bilan jami 5 nuqtada zanjir yopildi: (1) VOZVRAT modali tur qatorlari — skan bilan qaytsa zavodga +dona +gramm (op.dona, donaOst+=); (2) TOLOV > Vozvrat(ixtiyoriy) qatorlari — xuddi shunday; (3) SOTUV > Sotilgan gramm qatorlari — skan bilan sotilsa zavoddan -dona -gramm (berish yonalishi, donaOst-=, 0 dan pastga tushmaydi); (4) SOTUV > Vozvrat(ixtiyoriy) — +dona +gramm. Yagona naqsh: gramm maydoni yonida barcode SVG tugma -> sariq panel -> har skan +1 dona, gramm maydonga avto tushib maydonning oz oninput hisobi chaqiriladi, '-' oxirgisini ochiradi, Enter/+/- stopPropagation (v59). Skan ishlatilmasa: gramm avvalgidek, dona yozilmaydi (haftalik tekshiruv moslaydi). Har modal renderida uniSkanReset(prefix) — eski holat oqib otmaydi. Bir xil grammlar ALOHIDA dona (sinov: 2x3.55+2.10 = 3 dona).

## v74: OSTATKA MODALI TOLIQ QAYTA QURILDI — eski hamma-turlar-bir-royhat korinishi olib tashlandi, ozi kelishilgan zavod->tur->skan oqimiga otkazildi. openOstatkaModal endi tanlov ekranini (ost-choice) ochadi: 'Ostatka shakllantirish' / 'Ostatka tekshirish'. Tanlangach ost-form: Zavod select -> Tur select -> (Shakllantirishda) tur allaqachon boshlangich yozuviga ega bolsa sariq ogohlantirish, (Tekshirishda) kok panelda tizim hisobi (dona+gramm) -> bitta umumiy SKAN maydoni (Skan kirimdagi uslub: barcode input + Dona/Skan jami stat-kartalari, +/- tugmalari, Enter/+/- stopPropagation) -> Tekshirishda skan qilgan sari farq jonli korinadi (mos/yetishmayapti/ortiqcha) -> Saqlash: bitta tur uchun tip:mol yozuvi (inventar:boshlangich yoki tekshiruv), ostatka+donaOst yangilanadi, so'ng skan tozalanib xuddi shu ekranda BOSHQA TURGA otish mumkin ('Ortga' bosib yangi zavod/tur tanlash yoki tepadagi tur select'ni almashtirish — ostTurChange avtomatik skan holatini tozalab ogoh/sistema panelini yangilaydi). Eski funksiyalar (ostRejim/ostRowsChiz/ostUpd/ostSaqla/_ostSkan/ostSkanToggle/Add/DelLast/Apply) OLIB TASHLANDI, ornini ostChoice/ostZavodChange/ostTurChange/ostCurTur/ostFAdd/ostFDel/ostFRender/ostFormSaqla egalladi.

## v75: OSTATKA SKAN PANELI Skan kirim ekrani bilan bir xil boylikka ozgardi (foydalanuvchi solishtirib 'juda sodda' dedi). Qoshildi: USB/Bluetooth qollanma matni, va eng muhimi — RAQAMLANGAN SKAN ROYXATI (# | Gramm | ×) skRender bilan bir xil uslubda: eng yangi skan tepada va sariq fonda ajratiladi, har qatorni alohida × bilan ochirish mumkin (faqat oxirgisi emas — ostFRemoveAt(i) istalgan indeksni ochiradi, dona/gramm kartalari va farq darhol qayta hisoblanadi). Yangi funksiya: ostFRemoveAt. ost-f-l (bitta qatorli matn) olib tashlandi, ornini ost-f-rows (toliq royhat) egalladi.

## v76: ZAVOD/TUR SELECTLAR TUZATILDI — ost-zavod va ost-tur klass-siz native <select> edi, shuning uchun brauzerning xunuk sistema-dropdown korinishida chiqardi (Skan kirimdagi chiroyli select'dan farqli). Endi ikkalasi <div class="field"> ichiga olindi — xuddi Skan kirim ekranidagi (sk-zavod/sk-tur) bilan bir xil CSS (.field select): yumaloq burchak, maxsus chevron ikonka, katta font, gold fokus rangi. Boshqa hech narsa ozgarmadi — ostZavodChange/ostTurChange mantigi avvalgidek.

## v77: OSTATKA SKANIGA 1-SKAN/2-SKAN QOSHILDI (Ibrohim: 'shakllantirganda ham skanni tekshirish uchun kerak'). Zavod bergan ves qatorisiz — bu joyda kutilgan gramm yoq (Skan kirimdan farqli), lekin ikki pass va reconciliation logikasi AYNAN bir xil qayta ishlatildi: skReconcile endi ixtiyoriy parametr qabul qiladi (skReconcile(p1,p2) — parametrsiz chaqirilsa Skan kirim skState.pass1/2 bilan avvalgidek ishlaydi, ozgarish yoq). Yangi _ostSk={mode,pass1,pass2} holati va ostSk* funksiyalar toplami (Arr/Reset/SetMode/Add/DelLast/RemoveAt/Render) — sk*/skState bilan bir xil arxitektura, lekin Ostatka uchun mustaqil namespace. 2-skan toldirilsa comparison paneli (kam/ortiq, Skan kirimdagi 'Solishtirish' korinishida) darhol chiqadi. SAQLASHDA: rasmiy sanoq HAR DOIM 1-skan (Skan kirimdagi qoida bilan bir xil) — 1/2-skan mos kelmasa 'Diqqat: mos kelmadi... 1-skan boyicha davom etilsinmi?' sorab, tasdiqlansa 1-skan asosida davom etadi. Tekshirish rejimidagi tizim-bilan-farq ham HAR DOIM 1-skanga qarab hisoblanadi (2-skan faqat ozini tekshirish uchun, yakuniy hisobga kirmaydi).

## v78: OSTATKA MODAL -> TOLIQ EKRAN (screen) ga otkazildi — Skan kirim (s-skan) bilan bir xil naqsh, kichkina popup ornida. Yangi <div class="screen" id="s-ostatka">: back-row (← tugmasi s-home ga, sarlavha 'Ostatka'), ichida ikkita .card: ost-choice (2 tanlov tugmasi) va ost-form (zavod/tur/skan, avvalgidek). 4 ta chaqiruv nuqtasi (zavod desktop/mobil, klient desktop/mobil) openOstatkaModal() dan goTo('s-ostatka') ga otkazildi; goTo() ichiga 'if(id==='s-ostatka') initOstatka();' qoshildi. openOstatkaModal -> initOstatka (endi classList.add('open') kerak emas, goTo o'zi screen almashtiradi). modal-overlay/modal-title/modal-handle/closeModal butunlay olib tashlandi. Ichki mantiq (ostChoice/ostZavodChange/ostTurChange/ostSk*/ostFormSaqla) OZGARMADI — faqat tashqi konteyner almashdi. 'Ortga' tugmasi hali ham forma->tanlov (screen ichida), yangi tepadagi ← esa screen->s-home.

## v79: KLIENT OSTATKA SHAKLLANTIRISH qoshildi. Ostatka tugmasi endi 2 xil kontekstda ishlaydi: Zavod tarafdan (openOstatkaZavod, _ostCtx='zavod') — avvalgi zavod/tur/skan oqimi ozgarmadi; Klient tarafdan (openOstatkaKlient, _ostCtx='klient') — ost-choice/ost-form ORNIGA darhol Klient QIDIRUV+ROYXAT (ost-kl-search, qidiruv maydoni + bosilganda tanlash, allaqachon shakllantirilganlar '✓ shakllantirilgan' belgisi bilan) ochiladi. Klient tanlangach (ost-kl-form): barcha zavod-turlar royxati, har birida joriy balans hinti ('hozir: Xg', manfiy bolsa '(biz qarz)') va GRAMM input (musbat=klientda, MANFIY='-' yozilsa bizning qarzimiz — mavjud renderZavod/klientQarzSplit formulalari buni avtomatik togri joyga qoyadi, qoshimcha kod kerak emas). Saqlash (ostKlSaqla): faqat toldirilgan qatorlar uchun k.tarix.push({tip:'berish', gramm, inventar:'boshlangich'}) — ZAVOD OSTATKASIGA (t.ostatka) HECH QACHON TEGMAYDI (oddiy Berish modalidan farqli). Saqlagach avtomatik 'keyingi klient' uchun qidiruvga qaytadi (konveyer). MUHIM TUZATISH: 2 ta ochirish funksiyasi (kopEditOchir va kun-guruh ochirish, ~11055-qator) endi op.inventar==='boshlangich' bolsa 'berish' ochirilganda ZAVOD OSTATKASINI QAYTARMAYDI (avval har qanday 'berish' ochirilsa avtomatik +gramm qilib zavodga qaytarardi — bu boshlangich yozuvlar uchun XATO bolar edi, chunki ular hech qachon zavoddan chiqmagan). Sinov: musbat/manfiy gramm togri saqlanishi, zavod ostatka ozgarmasligi, ostKlTurQarz orqali KLIENTDA/BIZNING QARZIMIZ ga togri qoshilishi, boshlangich ochirilganda zavod tegilmasligi — hammasi tasdiqlandi.

## v80: (1) SKAN BLOK DIZAYNI Skan kirimga moslashtirildi — sarlavha 'SKAN — har buyum +1 dona' -> faqat 'SKAN', placeholder 'Barcode skan qiling...' -> 'Gramm skan qiling...' (faqat Ostatka blokida, uniSkan/kbskan ga tegilmadi). (2) VARIANT B: Tekshirishda farq YOQ bolsa endi HAM log yoziladi — avval 'Farq yoq — saqlash shart emas' deb hech narsa saqlamasdan chiqib ketardi, endi c.t.tarix ga {inventar:'tekshiruv', mos:true, dona:0, gramm:0} yoziladi (ostatka/donaOst ga tasir qilmaydi, faqat audit izi) — 'qaysi kunda tekshirdik' savoliga hisobotda javob boladi. (3) OSTATKA HISOBOTI (Excel/PDF) qoshildi — s-ostatka ekranining back-rowida (Skan kirimdagi joylashuv bilan bir xil). ostHisobotData() ZAVOD (barcha zavod-tur tarixidan inventar='boshlangich'/'tekshiruv', mos bolsa dona/gramm='mos' korinishida) VA KLIENT (barcha klientlar tarixidan tip='berish'+inventar='boshlangich', dona='—' — klientda dona kuzatilmaydi) yozuvlarini BIRGA, sana boyicha yangi-tepada tartiblab beradi. Excel — CSV (BOM, ; ajratgich, vergulli kasr, JAMI qatori), PDF — chop etish oynasi (Sana/Manba/Nom/Turi/Dona/Gramm ustunlari). Sinov: mos-log saqlanishi va ostatkaga tasir qilmasligi, hisobotda zavod+klient qatorlari togri aralashishi, Excel/PDF chaqiruvi xatosiz ishlashi tasdiqlandi.

## v81: DONA REGISTRI (t.donalar) — har zavod-turga qaysi ANIQ ogirliklardagi donalar borligi endi saqlanadi (donaOst/ostatka umumiy sonlarga PARALLEL). Maqsad: Ostatkada notogri tur skan qilinsa (masalan Oddiyga boshqa turning donalari kirgizilsa), keyinchalik shu turdan mos kelmaydigan ogirlik berilsa OGOHLANTIRISH chiqishi. Yordamchi funksiyalar: turDonalar, donaSlack (donaOst-donalar.length — eski/registrsiz davrdan qolgan noma'lum-shakl donalar, ular bilan solishtirilmaydi, vaqt otishi bilan ozi yopiladi), donaRegQosh (kirim/qaytish — ogirlik qoshiladi), donaRegOlish (chiqim — DONA_TOL=0.05g tolerantlik bilan mos qidiradi, topilsa registrdan oladi, topilmasa-va-slack-yoq-bolsa 'yoq' royxatiga qoshadi), donaTekshirVaOgohlantir (Berish/Sotuv saqlashdan OLDIN chaqiriladi — mos kelmasa confirm: 'Bu ogirlikda dona ROʻYXATDA YOʻQ! ... Baribir davom etilsinmi?', foydalanuvchi tanlagan A-qoida boyicha YUMSHOQ ogohlantirish — bekor qilsa saqlash toxtaydi, tasdiqlasa avvalgidek davom etadi). QAMROV — barcha 7 nuqta: Skan kirim va Ostatka Shakllantirish → donaRegQosh; Ostatka Tekshirish (mos ham, tuzatish ham) → REGISTR TOLIQ ALMASHTIRILADI (t.donalar=p1.slice(), chunki tekshiruv = 'hozirgi haqiqat'); Berish (kbSkan) va Sotuv>Sotilgan gramm (uniSkan) → saqlashdan OLDIN donaTekshirVaOgohlantir (bekor qilsa butun saqlash toxtaydi), saqlashda donaRegOlish; Vozvrat, Tolov>Vozvrat, Sotuv>Vozvrat (uniSkan) → donaRegQosh (qaytgan ogirlik registrga qoshiladi, foydalanuvchi sozi bilan). Yangi uniSkanArr(fid) yordamchisi qoshildi (uniSkanDona yonida) — skan sessiyasining togri ogirliklar massivini qaytaradi. Sinov: registrga qoshish, mos-kelmaslikda ogohlantirish+bekor, tasdiqlab-davom-etish, mos topilganda togri olinishi, SLACK (eski registrsiz zaxira) jim otkazilishi va slack tugagach qattiq tekshira boshlashi, va Ibrohimning aynan holati (notogri shakllantirish -> mos kelmaydigan berish -> ogohlantirish -> ikkala yol) — hammasi tasdiqlandi.

## v82: KLIENTGA BERISH — 2 yaxshilash. (1) Har tur qatoriga 'Klientda: Xg → Yg' qatori qoshildi (mavjud 'ostatka'/'bizda' qatorlaridan pastda, kok rangda) — ostKlTurQarz(k,zNom,tNom) orqali klientning shu zavod-turdagi JORIY balansi hisoblanadi (data-turqarz atributida saqlanadi), berishOstatkaUpdate ichida input ozgarganda jonli 'oldin → keyin' korsatiladi (manfiy/tuzatish qiymatlarda ham togri ishlaydi). Klient tanlanmagan bolsa bu qator korinmaydi. (2) CHEKKA JAMI qatori qoshildi — 2 va undan kop tur berilganda LINE bilan RAHMAT orasiga qalin 'JAMI: -Ng' qatori (barcha qatorlar yigindisi); FAQAT 1 ta tur bolsa korsatilmaydi (ozining takrori bolib qolmasligi uchun). Sinov: klientda oldin->keyin togri hisoblanishi (musbat va manfiy holatda), va chekda 2 tur uchun JAMI -24.00g togri chiqishi, 1 tur uchun chiqmasligi tasdiqlandi.

## v83: OSTATKA HISOBOTIGA DONA TAFSILOTLARI qoshildi. (1) ostFormSaqla endi HAR UCH holatda ('mos', shakllantirish, tekshiruv-tuzatish) tarix yozuviga donalar:p1.slice() ham yozadi — skan qilingan aniq ogirliklar ketma-ketligi saqlanadi (avval faqat jami dona/gramm yozilardi). (2) Yangi ostHisobotDonalar() — barcha zavod-tur tarixidan donalar mavjud yozuvlarni yigib, har bir donani alohida qator qilib beradi (Sana, Zavod·Tur, #, Gramm), yangi voqea tepada va # ichida ortib boruvchi tartibda; donalarsiz eski yozuvlar bu royxatga kirmaydi. (3) Excel (ostHisobotExcel) — mavjud jamlangan jadvaldan keyin ikkinchi bolim: '↓ Dona tafsilotlari' sarlavhasi + Sana;Zavod·Tur;#;Gramm jadvali, faylning ozida ketma-ket. (4) PDF (ostHisobotPDF) — rangli qayta ishlandi: oltin sarlavha (#b8860b) asosiy jadval uchun, 'Shakllantirish'/'Tekshiruv' endi rangli badge (yashil/kok, border-radius pill), zebra qator fonlari, JAMI qatori qora fonda; pastda qora sarlavhali ikkinchi jadval — dona tafsilotlari. Manfiy dona/gramm qiymatlarida qosh-belgi xatosi yoq (typeof tekshiruvi bilan togrilandi — avval '+-1' korinishi mumkin edi). Sinov: 3+2 dona togri yigildi va tartiblandi, Excel/PDF chaqiruvi xatosiz, manfiy son togri korsatilishi, rangli badge va ikkinchi jadval mavjudligi tasdiqlandi.

## v84: DONA MOS-KELMASLIK OGOHLANTIRISHI window.confirm() ga TAYANISHDAN sahifa-ichi maxsus modalga (modal-ozconfirm) otkazildi. SABAB: PWA/uy-ekran-yorligi yoki ayrim ichki brauzerlarda window.confirm() korinishsiz avtomatik 'OK' qaytarishi mumkin — foydalanuvchi hech narsa kormaydi, xato ogirlik bemalol qabul qilinadi (Ibrohim aniq shu holatni topdi: PDF/Excel togri, lekin ogohlantirish umuman chiqmasdi). YECHIM: (1) donaTekshirVaOgohlantir OLIB TASHLANDI, ornini SOF hisoblovchi donaMosEmaslarniTop(t,arr) (UI chaqirmaydi, faqat mos kelmagan ogirliklar royxatini qaytaradi) va donaMismatchMatn(royxat) (bir nechta tur uchun BIRLASHTIRILGAN ogohlantirish matnini quradi) egalladi. (2) Yangi ozConfirmOch(msg,cb)/ozConfirmJavob(ok) — HTML/CSS bilan chizilgan modal (window API emas), cb orqali asinxron javob qaytaradi — har qanday muhitda (PWA, webview, oddiy brauzer) bir xil ishonchli korinadi. (3) saqlashKlientBerish va saqlashKlientSotuv ASINXRON oqimga otkazildi: avval BARCHA qatorlar boyicha mos-kelmasliklar SOF hisoblanadi (hech qanday UI chaqirilmasdan), agar topilsa — bitta BIRLASHTIRILGAN ozConfirm oynasi ochiladi va asosiy saqlash mantigi ichki nomlangan funksiyaga (davomEt / _sotuvDavomEt — yopilish orqali tashqi ozgaruvchilarga kirishadi) kochirilib, faqat foydalanuvchi 'Baribir davom etish' bossagina chaqiriladi; hech qanday mos-kelmaslik bolmasa darhol davom etadi, oyna umuman korinmaydi. Sinov: haqiqiy Ibrohim stsenariysi (5 dona shakllantirilgan, 11g skan bilan berilgan) qayta yaratildi — endi ozConfirm modali TOGRI ochiladi, 'Bekor' bosilsa hech narsa saqlanmaydi va zavod ostatkasi ozgarmaydi, 'Baribir davom' bosilsa togri saqlanadi va ostatka kamayadi.

## v85: HAQIQIY ILDIZ TOPILDI VA TUZATILDI — grammNollash() (v65, dona-registridan ANCHA OLDIN yozilgan) faqat tt.ostatka=0 va tt.tarix=[] qilardi, lekin tt.donaOst va tt.donalar ga UMUMAN TEGMASDI! Natijada: agar biror turda ILGARI (masalan eski sinovlardan) donaOst>0 bolgan bolsa-yu, registr (donalar) hali mavjud bolmagan bolsa — 'toza' nollashdan keyin ham ESKI donaOst SAQLANIB QOLARDI. Keyingi Shakllantirish bu eski sonning USTIGA qoshardi (donaRegQosh — ADD, REPLACE emas), natijada donaOst = eski+yangi, lekin donalar faqat yangi donalarni oz ichiga olardi — doimiy SLACK (donaOst-donalar.length>0) hosil bolib, bu ATAYLAB 'eski/registrsiz zaxira' deb tekshirilmasdan otkazib yuborilardi (dizayn qoidasi B). Foydalanuvchi 'toza nolladim' deb oylasa ham, aslida validatsiya HECH QACHON qattiq ishlay olmasdi. TUZATISH: grammNollash() endi tt.donaOst=0 va tt.donalar=[] ni ham nollaydi — endi haqiqiy 'toza boshlanish' kafolatlanadi, slack qolmaydi. Diagnostika uchun qoshilgan vaqtinchalik console.log lar olib tashlandi (xato topilgach kerak emas). Sinov: donaOst=3 (registrsiz) + ostatka=47.5 bolgan eski holatdan nollash -> donaOst=0,donalar=[] -> qayta shakllantirish 5 dona -> slack=0 -> 11g mos kelmaydigan berish -> ozConfirm modali TOGRI ochildi, aynan Ibrohim tasvirlagan haqiqiy stsenariy toliq tasdiqlandi.

## v86: CHIQIM MAYDONI QULFLANDI (1-variant, Ibrohim tanlovi). MUAMMO: Berish/Sotuv oynasidagi KATTA gramm maydoniga to'g'ridan-to'g'ri jami gramm (masalan 24) yozilsa — sistema dona sonini bilmaydi (1 ta 24g mi yoki 8 ta 3g mi?), shuning uchun registrga yozilmaydi va tekshiruv ISHLAMAYDI. Foydalanuvchi aynan shu katta maydonga yozayotgan edi, skan paneli esa chetda qolardi (skan qilганда ham 'ishlamaydi'gandek ko'rinardi, chunki keyingi render skan holatini o'chirsa faqat katta maydondagi son qolardi). YECHIM: kbg- (Berish) va ksg- (Sotuv) maydonlari endi READONLY — faqat SKAN PANELIDAN to'ladi (skan yoki qo'lda gramm yozib + bosish, har biri = 1 dona). Maydonni bosish avtomatik skan panelini ochadi (kbSkanToggle / uniSkanToggle). Shu bilan har chiqim DOIM dona bo'yicha aniq hisoblanadi va donaMosEmaslarniTop tekshiruvi ishonchli ishlaydi (endi katta maydonni chetlab o'tib bo'lmaydi). ISTISNO: har maydon yonida '✎' tugmasi — pul-asoslangan manfiy berish, lom, yoki tuzatish uchun maydonni qo'lda ochadi (chiqimUnlock), unda dona kuzatilmaydi (eski jim xulq, ataylab tanlangan override). Yangi funksiya: chiqimUnlock(fid,btn). Save mantiqi O'ZGARMADI — mismatch/donaRegOlish avvaldan skan massividan (pass1/uniSkanArr) o'qiydi, readonly bilan qiymat faqat shu manbadan keladi, ya'ni tekshiruv avtomatik kafolatlanadi. ksg- type='number'->'text' inputmode='decimal' (parseNum baribir o'qiydi).

## v87: ASOSIY XATO TOPILDI — OGOHLANTIRISH SLACK TUFAYLI JIM O'TARDI. donaMosEmaslarniTop ichida 'else if(donaSlack(t)<=0) yoq.push(g)' sharti bor edi: agar turda SLACK (donaOst > donalar.length, ya'ni eski registrsiz qoldiq) bo'lsa, mos kelmaydigan har qanday og'irlik JIM o'tkazib yuborilardi — ogohlantirish UMUMAN chiqmasdi. Ibrohim eski ma'lumot ustida ishlagani uchun (nollash to'liq qilinmagan yoki eski donaOst qoldig'i bor) slack doim >0 bo'lib, dona tekshiruvi hech qachon ishlamasdi — 11g kabi ro'yxatda YO'Q og'irlik ham bemalol o'tib ketardi. TUZATISH: donaMosEmaslarniTop endi QATTIQ — agar turda registr bor bo'lsa (donalar.length>0), har berilayotgan og'irlik ro'yxatda qidiriladi, topilmasa OGOHLANTIRADI (slack endi ogohlantirishni o'chirmaydi). Registr umuman yo'q bo'lsa (hech qachon shakllantirilmagan) — taqqoslab bo'lmaydi, jim o'tadi. Sinov: donaOst=8/donalar=5 (slack=3) holatda 11g -> ESKI jim o'tardi, YANGI to'g'ri ogohlantiradi; 3.55g (ro'yxatda bor) -> to'g'ri jim; toza tur (slack=0) va registrsiz tur -> ikkalasi ham to'g'ri. donaRegOlish (bookkeeping) va donaSlack o'zgarmadi.

## v88: TOLERANTLIK ANIQ MOSGA O'TKAZILDI (Ibrohim: 'tarozim aniq, 0.00001g ham farq bermaydi, taxminiy emas'). DONA_TOL 0.05g -> 0.001g. Avval ±0.05g 'tarozi tebranishi' tolerantligi bor edi, shuning uchun 3.15g kiritilsa registrida 3.13g bo'lsa (farq 0.02g) MOS deb qabul qilinardi va jim o'tardi — Ibrohimning aynan misoli (3.15 adashib) ushlanmasdi. Endi 0.001g (faqat float xatosi uchun mayda epsilon) — amalda ANIQ mos: yozilgan gramm registrida aynan bo'lsa (0.01g gridda) o'tadi, 0.01g yoki undan katta farq -> XATO. Sinov (BUTTERFLY 3D: 2.10,3.13,4.12,1.32): 3.15 va 3.14 endi ogohlantiradi, 3.13/2.10/4.12/1.32 aniq mos jim o'tadi, vergulli kiritish (2,10) ishlaydi, berilgach son kamayadi, tugagach yana so'ralsa xato. donaRegOlish/donaMosEmaslarniTop mantiqi o'zgarmadi — faqat DONA_TOL qiymati.

## v88.1: TOLERANTLIK 0.001 -> 0 (Ibrohim: '0.0001 ham kerakmas, menda unaqa farq bo'lmaydi'). Endi MUTLAQ aniq mos: vazn registrida aynan bo'lsagina o'tadi. Float xavfsizligi: barcha qiymat roundG (2 xona) orqali o'tgani uchun bir xil vazn har doim bit-bir xil bo'ladi — tol=0 da ham noto'g'ri rad etmaydi (0.1+0.2=0.30000004 tuzog'i ham roundG bilan 0.30 ga tenglashadi). Sinov: 4 aniq vazn mos, 3.14/3.15 xato, string/vergul/nol-siz variantlar mos, klassik float tuzog'i mos — 11/11.

## v89: QULFLASH (v86) OLIB TASHLANDI + QO'LDA YOZISH ENDI TO'G'RIDAN TEKSHIRILADI. MUAMMO: v86 da kbg-/ksg- maydonlari readonly qilingandi (faqat skan panelidan to'ladi), lekin telefonda panel noqulay -> foydalanuvchi ✎ bilan ochib to'g'ridan yozardi, u esa ATAYLAB tekshiruvsiz o'tardi -> 'gramm yozaman lekin ogohlantirish chiqmaydi'. Bundan tashqari save-time tekshiruv FAQAT skan paneli (pass1/uniSkanArr) to'lgandagina ishlardi — panel ishlatilmasa tekshiruv umuman o'tkazib yuborilardi. YECHIM: (1) kbg- (Berish) va ksg- (Sotuv) maydonlari yana ERKIN (readonly, onclick-panel, ✎ tugma olib tashlandi) — avvalgidek to'g'ridan yozasiz. (2) saqlashKlientBerish va saqlashKlientSotuv mismatch tekshiruvi endi FALLBACK bilan: skan paneli ishlatilgan bo'lsa aniq donalar ro'yxati (pass1/uniSkanArr) bilan, AKS HOLDA yozilgan qiymat [roundG(g)] BITTA dona deb registrga solishtiriladi. Ya'ni panel shart emas — qo'lda yozganda ham donaMosEmaslarniTop ishlaydi. Manfiy (g<=0, biz qarzdor) tekshirilmaydi. Registrsiz tur (donalar bo'sh) — asos yo'q, jim. Ko'p dona bir turda: panel bilan (pass1) aniq; qo'lda yozilsa jami [g] bitta dona deb qaraladi (odatda 1 dona/tur berilgani uchun to'g'ri; ko'p dona kerak bo'lsa panel). chiqimUnlock endi ishlatilmaydi (funksiya qoldi, zarari yo'q). Sinov: 11/3.15 qo'lda -> ogohlantiradi, 3.13/2.10 qo'lda -> mos, panel [3.13,2.10] -> mos, bo'sh registr -> jim, manfiy -> tashqarida = 9/9. MUHIM: tur AVVAL Ostatka->Shakllantirish orqali skan qilib shakllantirilgan bo'lishi kerak (donalar to'lishi uchun) — aks holda taqqoslash uchun asos bo'lmaydi.

## v90: DONA BAZASI (PROBNIY, Variant 1) — Ibrohim: 'alohida baza qilaylik, shakllantirganda hamma grammlarni sana bo'yicha saqlab, kirib tekshirib ko'rsa bo'lsin. Variant 1, indexda ERPga qo'yib, zavodlar ichida turga qo'shib probniy'. MAQSAD: dona registrini asosiy ma'lumot/cloud sinxronidan MUSTAQIL alohida localStorage kalitiga (tilla-dona-baza) yozish — eski nusxa sinxronda uni o'chira olmaydi (hozirgi 'esida qolmayapti' muammoning ildizi shu edi). QILINGANI (3 nuqta): (1) Yangi funksiyalar donaBazaOl/Saqla/Qosh/Tur/Render — flat array, har yozuv {id, sana, zavod, tur, gramm, holat:'ombor'}, append-only. (2) ostFormSaqla shakllantirish (shakl) shoxobchasida donaBazaQosh(c.z.nom, c.t.nom, p1, sana) — har shakllantirishda skanlangan aniq grammlar SANA bilan bazaga qo'shiladi (asosiy donaRegQosh registriga PARALLEL, unga tegmaydi). (3) renderZavod tur detali (BIZDA/KLIENTDA/JAMI stat2 kartadan keyin) donaBazaRender(z.nom, t.nom) — o'sha zavod-turning bazadagi donalari SANA bo'yicha guruhlab ko'rsatiladi (har kun: nechta dona, jami gramm; har dona: gramm + ombor/sotilgan). PROBNIY QAMROVI: hozircha faqat SHAKLLANTIRISH yozadi va zavod->tur ichida KO'RSATADI (Ibrohim 'faqat shu joyini ko'ri' dedi). Berish/sotuv bilan bog'lash (holat->sotilgan) va global qidiruv keyingi bosqichda, bu ko'rinish tasdiqlangach. Asosiy ilovaning hech bir mantiqiga (donalar registri, berish, cloud) TEGILMADI — bu qo'shimcha mustaqil qatlam. Sinov: 4 dona sana bilan yozildi, grammlar/sana/holat to'g'ri, boshqa tur alohida, faqat bitta localStorage kaliti (mustaqil), qayta shakllantirishda append — 8/8.

## v91: DONA BAZASI kengaytirildi (Ibrohim rasm + talab). (1) OCHILADIGAN BLOK — donaBazaRender endi tur ichida sarlavha ko'rsatadi ('DONA BAZASI · N dona · Xg' + chevron), bosilsa ochiladi/yopiladi (_donaBazaOpen[zavod||tur] + donaBazaToggle). Ochilganda: SANA bo'yicha guruh (har kun: nechta dona, jami gramm; har dona: gramm + ombor/berilgan), pastda UMUMIY (ombor) qatori — nechta dona, jami necha gramm. (2) BERISH ENDI BAZADAN TEKSHIRADI — saqlashKlientBerish mismatch manbai donaMosEmaslarniTop(t.donalar) dan donaBazaMosEmas(z.nom,t.nom,arr) ga o'zgardi: klientga berayotganda shu zavod-turning bazadagi OMBOR donalaridan bor-yo'qligiga qaraydi, yo'q bo'lsa ogohlantiradi (aniq mos, DONA_TOL=0). (3) BERISH SAQLANGACH BAZA KAMAYADI — davomEt ichida donaBazaOlish(z.nom,t.nom,_bArr) mos donalarni 'berilgan' deb belgilaydi (ombordan chiqadi, keyingi berishda hisobga olinmaydi). Skan paneli ishlatilsa aniq pass1, aks holda yozilgan qiymat bitta dona. (4) Shakllantirish -> baza yozishi (v90) o'zgarmadi. Asosiy donalar registri (t.donalar) va ostatka mantiqi TEGILMADI — baza mustaqil manba, endi berish tekshiruvi ham shundan. Sinov: 11/3.15 yoq->ogohlantiradi, 3.13 bor, berilgach 3.13 ombordan chiqadi va keyin ogohlantiradi, 2.10 hali bor, umumiy 3 dona/7.54g — 8/8.

## v92: DONA BAZA CLOUD SINXRON (append-only MERGE) — Ibrohim: 'ikki qurilma boshqa-boshqa zavodni ostatka olsa sistema/cloud xato bermasligi kerak, 1 qurilma 1 tur cheklovi bomasin'. MUAMMO: asosiy ma'lumot BUTUN holda yoziladi — 2-qurilma o'z zavodini saqlaganda butun ma'lumotni (eski boshqa-zavod bilan) bosib yozadi, 1-qurilmaning yangi sanog'i o'chadi (boshqa zavod bo'lsa ham). YECHIM: dona baza endi HAR DONA = ALOHIDA Firestore hujjati sifatida sinxronlanadi — collection(cloudKol()).doc('_donabaza').collection('items'), id bo'yicha. (1) donaBazaCloudRef/Yoz — donaBazaQosh har yangi donani cloudga .set (id bo'yicha) yozadi; donaBazaOlish 'berilgan' holatini cloudga yozadi; offlaynda Firestore navbatga oladi. (2) donaBazaCloudListen — onSnapshot barcha hujjatlarni local bilan id bo'yicha MERGE qiladi (yo'q bo'lsa qo'shadi, holat/gramm o'zgarsa yangilaydi; local-only pending donalarni O'CHIRMAYDI). (3) cloudInit auth: u bor bo'lsa donaBazaCloudListen(), signout: donaBazaCloudUnsub(). ISOLYATSIYA: alohida '_donabaza' hujjati ostida — asosiy sinxron (holat chunk'lari, zavod_amallar) ga UMUMAN tegmaydi, Firestore subkolleksiya parent doc overwrite'idan mustaqil. NATIJA: 2 qurilma boshqa zavodni bir vaqtda sanaydi -> ikkalasi ham O'Z donalarini qo'shadi, merge bo'ladi, bir-birini o'chirmaydi (append bosib yozmaydi). Sinov (mock Firestore, 2 qurilma): A DIAMOND/3D 3 dona + B BUTTERFLY/Oddiy 2 dona -> ikkalasida ham 5 dona (hech biri o'chirmadi), A da berilgan belgilansa B ham ko'radi, boshqa donalar ombor qoladi — 8/8. Asosiy ma'lumot sinxroni O'ZGARMADI.

## v93: AMAL-LOG SINXRON — CHEKSIZ QURILMA, OTVORISHSIZ (Ibrohim: 'hammasini shakllantirib cloud otmaydigan qilib qurilmalar soni cheksiz bolsa ham ishlaydigan qilib ber'). PRINTSIP: har qurilma cloudga faqat OZI QILGAN yangi ishni yozadi, butun malumotni BOSIB YOZMAYDI. Ikki qism: (1) YOZUVLAR OPLOGI — collection(cloudKol()).doc('_amallar').collection('items'): save() ichidan amalSyncPush() barcha tarix massivlarini (zavod-tur tarix, klient tarix, lomlar, kassa) kezib, YANGI yozuvlarni (_id synced-setda yoq) har birini ALOHIDA hujjat qilib yozadi ({loc, rec:JSON, qurilma, vaqt}); amalListen() boshqa qurilmalar yozuvlarini id boyicha joyiga qoshadi (zavod/tur/klient nom boyicha topiladi, yoq bolsa yaratiladi) — qoshish bosib yozmaydi, dublikat yoq. (2) OSTATKA HISOBLAGICHLARI — doc('_hisob') maydonlari 'zavod||tur' (gramm) va 'zavod||tur||d' (dona): amalSyncPush lokal ostatka ozgarishini DELTA qilib FieldValue.increment() bilan yuboradi — N qurilma deltalari QOSHILADI (masalan 3 qurilma bir turdan bir vaqtda sotsa: -3.13-2.10-4.12 hammasi hisobda); hisobListen() cloud qiymatini lokal t.ostatka/donaOst ga oqizadi va baselineni tenglashtiradi. BIR MARTALIK INIT (amalInit): mavjud tarix umumiy baza deb belgilanadi (_id hash bilan, PUSH QILINMAYDI — dublikat va ming-hujjat-yuklash oldini oladi), hisob snap baseline yoziladi. OTVORISH OCHIRILDI: cloudListen endi remote-newer holatda dialog OCHMAYDI va yuklab OLMAYDI — blob faqat YANGI/BOSH qurilmani birinchi toldirish uchun (bootstrap), yuklagach amal-init flaglari tozalanadi (tarix qayta pushlanmasin). cloudTanlovOch endi chaqirilmaydi (tarif qoldi). _cloudRemoteNewer hech qachon true bolmaydi. Butun-blob yozish (cloudSaqla) ZAXIRA sifatida qoladi. JS bir-oqimli: mutatsiya+save() sinxron, Firestore latency-compensation oz pending incrementlarini snapshotda korsatadi — revert xavfi yoq. CHEGARA (halol): klient balanslari tarixdan hisoblanadi (yozuvlar oplogda — avtomatik togri); agar 2 qurilma AYNAN bir xil oxirgi fizik donani sotsa, tizim ikkalasini ham yozadi va ostatka haqiqatni korsatadi (bu fizikada bolmaydi — bitta dona ikki qolda bolmaydi). Sinov (mock Firestore, 3 qurilma): bir turdan bir vaqtda 3 sotuv -> ostatka hammada 10.65 va 3 yozuv hammada; bir vaqtda 2 zavodda shakllantirish -> ikkalasi hammada; sotuv+shakllantirish bir turda bir vaqtda -> ikkalasi hisobda — 7/7.

## v94: OSTATKA SKAN PANELI TARTIBI ALMASHTIRILDI (Ibrohim: skan royxati solishtirish tagida qolib oxirgi urgan gramm korinmasdi). ost-f-rows (#Gramm skan royxati) endi ost-recon (Solishtirish 1-skan<->2-skan) dan YUQORIDA — kartalardan darhol keyin. Skan royxatida eng oxirgi urgan gramm allaqachon TEPADA va gold fonda (ostSkRender: i=a.length-1 dan pastga, oxirgisi gold-bg) — endi u ekranning yuqorisida, tez skanda darhol korinadi. Solishtirish (uzun royxat) pastga tushdi, ma_lumot sifatida qoladi. FAQAT HTML DOM tartibi ozgardi (ost-recon ost-f-rows dan keyinga kochdi, margin-top 8->10); render mantigi (ostSkRender), skReconcile, saqlash TEGILMADI.

## v95: (1) A-VARIANT — jonli skanda zavod/tur almashtirilganda skan buferi bosh bolmasa SORALADI (Ibrohim: adashib boshqa zavodga skan qildim, almashtirsam grammlar 0 boladi). ost-zavod/ost-tur onchange endi ostZavodChangeUser/ostTurChangeUser — ostBufBor() (pass1+pass2>0) bolsa modal-ost-switch ochiladi: "Kochirish" (skan saqlanadi, faqat manzil ozgaradi -> ostTurChange(skipReset=true) buferni saqlaydi, ostSkRender bilan yangi kontekstga qayta hisoblaydi) yoki "Tozalash" (ostSkReset, eski xulq). Bufer bosh bolsa soramaydi. ostTurChange(skipReset) va ostZavodChange(skipReset) parametr qabul qiladi; ichki chaqiruvlar (initOstatka, saqlashdan keyin) parametrsiz -> reset (eski xulq saqlandi). (2) HISOBOT TAHRIRLASH/KOCHIRISH — ost-choice ga "Hisobot/Tahrirlash" tugmasi; modal-ost-hisobot barcha boshlangich yozuvlarni royxat qiladi (sana, zavod·tur, dona/gramm), bosilsa modal-ost-recedit: ZAVOD va TUR selectlari + dona/gramm (ozgarmaydi, butun partiya kochadi) + Saqlash/Bekor/Ochirish. ostRecSaqla boshqa zavod/tur tanlansa BUTUN partiyani kochiradi: eski turdan ostatka-=g, donaOst-=d, donalar dan olib tashlaydi, tarixdan op ni oladi; yangi turga hammasini qoshadi; dona bazasidagi mos ombor donalar zavod/turi yangilanadi (ostRecDonaBazaMove, cloudga ham). ostRecOchir butun partiyani ochiradi (ostatka/dona/donalar/tarix dan olib, dona bazada holat=ochirilgan). save() -> v93 hisob-increment orqali ikkala tur ostatkasi hamma qurilmada yangilanadi; dona baza per-yozuv cloud orqali kochadi. Sinov: Diamond·Oddiy 3 dona (9.35g) -> Butterfly·3D kochirish: eski 0/0/bosh, yangi 9.35/3/[2.10,3.13,4.12], tarix va dona baza (3 ombor) togri kochdi — 10/10. CHEKLOV (halol): boshqa qurilmada TARIX QATORINING JOYI eski zavodda qolishi mumkin (oplog mutatsiyani cheklangan tarqatadi), lekin OSTATKA TOTALLARI (increment) va DONA BAZA (per-yozuv) hamma qurilmada togri kochadi; yangi qurilma blob bootstrap orqali toliq togri holatni oladi.

## v96: KOCHIRISH/OCHIRISH ENDI HAMMA QURILMAGA TARQALADI (Ibrohim: men ozgartirdim, qolgan qurilmalarniki ham ozgarishi kerak). Avval (v93/v95) oplog faqat QOSHISHNI tarqatardi — kochirish/ochirish boshqa qurilmada tarix qatorining joyini ozgartirmasdi (raqamlar togri edi, faqat qator eski zavodda qolardi). YECHIM: (1) synced-tracking Set(id) -> OBYEKT (id->versiya/vaqt); eski massiv format avtomatik obyektga migratsiya. (2) amalListen endi VERSIYA solishtiradi: doc.vaqt known versiyadan katta bolsa qayta ishlanadi (avval faqat bor/yoq edi). (3) Yangi yordamchilar: amalRecAdd (yozuvni joyiga qoshadi, OSTATKAGA TEGMAYDI), amalRecRemoveById (yozuvni _id boyicha qayerda bolsa ham olib tashlaydi, ostatkaga tegmaydi). (4) amalMovePush(op,newLoc) — cloud hujjatini yangi loc + yangi vaqt + moved:true bilan yangilaydi; amalDeletePush(op) — deleted:true + yangi vaqt. (5) amalListen: doc.deleted bolsa amalRecRemoveById; loc ozgargan (known bor, vaqt yangi) bolsa eski joydan olib yangi joyga qoyadi (KOCHIRISH); yangi (known yoq) bolsa qoshadi. OSTATKA/DONA hamon hisob-increment orqali keladi (ikki marta hisoblanmaydi — amalRec* faqat tarix QATORINI kochiradi/ochiradi). (6) ostRecSaqla -> amalMovePush, ostRecOchir -> amalDeletePush. NATIJA: bir qurilmada kochirilsa/ochirilsa, boshqa qurilma ham tarix qatorini kochiradi/ochiradi — endi HAMMA JOYDA bir xil. Sinov (2 qurilma mock): A shakllantirdi->B kordi; A kochirdi Diamond->Butterfly -> B da ham kochdi; A ochirdi -> B da ham ochdi — 8/8. Faqat boshlangich yozuvlar (ostRec* orqali) kochirish/ochirish e_lon qiladi; oddiy sotuv/berish avvalgidek faqat qoshiladi.

## v97: XATOLAR TUZATILDI (Ibrohim ekranida: amalWalk kassa.forEach + Firebase ruxsat). (1) YIQILISH: data.kassa OBYEKT (zlar/tuzatishlar/zakazlar...), massiv EMAS — amalWalk (data.kassa||[]).forEach da yiqilardi, bu amalInit->amalListen->shakllantirish save() ni buzardi. TUZATISH: amalWalk endi Array.isArray bilan himoyalangan (A() yordamchi); kassa OPLOGDAN CHIQARILDI (obyekt bolgani uchun — u blob orqali sinxron boladi). amalRecAdd/amalRecRemoveById dan ham kassa branchi olib tashlandi/himoyalandi, lomlar Array.isArray bilan. (2) UNCAUGHT PROMISE: ruxsat rad etilganda Firestore .set() reject bolib uncaught-promise sifatida spam qilardi (try/catch async rejectni tutmaydi). Har yangi cloud .set() ga .catch(cloudXato) qoshildi (donaBazaCloudYoz, amalSyncPush op+hisob, amalMovePush, amalDeletePush, hisobListen seed) — endi ruxsat yoq bolsa JIM otadi, ilova lokal ishlayveradi. MUHIM: cloud sinxron (dona baza, amal-log, hisob) ISHLASHI uchun Firestore QOIDALARIGA yangi yollarga ruxsat kerak (_donabaza/_amallar ichki kolleksiyalari) — Ibrohimga alohida beriladi. Ushbu tuzatishdan keyin ilova LOKAL toliq ishlaydi (shakllantirish, dona baza, berish tekshiruvi), cloud-sinxron esa qoidalar yangilangach yoqiladi.

## v98: OSTATKANI HISOBOTDAN QAYTA TIKLASH tugmasi (Ibrohim: sinxrondan keyin BIZDA 0 korsatvotti lekin hisobotda kirim bor; hisobotdan ochirsam minusga tushvotti). SABAB: v93 sinxron tarix yozuvini (oplog) va ostatka raqamini (hisob-increment) IKKI ALOHIDA yoldan olib keldi; ruxsat bloklangani uchun yozuv keldi (Hisobotda korinadi) lekin raqam kelmadi (BIZDA 0 qoldi); Hisobotdan ochirilganda 0 dan ayirilib minusga tushardi. YECHIM (opt-in, xavfsiz): Sozlamalarga tugma — ostatkaQaytaTiklaOch. ostatkaHisobla(t) har turning ostatka(gramm) va donaOst ni tarixdan qayta hisoblaydi, formula ilovaning OZ teskari-mantigidan (o chirish 6339-6341): mol +gramm/+dona, vozvrat -gramm/+dona, chiqim/sotuv -jami/-dona. Tugma: oldin qancha tur ozgarishini korsatib tasdiq soraydi, avtomat backupExport oladi, keyin qayta hisoblab save() qiladi. Hech narsani AVTOMAT ozgartirmaydi — faqat foydalanuvchi bosganda. TEST rejimida bemalol sinaladi. Sinov: BIZDA 0 + Hisobotda 180.95 -> 180.95 tiklandi; -212.03 minus -> +212.03; aralash kirim/sotuv/chiqim/vozvrat togri; bosh tur 0 — 6/6.

## v99: HAMMANI CLOUD BILAN TO LDIRISH + OSTATKA TARIXDAN (Ibrohim: nechta qurilma ulangan bo lsa bir-birini to ldirsin, dona baza+tarix+ostatka; cloud tugmasiga qo shib, avtomat+majburan). ILDIZ TUZATISH: ostatka INCREMENT sinxroni O CHIRILDI (u chalkashlik/minus/0 sababi edi) — amalSyncPush hisob bloki va hisobListen o chirildi. Endi ostatka har qurilmada TARIXDAN hisoblanadi (ostatkaHisobla): tarix oplog orqali sinxronlanadi -> ostatka o z-o zidan hamma joyda bir xil, alohida raqam-sinxron shart emas, chalkashmaydi. amalListen: masofadan tarix kelganda hamma tur ostatkasi tarixdan qayta hisoblanadi. YANGI: syncFullFill() — dona bazani (hammasi, id bo yicha idempotent) + tarixni (MAJBURAN, synced-setga qaramay — ruxsat bloklangan paytda chiqmay qolganlarni ham) cloudga yuboradi, ostatkani tarixdan qayta hisoblaydi, blob zaxira ham yangilanadi. cloudToldir() — Cloud holati oynasidagi 🔄 Hammani cloud bilan to ldirish tugmasi (UI feedback + natija alert). Ikki-tomonlama: har qurilma o zinikini yuboradi, listener cloud dagini oladi -> kimda nima yetishmasa to ladi, hech narsa o chmaydi (append, id bo yicha). Sinov (2 qurilma mock): A da Simay, B da Dorika -> A to ldirdi -> B da Simay+ostatka to g ri keldi; B to ldirdi -> A da Dorika keldi; ikkalasida HAMMA zavod, ostatka tarixdan to g ri, hech narsa o chmadi — 12/12. Cloud tugmasi=majburan; ulanishda avtomat yangi yozuvlar baribir push bo ladi. Asosiy mantiq (sotuv/berish/foyda) tegilmadi.

## v99.1: AVTOMAT TO LDIRISH ulanishga qo shildi. Muammo: v99 da avtomat sinxron faqat YANGI yozuvlarni tez tarqatardi, eski malumot faqat qo lda tugma bosilganda otardi (srazu o zgarmasdi). YECHIM: auth ulanganda (u bor) 3.5 soniyadan keyin syncFullFill() AVTOMAT chaqiriladi — listenerlar ulangach o zinikini majburan cloudga yuboradi + ostatkani tarixdan qayta hisoblaydi. Endi qurilma ulangan zahoti O ZI to ladi (qo lda tugma faqat zaxira/majburlash uchun qoladi). Ikkala nusxa (2 auth handler) yangilandi.

## v100: (1) FOIZ KALITI SILJISHI TUZATILDI (Ibrohim: zavod ochsa keyingisining foizi osha zavodga otib qolyapti). SABAB: narx/foiz localStorage kalitlari tilla-foiz-<zi> zavod INDEKSIga boglangan (nomga emas), 30+ joyda ishlatiladi. Zavod ochsa massiv siljiydi, kalitlar joyida qolib keyingi zavod ochgan zavodning foizini olardi. YECHIM (xavfsiz, 30+ narx joyiga TEGILMADI, faqat 2 amal): narxKalitOchir(delIdx,n) zavod ochirilganda kalitlarni tekislaydi (keyingilarini bittaga suradi), narxKalitAlmash(i,j) ikki indeks kalitlarini almashtiradi. ochirZavod splice dan OLDIN narxKalitOchir chaqiradi, har zavodning foizi OZ joyida qoladi. (2) ZAVODNI TEPAGA CHIQARISH: zavod detali sarlavhasiga Tepaga tugmasi, zavodTepaga() zavodni 0-oringa kochiradi (splice+unshift) va foiz kalitlarini birga suradi (narxKalitAlmash ketma-ket), tepaga chiqqach ham har zavod OZ foizi bilan qoladi. Kurs->Turlar narxi ekrani data.zavodlar tartibida. Sinov: 3 zavod 0 ochirildi qolgan 2si oz foizini saqladi; Simay(2) tepaga oz 12.3% bilan 0-oringa 6/6. Asosiy narx-hisob (30+ joy) TEGILMADI.

## v101: QAT'IY NARX ZAVOD FOYDASI TUZATILDI (Simay). Ildiz: tizim getZavodNarx (kirim/tannarx) va getKatNarx (optom/sotuv) da MANUAL (qo'lda) narxni allaqachon qo'llaydi - agar tur uchun qat'iy narx yozilsa foiz o'rniga o'sha ishlatiladi va sotuvda kirimNarx o'shandan muhrlanadi. LEKIN suzuvchi (floating) foyda hisobida (kassaFifoModel 3603 va kassaSuzuvchiXaritasi 6942) kirimNarxHozir faqat kurs×foizdan hisoblanardi - qat'iy zavodda foiz(pct)=0 bo'lgani uchun kirimNarxHozir=kurs(74.2) bo'lib, manual dogovor(84) o'rniga kurs olinardi -> Simay suzuvchi foydasi noto'g'ri (36.91 kabi shishgan). TUZATISH (kichik, xavfsiz): ikkala joyda kirimNarxHozir endi avval getZavodNarx(zi,ti) ni (manual-aware) tekshiradi - qat'iy narx bor bo'lsa o'shani (84) ishlatadi, aks holda eski kurs×foiz formulasi (foiz zavodlar O'ZGARMAYDI). Natija: Simay uchun sotuv 85$, qat'iy kirim(dogovor) 84$ -> suzuvchi foyda=(85-84)×19.75=19.75$ TO'G'RI; dogovorni qo'lda 83.5 ga o'zgartirsa foyda 29.63 ga suzadi; 85 qilsa 0 ga - aynan Ibrohim aytgan model (foyda dogovor bilan suzadi, zavodga to'langanda muhrlangan kirimNarxda qotadi). Kirim/chiqim/ostatka/sotuv-saqlashga TEGILMADI - faqat suzuvchi foyda hisobi manual-aware bo'ldi. FOYDALANISH: Simay turiga foiz emas, QAT'IY narx yozing (kirim 84, optom 85) - narx ekranida qiymatni to'g'ridan-to'g'ri kiritsangiz manual bo'lib saqlanadi. Sinov: manual 84->kirimNarxHozir 84 (kurs emas), foyda 19.75/29.63/0 to'g'ri, foiz zavod eski xulq (74.2*1.12=83.1) - 6/6.

## v102: SOTUV DONA TEKSHIRUVI 2 BUG TUZATILDI (Ibrohim: ko'p zavodda grammda yo'q deb xato ogohlantiradi + ogohlantirish orqa fonda, saqlashni qabul qilmaydi, Esc dan keyin chek chiqaradi). BUG 1 (manba mos emas): sotuv mismatch donaMosEmaslarniTop(t.donalar) — ESKI registrdan tekshirardi, berish esa donaBazaMosEmas — dona bazadan. Foydalanuvchi dona bazani to'ldiradi, eski t.donalar ba'zi zavodlarda bo'sh/eskirgan (sinxron/ko'chirishdan keyin) -> o'sha zavodlar sotuvda 'yo'q' deb xato ogohlantirardi (1 zavod OK, ko'p zavodda ba'zilari xato). TUZATISH: sotuv mismatch endi donaBazaMosEmas(z.nom,t.nom,arr) — BERISH bilan bir xil manba (har zavod O'Z dona bazasidan), reg ham donaBazaOmbor dan; sotuv saqlashda donaBazaOlish(z.nom,t.nom,arr) qo'shildi — sotilgan dona bazadan ham 'berilgan' bo'ladi (avval faqat donaRegOlish/t.donalar). BUG 2 (ogohlantirish orqa fonda): modal-ozconfirm z-index 200 edi (boshqa modallar bilan bir xil) -> sotuv modali DOM'da keyinroq bo'lgani uchun ustiga chiqib ozConfirmni yopib qo'yardi (ko'rinmaydi, Esc chalkashligi). TUZATISH: modal-ozconfirm z-index 600 — endi hamma modal ustida, ko'rinadi; foydalanuvchi Bekor/Davom ni to'g'ri bosadi (chek faqat ozConfirmJavob(true) da _sotuvDavomEt orqali chiqadi). Sinov: har zavod o'z bazasidan (Simay 3.13 bor, Diamond 2.10 bor - oldin xato yo'q derdi, Butterfly 4.12 bor), Diamond 9.99 yo'q, Simay 2.10 yo'q (u Diamondniki) - 5/5.

## v103: BERISH CHEKI TUZATILDI (Ibrohim: Berildi -60.94 qatorining chek tugmasini bossam ostatkasini korsatvotti). SABAB: klientChekBasit faqat TOLOV/VOZVRAT cheki uchun yozilgan edi — ops_grouped faqat tolov_g/vozvrat_g ni to'ldiradi, body loop faqat shularni chop etadi. isBerish=true bo'lganda (Berildi qatori, bVal=hasBerish?1:0 to'g'ri kelardi) berish oplari uchun tolov_g/vozvrat_g=0 -> body BO'SH qolardi, chek faqat 'Ostatka' + 'QARZ TARKIBI' ko'rsatardi (foydalanuvchi 'ostatka' deb ko'rgan shu). TUZATISH: klientChekBasit boshiga isBerish bloki qo'shildi — o'sha kun BERILGAN mollar zavod-tur bo'yicha guruhlanib 'Klientga berildi' ro'yxati + 'JAMI berildi' chop etiladi (asl berish modal cheki formatida), so'ng mavjud Ostatka/Qarz tarkibi qoladi (ular berish chekida ham foydali). Tolov/vozvrat cheki O'ZGARMADI (isBerish=false bo'lsa blok o'tkazib yuboriladi). Sinov (rasmdagi -60.94 misoli, 6 zavod-tur): har biri to'g'ri qatorda, JAMI berildi -60.94g — mos.

## v104: OSTATKA "ZAVODGA QAYTDI" BUG TUZATILDI (Ibrohim: to'langan/berilgan tillani zavodga qaytarvordi). ILDIZ (Claude xatosi, v98/v99): klientga BERISH/SOTUV faqat KLIENT tarixiga yoziladi (k.tarix.push) va t.ostatka to'g'ridan kamayadi — ZAVOD tarixiga yozuv TUSHMAYDI. Lekin v98/v99 ostatkani FAQAT zavod tarixidan qayta hisoblardi (ostatkaHisobla) -> berilgan tillani ko'rmasdan ostatkani balandroq hisoblardi = go'yo berilgan tilla zavodga qaytdi. Va bu HAR sinxron/ulanishda AVTOMAT takrorlanardi (amalListen + syncFullFill v99.1) -> qayta-qayta buzardi. TUZATISH (3 qism): (1) ostatkaHisobla(t, zNom) endi KLIENT berish/sotuv/vozvratni HAM hisobga oladi — barcha klientlar tarixidan shu zNom+t.nom ga tegishlisi: berish -g/-dona (boshlangich bundan mustasno — zavoddan chiqmagan), vozvrat +g/+dona. (2) AVTOMAT qayta-hisoblash O'CHIRILDI ikki joyda (amalListen changed-block va syncFullFill 3-qadam) — running-total (har amal to'g'ri kamaytiradigan) TO'G'RI edi, endi buzilmaydi; masofadan kelgan tarix qatori amalRecAdd bilan qo'shiladi. (3) v98 tugma (Sozlamalar > Ostatkani qayta tiklash) endi ostatkaHisobla(t, z.nom) chaqiradi (2 joy: preview+apply) — bir marta bosib buzilgan ostatkalarni TO'G'RI (klient bilan) tiklaydi. Sinov: Diamond 100 kirim - 60 berish = 40g/2dona (qaytmaydi); ESKI klientsiz 100g (60 qaytardi); vozvrat +20 -> 60g/3dona; boshlangich berish ta'sir qilmaydi; boshqa zavod aralashmaydi — 7/7. FOYDALANISH: deploy -> Ctrl+Shift+R -> Sozlamalar > "Ostatkani qayta tiklash" BIR MARTA bosib buzilgan ostatkalarni to'g'rilash (avval backup avtomat olinadi).

## v105: ABDULHAMID ROLI SODDALASHTIRILDI (rol-hamid). Login o'zgarmadi (CREDS dagi mavjud hisob) — faqat rol 'admin'->'hamid'. applyRol endi 'hamid' rolida body.rol-hamid klassini qo'yadi (rol-zavod/rol-hamid ikkalasi ham tozalanadi, keyin mos biri qo'yiladi). CSS bilan yashiriladi (ma'lumot O'ZGARMAYDI, faqat ko'rinish): ZAVOD tarafda — Kassa (#kassa-card-pc, #kassa-card-mob, zavod-detali #ztab-kassa + #zavod-kassa-cont), LOM (#ztab-home-lom + #main-lom), Sherik (#ztab-sherik + #zavod-sherik-cont), Ostatka (ikki tugmaga .hamid-x klass); KLIENT tarafda — Kassa tab (#kt-kassa + #klient-kassa-list) yashirin, bu Kassa qoldiq + Joriy foyda + Kassa harakatlarini birga yopadi (uchovi shu tabda). Qolgani ishlaydi: berish/vozvrat/to'lov/sotuv, klient qarzi/tarix, skan kirim, kirim/chiqim/vozvrat, chek/PDF, kurs, hisobot. Admin (tilla) rolida hammasi avvalgidek ko'rinadi — CSS faqat rol-hamid da ta'sir qiladi.

## v106: ABDULHAMID KASSA KO'RINISHI TO'G'RILANDI (Ibrohim rasm: Abdulhamidga savdo/foyda hisoboti — JAMI KASSA/GRAMM/TO'LOVLAR/SKIDKA/FOYDA + grafik + sotuvlar ro'yxati — KO'RINSIN, faqat Kassa qoldiq/Joriy foyda/Kassa harakatlari yashirin). v105 da butun klient Kassa tab (#kt-kassa + #klient-kassa-list) yashirilgan edi — bu XATO edi, chunki rasmda ko'rsatilgan hisobot ham shu tabda. TUZATISH: (1) CSS dan #kt-kassa + #klient-kassa-list olib tashlandi — Kassa tab endi Abdulhamidga KO'RINADI. (2) renderKassa ichida rol tekshiruvi: _hamidRol=(getRol()==='hamid') bo'lsa faqat uch panel (kassaQoldiqPanelHTML=Kassa qoldiq, kassaFoydaPanelHTML=Joriy foyda, kassaLentaHTML=Kassa harakatlari) O'TKAZIB YUBORILADI; ularning ostidagi summary-row (JAMI KASSA/GRAMM/TO'LOVLAR/SKIDKA/FOYDA), grafik (Kun/Hafta/Oy/Yil + Sotuv/Foyda), va sotuvlar ro'yxati HAMMAGA (Abdulhamidga ham) ko'rinadi. Admin (tilla) da hammasi avvalgidek. Zavod tarafdagi yashirishlar (Kassa/LOM/Sherik/Ostatka — v105) o'zgarmadi.

## v107: ABDULHAMID FOYDANI QOTGAN (muhrlangan) KO'RSATADI, SUZUVCHI EMAS (Ibrohim: foydani suzuvchi qilish kerakmas, o'sha kuni sotilganda foydasini qotirib qo'yib ko'rsatish kerak). Har sotuv op'ida ikki qiymat bor: o.foyda = SOTUV LAHZASIDA qotgan (muhrlangan) foyda, o.foydaHozir = suzuvchi (kurs o'zgarishi bilan yangilanadigan). Admin (tilla) avvalgidek SUZUVCHI (foydaHozir) ko'radi + suzuvchi belgilari (chizib tashlangan qotgan + ▲/▼ strelka). Abdulhamid (rol-hamid): _hamidF=true bo'lsa hamma joyda o.foyda (QOTGAN) ishlatiladi — jami FOYDA, sessiya foydasi (list + grafik), va per-op ko'rsatish; per-op da _szO=!_hamidF bilan suzuvchi belgilari (chizib tashlash + strelka) UMUMAN ko'rsatilmaydi — faqat toza qotgan raqam. Grafik Foyda liniyasi ham sessiya foydasidan kelgani uchun avtomat qotganga o'tadi. foydaAsl (session) o'zgarmadi. Sinov: op(foyda=20,suzuvchi=5,foydaHozir=25) -> admin 25$ + strelka, Abdulhamid 20$ toza, suzuvchi belgisi yo'q — 4/4.

## v108: 999 QOPLASH — ARZON OLISH KURSNI PASAYTIRADI, ALOHIDA FOYDA YOZILMAYDI (Ibrohim modeli, ko'p mockup muhokamasidan keyin tasdiqlangan). MANTIQ: arzon 999 olinganda hech qanday alohida "999 foydasi" qatori YOZILMAYDI (u soxta/ikki marta sanash bo'lardi). Buning o'rniga: xarid puli FIFO bilan ENG ESKI naqd sovdadan boshlab sovdalarga taqsimlanadi; o'sha sovdalarning kirim kursi = olish narxi ÷ 1.7 bo'lib QOTADI -> suzuvchi foyda O'ZI ko'tariladi. Olingan GRAMM ahamiyatsiz (u zavodga chiqim bo'lib ketadi). QO'SHILDI: (1) kassa999Qoplash() — data.lomlar dan proba==='999' && tip==='kirim' xaridlarni ts bo'yicha oladi; tolov op'larni sessiya (ki|sana|soat) bo'yicha guruhlaydi, faqat NAQD qismi (op.naqtPul>0) havzaga kiradi (lom/karta bilan to'langan sovdalar — ALOQASI YO'Q); sessiyalar ENG ESKIDAN saraladi; har xarid puli FIFO bilan yuriladi (to'liq/qisman); sessiya ichida SKIDKA KABI gramm nisbatida sochiladi (har op ekv×ulush); bir op bir necha xariddan tegsa — o'lchovli o'rtacha kurs. Qaytaradi: op -> {ulush, qopKurs, qopPul}. (2) kassaSuzuvchiXaritasi ga ulandi: _qatiy=(getZavodNarx manual>0) bo'lsa 999 TA'SIR QILMAYDI (Simay chetda); aks holda kQop=qopKurs×(1+pct/100), _kh=ulush×kQop+(1-ulush)×kirimNarxHozir (qoplangan qism QOTADI, qolgani SUZADI), suzuvchi=ochiqEkv×(kirimNarx−_kh); xaritaga qopUlush/qopKurs/qopPul/qopUst/kirimKun/kirimQop qo'shildi. (3) renderKassa allOps ga shu maydonlar. (4) Sovda kengaytirilganda TEGIGA tushuntirish bloki: "Bu sovdaning $X puliga 999 olindi. Samarali kurs K — bugungi B dan F$ arzon. Sovdaning U% qismi shunda -> foyda +Y ko'tarildi." O'ZGARMADI: chiqim, zavod, qarz, dona baza, sotuv saqlash — hech biriga tegilmadi; hisob faqat KO'RSATISHDA (suzuvchi), saqlangan kirimNarx muhrlangan holicha. Sinov (Node): 13500$ -> Guli 10:49 to'liq, Rano to'liq, Shoazim LOM tegmadi, Oybek to'liq, kurs 125/1.7=73.53; Simay QAT'IY ortmadi, Butterfly foizli +93.86 ortdi; 11000$ -> Oybek QISMAN 61.7% (1231/1995); 3000$ -> Guli sessiyasi 52.9% ikkala turga ham sochildi, Rano tegmadi — 13/13.

## v109: KLIENT VOZVRATI = ZARAR (Ibrohim: vozvrat bu zarar, huddi foyda hisoblagandek zarar hisoblidi, kunlik kursdagi kirim bilan chiqimdagi farqdek hisoblab MINUS qilish kerak; oldingi vozvratlar ham minus bo'lib ko'rinsin). AVVAL: renderKassa faqat tip==='tolov' oplarni olardi -> vozvrat kassa foydasiga UMUMAN kirmasdi (mol qaytsa ham foyda o'shaligicha turardi — xato). QO'SHILDI: (1) kassaVozvratMargin(ki, zavodNom, turNom) — bugungi margin: kirim=getZavodNarx(zi,ti) (manual/qat'iy bo'lsa u, aks holda kurs×(1+foiz)), chiqim narxi=getKatNarx(zi,ti,ki) (A/B uchun a-manual yoki kurs×(1+a-foiz)); C kategoriyada getKatNarx BO'SH qaytargani uchun (C narxi qo'lda) — shu klientning o'sha zavod-turdagi ENG OXIRGI sotuv narxi (op.kurs) olinadi; narx yoki kirim aniqlanmasa null (hisoblanmaydi, xato raqam chiqmaydi). margin = narx − kirim. (2) renderKassa allOps ga vozvrat oplar qo'shildi: zarar = −gramm × margin, foyda=foydaHozir=zarar (suzuvchi 0). _kdVoz va lomOrtiqcha oplar chetda. MUHIM TANLOV: vozvrat gramm:0 va summa:0 bilan qo'shiladi — ya'ni JAMI KASSA va JAMI GRAMM ga TEGMAYDI (pul emas), faqat FOYDA ga minus tushadi; haqiqiy gramm vzGramm da ko'rsatish uchun saqlanadi. (3) Sessiya kaliti ki|sana|soat|V — vozvrat sotuv bilan qo'shilib ketmaydi, alohida qator. (4) Ko'rinish: qizil "VOZVRAT" belgisi, summa o'rniga faqat zarar, chek tugmasi yo'q, ochilganda tur bo'yicha jadval (Tur | Gramm | Margin | Zarar) + "chiqim − kirim" ko'rsatiladi + tushuntirish. (5) TO'LOVLAR/"ta sotuv" sanog'idan vozvrat chiqarildi (_sotuvSoni); FOYDA stat endi manfiy bo'lsa QIZIL (avval doim yashil va '+' hardcode edi). ESKI VOZVRATLAR avtomat hisoblanadi (margin bugungi kursdan olinadi, yozuvda narx saqlanmagan). Sinov (Node): A klient Butterfly-S narx 87.3 − kirim 85.8 = margin 1.5 -> 10g vozvrat −$15; Simay QAT'IY 85−84=1 (qo'lda margin); C klient narx=oxirgi sotuv 88.5 -> margin 2.7; notanish zavod/kurs yo'q -> hisoblanmaydi; foizli zavodda margin kurs bilan deyarli o'zgarmaydi (narx ham kirim ham birga pasayadi) — 11/11.

## v110: KASSA CHIQIMIDA LOM HAM (Ibrohim: chiqimda ham pul ham lom chiqib ketishi mumkin, shunda qolimizdagi pul va lom kamayadi). AVVAL: "± Qo'lda" chiqim faqat summa ($) ni olardi (data.kassa.qolda) — lom chiqarish YO'Q edi. QO'SHILDI: (1) modal-kassa-qolda ga lom bloki (#kq-lom-blok): proba select (583/999/750/585/375) + gramm (#kq-lomg) — CHIQIMDA ko'rinadi, KIRIMDA yashirin (kqTip da lb.style.display). (2) kassaQoldaSaqla qayta yozildi: pul VA/YOKI lom (bittasi bo'lsa yetarli); chiqimda yetarlilik tekshiruvi — naqd erkin puldan (kassaOqim−kassaMuzlatilgan) oshmasin, 999 o.toza dan, boshqa proba kassaEkv bilan o.lomEkv dan oshmasin; tasdiqlash matnida ikkala ta'sir ko'rsatiladi (naqd −$X, lom −Yg + 583 ekvivalenti). (3) Yozuv: pul -> data.kassa.qolda (avvalgidek), lom -> data.lomlar.push({tip:'chiqim', manba:'chiqim', proba, gramm, narx:0, summa:0}). MUHIM: summa:0 — chunki kassaOqim da `if(r.tip==='chiqim' && r.manba!=='zavod' && s>0){ o.naqd += s; }` (lom SOTISH pul kiritadi); bu esa sotish emas, CHIQIM — shuning uchun summa 0 bilan pul kirmaydi, faqat cho'ntak kamayadi. Lom sotish (manba!=='chiqim', summa>0) avvalgidek ishlaydi. (4) kassaHarakatlar lentasi: manba==='chiqim' uchun yangi yozuv "Qo'lda chiqim (lom) · proba · Xg → lom chiqdi" (avval "Lom sotildi → pul keldi" deb NOTO'G'RI ko'rinardi). ZAVOD/QARZ/FOYDA ga tegilmadi — chiqim sodda, siz aytganingizdek. Sinov (Node, kassaOqim mantiqi): boshlangich naqd $41372.9/lom 172.94/999 126 -> chiqim $3000+20g lom -> naqd $38372.9, lom 152.94, 999 126 (tegilmadi), lom chiqimi pul KIRITMADI; 999 10g chiqim -> 999 116, naqd o'zgarmadi; 750·10g -> ekv 12.86g to'g'ri ayrildi; lom SOTISH (manba!=chiqim, summa>0) hali ham +$350 kiritadi — 11/11.

## v111: VOZVRAT ZARARI TO'G'RILANDI — FAQAT OSTATKADAN ORTIQ QISMGA (Ibrohim: agar klient ostatkasini vozvrat qilsa zarar YOZILMAYDI — 10g qarzi bor 5g vozvrat qilsa hisoblanmaydi; 10g ostatkasi bor lekin 12g berib bizni 2g ga qarz qilsa — o'sha kungi kunlik kursdan hisoblab 2g ga zarar). MANTIQ: foyda TO'LOVda yoziladi (mol berilganda emas) -> klient to'lamagan molni qaytarsa foyda ham yozilmagan -> zarar YO'Q, faqat qarzi kamayadi. Ostatkadan ortiq qaytarsa — ortig'ini sotuv narxida qaytarib olgandek -> ZARAR. v109 XATO edi: HAMMA vozvratga zarar yozardi. JAVOBLAR: (1a) ostatka SHU zavod-tur bo'yicha; (2) margin VOZVRAT QILINGAN KUNDAGI kurs va klient KATEGORIYASI bo'yicha (foyda kabi, faqat minus); (3a) ostatka vozvrat PAYTIDAGI (tarix o'sha nuqtagacha); (4) ortiqcha 2g biz qarz bo'ladi — keyin klient mol olganda o'sha 2g qarzdan yechiladi va faqat to'langan grammdan foyda chiqadi (mavjud model, ikki marta sanash yo'q). QO'SHILDI: (1) kursSanada(sana,soat) — tilla-kurs-tarix ({sana,soat,kurs}) dan o'sha sana/soatga eng yaqin OLDINGI kursni topadi; topilmasa tilla-kurs-bugun. (2) narxlarKursda(zi,ti,kat,kurs) — berilgan kurs bo'yicha kirim (manual/qat'iy bo'lsa u — kursdan MUSTAQIL, aks holda kurs×(1+foiz)) va chiqim narxi (A/B: a-manual yoki kurs×(1+a-foiz), B ga tilla-b-ust qo'shiladi; C: 0 -> chaqiruvchi oxirgi sotuv narxini oladi). (3) klientOstatkaOldin(k,vop) — klientQarzSplit QOIDASI bilan bir xil: shu zavod|tur uchun berish +gramm, vozvrat −gramm, tolov −ekvivalent (_kdYopish chetda), FAQAT shu vozvratgacha (massiv tartibida, o===vop da to'xtaydi). (4) kassaVozvratMargin(ki, op) qayta yozildi — endi op oladi (zavod/tur/sana/soat/gramm), o'sha kungi kursni ishlatadi, C uchun vozvratgacha bo'lgan oxirgi sotuv narxini oladi, va {ortiq, ostOldin, kurs, margin} qaytaradi. (5) renderKassa: ortiq<=0 bo'lsa op UMUMAN qo'shilmaydi (zarar yo'q); zarar = −ortiq×margin. (6) Ko'rinish: sarlavhada "Xg qaytdi · ortiqcha Yg", jadval ustunlari Tur|Ortiqcha|Margin|Zarar, har qatorda "qaytdi Xg · ostatka Yg" va "kurs K" ko'rsatiladi, tushuntirish yangilandi. Sinov (Node): 10g ostatka+5g vozvrat -> ortiqcha 0, zarar YO'Q; 10g+12g -> ortiqcha 2g, 12.07 kursi 74.5 olindi (bugungi 75.3 EMAS), margin 1.5 -> zarar −$3.00; Diamond 10g qarzi bor Butterfly 5g qaytsa -> 5g ortiqcha (boshqa zavod qarzi hisobga olinmaydi, 1a); berish 10 − tolov 8 = ostatka 2, 5g qaytsa 3g ortiqcha; C kategoriya vozvratgacha oxirgi sotuv narxi 88.5; qat'iy narx margin 85−84=1 kursdan mustaqil — 8/8.

## v112: CHIQIM ORQA SANA KO'RINADIGAN + "ZAVODGA TO'LANMAGAN" KO'RSATKICHI (Ibrohim: kecha zavodga pul berdim (75.3 dan), lekin chiqim yozilmagan -> sotuvlar ochiq qolib bugun kurs oshgani uchun kechagi foydalar ▼ pasayib ketdi; rasmda kun jami ~$1,690.24 -> $1,484.82). ILDIZ: Sana maydoni MAVJUD edi, lekin "Kimga va sana" kartasining ICHIDA, ism ro'yxatining ostida ko'milib qolgan — foydalanuvchi topa olmagan. Hech narsa to'smasdi. QILINDI: (1) Sana maydoni YUQORIGA ko'chirildi — endi birinchi kartada ("Zavod va sana"), zavod tanlashning ostida, doim ko'rinadi (avval kartani ochish uchun zavod tanlash kerak edi). "Kimga" kartasi endi faqat ism. (2) cSanaChange() — sana bugungidan boshqa bo'lsa #c-sana-ogoh da qizil "⚠ ORQA SANA — dd.mm.yyyy (bugun emas)" + nima bo'lishi tushuntiriladi; initChiqim da ham chaqiriladi. (3) saqlashChiqim: orqa sana bo'lsa confirm — "o'sha kundagi sotuvlar yopiladi, kassadan pul o'sha kunda chiqadi, Z bilan yopilgan bo'lsa tafovutni tekshiring". MUHIM: confirm YOZUVLARDAN OLDIN qo'yildi (validatsiya tugagach, t.tarix.push loopidan oldin) — bekor qilinsa hech narsa o'zgarmaydi (agar keyin qo'yilsa, oplar allaqachon qo'shilgan bo'lib in-memory data buzilardi). (4) kassaZavodgaTolanmagan() — ochiq pozitsiya: har zavod-tur uchun sotilgan(tolov ekvivalent) − vozvrat − zavodga to'langan(t.tarix jami, mol/vozvrat chetda); kassaSuzuvchiXaritasi bilan AYNAN bir xil qoida. (5) Kassa qoldiq panelida yangi ko'rsatkich: "⏳ Zavodga to'lanmagan — foyda suzib turibdi · Xg" — bosilsa zavod-tur bo'yicha ro'yxat ochiladi (_tlmOch) + tushuntirish; jami 0 bo'lsa panel umuman chiqmaydi. Shunda to'lov yozilmay qolgani DARHOL ko'rinadi. Sinov (Node): 100g S + 40g Oddiy sotilgan, to'lovsiz -> 140g ochiq, eng kattasi birinchi; S ga 100g to'lov -> jami 40g, S ro'yxatdan chiqdi; 15g vozvrat -> 25g; hammasi to'langach 0 -> panel chiqmaydi; 'mol' kirim to'lov deb hisoblanmaydi -> 7/7.

## v113: KASSA CHIQIM MODALI (5-tugma) + TO'LOV BELGILARI (Ibrohim mockup bo'yicha, 1ma-1 tasdiqlangan). (1) TO'LOV BELGILARI: har sovda oldida kategoriya (A/B/C) yonida NAQT (yashil) / LOM (oltin) / KARTA (ko'k) belgilari — sessiya oplaridagi naqtPul/lomPul/kartaPul yig'indisidan; aralash bo'lsa bir nechtasi chiqadi (masalan NAQT+KARTA). Vozvrat qatorlarida ko'rsatilmaydi. (2) KASSA QOLDIQ PANELI 5 TUGMA: .kassa-btnlar grid repeat(4)->repeat(5); yangi "− Chiqim" qizil tugma (var(–red-bg)/var(–red)) "✓ Kunni yopish" dan OLDIN. Mobil (max-width:560px) da 2 ustunli grid o'zgarmadi. (3) YANGI MODAL #modal-kassa-chiqim: Sana (orqa sana bo'lsa qizil "⚠ ORQA SANA" ogohlantirishi); Kurs ($/g) — kursSanada(sana) dan AVTO qo'yiladi (sana o'zgarsa yangilanadi), lekin foydalanuvchi tegsa (_kcKursTegildi) avto to'xtaydi; Naqt pul $ / Lom 583 g / 999 g — har birining yorlig'ida "bor: X" (kassaOqim(sana) dan — O'SHA KUNGI qoldiq); Izoh. (4) kcHisob() jonli: "qoladi" uch cho'ntak (manfiy bo'lsa qizil), yetmasa ogohlantirish, va kurs taqqoslash bloki — kunlik kursdan ARZON bo'lsa yashil, QIMMAT bo'lsa qizil, farq $/g bilan. (5) kassaChiqimSaqla(): yetarlilik tekshiruvi O'SHA KUNGI qoldiqqa qarab (naqd/lom/999 alohida), tasdiqlash (orqa sana ko'rsatiladi), so'ng yozadi — naqt -> data.kassa.qolda {tip:'chiqim', kategoriya:'Chiqim', kcKurs}; lom/999 -> data.lomlar {tip:'chiqim', manba:'chiqim', summa:0, kcKurs}. summa:0 MUHIM — kassaOqim da `chiqim && manba!=='zavod' && summa>0` pul KIRITADI (lom sotish); bu esa chiqim, shuning uchun summa 0 bilan faqat cho'ntak kamayadi. kcKurs kelajakda foyda hisobi uchun saqlanadi. ESLATMA: foyda modeli (pul navbati — sovda naqdi eng eskidan, amal kursiga qarab foyda o'zgarishi) HALI QO'SHILMADI — u v108 (999 qoplash) bilan ikki marta sanashga olib keladi, almashtirish kerak; Ibrohimga aytildi. Sinov (Node): kursSanada 13.07->75.3 / 12.07->74.5 / 14.07->76.5; 13.07 ga chiqim (naqd 5000 + lom 20g + 999 10g) -> 13.07 holati naqd $45000 / lom 152.94 / 999 116, lom-999 chiqimi pul KIRITMADI; 12.07 holati (chiqimdan oldin) o'zgarmadi — naqd $50000 / lom 172.94; kurs farqi 75.3-74.0=1.30 ARZON; to'lov belgilari NAQT+KARTA / NAQT+LOM / LOM / KARTA / NAQT — 15/15.

## v113.1: CHIQIM MODALI FONI TUZATILDI (Ibrohim: chiqimni foni yo'q, background yo'q — modal shaffof chiqdi). SABAB (Claude xatosi): modal qutisiga class="modal-box" yozilgan edi — bunday klass CSS da UMUMAN YO'Q. Loyihada to'g'ri klass: .modal (fon, radius, padding, animatsiya) — .modal-overlay ichida. Shuning uchun quti fonsiz, formatsiz chiqdi (rasm: matnlar orqa ekran ustida suzib turibdi). TUZATISH: <div class="modal-box"> -> <div class="modal" style="max-width:440px;"> (qo'lda/olish modallari bilan bir xil); ustiga <div class="modal-handle"></div> qo'shildi (pastdan chiqadigan modal tutqichi, boshqa modallardagidek); modal-overlay ga onclick="if(event.target===this)closeModal('modal-kassa-chiqim')" — tashqarisiga bosilsa yopiladi (boshqa modallar kabi). Tekshirildi: 'modal-box' fayldan butunlay yo'qoldi (0 ta), chiqim modali blokida div balansi 15/15, sintaksis toza.

## v114: CLOUD LOGIN POYGASI (RACE) TUZATILDI (Ibrohim: cloudda shunaqa oshibka borki refresh qilsam chiqib ketvotti). SABAB: cloudLogin() da tasdiq signIn'ning .then() ICHIDA yozilardi: firebase.auth().signInWithEmailAndPassword(...).then(function(){ localStorage.setItem('tilla-cloud-tasdiq','1'); ... }). Lekin onAuthStateChanged auth holati o'zgarishi bilan DARHOL ishlaydi — .then() dan OLDIN. cloudInit dagi qat'iy qoida: TEST rejimda `if (u && localStorage.getItem('tilla-cloud-tasdiq')!=='1') { ... else { firebase.auth().signOut(); return; } }` — ya'ni tasdiq hali yozilmagani uchun signOut() ishlab, foydalanuvchini CHIQARIB yuborardi. (TEST rejimda localStorage o'ralgan: Storage.prototype patch bilan 'tilla-cloud-tasdiq' aslida 'TEST-tilla-cloud-tasdiq' bo'lib o'qiladi/yoziladi — shuning uchun haqiqiy rejimdagi tasdiq TEST ga o'tmaydi, muammo faqat TEST da ko'rinadi.) TUZATISH: tasdiq endi signInWithEmailAndPassword dan OLDIN yoziladi (onAuthStateChanged qachon ishlasa ham tayyor turadi); .catch() da esa localStorage.removeItem('tilla-cloud-tasdiq') — login muvaffaqiyatsiz bo'lsa tasdiq qolib ketmasin (aks holda keyingi meros sessiya TEST ga qonuniy deb kirib qolardi). onAuthStateChanged, cloudLogout, tilla-fb-signout (TEST<->haqiqiy almashish) mantiqiga TEGILMADI. ESLATMA: agar refresh'da chiqib ketish DAVOM etsa — sabab boshqa (masalan brauzer IndexedDB ni bloklashi yoki Firebase persistence), konsol xatosi kerak.

## v115: OFFSET = ZARAR (vozvrat kabi) + JAMI TO'LANDI = NAQT (Ibrohim: 185$ Naqt qilib ko'rsatib (425$ o'zi offset) deb ko'rsatsin; zarar offset vozvratga o'xshab, faqat biz C kategoriya qilib offsetda arzon olib qolamiz — zarari kamroq; offset zarar beradi DOIM, faqat kamroq chunki biz kam olamiz). AVVAL: _kdYopish (offset) oplar renderKassa da UMUMAN o'tkazib yuborilardi -> offset ko'rinmasdi va zarar bermasdi; sarlavhada/Jami to'landi da op.summa (425$) ko'rsatilardi — lekin naqd faqat 185$ kelgan. QO'SHILDI: (1) allOps ga OFFSET oplar qo'shildi (off:true): zi/ti topiladi, kirim=getZavodNarx(zi,ti) (BUGUNGI), narx=op.kurs (offset narxi — arzon, C kat), zarar = −ekvivalent×(narx−kirim); gramm:0 va summa:0 (JAMI GRAMM/KASSA ga tegmaydi), offGramm/offSumma ko'rsatish uchun. Vozvrat formulasi bilan bir xil, faqat narx sifatida offset narxi ishlatiladi -> arzon olsak zarar KAM (80 da −$4.5, 84.3 da −$17.4). "Ostatkadan ortiq" qoidasi YO'Q — offset doim zarar beradi (Ibrohim: "offset zarar beradi doim"). (2) Sessiyaga offSumma va naqtJami (naqtPul+kartaPul+lomPul) yig'iladi. (3) Sarlavhada endi $naqtJami ($185) ko'rsatiladi, ostida binafsha "($425.00 o'zi offset)"; OFFSET belgisi (binafsha) qo'shildi NAQT/LOM/KARTA yoniga. (4) Tur jadvalida binafsha "↔ Offset · zavod·tur · Xg · narx$ (kirim: Y)" qatori va qizil zarar. (5) "Jami to'landi (naqt)" = naqtJami; ostida "↔ Offset bilan yopildi $425". Sinov (Node, Ibrohim misoli): Simay 5g@85 (qat'iy kirim 84) -> +$5.00; 3D offset 3g@80 (bugungi kirim 78.5, margin 1.5) -> −$4.50; sarlavha $185.00 ($425.00 o'zi offset); sof foyda +$0.50; arzon olsak zarar kam (84.3->17.4, 80->4.5, 79->1.5) — 10/10. ANIQLANDI (kod yozilmadi): (a) v113 "− Chiqim" modali data.kassa.qolda + data.lomlar ga yozadi, ZAVOD tarixiga (t.tarix) YOZMAYDI -> sotuvni QULFLAMAYDI; qulflash faqat t.tarix dagi tolov op (jami gramm) orqali bo'ladi (kassaSuzuvchiXaritasi: tolanganG+=op.jami). Ya'ni pul-navbat foyda modeli hali qurilmagan. (b) kurs o'zgarganda faqat OCHIQ (ochiqEkv>0) sotuvlar suzadi; agar to'langan sotuv ham o'zgarayotgan bo'lsa — demak u aslida to'liq yopilmagan (tolanganG yetmagan).

## v116: PUL NAVBATI — v108 (999 qoplash) YAGONA MODELGA AYLANTIRILDI (Ibrohim: kassadan zavodga faqat PUL chiqarvorilik bo'ldi, nechi grammga qaysi turga to'langani Zavod ERPda hal qilinadi; sistema eng eski sovdadan pulni ajratvoladi, shunga kirgan klientlar kassasi QOTADI va 73.5 dan sovda qilgan qilib foydani ko'paytiradi; 126×3=$378 ni ALOHIDA YOZMASLIK — xato bo'lib qoladi; qolgan 34250$ Butterflyga chiqim, kurs yozamiz; kurs ko'tarilsa qotmagan foyda kamayadi, tushsa ko'payadi). O'ZGARISH: kassa999Qoplash -> kassaPulNavbati. Endi navbatga UCH XIL amal kiradi (kassaPulAmallar, ts bo'yicha saralangan): (1) 999 xaridi — data.lomlar kirim/999, kurs = narx÷1.7; (2) Kassa chiqimi (v113 modal) — data.kassa.qolda tip:'chiqim', kurs = kcKurs; (3) Zavodga chiqim — z.turlar[].tarix tip:'tolov', naqtSumma/naqtKurs; naqtKurs TUR narxi bo'lgani uchun asosiy kursga qaytariladi: naqtKurs ÷ (1+foiz) (_turFoiz). Navbat: sovda sessiyalari (ki|sana|soat), faqat NAQD qismi (naqtPul>0 — lom/karta kirmaydi), ENG ESKIDAN. Har amal pulni ketma-ket oladi (to'liq/qisman); sessiya ichida SKIDKA KABI gramm nisbatida sochiladi (ekv×ulush); bir op bir necha amaldan tegsa — o'lchovli o'rtacha kurs. kassaSuzuvchiXaritasi O'ZGARMADI (v108 dagi blend ishlaydi): qat'iy narxli turlar chetda (_qatiy), qoplangan qism kQop=qopKurs×(1+pct) da QOTADI, qolgani kunlik kursda SUZADI. ALOHIDA foyda qatori YO'Q — foyda kirim kursi o'zgarishi orqali o'zi chiqadi (ikki marta sanash yo'q). CHIQIM MODALI moslandi: kurs endi IKKI BOG'LANGAN BLOK — [999 narxi] = [583 kursi]; biriga yozsangiz ikkinchisi avto (kcKursSync: ÷1.7 va ×1.7); sana bo'yicha avto qo'yiladi (kcKursQoy, kursSanada dan), foydalanuvchi tegsa avto to'xtaydi; natija blokida "1:1 — foyda o'zgarmaydi" / "✓ Kurs tushdi — foyda ko'proq" / "⚠ Kurs ko'tarildi — foyda kamroq" + summa (pul × (kunlik÷kurs − 1)) ko'rsatiladi. Sinov (Node, Ibrohim misoli — $50,000 sovda, kunlik 128=75.294): 999 $15,750@125 (=73.529) -> Guli/Rano/Guli/Oybek to'liq, Abdulaziz 13:13 QISMAN 7.7% ($1,133), foyda = 15750×(75.294÷73.529−1) = $378.00 — AYNAN 126×3; zavodga $34,250 @ tur narx 80.6 -> asosiy 75.33 ≈ kunlik -> 1:1, foyda $0; @75.6 -> −$138.58 (kamayadi); @75.0 -> +$134.31 (ko'payadi); 128÷1.7=75.29, 75.294×1.7=128 — 11/11.

## v117: SOVDALARDA QULFLANISH KO'RINISHI (Ibrohim: sovdalar qulflansa oppoq bo'p turibdi, to'liq/qisman yo'q; mockupdagidek bo'lsin) + OFFSET SUMMASI TUZATILDI. (1) OFFSET XATO: sof offset sessiyalarida (Shahnoza Opa 22, Zuhra Opa 13 — 0.00g, $0) "($0 o'zi offset)" chiqardi, chunki kSumma allOps dagi o.summa yig'indisi, offset oplarda esa summa:0. TUZATISH: kSumma>0 bo'lsa u, aks holda kg.offSumma ko'rsatiladi -> endi "($27.26 o'zi offset)" kabi to'g'ri chiqadi. (2) QULFLANISH BELGISI: sessiya sarlavhasida NAQT/LOM/KARTA/OFFSET yoniga TO'LDI (yashil, ulush>=99.95%) yoki QISMAN (oltin, 0<ulush<99.95%) qo'shildi — ulush pul navbatidan (op.qopUlush, sessiya ichida bir xil). (3) LOADING BAR: sessiya ochilganda progress-bar — width=ulush%, to'liq bo'lsa yashil ("$X — to'liq qotdi"), qisman bo'lsa oltin ("$X / $Y · Z% qotdi"), tegmagan bo'lsa "qulflanmagan — foyda suzadi". Tur jadvalida kirim eski->yangi (strike + yashil) va foyda ▲ v108 dan beri bor. Mockup (qisman-loading-foyda.html) ko'rinishiga moslandi.

## v118: SARLAVHADA JAMI + TAGIDA NAQT·LOM·KARTA (Ibrohim: naqtni pulini ko'rsatsin, lomini tegiga yozib; jami summa yo'q chalkashiladi). v115 da sarlavha naqtJami ga o'zgartirilgan edi -> jami yo'qolib chalkashlik chiqdi. TUZATISH: sarlavhada yana JAMI (kSumma, ya'ni sovda summasi; sof offset sessiyalarida naqtJami) katta ko'rsatiladi; ostiga KICHKINA qator qo'shildi: "naqt $X · lom Yg · $Z · karta $W" (faqat 2+ to'lov turi bo'lsa chiqadi, rangli: naqt yashil, lom oltin, karta ko'k). "Jami to'landi" qatori ham yana JAMI ga qaytarildi (v115 da naqt qilingan edi) — ichkarida Naqt/Karta/Lom tafsilotlari allaqachon bor. Offset qatori ("↔ Offset bilan yopildi") o'zgarmadi.

## v118.1: VERSIYA IZOHLARI TUZATILDI. XATO: izoh matnida "var(–red-bg)" kabi ikki tire ("––") yozilgan edi. HTML izohi ichida ikki tire TAQIQLANGAN — brauzer izohni buzib, matnni sahifada ko'rsatib yubordi (Ibrohim rasm: izoh matnlari ekranda chiqib qolgan). TUZATISH: barcha 126 ta HTML izohi ichidagi ikki tire xavfsiz belgiga (–) almashtirildi. HAQIQIY KOD TEGILMADI: var(–red-bg) kabi CSS o'zgaruvchilari faqat izoh MATNIDA o'zgardi; haqiqiy CSS/JS da 37 ta var(–red-bg) va 264 ta var(–gold) joyida, :root o'zgaruvchilari butun, sintaksis toza. Kelajakda izohlarga ikki tire yozilmasin.

## v119: "± QO'LDA" VA "− CHIQIM" BITTAGA BIRLASHDI (Ibrohim: 1taga birlashtirvorilik, chiqim qilib nimadur olsak yoki obed nimadur qilsak yozadigan qilib). O'ZGARISH: (1) "± Qo'lda" tugmasi kassa panelidan OLIB TASHLANDI; tugmalar yana 4 ta (grid repeat(5)->repeat(4)): + Sotib olish · + Zakaz · − Chiqim · ✓ Kunni yopish. openKassaQolda/kassaQoldaSaqla funksiyalari va modali kodda QOLDI (eski yozuvlar buzilmasin), faqat tugma yo'q. (2) Chiqim modaliga "Nima uchun" (kategoriya) select qo'shildi: Zavodga to'lov (data-k=1), 999/lom olish (data-k=1), Obed, Ishxona rasxodi, Yo'l/benzin, Ish haqi, Arenda, Soliq, Shaxsiy, Boshqa. (3) kcKursli() — tanlangan optionda data-k=1 bo'lsa KURS bloki (999↔583) ko'rinadi va foyda ta'siri hisoblanadi (pul navbatiga kiradi); aks holda kurs bloki YASHIRINADI va o'rniga "Bu sof rasxod — kurs kerak emas, foydaga tegmaydi" izohi chiqadi. (4) Saqlashda kategoriya data.kassa.qolda.kategoriya va lomlar izohiga yoziladi; kurs faqat kursli kategoriyada (aks holda kcKurs=0 -> pul navbatiga KIRMAYDI, sof rasxod bo'lib qoladi); tasdiqlash matnida kategoriya ko'rsatiladi. NATIJA: bitta tugma, bitta modal — zavodga to'lov ham, obed ham shu yerda; kurs faqat kerak bo'lganda.

## v120: KARTA ALOHIDA CHO'NTAK (Ibrohim: kassada karta bo'lsa ko'rsatmayapti; 4 chontak, klientlarda ham naqt lom ko'rsatib kartani qo'shish kerak). AVVAL: kassaOqim da karta NAQDGA QO'SHILIB ketardi (`var pul = naqtPul + kartaPul; o.naqd += pul;`) -> kassa qoldiq panelida 3 cho'ntak (Naqd/Lom583/999), karta alohida ko'rinmasdi; klient karta bilan to'lasa pul qayerda ekani bilinmasdi. TUZATISH: (1) kassaOqim o obyektiga karta:0 qo'shildi; klient to'lovlarida naqtPul -> o.naqd, kartaPul -> o.karta (alohida); yakunda o.karta ham yaxlitlanadi. bugunKirim ikkalasini ham hisoblaydi (avvalgidek). (2) Kassa qoldiq paneli: karta bo'lsa 4 cho'ntak (Naqd · Karta · Lom 583 · 999), bo'lmasa avvalgidek 3 ta (grid dinamik: _kartaBor). Karta ko'k rangda. Naqd ostidagi erkin/band ko'rsatkichi o'zgarmadi. (3) Klient sovdalarida NAQT/LOM/KARTA belgilari (v113) va sarlavha ostidagi "naqt $X · lom Yg · karta $Z" qatori (v118) allaqachon bor. ESLATMA: karta pul navbatiga KIRMAYDI (999/zavodga naqd bilan to'lanadi) — navbatda faqat naqtPul. Chiqim modalida ham karta yo'q. Sinov (Node): naqt 813+1000=$1813, karta 1000+830=$1830, karta naqdga qo'shilmadi (eski: $3643 aralash), karta yo'q bo'lsa 0 -> panel 3 cho'ntak — 4/4.

## v121: JAMI KASSA VA KUN JAMIDAN LOM PULI AYRILDI (Ibrohim: klient kassasida lomni pulini qo'shib ko'rsatvotti, qo'shmasin). AVVAL: jamiSumma va kun jami op.summa (sovda TO'LIQ summasi) dan yig'ilardi -> lom bilan to'langan qism ham "kassa" deb sanalardi. Lekin LOM — TILLA, pul emas: u lom cho'ntagiga tushadi, naqd kassaga emas (kassaOqim ham shunday ishlaydi). Misol: Durdona Opa 999 — jami $377.55 = naqt $255.87 + lom 1.66g ($121.68); kassaga faqat $255.87 tushgan. TUZATISH: (1) jamiSumma (JAMI KASSA stati) endi Math.max(0, o.summa − o.lomPul) dan yig'iladi. (2) Sessiyaga kassaSumma maydoni qo'shildi (lomsiz), summa esa avvalgidek to'liq qoladi. (3) Kun jami (daySumma) endi kg.kassaSumma dan yig'iladi. O'ZGARMADI: "Jami to'landi" qatori va sarlavhadagi summa — ular sovdaning TO'LIQ summasi ($377.55), ostida "naqt $255.87 · lom 1.66g · $121.68" tafsiloti (v118). Ya'ni sovda jami joyida, faqat KASSA statistikasi to'g'ri. Karta kassaga kiradi (u pul). Sinov (Node): 3 sovda — jami $1,576.46, kassaga $486.49 (naqt), lom $1,089.97 qo'shilmadi; lomsiz sovda o'zgarmadi — 4/4.

## v122: FIRESTORE KVOTASI TUGADI — AVTOMAT syncFullFill O'CHIRILDI (Ibrohim konsolida: FirebaseError [code=resource-exhausted]: Quota exceeded + "Using maximum backoff delay"). SABAB (Claude xatosi, v99.1): auth ulanganda 3.5s dan keyin syncFullFill() AVTOMAT chaqirilardi — u BUTUN dona bazani va BUTUN tarixni (synced-setga qaramay, MAJBURAN) cloudga push qiladi. Ya'ni HAR refresh / HAR qayta ulanish = minglab yozuv. Firestore bepul tarif: kuniga 20,000 yozuv / 50,000 o'qish. Bugungi ko'p sinov-refreshlar bilan kvota tugadi. TUZATISH: 14160-qatordagi avtomat setTimeout(syncFullFill, 3500) OLIB TASHLANDI. syncFullFill funksiyasi va cloudToldir (Cloud holati > "🔄 Hammani cloud bilan to'ldirish") QOLDI — endi u faqat QO'LDA, kerak bo'lganda ishlaydi. Oddiy sinxron (amalSyncPush — faqat YANGI yozuvlar, donaBazaCloudYoz — faqat yangi dona) avvalgidek ishlaydi va kam yozadi. NATIJA: refresh endi kvota yemaydi. TIKLANISH: Firestore kvotasi har kuni Tinch okeani vaqti bilan yarim tunda (Toshkentda ~12:00-13:00) tiklanadi — shu paytgacha cloud yozmaydi, ILOVA LOKAL ISHLAYVERADI (localStorage), ma'lumot yo'qolmaydi.

## v123: KVOTA TUGAGANDA CLOUDGA YOZISH TO'XTATILADI (Ibrohim: v122 dan keyin ham xato o'zgarmadi — tabiiy, chunki kunlik kvota ALLAQACHON tugagan; har urinish rad etiladi va konsolni spam qiladi, stackda kassaSnabshotYubor .set() ko'rinardi). QO'SHILDI: (1) _kvotaTugadi bayrog'i + cloudXato(e) tutgichi — xatoda 'resource-exhausted' yoki 'Quota exceeded' bo'lsa bir marta bayroq qo'yiladi, cloud holati QIZIL 'kvota tugadi' bo'ladi va konsolga BITTA tushuntirish yoziladi (spam o'rniga). (2) cloudYozaOladi() — 5 ta yozuvchi funksiya boshiga qo'riq: kassaSnapshotYubor, cloudSaqlaNow, amalSyncPush, donaBazaCloudYoz, syncFullFill — kvota tugagach ular JIM chiqadi, bekorga urinmaydi. (3) Barcha jim .catch(function(){}) lar .catch(cloudXato) ga almashtirildi (7 joy) — endi ruxsat xatosi avvalgidek jim, lekin KVOTA xatosi aniqlanadi va yozish to'xtaydi. MUHIM: bu kvotani QAYTARMAYDI — u Tinch okeani yarim tunida (Toshkentda ~12:00-13:00) o'zi tiklanadi. Bu faqat: konsol tinchiydi, bekorga trafik ketmaydi, foydalanuvchi holatni ko'radi (qizil 'kvota tugadi'). ILOVA LOKAL TO'LIQ ISHLAYVERADI — localStorage ga yoziladi, ma'lumot yo'qolmaydi; kvota tiklangach sahifa yangilansa cloud o'zi davom etadi.

## v124: KUNLIK YOZUV CHEKLOVI — BLAZE DA HISOB OSHIB KETMASIN (Ibrohim: Blazega o'taman, lekin sening xatoying bilan 100$ lab ketib qolsachi?). ADOLATLI SAVOL — v99.1 avtomat syncFullFill mening xatoym edi va kunlik kvotani tugatdi. QATTIQ HIMOYA: (1) YOZUV_LIMIT=25000/kun; cloudYozuvSana(n) har cloud .set() da sanaydi (localStorage 'tilla-cloud-yozuv' = {sana, n} — kun almashsa AVTOMAT 0 dan boshlanadi); chegara oshsa _kvotaTugadi=true -> cloudYozaOladi() false qaytaradi -> 5 ta yozuvchi funksiya (kassaSnapshotYubor, cloudSaqlaNow, amalSyncPush, donaBazaCloudYoz, syncFullFill) JIM to'xtaydi, cloud holati qizil 'yozuv limiti', konsolga bitta ogohlantirish. Ilova LOKAL to'liq ishlayveradi. (2) 6 ta .set() ga sanoq ulandi. NARX HISOBI (halol): Firestore Blaze — yozuv $0.18/100k, o'qish $0.06/100k. Chegara oshgan eng yomon holat: 25,001 yozuv/kun = $0.045/kun = $1.35/oy. $100 ga yetish uchun ~55 MILLION yozuv kerak — brauzerdan jismonan mumkin emas (tarmoq + Firestore rate-limit). Ya'ni $100 xavfi YO'Q; eng yomon holat ham bir necha dollar. Blaze da bepul kvota (50k o'qish/20k yozuv kunlik) saqlanadi — faqat undan oshgani pullik. TAVSIYA: Firebase Console > Budget & alerts > $10 ogohlantirish ham qo'yilsin (zaxira). Sinov (Node): 24,999 da yozadi, 25,001 da TO'XTAYDI, bayroq qo'yiladi, ertangi kunda sanoq 0 dan, kunlik eng yomon $0.045 / oylik $1.35 — 7/7.

## v125: CHIQIMLAR HISOBOTI (Ibrohim: menga chiqimlar qatta nima bo'ganini ko'radigan hisobot kerak, kassadagi chiqimlarni alohida hisoboti). QO'SHILDI — Kassa ekranida yangi ochiladigan bo'lim "CHIQIMLAR" (FOYDA — JORIY HOLAT va KASSA HARAKATLARI orasida). (1) kassaChiqimlar() — kassadan chiqqan hammasini yig'adi: naqt (data.kassa.qolda tip:'chiqim') + lom/999 (data.lomlar manba:'chiqim'); bitta chiqim uch qatorga bo'lingan bo'lsa (naqt+lom+999) ts bo'yicha BIRLASHTIRILADI; har biriga kursSanada(sana) dan kunlik kurs olinib foyda ta'siri hisoblanadi: naqt × (kunlik ÷ chiqim kursi − 1); yangi tepada. (2) kassaChiqimPanelHTML() — sarlavhada jami naqt (qizil, bosilsa ochiladi/yopiladi, _chOch); ochilganda uch stat (Naqt/Lom/999 jami), har chiqim qatori: kategoriya + izoh, sana·soat, kurs (kunlik bilan), miqdorlar (−$X −Yg lom −Zg 999), foyda ta'siri (yashil/qizil), va 🗑 tugma; pastda qora "Foydaga ta'siri" jami; eng pastda "📄 PDF — chiqimlar hisoboti". (3) kassaChiqimOchir(ts) — tasdiq so'rab bitta chiqimning HAMMA qatorlarini (naqt + lom + 999) o'chiradi, kassaga qaytadi, save+render. (4) kassaChiqimPDF() — chop etish oynasi: Sana / Nima uchun / Naqt / Lom / 999 / Kurs / Foyda + JAMI qatori, oltin sarlavha, zebra qatorlar. FAQAT kassada yozilgan chiqimlar (zavod ERPdagi chiqimlar bu yerda yo'q — ular Zavod ekranida). Sinov (Node): 3 chiqim — zavodga to'lov $24,766.7 @74.06 (kunlik 75.3) -> foyda +$414.67; Obed $3000+20g lom (kurssiz) -> foyda $0, naqt va lom BIRLASHDI; 999 10g @74.5 (kunlik 74.5) -> 1:1 foyda $0; yangi tepada; jami naqt $27,766.7 — 8/8.

## v126: CHIQIM NIMA YOPGANINI KO'RSATADI (Ibrohim: yopilgan chiqimni loadingga o'xshab yopish ko'rinmayapti, yashil bo'b yopilishi kerak, nima yopganini ko'rsatish kerak; qismanni bossa to'liq ko'rsatsin — qaysi turni qancha pulidan ketgan, foydasi o'zgarganini ham). QO'SHILDI: (1) kassaAmalYopgan() — pul navbatini qayta yurib, HAR AMAL (999/chiqim/zavod) QAYSI sovdalarni yopganini qaytaradi: [{amal, sovdalar:[{knom, sana, soat, sm, ol, ulush, ops}]}]. (2) kassaSovdaTurlar(sv, opKurs) — qisman sovdaning TUR bo'yicha taqsimoti: har turga tushgan pul (gramm nisbatida — skidka kabi), qotgan gramm (ekv×ulush), kirim KUNLIK->CHIQIM kursida (qat'iy/manual bo'lsa O'ZGARMAYDI), va foyda o'zgarishi = gQ×(kKun−kOp); jami foyda ham. (3) kassaChiqimYopdiHTML(o) — CHIQIMLAR bo'limida har chiqim ostida: LOADING chiziqcha (yashil=hammasi sovdaga ketdi / oltin=X% ketdi), so'ng yopilgan sovdalar ro'yxati — "✓ Klient $X" (yashil, to'liq) yoki "◐ Klient qisman $X ▼" (oltin, BOSILADI). Qismanni bosilganda (kassaChiqimSovToggle, _chSov): ikki rangli chiziqcha ($X yopildi / $Y qoldi), uch qator (Sovda jami / Bu chiqim yopdi (%) / Qoldi — hali suzadi), va TUR JADVALI: Tur | Puli | Kirim (eski→yangi) | Foyda; har turda "Xg · Yg qotdi", qat'iy narxli turlarda "o'zgarmas" va foyda $0.00; pastda "Shu sovdadan foyda". Kurssiz chiqim (Obed va h.k.) -> "Sovda yopmadi — oddiy rasxod". Sinov (Node): chiqim $10,000 @74.06 (kunlik 75.294) -> Guli Opa $5,675 TO'LIQ, Azimjon $4,325/$12,450 QISMAN (34.7%); Azimjon turlari: Butterfly·Oddiy $1,786 kirim 80.6->79.2 foyda +$29.18 (20.84g qotdi), Butterfly·3D $1,191 kirim 82.8->81.5 +$18.06, Simay QAT'IY 84->84 $0.00; shu sovdadan +$47.24; turlar puli = sovda olingani — 8/8.

## v127: CHIQIMDAN "999 / LOM OLISH" KATEGORIYASI OLIB TASHLANDI (Ibrohim: chiqimdan 999 sotib olsam kassaga 999 qo'shilmayapti, faqat foyda ko'rsatvotti; olgan 999 ko'rinishi kerak, ko'payishi kerak). SABAB (Claude dizayn xatosi, v119): Chiqim modaliga "999 / lom olish" kategoriyasi qo'yilgan edi — lekin CHIQIM MODALI FAQAT AYIRADI (naqt/lom/999 kassadan chiqadi), u hech narsa OLIB KELMAYDI. Ya'ni 999 ni chiqim orqali "sotib olsa" — pul chiqib ketardi, 999 esa KELMASDI (cho'ntak 0 qolardi), faqat kurs orqali foyda ko'rinardi. Bu chalkashlik edi. TO'G'RI YO'L: "+ Sotib olish" tugmasi (openKassaOlish) — u hammasini to'g'ri qiladi: pul chiqadi (data.lomlar kirim/manba:'kocha'/summa) + 999 yoki lom KIRADI (cho'ntakka qo'shiladi) + narx yoziladi -> kassaPulAmallar uni AVTOMAT oladi (kurs = narx÷1.7) -> pul navbatida eng eski sovdalarni yopadi va foydani ko'taradi. TUZATISH: (1) "999 / lom olish" kategoriyasi Chiqim modalidan olib tashlandi (qolgan kursli kategoriya: "Zavodga to'lov"). (2) Modalga ko'k eslatma qo'shildi: "999 yoki lom SOTIB OLISH uchun — '+ Sotib olish' tugmasini ishlating. Chiqim faqat kassadan chiqaradi, olib kelmaydi." Sinov (Node): "+ Sotib olish" 126g @125 = $15,750 -> naqd $50,000->$34,250, 999 0->126g QO'SHILDI, pul navbatiga tushdi (kurs 73.53, pul $15,750); CHIQIM bilan qilinsa -> naqd kamayadi lekin 999 KELMAYDI (aynan Ibrohim ko'rgan xato) — 6/6.

## v128: QULFLANISH CHIZIQCHASI SOVDA QATORIGA KO'CHDI, A VARIANT (Ibrohim: chiqimlarda emas, kassaning o'zida to'lib ko'rsatmaydimi; yashil bo'b, chiqimlarda kerak emas — klient kassasida loading bo'lishi kerak; A variantdek qil). (1) KASSA SOVDALAR RO'YXATI: har sovda qatorining OSTIDA 4px ingichka chiziqcha — pul navbatidan qancha qulflangani (op.qopUlush): to'liq (>=99.5%) YASHIL, qisman OLTIN (foiz kengligida), qulflanmagan bo'sh (kulrang). Qator kengligiga to'liq cho'zilgan (margin -11px), qator ichida joy egallamaydi. Vozvrat qatorlarida yo'q. Sarlavhadagi TO'LDI/QISMAN belgilari (v117) o'z joyida qoladi — belgi + chiziqcha birga. (2) CHIQIMLAR bo'limidagi KATTA loading bar OLIB TASHLANDI (Ibrohim: u yerda kerak emas) — o'rniga sodda sarlavha: "Yopilgan sovdalar · N ta · $X". Chiqim ichidagi ✓/◐ ro'yxati va qisman sovdaning tur-tafsiloti (v126) O'ZGARMADI.

## v129: SOTIB OLISH — GRAMM ⇄ SUMMA ⇄ NARX BOG'LANDI (Ibrohim: grammga summayam qo'shish kerak, shunda gramm avtomat chiqadi yoki gramm yozsa summa). AVVAL: modalda faqat Gramm va Narx bor edi, Summa yo'q — "$15,750 ga 999 oldim" desa grammni qo'lda hisoblash kerak edi. QO'SHILDI: (1) #ko-summa maydoni — Gramm bilan yonma-yon (2 ustunli grid), tepasida "Ikkitasini yozing — uchinchisi avto". (2) koTeg(k) — _koOxirgi massivi oxirgi ikkita tegilgan maydonni eslaydi; koHisob() uchinchisini hisoblaydi: summa=gramm×narx / gramm=summa÷narx / narx=summa÷gramm. (3) AVTO MAYDON tanlash mantiqi: agar BITTA maydon bo'sh bo'lsa — o'shani hisoblaydi (foydalanuvchi ikkitasini yozdi); IKKITASI bo'sh bo'lsa — hech narsa qilmaydi (hali yetarli emas); HAMMASI to'la bo'lsa — oxirgi ikkitadan tashqarisini qayta hisoblaydi (masalan narx o'zgarsa summa yangilanadi, gramm saqlanadi). Bu muhim: avvalgi sodda mantiq bo'sh maydon bo'lsa to'la maydonni O'CHIRIB yuborardi. (4) Avto maydon KO'RINISHI: uzuq ramka + kulrang matn + "· avto" yorlig'i; qo'lda yozilganlar oltin ramka + qalin. (5) 999 ⇄ 583 sinxroni (koNarxSync) saqlandi; koHisob narxni o'zi hisoblaganda 583 ni koPreview CHAQIRMASDAN yangilaydi (aks holda koNarxSync->koPreview->koHisob CHEKSIZ SIKL bo'lardi) + _koIch qo'rig'i. Sinov (Node): 126g+125$/g -> summa $15,750; $15,750+125 -> gramm 126; 126g+$15,750 -> narx 125; hammasi to'la bo'lib narx 125->130 -> summa $16,380 (gramm saqlandi); summa 15,750->16,380 -> narx 130 (gramm saqlandi); ikkitasi bo'sh -> hech narsa hisoblanmaydi — 8/8.

## v130: (1) CHIQIMDAN SOVDALAR RO'YXATI OLIB TASHLANDI (Ibrohim: chiqimdan chiqarvor kassalarni). kassaChiqimYopdiHTML(o) chaqiruvi kassaChiqimPanelHTML dan olindi — endi CHIQIMLAR bo'limi faqat: kategoriya + izoh, sana/soat, kurs (kunlik bilan), miqdorlar, foyda ta'siri, 🗑. Yopilgan sovdalar ro'yxati va qisman tur-tafsiloti endi ko'rsatilmaydi (funksiyalar kodda qoldi, chaqirilmaydi). Qulflanish endi FAQAT sovdaning o'zida ko'rinadi (v128 chiziqcha + TO'LDI/QISMAN belgisi) — Ibrohim aynan shuni so'ragan. (2) SOVDA CHIZIQCHASI OVERFLOW TUZATILDI: v128 da chiziqchaga margin:8px -11px -1px (manfiy, qator kengligiga cho'zish uchun) qo'yilgan edi — bu gorizontal toshishga (o'ng tomonda kesilgan elementlar, keraksiz scroll) olib kelardi. Endi margin:8px 0 2px + border-radius:2px — qator ichida, toshmaydi. Fayldagi qolgan manfiy marginlar faqat tik (yuqori/past) — zararsiz.

## v130.1: VERSIYA BANNERI (Ibrohim: keyingi o'zgarishda vNNN qilib tepada dashboardda yozib ket, adashmasligim uchun). QO'SHILDI: APP_VER o'zgaruvchisi (hozir 'v130') + DOMContentLoaded da o'ng YUQORI burchakka kichkina oltin yorliq (position:fixed, z-index 99998). TEST rejimida TEST bannerining ostiga tushadi (top:20px), toza rejimda tepada (top:0). Bosilsa yashiriladi. QOIDA: HAR YANGI VERSIYADA APP_VER raqami YANGILANSIN — shunda qurilmada qaysi versiya turgani bir qarashda ko'rinadi (deploy qilindimi, Ctrl+Shift+R yordam berdimi — darhol bilinadi).

## v130.2: VERSIYA YORLIG'I O'NG PASTGA KO'CHIRILDI (Ibrohim rasm: log out tugmasining ustiga yozib qo'yibsan). Avval top:0/20px; right:6px edi — u yerda tepadagi tugmalar (cloud, kurs, mavzu, tarix, sozlamalar, chiqish) turadi va yorliq ularni to'sardi. Endi bottom:6px; right:6px — o'ng pastki burchak, hech narsani to'smaydi; shaffofroq (opacity .75, fon .55) va kichikroq (9px) — ko'zga tashlanmaydi, lekin kerak bo'lsa o'qiladi. Bosilsa yashiriladi (avvalgidek).

## v131: TEST BANNERI O'NG PASTGA (Ibrohim rasm: mobil versiyada test banner tepadagi knopkalarni yopib qo'yvotti). Avval: position:fixed; top:0; left:50%; katta matn "🧪 TEST REJIMI — alohida baza, haqiqiyga tegilmaydi" — telefonda ikki qatorga bo'linib, tepadagi tugmalar qatorini (cloud, kurs, mavzu, tarix, sozlamalar, chiqish) TO'SIB qo'yardi. Endi: bottom:6px; right:48px (versiya yorlig'ining chap yonida), qisqa "🧪 TEST" matni, kichik (9px), shaffof (opacity .8), bosilsa yashiriladi; to'liq matn title da (hover/uzoq bosishda ko'rinadi). Versiya yorlig'i (v131) bottom:6px; right:6px — ikkalasi yonma-yon o'ng pastda, hech narsani to'smaydi. APP_VER v130 -> v131.

## v132: CLOUD'DAN MAJBURAN YUKLAB OLISH tugmasi (Ibrohim: "Hammani cloud bilan to'ldirish" ni PC dan bossam iPhoneda o'zgarmayapti; lomlar/kassalar o'tdi lekin zavod va klient ostatkalari shakllanmayapti). ILDIZ (Claude qarorlari): (1) v93 da blob YUKLAB OLISH o'chirilgan edi — "blob faqat YANGI/BO'SH qurilmani birinchi to'ldirish uchun"; ma'lumoti bor qurilma cloud blobini HECH QACHON olmaydi. (2) Oplog (_amallar) faqat TARIXNI tashiydi. (3) data.kassa OBYEKT bo'lgani uchun v97 da oploqdan CHIQARILGAN — Z-hisoblar, tuzatishlar, zakazlar faqat blob orqali o'tadi. (4) Zavod ostatkasi — saqlangan running-total, oplogda yo'q; v104 da avtomat qayta-hisoblash ham o'chirilgan (u ostatkani buzardi). NATIJA: syncFullFill ("to'ldirish") faqat tarix+dona yuboradi -> boshqa qurilmada kassa va ostatka O'ZGARMAYDI. QO'SHILDI: Cloud holati oynasida IKKI tugma — "⬆ Bu qurilmanikini cloudga yuborish" (eski cloudToldir/syncFullFill: tarix+dona, qo'shadi, o'chirmaydi) va yangi "⬇ Cloud'dan yuklab olish (ustidan yozadi)" -> cloudMajburanOl(): tasdiq so'raydi (yo'qoladigan narsani aniq aytadi), AVTOMAT backupExport oladi, amal-init/synced flaglarini tozalaydi (yuklangach tarix qayta pushlanmasin), doc('holat') meta sini o'qib cloudYuklab(meta) chaqiradi — kassa, ostatka, klientlar, hammasi TO'LIQ yuklanadi. Ostidagi izohda ikkala tugma farqi tushuntirilgan. FOYDALANISH: to'g'ri qurilmada ⬆, boshqasida ⬇. APP_VER v131 -> v132.

## v133: KASSA SOVDALARIDA SUMMA USTUNI TEKISLANDI (Ibrohim rasm: kassadagi pullarni o'ng tarafga o'tqiz, o'rtada tartibsiz bo'p qolgan). SABAB: o'ng blok [summa+foyda][🖨] flex bo'lib, summa matni kengligi har xil ($500 / $2,929.92) -> chop tugmasi har qatorda BOSHQA joyda turardi, summalar ham tekis emas edi. TUZATISH: (1) summa/foyda ustuniga min-width:112px + white-space:nowrap — hamma summa bir xil kenglikda, o'ng chetga tekis; chop tugmalari bir ustunda. (2) o'ng blokka flex-shrink:0 va margin-left:auto — uzun klient ismi uni surib yubormaydi. (3) chap blokka min-width:0; flex:1 va belgilar qatoriga flex-wrap:wrap — uzun ism + ko'p belgi (NAQT/LOM/KARTA/OFFSET/TO'LDI) bo'lsa ikkinchi qatorga tushadi, o'ng ustunni bosmaydi. APP_VER v132 -> v133.

## v134: CHEKDAGI 3 XATO TUZATILDI (Ibrohim chek rasmi). (1) "Jami to'landi" -> "JAMI SUMMA" (2,299.13) — u to'langan pul emas, sovdaning jami summasi; naqt/lom/karta ostida alohida ko'rsatiladi. (2) Gramm avval yorliqsiz qavs ichida "(27.13)" chiqardi — endi "JAMI GRAMM 27.13" deb yozuv bilan. (3) ENG JIDDIY: N (naqt berildi) qatori faqat `ktNb>0 && ktKb>0` (naqt VA karta ikkalasi ham bo'lsa) chiqardi — faqat naqt berilsa (odatdagi holat!) N UMUMAN KO'RINMASDI, klient qancha naqt berganini bilib bo'lmasdi (rasmda: L 10.7×72.7=777.89 bor, N esa bo'sh). Endi har biri ALOHIDA: `if(ktNb>0) N`, `if(ktKb>0) K`. Uch tuzatish ham IKKI chekda — To'lov (kt-) va Sotuv (ks-); sotuv chekida qamrov sharti ham to'g'rilandi (`(_naqtBerdi2>0 && _kartaBerdi2>0)` -> `_naqtBerdi2>0 || _kartaBerdi2>0`), aks holda faqat naqtli sotuvda butun blok tushib qolardi. APP_VER v133 -> v134.

## v135: OFFSET SOVDA ICHIGA KIRDI (Ibrohim rasm: offsetga alohida ko'rsatma; kassaga Naqt+offset deb, 2-rasmga o'xshab offset summasini ko'rsatishi kerak; offset bo'lgan summani foyda emas ZARAR qilib ko'rsatish kerak; qolgan bergan naqt pulini alohida ko'rsatish kerak — shunda kassa to'g'ri chiqadi). ILDIZ: offset yozuvida (klientTolovSaqla, _kdYopish:true) SOAT maydoni YO'Q, sotuvda esa bor -> sessiya kaliti (ki|sana|soat) farq qilib, offset ALOHIDA QATOR bo'lib chiqardi ("Hafiza Opa OFFSET · 0.00g · $0 · ($329.16 o'zi offset)"), sotuvda esa "Jami to'landi $782.16" deb turib naqt faqat $453 edi — $329.16 hech qayerda ko'rinmasdi. TUZATISH: (1) allOps yig'ilgach, soati BO'SH offset oplarga o'sha kundagi (ki|sana) eng katta sotuv sessiyasining soati beriladi -> offset sotuv bilan BITTA sessiyaga tushadi. (2) Sarlavha ostidagi qatorga offset qo'shildi: "naqt $453.00 · offset $329.16" (binafsha) — 2-rasmdagi "naqt · lom" kabi. (3) Eski "($X o'zi offset)" qatori olib tashlandi. (4) "Jami to'landi" -> "JAMI SUMMA"; ostidagi Naqt/Karta/Lom tafsilotiga "↔ Offset Xg · $Y" qatori qo'shildi (binafsha). (5) Tur jadvalida offset qatori binafsha va ZARAR (v115 dan) — foyda endi 2.10+16.00−2.73 = +$15.37 (avval offset zarari sanalmay +$18.10 chiqardi). KASSAGA faqat naqt tushadi (offset pul emas — v121 dan). APP_VER v134 -> v135.

## v136: PERECHISLENIYA (Ibrohim mockup v3 bo'yicha, 1ma-1 tasdiqlangan). Perech = bankdan TO'G'RIDAN zavodga ketadi, biz klientga mol beramiz. Naqt/karta kabi to'lov turi, lekin kassada TURMAYDI va chiqimi YO'Q. Yangi maydon op.perechPul (naqtPul/kartaPul/lomPul yonida); eski yozuvlarda yo'q -> ||0, migratsiya kerak emas. Feruza rang: yangi CSS tokenlar (–teal / –teal–bg / –teal–bd) ikkala mavzuga.
(1) MODAL (kt- va ks- ikkalasida): Karta ostiga Perech qatori (katakcha + input). ktToggleTolov/ksSotuvToggleTolov o'rniga umumiy _tolovToggle(pre,tip,roOn,cb) + TOLOV_TURLARI ro'yxati — ✓ katakcha = "hammasi shu bilan" (kerakli summa, qolgan ikkitasi tozalanadi). AVTO-TO'LDIRISH qayta yozildi: eski lastChanged (ikki maydon bir-birini to'ldiradi) 3 maydonda ishlamasdi -> yangi _tolovAvto(pre,kerakli): qo'lda tegilgani (userEdited) QOTADI, tegilmaganlaridan BIRINCHISI (naqt->karta->perech) qoldiqni oladi; uchalasi tegilsa avto yo'q, sdacha/kam chiqadi.
(2) FOYDA QOTADI (Ibrohim: perech qotadi zavodga ketadi; kartayam navbatga kirmidi qotadi). kassaPulNavbati() ga qo'shildi: karta+perech navbatga KIRMAYDI, sotuv kunidagi kursda (kursSanada) DARHOL qotadi — ulush=(kartaPul+perechPul)÷summa, qopKurs=o'sha kungi asosiy kurs. kassaSuzuvchiXaritasi blendi O'ZGARMADI (_kh=ulush×_kQop+(1−ulush)×kirimNarxHozir) — perech/karta va 999/chiqim navbati bir xaritada o'lchovli o'rtacha bo'lib qo'shiladi; ALOHIDA foyda qatori yozilmaydi (v108/v116 falsafasi). Aralash sovdada naqd hissasi endi aniq nisbatda (it.shr=1−qulf÷summa) — avval naqd to'liq yeyilsa BUTUN gramm qotib ketardi. `if(!A.length) return m` olib tashlandi — amal bo'lmasa ham karta/perech qotadi.
(3) KASSA PANELI 3x2 (Ibrohim: 1x5 bo'p ketadi, 3x2 qil): TEPADA pul (Naqd · Karta · Perech — dinamik, bor bo'lsa chiqadi), TAGIDA oltin (Lom 583 · 999). Uchala pul cho'ntagi BOSILADI (› belgisi) -> hisobot. Naqd ostidagi erkin/band o'zgarmadi. kassaOqim ga o.perech qo'shildi — naqd bilan QO'SHILMAYDI, bu yig'ma OQIM (chiqimi yo'q).
(4) TO'LOV HISOBOTI — yangi #modal-tolov-hisobot, bitta modal uch kirish: openTolovHisobot('naqt'|'karta'|'perech'). Davr (Bugun/Hafta/Oy/Hammasi), qator: sana+soat · klient · zavod·tur · gramm · summa + QULF belgisi (TO'LDI / N% / suzadi — kassaPulNavbati ulushidan). Gramm = ekvivalent×(shu maydon÷summa) — aralash sovda ikki hisobotda ham chiqadi, ikki marta SANALMAYDI. PDF: tip 'tolov_hisobot'.
(5) CHEK: P qatori K dan keyin, har biri alohida; yorliq "JAMI SUMMA  N  K  P". Uch joyda (kt preview, ks preview, ks chop/PDF). Sdacha hisobiga perech qo'shildi. Kassa PDF (kassaPDFYukor) ga naqt/karta/perech/lom ustunlari va jami_naqt/jami_karta/jami_perech/jami_lom.
(6) UCHTA ESKI XATO TUZATILDI (perech shu joylarga qo'shilgani uchun majburiy edi): (a) saqlashKlientTolov da kartaPul:0 QAT'IY yozilardi -> To'lov modalidagi karta puli naqtPul ga singib ketardi, kassa "Naqd" ni ko'p ko'rsatardi VA u pul navbatiga kirib foydani noto'g'ri qulflardi. (b) sotuv saqlashda karta FAQAT lom bo'lganda yozilardi (_lomPulJamiSave>0 ? ... : 0) -> lomsiz sof karta sotuvi butunlay NAQT bo'lardi; endi maydon har doim o'qiladi (_aralash). (c) kassaHarakatlar (lenta) da pul=naqtPul+kartaPul -> lenta yugurma qoldig'i kassaOqim.naqd bilan mos kelmasdi (v120 dan beri karta alohida); endi lentaga faqat naqt tushadi, perech umuman kirmaydi (kassa harakati emas). Yo'l-yo'lakay: ks chek PREVIEW ida N/K faqat IKKALASI bo'lsa chiqardi (v134 buni kt da tuzatib, ks preview da o'tkazib yuborgan) — endi har biri alohida.
SINOV (Node, 29/29): navbatsiz ham perech ulush 0.7826 · qopKurs 71.8447; sof karta ulush 1 (TO'LDI); sof naqt xaritada yo'q (suzadi); foyda — sof karta +18.56 QOTDI, sof naqt −7.96 SUZDI, aralash naqt500+perech1800 -> +29.44 (asl 42.70 dan qisman); 999 xaridi $500@70 kelganda Butterfly ulush 1, qopKurs 71.44 (o'lchovli), Rano tegmadi; cho'ntaklar naqd 1500 / karta 1000 / perech 1800 — qo'shilib ketmadi; eski yozuv (naqtPul yo'q) naqdga tushdi va navbatga kirdi — buzilmadi; avto-to'ldirish perech1800->naqt500, naqt500+perech1000->karta800, uchalasi tegilsa avto yo'q, sdacha 200, manfiy chiqmaydi; ✓ katakcha almashinuvi. APP_VER v135 -> v136. ESLATMA: perech cho'ntagi CHIQIMSIZ — faqat o'sadi (yig'ma oqim), tagida "oqim" yozuvi bor.

## v136.1: KASSA PANELI 3x2 BO'LMADI — TUZATILDI (Ibrohim rasm: tepada bitta Naqd butun kenglikda, Karta va Perech umuman yo'q). SABAB (Claude xatosi): v136 da panelga v120 ning DINAMIK sharti (_kartaBor) ko'chirib olingan va perechga ham qo'llangan edi — `_pulN = 1 + (_kartaBor?1:0) + (_perechBor?1:0)`, ya'ni qiymat 0 bo'lsa cho'ntak UMUMAN chizilmasdi. Ibrohimning haqiqiy ma'lumotida karta $0 (v136 gacha To'lov modalidagi karta naqtga singib ketardi, Sotuvda esa faqat lom bilan yozilardi) va perech $0 (hali birinchi yozuv kiritilmagan) -> tepa grid repeat(1,1fr) bo'lib bitta Naqd qolgan. Ibrohim so'ragani DINAMIK emas, QAT'IY 3x2 edi. TUZATISH: _kartaBor/_perechBor/_pulN olib tashlandi; tepa qator DOIM grid-template-columns:1fr 1fr 1fr (Naqd · Karta · Perech — $0.00 bo'lsa ham turadi, hisoboti bosilaveradi va panel joyidan siljimaydi), tag qatori DOIM 1fr 1fr (Lom 583 · 999). Boshqa hech narsaga tegilmadi (kassaOqim, hisobot, foyda qulfi, chek — hammasi v136 dagidek). Sinov (Node, panel HTML rasmdagi haqiqiy holat bilan chizildi: naqd $214,986.85 / karta 0 / perech 0): tepa grid 3 ustun, tag grid 2 ustun, jami 2 grid, beshala katak ham chizildi, Karta $0.00 ko'rindi, Naqd/Karta/Perech uchtasida ham openTolovHisobot onclick bor, Lom583/999 bosilmaydi — 11/11; v136 ning eski 29 sinovi ham qayta o'tkazildi (29/29). APP_VER v136 -> v136.1.

## v137: SDACHA BO'LIMI TIRILTIRILDI (Ibrohim: "sdacha bo'limi ishlamayapti sotuv va to'lov modalida"). TASHXIS — bu v136 regressiyasi EMAS, v135 dan beri o'lik edi: sdachaTaqsimRender() 48 qator to'liq yozilgan, lekin HECH QAYERDAN CHAQIRILMASDI (eski faylda ham chaqiruv 0 ta); ikkala modal har renderda panelni SHARTSIZ yashirardi (kt: `if(ktTaqsimEl) ktTaqsimEl.style.display='none'`, ks: `tqEl2.style.display='none'` + ks-qaytim yashirilib qiymati tozalanardi); sdachaInpUpd/sdachaJamiUpd/sdachaPrich bo'sh {} stublar. O'rniga JIM avto-tanlov ishlardi — kod o'zi _ktSdachaTanlov ni birinchi qarzli turga qo'yib, saqlashda sdachani o'sha turga grammga aylantirardi, foydalanuvchiga ko'rsatmasdan. Sdacha RAQAMI to'g'ri hisoblanardi (Node bilan 6 stsenariy sinaldi: naqt 2500 -> 200; karta 3000 -> 700; naqt+karta+perech 2800 -> 500) — faqat TANLASH ko'rinmasdi.
(1) PANEL OCHILADI: kt da `sdachaTaqsimRender('kt', ktSdacha, ktTaqsimAllMap, ki_kt2)` + kt-sdacha-sum to'ldiriladi (sdacha>0.01 bo'lsa; aks holda yashiriladi); ks da `sdachaTaqsimRender('ks', ortiqcha, ksSdachaMap, _ksSotuvKi)` + ks-qaytim bloki ochiladi va qiymati ortiqcha bilan to'ladi (fokusda bo'lmasa — yozayotganda ustidan yozilmasin). Hozirgi avto-tanlov OLDINDAN BELGILANGAN bo'lib ko'rinadi — hech narsa bosilmasa natija v136 dagidek, lekin endi ko'rinadi va o'zgartirsa bo'ladi.
(2) RO'YXAT FAQAT KLIENT OLGAN TURLARDAN (Ibrohim: "bizda qolsinmas turga o'tishi kere, umumiy o'tmidi, qaysidur turga o'tqizvoramiz — klient olgan zavod turlariga, bizani qarz qib qoyadi"). kt da ktTaqsimAllMap AVVAL BUTUN KATALOGDAN qurilardi (data.zavodlar.forEach -> hamma tur) — klient ko'rmagan turlar ham chiqardi; endi faqat k.tarix dagi zavod-turlar (ks dagi ksSdachaMap allaqachon shunday edi — endi ikkalasi bir xil). Katalogda topilmagan tur (zi/ti<0) ro'yxatga kirmaydi.
(3) TARTIB VA BELGILAR: qarzi bor turlar TEPADA (kattaroq qarz oldinroq), keyin qarzi yo'qlar, Sdacha ENG OXIRIDA (avval sdacha birinchi edi). Har turda nishon: "QARZI BOR" (oltin) yoki "QARZI YO'Q" (yashil). Qarzli turda izoh "200.00$ ÷ 75.40$/g = 2.65g -> qarzidan yechiladi (30.50g -> 27.85g)", qarzsizda "-> biz klientga qarzdor (+)". "Bizda qolsin" varianti QURILMADI (Ibrohim rad etdi) — kodda qolgan 'bizda' shoxobchalari (kTolovSdachaTanlovSet, chek) allaqachon o'lik, tegilmadi. Klient hech qanday tur olmagan bo'lsa faqat Sdacha + tushuntirish matni (Ibrohim: "klient hech nima olmasdan lom sotsa, bizda allaqachon chiqim bor, o'shanga kirib chiqim qilib lomni ob qolamiz — bu muammomas").
(4) LOM SDACHASI ENDI KASSADAN CHIQIM (Ibrohim: "kassadan ketgan pul chiqimga o'tadi, unga masalan lom olganda bo'ladi — ortiqcha sdachi bo'lib lomimiz grami oshadi, kassada naqt pul kamayadi i hisobotda ko'rinadi"). MUAMMO: lom qarzdan katta bo'lsa (qarz $2,300, lom $2,500) saqlashda lomPul yig'indisi 2500, summa yig'indisi 2300, _ktQoldiq 0 ga qisiladi — lomning to'liq $2,500 i lom cho'ntagiga tushadi, klient qarzi esa $2,300 ga kamayadi, ortgan $200 uchun cho'ntakdan NAQT chiqadi lekin kassa bilmasdi (naqdni $200 ga ko'p ko'rsatardi). Klient lomi manba:'klient' bilan yoziladi -> naqdga tegmaydi (to'g'ri, u qarz to'lovi); ko'chadan olingan lom manba:'kocha' -> naqd −summa. Ortgan qism aynan "ko'chadan lom oldim" bilan bir xil. YECHIM: "Sdacha" tanlanганда va ortiqcha LOMDAN kelgan bo'lsa data.kassa.qolda ga {tip:'chiqim', summa, kategoriya:'Lom sdacha', izoh:klient nomi} yoziladi — mavjud mexanizm, yangi narsa ixtiro qilinmadi: kassaOqim 3.7 -> naqd −summa; kassaHarakatlar -> lentada qator; chiqim filtrida "qo'lda" bandi bor -> hisobotda ko'rinadi. NAQT/KARTA ortiqchasida yozuv YO'Q (avvalgi xulq to'g'ri edi: klient 2500 berdi, 200 qaytdi, kassaga sof 2300 tushadi). Manbani aniqlash: kt da lomOrtiqcha>0.01 -> _manba='lom'; ks da yangi window._ksSotuvOrtiqchaManba ('lom'/'gramm'/'pul') kSotuvCalc da qo'yiladi.
(5) v136 XATOSI TUZATILDI (meniki): sdachaTaqsimSaqla da `sdacha = ktNb + ktKb − ktKn` — PERECH unutilgandi, perech bilan ortiqcha to'lansa sdacha yo'qolardi. Endi ktNb+ktKb+ktPb.
SINOV (Node, 23/23 + v136 ning 40 tasi qayta): lom ortiqchasi+Sdacha -> qolda chiqim $199.97 'Lom sdacha'/'Butterfly', klient tarixiga hech narsa yozilmadi; naqt ortiqchasi+Sdacha -> qolda yozuvi YO'Q; perech bilan sdacha $500 (perechsiz $300 bo'lardi) -> qarzsiz turga klientda op 6.63g, qarzli turga tolov op _bizQarzYopildi ekv 6.63g; panel — qarzi bor tur birinchi, qarzsiz ikkinchi, Sdacha oxirida, nishonlar joyida, "Bizda qolsin" yo'q, panel display:block; tarixi yo'q klient -> faqat Sdacha + tushuntirish. APP_VER v136.1 -> v137.
QOLGAN (tegilmadi, Ibrohimga aytildi): (a) kTolovCalc dagi ktSdacha = ktLomOrtiqcha + totalGramOrtiqcha + pulOrtiqcha, sdachaTaqsimSaqla esa totalGramOrtiqcha ni KO'RMAYDI — gramm ortiqchasi ko'rsatiladi-yu saqlanmaydi (eski nomuvofiqlik). (b) sdachaTaqsimSaqla 'tur' holatida ekvivalent min(gramm,turQarz) ga qisiladi lekin summa to'liq yoziladi — qisilgan qism yo'qoladi. (c) qolda yozuvlari zavod ERP snabjenets payloadiga ham kiradi (manba==='qolda') — lom sdachasi u yerda ham chiqim bo'lib ko'rinadi.

## v137.1: PERECH QOLIB KETGAN 3-JOY TOPILDI (Ibrohim so'radi: "perechda nima xato qildin" -> audit qildim va yana bittasi chiqdi). ks CHOP/PDF chekining "Jami summa" yorlig'ida (_tMk) perech yo'q edi: `_tMk=(_tNbM>0?'  N':'')+(_tKbM>0?'  K':'')` -> perech bilan to'langanda chekning pastida "P  1,800.00#" qatori chiqardi (u v136 da to'g'ri qo'shilgan), lekin TEPADAGI yorliq "Jami summa  N" bo'lib qolardi — P ko'rinmasdi. Endi _tPbM qo'shildi.
ILDIZ: v136 da men aniq o'zgaruvchi nomlarini grepladim (_kartaBerdiSave, ktBerdiK2, _kbPrev, _ksKbM, _ktKbM, _kartaBerdi2) — `kt-karta-berildi` / `ks-karta-berildi` MAYDONINI o'qiydigan HAMMA joyni emas. Shuning uchun boshqa nomdagilar (sdachaTaqsimSaqla dagi ktKb -> v137 da tuzatildi; bu yerdagi _tKbM -> v137.1) ko'rinmay qoldi.
AUDIT (endi to'liq, ikki yo'nalishda): (1) `getElementById('k[ts]-karta-berildi')` o'qiladigan 14 joy — hammasida perech yonida bor (12405 yolg'on trevoga: nbKEl e'loni, perech reseti 6 qator pastda). (2) "Jami summa" yorlig'i quriladigan 3 joy (kt preview 11118, ks preview 12754, ks chop 13261) — uchalasi ham N+K+P. (3) op.kartaPul o'qiydigan joylar: 2115/3049/4169 eski-yozuv zaxira shoxobchasi `naqtPul!==undefined ? naqtPul : (kartaPul?0:summa)` — v136+ yozuvlarida naqtPul DOIM aniqlangan, shuning uchun bu shoxobcha perechli yozuvda umuman ishlamaydi (xato emas, tegilmadi); 11356/11432/13082 offset/_kdYopish/sdacha oplari `naqtPul:0, kartaPul:0` yozadi, perechPul yo'q — `parseNum(op.perechPul||0)` hamma joyda 0 beradi, funksional farq yo'q (tegilmadi).
SINOV: mavjud 63 sinov qayta o'tkazildi (v136: 40, v137: 23) — hammasi o'tdi. APP_VER v137 -> v137.1.
