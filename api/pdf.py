from http.server import BaseHTTPRequestHandler
import json, io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime

def _num(v, d=0):
    """v179.6: JSON da NaN `null` bo'lib keladi. `.get(k, 0)` esa faqat kalit
    YO'Q bo'lganda standart qiymat beradi — kalit bor-u qiymati null bo'lsa
    None qaytadi, keyin solishtirish yoki abs() TypeError berib 500 ga olib borardi."""
    if v is None:
        return d
    try:
        f = float(v)
    except (TypeError, ValueError):
        return d
    return d if f != f else f          # NaN ham d


def parse_d(s):
    try: return datetime.strptime(s, "%d.%m.%Y")
    except: return datetime.min

def in_davr(sana, dan, gacha):
    if not dan and not gacha: return True
    d = parse_d(sana)
    if dan and d < datetime.strptime(dan, "%Y-%m-%d"): return False
    if gacha and d > datetime.strptime(gacha, "%Y-%m-%d"): return False
    return True

def davr_label(dan, gacha):
    if dan and gacha:
        d1 = ".".join(reversed(dan.split("-")))
        d2 = ".".join(reversed(gacha.split("-")))
        return d1 + " — " + d2
    return "Hammasi"

C_DARK    = colors.HexColor('#111111')
C_HDR     = colors.HexColor('#1a1a1a')
C_GOLD    = colors.HexColor('#b8860b')
C_GREEN   = colors.HexColor('#2e7d32')
C_RED     = colors.HexColor('#c62828')
C_WHITE   = colors.white
C_GRAY    = colors.HexColor('#F7F7F7')
C_BLUE    = colors.HexColor('#1565c0')
C_ORANGE  = colors.HexColor('#C05621')
C_MUTED   = colors.HexColor('#718096')
C_AMBER   = colors.HexColor('#b8860b')
C_PURPLE  = colors.HexColor('#6b46c1')   # v174.5: offset (ilovadagi "⇄ Offset" rangi)

def P(text, font='Helvetica', size=10, color=colors.black, align='LEFT'):
    a = {'LEFT': TA_LEFT, 'CENTER': TA_CENTER, 'RIGHT': TA_RIGHT}
    s = ParagraphStyle('p', fontName=font, fontSize=size,
        textColor=color, alignment=a.get(align, TA_LEFT), leading=size + 3)
    return Paragraph(str(text) if text is not None else '', s)

def title_p(text):
    s = ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=13,
        textColor=C_DARK, alignment=TA_CENTER, spaceAfter=3)
    return Paragraph(text, s)

def sub_p(text):
    s = ParagraphStyle('s', fontName='Helvetica', fontSize=8,
        textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=5)
    return Paragraph(text, s)

def base_style():
    return [
        ('BACKGROUND',   (0, 0), (-1,  0), C_HDR),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID',         (0, 0), (-1, -1), 0.4, colors.HexColor('#dddddd')),
        ('ROWHEIGHT',    (0, 0), ( 0,  0), 22),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        ('LEFTPADDING',  (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]

# ═══════════════════════════════════════════════════════════════
# KURS TARIXI PDF — A4 portrait
# ═══════════════════════════════════════════════════════════════
def build_kurs_tarix(sarlavha, davr, sana, kunlar):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm, topMargin=12*mm, bottomMargin=12*mm)
    story = []
    W_total = A4[0] - 30*mm

    story.append(title_p(sarlavha))
    story.append(sub_p("Davr: " + davr))
    story.append(sub_p("Chiqarildi: " + sana))
    story.append(Spacer(1, 6*mm))

    for kun in kunlar:
        # Kun sarlavhasi
        hdr_tbl = Table([[
            P(kun['sana'], 'Helvetica-Bold', 11, C_DARK),
            P(kun['soat'] + " da kiritilgan", 'Helvetica', 8, C_MUTED, 'RIGHT'),
            P(str(kun['kurs']) + " $/g", 'Helvetica-Bold', 11, C_GOLD, 'RIGHT'),
        ]], colWidths=[W_total*0.35, W_total*0.35, W_total*0.30])
        hdr_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8F4E8')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0,0), (-1,-1), 1, C_GOLD),
        ]))
        story.append(hdr_tbl)

        # Turlar jadvali
        turlar = kun.get('turlar', [])
        if turlar:
            tdata = [[
                P("Zavod", 'Helvetica-Bold', 8, C_WHITE, 'LEFT'),
                P("Tur", 'Helvetica-Bold', 8, C_WHITE, 'LEFT'),
                P("Narx", 'Helvetica-Bold', 8, C_WHITE, 'RIGHT'),
            ]]
            rstyles = [
                ('BACKGROUND', (0,0), (-1,0), C_HDR),
            ]
            cur_zavod = ''
            for ri, t in enumerate(turlar, 1):
                zavod = t.get('zavod','')
                tur = t.get('tur','')
                narx = t.get('narx', 0)
                bg = C_GRAY if ri % 2 == 0 else C_WHITE
                tdata.append([
                    P(zavod if zavod != cur_zavod else '', 'Helvetica-Bold' if zavod != cur_zavod else 'Helvetica', 9, C_AMBER if zavod != cur_zavod else C_MUTED),
                    P('  ' + tur, size=9, color=C_DARK),
                    P(str(narx) + " $", 'Helvetica-Bold', 9, C_GREEN, 'RIGHT'),
                ])
                rstyles.append(('BACKGROUND', (0,ri), (-1,ri), bg))
                cur_zavod = zavod

            t_tbl = Table(tdata, colWidths=[W_total*0.35, W_total*0.40, W_total*0.25])
            t_tbl.setStyle(TableStyle(base_style() + rstyles))
            story.append(t_tbl)

        story.append(Spacer(1, 5*mm))

    story.append(sub_p(f"Jami: {len(kunlar)} ta kurs yozuvi"))

    doc.build(story)
    return buf.getvalue()


def build_pdf(zavodlar, filter_zavod, dan, gacha, label):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
        leftMargin=8*mm, rightMargin=8*mm, topMargin=8*mm, bottomMargin=8*mm)
    story = []
    HDR = ["Sana","Zavod","Tur","+/-","Kimga","Kirim(g)","Naqt($)","Kurs","Naqt→g","Lom(g)","Lom($)","Chiqim(g)","Ostatka(g)"]
    CW  = [x*mm for x in [24, 26, 16, 9, 26, 22, 24, 16, 20, 20, 24, 22, 24]]
    hdr_row = [P(h, 'Helvetica-Bold', 9, C_WHITE, 'CENTER') for h in HDR]
    all_rows = []
    for z in zavodlar:
        if filter_zavod and z["nom"] != filter_zavod: continue
        for t in z.get("turlar", []):
            bal = 0.0
            for op in t.get("tarix", []):
                if op["tip"] == "mol":      bal += _num(op.get("gramm"))          # v179.7
                elif op["tip"] == "vozvrat": bal  = max(0, bal - _num(op.get("gramm")))  # v179.7
                else:                        bal  = max(0, bal - _num(op.get("jami")))   # v179.7
                if not in_davr(op["sana"], dan, gacha): continue
                all_rows.append({"sana": op["sana"], "zavod": z["nom"], "tur": t["nom"],
                    "tip": op["tip"], "op": op, "ostatka": round(bal, 2)})
    all_rows.sort(key=lambda r: parse_d(r["sana"]))
    tdata = [hdr_row]; rstyles = []
    for ri, row in enumerate(all_rows, 1):
        op = row["op"]; is_k = row["tip"] == "mol"; is_v = row["tip"] == "vozvrat"
        def cell(v, bold=False, color=colors.HexColor('#212121'), align='LEFT'):
            return P(v, 'Helvetica-Bold' if bold else 'Helvetica', 9, color, align)
        trow = [
            cell(row["sana"]), cell(row["zavod"]), cell(row["tur"]),
            P("↓" if is_k else ("↩" if is_v else "↑"), 'Helvetica-Bold', 11,
              C_GREEN if is_k else (C_BLUE if is_v else C_RED), 'CENTER'),
            cell("" if is_k else (op.get("kimga") or "")),
            cell(f"+{_num(op.get('gramm')):,.2f}" if is_k else (f"-{_num(op.get('gramm')):,.2f}" if is_v else ""),   # v179.7
                 bold=True, color=C_GREEN if is_k else C_BLUE, align='RIGHT'),
            cell(f"{_num(op.get('naqtSumma')):,.0f}" if not is_k else "", align='RIGHT'),   # v179.7
            cell(str(op.get("naqtKurs","")) if not is_k else "", align='RIGHT'),
            cell(f"{_num(op.get('naqtGramm')):,.2f}" if not is_k else "", align='RIGHT'),   # v179.7
            cell(f"{_num(op.get('lomGramm')):,.2f}" if not is_k else "", align='RIGHT'),          # v179.7
            cell(f"{_num(op.get('lomPul')):,.0f}" if not is_k else "", align='RIGHT'),             # v179.7
            cell(f"{_num(op.get('jami')):,.2f}" if not is_k else "", bold=True, color=C_RED, align='RIGHT'),   # v179.7
            P(f"{_num(row['ostatka']):,.2f}", 'Helvetica-Bold', 9, C_AMBER, 'RIGHT'),              # v179.7
        ]
        tdata.append(trow)
        rstyles.append(('BACKGROUND', (0, ri), (-1, ri), C_WHITE if ri % 2 else C_GRAY))
    tK = round(sum(_num(r["op"].get("gramm")) for r in all_rows if r["tip"] == "mol"), 2)        # v179.7
    tC = round(sum(_num(r["op"].get("jami")) for r in all_rows if r["tip"] == "tolov"), 2)         # v179.7
    tN = round(sum(_num(r["op"].get("naqtSumma")) for r in all_rows if r["tip"] == "tolov"), 2)    # v179.7
    tL = round(sum(_num(r["op"].get("lomPul")) for r in all_rows if r["tip"] == "tolov"), 2)       # v179.7
    fin = {}
    for r in all_rows: fin[r["zavod"] + "|" + r["tur"]] = r["ostatka"]
    tO = round(sum(fin.values()), 2)
    jr = len(tdata)
    tdata.append([
        P('JAMI', 'Helvetica-Bold', 9, C_WHITE, 'CENTER'), '', '', '', '',
        P(f'+{tK:,.2f}g', 'Helvetica-Bold', 9, colors.HexColor('#68D391'), 'RIGHT'),
        P(f'Naqt: {tN:,.0f}$', 'Helvetica-Bold', 9, colors.HexColor('#F6E05E'), 'RIGHT'),
        '', '', '', P(f'Lom: {tL:,.0f}$', 'Helvetica-Bold', 9, colors.HexColor('#F6E05E'), 'RIGHT'),
        P(f'-{tC:,.2f}g', 'Helvetica-Bold', 9, colors.HexColor('#FC8181'), 'RIGHT'),
        P(f'{tO:,.2f}g', 'Helvetica-Bold', 10, colors.HexColor('#F6E05E'), 'RIGHT'),
    ])
    rstyles += [('BACKGROUND', (0, jr), (-1, jr), C_DARK), ('SPAN', (0, jr), (4, jr))]
    t1 = Table(tdata, colWidths=CW, repeatRows=1)
    t1.setStyle(TableStyle(base_style() + rstyles))
    story.append(title_p("TILLA HISOB — Kirdi-Chiqdi" + (" — " + filter_zavod if filter_zavod else " (Barcha)")))
    story.append(sub_p("Davr: " + label)); story.append(t1); story.append(Spacer(1, 8*mm))
    H2 = ["Zavod", "Tur", "Kirim(g)", "Chiqim(g)", "Ostatka(g)", "Naqt($)", "Lom($)", "Jami($)"]
    H2CW = [x*mm for x in [35, 25, 30, 30, 30, 36, 36, 36]]
    h2data = [[P(h, 'Helvetica-Bold', 9, C_WHITE, 'CENTER') for h in H2]]; h2styles = []
    gK = gC = gO = gN = gL = 0; ri2 = 1
    for z in zavodlar:
        if filter_zavod and z["nom"] != filter_zavod: continue
        for t in z.get("turlar", []):
            tk = tc = tn = tl = bal = 0
            for op in t.get("tarix", []):
                if op["tip"] == "mol":      bal += _num(op.get("gramm"))            # v179.7
                elif op["tip"] == "vozvrat": bal = max(0, bal - _num(op.get("gramm")))   # v179.7
                else:                        bal = max(0, bal - _num(op.get("jami")))    # v179.7
                if not in_davr(op["sana"], dan, gacha): continue
                if op["tip"] == "mol": tk += _num(op.get("gramm"))                       # v179.7
                else: tc += _num(op.get("jami")); tn += _num(op.get("naqtSumma")); tl += _num(op.get("lomPul"))   # v179.7
            o = round(bal, 2); bg = C_GRAY if ri2 % 2 == 0 else C_WHITE
            h2data.append([P(z["nom"], size=9), P(t["nom"], size=9),
                P(f'{tk:,.2f}', 'Helvetica-Bold', 9, C_GREEN, 'RIGHT'),
                P(f'{tc:,.2f}', 'Helvetica-Bold', 9, C_RED, 'RIGHT'),
                P(f'{o:,.2f}', 'Helvetica-Bold', 10, C_GOLD, 'RIGHT'),
                P(f'{tn:,.2f}', size=9, color=C_ORANGE, align='RIGHT'),
                P(f'{tl:,.2f}', size=9, color=C_ORANGE, align='RIGHT'),
                P(f'{(tn+tl):,.2f}', size=9, color=C_ORANGE, align='RIGHT')])
            h2styles.append(('BACKGROUND', (0, ri2), (-1, ri2), bg))
            gK += tk; gC += tc; gO += o; gN += tn; gL += tl; ri2 += 1
    jr2 = len(h2data)
    h2data.append([P('JAMI', 'Helvetica-Bold', 9, C_WHITE, 'CENTER'), '',
        P(f'{gK:,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#68D391'), 'RIGHT'),
        P(f'{gC:,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#FC8181'), 'RIGHT'),
        P(f'{gO:,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#F6E05E'), 'RIGHT'),
        P(f'{gN:,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#FBD38D'), 'RIGHT'),
        P(f'{gL:,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#FBD38D'), 'RIGHT'),
        P(f'{(gN+gL):,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#FBD38D'), 'RIGHT')])
    h2styles += [('BACKGROUND', (0, jr2), (-1, jr2), C_DARK), ('SPAN', (0, jr2), (1, jr2))]
    ht = Table(h2data, colWidths=H2CW, repeatRows=1)
    ht.setStyle(TableStyle(base_style() + h2styles))
    story.append(title_p("HISOBOT — Tur bo'yicha kirdi-chiqdi"))
    story.append(sub_p("Davr: " + label)); story.append(ht)
    doc.build(story); return buf.getvalue()


def build_klient_chek(klient_nom, ops_grouped, sana, qarz_tarkib=None):
    buf = io.BytesIO(); W = 72*mm
    est_h = 35 + len(ops_grouped)*28 + (len(qarz_tarkib)*6 if qarz_tarkib else 0) + 18
    def CP(text, font='Helvetica', size=8, color=colors.black, align='CENTER'):
        a = {'LEFT': TA_LEFT, 'CENTER': TA_CENTER, 'RIGHT': TA_RIGHT}
        s = ParagraphStyle('cp', fontName=font, fontSize=size, textColor=color, alignment=a.get(align, TA_CENTER), leading=size+2)
        return Paragraph(str(text) if text else '', s)
    def row(a, b, fa='Helvetica', fb='Helvetica', sa=8, sb=8, ca=C_MUTED, cb=colors.black):
        return Table([[CP(a,fa,sa,ca,'LEFT'), CP(b,fb,sb,cb,'RIGHT')]], colWidths=[W*0.55-3*mm, W*0.45-3*mm],
            style=[('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)])
    def dline():
        return Table([['']], colWidths=[W-6*mm], style=[('LINEBELOW',(0,0),(-1,-1),0.5,C_MUTED),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),2)])
    story = []
    story.append(CP('TILLA HISOB', 'Helvetica-Bold', 11, C_GOLD))
    story.append(CP('TOLOV CHEKI', size=8, color=C_MUTED))
    story.append(Spacer(1, 2*mm)); story.append(dline()); story.append(Spacer(1, 1*mm))
    story.append(row('Klient:', klient_nom, fb='Helvetica-Bold', cb=C_DARK))
    story.append(row('Sana:', sana, cb=C_DARK))
    story.append(Spacer(1, 1*mm)); story.append(dline()); story.append(Spacer(1, 1*mm))
    total_pul = total_tolov_g = total_vozvrat_g = total_qolgan = 0
    for item in ops_grouped:
        tur_nom = (item.get('zavod','') + ' · ' + item.get('tur','')) if item.get('tur') else item.get('zavod','')
        avvalgi=item.get('avvalgi_qarz',0); tolov_g=item.get('tolov_g',0)
        vozvrat_g=item.get('vozvrat_g',0); tolov_summa=item.get('tolov_summa',0)
        tolov_kurs=item.get('tolov_kurs',0); qolgan=max(0,avvalgi-tolov_g-vozvrat_g)
        story.append(CP(tur_nom,'Helvetica-Bold',8,C_DARK,'LEFT'))
        if avvalgi>0: story.append(row('  Qarz:',f'-{avvalgi:.2f}g',cb=C_RED))
        if tolov_g>0 and tolov_summa>0:
            story.append(row(f'  Tolov: {tolov_summa:,.0f}$/{tolov_kurs:.1f}$/g',f'+{tolov_g:.2f}g',cb=C_GREEN))
        elif tolov_g>0: story.append(row('  Tolov:',f'+{tolov_g:.2f}g',cb=C_GREEN))
        if vozvrat_g>0: story.append(row('  Vozvrat:',f'+{vozvrat_g:.2f}g',cb=C_GREEN))
        story.append(row('  Qoldi:',f'-{qolgan:.2f}g',fb='Helvetica-Bold',cb=C_GOLD))
        story.append(Spacer(1,1*mm))
        total_pul+=tolov_summa; total_tolov_g+=tolov_g; total_vozvrat_g+=vozvrat_g; total_qolgan+=qolgan
    story.append(dline()); story.append(Spacer(1,1*mm))
    if qarz_tarkib:
        story.append(CP('QARZ TARKIBI','Helvetica-Bold',7,C_MUTED,'CENTER'))
        story.append(Spacer(1,1*mm))
        for item in qarz_tarkib:
            nom=(item.get('zavod','')+' · '+item.get('tur','')); qarz=_num(item.get('qarz'))   # v179.7
            if qarz>0: story.append(row(nom,f'-{qarz:.2f}g',cb=C_RED))
        story.append(dline()); story.append(Spacer(1,1*mm))
    if total_pul>0: story.append(row('Jami pul:',f'{total_pul:,.0f}$',fb='Helvetica-Bold',cb=C_BLUE))
    story.append(row('Jami tolov:',f'+{total_tolov_g:.2f}g',fb='Helvetica-Bold',cb=C_GREEN))
    if total_vozvrat_g>0: story.append(row('Jami vozvrat:',f'+{total_vozvrat_g:.2f}g',fb='Helvetica-Bold',cb=C_GREEN))
    story.append(row('Umumiy qolgan:',f'-{total_qolgan:.2f}g',fb='Helvetica-Bold',cb=C_RED))
    story.append(Spacer(1,2*mm)); story.append(dline())
    story.append(CP('— Rahmat —',size=7,color=C_MUTED))
    doc = SimpleDocTemplate(buf, pagesize=(W, est_h*mm), leftMargin=3*mm, rightMargin=3*mm, topMargin=4*mm, bottomMargin=4*mm)
    doc.build(story); buf.seek(0); return buf.read()


def build_klient_qarz_chek(klient_nom, sana, jami_qarz, qarz_tarkib, biz_qarz=0):
    jami_qarz = _num(jami_qarz); biz_qarz = _num(biz_qarz)   # v179.7
    buf = io.BytesIO(); W = 72*mm; est_h = 50 + len(qarz_tarkib)*15 + 38
    def CP(text, font='Helvetica', size=8, color=colors.black, align='CENTER'):
        a = {'LEFT': TA_LEFT, 'CENTER': TA_CENTER, 'RIGHT': TA_RIGHT}
        s = ParagraphStyle('cp', fontName=font, fontSize=size, textColor=color, alignment=a.get(align, TA_CENTER), leading=size+2)
        return Paragraph(str(text) if text else '', s)
    def row2(a, b, fa='Helvetica', fb='Helvetica', sa=8, sb=8, ca=C_MUTED, cb=colors.black):
        return Table([[CP(a,fa,sa,ca,'LEFT'), CP(b,fb,sb,cb,'RIGHT')]], colWidths=[W*0.55-3*mm, W*0.45-3*mm],
            style=[('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)])
    def dline2():
        return Table([['']], colWidths=[W-6*mm], style=[('LINEBELOW',(0,0),(-1,-1),0.5,C_MUTED),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),2)])
    story = []
    story.append(CP('TILLA HISOB', 'Helvetica-Bold', 11, C_GOLD))
    story.append(CP('QARZ HOLATI', size=8, color=C_MUTED))
    story.append(Spacer(1, 2*mm)); story.append(dline2())
    story.append(row2('Klient:', klient_nom, fb='Helvetica-Bold', cb=C_DARK))
    story.append(row2('Sana:', sana, cb=C_DARK))
    story.append(Spacer(1, 1*mm)); story.append(dline2()); story.append(Spacer(1, 1*mm))
    by_zavod = {}
    for item in qarz_tarkib:
        z = item.get('zavod', '')
        if z not in by_zavod: by_zavod[z] = []
        by_zavod[z].append(item)
    # v172.12: biz qarzdor bo'lgan turlar avval BUTUNLAY tashlab yuborilardi
    # (qarz < 0.01 -> continue). Endi ular "(biz qarz)" bo'lib ko'rinadi.
    # v175.1 (Ibrohim): zavod ostidagi "Jami:" qatori OLIB TASHLANDI. Uni
    # hisoblagan z_total ham keraksiz qoldi. Pastdagi "KLIENT OSTATKASI"
    # boshqa manbadan keladi (jami_qarz) - unga TEGILMADI.
    for znom, turs in by_zavod.items():
        story.append(CP(znom, 'Helvetica-Bold', 9, C_GOLD, 'LEFT'))
        for t in turs:
            q = _num(t.get('qarz'))   # v179.7
            if q > 0.01:
                story.append(row2('  ' + t.get('tur',''), f"-{q:.2f}g", cb=C_RED))
            elif q < -0.01:
                story.append(row2('  ' + t.get('tur','') + ' (biz qarz)', f"+{abs(q):.2f}g", cb=C_GREEN))
        story.append(Spacer(1, 1*mm))
    story.append(dline2()); story.append(Spacer(1, 1*mm))
    # v172.12: "UMUMIY QARZ" o'rniga ikkita qator — klient ostatkasi va bizning
    # qarz alohida. Sof qoldiq YOZILMAYDI. Bizning qarz 0 bo'lsa chiqmaydi.
    story.append(Table([[CP('KLIENT OSTATKASI:', 'Helvetica-Bold', 10, C_RED, 'LEFT'),
        CP(f'-{abs(jami_qarz):.2f}g', 'Helvetica-Bold', 12, C_RED, 'RIGHT')]],
        colWidths=[W*0.55-3*mm, W*0.45-3*mm],
        style=[('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FFF0F0')),
               ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    if abs(biz_qarz) > 0.001:
        story.append(Table([[CP('BIZNING QARZ:', 'Helvetica-Bold', 10, C_GREEN, 'LEFT'),
            CP(f'+{abs(biz_qarz):.2f}g', 'Helvetica-Bold', 12, C_GREEN, 'RIGHT')]],
            colWidths=[W*0.55-3*mm, W*0.45-3*mm],
            style=[('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F0FFF4')),
                   ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    story.append(Spacer(1, 2*mm)); story.append(dline2())
    story.append(CP('— Tilla Hisob —', size=7, color=C_MUTED))
    doc = SimpleDocTemplate(buf, pagesize=(W, est_h*mm), leftMargin=3*mm, rightMargin=3*mm, topMargin=4*mm, bottomMargin=4*mm)
    doc.build(story); buf.seek(0); return buf.read()


def _ost_blok(b, kw):
    """v172.39: bitta zavod·tur bloki. Ibrohim so'ragan ko'rinish:
    nom (o'rtada) -> boshlang'ich qoldiq -> kunlik amallar (sana+gramm+amal) ->
    har kun oxiridagi qoldiq -> QOLDI. Qora fon YO'Q (Ibrohim: "yoqmadi")."""
    W = [kw * 0.30, kw * 0.36, kw * 0.34]
    # v179.11: blok bo'laklarga bo'lingan bo'lsa, davomida sarlavha belgilanadi.
    _nom = f"{b.get('zavod','')} · {b.get('tur','')}" + (' (davomi)' if b.get('_davomi') else '')
    d = [[P(_nom, 'Helvetica-Bold', 7.5, C_DARK, 'CENTER'), '', '']]
    st = [('SPAN', (0, 0), (2, 0)),
          ('BACKGROUND', (0, 0), (2, 0), colors.HexColor('#FBF3E0')),
          ('LINEBELOW', (0, 0), (2, 0), 0.9, C_GOLD)]
    # v172.43: boshi 0.00 bo'lsa qator CHIZILMAYDI (Ibrohim: "boshi 0 digan narsa yo'q,
    # boshida ostatka qo'shiladi shu bilan davom etadi"). 0 dan boshqa bo'lsa QOLADI —
    # aks holda `boshi + amallar = QOLDI` arifmetikasi ko'rinmay qoladi.
    r = 1
    _b = '' if b.get('_davomi') else str(b.get('boshi', '') or '')   # v179.11: davomida takrorlanmaydi
    if _b.replace('g', '').strip() not in ('0.00', '-0.00', '0', ''):
        d.append([P('boshi', 'Helvetica-Oblique', 6.5, C_MUTED), '',
                  P(_b, 'Helvetica-Bold', 7, C_DARK, 'RIGHT')])
        st.append(('SPAN', (0, r), (1, r)))
        st.append(('BACKGROUND', (0, r), (2, r), colors.HexColor('#F4F4F4')))
        r += 1
    for kun in (b.get('kunlar') or []):
        amal = kun.get('amallar') or []
        for i, a in enumerate(amal):
            nom = a.get('amal', '')
            # v172.41: 'ostatka' — shakllantirish yozuvi, oltin rangda (berildi/
            # vozvrat/tolov dan ajralib tursin, u klientga berilgan tilla emas)
            # v174.5: offset — bizning qarzimiz yopilishi, to'lovdan ajralib tursin.
            c = (C_RED if nom == 'berildi' else
                 C_BLUE if nom == 'vozvrat' else
                 C_GREEN if nom == 'tolov' else
                 C_PURPLE if nom == 'offset' else C_GOLD)
            # v174.5: 'ok' — offset o'qi (-> manzil / <- manba), index.html da quriladi.
            _ok = a.get('ok') or ''
            d.append([P(kun.get('sana', '') if i == 0 else '', 'Helvetica', 6.5, C_MUTED),
                      P(str(a.get('g', '')), 'Helvetica-Bold', 7, c, 'RIGHT'),
                      P(' ' + nom + ((' ' + _ok) if _ok else ''), 'Helvetica', 6.5, C_MUTED)])
            r += 1
        d.append(['', '', P(str(kun.get('qoldi', '')), 'Helvetica-Bold', 7, C_DARK, 'RIGHT')])
        st.append(('LINEABOVE', (0, r), (2, r), 0.5, colors.HexColor('#999999')))
        st.append(('BACKGROUND', (0, r), (2, r), colors.HexColor('#FFFDF6')))
        r += 1
    # v172.40: qoldiq rangi — klient qarzdor bo'lsa QIZIL, biz qarzdor bo'lsak
    # "+" bilan YASHIL (belgi index.html da qo'yiladi), nol bo'lsa oddiy qora.
    if not b.get('_qoldi_yoq'):          # v179.11: QOLDI faqat OXIRGI bo'lakda
        _h = b.get('holat', 'nol')
        _oc = C_RED if _h == 'qarz' else (C_GREEN if _h == 'bizda' else C_DARK)
        d.append([P('QOLDI', 'Helvetica-Bold', 7, colors.HexColor('#5c4708')), '',
                  P(str(b.get('oxiri', '')), 'Helvetica-Bold', 7.5, _oc, 'RIGHT')])
        st += [('SPAN', (0, r), (1, r)),
               ('BACKGROUND', (0, r), (2, r), colors.HexColor('#FBF3E0')),
               ('LINEABOVE', (0, r), (2, r), 0.9, C_GOLD)]
    st += [('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
           ('TOPPADDING', (0, 0), (-1, -1), 1.4), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.4),
           ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3),
           ('VALIGN', (0, 0), (-1, -1), 'TOP')]
    t = Table(d, colWidths=W)
    t.setStyle(TableStyle(st))
    return t


# v179.11 (Ibrohim: eng katta klientda PDF 500 berardi).
# XATO MATNI: "Flowable <Table 1 rows x 5 cols(tallest row 724)> ... 'Butterfly · Oddiy'
# (762 x 724.9), tallest cell 724.9 points, too large on page 9 in frame 'normal'
# (784 x 537.9)".
# SABAB: ostatka bloklari 5 ustunli BITTA QATORLI jadvalga joylanadi, unday qator
# sahifaga BO'LINA OLMAYDI. Bir zavod·turda kun ko'p bo'lsa blok 724.9 nuqta
# bo'lib ketdi, ramkada esa 537.9 nuqta joy bor — reportlab to'xtadi.
# YECHIM: uzun blok kunlar bo'yicha bo'laklarga bo'linadi. Ma'lumot yo'qolmaydi:
# «boshi» faqat birinchi bo'lakda, «QOLDI» faqat oxirgisida, oraliq bo'laklar
# sarlavhasida «(davomi)» turadi.
_OST_MAX_QATOR = 28          # bitta blokdagi maksimal kun-qatori (~28 x 12.8 nuqta)


def _ost_bolaklar(b, kw):
    kunlar = b.get('kunlar') or []
    if not kunlar:
        return [_ost_blok(b, kw)]
    guruh, joriy, sanoq = [], [], 0
    for kun in kunlar:
        n = len(kun.get('amallar') or []) + 1      # amal qatorlari + kun qoldig'i
        if joriy and sanoq + n > _OST_MAX_QATOR:
            guruh.append(joriy); joriy = []; sanoq = 0
        joriy.append(kun); sanoq += n
    if joriy:
        guruh.append(joriy)
    if len(guruh) < 2:
        return [_ost_blok(b, kw)]
    out = []
    for gi, g in enumerate(guruh):
        bb = dict(b)
        bb['kunlar'] = g
        if gi:
            bb['_davomi'] = True                   # boshi yo'q, sarlavhada (davomi)
        if gi < len(guruh) - 1:
            bb['_qoldi_yoq'] = True                # QOLDI faqat oxirgisida
        out.append(_ost_blok(bb, kw))
    return out


def build_klient_tarix(klient_nom, klient_tel, ops, dan, gacha,
                        jami_berildi, jami_vozvrat, jami_tolov_g, jami_tolov_pul, qarz_tarkib,
                        ost_bloklar=None, jami_qolgan=None,
                        klient_ostatka=None, biz_qarz=0):
    jami_berildi = _num(jami_berildi); jami_vozvrat = _num(jami_vozvrat)      # v179.6
    jami_tolov_g = _num(jami_tolov_g); jami_tolov_pul = _num(jami_tolov_pul)  # v179.6
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4), leftMargin=8*mm, rightMargin=8*mm, topMargin=8*mm, bottomMargin=8*mm)
    story = []; W_total = landscape(A4)[0] - 16*mm
    tt = Table([[P("TILLA HISOB — Klient hisoboti", 'Helvetica-Bold', 13, C_DARK),
                 P(klient_nom, 'Helvetica-Bold', 12, C_DARK, 'RIGHT')],
                [P(f"Davr: {davr_label(dan, gacha)}", 'Helvetica', 8, C_MUTED),
                 P(klient_tel or '', 'Helvetica', 8, C_MUTED, 'RIGHT')]],
        colWidths=[W_total*0.6, W_total*0.4])
    tt.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('LINEBELOW',(0,1),(-1,1),0.5,colors.HexColor('#dddddd'))]))
    story.append(tt); story.append(Spacer(1, 4*mm))
    # v175: qolgan endi index.html dan keladi (qarz_tarkib qatorlarining yig'indisi,
    # ilovadagi ekran bilan bir xil manba). Eski formula offsetni ham, sdachani ham,
    # zavod/tursiz to'lovlarni ham hisobga olmasdi. Zaxira sifatida saqlanadi.
    qolgan = round(jami_qolgan, 2) if jami_qolgan is not None \
             else round(jami_berildi - jami_vozvrat - jami_tolov_g, 2)
    # Biz qarzdor bo'lsak (manfiy) "+87.56g" yashil. Avval "-" qattiq yozilgani
    # uchun "--87.56g" bo'lib chiqardi.
    qolgan_txt = f"+{abs(qolgan):,.2f}g" if qolgan < -0.001 else f"-{qolgan:,.2f}g"
    qolgan_col = C_RED if qolgan > 0.001 else (C_GREEN if qolgan < -0.001 else C_DARK)
    # v175.3 (Ibrohim, A varianti): tepadagi katak qarz cheki bilan BIR XIL bo'lsin —
    # "KLIENT OSTATKASI" va "BIZNING QARZ" alohida ustunda, aralashtirilmaydi.
    # Biz qarzdor bo'lmasak beshinchi ustun UMUMAN chizilmaydi (Ibrohim qoidasi).
    # Eski hujjatlar uchun: klient_ostatka kelmasa avvalgidek yagona "QOLGAN QARZ".
    _ost = round(klient_ostatka, 2) if klient_ostatka is not None else None
    _biz = round(biz_qarz or 0, 2)
    if _ost is None:
        sarlavha = [P("QOLGAN QARZ",'Helvetica-Bold',8,C_WHITE,'CENTER')]
        qiymat   = [P(qolgan_txt,'Helvetica-Bold',13,qolgan_col,'CENTER')]
    else:
        sarlavha = [P("KLIENT OSTATKASI",'Helvetica-Bold',8,C_WHITE,'CENTER')]
        qiymat   = [P(f"-{_ost:,.2f}g",'Helvetica-Bold',13,
                      C_RED if _ost > 0.001 else C_DARK,'CENTER')]
        if _biz > 0.001:
            sarlavha.append(P("BIZNING QARZ",'Helvetica-Bold',8,C_WHITE,'CENTER'))
            qiymat.append(P(f"+{_biz:,.2f}g",'Helvetica-Bold',13,C_GREEN,'CENTER'))
    stat_data = [[P("JAMI BERILDI",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("VOZVRAT",'Helvetica-Bold',8,C_WHITE,'CENTER'),
                  P("TOLOV (PUL)",'Helvetica-Bold',8,C_WHITE,'CENTER')] + sarlavha,
                 [P(f"-{jami_berildi:,.2f}g",'Helvetica-Bold',13,C_RED,'CENTER'),P(f"+{jami_vozvrat:,.2f}g",'Helvetica-Bold',13,C_GREEN,'CENTER'),
                  P(f"+{jami_tolov_g:,.2f}g\n{jami_tolov_pul:,.0f}$",'Helvetica-Bold',13,C_GREEN,'CENTER')] + qiymat]
    _n = len(stat_data[0])
    st = Table(stat_data, colWidths=[W_total/_n]*_n)
    st.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),C_HDR),('BACKGROUND',(0,1),(-1,1),colors.HexColor('#F8F6F0')),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#dddddd')),('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(st); story.append(Spacer(1, 5*mm))
    HDR = ["Sana","Amal","Zavod","Tur","Gramm","Summa ($)","Kurs ($/g)","Ostatka"]
    CW  = [x*mm for x in [26, 22, 30, 22, 26, 26, 24, 28]]
    # v179.9: BITTA ULKAN JADVAL O'RNIGA BO'LAKLAR.
    # Har sessiya guruhiga uchta SPAN qo'yiladi (sana / amal / ostatka ustunlari).
    # reportlab SPAN larni BUTUN jadval bo'yicha qayta hisoblaydi, shuning uchun
    # vaqt KVADRATIK o'sardi — o'lchandi: 1000 amal 6.7 s, 2000 amal 19.9 s,
    # 4000 amal 69.6 s. Vercel 10 soniyadan keyin funksiyani o'ldiradi va 500
    # qaytaradi — Ibrohim eng ko'p amali bor klientda aynan shunga tushdi.
    # 300 qatorli bo'laklarga bo'linganda o'sish CHIZIQLI bo'ladi (1600 guruh:
    # 11.9 s -> 3.0 s) va SAHIFA SONI O'ZGARMAYDI — o'lchandi, 37/73/146 sahifa
    # ikkala usulda ham bir xil. Bo'linish faqat guruh CHEGARASIDA bo'ladi,
    # shuning uchun birlashtirilgan kataklar (SPAN) hech qachon bo'linmaydi.
    _BOLAK = 300
    def _sarlavha(): return [P(h,'Helvetica-Bold',9,C_WHITE,'CENTER') for h in HDR]
    _bolaklar = []
    tdata = [_sarlavha()]; rstyles = []
    for si, row in enumerate(ops):
        tip=row.get('tip',''); ostatka=_num(row.get('ostatka'))   # v179.6
        # v172.43: shakllantirish ham tip:'berish' bo'lib yoziladi (index 6505).
        # Sessiyaning HAMMA yozuvi shakllantirish bo'lsagina 'Ostatka' deyiladi.
        # Belgi qo'yilmaydi — Helvetica da ⊟ qora kvadrat bo'lib chiqishi mumkin.
        if tip=='berish' and row.get('shakl'):
                             amal_txt='Ostatka';   ac=C_GOLD; gc=C_GOLD; gsign=''
        elif tip=='berish':  amal_txt='↑ Berildi'; ac=C_RED;  gc=C_RED;  gsign=''
        elif tip=='vozvrat': amal_txt='↩ Vozvrat'; ac=C_BLUE; gc=C_GREEN; gsign='+'
        # v174.9: guruh butunlay offsetdan yopilgan bo'lsa "Offset" (binafsha).
        # Belgi (⇄) QO'YILMAYDI — yuqoridagi ⊟ izohi bilan bir sabab: standart
        # Helvetica da qora kvadrat bo'lib chiqishi mumkin.
        elif row.get('off_ses'): amal_txt='Offset'; ac=C_PURPLE; gc=C_GREEN; gsign='+'
        else: amal_txt='$ Tolov'; ac=C_GREEN; gc=C_GREEN; gsign='+'
        oc=C_RED if ostatka<-0.001 else C_GREEN
        bg=C_GRAY if si%2 else C_WHITE
        turlar=row.get('turlar') or []
        r0=len(tdata)
        if turlar:
            for ti, t in enumerate(turlar):
                tg=_num(t.get('gramm')); tsum=_num(t.get('summa')); tk=_num(t.get('kurs'))   # v179.6
                # v174.9: offset o'qi tur ostida ikkinchi qatorda (-> manzil / <- manba).
                _tok=t.get('ok') or ''
                _tur=(t.get('tur','') + (
                    '<br/><font size="6.5" color="#6b46c1">%s</font>' % _tok if _tok else ''))
                tdata.append([
                    P(row.get('sana','') if ti==0 else '',size=9,color=C_MUTED),
                    P(amal_txt if ti==0 else '','Helvetica-Bold',9,ac,'CENTER'),
                    P(t.get('zavod',''),size=9,color=C_MUTED),
                    P(_tur,'Helvetica-Bold',9,C_DARK),
                    P(f"{gsign}{abs(tg):,.2f}g",'Helvetica-Bold',9,gc,'RIGHT'),
                    P(f"{tsum:,.0f}$" if tsum else "—",size=9,align='RIGHT'),
                    P(f"{tk:,.1f}$/g" if tk else "—",size=9,color=C_MUTED,align='RIGHT'),
                    P(f"{ostatka:,.2f}g" if ti==0 else '','Helvetica-Bold',9,oc,'RIGHT')])
        else:
            tg=_num(row.get('gramm')); tsum=_num(row.get('summa')); tk=_num(row.get('kurs'))   # v179.6
            tdata.append([P(row.get('sana',''),size=9,color=C_MUTED),
                P(amal_txt,'Helvetica-Bold',9,ac,'CENTER'),
                P('',size=9,color=C_MUTED),P('',size=9),
                P(f"{gsign}{abs(tg):,.2f}g",'Helvetica-Bold',9,gc,'RIGHT'),
                P(f"{tsum:,.0f}$" if tsum else "—",size=9,align='RIGHT'),
                P(f"{tk:,.1f}$/g" if tk else "—",size=9,color=C_MUTED,align='RIGHT'),
                P(f"{ostatka:,.2f}g",'Helvetica-Bold',9,oc,'RIGHT')])
        r1=len(tdata)-1
        rstyles.append(('BACKGROUND',(0,r0),(-1,r1),bg))
        if r1>r0:
            rstyles.append(('SPAN',(0,r0),(0,r1)))
            rstyles.append(('SPAN',(1,r0),(1,r1)))
            rstyles.append(('SPAN',(7,r0),(7,r1)))
        rstyles.append(('LINEBELOW',(0,r1),(-1,r1),0.4,colors.HexColor('#cccccc')))
        if len(tdata) - 1 >= _BOLAK:          # v179.9: guruh chegarasida bo'linadi
            _bolaklar.append((tdata, rstyles))
            tdata = [_sarlavha()]; rstyles = []
    jr=len(tdata)
    tdata.append([P('JAMI','Helvetica-Bold',9,C_WHITE,'CENTER'),'','','',
        P(f"-{jami_berildi:,.2f}g",'Helvetica-Bold',9,colors.HexColor('#E05A5A'),'RIGHT'),
        P(f"{jami_tolov_pul:,.0f}$",'Helvetica-Bold',9,colors.HexColor('#F6E05E'),'RIGHT'),'',
        P(qolgan_txt,'Helvetica-Bold',9,colors.HexColor('#E05A5A') if qolgan>0.001 else colors.HexColor('#68D391'),'RIGHT')])
    rstyles+=[('BACKGROUND',(0,jr),(-1,jr),C_DARK),('SPAN',(0,jr),(3,jr))]
    _bolaklar.append((tdata, rstyles))            # v179.9: oxirgi bo'lak — JAMI shu yerda
    for _td, _rs in _bolaklar:                    # v179.9
        _t = Table(_td, colWidths=CW, repeatRows=1)
        _t.setStyle(TableStyle(base_style() + _rs))
        story.append(_t)
    if qarz_tarkib:
        story.append(Spacer(1,6*mm)); story.append(sub_p("Joriy qarz tarkibi"))
        qd=[]
        for q in qarz_tarkib:
            qv=_num(q.get('qarz'))   # v179.6
            col=C_RED if qv>0.001 else (C_GREEN if qv<-0.001 else C_MUTED)
            sign="−" if qv>0 else ("+" if qv<0 else "")
            qd.append([P(q.get('zavod','')+' · '+q.get('tur',''),size=9),P(f"{sign}{abs(qv):,.2f}g",'Helvetica-Bold',9,col,'RIGHT')])
        qt=Table(qd,colWidths=[80*mm,40*mm])
        qt.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#dddddd')),('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[C_WHITE,C_GRAY])])); story.append(qt)
    # v172.39: ZAVOD·TUR BO'YICHA KUNLIK OSTATKA — yangi bo'lim.
    # Yuqoridagi jadval TEGILMAYDI, bu uning ostiga tushadi.
    ost = ost_bloklar or []
    if ost:
        story.append(Spacer(1, 6*mm))
        story.append(sub_p("Zavod·tur bo'yicha kunlik ostatka"))
        NUS = 5                                   # bir qatorga nechta blok
        kw = (W_total - (NUS - 1) * 3*mm) / NUS
        _kengaytirilgan = []                               # v179.11: baland bloklar bo'linadi
        for _ob in ost:
            _kengaytirilgan.extend(_ost_bolaklar(_ob, kw))
        for i in range(0, len(_kengaytirilgan), NUS):
            hujayra = list(_kengaytirilgan[i:i + NUS])
            while len(hujayra) < NUS:
                hujayra.append('')                # oxirgi qator to'lmasa - bo'sh
            qt2 = Table([hujayra], colWidths=[kw]*NUS)
            qt2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 3*mm),
                ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm)]))
            story.append(qt2)
    doc.build(story); return buf.getvalue()


def build_klientlar_tarix(ops, dan, gacha, jami_berildi, jami_vozvrat, jami_tolov_g, jami_tolov_pul, qarz_tarkib):
    jami_berildi = _num(jami_berildi); jami_vozvrat = _num(jami_vozvrat)      # v179.7
    jami_tolov_g = _num(jami_tolov_g); jami_tolov_pul = _num(jami_tolov_pul)  # v179.7
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4), leftMargin=8*mm, rightMargin=8*mm, topMargin=8*mm, bottomMargin=8*mm)
    story = []; W_total = landscape(A4)[0] - 16*mm
    story.append(title_p("TILLA HISOB — Klientlar tarixi")); story.append(sub_p(f"Davr: {davr_label(dan, gacha)}")); story.append(Spacer(1, 4*mm))
    qolgan = round(jami_berildi - jami_vozvrat - jami_tolov_g, 2)
    stat_data = [[P("JAMI BERILDI",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("VOZVRAT",'Helvetica-Bold',8,C_WHITE,'CENTER'),
                  P("TOLOV (PUL)",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("TOLOV (GRAMM)",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("QOLGAN QARZ",'Helvetica-Bold',8,C_WHITE,'CENTER')],
                 [P(f"-{jami_berildi:,.2f}g",'Helvetica-Bold',12,C_RED,'CENTER'),P(f"+{jami_vozvrat:,.2f}g",'Helvetica-Bold',12,C_GREEN,'CENTER'),
                  P(f"{jami_tolov_pul:,.0f}$",'Helvetica-Bold',12,C_GOLD,'CENTER'),P(f"+{jami_tolov_g:,.2f}g",'Helvetica-Bold',12,C_GREEN,'CENTER'),
                  P(f"-{qolgan:,.2f}g",'Helvetica-Bold',12,C_RED if qolgan>0 else C_GREEN,'CENTER')]]
    st=Table(stat_data,colWidths=[W_total/5]*5)
    st.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),C_HDR),('BACKGROUND',(0,1),(-1,1),colors.HexColor('#F8F6F0')),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#dddddd')),('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(st); story.append(Spacer(1,5*mm))
    HDR=["Sana","Klient","Amal","Zavod","Tur","Gramm","Summa ($)","Kurs ($/g)","Klient ostatka"]
    CW=[x*mm for x in [22,30,20,26,20,22,22,20,24]]
    tdata=[[P(h,'Helvetica-Bold',8,C_WHITE,'CENTER') for h in HDR]]; rstyles=[]
    for ri,row in enumerate(ops,1):
        tip=row.get('tip','')
        gramm=_num(row.get('gramm')); summa=_num(row.get('summa'))          # v179.7
        kurs=_num(row.get('kurs')); ostatka=_num(row.get('ostatka'))        # v179.7
        if tip=='berish': amal='↑ Berildi'; ac=C_RED; gc=C_RED; gs=f"{abs(gramm):,.2f}g"
        elif tip=='vozvrat': amal='↩ Vozvrat'; ac=C_BLUE; gc=C_GREEN; gs=f"+{abs(gramm):,.2f}g"
        else: amal='$ Tolov'; ac=C_BLUE; gc=C_GREEN; gs=f"+{abs(gramm):,.2f}g"
        oc=C_RED if ostatka<-0.001 else C_GREEN; bg=C_GRAY if ri%2==0 else C_WHITE
        tdata.append([P(row.get('sana',''),size=9,color=C_MUTED),P(row.get('klient_nom',''),'Helvetica-Bold',9),
            P(amal,'Helvetica-Bold',9,ac,'CENTER'),P(row.get('zavod',''),size=9,color=C_MUTED),P(row.get('tur',''),size=9,color=C_MUTED),
            P(gs,'Helvetica-Bold',9,gc,'RIGHT'),P(f"{summa:,.0f}$" if summa else "—",size=9,align='RIGHT'),
            P(f"{kurs:,.1f}$/g" if kurs else "—",size=9,color=C_MUTED,align='RIGHT'),P(f"{ostatka:,.2f}g",'Helvetica-Bold',9,oc,'RIGHT')])
        rstyles.append(('BACKGROUND',(0,ri),(-1,ri),bg))
    jr=len(tdata)
    tdata.append([P('JAMI','Helvetica-Bold',9,C_WHITE,'CENTER'),'','','','',
        P(f"-{jami_berildi:,.2f}g",'Helvetica-Bold',9,colors.HexColor('#E05A5A'),'RIGHT'),
        P(f"{jami_tolov_pul:,.0f}$",'Helvetica-Bold',9,colors.HexColor('#F6E05E'),'RIGHT'),'',
        P(f"-{qolgan:,.2f}g",'Helvetica-Bold',9,colors.HexColor('#E05A5A') if qolgan>0 else colors.HexColor('#68D391'),'RIGHT')])
    rstyles+=[('BACKGROUND',(0,jr),(-1,jr),C_DARK),('SPAN',(0,jr),(4,jr))]
    mt=Table(tdata,colWidths=CW,repeatRows=1); mt.setStyle(TableStyle(base_style()+rstyles)); story.append(mt)
    if qarz_tarkib:
        story.append(Spacer(1,6*mm)); story.append(sub_p("Joriy qarz tarkibi"))
        qd=[]
        for q in qarz_tarkib:
            qv=_num(q.get('qarz')); col=C_RED if qv>0.001 else (C_GREEN if qv<-0.001 else C_MUTED)   # v179.7
            sign="−" if qv>0 else ("+" if qv<0 else "")
            qd.append([P(q.get('klient_nom',''),size=9),P(f"{sign}{abs(qv):,.2f}g",'Helvetica-Bold',9,col,'RIGHT')])
        qt=Table(qd,colWidths=[60*mm,40*mm])
        qt.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#dddddd')),('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[C_WHITE,C_GRAY])])); story.append(qt)
    doc.build(story); return buf.getvalue()


def build_kassa(ops, dan, gacha, jami_summa, jami_gramm, label):
    jami_summa = _num(jami_summa); jami_gramm = _num(jami_gramm)   # v179.7
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=12*mm, bottomMargin=12*mm)
    story = []; W_total = A4[0] - 30*mm
    story.append(title_p("TILLA HISOB — Kassa hisoboti")); story.append(sub_p("Davr: " + label)); story.append(Spacer(1, 4*mm))
    stat_data = [[P("JAMI KASSA",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("JAMI GRAMM",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("TOLOVLAR SONI",'Helvetica-Bold',8,C_WHITE,'CENTER')],
                 [P(f"${jami_summa:,.2f}",'Helvetica-Bold',14,C_GOLD,'CENTER'),P(f"{jami_gramm:,.2f}g",'Helvetica-Bold',14,C_GREEN,'CENTER'),P(f"{len(ops)} ta",'Helvetica-Bold',14,C_DARK,'CENTER')]]
    st=Table(stat_data,colWidths=[W_total/3]*3)
    st.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),C_HDR),('BACKGROUND',(0,1),(-1,1),colors.HexColor('#F8F6F0')),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#dddddd')),('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(st); story.append(Spacer(1,6*mm))
    HDR=["Sana","Klient","Zavod","Tur","Gramm (g)","Kurs ($/g)","Summa ($)"]
    CW=[x*mm for x in [24,34,30,22,24,24,28]]
    tdata=[[P(h,'Helvetica-Bold',9,C_WHITE,'CENTER') for h in HDR]]; rstyles=[]
    for ri,op in enumerate(ops,1):
        bg=C_GRAY if ri%2==0 else C_WHITE
        tdata.append([P(op.get('sana',''),size=9,color=C_MUTED),P(op.get('klient',''),'Helvetica-Bold',9),
            P(op.get('zavod',''),size=9,color=C_MUTED),P(op.get('tur',''),size=9,color=C_MUTED),
            P(f"{_num(op.get('gramm')):,.2f}",size=9,align='RIGHT'),P(f"{_num(op.get('kurs')):,.1f}",size=9,color=C_MUTED,align='RIGHT'),
            P(f"${_num(op.get('summa')):,.2f}",'Helvetica-Bold',9,C_GOLD,'RIGHT')])   # v179.7
        rstyles.append(('BACKGROUND',(0,ri),(-1,ri),bg))
    jr=len(tdata)
    tdata.append([P('JAMI','Helvetica-Bold',9,C_WHITE,'CENTER'),'','','',
        P(f"{jami_gramm:,.2f}",'Helvetica-Bold',9,colors.HexColor('#68D391'),'RIGHT'),'',
        P(f"${jami_summa:,.2f}",'Helvetica-Bold',10,colors.HexColor('#F6E05E'),'RIGHT')])
    rstyles+=[('BACKGROUND',(0,jr),(-1,jr),C_DARK),('SPAN',(0,jr),(3,jr))]
    mt=Table(tdata,colWidths=CW,repeatRows=1); mt.setStyle(TableStyle(base_style()+rstyles)); story.append(mt)
    doc.build(story); return buf.getvalue()


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body   = json.loads(self.rfile.read(length))
            tip    = body.get("tip", "")

            if tip == "kurs_tarix":
                pdf = build_kurs_tarix(
                    body.get("sarlavha", "KURS TARIXI"),
                    body.get("davr", ""),
                    body.get("sana", ""),
                    body.get("kunlar", []))
                return self._send_pdf(pdf, "kurs-tarix.pdf")

            if tip == "klient_qarz_chek":
                pdf = build_klient_qarz_chek(body.get("klient_nom",""), body.get("sana",""),
                    body.get("jami_qarz",0), body.get("qarz_tarkib",[]),
                    body.get("biz_qarz",0)); return self._send_pdf(pdf, "qarz-chek.pdf")

            if tip == "klient_chek":
                pdf = build_klient_chek(body.get("klient_nom",""), body.get("ops_grouped",[]),
                    body.get("sana",""), body.get("qarz_tarkib")); return self._send_pdf(pdf, "chek.pdf")

            if tip == "klient_tarix":
                pdf = build_klient_tarix(body.get("klient_nom",""), body.get("klient_tel",""),
                    body.get("ops",[]), body.get("dan"), body.get("gacha"),
                    body.get("jami_berildi",0), body.get("jami_vozvrat",0),
                    body.get("jami_tolov_g",0), body.get("jami_tolov_pul",0),
                    body.get("qarz_tarkib",[]),
                    body.get("ost_bloklar",[]),
                    body.get("jami_qolgan"),
                    body.get("klient_ostatka"),
                    body.get("biz_qarz",0)); return self._send_pdf(pdf, "klient-hisobot.pdf")

            if tip == "klientlar_tarix":
                pdf = build_klientlar_tarix(body.get("ops",[]), body.get("dan"), body.get("gacha"),
                    body.get("jami_berildi",0), body.get("jami_vozvrat",0),
                    body.get("jami_tolov_g",0), body.get("jami_tolov_pul",0),
                    body.get("qarz_tarkib",[])); return self._send_pdf(pdf, "klientlar-tarix.pdf")

            if tip == "kassa":
                pdf = build_kassa(body.get("ops",[]), body.get("dan"), body.get("gacha"),
                    body.get("jami_summa",0), body.get("jami_gramm",0),
                    body.get("label","Hammasi")); return self._send_pdf(pdf, "kassa.pdf")

            zavodlar=body.get("zavodlar",[]); dan=body.get("dan"); gacha=body.get("gacha")
            filter_zavod=body.get("zavod"); label=davr_label(dan, gacha)
            pdf=build_pdf(zavodlar, filter_zavod, dan, gacha, label)
            self._send_pdf(pdf, "tilla-hisobot.pdf")

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type","application/json")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def _send_pdf(self, pdf_bytes, filename):
        self.send_response(200)
        self.send_header("Content-Type","application/pdf")
        self.send_header("Content-Disposition",f"inline; filename={filename}")
        self.send_header("Content-Length",str(len(pdf_bytes)))
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(pdf_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        pass
