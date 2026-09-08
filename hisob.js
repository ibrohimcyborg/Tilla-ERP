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
