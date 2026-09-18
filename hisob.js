// ══════════════════════════════════════════════════════════════
// TILLA ERP — HISOB
//
// Bu fayl `index.html` DAN CHIQARILDI. Nusxa EMAS — asl joyidan olindi,
// index.html endi uni <script src="hisob.js"> bilan yuklaydi.
//
// Sabab (Ibrohim, 2026-09-06): POS Tilla ERP ichidan chiqarilib `pos.html`
// bo'ladi. Ikkalasi ham qarz va narxni AYNI shu funksiyalar bilan hisoblasin.
// Nusxalansa raqamlar ajraladi — v177.4 da aynan shu bo'lgan (POS +557.46,
// ilova 559.58).
//
// ⚠ NUSXA KO'CHIRILMAYDI. Bu funksiyalar faqat SHU YERDA yashaydi.
//
// SAHIFADAN KERAK BO'LADIGAN UCHTA NARSA (o'lchandi, boshqasi yo'q):
//   1. `data`        — global ma'lumot obyekti (zavodlar / klientlar)
//   2. `_aktivKat`   — narx kategoriyasi 'A' | 'B' | 'C' (getKatNarx uchun)
//   3. `localStorage` — kurs kalitlari: tilla-kurs-bugun, tilla-b-ust va h.k.
//
// `pos.html` yozilganda SHU UCHTASI e'lon qilinishi shart.
// Bu fayl o'zi hech nima bajarmaydi — faqat funksiya e'lon qiladi.
// ══════════════════════════════════════════════════════════════

var _ostKesh = null;   // v172.26: bir renderda qayta-qayta sanamaslik uchun
function turOstKeshTozala(){ _ostKesh = null; }

function parseNum(v) { if (!v && v !== 0) return 0; return parseFloat(String(v).replace(/,/g, '.')) || 0; }

// v188.23 (Ibrohim): «agar FAEF1,02 shunaqa narsalar kelib qosa qabul
// qimasligini» — skaner bir xil kodni takror o'qiganda 2 sekund kutib,
// oldiga «FAEF» kabi prefiks qo'shib yuborar ekan.
// Raqam / nuqta / vergul / probel / + / - dan BOSHQA belgi bo'lsa qiymat
// ISHONCHSIZ — taxmin qilinmaydi, rad etiladi.
// ⚠ parseNum ga TEGILMADI — u pul, kurs, proba maydonlarida ham ishlaydi.
function skShovqin(v){ return /[^\d.,\s+-]/.test(String(v == null ? '' : v)); }

function fmtG(g) { var v=parseFloat(g); return (v<0?'-':'')+Math.abs(v).toFixed(2); }

function fmtD(d) { return parseFloat(d).toLocaleString('en-US', {maximumFractionDigits:2}); }

function today() { return new Date().toLocaleDateString('ru-RU', {day:'2-digit',month:'2-digit',year:'numeric'}); }

function roundG(v) { return Math.round(v * 100) / 100; }

function _ostDelta(op, klientTomon){
  if(!op) return 0;
  var g = parseNum(op.gramm);
  if(klientTomon){
    if(!op.zavod || !op.tur) return 0;
    if(op.tip!=='berish' && op.tip!=='vozvrat') return 0;
    if(op.inventar==='boshlangich') return 0;   // zavoddan chiqmagan
    if(!(g > 0)) return 0;                      // manfiy berish — pul-asosli, omborga tegmaydi
    return (op.tip==='berish') ? -g : g;
  }
  if(op.tip!=='mol' && op.tip!=='vozvrat') return 0;
  if(!g) return 0;
  if(op.inventar) return (op.tip==='vozvrat' ? -g : g);   // shakllantirish / tekshiruv tuzatishi
  return (op.tip==='mol') ? g : -g;
}

function turOstMap(){
  if(_ostKesh) return _ostKesh;
  var m = {};
  (data.zavodlar||[]).forEach(function(z){
    (z.turlar||[]).forEach(function(t){
      var key = z.nom+'||'+t.nom, s = 0;
      (t.tarix||[]).forEach(function(op){ s += _ostDelta(op, false); });
      m[key] = s;
    });
  });
  (data.klientlar||[]).forEach(function(k){
    (k.tarix||[]).forEach(function(op){
      var d = _ostDelta(op, true);
      if(!d) return;
      var key = op.zavod+'||'+op.tur;
      m[key] = (m[key]||0) + d;
    });
  });
  Object.keys(m).forEach(function(key){ m[key] = roundG(m[key]); });
  _ostKesh = m;
  return m;
}

function turOst(zNom, tNom){
  var m = turOstMap();
  return m[zNom+'||'+tNom] || 0;
}

function klientJamiQarz(k) {
  return _qarzJamiRows(_qarzTarkibRows(k)).ostatka;
}

function klientJamiSavdo(k) {
  var g=0,pul=0;
  k.tarix.forEach(function(op){
    if(op.tip==='tolov' && !op._kdYopish) { g+=(op.ekvivalent||0); pul+=op.summa||0; }
  });
  return {g:Math.round(g*100)/100, pul:Math.round(pul*100)/100};
}

function getKatNarx(zi, ti, ki) {
  var kurs = parseFloat(localStorage.getItem('tilla-kurs-bugun') || '0');
  if (!kurs) return '';
  // v172.23: klient yozuvidagi kat emas — shu amal uchun tanlangan kategoriya (doim A dan boshlanadi)
  var kat = _aktivKat || 'A';
  if (kat === 'A' || kat === 'B') {
    // A: kurs + A%,  B: kurs + A% + ustama
    var aManual = JSON.parse(localStorage.getItem('tilla-a-manual-'+zi) || '{}');
    var aFoizlar = JSON.parse(localStorage.getItem('tilla-a-foiz-'+zi) || '{}');
    var aNarx = aManual[ti] ? aManual[ti] : ((parseFloat(aFoizlar[ti])||0) > 0 ? Math.round(kurs*(1+parseFloat(aFoizlar[ti])/100)*10)/10 : '');
    if (!aNarx) aNarx = getZavodNarx(zi, ti); // fallback
    if (kat === 'B' && aNarx) {
      var bUst = parseFloat(localStorage.getItem('tilla-b-ust') || '0') || 0;
      return bUst > 0 ? Math.round((parseFloat(aNarx)+bUst)*10)/10 : aNarx;
    }
    return aNarx;
  }
  // C: qo'lda narx kiritiladi — bo'sh qoladi
  return '';
}

function getZavodNarx(zi, ti) {
  var kurs = parseFloat(localStorage.getItem('tilla-kurs-bugun') || '0');
  if (!kurs) return '';
  var manual = JSON.parse(localStorage.getItem('tilla-manual-'+zi) || '{}');
  if (manual[ti]) return manual[ti];
  var foizlar = JSON.parse(localStorage.getItem('tilla-foiz-'+zi) || '{}');
  var pct = foizlar[ti] !== undefined ? parseFloat(foizlar[ti]) || 0 : 0;
  return pct > 0 ? Math.round(kurs*(1+pct/100)*10)/10 : '';
}

function _qarzJamiRows(qarz_tarkib){
  var ost=0, biz=0;
  (qarz_tarkib||[]).forEach(function(b){
    if(b.qarz>0) ost+=b.qarz; else biz+=-b.qarz;
  });
  return {ostatka:Math.round(ost*100)/100, bizQarz:Math.round(biz*100)/100};
}

function _qarzTarkibRows(k) {
  var qbd={};
  var naqtTolov=0; // zavod/tur siz to'lovlar yig'indisi
  k.tarix.forEach(function(op){
    if(op.tip==='berish'&&op.zavod&&op.tur){
      var key=op.zavod+'||'+op.tur;
      if(!qbd[key]) qbd[key]={zavod:op.zavod,tur:op.tur,qarz:0};
      qbd[key].qarz+=op.gramm;
    } else if(op.tip==='vozvrat'&&op.zavod&&op.tur){
      var key=op.zavod+'||'+op.tur;
      if(!qbd[key]) qbd[key]={zavod:op.zavod,tur:op.tur,qarz:0};
      qbd[key].qarz-=op.gramm;
    } else if(op.tip==='tolov'&&!op._kdYopish){
      if(op.zavod&&op.tur){
        var key=op.zavod+'||'+op.tur;
        if(!qbd[key]) qbd[key]={zavod:op.zavod,tur:op.tur,qarz:0};
        qbd[key].qarz-=(op.ekvivalent||0);
      } else {
        naqtTolov+=(op.ekvivalent||0);
      }
    } else if(op.tip==='tolov'&&op._kdYopish&&op.zavod&&op.tur){
      var key=op.zavod+'||'+op.tur;
      if(!qbd[key]) qbd[key]={zavod:op.zavod,tur:op.tur,qarz:0};
      qbd[key].qarz+=(op.ekvivalent||0);
    } else if(op.tip==='klientda'&&op.zavod&&op.tur){
      // v171.3: sdacha (klientda) yozuvi shu paytgacha bu yerda umuman qayta
      // ishlanmasdi — shuning uchun "Qarz tarkibi" da turi bilan KO'RINMASDI,
      // faqat yuqoridagi umumiy "bizning qarz" raqamiga jim qo'shilardi.
      // Yozuvda zavod/tur allaqachon saqlanadi (tarixda "↩ Butterfly · Oddiy"
      // deb chiqadi), endi taqsimotda ham o'sha tur ostiga tushadi.
      // Manfiyga o'tsa panel uni "↩ biz qarzdor" deb yashil ko'rsatadi.
      // Jami qarz alohida hisoblanadi (klientJamiQarz) — unga ta'sir qilmaydi.
      var key=op.zavod+'||'+op.tur;
      if(!qbd[key]) qbd[key]={zavod:op.zavod,tur:op.tur,qarz:0};
      qbd[key].qarz-=op.gramm;
    }
  });
  // naqtTolov ni turlar bo'yicha proportsional ayirish
  if(naqtTolov>0){
    var jamiPos=Object.values(qbd).reduce(function(a,b){return a+(b.qarz>0?b.qarz:0);},0);
    if(jamiPos>0.001){
      var qoldi=naqtTolov;
      var keys=Object.keys(qbd).filter(function(k){return qbd[k].qarz>0;});
      keys.forEach(function(key,i){
        if(i===keys.length-1){
          qbd[key].qarz=Math.max(0,Math.round((qbd[key].qarz-qoldi)*100)/100);
        } else {
          var pay=Math.round(naqtTolov*(qbd[key].qarz/jamiPos)*100)/100;
          pay=Math.min(pay,qbd[key].qarz);
          qbd[key].qarz=Math.max(0,Math.round((qbd[key].qarz-pay)*100)/100);
          qoldi=Math.round((qoldi-pay)*100)/100;
        }
      });
    }
  }
  var qarz_tarkib=[];
  Object.values(qbd).forEach(function(b){
    if(Math.abs(b.qarz)>0.01) qarz_tarkib.push(b);
  });
  qarz_tarkib.sort(function(a,b){ return Math.abs(b.qarz)-Math.abs(a.qarz); });
  return qarz_tarkib;
}

function _qarzTarkib(ki) {
  var k=data.klientlar[ki];
  return {k:k, qarz_tarkib:_qarzTarkibRows(k), jamiQarz:klientJamiQarz(k)};
}

// ═════════════════════════════════════════════════════════════════
// v188.32: quyidagi uchta funksiya index.html dan SHU YERGA ko'chdi.
// Sabab (Ibrohim): «POS sistemada muddati o'tganlani ko'rsatadigan qisen
// bo'larkan» — klientQarzHolat faqat index.html da edi, pos.html uni
// ko'rmasdi. hisob.js ni IKKALASI ham yuklaydi, shuning uchun nusxa
// qolmaydi va raqam ajralmaydi.
// ⚠ MANTIQ O'ZGARMADI — bir belgi ham tegilmagan, faqat joyi almashdi.
// ═════════════════════════════════════════════════════════════════

// v183 (Ibrohim): «tilla erp 24h sistemada ishlasin ... AM da bo'lgan ishlar
// PM bilan aralashib ketvotti, keyingi bo'lgan ish oldinga o'tib qolyapti».
// Sabab: new Date('2026-09-12T6:06') — Invalid Date. Nolsiz yoki AM/PM li
// BITTA soat NaN qaytarib, saralagichni tasodifiy qilib yuborardi.
// Endi har qanday shakl qat'iy 24h HH:MM ga keltiriladi.
function _soat24(s){
  if(s===undefined || s===null) return '00:00';
  s = String(s).trim();
  if(!s) return '00:00';
  var pm = /p\.?\s*m\.?$/i.test(s), am = /a\.?\s*m\.?$/i.test(s);
  var m = s.match(/(\d{1,2})\s*[:.]\s*(\d{1,2})/);
  if(!m) return '00:00';
  var h = parseInt(m[1],10), mi = parseInt(m[2],10);
  if(isNaN(h) || isNaN(mi)) return '00:00';
  if(pm && h < 12) h += 12;
  if(am && h === 12) h = 0;
  if(h > 23) h = 23;
  if(mi > 59) mi = 59;
  return String(h).padStart(2,'0')+':'+String(mi).padStart(2,'0');
}

function fdSanaTs(sana, soat){
  if(!sana) return 0;
  var p=sana.split('.'); if(p.length!==3) return 0;
  var t=new Date(p[2]+'-'+p[1]+'-'+p[0]+'T'+_soat24(soat)).getTime();
  return isNaN(t) ? 0 : t;
}

// v187.1 (Ibrohim): «shunchaki oxirgi oldi-berdi bo'gandan keyin yoki to'lov
// bo'gandan keyin hisoblashi kerak muddati o'tishini» → «B ni qil».
// Mockup: mockups/qarz-kun.html — B varianti tanlandi.
//
// AVVAL: sanagich faqat VOZVRAT va TO'LOV dan boshlanardi. Bugun berish
//   qilingan klientda ham eski nishon turib qolardi (Mirshohid Aka 23:
//   bugun 13.09 da berish bo'lgan, nishon esa «25 kun» — 19.08 dagi
//   to'lovdan sanardi).
// ENDI: har qanday oldi-berdi tiklaydi — berish, vozvrat, tolov.
//
// ⚠ ESKI XATO: sana MATN bo'lib solishtirilardi —
//   '19.08.2026' > '13.09.2026' JavaScriptda ROST ('1'='1', keyin '9'>'3'),
//   ya'ni avgust sentabrdan keyin deb qaralardi. Bir nechta amal bo'lganda
//   noto'g'ri sana tanlanardi. Endi fdSanaTs bilan haqiqiy vaqtga
//   aylantiriladi.
//
// ⚠ inventar yozuvlari (boshlang'ich ostatka shakllantirish, tekshiruv)
//   HISOBGA OLINMAYDI — ular klient bilan bo'lgan oldi-berdi emas, o'z
//   sanog'imiz. Aks holda ostatka shakllantirish hamma klientning
//   muddatini nolga tushirib yuborardi.
//
// Ranglar TEGILMADI: 0-3 yashil, 4-7 sariq, 8+ qizil — Ibrohim aytgan
// qoida allaqachon shunday edi.
function klientQarzHolat(k) {
  var eng=0, invEng=0;
  (k.tarix||[]).forEach(function(op){
    if(!op) return;
    if(op.tip!=='berish' && op.tip!=='vozvrat' && op.tip!=='tolov') return;
    var ts=fdSanaTs(op.sana);          // soatsiz — kun boshiga tenglashtiriladi
    if(op.inventar){ if(ts>invEng) invEng=ts; return; }
    if(ts>eng) eng=ts;
  });
  // v188.2 (Ibrohim): «nega ostatkadan qo'shilgan lekin oldi-berdi bo'maganni
  // muddatini o'tgan qilib ko'rsatmayapsan» — Humayra 23 da yagona yozuv
  // 03.08.2026 dagi boshlang'ich ostatka edi, nishon esa «0 kun» chiqardi.
  // v187.1 qoidasi SAQLANADI: haqiqiy oldi-berdi bo'lsa, ostatka shakllantirish
  // sanagichni tiklamaydi. Lekin boshqa hech nima bo'lmasa — sanagich
  // o'sha yozuvdan boshlanadi, aks holda qarzdor «0 kun» bo'lib turadi.
  if(!eng) eng=invEng;
  if(!eng) return {kun:0, rang:'green'};
  var n=new Date();
  var bugun=new Date(n.getFullYear(), n.getMonth(), n.getDate()).getTime();
  var kun=Math.round((bugun-eng)/86400000);
  return {kun:kun, rang:kun<=3?'green':kun<=7?'yellow':'red'};
}
